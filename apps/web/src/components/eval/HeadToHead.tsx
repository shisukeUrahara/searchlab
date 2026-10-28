import { METHOD_META, type HeadToHead as H2H } from "@/lib/api";

export function HeadToHead({ rows }: { rows: H2H[] }) {
  return (
    <div className="space-y-5">
      {rows.map((r) => {
        const total = r.a_better + r.tie + r.b_better || 1;
        const seg = [
          { n: r.a_better, label: `${METHOD_META[r.a].short} better`, cls: METHOD_META[r.a].bar },
          { n: r.tie, label: "tie", cls: "bg-line" },
          { n: r.b_better, label: `${METHOD_META[r.b].short} better`, cls: METHOD_META[r.b].bar },
        ];
        return (
          <div key={`${r.a}-${r.b}`}>
            <div className="mb-1.5 flex flex-wrap justify-between gap-2 text-sm">
              <span className="font-medium">
                {METHOD_META[r.a].short} vs {METHOD_META[r.b].short}
              </span>
              <span className="font-mono text-xs text-muted">
                {seg.map((s) => `${s.n} ${s.label}`).join(" · ")}
              </span>
            </div>
            <div className="flex h-3 overflow-hidden rounded-full bg-surface-2" role="img" aria-label={seg.map((s) => `${s.n} ${s.label}`).join(", ")}>
              {seg.map((s) => (
                <div key={s.label} className={s.cls} style={{ width: `${(s.n / total) * 100}%` }} />
              ))}
            </div>
          </div>
        );
      })}
      <p className="text-xs text-muted">Per query: which method ranked the first expected passage higher. A miss counts as rank 11.</p>
    </div>
  );
}
