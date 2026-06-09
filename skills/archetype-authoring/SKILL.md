---
name: archetype-authoring
description: >
  This skill should be used when the user asks to "create an archetype", "edit an archetype",
  "extend an archetype", "specialize an archetype", "design an archetype", "review / remediate
  an archetype" (the full intent -> lint -> fix -> re-lint pipeline), "write the rationale
  (description / purpose / misuse / use)" for one, or "translate / localise an archetype (add a
  language)". Covers creating, editing, specializing, reviewing, remediating, writing rationale
  prose for, and translating openEHR archetypes, plus importing a CKM archetype into the
  workspace for reuse. To merely explain an existing archetype with no edits, use the
  `/openehr-explain` command instead.
argument-hint: "<task: create|edit|extend|specialize> [archetype-id or concept]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__examples_search
  - mcp__openehr-assistant__examples_get
---

# Archetype Authoring

## Conflict Resolution

When guides conflict, apply this priority (highest first):
1. Rules and structural constraints
2. Syntax specifications
3. Anti-patterns
4. Principles and examples
5. Convenience

## Step 1: Load Guides (MANDATORY)

Before any archetype work, load the authoritative guides:

```
guide_get("archetypes/principles")
guide_get("archetypes/rules")
guide_get("archetypes/adl-syntax")
```

Load additional guides as needed:
- `guide_get("archetypes/structural-constraints")` — for cardinality, occurrences, existence rules
- `guide_get("archetypes/terminology")` — for terminology binding patterns
- `guide_get("archetypes/anti-patterns")` — to avoid common mistakes
- `guide_get("archetypes/formatting")` — for ADL formatting conventions

## Step 2: Research Before Creating

Before creating a new archetype, ALWAYS search CKM first:

```
ckm_archetype_search("<concept>")
```

**Reuse-first principle**: If a suitable archetype exists, use it. Only create new archetypes when no existing archetype covers the concept. If a close match exists, consider specialization instead.

**For deep reuse surveys** (unfamiliar domain, or the first few hits look marginal), dispatch the `ckm-scout` agent instead of running searches inline. It runs 3 parallel phrasings, ranks candidates, and returns a reuse/specialize/new recommendation — keeping CKM search noise out of this skill's context.

### Consult gold-standard reference archetypes (when applicable)

For a small set of well-curated CKM archetypes — blood pressure, medication order, problem/diagnosis, encounter, procedure, anatomical location (CLUSTER), translation requirements (ADMIN_ENTRY) — try `examples_search(kind="archetypes")` when authoring or reviewing an archetype of the same type. These are native `.adl` files exposed as `openehr://examples/archetypes/{name}` and serve as concrete prior-art references for RM-type intent, terminology binding patterns, and structural idioms. Skip this step when the concept is outside the curated set.

### Import a CKM archetype for reuse

When reuse means pulling a published archetype into the workspace (not just citing it), make it land as a wired-in file rather than a copy-paste note:

1. Fetch the native ADL with `ckm_archetype_get("<id>")`.
2. Write it into the project (e.g. a `local/` directory) under its canonical `openEHR-EHR-<TYPE>.<concept>.v<N>.adl` filename.
3. If it fills a slot in a target archetype/template, add the constrained slot reference (`allow_archetype … include`) so the reuse is actually wired in.

A reused file keeps its published `uid`/checksums; do not alter them.

## Step 3: Concept Design

### One Concept Per Archetype
Each archetype represents exactly one clinical concept. If you find yourself modeling multiple independent ideas, split into separate archetypes connected via slots.

### RM Entry Type Selection
Choose the correct Reference Model entry type:

| RM Type | Purpose | Examples |
|---------|---------|---------|
| OBSERVATION | Measured/observed data | Blood pressure, body weight, lab result |
| EVALUATION | Assessed/interpreted data | Diagnosis, risk assessment, problem |
| INSTRUCTION | Orders/requests | Medication order, procedure request |
| ACTION | Activities performed | Medication administration, procedure |
| ADMIN_ENTRY | Administrative data | Admission, discharge, transfer |
| CLUSTER | Reusable data groups | Address, anatomical location, device |

