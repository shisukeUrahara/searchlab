from collections import Counter
from pathlib import Path

from searchlab.corpus.pipeline import read_chunks
from searchlab.eval.queries import load_queries

CORPUS = Path(__file__).resolve().parents[4] / "fixtures" / "github-docs"


def test_split_sizes_and_unique_ids() -> None:
    dev, test = load_queries(CORPUS, "dev"), load_queries(CORPUS, "test")
    assert (len(dev), len(test)) == (15, 30)
    ids = [q.query_id for q in dev + test]
    assert len(ids) == len(set(ids))
    assert all(q.split == "dev" for q in dev) and all(q.split == "test" for q in test)


def test_every_gold_chunk_exists() -> None:
    known = {c.chunk_id for c in read_chunks(CORPUS / "chunks.jsonl")}
    for split in ("dev", "test"):
        for q in load_queries(CORPUS, split):  # type: ignore[arg-type]
            assert q.gold_chunk_ids, q.query_id
            assert set(q.gold_chunk_ids) <= known, q.query_id


def test_all_three_classes_present_in_test_split() -> None:
    counts = Counter(q.query_class for q in load_queries(CORPUS, "test"))
    assert set(counts) == {"exact_id", "paraphrase", "distractor"}
