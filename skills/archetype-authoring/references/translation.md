# Translate / add a locale

Add or translate per-language text in an archetype's `ontology.term_definitions` for a target language (ISO 639-1, e.g. `nl`, `de`, `fr`). In ADL 1.4 translations live in the ontology block, not a separate top-level `terminology` section.

1. Load `guide_get("openehr://guides/archetypes/language-standards")` and any per-language guide (e.g. `guide_get("openehr://guides/archetypes/language-standards-nl")`).
2. Locate the source-language `term_definitions` (e.g. `["en"]`); `term_bindings` are language-independent and stay unchanged.
3. Translate each at-code's `text` and `description` into clinically natural target-language wording — preserve clinical precision, flag uncertain terms for review, and reuse community terms where they already exist (via `ckm_archetype_get` / `examples_get`) rather than minting new ones.
4. Insert the new locale **at the top of its block** (anchor on the block opener + its first child; ADL is **tab**-indented, not spaces) in three places: `language.translations`, `description.details`, and `ontology.term_definitions`.
5. Verify (machine-checkable — base the "done" claim on it):
   - **at-code parity** — source vs target term counts match (e.g. `en vs nl: 69 = 69`);
   - **delimiter balance** — every `<` opened is closed across the inserted blocks;
   - **untouched invariants** — no change to at-codes, occurrences/cardinalities, units, value sets, or `term_bindings` (a translation edits text only);
   - **lint** — run the lint pass (see `review-remediate.md`) and surface its summary; failures block "done".
6. Advisory: editing makes `MD5-CAM`/`revision` stale — flag for upstream recomputation, never hand-fabricate. This never blocks producing the translation.
