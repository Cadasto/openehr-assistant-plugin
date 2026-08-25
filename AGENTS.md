# AI Guidelines: openEHR Assistant Plugin

This file provides guidance to AI coding assistants working in this repository.

## Project Overview

The **openEHR Assistant Plugin** is an AI plugin by Cadasto B.V. that provides clinical workflow integration with openEHR systems through skills, commands, agents, and hooks.

## Domain Context

**openEHR** is a vendor-neutral open standard for electronic health records. Key concepts:
- **Archetypes** — reusable clinical content definitions in ADL (Archetype Definition Language) format
- **Templates** — use-case-specific constraint sets combining archetypes, in four serialisations: **OET** (`.oet`, hand-authored source) and Archetype Designer **`.t.json`** (AOM2 differential source) compile to an **OPT** (runtime contract), from which a vendor **web template** (Better/EHRbase JSON) is derived for FLAT/STRUCTURED data entry. `.t.json` is a *source* template, not a web template
- **Compositions** — runtime clinical data instances conforming to templates
- **Reference Model (RM)** — core data types and structures
- **AQL** — Archetype Query Language for querying clinical data repositories
- **CKM** — Clinical Knowledge Manager, the international archetype/template registry

Not all openEHR content lives in CKM: a small convention exists of tagging GitHub repositories that publish archetypes/templates with the **`openehr-content`** topic (~14 repos — freshEHR, Apperta-CKM projects, regional programmes, individual modellers). It is a genuine secondary discovery channel, thinner but broader than CKM for *templates*, and **un-governed** — no editorial review, no dependable `lifecycle_state`, no integrity guarantee. Skills reference it only as a fallback after CKM, and only in the main session: no MCP tool searches it, so it needs `WebSearch`/`gh`.

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server provides:
- **12 MCP tools**: CKM search/retrieval, guide access, terminology resolution, type specifications, ADL idiom lookup, curated examples search/retrieval
- **14 MCP prompts**: Guided workflows for common tasks, each taking validated arguments
- **Resources**: Archetypes, templates, AQL, terminology, type specs, a guide registry spanning six categories (`archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/`, `howto/`), and the `openehr://examples/{kind}/{name}` namespace for curated worked examples (AQL, FLAT, STRUCTURED, reference `.adl` archetypes)

