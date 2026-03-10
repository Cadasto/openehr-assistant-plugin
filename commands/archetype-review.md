---
name: archetype-review
description: Multi-stage archetype review pipeline - intent analysis, lint, fix plan, patch, re-lint, and review packet
argument-hint: "<file path or archetype-id> [strict]"
allowed-tools:
  - Read
  - Edit
  - Write
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# /archetype-review

Full multi-stage review pipeline for an openEHR archetype. Progresses through intent analysis, linting, fix planning, patching, re-linting, and optional CKM review packet generation.

## Instructions

Parse arguments: **$ARGUMENTS**
- If "strict" is present, use STRICT mode; otherwise PERMISSIVE
- Remaining argument is a file path or archetype ID

Load the archetype (Read for files, `ckm_archetype_get` for IDs).

### Stage 1: Intent & Scope Analysis

Analyse the archetype for intent and scope ONLY. Do NOT lint yet. Do NOT propose edits.

Output:
1. **Concept statement** (1-3 sentences)
2. **Candidate ENTRY type** with reasoning
3. **Scope boundaries** (inclusions/exclusions)
4. **CKM reuse notes** — use `ckm_archetype_search` to find overlapping archetypes
5. **Must-not-change list**: paths, node identifiers, semantic meaning anchors

### Stage 2: Strict Lint Pass

Apply all 22 lint rules (see archetype-lint skill). Load guides:
```
guide_get("archetypes/rules")
guide_get("archetypes/structural-constraints")
guide_get("archetypes/anti-patterns")
```

Use `type_specification_get` to verify RM attributes (rule 4).

Output: PASS/FAIL + violations table (severity, rule, explanation, suggested fix).

**If PASS** -> skip to Stage 6.
**If FAIL** -> proceed to Stage 3.

### Stage 3: Fix Plan

Create a minimal-diff fix plan to resolve all ERRORs (and WARNINGs in STRICT mode).

Constraints:
- Preserve paths and at-codes unless MAJOR version bump is explicitly allowed
- Do not invent RM attributes
- Prefer template-level constraints over archetype constraints

Output:
- Ordered fix list with mapping to rule violations
- For each fix: whether it changes paths, whether it affects semantics
- Version bump recommendation (patch/minor/major) with justification

**Present the fix plan and WAIT for user approval before proceeding.**

### Stage 4: Patch Application

Apply the approved fix plan. Output:
1. **Revised archetype** (full ADL)
2. **Diff summary**: nodes added/removed, constraints changed, terminology changes, version changes

Constraints: preserve identifiers, preserve structure unless required for validity.

### Stage 5: Re-Lint

Re-lint the revised archetype using the same rules and mode.
- If PASS -> proceed to Stage 6
- If FAIL -> return to Stage 3 with remaining violations (max 3 iterations)

### Stage 6: Review Packet (Optional)

If the user wants a CKM-style review, generate:
1. **Purpose / Use / Misuse** text suggestions
2. **Rationale** for key modeling decisions
3. **Unresolved warnings** with justifications
4. **Questions for clinicians** (if ambiguity exists)
5. **Versioning justification**
