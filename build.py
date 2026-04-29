#!/usr/bin/env python3
"""
build.py — regenerate index.html from the template and current descriptors.

Run this script after editing ontology_descriptors.json. It reads the JSON,
embeds the data into _template.html, and writes the result to index.html.

Usage:
    cd ontology-site/
    python3 build.py

No arguments. No dependencies beyond a standard Python 3 install.

If you also want to regenerate the PDF deck (after editing _gen_pdf.py),
run:
    python3 _gen_pdf.py
which produces /mnt/user-data/outputs/ontological-categories-v9.pdf — copy
that file back into this folder, replacing ontological-categories-v9.pdf.
"""

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()

DATA_FILE     = HERE / "ontology_descriptors.json"
TEMPLATE_FILE = HERE / "_template.html"
OUTPUT_FILE   = HERE / "index.html"

PLACEHOLDER = "/* INJECTED_JSON */ {}"


def main() -> int:
    # 1. Sanity-check that the inputs exist.
    for f in (DATA_FILE, TEMPLATE_FILE):
        if not f.exists():
            print(f"ERROR: missing required file: {f.name}", file=sys.stderr)
            return 1

    # 2. Load and parse the JSON. Catches malformed edits before we ship them.
    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {DATA_FILE.name} is not valid JSON:", file=sys.stderr)
        print(f"  line {e.lineno}, column {e.colno}: {e.msg}", file=sys.stderr)
        return 1

    if "ontologies" not in data:
        print(f"ERROR: {DATA_FILE.name} has no top-level 'ontologies' key.", file=sys.stderr)
        return 1

    n_onts = len(data["ontologies"])

    # 3. Embed only what the runtime needs (ontologies). Schema and meta stay
    #    in the JSON file for human reference; they aren't read by the page.
    embed = {"ontologies": data["ontologies"]}
    embedded_json = json.dumps(embed, ensure_ascii=False)

    # 4. Read the template and inject.
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"ERROR: {TEMPLATE_FILE.name} has no '{PLACEHOLDER}' placeholder.", file=sys.stderr)
        print("       The template appears to be corrupted.", file=sys.stderr)
        return 1

    output = template.replace(PLACEHOLDER, embedded_json)
    OUTPUT_FILE.write_text(output, encoding="utf-8")

    # 5. Friendly summary.
    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"OK  {OUTPUT_FILE.name} regenerated — {n_onts} ontologies, {size_kb:.1f} KB")
    print()
    print("   Open index.html in your browser to preview.")
    print("   Re-upload the whole folder to your host to update the live site.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
