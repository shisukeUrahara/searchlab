from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from searchlab.api.app import AppDeps, create_app
from searchlab.domain.models import Split
from searchlab.embeddings.fake import FakeEmbedder
from searchlab.services.eval_service import EvalOutcome, run_eval
from searchlab.services.search_service import SearchService
from searchlab.wiring import load_chunks, make_retrievers

CORPUS = Path(__file__).resolve().parents[4] / "fixtures" / "github-docs"


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    emb, chunks = FakeEmbedder(), load_chunks(CORPUS)
    search = SearchService(make_retrievers(chunks, emb), chunks)

    def eval_fn(split: Split, k: int) -> EvalOutcome:
        return run_eval(CORPUS, emb, split, k, runs_dir=tmp_path / "runs", corpus_label="GH")

    graph = tmp_path / "graph.json"
    deps = AppDeps(search, CORPUS, tmp_path / "runs", eval_fn, "GitHub Docs (v1)", graph)
    return TestClient(create_app(deps))


def test_health_and_request_id_header(client: TestClient) -> None:
    r = client.get("/health", headers={"x-request-id": "abc123"})
    assert r.status_code == 200 and r.headers["x-request-id"] == "abc123"
    assert r.json()["chunk_count"] == 78 and r.json()["methods"] == ["bm25", "dense", "hybrid"]


def test_search_returns_three_ranked_columns(client: TestClient) -> None:
    r = client.post("/search", json={"query": "x-ratelimit-remaining", "top_k": 3})
    body = r.json()
    assert r.status_code == 200 and body["request_id"]
    assert [m["method"] for m in body["results"]] == ["bm25", "dense", "hybrid"]
    for m in body["results"]:
        assert len(m["hits"]) == 3 and [h["rank"] for h in m["hits"]] == [1, 2, 3]
        assert m["latency_ms"] >= 0
        assert all(h["source_id"].startswith("github-docs/") for h in m["hits"])


def test_search_validation_errors_use_stable_shape(client: TestClient) -> None:
    for payload in ({"query": ""}, {"query": "q", "top_k": 99}, {"query": "q", "methods": ["x"]}):
        r = client.post("/search", json=payload)
        body = r.json()
        assert r.status_code == 422 and body["code"] == "invalid_request"
        assert body["request_id"] and body["message"]


def test_chunk_lookup_and_404(client: TestClient) -> None:
    cid = client.post("/search", json={"query": "per_page"}).json()["results"][0]["hits"][0][
        "chunk_id"
    ]
    assert client.get(f"/chunks/{cid}").json()["chunk_id"] == cid
    r = client.get("/chunks/nope")
    assert r.status_code == 404 and r.json()["code"] == "chunk_not_found"


def test_sources_and_corpus(client: TestClient) -> None:
    assert len(client.get("/sources").json()["sources"]) == 6
    corpus = client.get("/corpus").json()
    assert corpus["label"] == "GitHub Docs (v1)" and corpus["chunk_count"] == 78
    assert len(corpus["docs"]) == 6 and sum(d["chunks"] for d in corpus["docs"]) == 78


def test_queries_are_paginated_and_filtered(client: TestClient) -> None:
    first = client.get("/queries", params={"split": "test", "limit": 10}).json()
    assert first["total"] == 30 and len(first["items"]) == 10
    assert first["split_label"] == "Holdout set"
    last = client.get("/queries", params={"split": "test", "limit": 10, "offset": 25}).json()
    assert len(last["items"]) == 5
    ids = {q["query_id"] for q in first["items"]} & {q["query_id"] for q in last["items"]}
    assert ids == set()
    exact = client.get("/queries", params={"split": "test", "query_class": "exact_id"}).json()
    assert exact["total"] == 10 and all(q["query_class"] == "exact_id" for q in exact["items"])
    found = client.get("/queries", params={"split": "test", "q": "SECURE_compare"}).json()
    assert [q["text"] for q in found["items"]] == ["secure_compare"]
    for bad in ({"split": "bad"}, {"limit": 0}, {"limit": 500}, {"offset": -1}):
        assert client.get("/queries", params=bad).status_code == 422


def test_eval_run_roundtrip_and_path_traversal_blocked(client: TestClient) -> None:
    assert client.get("/eval-runs").json() == []
    run_id = client.post("/eval-runs", json={"split": "dev", "rrf_k": 60}).json()["run_id"]
    listed = client.get("/eval-runs").json()
    assert listed[0]["id"] == run_id and listed[0]["label"].startswith("GH · Tuning set · RRF k=60")
    run = client.get(f"/eval-runs/{run_id}").json()
    assert run["manifest"]["sample_count"] == 15 and len(run["cases"]) == 45
    curve = run["curves"]["hybrid"]
    assert len(curve) == 10 and all(a <= b for a, b in zip(curve, curve[1:], strict=False))
    pairs = {(h["a"], h["b"]) for h in run["head_to_head"]}
    assert pairs == {("bm25", "dense"), ("bm25", "hybrid"), ("dense", "hybrid")}
    assert all(h["a_better"] + h["tie"] + h["b_better"] == 15 for h in run["head_to_head"])
    assert client.get("/eval-runs/..%2Fetc").status_code == 404
    assert client.get("/eval-runs/missing").json()["code"] == "run_not_found"


def test_uncached_query_without_api_key_returns_503(tmp_path: Path) -> None:
    from qdrant_client import QdrantClient

    from searchlab.embeddings.cache import CachingEmbedder
    from searchlab.retrieval.dense import DenseRetriever, build_dense_index
    from searchlab.store.qdrant_store import QdrantVectorStore

    chunks = load_chunks(CORPUS)
    live = FakeEmbedder()
    store = QdrantVectorStore(QdrantClient(":memory:"))
    build_dense_index(chunks, live, store)
    offline = CachingEmbedder(tmp_path / "cache", live.model_id, inner=None)  # empty cache
    search = SearchService({"dense": DenseRetriever(offline, store)}, chunks)
    app = create_app(AppDeps(search, CORPUS, tmp_path, lambda s, k: run_eval(CORPUS, live, s, k)))
    r = TestClient(app).post("/search", json={"query": "never embedded", "methods": ["dense"]})
    assert r.status_code == 503 and r.json()["code"] == "embedding_unavailable"
    assert r.json()["request_id"]


def test_graph_404_until_built_then_served(client: TestClient, tmp_path: Path) -> None:
    r = client.get("/graph")
    assert r.status_code == 404 and r.json()["code"] == "graph_not_built"
    (tmp_path / "graph.json").write_text('{"nodes": [], "edges": []}')
    assert client.get("/graph").json() == {"nodes": [], "edges": []}


def test_archived_v1_runs_get_labels_and_curves() -> None:
    from searchlab.services.run_report import list_runs, load_run

    runs_dir = CORPUS.parents[1] / "runs" / "github-docs"
    runs = list_runs(runs_dir)
    assert [r["split"] for r in runs] == ["test", "dev"]
    assert runs[0]["label"].startswith("Holdout set · RRF k=60")
    report = load_run(runs_dir, runs[0]["id"])
    assert report["curves"]["hybrid"][4] == 1.0  # Recall@5 from the archived run
