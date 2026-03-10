---
name: terminology
description: Resolve openEHR terminology IDs, codes, and rubrics
argument-hint: "<terminology code, rubric, or description>"
allowed-tools:
  - mcp__openehr-assistant__terminology_resolve
---

# /terminology

Resolve openEHR terminology identifiers and coded values.

## Instructions

1. Use `terminology_resolve` to look up: **$ARGUMENTS**
2. Present the resolved terminology with:
   - Code string
   - Rubric/display text
   - Terminology ID (e.g., openehr, SNOMED-CT, LOINC)
   - Any related codes or value sets
3. Explain the clinical meaning and typical usage context
