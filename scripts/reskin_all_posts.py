#!/usr/bin/env python3
"""Reskin migrated blog posts: strip Elementor/WP cruft and emit clean markdown/HTML."""

from __future__ import annotations

import argparse
import html as html_lib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def parse_front_matter(text: str) -> tuple[str, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end() :]


def youtube_ids_from_elementor(html: str) -> list[str]:
    ids = []
    for m in re.finditer(
        r'youtube_url\\":\\"https:\\/\\/www\.youtube\.com\\/watch\?v=([A-Za-z0-9_-]+)',
        html,
    ):
        ids.append(m.group(1))
    return list(dict.fromkeys(ids))


def normalize_links(html: str) -> str:
    html = html.replace("&#038;", "&amp;").replace("&amp;", "&")
    html = html_lib.unescape(html)

    def repl_site(m: re.Match) -> str:
        path = m.group(1)
        if path.startswith("/wp-content/"):
            return m.group(0)
        return path

    html = re.sub(
        r"https?://(?:www\.)?sellerchamp\.com(/[^\"'\s>]+)",
        repl_site,
        html,
        flags=re.I,
    )
    # Relative wp-content paths after bad imports
    html = re.sub(
        r'(src|href)="(/wp-content/[^"]+)"',
        r'\1="https://sellerchamp.com\2"',
        html,
    )
    html = re.sub(
        r"!\[\]\((/wp-content/[^)]+)\)",
        r"![](https://sellerchamp.com\1)",
        html,
    )
    html = re.sub(r'href="(/blog/[^"/]+)"', lambda m: f'href="{m.group(1)}/"', html)
    return html


def elementor_button_to_markdown(html: str) -> str:
    def repl(m: re.Match) -> str:
        href = m.group(1)
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if not label:
            label = "Book a demo"
        return f'\n\n[**{label}**]({href})\n\n'

    pattern = re.compile(
        r'<div class="elementor-button-wrapper">\s*'
        r'<a class="elementor-button[^"]*" href="([^"]+)"[^>]*>.*?'
        r'<span class="elementor-button-text">(.*?)</span>.*?</a>\s*</div>',
        re.S | re.I,
    )
    return pattern.sub(repl, html)


def img_to_markdown(html: str) -> str:
    def repl(m: re.Match) -> str:
        src = m.group(1)
        alt = (m.group(2) or "").strip()
        alt = re.sub(r"\s+", " ", alt)
        return f"\n\n![{alt}]({src})\n\n"

    pattern = re.compile(
        r"<p>\s*<img[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*(?:\balt=[\"']([^\"']*)[\"'])?[^>]*/?\s*>\s*</p>",
        re.I | re.S,
    )
    html = pattern.sub(repl, html)
    pattern2 = re.compile(
        r"<img[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*(?:\balt=[\"']([^\"']*)[\"'])?[^>]*/?>",
        re.I,
    )

    def repl2(m: re.Match) -> str:
        src = m.group(1)
        alt = (m.group(2) or "").strip()
        return f"\n\n![{alt}]({src})\n\n"

    return pattern2.sub(repl2, html)


def strip_wrapper_tags(html: str) -> str:
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    # Drop fusion / elementor chrome
    for _ in range(8):
        before = html
        html = re.sub(r"<div[^>]*>", "", html, flags=re.I)
        html = re.sub(r"</div>", "", html, flags=re.I)
        if html == before:
            break
    html = re.sub(r"<span[^>]*>", "", html, flags=re.I)
    html = re.sub(r"</span>", "", html, flags=re.I)
    html = re.sub(r"<li[^>]*>", "<li>", html, flags=re.I)
    html = re.sub(
        r"<(h[1-6])[^>]*>",
        lambda m: f"<{m.group(1)}>",
        html,
        flags=re.I,
    )
    html = re.sub(r"<p[^>]*>", "<p>", html, flags=re.I)
    return html


def strip_imported_footer(html: str) -> str:
    """Drop Elementor author box, testimonials, and TOC widgets from migrated WP footers."""
    markers = [
        r'<a class="elementor-author-box',
        r'<cite class="elementor-testimonial',
        r'<i class="elementor-toc__spinner',
        r"\nAzmi\s*\n",
    ]
    for pat in markers:
        m = re.search(pat, html, re.I)
        if m:
            html = html[: m.start()].rstrip()
            break
    html = re.sub(r"<meta\s+content=[^>]+>\s*", "", html, flags=re.I)
    html = re.sub(
        r"<i[^>]*class=\"[^\"]*eicon-(?:star|loading)[^\"]*\"[^>]*>\s*</i>\s*",
        "",
        html,
        flags=re.I,
    )
    return html


