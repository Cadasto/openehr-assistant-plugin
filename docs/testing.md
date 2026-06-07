# Testing and Validation

This is a pure-content repository — JSON manifests + markdown skills/commands/agents + a shared hook script. There is no build step or package manager. Testing means validating structure, then installing locally and exercising the components against the companion MCP server.

## Validation

- **Manifest / component validation** — `./scripts/validate.sh` (also run by CI on every PR): checks both `plugin.json` manifests, dual-host parity (name/version/description/author agree), declared component paths, the bundled `.mcp.json`, hook-config JSON, and SKILL.md / agent / command frontmatter (including `name` == directory/filename). The wrapper runs `scripts/validate.py`; if Python 3 isn't installed it prints a warning and skips (exit 0) rather than failing — install `python3` for the full local check, or rely on `claude plugin validate .` and CI. CI pins Python so the deep check always runs there.
- **Official validator** — `claude plugin validate .`: checks the manifest and component structure.
- **Structural review** — run the `plugin-dev:plugin-validator` agent after creating or modifying components.
- **Skill quality review** — run the `plugin-dev:skill-reviewer` agent: description-triggering quality, progressive disclosure, content structure.
- **Token cost** — `claude plugin details openehr-assistant` shows the inventory and projected token cost; keep skill/command metadata lean.

## Local triggering tests

Install from your working copy (see [install.md](install.md)), then exercise the components. The plugin expects a reachable openEHR Assistant MCP server (the bundled `.mcp.json` targets the hosted instance; override for a local server — see [install.md](install.md#mcp-wiring)).

- **Commands** — run a representative slash command and confirm it resolves its MCP tools without permission prompts:

  ```
  /archetype-search blood pressure        # CKM discovery
  /guide AQL syntax                        # guide browsing
  /type-spec DV_QUANTITY                   # type lookup
  ```

- **Skill auto-triggering** — mention an openEHR concept in conversation *without* a command (e.g. "help me design a blood pressure archetype") and confirm the relevant skill (`openehr-assistant`, `archetype-authoring`, …) engages and follows the Guide-First principle.
- **Hooks** — open a workspace containing `*.adl` / `*.oet` / `*.opt` files and confirm the `SessionStart` hook prints the openEHR context line. On Claude Code, a `Write`/`Edit` to an `.adl` file should emit the `/archetype-lint` reminder (PostToolUse).

After editing content, reinstall (or restart the session) to pick up changes.

## Releasing

See [versioning.md](versioning.md) for the semver policy, MCP compatibility alignment, and release steps.
