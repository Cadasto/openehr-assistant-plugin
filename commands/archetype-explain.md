---
name: archetype-explain
description: Explain the semantics, structure, and constraints of an openEHR archetype
argument-hint: "<archetype-id, CKM search terms, or file path>"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# /archetype-explain

Explain the semantics, structure, and constraints of an openEHR archetype without suggesting modifications.

## Instructions

1. Load archetype guides for context:
   ```
   guide_get("archetypes/principles")
   guide_get("archetypes/structural-constraints")
   guide_get("archetypes/terminology")
   ```
2. Retrieve the archetype: **$ARGUMENTS**
   - If an archetype ID is provided, use `ckm_archetype_get` directly
   - If search terms are provided, use `ckm_archetype_search` first, present candidates, and ask the user to select
3. Use `type_specification_get` to clarify RM types used in the archetype
4. Use `ckm_archetype_search` to discover related archetypes referenced in slots

## Prohibited Actions

- Do NOT suggest improvements or corrections
- Do NOT assume template or UI behavior
- Do NOT introduce new clinical concepts not present in the archetype

## Required Output

1. **High-Level Clinical Meaning**: What the archetype represents, typical use, what it does NOT represent
2. **Core Data Semantics**: Main data elements; mandatory vs optional; repeating vs single-instance
3. **Terminology Semantics**: Coded elements, value sets, bindings and their intent
4. **Structural Semantics**: Clusters/slots/repetitions rationale; protocol/state sections; implicit assumptions
5. **Semantic Boundaries & Assumptions**: Scope boundaries, ambiguities, decisions deferred to templates
6. **Summary**: One paragraph suitable for documentation
