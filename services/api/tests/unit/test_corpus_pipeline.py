from datetime import UTC, datetime
from pathlib import Path

from searchlab.corpus import pipeline, sources
from searchlab.corpus.manifest import verify_manifest

NOW = datetime(2026, 10, 27, 12, 0, tzinfo=UTC)


def fake_fetch(url: str) -> bytes:
    return f"---\ntitle: T for {url[-20:]}\n---\n\n## Part\n\nBody of {url[-12:]}.\n".encode()


def test_fetch_writes_files_and_manifest(tmp_path: Path) -> None:
    m = pipeline.fetch_snapshot(fake_fetch, tmp_path, now=NOW)
    assert len(m.sources) == len(sources.PATHS)
    assert m.sources[0].retrieved_at_utc == "2026-10-27T12:00:00Z"
    assert m.sources[0].repo_commit == sources.PINNED_SHA
    assert verify_manifest(m, tmp_path) == []


def test_verify_detects_tampering_and_missing(tmp_path: Path) -> None:
    m = pipeline.fetch_snapshot(fake_fetch, tmp_path, now=NOW)
    (tmp_path / m.sources[0].file).write_text("changed")
    (tmp_path / m.sources[1].file).unlink()
    problems = verify_manifest(m, tmp_path)
    assert any("mismatch" in p for p in problems)
    assert any("missing" in p for p in problems)


def test_rebuilding_chunks_gives_identical_ids(tmp_path: Path) -> None:
    m = pipeline.fetch_snapshot(fake_fetch, tmp_path, now=NOW)
    a = [c.chunk_id for c in pipeline.build_chunks(m, tmp_path)]
    b = [c.chunk_id for c in pipeline.build_chunks(m, tmp_path)]
    assert a == b and len(a) == len(set(a)) > 0


def test_chunks_jsonl_roundtrip(tmp_path: Path) -> None:
    m = pipeline.fetch_snapshot(fake_fetch, tmp_path, now=NOW)
    chunks = pipeline.build_chunks(m, tmp_path)
    out = tmp_path / "chunks.jsonl"
    pipeline.write_chunks(chunks, out)
    assert pipeline.read_chunks(out) == chunks


def test_source_helpers() -> None:
    p = sources.PATHS[0]
    assert sources.source_id(p) == "github-docs/rate-limits-for-the-rest-api"
    assert sources.docs_url(p) == (
        "https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api"
    )
