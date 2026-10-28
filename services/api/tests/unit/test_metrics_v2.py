import math

import pytest

from searchlab.eval.bootstrap import bootstrap_ci
from searchlab.eval.metrics import first_gold_rank, ndcg_at_k, recall_curve


def test_first_gold_rank() -> None:
    assert first_gold_rank(["a", "b", "c"], {"c"}) == 3
    assert first_gold_rank(["a"], {"z"}) is None


def test_ndcg_hand_computed() -> None:
    # one gold at rank 2: (1/log2 3) / (1/log2 2)
    assert ndcg_at_k(["x", "g"], {"g"}, 10) == pytest.approx(1 / math.log2(3))
    # two golds at ranks 1 and 3, ideal ranks 1 and 2
    got = ndcg_at_k(["g1", "x", "g2"], {"g1", "g2"}, 10)
    assert got == pytest.approx((1 + 1 / math.log2(4)) / (1 + 1 / math.log2(3)))
    assert ndcg_at_k(["g"], {"g"}, 10) == 1.0
    assert ndcg_at_k([], set(), 10) == 0.0


def test_recall_curve_is_monotonic_and_correct() -> None:
    curve = recall_curve([1, 3, None, 10], k_max=10)
    assert curve[0] == 0.25 and curve[2] == 0.5 and curve[9] == 0.75
    assert all(a <= b for a, b in zip(curve, curve[1:], strict=False))


def test_bootstrap_ci_reproducible_and_brackets_mean() -> None:
    values = [0, 1, 1, 0.5, 0.25, 1, 0, 1, 0.33, 0.5]
    lo, hi = bootstrap_ci(values)
    assert (lo, hi) == bootstrap_ci(values)
    assert lo <= sum(values) / len(values) <= hi
    assert bootstrap_ci([0.7] * 20) == pytest.approx((0.7, 0.7))
    assert bootstrap_ci([]) == (0.0, 0.0)
