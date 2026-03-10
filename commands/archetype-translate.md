---
name: archetype-translate
description: Add or translate language entries in an archetype terminology section
argument-hint: "<file path or archetype-id> <target language code>"
allowed-tools:
  - Read
  - Edit
  - Write
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_get
---

# /archetype-translate

Add or translate language entries in an archetype terminology section.

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
5. Locate the `ontology` / `terminology` section
6. For each at-code in the primary language:
   - Translate the `text` and `description` fields to the target language
   - Use clinically natural target-language wording
   - Maintain clinical precision — do not paraphrase clinical terms loosely
   - Preserve terminology bindings unchanged (codes are language-independent)
   - Flag uncertain or non-equivalent clinical terms for review
7. Add the new language block to the terminology section following ADL conventions
8. Update the `languages_available` list in the archetype header
9. If working with a file, use Edit to apply the translations

## Required Output

1. **Full updated ADL** with translated terminology section
2. **Translation mapping summary**: at-code -> original text -> translated text
3. **Translation warnings**: uncertain terms flagged for clinical review
