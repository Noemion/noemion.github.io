from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CORE_SPEC_PATH = ROOT / "spec" / "endem-core.md"
FORMAT_SPEC_PATH = ROOT / "spec" / "endem-format.md"
SOURCE_MANIFEST_SPEC_PATH = ROOT / "spec" / "endem-source-manifest.md"
CLOSURE_SPEC_PATH = ROOT / "spec" / "endem-closure-core.md"
SESSION_SPEC_PATH = ROOT / "spec" / "session-contract-core.md"
EVIDENCE_SPEC_PATH = ROOT / "spec" / "evidence-entry-core.md"
DIAGNOSTIC_SPEC_PATH = ROOT / "spec" / "diagnostics-core.md"
ADAPTER_SPEC_PATH = ROOT / "spec" / "adapter-core.md"
IDENTITY_SPEC_PATH = ROOT / "spec" / "identity-core.md"
TEXT_SPEC_PATH = ROOT / "spec" / "text-identifier-core.md"
AUTHORITY_SPEC_PATH = ROOT / "spec" / "authority-core.md"
THREAT_PATHS = (
    ROOT / "spec" / "endem-threat-model.md",
    ROOT / "spec" / "endem-closure-threat-model.md",
    ROOT / "spec" / "session-contract-threat-model.md",
    ROOT / "spec" / "evidence-entry-threat-model.md",
    ROOT / "spec" / "diagnostic-threat-model.md",
    ROOT / "spec" / "adapter-threat-model.md",
    ROOT / "spec" / "identity-threat-model.md",
    ROOT / "spec" / "text-identifier-threat-model.md",
    ROOT / "spec" / "authority-threat-model.md",
)
ERROR_CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
SCENARIO_CORPUS_PATH = ROOT / "spec" / "endem-scenarios.md"
CLOSURE_SCENARIO_PATH = ROOT / "spec" / "endem-closure-scenarios.md"
SESSION_SCENARIO_PATH = ROOT / "spec" / "session-contract-scenarios.md"
EVIDENCE_SCENARIO_PATH = ROOT / "spec" / "evidence-entry-scenarios.md"
DIAGNOSTIC_SCENARIO_PATH = ROOT / "spec" / "diagnostic-scenarios.md"
ADAPTER_SCENARIO_PATH = ROOT / "spec" / "adapter-scenarios.md"
IDENTITY_SCENARIO_PATH = ROOT / "spec" / "identity-scenarios.md"
TEXT_SCENARIO_PATH = ROOT / "spec" / "text-identifier-scenarios.md"
AUTHORITY_SCENARIO_PATH = ROOT / "spec" / "authority-scenarios.md"
PROFILE_PATH = ROOT / "spec" / "profiles" / "end-p0.json"
VECTOR_ROOT = ROOT / "vectors" / "semantic"
SCHEMA_PATH = ROOT / "vectors" / "vector.schema.json"

