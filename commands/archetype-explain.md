---
name: archetype-explain
description: Explain the semantics, structure, and constraints of an openEHR archetype
argument-hint: "<archetype-id, e.g., openEHR-EHR-OBSERVATION.blood_pressure.v2>"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# /archetype-explain

Explain the semantics, structure, and constraints of an openEHR archetype.

## Instructions

1. Use `ckm_archetype_get` to retrieve the archetype: **$ARGUMENTS**
2. Load relevant guides for context:
   - `guide_get("archetypes/principles")` for design rationale
   - `guide_get("archetypes/structural-constraints")` if constraint questions arise
3. Use `type_specification_get` to clarify RM types used in the archetype
4. Present a structured explanation:
   - **Purpose**: What clinical concept this archetype represents
   - **RM Type**: Entry type and why it was chosen
   - **Structure**: Data tree with key elements explained
   - **Constraints**: Notable cardinality, occurrences, value set restrictions
   - **Terminology**: Defined terms and any external bindings
   - **Slots**: What other archetypes can be nested
   - **Usage**: Common clinical scenarios where this archetype is used
