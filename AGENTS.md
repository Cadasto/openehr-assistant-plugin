# AI Guidelines: openEHR Assistant Plugin

This file provides guidance to AI coding assistants working in this repository.

## Project Overview

The **openEHR Assistant Plugin** is an AI plugin by Cadasto B.V. that provides clinical workflow integration with openEHR systems through skills, commands, agents, and hooks.

## Domain Context

**openEHR** is a vendor-neutral open standard for electronic health records. Key concepts:
- **Archetypes** — reusable clinical content definitions in ADL (Archetype Definition Language) format
- **Templates** — use-case-specific constraint sets combining archetypes (OET for authoring, OPT for runtime)
- **Compositions** — runtime clinical data instances conforming to templates
- **Reference Model (RM)** — core data types and structures
- **AQL** — Archetype Query Language for querying clinical data repositories
- **CKM** — Clinical Knowledge Manager, the international archetype/template registry

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server provides:
- **12 MCP tools**: CKM search/retrieval, guide access, terminology resolution, type specifications, ADL idiom lookup, curated examples search/retrieval
- **15 MCP prompts**: Guided workflows for common tasks
- **Resources**: Archetypes, templates, AQL, terminology, type specs, a guide registry spanning six categories (`archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/`, `howto/`), and the `openehr://examples/{kind}/{name}` namespace for curated worked examples (AQL, FLAT, STRUCTURED, reference `.adl` archetypes)

