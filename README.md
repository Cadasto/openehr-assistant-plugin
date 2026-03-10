# openEHR Assistant Plugin

AI plugin suite for clinical workflow integration with openEHR systems. Provides skills, commands, agents, and hooks for [Claude Code](https://claude.ai/code).

## Overview

This plugin connects Claude Code to the openEHR ecosystem through the companion [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server, enabling:

- **Archetype authoring** — create, edit, extend, and specialize clinical archetypes
- **Template design** — build and constrain templates for specific clinical workflows
- **Composition building** — generate FLAT, STRUCTURED, and CANONICAL format instances
- **AQL queries** — write, explain, and optimize Archetype Query Language queries
- **CKM discovery** — search the Clinical Knowledge Manager for archetypes and templates
- **Guide access** — browse 24 authoritative implementation guides

## Installation

```bash
claude plugin add cadasto/openehr-assistant-plugin
```

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
| `template-authoring` | Creating/reviewing templates | Template design with CGEM framework and narrowing principle |
| `composition-builder` | Building compositions | FLAT/STRUCTURED/CANONICAL format generation |
| `aql-query` | Writing AQL queries | Query authoring with optimization guidance |
| `openehr-assistant` | Any openEHR mention | Background awareness and tool routing |

### Commands

| Command | Description |
|---------|-------------|
| `/archetype-search <query>` | Find archetypes in CKM |
| `/archetype-explain <id>` | Explain archetype semantics and structure |
| `/template-search <query>` | Find templates in CKM |
| `/aql-designer <question or query>` | Explain, design, or review AQL queries |
| `/format-data <template or question>` | Explain or design openEHR data instances (FLAT/STRUCTURED/CANONICAL) based on a template |
| `/guide <topic>` | Browse openEHR implementation guides |
| `/terminology <code or term>` | Resolve terminology IDs and rubrics |
| `/type-spec <type name>` | Look up RM/AM/BASE type specifications |
| `/adl-idiom <pattern>` | Quick ADL constraint pattern lookup |
| `/archetype-fix-syntax <file>` | Fix ADL syntax errors preserving semantics |
| `/archetype-translate <file> <lang>` | Add/translate archetype language entries |

### Agent

| Agent | Description |
|-------|-------------|
| `clinical-modeler` | Clinical modeling specialist for template design, archetype selection, and model review |

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server provides:
- 10 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms)
- 15 MCP prompts (guided clinical workflows)
- 24 implementation guides (archetypes, templates, AQL, simplified formats)

## License

MIT - Cadasto B.V.
