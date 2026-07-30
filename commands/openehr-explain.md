---
name: openehr-explain
description: One-stop router that explains or looks up any openEHR thing — auto-detects an archetype, a template, an RM/AM/BASE type, an RM structural concept, an ADL idiom, an AQL query or keyword, or a terminology code (replaces /archetype-explain, /template-explain, /type-spec, /rm-structure, /adl-idiom, /terminology)
argument-hint: "<archetype|template id-or-file | RM/AM type | RM structural concept | ADL idiom | AQL query/keyword | terminology code>"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__type_specification_search
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__guide_get
  - Read
  - Glob
  - Grep
---

# /openehr-explain

Explain or look up whatever the user names: **$ARGUMENTS**. Auto-detect the kind of
input, route it to the matching lookup, and produce the explanation in that kind's
output shape. Read-only — never suggest modifications.

## Step 1 — Classify the input

Pick exactly one kind using these heuristics (first match wins):

- **Archetype** — an id like `openEHR-EHR-OBSERVATION.*` (any `openEHR-<RM>-<class>.<concept>.v#`),
  or a workspace path ending in `.adl`. (Other `.adl` references such as ADL2 are also archetypes.)
- **Template** — an id ending in a template/OPT identifier, or a path ending in `.oet` / `.opt`.
- **RM/AM/BASE type** — a single ALL-CAPS token in the openEHR type style: `DV_QUANTITY`,
  `COMPOSITION`, `OBSERVATION`, `ELEMENT`, `C_ATTRIBUTE`. Underscores and a leading `DV_`/`C_`
  are strong signals; no version, no path.
