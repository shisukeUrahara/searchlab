"""Heading-aware chunking with content-derived, stable chunk IDs."""
from __future__ import annotations

import hashlib
import re

from searchlab.domain.models import Chunk

_HEADING = re.compile(r"^(#{2,4})\s+(.*\S)\s*$")
MAX_CHARS = 1200


def chunk_id(source_id: str, heading: str, text: str) -> str:
    digest = hashlib.sha256(f"{source_id}\x00{heading}\x00{text}".encode()).hexdigest()
    return digest[:16]


def _sections(body: str) -> list[tuple[str, list[str]]]:
    """Split on ##..#### headings, ignoring '#' lines inside code fences."""
    sections: list[tuple[str, list[str]]] = [("", [])]
    path: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else _HEADING.match(line)
        if m:
            level = len(m.group(1)) - 2
            path = [*path[:level], m.group(2)]
            sections.append((" > ".join(path), []))
        else:
            sections[-1][1].append(line)
    return sections


def _split_long(text: str) -> list[str]:
    """Pack paragraphs up to MAX_CHARS; never cut inside a paragraph."""
    parts: list[str] = []
    current = ""
    for para in re.split(r"\n\n+", text):
        if current and len(current) + len(para) + 2 > MAX_CHARS:
            parts.append(current)
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        parts.append(current)
    return parts


def chunk_document(source_id: str, title: str, url: str, body: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    for heading, lines in _sections(body):
        text = "\n".join(lines).strip()
        if not text:
            continue
        for part in _split_long(text):
            chunks.append(
                Chunk(
                    chunk_id=chunk_id(source_id, heading, part),
                    source_id=source_id,
                    title=title,
                    heading=heading or title,
                    text=part,
                    url=url,
                )
            )
    return chunks
