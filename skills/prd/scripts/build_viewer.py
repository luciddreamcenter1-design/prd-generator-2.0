#!/usr/bin/env python3
"""Embed a PRD Markdown file into the interactive tracker HTML.

Usage: build_viewer.py PRD.md [PRD.html]
"""
import html
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "prd-viewer.html"


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__.strip())
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) == 3 else src.with_suffix(".html")

    md = src.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", md, re.M)
    title = title_match.group(1).strip() if title_match else src.stem
    # A literal "</script" would end the embedding <script> tag early.
    embedded = re.sub(r"</(script)", r"<\\/\1", md, flags=re.I)

    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("{{PRD_TITLE}}", html.escape(title)).replace("{{PRD_MARKDOWN}}", embedded)
    out.write_text(page, encoding="utf-8")
    tasks = len(re.findall(r"^\s*(?:[-*+]|\d+\.)\s+\[[ xX]\]", md, re.M))
    print(f"Wrote {out} ({tasks} checkboxes)")


if __name__ == "__main__":
    main()
