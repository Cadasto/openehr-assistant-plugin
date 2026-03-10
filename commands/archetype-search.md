---
name: archetype-search
description: Search for archetypes in the openEHR Clinical Knowledge Manager (CKM)
argument-hint: "<search query>"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
---

# /archetype-search

Search for openEHR archetypes in the Clinical Knowledge Manager.

## Instructions

1. Use `ckm_archetype_search` to find archetypes matching: **$ARGUMENTS**
2. Present results as a table with columns: ID, Concept, RM Type, Version, Status
3. If the user asks about a specific archetype from the results, use `ckm_archetype_get` to retrieve its full ADL content
4. Highlight any archetypes that are published vs draft
