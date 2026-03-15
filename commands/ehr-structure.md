---
name: ehr-structure
description: Explain EHR structural concepts: composition categories, ISM states, time semantics, versioning, entry types
argument-hint: "<concept: composition-categories | ism-states | time | versioning | entry-types | ehr-parts | ...>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# /ehr-structure

Explain openEHR EHR structural concepts.

## Instructions

1. Load the EHR information model guide:
   ```
   guide_get("rm/ehr-information-model")
   ```
2. Identify which concept the user is asking about: **$ARGUMENTS**
3. Use `type_specification_get` to look up specific RM types if the user needs class-level detail
4. Present a structured explanation covering:
   - Definition and purpose of the concept
   - Key components or states (tables where appropriate)
   - How it relates to other EHR structures
   - Practical implications for modeling or querying

## Concept Areas

- **ehr-parts** — Root EHR object, EHR_ACCESS, EHR_STATUS, Compositions, Folders, Tags, Contributions
- **composition-categories** — event, persistent, episodic: semantics, use cases, querying implications
- **entry-types** — OBSERVATION, EVALUATION, INSTRUCTION, ACTION, ADMIN_ENTRY: clinical statement mapping
- **ism-states** — Instruction State Machine: INITIAL → PLANNED → SCHEDULED → ACTIVE → COMPLETED/ABORTED/CANCELLED
- **time** — Observation time, healthcare event time, commit time, domain-specific times
- **versioning** — VERSIONED_OBJECT, VERSION (3-part UID), CONTRIBUTION, lifecycle states, audit, attestation
- **cross-cutting** — LOCATABLE, PARTY_PROXY, feeder audit, tags
