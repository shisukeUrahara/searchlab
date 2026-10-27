from __future__ import annotations

import json
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from searchlab.api.errors import ApiError, install_error_handlers
from searchlab.api.schemas import (
    EvalRunRequest,
    HealthResponse,
    HitOut,
    MethodOut,
    SearchRequest,
    SearchResponse,
)
from searchlab.corpus.manifest import read_manifest
from searchlab.domain.models import Split
from searchlab.eval.queries import load_queries
from searchlab.services.eval_service import EvalOutcome
from searchlab.services.search_service import SearchService

EvalFn = Callable[[Split, int], EvalOutcome]
SNIPPET = 320


@dataclass(frozen=True)
class AppDeps:
    search: SearchService
    corpus_dir: Path
    runs_dir: Path
    run_eval: EvalFn


def create_app(deps: AppDeps, cors_origins: list[str] | None = None) -> FastAPI:
    app = FastAPI(title="SearchLab API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware, allow_origins=cors_origins or [], allow_methods=["*"], allow_headers=["*"]
    )
    install_error_handlers(app)

    @app.middleware("http")
    async def request_id(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request.state.request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
        response = await call_next(request)
        response.headers["x-request-id"] = request.state.request_id
        return response

    @app.get("/health")
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok", chunk_count=deps.search.chunk_count, methods=deps.search.methods
        )

    @app.get("/sources")
    def sources() -> dict[str, Any]:
        return read_manifest(deps.corpus_dir / "source_manifest.json").model_dump()

    @app.get("/chunks/{chunk_id}")
    def chunk(chunk_id: str) -> dict[str, Any]:
        c = deps.search.chunk(chunk_id)
        if c is None:
            raise ApiError(404, "chunk_not_found", f"no chunk {chunk_id}")
        return c.model_dump()

    @app.post("/search")
    def search(req: SearchRequest, request: Request) -> SearchResponse:
        results = deps.search.search(req.query, req.methods, req.top_k)
        return SearchResponse(
            request_id=request.state.request_id,
            query=req.query,
            results=[
                MethodOut(
                    method=r.method,
                    latency_ms=round(r.latency_ms, 2),
                    hits=[
                        HitOut(
                            rank=h.rank,
                            score=h.score,
                            chunk_id=h.chunk.chunk_id,
                            title=h.chunk.title,
                            heading=h.chunk.heading,
                            snippet=h.chunk.text[:SNIPPET],
                            url=h.chunk.url,
                        )
                        for h in r.hits
                    ],
                )
                for r in results
            ],
        )

    @app.get("/queries")
    def queries(split: Split = "dev") -> list[dict[str, Any]]:
        return [q.model_dump() for q in load_queries(deps.corpus_dir, split)]

    @app.post("/eval-runs")
    def create_eval_run(req: EvalRunRequest) -> dict[str, Any]:
        outcome = deps.run_eval(req.split, req.rrf_k)
        return {"run_id": outcome.run_id}

    @app.get("/eval-runs")
    def list_eval_runs() -> list[str]:
        if not deps.runs_dir.exists():
            return []
        return sorted((p.name for p in deps.runs_dir.iterdir() if p.is_dir()), reverse=True)

    @app.get("/eval-runs/{run_id}")
    def get_eval_run(run_id: str) -> dict[str, Any]:
        run_dir = deps.runs_dir / run_id
        if "/" in run_id or ".." in run_id or not run_dir.is_dir():
            raise ApiError(404, "run_not_found", f"no run {run_id}")
        cases = [
            json.loads(line)
            for line in (run_dir / "per_case_results.jsonl").read_text().splitlines()
        ]
        return {
            "manifest": json.loads((run_dir / "run_manifest.json").read_text()),
            "scores": json.loads((run_dir / "scores.json").read_text()),
            "cases": cases,
        }

    return app

