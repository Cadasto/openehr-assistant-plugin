# openEHR Assistant Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.7.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![openehr-assistant-mcp](https://img.shields.io/badge/openehr--assistant--mcp-v0.19.0-brightgreen)](https://github.com/cadasto/openehr-assistant-mcp)
[![openEHR](https://img.shields.io/badge/openEHR-compatible-009688)](https://openehr.org)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

AI plugin suite for clinical workflow integration with [openEHR](https://openehr.org/) systems. Adds skills, commands, agents, and hooks for **[Claude Code](https://claude.ai/code)** and **[Cursor](https://cursor.com)** that guide AI assistants through openEHR modeling, CKM discovery, and specification lookups.

This plugin works with the [openEHR Assistant MCP Server](https://github.com/cadasto/openehr-assistant-mcp), which provides the tools, prompts, and resources (CKM, guides, terminology, type specs). The plugin supplies the workflow layer: when to load which guides, which commands to offer, and how to stay aligned with openEHR best practices.

**Recommended:** For installation, transports, and MCP client configuration of the server (hosted vs local, streamable-http vs stdio), see the **[openehr-assistant-mcp README](https://github.com/cadasto/openehr-assistant-mcp#quick-start)** — [Quick Start](https://github.com/cadasto/openehr-assistant-mcp#quick-start) and [Common client configurations](https://github.com/cadasto/openehr-assistant-mcp#common-client-configurations).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup (MCP server)](#setup-mcp-server)
- [Components](#components)
- [Companion MCP Server](#companion-mcp-server)
- [Contributing](#contributing)
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

**Claude Code** — from the Cadasto marketplace:

```
/plugin marketplace add cadasto/plugin-marketplace
/plugin install openehr-assistant@cadasto
```

or directly from the repo: `claude plugin add cadasto/openehr-assistant-plugin`.

**Cursor** — Add the plugin via Cursor’s plugin flow (e.g. from a Git URL or local path). The repo includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, commands, agents, and MCP config are shared with the Claude plugin.

See [docs/install.md](docs/install.md) for marketplace, local-development, update, and Cursor install details.

**Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) for maintainer workflows, **clone vs `git archive`** (`.gitattributes` `export-ignore`), and how to bump compatibility with [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp).

---

## Setup (MCP server)

This plugin expects the **openEHR Assistant MCP Server** to be configured in your client. The plugin ships with a default MCP config that points at the hosted server; you can override it for local or stdio use.

For **server installation, transports (streamable-http vs stdio), and client-specific configuration** (Claude Desktop, Cursor, LibreChat, Junie), see:

- **[openehr-assistant-mcp — Quick Start](https://github.com/cadasto/openehr-assistant-mcp#quick-start)** (hosted, Docker, stdio)
- **[openehr-assistant-mcp — Common client configurations](https://github.com/cadasto/openehr-assistant-mcp#common-client-configurations)**

Environment variables (e.g. `CKM_API_BASE_URL`) and Docker/stdio details are documented in the [MCP server README](https://github.com/cadasto/openehr-assistant-mcp).

> **One server, not two.** This plugin bundles its own `.mcp.json`, so it provides the `openehr-assistant` MCP server itself — prefer that. If you *also* added an `openehr-assistant` connector at claude.ai, the same tools appear twice (under a `claude_ai` namespace and the plugin's); that duplicate is optional. If a subagent reports CKM/guide tools "denied", it's a permission-policy gap, not a missing server — see the `permissions.allow` snippet in [`.claude/settings.json`](.claude/settings.json) and [docs/install.md](docs/install.md).

---

## Components

### Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `archetype-authoring` | Creating/editing/reviewing archetypes | Authoring, review & remediate pipeline, rationale prose, CKM-import — guide-first |
| `archetype-lint` | Reviewing/validating archetypes | 22 normative lint rules with STRICT/PERMISSIVE modes |
| `template-authoring` | Creating/reviewing templates | Template design with CGEM framework and narrowing principle |
| `composition-builder` | Building compositions | FLAT/STRUCTURED/CANONICAL format generation |
| `aql-authoring` | Writing AQL queries | Query authoring, explanation, and optimization |
| `demographic-modeling` | Designing demographic models | PARTY hierarchy, roles, relationships, identity patterns |
| `openehr-assistant` | Any openEHR mention | Clinical modeling, guide browsing, and tool routing |

### Commands

Multi-step workflows (authoring, review, AQL, compositions) are driven by the **skills** above, which auto-trigger from natural language. Commands are a small set of explicit one-shots:

| Command | Description |
|---------|-------------|
| `/ckm-search [archetype\|template] <query>` | Find archetypes or templates in CKM |
| `/openehr-explain <thing>` | Explain or look up any openEHR thing — archetype, template, RM/AM type, RM structural concept, ADL idiom, or terminology code (auto-detects) |
| `/semantic-diff <file-a> <file-b>` | Semantic diff of two artefacts (archetype or template); version-bump verdict or sibling/cross-artefact compatibility report |
| `/archetype-fix-syntax <file>` | Fix ADL syntax errors preserving semantics |
| `/archetype-translate <file> <lang>` | Add/translate archetype language entries (with at-code-parity verification) |
| `/template-from-form <form text or path>` | Map a clinical form to a template sketch (archetypes + narrowing) |
| `/archetype-impact <archetype-id>` | Scan workspace for references to an archetype (templates incl. `.t.json`, parent `.adl` slots, AQL) |

> Creating/editing/reviewing archetypes (incl. **rationale prose**), authoring templates, building compositions, writing AQL, and **browsing guides** are handled by the matching **skill** (no command needed) — just describe the task.

### Agents

| Agent | Description |
|-------|-------------|
| `clinical-modeler` | Local clinical-model file analyst (read/write/review/edit `.adl`/`.oet`/`.opt`). Writes locally; has read-only MCP lookups (terminology, type specs, guides, single CKM fetch) with offline fallback |
| `ckm-scout` | CKM reuse-search specialist — parallel searches, ranked recommendation |
| `spec-researcher` | Spec research specialist using llms.txt/.md twin methodology |

---

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server provides:

- 12 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms, curated examples)
- 15 MCP prompts (guided clinical workflows)
- Implementation guides across six categories: `archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/` (openEHR specification digests tracking the `development` branch), and `howto/` (toolchain how-tos)
- Curated worked examples at `openehr://examples/{kind}/{name}` — AQL, FLAT, STRUCTURED payloads, and CKM-published reference `.adl` archetypes

**Compatibility:** This plugin version is built and tested against **openehr-assistant-mcp v0.19.0** ([releases](https://github.com/cadasto/openehr-assistant-mcp/releases)). When updating the plugin, align with that server’s changelog so each plugin release stays compatible with a specific MCP server version.

Offline reference material in [`skills/openehr-assistant/reference/`](skills/openehr-assistant/reference/) includes a quick-reference (principles, rules, guide index), minimal ADL and AQL syntax cheatsheets, and an RM type reference (~30 commonly archetyped types with attributes for local lint rule 4 validation); see [AGENTS.md](AGENTS.md) (Syntax and grammar sources) for links to official specs and grammars.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

---

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the [`docs/`](docs/) references: [install](docs/install.md), [testing & validation](docs/testing.md), [versioning](docs/versioning.md), and [authoring conventions](docs/authoring.md). Before opening a PR, run `./scripts/validate.sh` and `claude plugin validate .` (CI runs the validator on every push). Please also review the [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

---

## License

[MIT License](LICENSE) — Cadasto B.V.
