#!/usr/bin/env python3
"""Audit WordPress URL coverage for the sellerchamp.com → sc_website migration."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"_site", "node_modules", ".cursor"}
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def post_body(text: str) -> str:
    m = FM_RE.match(text)
    return text[m.end() :] if m else text


def normalize_path(path: str) -> str:
    path = path.strip().strip('"\'')
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        path += "/"
    return path


def wp_paths_from_file(relpath: str) -> list[str]:
    paths = []
    for line in (ROOT / relpath).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        p = line.replace("https://sellerchamp.com", "").rstrip("/") + "/"
        if p == "//":
            p = "/"
        paths.append(p)
    return paths


def scan_site() -> tuple[set[str], dict[str, str]]:
    built: set[str] = set()
    redirects: dict[str, str] = {}

    for html in ROOT.rglob("*.html"):
        if any(part in SKIP_PARTS for part in html.parts) or "_posts" in html.parts:
            continue
        text = html.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        fm = text.split("---", 2)[1]
        perm = re.search(r"^permalink:\s*(.+)$", fm, re.M)
        if perm:
            built.add(normalize_path(perm.group(1)))
        for block in re.finditer(r"redirect_from:\s*\n((?:\s+-\s*.+\n)+)", fm):
            for line in block.group(1).splitlines():
                line = line.strip()
                if line.startswith("- "):
                    redirects[normalize_path(line[2:])] = str(html.relative_to(ROOT))

    return built, redirects


def scan_blog() -> set[str]:
    paths: set[str] = set()
    for md in (ROOT / "_posts").glob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        fm = text.split("---", 2)[1]
        perm = re.search(r"^permalink:\s*(.+)$", fm, re.M)
        if perm:
            paths.add(normalize_path(perm.group(1)))
        else:
            title = md.stem.split("-", 3)[-1] if md.stem.count("-") >= 3 else md.stem
            paths.add(f"/blog/{title}/")
    return paths


def elementor_posts() -> list[str]:
    out = []
    for md in (ROOT / "_posts").glob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        body = post_body(text)
        if re.search(r"class=[\"']elementor|elementor-widget|data-elementor", body, re.I):
            out.append(md.name)
    return sorted(out)


def refresh_inventory_from_sitemaps() -> tuple[int, int]:
    """Pull page/post URLs from sellerchamp.com into _data/wp_*.txt."""
    import urllib.request
    from xml.etree import ElementTree as ET

    ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    def fetch_locs(sitemap_url: str) -> list[str]:
        req = urllib.request.Request(sitemap_url, headers={"User-Agent": ua})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
        return sorted(
            el.text.strip()
            for el in root.findall(".//sm:loc", ns)
            if el.text
        )

    pages = fetch_locs("https://sellerchamp.com/page-sitemap.xml")
    posts = fetch_locs("https://sellerchamp.com/post-sitemap.xml")
    (ROOT / "_data/wp_pages.txt").write_text("\n".join(pages) + "\n", encoding="utf-8")
    (ROOT / "_data/wp_posts.txt").write_text("\n".join(posts) + "\n", encoding="utf-8")
    return len(pages), len(posts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="machine-readable summary (for CI)",
    )
    parser.add_argument(
        "--refresh-inventory",
        action="store_true",
        help="re-download page/post sitemaps into _data/wp_pages.txt and wp_posts.txt",
    )
    args = parser.parse_args()

    if args.refresh_inventory:
        n_pages, n_posts = refresh_inventory_from_sitemaps()
        print(f"Refreshed inventory: {n_pages} pages, {n_posts} posts")

    built, redirects = scan_site()
    wp_pages = set(wp_paths_from_file("_data/wp_pages.txt"))
    wp_posts = set(wp_paths_from_file("_data/wp_posts.txt"))
    blog = scan_blog()

    missing_pages = sorted(p for p in wp_pages if p not in built and p not in redirects)
    missing_posts = sorted(wp_posts - blog)
    legacy = elementor_posts()

    summary = {
        "wp_pages": len(wp_pages),
        "wp_posts": len(wp_posts),
        "built_page_permalinks": len(built),
        "redirect_from_rules": len(redirects),
        "missing_pages": missing_pages,
        "missing_blog_posts": missing_posts,
        "posts_with_elementor_markup": len(legacy),
    }

    if args.json:
        import json

        print(json.dumps(summary, indent=2))
        return 1 if missing_pages or missing_posts else 0

    print("=== Migration audit ===")
    print(f"WP pages: {summary['wp_pages']} | permalinks: {len(built)} | redirects: {len(redirects)}")
    print(f"Missing pages: {len(missing_pages)}")
    for m in missing_pages:
        print(f"  {m}")
    print(f"WP posts: {summary['wp_posts']} | blog permalinks: {len(blog)}")
    print(f"Missing posts: {len(missing_posts)}")
    for m in missing_posts[:20]:
        print(f"  {m}")
    if len(missing_posts) > 20:
        print(f"  ... +{len(missing_posts) - 20} more")
    print(f"Posts still on Elementor HTML (rewrite queue): {len(legacy)}")
    return 1 if missing_pages or missing_posts else 0


if __name__ == "__main__":
    sys.exit(main())