def tighten_copy(html: str) -> str:
    if html.lstrip().startswith(("![", "#")) and "<h2" not in html.lower():
        return html.strip() + ("\n" if not html.endswith("\n") else "")

    html = re.sub(r"<p>\s*<p>", "<p>", html, flags=re.I)
    html = re.sub(r"</p>\s*</p>", "</p>", html, flags=re.I)
    html = re.sub(r"([^\s>])<b>", r"\1 <b>", html)
    html = re.sub(r"</b>([^\s<.,;:!?])", r"</b> \1", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r">\s*<", ">\n\n<", html)
    html = re.sub(
        r"<b>You Might Also Like:\s*</b>",
        "<p><strong>You might also like:</strong>",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<b>Read [Mm]ore:\s*</b>",
        "<p><strong>Read more:</strong>",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<b>Check Out:\s*</b>",
        "<p><strong>Check out:</strong>",
        html,
        flags=re.I,
    )
    html = re.sub(r"</p>\s*<p>", "</p>\n\n<p>", html)
    html = re.sub(r"</h([2-4])>\s*<h", r"</h\1>\n\n<h", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip() + "\n"


def videos_block(ids: list[str]) -> str:
    if not ids:
        return ""
    rows = ['<div class="post-embed-row">']
    for vid in ids:
        rows.append('<div class="post-embed">')
        rows.append(
            f'<iframe src="https://www.youtube.com/embed/{vid}" '
            f'title="SellerChamp video" loading="lazy" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
            'gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
        )
        rows.append("</div>")
    rows.append("</div>\n")
    return "\n".join(rows)


def reskin_body(body: str) -> tuple[str, bool]:
    if not body.strip():
        return body, False
    if "elementor" not in body.lower() and "fusion-" not in body.lower():
        if 'class="elementor-widget-container"' in body:
            body = strip_wrapper_tags(body)
            return tighten_copy(body), True
        return body, False

    yt = youtube_ids_from_elementor(body)
    body = normalize_links(body)
    body = elementor_button_to_markdown(body)
    body = strip_wrapper_tags(body)
    body = img_to_markdown(body)
    body = tighten_copy(body)
    body = strip_imported_footer(body)
    if yt:
        body = body.rstrip() + "\n\n" + videos_block(yt)
    return body, True


def touch_front_matter(fm: str) -> str:
    fm = fm.strip() + "\n"
    if re.search(r"^reskin:\s*", fm, re.M):
        fm = re.sub(r"^reskin:\s*.*$", "reskin: true", fm, flags=re.M)
    else:
        fm = fm.rstrip() + "\nreskin: true\n"
    return fm


def process_file(path: Path, force: bool) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_front_matter(text)
    if not fm:
        return "skip_no_frontmatter"
    manual = bool(re.search(r"^reskin:\s*manual\s*$", fm, re.M))
    if manual:
        return "skip_manual"

    already = bool(re.search(r"^reskin:\s*true\s*$", fm, re.M))
    if already and not force:
        return "skip_already_reskinned"

    prior = body
    if already and not re.search(r"elementor|fusion-", prior, re.I):
        if prior.lstrip().startswith(("![", "#", "**")):
            return "skip_clean_body"

    new_body, changed = reskin_body(body)
    if not changed and already:
        new_body = strip_imported_footer(tighten_copy(normalize_links(prior)))

    if not changed and not already and not force:
        return "skip_no_elementor"

    fm = touch_front_matter(fm)
    path.write_text(f"---\n{fm}\n---\n\n{new_body.lstrip()}\n", encoding="utf-8")
    return "reskinned"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-run even if reskin: true")
    parser.add_argument("--limit", type=int, default=0, help="Max files (0 = all)")
    args = parser.parse_args()

    counts: dict[str, int] = {}
    files = sorted(POSTS.glob("*.md"))
    if args.limit:
        files = files[: args.limit]

    for path in files:
        status = process_file(path, args.force)
        counts[status] = counts.get(status, 0) + 1

    print("Reskin complete:")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())