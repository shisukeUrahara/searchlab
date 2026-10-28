"use client";
import { Bar, BarChart, CartesianGrid, ErrorBar, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { CLASS_LABEL, METHODS, METHOD_META, METHOD_VAR, type Method, type ScoreRow } from "@/lib/api";

export function ClassBars({ scores }: { scores: ScoreRow[] }) {
  const classes = [...new Set(scores.map((s) => s.query_class))].filter((c) => c !== "all");
  const rows = classes.map((c) => {
    const row: Record<string, unknown> = { cls: CLASS_LABEL[c] ?? c };
    METHODS.forEach((m) => {
      const s = scores.find((x) => x.method === m && x.query_class === c);
      row[m] = s?.mrr_at_10 ?? null;
      row[`${m}_err`] = s?.mrr_ci ? [s.mrr_at_10 - s.mrr_ci[0], s.mrr_ci[1] - s.mrr_at_10] : [0, 0];
      row[`${m}_n`] = s?.n ?? 0;
    });
    return row;
  });
  return (
    <figure className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} margin={{ top: 8, right: 16, bottom: 4, left: -8 }}>
          <CartesianGrid stroke="var(--line)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="cls" stroke="var(--muted)" tick={{ fontSize: 12 }} />
          <YAxis domain={[0, 1]} stroke="var(--muted)" tick={{ fontSize: 12 }} />
          <Tooltip
            cursor={{ fill: "var(--surface-2)" }}
            contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", borderRadius: 10, color: "var(--ink)" }}
            formatter={(v, name) => [Number(v).toFixed(3), METHOD_META[name as Method]?.short ?? String(name)]}
          />
          <Legend formatter={(v) => METHOD_META[v as Method]?.short ?? v} />
          {METHODS.map((m) => (
            <Bar key={m} dataKey={m} fill={METHOD_VAR[m]} radius={[4, 4, 0, 0]} isAnimationActive={false}>
              <ErrorBar dataKey={`${m}_err`} stroke="var(--ink)" strokeOpacity={0.55} width={4} />
            </Bar>
          ))}
        </BarChart>
      </ResponsiveContainer>
      <figcaption className="mt-1 font-mono text-xs text-muted">
        MRR@10 per query class. Whiskers: 95% bootstrap CI. Group sizes: {rows.map((r) => `${r.cls} n=${r.bm25_n}`).join(", ")}.
      </figcaption>
    </figure>
  );
}
