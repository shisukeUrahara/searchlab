# SearchLab design system
Product: a retrieval benchmarking lab over NASA engineering handbooks. Audience: AI engineers and hiring managers. Tone: precise, calm, technical, editorial. No NASA logos.

## Color tokens (light / dark)
- canvas #F6F4EF / #0A0F1A
- surface #FFFFFF / #111827
- surface-2 #EFECE5 / #172033
- ink (text) #0F1B2D / #E6EBF5
- muted text #5B6779 / #93A0B4
- line #E3DED4 / #233047
- primary #2F5BEA / #6C8CFF
- success #0E9F8A, warning #C98A1B, danger #C2463D
- method colors (charts, badges): BM25 #E0782E (orange), Dense #3B6FF0 (blue), Hybrid #11A38B (teal)

## Type
Headings Geist semibold, tight tracking. Body Inter 14-16px. IDs, scores, ranks, code: JetBrains Mono.

## Layout
8px grid, 12px radius cards, 1px hairline borders, very soft shadows. Max content width 1280px. Generous whitespace. Data dense but calm. Tables with sticky headers. Mobile: single column, bottom-sheet drawers, tabs instead of side-by-side columns.

## Components
Top nav with product mark (abstract orbit icon, no NASA insignia), links (Search, Vector map, Evaluation, Queries, Sources), light/dark toggle, small 'Unofficial · not affiliated with NASA' pill.
Rank badge (#1 mono chip), score bar, 'expected' check badge in success color, method legend dots.
