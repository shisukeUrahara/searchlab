from datetime import UTC, datetime
from pathlib import Path

import pytest

from searchlab.corpus import nasa
from searchlab.corpus.registry import get_corpus


def test_registry_has_nasa_with_pdf_dir() -> None:
    spec = get_corpus("nasa")
    assert spec.snapshot_dir.name == "pdf" and spec.label == "NASA handbooks"


def test_doc_ids_and_files_unique() -> None:
    assert len({d.source_id for d in nasa.DOCS}) == len(nasa.DOCS)
    assert len({d.file for d in nasa.DOCS}) == len(nasa.DOCS)


def test_fetch_rejects_non_pdf(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="did not return a PDF"):
        nasa.fetch_nasa(lambda url: b"<html>not found</html>", tmp_path,
                        now=datetime(2026, 10, 28, tzinfo=UTC))
