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
- **10 MCP tools**: CKM search/retrieval, guide access, terminology resolution, type specifications, ADL idiom lookup
- **15 MCP prompts**: Guided workflows for common tasks
- **Resources**: Archetypes, templates, AQL, terminology, type specs, and 24 implementation guides

MCP tool names in this plugin use the format: `mcp__openehr-assistant__<tool_name>`

## Guide-First Principle

All skills and commands instruct the AI assistant to **load relevant guides from the MCP server before answering**. The guides (24 markdown files) are the authoritative knowledge registry:
- `archetypes/` (11 files) — principles, rules, ADL syntax, idioms, structural constraints, terminology, anti-patterns, checklist, language standards, formatting
- `templates/` (5 files) — principles, rules, OET syntax, OET idioms, checklist
- `aql/` (4 files) — principles, syntax, idioms, checklist
- `simplified_formats/` (4 files) — principles, rules, idioms, checklist

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
| `guide-prompt-authoring` | Author new implementation guides and MCP prompt files for the openehr-assistant-mcp server |

### Commands (14)
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
| `/guide` | Browse openEHR guides |
| `/terminology` | Resolve terminology IDs |
| `/type-spec` | Look up RM/AM types |
| `/adl-idiom` | Quick ADL patterns |
| `/archetype-fix-syntax` | Fix ADL syntax |
| `/archetype-translate` | Translate archetype language |

### Agents (1)
| Agent | Purpose |
|-------|---------|
| `clinical-modeler` | Local clinical model file analyst for reading, writing, reviewing, and editing archetype/template files in the workspace (no MCP tool access) |

### Hooks
- **SessionStart** — detects openEHR resources in workspace and displays context

## Repository Layout

This repo supports **both Claude Code and Cursor**; shared assets (skills, commands, agents, `.mcp.json`) are used by both. Host-specific manifests and hook configs are separate.

- **Claude manifest**: `.claude-plugin/plugin.json` — name, version, description, author; component discovery uses default folders (skills/, commands/, agents/, hooks/, .mcp.json)
- **Cursor manifest**: `.cursor-plugin/plugin.json` — name, version, top-level paths (skills, rules, agents, commands, hooks, mcpServers)
- **MCP config**: `.mcp.json` — MCP server connection (default: streamable-http to hosted openehr-assistant-mcp); used by both hosts
- **Claude hooks**: `hooks/hooks.json` — array of `{ "type": "SessionStart", "command": "..." }`; use `${CLAUDE_PLUGIN_ROOT}` in command paths
- **Cursor hooks**: `hooks/cursor-hooks.json` — object `{ "hooks": { "sessionStart": [...] } }`; command runs from plugin root
- **Shared hook script**: `hooks/session-start.sh` — detects `.openehr-project.json`, `*.adl`, `*.oet`, `*.opt` and prints context
- **Cursor rules**: `rules/` — `.mdc` files (e.g. `openehr-context.mdc`) for Cursor-only rule guidance

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
- All markdown files use YAML frontmatter for metadata
- `allowed-tools` in frontmatter pre-approves MCP tools to avoid permission prompts
- Skills: use `auto-invocable` / `user-invocable` in frontmatter as needed; follow Guide-First (load MCP guides before acting)
- Commands: use `argument-hint` in frontmatter and `$ARGUMENTS` in body for user input; keep instructions concise for single-interaction completion

### Documentation Sync
When adding or renaming components, update: **AGENTS.md** (component tables), **README.md** (tables), and **hooks/session-start.sh** (the "Available: /command1, ..." list). Cursor uses the same skills/commands/agents paths; no separate Cursor-only list is required.

### Versioning
- Plugin version (and, for consistency, description and author) must be kept in sync in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Follow Semantic Versioning; update both manifests and **CHANGELOG.md** (Keep a Changelog format) when releasing.

### Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `fix(commands): corrected allowed-tools in archetype-search`, `feat(skills): added composition-builder skill`.
- Scopes: `skills`, `commands`, `agents`, `hooks`, `docs`, `mcp`.

### Branching
- Use feature branches and pull requests. Standard PR validation runs on every push.
