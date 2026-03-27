---
layout: default
title: "Legislation as Code: What Software Architecture Can Teach EU Data Law"
date: 2026-03-26
author: Ruth del Campo
---

# Legislation as Code: What Software Architecture Can Teach EU Data Law

*By Ruth del Campo — March 26, 2026*

## The compliance nightmare no one designed

A fintech company operating in the EU that uses AI for fraud detection must today comply with the GDPR, the Data Act, the AI Act, DORA, and NIS2 — simultaneously. The same data breach triggers three separate notifications to three different regulators, each with different materiality thresholds. The same user requesting their data may be entitled to batch export under GDPR Article 20, real-time API access under DMA Article 6(9), and a healthcare-specific interoperable format under EHDS Article 5 — for the same underlying personal data.

This is not a hypothetical. This is the reality of EU data regulation in 2026.

The EU has produced, in under a decade, an extraordinary body of data legislation: GDPR, the Data Act, the Data Governance Act, the AI Act, the Digital Services Act, the Digital Markets Act, DORA, NIS2, the EHDS, and more. Each law was drafted with genuine intent. Each addresses a real problem. But together, they form a system that no one designed as a system.

Software engineers have a name for this: **spaghetti code**.

## The parallel with software

In software, when multiple modules are developed independently, each solving its own problem without a shared architecture, the result is technical debt — overlapping logic, conflicting interfaces, and a codebase where changing one thing breaks three others.

EU data law has the same symptoms:

**Duplicated logic.** Data portability is defined in GDPR Article 20, expanded in Data Act Article 4, made real-time in DMA Article 6(9), and given sector-specific form in EHDS Article 5. Four implementations of the same concept, each with different scope, format requirements, and triggers.

**Conflicting interfaces.** EHDS Article 8 allows Member States to restrict health data portability when disclosure could endanger a health professional's vital interests. GDPR Article 20 contains no such restriction. Same data, same patient, contradictory outcomes depending on which law you invoke.

**Implicit dependencies.** Every major post-GDPR data law includes a "without prejudice to GDPR" clause. The Data Act says it in Article 1(5). The AI Act in Article 2(7). The DGA in Article 1(3). NIS2 in Article 2(12). This is the legislative equivalent of `import gdpr` — an implicit dependency that pushes conflict resolution onto the implementer (i.e., the company trying to comply).

**Inconsistent definitions.** The Data Act introduces "data holder." The AI Act introduces "deployer." GDPR uses "controller" and "processor." A single company may be all four simultaneously, subject to different obligations under each label for the same data processing activity.

## What software architecture teaches us

Software faced the same problems decades ago — and developed patterns to solve them. What if we applied those patterns to legislation?

### 1. The Base Class: a Data Law Foundation Regulation

In object-oriented programming, a **base class** defines shared behavior that all subclasses inherit. You don't redefine `toString()` in every class — you define it once and override only when needed.

EU data law needs a **Data Law Foundation Regulation** — a single horizontal instrument that defines, once and authoritatively:

- **Common definitions**: what "personal data," "data holder," "controller," "processor," "data subject," and "user" mean across all laws
- **Default portability**: a single portability standard (format, timing, API requirements) that sector laws can extend but not contradict
- **Default incident reporting**: one notification framework with a single entry point, fanning out to sector regulators
- **Default consent architecture**: a unified consent model that sector laws can add requirements to, but not fragment

Sector-specific laws (DORA, NIS2, EHDS) would then **extend** this base — adding sector-specific obligations without redefining the fundamentals. The AI Act and Data Act would be **mixins** — cross-cutting concerns that layer on top of the base without duplicating it.

```
DataLawFoundation (base class)
├── defines: PersonalData, Controller, Processor, DataHolder, User
├── defines: default_portability(format=JSON, timing=30_days)
├── defines: default_incident_report(to=SingleEntryPoint, within=72h)
├── defines: default_consent(granular=true, renewable=annual)
│
├── DORA extends DataLawFoundation
│   └── overrides: incident_report(to=FinancialRegulator, adds=ICT_classification)
│
├── NIS2 extends DataLawFoundation
│   └── overrides: incident_report(to=CSIRT, adds=critical_infrastructure_threshold)
│
├── EHDS extends DataLawFoundation
│   └── overrides: portability(format=HL7_FHIR, adds=clinical_restriction)
│   └── extends: consent(adds=secondary_use_research)
│
├── AIAct implements CrossCuttingConcern
│   └── adds: risk_classification, transparency_obligation, DPIA_requirement
│
├── DataAct implements CrossCuttingConcern
│   └── extends: portability(adds=non_personal_data, adds=real_time_access)
```

Today, the "without prejudice to GDPR" clause in every law is an informal, fragile version of this pattern. It pushes the resolution logic to the implementer. A proper base class would resolve conflicts at the source.

### 2. Interfaces, not implementations: regulatory APIs

In software, an **interface** defines *what* a module must do, not *how* it does it. This is the principle of separation of concerns.

Current EU law often prescribes implementation. GDPR Article 33 says breach notification must happen within 72 hours. DORA Article 19 says "without undue delay." NIS2 Article 23 says "without undue delay" but with different materiality thresholds. Three different implementations of the same intent: "tell the regulator quickly when something goes wrong."

A better approach: define a **Regulatory Reporting Interface**.

```
interface IncidentReport {
    classify(incident) → severity_level
    notify(authority, incident, severity_level) → within(timeframe)
    document(incident, response_actions) → audit_trail
}
```

