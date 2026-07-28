---
name: semantic-diff
description: Semantic diff between two openEHR artefacts — auto-detects archetype (ADL) vs template (OET/OPT) and version vs sibling/cross-artefact comparison; reports added/removed at-codes or archetype includes, cardinality/occurrences/narrowing and terminology-binding changes, and either a version-bump verdict (patch/minor/major per rule G1) or a sibling compatibility/divergence report with a path-compatibility table.
argument-hint: "<file-a> <file-b>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__ckm_template_get
---

# /semantic-diff

Compare two openEHR artefacts at the **semantic** level — not textual. Replaces `/archetype-diff` and `/template-diff`: it auto-detects whether the inputs are **archetypes** (ADL) or **templates** (OET/OPT), and whether the comparison is between two **versions** of the same concept or between **siblings / distinct concepts**, then produces the appropriate report.

## Instructions

1. Parse **$ARGUMENTS** into `<file-a>` and `<file-b>`. If only one argument was given, ask the user for the second and stop.
2. `Read` both files.
3. `Read` the semantic-diff rubric at the **plugin root** — `${CLAUDE_PLUGIN_ROOT}/references/semantic-diff-rubric.md` (Claude Code), or `../references/semantic-diff-rubric.md` from this command, or Glob the installed `references/semantic-diff-rubric.md` (host-agnostic). Follow its classification rules exactly.
4. **Detect the artefact type** from the file content/extension:
   - **Archetype** — ADL source (`.adl`; `archetype (...)` header, `definition`, `term_definitions`). Load the archetype rules guide:
     ```
     guide_get("openehr://guides/archetypes/rules")
     ```
   - **Template** — OET (authoring XML, `<template>`) or OPT (operational, `<template_id>` / flattened `OPERATIONAL_TEMPLATE`). Load the template rules guide:
     ```
     guide_get("openehr://guides/templates/rules")
     ```
   - If the two files are different artefact types (e.g. an ADL vs an OPT), report that mismatch and ask the user to confirm intent before proceeding.
5. **Detect the comparison mode** from the root identifiers:
   - **Version mode** — same root concept / archetype id / template id, differing version (or differing revision of the same concept). Use the version-bump workflow in §A.
   - **Sibling / cross-artefact mode** — **different** root concepts (e.g. `...health_summary` vs `...report`, or two distinct templates). Use the compatibility/divergence workflow in §B. Do **not** refuse, and do **not** emit a version-bump verdict — a bump is meaningless across distinct concepts.
6. Produce the report for the detected mode.

## A. Version mode (same concept, different version)

Compare the two artefacts and classify each change per the rubric (major / minor / patch). Then determine the overall bump: any major change → **major**; else any minor → **minor**; else **patch** (rubric rule **G1**).

**Archetype axes:**
- Root concept id and RM entry type.
- At-codes (ids, terms, definitions): added / removed / repurposed / renamed.
- Cardinality, occurrences, existence at each node.
- Value constraints (data types, ranges, units).
- Terminology bindings — when a binding differs, call `terminology_resolve` on both old and new codes and compare concept definitions to decide equivalence.
- Slot constraints.
- Language-specific terms (track translations separately from semantic changes).

**Template axes:**
- Included archetypes (by id) — added / removed / version-bumped.
- Slot fillers — added / removed / reassigned.
- Narrowing per archetype — compare cardinality, occurrences, existence, value sets, terminology bindings. **Stricter** narrowing = major (breaks composition consumers); **looser** = minor (previously-valid instances stay valid); new optional content = minor.
- RM-level composition category (event / persistent / episodic) — a change here is always major.

Use `type_specification_get` if you need authoritative RM/AM type detail (attributes, allowed structure) to judge a change. Produce the output per the rubric's **Output layout**, adapted for templates with archetype-level grouping where useful.

### Version-mode constraints
- If the two files turn out to have **different** root concepts, do not refuse: emit a one-line note that input concepts differ and you have auto-switched to **sibling mode** (§B), then produce the §B report instead.
- If a **template narrows an archetype beyond what that archetype allows**, flag it as a **validation error** rather than classifying — the template itself is broken.
- OET vs OPT of the *same* template is meaningful but mixes authoring and runtime forms; warn the user that the comparison spans format types.

## B. Sibling / cross-artefact mode (distinct concepts)

The two artefacts are different concepts, so a version bump does not apply. Emit a **compatibility / divergence** report instead (new-feature C1):

1. **Relationship line** — one line classifying the relationship: *same artefact* / *siblings (independent concepts in the same family)* / *one specialises the other* (detect from `specialize`/parent reference in ADL, or shared archetype includes in templates).
2. **Compatibility / divergence report:**
   - **Shared skeleton** — structure/paths (or shared archetype includes) common to both.
   - **Repurposed at-codes** — same at-code id used for a different concept across the two artefacts (a portability hazard).
   - **Additive fields** — paths/at-codes/includes present in one but not the other.
   - **Translation-coverage delta** — per-language `term_definitions` (archetypes) or language metadata (templates) present in one but missing in the other.
3. **Path-compatibility table** — list paths present in **both**, with a per-path verdict:

   | Path | A | B | Verdict |
   |------|---|---|---------|
   | `/data[...]/items[at0004]/value` | DV_QUANTITY {0..1} | DV_QUANTITY {0..1} | compatible |
   | `/...[at0010]/value` | DV_CODED_TEXT | DV_TEXT | type-changed |
   | `/...[at0021]` | present | — | removed |

   Verdicts: **compatible** (same path, type, and compatible constraints) / **type-changed** (path exists in both but RM type or value constraint differs) / **removed** (present in A, absent in B). Use `type_specification_get` to confirm RM-type compatibility where it is not obvious.

### Sibling-mode constraints
- Do **not** emit a patch/minor/major verdict and do **not** reference rule G1 — it is out of scope for distinct concepts.
- If you later determine the two are actually the same concept (e.g. one is a renamed copy), note that and switch to version mode (§A).

## Shared constraints

- This is a **semantic** tool: do **not** perform a git-style line-by-line diff. Line numbers are irrelevant.
- When uncertain whether a terminology binding is non-equivalent, resolve both codes via `terminology_resolve` and compare concept definitions before classifying.
- When uncertain whether a text change alters clinical meaning, quote both versions and flag for human review — do not auto-classify as patch.
- When a version-mode classification is genuinely ambiguous, report the finding under a **Review needed** group with a targeted question instead of guessing.
- To compare against a published revision the user does not have locally, fetch it with `ckm_archetype_get` (archetypes) or `ckm_template_get` (templates), then diff as above.
