---
layout: spec
title: "session contract Threat Model · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/session-contract-threat-model.html"
summary: "分析目标替换、权限扩大、秘密泄露、预算逃逸和会话复活等风险，确保旧会话不能被悄悄改写。"
document_status: "威胁模型"
---
# session contract Threat Model

- Document ID: `SESSION-THREAT`
- Version: `0.1.0-draft`
- Date: 2026-07-13
- Status: draft; paired with SESSION-CORE for future bounded runner and capability-domain design
- Implementation status: proposal-vector checker only; this document is not a sandbox, loader, broker or runtime

## 1. Protection objective

A session contract protects the boundary between a persistent, resolved goal artifact with separately verified external statements and one mutable execution session. The protected property is not that the session will succeed. It is that the session can use only the exact subject, statements, policies, environment bindings, capabilities, budgets, observation duties and authorities checked before operation, and that any material change closes the old authority rather than rewriting it.

An attacker may control model output, remote tool and Agent descriptions, task identifiers, environment variables, adapter metadata, cached validation, network responses, cancellation, retry paths, log fields and credential material. None of them becomes authority merely by appearing in a session context.

## 2. Threats and mandatory mitigations

### THR-SESSION-001 — Subject substitution after validation

An attacker validates one Endem or Endem closure and then loads another object through a mutable path, display name, latest tag or changed closure. `SESSION-SUB-001` binds the exact resolved content identity and every required external statement, and requires fresh layered validation at the establishment cutoff.

### THR-SESSION-002 — Stale policy, authority or revocation state

An attacker reuses a cached successful policy check after the signer, method, decision authority or grant has changed. `SESSION-POL-001` and `SESSION-SUB-001` bind exact policies, authorities, cutoff, expiry and revocation checks.

### THR-SESSION-003 — Environment self-description and adapter drift

A backend claims a safe version or environment, or changes model, protocol, locale, clock or isolation behavior after establishment. `SESSION-ENV-001` requires observed bindings; `SESSION-IMM-001` invalidates material drift.

### THR-SESSION-004 — Capability amplification and confused deputy

An attacker unions grants, uses ambient privilege, swaps token audience, passes credentials downstream or requests step-up authority inside the old session. `SESSION-CAP-001` requires intersection and a new session for broader authority; `SESSION-SEC-001` separates live credentials and handles.

### THR-SESSION-005 — Secret persistence and cross-session handle reuse

Tokens, cookies, descriptors or provider handles enter the session contract, evidence entry or logs and later reanimate authority. `SESSION-SEC-001` forbids live material in these objects; `SESSION-LIF-001` requires disposal and prohibits rehydration.

### THR-SESSION-006 — Budget escape through retries or delegation

A model, adapter or child task resets counters, changes units, ignores cancellation or delegates work outside the parent limit. `SESSION-BUD-001` requires typed finite envelopes and strict subdivision.

### THR-SESSION-007 — Dynamic dependency and activation laundering

Runtime discovery adds a new Endem closure member, or an activation result is treated as target satisfaction or permission. `SESSION-ACT-001` binds activation to the fixed closure and its own result domain.

### THR-SESSION-008 — Observation or decision authority omission

The session can act but no actor is responsible for required observations, evidence coverage, appraisal or final decision. `SESSION-OBS-001` requires a complete responsibility map and preserves all result domains.

### THR-SESSION-009 — Mutable contract and erased drift

A session silently patches policy, environment, capability or budget fields and overwrites old evidence to appear continuously valid. `SESSION-IMM-001` seals the session contract and makes material change an invalidation event.

### THR-SESSION-010 — Session resurrection and identifier-as-authority

An attacker serializes a session contract, copies a session ID, restores logs or resumes stale handles in another authorization context. `SESSION-LIF-001` makes session contract non-persistent, non-transferable and non-resumable.

## 3. Risks not solved by this model

This model does not prove an operating-system sandbox, credential store, capability broker, scheduler, network policy, process boundary, model isolation, event log or disposal mechanism. Platform-specific bypasses, side channels, denial of service, covert channels and implementation bugs require separate threat models and component evidence after the code stage is explicitly authorized.
