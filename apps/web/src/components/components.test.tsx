import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { KpiCards } from "./eval/KpiCards";
import { firstRank, rankTone } from "./eval/RankHeatmap";
import { Pager } from "./Pager";
import { MethodColumn } from "./search/MethodColumn";
import { Empty, ErrorBox, Loading } from "./StateViews";
import { ApiError, type MethodResult, type ScoreRow } from "@/lib/api";

const result: MethodResult = {
  method: "bm25",
  latency_ms: 1.234,
  hits: [
    { rank: 1, score: 9.5, chunk_id: "a", title: "T", heading: "Headers", snippet: "x-ratelimit", url: "u", source_id: "nasa/npr-7123-1d", page: 41 },
    { rank: 2, score: 4.1, chunk_id: "b", title: "T", heading: "Other", snippet: "foo", url: "u", source_id: "nasa/x", page: null },
  ],
};

const docs = { "nasa/npr-7123-1d": "NPR 7123.1D" };

describe("MethodColumn", () => {
  it("marks the expected chunk and reports its rank", () => {
    render(<MethodColumn docNumbers={docs} result={result} goldIds={["b"]} onOpen={() => {}} />);
    expect(screen.getByText("Expected passage at rank 2")).toBeInTheDocument();
    expect(screen.getAllByText("expected")).toHaveLength(1);
  });

  it("says when the expected chunk is missing", () => {
    render(<MethodColumn docNumbers={docs} result={result} goldIds={["zzz"]} onOpen={() => {}} />);
    expect(screen.getByText("Expected passage not in these results")).toBeInTheDocument();
  });

  it("shows no verdict banner without a labeled query", () => {
    render(<MethodColumn docNumbers={docs} result={result} goldIds={[]} onOpen={() => {}} />);
    expect(screen.queryByText(/Expected passage/)).toBeNull();
  });

  it("opens a chunk on click", () => {
    const onOpen = vi.fn();
    render(<MethodColumn docNumbers={docs} result={result} goldIds={[]} onOpen={onOpen} />);
    fireEvent.click(screen.getByText("Headers"));
    expect(onOpen).toHaveBeenCalledWith("a");
  });

  it("shows document number and page, falls back to source id", () => {
    render(<MethodColumn docNumbers={docs} result={result} goldIds={[]} onOpen={() => {}} />);
    expect(screen.getByText("NPR 7123.1D · p.41")).toBeInTheDocument();
    expect(screen.getByText("x")).toBeInTheDocument();
  });

  it("explains a method that could not run without an embedding", () => {
    render(<MethodColumn docNumbers={docs} result={{ ...result, hits: [], error: "embedding_unavailable" }} goldIds={["a"]} onOpen={() => {}} />);
    expect(screen.getByText("Needs an embedding for this question")).toBeInTheDocument();
    expect(screen.queryByText(/Expected passage/)).toBeNull();
  });

  it("explains a rejected API key", () => {
    render(<MethodColumn docNumbers={docs} result={{ ...result, hits: [], error: "embedding_failed" }} goldIds={[]} onOpen={() => {}} />);
    expect(screen.getByText("The embedding provider rejected this request")).toBeInTheDocument();
  });

  it("handles empty results", () => {
    render(<MethodColumn docNumbers={docs} result={{ ...result, hits: [] }} goldIds={[]} onOpen={() => {}} />);
    expect(screen.getByText("No matching passages.")).toBeInTheDocument();
  });
});

describe("state views", () => {
  it("renders API error code, message and request id", () => {
    render(<ErrorBox error={new ApiError("invalid_request", "query: too short", "r1")} />);
    expect(screen.getByRole("alert")).toHaveTextContent("invalid_request");
    expect(screen.getByText("request_id r1")).toBeInTheDocument();
  });

  it("offers retry", () => {
    const retry = vi.fn();
    render(<ErrorBox error={new Error("x")} onRetry={retry} />);
    fireEvent.click(screen.getByText("Retry"));
    expect(retry).toHaveBeenCalled();
  });

  it("renders loading and empty", () => {
    render(<><Loading label="Searching" /><Empty title="Nothing" hint="Try again" /></>);
    expect(screen.getByRole("status")).toHaveTextContent("Searching");
    expect(screen.getByText("Try again")).toBeInTheDocument();
  });
});

describe("KpiCards", () => {
  it("shows MRR with CI, marks the best method and the delta vs BM25", () => {
    const scores: ScoreRow[] = [
      { method: "bm25", query_class: "all", n: 80, recall_at_5: 0.9, mrr_at_10: 0.685, mrr_ci: [0.58, 0.79] },
      { method: "hybrid", query_class: "all", n: 80, recall_at_5: 1, mrr_at_10: 0.875, recall_at_1: 0.775 },
    ];
    render(<KpiCards scores={scores} />);
    expect(screen.getByText("0.875")).toBeInTheDocument();
    expect(screen.getByText("95% CI [0.580, 0.790]")).toBeInTheDocument();
    expect(screen.getAllByText("Best MRR")).toHaveLength(1);
    expect(screen.getByText("+0.190 vs BM25")).toBeInTheDocument();
    expect(screen.getByText("77.5%")).toBeInTheDocument();
  });
});

describe("rank helpers", () => {
  it("finds the first gold rank or null", () => {
    const base = { query_id: "q", query_class: "x", method: "bm25" as const, hit_at_5: true, reciprocal_rank_at_10: 1 };
    expect(firstRank({ ...base, ranked_chunk_ids: ["a", "b"], gold_chunk_ids: ["b"] })).toBe(2);
    expect(firstRank({ ...base, ranked_chunk_ids: ["a"], gold_chunk_ids: ["z"] })).toBeNull();
  });
  it("maps ranks to distinct tones", () => {
    const tones = [1, 2, 4, 7, null].map(rankTone);
    expect(new Set(tones).size).toBe(5);
  });
});

describe("Pager", () => {
  it("shows range and disables edges", () => {
    const onChange = vi.fn();
    render(<Pager total={80} pageSize={15} offset={0} onChange={onChange} noun="queries" />);
    expect(screen.getByText("Showing 1–15 of 80 queries")).toBeInTheDocument();
    expect(screen.getByLabelText("Previous page")).toBeDisabled();
    fireEvent.click(screen.getByLabelText("Next page"));
    expect(onChange).toHaveBeenCalledWith(15);
  });
});
