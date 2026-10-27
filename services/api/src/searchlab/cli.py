"""Thin command layer: parse args, call pipeline functions, print results."""
from __future__ import annotations

from pathlib import Path

import httpx
import typer

from searchlab.config import load_env
from searchlab.corpus import pipeline
from searchlab.corpus.manifest import verify_manifest, write_manifest
from searchlab.domain.models import Split
from searchlab.eval.runner import ScoreRow
from searchlab.services.eval_service import run_eval
from searchlab.wiring import load_chunks, make_embedder, make_retrievers

app = typer.Typer(no_args_is_help=True)

REPO_ROOT = Path(__file__).resolve().parents[4]
CORPUS_DIR = REPO_ROOT / "fixtures" / "github-docs"
RUNS_DIR = REPO_ROOT / "runs"
load_env(REPO_ROOT / "services" / "api" / ".env")


def _http_get(url: str) -> bytes:
    r = httpx.get(url, follow_redirects=True, timeout=30)
    r.raise_for_status()
    return r.content


@app.command()
def fetch() -> None:
    """Download the pinned docs and write source_manifest.json."""
    manifest = pipeline.fetch_snapshot(_http_get, CORPUS_DIR / "snapshot")
    write_manifest(manifest, pipeline.manifest_path(CORPUS_DIR))
    typer.echo(f"fetched {len(manifest.sources)} files")


@app.command()
def chunk() -> None:
    """Clean and chunk the snapshot into chunks.jsonl."""
    manifest = pipeline.load_manifest(CORPUS_DIR)
    problems = verify_manifest(manifest, CORPUS_DIR / "snapshot")
    if problems:
        raise typer.Exit(code=_fail(problems))
    chunks = pipeline.build_chunks(manifest, CORPUS_DIR / "snapshot")
    pipeline.write_chunks(chunks, CORPUS_DIR / "chunks.jsonl")
    typer.echo(f"wrote {len(chunks)} chunks")


@app.command()
def verify() -> None:
    """Check snapshot files against manifest checksums."""
    manifest = pipeline.load_manifest(CORPUS_DIR)
    problems = verify_manifest(manifest, CORPUS_DIR / "snapshot")
    if problems:
        raise typer.Exit(code=_fail(problems))
    typer.echo("manifest ok")


def _fail(problems: list[str]) -> int:
    for p in problems:
        typer.echo(p, err=True)
    return 1


def _print_scores(scores: list[ScoreRow]) -> None:
    typer.echo(f"{'method':8} {'class':11} {'n':>3} {'recall@5':>9} {'mrr@10':>7}")
    for r in scores:
        line = f"{r.method:8} {r.query_class:11} {r.n:>3} {r.recall_at_5:>9.3f} {r.mrr_at_10:>7.3f}"
        typer.echo(line)


@app.command()
def search(query: str, top_k: int = 5) -> None:
    """Run one query through all three methods."""
    retrievers = make_retrievers(load_chunks(CORPUS_DIR), make_embedder(CORPUS_DIR))
    for name, retriever in retrievers.items():
        typer.echo(f"\n== {name}")
        for h in retriever.search(query, top_k):
            typer.echo(f"{h.rank}. {h.score:.3f}  {h.chunk.heading[:60]}  [{h.chunk.chunk_id[:8]}]")


@app.command()
def tune(ks: str = "10,30,60,100") -> None:
    """Compare RRF k values on the DEV split only. Never touches the test split."""
    embedder = make_embedder(CORPUS_DIR)
    for k in (int(x) for x in ks.split(",")):
        outcome = run_eval(CORPUS_DIR, embedder, "dev", rrf_k=k)
        row = next(r for r in outcome.scores if r.method == "hybrid" and r.query_class == "all")
        typer.echo(f"rrf_k={k:<4} recall@5={row.recall_at_5:.3f} mrr@10={row.mrr_at_10:.3f}")


@app.command(name="eval")
def eval_cmd(split: Split = "dev", rrf_k: int = 60) -> None:
    """Evaluate all methods and write runs/<run_id>/."""
    outcome = run_eval(
        CORPUS_DIR, make_embedder(CORPUS_DIR), split, rrf_k, runs_dir=RUNS_DIR, repo_root=REPO_ROOT
    )
    _print_scores(outcome.scores)
    typer.echo(f"\nrun written to {outcome.run_dir}")
