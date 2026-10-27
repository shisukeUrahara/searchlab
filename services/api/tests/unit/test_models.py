import pytest
from pydantic import ValidationError

from searchlab.domain.models import Chunk


def make_chunk(**kw: str) -> Chunk:
    base = dict(chunk_id="c1", source_id="s1", title="T", heading="H", text="body", url="u")
    return Chunk(**{**base, **kw})


def test_chunk_is_immutable() -> None:
    c = make_chunk()
    with pytest.raises(ValidationError):
        c.text = "changed"  # type: ignore[misc]


def test_chunk_requires_fields() -> None:
    with pytest.raises(ValidationError):
        Chunk(chunk_id="c1")  # type: ignore[call-arg]
