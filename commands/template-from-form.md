---
name: template-from-form
description: Given a clinical form description (text or file), suggest a template sketch — the archetypes to aggregate, the RM entry type per field group, and narrowing notes per archetype. Output is a design sketch, not valid OET XML.
argument-hint: "<form description text OR path to form description file>"
allowed-tools:
  - Read
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__guide_get
---

# /template-from-form

Inverse clinical-modelling workflow: start from a form the user wants to implement and work backwards to a template design — the set of archetypes to include and the narrowing to apply per archetype.

## Instructions

1. Interpret **$ARGUMENTS** as either:
   - A path to a file (`.md`, `.txt`, `.html`) containing the form description — then `Read` it.
   - An inline text description — use directly.
2. Load the template-authoring and CGEM guides:
   ```
   guide_get("templates/principles")
   guide_get("templates/rules")
   ```
3. Parse the form into a structured field list. For each form field, capture: label, data type (free text / coded / quantity / date / boolean), cardinality (single / repeating), mandatoriness. Surface this inventory as a `## Parsed form inventory` section in your output so the user can verify interpretation before committing to a template.
4. For each field group (a cluster of related fields, e.g. vital signs together), decide the target RM entry type using this mapping:

| Form field group resembles… | RM entry type |
|---|---|
| Measured/observed data with time | OBSERVATION |
| Assessed/interpreted data (diagnosis, problem) | EVALUATION |
| Order, request, plan | INSTRUCTION |
| Activity performed | ACTION |
| Administrative (admission, demographics) | ADMIN_ENTRY |
| Reusable sub-structure | CLUSTER |

5. For each group, search CKM:
   ```
   ckm_archetype_search("<field-group concept>")
   ```
   and, if a matching existing template may exist:
   ```
   ckm_template_search("<form purpose>")
   ```
6. For each proposed archetype, identify the at-code path each form field maps to — if you can infer it from standard CKM archetypes. If not, flag the field as needing design input.

## Output format

```
# Template sketch — <form name>

## Proposed template

- **Name**: <suggested_template_id>
- **RM root**: COMPOSITION (category: event | persistent | episodic — justified)

## Archetypes to aggregate

### 1. <openEHR-EHR-OBSERVATION.vital_signs.v1> (existing CKM)
Maps these form fields:
- "Blood pressure (systolic)" → `/data/events/data/items[at0004]/value` (DV_QUANTITY mmHg)
- "Blood pressure (diastolic)" → `/data/events/data/items[at0005]/value` (DV_QUANTITY mmHg)

**Narrowing in template:**
- Make `position` mandatory
- Restrict `method` to oscillometric | auscultation

### 2. <openEHR-EHR-EVALUATION.problem_diagnosis.v1> (existing CKM)
Maps:
- "Primary diagnosis" → `/data/items[at0002]/value`

**Narrowing in template:**
- Bind `diagnosis_name` to SNOMED-CT finding value-set.

## Fields requiring design input

- "Trial cohort code" — no matching CKM archetype. Propose CLUSTER archetype specific to this study, or leave as ADMIN_ENTRY note.

## Next steps

- Refine the template with the `template-authoring` skill.
- For gap fields, dispatch `ckm-scout` for deeper reuse search before authoring new archetypes.
```

## Constraints

- Do NOT invent CKM archetype IDs. Only cite archetypes returned by `ckm_archetype_search`.
- Do NOT produce OET XML. This command outputs a design sketch; OET authoring is the `template-authoring` skill's job.
- The word "composition" in openEHR denotes a runtime data instance (a `COMPOSITION` RM object), not a design-time aggregation of archetypes. This command's output is a **template** — a design-time constraint set that, once instantiated, will produce compositions.
- If the form is incomplete (missing data types, cardinality, field labels), ask up to 3 clarifying questions before sketching.
