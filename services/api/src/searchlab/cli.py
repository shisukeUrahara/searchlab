"""Thin command layer: parse args, call pipeline functions, print results."""
from __future__ import annotations

from pathlib import Path

import httpx
import typer

from searchlab.config import load_env
from searchlab.corpus import pipeline
from searchlab.corpus.manifest import verify_manifest, write_manifest
from searchlab.corpus.registry import REPO_ROOT, CorpusSpec, get_corpus
from searchlab.domain.models import LabeledQuery, QueryClass, Split
from searchlab.embeddings.cache import CacheMissError
from searchlab.eval.runner import ScoreRow
from searchlab.labeling.llm import JsonLlm
from searchlab.services.eval_service import DirtyTreeError, run_eval
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
def eval_cmd(split: Split = "dev", rrf_k: int = 60, allow_dirty: bool = False) -> None:
    """Evaluate all methods and write runs/<corpus>/<run_id>/. Holdout needs a clean tree."""
    spec = _corpus()
    try:
        outcome = run_eval(spec.dir, make_embedder(spec.dir), split, rrf_k, runs_dir=spec.runs_dir,
                           repo_root=REPO_ROOT, corpus_label=spec.label, allow_dirty=allow_dirty)
    except DirtyTreeError as exc:
        raise typer.BadParameter(str(exc)) from exc
    _print_scores(outcome.scores)
    typer.echo(f"\nrun written to {outcome.run_dir}")


def _llm(model_id: str | None = None) -> JsonLlm:
    import os

    from openai import OpenAI

    from searchlab.labeling.llm import OpenAIJsonLlm

    if not os.environ.get("OPENAI_API_KEY"):
        raise typer.BadParameter("OPENAI_API_KEY is required for labeling")
    return OpenAIJsonLlm(OpenAI(), model_id) if model_id else OpenAIJsonLlm(OpenAI())


def _write_queries(path: Path, queries: list[LabeledQuery]) -> None:
    path.write_text("".join(q.model_dump_json() + "\n" for q in queries))


def _read_queries(path: Path) -> list[LabeledQuery]:
    return [LabeledQuery.model_validate_json(x) for x in path.read_text().splitlines() if x]


@app.command(name="draft-queries")
def draft_queries_cmd(exact: int = 40, paraphrase: int = 50, distractor: int = 30,
                      seed: int = 13) -> None:
    """Draft labeled queries with an LLM into queries.draft.jsonl (one seed gold chunk each)."""
    from searchlab.labeling.draft import draft_queries

    spec = _corpus()
    llm = _llm()
    counts: dict[QueryClass, int] = {"exact_id": exact, "paraphrase": paraphrase,
                                     "distractor": distractor}
    queries = draft_queries(load_chunks(spec.dir), llm, counts, seed=seed)
    _write_queries(spec.dir / "queries.draft.jsonl", queries)
    typer.echo(f"drafted {len(queries)} queries with {llm.model_id}")


@app.command(name="judge-pool")
def judge_pool_cmd(depth: int = 10, model: str = "") -> None:
    """Pool every method's top-k per draft query, LLM-judge relevance, write dev/test splits."""
    from searchlab.labeling.judge import JUDGE_MODEL, judge_query, pool

    spec = _corpus()
    llm = _llm(model or JUDGE_MODEL)
    chunks = load_chunks(spec.dir)
    retrievers = make_retrievers(chunks, make_embedder(spec.dir))
    judged: list[LabeledQuery] = []
    lines: list[str] = []
    for q in _read_queries(spec.dir / "queries.draft.jsonl"):
        updated, judgments = judge_query(q, pool(q.text, retrievers, depth), llm)
        judged.append(updated)
        lines += [j.model_dump_json() for j in judgments]
    (spec.dir / "judgments.jsonl").write_text("\n".join(lines) + "\n")
    for split in ("dev", "test"):
        _write_queries(spec.dir / f"queries.{split}.jsonl", [q for q in judged if q.split == split])
    extra = sum(len(q.gold_chunk_ids) - 1 for q in judged)
    typer.echo(f"judged {len(judged)} queries with {llm.model_id}, {extra} extra relevant chunks")


@app.command(name="review-sheet")
def review_sheet_cmd(n: int = 25, seed: int = 7) -> None:
    """Write docs/label_review.md with n random queries for a human spot-check."""
    from searchlab.labeling.review import pick_for_review, render_sheet

    spec = _corpus()
    queries = [q for s in ("dev", "test") for q in _read_queries(spec.dir / f"queries.{s}.jsonl")]
    chunks = {c.chunk_id: c for c in load_chunks(spec.dir)}
    out = REPO_ROOT / "docs" / "label_review.md"
    out.write_text(render_sheet(pick_for_review(queries, n, seed), chunks))
    typer.echo(f"wrote {out}")


@app.command(name="apply-review")
def apply_review_cmd() -> None:
    """Read ticked boxes from docs/label_review.md, report agreement, drop wrong labels."""
    from searchlab.labeling.review import apply_review, parse_sheet

    spec = _corpus()
    result = parse_sheet((REPO_ROOT / "docs" / "label_review.md").read_text())
    for split in ("dev", "test"):
        path = spec.dir / f"queries.{split}.jsonl"
        _write_queries(path, apply_review(_read_queries(path), result.wrong))
    typer.echo(f"checked {result.checked} labels, {len(result.wrong)} wrong, "
               f"agreement {result.agreement:.3f}")