CLAUSE_ID = re.compile(r"^(?:END|CLOSURE|SESSION|EVIDENCE|DIA|ADP|ID|TEXT|AUT)-[A-Z]+-[0-9]{3}$")
VECTOR_ID = re.compile(r"^SV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
SPEC_HEADING = re.compile(r"^### ((?:END|CLOSURE|SESSION|EVIDENCE|DIA|ADP|ID|TEXT|AUT)-[A-Z]+-[0-9]{3})\s+—", re.MULTILINE)
THREAT_HEADING = re.compile(r"^### (THR-(?:END|CLOSURE|SESSION|EVIDENCE|DIA|ADP|ID|TEXT|AUT)-[0-9]{3})\s+—", re.MULTILINE)
SCENARIO_HEADING = re.compile(r"^### (SCN-[0-9]{3})\s+—", re.MULTILINE)
REQUIRED_FACETS = ("source_expression", "meaning_projection", "situation", "goal_direction", "satisfaction_criteria", "unresolved_meaning")
ALLOWED_VERIFICATION_STATUS = {"covered-by-repo", "planned", "manual-authority"}
ALLOWED_EVIDENCE_STATUS = {"planned", "partial", "covered"}


def source_path_for_route(relative_path):
    direct = ROOT / relative_path
    if direct.exists():
        return direct
    markdown = direct.with_suffix(".md")
    return markdown if markdown.exists() else direct


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
    if not isinstance(documents, list) or len(documents) != 11:
        errors.append("spec/registry.json: eleven current core and format documents are required")
    else:
        documents_by_id = {document.get("spec_id"): document for document in documents}
        expected_documents = {
            "END-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "unfrozen",
                "path": "spec/endem-core.md",
            },
            "END-FMT": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only",
                "wire_status": "experimental-draft", "path": "spec/endem-format.md",
            },
            "END-SRCM": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only",
                "wire_status": "not-applicable", "path": "spec/endem-source-manifest.md",
            },
            "CLOSURE-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "unfrozen",
                "path": "spec/endem-closure-core.md",
            },
            "SESSION-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "not-applicable",
                "path": "spec/session-contract-core.md",
            },
            "EVIDENCE-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "unfrozen",
                "path": "spec/evidence-entry-core.md",
            },
            "DIA-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "unfrozen",
                "path": "spec/diagnostics-core.md",
            },
            "ADP-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "not-applicable",
                "path": "spec/adapter-core.md",
            },
            "ID-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "unfrozen",
                "path": "spec/identity-core.md",
            },
            "TEXT-IDENTIFIER-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "not-applicable",
                "path": "spec/text-identifier-core.md",
            },
            "AUT-CORE": {
                "version": "0.1.0-draft", "status": "draft",
                "implementation_status": "vector-checker-only", "wire_status": "not-applicable",
                "path": "spec/authority-core.md",
            },
        }
        if set(documents_by_id) != set(expected_documents):
            errors.append("spec/registry.json: document IDs must include END, CLOSURE, SESSION, EVIDENCE, DIA, ADP, ID, TEXT-IDENTIFIER and AUT current specifications")
        for spec_id, expected_document in expected_documents.items():
            document = documents_by_id.get(spec_id, {})
            for key, value in expected_document.items():
                if document.get(key) != value:
                    errors.append(
                        f"spec/registry.json: {spec_id} {key} must be {value!r}"
                    )
            if not (ROOT / document.get("path", "")).is_file():
                errors.append(f"spec/registry.json: {spec_id} document path does not exist")

    supporting_documents = registry.get("supporting_documents")
    if not isinstance(supporting_documents, list) or len(supporting_documents) != 21:
        errors.append("spec/registry.json: object and diagnostic threat/scenario documents, diagnostic catalog, P0 and P2 Profiles are required")
    else:
        supporting_by_id = {document.get("id"): document for document in supporting_documents}
        threat_document = supporting_by_id.get("END-THREAT", {})
        if threat_document.get("id") != "END-THREAT":
            errors.append("spec/registry.json: threat model ID must be END-THREAT")
        if threat_document.get("version") != "0.1.0-draft":
            errors.append("spec/registry.json: threat model version must be 0.1.0-draft")
        if threat_document.get("path") != "spec/endem-threat-model.md":
            errors.append("spec/registry.json: threat model path is incorrect")
        if not (ROOT / threat_document.get("path", "")).is_file():
            errors.append("spec/registry.json: threat model path does not exist")
        expected_supporting = {
            "CLOSURE-THREAT": "spec/endem-closure-threat-model.md",
            "EVIDENCE-THREAT": "spec/evidence-entry-threat-model.md",
            "SESSION-THREAT": "spec/session-contract-threat-model.md",
            "DIA-CAT": "spec/diagnostic-catalog.md",
            "DIA-THREAT": "spec/diagnostic-threat-model.md",
            "DIA-SCEN": "spec/diagnostic-scenarios.md",
            "END-SCEN": "spec/endem-scenarios.md",
            "CLOSURE-SCEN": "spec/endem-closure-scenarios.md",
            "EVIDENCE-SCEN": "spec/evidence-entry-scenarios.md",
            "SESSION-SCEN": "spec/session-contract-scenarios.md",
            "END-P0": "spec/profiles/end-p0.json",
            "END-P2": "spec/profiles/end-p2.json",
            "ADP-THREAT": "spec/adapter-threat-model.md",
            "ADP-SCEN": "spec/adapter-scenarios.md",
            "ID-THREAT": "spec/identity-threat-model.md",
            "ID-SCEN": "spec/identity-scenarios.md",
            "TEXT-THREAT": "spec/text-identifier-threat-model.md",
            "TEXT-SCEN": "spec/text-identifier-scenarios.md",
            "AUT-THREAT": "spec/authority-threat-model.md",
            "AUT-SCEN": "spec/authority-scenarios.md",
        }
        for document_id, path in expected_supporting.items():
            document = supporting_by_id.get(document_id, {})
            if document.get("version") != "0.1.0-draft" or document.get("path") != path:
                errors.append(f"spec/registry.json: invalid {document_id} registration")
            if not (ROOT / document.get("path", "")).is_file():
                errors.append(f"spec/registry.json: missing {document_id} source")

        scenario_document = supporting_by_id.get("END-SCEN", {})
        if scenario_document.get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: END-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("CLOSURE-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: CLOSURE-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("EVIDENCE-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: EVIDENCE-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("SESSION-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: SESSION-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("DIA-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: DIA-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("ADP-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: ADP-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("ID-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: ID-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("TEXT-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: TEXT-SCEN must remain a non-normative design corpus")
        if supporting_by_id.get("AUT-SCEN", {}).get("status") != "non-normative-design-corpus":
            errors.append("spec/registry.json: AUT-SCEN must remain a non-normative design corpus")

    terms = registry.get("terms")
    if not isinstance(terms, list) or not terms:
        errors.append("spec/registry.json: terms must be a non-empty list")
    else:
        term_names = [term.get("term") for term in terms]
        if len(term_names) != len(set(term_names)):
            errors.append("spec/registry.json: term names must be unique")
        for required_term in (
            "Noemion", "Endem", "closure", "contract", "evidence",
            "producer", "inspector", "runner", "form", "lint", "compose", "inspect", "run",
            "source", "meaning", "situation", "direction", "criteria", "unresolved", "observation",
            "reach", "maintain", "formed", "resolved", "unavailable", "undetermined", "stopped",
            "allowed", "denied", "pending", "profile", "time", "scope", "coverage", "guard", "signed", "view",
        ):
            if required_term not in term_names:
                errors.append(f"spec/registry.json: missing human term {required_term}")

    identifiers = registry.get("identifiers")
    if not isinstance(identifiers, list) or not identifiers:
        errors.append("spec/registry.json: identifiers must be a non-empty list")
    else:
        identifier_names = [item.get("identifier") for item in identifiers]
        if len(identifier_names) != len(set(identifier_names)):
            errors.append("spec/registry.json: identifier names must be unique")
        for required_identifier in (
            "Noemion", "Endem", "closure", "contract", "evidence",
            *REQUIRED_FACETS, "wire-format", "content-standard", "content-profile", "END-P0", "END-P2", "source-manifest",
            "satisfaction-result", "decision-result", "session-result", "evidence-status",
            "time-scope", "continuity-policy", "time-coverage",
            "relation-polarity", "negative-evidence", "observation-closure",
            "quantifier", "collection-scope", "cardinality-evidence",
            "measurement-construct", "estimand", "measurement-procedure", "threshold-contract",
            "criterion-leaf", "criterion-composition", "decisive-basis", "evaluation-coverage",
            "closure-member", "binding-record", "dependency-relation", "activation-guard", "activation-status",
            "session-subject", "policy-closure", "environment-binding", "capability-envelope",
            "budget-envelope", "observation-plan", "material-drift",
            "evidence-subject", "evidence-scope", "provenance-edge", "evidence-class",
            "validity-assessment", "coverage-assessment", "disclosure-manifest",
            "diagnostic-code", "diagnostic-layer", "diagnostic-location",
            "primary-diagnostic", "recovery-class",
            "adapter-binding", "peer-binding", "invocation-binding", "loss-manifest",
            "external-state", "delivery-evidence", "idempotency-class",
            "exact-content-identity", "identity-domain", "digest-reference",
            "signed-statement", "attestation-envelope", "validity-cutoff", "artifact-relation",
            "text-slot", "source-text-binding", "structural-identifier", "text-transform",
            "comparison-profile", "scalar-range", "hidden-character-inventory",
            "model-text-binding", "display-view",
            "authority-context", "authority-principal", "authorization-scope", "semantic-authorization",
            "authorization-decision", "delegation-chain", "multi-authority-policy",
            "consent-binding", "authorization-validity", "decision-replay-binding",
        ):
            if required_identifier not in identifier_names:
                errors.append(f"spec/registry.json: missing identifier {required_identifier}")
        wire_identifier = next((item for item in identifiers if item.get("identifier") == "wire-format"), None)
        if wire_identifier and wire_identifier.get("decision_status") != "accepted-draft":
            errors.append("spec/registry.json: wire-format must be accepted-draft")
        meaning_identifier = next((item for item in identifiers if item.get("identifier") == "meaning_projection"), None)
        meaning_definition = meaning_identifier.get("definition", "") if meaning_identifier else ""
        for boundary in (
            "确定性规则或范围有限具名权威确认",
            "语义授权不授予动作权限",
        ):
            if boundary not in meaning_definition:
                errors.append(
                    f"spec/registry.json: meaning_projection definition must separate meaning confirmation from action authorization: {boundary}"
                )

    experiments = registry.get("experiments")
    if not isinstance(experiments, list) or len(experiments) != 1:
        errors.append("spec/registry.json: exactly one P0 language experiment is required")
    else:
        experiment = experiments[0]
        expected_experiment = {
            "id": "P0-LANG-001",
            "status": "historical-research-evidence",
            "protocol": "experiments/p0-language/README.md",
            "results": "experiments/p0-language/results.json",
            "decision": "architecture/adr-0012-rust-core-language.html",
            "production_implementation": False,
        }
        for key, value in expected_experiment.items():
            if experiment.get(key) != value:
                errors.append(f"P0-LANG-001 {key} must be {value!r}")
        for path_field in ("protocol", "results", "decision"):
            if not source_path_for_route(experiment.get(path_field, "")).is_file():
                errors.append(f"P0-LANG-001 missing {path_field} file")
        results = load_json(ROOT / experiment.get("results", ""), errors)
        if results:
            if results.get("decision", {}).get("ktisor_structural_core") != "Rust 1.97.0 stable":
                errors.append("P0-LANG-001 must record the bounded Rust core decision")
            if results.get("linux_ci", {}).get("conclusion") != "success":
                errors.append("P0-LANG-001 must retain successful Linux CI evidence")
            if results.get("macos", {}).get("differential_mutation_count") != 144:
                errors.append("P0-LANG-001 must retain the 144-case differential result")
            macos = results.get("macos", {})
            if macos.get("vector_count") != 6 or macos.get("all_vectors_match") is not True:
                errors.append("P0-LANG-001 must retain the 6-vector macOS result")
            if macos.get("differential_mutations_match") is not True or macos.get("c_sanitizers_pass") is not True:
                errors.append("P0-LANG-001 must retain differential and sanitizer success")
            for language, source in (
                ("c", ROOT / "experiments/p0-language/c/validator.c"),
                ("rust", ROOT / "experiments/p0-language/rust/main.rs"),
            ):
                artifact = macos.get("artifacts", {}).get(language, {})
                actual_lines = sum(1 for line in source.read_text().splitlines() if line.strip())
                if artifact.get("source_nonblank_lines") != actual_lines:
                    errors.append(f"P0-LANG-001 {language} source line evidence drifted")
                if artifact.get("repeated_binary_sha256_match") is not True:
                    errors.append(f"P0-LANG-001 {language} repeated build evidence must be true")
            if results.get("linux_ci", {}).get("required_libfuzzer_runs") != 10000:
                errors.append("P0-LANG-001 Linux evidence must require 10000 libFuzzer runs")

    spec_clause_ids = SPEC_HEADING.findall(spec_text)
    if not spec_clause_ids:
        errors.append("spec sources: no normative clause headings found")
    if len(spec_clause_ids) != len(set(spec_clause_ids)):
        errors.append("spec sources: clause headings must be unique")

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
    if not isinstance(threats, list) or len(threats) != 99:
        errors.append("spec/registry.json: exactly 99 object and cross-cutting threats are required")
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
            if not re.fullmatch(r"THR-(?:END|CLOSURE|SESSION|EVIDENCE|DIA|ADP|ID|TEXT|AUT)-[0-9]{3}", threat_id):
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
        if clause_id.startswith("END-FMT-"):
            expected_implementation = "vector-checker-only"
        elif clause_id.startswith("END-SRCM-"):
            expected_implementation = "vector-checker-only"
        elif clause_id.startswith(("DIA-", "ADP-", "ID-", "TEXT-", "AUT-")):
            expected_implementation = "vector-checker-only"
        else:
            expected_implementation = "unimplemented"
        if clause.get("implementation_status") != expected_implementation:
            errors.append(
                f"{clause_id}: implementation must be {expected_implementation}"
            )
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
                ref_path = source_path_for_route(ref)
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
        if vector.get("vector_format") != "end-core.semantic-vector.v2":
            errors.append(f"{label}: invalid vector_format")
        vector_id = vector.get("id")
        if not isinstance(vector_id, str) or not VECTOR_ID.fullmatch(vector_id):
            errors.append(f"{label}: invalid vector id {vector_id!r}")
        else:
            vector_ids.append(vector_id)
        if vector.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
            errors.append(f"{label}: must pin END-CORE 0.1.0-draft")
        context = vector.get("context")
        if not isinstance(context, dict) or not isinstance(context.get("external_preconditions"), list):
            errors.append(f"{label}: v2 vectors must declare external_preconditions")

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
        "END-CORE-001", "END-SRC-001", "END-SIT-001", "END-UNRESOLVED-001", "END-AUT-001",
    ):
        if required_reject_clause not in rejected_clause_ids:
            errors.append(f"missing direct rejection vector for {required_reject_clause}")


def validate_public_boundary(errors):
    config_text = (ROOT / "_config.yml").read_text()
    workflow_text = (ROOT / ".github" / "workflows" / "pages.yml").read_text()
    core_text = CORE_SPEC_PATH.read_text()
    evidence_text = EVIDENCE_SPEC_PATH.read_text()
    for token in (
        "同一封闭输入产生同一规范结果",
        "实际进入 `source_expression` 的解码文本及其文本槽",
        "严格解码 Profile",
        "显式变换结果与损失",
        "MUST NOT` 通过未声明的 Unicode 规范化",
    ):
        if token not in core_text:
            errors.append(f"END-DET-001 missing exact deterministic-input boundary: {token}")
    if "相同的规范化来源" in core_text:
        errors.append("END-DET-001 must not rely on an undefined normalized-source identity")
    for token in (
        "实际执行的解析与变换",
        "算法或方法版本及其信息损失",
        "未定义的“规范化”",
    ):
        if token not in evidence_text:
            errors.append(f"EVIDENCE-OBS-001 missing explicit transformation boundary: {token}")
    if "python3 tests/semantic_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute semantic vectors, not only register them")
    if "python3 tests/result_domain_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute result-domain vectors")
    if "python3 tests/time_scope_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute maintain time and continuity vectors")
    if "python3 tests/negation_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute negation and absence vectors")
    if "python3 tests/quantification_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute quantification and membership vectors")
    if "python3 tests/measurement_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute measurement and threshold vectors")
    if "python3 tests/composition_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute composite situation and criteria vectors")
    if "python3 tests/endem_closure_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute closure and activation vectors")
    if "python3 tests/evidence_entry_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute evidence appraisal vectors")
    if "python3 tests/session_contract_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute contract vectors")
    if "python3 tests/p2_payload_test.py" not in workflow_text:
        errors.append("Pages workflow must execute complete END-P2 payload vectors")
    if "python3 tests/source_manifest_test.py" not in workflow_text:
        errors.append("Pages workflow must execute END-SRCM source manifest vectors")
    if "python3 tests/diagnostic_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute structured diagnostic vectors")
    if "python3 tests/adapter_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute external protocol adapter vectors")
    if "python3 tests/identity_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute exact identity and attestation vectors")
    if "python3 tests/text_identifier_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute text and identifier vectors")
    if "python3 tests/authority_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute authority and authorization vectors")
    for exact_exclusion in ("  - experiments/", "  - vectors/"):
        if exact_exclusion not in config_text:
            errors.append(f"_config.yml: missing exact exclusion {exact_exclusion.strip()!r}")
    if re.search(r"^\s*-\s+spec/?\s*$", config_text, re.MULTILINE):
        errors.append(
            "_config.yml: spec Markdown must be rendered into public HTML, not excluded"
        )
    if re.search(r"^\s*-\s+(?:experiments|vectors)\s*$", config_text, re.MULTILINE):
        errors.append(
            "_config.yml: bare experiments/vectors exclusions can also hide prefix-matching public routes"
        )

    public_contracts = {
        "specifications/index.html": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "END-P2",
            "spec/registry.json",
            "CLOSURE-CORE 0.1.0-draft",
            "SESSION-CORE 0.1.0-draft",
            "EVIDENCE-CORE 0.1.0-draft",
            "DIA-CORE 0.1.0-draft",
            "ADP-CORE 0.1.0-draft",
            "ID-CORE 0.1.0-draft",
            "TEXT-IDENTIFIER-CORE 0.1.0-draft",
            "AUT-CORE 0.1.0-draft",
            "正式条款",
            "机器可读登记",
            "Profile",
            "设计材料",
            "验证资料",
            "实现证据",
            "哪些边界还不能从规范推出",
            "当前没有 producer、inspector、runner",
        ),
        "specifications/endem.html": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "END-P2",
            "用一个健康目标读懂 Endem",
            "现行形成分类怎样阅读",
            "有类型外部陈述",
            "验证政策与截止点",
            "依赖方准入判断",
            "spec/endem-core.html",
            "spec/endem-format.html",
            "spec/endem-scenarios.html",
            "复杂目标从哪个问题进入",
            "五个结果域分别回答什么",
            "ADR-0015",
            "ADR-0016",
            "ADR-0017",
            "ADR-0018",
            "ADR-0019",
            "ADR-0020",
            "时间范围和连续性政策",
            "没有记录能否证明没有发生",
            "“所有”或数量条件怎样判断",
            "一个指标超过阈值是否足够",
            "查询未命中或日志为空只能形成",
            "测量程序违约为",
            "两个 Endem",
            "条款 ID",
            "尚非稳定 ABI",
        ),
        "specifications/index.html": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "机器可读登记",
            "版本化规范源",
            "用一个外部“已完成”状态走完整条查询链",
            "研究资料不能作为现行字段、命令、状态或互操作接口的依据",
            "向量通过也只说明已登记案例与草案一致",
        ),
        "architecture/adr-0012-rust-core-language.html": (
            "Rust 1.97.0",
            "forbid(unsafe_code)",
            "10,000 次 libFuzzer",
            "experiments/p0-language/results.json",
            "必须另写解析结构和错误路径",
            "实现语言继续待定",
            "不是生产实现",
        ),
        "architecture/adr-0013-end-p1-payload.html": (
            "END-P2",
            "profile_id=3",
            "spec/profiles/end-p2.json",
            "RFC 8949",
            "不是稳定 ABI",
        ),
        "architecture/adr-0014-source-manifest.html": (
            "END-SRCM",
            "实验性来源清单",
            "禁止模型直接生成规范对象",
            "正式来源语言",
        ),
        "architecture/adr-0015-result-domains.html": (
            "五个结果域",
            "met / unmet / undetermined / fault",
            "accepted / rejected / deferred",
            "completed / failed / stopped",
            "valid / invalid / revoked",
            "sufficient / insufficient",
            "不新增 END-P2 字段",
            "没有 runner",
        ),
        "architecture/adr-0016-mene-time-model.html": (
            "utc_window",
            "elapsed_window",
            "[start, end)",
            "strict",
            "budgeted",
            "采样",
            "undetermined",
            "fault",
            "RFC 3339",
            "RFC 9557",
            "GNU C Library",
            "GNU Coreutils",
            "W3C OWL-Time",
            "OpenTelemetry Metrics",
            "不增加 END-P2 字段",
            "没有计时器、监控器或求值组件",
        ),
        "architecture/adr-0017-negation-and-absence.html": (
            "同一关系、同一角色",
            "negative",
            "undetermined",
            "fault",
            "封闭观察范围",
            "W3C OWL 2 Primer",
            "W3C SHACL",
            "SPARQL 1.1 NOT EXISTS",
            "GNU grep",
            "OpenTelemetry Logs",
            "不增加 END-P2 字段",
            "没有日志收集器、策略引擎或求值器",
        ),
        "architecture/adr-0018-quantification-and-membership.html": (
            "一个量化目标不是",
            "enumerated",
            "rule-bound",
            "at_least",
            "at_most",
            "exactly",
            "空集合",
            "不同成员",
            "SHACL 1.2",
            "OWL 2",
            "COUNT(DISTINCT",
            "GNU",
            "不表示 producer、runner、求值器或 CLI 已经实现",
        ),
        "architecture/adr-0019-measurement-and-thresholds.html": (
            "测量谓词必须同时固定构念",
            "fixed_population",
            "generalized_population",
            "estimand",
            "arithmetic_mean",
            "quantile",
            "model_estimate",
            "不确定区间",
            "NIST AI 800-2",
            "NIST AI 800-3",
            "OpenTelemetry Metrics",
            "Prometheus",
            "GNU Units",
            "不表示遥测采集器、基准运行器、统计引擎、runner 或求值器已经实现",
        ),
        "architecture/adr-0020-composite-situations-and-criteria.html": (
            "第一阶段只允许用",
            "all_of",
            "any_of",
            "quantifier=every",
            "combiner=all_of",
            "decisive-basis",
            "evaluation-coverage",
            "未求值叶不是",
            "GNU Coreutils test",
            "GNU Bash Lists",
            "SHACL 1.2 Core",
            "不表示 producer、inspector、runner、CLI 或求值器已经实现",
        ),
        "architecture/adr-0021-synem-closure-and-activation.html": (
            "CLOSURE-CORE 0.1.0-draft",
            "active / inactive / unresolved / error",
            "Endem 组合闭包",
            "activation=active",
            "activation=inactive",
            "成员结果保持各自身份",
            "GNU ld",
            "GNU Guix",
            "GNU make",
            "W3C SHACL",
            "MCP 2025-11-25",
            "不表示 producer、inspector、runner、CLI、解析器或运行时已经实现",
        ),
        "architecture/adr-0022-iknem-evidence-and-appraisal.html": (
            "EVIDENCE-CORE 0.1.0-draft",
            "有范围证据记录（evidence）",
            "validity=valid",
            "coverage=sufficient",
            "model-candidate",
            "decision-record",
            "W3C PROV Data Model",
            "RFC 9334 RATS Architecture",
            "SLSA 1.2 Provenance",
            "GNU Guix 的 guix challenge",
            "OpenTelemetry GenAI 语义约定独立仓库",
            "MCP Security Best Practices",
            "不表示采集器、验证器、归并器、决定引擎、inspector 或 runner 已经实现",
        ),
        "architecture/adr-0023-endem-content-standard.html": (
            "END-CORE 0.1.0-draft",
            "END-P2 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "profile-accept",
            "external-prerequisites-not-evaluated",
            "内容能力集（Profile）",
            "END-P2 含来源形成 Profile",
            "GNU strip",
            "ONNX 1.23.0 IR",
            "SPDX 3.0.1",
            "ELF 不是由 IETF RFC 定义",
            "通用内容",
            "内容 Profile",
            "物理容器",
            "容器接受",
            "Profile 接受",
            "内容接受",
            "不新增重复规范 ID",
            "不能证明任何写入器、读取器、CLI 或运行时已经实现",
        ),
        "architecture/adr-0024-dromen-session-contract.html": (
            "权限只属于这一次会话",
            "SESSION-CORE 0.1.0-draft",
            "只读执行契约",
            "MCP 2025-11-25 授权规范",
            "ELF gABI",
            "Linux capabilities",
            "Linux no_new_privs",
            "Landlock",
            "不建立 contract 文件",
            "不表示 runner 已经实现",
        ),
        "architecture/adr-0025-structured-diagnostics.html": (
            "错误消息不能替系统作决定",
            "DIA-CORE 0.1.0-draft",
            "GNU GCC",
            "RFC 9457",
            "MCP 2025-11-25",
            "协议错误",
            "工具执行错误",
            "当前没有诊断生产器",
        ),
        "architecture/adr-0026-external-protocol-adapters.html": (
            "远端完成，不等于本地完成",
            "ADP-CORE 0.1.0-draft",
            "MCP 2025-11-25",
            "2026-07-28",
            "5 月 21 日",
            "尚未成为当前规范",
            "不作为当前符合性基线",
            "A2A 1.0",
            "RFC 9110",
            "GNU BFD",
            "能力交集",
            "当前没有协议 Profile",
        ),
        "architecture/adr-0027-exact-identity-and-attestation.html": (
            "签名有效，不等于制品获准",
            "ID-CORE 0.1.0-draft",
            "RFC 6920",
            "RFC 9052",
            "DSSE",
            "Sigstore Bundle",
            "SLSA 1.2",
            "GNU ld",
            "GNU Guix",
            "当前没有摘要器",
        ),
        "architecture/adr-0028-text-and-identifier-boundaries.html": (
            "显示相同，不等于输入相同",
            "TEXT-IDENTIFIER-CORE 0.1.0-draft",
            "RFC 3629",
            "UAX #15",
            "UAX #31",
            "UAX #9",
            "UTS #39",
            "UTS #55",
            "RFC 8264",
            "GNU libunistring",
            "当前没有 Unicode 处理器",
        ),
        "architecture/adr-0029-authority-and-authorization-decisions.html": (
            "身份已确认，不等于操作已获准",
            "AUT-CORE 0.1.0-draft",
            "grant deny defer",
            "RFC 9396",
            "RFC 8693",
            "RFC 9470",
            "RFC 9700",
            "MCP 2025-11-25",
            "GNU Guix",
            "当前没有权威目录",
        ),
        "architecture/adr-0030-endem-content-and-authorization-companions.html": (
            "内容身份不变，不等于授权仍然有效",
            "END-CON-006",
            "END-AUT-002",
            "END-ID-002",
            "END-FMT-015",
            "in-toto Attestation Framework 1.2",
            "The Update Framework 1.0.35",
            "GNU Guix",
            "MCP 2025-11-25",
            "当前改动只修正规范边界",
        ),
        "architecture/adr-0035-public-actions-and-internal-responsibilities.html": (
            "当前策略",
            "用户任务不是内部职责清单",
            "五项公开职责",
            "form",
            "lint",
            "compose",
            "inspect",
            "run",
            "form / lint / compose / inspect / run",
            "GNU Command-Line Interfaces",
            "Git glossary：porcelain 与 plumbing",
            "MCP 2025-11-25 Tools",
            "A2A 1.0 版本化规范",
            "OpenAI Agents SDK Tools",
            "conformance:",
            "普通动作词已接受",
            "动作名称不等于实现优先级",
            "没有可执行 <code>endem</code>",
        ),
        "architecture/adr-0036-source-bearing-and-stripped-release.html": (
            "当前策略",
            "移除原文，就得到另一份制品",
            "形成版保留原始自然语言",
            "最终发布版移除原文",
            "GNU GDB：Separate Debug Files",
            "GNU strip",
            "GNU objcopy",
            "SLSA 1.2 Provenance",
            "NIST AI 600-1",
            "END-P2",
            "END-PUB-001",
            "source_ref",
            "新身份与新验证",
            "摘要猜测",
            "没有受控伴随资料",
            "删除、重写、保留和外置不是一回事",
            "裁剪只能移除一类输入和披露风险",
            "没有可执行的裁剪命令",
        ),
        "specifications/endem-closure.html": (
            "CLOSURE-CORE 0.1.0-draft",
            "spec/endem-closure-core.html",
            "spec/endem-closure-threat-model.html",
            "spec/endem-closure-scenarios.html",
            "active / inactive / unresolved / error",
            "ADR-0021",
            "不是物理格式",
        ),
        "specifications/evidence-entry.html": (
            "EVIDENCE-CORE 0.1.0-draft",
            "spec/evidence-entry-core.html",
            "spec/evidence-entry-threat-model.html",
            "spec/evidence-entry-scenarios.html",
            "valid / invalid / revoked",
            "sufficient / insufficient",
            "model-candidate",
            "不是记录给自己的标签",
            "没有相应的采集、验证、归并、撤销或决定实现",
        ),
        "specifications/session-contract.html": (
            "SESSION-CORE 0.1.0-draft",
            "spec/session-contract-core.html",
            "spec/session-contract-threat-model.html",
            "spec/session-contract-scenarios.html",
            "SESSION-SUB-001",
            "SESSION-LIF-001",
            "不是文件、进程、模型上下文、凭据包、可恢复会话或最终结果",
            "contract API、平台隔离方式、事件格式和运行后端仍待确定",
            "当前没有 runner、装载器、沙箱、凭据代理、预算器或运行时",
        ),
        "specifications/diagnostics.html": (
            "DIA-CORE 0.1.0-draft",
            "稳定机器码",
            "生产语境",
            "主阻断诊断",
            "不得授予权限",
            "不保存令牌",
            "有限预算",
            "部分可信对象",
            "当前没有诊断生产器",
        ),
        "specifications/adapters.html": (
            "ADP-CORE 0.1.0-draft",
            "ADP-PIN-001",
            "ADP-SEC-001",
            "覆盖版本、身份、权限、副作用和安全威胁",
            "覆盖支持案例、反例与边界条件",
            "覆盖允许包络与确定拒绝",
            "仍保持开放",
        ),
        "specifications/identity.html": (
            "ID-CORE 0.1.0-draft",
            "ID-DOM-001",
            "ID-REL-001",
            "覆盖身份混淆、降级、重放、撤销和信任继承威胁",
            "用支持案例、反例与边界场景检查身份责任",
            "覆盖允许包络与确定拒绝，并绑定对应条款",
            "均保持开放",
        ),
        "specifications/text-and-identifiers.html": (
            "TEXT-IDENTIFIER-CORE 0.1.0-draft",
            "TEXT-SLT-001",
            "TEXT-ENC-001",
            "TEXT-SRC-001",
            "TEXT-IDN-001",
            "TEXT-NRM-001",
            "TEXT-CMP-001",
            "TEXT-RNG-001",
            "TEXT-BID-001",
            "TEXT-HID-001",
            "TEXT-MET-001",
            "TEXT-AIM-001",
            "TEXT-OUT-001",
            "都保持开放",
        ),
        "specifications/authority.html": (
            "AUT-CORE 0.1.0-draft",
            "AUT-CTX-001",
            "AUT-PRN-001",
            "AUT-SCP-001",
            "AUT-SEM-001",
            "AUT-DEC-001",
            "AUT-DEL-001",
            "AUT-MUL-001",
            "AUT-CNS-001",
            "AUT-TIM-001",
            "AUT-RPL-001",
            "AUT-CAP-001",
            "AUT-SEP-001",
            "仍保持开放",
        ),
        "development/implementation-roadmap.html": (
            "当前可以审查术语、规范、案例、威胁和验证设计",
            "也不表示组件已经开始实现",
            "现行设计标识，不是已发布接口",
            "普通英语词已经通过词首、职责和关键字检查",
            "Rust 与 C 的既有研究也只提供未来比较材料",
            "当前没有 Rust 组件、CLI、协议适配器",
            "候选版在正式发布前只作为迁移风险",
            "不进入 Endem 编码、evidence 身份、授权决定或最终接受",
        ),
    }
    for relative_path, tokens in public_contracts.items():
        text = source_path_for_route(relative_path).read_text()
        for token in tokens:
            markdown_token = re.sub(r"<code>(.*?)</code>", r"`\1`", token)
            if token not in text and markdown_token not in text:
                errors.append(f"{relative_path}: missing normative-source boundary {token!r}")


