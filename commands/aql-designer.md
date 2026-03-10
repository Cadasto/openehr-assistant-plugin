---
name: aql-designer
description: Explain, design, or review AQL (Archetype Query Language) queries
argument-hint: "<clinical question or AQL query to review>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_get
---

# /aql-designer

Explain, design, or review AQL queries.

## Instructions

1. Load the AQL guide for reference:
   ```
   guide_get("aql/syntax")
   guide_get("aql/idioms-cheatsheet")
   ```
2. Analyze the user's request: **$ARGUMENTS**
3. Depending on the task:

### Explaining an AQL query
- Break down each clause (SELECT, FROM, WHERE, ORDER BY)
- Explain the containment hierarchy and archetype references
- Describe what clinical data the query retrieves
- Note any parameters and their expected values

### Designing a new AQL query
- Identify which archetypes contain the needed data (use `ckm_archetype_get` to check paths)
- Build the containment hierarchy
- Construct appropriate SELECT paths
- Add WHERE conditions and ORDER BY as needed
- Use parameterized queries where appropriate

### Reviewing an AQL query
- Check syntax correctness against the guide
- Verify archetype paths exist (use `ckm_archetype_get`)
- Suggest optimizations (specific containment, selective paths)
- Run through `guide_get("aql/checklist")`
