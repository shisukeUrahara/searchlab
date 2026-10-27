# Build log

- **Corpus.** Pinned 6 pages at one commit, manifest with sha256. Rebuilding chunks twice gives byte-identical output.
- **Queries.** 45 drafted, each keyword-checked against its gold chunks. Reviewed by hand via `docs/query_review.md`.
- **BM25 vs dense.** On `X-Hub-Signature-256`, BM25 ranked the expected chunk 4th, dense 1st, hybrid 2nd. This contradicted the starting hypothesis.
- **Tuning.** RRF k had no effect on dev.
- **Test run.** Recall@5 = 1.0 everywhere (saturated). MRR@10: hybrid 0.856, dense 0.794, BM25 0.747.
- **Bugs found by testing.** `else` after a true `elsif` branch was rendered (fixed, regression test added). Uncached query with no key returned 500 (now 503 `embedding_unavailable`). `.env` could be copied into the API image (fixed with `Dockerfile.dockerignore`). CI typecheck failed on a clean checkout because Next generates `LayoutProps` (typecheck now runs `next typegen`).
