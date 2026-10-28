/** One color per NASA document, shared by the map, sources page and legends. */
export const DOC_COLORS: Record<string, string> = {
  "nasa/se-handbook": "#2cc7ae",
  "nasa/pm-handbook": "#6c8cff",
  "nasa/npr-7120-5f": "#38bdf8",
  "nasa/npr-7123-1d": "#f0a04b",
  "nasa/npr-7150-2d": "#b07cf7",
};
export const FALLBACK_DOC_COLOR = "#94a3b8";

export function docColor(sourceId: string): string {
  return DOC_COLORS[sourceId] ?? FALLBACK_DOC_COLOR;
}
