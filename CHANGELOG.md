# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

### Added
- Skill `guide-prompt-authoring`: multi-step workflow for authoring new implementation guides and MCP prompt files for the openehr-assistant-mcp server.

## [0.3.0] - 2026-03-10

### Added
- Skill `archetype-lint`: auto-invoked archetype validation with 22 normative lint rules (STRICT/PERMISSIVE).
- Commands `/archetype-lint`, `/archetype-review`, `/template-explain`.

### Changed
- **Claude Code**: Plugin manifest simplified to best practices (no explicit `components`; default folder discovery). Description and author (with `url`) aligned.
- **clinical-modeler** agent: scoped to local workspace file analysis only (no MCP tool access); use main-session openehr-assistant skill for CKM, guides, terminology.
- **openehr-assistant** skill: expanded with clinical modeling (template design, archetype selection, constraint specification, terminology binding, model review) and tool routing.

### Aligned
- **Cursor**: Manifest updated to 0.3.0; description and author match Claude manifest. All 6 skills, 14 commands, 1 agent, hooks, and rules remain in sync.

## [0.2.0] - 2026-03-10

### Added
- Cursor plugin support: `.cursor-plugin/plugin.json`, `hooks/cursor-hooks.json`, `rules/openehr-context.mdc`. Same skills, commands, agents, and MCP config as Claude; dual-host compatible.

## [0.1.0] - 2026-03-10

Initial public release.

### Added
- Plugin manifest (`.claude-plugin/plugin.json`).
- MCP server configuration (`.mcp.json`) connecting to the hosted openehr-assistant-mcp server.
- Skills: `openehr-assistant` (background awareness), `archetype-authoring`, `template-authoring`, `composition-builder`, `aql-query`.
- Commands: `/archetype-search`, `/archetype-explain`, `/template-search`, `/aql-designer`, `/format-data`, `/guide`, `/terminology`, `/type-spec`, `/adl-idiom`, `/archetype-fix-syntax`, `/archetype-translate`.
- Agent: `clinical-modeler` for clinical information modeling tasks.
- SessionStart hook for openEHR workspace detection.
- Documentation: README, AGENTS.md, CONTRIBUTING.md.
