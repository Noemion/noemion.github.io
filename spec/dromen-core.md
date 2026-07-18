---
layout: spec
title: "Dromen Core Session Contract · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/dromen-core.html"
summary: "规定一次受控会话怎样重新核对精确目标、政策、环境、能力和预算，并在实质条件变化后关闭旧权限。"
document_status: "规范草案"
---
# Dromen Core Session Contract

- Specification ID: `DRO-CORE`
- Version: `0.1.0-draft`
- Status: draft; accepted abstract session-boundary design
- Implementation status: proposal-vector checker only; no Drasor, loader, sandbox, capability broker or runtime exists
- Wire status: not applicable; Dromen is not a persistent object and has no file format

## 1. Purpose

Dromen is the sealed, read-only execution contract for exactly one Drase session. Drasor may establish it only after revalidating an exact attested Endem or Synem and intersecting the artifact limits with current policy, environment, authority, capability and budget limits.

Dromen separates a persistent goal artifact from the mutable world in which a session attempts to realize it. It does not contain live credentials, open handles, mutable observations, model memory or final results. Runtime events and observations become scoped Iknem; satisfaction, authority decisions and session termination remain separate result domains.

Any claimed authority, consent, delegation, authorization decision or capability grant `MUST` also pin and conform to the exact applicable `AUT-CORE` version. DRO-CORE defines the sealed session intersection; it does not redefine who may authorize its inputs.

The keywords `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY` are normative as described by BCP 14 when written in uppercase.

## 2. Position in the lifecycle

```text
attested Endem or Synem
        + current validation and revocation state
        + named policies and authorities
        + environment and adapter bindings
        + bounded capability and budget grants
        + observation and disclosure duties
                         |
                         v
              sealed Dromen for one Drase session
                         |
                         v
        runtime events and phain -> Iknem -> appraisal -> decision
```

An input proposal is not a Dromen. It becomes a Dromen only after all required bindings are checked and sealed. Any material change creates a new session proposal; it never mutates or resumes the old Dromen.

## 3. Normative clauses

### DRO-SUB-001 — The session subject must be exact, attested and freshly revalidated

**Requirement:** A Dromen `MUST` bind exactly one attested Endem or one attested Synem by exact content identity, Profile and attestation envelope. Drasor `MUST` recheck container, Profile, content, closure, signature, revocation and applicability at a named cutoff before establishment. A display name, search result, mutable path, latest version, cached success or external Task identifier `MUST NOT` substitute for the exact subject.

**Failure:** Missing, ambiguous, changed, invalid, revoked or not-yet-attested input rejects establishment. No Dromen or satisfaction result is created.

**Verification:** `DRO-SCN-001`, `DRO-SCN-002`; `vectors/dromen/cases.json`; future `conformance:dromen-subject-revalidation` component tests.

### DRO-POL-001 — Policies, authorities and cutoff must be closed before establishment

**Requirement:** A Dromen `MUST` bind the exact policy set, policy versions or identities, decision authorities, escalation authorities, applicable consent, cutoff and expiry used to establish the session. Conflicts and unresolved authority-bearing `apor` items `MUST` reject establishment unless a named policy proves they are outside the selected session scope. A model, adapter, tool description or remote Agent `MUST NOT` become a policy or authority merely by appearing in context.

**Failure:** An implicit default, mutable latest policy, missing authority, unresolved in-scope ambiguity or policy conflict rejects establishment.

**Verification:** `DRO-SCN-003`, `DRO-SCN-004`; `vectors/dromen/cases.json`; future `conformance:dromen-policy-closure` component tests.

### DRO-ENV-001 — Environment and backend assumptions must be explicit bindings

**Requirement:** A Dromen `MUST` declare the environment facts required by the subject and policy, including applicable platform, locale, time authority, isolation profile, adapters, protocol versions and model or rule backend identities. Each binding `MUST` distinguish a declared identifier from an observed property and name the observation used to confirm it. Undeclared environment state and remote self-description `MUST NOT` be treated as verified.

**Failure:** A missing required binding, unsupported protocol, unverified environment claim or material mismatch rejects establishment. Material drift after establishment invalidates the Dromen under `DRO-IMM-001`.

**Verification:** `DRO-SCN-005`, `DRO-SCN-006`; `vectors/dromen/cases.json`; future `conformance:dromen-environment-binding` component tests.

### DRO-CAP-001 — The capability envelope may only intersect and reduce authority

**Requirement:** The Dromen capability envelope `MUST` be the intersection of artifact and Synem limits, current policy, operator authorization, environment support and adapter bounds. Every grant `MUST` bind an action, resource or audience, scope, constraints, issuer or grant authority, expiry and revocation check. Missing required capability rejects establishment; optional capability loss may only deactivate a fixed Synem member through its declared guard. Step-up or broader authority `MUST` create a new Drase session proposal and `MUST NOT` mutate the current Dromen.

**Failure:** Union, fallback to ambient authority, wildcard expansion, token passthrough, audience substitution or runtime self-escalation invalidates the proposal or interrupts the established session.

**Verification:** `DRO-SCN-007`, `DRO-SCN-008`; `vectors/dromen/cases.json`; future `conformance:dromen-capability-intersection` component tests.

### DRO-SEC-001 — Live secrets and handles must remain outside the Dromen

