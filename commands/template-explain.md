---
name: template-explain
description: Explain the semantics, structure, and constraints of an openEHR template
argument-hint: "<template-id or CKM search terms>"
allowed-tools:
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# /template-explain

Explain the semantics, structure, and constraints of an openEHR template without suggesting modifications.

## Instructions

1. Load template guides for context:
   ```
   guide_get("templates/principles")
   guide_get("templates/rules")
   ```
2. Retrieve the template: **$ARGUMENTS**
   - If a template ID or CKM CID is provided, use `ckm_template_get` directly
   - If search terms are provided, use `ckm_template_search` first, present candidates, and ask the user to select
   - Ask preferred format before retrieval: OET (design-time, default) or OPT (operational)
3. When the template references archetypes, use `ckm_archetype_get` to retrieve them for deeper explanation
4. Use `type_specification_get` to clarify RM types when needed

## Prohibited Actions

- Do NOT suggest improvements or corrections
- Do NOT assume template or UI behavior beyond what is explicitly constrained
- Do NOT introduce new clinical concepts not present in the template

## Required Output

1. **Use Case & Context**: Clinical scenario this template supports; main purpose; intended users
2. **Composition Structure**: Root archetype overview; brief rationale for each included archetype
3. **Narrowing & Constraints**: Key exclusions (max=0), required element escalations (min=1), reduced value sets vs base archetypes
4. **Data & Terminology Semantics**: Meaning of coded items, units, clinical ranges
5. **UI & Implementation Hints**: Relevant annotations, labels, presentation constraints (hide_on_form, etc.)
6. **Summary**: One implementation-ready paragraph suitable for documentation; note dependency on target OPT
