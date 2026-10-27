# 0003 Evaluation protocol

**Decision.** 45 labeled queries in two splits: 15 dev (tuning allowed), 30 test (frozen, run once). Classes: exact_id, paraphrase, distractor. Metrics: Recall@5 (any gold chunk in top 5) and MRR@10. RRF k is chosen on dev only.

**Findings that shaped the write-up.**
- RRF k in {10, 30, 60, 100} gave identical dev scores, so the default 60 was kept.
- Recall@5 hit 1.0 for all methods on test. The corpus is too small for it to discriminate. MRR@10 is the usable signal.
- Metric choice was fixed before the test run. No metric was added afterward.

**Limits.** N=30, no confidence intervals, one repetition, synthetic queries, multi-chunk gold labels.