Use `type_specification_get` to verify RM type structure when uncertain.

### Identifier Scheme
Follow the pattern: `openEHR-EHR-<RM_TYPE>.<concept>.v<VERSION>`

Examples:
- `openEHR-EHR-OBSERVATION.blood_pressure.v2`
- `openEHR-EHR-CLUSTER.anatomical_location.v1`

## Step 4: ADL Authoring

### Constraint Patterns
Use `guide_adl_idiom_lookup` for specific ADL constraint patterns:
- Coded text constraints
- Quantity ranges with units
- Ordinal scales
- Date/time constraints
- Slot definitions

### Terminology Section
- Define all at-codes with clear, descriptive text
- Bind to standard terminologies (SNOMED CT, LOINC, ICD-10) where appropriate
- Use `terminology_resolve` to verify terminology codes
- Ensure semantic equivalence, not approximation, in bindings

### Design for Reuse
- Keep archetypes terminology-neutral (avoid hardcoding specific value sets)
- Use explicit slot constraints (avoid open wildcards like `include all`)
- Design for international use — avoid locale-specific assumptions

### Identifiers and checksums
- A new archetype needs a fresh `uid`. Generate one portably: `uuidgen`, else `cat /proc/sys/kernel/random/uuid`, else `python3 -c 'import uuid; print(uuid.uuid4())'`.
- **Do not hand-write build checksums** (`MD5-CAM-*`, `build_uid`) — they are tool-computed by CKM/ADL tooling. If you edit a published archetype, its checksum simply becomes stale: note that for upstream recomputation rather than inventing a value. This is advisory, not a blocker — a missing/stale checksum never stops local authoring.

## Step 5: Editing Existing Archetypes

When modifying existing archetypes:
- **Path stability**: Never rename or remove existing paths in minor versions
- **Backwards compatibility**: Additions are safe; removals require major version bump
- **Deprecation over removal**: Mark elements as deprecated before removing in next major version

## Step 6: Specialization

When extending via specialization:
- Only specialize for genuine semantic subtypes (e.g., blood_pressure -> invasive_blood_pressure)
- Single inheritance only — one parent archetype
- Preserve parent meaning — specialization narrows, never contradicts
- Maintain transparent lineage in the archetype identifier

## Step 7: Review & Remediate

The full review pipeline (this absorbs the former `/archetype-review` command). Run it when reviewing an archetype for quality, publication, or CKM submission. For a quick lint with no remediation, the `archetype-lint` skill (`/archetype-lint`) is the lighter entry point.

### 7a. Intent & provenance
- State the concept, the candidate ENTRY type, scope boundaries, and a **must-not-change list** (paths, at-codes, semantic anchors).
- **Provenance check (advisory):** decide whether the file is a mirror of a published CKM archetype (matching id/revision). If so, note that editing it locally diverges from canonical, and its `MD5-CAM` checksum will no longer match — prefer contributing the change upstream in CKM. Surface this as a caveat; it does not block local work.
- If the examples corpus holds the same archetype id, `examples_get` it and compare `uid`/revision to spot drift from the gold-standard.

### 7b. Lint
Apply the 22 normative lint rules — load `guide_get("archetypes/rules")` for the definitions (the `archetype-lint` skill runs this standalone). Also load:

```
guide_get("archetypes/checklist")
guide_get("archetypes/anti-patterns")
```

Use `type_specification_get` to verify RM attribute names (rule 4). Output PASS/FAIL plus a violations table (severity, rule, explanation, suggested fix).

