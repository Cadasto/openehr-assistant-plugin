# Fix ADL Syntax (syntax-only remediation)

Fix ADL syntax errors while preserving clinical semantics. This is a *syntax-only* mode: repair what prevents the archetype from parsing or validating structurally, and report — never fix — semantic or modelling issues.

## Workflow

1. Load the ADL syntax references:
   ```
   guide_get("openehr://guides/archetypes/adl-syntax")
   guide_get("openehr://guides/archetypes/reference-formatting")
   ```
2. Read the archetype content:
   - If a file path is provided, use the Read tool to load it.
   - If inline content is provided, analyze it directly.
3. Identify syntax issues:
   - Invalid ADL structure (missing sections, malformed blocks; section order: `archetype` → `specialise`? → `concept` → `language` → `description`? → `definition` → `invariant`? → `ontology` → `revision_history`?)
   - Remember the ADL 1.4 defaults before "fixing" them: unstated `occurrences`/`existence` = `{1..1}` — absence is not an error
   - Incorrect constraint syntax (use `guide_adl_idiom_lookup` for correct patterns)
   - Missing or mismatched at-codes
   - **Ontology** inconsistencies (`term_definitions`, `constraint_definitions`, `term_bindings` — standard ADL 1.4 has no separate top-level `terminology` section)
   - Invalid RM type references (verify with `type_specification_get`)
4. Fix each issue while preserving:
   - All clinical semantics and intent
   - Existing terminology bindings
   - Archetype path structure
   - Node IDs (at-codes)
5. Use `ckm_archetype_search` and `ckm_archetype_get` to compare patterns with existing CKM archetypes when uncertain.
6. If fixing a file, use the Edit tool to apply corrections.

## Conflict resolution

If conflicts arise between syntax and idioms, ADL syntax takes precedence over idioms.

## Prohibited actions

- Do NOT rename concepts or archetype IDs
- Do NOT add or remove clinical elements
- Do NOT change coded meaning or terminology bindings
- Do NOT alter occurrence/cardinality intent
- Do NOT reorganize tree structure for readability

## Required output

1. **Corrected ADL** in a code block (or the applied Edit, when fixing a file)
2. **Minimal change log**: what was fixed and why (before/after snippets)
3. **Remaining ambiguities**: issues that could not be resolved without semantic decisions
4. **Detected semantic issues** (do NOT fix): modeling quality, terminology meaning, scope, over/under-constraint — route these to the review-remediate pipeline (Step 7 of the main skill; `review-remediate.md` in this directory) or the `archetype-lint` skill
