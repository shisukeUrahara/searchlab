"""Uvicorn entrypoint: `uvicorn searchlab.api.main:app`."""
from __future__ import annotations

import os
from pathlib import Path

from searchlab.api.app import AppDeps, create_app
from searchlab.config import load_env
from searchlab.domain.models import Split
from searchlab.services.eval_service import EvalOutcome, run_eval
from searchlab.services.search_service import SearchService
from searchlab.wiring import load_chunks, make_embedder, make_retrievers

REPO_ROOT = Path(__file__).resolve().parents[5]
CORPUS_DIR = REPO_ROOT / "fixtures" / "github-docs"
RUNS_DIR = REPO_ROOT / "runs" / "github-docs"


def build() -> object:
    load_env(REPO_ROOT / "services" / "api" / ".env")
    embedder = make_embedder(CORPUS_DIR)
    chunks = load_chunks(CORPUS_DIR)
    retrievers = make_retrievers(chunks, embedder, qdrant_url=os.environ.get("QDRANT_URL"))
    search = SearchService(retrievers, chunks)

    def eval_fn(split: Split, rrf_k: int) -> EvalOutcome:
        return run_eval(CORPUS_DIR, embedder, split, rrf_k, runs_dir=RUNS_DIR, repo_root=REPO_ROOT)

    origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
    return create_app(AppDeps(search, CORPUS_DIR, RUNS_DIR, eval_fn), origins)


app = build()