This plugin is aligned with **openehr-assistant-mcp v0.20.0** — the tagged release that folds in the guide refresh (CGEM/OPT/web-template guides, PROC/CNF/BMM3 spec digests) and the audit hardening (stricter tool schemas, relevance-scored `guide_search`, parameterized prompts, consolidated `ckm_explorer`). When syncing or aligning plugin changes (skills, commands, allowed-tools, guide URIs), refer to that server’s [releases](https://github.com/cadasto/openehr-assistant-mcp/releases) and changelog so each plugin version remains compatible with a specific MCP server version.

MCP tool names in this plugin use the format: `mcp__openehr-assistant__<tool_name>`

### Calling conventions the server enforces

Since v0.20.0 the server publishes closed input schemas (`additionalProperties: false`), rejects
the empty string for optional enum arguments, and fails loudly rather than degrading silently.
These rules follow for anything written here, in skills, or in commands:

- **Omit an optional argument, or pass `null` — never `""`.** `kind`, `category`, `component`
  and friends are nullable enums; `""` is rejected with a JSON-RPC `-32602`.
- **`guide_get` / `examples_get` take a canonical URI or an explicit `category`/`kind` + `name`.**
  Write `guide_get("openehr://guides/aql/syntax")`, not `guide_get("aql/syntax")` — the bare
  `category/name` string is not a resolvable URI and fails with `Invalid guide URI`.
- **`ckm_archetype_get` needs a CID or a full archetype-id.** Pass the CID from
  `ckm_archetype_search` (digits and dots, e.g. `1013.1.7850`) or an id containing `openEHR-`;
  a concept or display name is rejected with an explicit "could not resolve … to a CID" error
  (it used to be mangled into a doomed request reported as a missing archetype).
  `ckm_template_get` takes the template CID.
- **`terminology_resolve` covers openEHR terminology only and throws when it cannot resolve.**
  Never route SNOMED CT / LOINC / ICD codes to it — read those rubrics from the artefact's own
  `term_bindings` / `term_definitions`.
- **Search tools return `{ items, total }`.** `total` counts matches *before* the `maxResults`
  cap, so report it when presenting a capped list, and raise `maxResults` (1–50 for
  `guide_search` / `ckm_*_search`, 1–30 for `examples_search`) to see more — out-of-range values
  are **rejected, not clamped**.
- **An empty `guide_search` envelope means "rephrase", not "no such guidance exists".**
  Zero-score hits are dropped, and `taskType` only re-ranks — it never filters.

## Guide-First Principle

All skills and commands instruct the AI assistant to **load relevant guides from the MCP server before answering**. The guides are the authoritative knowledge registry, organised across six categories. A compact offline summary lives at `skills/openehr-assistant/reference/openehr-quick-reference.md` for use by the `clinical-modeler` agent and as a quick refresher; the same folder contains minimal **ADL** and **AQL syntax cheatsheets** (`adl-syntax-cheatsheet.md`, `aql-syntax-cheatsheet.md`) for offline structural/syntax checks, and an **RM type reference** (`rm-type-reference.md`) covering 39 commonly archetyped RM types with their attributes for local lint rule 4 (Valid RM Attributes Only) validation. Canonical guides via MCP always take precedence.
- `archetypes/` — principles, rules, ADL syntax, idioms, structural constraints, terminology, anti-patterns, checklist, language standards, reference formatting (`reference-formatting`)
- `templates/` — principles, rules, CGEM framework (`cgem-framework`), OET syntax, OET idioms, checklist, and the serialisation set (`serialization-formats`, `opt-structure`, `web-template`)
- `aql/` — principles, syntax, idioms, checklist
- `simplified_formats/` — principles, rules, idioms, checklist
- `specs/` — openEHR specification digests covering AM, AM2, BASE, RM (including EHR, Demographic, Common, Data Types, Data Structures), QUERY (AQL), TERM, LANG (including BMM, BMM3, EL, ODIN), CDS (GDL2), PROC (overview, Task Planning, Decision Language), CNF (conformance guide), SM (platform services), ITS-REST. Digests track the openEHR **development** branch; the former `rm/` category has been migrated into this namespace.
- `howto/` — toolchain how-tos (e.g. `spec-lookup` for efficient external spec retrieval via `llms.txt` and Markdown twin URLs).

### Curated worked examples (new in MCP v0.16)

The MCP server exposes `openehr://examples/{kind}/{name}` for gold-standard patterns. Skills and commands may consult `examples_search` / `examples_get` when a concrete worked example would help — this is a **conditional** aid, not a mandatory first step. Kinds: `aql`, `flat`, `structured`, `archetypes` (CKM-published native `.adl` files).

## Syntax and grammar sources

Use these when you need authoritative ADL or AQL syntax (e.g. for the `archetype-authoring` fix-syntax mode, AQL authoring, or when MCP guides are unavailable). Canonical detail lives in MCP guides and official specs; treat the following as pointers.

- **ADL syntax**: Official narrative in [specifications-AM](https://github.com/openEHR/specifications-AM) (e.g. `docs/ADL1.4/`, appendix C references ANTLR grammars). Normative grammars: [adl-antlr](https://github.com/openEHR/adl-antlr) (referenced by the spec). Consolidated ANTLR4 grammars (ADL1.4, ADL2): [openEHR-antlr4](https://github.com/openEHR/openEHR-antlr4) (`reader_adl14`, `reader_adl2`). MCP guide: `guide_get("openehr://guides/archetypes/adl-syntax")`. Published spec: `https://specifications.openehr.org/releases/AM/development/` (see retrieval methodology below).
- **AQL syntax**: Official narrative and grammar in [specifications-QUERY](https://github.com/openEHR/specifications-QUERY) (`docs/AQL/`). ANTLR4 grammars: [openEHR-antlr4](https://github.com/openEHR/openEHR-antlr4) `reader_aql`. MCP guide: `guide_get("openehr://guides/aql/syntax")`. Published spec: `https://specifications.openehr.org/releases/QUERY/development/` (see retrieval methodology below).

The written ADL1.4 spec points to adl-antlr for grammars; openEHR-antlr4 is the single consolidated ANTLR source for both ADL and AQL and is valid for implementation and tooling.

## Retrieving openEHR specifications

The MCP server's `guide_get("openehr://guides/howto/spec-lookup")` is the canonical reference for efficient spec retrieval. Key points this plugin depends on:

1. **Site index** — `https://specifications.openehr.org/llms.txt` enumerates every release, document, and JSON endpoint as a machine-readable list; use it to resolve component/doc phrases to canonical URLs and discover sibling docs.
2. **Markdown twin** — **most** `*.html` spec pages have a `.md` counterpart at the same path (e.g. `releases/RM/development/ehr.html` ↔ `releases/RM/development/ehr.md`); the coverage is not guaranteed, so fall back to the HTML page (or `type_specification_get`) when a twin 404s rather than concluding the document does not exist. The same payload is obtainable by sending `Accept: text/markdown` against the HTML URL. Prefer the Markdown twin for prose, rationale, and examples — it is the cheapest textual source.
3. **Class-table caveat** — the Markdown twin **omits** per-class attribute, function, and invariant tables. For those, fall through to the HTML page or the MCP's `type_specification_get` tool, which is backed by the BMM definitions.
4. **Structured JSON APIs** — `/api/components.json`, `/api/classes.json`, `/api/releases.json` return component enumerations, cross-release class indexes, and release calendars; prefer these over scraping HTML when doing class or release lookups.
5. **Development branch, not latest** — this plugin targets `releases/XX/development/` (mirroring where the MCP's `specs/` digests point). Only use a specific release tag (e.g. `Release-1.1.0`) when the user explicitly asks for a fixed release version.

For spec overview questions ("what does the EHR IM define?", "summarise ADL2"), prefer `guide_get(category="specs", name="<component>-<doc>")` before fetching the full spec — digests are 250–900 words and link onward to canonical URLs.

## Components

### Skills (8)
| Skill | Purpose |
|-------|---------|
| `openehr-assistant` | Auto-invoked openEHR awareness, clinical modeling, **guide browsing** (`guide_search`/`guide_get`), and tool routing |
| `archetype-authoring` | Create, edit, extend, specialize archetypes; CKM-import for reuse; **review & remediate** pipeline (absorbs `/archetype-review`); **rationale prose** (absorbs `/archetype-rationale`); **translate / add a locale** (absorbs `/archetype-translate`); **fix ADL syntax** (absorbs `/archetype-fix-syntax`) |
| `archetype-lint` | Auto-invoked archetype validation with 24 normative lint rules (STRICT/PERMISSIVE) |
| `template-authoring` | Create and constrain templates (OET/OPT); **form → template sketch** with CGEM split (absorbs `/template-from-form`) |
| `composition-builder` | Build compositions (FLAT/STRUCTURED/CANONICAL) |
| `aql-authoring` | Write, explain, optimize AQL queries |
| `semantic-diff` | Semantic diff of two artefacts — archetype or template, version-bump **or** sibling/cross-artefact mode with a path-compatibility table; rubric bundled in `references/`; also `/semantic-diff`-invocable |
| `demographic-modeling` | Design demographic models (PARTY hierarchy, roles, relationships, identity patterns) |

### Commands (3)
A deliberately small slash surface — multi-step workflows live in the **skills** (which auto-trigger and are also `/`-invocable); commands are explicit one-shots. Former commands were merged (search/explain/lookups/diffs), folded into skills (`/aql-designer`→`aql-authoring`, `/format-data`→`composition-builder`, `/archetype-review` + `/archetype-rationale` + `/archetype-translate` + `/archetype-fix-syntax`→`archetype-authoring`, `/template-from-form`→`template-authoring`, `/rm-structure`→`/openehr-explain`, `/guide` + `/archetype-lint`→ the `openehr-assistant` and `archetype-lint` skills), or converted to a skill outright (`/semantic-diff`). Note: `/archetype-lint` and `/semantic-diff` still work — they resolve to the user-invocable skills of the same name.

| Command | Purpose |
|---------|---------|
| `/ckm-search` | Find CKM **archetypes or templates** (`[archetype\|template] <query>`; optional `rmClass` filter) — merges `/archetype-search` + `/template-search` |
| `/openehr-explain` | Explain / look up **any** openEHR thing — archetype, template, RM/AM type, **RM structural concept**, ADL idiom, **AQL query/keyword**, or terminology code (auto-detects) — merges `/archetype-explain`, `/template-explain`, `/type-spec`, `/rm-structure`, `/adl-idiom`, `/terminology` |
| `/archetype-impact` | Scan workspace for references to an archetype across templates (`.oet`/`.opt`/`.t.json`), parent `.adl` slots, and AQL |

### Agents (3)
| Agent | Purpose |
|-------|---------|
| `clinical-modeler` | Local clinical model file analyst for reading, writing, reviewing, and editing archetype/template files. Writes only to the workspace; has **read-only** MCP lookups (terminology, type specs, guides, single CKM archetype fetch) with offline-corpus fallback when blocked |
| `ckm-scout` | Context-isolated CKM reuse-search specialist. Runs parallel searches with varied phrasings and returns ranked reuse/specialize/new recommendations. Dispatched by `archetype-authoring` skill or directly by the user |
| `spec-researcher` | Context-isolated openEHR spec research using the `howto/spec-lookup` methodology (llms.txt, `.md` twin, BMM, HTML fallthrough). Tracks the `development` branch |

### Hooks
- **SessionStart** — detects openEHR resources in workspace and displays context
- **PostToolUse** (Claude Code only) — when `Write` or `Edit` targets an `.adl` file, emits a reminder to run `/archetype-lint`. Cursor's hook schema does not expose a PostToolUse equivalent at the time of writing; Cursor users can trigger the reminder manually.

## Repository Layout

This repo supports **both Claude Code and Cursor**; shared assets (skills, commands, agents, `.mcp.json`) are used by both. Host-specific manifests and hook configs are separate.

- **Claude manifest**: `.claude-plugin/plugin.json` — name, version, description, author; component discovery uses default folders (skills/, commands/, agents/, hooks/, .mcp.json)
- **Cursor manifest**: `.cursor-plugin/plugin.json` — name, version, top-level paths (skills, rules, agents, commands, hooks, mcpServers)
- **MCP config**: `.mcp.json` — MCP server connection (default: streamable-http to hosted openehr-assistant-mcp); used by both hosts
- **Claude hooks**: `hooks/hooks.json` — array of `{ "type": "SessionStart", "command": "..." }`; use `${CLAUDE_PLUGIN_ROOT}` in command paths
- **Cursor hooks**: `hooks/cursor-hooks.json` — object `{ "hooks": { "sessionStart": [...] } }`; command runs from plugin root
- **Shared hook script**: `hooks/session-start.sh` — detects `.openehr-project.json`, `*.adl`, `*.oet`, `*.t.json`, `*.opt`/`*.optx`/`*.optj` and prints context
- **Cursor rules**: `rules/` — `.mdc` files (e.g. `openehr-context.mdc`) for Cursor-only rule guidance
- **Claude settings**: `.claude/settings.json` enables the maintainer plugins used while developing this repo (skill-creator, superpowers, plugin-dev, claude-md-management); `.claude/CLAUDE.md` imports this file via `@../AGENTS.md`. `.claude/settings.local.json` is gitignored (personal overrides).
- **Validation**: `scripts/validate.sh` (graceful local wrapper — warns and skips if Python is absent) runs `scripts/validate.py`, which checks both manifests, dual-host parity, declared component paths, the bundled `.mcp.json`, and skill/command/agent frontmatter. CI pins Python and runs the validator strictly ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)).
- **Contributor docs**: `docs/` holds committed human-facing references — [install](docs/install.md), [testing](docs/testing.md), [versioning](docs/versioning.md), [authoring](docs/authoring.md); `.github/` holds issue + PR templates and the validate workflow.
- **Reference material**: bulky supplementary content lives inside the consuming skill's `references/` subdirectory (e.g. `skills/semantic-diff/references/semantic-diff-rubric.md`) — never under `commands/` (see Gotchas).

## Development

### Testing & validating

No build step — pure Markdown + JSON. Validate and dogfood locally:

```bash
./scripts/validate.sh                                 # manifests, dual-host parity, .mcp.json, frontmatter (warns & skips if Python is absent)
claude plugin validate .                              # manifest + component structure (no Python needed)
claude --plugin-dir /path/to/openehr-assistant-plugin # load locally for one session
```

Then verify a command (`/ckm-search blood pressure`) and skill auto-triggering against the configured MCP server. On Cursor, add the plugin via its plugin flow and verify the same. CI runs `scripts/validate.py` strictly on every push/PR ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)); locally, `scripts/validate.sh` runs the same checks but warns and skips if Python isn't installed. Fuller guidance lives in [`docs/`](docs/): [install](docs/install.md), [testing](docs/testing.md), [versioning](docs/versioning.md), [authoring](docs/authoring.md).

