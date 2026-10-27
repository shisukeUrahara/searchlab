import json
from pathlib import Path

from searchlab.embeddings.fake import FakeEmbedder
from searchlab.services.eval_service import run_eval

CORPUS = Path(__file__).resolve().parents[4] / "fixtures" / "github-docs"


def test_dry_run_scores_every_method_without_writing(tmp_path: Path) -> None:
    out = run_eval(CORPUS, FakeEmbedder(), "dev", runs_dir=None)
    assert out.run_dir is None
    overall = {s.method: s for s in out.scores if s.query_class == "all"}
    assert set(overall) == {"bm25", "dense", "hybrid"}
    assert all(s.n == 15 for s in overall.values())


def test_run_folder_has_all_artifacts_and_manifest_fields(tmp_path: Path) -> None:
    out = run_eval(CORPUS, FakeEmbedder(), "dev", rrf_k=30, runs_dir=tmp_path, repo_root=CORPUS)
    assert out.run_dir is not None
    names = {p.name for p in out.run_dir.iterdir()}
    assert {"run_manifest.json", "per_case_results.jsonl", "scores.csv", "scores.json",
            "chart.png", "checksums.txt"} <= names
    m = json.loads((out.run_dir / "run_manifest.json").read_text())
    assert m["sample_count"] == 15 and m["rrf_k"] == 30 and m["split"] == "dev"
    assert len(m["dataset_sha256"]) == 64 and m["embedding_model"] == "fake-64"
    cases = (out.run_dir / "per_case_results.jsonl").read_text().splitlines()
    assert len(cases) == 15 * 3
