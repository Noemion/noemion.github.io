from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registry.json"
SPEC_PATH = ROOT / "spec" / "endem-core.md"
THREAT_PATH = ROOT / "spec" / "endem-threat-model.md"
VECTOR_ROOT = ROOT / "vectors" / "semantic"
SCHEMA_PATH = ROOT / "vectors" / "vector.schema.json"

CLAUSE_ID = re.compile(r"^END-[A-Z]+-[0-9]{3}$")
VECTOR_ID = re.compile(r"^SV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
SPEC_HEADING = re.compile(r"^### (END-[A-Z]+-[0-9]{3})\s+—", re.MULTILINE)
THREAT_HEADING = re.compile(r"^### (THR-END-[0-9]{3})\s+—", re.MULTILINE)
REQUIRED_FACETS = ("rhem", "semion", "skena", "telis", "krin", "apor")
ALLOWED_VERIFICATION_STATUS = {"covered-by-repo", "planned", "manual-authority"}
ALLOWED_EVIDENCE_STATUS = {"planned", "partial", "covered"}


def load_json(path, errors):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot load JSON: {exc}")
        return None


def validate_registry(registry, spec_text, threat_text, errors):
    if registry.get("registry_version") != 1:
        errors.append("spec/registry.json: registry_version must be 1")

    documents = registry.get("documents")
    if not isinstance(documents, list) or len(documents) != 1:
        errors.append("spec/registry.json: exactly one current specification document is required")
    else:
        document = documents[0]
        expected_document = {
            "spec_id": "END-CORE",
            "version": "0.1.0-draft",
            "status": "draft",
            "implementation_status": "unimplemented",
            "wire_status": "unfrozen",
            "path": "spec/endem-core.md",
        }
        for key, value in expected_document.items():
            if document.get(key) != value:
                errors.append(
                    f"spec/registry.json: document {key} must be {value!r}"
                )
        if not (ROOT / document.get("path", "")).is_file():
            errors.append("spec/registry.json: document path does not exist")

    supporting_documents = registry.get("supporting_documents")
    if not isinstance(supporting_documents, list) or len(supporting_documents) != 1:
        errors.append("spec/registry.json: exactly one threat-model supporting document is required")
    else:
        threat_document = supporting_documents[0]
        if threat_document.get("id") != "END-THREAT":
            errors.append("spec/registry.json: threat model ID must be END-THREAT")
        if threat_document.get("version") != "0.1.0-draft":
            errors.append("spec/registry.json: threat model version must be 0.1.0-draft")
        if threat_document.get("path") != "spec/endem-threat-model.md":
            errors.append("spec/registry.json: threat model path is incorrect")
        if not (ROOT / threat_document.get("path", "")).is_file():
            errors.append("spec/registry.json: threat model path does not exist")

    terms = registry.get("terms")
    if not isinstance(terms, list) or not terms:
        errors.append("spec/registry.json: terms must be a non-empty list")
    else:
        term_names = [term.get("term") for term in terms]
        if len(term_names) != len(set(term_names)):
            errors.append("spec/registry.json: term names must be unique")
        for required_term in (
            "Noemion", "Endem", "Synem", "Dromen", "Tekmor",
            *REQUIRED_FACETS, "wire-format",
        ):
            if required_term not in term_names:
                errors.append(f"spec/registry.json: missing term {required_term}")
        wire_term = next((term for term in terms if term.get("term") == "wire-format"), None)
        if wire_term and wire_term.get("decision_status") != "unresolved":
            errors.append("spec/registry.json: wire-format must remain unresolved")

    spec_clause_ids = SPEC_HEADING.findall(spec_text)
    if not spec_clause_ids:
        errors.append("spec/endem-core.md: no normative clause headings found")
    if len(spec_clause_ids) != len(set(spec_clause_ids)):
        errors.append("spec/endem-core.md: clause headings must be unique")

    clauses = registry.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        errors.append("spec/registry.json: clauses must be a non-empty list")
        return set(), set()

    registry_clause_ids = [clause.get("id") for clause in clauses]
    if len(registry_clause_ids) != len(set(registry_clause_ids)):
        errors.append("spec/registry.json: clause IDs must be unique")
    for clause_id in registry_clause_ids:
        if not isinstance(clause_id, str) or not CLAUSE_ID.fullmatch(clause_id):
            errors.append(f"spec/registry.json: invalid clause ID {clause_id!r}")

    if set(registry_clause_ids) != set(spec_clause_ids):
        missing_registry = sorted(set(spec_clause_ids) - set(registry_clause_ids))
        missing_spec = sorted(set(registry_clause_ids) - set(spec_clause_ids))
        errors.append(
            "spec clause registry mismatch: "
            f"missing_registry={missing_registry}, missing_spec={missing_spec}"
        )

    threat_heading_ids = THREAT_HEADING.findall(threat_text)
    threats = registry.get("threats")
    if not isinstance(threats, list) or len(threats) < 10:
        errors.append("spec/registry.json: at least 10 registered Endem threats are required")
    else:
        threat_ids = [threat.get("id") for threat in threats]
        if len(threat_ids) != len(set(threat_ids)):
            errors.append("spec/registry.json: threat IDs must be unique")
        if set(threat_ids) != set(threat_heading_ids):
            errors.append(
                "threat registry mismatch: "
                f"missing_registry={sorted(set(threat_heading_ids) - set(threat_ids))}, "
                f"missing_document={sorted(set(threat_ids) - set(threat_heading_ids))}"
            )
        for threat in threats:
            threat_id = threat.get("id", "<unknown>")
            if not re.fullmatch(r"THR-END-[0-9]{3}", threat_id):
                errors.append(f"spec/registry.json: invalid threat ID {threat_id!r}")
            mapped_clauses = threat.get("clauses")
            if not isinstance(mapped_clauses, list) or not mapped_clauses:
                errors.append(f"{threat_id}: must map to one or more clauses")
            else:
                unknown = sorted(set(mapped_clauses) - set(registry_clause_ids))
                if unknown:
                    errors.append(f"{threat_id}: unknown mapped clauses {unknown}")
            if threat.get("evidence_status") not in {"planned", "partial"}:
                errors.append(f"{threat_id}: invalid evidence_status")

    covered_vector_refs = set()
    covered_repo_refs = set()
    for clause in clauses:
        clause_id = clause.get("id", "<unknown>")
        for field in (
            "decision_status", "implementation_status", "evidence_status",
            "failure_owner", "verification",
        ):
            if field not in clause:
                errors.append(f"{clause_id}: missing registry field {field}")
        if clause.get("implementation_status") != "unimplemented":
            errors.append(f"{clause_id}: implementation must remain unimplemented")
        if clause.get("evidence_status") not in ALLOWED_EVIDENCE_STATUS:
            errors.append(f"{clause_id}: invalid evidence_status")
        verification = clause.get("verification")
        if not isinstance(verification, list) or not verification:
            errors.append(f"{clause_id}: verification must be a non-empty list")
            continue
        for item in verification:
            status = item.get("status")
            if status not in ALLOWED_VERIFICATION_STATUS:
                errors.append(f"{clause_id}: invalid verification status {status!r}")
                continue
            if status in {"covered-by-repo", "planned"} and not item.get("ref"):
                errors.append(f"{clause_id}: {status} verification requires ref")
            if status == "manual-authority" and not item.get("authority"):
                errors.append(f"{clause_id}: manual-authority requires authority")
            if status == "covered-by-repo":
                ref = item["ref"]
                ref_path = ROOT / ref
                if not ref_path.is_file():
                    errors.append(f"{clause_id}: covered evidence does not exist: {ref}")
                covered_repo_refs.add(ref)
                if ref.startswith("vectors/semantic/"):
                    covered_vector_refs.add(ref)

    return set(registry_clause_ids), covered_vector_refs


def validate_vectors(clause_ids, covered_vector_refs, errors):
    if not SCHEMA_PATH.is_file():
        errors.append("missing vectors/vector.schema.json")
    else:
        schema = load_json(SCHEMA_PATH, errors)
        if schema and schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("vectors/vector.schema.json: must pin JSON Schema 2020-12")

    vector_paths = sorted(VECTOR_ROOT.glob("*.json"))
    if not vector_paths:
        errors.append("vectors/semantic: no vectors found")
        return

    vector_refs = {path.relative_to(ROOT).as_posix() for path in vector_paths}
    if vector_refs != covered_vector_refs:
        errors.append(
            "semantic vector registry mismatch: "
            f"unregistered={sorted(vector_refs - covered_vector_refs)}, "
            f"missing={sorted(covered_vector_refs - vector_refs)}"
        )

    vector_ids = []
    accept_count = 0
    reject_count = 0
    rejected_clause_ids = set()
    for path in vector_paths:
        vector = load_json(path, errors)
        if vector is None:
            continue
        label = path.relative_to(ROOT).as_posix()
        if vector.get("vector_format") != "noemion.semantic-vector.v1":
            errors.append(f"{label}: invalid vector_format")
        vector_id = vector.get("id")
        if not isinstance(vector_id, str) or not VECTOR_ID.fullmatch(vector_id):
            errors.append(f"{label}: invalid vector id {vector_id!r}")
        else:
            vector_ids.append(vector_id)
        if vector.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
            errors.append(f"{label}: must pin END-CORE 0.1.0-draft")

        input_model = vector.get("input")
        if not isinstance(input_model, dict):
            errors.append(f"{label}: input must be an object")
        else:
            missing_facets = [facet for facet in REQUIRED_FACETS if facet not in input_model]
            if missing_facets:
                errors.append(f"{label}: missing semantic facets {missing_facets}")

        expect = vector.get("expect")
        if not isinstance(expect, dict):
            errors.append(f"{label}: expect must be an object")
            continue
        result = expect.get("result")
        expected_clauses = expect.get("clauses")
        diagnostics = expect.get("diagnostics")
        if result not in {"accept", "reject"}:
            errors.append(f"{label}: result must be accept or reject")
        if not isinstance(expected_clauses, list) or not expected_clauses:
            errors.append(f"{label}: clauses must be a non-empty list")
            expected_clauses = []
        elif len(expected_clauses) != len(set(expected_clauses)):
            errors.append(f"{label}: clauses must be unique")
        unknown_clauses = sorted(set(expected_clauses) - clause_ids)
        if unknown_clauses:
            errors.append(f"{label}: unknown clauses {unknown_clauses}")
        if not isinstance(diagnostics, list):
            errors.append(f"{label}: diagnostics must be a list")
            diagnostics = []

        if result == "accept":
            accept_count += 1
            if diagnostics:
                errors.append(f"{label}: accept vector must not contain diagnostics")
        elif result == "reject":
            reject_count += 1
            if not diagnostics:
                errors.append(f"{label}: reject vector requires diagnostics")
            for diagnostic in diagnostics:
                if not isinstance(diagnostic, dict):
                    errors.append(f"{label}: diagnostic must be an object")
                    continue
                diagnostic_clause = diagnostic.get("clause")
                rejected_clause_ids.add(diagnostic_clause)
                if diagnostic_clause not in expected_clauses:
                    errors.append(
                        f"{label}: diagnostic clause {diagnostic_clause!r} "
                        "must appear in expect.clauses"
                    )
                code = diagnostic.get("code")
                if not isinstance(code, str) or not code.startswith("endem."):
                    errors.append(f"{label}: diagnostic code must start with endem.")
                location = diagnostic.get("location")
                if not isinstance(location, str) or not location.startswith("/"):
                    errors.append(f"{label}: diagnostic location must be a JSON Pointer")

    if len(vector_ids) != len(set(vector_ids)):
        errors.append("semantic vector IDs must be unique")
    if accept_count < 1 or reject_count < 4:
        errors.append("semantic vectors require at least one accept and four reject cases")
    for required_reject_clause in (
        "END-CORE-001", "END-SIT-001", "END-APR-001", "END-AUT-001",
    ):
        if required_reject_clause not in rejected_clause_ids:
            errors.append(f"missing direct rejection vector for {required_reject_clause}")


def validate_public_boundary(errors):
    config_text = (ROOT / "_config.yml").read_text()
    for exact_exclusion in ("  - spec/", "  - vectors/"):
        if exact_exclusion not in config_text:
            errors.append(f"_config.yml: missing exact exclusion {exact_exclusion.strip()!r}")
    if re.search(r"^\s*-\s+(?:spec|vectors)\s*$", config_text, re.MULTILINE):
        errors.append(
            "_config.yml: bare spec/vectors exclusions can also hide prefix-matching public routes"
        )

    public_contracts = {
        "specifications/index.html": (
            "END-CORE 0.1.0-draft",
            "spec/endem-core.md",
            "spec/registry.json",
            "vectors/semantic",
            "spec/endem-threat-model.md",
            "不是 .endem 线格式",
        ),
        "specifications/endem.html": (
            "END-CORE 0.1.0-draft",
            "spec/endem-core.md",
            "条款 ID",
            "物理编码仍未冻结",
        ),
        "docs/specifications-reference.md": (
            "END-CORE 0.1.0-draft",
            "spec/endem-core.md",
            "机器可读登记",
            "spec/endem-threat-model.md",
        ),
    }
    for relative_path, tokens in public_contracts.items():
        text = (ROOT / relative_path).read_text()
        for token in tokens:
            if token not in text:
                errors.append(f"{relative_path}: missing normative-source boundary {token!r}")


def main():
    errors = []
    registry = load_json(REGISTRY_PATH, errors)
    try:
        spec_text = SPEC_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-core.md: cannot read: {exc}")
        spec_text = ""
    try:
        threat_text = THREAT_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-threat-model.md: cannot read: {exc}")
        threat_text = ""

    if registry is not None:
        clause_ids, covered_vector_refs = validate_registry(
            registry, spec_text, threat_text, errors
        )
        validate_vectors(clause_ids, covered_vector_refs, errors)
    validate_public_boundary(errors)

    if errors:
        print("\n".join(errors))
        return 1
    print(
        "PASS: END-CORE 0.1.0-draft has unique clauses, explicit maturity, "
        "traceable evidence, 10 registered threats, and 5 semantic vectors"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
