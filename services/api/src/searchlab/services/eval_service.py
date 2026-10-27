"""Use case: evaluate all methods on a split and persist a reproducible run folder."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from searchlab.domain.models import Split
from searchlab.domain.ports import Embedder
from searchlab.eval.artifacts import git_state, sha256_file, write_run
from searchlab.eval.queries import load_queries
from searchlab.eval.runner import CaseResult, ScoreRow, evaluate, summarize
from searchlab.wiring import load_chunks, make_retrievers


@dataclass(frozen=True)
class EvalOutcome:
    run_id: str
    run_dir: Path | None
    results: list[CaseResult]
    scores: list[ScoreRow]


def run_eval(
    corpus_dir: Path,
    embedder: Embedder,
    split: Split,
    rrf_k: int = 60,
    runs_dir: Path | None = None,
    repo_root: Path | None = None,
) -> EvalOutcome:
    """Pass runs_dir=None for a dry run (used when tuning on the dev split)."""
    chunks = load_chunks(corpus_dir)
    queries = load_queries(corpus_dir, split)
    retrievers = make_retrievers(chunks, embedder, rrf_k=rrf_k)
    results = evaluate(retrievers, queries)
    scores = summarize(results)
    now = datetime.now(UTC)
    run_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{split}-k{rrf_k}"
    run_dir = None
    if runs_dir is not None:
        manifest = {
            "run_id": run_id,
            "created_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": split,
            "sample_count": len(queries),
            "methods": list(retrievers),
            "rrf_k": rrf_k,
            "embedding_model": embedder.model_id,
            "dataset_sha256": sha256_file(corpus_dir / f"queries.{split}.jsonl"),
            "corpus_manifest_sha256": sha256_file(corpus_dir / "source_manifest.json"),
            "chunks_sha256": sha256_file(corpus_dir / "chunks.jsonl"),
            "chunk_count": len(chunks),
            "metrics": {"recall_k": 5, "mrr_k": 10},
            "repetitions": 1,
            **(git_state(repo_root) if repo_root else {}),
        }
        run_dir = runs_dir / run_id
        write_run(run_dir, results, scores, manifest)
    return EvalOutcome(run_id, run_dir, results, scores)
