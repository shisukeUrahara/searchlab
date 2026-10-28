"use client";
import { ExternalLink, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { api, type Chunk } from "@/lib/api";
import { ErrorBox, Loading } from "./StateViews";

/** Side panel on desktop, bottom sheet on mobile. Esc or backdrop click closes it. */
export function ChunkDrawer({ chunkId, onClose }: { chunkId: string; onClose: () => void }) {
  const [state, setState] = useState<{ id: string; chunk?: Chunk; error?: unknown }>({ id: "" });
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    let live = true;
    api
      .chunk(chunkId)
      .then((chunk) => live && setState({ id: chunkId, chunk }))
      .catch((error) => live && setState({ id: chunkId, error }));
    return () => {
      live = false;
    };
  }, [chunkId]);

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
      previous?.focus();
    };
  }, [onClose]);

  const ready = state.id === chunkId;
  const c = state.chunk;
  return (
    <div className="fixed inset-0 z-40 flex items-end bg-ink/40 backdrop-blur-[2px] md:items-stretch md:justify-end" onClick={onClose}>
      <aside
        role="dialog"
        aria-modal="true"
        aria-label="Passage detail"
        onClick={(e) => e.stopPropagation()}
        className="max-h-[85vh] w-full overflow-y-auto rounded-t-2xl border-line bg-surface p-5 shadow-card md:max-h-none md:max-w-xl md:rounded-none md:border-l"
      >
        <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-line md:hidden" aria-hidden />
        <div className="flex items-start justify-between gap-4">
          <p className="font-mono text-xs text-muted">passage {chunkId}</p>
          <button
            ref={closeRef}
            onClick={onClose}
            aria-label="Close passage"
            className="grid size-8 place-items-center rounded-lg border border-line hover:bg-surface-2"
          >
            <X className="size-4" aria-hidden />
          </button>
        </div>
        {!ready && <div className="mt-4"><Loading label="Loading passage" /></div>}
        {ready && state.error !== undefined && <div className="mt-4"><ErrorBox error={state.error} /></div>}
        {ready && c && (
          <>
            <p className="mt-3 font-mono text-xs text-muted">{c.heading}</p>
            <h2 className="mt-1 text-lg font-semibold">{c.title}</h2>
            <a
              href={c.url}
              target="_blank"
              rel="noreferrer"
              className="mt-2 inline-flex items-center gap-1.5 text-sm text-primary underline-offset-2 hover:underline"
            >
              Open source{c.page ? ` at page ${c.page}` : ""} <ExternalLink className="size-3.5" aria-hidden />
            </a>
            <pre className="mt-4 whitespace-pre-wrap rounded-xl bg-surface-2 p-4 font-mono text-xs leading-relaxed">{c.text}</pre>
          </>
        )}
      </aside>
    </div>
  );
}
