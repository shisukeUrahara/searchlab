"""Use case: evaluate all methods on a split and persist a reproducible run folder."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from searchlab.domain.models import Split
from searchlab.domain.ports import Embedder
from searchlab.eval.artifacts import git_state, sha256_file, write_run
from searchlab.eval.naming import run_label
from searchlab.eval.queries import load_queries
from searchlab.eval.runner import CaseResult, ScoreRow, evaluate, summarize
from searchlab.wiring import load_chunks, make_retrievers


class DirtyTreeError(RuntimeError):
    """Holdout runs must come from a committed tree so the git SHA identifies the code."""


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
    corpus_label: str = "",
    allow_dirty: bool = False,
) -> EvalOutcome:
    """Pass runs_dir=None for a dry run (used when tuning on the dev split)."""
    git = git_state(repo_root) if repo_root else {}
    if runs_dir is not None and split == "test" and git.get("git_dirty") and not allow_dirty:
        raise DirtyTreeError("commit your changes before a holdout run (or pass allow_dirty)")
    chunks = load_chunks(corpus_dir)
    queries = load_queries(corpus_dir, split)
    retrievers = make_retrievers(chunks, embedder, rrf_k=rrf_k)
    results = evaluate(retrievers, queries)
    scores = summarize(results)
    now = datetime.now(UTC)
    run_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{split}-k{rrf_k}"
    run_dir = None
    if runs_dir is not None:
        created = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        manifest = {
            "run_id": run_id,
            "label": run_label(corpus_label, split, rrf_k, created),
            "created_at_utc": created,
            "split": split,
            "sample_count": len(queries),
            "methods": list(retrievers),
            "rrf_k": rrf_k,
            "embedding_model": embedder.model_id,
            "dataset_sha256": sha256_file(corpus_dir / f"queries.{split}.jsonl"),
            "corpus_manifest_sha256": sha256_file(corpus_dir / "source_manifest.json"),
            "chunks_sha256": sha256_file(corpus_dir / "chunks.jsonl"),
            "chunk_count": len(chunks),
            "metrics": {"recall_k": [1, 3, 5, 10], "mrr_k": 10, "ndcg_k": 10,
                        "ci": "95% percentile bootstrap over queries, 1000 draws, seed 0"},
            "repetitions": 1,
            "allow_dirty": allow_dirty,
            **git,
        }
        run_dir = runs_dir / run_id
        write_run(run_dir, results, scores, manifest)
    return EvalOutcome(run_id, run_dir, results, scores)
