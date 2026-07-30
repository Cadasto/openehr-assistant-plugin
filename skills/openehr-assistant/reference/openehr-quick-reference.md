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
| **B1** | ERROR | ID follows `<rm_publisher>-<rm_closure>-<rm_class>.<concept>.v<version>`; ADL 1.4 source uses major version only (`.v1`) — `v1.0.0` is the physical HRID (AM Identification / CKM metadata) |
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

## Composition Categories

| Category | Semantics | Use Case |
|----------|-----------|----------|
| **event** | Point-in-time record of a healthcare event | Encounter notes, lab results, vital signs |
| **persistent** | Ongoing patient state, maintained as a single updated instance | Problem list, medication list, allergies |
| **episodic** | Scoped to a bounded care period, transitions to inactive when episode ends | Hospital admission, care episode |

---

## ISM State Machine

Instructions and their Activities follow a standard state machine:

```
INITIAL → PLANNED → SCHEDULED → ACTIVE → COMPLETED
                                  ↓          ↑
                              SUSPENDED ──────┘
         POSTPONED ←──────┐
         CANCELLED ←──────┤
         ABORTED ←────────┘
         EXPIRED
```

Query for active medications or planned interventions via standardised ISM states.

> Full guide: `openehr://guides/specs/rm-ehr`

---

## Time Layers

| Layer | Where | Meaning |
|-------|-------|---------|
| **Observation time** | `HISTORY.origin`, `EVENT.time` | When the phenomenon was true (sample time) |
| **Healthcare event time** | `EVENT_CONTEXT.start_time` | When the encounter occurred |
| **Commit time** | `AUDIT_DETAILS.time_committed` | When data entered the EHR (server-side) |
| **Domain-specific times** | Archetyped values in Entries | Date of onset, resolution, medication start |

---

## Versioning Essentials

- **VERSIONED_OBJECT** — container with stable uid; holds all versions of one top-level item
- **VERSION uid** — 3-part: `{object_id :: creating_system_id :: version_tree_id}`
- **CONTRIBUTION** — atomic change-set grouping one or more Version commits
- **Lifecycle states** — `complete`, `incomplete`, `deleted`, `inactive`, `abandoned`
- **AUDIT_DETAILS** — every commit: system_id, committer, time_committed, change_type

> Full guide: `openehr://guides/specs/rm-ehr`

---

## PARTY Hierarchy

```
PARTY (abstract)
├── ACTOR (abstract) — real-world entities
│   ├── PERSON
│   ├── ORGANISATION
│   ├── GROUP        — named collection of actors
│   └── AGENT        — devices, software
└── ROLE             — competency performed by an Actor
```

- **PARTY_IDENTITY** — names (legal, alias). State-issued identifiers go in `PARTY.details`.
- **PARTY_RELATIONSHIP** — directed: source → target (e.g., patient-of, employed-by)

> Full guide: `openehr://guides/specs/rm-demographic`

---

## EHR/Demographic Separation

Three levels of subject identification via PARTY_SELF:

| Level | external_ref | Privacy |
|-------|-------------|---------|
| **Anonymous** | None anywhere | Maximum; cross-reference maintained externally (EHR Index) |
| **Single reference** | In EHR_STATUS.subject only | EHR contents remain anonymous |
| **Embedded** | In every PARTY_SELF instance | Convenient for closed/secure environments |

> Full guide: `openehr://guides/specs/rm-demographic`

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
- Template jobs: **composition** (fill slots), **element choice** (remove/mandate), **narrowing**, and **setting defaults**
- **Defaults vs assumed values**: template defaults appear in the recorded data; archetype-level assumed values do not
- **OET** and Archetype Designer **`.t.json`** (source layer — `.t.json` is AOM2 differential JSON, tool-managed, *not* a web template) for authoring; **OPT** (operational) flattened for runtime (XML in ADL 1.4 practice; OPT2 allows ADL/XML/JSON/YAML); **web template** (JSON) is the vendor runtime projection derived from the OPT, driving UI and FLAT/STRUCTURED paths
- Templates bridge clinical models and UIs (rename elements, `hide_on_form` flags)

> Full guides: `openehr://guides/templates/principles`, serialisation set: `openehr://guides/templates/serialization-formats`, `openehr://guides/templates/opt-structure`, `openehr://guides/templates/web-template`

---

## CGEM Framework (Dataset Splitting / Template Scoping)

freshEHR's analysis method for splitting a dataset before modelling — a **design aid, not an openEHR specification**; it operationalises the spec's own temporal composition model.

| Category | Data Nature | `COMPOSITION.category` | Versioning |
|----------|-------------|------------------|---|
| **Global Background** | True regardless of context, for life (allergies, problem list, CPR decision) | `persistent` (431) | one current version, updated in place |
| **Contextual Situation** | Single source of truth per care journey / episode / condition (staging, care plan) | `episodic` (451) | one current version per journey; new journey → new instance |
| **Event Assessment** | Each submission is a new record (clinic visit, lab, score) | `event` (433) | never overwritten; many over time |
| **Managed Response** | Formal order/fulfilment cycle (referral, prescription) | **no category code** — usually `event` | order state tracked across ACTIONs via the ISM |

