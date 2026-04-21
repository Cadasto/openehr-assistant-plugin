---
name: template-diff
description: Semantic diff between two openEHR templates (OET or OPT) — reports archetype includes added/removed, narrowing constraints changed, terminology bindings changed, and classifies the overall version bump (patch / minor / major).
argument-hint: "<file-a.oet|opt> <file-b.oet|opt>"
allowed-tools:
  - Read
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__guide_get
---

# /template-diff

Compare two versions of an openEHR template at the semantic level. Identifies whether archetype usage changed, whether narrowing became stricter or looser, and classifies the resulting version bump.

## Instructions

1. Parse **$ARGUMENTS** into `<file-a>` (old) and `<file-b>` (new).
2. `Read` both files.
3. `Read` the rubric: `commands/references/semantic-diff-rubric.md`.
4. Load the template rules guide:
   ```
   guide_get("templates/rules")
   ```
5. Compare along these axes:
   - Included archetypes (by id) — added / removed / version-bumped
   - Slot fillers — added / removed / reassigned
   - Narrowing: per archetype, compare constraints on cardinality, occurrences, existence, value sets, terminology bindings.
   - RM-level composition category (event / persistent / episodic) — a change here is always major.
6. Apply the rubric:
   - Stricter narrowing = major (breaking change for composition consumers).
   - Looser narrowing = minor (previously-valid instances remain valid).
   - New optional content = minor.
   - Description / cosmetic = patch.
7. Produce output per the rubric's layout, adapted for templates (include archetype-level grouping).

## Constraints

- If the two files are different templates (different template id), refuse and ask the user to confirm intent.
- When the template narrows an archetype beyond what that archetype allows, flag as **validation error** rather than classifying — the template itself is broken.
- OET vs OPT: a diff across format types (e.g. `.oet` vs `.opt`) is meaningful only if both represent the same template. Warn the user.
