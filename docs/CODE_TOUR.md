# Code tour

Read in this order. Each step is small and has tests next to it in `services/api/tests/`.

## 1. The data types (5 min)
`services/api/src/searchlab/domain/`
- `models.py`: `Chunk` (a piece of a doc page), `ScoredChunk` (a chunk plus score and rank), `LabeledQuery` (a question with the right chunk IDs).
- `ports.py`: three small interfaces. `Retriever.search(query, top_k)`, `Embedder.embed(texts)`, `VectorStore.upsert/query`. Everything else plugs into these. This is the "D" in SOLID: code depends on the interface, not on OpenAI or Qdrant.

## 2. Turning docs into chunks (15 min)
`corpus/`
- `sources.py`: the 6 pinned pages and the commit SHA.
- `clean.py`: removes GitHub's template tags (`{% ifversion %}` etc.). Read `_resolve_blocks`. It walks tags with a stack.
- `chunker.py`: splits at headings, makes the chunk ID by hashing the text. Same text gives the same ID.
- `manifest.py`: records a checksum per file. `verify_manifest` finds tampering.
- `pipeline.py`: glues fetch, clean, chunk together. Network access is passed in, so tests use a fake.
- `cli.py`: `searchlab fetch | chunk | verify`.

## 3. Three ways to search (20 min)
`retrieval/`
- `tokenize.py`: keeps `x-ratelimit-remaining` whole and also as parts. See ADR 0002.
- `bm25.py`: word matching. Returns only chunks that share a word with the query.
- `dense.py`: turns text into a vector (a list of numbers that captures meaning) and finds the nearest chunk vectors.
- `hybrid.py`: Reciprocal Rank Fusion. Each method gives a rank. A chunk gets `1/(60+rank)` from each list. Add them up. Chunks that appear in both lists rise.

Supporting pieces:
- `embeddings/openai_embedder.py`: calls OpenAI in batches.
- `embeddings/cache.py`: remembers every vector on disk, so repeat runs are free and work without a key.
- `store/qdrant_store.py`: saves and queries vectors.

## 4. Measuring (10 min)
`eval/`
- `metrics.py`: `hit_at_k` and `reciprocal_rank_at_k`. Plain functions, easy to check by hand.
- `runner.py`: runs every method on every query, then averages. Overall and per class.
- `artifacts.py`: writes the run folder (manifest, per-case rows, scores, chart, checksums).
- `queries.py`: loads the labeled queries.

## 5. Putting it together (10 min)
- `wiring.py`: the only file that chooses real classes (OpenAI, Qdrant, BM25). Change the setup here.
- `services/search_service.py`, `services/eval_service.py`: the two use cases. The CLI and the API both call them.
- `api/app.py`: HTTP routes. `api/errors.py`: every error looks like `{code, message, request_id}`.
- `cli.py`: `search`, `tune`, `eval`.

## 6. The web app (15 min)
`apps/web/src/`
- `lib/api.ts`: the one place that calls the API. Turns network failures into readable errors.
- `app/page.tsx`: the search page. A small state machine: idle, loading, error, done.
- `components/RankingColumn.tsx`: one column. Shows a green banner when the expected chunk was found.
- `components/ChunkDrawer.tsx`: side panel. Esc closes it. Focus moves into it.
- `app/eval/page.tsx`: run picker, metric table, and the queries where methods disagree.

## Trace one query
You type `X-Hub-Signature-256` and press Search.
1. `page.tsx` calls `api.search` → `POST /search`.
2. `api/app.py` validates the body, then calls `SearchService.search`.
3. For each method, `search_service.py` times `retriever.search`.
4. BM25 tokenizes the query and scores chunks. Dense embeds the query (cache first) and asks Qdrant for neighbors. Hybrid asks both and fuses.
5. The API returns three ranked lists plus latency and a `request_id`.
6. `RankingColumn` draws each list. If the text matches a labeled query, the expected chunk is highlighted.

## Why the tests are shaped this way
- Pure functions (metrics, tokenizer, RRF) have hand-computed expected values.
- Anything with I/O takes its dependency as an argument, so tests pass a fake (`FakeEmbedder`, in-memory Qdrant, fake fetcher).
- `tests/integration/` runs the whole API and the eval service without a network.
