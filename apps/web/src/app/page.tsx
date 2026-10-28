"use client";
import { useCallback, useEffect, useState } from "react";
import { api, METHODS, METHOD_LABEL, type LabeledQuery, type Method, type SearchResponse } from "@/lib/api";
import { ChunkDrawer } from "@/components/ChunkDrawer";
import { RankingColumn } from "@/components/RankingColumn";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";

type State =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "error"; error: unknown }
  | { kind: "done"; response: SearchResponse };

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [state, setState] = useState<State>({ kind: "idle" });
  const [labeled, setLabeled] = useState<LabeledQuery[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  const [tab, setTab] = useState<Method>("hybrid");

  const run = useCallback(
    async (q: string, k: number) => {
      if (!q.trim()) return;
      setQuery(q);
      setState({ kind: "loading" });
      try {
        setState({ kind: "done", response: await api.search(q, k) });
      } catch (error) {
        setState({ kind: "error", error });
      }
    },
    [],
  );

  useEffect(() => {
    Promise.all([api.queries("dev"), api.queries("test")])
      .then(([dev, test]) => setLabeled([...dev.items, ...test.items]))
      .catch(() => setLabeled([]));
    const q = new URLSearchParams(window.location.search).get("q");
    const timer = q ? setTimeout(() => void run(q, 5), 0) : undefined;
    return () => clearTimeout(timer);
  }, [run]);

  const gold = labeled.find((l) => l.text === query.trim())?.gold_chunk_ids ?? [];
  const suggestions = labeled.filter((l) => l.query_class === "exact_id").slice(0, 6);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Compare retrieval methods</h1>
        <p className="mt-1 text-sm text-muted">
          One query, three rankings, same 78 chunks of GitHub Docs. Pick a labeled query to see which method found the expected chunk.
        </p>
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          void run(query, topK);
        }}
        className="rounded-lg border border-line bg-surface p-4"
      >
        <label htmlFor="q" className="text-sm font-medium">Question or error string</label>
        <div className="mt-1 flex flex-col gap-3 md:flex-row">
          <input
            id="q"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="x-ratelimit-remaining"
            maxLength={500}
            className="flex-1 rounded-md border border-line bg-canvas px-3 py-2 font-mono text-sm"
          />
          <label className="flex items-center gap-2 text-sm">
            top-k
            <input
              type="range" min={1} max={10} value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              aria-label="top-k"
            />
            <span className="w-4 font-mono">{topK}</span>
          </label>
          <button
            type="submit"
            disabled={!query.trim() || state.kind === "loading"}
            className="rounded-md bg-primary px-5 py-2 text-sm font-medium text-primary-ink disabled:opacity-50"
          >
            Search
          </button>
        </div>
        {suggestions.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2" aria-label="Example queries">
            {suggestions.map((s) => (
              <button
                key={s.query_id}
                type="button"
                onClick={() => { setQuery(s.text); void run(s.text, topK); }}
                className="rounded-full border border-line px-3 py-1 font-mono text-xs hover:bg-canvas"
              >
                {s.text}
              </button>
            ))}
          </div>
        )}
      </form>

      {state.kind === "idle" && <Empty title="No search yet" hint="Type a query or click an example above." />}
      {state.kind === "loading" && <Loading label="Searching" />}
      {state.kind === "error" && <ErrorBox error={state.error} onRetry={() => run(query, topK)} />}
      {state.kind === "done" && (
        <>
          <div role="tablist" aria-label="Method" className="flex gap-2 md:hidden">
            {METHODS.map((m) => (
              <button
                key={m} role="tab" aria-selected={tab === m} onClick={() => setTab(m)}
                className={`rounded-md px-3 py-1.5 text-sm ${tab === m ? "bg-primary text-primary-ink" : "border border-line"}`}
              >
                {METHOD_LABEL[m].split(" ")[0]}
              </button>
            ))}
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {state.response.results.map((r) => (
              <div key={r.method} className={tab === r.method ? "" : "hidden md:block"}>
                <RankingColumn result={r} goldIds={gold} onOpen={setOpen} />
              </div>
            ))}
          </div>
          <p className="font-mono text-xs text-muted">request_id {state.response.request_id}</p>
        </>
      )}
      {open && <ChunkDrawer chunkId={open} onClose={() => setOpen(null)} />}
    </div>
  );
}
