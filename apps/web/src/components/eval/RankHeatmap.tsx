"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { CLASS_LABEL, METHODS, METHOD_META, type CaseRow, type LabeledQuery, type Method } from "@/lib/api";
import { Pager } from "../Pager";

const PAGE = 12;

export function firstRank(c: CaseRow): number | null {
  const i = c.ranked_chunk_ids.findIndex((id) => c.gold_chunk_ids.includes(id));
  return i === -1 ? null : i + 1;
}

export function rankTone(rank: number | null): string {
  if (rank === null) return "bg-danger-bg text-danger";
  if (rank === 1) return "bg-success text-white dark:text-[#0a0f1a]";
  if (rank <= 3) return "bg-success/45 text-ink";
  if (rank <= 5) return "bg-success/20 text-ink";
  return "bg-surface-2 text-muted";
}

export function RankHeatmap({ cases, queries }: { cases: CaseRow[]; queries: Record<string, LabeledQuery> }) {
  const [offset, setOffset] = useState(0);
  const [onlyDiff, setOnlyDiff] = useState(false);
  const rows = useMemo(() => {
    const by = new Map<string, { qid: string; cls: string; ranks: Partial<Record<Method, number | null>> }>();
    cases.forEach((c) => {
      const row = by.get(c.query_id) ?? { qid: c.query_id, cls: c.query_class, ranks: {} };
      row.ranks[c.method] = firstRank(c);
      by.set(c.query_id, row);
    });
    const all = [...by.values()];
    return onlyDiff ? all.filter((r) => new Set(Object.values(r.ranks)).size > 1) : all;
  }, [cases, onlyDiff]);
  const page = rows.slice(offset, offset + PAGE);

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={onlyDiff} onChange={(e) => { setOnlyDiff(e.target.checked); setOffset(0); }} className="accent-[var(--primary)]" />
          Only queries where methods disagree
        </label>
        <ul className="flex flex-wrap gap-3 font-mono text-xs text-muted" aria-label="Legend">
          {[["#1", 1], ["#2–3", 2], ["#4–5", 4], ["#6–10", 6], ["miss", null]].map(([l, r]) => (
            <li key={String(l)} className="flex items-center gap-1.5">
              <span className={`inline-block size-3 rounded ${rankTone(r as number | null)}`} aria-hidden />
              {l}
            </li>
          ))}
        </ul>
      </div>
      <div className="relative overflow-x-auto rounded-xl border border-line">
        <table className="w-full min-w-[640px] text-sm">
          <thead className="bg-surface-2 text-left font-mono text-xs uppercase text-muted">
            <tr>
              <th scope="col" className="px-3 py-2">Query</th>
              <th scope="col" className="px-3 py-2">Class</th>
              {METHODS.map((m) => (
                <th key={m} scope="col" className="px-3 py-2 text-center">{METHOD_META[m].short}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {page.map((r) => (
              <tr key={r.qid}>
                <td className="max-w-[380px] px-3 py-2">
                  <Link href={`/?q=${encodeURIComponent(queries[r.qid]?.text ?? "")}`} className="hover:underline">
                    <span className="mr-2 font-mono text-xs text-muted">{r.qid}</span>
                    {queries[r.qid]?.text ?? ""}
                  </Link>
                </td>
                <td className="whitespace-nowrap px-3 py-2 text-xs text-muted">{CLASS_LABEL[r.cls] ?? r.cls}</td>
                {METHODS.map((m) => {
                  const rank = r.ranks[m] ?? null;
                  return (
                    <td key={m} className="px-3 py-2 text-center">
                      <span className={`inline-block min-w-12 rounded-md px-2 py-1 font-mono text-xs ${rankTone(rank)}`}>
                        {rank === null ? "miss" : `#${rank}`}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Pager total={rows.length} pageSize={PAGE} offset={offset} onChange={setOffset} noun="queries" />
    </div>
  );
}
