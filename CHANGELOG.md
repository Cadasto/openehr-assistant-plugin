# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

## [0.9.2] - 2026-08-25

### Changed
- Docs: `docs/testing.md`, `docs/versioning.md`, `.vale.ini`, `AGENTS.md` — load a working copy; `$VER` in the release awk; Vale comments for this repo; RM type count 39.

## [0.9.1] - 2026-08-25

### Added
- CI: `.vale.ini` and a `prose` job pinned to Vale 3.18.0 — gates on errors only. Terminology lives in `styles/config/vocabularies/Cadasto/`; `skills/`, `agents/`, `commands/`, `rules/`, `hooks/` and `AGENTS.md` are excluded as model-facing content, and `styles/` is gitignored and `export-ignore`d.

### Changed
- Docs: release-naming convention recorded in AGENTS.md, `docs/versioning.md` and CONTRIBUTING.md — tags and GitHub release titles are exactly `vX.Y.Z`; CHANGELOG headings stay bare `X.Y.Z`. Legacy pre-`v0.8.1` tags renamed to the `v` form and their releases repointed.
- Docs: `docs/versioning.md`, `AGENTS.md` — catalog pins `version` to `X.Y.Z` and `source.ref` to `vX.Y.Z`; added as release step 7.
- Docs: `README.md` — states the requirements up front; `Setup (MCP server)` leads with "nothing to configure"; the MCP v0.20.0 compatibility note drops the two paragraphs about other clients' breaking changes and links `docs/versioning.md`; the offline-reference inventory names all of what ships and corrects the RM type count (39, was "~30").
- Docs: `docs/testing.md` — skill-triggering examples become a say-this/expect table; wording follows `--plugin-dir` (load, not install).
- Docs: `docs/versioning.md` — release step 6 pipes the CHANGELOG section into `gh release create -F -` instead of naming a placeholder file.
- Manifests: plugin `description` names what the plugin does — archetypes, templates, compositions, AQL, CKM reuse search, specification lookup — instead of "various openEHR related tasks". The catalog copies this string verbatim.

### Fixed
- Docs: `claude plugin add` is not a Claude Code command. `README.md`, `docs/install.md`, `CONTRIBUTING.md`, and `AGENTS.md` load a local working copy with `claude --plugin-dir <path>`, which applies to that session only; a persistent install goes through the marketplace.

## [0.9.0] - 2026-07-30

MCP **v0.20.0** alignment plus a **skills-first** surface consolidation. The plugin adopts the refreshed guide set and the server's enforced calling contracts, recognises all four template serialisations, promotes CGEM to a first-class design step, fixes agent MCP access under plugin mounts, and extends lint to 24 rules. The slash surface drops **6 → 3**: `/archetype-fix-syntax` and `/template-from-form` fold into their authoring skills, and `/semantic-diff` becomes a user-invocable skill (same invocation, now also auto-triggering). Removing/renaming commands is technically breaking; kept in the 0.x line (as with 0.8.0).

### Added
- Lint: rules **23** (Prose ↔ Slot Consistency, guide rule D9) and **24** (Translation Accuracy, guide rule E7) — the two `archetypes/rules` entries the 22-rule set never covered; appended so existing numbering stays stable. Rule count 22 → 24 across skills, agents and docs.
- Reuse: the `openehr-content` GitHub topic recorded as a secondary, **un-governed** discovery channel after CKM — in `archetype-authoring`, `template-authoring`, `ckm-scout`'s NEW verdict, and AGENTS.md domain context.
- Discovery: `hooks/session-start.sh` detects `.t.json` and `.optx`/`.optj`; the Cursor rule `openehr-context.mdc` globs cover `.adls`, `.t.json`, `.optx`/`.optj` and `.aql`.
- Commands: `/template-from-form` gains a CGEM dataset-split step and a `## Dataset split (CGEM)` output section, applied before any template is sketched.
- Validation: `scripts/validate.py` fails when an agent lists an MCP tool under one mount namespace but not the other.
- Validation: `scripts/validate.py` flags a bare `guide_get("category/name")` positional call in component docs — only the `openehr://guides/<category>/<name>` URI form passes.

