# Bugs & Iterations

## ITER-001 — 2026-10-20 — Initial archive import
- Built `scripts/sync.py`: paginates `/api/v1/archive`, fetches each post's HTML, converts to Markdown with markdownify, writes `essays/YYYY-MM-DD-slug.md` + `essays/INDEX.md`.
- Imported 36 essays (2025-10-16 → 2026-10-17). The first archive page only returns 23, so pagination is required.
- Strips Substack's "Thanks for reading / Subscribe now" boilerplate. Images stay as Substack CDN links.
