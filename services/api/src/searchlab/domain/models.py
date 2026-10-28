"""Core value objects shared by every layer. No I/O here."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

QueryClass = Literal["exact_id", "paraphrase", "distractor"]
Split = Literal["dev", "test"]
Method = Literal["bm25", "dense", "hybrid"]


class Chunk(BaseModel):
    model_config = ConfigDict(frozen=True)

    chunk_id: str
    source_id: str
    title: str
    heading: str
    text: str
    url: str
    page: int | None = None  # first PDF page of the chunk, when known


class ScoredChunk(BaseModel):
    model_config = ConfigDict(frozen=True)

    chunk: Chunk
    score: float
    rank: int


class LabeledQuery(BaseModel):
    model_config = ConfigDict(frozen=True)

    query_id: str
    text: str
    query_class: QueryClass
    split: Split
    gold_chunk_ids: tuple[str, ...]
