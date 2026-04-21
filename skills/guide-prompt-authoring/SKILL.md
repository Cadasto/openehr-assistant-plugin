---
name: guide-prompt-authoring
description: >
  This skill should be used when the user asks to "create a guide", "write a guide", "add a guide",
  "create a prompt", "write a prompt", "add a prompt", or "author guide/prompt content" for the
  openEHR Assistant MCP server. Covers authoring new implementation guides and MCP prompt files
  in the cadasto/openehr-assistant-mcp repository.
argument-hint: "<type: guide|prompt> <category/name or prompt-name> [topic description]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - mcp__openehr-assistant__guide_search
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Guide & Prompt Authoring

Create new implementation guides (`resources/guides/`) and MCP prompt files (`resources/prompts/` + `src/Prompts/`) for the openEHR Assistant MCP server repository.

## Conflict Resolution

When conventions conflict, apply this priority (highest first):
1. openEHR specification and formal grammar
2. Existing guide style (see `resources/guides/README.md`)
3. Prompt policy split (global policy vs task-specific constraints)
4. Consistency with sibling files in the same category
5. Convenience

## Step 1: Preparation (MANDATORY)

Before writing any content, complete these checks:

### 1a. Identify Scope

Determine what is being authored:
- **Guide** — normative reference content in `resources/guides/{category}/{name}.md`
- **Prompt** — task-specific MCP prompt in `resources/prompts/{name}.md` + PHP class in `src/Prompts/{Name}.php`

### 1b. Check openEHR Specifications

Verify the topic against authoritative sources before writing:
- Load relevant existing guides to understand current coverage:
  ```
  guide_search("<topic keywords>")
  guide_get("<category>/<name>")
  ```
- Check RM/AM type definitions if the topic involves data types or structures:
  ```
  type_specification_get("<type_name>")
  ```
- Verify terminology codes if the topic involves coded content:
  ```
  terminology_resolve("<code or term>")
  ```
- Cross-reference official openEHR specs at `specifications.openehr.org` and any formal grammar in the `docs/` directory of the MCP repo

### 1c. Check for Duplicates

Search existing guides and prompts to avoid overlap:
```
guide_search("<topic>")
```
Also search the local repo:
```
Glob: resources/guides/**/*.md
Glob: resources/prompts/*.md
Grep: "<key concept>" in resources/guides/
```

If an existing guide or prompt covers the topic, prefer editing it over creating a new file.

### 1d. Identify the Category

For **guides**, place the file in the correct category directory:

| Category | Directory | Content Focus |
|----------|-----------|---------------|
| Archetypes | `resources/guides/archetypes/` | Archetype design, ADL syntax, constraints, terminology |
| Templates | `resources/guides/templates/` | Template design, OET/OPT syntax, narrowing |
| AQL | `resources/guides/aql/` | Query language, syntax, patterns |
| Simplified Formats | `resources/guides/simplified_formats/` | Flat/Structured JSON serialization |
| Specifications | `resources/guides/specs/` | openEHR specification digests (250–900 words) covering AM, AM2, BASE, RM, QUERY, TERM, LANG, CDS, SM, ITS-REST; filenames follow `<component>-<doc>.md` (e.g. `rm-ehr.md`, `am2-ADL2.md`); digests track the `development` branch |
| How-Tos | `resources/guides/howto/` | Toolchain how-tos (e.g. `spec-lookup.md` for efficient external spec retrieval) |

The legacy `rm/` category has been retired — its three guides were migrated to `specs/rm-ehr`, `specs/rm-demographic`, and `specs/sm-openehr_platform`. New RM-adjacent digests belong in `specs/`.

**Spec digest schema.** Files in `resources/guides/specs/` follow a specific digest schema (scope, key classes, relations, canonical URLs) and are validated against it. Before authoring, inspect a sibling digest (e.g. `specs/rm-ehr.md`, `specs/am-ADL1.4.md`) and the category's README/validator to match conventions.

For **prompts**, identify the action pattern:

| Pattern | Naming | Example |
|---------|--------|---------|
| Design or review | `design_or_review_{subject}` | `design_or_review_archetype.md` |
| Explain | `explain_{subject}` | `explain_template.md` |
| Explore / browse | `{subject}_explorer` | `guide_explorer.md` |
| Fix / transform | `fix_{subject}` | `fix_adl_syntax.md` |
| Translate | `translate_{subject}` | `translate_archetype_language.md` |

## Step 2: Author a Guide

### 2a. Header Block

Every guide starts with a metadata header **before** the `---` separator:

```markdown
# Title

**Scope:** What this guide covers — one or two sentences.
**Related:** openehr://guides/{category}/{name}, openehr://guides/{category}/{other}
**Keywords:** comma, separated, discovery, terms

---
```

- **Scope** or **Purpose** is required
- **Related** lists canonical `openehr://guides/...` URIs for cross-referenced guides (optional but recommended)
- **Keywords** aids search and discovery (optional but recommended)

### 2b. Section Heading Style

Choose the heading style that fits the document type:

| Document Type | Heading Style | Example |
|---------------|---------------|---------|
| Long normative (rules, standards) | Lettered: A, B, C... | Rules numbered A1, A2, B1... |
| Short reference / cheat sheet | Numeric: 1, 2, 3... | Sections numbered sequentially |
| Principles / overview | Unnumbered short titles | Descriptive headings only |

### 2c. Content Principles

