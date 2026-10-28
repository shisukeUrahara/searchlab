"use client";
import { Network, Search, SearchCode } from "lucide-react";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ChunkDrawer } from "@/components/ChunkDrawer";
import { MethodColumn } from "@/components/search/MethodColumn";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";
import {
  api,
  METHODS,
  METHOD_META,
  type Chunk,
  type Corpus,
  type LabeledQuery,
  type Method,
  type SearchResponse,
} from "@/lib/api";

type State =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "error"; error: unknown }
  | { kind: "done"; response: SearchResponse };

const CHIP_COUNT = 6;

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [state, setState] = useState<State>({ kind: "idle" });
  const [labeled, setLabeled] = useState<LabeledQuery[]>([]);
  const [corpus, setCorpus] = useState<Corpus | null>(null);
  const [target, setTarget] = useState<Chunk | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  const [tab, setTab] = useState<Method>("hybrid");

  const run = useCallback(async (q: string, k: number) => {
    if (!q.trim()) return;
    setQuery(q);
    setState({ kind: "loading" });
    try {
      setState({ kind: "done", response: await api.search(q, k) });
    } catch (error) {
      setState({ kind: "error", error });
    }
  }, []);

  useEffect(() => {
    api.corpus().then(setCorpus).catch(() => setCorpus(null));
    Promise.all([api.queries("dev"), api.queries("test")])
      .then(([dev, test]) => setLabeled([...dev.items, ...test.items]))
      .catch(() => setLabeled([]));
    const q = new URLSearchParams(window.location.search).get("q");
    const timer = q ? setTimeout(() => void run(q, 5), 0) : undefined;
    return () => clearTimeout(timer);
  }, [run]);

  const searched = state.kind === "done" ? state.response.query : "";
  const match = labeled.find((l) => l.text === searched);
  const gold = useMemo(() => match?.gold_chunk_ids ?? [], [match]);

  useEffect(() => {
    if (!gold.length) return;
    let live = true;
    api.chunk(gold[0]).then((c) => live && setTarget(c)).catch(() => live && setTarget(null));
    return () => {
      live = false;
    };
  }, [gold]);

  const docNumbers = Object.fromEntries((corpus?.docs ?? []).map((d) => [d.source_id, d.doc_number]));
  const chips = useMemo(() => {
    const exact = labeled.filter((l) => l.split === "dev" && l.query_class === "exact_id");
    const other = labeled.filter((l) => l.split === "dev" && l.query_class !== "exact_id");
    return [...exact.slice(0, 4), ...other.slice(0, CHIP_COUNT - 4)];
  }, [labeled]);

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold md:text-4xl">Compare retrieval methods</h1>
          <p className="mt-2 text-muted">
            One query, three rankings. Keyword, vector and hybrid search over{" "}
            {corpus ? corpus.chunk_count.toLocaleString() : "…"} passages from five NASA engineering handbooks.
          </p>
        </div>
        {corpus && (
          <p className="flex flex-wrap items-center gap-x-2 gap-y-1 rounded-full border border-line bg-surface px-4 py-1.5 font-mono text-xs text-muted">
            <span className="size-1.5 rounded-full bg-primary" aria-hidden />
            {corpus.docs.length} handbooks <span aria-hidden>/</span> {corpus.chunk_count.toLocaleString()} passages
            <span aria-hidden>/</span> {corpus.embedding_dims}-dim vectors
          </p>
        )}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          void run(query, topK);
        }}
        className="rounded-2xl border border-line bg-surface p-4 shadow-card md:p-6"
      >
        <label htmlFor="q" className="sr-only">
          Question or identifier
        </label>
        <div className="flex items-center gap-3 rounded-xl border border-line bg-canvas px-4 transition-shadow focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/25">
          <SearchCode className="size-5 shrink-0 text-muted" aria-hidden />
          <input
            id="q"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask the handbooks, or type an identifier like KDP C or SWE-139"
            maxLength={500}
            autoComplete="off"
            className="h-12 min-w-0 flex-1 bg-transparent text-base outline-none placeholder:text-muted focus-visible:outline-none"
          />
          {match && searched === query && (
            <span className="hidden rounded-md border border-line px-2 py-0.5 font-mono text-xs text-muted sm:inline">
              {match.query_id}
            </span>
          )}
        </div>
        <div className="mt-4 flex flex-col gap-3 md:flex-row md:items-center">
          <label className="flex items-center gap-3 font-mono text-xs text-muted">
            Depth
            <input
              type="range"
              min={1}
              max={10}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              aria-label="Results per method"
              className="w-32 accent-[var(--primary)]"
            />
            <span className="w-12 text-ink">top-{topK}</span>
          </label>
          <div className="flex gap-2 md:ml-auto">
            <Link
              href={searched ? `/map?q=${encodeURIComponent(searched)}` : "/map"}
              className="inline-flex h-10 flex-1 items-center justify-center gap-2 rounded-lg border border-line px-4 text-sm font-medium hover:bg-surface-2 md:flex-none"
            >
              <Network className="size-4" aria-hidden />
              <span className="sm:hidden">Map</span>
              <span className="hidden sm:inline">Show on vector map</span>
            </Link>
            <button
              type="submit"
              disabled={!query.trim() || state.kind === "loading"}
              className="inline-flex h-10 flex-1 items-center justify-center gap-2 rounded-lg bg-primary px-5 text-sm font-medium text-primary-ink transition hover:opacity-90 disabled:opacity-50 md:flex-none"
            >
              <Search className="size-4" aria-hidden /> Search
            </button>
          </div>
        </div>
        {chips.length > 0 && (
          <div className="mt-4 border-t border-line pt-4">
            <p className="mb-2 font-mono text-xs text-muted">Labeled examples (fills the box; press Search to run)</p>
            <div role="group" className="relative -mx-1 flex gap-2 overflow-x-auto px-1 pb-1 md:flex-wrap" aria-label="Example queries">
              {chips.map((c) => (
                <button
                  key={c.query_id}
                  type="button"
                  onClick={() => setQuery(c.text)}
                  className="shrink-0 rounded-full border border-line bg-surface-2 px-3 py-1.5 text-sm hover:border-primary/50"
                >
                  {c.text}
                </button>
              ))}
            </div>
          </div>
        )}
      </form>

      {state.kind === "idle" && <Empty title="No search yet" hint="Type a question or pick a labeled example, then press Search." />}
      {state.kind === "loading" && <Loading label="Searching three retrievers" />}
      {state.kind === "error" && <ErrorBox error={state.error} onRetry={() => run(query, topK)} />}
      {state.kind === "done" && (
        <section aria-label="Results" className="space-y-4">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 font-mono text-xs uppercase tracking-wide text-muted">
            <span>Retrieval channels (k = {state.response.results[0]?.hits.length ?? topK})</span>
            {match && target && (
              <span className="rounded-md border border-line px-2 py-0.5 normal-case tracking-normal">
                Expected: {docNumbers[target.source_id] ?? target.source_id} · {target.heading.split(" > ").pop()}
                {match.gold_chunk_ids.length > 1 ? ` (+${match.gold_chunk_ids.length - 1} more)` : ""}
              </span>
            )}
            <span className="ml-auto hidden gap-4 normal-case tracking-normal md:flex">
              {METHODS.map((m) => (
                <span key={m} className="inline-flex items-center gap-1.5">
                  <span className={`size-2 rounded-full ${METHOD_META[m].dot}`} aria-hidden />
                  {METHOD_META[m].short}
                </span>
              ))}
            </span>
          </div>
          <div role="tablist" aria-label="Method" className="grid grid-cols-3 gap-1 rounded-xl bg-surface-2 p-1 md:hidden">
            {METHODS.map((m) => (
              <button
                key={m}
                role="tab"
                aria-selected={tab === m}
                onClick={() => setTab(m)}
                className="rounded-lg py-2 text-sm aria-selected:bg-surface aria-selected:font-medium aria-selected:shadow-card"
              >
                {METHOD_META[m].short}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-1 gap-5 md:grid-cols-3">
            {state.response.results.map((r) => (
              <div key={r.method} className={`min-w-0 ${tab === r.method ? "" : "hidden md:block"}`}>
                <MethodColumn result={r} goldIds={gold} docNumbers={docNumbers} onOpen={setOpen} />
              </div>
            ))}
          </div>
          <p className="font-mono text-xs text-muted">request_id {state.response.request_id}</p>
        </section>
      )}

      {corpus && (
        <footer className="flex flex-wrap gap-x-6 gap-y-1 border-t border-line pt-4 font-mono text-xs text-muted">
          <span>Corpus: {corpus.label}</span>
          <span>Chunking: PDF sections, ≤1,000 chars</span>
          <span>Embedding: {corpus.embedding_model}</span>
        </footer>
      )}
      {open && <ChunkDrawer chunkId={open} onClose={() => setOpen(null)} />}
    </div>
  );
}
