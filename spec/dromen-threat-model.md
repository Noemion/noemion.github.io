---
layout: spec
title: "Dromen Threat Model · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/dromen-threat-model.html"
summary: "威胁模型，记录攻击面、失败责任与采用限制。"
---
# Dromen Threat Model

- Document ID: `DRO-THREAT`
- Version: `0.1.0-draft`
- Date: 2026-07-13
- Status: draft; paired with DRO-CORE for future Drasor and capability-domain design
- Implementation status: proposal-vector checker only; this document is not a sandbox, loader, broker or runtime

## 1. Protection objective

Dromen protects the boundary between a persistent, attested goal artifact and one mutable execution session. The protected property is not that the session will succeed. It is that the session can use only the exact subject, policies, environment bindings, capabilities, budgets, observation duties and authorities that were checked before operation, and that any material change closes the old authority rather than rewriting it.

An attacker may control model output, remote tool and Agent descriptions, task identifiers, environment variables, adapter metadata, cached validation, network responses, cancellation, retry paths, log fields and credential material. None of them becomes authority merely by appearing in a session context.

## 2. Threats and mandatory mitigations

### THR-DRO-001 — Subject substitution after validation

An attacker validates one Endem or Synem and then loads another object through a mutable path, display name, latest tag or changed closure. `DRO-SUB-001` binds the exact attested identity and requires fresh layered validation at the establishment cutoff.

### THR-DRO-002 — Stale policy, authority or revocation state

An attacker reuses a cached successful policy check after the signer, method, decision authority or grant has changed. `DRO-POL-001` and `DRO-SUB-001` bind exact policies, authorities, cutoff, expiry and revocation checks.

### THR-DRO-003 — Environment self-description and adapter drift

A backend claims a safe version or environment, or changes model, protocol, locale, clock or isolation behavior after establishment. `DRO-ENV-001` requires observed bindings; `DRO-IMM-001` invalidates material drift.

### THR-DRO-004 — Capability amplification and confused deputy

An attacker unions grants, uses ambient privilege, swaps token audience, passes credentials downstream or requests step-up authority inside the old session. `DRO-CAP-001` requires intersection and a new session for broader authority; `DRO-SEC-001` separates live credentials and handles.

### THR-DRO-005 — Secret persistence and cross-session handle reuse

Tokens, cookies, descriptors or provider handles enter the Dromen, Iknem or logs and later reanimate authority. `DRO-SEC-001` forbids live material in these objects; `DRO-LIF-001` requires disposal and prohibits rehydration.

### THR-DRO-006 — Budget escape through retries or delegation

A model, adapter or child task resets counters, changes units, ignores cancellation or delegates work outside the parent limit. `DRO-BUD-001` requires typed finite envelopes and strict subdivision.

### THR-DRO-007 — Dynamic dependency and activation laundering

Runtime discovery adds a new Synem member, or an activation result is treated as target satisfaction or permission. `DRO-ACT-001` binds activation to the fixed closure and its own result domain.

### THR-DRO-008 — Observation or decision authority omission

The session can act but no actor is responsible for required observations, evidence coverage, appraisal or final decision. `DRO-OBS-001` requires a complete responsibility map and preserves all result domains.

### THR-DRO-009 — Mutable contract and erased drift

A session silently patches policy, environment, capability or budget fields and overwrites old evidence to appear continuously valid. `DRO-IMM-001` seals the Dromen and makes material change an invalidation event.

### THR-DRO-010 — Session resurrection and identifier-as-authority

An attacker serializes a Dromen, copies a session ID, restores logs or resumes stale handles in another authorization context. `DRO-LIF-001` makes Dromen non-persistent, non-transferable and non-resumable.

## 3. Risks not solved by this model

This model does not prove an operating-system sandbox, credential store, capability broker, scheduler, network policy, process boundary, model isolation, event log or disposal mechanism. Platform-specific bypasses, side channels, denial of service, covert channels and implementation bugs require separate threat models and component evidence after the code stage is explicitly authorized.