- **Concise and scannable** — content is consumed by AI agents; avoid verbose prose
- **Specification-aligned** — keep wording aligned with authoritative openEHR specs
- **Self-contained** — each guide should make sense on its own while referencing related guides
- **Examples over explanation** — use code blocks to demonstrate patterns
- **No duplicate content** — cross-reference other guides instead of repeating their rules

### 2d. Code Blocks and Checklists

- Use ` ```text ` for prose examples, other language tags when they add value (`adl`, `json`, `sql`)
- Use `☑` for conformance checklists embedded in guides
- Use `- [ ]` for interactive checklist guides (e.g., `checklist.md` files)

### 2e. Standard Guide Types

When creating a new guide, consider which type fits:

| Type | Filename | Purpose |
|------|----------|---------|
| Principles | `principles.md` | Core design philosophy and foundational concepts |
| Rules | `rules.md` | Specific normative rules and constraints |
| Syntax | `syntax.md` or `{format}-syntax.md` | Formal syntax reference |
| Idioms | `idioms-cheatsheet.md` or `{format}-idioms-cheatsheet.md` | Quick-reference patterns and examples |
| Anti-patterns | `anti-patterns.md` | Common mistakes with corrections |
| Checklist | `checklist.md` | Validation checklist for review |
| Terminology | `terminology.md` | Terminology and coding system guidance |
| Constraints | `structural-constraints.md` | Detailed constraint specifications |

## Step 3: Author a Prompt

### 3a. Prompt Markdown File

Create `resources/prompts/{name}.md` following the standard structure:

```markdown
## Role: user

{Task description and instructions for the assistant.}

Ground all decisions on:
- `openehr://guides/{category}/{guide1}`
- `openehr://guides/{category}/{guide2}`

### Workflow

1. {Step 1}
2. {Step 2}
3. {Step 3}

### Required Deliverables

1. {Deliverable 1}
2. {Deliverable 2}

### Conflict Resolution

{Priority hierarchy for resolving ambiguity.}

### Template Variables

- Task type: {{task_type}}
- {Other variables}: {{variable_name}}
```

Key rules:
- Use `## Role: user` to define the system/user message boundary
- Reference specific guides by their `openehr://guides/...` URI
- Include template variables (`{{var}}`) for user-supplied inputs
- Keep task-specific — global policy belongs in `resources/prompts/shared/policy.md`, not here
- Define required deliverables so output structure is predictable

### 3b. Prompt Policy Split

Follow this rule of thumb:
- **`resources/prompts/shared/policy.md`** — global, always-applicable policy (tool discipline, scope control, specification compliance, output standards)
- **`resources/prompts/{name}.md`** — task-specific constraints, required output structure, domain-specialized rules, guide references

Never duplicate shared policy in individual prompt files.

### 3c. PHP Prompt Class

Create `src/Prompts/{PascalName}.php`:

```php
<?php

declare(strict_types=1);

namespace Cadasto\OpenEHR\MCP\Assistant\Prompts;

use Mcp\Attribute\McpPrompt;
use Mcp\Attribute\McpPromptArgument;

#[McpPrompt(
    name: '{name}',
    description: '{Description of what this prompt does}',
)]
class {PascalName} extends AbstractPrompt
{
    public function __invoke(
        #[McpPromptArgument(
            name: '{arg_name}',
            description: '{Argument description}',
            required: true,
        )]
        string $argName,
    ): array {
        return $this->loadPromptMessages('{snake_name}', [
            'arg_name' => $argName,
        ]);
    }
}
```

Key conventions:
- Class name is PascalCase; matches markdown filename converted from snake_case
- Extends `AbstractPrompt` to load messages from YAML/markdown resources via `$this->loadPromptMessages()`
- Use `#[McpPrompt]` and `#[McpPromptArgument]` attributes for MCP discovery
- Pass template variables as the second argument to `loadPromptMessages()`

## Step 4: Quality Review

### 4a. Guide Checklist

Before finalizing a guide, verify:
- [ ] Header block includes Scope/Purpose
- [ ] Related guides are cross-referenced with `openehr://guides/...` URIs
- [ ] Keywords are present for discoverability
- [ ] Section headings follow the appropriate style for the document type
- [ ] Content is specification-aligned (checked against authoritative sources)
- [ ] No content duplicated from other guides — uses cross-references instead
- [ ] Code blocks use appropriate language tags
- [ ] Content is concise and scannable for AI consumption
- [ ] File is placed in the correct category directory
- [ ] Filename follows established naming conventions

### 4b. Prompt Checklist

Before finalizing a prompt, verify:
- [ ] Markdown file uses `## Role: user` section header
- [ ] References specific guides by `openehr://guides/...` URI
- [ ] Includes template variables for user inputs
- [ ] Defines required deliverables for structured output
- [ ] Does not duplicate shared policy from `resources/prompts/shared/policy.md`
- [ ] PHP class extends `AbstractPrompt` and uses `loadPromptMessages()`
- [ ] PHP class attributes (`#[McpPrompt]`, `#[McpPromptArgument]`) are correct
- [ ] Class name (PascalCase) matches markdown filename (snake_case)
- [ ] Arguments match template variables in the markdown file

### 4c. Documentation Sync

After creating new files, update these in the MCP repo:
- `AGENTS.md` — if adding a new prompt or changing resource structure
- `README.md` — if the change affects the public API or capabilities
- Add a PHPUnit test for new prompt classes in `tests/`

## Output

- Guides: write `.md` files to `resources/guides/{category}/{name}.md`
- Prompts: write `.md` to `resources/prompts/{name}.md` and `.php` to `src/Prompts/{PascalName}.php`
- Use the Write tool to create files and Edit tool to modify existing ones
