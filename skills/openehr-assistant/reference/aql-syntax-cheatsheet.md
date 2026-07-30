# AQL syntax cheatsheet

**Purpose:** Minimal offline reminder of AQL structure. For full syntax and path rules, use `guide_get("openehr://guides/aql/syntax")` or see AGENTS.md for spec and grammar links.

---

## AQL clause structure

- **SELECT** — list of projection items (e.g. path aliases, `c/content[...]`, `e` for composition)
- **FROM** — top-level composition variable and **CONTAINS** hierarchy (archetype and path constraints)
- **WHERE** — optional predicates (node-id, time, value filters)
- **ORDER BY** — optional sort (e.g. `e/time_created DESC`); **LIMIT n [OFFSET m]** optional pagination

Containment defines the candidate set; archetype paths in SELECT define what is projected. Validate paths against the deployed template (OPT).

---

## Quick reminders

- **MATCHES** with a `{…}` value list is spec-normative (items OR-ed; parameters allowed); `IN` is an engine extension — prefer MATCHES.
- Sibling disambiguation by name: `items[at0001, 'Systolic']` (shortcut for `[at0001 and name/value='Systolic']`).
- Version-aware queries: `CONTAINS VERSION v[LATEST_VERSION]` / `v[ALL_VERSIONS]` — always state the predicate explicitly (the no-predicate default is unspecified); grammar-level only, verify engine support.
- Spec-defined aggregates: `COUNT`, `MIN`, `MAX`, `SUM`, `AVG` (COUNT/MIN/MAX safest across engines); core single-row functions (LENGTH, CONCAT, ROUND, CURRENT_DATE_TIME/NOW, TERMINOLOGY, …) are spec-defined but engine coverage varies — anything else is an engine extension.

---

For full syntax use `guide_get("openehr://guides/aql/syntax")` or see AGENTS.md for spec/grammar links.
