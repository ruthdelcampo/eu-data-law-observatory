#!/usr/bin/env python3
"""
Split a large law markdown file into a directory of chapter-based files.

Usage: python3 scripts/split-law.py laws/eu-wide/gdpr.md
       python3 scripts/split-law.py --all          # split all laws over 100KB

Structure produced:
  laws/eu-wide/gdpr/
    _index.md       # Frontmatter, summary, key provisions, TOC
    recitals.md     # Preamble / "Whereas" section
    chapter-01.md   # Chapter I
    chapter-02.md   # Chapter II
    ...
    annexes.md      # All annexes combined

Small laws (under 100KB) are left as single files.
"""

import os
import re
import sys
import shutil
from pathlib import Path

SIZE_THRESHOLD = 100 * 1024  # 100KB
PROJECT_ROOT = Path(__file__).parent.parent


def parse_law_file(filepath):
    """Parse a law markdown file into frontmatter, sections, and full text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        return None
    frontmatter = fm_match.group(0)
    body = content[fm_match.end():]

    # Split body into pre-fulltext (summary, key provisions) and full text
    ft_match = re.search(r'^## Full Text\n', body, re.MULTILINE)
    if not ft_match:
        return None

    pre_fulltext = body[:ft_match.start()].strip()
    full_text = body[ft_match.end():].strip()

    return {
        'frontmatter': frontmatter,
        'pre_fulltext': pre_fulltext,
        'full_text': full_text,
    }


def split_into_parts(full_text):
    """Split the full text into recitals, chapters, and annexes."""
    lines = full_text.split('\n')
    parts = []
    current_part = {'type': 'preamble', 'title': 'Preamble', 'lines': []}

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect CHAPTER headings
        chapter_match = re.match(r'^CHAPTER\s+([IVXLCDM]+)', stripped)
        if chapter_match:
            # Save current part
            if current_part['lines'] or current_part['type'] == 'preamble':
                parts.append(current_part)

            # Look ahead for the chapter title (usually the next non-empty line)
            chapter_num = chapter_match.group(1)
            chapter_title = ''
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('CHAPTER'):
                    chapter_title = next_line
                    break

            current_part = {
                'type': 'chapter',
                'number': chapter_num,
                'title': chapter_title,
                'lines': [line],
            }
            continue

        # Detect TITLE headings (some laws use TITLE instead of CHAPTER)
        title_match = re.match(r'^TITLE\s+([IVXLCDM]+)', stripped)
        if title_match:
            if current_part['lines'] or current_part['type'] == 'preamble':
                parts.append(current_part)

            title_num = title_match.group(1)
            title_name = ''
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j].strip()
                if next_line and not re.match(r'^TITLE\s+', next_line):
                    title_name = next_line
                    break

            current_part = {
                'type': 'chapter',
                'number': title_num,
                'title': title_name,
                'lines': [line],
            }
            continue

        # Detect first ANNEX
        annex_match = re.match(r'^ANNEX\s+', stripped)
        if annex_match and current_part['type'] != 'annexes':
            if current_part['lines']:
                parts.append(current_part)
            current_part = {
                'type': 'annexes',
                'title': 'Annexes',
                'lines': [line],
            }
            continue

        current_part['lines'].append(line)

    # Don't forget the last part
    if current_part['lines']:
        parts.append(current_part)

    return parts


def roman_to_int(roman):
    """Convert roman numeral to integer for file naming."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev = 0
    for c in reversed(roman.upper()):
        val = values.get(c, 0)
        if val < prev:
            result -= val
        else:
            result += val
        prev = val
    return result


def write_split(filepath, parsed, parts):
    """Write the split parts to a directory."""
    law_dir = filepath.with_suffix('')  # Remove .md extension to get dir name
    law_dir.mkdir(parents=True, exist_ok=True)

    # Read abbreviation from frontmatter for the TOC
    abbr_match = re.search(r'^abbreviation:\s*(.+)$', parsed['frontmatter'], re.MULTILINE)
    abbreviation = abbr_match.group(1).strip() if abbr_match else 'Law'

    # Build TOC entries
    toc_lines = []
    files_written = []

    for part in parts:
        if part['type'] == 'preamble':
            filename = 'recitals.md'
            toc_lines.append(f'- [Recitals & Preamble](recitals.md)')
        elif part['type'] == 'chapter':
            num_int = roman_to_int(part['number'])
            filename = f'chapter-{num_int:02d}.md'
            title_display = f"Chapter {part['number']}"
            if part['title']:
                title_display += f" — {part['title']}"
            toc_lines.append(f'- [{title_display}]({filename})')
        elif part['type'] == 'annexes':
            filename = 'annexes.md'
            toc_lines.append(f'- [Annexes](annexes.md)')
        else:
            continue

        part_content = '\n'.join(part['lines']).strip()
        if part_content:
            out_path = law_dir / filename
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(part_content + '\n')
            files_written.append(filename)

    # Write _index.md
    toc_md = '\n'.join(toc_lines)
    index_content = f"""{parsed['frontmatter']}
{parsed['pre_fulltext']}

## Table of Contents

{toc_md}
"""
    with open(law_dir / '_index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    files_written.insert(0, '_index.md')

    return files_written


def process_file(filepath):
    """Process a single law file."""
    filepath = Path(filepath)
    size = filepath.stat().st_size

    if size < SIZE_THRESHOLD:
        print(f"  SKIP {filepath.name}: {size // 1024}KB (under threshold)")
        return False

    parsed = parse_law_file(filepath)
    if not parsed:
        print(f"  ERROR {filepath.name}: Could not parse")
        return False

    parts = split_into_parts(parsed['full_text'])
    chapters = [p for p in parts if p['type'] == 'chapter']
    annexes = [p for p in parts if p['type'] == 'annexes']

    if len(chapters) < 2:
        print(f"  SKIP {filepath.name}: Only {len(chapters)} chapters, not worth splitting")
        return False

    files = write_split(filepath, parsed, parts)

    # Remove the original single file
    filepath.unlink()

    print(f"  SPLIT {filepath.name}: {len(chapters)} chapters"
          f"{f' + annexes' if annexes else ''}"
          f" -> {len(files)} files in {filepath.stem}/")
    return True


def main():
    if '--all' in sys.argv:
        # Find all .md files in laws/ over the threshold
        laws_dir = PROJECT_ROOT / 'laws'
        targets = sorted(laws_dir.rglob('*.md'))
        targets = [t for t in targets if t.name != '.gitkeep' and t.name != '_index.md']
    else:
        if len(sys.argv) < 2:
            print("Usage: python3 scripts/split-law.py <file.md>")
            print("       python3 scripts/split-law.py --all")
            sys.exit(1)
        targets = [Path(sys.argv[1])]

    print(f"Processing {len(targets)} files...\n")

    split_count = 0
    for target in targets:
        if process_file(target):
            split_count += 1

    print(f"\nSplit {split_count} laws into chapter directories.")


if __name__ == '__main__':
    main()
