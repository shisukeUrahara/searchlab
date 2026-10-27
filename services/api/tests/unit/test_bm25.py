from searchlab.domain.models import Chunk
from searchlab.retrieval.bm25 import Bm25Retriever
from searchlab.retrieval.tokenize import tokenize


def chunk(cid: str, text: str, heading: str = "H") -> Chunk:
    return Chunk(chunk_id=cid, source_id="s", title="T", heading=heading, text=text, url="u")


def test_tokenizer_keeps_compound_and_parts() -> None:
    toks = tokenize("Check `x-ratelimit-remaining` now")
    assert "x-ratelimit-remaining" in toks
    assert {"x", "ratelimit", "remaining"} <= set(toks)


def test_tokenizer_keeps_trailing_equals_and_dotted_names() -> None:
    toks = tokenize('starts with sha256= and crypto.timingSafeEqual and rel="next"')
    assert "sha256=" in toks and "sha256" in toks
    assert "crypto.timingsafeequal" in toks and "timingsafeequal" in toks
    assert "rel" in toks and "next" in toks


def test_tokenizer_plain_word_not_duplicated() -> None:
    assert tokenize("pagination") == ["pagination"]


CHUNKS = [
    chunk("a", "The x-ratelimit-remaining header shows requests left."),
    chunk("b", "Pagination uses the link header and per_page."),
    chunk("c", "Webhook secrets and signatures."),
]


def test_exact_identifier_ranks_first() -> None:
    hits = Bm25Retriever(CHUNKS).search("x-ratelimit-remaining", top_k=3)
    assert hits[0].chunk.chunk_id == "a"
    assert [h.rank for h in hits] == list(range(1, len(hits) + 1))


def test_scores_sorted_descending_and_top_k_respected() -> None:
    hits = Bm25Retriever(CHUNKS).search("header link", top_k=1)
    assert len(hits) == 1 and hits[0].chunk.chunk_id == "b"


def test_no_overlap_or_empty_query_returns_nothing() -> None:
    r = Bm25Retriever(CHUNKS)
    assert r.search("zzzunknown", 5) == []
    assert r.search("   ", 5) == []
