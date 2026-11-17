#!/usr/bin/env python3
"""Import TablePress tables from saved WP HTML into _includes/checklists/."""

from __future__ import annotations

import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_includes" / "checklists"


def clean_table(html: str) -> str:
    m = re.search(r"<table[^>]*tablepress[^>]*>.*?</table>", html, re.S | re.I)
    if not m:
        return ""
    table = m.group(0)
    table = re.sub(r"\s+id=\"[^\"]+\"", "", table)
    table = re.sub(r"\s+onchange=\"[^\"]+\"", "", table)
    table = re.sub(r"\s+id=\"frontend-checklist[^\"]*\"", "", table)
    table = re.sub(
        r"class=\"tablepress[^\"]*\"",
        'class="resource-checklist"',
        table,
        count=1,
    )
    table = re.sub(r"<p><label><input([^>]*)></label></p>", r"<input\1>", table, flags=re.I)
    table = re.sub(r"type=\"checkbox\"", 'type="checkbox" aria-label="Mark complete"', table)
    table = re.sub(r"<br\s*/?>", "<br>", table, flags=re.I)
    return unescape(table)


def main() -> None:
    mapping = {
        "amazon-fba-checklist.html": Path("/tmp/amazon-fba-checklist.html"),
        "ebay-description-table.html": Path("/tmp/ebay-description.html"),
        "ecommerce-seo-checklist-table.html": Path("/tmp/ecommerce-seo-checklist.html"),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in mapping.items():
        if not src.exists():
            print(f"skip missing {src}")
            continue
        html = src.read_text(encoding="utf-8", errors="replace")
        table = clean_table(html)
        if not table:
            print(f"no table in {name}")
            continue
        (OUT / name).write_text(table + "\n", encoding="utf-8")
        print(f"wrote {name} ({len(table)} bytes)")


if __name__ == "__main__":
    main()