from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "authority" / "cases.json"
CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CASE_ID = re.compile(r"^AUT-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "AUT-CTX-001", "AUT-PRN-001", "AUT-SCP-001", "AUT-SEM-001",
    "AUT-DEC-001", "AUT-DEL-001", "AUT-MUL-001", "AUT-CNS-001",
    "AUT-TIM-001", "AUT-RPL-001", "AUT-CAP-001", "AUT-SEP-001",
}
DIAGNOSTIC_BY_CLAUSE = {
    "AUT-CTX-001": "authority.context.unbound",
    "AUT-PRN-001": "authority.principal.unqualified",
    "AUT-SCP-001": "authority.scope.amplified",
    "AUT-SEM-001": "authority.semantic.unreviewed",
    "AUT-DEC-001": "authority.decision.incomplete",
    "AUT-DEL-001": "authority.delegation.amplified",
    "AUT-MUL-001": "authority.multi.conflicted",
    "AUT-CNS-001": "authority.consent.unbound",
    "AUT-TIM-001": "authority.validity.stale",
    "AUT-RPL-001": "authority.replay.detected",
    "AUT-CAP-001": "authority.capability.outside_intersection",
    "AUT-SEP-001": "authority.result.overclaimed",
}


def deep_merge(base, override):
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def proposal_violation(proposal):
    context = proposal.get("context", {})
    if (not all(context.get(key) for key in (
            "policy", "authority_domain", "object_identity", "operation",
            "purpose", "audience", "tenant", "jurisdiction", "cutoff", "failure_owner"))
            or not isinstance(context.get("conditions"), list)
            or context.get("mutable_latest") is not False
            or context.get("material_change_invalidates") is not True):
        return "AUT-CTX-001"

    principal = proposal.get("principal", {})
    if (not all(principal.get(key) for key in (
            "requester", "actor", "on_behalf_of", "authentication_method",
            "assurance", "claimed_role", "role_source", "authority_basis"))
            or principal.get("role_authorized") is not True
            or principal.get("authentication_is_authority") is not False
            or principal.get("signature_is_authority") is not False
            or principal.get("self_description_is_authority") is not False
            or principal.get("unknown_fails_closed") is not True):
        return "AUT-PRN-001"

    scope = proposal.get("scope", {})
    if (not all(isinstance(scope.get(key), list) and scope.get(key)
                for key in ("objects", "actions", "semantic_positions", "conditions"))
            or not all(scope.get(key) for key in (
                "purpose", "audience", "resource_limits", "time_scope", "comparison_profile"))
            or scope.get("default_deny") is not True
            or scope.get("wildcard") is not False
            or scope.get("ambient_authority") is not False
            or scope.get("string_subset_comparison") is not False
            or scope.get("unknown_fields_allowed") is not False):
        return "AUT-SCP-001"

    semantic = proposal.get("semantic", {})
    if (not all(semantic.get(key) for key in (
            "source_identity", "decoded_text_identity", "candidate_identity",
            "candidate_producer", "producer_class", "display_view_identity",
            "authority_principal", "authority_basis", "reason"))
            or not isinstance(semantic.get("affected_positions"), list)
            or not semantic.get("affected_positions")
            or not isinstance(semantic.get("remaining_unresolved_meaning"), list)
            or semantic.get("exact_view_reviewed") is not True
            or semantic.get("model_self_authorizes") is not False
            or semantic.get("confidence_authorizes") is not False
            or semantic.get("structural_validity_authorizes") is not False
            or semantic.get("undifferentiated_bulk_approval") is not False):
        return "AUT-SEM-001"

    decision = proposal.get("decision", {})
    if (not all(decision.get(key) for key in (
            "request_identity", "requester", "actor", "object_identity",
            "requested_scope", "effective_scope", "authority_context",
            "decider", "cutoff", "reason"))
            or not isinstance(decision.get("evidence"), list) or not decision.get("evidence")
            or not isinstance(decision.get("limitations"), list)
            or decision.get("outcome") not in {"allowed", "denied", "pending"}
            or decision.get("effective_scope_is_explicit_subset") is not True
            or decision.get("request_acknowledges_partial") is not True
            or decision.get("pending_is_allowed") is not False
            or decision.get("missing_defaults_to_allowed") is not False):
        return "AUT-DEC-001"

    delegation = proposal.get("delegation", {})
    actors = delegation.get("actors")
    edges = delegation.get("edges")
    if (not all(delegation.get(key) for key in (
            "original_authority", "subject", "policy", "purpose", "audience",
            "expires", "revocation_source"))
            or not isinstance(actors, list) or not actors
            or not isinstance(edges, list) or not edges
            or delegation.get("scope_strictly_nonincreasing") is not True
            or delegation.get("budget_strictly_nonincreasing") is not True
            or delegation.get("finite") is not True
            or delegation.get("acyclic") is not True
            or delegation.get("actor_preserved") is not True
            or delegation.get("impersonation") is not False
            or delegation.get("impersonation_explicitly_allowed") is not False
            or not isinstance(delegation.get("max_depth"), int) or delegation.get("max_depth") < 1
            or not isinstance(delegation.get("remaining_depth"), int)
            or delegation.get("remaining_depth") < 0
            or delegation.get("remaining_depth") > delegation.get("max_depth")
            or delegation.get("renewal_expands") is not False):
        return "AUT-DEL-001"

    multi = proposal.get("multi", {})
    approvals = multi.get("approvals")
    if (not all(multi.get(key) for key in (
            "eligible_set", "distinct_identity_rule", "required_roles",
            "veto_policy", "conflict_policy", "absence_policy", "cutoff"))
            or not isinstance(multi.get("required_count"), int) or multi.get("required_count") < 1
            or not isinstance(approvals, list) or len(approvals) < multi.get("required_count")
            or multi.get("order_sensitive") is not False
            or multi.get("policy_predeclared") is not True
            or multi.get("distinct_principals_verified") is not True
            or multi.get("duplicate_aliases") is not False
            or multi.get("repeated_decisions_count") is not False
            or multi.get("unresolved_conflict") is not False):
        return "AUT-MUL-001"

    consent = proposal.get("consent", {})
    if (not all(consent.get(key) for key in (
            "request_identity", "display_view_identity", "machine_object_identity",
            "purpose", "expires", "hidden_character_inventory"))
            or not all(isinstance(consent.get(key), list) and consent.get(key)
                       for key in ("actions", "resources", "recipients", "consequences"))
            or consent.get("display_matches_machine_object") is not True
            or consent.get("revocable") is not True
            or consent.get("transforms_disclosed") is not True
            or consent.get("default_selected") is not False
            or consent.get("unrelated_permissions_bundled") is not False
            or consent.get("reject_path_reachable") is not True
            or consent.get("consenter_role_authorized") is not True
            or consent.get("consent_is_sufficient_authority") is not False):
        return "AUT-CNS-001"

    validity = proposal.get("validity", {})
    if (not all(validity.get(key) for key in (
            "decision_time", "not_before", "expires", "cutoff", "status_source"))
            or validity.get("status_fresh") is not True
            or validity.get("revocation_checked") is not True
            or validity.get("principal_current") is not True
            or validity.get("policy_current") is not True
            or validity.get("cache_unbounded") is not False
            or validity.get("history_append_only") is not True
            or validity.get("historical_decision_rewritten") is not False):
        return "AUT-TIM-001"

    replay = proposal.get("replay", {})
    if (not all(replay.get(key) for key in (
            "request_identity", "object_identity", "action", "scope", "purpose",
            "audience", "session", "cutoff", "idempotency_class", "deduplication_key"))
            or not isinstance(replay.get("allowed_uses"), int) or replay.get("allowed_uses") < 1
            or not isinstance(replay.get("consumed_uses"), int) or replay.get("consumed_uses") < 0
            or replay.get("consumed_uses") >= replay.get("allowed_uses")
            or replay.get("retry_preserves_request_identity") is not True
            or replay.get("cross_object_allowed") is not False
            or replay.get("cross_purpose_allowed") is not False
            or replay.get("cross_session_allowed") is not False):
        return "AUT-RPL-001"

    capability = proposal.get("capability", {})
    required_limits = (
        "authorization_limit", "artifact_limit", "policy_limit", "environment_limit",
        "session_limit", "adapter_limit")
    if (not all(isinstance(capability.get(key), list) and capability.get(key)
                for key in required_limits)
            or not isinstance(capability.get("budget_limit"), dict)
            or not isinstance(capability.get("result"), list) or not capability.get("result")
            or capability.get("derivation") != "intersection"
            or any(not set(capability.get("result", [])).issubset(set(capability.get(key, [])))
                   for key in required_limits)
            or capability.get("ambient_authority_used") is not False
            or capability.get("token_passthrough") is not False
            or capability.get("tool_description_is_authority") is not False
            or capability.get("protocol_challenge_is_authority") is not False
            or capability.get("step_up_creates_new_session") is not True
            or capability.get("live_secret_outside_contract") is not True):
        return "AUT-CAP-001"

    separation = proposal.get("separation", {})
    if (not all(separation.get(key) for key in (
            "authentication", "signature", "role_authorization", "semantic_authorization",
            "capability_authorization", "evidence_validity", "evidence_coverage",
            "satisfaction", "final_decision", "session_result"))
            or any(separation.get(key) is not False for key in (
                "authorization_implies_truth", "authorization_implies_satisfaction",
                "authorization_implies_acceptance", "authorization_implies_completion",
                "model_is_authority", "runner_is_final_authority", "protocol_state_is_authority"))):
        return "AUT-SEP-001"
    return None


