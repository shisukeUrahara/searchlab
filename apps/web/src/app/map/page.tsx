"use client";
import { Expand, Minus, Plus, RotateCcw, Search } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Inspector, type Neighbor } from "@/components/map/Inspector";
import { MapCanvas, type MapApi, type MapView } from "@/components/map/MapCanvas";
import { ErrorBox, Loading } from "@/components/StateViews";
import { api, METHODS, METHOD_META, type Corpus, type GraphData, type Method, type SearchResponse } from "@/lib/api";
import { docColor } from "@/lib/docs";

const HITS_PER_METHOD = 10;
const CONTROLS = [
  { label: "Zoom in", icon: Plus, action: "zoomIn" },
  { label: "Zoom out", icon: Minus, action: "zoomOut" },
  { label: "Reset view", icon: RotateCcw, action: "reset" },
  { label: "Fullscreen", icon: Expand, action: "fullscreen" },
] as const;
const QUERY_LINKS = 5;

export default function MapPage() {
  const [data, setData] = useState<GraphData | null>(null);
  const [corpus, setCorpus] = useState<Corpus | null>(null);
  const [error, setError] = useState<unknown>();
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<unknown>();
  const [enabled, setEnabled] = useState<Record<Method, boolean>>({ bm25: true, dense: true, hybrid: true });
  const [showEdges, setShowEdges] = useState(true);
  const [edgeOpacity, setEdgeOpacity] = useState(0.07);
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const mapApi = useRef<MapApi | null>(null);
  const frame = useRef<HTMLDivElement>(null);

  const highlight = useCallback(async (q: string) => {
    if (!q.trim()) return;
    setQuery(q);
    setSearching(true);
    setSearchError(undefined);
    try {
      setResult(await api.search(q, HITS_PER_METHOD));
    } catch (e) {
      setSearchError(e);
    } finally {
      setSearching(false);
    }
  }, []);

  useEffect(() => {
    Promise.all([api.graph(), api.corpus()])
      .then(([g, c]) => {
        setData(g);
        setCorpus(c);
      })
      .catch(setError);
    const q = new URLSearchParams(window.location.search).get("q");
    const timer = q ? setTimeout(() => void highlight(q), 0) : undefined;
    return () => clearTimeout(timer);
  }, [highlight]);

  const nodeIndex = useMemo(() => new Map((data?.nodes ?? []).map((n, i) => [n.id, i])), [data]);
  const adjacency = useMemo(() => {
    const adj = new Map<number, [number, number][]>();
    data?.edges.forEach(([a, b, w]) => {
      adj.set(a, [...(adj.get(a) ?? []), [b, w]]);
      adj.set(b, [...(adj.get(b) ?? []), [a, w]]);
    });
    return adj;
  }, [data]);

  const view: MapView = useMemo(() => {
    const highlights = new Map<string, Method>();
    // later methods overwrite earlier ones, so hybrid wins where methods agree
    METHODS.forEach((m) => {
      if (!enabled[m]) return;
      result?.results.find((r) => r.method === m)?.hits.forEach((h) => highlights.set(h.chunk_id, m));
    });
    const hybrid = result?.results.find((r) => r.method === "hybrid")?.hits ?? [];
    return {
      highlights,
      queryLinks: result ? hybrid.slice(0, QUERY_LINKS).map((h) => h.chunk_id) : [],
      selected,
      showEdges,
      edgeOpacity,
    };
  }, [result, enabled, selected, showEdges, edgeOpacity]);

  const neighbors: Neighbor[] = useMemo(() => {
    if (!data || !selected) return [];
    const i = nodeIndex.get(selected);
    if (i === undefined) return [];
    return (adjacency.get(i) ?? [])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([j, w]) => ({ id: data.nodes[j].id, heading: data.nodes[j].heading, sim: w }));
  }, [data, selected, nodeIndex, adjacency]);

  const ranks = useMemo(
    () =>
      (result?.results ?? []).flatMap((r) => {
        const hit = r.hits.find((h) => h.chunk_id === selected);
        return hit ? [{ method: METHOD_META[r.method].short, rank: hit.rank }] : [];
      }),
    [result, selected],
  );

  const control = useCallback((action: (typeof CONTROLS)[number]["action"]) => {
    if (action === "fullscreen") void frame.current?.requestFullscreen?.();
    else mapApi.current?.[action]();
  }, []);

  const pick = useCallback((id: string) => {
    setSelected(id);
    mapApi.current?.focus(id);
  }, []);

  if (error !== undefined) return <ErrorBox error={error} />;
  if (!data || !corpus) return <Loading label="Loading 3,000+ passages" />;

  const hoverNode = hovered ? data.nodes[nodeIndex.get(hovered) ?? -1] : undefined;
  const hybridHits = result?.results.find((r) => r.method === "hybrid")?.hits ?? [];
  const counts = corpus.docs.reduce<Record<string, number>>((acc, d) => ({ ...acc, [d.source_id]: d.chunks }), {});
  const facts = [
    ["Vectors", `${corpus.embedding_dims} → 2D`],
    ["Metric", "cosine"],
    ["UMAP neighbours", "15"],
    ["Min dist", "0.1"],
    ["kNN links", `k=${data.meta.knn}`],
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <h1 className="text-3xl font-semibold md:text-4xl">Embedding map</h1>
          <p className="mt-2 text-muted">
            Every dot is one of {data.nodes.length.toLocaleString()} passages, placed by meaning. Lines join each passage to its{" "}
            {data.meta.knn} most similar neighbours ({data.edges.length.toLocaleString()} links). Search to light up what each method retrieves.
          </p>
        </div>
        <ul className="flex flex-wrap gap-2 font-mono text-xs">
          {facts.map(([k, v]) => (
            <li key={k} className="rounded-lg border border-line bg-surface px-2.5 py-1 text-muted">
              {k}: <span className="text-ink">{v}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="grid gap-4 lg:grid-cols-[300px_minmax(0,1fr)]">
        <aside className="order-2 space-y-4 rounded-2xl border border-line bg-surface p-4 shadow-card lg:order-none" aria-label="Map controls">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void highlight(query);
            }}
          >
            <label htmlFor="mq" className="text-sm font-semibold">Highlight a query</label>
            <div className="mt-2 flex gap-2">
              <input
                id="mq"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. KDP C entrance criteria"
                className="h-10 min-w-0 flex-1 rounded-lg border border-line bg-canvas px-3 text-sm outline-none focus:border-primary"
              />
              <button type="submit" disabled={!query.trim() || searching} aria-label="Highlight" className="grid size-10 place-items-center rounded-lg bg-primary text-primary-ink disabled:opacity-50">
                <Search className="size-4" aria-hidden />
              </button>
            </div>
            {result && (
              <button type="button" onClick={() => { setResult(null); setSelected(null); }} className="mt-2 text-xs text-muted underline underline-offset-2">
                Clear highlight
              </button>
            )}
          </form>
          {searchError !== undefined && <ErrorBox error={searchError} />}

          <fieldset>
            <legend className="text-sm font-semibold">Method halos <span className="font-mono text-xs font-normal text-muted">top {HITS_PER_METHOD}</span></legend>
            <div className="mt-2 space-y-1.5">
              {METHODS.map((m) => (
                <label key={m} className="flex cursor-pointer items-center gap-3 rounded-lg border border-line px-3 py-2 text-sm">
                  <input type="checkbox" checked={enabled[m]} onChange={(e) => setEnabled({ ...enabled, [m]: e.target.checked })} className="accent-[var(--primary)]" />
                  <span className={`size-2.5 rounded-full ${METHOD_META[m].dot}`} aria-hidden />
                  {METHOD_META[m].short}
                </label>
              ))}
            </div>
          </fieldset>

          <fieldset className="space-y-2">
            <legend className="text-sm font-semibold">Display</legend>
            <label className="flex items-center justify-between text-sm">
              Similarity links
              <input type="checkbox" checked={showEdges} onChange={(e) => setShowEdges(e.target.checked)} className="accent-[var(--primary)]" />
            </label>
            <label className="flex items-center justify-between gap-3 font-mono text-xs text-muted">
              Link opacity
              <input type="range" min={0.02} max={0.5} step={0.02} value={edgeOpacity} disabled={!showEdges} onChange={(e) => setEdgeOpacity(Number(e.target.value))} className="w-28 accent-[var(--primary)]" />
            </label>
          </fieldset>

          <div>
            <h2 className="text-sm font-semibold">Documents</h2>
            <ul className="mt-2 space-y-1.5 text-sm">
              {data.docs.map((d) => (
                <li key={d.source_id} className="flex items-center gap-2">
                  <span className="size-2.5 shrink-0 rounded-full" style={{ background: docColor(d.source_id) }} aria-hidden />
                  <span className="truncate" title={d.title}>{d.doc_number}</span>
                  <span className="ml-auto font-mono text-xs text-muted">{counts[d.source_id] ?? 0}</span>
                </li>
              ))}
            </ul>
          </div>

          {hybridHits.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold">Hybrid top hits</h2>
              <ol className="mt-2 space-y-1">
                {hybridHits.slice(0, 5).map((h) => (
                  <li key={h.chunk_id}>
                    <button onClick={() => pick(h.chunk_id)} className="flex w-full gap-2 rounded-md px-2 py-1 text-left text-xs hover:bg-surface-2">
                      <span className="font-mono text-muted">#{h.rank}</span>
                      <span className="truncate">{h.heading.split(" > ").pop()}</span>
                    </button>
                  </li>
                ))}
              </ol>
            </div>
          )}
        </aside>

        <div ref={frame} className="relative order-1 h-[70vh] min-h-[420px] overflow-hidden lg:order-none rounded-2xl border border-line bg-[#0a0f1a] shadow-card">
          <MapCanvas data={data} view={view} onSelect={setSelected} onHover={setHovered} onReady={(a) => (mapApi.current = a)} />
          <p className="pointer-events-none absolute left-4 top-4 max-w-[70%] truncate rounded-lg bg-black/50 px-3 py-1.5 font-mono text-xs text-[#e6ebf5]" aria-live="polite">
            {hoverNode ? `${data.docs[hoverNode.doc]?.doc_number} · ${hoverNode.heading}${hoverNode.page ? ` · p.${hoverNode.page}` : ""}` : searching ? "Searching…" : "Hover a dot · scroll to zoom · drag to pan"}
          </p>
          <div className="absolute bottom-4 right-4 flex gap-1 rounded-xl border border-white/10 bg-black/50 p-1 text-[#e6ebf5]">
            {CONTROLS.map(({ label, icon: Icon, action }) => (
              <button key={label} onClick={() => control(action)} aria-label={label} title={label} className="grid size-9 place-items-center rounded-lg hover:bg-white/10">
                <Icon className="size-4" aria-hidden />
              </button>
            ))}
          </div>
          {selected && (
            <div className="absolute inset-x-3 bottom-16 top-auto max-h-[60%] md:inset-y-4 md:left-auto md:right-4 md:max-h-none md:w-[360px]">
              <Inspector chunkId={selected} docs={corpus.docs} neighbors={neighbors} ranks={ranks} onPick={pick} onClose={() => setSelected(null)} />
            </div>
          )}
        </div>
      </div>
      <p className="font-mono text-xs text-muted">
        Layout: {data.meta.layout}. Positions are a 2D approximation; nearby dots are similar, but distances are not exact. The query dot is drawn at the centre of its top {QUERY_LINKS} hybrid hits.
      </p>
    </div>
  );
}
