import { METHODS, METHOD_LABEL, METHOD_META, type ScoreRow } from "@/lib/api";
import { ci, fmt, pct } from "./format";

function Metric({ label, value, interval, bar, barClass }: { label: string; value: string; interval?: string; bar?: number; barClass: string }) {
  return (
    <div className="border-t border-line py-3 first:border-t-0 first:pt-0">
      <div className="flex items-baseline justify-between gap-2 font-mono text-xs text-muted">
        <span>{label}</span>
        {interval && <span title="95% bootstrap confidence interval">95% CI {interval}</span>}
      </div>
      <p className="mt-1 font-mono text-2xl font-semibold tracking-tight">{value}</p>
      {bar !== undefined && (
        <div className="mt-2 h-1.5 rounded-full bg-surface-2" aria-hidden>
          <div className={`h-1.5 rounded-full ${barClass}`} style={{ width: `${Math.max(2, bar * 100)}%` }} />
        </div>
      )}
    </div>
  );
}

export function KpiCards({ scores }: { scores: ScoreRow[] }) {
  const overall = METHODS.map((m) => scores.find((s) => s.method === m && s.query_class === "all")).filter((s): s is ScoreRow => !!s);
  const best = overall.reduce<ScoreRow | null>((a, s) => (!a || s.mrr_at_10 > a.mrr_at_10 ? s : a), null);
  const base = overall.find((s) => s.method === "bm25");
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {overall.map((s) => {
        const meta = METHOD_META[s.method];
        const isBest = best?.method === s.method;
        const delta = base && s.method !== "bm25" ? s.mrr_at_10 - base.mrr_at_10 : null;
        return (
          <section
            key={s.method}
            aria-label={`${METHOD_LABEL[s.method]} metrics`}
            className={`rounded-2xl border bg-surface p-5 shadow-card ${isBest ? "border-success ring-1 ring-success/30" : "border-line"}`}
          >
            <header className="mb-4 flex items-center gap-2">
              <span className={`size-2.5 rounded-full ${meta.dot}`} aria-hidden />
              <h3 className="font-semibold">{METHOD_LABEL[s.method]}</h3>
              {isBest && <span className="rounded-full bg-success-bg px-2 py-0.5 text-xs text-success">Best MRR</span>}
              <span className="ml-auto font-mono text-xs text-muted">N={s.n}</span>
            </header>
            <Metric label="MRR@10" value={fmt(s.mrr_at_10)} interval={ci(s.mrr_ci)} bar={s.mrr_at_10} barClass={meta.bar} />
            {delta !== null && (
              <p className={`-mt-1 mb-2 font-mono text-xs ${delta >= 0 ? "text-success" : "text-danger"}`}>
                {delta >= 0 ? "+" : ""}
                {delta.toFixed(3)} vs BM25
              </p>
            )}
            <Metric label="Recall@1" value={pct(s.recall_at_1)} barClass={meta.bar} />
            <Metric label="Recall@5" value={pct(s.recall_at_5)} interval={ci(s.recall_at_5_ci, 2)} barClass={meta.bar} />
            <Metric label="nDCG@10" value={fmt(s.ndcg_at_10)} barClass={meta.bar} />
          </section>
        );
      })}
    </div>
  );
}