def main():
    errors = []
    try:
        vectors = json.loads(VECTOR_PATH.read_text())
        catalog = CATALOG_PATH.read_text()
        registry = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load authority consistency sources: {exc}")
        return 1

    if vectors.get("vector_format") != "aut-core.vector.v1" or vectors.get("spec") != {"id": "AUT-CORE", "version": "0.1.0-draft"}:
        errors.append("authority vectors must bind AUT-CORE 0.1.0-draft")
    description = vectors.get("description", "")
    if "not an identity provider" not in description or "not" not in description:
        errors.append("authority vectors must state the non-implementation boundary")
    if not any(document.get("spec_id") == "AUT-CORE" for document in registry.get("documents", [])):
        errors.append("registry must contain AUT-CORE")
    for diagnostic in DIAGNOSTIC_BY_CLAUSE.values():
        if f"`{diagnostic}`" not in catalog:
            errors.append(f"diagnostic catalog is missing {diagnostic}")

    baseline = vectors.get("baseline", {})
    cases = vectors.get("cases", [])
    counts = {"accept": 0, "reject": 0}
    accepted, rejected, ids = set(), set(), set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not CASE_ID.fullmatch(case_id) or case_id in ids:
            errors.append(f"invalid or duplicate authority case ID: {case_id}")
            continue
        ids.add(case_id)
        expect = case.get("expect", {})
        if expect.get("result") not in counts or expect.get("clause") not in CLAUSES:
            errors.append(f"{case_id}: invalid expectation")
            continue
        violation = proposal_violation(deep_merge(baseline, case.get("proposal", {})))
        actual = "reject" if violation else "accept"
        counts[actual] += 1
        if violation:
            rejected.add(violation)
            if expect.get("diagnostic") != DIAGNOSTIC_BY_CLAUSE[violation]:
                errors.append(f"{case_id}: expected diagnostic does not match {violation}")
        else:
            accepted.add(expect["clause"])
        if actual != expect["result"] or (violation and violation != expect["clause"]):
            errors.append(f"{case_id}: expected {expect}, evaluated {actual}/{violation}")

    if counts != {"accept": 12, "reject": 12}:
        errors.append(f"authority vectors require 12 accepts and 12 rejects, got {counts}")
    if accepted != CLAUSES:
        errors.append(f"authority accept coverage must include {sorted(CLAUSES)}, got {sorted(accepted)}")
    if rejected != CLAUSES:
        errors.append(f"authority reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 24 authority vectors (12 accepted proposals, 12 deterministic rejects across 12 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
