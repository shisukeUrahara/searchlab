from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query, Request, Response
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
from searchlab.domain.models import QueryClass, Split
from searchlab.eval.naming import SPLIT_LABEL
from searchlab.eval.queries import load_queries, page_queries
from searchlab.services.eval_service import DirtyTreeError, EvalOutcome
from searchlab.services.run_report import RunNotFoundError, list_runs, load_run
from searchlab.services.search_service import SearchService

EvalFn = Callable[[Split, int], EvalOutcome]
SNIPPET = 320


@dataclass(frozen=True)
class AppDeps:
    search: SearchService
    corpus_dir: Path
    runs_dir: Path
    run_eval: EvalFn
    corpus_label: str = ""
    graph_path: Path | None = None
    embedding_model: str = ""
    embedding_dims: int = 0


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
                    error=r.error,
                    hits=[
                        HitOut(
                            rank=h.rank,
                            score=h.score,
                            chunk_id=h.chunk.chunk_id,
                            title=h.chunk.title,
                            heading=h.chunk.heading,
                            snippet=h.chunk.text[:SNIPPET],
                            url=h.chunk.url,
                            source_id=h.chunk.source_id,
                            page=h.chunk.page,
                        )
                        for h in r.hits
                    ],
                )
                for r in results
            ],
        )

    @app.get("/corpus")
    def corpus() -> dict[str, Any]:
        manifest = read_manifest(deps.corpus_dir / "source_manifest.json")
        counts = deps.search.chunk_counts_by_source()
        titles = deps.search.titles_by_source()
        return {
            "label": deps.corpus_label,
            "chunk_count": deps.search.chunk_count,
            "embedding_model": deps.embedding_model,
            "embedding_dims": deps.embedding_dims,
            "docs": [
                {"source_id": s.source_id, "doc_number": s.doc_number, "url": s.url,
                 "title": titles.get(s.source_id, s.source_id), "pages": s.pages,
                 "chunks": counts.get(s.source_id, 0), "retrieved_at_utc": s.retrieved_at_utc,
                 "sha256": s.sha256, "license": s.license, "transformation": s.transformation}
                for s in manifest.sources
            ],
        }

    @app.get("/queries")
    def queries(
        split: Split = "dev",
        limit: int = Query(15, ge=1, le=200),
        offset: int = Query(0, ge=0),
        query_class: QueryClass | None = None,
        q: str | None = Query(None, max_length=200),
    ) -> dict[str, Any]:
        all_queries = load_queries(deps.corpus_dir, split)
        page, total = page_queries(all_queries, limit, offset, query_class, q)
        class_counts: dict[str, int] = {}
        for x in all_queries:
            class_counts[x.query_class] = class_counts.get(x.query_class, 0) + 1

        def sources(ids: tuple[str, ...]) -> list[str]:
            found = (deps.search.chunk(i) for i in ids)
            return list(dict.fromkeys(c.source_id for c in found if c))

        items = [{**x.model_dump(), "gold_sources": sources(x.gold_chunk_ids)} for x in page]
        return {"items": items, "total": total, "limit": limit, "offset": offset,
                "split_label": SPLIT_LABEL[split], "split_total": len(all_queries),
                "class_counts": class_counts}

    @app.post("/eval-runs")
    def create_eval_run(req: EvalRunRequest) -> dict[str, Any]:
        try:
            outcome = deps.run_eval(req.split, req.rrf_k)
        except DirtyTreeError as exc:
            raise ApiError(409, "dirty_tree", str(exc)) from exc
        return {"run_id": outcome.run_id}

    @app.get("/eval-runs")
    def list_eval_runs() -> list[dict[str, Any]]:
        return list_runs(deps.runs_dir)

    @app.get("/eval-runs/{run_id}")
    def get_eval_run(run_id: str) -> dict[str, Any]:
        try:
            return load_run(deps.runs_dir, run_id)
        except RunNotFoundError as exc:
            raise ApiError(404, "run_not_found", f"no run {run_id}") from exc

    @app.get("/graph")
    def graph() -> Response:
        if deps.graph_path is None or not deps.graph_path.exists():
            raise ApiError(404, "graph_not_built", "run `searchlab project` to build the map")
        return Response(deps.graph_path.read_bytes(), media_type="application/json")

    return app

