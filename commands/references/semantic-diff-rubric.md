# Semantic Diff Rubric — Archetypes and Templates

Purpose: classify changes between two versions of an archetype or template to recommend the correct version bump (patch / minor / major) per openEHR rule **G1** (semantic or data-invalidating changes → major).

## Classification rules

### Major (semantic or breaking)

- At-code **removed** or **repurposed** (existing code now refers to a different concept).
- RM entry type **changed** (e.g. OBSERVATION → EVALUATION).
- Cardinality **tightened** on an existing field (`min=0` → `min=1`; `max=*` → `max=1`).
- Occurrences **tightened** such that previously-valid instances become invalid.
- Existence **tightened** (`existence matches {0..1}` → `existence matches {1..1}`).
- Terminology binding **replaced** with a non-equivalent coding.
- Slot constraint **tightened** to exclude archetypes that were previously valid.
- Language / name / description changes that alter **clinical meaning** (not translations).

### Minor (additive, non-breaking)

- New at-code **added** as optional field (`min=0`).
- Cardinality **widened** (`min=1` → `min=0`; `max=1` → `max=*`).
- Occurrences **widened**.
- Terminology binding **added** where none existed (opt-in).
- New slot **added** with open constraint.
- New translation added.

### Patch (cosmetic / clarifying)

- Description text changed without altering clinical meaning.
- Typo fixes.
- Formatting / whitespace / comment changes.
- Translation corrections.

## Output layout (for the commands)

```
# <archetype-id or template-id>  <v_old> → <v_new>

## Verdict
- **Recommended bump:** major | minor | patch
- **Rule triggered:** G1 (if major), else N/A

## Changes

### Major changes
- <at0014> removed (was: "diastolic Korotkoff sound")
- <at0003>/value terminology binding changed: SNOMED-CT 8480-6 → LOINC 29463-7 (not semantically equivalent)

### Minor changes
- <at0021> added as optional "cuff calibration date" (DV_DATE, min=0, max=1)

### Patch changes
- description: tense corrected in paragraph 2
```

## Notes for the implementer

- When uncertain whether a binding is "non-equivalent", call `terminology_resolve` on both old and new codes and compare concept definitions.
- When uncertain whether a text change alters clinical meaning, quote both versions and flag the change for human review — do not auto-classify as patch.
- If the files are not the same archetype (different root concept id), refuse the diff and ask the user to confirm intent.
