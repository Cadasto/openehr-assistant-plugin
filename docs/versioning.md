# Versioning and Releases

This plugin is versioned with [semver](https://semver.org), adapted to skill/command/agent content:

| Bump | When |
|------|------|
| **Major** | A skill/command/agent is removed or renamed, or its behaviour/scope changes incompatibly |
| **Minor** | A new skill/command/agent is added, or an existing one's coverage meaningfully expands |
| **Patch** | Typos, clarifications, reference fixes — no behaviour change |

## Release steps

1. Bump `version` in **both** manifests (they must agree): `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Keep `description` and `author` identical across both.
2. Run `./scripts/validate.sh` (checks dual-host parity; warns and skips if Python is absent) and `claude plugin validate .`.
3. Fold the accumulated `## [Unreleased]` notes into a dated `## [X.Y.Z]` section in [CHANGELOG.md](../CHANGELOG.md) (Keep a Changelog format — see [AGENTS.md](../AGENTS.md#changelog-style)).
4. Commit (`chore(release): vX.Y.Z`) and tag: `git tag -a vX.Y.Z -m "openEHR Assistant Plugin vX.Y.Z"`.
5. Push commits and the tag: `git push origin main --follow-tags`.

## MCP compatibility

This plugin is built and tested against a specific [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server version (currently tracked in [AGENTS.md](../AGENTS.md#companion-mcp-server) and [README.md](../README.md)). When the server adds, renames, or removes tools / guide URIs / example kinds, align this plugin in the same release — see [CONTRIBUTING.md](../CONTRIBUTING.md#when-bumping-openehr-assistant-mcp-compatibility) for the full checklist (tool ids in `allowed-tools`, guide URIs, bundled offline archetype corpus).

## Marketplace

This plugin is listed in the separate [cadasto/plugin-marketplace](https://github.com/cadasto/plugin-marketplace) repo via a GitHub `source`, so the marketplace always tracks `main` — no version pin to bump there. Only update the marketplace when the plugin's `name`, `description`, or `repo` changes.
