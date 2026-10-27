import { METHOD_LABEL, type ScoreRow } from "@/lib/api";

export function MetricTable({ scores }: { scores: ScoreRow[] }) {
  const classes = ["all", ...new Set(scores.map((s) => s.query_class).filter((c) => c !== "all"))];
  return (
    <div className="overflow-x-auto rounded-lg border border-line bg-surface">
      <table className="w-full text-sm">
        <caption className="sr-only">Recall@5 and MRR@10 by method and query class</caption>
        <thead className="bg-canvas text-left text-xs uppercase text-muted">
          <tr>
            <th className="px-4 py-2">Method</th>
            <th className="px-4 py-2">Class</th>
            <th className="px-4 py-2 text-right">N</th>
            <th className="px-4 py-2 text-right">Recall@5</th>
            <th className="px-4 py-2 text-right">MRR@10</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-line">
          {classes.flatMap((cls) =>
            scores
              .filter((s) => s.query_class === cls)
              .map((s) => (
                <tr key={`${s.method}-${cls}`} className={cls === "all" ? "font-medium" : ""}>
                  <td className="px-4 py-2">{METHOD_LABEL[s.method]}</td>
                  <td className="px-4 py-2 font-mono text-xs">{cls}</td>
                  <td className="px-4 py-2 text-right">{s.n}</td>
                  <td className="px-4 py-2 text-right font-mono">{s.recall_at_5.toFixed(3)}</td>
                  <td className="px-4 py-2 text-right font-mono">{s.mrr_at_10.toFixed(3)}</td>
                </tr>
              )),
          )}
        </tbody>
      </table>
    </div>
  );
}
