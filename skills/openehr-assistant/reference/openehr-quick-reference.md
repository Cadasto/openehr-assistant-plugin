# openEHR Quick Reference

**Purpose:** Compact offline reference for reviewing openEHR artifacts without MCP access. For full detail, retrieve the canonical guides via `guide_get()`.
**Keywords:** archetypes, templates, AQL, principles, rules, anti-patterns, CGEM

---

## Archetype Principles

- Each archetype represents **one coherent clinical concept** — modelled independent of UIs or workflows
- **Two-level modelling**: stable Reference Model (RM) separated from expressive archetypes
- **Terminology-neutral**: external code systems (SNOMED CT, LOINC) are bound, not embedded
- **Reuse-first**: search CKM before creating; specialise only for true semantic subtypes
- **Paths are a public API**: stable identifiers (at-codes) and paths enable AQL querying; path changes require a major version
- **Archetypes model data, not process**: workflow and UI constraints belong in templates or applications

> Full guide: `openehr://guides/archetypes/principles`

---

## Key Archetype Design Rules

| Rule | Severity | Summary |
|------|----------|---------|
| **A1** | ERROR | One coherent concept per archetype |
| **A2** | ERROR | Do not combine unrelated concepts |
| **B1** | ERROR | ID follows `openEHR-<DOMAIN>-<RM_TYPE>.<concept>.v<VERSION>` |
| **C1** | ERROR | Use RM structures as intended |
| **C2** | WARNING | Cardinalities justified by clinical reality, not UI convenience |
| **C3** | WARNING | Maximise optionality in archetypes; restriction belongs in templates |
| **D1** | WARNING | Reuse published archetypes wherever semantically appropriate |
| **D2** | WARNING | Slots explicitly constrained (no open wildcards) |
| **E1** | WARNING | Terminology-neutral; bindings optional but recommended |
| **E4** | ERROR | Bindings reflect semantic equivalence, not approximation |
| **F1** | ERROR | All nodes have stable at-codes unchanged across compatible versions |
| **G1** | ERROR | Semantic/data-invalidating changes require major version increment |

> Full guide: `openehr://guides/archetypes/rules`

---

## RM Entry Type Selection

| RM Type | Purpose | Examples |
|---------|---------|---------|
| OBSERVATION | Measured/observed data | Blood pressure, body weight, lab result |
| EVALUATION | Assessed/interpreted data | Diagnosis, risk assessment, problem |
| INSTRUCTION | Orders/requests | Medication order, procedure request |
| ACTION | Activities performed | Medication administration, procedure |
| ADMIN_ENTRY | Administrative data | Admission, discharge, transfer |
| CLUSTER | Reusable data groups | Address, anatomical location, device |

---

## Anti-Patterns

1. **Multi-Concept Archetypes** — mixing unrelated concepts; split and use slots
2. **Terminology Without Meaning** — undocumented or arbitrary code bindings
3. **Over-Specialisation** — specialising for local preference; use templates instead
4. **RM Misuse** — ignoring RM intent (e.g. OBSERVATION as generic record)
5. **Embedded Workflow** — encoding UI or process logic in archetypes
6. **Arbitrary Cardinality** — unjustified min/max constraints
7. **Path-Breaking Refactors** — structural changes that break existing paths

> Full guide: `openehr://guides/archetypes/anti-patterns`

---

## Template Principles

- Templates define datasets for **specific use cases** — minimal, not maximal
- Templates **aggregate** multiple archetypes into coherent COMPOSITION structures
- **Narrowing Principle**: templates can only further constrain archetypes, never relax
  - Mandatory stays mandatory
  - Optional can become mandatory or excluded (`max=0`)
  - Value sets can be reduced but not expanded
- **OET** (source) for authoring; **OPT** (operational) flattened XML for runtime
- Templates bridge clinical models and UIs (rename elements, `hide_on_form` flags)

> Full guide: `openehr://guides/templates/principles`

---

## CGEM Framework (Template Scoping)

| Category | Data Nature | Composition Type |
|----------|-------------|------------------|
| **Global Background** | True regardless of context (allergies, CPR decision) | Longitudinal persistent |
| **Contextual Situation** | Single source per care journey (staging, care plan) | Episodic persistent |
| **Event Assessment** | Each submission is a new record (clinic visit, lab) | Event |
| **Managed Response** | Formal order/fulfilment cycle (referral, prescription) | Instruction/Action |

One form can read/write multiple compositions. Distinguish true managed workflows (Instruction/Action) from simple records.

---

## AQL Essentials

- **Semantics-first**: queries target RM types and archetypes, not storage schema
- **Two pillars**: containment (`CONTAINS`) defines candidate set; archetype paths define projection
- **Prerequisite**: know which OPT and archetypes are deployed; validate paths against them
- **Containment is not a join**: `CONTAINS` expresses RM hierarchy, not table relationships
- **Node-id predicates** on repeating segments prevent ambiguity
- **Stored queries** preferred for production (governance, caching, auditability)

> Full guide: `openehr://guides/aql/principles`

---

## Conflict Resolution Priority

When guides conflict, apply this priority (highest first):

1. Rules and structural constraints
2. Syntax specifications
3. Anti-patterns
4. Principles and examples
5. Convenience

---

## Canonical Guide Index

### Archetypes
| Guide | URI |
|-------|-----|
| Principles | `openehr://guides/archetypes/principles` |
| Rules (22 normative) | `openehr://guides/archetypes/rules` |
| ADL 1.4 Syntax | `openehr://guides/archetypes/adl-syntax` |
| ADL Idioms Cheatsheet | `openehr://guides/archetypes/adl-idioms-cheatsheet` |
| Structural Constraints | `openehr://guides/archetypes/structural-constraints` |
| Terminology Binding | `openehr://guides/archetypes/terminology` |
| Anti-Patterns | `openehr://guides/archetypes/anti-patterns` |
| Quality Checklist | `openehr://guides/archetypes/checklist` |
| Formatting | `openehr://guides/archetypes/reference-formatting` |
| Language Standards | `openehr://guides/archetypes/language-standards` |

### Templates
| Guide | URI |
|-------|-----|
| Principles | `openehr://guides/templates/principles` |
| Rules | `openehr://guides/templates/rules` |
| OET Syntax | `openehr://guides/templates/oet-syntax` |
| OET Idioms | `openehr://guides/templates/oet-idioms-cheatsheet` |
| Checklist | `openehr://guides/templates/checklist` |

### AQL
| Guide | URI |
|-------|-----|
| Principles | `openehr://guides/aql/principles` |
| Syntax | `openehr://guides/aql/syntax` |
| Idioms | `openehr://guides/aql/idioms-cheatsheet` |
| Checklist | `openehr://guides/aql/checklist` |

### Simplified Formats
| Guide | URI |
|-------|-----|
| Principles | `openehr://guides/simplified_formats/principles` |
| Rules | `openehr://guides/simplified_formats/rules` |
| Idioms | `openehr://guides/simplified_formats/idioms-cheatsheet` |
| Checklist | `openehr://guides/simplified_formats/checklist` |

### Reference Model
| Guide | URI |
|-------|-----|
| EHR Information Model | `openehr://guides/rm/ehr-information-model` |
| Demographic Model | `openehr://guides/rm/demographic-model` |
| Platform Services | `openehr://guides/rm/platform-services` |

---
