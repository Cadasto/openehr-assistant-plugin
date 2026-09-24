# Testing and validation

This page is for contributors checking a change before they open a pull request: which validators to run, and how to exercise the components by hand against the companion MCP server. The repository holds only content (JSON manifests, Markdown skills, commands, and agents, and shared hook scripts), with no build step and no package manager. Testing means validating structure, then loading a working copy and trying the components.

## Validation

- **Manifest and component validation**: `./scripts/validate.sh`, also run by CI on every pull request. It checks both `plugin.json` manifests, dual-host parity (name, version, description, and author agree), declared component paths, the bundled `.mcp.json`, hook-config JSON, and SKILL.md, agent, and command frontmatter (including `name` == directory/filename). The wrapper runs `scripts/validate.py`; if Python 3 is not installed it prints a warning and skips (exit 0) rather than failing. Install `python3` for the full local check, or rely on `claude plugin validate .` and CI. CI pins Python, so the deep check always runs there.
- **Official validator**: `claude plugin validate .` checks the manifest and component structure.
- **Prose lint**: `vale sync`, then `vale --minAlertLevel=error .`, with the repository's [`.vale.ini`](../.vale.ini). The CI `prose` job runs the same commands on Vale 3.18.0 and fails on errors only.
- **Structural review**: run the `plugin-dev:plugin-validator` agent after creating or modifying components.
- **Skill quality review**: run the `plugin-dev:skill-reviewer` agent for description-triggering quality, progressive disclosure, and content structure.
- **Token cost**: `claude plugin details openehr-assistant` shows the inventory and projected token cost; keep skill and command metadata lean.

## Local triggering tests

Load your working copy (see [install.md](install.md)), then exercise the components. The plugin expects a reachable openEHR Assistant MCP server: the bundled `.mcp.json` targets the hosted instance, and you can override it for a local server (see [install.md](install.md#mcp-wiring)).

- **Commands**: run a representative slash command and confirm it resolves its MCP tools without permission prompts:

  ```text
  /ckm-search blood pressure               # CKM discovery (archetypes or templates)
  /openehr-explain DV_QUANTITY             # type / archetype / RM-concept / idiom / terminology lookup
  /archetype-impact openEHR-EHR-OBSERVATION.blood_pressure.v2   # workspace impact scan
  ```

  Guide browsing has no command. Ask in natural language ("show me the AQL syntax guide") and the auto-invoked `openehr-assistant` skill loads it via `guide_search` / `guide_get`.

  If a command (or a dispatched subagent) reports an MCP tool as denied, the server is present and the host's permission policy is blocking it. Add the `permissions.allow` snippet from [install.md](install.md#subagents-and-mcp-permissions).

  If the tools, prompts, or guides a **self-hosted** server advertises look stale (a guide the release notes added is missing, or an argument the new schema rejects still passes), the server's discovery cache is out of date, not the plugin. Since MCP v0.20.0 that cache is namespaced by `APP_VERSION`, so an upgrade without a version bump keeps serving the old capability ads. Clear it server-side, as the MCP discovery cache gotcha in the MCP repository's `docs/development.md` describes. The hosted instance in the bundled `.mcp.json` is unaffected.

- **Skill auto-triggering**: describe a task in conversation *without* a command, and confirm the skill engages and follows the Guide-First principle:

  | Say this | Expect |
  |----------|--------|
  | help me design a blood pressure archetype | `archetype-authoring` |
  | lint this archetype | `archetype-lint` |
  | this archetype won't parse | `archetype-authoring`, fix-syntax mode |
  | sketch a template from this form | `template-authoring` |
  | compare these two archetypes | `semantic-diff` |

  Skills are `/`-invocable too: `/archetype-lint`, `/semantic-diff old.adl new.adl`.
- **Hooks**: open a workspace containing `*.adl` / `*.oet` / `*.opt` files and confirm the `SessionStart` hook prints the openEHR context line. On Claude Code, a `Write` or `Edit` to an `.adl` file should emit the `/archetype-lint` reminder (PostToolUse).

After editing content, restart the session to pick it up: the host reads a plugin's components at launch.

## Releasing

See [versioning.md](versioning.md) for the SemVer policy, MCP compatibility alignment, and release steps.