### File Conventions
- Skills go in `skills/<name>/SKILL.md`
- Commands go in `commands/<name>.md`
- Agents go in `agents/<name>.md`
- Contributor reference, plans, specs, and design docs go in **`docs/`**
- All markdown files use YAML frontmatter for metadata
- `allowed-tools` (skills/commands) pre-approves MCP tools to avoid permission prompts; **agents use `tools:`** instead — `allowed-tools:` in an agent file is ignored and the agent silently inherits all tools
- Skills: use `auto-invocable` / `user-invocable` in frontmatter as needed; `argument-hint` and `$ARGUMENTS` work here too (skills are `/`-invocable); follow Guide-First (load MCP guides before acting)
- Commands: use `argument-hint` in frontmatter and `$ARGUMENTS` in body for user input; keep instructions concise for single-interaction completion. Prefer a skill for anything multi-step — commands are thin one-shots (see [docs/authoring.md](docs/authoring.md))

### Documentation Sync
When adding or renaming components, update: **AGENTS.md** (component tables), **README.md** (tables), and **hooks/session-start.sh** (the "Available: /command1, ..." list). Cursor uses the same skills/commands/agents paths; no separate Cursor-only list is required.

### Versioning
- Plugin version (and, for consistency, description and author) must be kept in sync in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Follow Semantic Versioning; update both manifests and **CHANGELOG.md** (Keep a Changelog format) when releasing.
- **Release naming:** git tags and GitHub release titles are exactly **`vX.Y.Z`** (annotated tag; no bare `X.Y.Z`, no descriptive suffix in the title). The release *theme* belongs in the CHANGELOG — its version section becomes the release notes — and CHANGELOG headings stay **bare** `## [X.Y.Z] - YYYY-MM-DD` per Keep a Changelog; only the tag and release title carry the `v`.

