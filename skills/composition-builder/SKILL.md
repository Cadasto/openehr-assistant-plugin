---
name: composition-builder
description: >
  Use when building, validating, or converting openEHR compositions
  in FLAT, STRUCTURED, or CANONICAL format.
auto-invocable: true
user-invocable: true
argument-hint: "<template-id> [format: flat|structured|canonical]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# Composition Builder

## Step 1: Load Guides (MANDATORY)

Before building any composition, load the authoritative guides:

```
guide_get("simplified_formats/principles")
guide_get("simplified_formats/rules")
guide_get("simplified_formats/idioms-cheatsheet")
```

## Step 2: Retrieve Template

Load the target template to understand the structure:

```
ckm_template_get("<template-id>")
```

This reveals the archetype structure, constraints, and required fields.

## Step 3: Choose Format

### FLAT Format
Pipe-delimited paths with value suffixes. Best for simple integrations and form submissions.

```json
{
  "ctx/language": "en",
  "ctx/territory": "NL",
  "ctx/composer_name": "Dr. Smith",
  "vitals/body_temperature/any_event/temperature|magnitude": 37.2,
  "vitals/body_temperature/any_event/temperature|unit": "Cel"
}
```

Key suffixes: `|magnitude`, `|unit`, `|code`, `|value`, `|terminology`, `|name`

### STRUCTURED Format
Nested JSON mirroring the archetype hierarchy. Best for complex UIs and programmatic construction.

```json
{
  "ctx": { "language": "en", "territory": "NL" },
  "vitals": {
    "body_temperature": [{
      "any_event": [{
        "temperature": [{ "|magnitude": 37.2, "|unit": "Cel" }]
      }]
    }]
  }
}
```

### CANONICAL Format
Full Reference Model representation with `_type` annotations. Best for archival and CDR interactions.

```json
{
  "_type": "COMPOSITION",
  "archetype_details": { ... },
  "content": [{
    "_type": "OBSERVATION",
    "data": { ... }
  }]
}
```

## Step 4: Composition Metadata

Every composition requires:
- **composer**: Who created the data (name, optionally ID)
- **language**: ISO 639-1 code (e.g., `en`, `nl`)
- **territory**: ISO 3166-1 code (e.g., `NL`, `US`)
- **category**: `event` (point-in-time) or `persistent` (ongoing)
- **context**: `start_time` and `setting` (e.g., `primary medical care`, `secondary medical care`)

## Step 5: RM Data Types

Use `type_specification_get` for detailed type structure when needed.

| RM Type | Example Use | Key Fields |
|---------|------------|------------|
| DV_TEXT | Free text | `value` |
| DV_CODED_TEXT | Coded values | `value`, `defining_code` (terminology_id + code_string) |
| DV_QUANTITY | Measurements | `magnitude`, `units`, optionally `precision` |
| DV_DATE_TIME | Timestamps | ISO 8601 value |
| DV_ORDINAL | Ordered scales | `value` (integer), `symbol` (DV_CODED_TEXT) |
| DV_BOOLEAN | True/false | `value` |
| DV_COUNT | Counts | `magnitude` |
| DV_PROPORTION | Ratios/percentages | `numerator`, `denominator`, `type` |
| DV_DURATION | Time periods | ISO 8601 duration (e.g., `P2D`, `PT4H`) |
| DV_IDENTIFIER | External IDs | `id`, `type`, `issuer`, `assigner` |
| DV_URI | URIs/URLs | `value` |
| DV_PARSABLE | Structured text | `value`, `formalism` |

## Step 6: Validation

Before finalizing a composition, verify:
- [ ] All required fields are present (check template constraints)
- [ ] Cardinality constraints are met (min/max occurrences)
- [ ] `_type` annotations are correct (CANONICAL format)
- [ ] Terminology codes are valid (use `terminology_resolve` if needed)
- [ ] Date/time values are valid ISO 8601
- [ ] Quantity units match archetype constraints
- [ ] Composition metadata is complete (composer, language, territory, category)
