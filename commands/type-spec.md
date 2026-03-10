---
name: type-spec
description: Look up openEHR Reference Model, Archetype Model, and BASE type specifications
argument-hint: "<type name, e.g., DV_QUANTITY, OBSERVATION, COMPOSITION>"
allowed-tools:
  - mcp__openehr-assistant__type_specification_search
  - mcp__openehr-assistant__type_specification_get
---

# /type-spec

Look up openEHR RM/AM/BASE type specifications.

## Instructions

1. Use `type_specification_search` to find types matching: **$ARGUMENTS**
2. Present matching types with their package and description
3. Use `type_specification_get` to retrieve the full specification of the most relevant type
4. Present the type with:
   - Attributes and their types
   - Inheritance hierarchy
   - Constraints and invariants
   - Usage examples where helpful