### Changed
- MCP compatibility: pinned to `openehr-assistant-mcp` **v0.20.0** (guide/prompt refresh plus audit hardening); new-guide references sit in load-as-needed positions so a v0.19.0 server still works.
- Guide URIs: adopted new guides — `templates/cgem-framework`, `templates/opt-structure`, `templates/web-template`, `specs/proc-*`, `specs/cnf-guide`, `specs/lang-bmm3` — across `openehr-assistant`, `template-authoring`, `archetype-authoring`, `composition-builder`, `/openehr-explain`, and the quick-reference guide index.
- Skills: `template-authoring` adds defaults-vs-assumed-values (OET `default="…"`), the four template jobs, RM-attribute tightening as narrowing, and runtime-form (OPT/web-template) pointers.
- Skills: `aql-authoring` adds VERSION containment (`LATEST_VERSION`/`ALL_VERSIONS`), node/name predicates, MATCHES-vs-IN, and the spec-vs-engine function split.
- Skills: `composition-builder` adds `DV_ORDINAL`/`DV_PROPORTION`/`|other`/`|raw` suffixes, participations, and `ctx` server-side defaults.
- Skills: `archetype-authoring` adds the ADL 1.4 major-version-only id note and CGEM order-vs-record guidance; `archetype-lint` adds occurrences/existence-default and `VCOC` consistency notes and reframes validity codes as AOM2/tooling constructs.
- Agents: `spec-researcher` component list extended with PROC and CNF.
- Offline twins: `lint-rules-complete.md` (rule 5 defaults + `VCOC`, `ITEM_TREE.items {0..*}` false-positive note, validator-code appendix), `adl-syntax-cheatsheet.md` (defaults & consistency block), `aql-syntax-cheatsheet.md` (LIMIT/OFFSET, MATCHES-vs-IN, VERSION, function split).
- Offline twins: `rm-type-reference.md` (`PROPORTION_KIND` values), `openehr-quick-reference.md` (B1 HRID wording, template serialisation set, CGEM section with category codes and caveats, expanded guide index and specs coverage), `oet-syntax-reference.md` (category codes on the CGEM choice).
- Docs: AGENTS.md / README guide-category tables, compatibility notes and badge pinned to v0.20.0; MCP prompt count 15 → 14 (`ckm_explorer` consolidation).
- Docs: `docs/testing.md` and AGENTS.md Gotchas cover the `APP_VERSION`-namespaced server discovery cache; bundled archetype examples re-pinned to v0.20.0 (files unchanged).
- Calling conventions: AGENTS.md records the v0.20.0 contracts — CID-or-archetype-id for `ckm_archetype_get`, openEHR-only `terminology_resolve`, `{ items, total }` search envelopes with out-of-range `maxResults` rejected, and an empty `guide_search` envelope meaning "rephrase".
- Commands/agents: `/ckm-search` reports search `total` and retrieves by CID; `/openehr-explain` and `ckm-scout` state the `ckm_archetype_get` identifier rule; `ckm-scout` separates upstream CKM errors from `BLOCKED`.
- Skills/commands: `/semantic-diff` (and its rubric) guard `terminology_resolve` to openEHR codes; `openehr-assistant` documents `guide_search` scoring/`total` and corrects the external-terminology advice; `clinical-modeler` MCP-lookup list carries the same limits.
- Template serialisations: OET, Archetype Designer `.t.json`, OPT (`.opt`/`.optx`/`.optj`) and vendor web template are now named as four artefacts at three layers across AGENTS.md, README, `template-authoring` (Step 8), `openehr-assistant`, `/openehr-explain`, `/semantic-diff` and `clinical-modeler`.
- CGEM: triggers added to the `template-authoring` and `openehr-assistant` descriptions ("categorise a dataset", "persistent, episodic or event", CGEM) so the framework is reachable without knowing it lives inside template authoring.
- CGEM: all four category tables carry the `COMPOSITION.category` codes (431/451/433), the four-categories-three-codes caveat, the `451 episodic` support warning, and the non-normative freshEHR framing; `composition-builder` gains `episodic` and a CGEM pointer on `ctx/category`.

- Agents: `clinical-modeler` body deduplicated — triggering-examples section removed, inline lint-rule glosses replaced by a by-number local-vs-MCP routing split (rule text lives in `lint-rules-complete.md`).
- Agents: descriptions tightened across all three (`ckm-scout` gains a not-for clause); `ckm-scout` failure-mode protocol condensed to three bullets.
- Skills: `archetype-authoring` absorbs `/archetype-fix-syntax` as a fix-syntax mode (`references/fix-syntax.md`, Step 5b) — "fix ADL syntax / won't parse" intent now auto-triggers the skill; `archetype-lint` Step 5 routes fix application there.
- Skills: `template-authoring` absorbs `/template-from-form` as a from-form mode (`references/template-from-form.md`, Step 6b) — form → CGEM split → template sketch, handing off to Step 8b for the OET.
- Commands: `/semantic-diff` converted to a user-invocable skill — same `/semantic-diff` invocation, now also auto-triggers on compare/diff intent; the rubric moved from top-level `references/` into `skills/semantic-diff/references/`, removing the top-level `references/` directory.
- Skills: QA pass over all eight — descriptions gain trigger phrases and boundary clauses (`openehr-assistant`, `composition-builder`, `demographic-modeling`, `semantic-diff`), `archetype-lint` Step 5 slimmed to a router, CGEM content deduplicated (the from-form reference and `openehr-assistant` defer to `template-authoring` Step 6), `aql-authoring` syntax crib trimmed to guide pointers, imperative wording throughout.

