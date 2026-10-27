# SearchLab

Search debugger for developer docs. Run one query through **BM25**, **dense (vector)** and **hybrid (RRF)** retrieval and compare the rankings side by side. A labeled query set scores each method with Recall@5 and MRR@10.

> Status: early scaffold. No results yet. Every number published here will come from a saved, reproducible run.

## Disclaimer
Independent portfolio project. Not affiliated with or endorsed by GitHub. Indexed text comes from selected pages of [github/docs](https://github.com/github/docs) (CC BY 4.0). See [NOTICE.md](NOTICE.md).

## Planned layout
- `apps/web` - Next.js UI (three-column ranking view, eval report)
- `services/api` - FastAPI search + eval service
- `fixtures/github-docs` - pinned doc snapshot, source manifest, labeled queries
- `docs` - decisions and build log

## Checkpoints
- [ ] SL-1 Source manifest + UI states + 30 labeled questions
- [ ] SL-2 BM25 vs dense on identical queries
- [ ] SL-3 Hybrid + held-out eval report
