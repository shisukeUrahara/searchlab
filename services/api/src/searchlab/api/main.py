"""Uvicorn entrypoint: `uvicorn searchlab.api.main:app`."""
from __future__ import annotations

import os

from searchlab.api.app import AppDeps, create_app
from searchlab.config import load_env
from searchlab.corpus.registry import REPO_ROOT, get_corpus
from searchlab.domain.models import Split
from searchlab.services.eval_service import EvalOutcome, run_eval
from searchlab.services.search_service import SearchService
from searchlab.wiring import load_chunks, make_embedder, make_retrievers


def build() -> object:
    load_env(REPO_ROOT / "services" / "api" / ".env")
    spec = get_corpus()
    corpus_dir, runs_dir = spec.dir, spec.runs_dir
    embedder = make_embedder(corpus_dir)
    chunks = load_chunks(corpus_dir)
    retrievers = make_retrievers(chunks, embedder, qdrant_url=os.environ.get("QDRANT_URL"))
    search = SearchService(retrievers, chunks)

    def eval_fn(split: Split, rrf_k: int) -> EvalOutcome:
        return run_eval(corpus_dir, embedder, split, rrf_k, runs_dir=runs_dir, repo_root=REPO_ROOT)

    origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
    return create_app(AppDeps(search, corpus_dir, runs_dir, eval_fn), origins)


app = build()
