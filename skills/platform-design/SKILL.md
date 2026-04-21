---
name: platform-design
description: >
  This skill should be used when the user asks to "design platform services",
  "plan EHR service integration", "design contribution workflows",
  "plan versioning strategy", "design against openEHR services",
  or "understand platform architecture".
  Covers designing against openEHR platform service interfaces,
  REST API patterns, version update semantics, and contribution workflows.
argument-hint: "<task: design|review|explain> [service or use-case]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# Platform Design

## Step 1: Load Guides (MANDATORY)

Before any platform design work, load the authoritative guides:

```
guide_get("specs/sm-openehr_platform")
guide_get("specs/rm-ehr")
```

Load additional guides as needed:
- `guide_get("specs/rm-demographic")` — if demographic service is in scope

## Step 2: Clarify Scope

Before designing, establish which parts of the platform are involved:

- **Which services are relevant?** (Definitions, EHR, Demographic, Query, Admin, etc.)
- **What is the integration pattern?** (direct CDR access, REST API, middleware)
- Are multiple EHR systems involved, or a single CDR?
- Is demographic data managed within the same platform or via an external system?

## Step 3: Service Interface Guidance

Walk through the relevant service interfaces from the loaded guides:

- **Call conventions**: distinguish queries (read-only, idempotent) from commands (state-changing)
- **CALL_STATUS error codes**: always handle and surface meaningful errors to callers
- **List handling**: use `item_offset` and `items_to_fetch` parameters for paginated result sets
- Use `type_specification_get` to verify the structure of service request/response types when uncertain

Map each integration point to its owning service before proceeding to detailed design.

## Step 4: Version Update Semantics

Model versioned data correctly using the UPDATE_VERSION pattern:

- **Core fields**: `preceding_version_uid`, `lifecycle_state`, `attestations`, `data`, `audit`
- **Concrete UPDATE_VERSION types**:
  - `UV_COMPOSITION` — for EHR compositions
  - `UV_FOLDER` — for EHR directory folders
  - `UV_PARTY` — for demographic party records
- The server creates the CONTRIBUTION and VERSION objects; the client supplies the update payload
- **CONTRIBUTION as atomic change-set**: group related version updates into a single CONTRIBUTION to ensure consistency — a CONTRIBUTION either fully commits or fully rolls back

## Step 5: OpenAPI Reference

For exact REST endpoint details, fetch the relevant OpenAPI schema:

https://github.com/openEHR/specifications-ITS-REST/tree/master/computable/OAS

| Schema | Service |
|--------|---------|
| `ehr-validation.openapi.yaml` | EHR, Composition, Directory, Contribution |
| `demographic-validation.openapi.yaml` | Person, Organisation, Group, Agent, Role |
| `definition-validation.openapi.yaml` | Templates, Stored Queries |
| `query-validation.openapi.yaml` | AQL execution |
| `admin-validation.openapi.yaml` | Admin operations |
| `system-validation.openapi.yaml` | Service discovery |
| `overview-validation.openapi.yaml` | HTTP conventions |

## Step 6: Deployment Patterns

Apply standard openEHR deployment patterns:

- **5-tier architecture**: presentation, application, service, persistence, terminology — keep tiers loosely coupled
- **Minimal system components**: start with only the services required; add services as requirements grow
- **Service separation**: do not conflate EHR and demographic concerns in the same service boundary
- **EHR Index**: use for cross-referencing EHR identifiers with demographic party identifiers
- **Definitions service**: acts as the runtime repository for archetypes, templates, and stored AQL queries — all other services depend on it at runtime

## Step 7: Design Output

Produce a complete design covering:

- **Identified service interfaces**: list each service and the operations called
- **Data flow diagram**: show how data moves between client, services, and CDR
- **Versioning strategy**: document how UPDATE_VERSION and CONTRIBUTION will be used for each versioned resource
- **Contribution boundaries**: define what constitutes an atomic change-set for each workflow
- **Error handling approach**: map CALL_STATUS codes to application-level responses
