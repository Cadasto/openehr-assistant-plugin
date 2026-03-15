# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

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
