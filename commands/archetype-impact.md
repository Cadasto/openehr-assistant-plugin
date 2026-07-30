---
name: archetype-impact
description: Scan the current workspace for all references to a given archetype across templates (.oet / .t.json source, .opt compiled) and AQL files, producing an impact table useful before editing a widely-reused archetype.
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
   Glob: **/*.t.json
   Glob: **/*.adl
   Glob: **/*.aql
   Glob: **/*.sql
   Glob: **/*.md
   ```
   (`.t.json` catches Archetype Designer **source** templates — AOM2 differential JSON with `templateOverlays`, *not* web templates; `.adl` catches **parent archetypes** that slot this one in via `allow_archetype`/`include`; `.md` catches AQL examples and documentation. A **web template** is derived runtime JSON with no extension convention — if the workspace holds one, the reference is generated, not authored, so treat it as downstream of its OPT.)
3. For each file, grep for the archetype id:
   ```
   Grep: pattern="<archetype-id>", path=<file>
   ```
4. For templates (`.oet`/`.opt`/`.t.json`) that mention the archetype, also inspect whether it's:
   - a top-level included archetype (in `<Items>` / the template's content tree),
   - nested as a slot filler (in `<Rule ... archetypeId>` or a JSON slot reference),
   - in a `.t.json`, carried as a `templateOverlays` entry (the differential overlay for that archetype) or named by `parentArchetypeId`,
   - referenced only as documentation text.
   Distinguish **source** templates (`.oet`, `.t.json` — where an edit propagates on the next compile) from **compiled** ones (`.opt` — where the reference is inlined and stale until regenerated); the recommendation differs.
5. For other archetypes (`.adl`), check whether they reference this archetype as a **slot constraint** — grep for the id inside `allow_archetype` / `include` blocks; if found, the other archetype is a *parent* whose slot this one fills.
6. For AQL/SQL/md files, extract the full line(s) containing the reference so the user can see the containment and predicate context.
7. Optionally call `ckm_archetype_get("<archetype-id>")` once to resolve the concept name and report it alongside the impact table for clarity.

## Output format

```
# Impact Analysis — <archetype-id>

**Concept:** <resolved concept name from CKM>

## Summary

- Source templates referencing (`.oet`, `.t.json`): <N>
- Compiled/operational templates referencing (`.opt`): <O>
- Parent archetypes (slot constraints): <P>
- AQL queries referencing: <M>
- Documentation / misc: <K>

## Templates

| File | Reference type | Line |
|---|---|---|
| `templates/antenatal.oet` | Top-level include | L42 |
| `templates/vitals.oet` | Slot filler under `openEHR-EHR-COMPOSITION.encounter.v1` | L118 |
| `Health Certificate.t.json` | `templateOverlays` entry (AD source template) | L210 |
| `templates/vitals.opt` | Inlined constraint (compiled — regenerate after the edit) | L2041 |

## Parent archetypes (slot constraints)

| File | Slot | Line |
|---|---|---|
| `openEHR-EHR-COMPOSITION.report.v1.adl` | `allow_archetype … include` | L394 |

## AQL queries

| File | Line | Excerpt |
|---|---|---|
| `queries/cohort.aql` | L17 | `CONTAINS OBSERVATION o[openEHR-EHR-OBSERVATION.blood_pressure.v2]` |

## Documentation / misc

| File | Line | Context |
|---|---|---|
| `docs/design.md` | L83 | Mention in design rationale |

## Recommendation

- If editing: review each consumer for compatibility. AQL paths that target narrowed fields may break if at-codes change. Source templates (`.oet`, `.t.json`) pick the change up on the next compile; every `.opt` listed must be **regenerated**, and any web template derived from it re-fetched.
- If not editing (exploration): no action.
```

## Notes

- This command is local-only. It does NOT query CKM for downstream users (that would require CKM-wide search out of scope here).
- If the workspace has no matches, report that clearly rather than producing an empty table.
