# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

## [0.6.0] - 2026-04-22

### Added
- Commands `/archetype-rationale` and `/template-from-form` (rationale prose; inverse form → template sketch).
- Commands `/archetype-impact`, `/archetype-diff`, `/template-diff` (workspace impact scan; semantic diffs with G1 version-bump rubric in `commands/references/semantic-diff-rubric.md`).
- Agents `ckm-scout` (reuse-first CKM search) and `spec-researcher` (isolated spec lookup via `howto/spec-lookup`).
- Hook `lint-on-save` (Claude PostToolUse): reminder after `.adl` writes/edits.

### Changed
- Commands `archetype-translate` and `archetype-fix-syntax`: ADL 1.4 wording (`ontology`, `language.translations`; no top-level `terminology` section).
- Agent `clinical-modeler` and offline refs under `skills/openehr-assistant/reference/`: ADL section order and ontology vs terminology clarified against MCP spec copies.
- Cursor rule `openehr-context.mdc`: `name` in frontmatter.

### Removed
- Skill `platform-design`; use `openehr-assistant` with `guide_get("specs/…")` / ITS digests instead (8 → 7 skills).

## [0.5.0] - 2026-04-21

### Added
- MCP **v0.16.0**: `examples_search` / `examples_get`, `openehr://examples/{kind}/{name}`; router and `openehr-assistant` skill updated accordingly.
- Guide routing: `specs/` and `howto/` categories; conditional example hints in `aql-query`, `composition-builder`, `archetype-authoring`.
- Offline spec appendix (`llms.txt`, Markdown twin caveat); bundled example archetypes tagged **Synced from** v0.16.0.
- `.gitattributes` `export-ignore` for maintainer-only paths; CONTRIBUTING sections on archives and MCP bumps; README contributor link.

### Changed
- Commands `/ehr-structure` and `/demographic-structure` merged into `/rm-structure <domain> <concept>` (16 → 15 commands).
- Guide and doc URIs: `rm/*` → `specs/*`; external spec links follow `development` and `howto/spec-lookup` instead of `latest`.
- Cursor rule decoupled from AGENTS.md for end users; Claude manifest aligned with Cursor (`displayName`, `keywords`); MCP compatibility set to v0.16.0.

### Removed
- Skill `guide-prompt-authoring` (canonical copy under openehr-assistant-mcp `.cursor/skills/guide-prompt-authoring/`).

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
