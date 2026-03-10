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

1. Use `type_specification_search` with a pattern matching: **$ARGUMENTS**
   - Use `*` wildcards for broad search (e.g., `*ENTRY*`, `DV_*`)
2. Present up to 10 matching types with: name, documentation, component, package
3. If multiple matches, ask the user which type to retrieve
4. Once confirmed, use `type_specification_get` to fetch the full definition
5. Present the type with:
   - Raw BMM JSON definition
   - Explanation for implementers: purpose, key attributes and their types, inheritance hierarchy, constraints/invariants
