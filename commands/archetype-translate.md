---
name: archetype-translate
description: Add or translate per-language text in an archetype ontology (term_definitions), plus language metadata
argument-hint: "<file path or archetype-id> <target language code>"
allowed-tools:
  - Read
  - Edit
  - Write
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_get
---

# /archetype-translate

Add or translate **term_definition** entries under **`ontology`** for a target language (and update `language` / `languages_available` as required). In ADL 1.4, translations and local rubrics live in the ontology block, not in a separate top-level file section named `terminology`.

## Instructions

1. Load the translation guide:
   ```
   guide_get("archetypes/language-standards")
   ```
2. Parse the arguments: **$ARGUMENTS**
   - Identify the archetype (file path or archetype ID)
   - Identify the target language code (ISO 639-1, e.g., `nl`, `de`, `fr`, `es`)
3. If an archetype ID is provided, use `ckm_archetype_get` to retrieve it
   If a file path is provided, use Read to load the file
4. Search for per-language guides when available for the target language:
   ```
   guide_get("archetypes/language-standards-<lang>")
   ```
5. Locate **`ontology`** → **`term_definitions`** for the source language (e.g. `["en"]`); **`term_bindings`** stay unchanged (codes are language-independent)
6. For each at-code in the primary language:
   - Translate the `text` and `description` fields to the target language
   - Use clinically natural target-language wording
   - Maintain clinical precision — do not paraphrase clinical terms loosely
   - Preserve terminology bindings unchanged (codes are language-independent)
   - Flag uncertain or non-equivalent clinical terms for review
7. Add a sibling language block under `ontology.term_definitions` for the target locale (same `items` keys as the source language), following ADL / `guide_get("archetypes/language-standards")` conventions
8. Update the **`language`** section as required: per ADL 1.4, translated locales are tracked with **`translations`** (successor to legacy `languages_available`); some CKM files only declare `original_language` under `language` — follow the target archetype’s existing pattern and **`guide_get("archetypes/language-standards")`**
9. If working with a file, use Edit to apply the translations

## Edit mechanics (ADL is tab-sensitive)

Translations land in **three** locations. Insert each **at the top of its block** — anchor on the block opener plus its first child and prepend the new locale, rather than matching nested closing-delimiter runs (which is brittle in a whitespace-sensitive format):
- `language.translations` — a `["<lang>"] = <...>` language-metadata entry.
- `description.details` — a `["<lang>"] = <...>` purpose/use/misuse block.
- `ontology.term_definitions` — the `["<lang>"]` term block, mirroring the source locale's `items` keys.

Indent with **tabs** (not spaces) at the surrounding block's depth. Reuse community terms where they exist: if the fetched archetype (or `examples_get`) already carries the target locale, inherit its wording instead of minting new terms.

## Required Output

1. **Full updated ADL** with new/updated `ontology.term_definitions` (and `language.translations` / `description.details`) for the target language.
2. **Translation mapping summary**: at-code -> original text -> translated text.
3. **Translation warnings**: uncertain terms flagged for clinical review.
4. **Verification block** (machine-checkable — base the "done" claim on it):
   - **at-code parity** — source vs target locale term counts match (e.g. `en vs nl: 69 = 69`); any missing/extra at-code is an error.
   - **delimiter balance** — every `<` opened is closed across the inserted blocks.
   - **untouched invariants** — no change to at-codes, occurrences/cardinalities, units, value sets, or `term_bindings` (a translation edits text only).
   - **lint** — run `/archetype-lint` on the result and surface its summary; failures block the "done" claim.
5. **Metadata note (advisory)** — editing makes the archetype's `MD5-CAM` checksum and `revision` stale; flag them for upstream recomputation via CKM/ADL tooling rather than hand-fabricating a value. Advisory only — it never blocks producing the translation.
