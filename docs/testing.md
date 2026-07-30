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
  /ckm-search blood pressure               # CKM discovery (archetypes or templates)
  /openehr-explain DV_QUANTITY             # type / archetype / RM-concept / idiom / terminology lookup
  /semantic-diff old.adl new.adl           # version-bump / sibling diff
  ```

  Guide browsing has no command — ask in natural language ("show me the AQL syntax guide") and the auto-invoked `openehr-assistant` skill loads it via `guide_search` / `guide_get`.

  If a command (or a dispatched subagent) reports an MCP tool "denied", that's a host permission-policy gap, not a missing server — add the `permissions.allow` snippet (see [install.md](install.md#subagents--mcp-permissions)).

  If the tools, prompts, or guides a **self-hosted** server advertises look stale (a guide the release notes added is missing, an argument the new schema rejects still passes), the server's discovery cache is stale, not the plugin: since MCP v0.20.0 that cache is namespaced by `APP_VERSION`, so an upgrade without a version bump keeps serving the old capability ads — clear it server-side (see the MCP repo's `docs/development.md` → "Gotcha — MCP discovery cache"). The hosted instance in the bundled `.mcp.json` is unaffected.

- **Skill auto-triggering** — mention an openEHR concept in conversation *without* a command (e.g. "help me design a blood pressure archetype", or "lint this archetype" → `archetype-lint`) and confirm the relevant skill (`openehr-assistant`, `archetype-authoring`, `archetype-lint`, …) engages and follows the Guide-First principle. Skills are also `/`-invocable (e.g. `/archetype-lint`).
- **Hooks** — open a workspace containing `*.adl` / `*.oet` / `*.opt` files and confirm the `SessionStart` hook prints the openEHR context line. On Claude Code, a `Write`/`Edit` to an `.adl` file should emit the `/archetype-lint` reminder (PostToolUse).

After editing content, reinstall (or restart the session) to pick up changes.

## Releasing

See [versioning.md](versioning.md) for the semver policy, MCP compatibility alignment, and release steps.