### 7c. Remediate
- **On FAIL (ERRORs):** produce a minimal-diff fix plan mapped to rule violations — for each fix, note whether it changes paths or semantics and the version-bump implication. Present the plan and wait for approval; then patch and re-lint (max ~3 iterations).
- **On PASS with WARNING/INFO:** do not stop at "nothing to improve." Produce an advisory-remediation block — issue → suggested improvement → which fixes touch paths/semantics/checksums — without invoking the ERROR-only fix machinery. "Spot issues and suggest improvements" is a valid request even when the archetype passes.

### 7d. Review packet (optional)
For a CKM-style review, generate justifications for any unresolved warnings and questions for clinicians, alongside the rationale prose below.

### 7e. Rationale prose (description / purpose / misuse / use)
Draft CKM-quality rationale prose when the structure is stable but the prose is thin or missing (used late, pre-CKM-submission). Works on a workspace `.adl` or a CKM id (`ckm_archetype_get`).

1. Load `guide_get("archetypes/principles")` and `guide_get("archetypes/language-standards")` for vocabulary.
2. Ground the prose in the bound terminology: resolve **openEHR** codes with `terminology_resolve`; for **SNOMED CT / LOINC / ICD** bindings (which `terminology_resolve` does *not* cover — openEHR terminology only) read the rubric from the archetype's own `term_definitions` / `term_bindings` and do not fabricate an external preferred term.
3. Match prose style to 1–2 published siblings of the same RM entry type (`ckm_archetype_get`); if a specific sibling id is blocked, fall back to any published archetype of that type.
4. Draft each section: **description** (≤2 sentences — what is captured), **purpose** (2–3 sentences — why it exists), **misuse** (what it should NOT be used for, redirecting to siblings), **use** (concrete recording scenarios).

These fields live under `description.details["<lang>"]` in ADL 1.4 (`misuse`/`use` are single newline-joined string values, not bullet arrays) — present a readable sketch but tell the user how it maps into ADL. Use consistent openEHR vocabulary ("record" not "capture", "clinical statement" not "entry"); keep British English; never invent clinical facts — leave a flagged `TODO: clinical input needed — <question>` where a section can't be grounded.

Final checklist:
- [ ] One concept per archetype
- [ ] Correct RM type selected
- [ ] Valid ADL 1.4 syntax
- [ ] All at-codes defined in terminology section
- [ ] Terminology bindings use semantic equivalence
- [ ] Slot constraints are explicit
- [ ] No anti-patterns present
- [ ] Formatting follows conventions

## Step 8: Translate / add a locale

Add or translate per-language text in an archetype's `ontology.term_definitions` for a target language (ISO 639-1, e.g. `nl`, `de`, `fr`). In ADL 1.4 translations live in the ontology block, not a separate top-level `terminology` section.

1. Load `guide_get("archetypes/language-standards")` and any per-language guide (e.g. `guide_get("archetypes/language-standards-nl")`).
2. Locate the source-language `term_definitions` (e.g. `["en"]`); `term_bindings` are language-independent and stay unchanged.
3. Translate each at-code's `text` and `description` into clinically natural target-language wording — preserve clinical precision, flag uncertain terms for review, and reuse community terms where they already exist (via `ckm_archetype_get` / `examples_get`) rather than minting new ones.
4. Insert the new locale **at the top of its block** (anchor on the block opener + its first child; ADL is **tab**-indented, not spaces) in three places: `language.translations`, `description.details`, and `ontology.term_definitions`.
5. Verify (machine-checkable — base the "done" claim on it):
   - **at-code parity** — source vs target term counts match (e.g. `en vs nl: 69 = 69`);
   - **delimiter balance** — every `<` opened is closed across the inserted blocks;
   - **untouched invariants** — no change to at-codes, occurrences/cardinalities, units, value sets, or `term_bindings` (a translation edits text only);
   - **lint** — run the Step 7b lint pass and surface its summary; failures block "done".
6. Advisory: editing makes `MD5-CAM`/`revision` stale — flag for upstream recomputation, never hand-fabricate. This never blocks producing the translation.

## Output

Generate valid ADL 1.4 files. Use the Write tool to create `.adl` files in the appropriate project location.
