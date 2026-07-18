---
layout: spec
title: "Session Contract Core · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/session-contract-core.html"
summary: "规定一次受控会话怎样重新核对精确目标、政策、环境、能力和预算，并在实质条件变化后关闭旧权限。"
document_status: "规范草案"
---
# Session Contract Core

- Specification ID: `SESSION-CORE`
- Version: `0.1.0-draft`
- Status: draft; accepted abstract session-boundary design
- Implementation status: proposal-vector checker only; no bounded runner, loader, sandbox, capability broker or runtime exists
- Wire status: not applicable; session contract is not a persistent object and has no file format

## 1. Purpose

A session contract is the sealed, read-only execution contract for exactly one run session. A bounded runner may establish it only after revalidating an exact, `resolved` Endem or Endem closure; checking the required external statements against a named policy, cutoff and revocation state; and intersecting the artifact limits with current policy, environment, authority, capability and budget limits.

A session contract separates a persistent goal artifact from the mutable world in which a session attempts to realize it. It does not contain live credentials, open handles, mutable observations, model memory or final results. Runtime events and observations become scoped evidence entries; satisfaction, authority decisions and session termination remain separate result domains.

Any claimed authority, consent, delegation, authorization decision or capability grant `MUST` also pin and conform to the exact applicable `AUT-CORE` version. `SESSION-CORE` defines the sealed session intersection; it does not redefine who may authorize its inputs.

The keywords `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY` are normative as described by BCP 14 when written in uppercase.

## 2. Position in the lifecycle

```text
resolved Endem or Endem closure
        + required external statements
        + statement policy, cutoff, validity and revocation state
        + named policies and authorities
        + environment and adapter bindings
        + bounded capability and budget grants
        + observation and disclosure duties
                         |
                         v
              sealed session contract for one run
                         |
                         v
        runtime events and structured observations -> evidence entries -> appraisal -> decision
```

An input proposal is not a session contract. It becomes a session contract only after all required bindings are checked and sealed. Any material change creates a new session proposal; it never mutates or resumes the old session contract.

## 3. Normative clauses

### SESSION-SUB-001 — The session subject and external statements must be exact and freshly revalidated

**Requirement:** A session contract `MUST` bind exactly one `resolved` Endem or Endem closure by exact content identity and Profile. It `MUST` separately bind every required external statement, statement type, subject digest, verification policy, verification result, named cutoff, revocation state and relying-party applicability decision. A bounded runner `MUST` recheck the container, Profile, content, closure and every external relation before establishment. A display name, search result, mutable path, latest version, cached success, signature-presence flag or external Task identifier `MUST NOT` substitute for these checks.

**Failure:** An unresolved, missing, ambiguous or changed subject, or a missing, invalid, revoked, out-of-scope or policy-inapplicable required statement, rejects establishment. No session contract or satisfaction result is created.

**Verification:** `SESSION-SCN-001`, `SESSION-SCN-002`; `vectors/session-contract/cases.json`; future `conformance:session_contract-subject-revalidation` component tests.

### SESSION-POL-001 — Policies, authorities and cutoff must be closed before establishment

**Requirement:** A session contract `MUST` bind the exact policy set, policy versions or identities, decision authorities, escalation authorities, applicable consent, cutoff and expiry used to establish the session. Conflicts and unresolved authority-bearing `unresolved_meaning` items `MUST` reject establishment unless a named policy proves they are outside the selected session scope. A model, adapter, tool description or remote Agent `MUST NOT` become a policy or authority merely by appearing in context.

**Failure:** An implicit default, mutable latest policy, missing authority, unresolved in-scope ambiguity or policy conflict rejects establishment.

**Verification:** `SESSION-SCN-003`, `SESSION-SCN-004`; `vectors/session-contract/cases.json`; future `conformance:session_contract-policy-closure` component tests.

### SESSION-ENV-001 — Environment and backend assumptions must be explicit bindings

**Requirement:** A session contract `MUST` declare the environment facts required by the subject and policy, including applicable platform, locale, time authority, isolation profile, adapters, protocol versions and model or rule backend identities. Each binding `MUST` distinguish a declared identifier from an observed property and name the observation used to confirm it. Undeclared environment state and remote self-description `MUST NOT` be treated as verified.

**Failure:** A missing required binding, unsupported protocol, unverified environment claim or material mismatch rejects establishment. Material drift after establishment invalidates the session contract under `SESSION-IMM-001`.

**Verification:** `SESSION-SCN-005`, `SESSION-SCN-006`; `vectors/session-contract/cases.json`; future `conformance:session_contract-environment-binding` component tests.

### SESSION-CAP-001 — The capability envelope may only intersect and reduce authority

**Requirement:** The session contract capability envelope `MUST` be the intersection of artifact and Endem closure limits, current policy, operator authorization, environment support and adapter bounds. Every allowed capability `MUST` bind an action, resource or audience, scope, constraints, issuing authority, expiry and revocation check. Missing required capability rejects establishment; optional capability loss may only deactivate a fixed Endem closure member through its declared guard. Step-up or broader authority `MUST` create a new run-session proposal and `MUST NOT` mutate the current session contract.

**Failure:** Union, fallback to ambient authority, wildcard expansion, token passthrough, audience substitution or runtime self-escalation invalidates the proposal or interrupts the established session.

**Verification:** `SESSION-SCN-007`, `SESSION-SCN-008`; `vectors/session-contract/cases.json`; future `conformance:session_contract-capability-intersection` component tests.

