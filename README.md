# openEHR Assistant Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.5.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![openehr-assistant-mcp](https://img.shields.io/badge/openehr--assistant--mcp-v0.16.0-brightgreen)](https://github.com/Cadasto/openehr-assistant-mcp)
[![openEHR](https://img.shields.io/badge/openEHR-compatible-009688)](https://openehr.org)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

AI plugin suite for clinical workflow integration with [openEHR](https://openehr.org/) systems. Adds skills, commands, agents, and hooks for **[Claude Code](https://claude.ai/code)** and **[Cursor](https://cursor.com)** that guide AI assistants through openEHR modeling, CKM discovery, and specification lookups.

This plugin works with the [openEHR Assistant MCP Server](https://github.com/Cadasto/openehr-assistant-mcp), which provides the tools, prompts, and resources (CKM, guides, terminology, type specs). The plugin supplies the workflow layer: when to load which guides, which commands to offer, and how to stay aligned with openEHR best practices.

**Recommended:** For installation, transports, and MCP client configuration of the server (hosted vs local, streamable-http vs stdio), see the **[openehr-assistant-mcp README](https://github.com/Cadasto/openehr-assistant-mcp#quick-start)** — [Quick Start](https://github.com/Cadasto/openehr-assistant-mcp#quick-start) and [Common client configurations](https://github.com/Cadasto/openehr-assistant-mcp#common-client-configurations).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup (MCP server)](#setup-mcp-server)
- [Components](#components)
- [Companion MCP Server](#companion-mcp-server)
- [License](#license)

---

## Features

- **Guide-first workflows** — Skills and commands instruct the assistant to load relevant implementation guides from the MCP server before answering.
- **Archetype authoring** — Create, edit, extend, and specialize clinical archetypes with lint rules and idiom lookup.
- **Template design** — Build and constrain templates using the CGEM framework and narrowing principle.
- **Composition building** — Generate FLAT, STRUCTURED, and CANONICAL format instances.
- **AQL queries** — Write, explain, and optimize Archetype Query Language queries.
- **CKM discovery** — Search the Clinical Knowledge Manager for archetypes and templates.
- **Demographic modeling** — PARTY hierarchy, roles, relationships, identity patterns.
- **Offline reference** — Quick-reference, ADL/AQL syntax cheatsheets, and RM type reference in the repo when MCP is unavailable.

---

## Installation

**Claude Code**

```bash
claude plugin add cadasto/openehr-assistant-plugin
```

**Cursor** — Add the plugin via Cursor’s plugin flow (e.g. from a Git URL or local path). The repo includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, commands, agents, and MCP config are shared with the Claude plugin.

**Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) for maintainer workflows, **clone vs `git archive`** (`.gitattributes` `export-ignore`), and how to bump compatibility with [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp).

---

## Setup (MCP server)

This plugin expects the **openEHR Assistant MCP Server** to be configured in your client. The plugin ships with a default MCP config that points at the hosted server; you can override it for local or stdio use.

For **server installation, transports (streamable-http vs stdio), and client-specific configuration** (Claude Desktop, Cursor, LibreChat, Junie), see:

- **[openehr-assistant-mcp — Quick Start](https://github.com/Cadasto/openehr-assistant-mcp#quick-start)** (hosted, Docker, stdio)
- **[openehr-assistant-mcp — Common client configurations](https://github.com/Cadasto/openehr-assistant-mcp#common-client-configurations)**

Environment variables (e.g. `CKM_API_BASE_URL`) and Docker/stdio details are documented in the [MCP server README](https://github.com/Cadasto/openehr-assistant-mcp).

---

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
| `openehr-assistant` | Any openEHR mention | Clinical modeling and tool routing |

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
| `/rm-structure <domain> <concept>` | Explain RM structural concepts in a given domain (`ehr` or `demographic`) — composition categories, ISM states, time, versioning, PARTY hierarchy, identities, privacy |
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

---

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/Cadasto/openehr-assistant-mcp) server provides:

- 12 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms, curated examples)
- 15 MCP prompts (guided clinical workflows)
- Implementation guides across six categories: `archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/` (openEHR specification digests tracking the `development` branch), and `howto/` (toolchain how-tos)
- Curated worked examples at `openehr://examples/{kind}/{name}` — AQL, FLAT, STRUCTURED payloads, and CKM-published reference `.adl` archetypes

**Compatibility:** This plugin version is built and tested against **openehr-assistant-mcp v0.16.0** ([releases](https://github.com/Cadasto/openehr-assistant-mcp/releases)). When updating the plugin, align with that server’s changelog so each plugin release stays compatible with a specific MCP server version.

Offline reference material in [`skills/openehr-assistant/reference/`](skills/openehr-assistant/reference/) includes a quick-reference (principles, rules, guide index), minimal ADL and AQL syntax cheatsheets, and an RM type reference (~30 commonly archetyped types with attributes for local lint rule 4 validation); see [AGENTS.md](AGENTS.md) (Syntax and grammar sources) for links to official specs and grammars.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

---

## License

[MIT License](LICENSE) — Cadasto B.V.
