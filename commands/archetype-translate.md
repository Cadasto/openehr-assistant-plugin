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

## Required Output

1. **Full updated ADL** with new/updated `ontology.term_definitions` for the target language
2. **Translation mapping summary**: at-code -> original text -> translated text
3. **Translation warnings**: uncertain terms flagged for clinical review
