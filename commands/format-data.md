---
name: format-data
description: Explain or design openEHR data instances (FLAT/STRUCTURED/CANONICAL formats) based on a given template
argument-hint: "<template-id or format question>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__type_specification_get
---

# /format-data

Explain or design openEHR simplified format instances.

## Instructions

1. Load the simplified formats guide:
   ```
   guide_get("simplified_formats/principles")
   guide_get("simplified_formats/idioms-cheatsheet")
   ```
2. Analyze the user's request: **$ARGUMENTS**
3. If a template is referenced, load it:
   ```
   ckm_template_get("<template-id>")
   ```
4. Depending on the task:

### Explaining a format
- Identify the format type (FLAT, STRUCTURED, or CANONICAL)
- Explain the path structure and value encoding
- Map paths back to archetype elements
- Clarify data type representations

### Designing a format instance
- Load the target template to understand structure
- Generate the format instance with correct paths and values
- Include composition metadata (composer, language, territory, context)
- Use `type_specification_get` to verify RM data type encoding
- Validate required fields and cardinality constraints

### Converting between formats
- Explain the mapping between format representations
- Show equivalent structures in both source and target formats