**Requirement:** A Dromen `MUST` contain only non-secret capability descriptors and irreversible references needed for audit. Bearer tokens, refresh tokens, private keys, session cookies, file descriptors, sockets, process handles and provider-native capability handles `MUST NOT` enter the Dromen, Iknem or persistent logs. A separate minimal capability domain may hold live material and `MUST` bind it to the Dromen session, intended resource or audience, scope and expiry. Rotation that preserves the descriptor MAY occur outside the Dromen; any scope, audience or authority change requires a new session.

**Failure:** Secret material in the proposal, an unbound handle, reusable cross-session reference or passthrough token rejects establishment or invalidates the session.

**Verification:** `DRO-SCN-009`; `vectors/dromen/cases.json`; future `conformance:dromen-secret-separation` component tests.

### DRO-BUD-001 — Budgets, time and cancellation must be finite and typed

**Requirement:** A Dromen `MUST` bind finite limits for every resource class the session may consume, including applicable elapsed time, calls, retries, tokens, bytes, storage, processes and cost. Each limit `MUST` name its unit, counter authority, reset rule and exhaustion action. Retries, child tasks, model delegation and protocol adapters `MUST` consume the same enclosing limits or a strict subdivision. Cancellation and deadline propagation `MUST` be defined before operation.

**Failure:** An unbounded required resource, incompatible units, hidden reset, child-budget escape or ignored cancellation rejects establishment or interrupts the session. Exhaustion does not imply `unmet`.

**Verification:** `DRO-SCN-010`; `vectors/dromen/cases.json`; future `conformance:dromen-budget-envelope` component tests.

### DRO-ACT-001 — Synem activation must remain inside the fixed closure and outside satisfaction

**Requirement:** For a Synem subject, a Dromen `MUST` bind the exact closed member set, activation guards, input event identities, cutoff and initial `active / inactive / unresolved / error` classifications. Runtime re-evaluation MAY change activation events only under the already bound guard and evidence rules; it `MUST NOT` add members, alter closure identity, grant capability or mutate the Dromen. Activation status `MUST NOT` map directly to `met / unmet / agno / fault`.

**Failure:** Runtime dependency discovery, latest-version lookup, activation-driven permission gain, missing guard basis or result-domain conversion invalidates establishment or the affected session path.

**Verification:** `DRO-SCN-011`; `vectors/dromen/cases.json`; future `conformance:dromen-activation-boundary` component tests.

### DRO-OBS-001 — Observation, appraisal, disclosure and decision duties must be assigned

**Requirement:** A Dromen `MUST` map each applicable `krin` responsibility to authorized observation producers, methods, environment and time bounds, expected `phain` relation positions, required Iknem classes, disclosure rules, appraisal policy and named decision authority. The map `MUST` preserve the separation of observation, satisfaction, evidence validity, coverage, final decision and session termination. Model outputs and external protocol states remain typed candidates or sourced events.

**Failure:** An unassigned required observation, missing decision authority, hidden disclosure loss, or direct mapping from tool or Agent success to `met` or `accepted` rejects establishment.

**Verification:** `DRO-SCN-012`, `DRO-SCN-013`; `vectors/dromen/cases.json`; future `conformance:dromen-observation-plan` component tests.

### DRO-IMM-001 — Establishment seals the contract and material drift invalidates it

**Requirement:** After establishment, the Dromen `MUST` be read-only. Changes to subject identity, attestation or revocation state, policy, authority, required environment, capability descriptor, budget, activation guard, observation duty or disclosure policy `MUST` invalidate the Dromen and interrupt or fail the Drase session according to its predeclared rule. The implementation `MUST` append a scoped event and preserve prior Iknem; it `MUST NOT` patch the old Dromen or erase the drift.

**Failure:** In-place mutation, silent refresh to broader authority, continued operation after material drift or overwriting prior evidence violates the session boundary.

**Verification:** `DRO-SCN-014`; `vectors/dromen/cases.json`; future `conformance:dromen-drift-invalidation` component tests.

### DRO-LIF-001 — A Dromen is non-persistent, non-transferable and non-resumable

**Requirement:** A Dromen `MUST` belong to exactly one Drase session and one authorization context. It `MUST NOT` have a file extension, portable wire format, global content identity, package coordinate or cross-session reuse mechanism. Diagnostic snapshots MAY record redacted descriptors as Iknem or session events, but `MUST NOT` rehydrate, transfer or resurrect the Dromen. Session completion, failure, interruption or invalidation `MUST` make all bound live capability material unreachable and trigger the declared disposal procedure.

**Failure:** Serializing a reusable Dromen, accepting a copied session identifier as authority, resuming with stale handles, or reconstructing a session from logs violates the lifecycle and requires rejection.

**Verification:** `DRO-SCN-015`; `vectors/dromen/cases.json`; future `conformance:dromen-session-disposal` component tests.

## 4. Current non-goals

This specification does not define a Dromen file, extension, magic number, serialization, stable ABI, runtime API, capability broker, sandbox, event encoding, process model, recovery protocol or implementation language. It also does not select Linux namespaces, seccomp, Landlock, containers, virtual machines or a model SDK. Those mechanisms may satisfy future implementation obligations only after the user opens the component-code stage and independent evidence demonstrates their actual isolation properties.
