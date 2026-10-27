"""Source manifest: one row per indexed file, with a checksum so tampering is detectable."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pydantic import BaseModel


class SourceEntry(BaseModel):
    source_id: str
    company_reference: str
    url: str
    repo_path: str
    repo_commit: str
    retrieved_at_utc: str
    license: str
    transformation: str
    sha256: str
    file: str


class Manifest(BaseModel):
    sources: list[SourceEntry]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_manifest(manifest: Manifest, path: Path) -> None:
    path.write_text(json.dumps(manifest.model_dump(), indent=2) + "\n")


def read_manifest(path: Path) -> Manifest:
    return Manifest.model_validate_json(path.read_text())


def verify_manifest(manifest: Manifest, snapshot_dir: Path) -> list[str]:
    """Return a list of problems; empty list means every file matches its checksum."""
    problems: list[str] = []
    for entry in manifest.sources:
        f = snapshot_dir / entry.file
        if not f.exists():
            problems.append(f"missing: {entry.file}")
        elif sha256_bytes(f.read_bytes()) != entry.sha256:
            problems.append(f"checksum mismatch: {entry.file}")
    return problems
