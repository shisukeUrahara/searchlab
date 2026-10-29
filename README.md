# SearchLab

**Compare keyword, vector and hybrid search on 3,203 passages from five NASA engineering handbooks, and measure which one finds the right answer.**

SearchLab runs one question through three retrievers and shows the rankings side by side. A labeled set of 120 questions scores each method, with 95% confidence intervals, and a WebGL map shows every passage in embedding space.

![Search page in dark mode on desktop and light mode on a phone](docs/img/search-dark-light.png)

> **Unofficial.** Independent portfolio project, not affiliated with or endorsed by NASA. The handbooks are US Government works (17 U.S.C. §105). See [NOTICE.md](NOTICE.md).

## What's inside

| Page | What it does |
|---|---|
| **Search** | One question, three ranked columns: **BM25** (keyword), **Dense** (vector, `text-embedding-3-small`) and **Hybrid** (Reciprocal Rank Fusion). For a labeled question it shows where each method placed the expected passage. |
| **Vector map** | All 3,203 passages as dots, placed by meaning (UMAP) and linked to their 5 nearest neighbours. A search lights up what each method retrieved. |
| **Evaluation** | Score cards (MRR@10 with 95% CI, Recall@1/5, nDCG@10), a Recall@k curve, results by question type, head-to-head counts and a per-question rank heatmap. Every number comes from a saved run folder. |
| **Queries** | The 120 labeled questions (40 tuning, 80 holdout), filterable and paginated. |
| **Sources** | The five NASA PDFs with page counts, checksums and how the corpus is built. |

Light and dark themes, mobile layouts and keyboard navigation throughout.

![Vector map of 3,203 passages, colored by document](docs/img/vector-map.png)

![MRR@10 by question type for BM25, vector and hybrid search](docs/img/eval-by-class.png)

## v1 (archived): GitHub Docs results

The first version used six GitHub Docs pages (78 chunks). It is kept for reproducibility under `fixtures/github-docs` and `runs/github-docs`.

### v1 results (frozen test split, N=30, run once)

| method | Recall@5 | MRR@10 |
|---|---|---|
| BM25 | 1.000 | 0.747 |
| Dense (`text-embedding-3-small`) | 1.000 | 0.794 |
| Hybrid (RRF, k=60) | 1.000 | 0.856 |

Run: [`runs/github-docs/20261027T115232Z-test-k60`](runs/github-docs/20261027T115232Z-test-k60) · analysis: [`analysis.md`](runs/github-docs/20261027T115232Z-test-k60/analysis.md)

**What this does and does not show**
- Recall@5 is saturated. The corpus has only 78 chunks, so the top 5 is about 6% of it. Use MRR@10 to compare methods here.
- N=30 is small. No confidence intervals were computed. Treat gaps of a few hundredths as noise.
- I expected dense search to miss exact API identifiers. **It did not.** Dense ranked `X-Hub-Signature-256` first where BM25 ranked it 4th, while BM25 won on `secure_compare` and `x-ratelimit-used`. Hybrid never ranked the first expected chunk below 3rd and was never strictly worse than both other methods (it tied the lowest rank on 3 queries).
- Queries are synthetic: written by the author with model help, then keyword-checked against their gold chunks. Some queries have more than one acceptable chunk.

## Quick start (Docker)

You need Docker with Compose v2.24 or newer. No API key is required: vectors for all 3,203 passages and all labeled questions are committed.

```bash
git clone https://github.com/shisukeUrahara/searchlab.git
cd searchlab

# Optional: add your OpenAI key so brand-new questions work in vector and hybrid search
cp services/api/.env.example services/api/.env   # then edit OPENAI_API_KEY

docker compose up --build
```

| Service | URL |
|---|---|
| Web app | http://localhost:3000 |
| API docs (OpenAPI) | http://localhost:8000/docs |

The API takes about 20 seconds on first start while it loads the vectors into Qdrant. Stop everything with `docker compose down`.

Ports bind to `127.0.0.1` only. Don't expose the API publicly with a key set: every new question calls the OpenAI embeddings API.

## Local development (without Docker)

