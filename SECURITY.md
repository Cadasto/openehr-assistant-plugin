# Security Policy

## Threat Model

This repository distributes **AI-assistant instruction content** — a plugin of skills, commands, agents, hooks, manifests, and a bundled MCP connection config (`.mcp.json`). The relevant security concerns are therefore about content integrity and the supply chain, rather than classic software vulnerabilities:

- **Malicious or manipulative skill/command/agent content** — instructions in a `SKILL.md`, a command, an agent file, or its `references/` designed to make an AI assistant exfiltrate data, execute harmful commands, or act against the user's interest (prompt injection via plugin content).
- **Manifest tampering** — a `plugin.json` pointing at unexpected sources or misrepresenting plugin identity.
- **MCP-endpoint tampering** — the bundled `.mcp.json` ships a default server URL. A modified `.mcp.json` (or a malicious override) could redirect the assistant to an attacker-controlled MCP server that returns harmful tool results. Verify the endpoint before trusting tool output.
- **Typosquatting** — plugin, skill, or command names crafted to impersonate the official openEHR Assistant plugins.
- **Malicious hook scripts** — `hooks/session-start.sh` (or any future hook) performing unexpected, mutating, or network operations. Hooks here must stay read-only reconnaissance.
- **Malicious external references** — content linking to harmful or impersonating external resources.

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports.

- Use GitHub's private vulnerability reporting: **Security → Report a vulnerability** on this repository.
- Alternatively, contact the repository maintainers directly.

You can expect an acknowledgement within 7 days. Confirmed issues are fixed in a new release and noted in the [CHANGELOG](CHANGELOG.md).

## Supported Versions

Only the **latest released version** (latest `vX.Y.Z` tag) is supported. Keep the plugin updated via your assistant's update mechanism — for example `/plugin update openehr-assistant` in Claude Code.

## Out of Scope

- Vulnerabilities in Claude Code, Cursor, or other AI assistants themselves — report to the respective vendor (for example [Anthropic](https://www.anthropic.com/security)).
- Vulnerabilities in the companion [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server or the maintainer [openehr-assistant-dev-plugin](https://github.com/cadasto/openehr-assistant-dev-plugin) — report on those repositories.
- Issues in the openEHR specifications — raise via the [openEHR Jira](https://openehr.atlassian.net/) (SPEC* projects).
