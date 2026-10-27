from searchlab.corpus.clean import clean_markdown

DOC = """---
title: Rate limits
versions:
  fpt: '*'
---

{% ifversion ghes %}
Server only.
{% else %}
Cloud text for {% data variables.product.prodname_github_app %}.
{% endif %}

{% data reusables.rest-api.secondary-rate-limit-rest-graphql %}

Always shown.
"""


def test_title_from_frontmatter() -> None:
    assert clean_markdown(DOC).title == "Rate limits"


def test_ifversion_keeps_fpt_branch_only() -> None:
    body = clean_markdown(DOC).body
    assert "Server only" not in body
    assert "Cloud text for GitHub App." in body
    assert "Always shown." in body


def test_reusables_dropped_and_counted() -> None:
    doc = clean_markdown(DOC)
    assert "reusables" not in doc.body
    assert doc.dropped_reusables == 1


def test_nested_inactive_block_stays_hidden() -> None:
    raw = "{% ifversion ghes %}{% ifversion fpt %}x{% endif %}y{% endif %}z"
    assert clean_markdown(raw).body.strip() == "z"


def test_or_condition_and_elsif() -> None:
    raw = "{% ifversion ghec or fpt %}A{% elsif ghes %}B{% else %}C{% endif %}"
    assert clean_markdown(raw).body.strip() == "A"


def test_no_liquid_left_over_on_real_snapshot() -> None:
    from pathlib import Path

    snap = Path(__file__).resolve().parents[4] / "fixtures/github-docs/snapshot"
    for f in snap.glob("*.md"):
        body = clean_markdown(f.read_text()).body
        assert "{%" not in body and "%}" not in body, f.name
