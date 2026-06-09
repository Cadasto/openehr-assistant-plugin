# Skill, Command, and Agent Authoring Conventions

The detailed companion to [AGENTS.md](../AGENTS.md) and [CONTRIBUTING.md](../CONTRIBUTING.md#adding-or-modifying-components). AGENTS.md is authoritative; this expands on the *how*.

## Naming

- **Plugin name**: `openehr-assistant` — Claude Code plugin names live in a flat global namespace, so the descriptive name disambiguates it from the maintainer `openehr-assistant-dev` plugin.
- **Skill / command / agent names**: terse activity nouns (e.g. `archetype-authoring`, `aql-authoring`, `clinical-modeler`). Skills are namespaced as `<plugin>:<skill>` (`openehr-assistant:archetype-authoring`), so don't repeat the plugin's words in a component name. A component's frontmatter `name` **must** equal its directory (skills) or filename stem (commands/agents) — `scripts/validate.py` enforces this.

## Layout

- `skills/<name>/SKILL.md` — one subdirectory per skill, YAML frontmatter + markdown body. Optional `references/` and `examples/` subdirectories for bulky supplementary content (e.g. `skills/openehr-assistant/reference/`, `…/examples/`).
- `commands/<name>.md` — one file per slash command, YAML frontmatter + body. Shared command reference material lives in the top-level `references/` directory (e.g. `references/semantic-diff-rubric.md`), **not** under `commands/` — host validators treat every `commands/**/*.md` as a command, so a reference file there is mis-detected.
- `agents/<name>.md` — one file per agent, YAML frontmatter + system prompt.
- Keep both manifests (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`) in sync.

## Choosing skill vs command vs agent

- **Command** — a thin, single-interaction wrapper around MCP tools for a focused task. Use `$ARGUMENTS` for input and `argument-hint` in frontmatter. Keep instructions concise; the command should complete in one turn.
- **Skill** — a multi-step, context-rich workflow that may span several turns and load multiple guides. Mark `auto-invocable` / `user-invocable` as appropriate.
- **Agent** — a context-isolated subagent for heavy or parallel work (e.g. `ckm-scout`, `spec-researcher`) so the main session's context stays clean.

## The `description` field (the trigger)

For **skills**, the `description` is always-on trigger metadata — it sits in context every session, so keep it **lean (~50–75 words)**, third person:

1. **What + scope** — one sentence: what the skill does and when it applies.
2. **Triggers** — "This skill should be used when the user asks to …" with 3–5 *representative* (not exhaustive) actions. More phrases past that add length without improving triggering.
3. **Anti-triggers** — a short "Not for …" that routes overlapping cases to the right place (e.g. local-file work → the `clinical-modeler` agent; spec lookup → `spec-researcher`).

For **commands**, the `description` is the one-line palette entry; pair it with `argument-hint`.

## Body

- **Guide-First.** Skills and commands instruct the assistant to load the relevant MCP guide(s) (`guide_search` / `guide_get`) before answering. MCP guides are the authoritative knowledge registry; offline references under `skills/openehr-assistant/reference/` are fallbacks only.
- Imperative voice; explain *why* a step matters rather than relying on bare `MUST`/`NEVER`. Keep skill bodies focused (~1,000 words); push bulky material to `references/`.
- `allowed-tools` pre-approves `mcp__openehr-assistant__<tool>` ids to avoid permission prompts.
- Stay factual and grounded — do not invent identifiers, paths, or conventions. For openEHR spec detail, retrieve from `specifications.openehr.org` (see [AGENTS.md](../AGENTS.md#retrieving-openehr-specifications)).

## Before committing

Run `./scripts/validate.sh` and `claude plugin validate .`, then test triggering locally — see [testing.md](testing.md). When adding or renaming a component, sync **AGENTS.md**, **README.md**, and **hooks/session-start.sh** (the available-commands list).
