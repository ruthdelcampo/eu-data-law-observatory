#!/usr/bin/env python3
"""
Convert a raw EUR-Lex HTML file to clean markdown.

Usage: python3 scripts/convert-to-markdown.py raw/eu-wide/gdpr.html
Output: prints markdown to stdout (redirect to file)

This extracts the legal text from EUR-Lex HTML, stripping navigation,
scripts, styles, and layout tables, producing clean readable markdown.
"""

import sys
import re
from bs4 import BeautifulSoup, NavigableString
import html2text


def extract_legal_content(html_content):
    """Extract the main legal text from EUR-Lex HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove scripts, styles, nav elements
    for tag in soup.find_all(['script', 'style', 'nav', 'link', 'meta']):
        tag.decompose()

    # Remove the TOC sidebar
    toc = soup.find('div', id='TOC')
    if toc:
        toc.decompose()

    # Remove the OJ header table (date/language/journal info)
    for table in soup.find_all('table'):
        if table.find('p', class_='oj-hd-ti'):
            table.decompose()
            break

    # Convert EUR-Lex layout tables (used for recitals/numbered paragraphs)
    # into simple paragraph text. These tables have 2 columns: number + text.
    for table in soup.find_all('table'):
        cols = table.find_all('col')
        # Layout tables typically have 2 cols with 4% + 96% or similar
        if len(cols) == 2:
            rows = table.find_all('tr')
            replacement = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    num_text = cells[0].get_text(strip=True)
                    body_text = cells[1]
                    # Create a new paragraph with the number prefix
                    new_p = soup.new_tag('p')
                    new_p.string = ''
                    if num_text:
                        new_p.append(soup.new_string(num_text + ' '))
                    for child in list(body_text.children):
                        new_p.append(child.extract())
                    replacement.append(new_p)
            if replacement:
                for p in replacement:
                    table.insert_before(p)
                table.decompose()

    # The main content is in div#docHtml
    doc = soup.find('div', id='docHtml')
    if not doc:
        # Fallback: try the eli-container
        doc = soup.find('div', class_='eli-container')
    if not doc:
        # Last fallback: use body
        doc = soup.find('body')

    return doc


def convert_to_markdown(doc_element):
    """Convert the extracted HTML element to markdown."""
    h = html2text.HTML2Text()
    h.body_width = 0  # No wrapping
    h.unicode_snob = True
    h.protect_links = True
    h.wrap_links = False
    h.single_line_break = False
    h.skip_internal_links = True
    h.ignore_images = True
    h.ignore_emphasis = False

    raw_md = h.handle(str(doc_element))

    # Clean up common artifacts
    # Remove excessive blank lines (more than 2 consecutive)
    raw_md = re.sub(r'\n{4,}', '\n\n\n', raw_md)
    # Remove trailing whitespace on lines
    raw_md = re.sub(r'[ \t]+$', '', raw_md, flags=re.MULTILINE)
    # Clean up table remnants from layout tables
    raw_md = re.sub(r'\|[ \t]*\|', '', raw_md)
    # Remove empty table rows
    raw_md = re.sub(r'^\|[\s|]*\|$', '', raw_md, flags=re.MULTILINE)
    # Clean leftover pipe characters from layout tables
    raw_md = re.sub(r'^\s*\|\s*$', '', raw_md, flags=re.MULTILINE)
    # Remove horizontal rules that were table borders
    raw_md = re.sub(r'^-{4,}$', '---', raw_md, flags=re.MULTILINE)

    return raw_md.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/convert-to-markdown.py <html_file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    doc = extract_legal_content(html_content)
    if not doc:
        print(f"Error: Could not find legal content in {filepath}", file=sys.stderr)
        sys.exit(1)

    markdown = convert_to_markdown(doc)
    print(markdown)


if __name__ == '__main__':
    main()
