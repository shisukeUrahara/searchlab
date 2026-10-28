from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace

import pytest

from searchlab.config import load_env
from searchlab.embeddings.cache import CacheMissError, CachingEmbedder
from searchlab.embeddings.fake import FakeEmbedder
from searchlab.embeddings.openai_embedder import BATCH, OpenAIEmbedder


class Counting:
    model_id = "m"

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        return [[float(len(t)), 1.0] for t in texts]


def test_cache_hits_skip_inner_and_dedupe(tmp_path: Path) -> None:
    inner = Counting()
    c = CachingEmbedder(tmp_path, "m", inner)
    assert c.embed(["aa", "b", "aa"]) == [[2.0, 1.0], [1.0, 1.0], [2.0, 1.0]]
    assert (tmp_path / "m.npz").exists()
    assert inner.calls == [["aa", "b"]]
    c.embed(["aa", "b"])
    assert len(inner.calls) == 1


def test_cache_persists_across_instances_and_works_offline(tmp_path: Path) -> None:
    CachingEmbedder(tmp_path, "m", Counting()).embed(["x"])
    offline = CachingEmbedder(tmp_path, "m", inner=None)
    assert offline.embed(["x"]) == [[1.0, 1.0]]
    with pytest.raises(CacheMissError):
        offline.embed(["never seen"])


def test_fake_embedder_is_deterministic_and_normalised() -> None:
    f = FakeEmbedder()
    a, b = f.embed(["rate limit headers"])[0], f.embed(["rate limit headers"])[0]
    assert a == b
    assert abs(sum(x * x for x in a) - 1.0) < 1e-9


def test_openai_embedder_batches_and_keeps_order() -> None:
    calls: list[int] = []

    def create(model: str, input: list[str]) -> SimpleNamespace:
        calls.append(len(input))
        data = [SimpleNamespace(index=i, embedding=[float(len(t))]) for i, t in enumerate(input)]
        return SimpleNamespace(data=list(reversed(data)))  # API order must not matter

    client = SimpleNamespace(embeddings=SimpleNamespace(create=create))
    texts = ["a" * (i + 1) for i in range(BATCH + 5)]
    out = OpenAIEmbedder(client).embed(texts)
    assert calls == [BATCH, 5]
    assert [v[0] for v in out] == [float(i + 1) for i in range(len(texts))]


def test_load_env_does_not_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = tmp_path / ".env"
    f.write_text("# c\nA_KEY='one'\nB_KEY=two\n")
    monkeypatch.setenv("B_KEY", "keep")
    monkeypatch.delenv("A_KEY", raising=False)
    load_env(f)
    import os

    assert os.environ["A_KEY"] == "one" and os.environ["B_KEY"] == "keep"


def test_legacy_jsonl_cache_is_read_and_saved_as_npz(tmp_path: Path) -> None:
    import hashlib
    import json

    key = hashlib.sha256(b"old").hexdigest()
    (tmp_path / "m.jsonl").write_text(json.dumps({"k": key, "v": [0.5, 0.25]}) + "\n")
    c = CachingEmbedder(tmp_path, "m", inner=None)
    assert c.embed(["old"]) == [[0.5, 0.25]]
    c.save()
    (tmp_path / "m.jsonl").unlink()
    assert CachingEmbedder(tmp_path, "m").embed(["old"]) == [[0.5, 0.25]]


def test_vectors_stored_as_float16(tmp_path: Path) -> None:
    import numpy as np

    CachingEmbedder(tmp_path, "m", Counting()).embed(["abc"])
    assert np.load(tmp_path / "m.npz")["vectors"].dtype == np.float16
