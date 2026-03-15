---
name: aql-designer
description: Explain, design, or review AQL (Archetype Query Language) queries
argument-hint: "<clinical question or AQL query to review>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__type_specification_get
---

# /aql-designer

Explain, design, or review AQL queries.

## Instructions

1. Load the AQL guide for reference:
   ```
   guide_get("aql/principles")
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
- State assumptions about deployed templates/archetypes

### Designing a new AQL query
- Identify which archetypes contain the needed data (use `ckm_archetype_get` to check paths)
- Verify paths against deployed OPT templates using `ckm_template_get`
- Build the containment hierarchy
- Construct appropriate SELECT paths
- Add WHERE conditions and ORDER BY as needed
- Use parameterized queries where appropriate

### Reviewing an AQL query
- Check syntax correctness against the guide
- Verify archetype paths exist (use `ckm_archetype_get`)
- Verify paths against deployed templates (use `ckm_template_get`)
- Suggest optimizations (specific containment, selective paths)
- Run through `guide_get("aql/checklist")`

4. For all tasks:
   - Treat AQL paths as archetype paths; verify against deployed OPT templates
   - State assumptions about deployed templates/archetypes before final output
   - Do not assume engine-specific behavior beyond the AQL specification

## Required Output

1. **Clinical intent** and target deployed templates/archetypes
2. **Containment tree** and constraints
3. **Query or review findings** with path rationale
4. **Parameters and safety notes**
5. **Checklist validation summary** (from `guide_get("aql/checklist")`)
