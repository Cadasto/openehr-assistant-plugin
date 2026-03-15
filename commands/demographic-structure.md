---
name: demographic-structure
description: Explain demographic model concepts: PARTY hierarchy, roles, identities, relationships, privacy patterns
argument-hint: "<concept: party-hierarchy | roles | identities | relationships | privacy | versioning | ...>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# /demographic-structure

Explain openEHR demographic model concepts.

## Instructions

1. Load the demographic model guide:
   ```
   guide_get("rm/demographic-model")
   ```
2. Identify which concept the user is asking about: **$ARGUMENTS**
3. Use `type_specification_get` to look up specific RM types if the user needs class-level detail
4. Present a structured explanation covering:
   - Definition and purpose of the concept
   - Key components or relationships (tables/trees where appropriate)
   - How it relates to EHR structures and privacy
   - Practical implications for modeling or deployment

## Concept Areas

- **party-hierarchy** — PARTY → ACTOR (PERSON, ORGANISATION, GROUP, AGENT) and ROLE
- **roles** — ROLE as PARTY subtype, performer reference, CAPABILITY, credentials, time_validity
- **identities** — PARTY_IDENTITY (names) vs PARTY.details (state-issued identifiers); CONTACT and ADDRESS
- **relationships** — PARTY_RELATIONSHIP: directionality, source/target, serialisation safety
- **privacy** — EHR/demographic separation, PARTY_PROXY subtypes, 3 identification levels, EHR Index
- **versioning** — VERSIONED_PARTY, same change control as EHR, lifecycle states
- **archetyping** — Archetypable structures: PARTY.details, PARTY_IDENTITY.details, ADDRESS.details, CAPABILITY.credentials
