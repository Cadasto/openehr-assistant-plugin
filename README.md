# openEHR Assistant Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.9.2-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![openehr-assistant-mcp](https://img.shields.io/badge/openehr--assistant--mcp-v0.20.0-brightgreen)](https://github.com/cadasto/openehr-assistant-mcp)
[![openEHR](https://img.shields.io/badge/openEHR-compatible-009688)](https://openehr.org)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

An AI plugin by **Cadasto B.V.** for [openEHR](https://openehr.org/) clinical modelling in **[Claude Code](https://claude.ai/code)** and **[Cursor](https://cursor.com)**. It is for anyone who authors or reviews archetypes, templates, compositions, or AQL with an AI assistant. It adds eight skills, three slash commands, three agents, two hooks, and a Cursor rule that guide the assistant through openEHR modelling, CKM discovery, and specification lookup.

The plugin supplies the workflow layer: when to load which guides, which commands to offer, and how to stay aligned with openEHR best practices. It does not carry the tools themselves. The tools, prompts, and resources (CKM, guides, terminology, type specifications) come from the companion [openEHR Assistant MCP Server](https://github.com/cadasto/openehr-assistant-mcp). To build the openEHR Assistant tooling itself (MCP tools, guides, examples), use the maintainer [openehr-assistant-dev](https://github.com/cadasto/openehr-assistant-dev-plugin) plugin instead.

**Requirements.** A Claude Code or Cursor host, and a reachable openEHR Assistant MCP server. A default install needs no server setup: the plugin bundles a config pointing at the hosted instance. Without a reachable server the guide-first workflows have nothing to load; the `clinical-modeler` agent falls back to the offline reference material in this repo, and `ckm-scout` and `spec-researcher` stop and say so.

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Components](#components)
- [Setup (MCP server)](#setup-mcp-server)
- [Companion MCP server](#companion-mcp-server)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Features

- **Guide-first workflows**: skills and commands instruct the assistant to load the relevant implementation guides from the MCP server before answering.
- **Archetype authoring**: create, edit, extend, and specialise clinical archetypes, with lint rules and idiom lookup.
- **Template design**: split a dataset across compositions with the CGEM framework (persistent / episodic / event), then build and constrain each template using the narrowing principle.
- **Composition building**: generate FLAT, STRUCTURED, and CANONICAL instances.
- **AQL queries**: write, explain, and optimise Archetype Query Language queries.
- **CKM discovery**: search the Clinical Knowledge Manager for archetypes and templates.
- **Demographic modelling**: PARTY hierarchy, roles, relationships, identity patterns.
- **Offline reference**: a quick reference, ADL and AQL syntax cheatsheets, ADL idiom and OET syntax references, the complete lint-rule set, and an RM type reference, carried in the repo for when the MCP server is unreachable.

## Installation

**Claude Code**, from the Cadasto marketplace:

```text
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install openehr-assistant@cadasto
```

Or load a local working copy for a single session: `claude --plugin-dir /path/to/openehr-assistant-plugin`.

**Cursor**: add this repository through Cursor's plugin flow (Settings → Plugins), from a Git URL or a local path. The repository includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, commands, agents, and the MCP config are shared with the Claude plugin.

See [docs/install.md](docs/install.md) for marketplace, local-development, update, and Cursor install details.

**Contributors:** see [CONTRIBUTING.md](CONTRIBUTING.md) for maintainer workflows, **clone vs `git archive`** (`.gitattributes` `export-ignore`), and how to bump compatibility with [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp).

## Components

### Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `archetype-authoring` | Creating/editing/reviewing/translating archetypes | Authoring, review and remediation, rationale prose, translation, ADL syntax fixing, CKM import; guide-first |
| `archetype-lint` | Linting/validating archetype rules compliance | 24 normative lint rules with STRICT/PERMISSIVE modes |
| `template-authoring` | Creating/reviewing templates | Template design with the CGEM framework and narrowing principle; form → template sketch |
| `composition-builder` | Building compositions | FLAT/STRUCTURED/CANONICAL format generation |
| `aql-authoring` | Writing AQL queries | Query authoring, explanation, and optimisation |
| `semantic-diff` | Comparing two artefacts (also `/semantic-diff`) | Version-bump verdict or sibling/cross-artefact compatibility report |
| `demographic-modeling` | Designing demographic models | PARTY hierarchy, roles, relationships, identity patterns |
| `openehr-assistant` | Any openEHR mention | Clinical modelling, guide browsing, and tool routing |

### Commands

The **skills** above drive the multi-step workflows (authoring, review, AQL, compositions) and trigger from natural language. Commands are a small set of explicit one-shots:

| Command | Description |
|---------|-------------|
| `/ckm-search [archetype\|template] <query>` | Find archetypes or templates in CKM (optional `rmClass` filter) |
| `/openehr-explain <thing>` | Explain or look up any openEHR thing: archetype, template, RM/AM type, RM structural concept, ADL idiom, AQL query/keyword, or terminology code (auto-detects) |
| `/archetype-impact <archetype-id>` | Scan the workspace for references to an archetype (source templates `.oet`/`.t.json`, compiled `.opt`, parent `.adl` slots, AQL) |

> For everything else, describe the task and the matching **skill** handles it, with no command needed: creating, editing, and reviewing archetypes (including **rationale prose**, **translation**, and **ADL syntax fixing**), linting, authoring templates (including the **form → template sketch**), building compositions, writing AQL, **diffing two artefacts**, and **browsing guides**.

### Agents

| Agent | Description |
|-------|-------------|
| `clinical-modeler` | Local clinical-model file analyst (read/write/review/edit `.adl`/`.oet`/`.t.json`/`.opt`). Writes locally; has read-only MCP lookups (terminology, type specs, guides, single CKM fetch) with offline fallback |
| `ckm-scout` | CKM reuse-search specialist: runs parallel searches and returns a ranked recommendation |
| `spec-researcher` | Spec research specialist using the llms.txt/.md twin methodology |

### Hooks and Cursor rule

| Component | Host | What it does |
|-----------|------|--------------|
| `SessionStart` hook ([`hooks/session-start.sh`](hooks/session-start.sh)) | Claude Code, Cursor | Detects openEHR files in the workspace (`.openehr-project.json`, `.adl`, `.oet`, `.t.json`, `.opt`/`.optx`/`.optj`) and prints a context line listing the commands and skills |
| `PostToolUse` hook ([`hooks/lint-on-save.sh`](hooks/lint-on-save.sh)) | Claude Code | After a `Write` or `Edit` to an `.adl` file, suggests running `/archetype-lint` on it |
| Rule [`rules/openehr-context.mdc`](rules/openehr-context.mdc) | Cursor | Applies to openEHR files (`.adl`, `.adls`, `.oet`, `.t.json`, `.opt`/`.optx`/`.optj`, `.aql`) and asks the assistant to load MCP guides before answering or editing |

## Setup (MCP server)

Nothing to configure for a default install: the plugin bundles a `.mcp.json` pointing at the hosted **openEHR Assistant MCP Server** over `streamable-http`.

To use your own server instead (local, Docker, or `stdio`), override that config in your host. The server's own README documents installation, transports, client-specific configuration (Claude Desktop, Cursor, LibreChat, Junie), and environment variables such as `CKM_API_BASE_URL`:

- **[openehr-assistant-mcp: Quick Start](https://github.com/cadasto/openehr-assistant-mcp#quick-start)** (hosted, Docker, stdio)
- **[openehr-assistant-mcp: Common client configurations](https://github.com/cadasto/openehr-assistant-mcp#common-client-configurations)**

> **One server, not two.** This plugin bundles its own `.mcp.json`, so it provides the `openehr-assistant` MCP server itself; prefer that. If you *also* added an `openehr-assistant` connector at claude.ai, the same tools appear twice (under a `claude_ai` namespace and the plugin's), and you can drop the connector. If a subagent reports CKM or guide tools as denied, the server is there but the host's permission policy blocks the subagent: see the `permissions.allow` snippet in [`.claude/settings.json`](.claude/settings.json) and [docs/install.md](docs/install.md#subagents-and-mcp-permissions).

## Companion MCP server

The [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server provides:

- 12 MCP tools (CKM search, guide access, terminology, type specs, ADL idioms, curated examples)
- 14 MCP prompts (guided clinical workflows, each taking validated arguments)
- Implementation guides across six categories: `archetypes/`, `templates/`, `aql/`, `simplified_formats/`, `specs/` (openEHR specification digests tracking the `development` branch), and `howto/` (toolchain how-tos)
- Curated worked examples at `openehr://examples/{kind}/{name}`: AQL, FLAT, STRUCTURED payloads, and CKM-published reference `.adl` archetypes

**Compatibility.** Built and tested against **openehr-assistant-mcp v0.20.0**. That release folds in the guide refresh (CGEM/OPT/web-template guides, PROC/CNF/BMM3 spec digests) and the audit hardening (stricter tool schemas, relevance-scored `guide_search`, parameterised prompts, the two CKM explorer prompts merged into one `ckm_explorer`); see the server [releases](https://github.com/cadasto/openehr-assistant-mcp/releases). Against a v0.19.0 server, references to the newer guides degrade through `guide_search` fallbacks; pin v0.20.0 for the full guide set. Every plugin release aligns with a specific server version, and the alignment checklist is in [docs/versioning.md](docs/versioning.md#mcp-compatibility).

Offline reference material in [`skills/openehr-assistant/reference/`](skills/openehr-assistant/reference/) carries a quick reference (principles, rules, guide index), ADL and AQL syntax cheatsheets, fuller ADL and OET syntax references, an ADL idiom reference, the complete lint-rule set, and an RM type reference (39 commonly archetyped types, with the attributes local lint rule 4 validates against). For the official specs and grammars behind them, see [AGENTS.md](AGENTS.md#syntax-and-grammar-sources).

## Development

No build step: the plugin is pure Markdown + JSON. Validate locally before opening a PR:

```bash
./scripts/validate.sh        # manifests, dual-host parity, .mcp.json, frontmatter (warns & skips if Python is absent)
claude plugin validate .     # manifest + component structure
```

CI runs the validator and a Vale prose check on every pull request and on pushes to `main`. Contributions are welcome: start with [CONTRIBUTING.md](CONTRIBUTING.md), and review the [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

## Documentation

- [docs/install.md](docs/install.md): install on both hosts, MCP wiring, and subagent permissions
- [docs/testing.md](docs/testing.md): validate and exercise the components locally
- [docs/versioning.md](docs/versioning.md): SemVer, MCP compatibility, and release steps
- [docs/authoring.md](docs/authoring.md): skill, command, and agent authoring conventions
- [CHANGELOG.md](CHANGELOG.md): release notes

## License

[MIT License](LICENSE)