### SESSION-SEC-001 — Live secrets and handles must remain outside the session contract

**Requirement:** A session contract `MUST` contain only non-secret capability descriptors and irreversible references needed for audit. Bearer tokens, refresh tokens, private keys, session cookies, file descriptors, sockets, process handles and provider-native capability handles `MUST NOT` enter the session contract, evidence entry or persistent logs. A separate minimal capability domain may hold live material and `MUST` bind it to the exact run session, intended resource or audience, scope and expiry. Rotation that preserves the descriptor MAY occur outside the session contract; any scope, audience or authority change requires a new session.

**Failure:** Secret material in the proposal, an unbound handle, reusable cross-session reference or passthrough token rejects establishment or invalidates the session.

**Verification:** `SESSION-SCN-009`; `vectors/session-contract/cases.json`; future `conformance:session_contract-secret-separation` component tests.

### SESSION-BUD-001 — Budgets, time and cancellation must be finite and typed

**Requirement:** A session contract `MUST` bind finite limits for every resource class the session may consume, including applicable elapsed time, calls, retries, tokens, bytes, storage, processes and cost. Each limit `MUST` name its unit, counter authority, reset rule and exhaustion action. Retries, child tasks, model delegation and protocol adapters `MUST` consume the same enclosing limits or a strict subdivision. Cancellation and deadline propagation `MUST` be defined before operation.

**Failure:** An unbounded required resource, incompatible units, hidden reset, child-budget escape or ignored cancellation rejects establishment or interrupts the session. Exhaustion does not imply `unmet`.

**Verification:** `SESSION-SCN-010`; `vectors/session-contract/cases.json`; future `conformance:session_contract-budget-envelope` component tests.

### SESSION-ACT-001 — Endem closure activation must remain inside the fixed closure and outside satisfaction

**Requirement:** For a Endem closure subject, a session contract `MUST` bind the exact closed member set, activation guards, input event identities, cutoff and initial `active / inactive / unresolved / error` classifications. Runtime re-evaluation MAY change activation events only under the already bound guard and evidence rules; it `MUST NOT` add members, alter closure identity, grant capability or mutate the session contract. Activation status `MUST NOT` map directly to `met / unmet / undetermined / fault`.

**Failure:** Runtime dependency discovery, latest-version lookup, activation-driven permission gain, missing guard basis or result-domain conversion invalidates establishment or the affected session path.

**Verification:** `SESSION-SCN-011`; `vectors/session-contract/cases.json`; future `conformance:session_contract-activation-boundary` component tests.

### SESSION-OBS-001 — Observation, appraisal, disclosure and decision duties must be assigned

**Requirement:** A session contract `MUST` map each applicable `satisfaction_criteria` responsibility to authorized observation producers, methods, environment and time bounds, expected `structured_observation` relation positions, required evidence entry classes, disclosure rules, appraisal policy and named decision authority. The map `MUST` preserve the separation of observation, satisfaction, evidence validity, coverage, final decision and session termination. Model outputs and external protocol states remain typed candidates or sourced events.

**Failure:** An unassigned required observation, missing decision authority, hidden disclosure loss, or direct mapping from tool or Agent success to `met` or `accepted` rejects establishment.

**Verification:** `SESSION-SCN-012`, `SESSION-SCN-013`; `vectors/session-contract/cases.json`; future `conformance:session_contract-observation-plan` component tests.

### SESSION-IMM-001 — Establishment seals the contract and material drift invalidates it

**Requirement:** After establishment, the session contract `MUST` be read-only. Changes to subject identity, external statements, verification results, revocation state, policy, authority, required environment, capability descriptor, budget, activation guard, observation duty or disclosure policy `MUST` invalidate the session contract and stop or fail the run according to its predeclared rule. The implementation `MUST` append a scoped event and preserve prior evidence entries; it `MUST NOT` patch the old session contract or erase the drift.

**Failure:** In-place mutation, silent refresh to broader authority, continued operation after material drift or overwriting prior evidence violates the session boundary.

**Verification:** `SESSION-SCN-014`; `vectors/session-contract/cases.json`; future `conformance:session_contract-drift-invalidation` component tests.

### SESSION-LIF-001 — A session contract is non-persistent, non-transferable and non-resumable

**Requirement:** A session contract `MUST` belong to exactly one run and one authorization context. It `MUST NOT` have a file extension, portable wire format, global content identity, package coordinate or cross-session reuse mechanism. Diagnostic snapshots MAY record redacted descriptors as evidence entries or session events, but `MUST NOT` rehydrate, transfer or resurrect the session contract. Completion, failure, stop or invalidation `MUST` make all bound live capability material unreachable and trigger the declared disposal procedure.

**Failure:** Serializing a reusable session contract, accepting a copied session identifier as authority, resuming with stale handles, or reconstructing a session from logs violates the lifecycle and requires rejection.

**Verification:** `SESSION-SCN-015`; `vectors/session-contract/cases.json`; future `conformance:session_contract-session-disposal` component tests.

## 4. Current non-goals

This specification does not define a session contract file, extension, magic number, serialization, stable ABI, runtime API, capability broker, sandbox, event encoding, process model, recovery protocol or implementation language. It also does not select Linux namespaces, seccomp, Landlock, containers, virtual machines or a model SDK. Those mechanisms may satisfy future implementation obligations only after the user opens the component-code stage and independent evidence demonstrates their actual isolation properties.
