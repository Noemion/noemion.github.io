from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "diagnostics" / "cases.json"
CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
CASE_ID = re.compile(r"^DI-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "DIA-IDN-001", "DIA-PIN-001", "DIA-LAY-001", "DIA-LOC-001",
    "DIA-PRI-001", "DIA-REC-001", "DIA-EXT-001", "DIA-SEC-001",
    "DIA-BND-001", "DIA-ATM-001",
}
LAYERS = {
    "source", "structure", "profile", "semantic", "closure", "session",
    "evidence", "policy", "protocol", "backend", "internal",
}
LOCATION_KINDS = {
    "source_range", "byte_range", "record_id", "semantic_path", "graph_path",
    "session_binding", "evidence_ref", "external_request",
}
RECOVERY_CLASSES = {
    "fix-input", "refresh-binding", "obtain-authority", "retry-transient",
    "operator-review", "do-not-retry",
}
DIAGNOSTIC_BY_CLAUSE = {
    "DIA-IDN-001": "diagnostic.identity.unregistered",
    "DIA-PIN-001": "diagnostic.context.unpinned",
    "DIA-LAY-001": "diagnostic.layer.coerced",
    "DIA-LOC-001": "diagnostic.location.invalid",
    "DIA-PRI-001": "diagnostic.primary.nondeterministic",
    "DIA-REC-001": "diagnostic.recovery.unauthorized",
    "DIA-EXT-001": "diagnostic.external.unmapped",
    "DIA-SEC-001": "diagnostic.disclosure.secret",
    "DIA-BND-001": "diagnostic.budget.exceeded",
    "DIA-ATM-001": "diagnostic.atomicity.partial_success",
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
    identity = proposal.get("identity")
    if (
        not isinstance(identity, dict)
        or not identity.get("code")
        or identity.get("registered") is not True
        or identity.get("unique") is not True
        or not identity.get("title")
        or identity.get("message_advisory") is not True
        or identity.get("consumer_parses_message") is not False
        or identity.get("rendering_preserves_identity") is not True
    ):
        return "DIA-IDN-001"
    context = proposal.get("context")
    if (
        not isinstance(context, dict)
        or not context.get("producer")
        or not context.get("operation")
        or not context.get("subject")
        or not isinstance(context.get("spec_versions"), list)
        or len(context.get("spec_versions")) < 2
        or not context.get("occurrence")
        or context.get("mutable_selector") is not False
        or context.get("volatile_in_identity") is not False
    ):
        return "DIA-PIN-001"
    layer = proposal.get("layer")
    if (
        not isinstance(layer, dict)
        or layer.get("kind") not in LAYERS
        or not layer.get("executed_through")
        or layer.get("source_preserved") is not True
        or layer.get("result_domains_separate") is not True
        or layer.get("external_status_promotes") is not False
    ):
        return "DIA-LAY-001"
    location = proposal.get("location")
    if (
        not isinstance(location, dict)
        or location.get("kind") not in LOCATION_KINDS
        or location.get("value") in (None, "")
        or location.get("typed") is not True
        or location.get("bounded") is not True
        or location.get("escaped") is not True
        or location.get("raw_attacker_text") is not False
    ):
        return "DIA-LOC-001"
    primary = proposal.get("primary")
    if (
        not isinstance(primary, dict)
        or primary.get("single") is not True
        or primary.get("deterministic") is not True
        or primary.get("precedence") != "layer-rule-location-code"
        or primary.get("arrival_order_used") is not False
        or primary.get("related_ordered") is not True
    ):
        return "DIA-PRI-001"
    recovery = proposal.get("recovery")
    if (
        not isinstance(recovery, dict)
        or recovery.get("class") not in RECOVERY_CLASSES
        or recovery.get("preconditions_declared") is not True
        or recovery.get("scope_declared") is not True
        or recovery.get("grants_authority") is not False
        or recovery.get("mutates_artifact") is not False
        or recovery.get("budget_bound") is not True
    ):
        return "DIA-REC-001"
    external = proposal.get("external")
    if (
        not isinstance(external, dict)
        or not external.get("origin")
        or not external.get("protocol")
        or external.get("structured_status_preserved") is not True
        or not external.get("local_mapping")
        or external.get("message_parsed") is not False
        or external.get("unknown_becomes_success") is not False
    ):
        return "DIA-EXT-001"
    security = proposal.get("security")
    if (
        not isinstance(security, dict)
        or security.get("contains_live_secret") is not False
        or security.get("default_minimal") is not True
        or not security.get("redaction_policy")
        or security.get("redaction_effect_declared") is not True
        or security.get("debug_material_separate") is not True
    ):
        return "DIA-SEC-001"
    bounds = proposal.get("bounds")
    if (
        not isinstance(bounds, dict)
        or any(not isinstance(bounds.get(name), int) or bounds.get(name) <= 0 for name in (
            "max_diagnostics", "max_cause_depth", "max_locations",
            "max_message_bytes", "max_output_bytes",
        ))
        or bounds.get("checked_before_allocation") is not True
        or bounds.get("primary_survives_truncation") is not True
    ):
        return "DIA-BND-001"
    atomicity = proposal.get("atomicity")
    if (
        not isinstance(atomicity, dict)
        or atomicity.get("blocking") is not True
        or atomicity.get("partial_trusted_output") is not False
        or atomicity.get("success_status") is not False
        or atomicity.get("unexecuted_layers") != "not-run"
        or atomicity.get("warning_promotes_state") is not False
    ):
        return "DIA-ATM-001"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
        catalog = CATALOG_PATH.read_text()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read diagnostic vectors or catalog: {exc}")
        return 1
    if document.get("vector_format") != "dia-core.vector.v1":
        errors.append("diagnostic vectors must use dia-core.vector.v1")
    if document.get("spec") != {"id": "DIA-CORE", "version": "0.1.0-draft"}:
        errors.append("diagnostic vectors must pin DIA-CORE 0.1.0-draft")
    if document.get("catalog") != {"id": "DIA-CAT", "version": "0.1.0-draft"}:
        errors.append("diagnostic vectors must pin DIA-CAT 0.1.0-draft")
    if "not a diagnostic producer, renderer, logger, retry engine, protocol adapter, CLI, runtime, or component implementation" not in document.get("description", ""):
        errors.append("diagnostic vectors must state their non-implementation boundary")
    baseline = document.get("baseline")
    if not isinstance(baseline, dict):
        errors.append("diagnostic vectors require a baseline proposal")
        baseline = {}
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 20:
        errors.append("diagnostic vectors require exactly 20 proposal cases")
        cases = []
    for code in DIAGNOSTIC_BY_CLAUSE.values():
        if f"`{code}`" not in catalog:
            errors.append(f"diagnostic catalog is missing {code}")
    seen = set()
    counts = {"accept": 0, "reject": 0}
    accepted = set()
    rejected = set()
    for index, case in enumerate(cases):
        case_id = case.get("id") if isinstance(case, dict) else None
        if not isinstance(case_id, str) or CASE_ID.fullmatch(case_id) is None or case_id in seen:
            errors.append(f"case[{index}]: invalid or duplicate id {case_id!r}")
            continue
        seen.add(case_id)
        expect = case.get("expect")
        if not isinstance(expect, dict) or expect.get("result") not in counts or expect.get("clause") not in CLAUSES:
            errors.append(f"{case_id}: invalid expectation")
            continue
        proposal = deep_merge(baseline, case.get("proposal", {}))
        violation = proposal_violation(proposal)
        actual = "reject" if violation else "accept"
        counts[actual] += 1
        if violation:
            rejected.add(violation)
        else:
            accepted.add(expect["clause"])
        expected_diagnostic = expect.get("diagnostic")
        if violation and expected_diagnostic != DIAGNOSTIC_BY_CLAUSE[violation]:
            errors.append(f"{case_id}: expected diagnostic does not match {violation}")
        if actual != expect["result"] or (violation and violation != expect["clause"]):
            errors.append(f"{case_id}: expected {expect}, evaluated {actual}/{violation}")
    if counts != {"accept": 10, "reject": 10}:
        errors.append(f"diagnostic vectors require 10 accepts and 10 rejects, got {counts}")
    if accepted != CLAUSES:
        errors.append(f"diagnostic accept coverage must include {sorted(CLAUSES)}, got {sorted(accepted)}")
    if rejected != CLAUSES:
        errors.append(f"diagnostic reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 20 diagnostic vectors (10 accepted envelopes, 10 deterministic rejects across 10 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
