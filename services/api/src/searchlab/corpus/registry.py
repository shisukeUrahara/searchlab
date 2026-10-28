"""Named corpora. Each spec knows how to fetch its sources and turn them into chunks."""
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from searchlab.corpus import nasa, pipeline
from searchlab.corpus.manifest import Manifest
from searchlab.domain.models import Chunk

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_CORPUS = "nasa"

Fetcher = Callable[[str], bytes]


@dataclass(frozen=True)
class CorpusSpec:
    name: str
    label: str
    snapshot_subdir: str
    fetch: Callable[[Fetcher, Path], Manifest]
    build_chunks: Callable[[Manifest, Path], list[Chunk]]

    @property
    def dir(self) -> Path:
        return REPO_ROOT / "fixtures" / self.name

    @property
    def snapshot_dir(self) -> Path:
        return self.dir / self.snapshot_subdir

    @property
    def runs_dir(self) -> Path:
        return REPO_ROOT / "runs" / self.name


CORPORA: dict[str, CorpusSpec] = {
    "github-docs": CorpusSpec(
        name="github-docs",
        label="GitHub Docs (v1)",
        snapshot_subdir="snapshot",
        fetch=pipeline.fetch_snapshot,
        build_chunks=pipeline.build_chunks,
    ),
    "nasa": CorpusSpec(
        name="nasa",
        label="NASA handbooks",
        snapshot_subdir="pdf",
        fetch=nasa.fetch_nasa,
        build_chunks=nasa.build_nasa_chunks,
    ),
}


class UnknownCorpusError(ValueError):
    pass


def get_corpus(name: str | None = None) -> CorpusSpec:
    key = name or os.environ.get("SEARCHLAB_CORPUS") or DEFAULT_CORPUS
    if key not in CORPORA:
        raise UnknownCorpusError(f"unknown corpus {key!r}; choose from {sorted(CORPORA)}")
    return CORPORA[key]
