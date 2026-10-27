import { METHOD_LABEL, type MethodResult } from "@/lib/api";

interface Props {
  result: MethodResult;
  goldIds: string[];
  onOpen: (chunkId: string) => void;
}

export function RankingColumn({ result, goldIds, onOpen }: Props) {
  const firstGold = result.hits.find((h) => goldIds.includes(h.chunk_id))?.rank;
  return (
    <section aria-label={METHOD_LABEL[result.method]} className="rounded-lg border border-line bg-surface">
      <header className="flex items-baseline justify-between border-b border-line px-4 py-3">
        <h2 className="font-semibold">{METHOD_LABEL[result.method]}</h2>
        <span className="font-mono text-xs text-muted">{result.latency_ms.toFixed(1)} ms</span>
      </header>
      {goldIds.length > 0 && (
        <p
          className={`mx-4 mt-3 rounded-md px-3 py-1.5 text-xs ${firstGold ? "bg-success-bg text-success" : "bg-danger-bg text-danger"}`}
        >
          {firstGold ? `Expected chunk found at rank ${firstGold}` : "Expected chunk not in these results"}
        </p>
      )}
      {result.hits.length === 0 ? (
        <p className="p-4 text-sm text-muted">No matching chunks.</p>
      ) : (
        <ol className="divide-y divide-line">
          {result.hits.map((h) => {
            const isGold = goldIds.includes(h.chunk_id);
            return (
              <li key={h.chunk_id}>
                <button
                  onClick={() => onOpen(h.chunk_id)}
                  className={`block w-full px-4 py-3 text-left hover:bg-canvas ${isGold ? "bg-success-bg/60" : ""}`}
                >
                  <div className="flex items-center gap-2 text-xs">
                    <span className="rounded bg-ink px-1.5 py-0.5 font-mono text-surface">#{h.rank}</span>
                    <span className="font-mono text-muted">{h.score.toFixed(3)}</span>
                    {isGold && <span className="font-medium text-success">✓ expected</span>}
                  </div>
                  <p className="mt-1 text-sm font-medium">{h.heading}</p>
                  <p className="mt-1 line-clamp-2 text-xs text-muted">{h.snippet}</p>
                </button>
              </li>
            );
          })}
        </ol>
      )}
    </section>
  );
}
