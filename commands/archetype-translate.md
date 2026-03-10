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
4. Locate the `ontology` / `terminology` section
5. For each at-code in the primary language:
   - Translate the `text` and `description` fields to the target language
   - Maintain clinical precision — do not paraphrase clinical terms loosely
   - Preserve terminology bindings unchanged (codes are language-independent)
6. Add the new language block to the terminology section following ADL conventions
7. Update the `languages_available` list in the archetype header
8. If working with a file, use Edit to apply the translations
9. Present a summary of translated terms
