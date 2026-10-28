"""Read saved run folders and derive chart data (recall curves, head-to-head wins)."""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

from searchlab.eval.metrics import first_gold_rank, recall_curve
from searchlab.eval.naming import run_label

K_MAX = 10


class RunNotFoundError(LookupError):
    pass


def _manifest(run_dir: Path) -> dict[str, Any]:
    m: dict[str, Any] = json.loads((run_dir / "run_manifest.json").read_text())
    m.setdefault("label", run_label("", m["split"], m["rrf_k"], m["created_at_utc"]))
    return m


def list_runs(runs_dir: Path) -> list[dict[str, Any]]:
    if not runs_dir.exists():
        return []
    runs = []
    for d in runs_dir.iterdir():
        if (d / "run_manifest.json").exists():
            m = _manifest(d)
            runs.append({"id": d.name, "label": m["label"], "split": m["split"],
                         "created": m["created_at_utc"], "n": m["sample_count"]})
    return sorted(runs, key=lambda r: r["created"], reverse=True)


def _first_ranks(cases: list[dict[str, Any]]) -> dict[str, dict[str, int | None]]:
    """method -> query_id -> rank of first gold chunk (None if not in the top 10)."""
    out: dict[str, dict[str, int | None]] = {}
    for c in cases:
        rank = first_gold_rank(c["ranked_chunk_ids"], set(c["gold_chunk_ids"]))
        out.setdefault(c["method"], {})[c["query_id"]] = rank
    return out


def head_to_head(ranks: dict[str, dict[str, int | None]]) -> list[dict[str, Any]]:
    """For each method pair, count queries where A ranks the first gold chunk higher, tie, or B."""
    big = K_MAX + 1
    rows = []
    for a, b in combinations(ranks, 2):
        wins = ties = losses = 0
        for qid, ra in ranks[a].items():
            x, y = ra or big, ranks[b].get(qid) or big
            wins += x < y
            ties += x == y
            losses += x > y
        rows.append({"a": a, "b": b, "a_better": wins, "tie": ties, "b_better": losses})
    return rows


def load_run(runs_dir: Path, run_id: str) -> dict[str, Any]:
    run_dir = runs_dir / run_id
    if "/" in run_id or ".." in run_id or not (run_dir / "run_manifest.json").is_file():
        raise RunNotFoundError(run_id)
    cases = [json.loads(x) for x in (run_dir / "per_case_results.jsonl").read_text().splitlines()]
    ranks = _first_ranks(cases)
    return {
        "manifest": _manifest(run_dir),
        "scores": json.loads((run_dir / "scores.json").read_text()),
        "cases": cases,
        "curves": {m: recall_curve(list(r.values()), K_MAX) for m, r in ranks.items()},
        "head_to_head": head_to_head(ranks),
    }
