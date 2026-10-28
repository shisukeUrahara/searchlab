"""Write a reproducible run folder: manifest, per-case rows, scores, chart, checksums."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from searchlab.eval.runner import CaseResult, ScoreRow  # noqa: E402


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state(repo: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo, capture_output=True, text=True, check=False
        ).stdout.strip()

    return {"git_sha": run("rev-parse", "HEAD"), "git_dirty": bool(run("status", "--porcelain"))}


def write_scores_csv(scores: Sequence[ScoreRow], path: Path) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        cols = ["recall_at_1", "recall_at_3", "recall_at_5", "recall_at_10", "mrr_at_10",
                "ndcg_at_10"]
        w.writerow(["method", "query_class", "n", *cols, "mrr_ci_low", "mrr_ci_high"])
        for s in scores:
            ci = s.mrr_ci or (float("nan"), float("nan"))
            w.writerow([s.method, s.query_class, s.n, *(f"{getattr(s, c):.4f}" for c in cols),
                        f"{ci[0]:.4f}", f"{ci[1]:.4f}"])


def write_chart(scores: Sequence[ScoreRow], path: Path, title: str) -> None:
    overall = [s for s in scores if s.query_class == "all"]
    names = [s.method for s in overall]
    fig, ax = plt.subplots(figsize=(6, 4), dpi=160)
    xs = range(len(names))
    ax.bar([x - 0.2 for x in xs], [s.recall_at_5 for s in overall], 0.4, label="Recall@5")
    ax.bar([x + 0.2 for x in xs], [s.mrr_at_10 for s in overall], 0.4, label="MRR@10")
    ax.set_xticks(list(xs), names)
    ax.set_ylim(0, 1)
    ax.set_title(f"{title} (N={overall[0].n})", fontsize=10)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_run(
    out_dir: Path,
    results: Sequence[CaseResult],
    scores: Sequence[ScoreRow],
    manifest: dict[str, Any],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out_dir / "per_case_results.jsonl").write_text(
        "".join(r.model_dump_json() + "\n" for r in results)
    )
    (out_dir / "scores.json").write_text(
        json.dumps([s.model_dump() for s in scores], indent=2) + "\n"
    )
    write_scores_csv(scores, out_dir / "scores.csv")
    write_chart(scores, out_dir / "chart.png", f"SearchLab {manifest['split']} split")
    lines = [f"{sha256_file(p)}  {p.name}" for p in sorted(out_dir.iterdir())
             if p.name != "checksums.txt"]
    (out_dir / "checksums.txt").write_text("\n".join(lines) + "\n")
