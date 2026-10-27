from qdrant_client import QdrantClient

from searchlab.domain.models import Chunk
from searchlab.embeddings.fake import FakeEmbedder
from searchlab.retrieval.dense import DenseRetriever, build_dense_index
from searchlab.store.qdrant_store import QdrantVectorStore


def chunk(cid: str, text: str) -> Chunk:
    return Chunk(chunk_id=cid, source_id="s", title="T", heading="H", text=text, url="u")


CHUNKS = [
    chunk("0000000000000001", "rate limit headers remaining requests"),
    chunk("0000000000000002", "pagination link header next page"),
    chunk("0000000000000003", "webhook secret signature validation"),
]


def make() -> DenseRetriever:
    emb, store = FakeEmbedder(), QdrantVectorStore(QdrantClient(":memory:"))
    build_dense_index(CHUNKS, emb, store)
    return DenseRetriever(emb, store)


def test_most_similar_chunk_is_first_with_ranks_from_one() -> None:
    hits = make().search("webhook signature secret", top_k=3)
    assert hits[0].chunk.chunk_id == "0000000000000003"
    assert [h.rank for h in hits] == [1, 2, 3]
    assert hits[0].score >= hits[1].score >= hits[2].score


def test_top_k_limits_results() -> None:
    assert len(make().search("rate limit", top_k=2)) == 2


def test_empty_query_and_empty_store() -> None:
    assert make().search("  ", 3) == []
    empty = DenseRetriever(FakeEmbedder(), QdrantVectorStore(QdrantClient(":memory:")))
    assert empty.search("anything", 3) == []


def test_reindexing_same_chunks_is_idempotent() -> None:
    emb, store = FakeEmbedder(), QdrantVectorStore(QdrantClient(":memory:"))
    build_dense_index(CHUNKS, emb, store)
    build_dense_index(CHUNKS, emb, store)
    assert len(DenseRetriever(emb, store).search("rate", top_k=10)) == 3
