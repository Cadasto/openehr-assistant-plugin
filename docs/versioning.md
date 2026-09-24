# Versioning and releases

This page is for maintainers cutting a release: which version number a change earns, the steps from manifest bump to GitHub release, how a release stays aligned with the MCP server, and how it reaches users through the marketplace. The plugin follows [Semantic Versioning](https://semver.org), adapted to skill, command, and agent content.

**Naming:** git tags and GitHub release titles are exactly `vX.Y.Z`: annotated tags, no bare `X.Y.Z` form, and no descriptive suffix in the release title. The theme belongs in the CHANGELOG section, which doubles as the release notes. CHANGELOG headings stay bare `## [X.Y.Z] - YYYY-MM-DD` per Keep a Changelog.

| Bump | When |
|------|------|
| **Major** | A skill/command/agent is removed or renamed, or its behaviour/scope changes incompatibly |
| **Minor** | A new skill/command/agent is added, or an existing one's coverage meaningfully expands |
| **Patch** | Typos, clarifications, reference fixes; no behaviour change |

## Release steps

1. Bump `version` in **both** manifests (they must agree): `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Keep `description` and `author` identical across both. Update the version badge in [README.md](../README.md) to match.
2. Run `./scripts/validate.sh` (checks dual-host parity; warns and skips if Python is absent) and `claude plugin validate .`.
3. Fold the accumulated `## [Unreleased]` notes into a dated `## [X.Y.Z]` section in [CHANGELOG.md](../CHANGELOG.md) (Keep a Changelog format; see [AGENTS.md](../AGENTS.md#changelog-style)).
4. Commit (`chore(release): vX.Y.Z`) and tag: `git tag -a vX.Y.Z -m "openEHR Assistant Plugin vX.Y.Z"`.
5. Push commits and the tag: `git push origin main --follow-tags`.
6. Create the GitHub release from the tag, titled exactly `vX.Y.Z`, with the new CHANGELOG section as the notes body. `-F -` reads that body from standard input. Set `VER` to the release being tagged (for example `0.9.1`); the heading match and the tag both use it:

   ```bash
   VER=0.9.1
   awk -v ver="$VER" '
     $0 ~ "^## \\[" ver "\\]" {f=1; next}
     /^## \[/ {f=0}
     f
   ' CHANGELOG.md | gh release create "v$VER" --title "v$VER" -F -
   ```
7. **Update the marketplace entry.** The release is not live until this lands; see [Marketplace](#marketplace).

## MCP compatibility

Each plugin release is built and tested against a specific [openehr-assistant-mcp](https://github.com/cadasto/openehr-assistant-mcp) server version, currently tracked in [AGENTS.md](../AGENTS.md#companion-mcp-server) and [README.md](../README.md) (the compatibility note and the `openehr-assistant-mcp` badge). When the server adds, renames, or removes tools, guide URIs, or example kinds, align this plugin in the same release. [CONTRIBUTING.md](../CONTRIBUTING.md#when-bumping-openehr-assistant-mcp-compatibility) has the full checklist: tool ids in `allowed-tools`, guide URIs, and the bundled offline archetype corpus.

## Marketplace

This plugin is listed in the separate [Cadasto/plugin-marketplace](https://github.com/Cadasto/plugin-marketplace) repository as `openehr-assistant@cadasto`. The catalog **pins every entry to a release tag**, so tagging and pushing a release here does not ship it: users see nothing until the marketplace entry moves.

After step 6, update the entry in `Cadasto/plugin-marketplace`:

1. Bump that entry's `version` to `X.Y.Z` and `source.ref` to `vX.Y.Z` together (validation there rejects a mismatch).
2. Bump the catalog's own `metadata.version`: a plugin minor or major is a catalog **minor**, a plugin patch is a catalog **patch**.
3. Add a dated `## [X.Y.Z] - YYYY-MM-DD` section in the catalog `CHANGELOG.md`, then run `python3 scripts/validate.py --fix`.

See the catalog's [docs/versioning.md](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/versioning.md).

The catalog copies `description`, `version`, and `keywords` verbatim from `.claude-plugin/plugin.json`. Fix those in this repository and copy them into the catalog when the next release is pinned.
