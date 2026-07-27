#!/usr/bin/env python3
"""Migrate SellerChamp WordPress blog posts to Jekyll Markdown.

Reads URLs from _data/wp_posts.txt, fetches each post, extracts title/date/body,
writes _posts/YYYY-MM-DD-slug.md with permalink /blog/slug/.
"""

from __future__ import annotations

import html as html_lib
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL_LIST = ROOT / "_data" / "wp_posts.txt"
POSTS_DIR = ROOT / "_posts"
USER_AGENT = "SellerChampJekyllMigrator/1.0 (+https://sellerchamp.com)"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract(tag: str, html: str, attr: str | None = None) -> str | None:
    if attr:
        m = re.search(rf'<{tag}[^>]*{attr}=["\']([^"\']+)["\']', html, re.I)
        return html_lib.unescape(m.group(1).strip()) if m else None
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.I | re.S)
    if not m:
        return None
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return html_lib.unescape(re.sub(r"\s+", " ", text)).strip()


def extract_content(html: str) -> str:
    patterns = [
        r'<div[^>]+class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>\s*(?:<footer|</article|<div class="fusion-)',
        r'<div[^>]+class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*(?:<footer|</article)',
        r'<article[^>]*>(.*?)</article>',
    ]
    body = None
    for pat in patterns:
        m = re.search(pat, html, re.I | re.S)
        if m and len(m.group(1)) > 200:
            body = m.group(1)
            break
    if not body:
        return "_Content could not be extracted automatically. Please re-import from WordPress._\n"

    # Drop scripts/styles
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.I | re.S)
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.I | re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    # Convert simple tags to markdown-ish HTML kept as HTML in MD
    # Keep a cleaned HTML block (Jekyll markdown allows HTML)
    body = re.sub(r"\s+", " ", body)
    body = re.sub(r">\s+<", ">\n<", body)
    # Limit extremely long noisy footers
    for stopper in ("Related Posts", "Leave a Reply", "You may also like"):
        idx = body.find(stopper)
        if idx > 0:
            body = body[:idx]
    return body.strip() + "\n"


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def yaml_escape(s: str) -> str:
    if any(c in s for c in ':#{}[]&*!|>\'"%@`'):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def migrate_one(url: str) -> bool:
    slug = slug_from_url(url)
    try:
        html = fetch(url)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL fetch {url}: {exc}")
        return False

    title = extract("h1", html) or extract("title", html) or slug.replace("-", " ").title()
    if title.endswith(" | SellerChamp"):
        title = title[: -len(" | SellerChamp")].strip()
    if "SellerChamp" in title and "|" in title:
        title = title.split("|")[0].strip()

    date = None
    for pat in [
        r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)',
        r'<time[^>]+datetime=["\']([^"\']+)',
        r'"datePublished"\s*:\s*"([^"]+)"',
    ]:
        m = re.search(pat, html, re.I)
        if m:
            date = m.group(1)[:10]
            break
    if not date:
        date = "2024-01-01"

    description = extract("meta", html)  # won't work well
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.I)
    description = html_lib.unescape(m.group(1).strip()) if m else ""

    author = None
    am = re.search(r'rel=["\']author["\'][^>]*>([^<]+)', html, re.I)
    if am:
        author = html_lib.unescape(am.group(1).strip())

    content = extract_content(html)
    out = POSTS_DIR / f"{date}-{slug}.md"
    fm = [
        "---",
        f"title: {yaml_escape(title)}",
        f"date: {date} 12:00:00 +0000",
        f"permalink: /blog/{slug}/",
    ]
    if description:
        fm.append(f"description: {yaml_escape(description)}")
    if author:
        fm.append(f"author: {yaml_escape(author)}")
    fm.append("---\n")
    out.write_text("\n".join(fm) + "\n" + content, encoding="utf-8")
    print(f"OK {out.name}")
    return True


def main() -> int:
    POSTS_DIR.mkdir(exist_ok=True)
    urls = [u.strip() for u in URL_LIST.read_text().splitlines() if u.strip().startswith("http")]
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(urls)
    ok = 0
    for i, url in enumerate(urls[:limit]):
        if migrate_one(url):
            ok += 1
        time.sleep(0.35)
        if (i + 1) % 25 == 0:
            print(f"... {i + 1}/{min(limit, len(urls))}")
    print(f"Done: {ok}/{min(limit, len(urls))} migrated")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
