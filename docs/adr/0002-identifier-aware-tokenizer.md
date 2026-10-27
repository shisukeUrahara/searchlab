# 0002 Identifier-aware tokenizer

**Decision.** Lowercase, then emit each compound token whole (`x-ratelimit-remaining`, `crypto.timingsafeequal`, `sha256=`) **and** its parts (`x`, `ratelimit`, `remaining`).

**Why.** A plain word tokenizer splits API names apart and loses exact-match precision. Emitting both lets an exact query match the whole token and a partial query still match.

**Rejected.** Character n-grams (bigger index, noisier ranks). Whitespace split only (misses punctuation-attached tokens).

**Known gap.** No stemming and no stop words. Both retrievers index `heading + text` so they see identical content.
