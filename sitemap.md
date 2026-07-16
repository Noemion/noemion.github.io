# Noemion Public Discovery

Version: 3

Noemion publishes its current project portal, architecture, specifications, component boundaries, development status, the Endem application, and manuals as canonical HTML pages. This Markdown index provides a compact discovery surface for readers and automated tools.

## Discovery surfaces

- [Project portal](https://noemion.github.io/index.html) — project purpose, boundaries, current status, and reading paths
- [Markdown discovery index](https://noemion.github.io/sitemap.md) — this document

## Project and background

- [Project background](https://noemion.github.io/about/index.html) — why natural-language intent needs a reviewable goal artifact, what Noemion studies, adjacent-system boundaries, and current limits
- [Background and boundaries](https://noemion.github.io/about/background.html) — why natural-language goals need a separate identity and trust boundary
- [Intellectual foundations](https://noemion.github.io/about/intellectual-foundations.html) — turning philosophical distinctions into testable developer questions without treating philosophy as a software specification
- [Frequently asked questions](https://noemion.github.io/faq/index.html) — direct answers about scope, status, and non-goals

## Architecture and components

- [Architecture](https://noemion.github.io/architecture/index.html) — trace one developer task through responsibility owners, stop conditions, artifacts, sessions, evidence, and decisions
- [Endem lifecycle](https://noemion.github.io/architecture/endem-lifecycle.html) — source, deterministic formation, closure, evidence, loading, and execution boundaries
- [Architecture decisions](https://noemion.github.io/architecture/decisions.html) — accepted responsibility boundaries and explicitly unfrozen interfaces
- [Agent system boundaries](https://noemion.github.io/architecture/agent-system-boundaries.html) — one Agent call separates goals, actors, authorization, sessions, external facts, evidence, and decisions
- [ADR-0008](https://noemion.github.io/architecture/adr-0008-endem-system.html) — historical record retaining Endem, `.endem`, and one application entry while routing retired terms to current decisions
- [ADR-0009](https://noemion.github.io/architecture/adr-0009-propositional-kernel.html) — historical record retaining expression, meaning, situation, goal, criteria, and uncertainty separation while retiring the earlier field names and states
- [ADR-0010](https://noemion.github.io/architecture/adr-0010-native-lexicon.html) — current native lexicon, six semantic facets, and situation/goal/evidence separation
- [ADR-0011](https://noemion.github.io/architecture/adr-0011-endem-container.html) — experimental byte boundary and ordered reading path across END-FMT, structural P0, source-bearing P1, and the undefined release Profile
- [ADR-0012](https://noemion.github.io/architecture/adr-0012-rust-core-language.html) — bounded historical language evidence and the conditional Rust review baseline for a future Ktisor structural core
- [ADR-0013](https://noemion.github.io/architecture/adr-0013-end-p1-payload.html) — source-bearing formation Profile, ordered validation path, closed references, and non-publishable boundary
- [ADR-0014](https://noemion.github.io/architecture/adr-0014-source-manifest.html) — experimental source manifest, semantic-confirmation boundary, deterministic mapping, and removal conditions
- [ADR-0015](https://noemion.github.io/architecture/adr-0015-result-domains.html) — five non-interchangeable result domains, producer boundaries, allowed decisions, and external-state mappings
- [ADR-0016](https://noemion.github.io/architecture/adr-0016-mene-time-model.html) — time evidence for sustained goals, explicit continuity budgets, coverage gaps, and external task boundaries
- [ADR-0017](https://noemion.github.io/architecture/adr-0017-negation-and-absence.html) — explicit negative relations, query-relative absence, closed observation evidence, and external tool boundaries
- [ADR-0018](https://noemion.github.io/architecture/adr-0018-quantification-and-membership.html) — authoritative member scopes, distinct identities, decisive cardinality evidence, and paginated Agent-list boundaries
- [ADR-0019](https://noemion.github.io/architecture/adr-0019-measurement-and-thresholds.html) — measurement constructs and populations, replayable procedures, scoped terminology, uncertainty, and threshold comparison
- [ADR-0020](https://noemion.github.io/architecture/adr-0020-composite-situations-and-criteria.html) — composite situations, aligned criteria, four-result propagation, and decisive short-circuit evidence
- [ADR-0021](https://noemion.github.io/architecture/adr-0021-synem-closure-and-activation.html) — exact Synem closure, permission convergence, member result separation, and session activation
- [ADR-0022](https://noemion.github.io/architecture/adr-0022-iknem-evidence-and-appraisal.html) — scoped Iknem evidence, provenance, validity, coverage, appraisal, decision, and disclosure boundaries
- [ADR-0023](https://noemion.github.io/architecture/adr-0023-endem-content-standard.html) — layered Endem content standard, closed content Profiles, container rules, and conformance boundaries
- [ADR-0024](https://noemion.github.io/architecture/adr-0024-dromen-session-contract.html) — one-session subject, policy, environment, capability, budget, observation, immutability, and disposal contract
- [ADR-0025](https://noemion.github.io/architecture/adr-0025-structured-diagnostics.html) — stable diagnostic identity, context, layers, locations, recovery, disclosure, bounds, and atomic failure
- [ADR-0026](https://noemion.github.io/architecture/adr-0026-external-protocol-adapters.html) — protocol-independent external adapter version, peer, capability, state, retry, delivery, and security boundaries
- [ADR-0027](https://noemion.github.io/architecture/adr-0027-exact-identity-and-attestation.html) — exact content identity, immutable references, signed statements, validity, reproducibility, and derived-artifact relations
- [ADR-0028](https://noemion.github.io/architecture/adr-0028-text-and-identifier-boundaries.html) — text slots, strict UTF-8, source provenance, identifiers, normalization, bidi, hidden characters, model input, and display boundaries
- [ADR-0029](https://noemion.github.io/architecture/adr-0029-authority-and-authorization-decisions.html) — authority contexts, principal qualification, bounded scope, delegation, consent, replay, and result separation
- [ADR-0030](https://noemion.github.io/architecture/adr-0030-endem-content-and-authorization-companions.html) — stable Endem content identity, untrusted authority selectors, external authorization prerequisites, and companion relations
- [ADR-0031](https://noemion.github.io/architecture/adr-0031-release-name-collision-gate.html) — release-name collision evidence, Iknem and Drasor/drase selection, and one-time migration without compatibility aliases
- [ADR-0032](https://noemion.github.io/architecture/adr-0032-deterministic-maker-name-collision.html) — exact action-name collision evidence, Ktisor/ktise selection, action maturity, and direct replacement boundaries
- [ADR-0033](https://noemion.github.io/architecture/adr-0033-text-identifier-specification-name.html) — explicit text-and-identifier standard naming, rejected ambiguous candidates, and one-time route and registry migration
- [ADR-0034](https://noemion.github.io/architecture/adr-0034-pronunciation-and-oral-distinction.html) — pronunciation, oral distinguishability, human evidence, speech-model limits, and release-name review boundaries
- [ADR-0035](https://noemion.github.io/architecture/adr-0035-public-actions-and-internal-responsibilities.html) — five public actions, internal conformance, external signing, derivation responsibilities, and one-time migration
- [ADR-0036](https://noemion.github.io/architecture/adr-0036-source-bearing-and-stripped-release.html) — source-bearing formation artifacts, source-stripped release artifacts, companion boundaries, identity, and verification limits
- [Open questions](https://noemion.github.io/architecture/open-questions.html) — routes unresolved semantic, format, runtime, naming, and evidence questions to current authority or scoped research
- [Components](https://noemion.github.io/components/index.html) — Ktisor, Theor, and Drasor responsibility boundaries
- [Ktisor](https://noemion.github.io/components/ktisor.html) — deterministic Endem/Synem production, production-side checking, release derivation, and external-signing separation
- [Theor](https://noemion.github.io/components/theor.html) — independent direct reading, scoped views, differential comparison, and non-production diagnostic boundary
- [Drasor](https://noemion.github.io/components/drasor.html) — constrained loading, capability mediation, evidence collection, and execution boundary

## Specifications

- [Specifications](https://noemion.github.io/specifications/index.html) — authority, maturity, and normative-source map
- [Endem](https://noemion.github.io/specifications/endem.html) — the smallest deterministic natural-language goal artifact and its canonical fields
- [Synem](https://noemion.github.io/specifications/synem.html) — exact closure binding multiple goals, transitive dependencies, authority intersection, and session activation
- [Dromen](https://noemion.github.io/specifications/dromen.html) — read-only contract binding an exact subject, current authority, environment, capabilities, budgets, and observation duties for one session
- [Iknem](https://noemion.github.io/specifications/iknem.html) — scoped evidence binding an exact subject, method, provenance, validity, coverage, and decision boundary
- [Structured diagnostics](https://noemion.github.io/specifications/diagnostics.html) — cross-object machine identity, locations, recovery, safety, and result-domain separation
- [External protocol adapters](https://noemion.github.io/specifications/adapters.html) — version pinning, peer trust, capability intersection, state separation, retry, delivery, and security boundaries
- [Exact identity and attestation](https://noemion.github.io/specifications/identity.html) — cross-artifact byte identity, signed statements, validity cutoffs, reproducibility, and companion relations
- [Text and identifier boundaries](https://noemion.github.io/specifications/text-and-identifiers.html) — strict UTF-8, source provenance, ASCII identifiers, comparison, ranges, bidi, hidden characters, model input, and display views
- [Authority and authorization decisions](https://noemion.github.io/specifications/authority.html) — named authority, exact scope, semantic authorization, delegation, consent, revocation, replay, and capability intersection

## Guides and reference

- [Documentation center](https://noemion.github.io/docs/index.html) — task-oriented reading paths
- [Getting started](https://noemion.github.io/docs/getting-started.html) — one dependency-upgrade case separates goals, authorization, protocol states, evidence, and final decisions
- [Installation and usage](https://noemion.github.io/docs/installation-and-usage.html) — current availability and future release principles
- [Terminology and pronunciation validation](https://noemion.github.io/docs/terminology-and-pronunciation.html) — human first-read, listen-back, responsibility matching, statistical boundary, and release-name stop rules
- [Architecture guide](https://noemion.github.io/docs/architecture-guide.html) — one Agent task mapped to artifact, session, action, evidence, and decision boundaries
- [Development guide](https://noemion.github.io/docs/development-guide.html) — a falsifiable change claim carried through authority, failure ownership, evidence, and claim limits
- [Endem application reference](https://noemion.github.io/docs/endem-reference.html) — Endem actions, components, trust boundaries, and current status
- [Specifications reference](https://noemion.github.io/docs/specifications-reference.html) — task-based source lookup, authority order, research status, ADRs, and evidence boundaries

## Development and resources

- [Development](https://noemion.github.io/development/index.html) — current contribution scope, falsifiable change claims, minimum evidence, stop conditions, and reporting routes
- [Current stage](https://noemion.github.io/development/current-stage.html) — completed work, active design, and planned work
- [Implementation roadmap](https://noemion.github.io/development/implementation-roadmap.html) — current work, evidence required to advance, validation slices, and stop conditions
- [Testing strategy](https://noemion.github.io/development/testing.html) — change-to-evidence matrix, failure paths, determinism, malformed inputs, and claim limits
- [Downloads and resource status](https://noemion.github.io/downloads/index.html) — truthful availability, signing, and release-resource status
- [News and progress](https://noemion.github.io/news/index.html) — dated, verifiable project updates

## Endem application

- [Endem](https://noemion.github.io/endem/index.html) — a task-based guide to the planned single command surface, trust boundaries, stop conditions, and current availability

## Endem manual

- [Manual index](https://noemion.github.io/endem/docs/index.html) — responsibilities, actions, trust boundaries, and reading order
- [Format](https://noemion.github.io/endem/docs/format.html) — canonical Endem fields, explicit source transformations, deterministic formation, and round-trip limits
- [Binding](https://noemion.github.io/endem/docs/binding.html) — symbols, references, Synem closure, conflict handling, and packing
- [Safety](https://noemion.github.io/endem/docs/safety.html) — bounded parsing, checked arithmetic, independent reading, integrity, and signing boundaries
- [Running](https://noemion.github.io/endem/docs/running.html) — Dromen creation, constrained execution, observations, evidence closure, and acceptance
- [Reference](https://noemion.github.io/endem/docs/reference.html) — task lookup for actions, objects, result domains, goal constraints, diagnostics, and authoritative sources

## Availability and authority

- Canonical website explanations are HTML. Versioned implementation obligations live in the linked `spec/*.md` sources, while `spec/registry.json` and `vectors/` provide machine-readable maturity and test traceability; they are not duplicate Pages routes.
- Project status, proposed designs, normative specifications, and verified evidence remain distinct. Follow each page's maturity and authority labels.
- END-CORE 0.1.0-draft and its first semantic vectors are public engineering drafts, not a stable specification or wire-format release.
- No public executable release is currently available. The downloads page is the authoritative source for release availability.

## Usage

```bash
curl https://noemion.github.io/sitemap.md
```
