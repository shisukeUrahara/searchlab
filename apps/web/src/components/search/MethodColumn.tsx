import { CircleAlert, CircleCheck, KeyRound } from "lucide-react";
import { METHOD_LABEL, METHOD_META, type MethodResult } from "@/lib/api";
import { ResultCard } from "./ResultCard";

interface Props {
  result: MethodResult;
  goldIds: string[];
  docNumbers: Record<string, string>;
  onOpen: (chunkId: string) => void;
}

export function MethodColumn({ result, goldIds, docNumbers, onOpen }: Props) {
  const meta = METHOD_META[result.method];
  const firstGold = result.hits.find((h) => goldIds.includes(h.chunk_id))?.rank;
  const maxScore = Math.max(0, ...result.hits.map((h) => h.score));
  return (
    <section aria-label={METHOD_LABEL[result.method]} className="space-y-3">
      <header className="rounded-xl border border-line bg-surface p-4 shadow-card">
        <div className="flex items-center gap-2">
          <span className={`size-2.5 rounded-full ${meta.dot}`} aria-hidden />
          <h2 className="font-semibold">{METHOD_LABEL[result.method]}</h2>
          <span className="ml-auto rounded-md bg-surface-2 px-2 py-0.5 font-mono text-xs text-muted">
            {result.latency_ms.toFixed(1)} ms
          </span>
        </div>
        <p className="mt-2 font-mono text-xs text-muted">{meta.detail}</p>
        {goldIds.length > 0 && !result.error && (
          <p
            className={`mt-3 flex items-center gap-2 rounded-lg px-3 py-2 font-mono text-xs ${
              firstGold === 1
                ? "bg-success-bg text-success"
                : firstGold
                  ? "bg-surface-2 text-ink"
                  : "bg-danger-bg text-danger"
            }`}
          >
            {firstGold ? <CircleCheck className="size-3.5" aria-hidden /> : <CircleAlert className="size-3.5" aria-hidden />}
            {firstGold ? `Expected passage at rank ${firstGold}` : "Expected passage not in these results"}
          </p>
        )}
      </header>
      {result.error === "embedding_failed" ? (
        <div role="status" className="rounded-xl border border-dashed border-danger/40 bg-danger-bg/60 p-5 text-sm">
          <p className="flex items-center gap-2 font-medium text-danger">
            <KeyRound className="size-4" aria-hidden /> The embedding provider rejected this request
          </p>
          <p className="mt-1.5 text-muted">
            Check <code className="font-mono text-xs">OPENAI_API_KEY</code> in services/api/.env. Keyword search (BM25) still answers.
          </p>
        </div>
      ) : result.error === "embedding_unavailable" ? (
        <div role="status" className="rounded-xl border border-dashed border-warn/40 bg-warn-bg/60 p-5 text-sm">
          <p className="flex items-center gap-2 font-medium text-warn">
            <KeyRound className="size-4" aria-hidden /> Needs an embedding for this question
          </p>
          <p className="mt-1.5 text-muted">
            New questions need an OpenAI API key to be turned into a vector. Saved example questions work without one.
            Keyword search (BM25) still answers.
          </p>
        </div>
      ) : result.hits.length === 0 ? (
        <p className="rounded-xl border border-dashed border-line p-6 text-center text-sm text-muted">No matching passages.</p>
      ) : (
        <ol className="space-y-3">
          {result.hits.map((h) => (
            <li key={h.chunk_id}>
              <ResultCard
                hit={h}
                method={result.method}
                maxScore={maxScore}
                docNumber={docNumbers[h.source_id] ?? h.source_id.split("/")[1]}
                expected={goldIds.includes(h.chunk_id)}
                onOpen={onOpen}
              />
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
