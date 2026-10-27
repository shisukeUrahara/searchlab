"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Search" },
  { href: "/queries", label: "Queries" },
  { href: "/eval", label: "Evaluation" },
  { href: "/sources", label: "Sources" },
];

export function Nav() {
  const path = usePathname();
  return (
    <header className="border-b border-line bg-surface">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-x-8 gap-y-2 px-4 py-3">
        <span className="text-lg font-semibold tracking-tight">SearchLab</span>
        <nav aria-label="Main" className="flex gap-1 text-sm">
          {LINKS.map((l) => {
            const active = l.href === "/" ? path === "/" : path.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={`rounded-md px-3 py-1.5 ${active ? "bg-primary text-primary-ink" : "text-muted hover:bg-canvas"}`}
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
        <span className="ml-auto rounded-full bg-warn-bg px-3 py-1 text-xs text-warn">
          Unofficial · not affiliated with GitHub · docs CC BY 4.0
        </span>
      </div>
    </header>
  );
}
