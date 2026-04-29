#!/usr/bin/env python3
"""
split_pdf.py — split the full deck into one PDF per ontology.

Reads ontological-categories-v9.pdf, splits each page into a separate file
named diagram-<key>.pdf inside the diagrams/ subfolder. The chooser links
to these files so visitors land directly on the right diagram, regardless
of browser or PDF viewer.

Page-to-key mapping is read from ontology_descriptors.json (the 'page' field
of each ontology entry, 1-indexed).

Usage:
    cd ontology-site/
    python3 split_pdf.py

Requires pypdf (install with: pip install pypdf --break-system-packages, or
pip install pypdf in a venv).

Run this script after replacing the source PDF (e.g. after editing the deck
with _gen_pdf.py and copying the new PDF in). It overwrites the diagrams/
folder.
"""

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()

SRC_PDF   = HERE / "ontological-categories-v9.pdf"
DATA_FILE = HERE / "ontology_descriptors.json"
OUT_DIR   = HERE / "diagrams"


def main() -> int:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("ERROR: pypdf is not installed.", file=sys.stderr)
        print("       Install with: pip install pypdf", file=sys.stderr)
        return 1

    if not SRC_PDF.exists():
        print(f"ERROR: source PDF not found: {SRC_PDF.name}", file=sys.stderr)
        return 1
    if not DATA_FILE.exists():
        print(f"ERROR: descriptor file not found: {DATA_FILE.name}", file=sys.stderr)
        return 1

    with DATA_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    OUT_DIR.mkdir(exist_ok=True)

    reader = PdfReader(str(SRC_PDF))
    n_src = len(reader.pages)

    n_written = 0
    for key, o in data["ontologies"].items():
        page_idx = o["page"] - 1
        if not (0 <= page_idx < n_src):
            print(f"WARN: '{key}' has page={o['page']} but PDF only has {n_src} pages — skipping", file=sys.stderr)
            continue
        writer = PdfWriter()
        writer.add_page(reader.pages[page_idx])
        out_path = OUT_DIR / f"diagram-{key}.pdf"
        with out_path.open("wb") as f:
            writer.write(f)
        n_written += 1

    print(f"OK  {n_written} diagrams written to {OUT_DIR.name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
