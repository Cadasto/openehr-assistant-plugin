---
name: terminology
description: Resolve openEHR terminology IDs, codes, and rubrics
argument-hint: "<terminology code, rubric, or description>"
allowed-tools:
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__guide_get
---

# /terminology

Resolve openEHR terminology identifiers and coded values.

## Instructions

1. Load terminology context: `guide_get("archetypes/terminology")`
2. Use `terminology_resolve` to look up: **$ARGUMENTS**
3. Distinguish between:
   - **Terminology groups**: collections of concept-rubric pairs identified by openEHR groupId
   - **Codesets**: standardized enumerations used in openEHR models
4. Present resolved terminology with:
   - Code string
   - Rubric/display text
   - Terminology ID (e.g., openehr, SNOMED-CT, LOINC)
   - Any related codes or value sets
5. Explain whether result is a group or codeset, its purpose in openEHR, and clinical usage context
