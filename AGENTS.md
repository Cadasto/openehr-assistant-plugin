# AGENTS.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

The **openEHR Assistant Plugin** is a Claude Code plugin by Cadasto B.V. that provides clinical workflow integration with openEHR systems through skills, commands, agents, and hooks.

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

All skills and commands instruct Claude to **load relevant guides from the MCP server before answering**. The guides (24 markdown files) are the authoritative knowledge registry:
- `archetypes/` (11 files) — principles, rules, ADL syntax, idioms, structural constraints, terminology, anti-patterns, checklist, language standards, formatting
- `templates/` (5 files) — principles, rules, OET syntax, OET idioms, checklist
- `aql/` (4 files) — principles, syntax, idioms, checklist
- `simplified_formats/` (4 files) — principles, rules, idioms, checklist

## Components

### Skills (5)
| Skill | Purpose |
|-------|---------|
| `openehr-assistant` | Background auto-invoked openEHR awareness and tool routing |
| `archetype-authoring` | Create, edit, extend, specialize archetypes |
| `template-authoring` | Create and constrain templates (OET/OPT) |
| `composition-builder` | Build compositions (FLAT/STRUCTURED/CANONICAL) |
| `aql-query` | Write, explain, optimize AQL queries |

### Commands (11)
| Command | Purpose |
|---------|---------|
| `/archetype-search` | Find CKM archetypes |
| `/archetype-explain` | Explain archetype semantics |
| `/template-search` | Find CKM templates |
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
| `clinical-modeler` | Clinical modeling specialist for template design, archetype selection, model review |

### Hooks
- **SessionStart** — detects openEHR resources in workspace and displays context

## Development

### Testing Locally

Install the plugin from a local path:
```bash
claude plugin add /path/to/openehr-assistant-plugin
```

Verify MCP connection by running any command that uses MCP tools:
```
/archetype-search blood pressure
```

### File Conventions
- Skills go in `skills/<name>/SKILL.md`
- Commands go in `commands/<name>.md`
- Agents go in `agents/<name>.md`
- All markdown files use YAML frontmatter for metadata
- `allowed-tools` in frontmatter pre-approves MCP tools to avoid permission prompts
