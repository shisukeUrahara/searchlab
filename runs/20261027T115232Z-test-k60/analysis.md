# Test-split analysis (N=30, frozen, run once)

Config: 78 chunks from 6 pinned GitHub Docs pages, OpenAI text-embedding-3-small, RRF k=60 (k made no difference on the dev split).

| method | Recall@5 | MRR@10 |
|---|---|---|
| bm25 | 1.000 | 0.747 |
| dense | 1.000 | 0.794 |
| hybrid | 1.000 | 0.856 |

## What this does and does not show
- Recall@5 is saturated (1.0 for all). With only 78 chunks, the top 5 is about 6% of the corpus, so this metric cannot separate the methods here. A larger corpus is needed.
- MRR@10 separates them: hybrid > dense > bm25. N=30 is small, so differences of a few hundredths are not reliable. No confidence intervals were computed.
- Hypothesis "dense retrieval misses exact identifiers" was NOT supported. Dense ranked `X-Hub-Signature-256` and `sha256=` first where BM25 ranked them 4th. BM25 won on `secure_compare`, `x-ratelimit-used`, `x-ratelimit-resource`.
- Hybrid was never the worst method on any differing test case, and never ranked a gold chunk lower than 3rd.

## Caveats
- Queries are synthetic, written by the author with model assistance, then keyword-checked against gold chunks.
- Gold labels allow several chunks for some queries, which raises scores.
- Chunking, tokenizer and the embedding text (heading + body) were fixed before the test run.
- One run, one repetition. Embedding vectors are cached in `fixtures/github-docs/embeddings_cache/`.
