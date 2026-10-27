# 0001 Chunking and cleaning

**Decision.** Keep the github.com view of each page. Resolve Liquid `ifversion` blocks (only `fpt` active), substitute a small map of `data variables`, drop `data reusables`. Split on `##`–`####` headings (ignoring `#` inside code fences), pack paragraphs up to 1,200 characters, never cut inside a paragraph. Chunk ID = first 16 hex chars of sha256(source, heading path, text).

**Why.** Content-derived IDs make reindexing idempotent: unchanged text keeps its ID and a changed chunk gets a new one. Heading paths give readable citations.

**Rejected.** Fixed-size windows (cut identifiers and code in half). Keeping all Liquid branches (server and cloud variants contradict each other).

**Cost.** Reusables are dropped, so some sections lose text. One chunk is 1,467 characters because a single paragraph exceeds the cap.
