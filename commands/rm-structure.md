---
name: rm-structure
description: Explain openEHR Reference Model structural concepts in a given domain (ehr or demographic) — composition categories, ISM states, time, versioning, PARTY hierarchy, identities, privacy, etc.
argument-hint: "<domain: ehr | demographic> <concept>"
allowed-tools:
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
---

# /rm-structure

Explain openEHR Reference Model structural concepts. The first argument selects the RM domain; the second names the concept to explain.

## Instructions

1. Parse **$ARGUMENTS** into `<domain>` (first token) and `<concept>` (remainder).
2. Load the RM spec digest for the selected domain:
   - `ehr` → `guide_get("specs/rm-ehr")`
   - `demographic` → `guide_get("specs/rm-demographic")`
3. Use `type_specification_get` to look up specific RM types if the user needs class-level detail (attributes, functions, invariants).
4. Present a structured explanation covering:
   - Definition and purpose of the concept
   - Key components or states (tables/trees where appropriate)
   - How it relates to other RM structures (and, where relevant, the other domain)
   - Practical implications for modeling, querying, or deployment

## Concept Areas by Domain

### `ehr` — EHR Information Model
- **ehr-parts** — Root EHR object, EHR_ACCESS, EHR_STATUS, Compositions, Folders, Tags, Contributions
- **composition-categories** — event, persistent, episodic: semantics, use cases, querying implications
- **entry-types** — OBSERVATION, EVALUATION, INSTRUCTION, ACTION, ADMIN_ENTRY: clinical statement mapping
- **ism-states** — Instruction State Machine: INITIAL → PLANNED → SCHEDULED → ACTIVE → COMPLETED/ABORTED/CANCELLED
- **time** — Observation time, healthcare event time, commit time, domain-specific times
- **versioning** — VERSIONED_OBJECT, VERSION (3-part UID), CONTRIBUTION, lifecycle states, audit, attestation
- **cross-cutting** — LOCATABLE, PARTY_PROXY, feeder audit, tags

### `demographic` — Demographic Model
- **party-hierarchy** — PARTY → ACTOR (PERSON, ORGANISATION, GROUP, AGENT) and ROLE
- **roles** — ROLE as PARTY subtype, performer reference, CAPABILITY, credentials, time_validity
- **identities** — PARTY_IDENTITY (names) vs PARTY.details (state-issued identifiers); CONTACT and ADDRESS
- **relationships** — PARTY_RELATIONSHIP: directionality, source/target, serialisation safety
- **privacy** — EHR/demographic separation, PARTY_PROXY subtypes, 3 identification levels, EHR Index
- **versioning** — VERSIONED_PARTY, same change control as EHR, lifecycle states
- **archetyping** — Archetypable structures: PARTY.details, PARTY_IDENTITY.details, ADDRESS.details, CAPABILITY.credentials

## Notes

- If the user omits the domain, infer it from the concept keyword (e.g. "composition" → ehr, "party" → demographic) and state the inference up-front.
- For broader RM sub-domains covered by the `specs/` category (Common, Data Structures, Data Types, Integration, EHR Extract, Support), route the user to `/guide specs/<component>-<doc>` instead — this command scopes to the two primary information-model domains.
