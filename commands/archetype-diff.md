---
name: archetype-diff
description: Semantic diff between two openEHR archetype versions — reports added/removed at-codes, cardinality changes, terminology binding changes, and classifies the overall version bump (patch / minor / major) per rule G1.
argument-hint: "<file-a.adl> <file-b.adl>"
allowed-tools:
  - Read
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__guide_get
---

# /archetype-diff

Compare two versions of an openEHR archetype at the semantic level — not textual. Useful before releasing a new version to decide whether the bump is patch, minor, or major.

## Instructions

1. Parse **$ARGUMENTS** into `<file-a>` (old) and `<file-b>` (new). If the user provided only one argument, ask for the second.
2. `Read` both files.
3. `Read` the semantic-diff rubric: `commands/references/semantic-diff-rubric.md`. Follow its classification rules exactly.
4. Load the rules guide for authoritative reference:
   ```
   guide_get("archetypes/rules")
   ```
5. Compare the two ADL files along these axes:
   - Root concept id and RM entry type
   - At-codes (ids, terms, definitions): added / removed / repurposed / renamed
   - Cardinality, occurrences, existence at each node
   - Value constraints (data types, ranges, units)
   - Terminology bindings (call `terminology_resolve` on both old and new codes where they differ)
   - Slot constraints
   - Language-specific terms (track translations separately from semantic changes)
6. Classify each change per the rubric (major / minor / patch).
7. Determine the overall version bump: any major change → major; else any minor → minor; else patch.
8. Produce the output per the rubric's output layout.

## Constraints

- If the two files are different archetypes (different root concept), refuse and ask the user to confirm intent.
- Do NOT perform git-style line-by-line diff. This is a semantic tool. Line numbers are irrelevant.
- When classification is genuinely ambiguous, report the finding under a **Review needed** group with a targeted question for the user instead of guessing.
