"use client";
import { useEffect, useState } from "react";
import { api, type Source } from "@/lib/api";
import { ErrorBox, Loading } from "@/components/StateViews";

export default function SourcesPage() {
  const [data, setData] = useState<{ rows?: Source[]; error?: unknown } | null>(null);
  useEffect(() => {
    api.sources().then((r) => setData({ rows: r.sources })).catch((error) => setData({ error }));
  }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold tracking-tight">Sources</h1>
      <p className="text-sm text-muted">
        Six pages from github/docs, pinned to one commit. Content is CC BY 4.0. This project is independent and not affiliated with GitHub.
      </p>
      {!data && <Loading />}
      {data?.error !== undefined && <ErrorBox error={data.error} />}
      {data?.rows && (
        <div className="overflow-x-auto rounded-lg border border-line bg-surface">
          <table className="w-full text-sm">
            <thead className="bg-canvas text-left text-xs uppercase text-muted">
              <tr><th className="px-4 py-2">Page</th><th className="px-4 py-2">Commit</th><th className="px-4 py-2">Retrieved (UTC)</th><th className="px-4 py-2">sha256</th></tr>
            </thead>
            <tbody className="divide-y divide-line">
              {data.rows.map((s) => (
                <tr key={s.source_id}>
                  <td className="px-4 py-2"><a className="text-primary underline" href={s.url} target="_blank" rel="noreferrer">{s.source_id.split("/")[1]}</a></td>
                  <td className="px-4 py-2 font-mono text-xs">{s.repo_commit.slice(0, 8)}</td>
                  <td className="px-4 py-2 font-mono text-xs">{s.retrieved_at_utc}</td>
                  <td className="px-4 py-2 font-mono text-xs">{s.sha256.slice(0, 12)}…</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
