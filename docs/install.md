# Installing the openEHR Assistant Plugin

This plugin is distributed for both [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins) (`.claude-plugin/`) and [Cursor](https://cursor.com/docs/plugins) (`.cursor-plugin/`). Skill, command, agent, and rule content is shared; only the manifest and hook layer differ.

> This is the **user-facing** plugin — for clinical modelling, AQL, CKM discovery, and specification lookup. If you instead want to *build* the openEHR Assistant tooling (MCP tools, guides, examples), see the maintainer [openehr-assistant-dev](https://github.com/cadasto/openehr-assistant-dev-plugin) plugin.

## Claude Code

### Install (from the Cadasto marketplace)

```
/plugin marketplace add cadasto/plugin-marketplace
/plugin install openehr-assistant@cadasto
```

The marketplace name is `cadasto`, so installed plugins are addressed as `<plugin>@cadasto`.

### Install (local working copy, for development)

```bash
claude plugin add /path/to/openehr-assistant-plugin
```

### Update / inspect

```
/plugin marketplace update cadasto
/plugin update openehr-assistant
```

```bash
claude plugin details openehr-assistant   # component inventory + projected token cost
```

A session restart is required for an update to take effect.

## Cursor

Add this repository as a plugin (Cursor **Settings → Plugins**, via Git URL or local path). The repo root contains `.cursor-plugin/plugin.json`; skills, commands, agents, rules, the bundled MCP config (`.mcp.json`), and the Cursor hook config (`hooks/cursor-hooks.json`) are declared there. After changing content locally, reload or reinstall the plugin so Cursor picks it up.

## MCP wiring

Unlike the maintainer plugin, this plugin **bundles a `.mcp.json`** so it works out of the box: it points at the hosted openEHR Assistant MCP server (`streamable-http`). Skill / command / agent `allowed-tools` reference `mcp__openehr-assistant__*` tools resolved from that server.

To use a **local or `stdio`** MCP server instead, override the bundled config in your host. For server installation, transports, and client-specific configuration, see the [openehr-assistant-mcp — Quick Start](https://github.com/cadasto/openehr-assistant-mcp#quick-start) and [AGENTS.md](../AGENTS.md#repository-layout).

## Subagents & MCP permissions

The plugin's agents (`ckm-scout`, `spec-researcher`, and `clinical-modeler`'s read-only lookups) call MCP tools. Agent frontmatter (`tools:`) grants the *capability*, but your host's **permission policy** must still allow the server — otherwise a subagent can be silently denied CKM/guide access even though the same tools work in the main session.

If you hit that, pre-approve the server in your project's `.claude/settings.json` (the plugin repo already ships this in its own [`.claude/settings.json`](../.claude/settings.json)):

```json
{
  "permissions": {
    "allow": [
      "mcp__openehr-assistant",
      "mcp__plugin_openehr-assistant_openehr-assistant"
    ]
  }
}
```

Both namespaces are listed because the server may be wired as the plugin-bundled one (`mcp__plugin_openehr-assistant_openehr-assistant__*`) or registered directly under its plain name in a project/user `.mcp.json` (`mcp__openehr-assistant__*`). All openEHR Assistant tools are read-only, so allowing the whole server is safe. The agents fail loud with `BLOCKED: …` and route the lookup back to the main session when this isn't in place.

### Mount shape matters for the agents

The same server yields a different tool-id namespace per mount, and agent `tools:` entries are matched **literally**:

| How the server is mounted | Live tool ids |
|---|---|
| Project or user `.mcp.json` under the key `openehr-assistant` | `mcp__openehr-assistant__<tool>` |
| This plugin's bundled `.mcp.json` | `mcp__plugin_openehr-assistant_openehr-assistant__<tool>` |
| claude.ai connector | `mcp__claude_ai_<connector>__<tool>` |

The three agents ship both of the first two forms, so they work under either without configuration. The **connector** shape is named after your connector, so the plugin cannot predict it: under a connector-only mount the agents lose MCP access (and `ckm-scout`, whose `tools:` is MCP-only, is refused with `would be spawned with zero tools`). If that is your setup, register the server in a project `.mcp.json` as well — that is the one mount the agents can rely on:

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

The main session is unaffected either way — only agent `tools:` matching is namespace-sensitive.