### CHANGELOG style
- Entries go under `## [Unreleased]` while work is in flight and get folded into the next `## [X.Y.Z] - YYYY-MM-DD` section at release.
- Use the Keep a Changelog groups in order: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**. Omit empty groups.
- One line per bullet. Lead with the subsystem (`Commands:`, `Guide URIs:`, `Cursor rule <path>:`) and state the change tersely. Use backticks for file, command, tool, URI, and frontmatter-key names.
- No rationale, no PR links, no restating *why* — that belongs in commit messages or the PR description. CHANGELOG captures *what* changed for a reader who wants a compact release delta.
- If a bullet is three lines, it is too long.
- When consolidating accumulated `[Unreleased]` work into a new release, check `git log <last-tag>..HEAD` to ensure every commit is represented exactly once across the groups.

### Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `fix(commands): corrected allowed-tools in archetype-search`, `feat(skills): added composition-builder skill`.
- Scopes: `skills`, `commands`, `agents`, `hooks`, `docs`, `mcp`.

### Branching
- Use feature branches and pull requests. Standard PR validation runs on every push.

## Gotchas

- **Agents use `tools:`, not `allowed-tools:`.** `allowed-tools:` is a skills/commands key; in an agent file it is ignored and the agent silently inherits *all* tools. Use `tools:` (a YAML list is fine). See `agents/clinical-modeler.md` for the correct form.
- **An MCP id in agent `tools:` must be listed under *both* mount namespaces.** `tools:` entries are matched literally against live tool ids, and an MCP tool's id depends on how the server was mounted: `mcp__openehr-assistant__<tool>` for a project/user `.mcp.json`, `mcp__plugin_openehr-assistant_openehr-assistant__<tool>` when it comes from this plugin's bundled `.mcp.json` (a claude.ai connector gives a third shape, `mcp__claude_ai_<connector>__<tool>`). A non-matching entry is **dropped silently**, and an agent whose entire `tools:` list resolves to nothing is **refused** — `would be spawned with zero tools`. So `ckm-scout` (MCP-only `tools:`) failed to spawn at all under a plugin mount, while `clinical-modeler` and `spec-researcher` spawned with built-ins only and hit their `BLOCKED: …` path. All three now list both forms, and `scripts/validate.py` enforces the pairing. Note the contrast with skills/commands: `allowed-tools` only pre-approves permissions, so a namespace miss there costs a prompt, not access.
- **Never put reference `.md` files under `commands/`.** Host validators (`claude plugin validate`) treat every `commands/**/*.md` as a command and warn on missing frontmatter — so a reference file there is mis-detected. Reference material belongs inside the consuming skill's `references/` subdirectory (e.g. `skills/semantic-diff/references/semantic-diff-rubric.md`); a command that needs bulky reference content is a sign it should be a skill.
- **Subagents need the MCP server pre-approved or they silently lose CKM/guide access.** Agent frontmatter `tools:` grants the *capability*, but the host's permission policy must still allow the server. The repo's `.claude/settings.json` `permissions.allow` lists the `openehr-assistant` server (both the bundled `mcp__plugin_openehr-assistant_openehr-assistant` and `mcp__openehr-assistant` namespaces); users who hit "CKM denied in a subagent" should add the same to their project settings. `ckm-scout` / `spec-researcher` / `clinical-modeler` fail loud with `BLOCKED: …` and route the lookup back to the main session when this isn't in place.
- **MCP tool parameters are named, not positional.** Skill/command examples use the readable `tool("value")` shorthand, but the real calls take the server's JSON params — e.g. `ckm_archetype_search` → `keyword`, `*_get` → `identifier`, `type_specification_get` → `name`. When unsure, the tool's loaded schema is authoritative; don't guess `{ query }`.
- **Deferred MCP tool schemas load on first use.** In review/diff flows that call several MCP tools, reference the tools early so their schemas resolve before the first call (avoids first-call round-trips). This is partly a host concern.
- **A self-hosted server advertising stale tools/prompts/guides is a server cache, not a plugin bug.** Since MCP v0.20.0 the discovery cache is namespaced by `APP_VERSION`; upgrading the server without bumping its version keeps the old capability ads. Clear it server-side (MCP repo `docs/development.md`). The hosted instance in `.mcp.json` is unaffected.
- **The Cursor hook uses a workspace-relative command** (`bash hooks/session-start.sh`), *not* `${CLAUDE_PLUGIN_ROOT}` (a Claude-Code-only variable). Keep both hook configs in step; don't "fix" the Cursor one to use the variable.
- **Lint rules have one source of truth: `guide_get("openehr://guides/archetypes/rules")`.** The `archetype-lint` skill keeps only a compact index; `skills/openehr-assistant/reference/lint-rules-complete.md` is the offline twin for the `clinical-modeler` agent. When the guide changes, update the offline twin — don't re-inline full rule text into the skill.
- **Register in the marketplace separately — and repin it on every release.** Public availability requires an entry in the `cadasto` marketplace, maintained in `Cadasto/plugin-marketplace`. That entry is pinned to a release tag, so tagging here ships nothing until the entry's `version` and `source.ref` are bumped; see [docs/versioning.md](docs/versioning.md#marketplace).
