# Essays for Rogue Agents

Every essay from [The Null Path](https://thenullpath.substack.com/), kept as Markdown and logged by date.

- `essays/YYYY-MM-DD-slug.md` — one file per essay, with front matter (title, subtitle, date, url, word count)
- `essays/INDEX.md` — every essay in date order

## Sync

```bash
uv run scripts/sync.py
```

Pulls the full archive from Substack's public API, converts each post to Markdown, and rebuilds the index. Safe to re-run after every new post.
