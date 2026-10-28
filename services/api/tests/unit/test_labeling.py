from typing import Any

from searchlab.domain.models import Chunk, LabeledQuery, ScoredChunk
from searchlab.labeling.draft import assign_splits, draft_queries, identifiers, sample_chunks
from searchlab.labeling.judge import judge_query, pool


def chunk(i: int, doc: str, text: str) -> Chunk:
    return Chunk(chunk_id=f"{i:016x}", source_id=doc, title="T", heading=f"H{i}",
                 text=text + " filler" * 60, url="u")


CHUNKS = [chunk(i, f"d{i % 3}", f"Section {i} on KDP C and NPR 7123.1") for i in range(30)]


class FakeLlm:
    model_id = "fake"

    def __init__(self, reply: dict[str, Any] | None = None) -> None:
        self.prompts: list[str] = []
        self.reply = reply

    def complete_json(self, system: str, user: str) -> dict[str, Any]:
        self.prompts.append(user)
        return self.reply if self.reply is not None else {"query": f"q{len(self.prompts)}"}


def test_identifiers_found_and_common_words_ignored() -> None:
    ids = identifiers("At KDP C the NASA team checks NPR 7123.1 and SWE-139 per THE plan.")
    assert "KDP C" in ids and "NPR 7123.1" in ids and "SWE-139" in ids
    assert "NASA" not in ids and "THE" not in ids


def test_sampling_spreads_across_docs_without_reuse() -> None:
    picks = sample_chunks(CHUNKS, {"exact_id": 6, "paraphrase": 6}, seed=1)
    ids = [c.chunk_id for _, c in picks]
    assert len(ids) == len(set(ids)) == 12
    docs = [c.source_id for k, c in picks if k == "exact_id"]
    assert sorted(docs) == ["d0", "d0", "d1", "d1", "d2", "d2"]


def test_assign_splits_counts_and_seed() -> None:
    s = assign_splits(30, 1 / 3, seed=5)
    assert s.count("dev") == 10 and s == assign_splits(30, 1 / 3, seed=5)


def test_draft_builds_queries_with_seed_gold_and_class_prompts() -> None:
    llm = FakeLlm()
    qs = draft_queries(CHUNKS, llm, {"exact_id": 3, "paraphrase": 3, "distractor": 3}, seed=2)
    assert len(qs) == 9 and all(len(q.gold_chunk_ids) == 1 for q in qs)
    assert "exact identifier" in llm.prompts[0]
    assert "Do NOT use" in llm.prompts[3]
    assert "sounds like it is about" in llm.prompts[6]
    assert [q.query_id for q in qs][:2] == ["n001", "n002"]


def test_empty_llm_reply_is_skipped() -> None:
    assert draft_queries(CHUNKS, FakeLlm({}), {"paraphrase": 2}) == []


class Fixed:
    def __init__(self, cs: list[Chunk]) -> None:
        self.cs = cs

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        return [ScoredChunk(chunk=c, score=1, rank=i) for i, c in enumerate(self.cs[:top_k], 1)]


def test_pool_is_union_without_duplicates() -> None:
    p = pool("q", {"a": Fixed(CHUNKS[:3]), "b": Fixed(CHUNKS[2:5])})
    assert [c.chunk_id for c in p] == [c.chunk_id for c in CHUNKS[:5]]


def test_judge_keeps_seed_and_adds_llm_relevant() -> None:
    q = LabeledQuery(query_id="n001", text="x", query_class="paraphrase", split="test",
                     gold_chunk_ids=(CHUNKS[0].chunk_id,))
    llm = FakeLlm({"relevant": [2, "1", "junk", 99]})
    updated, js = judge_query(q, CHUNKS[:4], llm)
    assert updated.gold_chunk_ids == (CHUNKS[0].chunk_id, CHUNKS[1].chunk_id, CHUNKS[2].chunk_id)
    assert sum(j.relevant for j in js) == 3 and js[0].source == "seed"
    assert CHUNKS[0].text[:20] not in llm.prompts[0]  # seed chunk is not re-judged
