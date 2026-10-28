"use client";
import { CircleCheck, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { ClassBars } from "@/components/eval/ClassBars";
import { HeadToHead } from "@/components/eval/HeadToHead";
import { KpiCards } from "@/components/eval/KpiCards";
import { RankHeatmap } from "@/components/eval/RankHeatmap";
import { RecallCurve } from "@/components/eval/RecallCurve";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";
import { api, type EvalRun, type LabeledQuery, type RunSummary } from "@/lib/api";

function Card({ title, sub, children }: { title: string; sub?: string; children: ReactNode }) {
  return (
    <section className="rounded-2xl border border-line bg-surface p-5 shadow-card">
      <h2 className="text-lg font-semibold">{title}</h2>
      {sub && <p className="mt-0.5 text-sm text-muted">{sub}</p>}
      <div className="mt-4">{children}</div>
    </section>
  );
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
    return () => {
      live = false;
    };
  }, [runId]);

  if (error !== undefined) return <ErrorBox error={error} />;
  if (!runs) return <Loading label="Loading evaluation runs" />;
  if (runs.length === 0)
    return <Empty title="No evaluation runs yet" hint="Run: uv run searchlab eval --split dev" />;

  const ready = run?.id === runId;
  const d = ready ? run?.data : undefined;
  const m = d?.manifest;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold md:text-4xl">Evaluation</h1>
          <p className="mt-2 text-muted">
            Labeled queries scored for each method. Every number comes from a saved run folder in the repository.
          </p>
        </div>
        <label className="flex flex-col gap-1 text-sm lg:items-end">
          <span className="font-mono text-xs text-muted">Run</span>
          <select
            value={runId}
            onChange={(e) => setRunId(e.target.value)}
            className="h-10 max-w-full rounded-lg border border-line bg-surface px-3 text-sm"
          >
            {runs.map((r) => (
              <option key={r.id} value={r.id}>
                {r.label} (N={r.n})
              </option>
            ))}
          </select>
        </label>
      </div>

      {!ready && <Loading label="Loading run" />}
      {ready && run?.error !== undefined && <ErrorBox error={run.error} />}
      {d && m && (
        <>
          <div className="rounded-2xl border border-line bg-surface p-4 font-mono text-xs shadow-card">
          <dl className="grid grid-cols-2 gap-x-6 gap-y-3 sm:grid-cols-3 lg:grid-cols-6">
            {[
              ["Set", m.split === "test" ? "Holdout" : "Tuning"],
              ["Queries", String(m.sample_count)],
              ["Passages", m.chunk_count.toLocaleString()],
              ["Embeddings", m.embedding_model],
              ["RRF k", String(m.rrf_k)],
              ["Commit", m.git_sha ? m.git_sha.slice(0, 7) : "n/a"],
            ].map(([k, v]) => (
              <div key={k} className="min-w-0">
                <dt className="text-muted">{k}</dt>
                <dd className="truncate text-ink" title={v}>{v}</dd>
              </div>
            ))}
          </dl>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              {m.git_dirty === false ? (
                <span className="inline-flex items-center gap-1.5 text-success"><CircleCheck className="size-3.5" aria-hidden /> Clean tree: the commit identifies the exact code</span>
              ) : m.git_dirty ? (
                <span className="inline-flex items-center gap-1.5 text-warn"><TriangleAlert className="size-3.5" aria-hidden /> Uncommitted changes when this run was made</span>
              ) : null}
              <span className="ml-auto text-muted">{m.created_at_utc}</span>
            </div>
          </div>

          <KpiCards scores={d.scores} />

          <div className="grid gap-6 lg:grid-cols-2">
            <Card title="Recall@k" sub="Share of queries with an expected passage in the top k.">
              <RecallCurve curves={d.curves} />
            </Card>
            <Card title="MRR@10 by query class" sub="Which method wins depends on the kind of question.">
              <ClassBars scores={d.scores} />
            </Card>
          </div>

          <Card title="Head to head" sub={`Pairwise comparison over the same ${m.sample_count} queries.`}>
            <HeadToHead rows={d.head_to_head} />
          </Card>

          <Card title="Rank of the first expected passage" sub="One row per query. Click a query to run it on the Search page.">
            <RankHeatmap cases={d.cases} queries={queries} />
          </Card>

          <section className="rounded-2xl border border-warn/30 bg-warn-bg/50 p-5">
            <h2 className="flex items-center gap-2 font-semibold"><TriangleAlert className="size-4 text-warn" aria-hidden /> Caveats</h2>
            <ul className="mt-3 list-disc space-y-1.5 pl-5 text-sm">
              <li>Queries were drafted by an LLM from passages and are synthetic. Drafting from passage text can favour keyword matching.</li>
              <li>Extra relevant passages were judged by an LLM on pooled top-10 results; a human spot-checked a sample (see README for the agreement rate).</li>
              <li>Confidence intervals are 95% percentile bootstrap over queries (1,000 draws, fixed seed). Small classes have wide intervals.</li>
              <li>{m.split === "test" ? "Holdout set: run once, after tuning on the separate tuning set." : "Tuning set: used to choose settings, so these numbers are optimistic."}</li>
            </ul>
          </section>
        </>
      )}
    </div>
  );
}
