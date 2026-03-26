# CLAUDE.md — EU Data Law Observatory

## Project overview

This repository is an observatory for EU data legislation. We collect official legal texts from EUR-Lex, archive the raw HTML, and convert them into structured markdown for analysis with AI tools.

**Thesis**: EU data laws exist at multiple levels (horizontal, sector-specific, national) and sometimes conflict or follow different principles. This observatory makes that landscape navigable.

## Repository structure

```
raw/                    Original HTML from EUR-Lex (never modify these after fetching)
  eu-wide/              Horizontal regulations (GDPR, Data Act, AI Act, etc.)
  sector-specific/      By sector: finance/, health/, telecom/, cybersecurity/, energy/, public/
  national/             Member-state implementations (future)

laws/                   Processed markdown (the main working content)
  eu-wide/
  sector-specific/      Same sector subdirectories as raw/
  national/

scripts/                Utility scripts
blog/                   Blog post drafts
registry.yaml           Master index of all tracked laws
```

## Naming conventions

- **Files**: kebab-case, descriptive short name: `gdpr.md`, `data-act.md`, `nis2.md`
- **Directories**: lowercase, kebab-case for sectors: `sector-specific/finance/`
- **Raw files**: Same name as the law markdown but with `.html` extension: `raw/eu-wide/gdpr.html`

## How to add a new law

### Step 1: Register it

Add an entry to `registry.yaml` with all known metadata. Required fields:
- `abbreviation`, `title`, `celex`, `type`, `scope`, `sector`
- `enacted`, `in_force`, `eurlex_url`, `status`
- Set `observatory_status: pending`

### Step 2: Fetch the raw HTML

```bash
./scripts/fetch-law.sh <CELEX_NUMBER> <path>
# Example: ./scripts/fetch-law.sh 32016R0679 eu-wide/gdpr
```

This downloads from EUR-Lex and saves to `raw/<path>.html`. Update `observatory_status` to `collected` in the registry.

### Step 3: Convert to markdown

Create `laws/<path>.md` with:

1. **YAML frontmatter** (see schema below)
2. **Summary section** — plain-language explanation of what the law does, who it affects, key provisions (AI-assisted)
3. **Key Provisions section** — the most important articles extracted and explained
4. **Full Text section** — the complete legal text converted from HTML to markdown

Update `observatory_status` to `processed` in the registry.

## Frontmatter schema

```yaml
---
title: "Full Official Name"
abbreviation: SHORT_NAME
celex: "3YYYYRNNNN"              # CELEX number from EUR-Lex
type: regulation                  # regulation | directive | decision
scope: eu-wide                    # eu-wide | sector-specific | national
sector: null                      # finance | health | telecom | cybersecurity | energy | public | null
enacted: YYYY-MM-DD
in_force: YYYY-MM-DD
eurlex_url: "https://eur-lex.europa.eu/eli/..."
status: in-force                  # in-force | proposed | repealed | amended
related_laws: []                  # List of abbreviations of related laws
tags: []                          # Descriptive tags
last_updated: YYYY-MM-DD         # When this markdown was last updated
---
```

## Markdown formatting for legal text

When converting legal text to markdown:

- **Recitals**: Use blockquotes with numbering: `> (1) Whereas...`
- **Articles**: Use `### Article 1 — Title` (H3 with em dash)
- **Paragraphs**: Numbered lists within articles: `1. The controller shall...`
- **Points/subpoints**: Use lettered lists: `(a) the identity...`
- **Chapters/Titles**: Use H2: `## Chapter I — General Provisions`
- **Sections**: Use H3 if within a chapter, otherwise H2
- **Annexes**: Use H2: `## Annex I — ...`
- **Cross-references**: Keep the original reference text (e.g., "referred to in Article 6(1)")
- **Footnotes**: Convert to markdown footnotes `[^1]`
- Preserve all original numbering and structure exactly as in the official text

## EUR-Lex reference

- **CELEX number format**: `{Sector}{Year}{Type}{Number}`
  - Sector 3 = secondary legislation
  - Type: R = Regulation, L = Directive, D = Decision
  - Example: `32016R0679` = 2016 Regulation 679 (GDPR)

- **URL patterns**:
  - HTML: `https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}`
  - PDF: `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:{celex}`
  - ELI: `https://eur-lex.europa.eu/eli/reg/{year}/{number}/oj`

- **API access**: SPARQL endpoint at `https://publications.europa.eu/webapi/rdf/sparql`

## Common workflows

### Fetch and process a law
```
1. Add to registry.yaml
2. ./scripts/fetch-law.sh CELEX path
3. Convert HTML to markdown with frontmatter
4. Update registry observatory_status
```

### Update an existing law
If a law has been amended or a consolidated version is available:
1. Re-fetch the raw HTML (the old version is in git history)
2. Update the markdown
3. Update `last_updated` in frontmatter

### Write a blog post
Blog posts go in `blog/` as markdown files. Name format: `YYYY-MM-DD-slug.md`.
Focus on analysis, comparisons, and the conflicts/overlaps between laws.

## Important notes

- **Never modify files in `raw/`** after initial fetch — they are the archival originals
- **English versions only** for now (all post-1973 EU laws are available in English)
- **Legal texts are not copyrighted** — they are official documents of the EU
- **Always verify CELEX numbers** against EUR-Lex before fetching
- When in doubt about a law's metadata, check EUR-Lex directly
