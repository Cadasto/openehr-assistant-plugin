# openEHR Assistant Plugin

AI plugin suite for clinical workflow integration with openEHR systems. Provides skills, commands, agents, and hooks for **[Claude Code](https://claude.ai/code)** and **[Cursor](https://cursor.com)**.

## Overview

This plugin connects Claude Code to the openEHR ecosystem through the companion [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server, enabling:

- **Archetype authoring** — create, edit, extend, and specialize clinical archetypes
- **Template design** — build and constrain templates for specific clinical workflows
- **Composition building** — generate FLAT, STRUCTURED, and CANONICAL format instances
- **AQL queries** — write, explain, and optimize Archetype Query Language queries
- **CKM discovery** — search the Clinical Knowledge Manager for archetypes and templates
- **Demographic modeling** — design demographic models using the PARTY hierarchy, roles, and relationships
- **Platform design** — design against openEHR platform service interfaces and REST API patterns
- **Guide access** — browse 27 authoritative implementation guides

## Installation

**Claude Code**
```bash
claude plugin add cadasto/openehr-assistant-plugin
```

**Cursor** — Add the plugin via Cursor’s plugin flow (e.g. from a Git URL or local path). The repo includes a Cursor manifest at `.cursor-plugin/plugin.json`; skills, commands, agents, and MCP config are shared with the Claude plugin.

## MCP Configuration

The plugin connects to the openEHR Assistant MCP server. Three transport options are available:

### Hosted (default, zero-setup)

The plugin ships pre-configured to use the hosted server:

```json
{
  "mcpServers": {
    "openehr-assistant": {
      "type": "streamable-http",
      "url": "https://openehr-assistant-mcp.apps.cadasto.com/"
    }
  }
}
```

### Local Docker (stdio)

Run the MCP server locally via Docker with stdio transport:

```json
{
  "mcpServers": {
    "openehr-assistant": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/cadasto/openehr-assistant-mcp:latest", "php", "public/index.php", "--transport=stdio"]
    }
  }
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CKM_API_BASE_URL` | Base URL CKM API server | `https://ckm.openehr.org/ckm/rest` |

## Components

### Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `archetype-authoring` | Creating/editing archetypes | Multi-step archetype authoring with guide-first approach |
| `archetype-lint` | Reviewing/validating archetypes | 22 normative lint rules with STRICT/PERMISSIVE modes |
| `template-authoring` | Creating/reviewing templates | Template design with CGEM framework and narrowing principle |
| `composition-builder` | Building compositions | FLAT/STRUCTURED/CANONICAL format generation |
| `aql-query` | Writing AQL queries | Query authoring with optimization guidance |
| `demographic-modeling` | Designing demographic models | PARTY hierarchy, roles, relationships, identity patterns |
| `platform-design` | Designing platform services | Service interfaces, REST API patterns, version update semantics |
| `openehr-assistant` | Any openEHR mention | Clinical modeling (template design, archetype selection, constraint specification, terminology binding, model review) and tool routing |
| `guide-prompt-authoring` | Creating guides or prompts | Author new implementation guides and MCP prompt files for the openehr-assistant-mcp server |

### Commands

| Command | Description |
|---------|-------------|
| `/archetype-search <query>` | Find archetypes in CKM |
| `/archetype-explain <id>` | Explain archetype semantics and structure |
| `/archetype-lint <file or id> [strict]` | Lint archetype against 22 normative rules |
| `/archetype-review <file or id> [strict]` | Multi-stage review pipeline (intent, lint, fix, re-lint, review packet) |
| `/template-search <query>` | Find templates in CKM |
| `/template-explain <id>` | Explain template semantics and structure |
| `/aql-designer <question or query>` | Explain, design, or review AQL queries |
| `/format-data <template or question>` | Explain or design openEHR data instances (FLAT/STRUCTURED/CANONICAL) based on a template |
| `/ehr-structure <concept>` | Explain EHR structural concepts (composition categories, ISM states, time, versioning) |
| `/demographic-structure <concept>` | Explain demographic model concepts (PARTY hierarchy, roles, identities, privacy) |
| `/guide <topic>` | Browse openEHR implementation guides |
| `/terminology <code or term>` | Resolve terminology IDs and rubrics |
| `/type-spec <type name>` | Look up RM/AM/BASE type specifications |
| `/adl-idiom <pattern>` | Quick ADL constraint pattern lookup |
| `/archetype-fix-syntax <file>` | Fix ADL syntax errors preserving semantics |
| `/archetype-translate <file> <lang>` | Add/translate archetype language entries |

### Agent

| Agent | Description |
|-------|-------------|
| `clinical-modeler` | Local clinical model file analyst for reading, writing, reviewing, and editing archetype/template files in the workspace |

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server provides:
- 10 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms)
- 15 MCP prompts (guided clinical workflows)
- 27 implementation guides (archetypes, templates, AQL, simplified formats, RM)

Offline reference material in `skills/openehr-assistant/reference/` includes a quick-reference (principles, rules, guide index) and minimal ADL and AQL syntax cheatsheets; see **AGENTS.md** (Syntax and grammar sources) for links to official specs and grammars.

## License

MIT - Cadasto B.V.
