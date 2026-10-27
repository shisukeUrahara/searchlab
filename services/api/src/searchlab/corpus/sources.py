"""The pinned corpus definition. Change the SHA or paths only with a new snapshot."""
from __future__ import annotations

REPO = "github/docs"
PINNED_SHA = "9568e964d18d76267faf57050dc662c450a13214"
LICENSE = "CC BY 4.0 (content), per github/docs repository"
TRANSFORMATION = "frontmatter removed; github.com (fpt) Liquid branches kept; reusables dropped"

PATHS = (
    "content/rest/using-the-rest-api/rate-limits-for-the-rest-api.md",
    "content/rest/using-the-rest-api/using-pagination-in-the-rest-api.md",
    "content/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app.md",
    "content/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation.md",
    "content/webhooks/using-webhooks/handling-webhook-deliveries.md",
    "content/webhooks/using-webhooks/validating-webhook-deliveries.md",
)


def source_id(path: str) -> str:
    return "github-docs/" + path.rsplit("/", 1)[-1].removesuffix(".md")


def docs_url(path: str) -> str:
    return "https://docs.github.com/en/" + path.removeprefix("content/").removesuffix(".md")


def raw_url(path: str, sha: str = PINNED_SHA) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{sha}/{path}"
