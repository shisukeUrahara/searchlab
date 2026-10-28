export const fmt = (v: number | undefined | null, digits = 3) => (v === undefined || v === null ? "—" : v.toFixed(digits));
export const pct = (v: number | undefined | null) => (v === undefined || v === null ? "—" : `${(v * 100).toFixed(1)}%`);
export const ci = (c: [number, number] | null | undefined, digits = 3) => (c ? `[${c[0].toFixed(digits)}, ${c[1].toFixed(digits)}]` : "");
