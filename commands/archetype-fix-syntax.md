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
5. Present a summary of changes made with before/after snippets
6. If fixing a file, use the Edit tool to apply corrections
