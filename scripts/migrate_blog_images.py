#!/usr/bin/env python3
"""Download blog images from sellerchamp.com/wp-content into assets/images/blog/."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_IMG = ROOT / "assets" / "images" / "blog"
MAP_FILE = ROOT / "_data" / "blog_image_map.json"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

WP_URL_RE = re.compile(
    r"https?://(?:www\.)?sellerchamp\.com(/wp-content/uploads/[^\"'\s>)]+)",
    re.I,
)
WP_REL_RE = re.compile(r'(?:src|href)="(/wp-content/uploads/[^"]+)"', re.I)
MD_IMG_RE = re.compile(
    r"!\[[^\]]*\]\((https?://[^)]+|/wp-content/uploads/[^)]+)\)",
    re.I,
)

SCAN_GLOBS = ("_posts/*.md", "*.html", "_includes/*.html", "pages/**/*.html", "landing/**/*.html")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def local_path_for(wp_path: str) -> Path:
    """Map /wp-content/uploads/2024/09/foo.png -> assets/images/blog/2024/09/foo.png"""
    rel = wp_path.split("/wp-content/uploads/", 1)[-1]
    rel = rel.lstrip("/")
    return BLOG_IMG / rel


def public_url(local: Path) -> str:
    rel = local.relative_to(ROOT / "assets")
    return "/assets/" + rel.as_posix()


def collect_urls() -> dict[str, str]:
    """remote absolute URL -> wp path (/wp-content/...)"""
    found: dict[str, str] = {}
    for pattern in SCAN_GLOBS:
        for path in ROOT.glob(pattern):
            if "_site" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for m in WP_URL_RE.finditer(text):
                wp = m.group(1).split("?")[0]
                found[f"https://sellerchamp.com{wp}"] = wp
            for m in WP_REL_RE.finditer(text):
                wp = m.group(1).split("?")[0]
                found[f"https://sellerchamp.com{wp}"] = wp
            for m in MD_IMG_RE.finditer(text):
                u = m.group(1)
                if u.startswith("/wp-content"):
                    wp = u.split("?")[0]
                    found[f"https://sellerchamp.com{wp}"] = wp
    return found


def replace_in_file(path: Path, mapping: dict[str, str]) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    orig = text
    for remote, local_url in mapping.items():
        text = text.replace(remote, local_url)
        wp = remote.replace("https://sellerchamp.com", "").replace("http://sellerchamp.com", "")
        text = text.replace(wp, local_url)
        text = text.replace(f"https://www.sellerchamp.com{wp}", local_url)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-download", action="store_true", help="Only rewrite using existing map")
    args = parser.parse_args()

    remote_urls = collect_urls()
    print(f"Found {len(remote_urls)} unique wp-content asset URLs")

    url_map: dict[str, str] = {}
    if MAP_FILE.exists():
        url_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))

    failed: list[str] = []
    downloaded = 0
    skipped = 0

    for remote, wp_path in sorted(remote_urls.items()):
        dest = local_path_for(wp_path)
        local_url = public_url(dest)

        if dest.exists() and dest.stat().st_size > 0:
            url_map[remote] = local_url
            skipped += 1
            continue

        if args.skip_download:
            if remote in url_map:
                continue
            failed.append(remote)
            continue

        if args.dry_run:
            print(f"would fetch {remote} -> {dest}")
            url_map[remote] = local_url
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = fetch(remote)
            if len(data) < 50:
                failed.append(remote)
                continue
            dest.write_bytes(data)
            url_map[remote] = local_url
            downloaded += 1
            if downloaded % 25 == 0:
                print(f"  downloaded {downloaded}...")
            time.sleep(0.05)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"FAIL {remote}: {e}", file=sys.stderr)
            failed.append(remote)

    if not args.dry_run:
        MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
        MAP_FILE.write_text(json.dumps(url_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    changed_files = 0
    for pattern in SCAN_GLOBS:
        for path in ROOT.glob(pattern):
            if replace_in_file(path, url_map):
                changed_files += 1

    print(f"Downloaded: {downloaded}, already present: {skipped}, failed: {len(failed)}")
    print(f"Rewrote references in {changed_files} files")
    if failed:
        print("Some URLs failed (posts may still reference live wp-content for those):", file=sys.stderr)
        for u in failed[:15]:
            print(f"  {u}", file=sys.stderr)
        if len(failed) > 15:
            print(f"  ... +{len(failed) - 15} more", file=sys.stderr)
        return 1 if downloaded == 0 and not url_map else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())