This plugin is aligned with **openehr-assistant-mcp v0.16.0**. When syncing or aligning plugin changes (skills, commands, allowed-tools, guide URIs), refer to that server’s [releases](https://github.com/Cadasto/openehr-assistant-mcp/releases) and changelog so each plugin version remains compatible with a specific MCP server version.

MCP tool names in this plugin use the format: `mcp__openehr-assistant__<tool_name>`

## Guide-First Principle

All skills and commands instruct the AI assistant to **load relevant guides from the MCP server before answering**. The guides are the authoritative knowledge registry, organised across six categories. A compact offline summary lives at `skills/openehr-assistant/reference/openehr-quick-reference.md` for use by the `clinical-modeler` agent and as a quick refresher; the same folder contains minimal **ADL** and **AQL syntax cheatsheets** (`adl-syntax-cheatsheet.md`, `aql-syntax-cheatsheet.md`) for offline structural/syntax checks, and an **RM type reference** (`rm-type-reference.md`) covering ~30 commonly archetyped RM types with their attributes for local lint rule 4 (Valid RM Attributes Only) validation. Canonical guides via MCP always take precedence.
- `archetypes/` — principles, rules, ADL syntax, idioms, structural constraints, terminology, anti-patterns, checklist, language standards, formatting
- `templates/` — principles, rules, OET syntax, OET idioms, checklist
- `aql/` — principles, syntax, idioms, checklist
- `simplified_formats/` — principles, rules, idioms, checklist
- `specs/` — openEHR specification digests covering AM, AM2, BASE, RM (including EHR, Demographic, Common, Data Types, Data Structures), QUERY (AQL), TERM, LANG, CDS (GDL2), SM (platform services), ITS-REST. Digests track the openEHR **development** branch; the former `rm/` category has been migrated into this namespace.
- `howto/` — toolchain how-tos (e.g. `spec-lookup` for efficient external spec retrieval via `llms.txt` and Markdown twin URLs).

### Curated worked examples (new in MCP v0.16)

The MCP server exposes `openehr://examples/{kind}/{name}` for gold-standard patterns. Skills and commands may consult `examples_search` / `examples_get` when a concrete worked example would help — this is a **conditional** aid, not a mandatory first step. Kinds: `aql`, `flat`, `structured`, `archetypes` (CKM-published native `.adl` files).

## Syntax and grammar sources

Use these when you need authoritative ADL or AQL syntax (e.g. for `/archetype-fix-syntax`, AQL authoring, or when MCP guides are unavailable). Canonical detail lives in MCP guides and official specs; treat the following as pointers.

- **ADL syntax**: Official narrative in [specifications-AM](https://github.com/openEHR/specifications-AM) (e.g. `docs/ADL1.4/`, appendix C references ANTLR grammars). Normative grammars: [adl-antlr](https://github.com/openEHR/adl-antlr) (referenced by the spec). Consolidated ANTLR4 grammars (ADL1.4, ADL2): [openEHR-antlr4](https://github.com/openEHR/openEHR-antlr4) (`reader_adl14`, `reader_adl2`). MCP guide: `guide_get("archetypes/adl-syntax")`. Published spec: `https://specifications.openehr.org/releases/AM/development/` (see retrieval methodology below).
- **AQL syntax**: Official narrative and grammar in [specifications-QUERY](https://github.com/openEHR/specifications-QUERY) (`docs/AQL/`). ANTLR4 grammars: [openEHR-antlr4](https://github.com/openEHR/openEHR-antlr4) `reader_aql`. MCP guide: `guide_get("aql/syntax")`. Published spec: `https://specifications.openehr.org/releases/QUERY/development/` (see retrieval methodology below).

The written ADL1.4 spec points to adl-antlr for grammars; openEHR-antlr4 is the single consolidated ANTLR source for both ADL and AQL and is valid for implementation and tooling.

## Retrieving openEHR specifications

The MCP server's `guide_get("howto/spec-lookup")` is the canonical reference for efficient spec retrieval. Key points this plugin depends on:

1. **Site index** — `https://specifications.openehr.org/llms.txt` enumerates every release, document, and JSON endpoint as a machine-readable list; use it to resolve component/doc phrases to canonical URLs and discover sibling docs.
2. **Markdown twin** — every `*.html` spec page has a `.md` counterpart with the same path (e.g. `releases/RM/development/ehr.html` ↔ `releases/RM/development/ehr.md`). The same payload is obtainable by sending `Accept: text/markdown` against the HTML URL. Prefer the Markdown twin for prose, rationale, and examples — it is the cheapest textual source.
3. **Class-table caveat** — the Markdown twin **omits** per-class attribute, function, and invariant tables. For those, fall through to the HTML page or the MCP's `type_specification_get` tool, which is backed by the BMM definitions.
4. **Structured JSON APIs** — `/api/components.json`, `/api/classes.json`, `/api/releases.json` return component enumerations, cross-release class indexes, and release calendars; prefer these over scraping HTML when doing class or release lookups.
5. **Development branch, not latest** — this plugin targets `releases/XX/development/` (mirroring where the MCP's `specs/` digests point). Only use a specific release tag (e.g. `Release-1.1.0`) when the user explicitly asks for a fixed release version.

For spec overview questions ("what does the EHR IM define?", "summarise ADL2"), prefer `guide_get(category="specs", name="<component>-<doc>")` before fetching the full spec — digests are 250–900 words and link onward to canonical URLs.

## Components

### Skills (7)
| Skill | Purpose |
|-------|---------|
| `openehr-assistant` | Auto-invoked openEHR awareness, clinical modeling (template design, archetype selection, constraint specification, terminology binding, model review), and tool routing |
| `archetype-authoring` | Create, edit, extend, specialize archetypes |
| `archetype-lint` | Auto-invoked archetype validation with 22 normative lint rules (STRICT/PERMISSIVE) |
| `template-authoring` | Create and constrain templates (OET/OPT) |
| `composition-builder` | Build compositions (FLAT/STRUCTURED/CANONICAL) |
| `aql-query` | Write, explain, optimize AQL queries |
| `demographic-modeling` | Design demographic models (PARTY hierarchy, roles, relationships, identity patterns) |

### Commands (20)
| Command | Purpose |
|---------|---------|
| `/archetype-search` | Find CKM archetypes |
| `/archetype-explain` | Explain archetype semantics |
| `/archetype-lint` | Lint archetype against 22 normative rules |
| `/archetype-review` | Multi-stage archetype review pipeline (intent, lint, fix, re-lint, review packet) |
| `/template-search` | Find CKM templates |
| `/template-explain` | Explain template semantics |
| `/aql-designer` | Explain/design/review AQL |
| `/format-data` | Explain or design openEHR data instances (FLAT/STRUCTURED/CANONICAL) based on a template |
| `/rm-structure` | Explain RM structural concepts in a given domain (ehr or demographic) — composition categories, ISM states, time, versioning, PARTY hierarchy, identities, privacy |
| `/guide` | Browse openEHR guides |
| `/terminology` | Resolve terminology IDs |
| `/type-spec` | Look up RM/AM types |
| `/adl-idiom` | Quick ADL patterns |
| `/archetype-fix-syntax` | Fix ADL syntax |
| `/archetype-translate` | Translate archetype language |
| `/archetype-rationale` | Generate CKM-quality rationale prose (description, purpose, misuse, use) for an archetype |
| `/composition-from-form` | Map a clinical form to archetype composition + template sketch with narrowing notes |
| `/archetype-impact` | Scan workspace for references to a given archetype across templates and AQL files |
| `/archetype-diff` | Semantic diff between two archetype versions; classifies the version bump (patch / minor / major) per rule G1 |
| `/template-diff` | Semantic diff between two template versions; classifies the version bump |

### Agents (3)
| Agent | Purpose |
|-------|---------|
| `clinical-modeler` | Local clinical model file analyst for reading, writing, reviewing, and editing archetype/template files in the workspace. Includes local RM attribute validation via `rm-type-reference.md` (no MCP tool access) |
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
- **Shared hook script**: `hooks/session-start.sh` — detects `.openehr-project.json`, `*.adl`, `*.oet`, `*.opt` and prints context
- **Cursor rules**: `rules/` — `.mdc` files (e.g. `openehr-context.mdc`) for Cursor-only rule guidance
- **Plans, specs, design docs**: Create in **`input/`**, not in `docs/`. Use `input/` for implementation plans, specifications, design documents, and similar artifacts produced by or for AI assistants.

## Development

### Testing Locally

**Claude Code** — Install from a local path:
```bash
claude plugin add /path/to/openehr-assistant-plugin
```
Verify with: `/archetype-search blood pressure`

**Cursor** — Add the plugin from a local path (e.g. via Cursor settings or “Add plugin” using the repo path). Verify with `/archetype-search blood pressure` or any command that uses MCP tools.

### File Conventions
- Skills go in `skills/<name>/SKILL.md`
- Commands go in `commands/<name>.md`
- Agents go in `agents/<name>.md`
- **Plans, specs, and design docs** go in **`input/`** (not `docs/`)
- All markdown files use YAML frontmatter for metadata
- `allowed-tools` in frontmatter pre-approves MCP tools to avoid permission prompts
- Skills: use `auto-invocable` / `user-invocable` in frontmatter as needed; follow Guide-First (load MCP guides before acting)
- Commands: use `argument-hint` in frontmatter and `$ARGUMENTS` in body for user input; keep instructions concise for single-interaction completion

### Documentation Sync
When adding or renaming components, update: **AGENTS.md** (component tables), **README.md** (tables), and **hooks/session-start.sh** (the "Available: /command1, ..." list). Cursor uses the same skills/commands/agents paths; no separate Cursor-only list is required.

### Versioning
- Plugin version (and, for consistency, description and author) must be kept in sync in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Follow Semantic Versioning; update both manifests and **CHANGELOG.md** (Keep a Changelog format) when releasing.

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
