"use client";
import { ExternalLink, X } from "lucide-react";
import { useEffect, useState } from "react";
import { api, type Chunk, type CorpusDoc } from "@/lib/api";
import { docColor } from "@/lib/docs";
import { ErrorBox, Loading } from "../StateViews";

export interface Neighbor {
  id: string;
  heading: string;
  sim: number;
}

interface Props {
  chunkId: string;
  docs: CorpusDoc[];
  neighbors: Neighbor[];
  ranks: { method: string; rank: number }[];
  onPick: (id: string) => void;
  onClose: () => void;
}

export function Inspector({ chunkId, docs, neighbors, ranks, onPick, onClose }: Props) {
  const [state, setState] = useState<{ id: string; chunk?: Chunk; error?: unknown }>({ id: "" });
  useEffect(() => {
    let live = true;
    api.chunk(chunkId)
      .then((chunk) => live && setState({ id: chunkId, chunk }))
      .catch((error) => live && setState({ id: chunkId, error }));
    return () => {
      live = false;
    };
  }, [chunkId]);
  const c = state.id === chunkId ? state.chunk : undefined;
  const doc = c ? docs.find((d) => d.source_id === c.source_id) : undefined;
  return (
    <section aria-label="Passage inspector" className="flex max-h-full flex-col overflow-hidden rounded-2xl border border-white/10 bg-[#111827]/95 text-[#e6ebf5] shadow-2xl backdrop-blur">
      <header className="flex items-start justify-between gap-3 border-b border-white/10 p-4">
        <div>
          <h2 className="font-semibold">Passage inspector</h2>
          <p className="font-mono text-xs text-[#93a0b4]">{chunkId}</p>
        </div>
        <button onClick={onClose} aria-label="Close inspector" className="grid size-8 place-items-center rounded-lg hover:bg-white/10">
          <X className="size-4" aria-hidden />
        </button>
      </header>
      <div className="space-y-4 overflow-y-auto p-4">
        {state.id !== chunkId && <Loading label="Loading passage" />}
        {state.id === chunkId && state.error !== undefined && <ErrorBox error={state.error} />}
        {c && (
          <>
            <div className="rounded-xl border border-white/10 p-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="inline-flex items-center gap-2 rounded-md bg-white/5 px-2 py-0.5 font-mono text-xs">
                  <span className="size-2 rounded-full" style={{ background: docColor(c.source_id) }} aria-hidden />
                  {doc?.doc_number ?? c.source_id}
                </span>
                <a href={c.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 font-mono text-xs text-[#6c8cff] hover:underline">
                  Open PDF{c.page ? ` page ${c.page}` : ""} <ExternalLink className="size-3" aria-hidden />
                </a>
              </div>
              <p className="mt-2 text-sm">{c.title}</p>
              <p className="mt-1 font-mono text-xs text-[#93a0b4]">{c.heading}</p>
            </div>
            {ranks.length > 0 && (
              <dl className="grid grid-cols-3 gap-2 text-center">
                {ranks.map((r) => (
                  <div key={r.method} className="rounded-lg border border-white/10 p-2">
                    <dt className="font-mono text-[11px] uppercase text-[#93a0b4]">{r.method}</dt>
                    <dd className="font-mono text-sm">#{r.rank}</dd>
                  </div>
                ))}
              </dl>
            )}
            <pre className="max-h-64 overflow-y-auto whitespace-pre-wrap rounded-xl bg-black/30 p-3 font-mono text-xs leading-relaxed">{c.text}</pre>
          </>
        )}
        {neighbors.length > 0 && (
          <div>
            <h3 className="mb-2 text-sm font-semibold">Nearest neighbours (cosine)</h3>
            <ul className="space-y-1.5">
              {neighbors.map((n) => (
                <li key={n.id}>
                  <button onClick={() => onPick(n.id)} className="flex w-full items-center justify-between gap-3 rounded-lg border border-white/10 px-3 py-2 text-left text-xs hover:bg-white/5">
                    <span className="truncate">{n.heading}</span>
                    <span className="shrink-0 font-mono text-[#93a0b4]">{n.sim.toFixed(3)}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
