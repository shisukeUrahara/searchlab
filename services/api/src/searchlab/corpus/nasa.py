"""NASA handbook corpus: five public PDFs (US Government works, 17 U.S.C. 105)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader

from searchlab.corpus.chunker import chunk_id, pack_lines
from searchlab.corpus.manifest import Manifest, SourceEntry, sha256_bytes
from searchlab.corpus.pdf_loader import load_pdf_sections
from searchlab.domain.models import Chunk

PDF_MAX_CHARS = 1000
MIN_CHARS = 40  # drop extraction crumbs such as lone figure labels
LICENSE = "US Government work (17 U.S.C. 105); not affiliated with or endorsed by NASA"
TRANSFORMATION = "pypdf text; running headers/footers removed; front matter and references skipped"


@dataclass(frozen=True)
class NasaDoc:
    source_id: str
    doc_number: str
    title: str
    url: str

    @property
    def file(self) -> str:
        return self.url.rsplit("/", 1)[-1]


DOCS = (
    NasaDoc("nasa/se-handbook", "NASA/SP-2016-6105 Rev2", "NASA Systems Engineering Handbook",
            "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf"),
    NasaDoc("nasa/pm-handbook", "NASA/SP-2014-3705",
            "NASA Space Flight Program and Project Management Handbook",
            "https://ntrs.nasa.gov/api/citations/20150000400/downloads/20150000400.pdf"),
    NasaDoc("nasa/npr-7120-5f", "NPR 7120.5F",
            "NASA Space Flight Program and Project Management Requirements",
            "https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7120_005F_/N_PR_7120_005F_.pdf"),
    NasaDoc("nasa/npr-7123-1d", "NPR 7123.1D",
            "NASA Systems Engineering Processes and Requirements",
            "https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7123_001D_/N_PR_7123_001D_.pdf"),
    NasaDoc("nasa/npr-7150-2d", "NPR 7150.2D", "NASA Software Engineering Requirements",
            "https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7150_002D_/N_PR_7150_002D_.pdf"),
)


def fetch_nasa(
    fetch: Callable[[str], bytes], pdf_dir: Path, now: datetime | None = None
) -> Manifest:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    stamp = (now or datetime.now(UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries: list[SourceEntry] = []
    for doc in DOCS:
        data = fetch(doc.url)
        if not data.startswith(b"%PDF"):
            raise ValueError(f"{doc.url} did not return a PDF")
        path = pdf_dir / doc.file
        path.write_bytes(data)
        entries.append(
            SourceEntry(
                source_id=doc.source_id,
                company_reference="NASA",
                url=doc.url,
                doc_number=doc.doc_number,
                pages=len(PdfReader(path).pages),
                retrieved_at_utc=stamp,
                license=LICENSE,
                transformation=TRANSFORMATION,
                sha256=sha256_bytes(data),
                file=doc.file,
            )
        )
    return Manifest(sources=entries)


def build_nasa_chunks(manifest: Manifest, pdf_dir: Path) -> list[Chunk]:
    titles = {d.source_id: d.title for d in DOCS}
    chunks: list[Chunk] = []
    seen: set[str] = set()
    for entry in manifest.sources:
        for section in load_pdf_sections(pdf_dir / entry.file):
            for part in pack_lines(section.text, PDF_MAX_CHARS):
                if len(part.strip()) < MIN_CHARS:
                    continue
                cid = chunk_id(entry.source_id, section.heading, part)
                if cid in seen:  # identical text under the same heading: keep the first
                    continue
                seen.add(cid)
                chunks.append(
                    Chunk(
                        chunk_id=cid,
                        source_id=entry.source_id,
                        title=titles.get(entry.source_id, entry.source_id),
                        heading=section.heading,
                        text=part,
                        url=f"{entry.url}#page={section.page}",
                        page=section.page,
                    )
                )
    return chunks
