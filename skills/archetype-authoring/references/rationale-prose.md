# Rationale prose (description / purpose / misuse / use)

Draft CKM-quality rationale prose when the structure is stable but the prose is thin or missing (used late, pre-CKM-submission). Works on a workspace `.adl` or a CKM id (`ckm_archetype_get`).

1. Load `guide_get("archetypes/principles")` and `guide_get("archetypes/language-standards")` for vocabulary.
2. Ground the prose in the bound terminology: resolve **openEHR** codes with `terminology_resolve`; for **SNOMED CT / LOINC / ICD** bindings (which `terminology_resolve` does *not* cover — openEHR terminology only) read the rubric from the archetype's own `term_definitions` / `term_bindings` and do not fabricate an external preferred term.
3. Match prose style to 1–2 published siblings of the same RM entry type (`ckm_archetype_get`); if a specific sibling id is blocked, fall back to any published archetype of that type.
4. Draft each section: **description** (≤2 sentences — what is captured), **purpose** (2–3 sentences — why it exists), **misuse** (what it should NOT be used for, redirecting to siblings), **use** (concrete recording scenarios).

These fields live under `description.details["<lang>"]` in ADL 1.4 (`misuse`/`use` are single newline-joined string values, not bullet arrays) — present a readable sketch but explain how it maps into ADL. Use consistent openEHR vocabulary ("record" not "capture", "clinical statement" not "entry"); keep British English; never invent clinical facts — leave a flagged `TODO: clinical input needed — <question>` where a section can't be grounded.