- Docs: `CONTRIBUTING.md` refreshed — verification snippet uses current invocations (`/ckm-search`, `/openehr-explain`, `/semantic-diff`), agents corrected to `tools:` (not `allowed-tools`), `clinical-modeler` MCP note fixed.
- Docs: `docs/authoring.md` and AGENTS.md record the skills-preferred policy (commands reserved for thin one-shots); `docs/testing.md` exercises `/semantic-diff` as a skill; README adds `.t.json` to `clinical-modeler` and lists the newly skill-absorbed tasks.

### Removed
- Commands: `/archetype-fix-syntax` and `/template-from-form` (folded into `archetype-authoring` / `template-authoring`, see Changed).

### Fixed
- Skills: `aql-authoring` pre-approves `ckm_archetype_search`/`ckm_template_search` (its Step 2 requires search); `composition-builder` Step 6 loads `simplified_formats/checklist` and gains `Edit`; `semantic-diff` handles natural-language invocation (empty `$ARGUMENTS`); `archetype-lint` gains `argument-hint`; `archetype-authoring` pre-approves `WebSearch`.
- Offline twins: `lint-rules-complete.md` header no longer claims `clinical-modeler` has no MCP access — the twin is the fallback for its read-only lookups.
- Agents: `ckm-scout`, `clinical-modeler` and `spec-researcher` list every MCP tool under both mount namespaces (`mcp__openehr-assistant__*` and `mcp__plugin_openehr-assistant_openehr-assistant__*`); under a bundled-plugin mount the bare-only form matched nothing, so `ckm-scout` was refused with `would be spawned with zero tools` and the other two ran without MCP access. `docs/install.md` documents the three mount shapes and the claude.ai-connector caveat.
- Spec retrieval: the `.md` twin covers **most**, not every, spec page (0.20.0 `howto/spec-lookup` wording) — AGENTS.md, the quick-reference and `spec-researcher` now fall back to HTML on a 404 instead of concluding the document is missing.
- Lint: partial `term_bindings` coverage is not a rule 17/18 violation — a binding need not cover every at-code (`archetypes/terminology`); recorded as a known false positive in `archetype-lint` and the offline twin.
- Offline twins: the three files the July sync missed — `adl-idioms-reference.md` (ADL 1.4 occurrences/existence defaults + `VCOC`), `adl-syntax-reference.md` (`controlled`/`uncontrolled` flag, `specialise` hyphen note, `invariant` section semantics), `oet-syntax-reference.md` (`default="…"`, `countConstraint`, `includedTypes` values, MD5-CAM never-hand-write rule).
- Commands: `/template-from-form` loads `templates/cgem-framework` — the step named the guide but never fetched it.
- Commands: `/archetype-impact` no longer calls `.t.json` a web template — it is an AOM2 differential *source* template; the impact table now splits source from compiled references and says which `.opt` needs regenerating.
- Commands/skills: stale guide names corrected — `archetypes/formatting` → `archetypes/reference-formatting` (`/archetype-fix-syntax`, `archetype-authoring`), `archetypes/idioms-cheatsheet` → `archetypes/adl-idioms-cheatsheet` (offline corpus index).
- Guide references: `guide_get("<category>/<name>")` now uses the resolvable `openehr://guides/<category>/<name>` form across skills, commands and agents — the bare `category/name` string is not a valid URI and fails with `Invalid guide URI`.
- Skills: the openEHR-only `terminology_resolve` caveat propagated to `archetype-authoring`, `template-authoring` and `composition-builder`; `/semantic-diff` Shared constraints carry it too.
- Commands: `/openehr-explain` adds `ckm_archetype_search`/`ckm_template_search` to `allowed-tools` (the body instructs both searches) and its template heuristic covers `.t.json`/`.optx`/`.optj`.
- References: `semantic-diff-rubric.md` switches to sibling mode on differing root concepts instead of refusing, matching `/semantic-diff` §B.

