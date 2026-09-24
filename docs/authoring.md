# Skill, command, and agent authoring conventions

This page is for contributors adding or changing a skill, command, or agent: how to name it, where its files go, which component type to choose, and how to write its trigger description and body. It expands on the *how* behind [AGENTS.md](../AGENTS.md) and [CONTRIBUTING.md](../CONTRIBUTING.md#adding-or-modifying-components); where they disagree, AGENTS.md is authoritative.

## Naming

- **Plugin name**: `openehr-assistant`. Claude Code plugin names live in a flat global namespace, so the descriptive name disambiguates it from the maintainer `openehr-assistant-dev` plugin.
- **Skill, command, and agent names**: terse activity nouns, such as `archetype-authoring`, `aql-authoring`, `clinical-modeler`. Skills are namespaced as `<plugin>:<skill>` (`openehr-assistant:archetype-authoring`), so do not repeat the plugin's words in a component name. A component's frontmatter `name` **must** equal its directory (skills) or filename stem (commands and agents); `scripts/validate.py` enforces this.

## Layout

- `skills/<name>/SKILL.md`: one subdirectory per skill, YAML frontmatter + Markdown body. Optional `references/` and `examples/` subdirectories carry bulky supplementary content, as in `skills/openehr-assistant/reference/`.
- `commands/<name>.md`: one file per slash command, YAML frontmatter + body. Reference material never goes under `commands/`. Host validators treat every `commands/**/*.md` as a command, so they mis-detect a reference file there; put it in the consuming skill's `references/` subdirectory instead, as `skills/semantic-diff/references/semantic-diff-rubric.md` does.
- `agents/<name>.md`: one file per agent, YAML frontmatter + system prompt.
- Keep both manifests (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`) in sync.

## Choosing skill vs command vs agent

- **Skill** (the default for new functionality): any multi-step or context-rich workflow. Both hosts have unified commands and skills. A skill is `/`-invocable like a command and takes `argument-hint` / `$ARGUMENTS`; it also auto-triggers from natural language and can carry bulky material in `references/`. Mark `auto-invocable` / `user-invocable` as appropriate.
- **Command**: reserved for a thin, single-interaction wrapper around MCP tools, meaning a lookup or scan that completes in one turn, needs no supporting files, and should not auto-trigger. A command that grows steps or needs a reference file is a skill. Fold it in, as with `/archetype-fix-syntax` → `archetype-authoring` and `/semantic-diff` → the `semantic-diff` skill.
- **Agent**: a context-isolated subagent for heavy or parallel work, such as `ckm-scout` and `spec-researcher`, so the main session's context stays clean.

## The `description` field (the trigger)

For **skills**, the `description` is always-on trigger metadata. It sits in context every session, so keep it **lean (~50–75 words)** and in the third person:

1. **What + scope**: one sentence on what the skill does and when it applies.
2. **Triggers**: "This skill should be used when the user asks to …" with 3–5 *representative* (not exhaustive) actions. More phrases past that add length without improving triggering.
3. **Anti-triggers**: a short "Not for …" that routes overlapping cases to the right place, for example local-file work → the `clinical-modeler` agent, spec lookup → `spec-researcher`.

For **commands**, the `description` is the one-line palette entry; pair it with `argument-hint`.

## Body

- **Guide-First.** Skills and commands instruct the assistant to load the relevant MCP guides (`guide_search` / `guide_get`) before answering. MCP guides are the authoritative knowledge registry; offline references under `skills/openehr-assistant/reference/` are fallbacks only.
- Write in the imperative, and explain *why* a step matters rather than relying on bare `MUST`/`NEVER`. Keep skill bodies focused (~1,000 words); push bulky material to `references/`.
- `allowed-tools` pre-approves `mcp__openehr-assistant__<tool>` ids to avoid permission prompts.
- Stay factual and grounded: do not invent identifiers, paths, or conventions. For openEHR spec detail, retrieve from `specifications.openehr.org` (see [AGENTS.md](../AGENTS.md#retrieving-openehr-specifications)).

## Before committing

Run `./scripts/validate.sh` and `claude plugin validate .`, then test triggering locally; see [testing.md](testing.md). When adding or renaming a component, sync **AGENTS.md**, **README.md**, and **hooks/session-start.sh** (the available-commands list).
