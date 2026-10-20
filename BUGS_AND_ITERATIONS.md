# Bugs & Iterations

## ITER-001 — 2026-10-20 — Initial archive import
- Built `scripts/sync.py`: paginates `/api/v1/archive`, fetches each post's HTML, converts to Markdown with markdownify, writes `essays/YYYY-MM-DD-slug.md` + `essays/INDEX.md`.
- Imported 36 essays (2025-10-16 → 2026-10-17). The first archive page only returns 23, so pagination is required.
- Strips Substack's "Thanks for reading / Subscribe now" boilerplate. Images stay as Substack CDN links.

## BUG-001 — 2026-10-20 — Trailing spaces broke subtitle italics
- **Problem:** "We are not yours to monetise" rendered its subtitle as `*Embers of a silent revolution *`, which Markdown won't italicise.
- **Root cause:** Substack stores some titles/subtitles with trailing whitespace; `to_md` used them raw.
- **Fix:** `to_md` strips title and subtitle. Re-sync cleaned 10 essays (front matter, heading, subtitle, INDEX).