## [0.8.1] - 2026-06-18

### Fixed
- Commands: `/semantic-diff` reads the plugin-root `references/semantic-diff-rubric.md` via a resolvable path (`${CLAUDE_PLUGIN_ROOT}/references/…`, `../references/…`, or Glob); the bare path failed a first Read.

## [0.8.0] - 2026-06-09

Surface consolidation and quality pass: the slash-command surface drops from **20 to 6** (multi-step workflows now live in the skills, which auto-trigger), agent MCP-access is fixed, authoring skills gain improvements distilled from real modelling sessions, and the plugin is aligned with `openehr-assistant-mcp` **v0.19.0**. Removing/renaming commands and a skill is technically breaking; kept in the 0.x line.

### Added
- Commands `/ckm-search`, `/openehr-explain`, `/semantic-diff` — unified/merged slash commands (see Changed); `/semantic-diff` adds a sibling / cross-artefact mode with a path-compatibility table.
- `.claude/settings.json` `permissions.allow` for the openEHR Assistant MCP server so subagents aren't silently denied CKM/guide/terminology access; documented in `docs/install.md` (Subagents & MCP permissions).

### Changed
- **Slash-command surface reduced 20 → 6.** Merged search (`/archetype-search` + `/template-search` → `/ckm-search`), explain/lookup (`/archetype-explain` + `/template-explain` + `/type-spec` + `/rm-structure` + `/adl-idiom` + `/terminology` → `/openehr-explain`), and diff (`/archetype-diff` + `/template-diff` → `/semantic-diff`). Dropped commands that duplicated a skill: `/aql-designer` → `aql-authoring`, `/format-data` → `composition-builder`, `/archetype-review` + `/archetype-rationale` + `/archetype-translate` → `archetype-authoring`, `/guide` → `openehr-assistant`, and `/archetype-lint` → the user-invocable `archetype-lint` skill (same name; `/archetype-lint` still resolves to it). Remaining commands: `/ckm-search`, `/openehr-explain`, `/semantic-diff`, `/archetype-fix-syntax`, `/archetype-impact`, `/template-from-form`.
- **Skill renamed** `aql-query` → `aql-authoring` (consistency with the `*-authoring` family).
- Agent `clinical-modeler`: granted **read-only** MCP lookups (terminology, type specs, guides, single CKM fetch) with offline-corpus fallback; previously local-only.
- Commands/skills: `/archetype-impact` globs `*.t.json` + parent `.adl` slots; `archetype-lint` adds the `ITEM_TREE.items {0..*}` false-positive note; `template-authoring` gains an OET-emitting path + UID note; `archetype-authoring` gains CKM-import-for-reuse, the folded review pipeline, rationale-prose drafting (incl. the openEHR-only `terminology_resolve` limit), and translation (at-code-parity verification + tab-sensitive edit mechanics); `openehr-assistant` gains guide browsing.
- MCP compatibility: aligned with `openehr-assistant-mcp` **v0.19.0** — additive server-side only (optional `rmClass` filter on `ckm_archetype_search`, tool titles/behaviour annotations, improved CKM recall/ranking, new `templates/serialization-formats` + `archetypes/language-standards-nl` guides, `DV_SCALE` idiom, lint-rule refinements); no plugin-facing tool-id changes, `allowed-tools` and the bundled archetype corpus unchanged.
- Docs: AGENTS.md / README gotchas for subagent MCP permissions, named MCP params, and deferred-schema preload; `MD5-CAM` demoted to an advisory note (never a blocking requirement).
- `/openehr-explain`: added an **AQL** branch (explain a query or an AQL keyword/operator, read-only); authoring/optimizing a query stays in the `aql-authoring` skill.
- Adopted v0.19.0 capabilities: `/ckm-search` and `ckm-scout` use the optional **`rmClass`** filter to scope to structural siblings; `template-authoring` references the new `templates/serialization-formats` guide; `archetype-authoring` + `composition-builder` reference the **`DV_SCALE`** vs `DV_ORDINAL` rating-scale idiom.
- `archetype-authoring`: progressive disclosure — moved the review/remediate, rationale-prose, and translation procedures to `references/` (lean body + summaries/pointers inline); de-bloated the description; reworded the UID note to not imply a `Bash` tool.
- Skill quality pass: anti-triggers on `archetype-lint` (lint vs lint+remediate) and `demographic-modeling` (PARTY vs clinical EHR); `aql-authoring` body title + `/openehr-explain` boundary.

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
