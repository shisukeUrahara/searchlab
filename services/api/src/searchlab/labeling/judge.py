"""Pooled relevance judging: every method's top-k for a query goes to one LLM judgment.

The seed chunk the query was drafted from always stays gold. Extra chunks the judge marks
relevant are added, so methods are not penalised for finding a different correct passage.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from searchlab.domain.models import Chunk, LabeledQuery
from searchlab.domain.ports import Retriever
from searchlab.labeling.llm import JsonLlm

POOL_DEPTH = 10
SNIPPET = 700

JUDGE_MODEL = "gpt-4.1-2025-04-14"
SYSTEM = (
    "You are a strict relevance judge for a search benchmark over NASA handbooks. "
    "Grade each numbered passage for the query:\n"
    "2 = the passage itself states the specific answer or the exact item the query names "
    "(for an identifier query, the passage must contain that identifier and say what it is "
    "or requires);\n"
    "1 = same general topic but does not answer;\n"
    "0 = unrelated.\n"
    "Most passages should be 0 or 1. Reply with JSON {\"grades\": {\"<number>\": 0|1|2}}."
)


class Judgment(BaseModel):
    query_id: str
    chunk_id: str
    relevant: bool
    source: str  # "seed" or "llm"
    grade: int | None = None  # LLM grade 0-2; None for the seed chunk


def pool(query: str, retrievers: Mapping[str, Retriever], depth: int = POOL_DEPTH) -> list[Chunk]:
    seen: dict[str, Chunk] = {}
    for r in retrievers.values():
        for hit in r.search(query, depth):
            seen.setdefault(hit.chunk.chunk_id, hit.chunk)
    return list(seen.values())


def judge_query(
    q: LabeledQuery, candidates: Sequence[Chunk], llm: JsonLlm
) -> tuple[LabeledQuery, list[Judgment]]:
    seed = set(q.gold_chunk_ids)
    others = [c for c in candidates if c.chunk_id not in seed]
    judgments = [Judgment(query_id=q.query_id, chunk_id=c, relevant=True, source="seed")
                 for c in q.gold_chunk_ids]
    if not others:
        return q, judgments
    listing = "\n\n".join(
        f"[{i}] {c.heading}\n{c.text[:SNIPPET]}" for i, c in enumerate(others, start=1)
    )
    reply = llm.complete_json(SYSTEM, f"Query: {q.text}\n\nPassages:\n{listing}")
    grades = _grades(reply.get("grades"))
    extra: list[str] = []
    for i, c in enumerate(others, start=1):
        grade = grades.get(i, 0)
        rel = grade == 2
        judgments.append(Judgment(query_id=q.query_id, chunk_id=c.chunk_id, relevant=rel,
                                  source="llm", grade=grade))
        if rel:
            extra.append(c.chunk_id)
    updated = q.model_copy(update={"gold_chunk_ids": (*q.gold_chunk_ids, *extra)})
    return updated, judgments


def _grades(raw: object) -> dict[int, int]:
    """Parse {"1": 2, "2": 0} defensively; anything malformed counts as 0."""
    if not isinstance(raw, dict):
        return {}
    out: dict[int, int] = {}
    for k, v in raw.items():
        if str(k).isdigit() and v in (0, 1, 2):
            out[int(k)] = int(v)
    return out
