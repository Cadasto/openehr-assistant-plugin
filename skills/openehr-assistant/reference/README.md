# Offline Reference Corpus

**Purpose:** Compact, offline reference material for openEHR structural and syntax checks. These files exist primarily for the **`clinical-modeler` agent**, which has *no MCP access* and so cannot call `guide_get` / `type_specification_get`. They are also a quick refresher for the main session.

**Authority:** In the main session, the MCP guides (`guide_get(...)`) and `type_specification_get` are **authoritative**. These files are condensed offline twins — if a file disagrees with the loaded guide or the live spec, the guide/spec wins. Keep them in sync when the corresponding guide changes (see `CONTRIBUTING.md` → "When bumping openehr-assistant-mcp compatibility").

> Do not delete these as "unreferenced" — they are loaded on demand by the offline agent, not linked from every SKILL.md.

## Index — load on demand

| File | Load when… | Authoritative source |
|------|-----------|----------------------|
| `openehr-quick-reference.md` | A fast refresher on principles, rules, and the guide index is needed | the relevant MCP guide |
| `adl-syntax-cheatsheet.md` | A minimal ADL syntax check is needed offline | `guide_get("openehr://guides/archetypes/adl-syntax")` |
| `adl-syntax-reference.md` | Fuller ADL syntax detail is needed offline | `guide_get("openehr://guides/archetypes/adl-syntax")` + specifications-AM |
| `adl-idioms-reference.md` | An ADL constraint idiom/pattern lookup is needed offline | `guide_adl_idiom_lookup` / `guide_get("openehr://guides/archetypes/adl-idioms-cheatsheet")` |
| `aql-syntax-cheatsheet.md` | A minimal AQL syntax check is needed offline | `guide_get("openehr://guides/aql/syntax")` |
| `oet-syntax-reference.md` | OET/template syntax detail is needed offline | `guide_get("openehr://guides/templates/oet-syntax")` |
| `rm-type-reference.md` | Validating RM attribute names (lint rule 4) offline | `type_specification_get` (BMM-backed) |
| `lint-rules-complete.md` | The full 22 lint-rule definitions are needed offline | `guide_get("openehr://guides/archetypes/rules")` |
