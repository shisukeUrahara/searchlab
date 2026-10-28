"use client";
import { Check, Copy, ExternalLink, FileDown, Layers, Scissors, Sparkles, SplitSquareVertical, Scale } from "lucide-react";
import { useEffect, useState } from "react";
import { ErrorBox, Loading } from "@/components/StateViews";
import { api, type Corpus, type CorpusDoc } from "@/lib/api";
import { docColor } from "@/lib/docs";

const STEPS = [
  { icon: FileDown, title: "Fetch PDF", body: "Download each public PDF, check it starts with %PDF, record sha256, page count and time." },
  { icon: Scissors, title: "Strip headers", body: "Drop lines that repeat at the top or bottom of 30%+ of pages (page numbers, running titles)." },
  { icon: SplitSquareVertical, title: "Split by section", body: "Use the PDF outline when present, numbered headings otherwise. Skip front matter and references." },
  { icon: Layers, title: "Chunk ≤1,000 chars", body: "Pack lines into passages of up to 1,000 characters. Drop crumbs under 40. ID = hash of text." },
  { icon: Sparkles, title: "Embed", body: "text-embedding-3-small vectors, cached as float16 so the app runs without an API key." },
];

function Sha({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      onClick={() => {
        void navigator.clipboard?.writeText(value).then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        });
      }}
      aria-label="Copy sha256"
      className="flex w-full items-center justify-between gap-2 rounded-lg bg-surface-2 px-3 py-2 font-mono text-xs text-muted hover:text-ink"
    >
      <span className="truncate">sha256 {value.slice(0, 10)}…{value.slice(-8)}</span>
      {copied ? <Check className="size-3.5 text-success" aria-hidden /> : <Copy className="size-3.5" aria-hidden />}
    </button>
  );
}

function DocCard({ d }: { d: CorpusDoc }) {
  const facts = [
    ["Pages", d.pages ?? "—"],
    ["Passages", d.chunks.toLocaleString()],
    ["Retrieved", d.retrieved_at_utc?.slice(0, 10) ?? "—"],
    ["Status", "US Gov. work"],
  ];
  return (
    <article className="flex flex-col overflow-hidden rounded-2xl border border-line bg-surface shadow-card">
      <div className="h-1.5" style={{ background: docColor(d.source_id) }} aria-hidden />
      <div className="flex flex-1 flex-col gap-4 p-5">
        <div>
          <span className="inline-flex items-center gap-1.5 rounded-md border border-line px-2 py-0.5 font-mono text-xs">
            <span className="size-2 rounded-full" style={{ background: docColor(d.source_id) }} aria-hidden />
            {d.doc_number}
          </span>
          <h2 className="mt-3 font-semibold leading-snug">{d.title}</h2>
        </div>
        <dl className="grid grid-cols-2 gap-2">
          {facts.map(([k, v]) => (
            <div key={k} className="rounded-lg bg-surface-2 px-3 py-2">
              <dt className="font-mono text-[11px] uppercase text-muted">{k}</dt>
              <dd className="font-mono text-sm">{v}</dd>
            </div>
          ))}
        </dl>
        {d.sha256 && <Sha value={d.sha256} />}
        <a href={d.url} target="_blank" rel="noreferrer" className="mt-auto inline-flex items-center gap-1.5 text-sm text-primary hover:underline">
          Open PDF <ExternalLink className="size-3.5" aria-hidden />
        </a>
      </div>
    </article>
  );
}

export default function SourcesPage() {
  const [corpus, setCorpus] = useState<Corpus | null>(null);
  const [error, setError] = useState<unknown>();
  useEffect(() => {
    api.corpus().then(setCorpus).catch(setError);
  }, []);
  if (error !== undefined) return <ErrorBox error={error} />;
  if (!corpus) return <Loading label="Loading sources" />;
  const pages = corpus.docs.reduce((a, d) => a + (d.pages ?? 0), 0);

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold md:text-4xl">Sources</h1>
          <p className="mt-2 text-muted">
            Five public NASA documents. They are works of the US Government, so they are not under copyright in the US
            (17 U.S.C. §105). This project is independent and not affiliated with or endorsed by NASA.
          </p>
        </div>
        <ul className="flex flex-wrap gap-2 font-mono text-xs">
          {[["Documents", corpus.docs.length], ["Pages", pages.toLocaleString()], ["Passages", corpus.chunk_count.toLocaleString()]].map(([k, v]) => (
            <li key={k} className="rounded-lg border border-line bg-surface px-2.5 py-1 text-muted">
              {k}: <span className="text-ink">{v}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {corpus.docs.map((d) => (
          <DocCard key={d.source_id} d={d} />
        ))}
        <article className="flex flex-col gap-3 rounded-2xl border border-dashed border-line p-5">
          <h2 className="flex items-center gap-2 font-semibold"><Scale className="size-4 text-primary" aria-hidden /> Reproducible by design</h2>
          <p className="text-sm text-muted">
            Passage IDs are a hash of document, section and text, so rebuilding gives byte-identical output. A manifest records
            every file&apos;s sha256, and <code className="font-mono text-xs">searchlab verify</code> checks them.
          </p>
          <a href="https://github.com/shisukeUrahara/searchlab/tree/main/services/api/src/searchlab/corpus" target="_blank" rel="noreferrer" className="mt-auto inline-flex items-center gap-1.5 text-sm text-primary hover:underline">
            Read the ingestion code <ExternalLink className="size-3.5" aria-hidden />
          </a>
        </article>
      </div>

      <section className="rounded-2xl border border-line bg-surface p-5 shadow-card">
        <h2 className="text-lg font-semibold">How the corpus is built</h2>
        <ol className="mt-4 grid gap-3 md:grid-cols-5">
          {STEPS.map((s, i) => (
            <li key={s.title} className="rounded-xl border border-line bg-canvas p-4">
              <div className="flex items-center justify-between">
                <span className="grid size-6 place-items-center rounded-full bg-primary/15 font-mono text-xs text-primary">{i + 1}</span>
                <s.icon className="size-4 text-muted" aria-hidden />
              </div>
              <h3 className="mt-3 text-sm font-semibold">{s.title}</h3>
              <p className="mt-1 text-xs leading-relaxed text-muted">{s.body}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