Each sector law implements this interface according to its context. DORA adds financial materiality thresholds. NIS2 adds critical infrastructure criteria. But the *shape* of compliance is uniform. A company knows it must implement `IncidentReport` — the method signatures are the same, even if the internal logic differs.

This is not merely an analogy. Estonia's X-Road, the country's digital backbone, already works this way — government services expose standardized APIs, and new regulations plug into existing infrastructure rather than requiring parallel systems.

### 3. Composition over inheritance: modular compliance

The "Gang of Four" design pattern principle — **favor composition over inheritance** — suggests that complex behavior should be built by combining small, focused components rather than deep inheritance hierarchies.

Applied to legislation: instead of a company needing to read and reconcile 9 separate regulations, compliance obligations should be **composable modules**.

```
ComplianceProfile = compose(
    base = DataLawFoundation,
    sector = [DORA, NIS2],
    cross_cutting = [AIAct],
    entity_type = FinancialInstitution,
    data_types = [PersonalData, FinancialData, BiometricData],
    activities = [Profiling, AutomatedDecisionMaking, CrossBorderTransfer]
)

# Output: a single, resolved set of obligations
# - No contradictions
# - No duplicate reporting
# - Clear priority rules
```

This is what a **compliance compiler** would do. Given a company's profile — its sector, activities, data types, and entity roles — it produces a resolved, non-contradictory set of obligations. Conflicts are resolved at compile time by the legislature, not at runtime by the company.

### 4. Version control: laws as living documents

Software uses **version control** — every change is tracked, diffable, and reversible. When a function's behavior changes, its dependents can see exactly what changed and adapt.

EU law amendments are published as new Official Journal entries that textually modify existing articles. A company reading the GDPR today sees the original 2016 text; to understand the current state, they must cross-reference all subsequent amendments manually.

Legislation should adopt **semantic versioning**:
- **GDPR v2.1.0**: Major version = fundamental restructuring. Minor version = new articles or obligations added. Patch = clarifications or technical corrections.
- Each version comes with a **changelog** — not just the amended text, but a plain-language summary of what changed and why.
- Consolidated texts are the default, not a separate EUR-Lex product.

This already exists in some form — EUR-Lex provides consolidated texts. But the authoring process itself should be version-controlled, and amendment impact should be machine-readable.

### 5. Type safety: machine-readable obligations

In typed programming languages, the compiler catches errors before runtime. You cannot pass a string where an integer is expected.

Legislation today is written in natural language — maximally flexible, maximally ambiguous. "Without undue delay" means different things to different regulators. "Structured, commonly used, machine-readable format" is undefined.

**Machine-readable legislation** would make obligations precise:

```yaml
obligation:
  name: breach_notification
  trigger:
    event: personal_data_breach
    severity: high  # defined in Annex I
  action:
    notify:
      recipient: competent_dpa
      timeframe: 72_hours
      format: ENISA_standard_v2
    document:
      retention: 5_years
      access: auditor, dpa
  exceptions:
    - condition: breach_unlikely_to_result_in_risk
      action: document_only
```

This is not science fiction. The OECD has been exploring "Rules as Code" since 2020. New Zealand has piloted machine-consumable legislation. France's DILA (Direction de l'information legale et administrative) publishes legal texts in structured XML. The technology exists; the political will is the bottleneck.

## A proposal: the EU Data Law Compiler

Combining these patterns, here is a concrete proposal for legislation in the age of AI:

### 1. Enact a Data Law Foundation Regulation
A single horizontal regulation that consolidates all shared definitions, default obligations, and conflict-resolution rules currently scattered across GDPR, Data Act, DGA, and future instruments. Sector laws extend this foundation; they do not redefine it.

### 2. Establish a machine-readable legislative format
All new EU data legislation must be published in both natural language and a structured, machine-readable format (building on Akoma Ntoso / ELI standards). Obligations, definitions, cross-references, and exceptions are expressed as formal rules alongside the legal text.

### 3. Build the Compliance Compiler
An open-source, EU-maintained tool that takes as input:
- A company's profile (sector, size, activities, data types processed, jurisdictions)
- The current corpus of EU data law in machine-readable format

And produces as output:
- A resolved, non-contradictory compliance checklist
- Specific obligations with article references
- Conflict resolutions with explanations
- A diff when any law is updated, showing exactly how the company's obligations changed

### 4. Create a single incident reporting gateway
One entry point for all data-related incident reports. The gateway routes notifications to the appropriate authorities (DPA, financial regulator, CSIRT) based on the incident classification, eliminating the current burden of parallel reporting.

### 5. Adopt semantic versioning for legislation
Every amendment is versioned, changelogged, and diffable. Companies subscribe to the laws relevant to their profile and receive structured notifications when obligations change.

## Why this matters now

The AI Act enters full application in 2026. The EHDS is being implemented. The Data Act obligations take effect. Each new law multiplies the compliance surface non-linearly.

Without architectural thinking, EU data law will become what legacy software becomes: a system so complex that no one fully understands it, where every change risks unintended consequences, and where the cost of compliance becomes a barrier to the innovation the laws were meant to enable.

The EU has the opportunity — and arguably the obligation — to apply to its own regulatory output the same engineering discipline it demands of the companies it regulates.

Legislation can be modular. Compliance can be composable. And law, like code, can be refactored.

---

*Ruth del Campo is the former Director of Data for the Government of Spain. This blog is part of the [EU Data Law Observatory](https://ruthdelcampo.github.io/eu-data-law-observatory/), an open-source project tracking fragmentation, overlaps, and conflicts across EU data legislation.*
