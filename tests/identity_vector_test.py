from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "identity" / "cases.json"
CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CASE_ID = re.compile(r"^ID-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "ID-DOM-001", "ID-BYT-001", "ID-REF-001", "ID-ALG-001",
    "ID-DSP-001", "ID-EQV-001", "ID-STM-001", "ID-ENV-001",
    "ID-AUT-001", "ID-VAL-001", "ID-REP-001", "ID-REL-001",
}
DIAGNOSTIC_BY_CLAUSE = {
    "ID-DOM-001": "identity.domain.unbound",
    "ID-BYT-001": "identity.bytes.input_undefined",
    "ID-REF-001": "identity.reference.mutable",
    "ID-ALG-001": "identity.algorithm.disallowed",
    "ID-DSP-001": "identity.display.used_for_binding",
    "ID-EQV-001": "identity.equivalence.overclaimed",
    "ID-STM-001": "identity.statement.context_incomplete",
    "ID-ENV-001": "identity.envelope.material_incomplete",
    "ID-AUT-001": "identity.authority.overclaimed",
    "ID-VAL-001": "identity.validity.context_incomplete",
    "ID-REP-001": "identity.reproducibility.unproven",
    "ID-REL-001": "identity.relation.inherited",
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
    domain = proposal.get("domain", {})
    if (not all(domain.get(key) for key in ("id", "version", "object_kind", "object_spec", "representation", "profile"))
            or domain.get("input_boundary_defined") is not True
            or domain.get("all_context_compared") is not True):
        return "ID-DOM-001"

    byte_input = proposal.get("bytes", {})
    byte_range = byte_input.get("range")
    if (byte_input.get("input_kind") not in {"whole-object", "normative-byte-range"}
            or not isinstance(byte_range, dict)
            or not isinstance(byte_range.get("start"), int) or byte_range.get("start") < 0
            or not isinstance(byte_range.get("length"), int) or byte_range.get("length") <= 0
            or not byte_input.get("ordering")
            or byte_input.get("normalization") not in {"none", "normative-canonicalization"}
            or not isinstance(byte_input.get("includes"), list)
            or not isinstance(byte_input.get("excludes"), list)
            or byte_input.get("mutable_source") is not False
            or byte_input.get("self_referential") is not False
            or byte_input.get("envelope_included") is not False):
        return "ID-BYT-001"

    reference = proposal.get("reference", {})
    if (not all(reference.get(key) for key in ("domain", "object_kind", "object_spec", "representation", "profile", "algorithm", "output_bits", "digest", "encoding"))
            or not isinstance(reference.get("output_bits"), int) or reference.get("output_bits") <= 0
            or reference.get("complete") is not True
            or reference.get("mutable_selector") is not False
            or reference.get("matches_one_allowed_identity") is not True):
        return "ID-REF-001"

    algorithm = proposal.get("algorithm_policy", {})
    if (not all(algorithm.get(key) for key in ("registry", "algorithm", "purpose", "parameters", "status", "minimum_security_bits"))
            or algorithm.get("status") != "allowed-for-proposal"
            or algorithm.get("registered") is not True
            or algorithm.get("parameters_pinned") is not True
            or algorithm.get("unknown_fails_closed") is not True
            or algorithm.get("silent_substitution") is not False
            or algorithm.get("release_algorithm_selected") is not False):
        return "ID-ALG-001"

    display = proposal.get("display", {})
    if (not display.get("short")
            or display.get("display_only") is not True
            or display.get("binding_uses_full") is not True
            or display.get("ambiguity_action") != "expand-or-require-full"
            or display.get("first_match_allowed") is not False
            or display.get("build_id_is_checksum") is not False):
        return "ID-DSP-001"

    equivalence = proposal.get("equivalence", {})
    if (equivalence.get("exact_identity_only") is not True
            or equivalence.get("semantic_key") is not None
            or equivalence.get("same_means_true") is not False
            or equivalence.get("different_means_semantically_different") is not False
            or equivalence.get("derived_inherits_identity") is not False
            or equivalence.get("equivalence_claim") is not None):
        return "ID-EQV-001"

    statement = proposal.get("statement", {})
    if (not all(statement.get(key) for key in ("profile", "context", "payload_type", "object_reference", "object_kind", "object_spec", "object_profile", "claim_kind", "purpose", "audience", "subject", "policy"))
            or not isinstance(statement.get("evidence_refs"), list)
            or statement.get("critical_fields_protected") is not True
            or statement.get("algorithm_protected") is not True
            or statement.get("cross_context_replay_allowed") is not False):
        return "ID-STM-001"

    envelope = proposal.get("envelope", {})
    materials = set(envelope.get("verification_material", []))
    if (envelope.get("outside_object_identity") is not True
            or envelope.get("statement_bound") is not True
            or not all(envelope.get(key) for key in ("profile", "signature", "own_identity"))
            or len(materials) < 2 or materials == {"kid"}
            or envelope.get("material_origins_versioned") is not True
            or envelope.get("missing_effects_declared") is not True
            or envelope.get("key_id_is_hint_only") is not True
            or envelope.get("inherits_subject_identity") is not False):
        return "ID-ENV-001"

    authority = proposal.get("authority", {})
    if (authority.get("cryptographic_verification") is not True
            or any(authority.get(key) is not True for key in ("signer_authenticated", "role_authorized", "statement_applicable", "policy_satisfied", "domains_separate"))
            or authority.get("final_decision") not in {"accepted", "rejected", "deferred"}
            or any(authority.get(key) is not False for key in ("signature_proves_truth", "signature_grants_capability", "log_inclusion_is_acceptance"))):
        return "ID-AUT-001"

    validity = proposal.get("validity", {})
    if (not all(validity.get(key) for key in ("cutoff", "trust_roots", "policy", "signing_time_basis"))
            or any(validity.get(key) is not True for key in ("key_period_checked", "revocation_checked", "transparency_role_limited", "status_fresh", "offline_material_bounded"))
            or validity.get("cache_unbounded") is not False
            or validity.get("rotation_changes_content_identity") is not False
            or validity.get("revocation_changes_content_identity") is not False):
        return "ID-VAL-001"

    reproducibility = proposal.get("reproducibility", {})
    outputs = reproducibility.get("output_identities", [])
    if (reproducibility.get("claim") != "bit-for-bit"
            or any(reproducibility.get(key) is not True for key in ("inputs_pinned", "dependency_closure_pinned", "tools_pinned", "parameters_pinned", "environment_constrained"))
            or not isinstance(reproducibility.get("independent_paths"), int) or reproducibility.get("independent_paths") < 2
            or len(outputs) != reproducibility.get("independent_paths") or len(set(outputs)) != 1
            or reproducibility.get("byte_comparison") != "equal"
            or reproducibility.get("shared_cache") is not False
            or reproducibility.get("build_id_only") is not False
            or reproducibility.get("difference_cause_claimed") is not None):
        return "ID-REP-001"

    relation = proposal.get("relation", {})
    if (not all(relation.get(key) for key in ("type", "version", "source_identity", "derived_identity", "transformation", "producer"))
            or relation.get("source_identity") == relation.get("derived_identity")
            or not isinstance(relation.get("preserved"), list)
            or not isinstance(relation.get("loss_manifest"), list) or not relation.get("loss_manifest")
            or not isinstance(relation.get("verification_conditions"), list) or not relation.get("verification_conditions")
            or relation.get("raw_source_in_derived") is not False
            or relation.get("source_references_closed") is not True
            or relation.get("companion_public") is not False
            or relation.get("source_fidelity_claim_without_companion") is not False
            or any(relation.get(key) is not False for key in ("inherits_source_identity", "inherits_signature", "inherits_iknem", "inherits_acceptance", "inherits_capability", "semantic_equivalence_claim"))):
        return "ID-REL-001"
    return None


def main():
    errors = []
    try:
        vectors = json.loads(VECTOR_PATH.read_text())
        catalog = CATALOG_PATH.read_text()
        registry = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load identity consistency sources: {exc}")
        return 1

    if vectors.get("vector_format") != "id-core.vector.v1" or vectors.get("spec") != {"id": "ID-CORE", "version": "0.1.0-draft"}:
        errors.append("identity vectors must bind ID-CORE 0.1.0-draft")
    description = vectors.get("description", "")
    if "not a digest" not in description or "not a release algorithm decision" not in description:
        errors.append("identity vectors must state the non-implementation and algorithm-selection boundaries")
    if not any(document.get("spec_id") == "ID-CORE" for document in registry.get("documents", [])):
        errors.append("registry must contain ID-CORE")
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
            errors.append(f"invalid or duplicate identity case ID: {case_id}")
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
        errors.append(f"identity vectors require 12 accepts and 12 rejects, got {counts}")
    if accepted != CLAUSES:
        errors.append(f"identity accept coverage must include {sorted(CLAUSES)}, got {sorted(accepted)}")
    if rejected != CLAUSES:
        errors.append(f"identity reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 24 identity vectors (12 accepted proposals, 12 deterministic rejects across 12 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
