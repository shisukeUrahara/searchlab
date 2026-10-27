import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { MetricTable } from "./MetricTable";
import { RankingColumn } from "./RankingColumn";
import { Empty, ErrorBox, Loading } from "./StateViews";
import { ApiError, type MethodResult, type ScoreRow } from "@/lib/api";

const result: MethodResult = {
  method: "bm25",
  latency_ms: 1.234,
  hits: [
    { rank: 1, score: 9.5, chunk_id: "a", title: "T", heading: "Headers", snippet: "x-ratelimit", url: "u" },
    { rank: 2, score: 4.1, chunk_id: "b", title: "T", heading: "Other", snippet: "foo", url: "u" },
  ],
};

describe("RankingColumn", () => {
  it("marks the expected chunk and reports its rank", () => {
    render(<RankingColumn result={result} goldIds={["b"]} onOpen={() => {}} />);
    expect(screen.getByText("Expected chunk found at rank 2")).toBeInTheDocument();
    expect(screen.getAllByText("✓ expected")).toHaveLength(1);
  });

  it("says when the expected chunk is missing", () => {
    render(<RankingColumn result={result} goldIds={["zzz"]} onOpen={() => {}} />);
    expect(screen.getByText("Expected chunk not in these results")).toBeInTheDocument();
  });

  it("shows no verdict banner without a labeled query", () => {
    render(<RankingColumn result={result} goldIds={[]} onOpen={() => {}} />);
    expect(screen.queryByText(/Expected chunk/)).toBeNull();
  });

  it("opens a chunk on click", () => {
    const onOpen = vi.fn();
    render(<RankingColumn result={result} goldIds={[]} onOpen={onOpen} />);
    fireEvent.click(screen.getByText("Headers"));
    expect(onOpen).toHaveBeenCalledWith("a");
  });

  it("handles empty results", () => {
    render(<RankingColumn result={{ ...result, hits: [] }} goldIds={[]} onOpen={() => {}} />);
    expect(screen.getByText("No matching chunks.")).toBeInTheDocument();
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

describe("MetricTable", () => {
  it("formats metrics to 3 decimals", () => {
    const scores: ScoreRow[] = [
      { method: "hybrid", query_class: "all", n: 30, recall_at_5: 1, mrr_at_10: 0.8561 },
    ];
    render(<MetricTable scores={scores} />);
    expect(screen.getByText("1.000")).toBeInTheDocument();
    expect(screen.getByText("0.856")).toBeInTheDocument();
  });
});
