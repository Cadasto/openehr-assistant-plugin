---
name: ckm-search
description: Search the openEHR Clinical Knowledge Manager (CKM) for archetypes or templates
argument-hint: "[archetype|template] <search query> [rm:<RM_CLASS>]"
allowed-tools:
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
---

# /ckm-search

Search the openEHR Clinical Knowledge Manager for reusable archetypes or templates. **Reuse first**: prefer published CKM artefacts over authoring new ones.

## Instructions

1. Parse **$ARGUMENTS**:
   - If it starts with `archetype` or `template`, that keyword selects the kind; the rest is the query.
   - Otherwise infer the kind from the query (a whole-form / document concept usually means a template; a single clinical concept usually means an archetype). When unclear, **search archetypes by default** and offer to search templates too.
   - If the query is ambiguous, ask 1-2 clarifying questions before searching.
   - Never invent CIDs, archetype IDs, or template metadata.
2. Search:
   - **Archetypes** → `ckm_archetype_search`. To scope to a structural class, pass the optional **`rmClass`** filter (e.g. `COMPOSITION`, `OBSERVATION`, `CLUSTER`) — surface it when the user wants only siblings of one RM type, or parses `rm:<RM_CLASS>` from `$ARGUMENTS`. If recall is low, retry with broader or alternative phrasings (synonyms, drop qualifiers) — CKM matches against all search words.
   - **Templates** → `ckm_template_search`.
3. Present up to 15 candidates as a table, and state the envelope's `total` (matches before the result cap) so a capped list does not read as the whole result set:
   - Archetypes: CID, Archetype ID, RM Type, Version, Status — highlight published vs draft.
   - Templates: CID, Display Name, Status.
4. Ask the user to select a candidate, and the preferred output format:
   - Archetype: ADL (default), XML, or mindmap.
   - Template: OET (design-time, default) or OPT (operational, flattened constraints).
5. Retrieve the selection with `ckm_archetype_get` or `ckm_template_get`, passing the **CID from the search hit** (`ckm_archetype_get` also accepts a full `openEHR-…` archetype-id; a concept or display name is rejected). Present it in a code block with a brief explanation:
   - **Archetype**: purpose and clinical concept; use/misuse guidance; key sections and notable constraints. Use `guide_adl_idiom_lookup` to explain ADL patterns if needed.
   - **Template**: design intent and clinical context; archetypes used and their roles; notable constraints and narrowing decisions. For an OET, optionally use `ckm_archetype_get` on referenced archetypes for context.
