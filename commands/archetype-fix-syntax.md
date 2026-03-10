---
name: archetype-fix-syntax
description: Fix ADL syntax errors in an archetype while preserving its clinical semantics
argument-hint: "<file path or archetype content>"
allowed-tools:
  - Read
  - Edit
  - Write
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
---

# /archetype-fix-syntax

Fix ADL syntax errors while preserving clinical semantics.

## Instructions

1. Load the ADL syntax reference:
   ```
   guide_get("archetypes/adl-syntax")
   guide_get("archetypes/formatting")
   ```
2. Read the archetype content from: **$ARGUMENTS**
   - If a file path is provided, use the Read tool to load it
   - If inline content is provided, analyze it directly
3. Identify syntax issues:
   - Invalid ADL structure (missing sections, malformed blocks)
   - Incorrect constraint syntax (use `guide_adl_idiom_lookup` for correct patterns)
   - Missing or mismatched at-codes
   - Terminology section inconsistencies
   - Invalid RM type references (verify with `type_specification_get`)
4. Fix each issue while preserving:
   - All clinical semantics and intent
   - Existing terminology bindings
   - Archetype path structure
   - Node IDs (at-codes)
5. Use `ckm_archetype_search` and `ckm_archetype_get` to compare patterns with existing CKM archetypes when uncertain
6. If fixing a file, use the Edit tool to apply corrections

## Conflict Resolution

If conflicts arise between syntax and idioms, ADL syntax takes precedence over idioms.

## Prohibited Actions

- Do NOT rename concepts or archetype IDs
- Do NOT add or remove clinical elements
- Do NOT change coded meaning or terminology bindings
- Do NOT alter occurrence/cardinality intent
- Do NOT reorganize tree structure for readability

## Required Output

1. **Corrected ADL** in a code block
2. **Minimal change log**: what was fixed and why (before/after snippets)
3. **Remaining ambiguities**: issues that could not be resolved without semantic decisions
4. **Detected Semantic Issues** (do NOT fix): modeling quality, terminology meaning, scope, over/under-constraint
