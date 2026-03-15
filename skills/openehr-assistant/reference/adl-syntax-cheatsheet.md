# ADL syntax cheatsheet

**Purpose:** Minimal offline reminder of ADL 1.4 structure. For full syntax and constraint patterns, use `guide_get("archetypes/adl-syntax")` or see AGENTS.md for spec and grammar links.

---

## ADL 1.4 section order

1. **Header** — `archetype (adl_version)` line, `concept`, `language`, optional `description`, `definition`, `ontology`, `terminology`
2. **definition** — cADL tree (composite and primitive constraints)
3. **rules** — optional assertions (e.g. slot constraints)
4. **ontology** — at-codes, ac-codes, term bindings
5. **terminology** — external terminology bindings (code sets, constraint bindings)

Sections must appear in this order. Every node in the definition must have a corresponding at-code in the ontology; terminology section links to external code systems.

---

For full syntax use `guide_get("archetypes/adl-syntax")` or see AGENTS.md for spec/grammar links.
