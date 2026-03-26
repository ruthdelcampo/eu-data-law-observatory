---
title: Cyber Resilience Act
abbreviation: CRA
celex: 32024R2847
type: regulation
scope: sector-specific
sector: cybersecurity
enacted: 2024-10-23
in_force: 2024-12-10
eurlex_url: "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"
status: in-force
related_laws: [NIS2, GDPR, AI Act, DORA, eIDAS 2]
tags: [cybersecurity, products-with-digital-elements, vulnerability-handling, CE-marking, security-by-design, software-security, hardware-security, supply-chain, SBOM]
last_updated: 2026-03-26
---

## Summary

The Cyber Resilience Act (Regulation (EU) 2024/2847) is a horizontal EU regulation that establishes mandatory cybersecurity requirements for products with digital elements -- both hardware and software -- placed on the EU market. Enacted on 23 October 2024 and entering into force on 10 December 2024, the CRA addresses the widespread problem of insufficient cybersecurity in connected products by requiring security to be built in from the design phase onward. It applies to any product with a direct or indirect logical or physical data connection to a device or network, covering everything from consumer IoT devices and operating systems to industrial control systems and network equipment.

The regulation places primary responsibility on manufacturers, who must conduct cybersecurity risk assessments, ensure products meet essential cybersecurity requirements (set out in Annex I), handle vulnerabilities throughout a defined support period of at least five years, and maintain a software bill of materials (SBOM). Importers and distributors also bear obligations to verify compliance before making products available on the EU market. Products must carry the CE marking to indicate conformity with cybersecurity requirements, and manufacturers must report actively exploited vulnerabilities to ENISA and the relevant national CSIRT within 24 hours of becoming aware of them, with follow-up reports at 72 hours and a final report within 14 days.

The CRA classifies products into default, important (Class I and II in Annex III), and critical (Annex IV) categories, each subject to increasingly stringent conformity assessment procedures. Important products include items such as identity management systems, firewalls, intrusion detection systems, and VPN products. Critical products include those on which essential entities under NIS2 critically depend. The regulation also includes specific provisions for free and open-source software, introducing the concept of "open-source software stewards" who have lighter obligations than commercial manufacturers but must still support vulnerability handling. The CRA explicitly interacts with the AI Act: products with digital elements classified as high-risk AI systems that comply with CRA cybersecurity requirements are deemed to satisfy the cybersecurity provisions of the AI Act.

Market surveillance and enforcement are carried out by national authorities under the framework established by Regulation (EU) 2019/1020, with penalties for non-compliance that can reach up to 15 million EUR or 2.5% of worldwide annual turnover, whichever is higher. The regulation includes transitional provisions, with manufacturer reporting obligations applying from 11 September 2026 and the full set of obligations applying from 11 December 2027.

## Key Provisions

- **Article 1 -- Subject matter**: Establishes the scope of the regulation, covering rules for market placement, essential cybersecurity requirements for design/development/production, vulnerability handling obligations, and market surveillance rules.
- **Article 2 -- Scope**: Applies to all products with digital elements that have a data connection to a device or network; excludes medical devices, vehicles, aviation products, and products for national security/defence.
- **Article 6 -- Requirements for products with digital elements**: Products may only be placed on the market if they meet essential cybersecurity requirements (Annex I Part I) and the manufacturer's processes comply with vulnerability handling requirements (Annex I Part II).
- **Article 7 -- Important products with digital elements**: Defines two classes (I and II) of important products in Annex III, subject to stricter conformity assessment procedures based on cybersecurity risk.
- **Article 8 -- Critical products with digital elements**: Allows the Commission to require European cybersecurity certification for critical product categories listed in Annex IV.
- **Article 12 -- High-risk AI systems**: Creates a compliance bridge with the AI Act -- CRA-compliant products are deemed to meet the cybersecurity requirements of the AI Act for high-risk AI systems.
- **Article 13 -- Obligations of manufacturers**: The core obligations article requiring cybersecurity risk assessment, security by design, a minimum 5-year support period, SBOM maintenance, coordinated vulnerability disclosure policies, CE marking, and provision of security updates for at least 10 years.
- **Article 14 -- Reporting obligations of manufacturers**: Mandates notification of actively exploited vulnerabilities (24h early warning, 72h detailed notification, 14-day final report) and severe security incidents to CSIRTs and ENISA via a single reporting platform.
- **Articles 15-20 -- Obligations of importers, distributors, and open-source software stewards**: Extends supply chain responsibility to importers and distributors who must verify manufacturer compliance; introduces lighter obligations for open-source software stewards.
- **Articles 32-34 -- Conformity assessment**: Defines conformity assessment procedures ranging from internal control (default) to third-party assessment (for important Class II and critical products).
- **Annex I -- Essential cybersecurity requirements**: Two-part annex covering product security requirements (Part I: security by design, access control, data protection, resilience) and vulnerability handling process requirements (Part II: SBOM, coordinated disclosure, security updates).
- **Annex III -- Important product categories**: Lists Class I (e.g., password managers, VPNs, firewalls) and Class II (e.g., hypervisors, HSMs, smartcard readers) products subject to stricter assessment.
- **Article 64 -- Penalties**: Non-compliance with essential cybersecurity requirements can result in fines up to 15 million EUR or 2.5% of global turnover; other violations up to 10 million EUR or 2%.

## Table of Contents

- [Recitals & Preamble](recitals.md)
- [Chapter I — GENERAL PROVISIONS](chapter-01.md)
- [Chapter II — OBLIGATIONS OF ECONOMIC OPERATORS AND PROVISIONS IN RELATION TO FREE AND OPEN-SOURCE SOFTWARE](chapter-02.md)
- [Chapter III — CONFORMITY OF THE PRODUCT WITH DIGITAL ELEMENTS](chapter-03.md)
- [Chapter IV — NOTIFICATION OF CONFORMITY ASSESSMENT BODIES](chapter-04.md)
- [Chapter V — MARKET SURVEILLANCE AND ENFORCEMENT](chapter-05.md)
- [Chapter VI — DELEGATED POWERS AND COMMITTEE PROCEDURE](chapter-06.md)
- [Chapter VII — CONFIDENTIALITY AND PENALTIES](chapter-07.md)
- [Chapter VIII — TRANSITIONAL AND FINAL PROVISIONS](chapter-08.md)
- [Annexes](annexes.md)
