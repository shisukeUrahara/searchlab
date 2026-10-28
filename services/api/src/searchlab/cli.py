"""Thin command layer: parse args, call pipeline functions, print results."""
from __future__ import annotations

import httpx
import typer

from searchlab.config import load_env
from searchlab.corpus import pipeline
from searchlab.corpus.manifest import verify_manifest, write_manifest
from searchlab.corpus.registry import REPO_ROOT, CorpusSpec, get_corpus
from searchlab.domain.models import Split
from searchlab.embeddings.cache import CacheMissError
from searchlab.eval.runner import ScoreRow
from searchlab.services.eval_service import run_eval
from searchlab.wiring import load_chunks, make_embedder, make_retrievers

app = typer.Typer(no_args_is_help=True)

load_env(REPO_ROOT / "services" / "api" / ".env")
_state: dict[str, CorpusSpec] = {}


@app.callback()
def main(
    corpus: str = typer.Option(None, help="Corpus name (default: $SEARCHLAB_CORPUS)"),
) -> None:
    """SearchLab command line."""
    _state["corpus"] = get_corpus(corpus)


def _corpus() -> CorpusSpec:
    return _state.get("corpus") or get_corpus()


def _http_get(url: str) -> bytes:
    r = httpx.get(url, follow_redirects=True, timeout=30)
    r.raise_for_status()
    return r.content


@app.command()
def fetch() -> None:
    """Download the pinned docs and write source_manifest.json."""
    spec = _corpus()
    manifest = spec.fetch(_http_get, spec.snapshot_dir)
    write_manifest(manifest, pipeline.manifest_path(spec.dir))
    typer.echo(f"fetched {len(manifest.sources)} files")


@app.command()
def chunk() -> None:
    """Clean and chunk the snapshot into chunks.jsonl."""
    spec = _corpus()
    manifest = pipeline.load_manifest(spec.dir)
    problems = verify_manifest(manifest, spec.snapshot_dir)
    if problems:
        raise typer.Exit(code=_fail(problems))
    chunks = spec.build_chunks(manifest, spec.snapshot_dir)
    pipeline.write_chunks(chunks, spec.dir / "chunks.jsonl")
    typer.echo(f"wrote {len(chunks)} chunks")


@app.command()
def verify() -> None:
    """Check snapshot files against manifest checksums."""
    spec = _corpus()
    problems = verify_manifest(pipeline.load_manifest(spec.dir), spec.snapshot_dir)
    if problems:
        raise typer.Exit(code=_fail(problems))
    typer.echo(f"{spec.name}: manifest ok")


def _fail(problems: list[str]) -> int:
    for p in problems:
        typer.echo(p, err=True)
    return 1


def _print_scores(scores: list[ScoreRow]) -> None:
    head = f"{'method':8} {'class':11} {'n':>3} {'R@1':>6} {'R@5':>6} {'MRR@10':>7}  95% CI"
    typer.echo(head)
    for r in scores:
        ci = f"[{r.mrr_ci[0]:.3f}, {r.mrr_ci[1]:.3f}]" if r.mrr_ci else ""
        typer.echo(f"{r.method:8} {r.query_class:11} {r.n:>3} {r.recall_at_1:>6.3f} "
                   f"{r.recall_at_5:>6.3f} {r.mrr_at_10:>7.3f}  {ci}")


@app.command()
def embed() -> None:
    """Embed every chunk (cache first) so search and eval work offline."""
    from searchlab.retrieval.dense import chunk_embedding_text

    spec = _corpus()
    chunks = load_chunks(spec.dir)
    embedder = make_embedder(spec.dir)
    embedder.embed([chunk_embedding_text(c) for c in chunks])
    typer.echo(f"{spec.name}: {len(chunks)} chunks embedded with {embedder.model_id}")


@app.command()
def search(query: str, top_k: int = 5) -> None:
    """Run one query through all three methods."""
    spec = _corpus()
    retrievers = make_retrievers(load_chunks(spec.dir), make_embedder(spec.dir))
    for name, retriever in retrievers.items():
        typer.echo(f"\n== {name}")
        try:
            hits = retriever.search(query, top_k)
        except CacheMissError:
            typer.echo("query not in embedding cache and OPENAI_API_KEY is not set", err=True)
            continue
        for h in hits:
            typer.echo(f"{h.rank}. {h.score:.3f}  {h.chunk.heading[:60]}  [{h.chunk.chunk_id[:8]}]")


@app.command()
def tune(ks: str = "10,30,60,100") -> None:
    """Compare RRF k values on the DEV split only. Never touches the test split."""
    spec = _corpus()
    embedder = make_embedder(spec.dir)
    for k in (int(x) for x in ks.split(",")):
        outcome = run_eval(spec.dir, embedder, "dev", rrf_k=k)
        row = next(r for r in outcome.scores if r.method == "hybrid" and r.query_class == "all")
        typer.echo(f"rrf_k={k:<4} recall@5={row.recall_at_5:.3f} mrr@10={row.mrr_at_10:.3f}")


@app.command(name="eval")
def eval_cmd(split: Split = "dev", rrf_k: int = 60) -> None:
    """Evaluate all methods and write runs/<run_id>/."""
    spec = _corpus()
    outcome = run_eval(
        spec.dir, make_embedder(spec.dir), split, rrf_k, runs_dir=spec.runs_dir, repo_root=REPO_ROOT
    )
    _print_scores(outcome.scores)
    typer.echo(f"\nrun written to {outcome.run_dir}")
