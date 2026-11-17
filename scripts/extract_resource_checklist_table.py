#!/usr/bin/env python3
"""Extract TablePress checklist HTML from saved WordPress page HTML."""

from __future__ import annotations

import argparse
import re
import sys
from html import unescape
from pathlib import Path

ROW_RE = re.compile(
    r"<tr[^>]*>\s*"
    r"(?:<td[^>]*colspan[^>]*><strong>(.*?)</strong></td>|"
    r"<td class=\"column-1\">(.*?)</td>\s*"
    r"<td class=\"column-2\">(.*?)</td>\s*"
    r"<td class=\"column-3\">.*?</td>)",
    re.S | re.I,
)


def clean(cell: str) -> str:
    cell = re.sub(r"<br\s*/?>", " ", cell, flags=re.I)
    cell = re.sub(r"<[^>]+>", "", cell)
    return unescape(re.sub(r"\s+", " ", cell)).strip()


def extract_table(html: str) -> str:
    m = re.search(r"<table[^>]*tablepress[^>]*>(.*?)</table>", html, re.S | re.I)
    if not m:
        return ""
    body = m.group(1)
    out: list[str] = ["<table class=\"resource-checklist\">", "<thead>", "<tr>", "<th scope=\"col\">Step</th>", "<th scope=\"col\">What to do</th>", "<th scope=\"col\" class=\"resource-checklist__done\">Done</th>", "</tr>", "</thead>", "<tbody>"]
    for row in ROW_RE.finditer(body):
        section, step, desc = row.group(1), row.group(2), row.group(3)
        if section:
            title = clean(section)
            out.append(f'<tr class="resource-checklist__section"><td colspan="3"><strong>{title}</strong></td></tr>')
        elif step and desc:
            out.append(
                '<tr>'
                f"<td>{clean(step)}</td>"
                f"<td>{clean(desc)}</td>"
                '<td><input type="checkbox" aria-label="Mark complete"></td>'
                "</tr>"
            )
    out.extend(["</tbody>", "</table>"])
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    args = parser.parse_args()
    html = args.html_file.read_text(encoding="utf-8", errors="replace")
    table = extract_table(html)
    if not table:
        print("No tablepress checklist found", file=sys.stderr)
        return 1
    sys.stdout.write(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())