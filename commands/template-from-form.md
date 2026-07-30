---
name: template-from-form
description: Given a clinical form description (text or file), split it across compositions with the CGEM framework (Global Background / Contextual Situation / Event Assessment / Managed Response → persistent / episodic / event), then sketch each template — the archetypes to aggregate, the RM entry type per field group, and narrowing notes per archetype. Output is a design sketch, not valid OET XML.
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
   guide_get("openehr://guides/templates/principles")
   guide_get("openehr://guides/templates/rules")
   guide_get("openehr://guides/templates/cgem-framework")
   ```
3. Parse the form into a structured field list. For each form field, capture: label, data type (free text / coded / quantity / date / boolean), cardinality (single / repeating), mandatoriness. Surface this inventory as a `## Parsed form inventory` section in your output so the user can verify interpretation before committing to a template.
4. **Split the dataset before sketching any template.** A form is a screen, not a composition — classify each field (or field group) into one CGEM category, then group same-category fields into candidate compositions. Report this as a `## Dataset split (CGEM)` section:

   | CGEM category | Data nature | `COMPOSITION.category` | Candidate template |
   |---|---|---|---|
   | **Global Background** | true for life, one current version updated in place | `persistent` (431) | usually **already modelled** — reuse a published template; often *read-only* on this form |
   | **Contextual Situation** | single source of truth for one journey / episode / condition | `episodic` (451) | one instance per pathway |
   | **Event Assessment** | discrete repeated recording, each submission a new record | `event` (433) | prime reuse candidate across forms |
   | **Managed Response** | genuine order/fulfilment cycle tracked to completion | **no category code** — usually `event` | INSTRUCTION + ACTION with ISM tracking |

   Then state, in the output:
   - how many compositions the form implies, and which are **written** vs merely **read** (Global Background is frequently read via AQL, not written by the form);
   - that four CGEM categories map onto **three** category codes — Managed Response is distinguished by INSTRUCTION/ACTION + the ISM, not by its category;
   - a caveat where a split depends on `451 episodic`, which is normative but unevenly implemented (`persistent` plus governance conventions is the common fallback);
   - any field that *looks* like a Managed Response but is really a simple record ("Seen by key worker? Y/N", "Referral date") — downgrade it to a Contextual or Event template and say so.

   CGEM is freshEHR's analysis method, not an openEHR specification — present it as a design rationale the user can overrule, not a rule.
5. For each field group (a cluster of related fields, e.g. vital signs together), decide the target RM entry type using this mapping:

| Form field group resembles… | RM entry type |
|---|---|
| Measured/observed data with time | OBSERVATION |
| Assessed/interpreted data (diagnosis, problem) | EVALUATION |
| Order, request, plan | INSTRUCTION |
| Activity performed | ACTION |
| Administrative (admission, demographics) | ADMIN_ENTRY |
| Reusable sub-structure | CLUSTER |

6. For each group, search CKM:
   ```
   ckm_archetype_search("<field-group concept>")
   ```
   and, if a matching existing template may exist:
   ```
   ckm_template_search("<form purpose>")
   ```
7. For each proposed archetype, identify the at-code path each form field maps to — if you can infer it from standard CKM archetypes. If not, flag the field as needing design input.

## Output format

```
# Template sketch — <form name>

## Dataset split (CGEM)

| Field / group | CGEM category | `COMPOSITION.category` | Written or read | Target template |
|---|---|---|---|---|
| Allergies list | Global Background | `persistent` (431) | read | existing published allergies template |
| Vital signs block | Event Assessment | `event` (433) | written | `<suggested_template_id>` (sketched below) |
| Referral request | Managed Response | `event` — INSTRUCTION/ACTION + ISM | written | separate order template |

<one paragraph: how many compositions this form implies, which are read vs written, and any episodic-support caveat>

## Proposed template(s)

- **Name**: <suggested_template_id>
- **RM root**: COMPOSITION (category: event | persistent | episodic — justified from the CGEM split above)

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
- Do NOT force a one-form-one-template answer. If the CGEM split says three compositions, sketch the one the user is authoring and name the others with their category and reuse status.
- Do NOT produce OET XML. This command outputs a design sketch; OET authoring is the `template-authoring` skill's job.
- The word "composition" in openEHR denotes a runtime data instance (a `COMPOSITION` RM object), not a design-time aggregation of archetypes. This command's output is a **template** — a design-time constraint set that, once instantiated, will produce compositions.
- If the form is incomplete (missing data types, cardinality, field labels), ask up to 3 clarifying questions before sketching.
