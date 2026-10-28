"""Human spot-check: a Markdown sheet with one checkbox per gold label; tick the wrong ones."""
from __future__ import annotations

import random
import re
from collections.abc import Sequence
from dataclasses import dataclass

from searchlab.domain.models import Chunk, LabeledQuery

_BOX = re.compile(r"^- \[(?P<mark>[ xX])\] wrong · (?P<qid>\w+) · (?P<cid>[0-9a-f]{16})\b")


@dataclass(frozen=True)
class ReviewResult:
    checked: int
    wrong: list[tuple[str, str]]

    @property
    def agreement(self) -> float:
        return 1 - len(self.wrong) / self.checked if self.checked else 0.0


def pick_for_review(queries: Sequence[LabeledQuery], n: int, seed: int) -> list[LabeledQuery]:
    return random.Random(seed).sample(list(queries), min(n, len(queries)))


def render_sheet(queries: Sequence[LabeledQuery], chunks: dict[str, Chunk]) -> str:
    lines = [
        "# Label spot-check",
        "",
        "For each query, read the passages listed as correct answers.",
        "Tick `[x]` on a line only if that passage does NOT answer the query.",
        "Leave the others as `[ ]`.",
        "Then run: `uv run searchlab --corpus nasa apply-review`.",
        "",
    ]
    for q in queries:
        lines += [f"## {q.query_id} · {q.query_class} · {q.split}", "", f"**Query:** {q.text}", ""]
        for cid in q.gold_chunk_ids:
            c = chunks[cid]
            snippet = " ".join(c.text.split())[:600]
            lines += [f"- [ ] wrong · {q.query_id} · {cid} · *{c.heading}* (p{c.page})",
                      f"  > {snippet}", ""]
    return "\n".join(lines) + "\n"


def parse_sheet(text: str) -> ReviewResult:
    checked, wrong = 0, []
    for line in text.splitlines():
        m = _BOX.match(line)
        if m:
            checked += 1
            if m["mark"].lower() == "x":
                wrong.append((m["qid"], m["cid"]))
    return ReviewResult(checked, wrong)


def apply_review(
    queries: Sequence[LabeledQuery], wrong: Sequence[tuple[str, str]]
) -> list[LabeledQuery]:
    """Remove wrong gold labels; drop queries left with no gold."""
    bad: dict[str, set[str]] = {}
    for qid, cid in wrong:
        bad.setdefault(qid, set()).add(cid)
    out: list[LabeledQuery] = []
    for q in queries:
        gold = tuple(c for c in q.gold_chunk_ids if c not in bad.get(q.query_id, set()))
        if gold:
            out.append(q.model_copy(update={"gold_chunk_ids": gold}))
    return out
