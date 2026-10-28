from pathlib import Path

import pytest

from searchlab.corpus.pipeline import read_chunks
from searchlab.corpus.registry import UnknownCorpusError, get_corpus
from searchlab.domain.models import Chunk


def test_default_and_env_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SEARCHLAB_CORPUS", raising=False)
    assert get_corpus().name == "github-docs"
    monkeypatch.setenv("SEARCHLAB_CORPUS", "github-docs")
    assert get_corpus().dir.name == "github-docs"


def test_unknown_corpus_raises() -> None:
    with pytest.raises(UnknownCorpusError):
        get_corpus("nope")


def test_spec_paths() -> None:
    spec = get_corpus("github-docs")
    assert spec.snapshot_dir == spec.dir / "snapshot"
    assert spec.runs_dir.parts[-2:] == ("runs", "github-docs")


def test_v1_corpus_rebuilds_identical_chunk_ids() -> None:
    spec = get_corpus("github-docs")
    from searchlab.corpus.pipeline import load_manifest

    rebuilt = spec.build_chunks(load_manifest(spec.dir), spec.snapshot_dir)
    committed = read_chunks(spec.dir / "chunks.jsonl")
    assert [c.chunk_id for c in rebuilt] == [c.chunk_id for c in committed]


def test_page_is_optional_and_backward_compatible(tmp_path: Path) -> None:
    old_line = '{"chunk_id":"a","source_id":"s","title":"T","heading":"H","text":"x","url":"u"}'
    assert Chunk.model_validate_json(old_line).page is None
