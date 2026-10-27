"""Tiny .env loader and settings. No secrets are ever logged or committed."""
from __future__ import annotations

import os
from pathlib import Path


def load_env(path: Path) -> None:
    """Load KEY=VALUE lines into os.environ without overriding existing variables."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))
