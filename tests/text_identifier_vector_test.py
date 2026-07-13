from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "text-identifier" / "cases.json"
CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CASE_ID = re.compile(r"^TEXT-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "TEXT-SLT-001", "TEXT-ENC-001", "TEXT-SRC-001", "TEXT-IDN-001",
    "TEXT-NRM-001", "TEXT-CMP-001", "TEXT-RNG-001", "TEXT-BID-001",
    "TEXT-HID-001", "TEXT-MET-001", "TEXT-AIM-001", "TEXT-OUT-001",
}
DIAGNOSTIC_BY_CLAUSE = {
    "TEXT-SLT-001": "text.slot.untyped",
    "TEXT-ENC-001": "text.encoding.invalid",
    "TEXT-SRC-001": "text.source.provenance_incomplete",
    "TEXT-IDN-001": "text.identifier.out_of_profile",
    "TEXT-NRM-001": "text.normalization.implicit",
    "TEXT-CMP-001": "text.comparison.domain_unbound",
    "TEXT-RNG-001": "text.range.unit_mismatch",
    "TEXT-BID-001": "text.bidi.boundary_hidden",
    "TEXT-HID-001": "text.hidden.silent",
    "TEXT-MET-001": "text.metadata.overclaimed",
    "TEXT-AIM-001": "text.model.view_unbound",
    "TEXT-OUT-001": "text.output.provenance_missing",
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
    slot = proposal.get("slot", {})
    if (slot.get("kind") not in {"source-content", "structural-identifier", "registered-token", "descriptive-text", "display-message"}
            or not all(slot.get(key) for key in ("profile", "normative_use", "failure_effect"))
            or any(slot.get(key) is not True for key in ("encoding_rules_bound", "comparison_rules_bound", "display_rules_bound"))):
        return "TEXT-SLT-001"

    encoding = proposal.get("encoding", {})
    if (encoding.get("name") != "UTF-8"
            or any(encoding.get(key) is not True for key in ("rfc3629", "valid", "shortest_form", "scalar_values_only", "decoded_before_transform", "invalid_fails_atomic"))
            or encoding.get("implicit_local_encoding") is not False):
        return "TEXT-ENC-001"

    source = proposal.get("source", {})
    if (not all(source.get(key) for key in ("source_byte_identity", "decoded_text_identity", "charset", "decode_profile"))
            or not isinstance(source.get("transforms"), list) or not source.get("transforms")
            or not isinstance(source.get("loss_manifest"), list)
            or source.get("relation_explicit") is not True
            or source.get("decoded_content_preserved") is not True
            or source.get("claims_raw_byte_preservation") is not False
            or source.get("silent_deletion") is not False):
        return "TEXT-SRC-001"

    identifier = proposal.get("identifier", {})
    if (identifier.get("class") != "ascii-current-profile"
            or not identifier.get("pattern")
            or not isinstance(identifier.get("byte_length"), int) or not 1 <= identifier.get("byte_length") <= 255
            or identifier.get("normalization") != "none"
            or identifier.get("case_sensitive") is not True
            or identifier.get("locale_independent") is not True
            or identifier.get("unicode_extension") is not False
            or identifier.get("confusable_matching") is not False):
        return "TEXT-IDN-001"

    normalization = proposal.get("normalization", {})
    if (not all(normalization.get(key) for key in ("profile", "slot", "unicode_version"))
            or normalization.get("form") not in {"none", "NFC", "NFD", "NFKC", "NFKD"}
            or normalization.get("explicit") is not True
            or normalization.get("compatibility_blind") is not False
            or normalization.get("changes_create_new_identity") is not True
            or normalization.get("original_preserved") is not True
            or normalization.get("semantic_equivalence_claim") is not False):
        return "TEXT-NRM-001"

    comparison = proposal.get("comparison", {})
    if (not all(comparison.get(key) for key in ("profile", "domain", "unicode_version", "result_scope"))
            or comparison.get("domain") not in {"exact-bytes", "unicode-scalars", "normalized-text", "case-mapped-text", "locale-collation", "confusable-risk"}
            or comparison.get("operands_same_slot") is not True
            or comparison.get("normalization") not in {"none", "NFC", "NFD", "NFKC", "NFKD"}
            or comparison.get("confusable_equivalence") is not False
            or comparison.get("locale") == "process-default"):
        return "TEXT-CMP-001"

    text_range = proposal.get("range", {})
    if (not all(text_range.get(key) for key in ("subject_identity", "representation", "unit"))
            or text_range.get("unit") != "unicode-scalar"
            or not isinstance(text_range.get("start"), int) or text_range.get("start") < 0
            or not isinstance(text_range.get("length"), int) or text_range.get("length") <= 0
            or text_range.get("half_open") is not True
            or text_range.get("checked_arithmetic") is not True
            or text_range.get("transform_map") not in {None, "explicit"}
            or any(text_range.get(key) is not False for key in ("bytes_as_scalars", "graphemes_as_scalars", "tokens_as_scalars"))):
        return "TEXT-RNG-001"

    bidi = proposal.get("bidi", {})
    if (bidi.get("storage_order") != "logical"
            or not bidi.get("uax9_version")
            or any(bidi.get(key) is not True for key in ("slot_isolation", "control_inventory", "review_reveals_controls"))
            or bidi.get("structural_controls_allowed") is not False
            or bidi.get("display_order_used_for_identity") is not False
            or bidi.get("display_rewrites_storage") is not False):
        return "TEXT-BID-001"

    hidden = proposal.get("hidden", {})
    if (not hidden.get("unicode_version")
            or hidden.get("inventory") is not True
            or not isinstance(hidden.get("categories"), list) or not hidden.get("categories")
            or hidden.get("source_preserved") is not True
            or hidden.get("structural_allowed") is not False
            or hidden.get("review_visualization") is not True
            or hidden.get("warning_is_identity") is not False
            or hidden.get("skeleton_is_identity") is not False
            or hidden.get("auto_rewrite") is not False):
        return "TEXT-HID-001"

    metadata = proposal.get("metadata", {})
    if (not all(metadata.get(key) for key in ("language_tag", "media_type"))
            or metadata.get("declarations_validated") is not True
            or metadata.get("declaration_only") is not True
            or metadata.get("locale_affects_normative_result") is not False
            or metadata.get("unicode_version_pinned") is not True
            or metadata.get("language_transform_profile") is not None
            or metadata.get("model_detection_is_fact") is not False):
        return "TEXT-MET-001"

    model = proposal.get("model", {})
    if (not all(model.get(key) for key in ("input_identity", "hidden_inventory_ref", "model_identity", "tokenizer_identity", "display_view_identity"))
            or not isinstance(model.get("transform_chain"), list) or not model.get("transform_chain")
            or model.get("view_difference_declared") is not True
            or model.get("output_class") != "model-candidate"
            or any(model.get(key) is not False for key in ("may_authorize", "may_write_normative", "may_drop_hidden"))):
        return "TEXT-AIM-001"

    output = proposal.get("output", {})
    if (not all(output.get(key) for key in ("source_identity", "view_profile"))
            or any(output.get(key) is not True for key in ("escaping_declared", "truncation_declared", "normalization_declared", "direction_isolation_declared", "control_visualization_available", "copy_exact_available", "loss_effects_declared"))
            or output.get("display_used_for_binding") is not False):
        return "TEXT-OUT-001"
    return None


def main():
    errors = []
    try:
        vectors = json.loads(VECTOR_PATH.read_text())
        catalog = CATALOG_PATH.read_text()
        registry = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load text consistency sources: {exc}")
        return 1

    if vectors.get("vector_format") != "text-identifier-core.vector.v1" or vectors.get("spec") != {"id": "TEXT-IDENTIFIER-CORE", "version": "0.1.0-draft"}:
        errors.append("text vectors must bind TEXT-IDENTIFIER-CORE 0.1.0-draft")
    description = vectors.get("description", "")
    if "not a Unicode processor" not in description or "not a" not in description:
        errors.append("text vectors must state the non-implementation boundary")
    if not any(document.get("spec_id") == "TEXT-IDENTIFIER-CORE" for document in registry.get("documents", [])):
        errors.append("registry must contain TEXT-IDENTIFIER-CORE")
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
            errors.append(f"invalid or duplicate text case ID: {case_id}")
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
        errors.append(f"text vectors require 12 accepts and 12 rejects, got {counts}")
    if accepted != CLAUSES:
        errors.append(f"text accept coverage must include {sorted(CLAUSES)}, got {sorted(accepted)}")
    if rejected != CLAUSES:
        errors.append(f"text reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 24 text vectors (12 accepted proposals, 12 deterministic rejects across 12 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
