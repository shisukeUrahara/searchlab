"use client";
import { useEffect, useState } from "react";
import { api, METHOD_LABEL, type EvalRun, type LabeledQuery, type RunSummary } from "@/lib/api";
import { MetricTable } from "@/components/MetricTable";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";

function rankOf(ids: string[], gold: string[]): number | null {
  const i = ids.findIndex((x) => gold.includes(x));
  return i === -1 ? null : i + 1;
}

export default function EvalPage() {
  const [runs, setRuns] = useState<RunSummary[] | null>(null);
  const [runId, setRunId] = useState("");
  const [run, setRun] = useState<{ id: string; data?: EvalRun; error?: unknown } | null>(null);
  const [queries, setQueries] = useState<Record<string, LabeledQuery>>({});
  const [error, setError] = useState<unknown>();

  useEffect(() => {
    Promise.all([api.runs(), api.queries("dev"), api.queries("test")])
      .then(([r, dev, test]) => {
        setRuns(r);
        setQueries(Object.fromEntries([...dev.items, ...test.items].map((q) => [q.query_id, q])));
        setRunId((r.find((x) => x.split === "test") ?? r[0])?.id ?? "");
      })
      .catch(setError);
  }, []);

  useEffect(() => {
    if (!runId) return;
    let live = true;
    api.run(runId)
      .then((data) => live && setRun({ id: runId, data }))
      .catch((e) => live && setRun({ id: runId, error: e }));
    return () => { live = false; };
  }, [runId]);

  if (error !== undefined) return <ErrorBox error={error} />;
  if (!runs) return <Loading />;
  if (runs.length === 0) return <Empty title="No eval runs yet" hint="Run: uv run searchlab eval --split dev" />;

  const ready = run?.id === runId;
  const m = run?.data?.manifest;
  const byQuery = new Map<string, Record<string, number | null>>();
  run?.data?.cases.forEach((c) => {
    const row = byQuery.get(c.query_id) ?? {};
    row[c.method] = rankOf(c.ranked_chunk_ids, c.gold_chunk_ids);
    byQuery.set(c.query_id, row);
  });
  const differing = [...byQuery].filter(([, r]) => new Set(Object.values(r)).size > 1);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Evaluation</h1>
      <label className="flex items-center gap-2 text-sm">
        Run
        <select value={runId} onChange={(e) => setRunId(e.target.value)} className="rounded-md border border-line bg-surface px-2 py-1 font-mono text-xs">
          {runs.map((r) => <option key={r.id} value={r.id}>{r.label}</option>)}
        </select>
      </label>
      {!ready && <Loading />}
      {ready && run?.error !== undefined && <ErrorBox error={run.error} />}
      {ready && run?.data && m && (
        <>
          <dl className="grid grid-cols-2 gap-3 rounded-lg border border-line bg-surface p-4 text-sm md:grid-cols-4">
            {[["Split", m.split], ["N queries", m.sample_count], ["RRF k", m.rrf_k], ["Embeddings", m.embedding_model], ["Chunks", m.chunk_count], ["Git SHA", String(m.git_sha ?? "n/a").slice(0, 8)], ["Dirty tree", String(m.git_dirty ?? "n/a")], ["Dataset sha", String(m.dataset_sha256).slice(0, 10)]].map(([k, v]) => (
              <div key={String(k)}><dt className="text-xs text-muted">{k}</dt><dd className="font-mono">{String(v)}</dd></div>
            ))}
          </dl>
          <MetricTable scores={run.data.scores} />
          <section>
            <h2 className="mb-2 font-semibold">Queries where methods differ (rank of first expected chunk)</h2>
            {differing.length === 0 ? <Empty title="All methods ranked every query the same" /> : (
              <div className="overflow-x-auto rounded-lg border border-line bg-surface">
                <table className="w-full text-sm">
                  <thead className="bg-canvas text-left text-xs uppercase text-muted">
                    <tr><th className="px-4 py-2">Query</th>{(["bm25", "dense", "hybrid"] as const).map((x) => <th key={x} className="px-4 py-2 text-right">{METHOD_LABEL[x].split(" ")[0]}</th>)}</tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {differing.map(([qid, r]) => (
                      <tr key={qid}>
                        <td className="px-4 py-2"><span className="font-mono text-xs text-muted">{qid}</span> {queries[qid]?.text}</td>
                        {(["bm25", "dense", "hybrid"] as const).map((x) => <td key={x} className="px-4 py-2 text-right font-mono">{r[x] ?? "miss"}</td>)}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
