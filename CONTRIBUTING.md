# Contributing to openehr-assistant-plugin

Thank you for your interest in contributing! This document explains how to propose changes and follow our conventions so that we can review and merge your work efficiently.


## Table of contents
- [Code of Conduct](#code-of-conduct)
- [Getting help and asking questions](#getting-help-and-asking-questions)
- [Project setup](#project-setup)
- [Plugin structure](#plugin-structure)
- [Adding or modifying components](#adding-or-modifying-components)
- [Testing locally](#testing-locally)
- [Commit messages and pull requests](#commit-messages-and-pull-requests)
- [Branching, issues, and release notes](#branching-issues-and-release-notes)
- [Versioning](#versioning)
- [Security](#security)


## Code of Conduct
Please be respectful and constructive. By participating, you agree to uphold a professional and inclusive environment. If you encounter unacceptable behavior, contact the maintainers privately via the repository's security/contact channels.


## Getting help and asking questions
- For usage questions, open a GitHub Discussion (if enabled) or a Question issue.
- For bugs, open an Issue and include: expected behavior, actual behavior, steps to reproduce, and environment details.
- For feature requests, explain the use-case and proposed UX.


## Project setup

Prerequisites:
- [Claude Code](https://claude.ai/code) CLI installed

Clone and install:
```bash
git clone <your-fork-url>
cd openehr-assistant-plugin
claude plugin add .
```

No build step is required — the plugin is pure markdown and JSON.


## Plugin structure

```
.claude-plugin/plugin.json     # Claude Code plugin manifest
.cursor-plugin/plugin.json    # Cursor plugin manifest (same version, component paths)
.mcp.json                     # MCP server connection config (shared)
skills/                        # Multi-step authoring workflows
  <name>/SKILL.md
commands/                      # Slash commands (thin MCP tool wrappers)
  <name>.md
agents/                        # Specialized subagents
  <name>.md
hooks/                         # Event hooks
  hooks.json                   # Claude format (array with type + command)
  cursor-hooks.json            # Cursor format (hooks.sessionStart, etc.)
  session-start.sh             # Shared script
rules/                         # Cursor-only rules (.mdc)
  openehr-context.mdc
```

Key conventions:
- Skills go in `skills/<name>/SKILL.md` with YAML frontmatter.
- Commands go in `commands/<name>.md` with YAML frontmatter.
- Agents go in `agents/<name>.md` with YAML frontmatter.
- All components use `allowed-tools` in frontmatter to pre-approve MCP tools.
- MCP tool names follow the format `mcp__openehr-assistant__<tool_name>`.


## Adding or modifying components

### Skills
Skills are multi-step, context-rich workflows. When adding a skill:
- Follow the Guide-First principle: instruct the skill to load relevant MCP guides before acting.
- Include `auto-invocable: true` for automatic triggering and/or `user-invocable: true` for manual use.
- List all required MCP tools in `allowed-tools`.
- Use progressive disclosure: mandatory steps first, then detailed guidance.

### Commands
Commands are thin wrappers around MCP tools for quick, focused tasks. When adding a command:
- Keep instructions concise — commands should complete in one interaction.
- Use `$ARGUMENTS` to capture user input.
- Include `argument-hint` in frontmatter to guide users.

### Agents
Agents are specialized subagents for complex domain tasks. When adding an agent:
- Write a clear system prompt explaining the agent's expertise.
- List all MCP tools the agent may need in `allowed-tools`.

### Hooks
Hooks respond to Claude Code events. When modifying hooks:
- Keep hook scripts fast — they run on every session start.
- Use `${CLAUDE_PLUGIN_ROOT}` for paths relative to the plugin root.

### Documentation
When adding or renaming components, update all references in:
- `AGENTS.md` (components table)
- `README.md` (commands/skills tables)
- `hooks/session-start.sh` (available commands list)


## Testing locally

Install the plugin from a local path:
```bash
claude plugin add /path/to/openehr-assistant-plugin
```

Verify components work:
```
/archetype-search blood pressure        # Test discovery command
/guide AQL syntax                        # Test guide browsing
/type-spec DV_QUANTITY                   # Test type lookup
```

Test skill auto-triggering by mentioning openEHR concepts in conversation without using a command.


## Commit messages and pull requests
- Use conventional commits when possible (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
- Write descriptive titles and include context in the body: what, why, how, and risks.
- One logical change per PR. Large changes can be split into smaller PRs.
- Link related issues using GitHub keywords (e.g., `Fixes #123`).

PR checklist:
- [ ] Component works when tested locally with `claude plugin add .`
- [ ] All references updated (AGENTS.md, README.md, hooks)
- [ ] CHANGELOG.md updated
- [ ] No debug code or leftover comments


## Branching, issues, and release notes
- Default branch: `main`
- Create feature branches from `main`: `feature/short-description` or `fix/short-description`
- We follow SemVer for releases and maintain a `CHANGELOG.md` (Keep a Changelog format).


## Versioning
- Plugin version is defined in both `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Update **both** when releasing new versions.
- Follow Semantic Versioning: breaking changes bump major, new features bump minor, fixes bump patch.


## Security
Do not open public issues for security vulnerabilities. Instead, please report privately using GitHub's security advisories or contact the maintainers directly.

Thank you for contributing!
