# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

### Added
- Commands `/ckm-search`, `/openehr-explain`, `/semantic-diff` — unified/merged slash commands (see Changed); `/semantic-diff` adds a sibling / cross-artefact mode with a path-compatibility table.
- `.claude/settings.json` `permissions.allow` for the openEHR Assistant MCP server so subagents aren't silently denied CKM/guide/terminology access; documented in `docs/install.md` (Subagents & MCP permissions).

### Changed
- **Slash-command surface reduced 20 → 11.** Merged search (`/archetype-search` + `/template-search` → `/ckm-search`), explain/lookup (`/archetype-explain` + `/template-explain` + `/type-spec` + `/adl-idiom` + `/terminology` → `/openehr-explain`), and diff (`/archetype-diff` + `/template-diff` → `/semantic-diff`). Dropped `/aql-designer`, `/format-data`, `/archetype-review` — folded into the `aql-query`, `composition-builder`, and `archetype-authoring` skills.
- Agent `clinical-modeler`: granted **read-only** MCP lookups (terminology, type specs, guides, single CKM fetch) with offline-corpus fallback; previously local-only.
- Commands/skills: `/archetype-impact` globs `*.t.json` + parent `.adl` slots; `/archetype-translate` gains an at-code-parity verification block + tab-sensitive edit mechanics; `/archetype-rationale` documents the openEHR-only `terminology_resolve` limit; `archetype-lint` adds the `ITEM_TREE.items {0..*}` false-positive note; `template-authoring` gains an OET-emitting path + UID note; `archetype-authoring` gains CKM-import-for-reuse + the folded review pipeline.
- MCP compatibility: aligned with `openehr-assistant-mcp` **v0.18.0** — no plugin-facing tool changes (server-side: `enum`-constrained tool params, CKM search scoring retune, transport Host-header fix); `allowed-tools` ids and the bundled archetype corpus unchanged.
- Docs: AGENTS.md / README gotchas for subagent MCP permissions, named MCP params, and deferred-schema preload; `MD5-CAM` demoted to an advisory note (never a blocking requirement).

### Fixed
- Agents `ckm-scout` / `spec-researcher` / `clinical-modeler`: explicit `BLOCKED: …` fail-loud with a main-session fallback when MCP access is denied (previously degraded silently).

## [0.7.0] - 2026-06-07

Contributor tooling, CI, and community files, plus skill/command quality refinements. No change to end-user skill/command behaviour beyond the triggering and guide-deferral refinements below.

### Added
- Validation: `scripts/validate.py` and `scripts/validate.sh` (manifests, dual-host parity, bundled `.mcp.json`, skill/command/agent frontmatter) plus `.github/workflows/validate.yml` (pins Python, strict in CI).
- Community/scaffolding: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/PULL_REQUEST_TEMPLATE.md`.
- Docs: `docs/install.md`, `docs/testing.md`, `docs/versioning.md`, `docs/authoring.md` contributor references.
- `.claude/`: `settings.json` (enables maintainer plugins incl. `openehr-assistant-dev@cadasto`) and `CLAUDE.md` delegating to `AGENTS.md`.
- `skills/openehr-assistant/reference/README.md` indexing the offline reference corpus.

### Changed
- Skills: de-duplicated the 22 lint rules — `archetype-lint` is now a compact index deferring to `guide_get("archetypes/rules")`; `reference/lint-rules-complete.md` marked the offline twin.
- Skills: sharpened triggering boundaries against sibling commands (`aql-query`↔`/aql-designer`, `composition-builder`↔`/format-data`, `template-authoring`↔`/template-search`+`/template-explain`); `archetype-authoring` routes pure-explain to `/archetype-explain`; `openehr-assistant` gained an anti-trigger; `ckm-scout` handoff added to `demographic-modeling`.
- Commands: `/archetype-lint` and `/archetype-review` defer rule definitions to the loaded `archetypes/rules` guide.
- Commands: shared `semantic-diff-rubric.md` moved from `commands/references/` to top-level `references/` (consumed by `/archetype-diff`, `/template-diff`).
- Docs: `AGENTS.md` gained a Gotchas section and a `tools:` vs `allowed-tools` clarification; `README.md` and `CONTRIBUTING.md` link `docs/`, validation, community files, and marketplace install; `github.com/Cadasto` → `github.com/cadasto` URLs.
- Repo: dropped the `input/` scratch convention (removed from `.gitignore`); ignore `CLAUDE.local.md`.

### Fixed
- Agents: `ckm-scout` and `spec-researcher` now use `tools:` instead of `allowed-tools:` (ignored in agent frontmatter), so their intended tool sandboxes actually apply.

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
