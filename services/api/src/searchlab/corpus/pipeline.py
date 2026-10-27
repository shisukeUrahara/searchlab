"""Orchestrates fetch -> manifest -> clean -> chunk -> chunks.jsonl. I/O is injected."""
from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from searchlab.corpus import sources
from searchlab.corpus.chunker import chunk_document
from searchlab.corpus.clean import clean_markdown
from searchlab.corpus.manifest import Manifest, SourceEntry, read_manifest, sha256_bytes
from searchlab.domain.models import Chunk

Fetcher = Callable[[str], bytes]


def fetch_snapshot(fetch: Fetcher, snapshot_dir: Path, now: datetime | None = None) -> Manifest:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = (now or datetime.now(UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries: list[SourceEntry] = []
    for path in sources.PATHS:
        data = fetch(sources.raw_url(path))
        name = path.rsplit("/", 1)[-1]
        (snapshot_dir / name).write_bytes(data)
        entries.append(
            SourceEntry(
                source_id=sources.source_id(path),
                company_reference="GitHub",
                url=sources.docs_url(path),
                repo_path=path,
                repo_commit=sources.PINNED_SHA,
                retrieved_at_utc=stamp,
                license=sources.LICENSE,
                transformation=sources.TRANSFORMATION,
                sha256=sha256_bytes(data),
                file=name,
            )
        )
    return Manifest(sources=entries)


def build_chunks(manifest: Manifest, snapshot_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for entry in manifest.sources:
        doc = clean_markdown((snapshot_dir / entry.file).read_text())
        chunks.extend(chunk_document(entry.source_id, doc.title, entry.url, doc.body))
    return chunks


def write_chunks(chunks: list[Chunk], path: Path) -> None:
    path.write_text("".join(c.model_dump_json() + "\n" for c in chunks))


def read_chunks(path: Path) -> list[Chunk]:
    return [Chunk.model_validate_json(line) for line in path.read_text().splitlines() if line]


def manifest_path(corpus_dir: Path) -> Path:
    return corpus_dir / "source_manifest.json"


def load_manifest(corpus_dir: Path) -> Manifest:
    return read_manifest(manifest_path(corpus_dir))
