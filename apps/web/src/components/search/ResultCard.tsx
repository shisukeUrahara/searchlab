import { CircleCheck } from "lucide-react";
import { METHOD_META, type Hit, type Method } from "@/lib/api";

interface Props {
  hit: Hit;
  method: Method;
  maxScore: number;
  docNumber: string;
  expected: boolean;
  onOpen: (chunkId: string) => void;
}

export function ResultCard({ hit, method, maxScore, docNumber, expected, onOpen }: Props) {
  const width = maxScore > 0 ? Math.max(6, (hit.score / maxScore) * 100) : 0;
  return (
    <button
      type="button"
      onClick={() => onOpen(hit.chunk_id)}
      aria-label={`Rank ${hit.rank}: ${hit.heading}${expected ? " (expected passage)" : ""}`}
      className={`group block w-full rounded-xl border bg-surface p-4 text-left shadow-card transition hover:-translate-y-px hover:border-primary/40 ${
        expected ? "border-success ring-1 ring-success/40" : "border-line"
      }`}
    >
      <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
        <span className={`rounded-md px-1.5 py-0.5 font-semibold ${expected ? "bg-success-bg text-success" : "bg-surface-2"}`}>
          #{hit.rank}
        </span>
        <span className="text-muted">score {hit.score.toFixed(hit.score > 1 ? 2 : 4)}</span>
        {expected && (
          <span className="inline-flex items-center gap-1 rounded-full bg-success-bg px-2 py-0.5 text-success">
            <CircleCheck className="size-3" aria-hidden /> expected
          </span>
        )}
        <span className="ml-auto rounded-md border border-line px-1.5 py-0.5 text-muted">
          {docNumber}
          {hit.page ? ` · p.${hit.page}` : ""}
        </span>
      </div>
      <div className="mt-3 h-1 rounded-full bg-surface-2" aria-hidden>
        <div className={`h-1 rounded-full ${METHOD_META[method].bar}`} style={{ width: `${width}%` }} />
      </div>
      <p className="mt-3 truncate font-mono text-xs text-muted" title={hit.heading}>
        {hit.heading}
      </p>
      <p className="mt-1.5 line-clamp-2 text-sm leading-relaxed">{hit.snippet}</p>
    </button>
  );
}
