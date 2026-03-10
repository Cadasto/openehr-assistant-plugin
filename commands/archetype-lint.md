---
name: archetype-lint
description: Lint an openEHR archetype against 22 normative modeling rules
argument-hint: "<file path or archetype-id> [strict]"
allowed-tools:
  - Read
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# /archetype-lint

Lint an openEHR archetype against 22 normative rules. Returns PASS/FAIL with a violations table.

## Instructions

1. Parse arguments: **$ARGUMENTS**
   - If "strict" is present, use STRICT mode; otherwise PERMISSIVE
   - Remaining argument is a file path or archetype ID
2. Load the archetype:
   - File path -> use Read
   - Archetype ID -> use `ckm_archetype_get`
3. Load the rules reference:
   ```
   guide_get("archetypes/rules")
   guide_get("archetypes/structural-constraints")
   ```
4. Apply all 22 lint rules from the archetype-lint skill
5. Use `type_specification_get` to verify RM attributes when uncertain (rule 4)
6. Return the structured lint report:
   - Archetype ID, mode, overall PASS/FAIL status
   - Violations table: severity, rule number, explanation, suggested fix
   - Summary counts (ERRORs, WARNINGs, INFOs)
