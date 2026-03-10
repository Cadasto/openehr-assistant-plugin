---
name: template-search
description: Search for templates in the openEHR Clinical Knowledge Manager (CKM)
argument-hint: "<search query>"
allowed-tools:
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
---

# /template-search

Search for openEHR templates in the Clinical Knowledge Manager.

## Instructions

1. Use `ckm_template_search` to find templates matching: **$ARGUMENTS**
2. Present results as a table with columns: ID, Name, Status
3. If the user asks about a specific template from the results, use `ckm_template_get` to retrieve its full content
