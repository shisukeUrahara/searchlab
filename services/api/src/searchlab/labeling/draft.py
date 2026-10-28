"""Draft labeled queries from sampled chunks, one LLM call per query.

Classes:
- exact_id: must contain an identifier that appears in the chunk (NPR 7123.1, KDP C, SWE-139, TRL)
- paraphrase: natural question that avoids the chunk's rarest words
- distractor: question built to look like a neighboring section's topic but answered here
"""
from __future__ import annotations

import math
import random
import re
from collections import Counter
from collections.abc import Sequence

from searchlab.domain.models import Chunk, LabeledQuery, QueryClass, Split
from searchlab.labeling.llm import JsonLlm
from searchlab.retrieval.tokenize import tokenize

_IDENT = re.compile(
    r"\b(?:NPR|NPD|NASA-STD|NASA-HDBK)\s?\d{4}(?:\.\d+[A-Z]?)?\b"
    r"|\bSWE-\d{3}\b|\bKDP[ -][A-F0-9I]{1,3}\b|\bTRL\s?\d\b|\b[A-Z]{3,6}\b"
)
_NOT_IDS = {"NASA", "THE", "AND", "FOR", "NOTE", "WITH", "SHALL", "TABLE", "FIGURE", "THIS"}
MIN_TEXT = 300

SYSTEM = (
    "You write search queries for evaluating a retrieval system over NASA program and "
    "systems-engineering handbooks. Reply with JSON {\"query\": \"...\"} only."
)


def identifiers(text: str) -> list[str]:
    found = [m.group(0) for m in _IDENT.finditer(text)]
    return [f for f in dict.fromkeys(found) if f not in _NOT_IDS]


def rare_words(chunk: Chunk, df: Counter[str], n_docs: int, k: int = 6) -> list[str]:
    toks = {t for t in tokenize(chunk.text) if len(t) > 3 and t.isalpha()}
    return sorted(toks, key=lambda t: -math.log(n_docs / (1 + df[t])))[:k]


def doc_frequencies(chunks: Sequence[Chunk]) -> Counter[str]:
    df: Counter[str] = Counter()
    for c in chunks:
        df.update(set(tokenize(c.text)))
    return df


def _round_robin(by_doc: dict[str, list[Chunk]], n: int, rng: random.Random) -> list[Chunk]:
    pools = {k: rng.sample(v, len(v)) for k, v in sorted(by_doc.items())}
    out: list[Chunk] = []
    while len(out) < n and any(pools.values()):
        for pool in pools.values():
            if pool and len(out) < n:
                out.append(pool.pop())
    return out


def sample_chunks(
    chunks: Sequence[Chunk], counts: dict[QueryClass, int], seed: int
) -> list[tuple[QueryClass, Chunk]]:
    """Spread picks evenly across documents; no chunk is used twice."""
    rng = random.Random(seed)
    usable = [c for c in chunks if len(c.text) >= MIN_TEXT]
    picked: list[tuple[QueryClass, Chunk]] = []
    used: set[str] = set()
    for cls, n in counts.items():
        pool = [
            c for c in usable
            if c.chunk_id not in used and (cls != "exact_id" or identifiers(c.text))
        ]
        by_doc: dict[str, list[Chunk]] = {}
        for c in pool:
            by_doc.setdefault(c.source_id, []).append(c)
        for c in _round_robin(by_doc, n, rng):
            used.add(c.chunk_id)
            picked.append((cls, c))
    return picked


def build_prompt(cls: QueryClass, chunk: Chunk, rare: list[str], neighbor: str) -> str:
    passage = f"Section: {chunk.heading}\nPassage:\n{chunk.text}"
    if cls == "exact_id":
        ident = identifiers(chunk.text)[0]
        task = (f"Write a short query (2-8 words) an engineer would type that contains the exact "
                f"identifier '{ident}' and that this passage answers.")
    elif cls == "paraphrase":
        task = ("Write one natural question (8-20 words) that this passage answers. Do NOT use "
                f"any of these words: {', '.join(rare)}. Use everyday synonyms instead.")
    else:
        task = (f"Write one question (8-20 words) that sounds like it is about '{neighbor}' but is "
                "actually answered by this passage, not by that section.")
    return f"{passage}\n\nTask: {task}"


def assign_splits(n: int, tuning_share: float, seed: int) -> list[Split]:
    n_tuning = round(n * tuning_share)
    dev: list[Split] = ["dev"] * n_tuning
    test: list[Split] = ["test"] * (n - n_tuning)
    splits = dev + test
    random.Random(seed).shuffle(splits)
    return splits


def draft_queries(
    chunks: Sequence[Chunk],
    llm: JsonLlm,
    counts: dict[QueryClass, int],
    seed: int = 13,
    tuning_share: float = 1 / 3,
) -> list[LabeledQuery]:
    df, n_docs = doc_frequencies(chunks), len(chunks)
    neighbors: dict[str, list[str]] = {}
    for c in chunks:
        neighbors.setdefault(c.source_id, []).append(c.heading)
    rng = random.Random(seed)
    out: list[LabeledQuery] = []
    picks = sample_chunks(chunks, counts, seed)
    for cls in counts:
        cls_picks = [c for k, c in picks if k == cls]
        splits = assign_splits(len(cls_picks), tuning_share, seed)
        for chunk, split in zip(cls_picks, splits, strict=True):
            others = [h for h in neighbors[chunk.source_id] if h != chunk.heading]
            neighbor = rng.choice(others) if others else chunk.title
            prompt = build_prompt(cls, chunk, rare_words(chunk, df, n_docs), neighbor)
            text = str(llm.complete_json(SYSTEM, prompt).get("query", "")).strip()
            if not text:
                continue
            out.append(
                LabeledQuery(
                    query_id=f"n{len(out) + 1:03d}",
                    text=text,
                    query_class=cls,
                    split=split,
                    gold_chunk_ids=(chunk.chunk_id,),
                )
            )
    return out
