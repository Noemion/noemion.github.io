from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "adapters" / "cases.json"
CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CASE_ID = re.compile(r"^AD-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "ADP-PIN-001", "ADP-PEE-001", "ADP-CAP-001", "ADP-INV-001",
    "ADP-MAP-001", "ADP-STA-001", "ADP-ART-001", "ADP-ERR-001",
    "ADP-CAN-001", "ADP-RTY-001", "ADP-DEL-001", "ADP-SEC-001",
}
DIAGNOSTIC_BY_CLAUSE = {
    "ADP-PIN-001": "adapter.protocol.version_unpinned",
    "ADP-PEE-001": "adapter.peer.binding_invalid",
    "ADP-CAP-001": "adapter.capability.outside_intersection",
    "ADP-INV-001": "adapter.invocation.context_incomplete",
    "ADP-MAP-001": "adapter.mapping.loss_undeclared",
    "ADP-STA-001": "adapter.state.domain_confused",
    "ADP-ART-001": "adapter.artifact.candidate_unbound",
    "ADP-ERR-001": "adapter.error.provenance_lost",
    "ADP-CAN-001": "adapter.cancellation.finality_unproven",
    "ADP-RTY-001": "adapter.retry.not_authorized",
    "ADP-DEL-001": "adapter.delivery.evidence_incomplete",
    "ADP-SEC-001": "adapter.security.envelope_invalid",
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
    protocol = proposal.get("protocol", {})
    if (not all(protocol.get(key) for key in ("id", "version", "binding", "schema", "transport"))
            or protocol.get("stability") not in {"stable", "candidate", "experimental"}
            or protocol.get("latest") is not False
            or protocol.get("unknown_extensions") != []
            or not isinstance(protocol.get("extensions"), list)):
        return "ADP-PIN-001"

    peer = proposal.get("peer", {})
    if (not all(peer.get(key) for key in ("discovery_source", "declared_subject", "endpoint", "authenticated_subject", "tenant", "audience", "policy_decision"))
            or peer.get("self_claim_is_authority") is not False
            or peer.get("redirect_revalidated") is not True):
        return "ADP-PEE-001"

    capabilities = proposal.get("capabilities", {})
    sets = [set(capabilities.get(key, [])) for key in ("protocol", "peer", "adapter", "session_contract", "policy")]
    intersection = set.intersection(*sets) if sets else set()
    if (set(capabilities.get("effective", [])) != intersection
            or capabilities.get("unknown_default_denied") is not True
            or capabilities.get("mutates_current_dromen") is not False):
        return "ADP-CAP-001"

    invocation = proposal.get("invocation", {})
    if (not all(invocation.get(key) for key in ("session", "call", "subject", "peer_binding", "operation", "input_identity", "capability_basis", "budget", "deadline", "idempotency", "observation_responsibility"))
            or invocation.get("subject") == "latest"
            or invocation.get("external_ids_replace_local_call") is not False
            or invocation.get("traceable") is not True):
        return "ADP-INV-001"

    mapping = proposal.get("mapping", {})
    if (not all(mapping.get(key) for key in ("version", "raw_kind", "raw_identity"))
            or mapping.get("preserves_origin") is not True
            or not isinstance(mapping.get("loss_manifest"), list)
            or mapping.get("undeclared_loss") is not False
            or (mapping.get("loss_manifest") and mapping.get("claims_complete") is not False)):
        return "ADP-MAP-001"

    state = proposal.get("state", {})
    if (not state.get("external") or state.get("local_implications") != []
            or state.get("result_domains_preserved") is not True):
        return "ADP-STA-001"

    artifact = proposal.get("artifact", {})
    if (artifact.get("candidate") is not True
            or not all(artifact.get(key) for key in ("producer_call", "peer", "media_type", "content_identity", "integrity", "disclosure"))
            or artifact.get("bounded") is not True
            or artifact.get("promoted_object") is not None
            or artifact.get("remote_name_is_identity") is not False):
        return "ADP-ART-001"

    error = proposal.get("error", {})
    if (not error.get("dia_core") or error.get("source_layers_separate") is not True
            or error.get("machine_mapping") is not True
            or error.get("parses_message") is not False
            or error.get("unknown_preserved") is not True
            or error.get("changes_result_or_authority") is not False):
        return "ADP-ERR-001"

    lifecycle = proposal.get("lifecycle", {})
    if (lifecycle.get("rollback_claimed") is not False
            or lifecycle.get("terminal_immutable") is not True
            or lifecycle.get("followup_new_call") is not True
            or lifecycle.get("resurrects_dromen") is not False):
        return "ADP-CAN-001"

    retry = proposal.get("retry", {})
    retry_class = retry.get("class")
    automatic_allowed = retry_class in {"read-only", "idempotent", "deduplicated"}
    if (retry_class not in {"read-only", "idempotent", "deduplicated", "non-idempotent"}
            or not retry.get("classifier_authority")
            or not retry.get("evidence")
            or (retry.get("automatic") is True and not automatic_allowed)
            or (retry_class == "deduplicated" and not retry.get("dedup_key"))
            or retry.get("original_application_checked") is not True
            or retry.get("budget_shared") is not True
            or retry.get("deadline_valid") is not True
            or retry.get("cancelled") is not False
            or retry.get("recursive") is not False):
        return "ADP-RTY-001"

    delivery = proposal.get("delivery", {})
    if (delivery.get("mode") not in {"stream", "webhook", "push", "poll"}
            or not all(delivery.get(key) for key in ("authorization_context", "sequence_authority", "gap_policy", "terminal_evidence"))
            or delivery.get("dedup") is not True
            or not isinstance(delivery.get("max_reorder"), int) or delivery.get("max_reorder") < 0
            or delivery.get("gaps") != []
            or delivery.get("bounded") is not True
            or delivery.get("stream_close_is_completion") is not False):
        return "ADP-DEL-001"

    security = proposal.get("security", {})
    network = security.get("network_policy", {})
    if (security.get("credential_mode") != "external-capability-domain"
            or any(security.get(key) is not True for key in ("audience_bound", "scope_bound", "session_bound", "tenant_filter", "resource_bounds"))
            or security.get("token_passthrough") is not False
            or security.get("static_secret_embedded") is not False
            or not security.get("disclosure")
            or any(network.get(key) is not True for key in ("ssrf", "redirect", "origin", "dns_rebinding"))
            or network.get("private_addresses") != "deny"):
        return "ADP-SEC-001"
    return None


def main():
    errors = []
    try:
        vectors = json.loads(VECTOR_PATH.read_text())
        catalog = CATALOG_PATH.read_text()
        registry = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load adapter consistency sources: {exc}")
        return 1

    if vectors.get("vector_format") != "adp-core.vector.v1" or vectors.get("spec") != {"id": "ADP-CORE", "version": "0.1.0-draft"}:
        errors.append("adapter vectors must bind ADP-CORE 0.1.0-draft")
    if "not an MCP" not in vectors.get("description", ""):
        errors.append("adapter vectors must state their non-implementation boundary")
    if not any(document.get("spec_id") == "ADP-CORE" for document in registry.get("documents", [])):
        errors.append("registry must contain ADP-CORE")
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
            errors.append(f"invalid or duplicate adapter case ID: {case_id}")
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
        errors.append(f"adapter vectors require 12 accepts and 12 rejects, got {counts}")
    if accepted != CLAUSES:
        errors.append(f"adapter accept coverage must include {sorted(CLAUSES)}, got {sorted(accepted)}")
    if rejected != CLAUSES:
        errors.append(f"adapter reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 24 adapter vectors (12 accepted envelopes, 12 deterministic rejects across 12 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
