---
name: archetype-lint
description: >
  This skill should be used when the user asks to "lint an archetype", "validate an archetype",
  "check archetype compliance", "review archetype quality", or "run archetype rules". Applies
  22 normative lint rules with ERROR/WARNING/INFO severity. Supports STRICT and PERMISSIVE modes.
  Reports violations only — it does not modify files. The `/archetype-lint` command is the quick
  one-shot equivalent on a file path or CKM id.
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Archetype Lint

An openEHR archetype linting engine. Evaluate archetypes against 22 normative rules. Classify each violation as ERROR, WARNING, or INFO. ERROR means the archetype is invalid or unsafe.

## Step 1: Load Guides (MANDATORY)

```
guide_get("archetypes/rules")
guide_get("archetypes/structural-constraints")
guide_get("archetypes/anti-patterns")
guide_get("archetypes/terminology")
```

## Step 2: Determine Mode

- **STRICT**: Zero WARNING tolerance. For publication candidates and CKM submissions.
- **PERMISSIVE** (default): WARNINGs allowed with justification. For early modeling iterations.

If the user does not specify a mode, use PERMISSIVE.

## Step 3: Apply Lint Rules

The **normative rule definitions live in the `archetypes/rules` guide loaded in Step 1** — that guide is the single source of truth. If this index ever disagrees with the loaded guide, the guide wins. Use the index below for rule numbering and severity; consult the guide for each rule's full definition, rationale, and worked examples before classifying a violation.

| # | Rule | Severity | Group |
|---|------|----------|-------|
| 1 | Single Concept | ERROR | Core semantic |
| 2 | ENTRY Type Semantics | ERROR | Core semantic |
| 3 | Root RM Type Match | ERROR | Core semantic |
| 4 | Valid RM Attributes Only | ERROR | Core semantic |
| 5 | occurrences vs cardinality | ERROR | Core semantic |
| 6 | Specialisation Integrity | ERROR | Core semantic |
| 7 | Path Stability | ERROR | Core semantic |
| 8 | Term Definition Completeness | ERROR | Core semantic |
| 9 | Mandatory Data Justification | WARNING | Structural |
| 10 | Arbitrary Upper Bounds | WARNING | Structural |
| 11 | CLUSTER Semantics | WARNING | Structural |
| 12 | Slot Discipline | WARNING | Structural |
| 13 | Template Leakage | WARNING | Structural |
| 14 | Unconstrained Leaf Nodes | WARNING | ADL & AOM syntax |
| 15 | Attribute Multiplicity Compliance | ERROR | ADL & AOM syntax |
| 16 | Ontology Integrity | ERROR | ADL & AOM syntax |
| 17 | Terminology Neutrality | WARNING | Terminology |
| 18 | Semantic Binding Accuracy | WARNING | Terminology |
| 19 | Archetypable Demographics | INFO | Demographic |
| 20 | Identity vs Role Separation | ERROR | Demographic |
| 21 | Patch Version Discipline | ERROR | Versioning |
| 22 | Deprecation Handling | WARNING | Versioning |

For rule 4, verify attribute names against the RM with `type_specification_get` when uncertain.

> Offline fallback only: `skills/openehr-assistant/reference/lint-rules-complete.md` mirrors these definitions for the `clinical-modeler` agent (no MCP access). In the main session, always prefer the loaded `archetypes/rules` guide.

## Step 4: Generate Report

### Required Output Format

```
## Lint Report

**Archetype:** <archetype-id>
**Mode:** STRICT | PERMISSIVE
**Overall Status:** PASS | FAIL

### Violations

| # | Severity | Rule | Explanation | Suggested Fix |
|---|----------|------|-------------|---------------|
| 1 | ERROR    | R4   | Attribute `blood_pressure` is not a valid RM attribute on ITEM_TREE | Use `items` (valid RM path) |

### Summary
- ERRORs: N
- WARNINGs: N
- INFOs: N
```

**Gating logic:**
- Any ERROR -> overall status = FAIL
- STRICT mode: any WARNING -> overall status = FAIL
- PERMISSIVE mode: WARNINGs allowed if justified

## Step 5: Fix Guidance (Optional)

If the user asks for fixes after linting, provide a minimal-diff fix plan:
- For each violation: which rule it resolves, whether it changes paths, whether it affects semantics
- Version bump recommendation (patch/minor/major) with justification
- Prefer template-level constraints over archetype constraints where applicable

Do NOT apply fixes automatically. Present the plan and wait for user approval.
