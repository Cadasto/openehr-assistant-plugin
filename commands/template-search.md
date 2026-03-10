---
name: template-search
description: Search for templates in the openEHR Clinical Knowledge Manager (CKM)
argument-hint: "<search query>"
allowed-tools:
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__ckm_archetype_get
---

# /template-search

Search for openEHR templates in the Clinical Knowledge Manager.

## Instructions

1. Use `ckm_template_search` to find templates matching: **$ARGUMENTS**
   - Never invent CIDs or template metadata
   - If ambiguous, ask 1-2 clarifying questions
2. Present up to 15 candidates as a table with: CID, Display Name, Status
3. Ask the user to select a candidate
4. Ask preferred format: OET (design-time, default) or OPT (operational with flattened constraints)
5. Use `ckm_template_get` to retrieve the selected template
6. If format is OET and archetypes are referenced, use `ckm_archetype_get` to retrieve them for context
7. Present the template in a code block with a brief explanation:
   - Design intent and clinical context
   - Archetypes used and their roles
   - Notable constraints and narrowing decisions