def main():
    errors = []
    registry = load_json(REGISTRY_PATH, errors)
    try:
        spec_text = (
            CORE_SPEC_PATH.read_text() + "\n" + FORMAT_SPEC_PATH.read_text()
            + "\n" + SOURCE_MANIFEST_SPEC_PATH.read_text()
            + "\n" + CLOSURE_SPEC_PATH.read_text()
            + "\n" + SESSION_SPEC_PATH.read_text()
            + "\n" + EVIDENCE_SPEC_PATH.read_text()
            + "\n" + DIAGNOSTIC_SPEC_PATH.read_text()
            + "\n" + ADAPTER_SPEC_PATH.read_text()
            + "\n" + IDENTITY_SPEC_PATH.read_text()
            + "\n" + TEXT_SPEC_PATH.read_text()
            + "\n" + AUTHORITY_SPEC_PATH.read_text()
        )
    except OSError as exc:
        errors.append(f"spec sources: cannot read: {exc}")
        spec_text = ""
    try:
        threat_text = "\n".join(path.read_text() for path in THREAT_PATHS)
    except OSError as exc:
        errors.append(f"threat model sources: cannot read: {exc}")
        threat_text = ""
    try:
        scenario_text = SCENARIO_CORPUS_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-scenarios.md: cannot read: {exc}")
        scenario_text = ""
    try:
        closure_scenario_text = CLOSURE_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-closure-scenarios.md: cannot read: {exc}")
        closure_scenario_text = ""
    try:
        evidence_scenario_text = EVIDENCE_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/evidence-entry-scenarios.md: cannot read: {exc}")
        evidence_scenario_text = ""
    try:
        session_scenario_text = SESSION_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/session-contract-scenarios.md: cannot read: {exc}")
        session_scenario_text = ""
    try:
        diagnostic_scenario_text = DIAGNOSTIC_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/diagnostic-scenarios.md: cannot read: {exc}")
        diagnostic_scenario_text = ""
    try:
        adapter_scenario_text = ADAPTER_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/adapter-scenarios.md: cannot read: {exc}")
        adapter_scenario_text = ""
    try:
        identity_scenario_text = IDENTITY_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/identity-scenarios.md: cannot read: {exc}")
        identity_scenario_text = ""
    try:
        text_scenario_text = TEXT_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/text-identifier-scenarios.md: cannot read: {exc}")
        text_scenario_text = ""
    try:
        authority_scenario_text = AUTHORITY_SCENARIO_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/authority-scenarios.md: cannot read: {exc}")
        authority_scenario_text = ""

    scenario_ids = SCENARIO_HEADING.findall(scenario_text)
    if scenario_ids != [f"SCN-{index:03d}" for index in range(1, 31)]:
        errors.append("spec/endem-scenarios.md: scenario IDs must be unique and ordered SCN-001 through SCN-030")
    for token in (
        "事态由对象结合构成（2.01）",
        "图示形式由结构显示而非自我陈述（2.17–2.172）",
        "禁止事项由否定事态表达",
        "观察不足不同于未满足",
        "求值故障不同于观察不足",
        "两个独立根必须拆分",
        "completed` 不等于 `met` 或 `accepted",
        "failed` 不等于 `unmet",
        "半开区间 `[start,end)`",
        "离散健康采样不能证明连续可用",
        "单调时钟",
        "观测覆盖空洞",
        "否定不创造第二套关系",
        "没有访问日志不等于没有访问",
        "封闭范围才允许从缺席推断",
        "全部生产节点健康需要固定全集",
        "任一区域就绪可以由一个见证确定",
        "至少三个批准按不同主体计数",
        "空集合和成员漂移不能静默决定结果",
        "p95 响应时间需要完整测量契约",
        "固定基准准确率不等于普遍能力",
        "单位可换算不等于可以随意换算",
        "缺样本和统计程序故障必须分开",
        "同一服务终态可以使用复合根",
        "独立报告与部署必须拆成两个 Endem",
        "决定性短路仍要保存覆盖",
        "条件目标暂不进入组合语言",
        "不是可执行测试",
    ):
        if token not in scenario_text:
            errors.append(f"spec/endem-scenarios.md: missing design-review boundary {token!r}")

    closure_scenario_ids = re.findall(r"^### (CLOSURE-SCN-[0-9]{3})\s+—", closure_scenario_text, re.MULTILINE)
    if closure_scenario_ids != [f"CLOSURE-SCN-{index:03d}" for index in range(1, 11)]:
        errors.append("spec/endem-closure-scenarios.md: scenario IDs must be unique and ordered CLOSURE-SCN-001 through CLOSURE-SCN-010")
    for token in ("完整闭包", "搜索顺序", "权限取交集", "成员完成不等于闭包接受", "未激活不是未知满足", "不是清单语法"):
        if token not in closure_scenario_text:
            errors.append(f"spec/endem-closure-scenarios.md: missing design-review boundary {token!r}")

    evidence_scenario_ids = re.findall(r"^### (EVIDENCE-SCN-[0-9]{3})\s+—", evidence_scenario_text, re.MULTILINE)
    if evidence_scenario_ids != [f"EVIDENCE-SCN-{index:03d}" for index in range(1, 15)]:
        errors.append("spec/evidence-entry-scenarios.md: scenario IDs must be unique and ordered EVIDENCE-SCN-001 through EVIDENCE-SCN-014")
    for token in ("固定测试集不能代表未知总体", "循环自证", "模型解释保持候选", "有效签名遇到撤销", "重复日志仍不能补齐覆盖", "不得保存实时凭据"):
        if token not in evidence_scenario_text:
            errors.append(f"spec/evidence-entry-scenarios.md: missing design-review boundary {token!r}")

    session_scenario_ids = re.findall(r"^### (SESSION-SCN-[0-9]{3})\s+—", session_scenario_text, re.MULTILINE)
    if session_scenario_ids != [f"SESSION-SCN-{index:03d}" for index in range(1, 16)]:
        errors.append("spec/session-contract-scenarios.md: scenario IDs must be unique and ordered SESSION-SCN-001 through SESSION-SCN-015")
    for token in ("显示名不能选择会话主体", "最新政策不是稳定输入", "能力取交集", "Step-up 授权不能修改运行契约", "委托任务共享外层预算", "诊断快照不能恢复权限"):
        if token not in session_scenario_text:
            errors.append(f"spec/session-contract-scenarios.md: missing design-review boundary {token!r}")

    diagnostic_scenario_ids = re.findall(r"^### (DIA-SCN-[0-9]{3})\s+—", diagnostic_scenario_text, re.MULTILINE)
    if diagnostic_scenario_ids != [f"DIA-SCN-{index:03d}" for index in range(1, 16)]:
        errors.append("spec/diagnostic-scenarios.md: scenario IDs must be unique and ordered DIA-SCN-001 through DIA-SCN-015")
    for token in ("中文与英文消息共享同一机器码", "MCP 协议错误与工具执行错误分开", "结构失败先于尚未执行的语义失败", "权限拒绝不能触发自动提权", "诊断上限保留主错误", "报错后不能返回部分可信对象"):
        if token not in diagnostic_scenario_text:
            errors.append(f"spec/diagnostic-scenarios.md: missing design-review boundary {token!r}")

    adapter_scenario_ids = re.findall(r"^### (ADP-SCN-[0-9]{3})\s+—", adapter_scenario_text, re.MULTILINE)
    if adapter_scenario_ids != [f"ADP-SCN-{index:03d}" for index in range(1, 19)]:
        errors.append("spec/adapter-scenarios.md: scenario IDs must be unique and ordered ADP-SCN-001 through ADP-SCN-018")
    for token in ("稳定版与候选版不能共用绑定", "Agent Card 只是自我描述", "外部 completed 不等于 accepted", "取消或断流不证明副作用回滚", "非幂等调用断连后不自动重试", "令牌透传与 SSRF 默认拒绝"):
        if token not in adapter_scenario_text:
            errors.append(f"spec/adapter-scenarios.md: missing design-review boundary {token!r}")

    identity_scenario_ids = re.findall(r"^### (ID-SCN-[0-9]{3})\s+—", identity_scenario_text, re.MULTILINE)
    if identity_scenario_ids != [f"ID-SCN-{index:03d}" for index in range(1, 19)]:
        errors.append("spec/identity-scenarios.md: scenario IDs must be unique and ordered ID-SCN-001 through ID-SCN-018")
    for token in ("同一摘要文本位于不同对象域", "短摘要只帮助人阅读", "发布签名覆盖用途和受众", "撤销改变评估不改变历史字节", "两条独立路径逐字节复现", "压缩与迁移不能继承信任"):
        if token not in identity_scenario_text:
            errors.append(f"spec/identity-scenarios.md: missing design-review boundary {token!r}")

    text_scenario_ids = re.findall(r"^### (TEXT-SCN-[0-9]{3})\s+—", text_scenario_text, re.MULTILINE)
    if text_scenario_ids != [f"TEXT-SCN-{index:03d}" for index in range(1, 19)]:
        errors.append("spec/text-identifier-scenarios.md: scenario IDs must be unique and ordered TEXT-SCN-001 through TEXT-SCN-018")
    for token in ("同一字符串位于不同文本槽", "解码必须原子失败", "不等于保存来源清单的原始字节", "当前 ASCII 语法直接拒绝", "不得盲目做 NFKC", "END-P2 范围按标量计数", "安全审查视图显示控制符名称和位置", "模型输入身份、预处理链、隐藏字符清单和显示视图必须共同记录"):
        if token not in text_scenario_text:
            errors.append(f"spec/text-identifier-scenarios.md: missing design-review boundary {token!r}")

    authority_scenario_ids = re.findall(r"^### (AUT-SCN-[0-9]{3})\s+—", authority_scenario_text, re.MULTILINE)
    if authority_scenario_ids != [f"AUT-SCN-{index:03d}" for index in range(1, 19)]:
        errors.append("spec/authority-scenarios.md: scenario IDs must be unique and ordered AUT-SCN-001 through AUT-SCN-018")
    for token in ("不能让 `latest` 静默改写", "已通过高强度认证", "模型以 0.97 置信度", "每一级范围", "重复签名不能满足", "显示与机器对象不一致", "一次批准不能用于另一个对象", "任何一层都不能洗白"):
        if token not in authority_scenario_text:
            errors.append(f"spec/authority-scenarios.md: missing design-review boundary {token!r}")

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
        "PASS: END-CORE, END-FMT, END-SRCM, CLOSURE-CORE, SESSION-CORE, EVIDENCE-CORE, DIA-CORE, ADP-CORE, ID-CORE, TEXT-IDENTIFIER-CORE and AUT-CORE 0.1.0-draft have unique clauses, explicit "
        "maturity, traceable evidence, 99 registered threats, executed semantic "
        "vectors, 30 natural-language design scenarios, 12 result-domain vectors, "
        "12 maintain time and continuity vectors, 12 negation and absence vectors, "
        "12 quantification and membership vectors, "
        "12 measurement and threshold vectors, "
        "12 composite situation and criteria vectors, "
        "12 closure and activation vectors, "
        "20 contract vectors, "
        "18 evidence appraisal vectors, "
        "20 structured diagnostic vectors, "
        "24 external protocol adapter vectors, "
        "24 exact identity and attestation vectors, "
        "24 text and identifier vectors, "
        "24 authority and authorization vectors, "
        "END-P2 payload/source vectors, "
        "and P0-LANG-001 historical language evidence"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
