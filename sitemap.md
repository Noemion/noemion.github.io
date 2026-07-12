# Noemion Public Discovery

Version: 3

Noemion publishes its current project portal, architecture, specifications, component boundaries, development status, the Endem application, and manuals as canonical HTML pages. This Markdown index provides a compact discovery surface for readers and automated tools.

## Discovery surfaces

- [Project portal](https://noemion.github.io/index.html) — project purpose, boundaries, current status, and reading paths
- [Markdown discovery index](https://noemion.github.io/sitemap.md) — this document

## Project and background

- [Project background](https://noemion.github.io/about/index.html) — motivation, scope, non-goals, and intellectual foundations
- [Background and boundaries](https://noemion.github.io/about/background.html) — why expression and goal identity need a separate engineering artifact
- [Intellectual foundations](https://noemion.github.io/about/intellectual-foundations.html) — philosophical sources, engineering analogies, and adoption boundaries
- [Frequently asked questions](https://noemion.github.io/faq/index.html) — direct answers about scope, status, and non-goals

## Architecture and components

- [Architecture](https://noemion.github.io/architecture/index.html) — system layers, artifact lifecycle, and trust boundaries
- [Endem lifecycle](https://noemion.github.io/architecture/endem-lifecycle.html) — source, deterministic formation, closure, evidence, loading, and execution boundaries
- [Architecture decisions](https://noemion.github.io/architecture/decisions.html) — accepted responsibility boundaries and explicitly unfrozen interfaces
- [ADR-0008](https://noemion.github.io/architecture/adr-0008-endem-system.html) — accepted Endem vocabulary, artifact lifecycle, and single-application topology
- [Open questions](https://noemion.github.io/architecture/open-questions.html) — unresolved design questions and decision boundaries
- [Components](https://noemion.github.io/components/index.html) — Core, Reader, and Runner responsibility boundaries
- [Core](https://noemion.github.io/components/core.html) — deterministic Endem formation, checking, binding, and packing boundary
- [Reader](https://noemion.github.io/components/reader.html) — independent, bounded, read-only interpretation and diagnostic boundary
- [Runner](https://noemion.github.io/components/runner.html) — constrained loading, capability mediation, evidence collection, and execution boundary

## Specifications

- [Specifications](https://noemion.github.io/specifications/index.html) — authority, maturity, and normative-source map
- [Endem](https://noemion.github.io/specifications/endem.html) — the smallest deterministic natural-language goal artifact and its canonical fields
- [Weave](https://noemion.github.io/specifications/weave.html) — resolved, composable closure and binding rules
- [Witness](https://noemion.github.io/specifications/witness.html) — scoped evidence, provenance, integrity, and acceptance claims

## Guides and reference

- [Documentation center](https://noemion.github.io/docs/index.html) — task-oriented reading paths
- [Getting started](https://noemion.github.io/docs/getting-started.html) — problem background, core artifacts, and recommended reading order
- [Installation and usage](https://noemion.github.io/docs/installation-and-usage.html) — current availability and future release principles
- [Architecture guide](https://noemion.github.io/docs/architecture-guide.html) — system layers, lifecycle, and trust boundaries
- [Development guide](https://noemion.github.io/docs/development-guide.html) — specification-first workflow, testing, and contribution guidance
- [Endem application reference](https://noemion.github.io/docs/endem-reference.html) — Endem actions, components, trust boundaries, and current status
- [Specifications reference](https://noemion.github.io/docs/specifications-reference.html) — authority, maturity, ADRs, and specification reading order

## Development and resources

- [Development](https://noemion.github.io/development/index.html) — current work, validation strategy, and future planning
- [Current stage](https://noemion.github.io/development/current-stage.html) — completed work, active design, and planned work
- [Implementation roadmap](https://noemion.github.io/development/implementation-roadmap.html) — phases, application responsibilities, and completion criteria
- [Testing strategy](https://noemion.github.io/development/testing.html) — determinism, fuzzing, malformed inputs, and consistency testing
- [Downloads and resource status](https://noemion.github.io/downloads/index.html) — truthful availability, signing, and release-resource status
- [News and progress](https://noemion.github.io/news/index.html) — dated, verifiable project updates

## Endem application

- [Endem](https://noemion.github.io/endem/index.html) — the single public command surface for form, check, bind, pack, seal, see, run, and test

## Endem manual

- [Manual index](https://noemion.github.io/endem/docs/index.html) — responsibilities, actions, trust boundaries, and reading order
- [Format](https://noemion.github.io/endem/docs/format.html) — canonical Endem fields, encoding, deterministic formation, and round trips
- [Binding](https://noemion.github.io/endem/docs/binding.html) — symbols, references, Weave closure, conflict handling, and packing
- [Safety](https://noemion.github.io/endem/docs/safety.html) — bounded parsing, checked arithmetic, independent reading, integrity, and signing boundaries
- [Running](https://noemion.github.io/endem/docs/running.html) — Frame creation, constrained execution, observations, evidence closure, and acceptance
- [Reference](https://noemion.github.io/endem/docs/reference.html) — actions, artifacts, diagnostics, states, and normative sources

## Availability and authority

- The canonical public content is HTML. Markdown files under the source repository are authoring inputs for selected manuals and are not public route twins.
- Project status, proposed designs, normative specifications, and verified evidence remain distinct. Follow each page's maturity and authority labels.
- No public executable release is currently available. The downloads page is the authoritative source for release availability.

## Usage

```bash
curl https://noemion.github.io/sitemap.md
```
