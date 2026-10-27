"""Tokenizer that keeps API identifiers whole AND searchable by their parts.

`x-ratelimit-remaining` -> ["x-ratelimit-remaining", "x", "ratelimit", "remaining"]
"""
from __future__ import annotations

import re

_COMPOUND = re.compile(r"[a-z0-9_]+(?:[-.][a-z0-9_]+)*=?")
_PART = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for compound in _COMPOUND.findall(text.lower()):
        tokens.append(compound)
        parts = _PART.findall(compound)
        if len(parts) > 1 or parts != [compound]:
            tokens.extend(parts)
    return tokens
