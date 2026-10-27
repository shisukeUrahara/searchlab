"use client";
import { useEffect, useRef, useState } from "react";
import { api, type Chunk } from "@/lib/api";
import { ErrorBox, Loading } from "./StateViews";

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
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const ready = state.id === chunkId;
  return (
    <div className="fixed inset-0 z-20 flex justify-end bg-ink/30" onClick={onClose}>
      <aside
        role="dialog"
        aria-modal="true"
        aria-label="Chunk detail"
        onClick={(e) => e.stopPropagation()}
        className="h-full w-full overflow-y-auto bg-surface p-5 shadow-xl md:max-w-xl"
      >
        <div className="flex items-start justify-between gap-4">
          <p className="font-mono text-xs text-muted">chunk {chunkId}</p>
          <button ref={closeRef} onClick={onClose} className="rounded-md border border-line px-3 py-1 text-sm">
            Close (Esc)
          </button>
        </div>
        {!ready && <div className="mt-4"><Loading label="Loading chunk" /></div>}
        {ready && state.error !== undefined && <div className="mt-4"><ErrorBox error={state.error} /></div>}
        {ready && state.chunk && (
          <>
            <h2 className="mt-3 text-lg font-semibold">{state.chunk.heading}</h2>
            <a href={state.chunk.url} target="_blank" rel="noreferrer" className="text-sm text-primary underline">
              {state.chunk.title} on docs.github.com
            </a>
            <pre className="mt-4 whitespace-pre-wrap rounded-md bg-canvas p-4 font-mono text-xs leading-relaxed">
              {state.chunk.text}
            </pre>
          </>
        )}
      </aside>
    </div>
  );
}
