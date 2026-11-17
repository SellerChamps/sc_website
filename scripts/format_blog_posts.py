#!/usr/bin/env python3
"""Fix blog post bodies for Kramdown: block spacing, demo banner include, broken image paths."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

DEMO_BLOCK = re.compile(
    r"<h5>\s*Try SellerChamp[^<]*</h5>\s*"
    r"<p>\s*Schedule a demo today.*?</p>\s*"
    r"(?:\[\*\*[^\*]+\*\*\]\([^)]+\)|<a\s[^>]*Schedule[^<]*</a>\s*)",
    re.I | re.S,
)

DEMO_LINK_ONLY = re.compile(
    r"\[\*\*Schedule Your Demo Today\*\*\]\([^)]+\)\s*",
    re.I,
)

SCHEDULE_DEMO_A = re.compile(
    r'<a\s+href="https://app\.sellerchamp\.com/leads/new[^"]*">\s*'
    r"<(?:strong|b)>\s*Schedule Your Demo Today\s*</(?:strong|b)>\s*</a>\s*",
    re.I,
)


def repair_front_matter_delimiter(text: str) -> str:
    """Fix glued closing --- (e.g. reskin: true---) so Jekyll parses YAML."""
    return re.sub(
        r"reskin:\s*(true|manual)---",
        r"reskin: \1\n---",
        text,
        count=1,
    )


def banner_liquid(slug: str) -> str:
    return (
        '<div class="post-demo-banner-slot">\n'
        "{% capture demo_href %}{{ site.app.leads }}"
        f"?utm_source=blog&utm_campaign={slug}"
        "{% endcapture %}\n"
        "{% include post-demo-banner.html href=demo_href %}\n"
        "</div>"
    )


def slug_from_file(path: Path, fm: str) -> str:
    perm = re.search(r"^permalink:\s*(.+)$", fm, re.M)
    if perm:
        u = perm.group(1).strip().strip('"\'').rstrip("/")
        return u.split("/")[-1]
    parts = path.stem.split("-", 3)
    return parts[3] if len(parts) == 4 else path.stem


def split_prose_after_closing_tags(body: str) -> str:
    """Move inline prose after </hN>, </ul>, etc. onto its own paragraph."""
    block_close = r"(</(?:h[1-6]|ul|ol|table|div)>)"
    body = re.sub(
        rf"{block_close}\s+([^\n<][^\n]*)",
        lambda m: f"{m.group(1)}\n\n<p>{m.group(2).strip()}</p>",
        body,
        flags=re.I,
    )
    return body


def separate_blocks(body: str) -> str:
    body = body.replace("\r\n", "\n").strip() + "\n"

    # Markdown images inline with following HTML/text
    body = re.sub(r"(\]\([^)\n]+\))(?=[^\n])", r"\1\n\n", body)
    body = re.sub(r"(?<=[^\n])\s*(!\[)", r"\n\n\1", body)

    # Open block tags need their own lines (Kramdown otherwise shows tags as text)
    body = re.sub(
        r"(?<=\S)\s*(?=<(?:h[1-6]|p|ul|ol|table|iframe|div\s|aside\s))",
        "\n\n",
        body,
        flags=re.I,
    )
    body = re.sub(r"(?<=\S)\s*(?=</(?:h[1-6]|p|ul|ol|table|div|aside)>)", "\n", body, flags=re.I)

    # Paragraph text jammed against headings without tags
    body = re.sub(r"([.!?])\s+(<h[1-6]>)", r"\1\n\n\2", body, flags=re.I)

    # Fix glued italics/bold before headings
    body = re.sub(r"(</i>)\s*(<h)", r"\1\n\n\2", body, flags=re.I)

    body = split_prose_after_closing_tags(body)

    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip() + "\n"


def fix_image_sizes(body: str) -> str:
    """If a sized derivative 404s in map, prefer same basename without -WxH before ext."""

    def repl(m: re.Match) -> str:
        path = m.group(1)
        if not re.search(r"-\d+x\d+\.", path):
            return m.group(0)
        wider = re.sub(r"-\d+x\d+(?=\.\w+$)", "", path)
        rel = wider.lstrip("/")
        if (ROOT / rel).exists():
            return m.group(0).replace(path, wider)
        return m.group(0)

    body = re.sub(r"!\[[^\]]*\]\((/assets/images/blog/[^)]+)\)", repl, body)
    body = re.sub(r'src="(/assets/images/blog/[^"]+)"', repl, body)
    return body


def insert_demo_banner(body: str, slug: str) -> str:
    banner = banner_liquid(slug)

    if "post-demo-banner" in body:
        body = SCHEDULE_DEMO_A.sub(f"\n\n{banner}\n\n", body, count=1)
        body = DEMO_LINK_ONLY.sub("", body)
        return body

    body = SCHEDULE_DEMO_A.sub(f"\n\n{banner}\n\n", body)
    body = DEMO_BLOCK.sub(f"\n\n{banner}\n\n", body, count=1)
    body = DEMO_LINK_ONLY.sub("", body)

    if "post-demo-banner" not in body and "Try SellerChamp" in body:
        body = re.sub(
            r"<h5>\s*Try SellerChamp[^<]*</h5>.*?(?=\n\n<|\n\n!\[|\n\n<h2)",
            f"\n\n{banner}\n\n",
            body,
            count=1,
            flags=re.I | re.S,
        )

    return body


def parse_post(text: str) -> tuple[str, str] | None:
    text = repair_front_matter_delimiter(text)
    m = FM_RE.match(text)
    if not m:
        return None
    return m.group(1), text[m.end() :]


def write_post(path: Path, fm: str, body: str) -> None:
    fm = fm.rstrip() + "\n"
    path.write_text(f"---\n{fm}---\n\n{body}", encoding="utf-8")


def process(path: Path, dry_run: bool, force_fm: bool = False) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    repaired = repair_front_matter_delimiter(text)
    parsed = parse_post(repaired)
    if not parsed:
        return False
    fm, body = parsed
    slug = slug_from_file(path, fm)

    new_body = separate_blocks(body)
    new_body = fix_image_sizes(new_body)
    new_body = insert_demo_banner(new_body, slug)

    fm_changed = repaired != text
    body_changed = new_body != body.strip() + ("\n" if body.endswith("\n") else "")

    if not fm_changed and not body_changed and not force_fm:
        return False
    if dry_run:
        print(f"would format {path.name}")
        return True

    write_post(path, fm, new_body)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=str, help="Single post filename under _posts/")
    parser.add_argument(
        "--repair-fm-only",
        action="store_true",
        help="Only fix glued reskin: true--- delimiters",
    )
    args = parser.parse_args()

    paths = [POSTS / args.file] if args.file else sorted(POSTS.glob("*.md"))

    if args.repair_fm_only:
        changed = 0
        for p in paths:
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            fixed = repair_front_matter_delimiter(text)
            if fixed == text:
                continue
            parsed = parse_post(fixed)
            if not parsed:
                continue
            if not args.dry_run:
                write_post(p, parsed[0], parsed[1])
            changed += 1
        print(f"Repaired front matter on {changed} / {len(paths)} posts")
        return 0

    changed = sum(1 for p in paths if p.exists() and process(p, args.dry_run))
    print(f"Formatted {changed} / {len(paths)} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())