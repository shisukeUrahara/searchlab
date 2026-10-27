from searchlab.corpus.chunker import MAX_CHARS, chunk_document

BODY = """Intro text.

## Primary limits

Five thousand per hour.

### Headers

Look at `x-ratelimit-remaining`.

```
# not a heading
```

## Secondary limits

Wait for `retry-after`.
"""


def run(body: str = BODY) -> list:
    return chunk_document("s1", "Rate limits", "https://x/y", body)


def test_splits_on_headings_and_builds_path() -> None:
    headings = [c.heading for c in run()]
    assert headings == [
        "Rate limits",
        "Primary limits",
        "Primary limits > Headers",
        "Secondary limits",
    ]


def test_code_fence_hash_is_not_a_heading() -> None:
    headers_chunk = run()[2]
    assert "# not a heading" in headers_chunk.text


def test_ids_are_stable_and_unique() -> None:
    a, b = run(), run()
    assert [c.chunk_id for c in a] == [c.chunk_id for c in b]
    assert len({c.chunk_id for c in a}) == len(a)


def test_changed_text_changes_only_that_chunk_id() -> None:
    before = {c.heading: c.chunk_id for c in run()}
    after = {c.heading: c.chunk_id for c in run(BODY.replace("Five thousand", "Ten thousand"))}
    changed = [h for h in before if before[h] != after[h]]
    assert changed == ["Primary limits"]


def test_long_sections_split_on_paragraph_boundaries() -> None:
    para = "word " * 100
    body = "## Big\n\n" + "\n\n".join([para.strip()] * 6)
    chunks = chunk_document("s1", "T", "u", body)
    assert len(chunks) > 1
    assert all(len(c.text) <= MAX_CHARS for c in chunks)
    assert all(c.heading == "Big" for c in chunks)
