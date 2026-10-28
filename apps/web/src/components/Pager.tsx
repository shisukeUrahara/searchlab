import { ChevronLeft, ChevronRight } from "lucide-react";

interface Props {
  total: number;
  pageSize: number;
  offset: number;
  onChange: (offset: number) => void;
  noun?: string;
}

export function Pager({ total, pageSize, offset, onChange, noun = "items" }: Props) {
  const pages = Math.max(1, Math.ceil(total / pageSize));
  const page = Math.floor(offset / pageSize) + 1;
  const from = total === 0 ? 0 : offset + 1;
  const to = Math.min(offset + pageSize, total);
  return (
    <nav aria-label="Pagination" className="flex flex-wrap items-center justify-between gap-3 text-sm">
      <p className="font-mono text-xs text-muted" aria-live="polite">
        Showing {from}–{to} of {total} {noun}
      </p>
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={() => onChange(Math.max(0, offset - pageSize))}
          disabled={page <= 1}
          aria-label="Previous page"
          className="grid size-9 place-items-center rounded-lg border border-line disabled:opacity-40"
        >
          <ChevronLeft className="size-4" aria-hidden />
        </button>
        <span className="font-mono text-xs">
          Page {page} of {pages}
        </span>
        <button
          type="button"
          onClick={() => onChange(offset + pageSize)}
          disabled={page >= pages}
          aria-label="Next page"
          className="grid size-9 place-items-center rounded-lg border border-line disabled:opacity-40"
        >
          <ChevronRight className="size-4" aria-hidden />
        </button>
      </div>
    </nav>
  );
}
