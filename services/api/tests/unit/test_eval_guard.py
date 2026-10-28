import subprocess
from pathlib import Path

import pytest

from searchlab.embeddings.fake import FakeEmbedder
from searchlab.eval.naming import run_label
from searchlab.services.eval_service import DirtyTreeError, run_eval

CORPUS = Path(__file__).resolve().parents[4] / "fixtures" / "github-docs"


def _repo(path: Path, dirty: bool) -> Path:
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    (path / "f.txt").write_text("x")
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.email=a@b", "-c", "user.name=t",
                    "commit", "-qm", "init"], check=True)
    if dirty:
        (path / "f.txt").write_text("changed")
    return path


def test_holdout_refuses_dirty_tree(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "r", dirty=True)
    with pytest.raises(DirtyTreeError):
        run_eval(CORPUS, FakeEmbedder(), "test", runs_dir=tmp_path / "runs", repo_root=repo)


def test_holdout_allowed_on_clean_tree_and_with_override(tmp_path: Path) -> None:
    clean = _repo(tmp_path / "c", dirty=False)
    out = run_eval(CORPUS, FakeEmbedder(), "test", runs_dir=tmp_path / "a", repo_root=clean)
    assert out.run_dir is not None
    dirty = _repo(tmp_path / "d", dirty=True)
    out = run_eval(CORPUS, FakeEmbedder(), "test", runs_dir=tmp_path / "b", repo_root=dirty,
                   allow_dirty=True)
    assert out.run_dir is not None


def test_tuning_runs_ignore_dirty_tree(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "r", dirty=True)
    assert run_eval(CORPUS, FakeEmbedder(), "dev", runs_dir=tmp_path / "x", repo_root=repo).run_dir


def test_run_label() -> None:
    assert run_label("NASA", "test", 60, "2026-10-28T09:05:00Z") == (
        "NASA · Holdout set · RRF k=60 · 28 Oct 2026 09:05 UTC"
    )
