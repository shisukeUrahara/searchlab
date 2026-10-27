"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, type LabeledQuery } from "@/lib/api";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";

export default function QueriesPage() {
  const [split, setSplit] = useState<"dev" | "test">("dev");
  const [data, setData] = useState<{ split: string; rows?: LabeledQuery[]; error?: unknown }>({ split: "" });

  useEffect(() => {
    let live = true;
    api.queries(split)
      .then((rows) => live && setData({ split, rows }))
      .catch((error) => live && setData({ split, error }));
    return () => { live = false; };
  }, [split]);

  const ready = data.split === split;
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold tracking-tight">Labeled queries</h1>
      <p className="text-sm text-muted">
        Synthetic questions with known answer chunks. The dev split was used for tuning. The test split is frozen.
      </p>
      <div role="group" aria-label="Split" className="flex gap-2">
        {(["dev", "test"] as const).map((s) => (
          <button key={s} aria-pressed={split === s} onClick={() => setSplit(s)}
            className={`rounded-md px-3 py-1.5 text-sm ${split === s ? "bg-primary text-primary-ink" : "border border-line"}`}>
            {s}
          </button>
        ))}
      </div>
      {!ready && <Loading />}
      {ready && data.error !== undefined && <ErrorBox error={data.error} />}
      {ready && data.rows?.length === 0 && <Empty title="No queries" />}
      {ready && data.rows && data.rows.length > 0 && (
        <ul className="divide-y divide-line rounded-lg border border-line bg-surface">
          {data.rows.map((q) => (
            <li key={q.query_id}>
              <Link href={`/?q=${encodeURIComponent(q.text)}`} className="flex flex-wrap items-center gap-3 px-4 py-3 hover:bg-canvas">
                <span className="font-mono text-xs text-muted">{q.query_id}</span>
                <span className="rounded-full bg-canvas px-2 py-0.5 text-xs">{q.query_class}</span>
                <span className="flex-1 font-mono text-sm">{q.text}</span>
                <span className="text-xs text-muted">{q.gold_chunk_ids.length} expected</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