- **RM structural concept** — how the model is *structured* rather than one class: e.g.
  "composition categories", "ISM states", "versioning", "PARTY hierarchy", "identities vs
  identifiers", "privacy / EHR–demographic separation"; often prefixed with a domain
  (`ehr` / `demographic`). Distinguish from a bare class token (that's an RM/AM type).
- **ADL idiom / pattern** — phrasing about *how to constrain*: "coded text constraint",
  "ordinal scale", "quantity range", "slot", "how do I constrain …", "what's the ADL for …".
- **AQL query / keyword** — an AQL statement (contains `SELECT` / `FROM` / `CONTAINS` / `WHERE`),
  or a question about AQL syntax — a clause/operator/function ("what does `CONTAINS` do", "AQL for
  latest-per-EHR"). Explanation only; to *write / optimize / review* a query, that is the
  `aql-authoring` skill, not this command.
- **Terminology** — an openEHR terminology code/term, a `local::`/`at####` code, a known
  terminology id (e.g. `openehr`, SNOMED-CT, LOINC) code, or the URI `openehr://terminology`.

If the input is a workspace file path, you may `Read` it (and `Glob`/`Grep` to locate it)
to confirm the kind before routing. If genuinely ambiguous (e.g. an ALL-CAPS token that
could be a type or a terminology rubric), ask **one** brief clarifying question, then route.

## Step 2 — Route to the matching lookup and explain

### A. Archetype  (`ckm_archetype_get`)
1. Load context: `guide_get("openehr://guides/archetypes/principles")`, `guide_get("openehr://guides/archetypes/structural-constraints")`, `guide_get("openehr://guides/archetypes/terminology")`.
2. Retrieve with `ckm_archetype_get` or `Read` (workspace `.adl`). The identifier must be a CKM CID (e.g. `1013.1.7850`) or a full archetype-id (`openEHR-EHR-…`) — for a bare concept name, run `ckm_archetype_search` first and take the CID from the hit.
3. Clarify RM types with `type_specification_get`; note related archetypes referenced in slots.
4. **Do NOT** suggest improvements, assume template/UI behavior, or add concepts not present.
5. Output:
   1. **High-Level Clinical Meaning** — what it represents, typical use, what it does NOT represent
   2. **Core Data Semantics** — main elements; mandatory vs optional; repeating vs single
   3. **Terminology Semantics** — coded elements, value sets, bindings and intent
   4. **Structural Semantics** — clusters/slots/repetitions rationale; protocol/state; implicit assumptions
   5. **Semantic Boundaries & Assumptions** — scope edges, ambiguities, decisions deferred to templates
   6. **Summary** — one documentation-ready paragraph

### B. Template  (`ckm_template_get`)
1. Load context: `guide_get("openehr://guides/templates/principles")`, `guide_get("openehr://guides/templates/rules")`. For a runtime artefact (`.opt` file, web-template JSON, or questions about FLAT path ids), also `guide_get("openehr://guides/templates/opt-structure")` / `guide_get("openehr://guides/templates/web-template")`.
2. Retrieve with `ckm_template_get` (CKM CID) or `Read` (workspace `.oet`, `.t.json`, `.opt`/`.optx`/`.optj`, or a web-template JSON). For a CID, ask the preferred format first: OET (design-time, default) or OPT (operational). Name the layer you are explaining — **source** (OET / Archetype Designer `.t.json`: slots and overlays intact), **compiled** (OPT: constraints inlined), or **derived runtime** (web template: simplified, lossy, the FLAT/STRUCTURED path schema) — and load `guide_get("openehr://guides/templates/serialization-formats")` when the artefact is not an OET.
3. Retrieve referenced archetypes via `ckm_archetype_get` for deeper explanation; clarify RM types with `type_specification_get`.
4. **Do NOT** suggest improvements, assume UI behavior beyond what is explicitly constrained, or add concepts not present.
5. Output:
   1. **Use Case & Context** — clinical scenario, main purpose, intended users
   2. **Composition Structure** — root archetype overview; brief rationale per included archetype
   3. **Narrowing & Constraints** — exclusions (`max=0`), required escalations (`min=1`), reduced value sets vs base archetypes
   4. **Data & Terminology Semantics** — meaning of coded items, units, clinical ranges
   5. **UI & Implementation Hints** — annotations, labels, presentation constraints (`hide_on_form`, etc.)
   6. **Summary** — one implementation-ready paragraph; note dependency on the target OPT

### C. RM/AM/BASE type  (`type_specification_search` → `type_specification_get`)
1. `type_specification_search` for the name (use `*` wildcards for broad search, e.g. `*ENTRY*`, `DV_*`).
2. Present up to 10 matches with name, documentation, component, package. If several plausible matches, ask which to retrieve.
3. Once confirmed, `type_specification_get` for the full definition.
4. Output:
   - Raw BMM JSON definition
   - Implementer explanation: purpose, key attributes and their types, inheritance hierarchy, constraints/invariants

### D. ADL idiom / pattern  (`guide_adl_idiom_lookup`)
1. `guide_adl_idiom_lookup` for the requested pattern.
2. Output:
   - ADL code snippet showing the constraint pattern
   - Brief explanation of what the pattern does
   - When to use this pattern
   - Common variations or modifications

### E. Terminology  (`terminology_resolve`)
1. Load context: `guide_get("openehr://guides/archetypes/terminology")`.
2. `terminology_resolve` for the code/rubric/description — **openEHR terminology only**; it errors on anything it cannot resolve, so do not route SNOMED CT / LOINC / ICD codes to it (say so and read the rubric from the artefact's `term_bindings` instead).
3. Distinguish **terminology groups** (concept-rubric pairs under an openEHR groupId) from **codesets** (standardized enumerations).
4. Output:
   - Code string
   - Rubric / display text
   - Terminology ID (e.g. `openehr`, SNOMED-CT, LOINC)
   - Related codes or value sets
   - Whether it is a group or codeset, its purpose in openEHR, and clinical usage context

### F. RM structural concept  (`guide_get("openehr://guides/specs/rm-ehr" | ".../specs/rm-demographic")` + `type_specification_get`)
1. Determine the domain — `ehr` or `demographic`. If not given, infer from the concept (e.g. "composition" → ehr, "party" → demographic) and state the inference up front.
2. Load the RM digest: `guide_get("openehr://guides/specs/rm-ehr")` or `guide_get("openehr://guides/specs/rm-demographic")`.
3. Use `type_specification_get` for class-level detail (attributes, functions, invariants) when the user needs it.
4. Output: definition & purpose; key components/states (tables/trees where apt); relation to other RM structures (and the other domain where relevant); practical implications for modelling, querying, or deployment.
   - Concept areas — **ehr**: ehr-parts, composition-categories, entry-types, ISM states, time, versioning, cross-cutting (`LOCATABLE`/`PARTY_PROXY`). **demographic**: party-hierarchy, roles, identities (`PARTY_IDENTITY` vs `PARTY.details`), relationships, privacy, versioning, archetyping.
   - For broader `specs/` sub-domains (Common, Data Structures, Data Types, Integration, EHR Extract, and the PROC/CNF/LANG digests — Task Planning, Decision Language, conformance, BMM/BMM3), point the user to `guide_get("openehr://guides/specs/<component>-<doc>")`.

### G. AQL query / keyword  (`guide_get("openehr://guides/aql/syntax")` + `ckm_archetype_get`)
1. Load context: `guide_get("openehr://guides/aql/syntax")` (and `guide_get("openehr://guides/aql/principles")` for concepts).
2. **Given a full query** — explain its structure and what it returns: `SELECT` projection, `FROM`/`CONTAINS` containment, `WHERE` predicates, `ORDER BY`/`LIMIT`. Resolve referenced archetype paths with `ckm_archetype_get` where it aids the explanation; verify path endpoints against the deployed template, not display labels.
3. **Given a keyword / operator / function** — explain its meaning, syntax, and a minimal example from the guide.
4. **Read-only.** Do NOT optimize or rewrite. To author, optimize, or review a query, hand off to the `aql-authoring` skill.
