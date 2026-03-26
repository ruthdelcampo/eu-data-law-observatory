# EU Data Law Observatory

An open observatory tracking the European Union's data legislation landscape — mapping fragmentation, overlaps, and conflicts across horizontal, sector-specific, and national data laws.

## Thesis

The EU has enacted a growing body of data-related legislation at multiple levels:

- **Horizontal laws** that apply broadly (GDPR, Data Act, AI Act, DSA, DMA...)
- **Sector-specific laws** targeting industries like finance (DORA, PSD2), health (EHDS), cybersecurity (NIS2, CRA), and more
- **National implementations** of EU directives, which vary across member states

These laws sometimes follow different principles, create overlapping obligations, and conflict with each other. The EU itself acknowledged this with the **Digital Omnibus** package (November 2025), a proposal to harmonize definitions and reduce contradictions across its own digital legislation.

This observatory aims to collect, archive, and eventually analyze this body of law to make the landscape navigable and the conflicts visible.

## What's in this repository

### Pipeline

Each law goes through a collection pipeline:

```
EUR-Lex (HTML) --> raw/ (archived original) --> laws/ (processed markdown with metadata)
```

1. **Fetch** the official text from EUR-Lex in HTML format
2. **Convert** to clean, readable markdown
3. **Enrich** with structured YAML frontmatter (metadata, dates, relationships)

### Directory structure

```
raw/                    Original HTML from EUR-Lex (archival)
  eu-wide/
  sector-specific/      Organized by sector (finance, health, telecom, etc.)
  national/

laws/                   Processed markdown versions (the main content)
  eu-wide/
  sector-specific/
  national/

scripts/                Utility scripts (fetching, conversion)
blog/                   Blog post drafts
registry.yaml           Master index of all tracked laws
```

### Law format

Each processed law includes YAML frontmatter with structured metadata:

```yaml
title: "General Data Protection Regulation"
abbreviation: GDPR
celex: "32016R0679"
type: regulation
scope: eu-wide
enacted: 2016-04-27
in_force: 2018-05-25
status: in-force
tags: [privacy, personal-data, data-protection]
```

Followed by a summary, key provisions, and the full converted text.

## Laws tracked

| Law | Type | Scope | In Force | Status |
|-----|------|-------|----------|--------|
| GDPR | Regulation | EU-wide | 2018 | In force |
| Data Act | Regulation | EU-wide | 2025 | In force |
| Data Governance Act | Regulation | EU-wide | 2023 | In force |
| AI Act | Regulation | EU-wide | 2024 (phased) | In force |
| Digital Services Act | Regulation | EU-wide | 2024 | In force |
| Digital Markets Act | Regulation | EU-wide | 2023 | In force |
| ePrivacy Directive | Directive | EU-wide | 2002 | In force |
| Free Flow of Non-Personal Data | Regulation | EU-wide | 2019 | In force |
| eIDAS 2 | Regulation | EU-wide | 2024 | In force |
| Interoperable Europe Act | Regulation | EU-wide | 2024 | In force |
| DORA | Regulation | Finance | 2025 | In force |
| PSD2 | Directive | Finance | 2018 | In force |
| EHDS | Regulation | Health | 2025 | In force |
| Clinical Trials Regulation | Regulation | Health | 2022 | In force |
| NIS2 | Directive | Cybersecurity | 2024 | In force |
| Cyber Resilience Act | Regulation | Cybersecurity | 2024 (phased) | In force |
| Open Data Directive | Directive | Public sector | 2021 | In force |
| Digital Omnibus | Regulation | EU-wide | -- | Proposed |

## Roadmap

- [x] **Phase 0**: Research the landscape and design the observatory
- [ ] **Phase 1**: Collect and archive laws (raw HTML + markdown conversion)
- [ ] **Phase 2**: Conflict and overlap analysis across laws
- [ ] **Phase 3**: Blog posts and public analysis
- [ ] **Phase 4**: Website / interactive explorer

## Tools

Fetch a law from EUR-Lex:

```bash
./scripts/fetch-law.sh <CELEX_NUMBER> <output_path>
# Example: ./scripts/fetch-law.sh 32016R0679 eu-wide/gdpr
```

## Data sources

All legal texts are sourced from [EUR-Lex](https://eur-lex.europa.eu/), the official database of EU law. EUR-Lex content is available for reuse under the [Commission Decision 2011/833/EU](https://eur-lex.europa.eu/eli/dec/2011/833/oj).

## License

This project is licensed under [CC BY 4.0](LICENSE). Legal texts themselves are official documents of the European Union and are not subject to copyright.

## Contributing

Contributions are welcome. If you'd like to help:

1. Check `registry.yaml` for laws with `observatory_status: pending`
2. Follow the pipeline: fetch raw HTML, convert to markdown, add frontmatter
3. Submit a pull request

See `CLAUDE.md` for detailed conventions and formatting standards.
