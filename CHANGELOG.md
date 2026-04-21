# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

### Added
- Commands: `/archetype-rationale` — generate CKM-quality rationale prose (description, purpose, misuse, use) for an archetype.
- Agents: `ckm-scout` subagent — reuse-first CKM search with parallel phrasings and ranked recommendation.
- Commands: `/composition-from-form` — inverse modelling from form description to archetype composition and template sketch.

### Changed
- Commands [`archetype-translate.md`](commands/archetype-translate.md) and [`archetype-fix-syntax.md`](commands/archetype-fix-syntax.md): wording aligned with ADL 1.4 (`ontology.term_definitions`, `language.translations` vs legacy names; no top-level `terminology` section).
- [`agents/clinical-modeler.md`](agents/clinical-modeler.md): structural review checklist aligned with ADL 1.4 spec section order and ontology/`term_definitions` (not a separate `terminology` section); documented Rule 19 (INFO).
- Offline ADL/RM reference docs aligned with MCP spec copies ([`docs/specs/AM/ADL1.4.md`](https://github.com/Cadasto/openehr-assistant-mcp/blob/main/docs/specs/AM/ADL1.4.md), RM data types): [`adl-syntax-cheatsheet.md`](skills/openehr-assistant/reference/adl-syntax-cheatsheet.md), [`adl-syntax-reference.md`](skills/openehr-assistant/reference/adl-syntax-reference.md), [`rm-type-reference.md`](skills/openehr-assistant/reference/rm-type-reference.md).
- Cursor rule [`rules/openehr-context.mdc`](rules/openehr-context.mdc): added frontmatter `name: openehr-context`.

### Removed
- Skill `platform-design` — routing absorbed into `openehr-assistant` (suggest `guide_get("specs/sm-openehr_platform")` / `guide_get("specs/its-rest-api")` for platform/service work). Skills: 8 → 7.

## [0.5.0] - 2026-04-21

### Added
- MCP v0.16.0: `examples_search` / `examples_get` tools and `openehr://examples/{kind}/{name}` resource namespace routed via `openehr-assistant` skill.
- Guide categories `specs/` (digests tracking `development`) and `howto/` (e.g. `spec-lookup`) surfaced in the router.
- Conditional example-retrieval hints in `aql-query`, `composition-builder`, `archetype-authoring` skills.
- Offline quick-reference appendix: `llms.txt`, `.md` twin URL pattern, class-table caveat.
- `.gitattributes` `export-ignore` for maintainer-only paths (`AGENTS.md`, `CONTRIBUTING.md`, `.github/**`).
- `**Synced from:**` version tag in `skills/openehr-assistant/examples/README.md` (byte-verified against MCP v0.16.0).
- CONTRIBUTING.md: "Repository archives" and "When bumping openehr-assistant-mcp compatibility" sections; README link to the contributor workflow.

### Changed
- Commands: merged `/ehr-structure` + `/demographic-structure` → `/rm-structure <domain> <concept>`. 16 → 15.
- Guide URIs: `rm/*` → `specs/*` (`rm-ehr`, `rm-demographic`, `sm-openehr_platform`); stale `rm/` fixed in `/guide` help.
- External spec retrieval: replaced `releases/XX/latest` URLs with a methodology tracking `development` via `howto/spec-lookup`.
- Cursor rule `rules/openehr-context.mdc`: dropped AGENTS.md dependency; added curated-examples and slash-command hints.
- Claude manifest: `displayName` and `keywords` aligned with Cursor manifest.
- Compatibility pointer: openehr-assistant-mcp **v0.16.0**.

### Removed
- Skill `guide-prompt-authoring` — relocated to openehr-assistant-mcp as a Cursor project skill.

## [0.4.0] - 2026-03-15

### Added
- Skill `guide-prompt-authoring` for authoring guides and MCP prompts.
- Skills `demographic-modeling` and `platform-design`.
- Commands `/ehr-structure` and `/demographic-structure`.
- Offline reference: ADL/AQL cheatsheets, syntax/lint/RM refs, quick-reference, example archetypes.
- AGENTS.md: Syntax and grammar sources; plans/specs in `input/`.
- README: MCP v0.15.0 compatibility; link to MCP repo for setup.

### Changed
- README: structure aligned with MCP repo; MCP config and env vars moved to openehr-assistant-mcp docs.
- Commands `/aql-designer`, `/archetype-explain`, `/template-explain`, `/guide` enhanced.
- clinical-modeler: offline refs and examples.
- SessionStart and docs: component list updated.

## [0.3.0] - 2026-03-10

### Added
- Skill `archetype-lint` with 22 normative lint rules (STRICT/PERMISSIVE).
- Commands `/archetype-lint`, `/archetype-review`, `/template-explain`.

### Changed
- Claude manifest simplified; description and author aligned.
- clinical-modeler: local workspace only, no MCP; use main session for CKM/guides/terminology.
- openehr-assistant skill: clinical modeling and tool routing.
- Cursor manifest 0.3.0; in sync with Claude (6 skills, 14 commands, 1 agent, hooks, rules).

## [0.2.0] - 2026-03-10

### Added
- Cursor plugin: `.cursor-plugin/plugin.json`, `hooks/cursor-hooks.json`, `rules/openehr-context.mdc`. Dual-host with Claude.

## [0.1.0] - 2026-03-10

### Added
- Plugin manifest and MCP config (hosted openehr-assistant-mcp).
- Skills: `openehr-assistant`, `archetype-authoring`, `template-authoring`, `composition-builder`, `aql-query`.
- Commands: `/archetype-search`, `/archetype-explain`, `/template-search`, `/aql-designer`, `/format-data`, `/guide`, `/terminology`, `/type-spec`, `/adl-idiom`, `/archetype-fix-syntax`, `/archetype-translate`.
- Agent `clinical-modeler`, SessionStart hook, README, AGENTS.md, CONTRIBUTING.md.
