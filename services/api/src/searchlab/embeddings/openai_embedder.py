from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from searchlab.embeddings.errors import EmbeddingProviderError

BATCH = 96


class OpenAIEmbedder:
    def __init__(self, client: Any, model_id: str = "text-embedding-3-small") -> None:
        self._client = client
        self.model_id = model_id

    @classmethod
    def from_env(cls, model_id: str = "text-embedding-3-small") -> OpenAIEmbedder:
        import os

        from openai import OpenAI

        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not set (put it in services/api/.env)")
        return cls(OpenAI(api_key=key), model_id)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        from openai import OpenAIError

        out: list[list[float]] = []
        for i in range(0, len(texts), BATCH):
            batch = list(texts[i : i + BATCH])
            try:
                resp = self._client.embeddings.create(model=self.model_id, input=batch)
            except OpenAIError as exc:  # bad key, rate limit, network, outage
                raise EmbeddingProviderError(f"{type(exc).__name__} from OpenAI") from exc
            ordered = sorted(resp.data, key=lambda d: d.index)
            out.extend([list(d.embedding) for d in ordered])
        return out
