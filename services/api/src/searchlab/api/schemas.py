from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from searchlab.domain.models import Method, Split

MethodName = Method


def _all_methods() -> list[MethodName]:
    return ["bm25", "dense", "hybrid"]


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    methods: list[MethodName] = Field(default_factory=_all_methods)
    top_k: int = Field(default=5, ge=1, le=20)


class HitOut(BaseModel):
    rank: int
    score: float
    chunk_id: str
    title: str
    heading: str
    snippet: str
    url: str
    source_id: str
    page: int | None = None


class MethodOut(BaseModel):
    method: MethodName
    latency_ms: float
    hits: list[HitOut]
    error: str | None = None


class SearchResponse(BaseModel):
    request_id: str
    query: str
    results: list[MethodOut]


class EvalRunRequest(BaseModel):
    split: Split = "dev"
    rrf_k: int = Field(default=60, ge=1, le=1000)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    chunk_count: int
    methods: list[str]
