#!/usr/bin/env python3
"""
Batch convert all collected raw HTML files to markdown with frontmatter.

Reads registry.yaml, finds all 'collected' laws, converts their HTML to
markdown, prepends YAML frontmatter, and writes to laws/ directory.

Usage: python3 scripts/batch-convert.py
"""

import os
import sys
import re
import yaml
from pathlib import Path

# Add scripts dir to path so we can import the converter
sys.path.insert(0, os.path.dirname(__file__))
from importlib.machinery import SourceFileLoader
converter = SourceFileLoader("converter", os.path.join(os.path.dirname(__file__), "convert-to-markdown.py")).load_module()

PROJECT_ROOT = Path(__file__).parent.parent

# Map from registry entries to file paths
FILE_MAP = {
    "GDPR": ("eu-wide", "gdpr"),
    "Data Act": ("eu-wide", "data-act"),
    "DGA": ("eu-wide", "dga"),
    "AI Act": ("eu-wide", "ai-act"),
    "DSA": ("eu-wide", "dsa"),
    "DMA": ("eu-wide", "dma"),
    "ePrivacy Directive": ("eu-wide", "eprivacy-directive"),
    "FFD Regulation": ("eu-wide", "ffd-regulation"),
    "eIDAS 2": ("eu-wide", "eidas2"),
    "Interoperable Europe Act": ("eu-wide", "interoperable-europe-act"),
    "DORA": ("sector-specific/finance", "dora"),
    "PSD2": ("sector-specific/finance", "psd2"),
    "EHDS": ("sector-specific/health", "ehds"),
    "CTR": ("sector-specific/health", "ctr"),
    "NIS2": ("sector-specific/cybersecurity", "nis2"),
    "CRA": ("sector-specific/cybersecurity", "cra"),
    "Open Data Directive": ("sector-specific/public", "open-data-directive"),
}


def build_frontmatter(law):
    """Build YAML frontmatter string from registry entry."""
    fields = {
        "title": law["title"],
        "abbreviation": law["abbreviation"],
        "celex": law.get("celex"),
        "type": law.get("type"),
        "scope": law.get("scope"),
        "sector": law.get("sector"),
        "enacted": str(law.get("enacted")) if law.get("enacted") else None,
        "in_force": str(law.get("in_force")) if law.get("in_force") else None,
        "eurlex_url": law.get("eurlex_url"),
        "status": law.get("status"),
        "related_laws": [],
        "tags": [],
        "last_updated": "2026-03-26",
    }

    lines = ["---"]
    for key, val in fields.items():
        if val is None:
            lines.append(f"{key}: null")
        elif isinstance(val, list):
            lines.append(f"{key}: {val}")
        elif isinstance(val, str) and any(c in val for c in ':#{}[],"\''):
            lines.append(f'{key}: "{val}"')
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def process_law(law, dry_run=False):
    """Process a single law: convert HTML to markdown with frontmatter."""
    abbr = law["abbreviation"]
    if abbr not in FILE_MAP:
        print(f"  SKIP: No file mapping for {abbr}")
        return False

    dir_path, filename = FILE_MAP[abbr]
    raw_path = PROJECT_ROOT / "raw" / dir_path / f"{filename}.html"
    out_path = PROJECT_ROOT / "laws" / dir_path / f"{filename}.md"

    if not raw_path.exists():
        print(f"  SKIP: Raw file not found: {raw_path}")
        return False

    if dry_run:
        print(f"  Would convert: {raw_path} -> {out_path}")
        return True

    print(f"  Converting: {abbr}...", end=" ", flush=True)

    # Read and convert HTML
    with open(raw_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    doc = converter.extract_legal_content(html_content)
    if not doc:
        print("FAILED (no content found)")
        return False

    markdown = converter.convert_to_markdown(doc)

    # Build frontmatter
    frontmatter = build_frontmatter(law)

    # Combine
    full_content = f"{frontmatter}\n\n## Summary\n\n<!-- TODO: AI-generated summary -->\n\n## Key Provisions\n\n<!-- TODO: Extract key articles -->\n\n## Full Text\n\n{markdown}\n"

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    size_kb = len(full_content) / 1024
    print(f"OK ({size_kb:.0f} KB)")
    return True


def main():
    dry_run = "--dry-run" in sys.argv

    # Load registry
    registry_path = PROJECT_ROOT / "registry.yaml"
    with open(registry_path, "r") as f:
        registry = yaml.safe_load(f)

    laws = registry.get("laws", [])
    collected = [l for l in laws if l.get("observatory_status") == "collected"]

    print(f"Found {len(collected)} collected laws to convert.\n")

    success = 0
    for law in collected:
        if process_law(law, dry_run=dry_run):
            success += 1

    print(f"\nConverted {success}/{len(collected)} laws.")

    if not dry_run and success > 0:
        # Update registry status
        for law in laws:
            abbr = law["abbreviation"]
            if abbr in FILE_MAP and law.get("observatory_status") == "collected":
                law["observatory_status"] = "processed"

        with open(registry_path, "w") as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print("Updated registry.yaml (status -> processed)")


if __name__ == "__main__":
    main()