- **Four categories, three codes** — Managed Response is not a `COMPOSITION.category`; it is an `event` (sometimes `persistent`) composition distinguished by INSTRUCTION/ACTION + the ISM.
- **`451 episodic`** is normative but unevenly implemented — confirm platform support; `persistent` plus governance conventions is the common fallback.
- One form can read/write **multiple** compositions across several categories; Global Background is often only *read*. Distinguish true managed workflows from simple records ("Referral date" is a record, not an order).

> Full guide: `openehr://guides/templates/cgem-framework` (freshEHR CGEM — definitions, openEHR mapping table, caveats)

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

## Syntax cheatsheets

Minimal offline syntax reminders (full detail: MCP guides or AGENTS.md):

- **ADL**: [adl-syntax-cheatsheet.md](adl-syntax-cheatsheet.md) — ADL 1.4 section order; use `guide_get("openehr://guides/archetypes/adl-syntax")` or AGENTS.md for spec/grammar links.
- **AQL**: [aql-syntax-cheatsheet.md](aql-syntax-cheatsheet.md) — SELECT/FROM/WHERE structure; use `guide_get("openehr://guides/aql/syntax")` or AGENTS.md for spec/grammar links.

---

## Canonical Guide Index

### Archetypes
| Guide | URI |
|-------|-----|
| Principles | `openehr://guides/archetypes/principles` |
| Design Rules (rule sets A–K) | `openehr://guides/archetypes/rules` |
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
| CGEM Framework | `openehr://guides/templates/cgem-framework` |
| OET Syntax | `openehr://guides/templates/oet-syntax` |
| OET Idioms | `openehr://guides/templates/oet-idioms-cheatsheet` |
| Serialization Formats | `openehr://guides/templates/serialization-formats` |
| OPT Structure | `openehr://guides/templates/opt-structure` |
| Web Template | `openehr://guides/templates/web-template` |
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

### Specification digests (reference-model and related)
| Guide | URI |
|-------|-----|
| EHR Information Model | `openehr://guides/specs/rm-ehr` |
| Demographic Model | `openehr://guides/specs/rm-demographic` |
| Platform Services | `openehr://guides/specs/sm-openehr_platform` |

The MCP server exposes additional spec digests under `openehr://guides/specs/` covering AM (ADL1.4, AOM1.4, Overview, Identification), AM2 (ADL2, AOM2, OPT2), BASE, QUERY (AQL), TERM, LANG (incl. BMM, BMM3, EL, ODIN), CDS (GDL2), PROC (overview, task planning, decision language), CNF (conformance guide), SM, and ITS-REST. Digests track the openEHR **development** branch.

### OpenAPI REST Schemas

Validation schemas (OAS 3.x) for the openEHR REST API:

https://github.com/openEHR/specifications-ITS-REST/tree/master/computable/OAS

| Schema | Covers |
|--------|--------|
| `ehr-validation.openapi.yaml` | EHR, Composition, Directory, Contribution, Tags |
| `demographic-validation.openapi.yaml` | Person, Organisation, Group, Agent, Role |
| `definition-validation.openapi.yaml` | Templates (ADL 1.4/2), Stored Queries |
| `query-validation.openapi.yaml` | AQL execution, Stored Query execution |
| `admin-validation.openapi.yaml` | EHR deletion (admin) |
| `system-validation.openapi.yaml` | Service discovery, conformance |
| `overview-validation.openapi.yaml` | Cross-cutting: HTTP conventions, headers, status codes |

---

## Online retrieval path (when MCP is available)

When MCP access is available, prefer routed retrieval over direct HTTP fetches:

1. **Spec overview questions** → `guide_get(category="specs", name="<component>-<doc>")` (250–900 word digests tracking the `development` branch).
2. **Class-level attribute / function / invariant detail** → `type_specification_get("<TYPE_NAME>")` (BMM-backed, exhaustive).
3. **Worked examples** (AQL, FLAT, STRUCTURED, reference `.adl` archetypes) → `examples_search(kind=...)` / `examples_get("openehr://examples/<kind>/<name>")`.
4. **Efficient external spec retrieval** → `guide_get("openehr://guides/howto/spec-lookup")`; it documents the `llms.txt` site index, the `.md` twin URL pattern (**most** `*.html` spec pages have a `.md` counterpart — prose only, not per-class tables; fall back to HTML when a twin 404s), and the `/api/{components,classes,releases}.json` endpoints.

This plugin tracks `releases/XX/development/` for external spec URLs unless the user explicitly asks for a fixed release tag.

---
