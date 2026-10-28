export function Logo() {
  return (
    <svg viewBox="0 0 32 32" className="size-7" aria-hidden>
      <circle cx="16" cy="16" r="4.5" className="fill-primary" />
      <ellipse cx="16" cy="16" rx="13" ry="6" transform="rotate(-28 16 16)"
        className="fill-none stroke-ink/70" strokeWidth="1.6" />
      <circle cx="27" cy="10.5" r="2" className="fill-m-hybrid" />
    </svg>
  );
}
