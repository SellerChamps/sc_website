#!/usr/bin/env python3
"""Fail CI if em dash (—) or en dash (–) appears in user-facing paths.

Scans pages/, landing/, _includes/ (except vendor), index.html, and string
values in _data/integrations.yml. Catches Unicode dashes and HTML entities
(&mdash;, &ndash;, &#8212;, &#8211;). Exempt: this script, no-em-dash.mdc comment examples.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EM = "\u2014"
EN = "\u2013"
DASH_ENTITY_RE = re.compile(
    r"(?:&mdash;|&ndash;|&#8212;|&#8211;|&#x2014;|&#x2013;)",
    re.IGNORECASE,
)
GLOBS = [
    "pages/**/*.html",
    "landing/**/*.html",
    "_includes/**/*.html",
    "index.html",
    "_data/integrations.yml",
]
SKIP = {"node_modules", "_site", ".cursor/skills"}


def line_has_dash(line: str) -> bool:
    return EM in line or EN in line or DASH_ENTITY_RE.search(line) is not None


def scan_file(path: Path) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line_has_dash(line):
            hits.append((i, line.strip()[:120]))
    return hits


def main() -> int:
    bad: list[tuple[Path, int, str]] = []
    for pattern in GLOBS:
        for path in ROOT.glob(pattern):
            if any(part in SKIP for part in path.parts):
                continue
            for line_no, snippet in scan_file(path):
                bad.append((path.relative_to(ROOT), line_no, snippet))
    if not bad:
        print("No em/en dashes (Unicode or HTML entities) in scanned user-facing paths.")
        return 0
    print(f"Found {len(bad)} line(s) with em or en dash:")
    for path, line_no, snippet in bad[:40]:
        print(f"  {path}:{line_no}: {snippet}")
    if len(bad) > 40:
        print(f"  ... +{len(bad) - 40} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())