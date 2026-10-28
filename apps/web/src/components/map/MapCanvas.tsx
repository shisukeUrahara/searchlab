"use client";
import Graph from "graphology";
import { useEffect, useRef } from "react";
import type Sigma from "sigma";
import type { GraphData, Method } from "@/lib/api";
import { docColor } from "@/lib/docs";

export const QUERY_NODE = "__query__";
/** Graph units the query dot sits away from its hits' centre, so it never covers them. */
const QUERY_OFFSET = 28;
const LABEL = "#e6ebf5";
const METHOD_COLOR: Record<Method, string> = { bm25: "#f0924a", dense: "#6c8cff", hybrid: "#2cc7ae" };
function faded(hex: string, alpha = 0.22): string {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${alpha})`;
}

export interface MapView {
  /** chunk id -> method that should color it (first enabled method that hit it) */
  highlights: Map<string, Method>;
  /** chunk ids the query node links to (approximate placement at their centroid) */
  queryLinks: string[];
  selected: string | null;
  showEdges: boolean;
  edgeOpacity: number;
}

export interface MapApi {
  zoomIn: () => void;
  zoomOut: () => void;
  reset: () => void;
  focus: (id: string) => void;
}

interface Props {
  data: GraphData;
  view: MapView;
  onSelect: (id: string | null) => void;
  onHover: (id: string | null) => void;
  onReady: (api: MapApi) => void;
}

/** Imperative sigma.js (WebGL) canvas. React state flows in through a ref + refresh(). */
export function MapCanvas({ data, view, onSelect, onHover, onReady }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<Graph | null>(null);
  const viewRef = useRef(view);
  const hovered = useRef<string | null>(null);
  const handlers = useRef({ onSelect, onHover, onReady });

  useEffect(() => {
    handlers.current = { onSelect, onHover, onReady };
  });

  useEffect(() => {
    let killed = false;
    const graph = new Graph();
    data.nodes.forEach((n) => {
      graph.addNode(n.id, {
        x: n.x,
        y: -n.y,
        size: 3,
        color: docColor(data.docs[n.doc]?.source_id ?? ""),
        faded: faded(docColor(data.docs[n.doc]?.source_id ?? "")),
        label: n.heading.split(" > ").pop() ?? n.heading,
      });
    });
    data.edges.forEach(([a, b, w]) => {
      const s = data.nodes[a]?.id;
      const t = data.nodes[b]?.id;
      if (s && t && !graph.hasEdge(s, t)) graph.addEdge(s, t, { weight: w, size: 0.4 });
    });
    graphRef.current = graph;

    import("sigma").then(({ default: SigmaCtor }) => {
      if (killed || !container.current) return;
      const sigma = new SigmaCtor(graph, container.current, {
        settings: {
          hideEdgesOnMove: true,
          labelRenderedSizeThreshold: 9,
          labelDensity: 0.4,
          minCameraRatio: 0.02,
          maxCameraRatio: 3,
        },
        nodeReducer: (key, raw, attrs) => {
          const d = { ...raw, labelColor: LABEL };
          const v = viewRef.current;
          const isQuery = key === QUERY_NODE;
          const method = v.highlights.get(key);
          const active = v.highlights.size > 0;
          const isSel = v.selected === key;
          const isHover = hovered.current === key;
          if (isQuery) return { ...d, color: "#ffffff", size: 9, label: "your query", labelVisibility: "visible", zIndex: 3 };
          if (method) {
            return { ...d, color: METHOD_COLOR[method], size: isSel ? 10 : 7, labelVisibility: isSel || isHover ? "visible" : "auto", zIndex: 2 };
          }
          if (isSel) return { ...d, size: 8, color: "#ffffff", labelVisibility: "visible", zIndex: 3 };
          if (isHover) return { ...d, size: 5, labelVisibility: "visible", zIndex: 2 };
          return active ? { ...d, color: String(attrs.faded), label: null, zIndex: 0 } : { ...d, label: null };
        },
        edgeReducer: (key, d) => {
          const v = viewRef.current;
          const g = graphRef.current;
          const [s, t] = g ? g.extremities(key) : ["", ""];
          if (s === QUERY_NODE || t === QUERY_NODE) return { ...d, color: "rgba(255,255,255,0.7)", size: 1.2, zIndex: 2 };
          // while a query is highlighted, background links would hide the hits
          if (!v.showEdges || v.highlights.size > 0) return { ...d, visibility: "hidden" };
          const touchesSel = v.selected !== null && (s === v.selected || t === v.selected);
          if (touchesSel) return { ...d, color: "rgba(255,255,255,0.75)", size: 1, zIndex: 1 };
          return { ...d, color: `rgba(148,163,184,${v.edgeOpacity})` };
        },
      });
      sigma.on("clickNode", ({ node }) => handlers.current.onSelect(node === QUERY_NODE ? null : node));
      sigma.on("clickStage", () => handlers.current.onSelect(null));
      sigma.on("enterNode", ({ node }) => {
        hovered.current = node;
        handlers.current.onHover(node);
        sigma.refresh();
      });
      sigma.on("leaveNode", () => {
        hovered.current = null;
        handlers.current.onHover(null);
        sigma.refresh();
      });
      sigmaRef.current = sigma;
      const camera = sigma.getCamera();
      handlers.current.onReady({
        zoomIn: () => void camera.zoomIn({ duration: 250 }),
        zoomOut: () => void camera.zoomOut({ duration: 250 }),
        reset: () => void camera.reset({ duration: 300 }),
        focus: (id) => {
          const pos = sigma.getNodeDisplayData(id);
          if (pos) void camera.animate({ x: pos.x, y: pos.y, ratio: 0.45 }, { duration: 500 });
        },
      });
    });
    return () => {
      killed = true;
      sigmaRef.current?.kill();
      sigmaRef.current = null;
    };
  }, [data]);

  useEffect(() => {
    viewRef.current = view;
    const graph = graphRef.current;
    if (graph) {
      if (graph.hasNode(QUERY_NODE)) graph.dropNode(QUERY_NODE);
      const linked = view.queryLinks.filter((id) => graph.hasNode(id));
      if (linked.length) {
        const xs = linked.map((id) => graph.getNodeAttribute(id, "x") as number);
        const ys = linked.map((id) => graph.getNodeAttribute(id, "y") as number);
        const mean = (a: number[]) => a.reduce((s, v) => s + v, 0) / a.length;
        graph.addNode(QUERY_NODE, {
          x: mean(xs) - QUERY_OFFSET,
          y: mean(ys) + QUERY_OFFSET,
          size: 9,
          color: "#fff",
          label: "your query",
        });
        linked.forEach((id) => graph.addEdge(QUERY_NODE, id, { size: 1.2 }));
      }
    }
    sigmaRef.current?.refresh();
  }, [view]);

  return <div ref={container} className="absolute inset-0" aria-hidden />;
}
