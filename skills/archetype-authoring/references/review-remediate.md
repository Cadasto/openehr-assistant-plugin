# Review & Remediate pipeline

Full review pipeline for an archetype (absorbs the former `/archetype-review` command). Load this when reviewing for quality, publication, or CKM submission. For a quick lint with no remediation, use the `archetype-lint` skill (`/archetype-lint`).

## 1. Intent & provenance
- State the concept, the candidate ENTRY type, scope boundaries, and a **must-not-change list** (paths, at-codes, semantic anchors).
- **Provenance check (advisory):** decide whether the file is a mirror of a published CKM archetype (matching id/revision). If so, note that editing it locally diverges from canonical, and its `MD5-CAM` checksum will no longer match — prefer contributing the change upstream in CKM. Surface this as a caveat; it does not block local work.
- If the examples corpus holds the same archetype id, `examples_get` it and compare `uid`/revision to spot drift from the gold-standard.

## 2. Lint
Apply the 24 normative lint rules — load `guide_get("openehr://guides/archetypes/rules")` for the definitions (the `archetype-lint` skill runs this standalone). Also load:

```
guide_get("openehr://guides/archetypes/checklist")
guide_get("openehr://guides/archetypes/anti-patterns")
```

Use `type_specification_get` to verify RM attribute names (rule 4). Output PASS/FAIL plus a violations table (severity, rule, explanation, suggested fix).

## 3. Remediate
- **On FAIL (ERRORs):** produce a minimal-diff fix plan mapped to rule violations — for each fix, note whether it changes paths or semantics and the version-bump implication. Present the plan and wait for approval; then patch and re-lint (max ~3 iterations).
- **On PASS with WARNING/INFO:** do not stop at "nothing to improve." Produce an advisory-remediation block — issue → suggested improvement → which fixes touch paths/semantics/checksums — without invoking the ERROR-only fix machinery. "Spot issues and suggest improvements" is a valid request even when the archetype passes.

## 4. Review packet (optional)
For a CKM-style review, generate justifications for any unresolved warnings and questions for clinicians, alongside the rationale prose (see `rationale-prose.md`).

## Final checklist
- [ ] One concept per archetype
- [ ] Correct RM type selected
- [ ] Valid ADL 1.4 syntax
- [ ] All at-codes defined in terminology section
- [ ] Terminology bindings use semantic equivalence
- [ ] Slot constraints are explicit
- [ ] No anti-patterns present
- [ ] Formatting follows conventions
