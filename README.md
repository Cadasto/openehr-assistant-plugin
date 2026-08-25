# openEHR Assistant Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.9.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![openehr-assistant-mcp](https://img.shields.io/badge/openehr--assistant--mcp-v0.20.0-brightgreen)](https://github.com/cadasto/openehr-assistant-mcp)
[![openEHR](https://img.shields.io/badge/openEHR-compatible-009688)](https://openehr.org)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

AI plugin suite for clinical workflow integration with [openEHR](https://openehr.org/) systems. Adds skills, commands, agents, and hooks for **[Claude Code](https://claude.ai/code)** and **[Cursor](https://cursor.com)** that guide AI assistants through openEHR modeling, CKM discovery, and specification lookups.

This plugin works with the [openEHR Assistant MCP Server](https://github.com/cadasto/openehr-assistant-mcp), which provides the tools, prompts, and resources (CKM, guides, terminology, type specs). The plugin supplies the workflow layer: when to load which guides, which commands to offer, and how to stay aligned with openEHR best practices.

**Requirements.** A Claude Code or Cursor host, and a reachable openEHR Assistant MCP server. A default install needs no server setup — the plugin bundles a config pointing at the hosted instance. Without a reachable server the guide-first workflows have nothing to load; the `clinical-modeler` agent falls back to the offline reference material in this repo, and `ckm-scout` and `spec-researcher` stop and say so.

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
- **Template design** — Split a dataset across compositions with the CGEM framework (persistent / episodic / event), then build and constrain each template using the narrowing principle.
- **Composition building** — Generate FLAT, STRUCTURED, and CANONICAL format instances.
- **AQL queries** — Write, explain, and optimize Archetype Query Language queries.
- **CKM discovery** — Search the Clinical Knowledge Manager for archetypes and templates.
- **Demographic modeling** — PARTY hierarchy, roles, relationships, identity patterns.
- **Offline reference** — Quick reference, ADL and AQL syntax cheatsheets, ADL idiom and OET syntax references, the complete lint-rule set, and an RM type reference, carried in the repo for when the MCP server is unreachable.

---

## Installation

**Claude Code** — from the Cadasto marketplace:

```text
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install openehr-assistant@cadasto
```

Or load a local working copy for a single session: `claude --plugin-dir /path/to/openehr-assistant-plugin`.

**Cursor** — Add the plugin via Cursor's plugin flow, from a Git URL or a local path. The repo includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, commands, agents, and MCP config are shared with the Claude plugin.

See [docs/install.md](docs/install.md) for marketplace, local-development, update, and Cursor install details.

**Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) for maintainer workflows, **clone vs `git archive`** (`.gitattributes` `export-ignore`), and how to bump compatibility with [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp).

---

## Setup (MCP server)

Nothing to configure for a default install: the plugin bundles a `.mcp.json` pointing at the hosted **openEHR Assistant MCP Server** over `streamable-http`.

To use your own server instead — local, Docker, or `stdio` — override that config in your host. The server's own README documents installation, transports, client-specific configuration (Claude Desktop, Cursor, LibreChat, Junie), and environment variables such as `CKM_API_BASE_URL`:

- **[openehr-assistant-mcp — Quick Start](https://github.com/cadasto/openehr-assistant-mcp#quick-start)** (hosted, Docker, stdio)
- **[openehr-assistant-mcp — Common client configurations](https://github.com/cadasto/openehr-assistant-mcp#common-client-configurations)**

> **One server, not two.** This plugin bundles its own `.mcp.json`, so it provides the `openehr-assistant` MCP server itself — prefer that. If you *also* added an `openehr-assistant` connector at claude.ai, the same tools appear twice (under a `claude_ai` namespace and the plugin's); that duplicate is optional. If a subagent reports CKM/guide tools as denied, it's a permission-policy gap, not a missing server — see the `permissions.allow` snippet in [`.claude/settings.json`](.claude/settings.json) and [docs/install.md](docs/install.md).

---

## Components

### Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `archetype-authoring` | Creating/editing/reviewing/translating archetypes | Authoring, review & remediate, rationale prose, translation, ADL syntax fixing, CKM-import — guide-first |
| `archetype-lint` | Linting/validating archetype rules compliance | 24 normative lint rules with STRICT/PERMISSIVE modes |
| `template-authoring` | Creating/reviewing templates | Template design with CGEM framework and narrowing principle; form → template sketch |
| `composition-builder` | Building compositions | FLAT/STRUCTURED/CANONICAL format generation |
| `aql-authoring` | Writing AQL queries | Query authoring, explanation, and optimization |
| `semantic-diff` | Comparing two artefacts (also `/semantic-diff`) | Version-bump verdict or sibling/cross-artefact compatibility report |
| `demographic-modeling` | Designing demographic models | PARTY hierarchy, roles, relationships, identity patterns |
| `openehr-assistant` | Any openEHR mention | Clinical modeling, guide browsing, and tool routing |

### Commands

Multi-step workflows (authoring, review, AQL, compositions) are driven by the **skills** above, which auto-trigger from natural language. Commands are a small set of explicit one-shots:

| Command | Description |
|---------|-------------|
| `/ckm-search [archetype\|template] <query>` | Find archetypes or templates in CKM (optional `rmClass` filter) |
| `/openehr-explain <thing>` | Explain or look up any openEHR thing — archetype, template, RM/AM type, RM structural concept, ADL idiom, AQL query/keyword, or terminology code (auto-detects) |
| `/archetype-impact <archetype-id>` | Scan workspace for references to an archetype (source templates `.oet`/`.t.json`, compiled `.opt`, parent `.adl` slots, AQL) |

> Creating/editing/reviewing archetypes (incl. **rationale prose**, **translation**, and **ADL syntax fixing**), linting, authoring templates (incl. the **form → template sketch**), building compositions, writing AQL, **diffing two artefacts**, and **browsing guides** are handled by the matching **skill** (no command needed) — just describe the task.

### Agents

| Agent | Description |
|-------|-------------|
| `clinical-modeler` | Local clinical-model file analyst (read/write/review/edit `.adl`/`.oet`/`.t.json`/`.opt`). Writes locally; has read-only MCP lookups (terminology, type specs, guides, single CKM fetch) with offline fallback |
| `ckm-scout` | CKM reuse-search specialist — parallel searches, ranked recommendation |
| `spec-researcher` | Spec research specialist using llms.txt/.md twin methodology |

---

## Companion MCP Server

The [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server provides:

- 12 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms, curated examples)
- 14 MCP prompts (guided clinical workflows, each taking validated arguments)
- Implementation guides across six categories: `archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/` (openEHR specification digests tracking the `development` branch), and `howto/` (toolchain how-tos)
- Curated worked examples at `openehr://examples/{kind}/{name}` — AQL, FLAT, STRUCTURED payloads, and CKM-published reference `.adl` archetypes

**Compatibility.** Built and tested against **openehr-assistant-mcp v0.20.0**, which folds in the guide refresh (CGEM/OPT/web-template guides, PROC/CNF/BMM3 spec digests) and the audit hardening (stricter tool schemas, relevance-scored `guide_search`, parameterized prompts, the two CKM explorer prompts merged into one `ckm_explorer`) — see [releases](https://github.com/cadasto/openehr-assistant-mcp/releases). Against a v0.19.0 server, references to the newer guides degrade through `guide_search` fallbacks; pin v0.20.0 for the full guide set. Every plugin release aligns with a specific server version — the checklist is in [docs/versioning.md](docs/versioning.md#mcp-compatibility).

Offline reference material in [`skills/openehr-assistant/reference/`](skills/openehr-assistant/reference/) carries a quick reference (principles, rules, guide index), ADL and AQL syntax cheatsheets, fuller ADL and OET syntax references, an ADL idiom reference, the complete lint-rule set, and an RM type reference — 39 commonly archetyped types with the attributes local lint rule 4 validates against. For the official specs and grammars behind them, see [AGENTS.md](AGENTS.md#syntax-and-grammar-sources).

See [CHANGELOG.md](CHANGELOG.md) for release notes.

---

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the [`docs/`](docs/) references: [install](docs/install.md), [testing & validation](docs/testing.md), [versioning](docs/versioning.md), and [authoring conventions](docs/authoring.md). Before opening a PR, run `./scripts/validate.sh` and `claude plugin validate .` (CI runs the validator on every push). Please also review the [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

---

## License

[MIT License](LICENSE) — Cadasto B.V.
