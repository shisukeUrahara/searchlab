from searchlab.domain.models import Chunk, LabeledQuery
from searchlab.labeling.review import apply_review, parse_sheet, pick_for_review, render_sheet

A, B = "a" * 16, "b" * 16
CHUNKS = {cid: Chunk(chunk_id=cid, source_id="s", title="T", heading=f"H{cid[0]}", text="txt",
                     url="u", page=3) for cid in (A, B)}
QS = [
    LabeledQuery(query_id="n001", text="q1", query_class="paraphrase", split="test",
                 gold_chunk_ids=(A, B)),
    LabeledQuery(query_id="n002", text="q2", query_class="exact_id", split="dev",
                 gold_chunk_ids=(B,)),
]


def test_roundtrip_untouched_sheet_is_full_agreement() -> None:
    res = parse_sheet(render_sheet(QS, CHUNKS))
    assert res.checked == 3 and res.wrong == [] and res.agreement == 1.0


def test_ticked_boxes_become_wrong_labels_and_are_removed() -> None:
    sheet = render_sheet(QS, CHUNKS)
    sheet = sheet.replace(f"- [ ] wrong · n001 · {B}", f"- [x] wrong · n001 · {B}")
    sheet = sheet.replace(f"- [ ] wrong · n002 · {B}", f"- [X] wrong · n002 · {B}")
    res = parse_sheet(sheet)
    assert res.wrong == [("n001", B), ("n002", B)]
    assert round(res.agreement, 3) == 0.333
    fixed = apply_review(QS, res.wrong)
    assert [(q.query_id, q.gold_chunk_ids) for q in fixed] == [("n001", (A,))]


def test_pick_is_seeded() -> None:
    assert pick_for_review(QS, 1, seed=3) == pick_for_review(QS, 1, seed=3)
