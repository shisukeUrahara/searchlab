"use client";
import { ArrowUpRight, Info, Search } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Pager } from "@/components/Pager";
import { Empty, ErrorBox, Loading } from "@/components/StateViews";
import { api, CLASS_LABEL, type Corpus, type QueryPage } from "@/lib/api";
import { docColor } from "@/lib/docs";

const PAGE = 15;
const CLASSES = ["exact_id", "paraphrase", "distractor"] as const;
const CLASS_TONE: Record<string, string> = {
  exact_id: "bg-m-bm25/10 text-m-bm25-ink",
  paraphrase: "bg-m-dense/10 text-m-dense-ink",
  distractor: "bg-distractor-ink/10 text-distractor-ink",
};

type Split = "dev" | "test";

export default function QueriesPage() {
  const [split, setSplit] = useState<Split>("test");
  const [cls, setCls] = useState<string>("");
  const [text, setText] = useState("");
  const [q, setQ] = useState("");
  const [offset, setOffset] = useState(0);
  const [data, setData] = useState<{ key: string; page?: QueryPage; error?: unknown } | null>(null);
  const [splitTotals, setSplitTotals] = useState<Record<Split, number>>({ dev: 0, test: 0 });
  const [corpus, setCorpus] = useState<Corpus | null>(null);

  useEffect(() => {
    api.corpus().then(setCorpus).catch(() => setCorpus(null));
    Promise.all([api.queries("dev", 1), api.queries("test", 1)])
      .then(([d, t]) => setSplitTotals({ dev: d.total, test: t.total }))
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    const t = setTimeout(() => {
      setQ(text.trim());
      setOffset(0);
    }, 250);
    return () => clearTimeout(t);
  }, [text]);

  const key = `${split}|${cls}|${q}|${offset}`;
  useEffect(() => {
    let live = true;
    api.queries(split, PAGE, offset, { queryClass: cls || undefined, q: q || undefined })
      .then((page) => live && setData({ key, page }))
      .catch((error) => live && setData({ key, error }));
    return () => {
      live = false;
    };
  }, [key, split, cls, q, offset]);

  const docNumbers = Object.fromEntries((corpus?.docs ?? []).map((d) => [d.source_id, d.doc_number]));
  const page = data?.key === key ? data.page : undefined;
  const counts = page?.class_counts ?? {};
  const choose = (next: () => void) => {
    next();
    setOffset(0);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold md:text-4xl">Labeled queries</h1>
          <p className="mt-2 text-muted">
            The questions used to score each method, with the passages that count as correct answers.
          </p>
        </div>
        <ul className="flex flex-wrap gap-2 font-mono text-xs">
          {[
            ["Total", splitTotals.dev + splitTotals.test],
            ["Holdout", splitTotals.test],
            ["Tuning", splitTotals.dev],
          ].map(([k, v]) => (
            <li key={k} className="rounded-lg border border-line bg-surface px-2.5 py-1 text-muted">
              {k}: <span className="text-ink">{v}</span>
            </li>
          ))}
        </ul>
      </div>

      <p className="flex gap-3 rounded-xl border border-line border-l-4 border-l-primary bg-surface p-4 text-sm">
        <Info className="mt-0.5 size-4 shrink-0 text-primary" aria-hidden />
        <span>
          <strong>How these were made:</strong> an LLM drafted each question from a passage. A second LLM judged which other
          top-ranked passages also answer it. A person spot-checked a random sample. The questions are synthetic.
        </span>
      </p>

      <div className="space-y-4 rounded-2xl border border-line bg-surface p-4 shadow-card">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div role="tablist" aria-label="Query set" className="inline-grid grid-cols-2 gap-1 rounded-xl bg-surface-2 p-1">
            {(["dev", "test"] as const).map((s) => (
              <button
                key={s}
                role="tab"
                aria-selected={split === s}
                onClick={() => choose(() => setSplit(s))}
                className="rounded-lg px-4 py-1.5 text-sm aria-selected:bg-surface aria-selected:font-medium aria-selected:shadow-card"
              >
                {s === "dev" ? "Tuning set" : "Holdout set"} <span className="font-mono text-xs text-muted">({splitTotals[s]})</span>
              </button>
            ))}
          </div>
          <label className="relative flex h-10 items-center gap-2 rounded-lg border border-line bg-canvas px-3 focus-within:border-primary md:w-80">
            <Search className="size-4 text-muted" aria-hidden />
            <span className="sr-only">Filter queries</span>
            <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Filter by text…" className="min-w-0 flex-1 bg-transparent text-sm outline-none" />
          </label>
        </div>
        <div className="flex flex-wrap items-center gap-2" role="group" aria-label="Query class">
          <span className="font-mono text-xs uppercase text-muted">Class</span>
          {["", ...CLASSES].map((c) => (
            <button
              key={c || "all"}
              aria-pressed={cls === c}
              onClick={() => choose(() => setCls(c))}
              className="rounded-full border border-line px-3 py-1 text-sm aria-pressed:border-ink aria-pressed:bg-ink aria-pressed:text-canvas"
            >
              {c ? CLASS_LABEL[c] : "All"}
              <span className="ml-1 font-mono text-xs opacity-70">
                {c ? counts[c] ?? 0 : Object.values(counts).reduce((a, b) => a + b, 0)}
              </span>
            </button>
          ))}
        </div>
      </div>

      {!page && data?.key !== key && <Loading label="Loading queries" />}
      {data?.key === key && data.error !== undefined && <ErrorBox error={data.error} />}
      {page && page.items.length === 0 && <Empty title="No queries match" hint="Try another class or clear the text filter." />}
      {page && page.items.length > 0 && (
        <div className="space-y-4">
          <div className="relative overflow-x-auto rounded-2xl border border-line bg-surface shadow-card">
            <table className="w-full min-w-[720px] text-sm">
              <thead className="bg-surface-2 text-left font-mono text-xs uppercase text-muted">
                <tr>
                  <th scope="col" className="px-4 py-3">ID</th>
                  <th scope="col" className="px-4 py-3">Class</th>
                  <th scope="col" className="px-4 py-3">Query</th>
                  <th scope="col" className="px-4 py-3">Target document</th>
                  <th scope="col" className="px-4 py-3 text-right">Correct passages</th>
                  <th scope="col" className="px-4 py-3"><span className="sr-only">Actions</span></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {page.items.map((row) => (
                  <tr key={row.query_id} className="hover:bg-surface-2/50">
                    <td className="px-4 py-3 font-mono text-xs text-muted">{row.query_id}</td>
                    <td className="px-4 py-3">
                      <span className={`whitespace-nowrap rounded-md px-2 py-0.5 font-mono text-xs ${CLASS_TONE[row.query_class] ?? ""}`}>
                        {CLASS_LABEL[row.query_class] ?? row.query_class}
                      </span>
                    </td>
                    <td className="px-4 py-3">{row.text}</td>
                    <td className="px-4 py-3">
                      {row.gold_sources?.[0] && (
                        <span className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-md border border-line px-2 py-0.5 font-mono text-xs">
                          <span className="size-2 rounded-full" style={{ background: docColor(row.gold_sources[0]) }} aria-hidden />
                          {docNumbers[row.gold_sources[0]] ?? row.gold_sources[0]}
                          {row.gold_sources.length > 1 && <span className="text-muted">+{row.gold_sources.length - 1}</span>}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-xs">{row.gold_chunk_ids.length}</td>
                    <td className="px-4 py-3 text-right">
                      <Link
                        href={`/?q=${encodeURIComponent(row.text)}`}
                        className="inline-flex items-center gap-1 whitespace-nowrap rounded-lg border border-line px-2.5 py-1 text-xs text-primary hover:bg-surface-2"
                      >
                        Try it <ArrowUpRight className="size-3" aria-hidden />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pager total={page.total} pageSize={PAGE} offset={offset} onChange={setOffset} noun={split === "dev" ? "tuning queries" : "holdout queries"} />
        </div>
      )}
    </div>
  );
}
