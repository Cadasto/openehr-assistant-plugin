---
name: guide
description: Browse and retrieve openEHR implementation guides
argument-hint: "<topic or guide path>"
allowed-tools:
  - mcp__openehr-assistant__guide_search
  - mcp__openehr-assistant__guide_get
---

# /guide

Browse and retrieve openEHR implementation guides.

## Instructions

1. Use `guide_search` to find guides matching: **$ARGUMENTS**
2. Present available guides with their paths and descriptions
3. Use `guide_get` to load the full content of relevant guides
4. Summarize key points from the guide content

## Available Guide Categories

- `archetypes/` — Principles, rules, ADL syntax, idioms, constraints, terminology, anti-patterns, checklist, formatting
- `templates/` — Principles, rules, OET syntax, idioms, checklist
- `aql/` — Principles, syntax, idioms, checklist
- `simplified_formats/` — Principles, rules, idioms, checklist
- `specs/` — openEHR specification digests (RM, AM, AM2, BASE, QUERY, TERM, LANG, CDS, SM, ITS-REST); tracks the `development` branch
- `howto/` — Toolchain how-tos (e.g. `spec-lookup` for efficient external spec retrieval)
