# Template from Form (inverse workflow)

Inverse clinical-modelling workflow: start from a form the user wants to implement and work backwards to a template design — the set of archetypes to include and the narrowing to apply per archetype. **Output is a design sketch, not valid OET XML**; turning a confirmed sketch into an OET is Step 8b of the main skill.

## Workflow

1. Interpret the form description as either:
   - A path to a file (`.md`, `.txt`, `.html`) containing the form description — then `Read` it.
   - An inline text description — use directly.
2. Load the CGEM guide — and, if this mode was entered directly without running Step 1 of the main skill, load its mandatory guides too (`templates/principles`, `templates/rules`):
   ```
   guide_get("openehr://guides/templates/cgem-framework")
   ```
3. Parse the form into a structured field list. For each form field, capture: label, data type (free text / coded / quantity / date / boolean), cardinality (single / repeating), mandatoriness. Surface this inventory as a `## Parsed form inventory` section in the output so the user can verify interpretation before committing to a template.
4. **Split the dataset before sketching any template.** A form is a screen, not a composition — classify each field (or field group) into one CGEM category **using the Step 6 table and caveats of the main skill** (already in context; do not restate them from memory), then group same-category fields into candidate compositions. What this mode adds on top of Step 6:
   - a candidate-template mapping per category: Global Background is usually **already modelled** (reuse a published template; often *read-only* on this form); Contextual Situation → one instance per pathway; Event Assessment → prime reuse candidate across forms; Managed Response → a separate order template (INSTRUCTION + ACTION with ISM tracking);
   - report the split as a `## Dataset split (CGEM)` section, stating how many compositions the form implies and which are **written** vs merely **read** (Global Background is frequently read via AQL, not written by the form), plus the three Step 6 caveats;
   - downgrade any field that *looks* like a Managed Response but is really a simple record ("Seen by key worker? Y/N", "Referral date") to a Contextual or Event template, and say so.

   Present CGEM as a design rationale the user can overrule, not a rule.
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
7. For each proposed archetype, identify the at-code path each form field maps to — if it can be inferred from standard CKM archetypes. If not, flag the field as needing design input.

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

- Turn the confirmed sketch into an OET (Step 8b of this skill).
- For gap fields, dispatch `ckm-scout` for deeper reuse search before authoring new archetypes.
```

## Constraints

- Do NOT invent CKM archetype IDs. Only cite archetypes returned by `ckm_archetype_search`.
- Do NOT force a one-form-one-template answer. If the CGEM split says three compositions, sketch the one the user is authoring and name the others with their category and reuse status.
- Do NOT produce OET XML in this mode. The output is a design sketch; emitting the OET is Step 8b, after the user confirms the design.
- The word "composition" in openEHR denotes a runtime data instance (a `COMPOSITION` RM object), not a design-time aggregation of archetypes. This mode's output is a **template** — a design-time constraint set that, once instantiated, will produce compositions.
- If the form is incomplete (missing data types, cardinality, field labels), ask up to 3 clarifying questions before sketching.
