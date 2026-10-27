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
        return run_eval(CORPUS, emb, split, k, runs_dir=tmp_path)

    return TestClient(create_app(AppDeps(search, CORPUS, tmp_path, eval_fn)))


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


def test_sources_and_queries(client: TestClient) -> None:
    assert len(client.get("/sources").json()["sources"]) == 6
    assert len(client.get("/queries", params={"split": "test"}).json()) == 30
    assert client.get("/queries", params={"split": "bad"}).status_code == 422


def test_eval_run_roundtrip_and_path_traversal_blocked(client: TestClient) -> None:
    assert client.get("/eval-runs").json() == []
    run_id = client.post("/eval-runs", json={"split": "dev", "rrf_k": 60}).json()["run_id"]
    assert run_id in client.get("/eval-runs").json()
    run = client.get(f"/eval-runs/{run_id}").json()
    assert run["manifest"]["sample_count"] == 15 and len(run["cases"]) == 45
    assert client.get("/eval-runs/..%2Fetc").status_code == 404
    assert client.get("/eval-runs/missing").json()["code"] == "run_not_found"
