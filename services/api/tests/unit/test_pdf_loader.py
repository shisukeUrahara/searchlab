from searchlab.corpus.chunker import pack_lines
from searchlab.corpus.pdf_loader import (
    Marker,
    join_pages,
    outline_markers,
    page_of,
    regex_markers,
    split_sections,
    strip_running_lines,
)


def test_running_headers_and_page_numbers_removed() -> None:
    words = "alpha beta gamma delta epsilon zeta eta theta iota".split()
    pages = [f"NASA HANDBOOK\nBody {w}\nPage {i} of 9\n{i}" for i, w in enumerate(words, 1)]
    out = strip_running_lines(pages)
    assert all("NASA HANDBOOK" not in p and "Page" not in p for p in out)
    assert out[2] == "Body gamma"


def test_repeated_body_tags_survive() -> None:
    body = "\n".join(f"filler line {c}" for c in "abcdefgh")
    pages = [f"top {w}\n{body}\n5.3.{i} The manager shall do x.\n[SWE-0{i}8]\n{body}\nend {w}"
             for i, w in enumerate("abcdefghij")]
    out = strip_running_lines(pages)
    assert all("[SWE-" in p for p in out)


def test_rare_lines_are_kept() -> None:
    pages = ["Unique A\nShared", "Unique B\nShared", "Unique C", "Unique D", "Unique E",
             "Unique F", "Unique G", "Unique H", "Unique I", "Unique J"]
    out = strip_running_lines(pages)
    assert "Shared" in out[0]  # only on 2 of 10 pages


def test_regex_headings_skip_three_level_requirements() -> None:
    text = "Chapter 6. Systems Engineering\n6.1 Plan Function\n6.1.1 A SEMP is used to x.\nbody"
    heads = [m.heading for m in regex_markers(text)]
    assert heads == ["Chapter 6. Systems Engineering", "6.1 Plan Function"]


def test_split_sections_and_pages() -> None:
    text, starts = join_pages(["1.0 Intro\nhello", "2.0 Next\nworld"])
    secs = split_sections(text, [Marker(0, "1.0 Intro"), Marker(starts[1], "2.0 Next")], starts)
    assert [(s.heading, s.text, s.page) for s in secs] == [
        ("1.0 Intro", "hello", 1),
        ("2.0 Next", "world", 2),
    ]


def test_outline_builds_paths_and_skips_front_matter() -> None:
    text, starts = join_pages(["Table of Contents\n...", "3.0 Life Cycle\nA\n3.1 Programs\nB"])
    entries = [(0, "Table of Contents", 0), (0, "3.0 Life Cycle", 1), (1, "3.1 Programs", 1)]
    markers = outline_markers(entries, text, starts)
    assert [m.heading for m in markers] == ["3.0 Life Cycle", "3.0 Life Cycle > 3.1 Programs"]
    assert markers[1].offset > markers[0].offset  # found inside the page, not page start
    assert page_of(markers[1].offset, starts) == 2


def test_pack_lines_respects_cap_and_keeps_all_text() -> None:
    text = "\n".join(f"line {i} " + "x" * 50 for i in range(100))
    parts = pack_lines(text, 300)
    assert all(len(p) <= 300 for p in parts)
    assert "\n".join(parts) == text
