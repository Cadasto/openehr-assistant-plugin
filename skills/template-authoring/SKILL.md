---
name: template-authoring
description: >
  This skill should be used when the user asks to "create a template", "design a template",
  "constrain archetypes into a template", "review a template", or "work with OET/OPT files".
  Covers creating openEHR templates, constraining archetypes, reviewing designs, and OET/OPT authoring.
  Use `/ckm-search` to find existing CKM templates and `/openehr-explain` to explain one; this
  skill is for authoring and constraining new OET designs.
argument-hint: "<task: create|review> [template-id or use-case]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Template Authoring

## Conflict Resolution

When guides conflict, apply this priority (highest first):
1. Rules and syntax specifications
2. Idioms and structural constraints
3. Principles
4. Convenience

## Step 1: Load Guides (MANDATORY)

Before any template work, load the authoritative guides:

```
guide_get("templates/principles")
guide_get("templates/rules")
```

Load additional guides as needed:
- `guide_get("templates/oet-syntax")` — OET authoring syntax
- `guide_get("templates/oet-idioms-cheatsheet")` — common OET patterns

## Step 2: Research Before Creating

Search for existing templates first:

```
ckm_template_search("<use-case>")
```

If creating a new template, search for archetypes to include:

```
ckm_archetype_search("<concept>")
```

## Step 3: Use-Case Specificity

Templates target particular clinical workflows. Define the use-case clearly:
- What clinical scenario does this template serve? (e.g., discharge summary, vital signs form, medication reconciliation)
- What data points are required vs optional?
- Who will use it? (clinician, nurse, admin)

## Step 4: Archetype Aggregation

### Selecting Archetypes
- Choose archetypes that precisely fit the use-case
- Minimize archetype count — each should serve a clear purpose
- Prefer well-established CKM archetypes over custom ones

### COMPOSITION Structure
Templates are rooted in a COMPOSITION archetype. Nest entry archetypes (OBSERVATION, EVALUATION, INSTRUCTION, ACTION) and CLUSTER archetypes within it.

Use `type_specification_get` to verify COMPOSITION structure when needed.

## Step 5: The Narrowing Principle

Templates constrain archetypes — they NEVER expand:
- **Mandatory stays mandatory**: Cannot make required fields optional
- **Optional can become mandatory**: Can set `min=1` on optional fields
- **Optional can be excluded**: Set `max=0` to hide fields
- **Value sets only narrow**: Can restrict coded text options, never add new ones
- **Cardinality only narrows**: Can reduce max occurrences, never increase beyond archetype definition

## Step 6: CGEM Framework

Use the CGEM framework to guide how clinical data splits across templates:

| Category | Description | Template Scope |
|----------|-------------|---------------|
| **Global Background** | Persistent patient data (allergies, diagnoses, demographics) | Persistent compositions |
| **Contextual Situation** | Episodic context (reason for encounter, admission details) | Episode-level compositions |
| **Event Assessment** | Point-in-time observations and evaluations | Event compositions |
| **Managed Response** | Orders, plans, actions taken | Action/instruction compositions |

## Step 7: Terminology in Templates

- Prefer DV_CODED_TEXT over free text where possible
- Constrain value sets to the local clinical context
- Use `terminology_resolve` to verify terminology bindings inherited from archetypes

## Step 8: OET vs OPT

| Format | Purpose |
|--------|---------|
| **OET** | Authoring format — human-editable XML for template design |
| **OPT** | Operational Template — flattened XML for runtime deployment |
| **ADL-Designer `.t.json`** | ADL-Designer's differential template JSON (tool-generated) |
| **Web Template** | Flattened JSON representation for modern UI development |

For when each format is hand-authorable vs tool-generated and what checksums each carries, load `guide_get("templates/serialization-formats")`. Reference syntax guides:
```
guide_get("templates/oet-syntax")
guide_get("templates/oet-idioms-cheatsheet")
```

## Step 8b: Emit the OET

Produce a real, slot-correct OET — not just a design sketch. (`/template-from-form` produces the sketch; this skill turns a confirmed design into the file.) Following `templates/oet-syntax`:

1. Root `<template>` with a root **COMPOSITION** archetype reference and a fresh `<id>` (see UID note below).
2. A `<Content>` entry per included archetype, nested to mirror the COMPOSITION → SECTION → ENTRY → CLUSTER structure.
3. `<Rule path="…">` elements for each narrowing constraint (`min`/`max`, `limitToList`, unit hardening, `hide_on_form`, label overrides) — respecting the narrowing principle (Step 5).
4. A trailing `<Context>` if the design needs composition context (e.g. `/context/setting` fixed to a code).

There is **no automated OET/OPT validator** available, so validate manually against the loaded `templates/oet-syntax` guide and the Step 9 checklist; state any constraint you could not confirm rather than asserting validity.

## Step 9: Quality Review

Run through the quality checklist:

```
guide_get("templates/checklist")
```

Verify:
- [ ] Clear use-case definition
- [ ] Appropriate archetype selection
- [ ] Narrowing principle respected (no expansions)
- [ ] Required fields marked correctly
- [ ] Excluded fields set to max=0
- [ ] Terminology constraints appropriate for context
- [ ] Value sets verified (quantity constraints, unit hardening, "limit to list" coded text)
- [ ] Annotations and UI hints appropriate (hide_on_form, contextual label overrides)
- [ ] Valid OET syntax

## Output

Generate valid OET files. Use the Write tool to create `.oet` files in the appropriate project location.

### Identifiers and checksums
- A new template needs a fresh `uid` — mint a random UUID (v4). If a shell is available, `uuidgen` (or `python3 -c 'import uuid; print(uuid.uuid4())'`) works; otherwise generate the UUID directly (this skill has no `Bash` tool, so don't assume shell access).
- Do not hand-write build checksums (`MD5-CAM-*`, `build_uid`) — they are tool-computed; a missing/stale checksum is advisory and never blocks authoring the OET.
