---
name: archetype-search
description: Search for archetypes in the openEHR Clinical Knowledge Manager (CKM)
argument-hint: "<search query>"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
---

# /archetype-search

Search for openEHR archetypes in the Clinical Knowledge Manager.

## Instructions

1. Use `ckm_archetype_search` to find archetypes matching: **$ARGUMENTS**
   - Never invent CIDs or archetype IDs
   - If ambiguous, ask 1-2 clarifying questions
2. Present up to 15 candidates as a table with: CID, Archetype ID, RM Type, Version, Status
   - Highlight published vs draft archetypes
3. Ask the user to select a candidate
4. Ask preferred output format: ADL (default), XML, or mindmap
5. Use `ckm_archetype_get` to retrieve the selected archetype in the chosen format
6. Present the content in a code block with a brief explanation:
   - Purpose and clinical concept
   - Use/misuse guidance
   - Key sections and notable constraints
   - Use `guide_adl_idiom_lookup` to explain ADL patterns if needed
