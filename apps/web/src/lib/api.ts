export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Method = "bm25" | "dense" | "hybrid";
export const METHODS: Method[] = ["bm25", "dense", "hybrid"];
export const METHOD_LABEL: Record<Method, string> = {
  bm25: "BM25 (keyword)",
  dense: "Dense (vector)",
  hybrid: "Hybrid (RRF)",
};

export interface Hit {
  rank: number;
  score: number;
  chunk_id: string;
  title: string;
  heading: string;
  snippet: string;
  url: string;
}
export interface MethodResult {
  method: Method;
  latency_ms: number;
  hits: Hit[];
}
export interface SearchResponse {
  request_id: string;
  query: string;
  results: MethodResult[];
}
export interface LabeledQuery {
  query_id: string;
  text: string;
  query_class: "exact_id" | "paraphrase" | "distractor";
  split: "dev" | "test";
  gold_chunk_ids: string[];
}
export interface Chunk {
  chunk_id: string;
  source_id: string;
  title: string;
  heading: string;
  text: string;
  url: string;
}
export interface ScoreRow {
  method: Method;
  query_class: string;
  n: number;
  recall_at_5: number;
  mrr_at_10: number;
}
export interface CaseRow {
  query_id: string;
  query_class: string;
  method: Method;
  ranked_chunk_ids: string[];
  gold_chunk_ids: string[];
  hit_at_5: boolean;
  reciprocal_rank_at_10: number;
}
export interface EvalRun {
  manifest: Record<string, string | number | boolean | string[]>;
  scores: ScoreRow[];
  cases: CaseRow[];
}
export interface Source {
  source_id: string;
  url: string;
  repo_path: string;
  repo_commit: string;
  retrieved_at_utc: string;
  license: string;
  transformation: string;
  sha256: string;
}

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public requestId?: string,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, init);
  } catch {
    throw new ApiError("network_error", `Cannot reach the API at ${API_URL}. Is it running?`);
  }
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    throw new ApiError(body?.code ?? "http_error", body?.message ?? res.statusText, body?.request_id);
  }
  return body as T;
}

export const api = {
  search: (query: string, topK: number) =>
    request<SearchResponse>("/search", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ query, top_k: topK }),
    }),
  queries: (split: "dev" | "test") => request<LabeledQuery[]>(`/queries?split=${split}`),
  chunk: (id: string) => request<Chunk>(`/chunks/${encodeURIComponent(id)}`),
  sources: () => request<{ sources: Source[] }>("/sources"),
  runs: () => request<string[]>("/eval-runs"),
  run: (id: string) => request<EvalRun>(`/eval-runs/${encodeURIComponent(id)}`),
};
