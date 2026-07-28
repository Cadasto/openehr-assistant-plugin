# ADL syntax cheatsheet

**Purpose:** Minimal offline reminder of ADL 1.4 structure. For full syntax and constraint patterns, use `guide_get("openehr://guides/archetypes/adl-syntax")` or see AGENTS.md for spec and grammar links.

---

## ADL 1.4 section order

Aligned with the canonical structure in the openEHR ADL 1.4 specification (archetype as a whole):

1. **`archetype`** — `archetype (adl_version=1.4)` and archetype identifier line
2. **`specialise` / `specialize`** (optional) — parent archetype id
3. **`concept`** — coded concept (terminology code)
4. **`language`** — dADL language section
5. **`description`** (optional) — dADL metadata
6. **`definition`** — cADL constraint tree (slot assertions live here, not in a separate top-level `rules` keyword)
7. **`invariant`** (optional) — top-level first-order assertions (not to be confused with slot rules inside `definition`)
8. **`ontology`** — dADL: `term_definitions`, `constraint_definitions`, `term_bindings` (external terminology bindings are expressed here; ADL 1.4 has no separate top-level `terminology` section)
9. **`revision_history`** (optional) — dADL; expected when the archetype is marked `controlled`

Sections must appear in this order. Every node in the definition must have a corresponding at-code in the ontology.

---

## ADL 1.4 defaults & consistency

- Unstated `occurrences` = `{1..1}`; unstated `existence` = `{1..1}`; `{0}`/`{0..0}` prohibits the node/attribute.
- Existence allows only `{0}`, `{0..1}`, `{1}` (and the `..` spellings); cardinality is for container attributes, occurrences for object nodes — never interchange.
- Consistency: the sum of sibling occurrences ranges must fit inside the container's cardinality interval (validator check `VCOC`).
- `use_node`: the stated RM type must equal or be a supertype of the target node's type (validator check `VUNT`); an `occurrences` on the reference overrides the target's.
- Header may carry `controlled`/`uncontrolled` after the version; `controlled` archetypes should end with a `revision_history`.
- ADL 1.4 source ids carry the **major version only** (`.v1`); the 3-part `v1.0.0` form is the physical HRID (AM Identification / CKM revision metadata).

---

For full syntax use `guide_get("openehr://guides/archetypes/adl-syntax")` or see AGENTS.md for spec/grammar links.
