"""Minimal JSON-in/JSON-out LLM port so labeling logic is testable without a network."""
from __future__ import annotations

import json
from typing import Any, Protocol

DEFAULT_MODEL = "gpt-4.1-mini-2025-04-14"


class JsonLlm(Protocol):
    model_id: str

    def complete_json(self, system: str, user: str) -> dict[str, Any]: ...


class OpenAIJsonLlm:
    def __init__(self, client: Any, model_id: str = DEFAULT_MODEL) -> None:
        self._client = client
        self.model_id = model_id

    def complete_json(self, system: str, user: str) -> dict[str, Any]:
        resp = self._client.chat.completions.create(
            model=self.model_id,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        try:
            data = json.loads(resp.choices[0].message.content or "{}")
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}
