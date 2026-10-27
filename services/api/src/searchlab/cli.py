"""Thin command layer: parse args, call pipeline functions, print results."""
from __future__ import annotations

from pathlib import Path

import httpx
import typer

from searchlab.corpus import pipeline
from searchlab.corpus.manifest import verify_manifest, write_manifest

app = typer.Typer(no_args_is_help=True)

CORPUS_DIR = Path(__file__).resolve().parents[4] / "fixtures" / "github-docs"


def _http_get(url: str) -> bytes:
    r = httpx.get(url, follow_redirects=True, timeout=30)
    r.raise_for_status()
    return r.content


@app.command()
def fetch() -> None:
    """Download the pinned docs and write source_manifest.json."""
    manifest = pipeline.fetch_snapshot(_http_get, CORPUS_DIR / "snapshot")
    write_manifest(manifest, pipeline.manifest_path(CORPUS_DIR))
    typer.echo(f"fetched {len(manifest.sources)} files")


@app.command()
def chunk() -> None:
    """Clean and chunk the snapshot into chunks.jsonl."""
    manifest = pipeline.load_manifest(CORPUS_DIR)
    problems = verify_manifest(manifest, CORPUS_DIR / "snapshot")
    if problems:
        raise typer.Exit(code=_fail(problems))
    chunks = pipeline.build_chunks(manifest, CORPUS_DIR / "snapshot")
    pipeline.write_chunks(chunks, CORPUS_DIR / "chunks.jsonl")
    typer.echo(f"wrote {len(chunks)} chunks")


@app.command()
def verify() -> None:
    """Check snapshot files against manifest checksums."""
    manifest = pipeline.load_manifest(CORPUS_DIR)
    problems = verify_manifest(manifest, CORPUS_DIR / "snapshot")
    if problems:
        raise typer.Exit(code=_fail(problems))
    typer.echo("manifest ok")


def _fail(problems: list[str]) -> int:
    for p in problems:
        typer.echo(p, err=True)
    return 1
