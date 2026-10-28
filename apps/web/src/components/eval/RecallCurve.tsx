"use client";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { METHODS, METHOD_META, METHOD_VAR, type Method } from "@/lib/api";

export function RecallCurve({ curves }: { curves: Partial<Record<Method, number[]>> }) {
  const k = Math.max(0, ...METHODS.map((m) => curves[m]?.length ?? 0));
  const rows = Array.from({ length: k }, (_, i) => ({
    k: i + 1,
    ...Object.fromEntries(METHODS.map((m) => [m, curves[m]?.[i] ?? null])),
  }));
  return (
    <figure className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 8, right: 16, bottom: 4, left: -8 }}>
          <CartesianGrid stroke="var(--line)" strokeDasharray="3 3" />
          <XAxis dataKey="k" stroke="var(--muted)" tick={{ fontSize: 12 }} tickFormatter={(v) => `k=${v}`} />
          <YAxis domain={[0, 1]} stroke="var(--muted)" tick={{ fontSize: 12 }} tickFormatter={(v) => `${Math.round(v * 100)}%`} />
          <Tooltip
            contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", borderRadius: 10, color: "var(--ink)" }}
            formatter={(v, name) => [`${(Number(v) * 100).toFixed(1)}%`, METHOD_META[name as Method]?.short ?? String(name)]}
            labelFormatter={(l) => `Recall@${l}`}
          />
          <Legend formatter={(v) => METHOD_META[v as Method]?.short ?? v} />
          {METHODS.map((m) => (
            <Line key={m} type="monotone" dataKey={m} stroke={METHOD_VAR[m]} strokeWidth={2.5} dot={{ r: 3 }} isAnimationActive={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <figcaption className="sr-only">Recall at k from 1 to {k} for each method.</figcaption>
    </figure>
  );
}
