"""PDF -> sections. Pure text functions are separate from pypdf I/O so they are easy to test.

Pipeline: extract page text -> drop running headers/footers -> find section starts
(PDF outline when present, numbered-heading regex otherwise) -> slice text between starts.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pypdf import PdfReader

RUNNING_LINE_SHARE = 0.3
SKIP_TITLES = ("title page", "table of contents", "table of figures", "table of tables",
               "table of boxes", "contents", "bibliography", "references", "index",
               "figures", "tables", "list of figures", "list of tables")

# "Chapter 6. Systems Engineering Management Plan" or "6.1 Systems Engineering Management Plan
# Function". Three-level numbers (6.1.1) are requirement paragraphs in NPRs, not headings.
_HEADING = re.compile(r"^(Chapter\s+\d+\.?\s+\S.{2,80}|\d{1,2}\.\d{1,2}\s+[A-Z][^.]{2,80})$")


@dataclass(frozen=True)
class Marker:
    offset: int
    heading: str


@dataclass(frozen=True)
class Section:
    heading: str
    text: str
    page: int  # 1-based page where the section starts


def _norm(line: str) -> str:
    return re.sub(r"\d+", "#", line.strip().lower())


def _edges(lines: list[str]) -> set[int]:
    """Indexes of lines where headers/footers live: the first 3 and last 4 lines of a page."""
    n = len(lines)
    return set(range(min(3, n))) | set(range(max(0, n - 4), n))


def strip_running_lines(pages: list[str]) -> list[str]:
    """Remove header/footer lines that repeat on many pages (digits masked), plus bare numbers.

    Only lines at a page's top or bottom are candidates, so repeated body lines such as
    requirement tags ("[SWE-088]") survive.
    """
    split = [[ln for ln in page.splitlines() if ln.strip()] for page in pages]
    counts: Counter[str] = Counter()
    for lines in split:
        counts.update({_norm(lines[i]) for i in _edges(lines)})
    min_pages = max(3, int(len(pages) * RUNNING_LINE_SHARE))
    running = {k for k, v in counts.items() if v >= min_pages}
    out: list[str] = []
    for lines in split:
        edges = _edges(lines)
        kept = [
            ln.rstrip()
            for i, ln in enumerate(lines)
            if not (i in edges and _norm(ln) in running) and not ln.strip().isdigit()
        ]
        out.append("\n".join(kept))
    return out


def join_pages(pages: list[str]) -> tuple[str, list[int]]:
    """Concatenate pages; return text and the char offset where each page starts."""
    starts: list[int] = []
    parts: list[str] = []
    pos = 0
    for page in pages:
        starts.append(pos)
        parts.append(page)
        pos += len(page) + 1
    return "\n".join(parts), starts


def page_of(offset: int, starts: list[int]) -> int:
    page = 0
    for i, s in enumerate(starts):
        if s <= offset:
            page = i
    return page + 1


def regex_markers(text: str) -> list[Marker]:
    markers: list[Marker] = []
    pos = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if _HEADING.match(stripped):
            markers.append(Marker(pos, re.sub(r"\s+", " ", stripped)))
        pos += len(line) + 1
    return markers


def outline_markers(
    entries: list[tuple[int, str, int]], text: str, starts: list[int]
) -> list[Marker]:
    """entries = (depth, title, 0-based page). Find each title on its page, else use page start.

    The heading becomes a path ("3.0 Life Cycle > 3.1 Programs") using outline depth.
    """
    markers: list[Marker] = []
    path: list[str] = []
    skip_below: int | None = None  # depth of a skipped entry; its children are skipped too
    for depth, title, page in entries:
        title = re.sub(r"\s+", " ", title).strip()
        path = [*path[:depth], title]
        if skip_below is not None and depth > skip_below:
            continue
        skip_below = None
        if title.lower().startswith(SKIP_TITLES):
            skip_below = depth
            continue
        start = starts[page]
        end = starts[page + 1] if page + 1 < len(starts) else len(text)
        found = _find_title(text[start:end], title)
        markers.append(Marker(start + found, " > ".join(path)))
    return markers


def _find_title(page_text: str, title: str) -> int:
    probe = re.sub(r"\s+", " ", title).lower()[:40]
    flat = page_text.lower()
    idx = flat.find(probe)
    if idx >= 0:
        return idx
    words = probe.split()
    if len(words) > 1:  # PDF text may break the title over lines
        idx = flat.find(words[0] + " " + words[1])
        if idx < 0:
            idx = flat.find(words[0] + "\n" + words[1])
    return max(idx, 0)


def split_sections(text: str, markers: list[Marker], starts: list[int]) -> list[Section]:
    ordered = sorted(markers, key=lambda m: m.offset)
    sections: list[Section] = []
    for i, m in enumerate(ordered):
        end = ordered[i + 1].offset if i + 1 < len(ordered) else len(text)
        body = text[m.offset:end].strip()
        # drop the heading line itself from the body when it is repeated there
        first, _, rest = body.partition("\n")
        if first.strip().lower() and first.strip().lower() in m.heading.lower():
            body = rest.strip()
        if body:
            sections.append(Section(m.heading, body, page_of(m.offset, starts)))
    return sections


# ---- pypdf I/O ----

def _flatten_outline(
    reader: PdfReader, items: list[Any], depth: int = 0
) -> list[tuple[int, str, int]]:
    out: list[tuple[int, str, int]] = []
    for item in items:
        if isinstance(item, list):
            out.extend(_flatten_outline(reader, item, depth + 1))
        else:
            page = reader.get_destination_page_number(item)
            if page is not None and page >= 0:
                out.append((depth, str(item.title), page))
    return out


def load_pdf_sections(path: Path) -> list[Section]:
    reader = PdfReader(path)
    pages = strip_running_lines([p.extract_text() or "" for p in reader.pages])
    text, starts = join_pages(pages)
    entries = _flatten_outline(reader, reader.outline) if reader.outline else []
    markers = outline_markers(entries, text, starts) if entries else regex_markers(text)
    if not markers:
        markers = [Marker(0, path.stem)]
    return split_sections(text, markers, starts)
