---
name: archetype-impact
description: Scan the current workspace for all references to a given archetype across templates (.oet / .opt) and AQL files, producing an impact table useful before editing a widely-reused archetype.
argument-hint: "<archetype-id, e.g. openEHR-EHR-OBSERVATION.blood_pressure.v2>"
allowed-tools:
  - Glob
  - Grep
  - Read
  - mcp__openehr-assistant__ckm_archetype_get
---

# /archetype-impact

Compute the impact of editing a given archetype by finding every workspace artefact that references it — templates that include it, AQL queries that path into it, and any other place the archetype id or its at-codes appear.

## Instructions

1. Extract `<archetype-id>` from **$ARGUMENTS**. Validate it matches the pattern `openEHR-<DOMAIN>-<RM_TYPE>.<concept>.v<N>`.
2. Glob the workspace for candidate files:
   ```
   Glob: **/*.oet
   Glob: **/*.opt
   Glob: **/*.aql
   Glob: **/*.sql
   Glob: **/*.md
   ```
   (`.md` catches AQL examples and documentation that may reference the archetype.)
3. For each file, grep for the archetype id:
   ```
   Grep: pattern="<archetype-id>", path=<file>
   ```
4. For templates (`.oet`/`.opt`) that mention the archetype, also inspect whether it's:
   - a top-level included archetype (in `<Items>`),
   - nested as a slot filler (in `<Rule ... archetypeId>`),
   - referenced only as documentation text.
5. For AQL/SQL/md files, extract the full line(s) containing the reference so the user can see the containment and predicate context.
6. Optionally call `ckm_archetype_get("<archetype-id>")` once to resolve the concept name and report it alongside the impact table for clarity.

## Output format

```
# Impact Analysis — <archetype-id>

**Concept:** <resolved concept name from CKM>

## Summary

- Templates referencing: <N>
- AQL queries referencing: <M>
- Documentation / misc: <K>

## Templates

| File | Reference type | Line |
|---|---|---|
| `templates/antenatal.oet` | Top-level include | L42 |
| `templates/vitals.oet` | Slot filler under `openEHR-EHR-COMPOSITION.encounter.v1` | L118 |

## AQL queries

| File | Line | Excerpt |
|---|---|---|
| `queries/cohort.aql` | L17 | `CONTAINS OBSERVATION o[openEHR-EHR-OBSERVATION.blood_pressure.v2]` |

## Documentation / misc

| File | Line | Context |
|---|---|---|
| `docs/design.md` | L83 | Mention in design rationale |

## Recommendation

- If editing: review each consumer for compatibility. AQL paths that target narrowed fields may break if at-codes change.
- If not editing (exploration): no action.
```

## Notes

- This command is local-only. It does NOT query CKM for downstream users (that would require CKM-wide search out of scope here).
- If the workspace has no matches, report that clearly rather than producing an empty table.
