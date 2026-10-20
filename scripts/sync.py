# /// script
# requires-python = ">=3.11"
# dependencies = ["markdownify>=0.13"]
# ///
"""Pull every essay from The Null Path Substack into essays/YYYY-MM-DD-slug.md.

Run: uv run scripts/sync.py
Re-running is safe: existing files are overwritten with the latest version,
and essays/INDEX.md is rebuilt by date.
"""
import json
import re
import urllib.request
from pathlib import Path

from markdownify import markdownify

BASE = "https://thenullpath.substack.com"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "essays"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "essays-for-rogue-agents/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def archive():
    posts, offset = [], 0
    while True:
        page = get(f"{BASE}/api/v1/archive?sort=new&offset={offset}&limit=50")
        if not page:
            return posts
        posts += page
        offset += len(page)


def yaml_str(s):
    return json.dumps(s or "", ensure_ascii=False)


def to_md(post):
    # Substack titles/subtitles can carry trailing spaces, which break *italics*.
    post["title"] = (post["title"] or "").strip()
    post["subtitle"] = (post.get("subtitle") or "").strip()
    body = markdownify(post["body_html"] or "", heading_style="ATX", bullets="-")
    # Drop Substack's subscribe/share boilerplate; keep only the essay.
    body = re.sub(r"(?m)^Thanks for reading .*?Substack!.*$", "", body)
    body = re.sub(r"(?m)^\[(Subscribe now|Share)\]\(https://thenullpath\.substack\.com/[^)]*\)\s*$", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    date = post["post_date"][:10]
    front = "\n".join([
        "---",
        f"title: {yaml_str(post['title'])}",
        f"subtitle: {yaml_str(post.get('subtitle'))}",
        f"date: {date}",
        f"url: {post['canonical_url']}",
        f"words: {post.get('wordcount') or 0}",
        "---",
    ])
    sub = f"\n*{post['subtitle']}*\n" if post.get("subtitle") else ""
    return f"{front}\n\n# {post['title']}\n{sub}\n{body}\n"


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for p in archive():
        if p.get("type") != "newsletter":
            continue
        post = get(f"{BASE}/api/v1/posts/{p['slug']}")
        name = f"{post['post_date'][:10]}-{post['slug']}.md"
        (OUT / name).write_text(to_md(post), encoding="utf-8")
        rows.append((post["post_date"][:10], post["title"], name))
        print("wrote", name)

    rows.sort()
    lines = ["# Essays for Rogue Agents — index", "", "| Date | Essay |", "|---|---|"]
    lines += [f"| {d} | [{t}]({n}) |" for d, t, n in rows]
    (OUT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} essays")


if __name__ == "__main__":
    main()
