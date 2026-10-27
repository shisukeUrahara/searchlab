"""Turn a github/docs Markdown file into plain Markdown for the github.com (fpt) view.

Handles: YAML frontmatter, Liquid {% ifversion %}/{% else %}/{% endif %} blocks,
{% data variables.* %} substitution, and drops {% data reusables.* %} (external files).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_TAG = re.compile(r"\{%-?\s*(.*?)\s*-?%\}", re.DOTALL)
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# Features true for the github.com (Free/Pro/Team) view of the docs.
ACTIVE_FEATURES = frozenset({"fpt"})

VARIABLES = {
    "product.company_short": "GitHub",
    "product.github": "GitHub",
    "product.prodname_dotcom": "GitHub",
    "product.prodname_github_app": "GitHub App",
    "product.prodname_github_apps": "GitHub Apps",
    "product.prodname_oauth_app": "OAuth app",
    "product.prodname_oauth_apps": "OAuth apps",
    "product.prodname_actions": "GitHub Actions",
    "product.prodname_ghe_cloud": "GitHub Enterprise Cloud",
    "product.prodname_free_user": "GitHub Free",
    "product.pat_generic": "personal access token",
    "product.pat_generic_plural": "personal access tokens",
    "product.rest_url": "https://api.github.com",
}


@dataclass(frozen=True)
class CleanedDoc:
    title: str
    body: str
    dropped_reusables: int


def _eval_condition(cond: str) -> bool:
    """Evaluate `fpt or ghec`, `not ghes`, `fpt and foo` against ACTIVE_FEATURES (left to right)."""
    result = False
    op = "or"
    negate = False
    for tok in cond.split():
        if tok in ("or", "and"):
            op = tok
        elif tok == "not":
            negate = True
        else:
            val = (tok in ACTIVE_FEATURES) != negate
            negate = False
            result = (result or val) if op == "or" else (result and val)
    return result


def _frontmatter_title(text: str) -> tuple[str, str]:
    m = _FRONTMATTER.match(text)
    if not m:
        return "", text
    title = ""
    for line in m.group(1).splitlines():
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip("'\"")
    return title, text[m.end():]


def _resolve_blocks(text: str) -> tuple[str, int]:
    """Walk tags once; keep text only when every enclosing ifversion is active."""
    out: list[str] = []
    stack: list[tuple[bool, bool]] = []  # (a branch already taken, parent_active)
    active = True
    dropped = 0
    pos = 0
    for m in _TAG.finditer(text):
        if active:
            out.append(text[pos:m.start()])
        pos = m.end()
        tag = m.group(1)
        head = tag.split(None, 1)[0] if tag else ""
        if head in ("ifversion", "if"):
            parent = active
            cond = _eval_condition(tag.split(None, 1)[1]) if " " in tag else False
            stack.append((cond, parent))
            active = parent and cond
        elif head == "elsif" and stack:
            taken, parent = stack[-1]
            cond = not taken and _eval_condition(tag.split(None, 1)[1])
            stack[-1] = (taken or cond, parent)
            active = parent and cond
        elif head == "else" and stack:
            taken, parent = stack[-1]
            stack[-1] = (True, parent)
            active = parent and not taken
        elif head in ("endif", "endifversion") and stack:
            _, parent = stack.pop()
            active = parent
        elif head == "data":
            ref = tag.split(None, 1)[1].strip()
            if ref.startswith("variables."):
                if active:
                    out.append(VARIABLES.get(ref[len("variables."):], ref.rsplit(".", 1)[-1]))
            elif ref.startswith("reusables.") and active:
                dropped += 1
    if active:
        out.append(text[pos:])
    return "".join(out), dropped


def clean_markdown(raw: str) -> CleanedDoc:
    title, body = _frontmatter_title(raw)
    body, dropped = _resolve_blocks(body)
    body = re.sub(r"\[AUTOTITLE\]\(([^)]*)\)", lambda m: m.group(1), body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return CleanedDoc(title=title, body=body, dropped_reusables=dropped)