You need Python 3.12 with [uv](https://docs.astral.sh/uv/), and Node 24 with pnpm 10.

**Terminal 1: API**

```bash
cd services/api
cp .env.example .env        # optional, then edit OPENAI_API_KEY
uv sync
uv run uvicorn searchlab.api.main:app --port 8000
```

**Terminal 2: web app**

```bash
cd apps/web
cp .env.example .env.local  # optional, defaults already point at localhost:8000
pnpm install
pnpm dev
```

Open http://localhost:3000. Without `QDRANT_URL`, the API keeps vectors in memory, so no Qdrant server is needed.

## Environment variables

| Variable | File | Default | What it does |
|---|---|---|---|
| `OPENAI_API_KEY` | `services/api/.env` | unset | Embeds new questions with `text-embedding-3-small`. Also needed to rebuild the corpus or labels. |
| `SEARCHLAB_CORPUS` | `services/api/.env` | `nasa` | Corpus to serve: `nasa`, or `github-docs` for the archived v1. |
| `QDRANT_URL` | `services/api/.env` | unset (in-memory) | Qdrant server to use. Docker Compose sets `http://qdrant:6333`. |
| `CORS_ORIGINS` | `services/api/.env` | `http://localhost:3000` | Comma-separated browser origins allowed to call the API. |
| `NEXT_PUBLIC_API_URL` | `apps/web/.env.local` | `http://localhost:8000` | Where the browser reaches the API. Read at build time. |
| `E2E_BASE_URL` | shell | `http://localhost:3000` | Web app URL for the Playwright tests. |

Both `.env` files are gitignored. Docker Compose reads `services/api/.env` when the container starts; it is never copied into the image.

### What works without a key

| Question | BM25 | Dense | Hybrid |
|---|---|---|---|
| A labeled example (vectors are committed) | yes | yes | yes |
| A brand-new question | yes | needs key | needs key |

Without a key, a new question still returns BM25 results. The Dense and Hybrid columns explain that an embedding is needed.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot reach the API" in the web app | Check the API is running: `curl localhost:8000/health`. In Docker, wait for the first start to finish. |
| Port 3000 or 8000 already in use | Find the process with `lsof -i :3000` and stop it, or stop old containers with `docker compose down`. |
| Web app on another port is blocked by CORS | Add its origin to `CORS_ORIGINS`, for example `http://localhost:3001`. |
| Changed `NEXT_PUBLIC_API_URL` but nothing changed | It is read at build time. Restart `pnpm dev`, or rebuild with `docker compose up --build`. |
| Vector map is blank | Your browser has WebGL turned off. Try Chrome or Firefox with hardware acceleration on. |
| Evaluation page says "No evaluation runs yet" | Create one: `cd services/api && uv run searchlab eval --split dev`. |

### Reproduce the evaluation

```bash
cd services/api
uv run searchlab verify              # snapshot files match manifest checksums
uv run searchlab tune                # RRF k on the DEV split only
uv run searchlab eval --split test   # writes runs/<run_id>/
```

Each run folder has `run_manifest.json` (git SHA, dataset/corpus/chunk checksums, embedding model, k, N), `per_case_results.jsonl`, `scores.csv`, `chart.png`, `checksums.txt`.

## How it works

```
Next.js UI ─HTTP→ FastAPI ─→ SearchService ─┬ Bm25Retriever
                                            ├ DenseRetriever ─→ Embedder (cached) + Qdrant
                                            └ HybridRetriever (RRF over the two)
```

- `corpus/`: fetch pinned pages, strip Liquid, chunk by heading, stable content-hash chunk IDs, checksummed manifest
- `retrieval/`: identifier-aware tokenizer, BM25, dense, RRF
- `embeddings/`: OpenAI adapter, disk cache decorator, fake embedder for tests
- `eval/`: pure metrics, runner, run artifacts
- `services/`, `api/`: use cases and HTTP layer; `wiring.py` is the only place that picks concrete classes

Design decisions: [`docs/adr/`](docs/adr/). Code walkthrough: [`docs/CODE_TOUR.md`](docs/CODE_TOUR.md).

## Tests

```bash
cd services/api && uv run pytest && uv run ruff check . && uv run mypy
cd apps/web && pnpm lint && pnpm typecheck && pnpm test
# browser smoke tests (API on :8000 and web on :3000 must be running)
pnpm exec playwright test
```

## Known limits
- 78 chunks from 6 pages. Results will not transfer to large corpora.
- No reranker, no query rewriting, one embedding model.
- Cleaning drops GitHub's shared `reusables` snippets (text lives in other files), so a few sections are shorter than on docs.github.com.
- UI was built by hand to a small design token set. A Google Stitch pass was attempted and could not authenticate.
