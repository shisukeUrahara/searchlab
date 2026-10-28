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

SYSTEM = (
    "You judge search results. A passage is relevant only if it directly answers or states "
    "the information the query asks for. Reply with JSON {\"relevant\": [numbers]}."
)


class Judgment(BaseModel):
    query_id: str
    chunk_id: str
    relevant: bool
    source: str  # "seed" or "llm"


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
    raw = reply.get("relevant", [])
    picked = {int(i) for i in raw if isinstance(i, int | str) and str(i).isdigit()}
    extra: list[str] = []
    for i, c in enumerate(others, start=1):
        rel = i in picked
        judgments.append(Judgment(query_id=q.query_id, chunk_id=c.chunk_id, relevant=rel,
                                  source="llm"))
        if rel:
            extra.append(c.chunk_id)
    updated = q.model_copy(update={"gold_chunk_ids": (*q.gold_chunk_ids, *extra)})
    return updated, judgments
