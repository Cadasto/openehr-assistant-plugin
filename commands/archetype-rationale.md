---
name: archetype-rationale
description: Generate CKM-quality rationale prose (description, purpose, misuse, use) for an openEHR archetype.
argument-hint: "<file or CKM id> [--section=description|purpose|misuse|use|all]"
allowed-tools:
  - Read
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__terminology_resolve
---

# /archetype-rationale

Draft CKM-quality rationale prose for an archetype's description, purpose, misuse, and use sections. Used late in the archetype lifecycle (pre-CKM-submission) when the structure is stable and prose is thin or missing.

## Instructions

1. Parse **$ARGUMENTS** into `<target>` and optional `--section=...` (default `all`).
2. Load the archetype:
   - If `<target>` is a file path → `Read` it.
   - If `<target>` is a CKM id (e.g. `openEHR-EHR-OBSERVATION.blood_pressure.v2`) → `ckm_archetype_get("<target>")`.
3. Load the authoring and language guides:
   ```
   guide_get("archetypes/principles")
   guide_get("archetypes/language-standards")
   ```
4. For at least two terminology codes bound in the archetype, call `terminology_resolve` to ground the prose in accurate clinical meaning.
5. Inspect 1–2 sibling CKM archetypes of the same RM entry type to match prose style:
   ```
   ckm_archetype_get("openEHR-EHR-OBSERVATION.blood_pressure.v2")   # example sibling
   ```
6. Draft each requested section (or all four):
   - **description** (≤2 sentences): what clinical phenomenon is captured.
   - **purpose** (2–3 sentences): why it exists; intended record.
   - **misuse** (bulleted list): what this archetype should NOT be used for. Reference sibling archetypes for redirection.
   - **use** (bulleted list): concrete recording scenarios.
7. Present output in this exact layout so the user can copy-paste into ADL:

```
description:
  <generated text>

purpose:
  <generated text>

misuse:
  - <generated bullet>
  - <generated bullet>

use:
  - <generated bullet>
  - <generated bullet>
```

This layout is a **logical sketch for readability**, not valid ADL syntax. In ADL 1.4, these fields live under `description.details["<lang>"]` as multi-line string values (`misuse` and `use` are single string fields, not bullet arrays). When pasting into an archetype, join the bullets into newline-separated prose and wrap each section as an ADL string literal. Point this out to the user in your response.

## Quality standards

- Use consistent openEHR vocabulary (see `guide_get("archetypes/language-standards")`) — prefer "record" over "capture", "clinical statement" over "entry", etc.
- Do NOT invent clinical facts. If a section cannot be grounded in the archetype's own structure or terminology bindings, leave a clearly-flagged `TODO: clinical input needed — <specific question>` placeholder.
- Keep British English consistent with CKM's editorial style.
- No marketing language, no adjectives without clinical justification.
