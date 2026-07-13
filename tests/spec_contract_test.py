from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CORE_SPEC_PATH = ROOT / "spec" / "endem-core.md"
FORMAT_SPEC_PATH = ROOT / "spec" / "endem-format.md"
SOURCE_MANIFEST_SPEC_PATH = ROOT / "spec" / "endem-source-manifest.md"
THREAT_PATH = ROOT / "spec" / "endem-threat-model.md"
ERROR_CATALOG_PATH = ROOT / "spec" / "endem-errors.md"
SCENARIO_CORPUS_PATH = ROOT / "spec" / "endem-scenarios.md"
PROFILE_PATH = ROOT / "spec" / "profiles" / "end-p0.json"
VECTOR_ROOT = ROOT / "vectors" / "semantic"
SCHEMA_PATH = ROOT / "vectors" / "vector.schema.json"

CLAUSE_ID = re.compile(r"^END-[A-Z]+-[0-9]{3}$")
VECTOR_ID = re.compile(r"^SV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
SPEC_HEADING = re.compile(r"^### (END-[A-Z]+-[0-9]{3})\s+—", re.MULTILINE)
THREAT_HEADING = re.compile(r"^### (THR-END-[0-9]{3})\s+—", re.MULTILINE)
SCENARIO_HEADING = re.compile(r"^### (SCN-[0-9]{3})\s+—", re.MULTILINE)
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
    if not isinstance(documents, list) or len(documents) != 3:
        errors.append("spec/registry.json: END-CORE, END-FMT and END-SRCM documents are required")
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
        }
        if set(documents_by_id) != set(expected_documents):
            errors.append("spec/registry.json: document IDs must be END-CORE, END-FMT and END-SRCM")
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
    if not isinstance(supporting_documents, list) or len(supporting_documents) != 5:
        errors.append("spec/registry.json: threat, error catalog, scenario corpus, P0 and P1 Profile documents are required")
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
            "END-ERRCAT": "spec/endem-errors.md",
            "END-SCEN": "spec/endem-scenarios.md",
            "END-P0": "spec/profiles/end-p0.json",
            "END-P1": "spec/profiles/end-p1.json",
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

    terms = registry.get("terms")
    if not isinstance(terms, list) or not terms:
        errors.append("spec/registry.json: terms must be a non-empty list")
    else:
        term_names = [term.get("term") for term in terms]
        if len(term_names) != len(set(term_names)):
            errors.append("spec/registry.json: term names must be unique")
        for required_term in (
            "Noemion", "Endem", "Synem", "Dromen", "Tekmor",
            *REQUIRED_FACETS, "wire-format", "END-P0", "END-P1", "source-manifest",
            "satisfaction-result", "decision-result", "session-result", "evidence-status",
            "time-scope", "continuity-policy", "time-coverage",
            "relation-polarity", "negative-evidence", "observation-closure",
            "quantifier", "collection-scope", "cardinality-evidence",
            "measurement-construct", "estimand", "measurement-procedure", "threshold-contract",
            "criterion-leaf", "criterion-composition", "decisive-basis", "evaluation-coverage",
        ):
            if required_term not in term_names:
                errors.append(f"spec/registry.json: missing term {required_term}")
        wire_term = next((term for term in terms if term.get("term") == "wire-format"), None)
        if wire_term and wire_term.get("decision_status") != "accepted-draft":
            errors.append("spec/registry.json: wire-format must be accepted-draft")

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
            if not (ROOT / experiment.get(path_field, "")).is_file():
                errors.append(f"P0-LANG-001 missing {path_field} file")
        results = load_json(ROOT / experiment.get("results", ""), errors)
        if results:
            if results.get("decision", {}).get("poiet_structural_core") != "Rust 1.97.0 stable":
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
    if not isinstance(threats, list) or len(threats) != 15:
        errors.append("spec/registry.json: exactly 15 registered Endem threats are required")
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
        if clause_id.startswith("END-FMT-"):
            expected_implementation = "vector-checker-only"
        elif clause_id.startswith("END-SRCM-"):
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
        "END-CORE-001", "END-SRC-001", "END-SIT-001", "END-APR-001", "END-AUT-001",
    ):
        if required_reject_clause not in rejected_clause_ids:
            errors.append(f"missing direct rejection vector for {required_reject_clause}")


def validate_public_boundary(errors):
    config_text = (ROOT / "_config.yml").read_text()
    workflow_text = (ROOT / ".github" / "workflows" / "pages.yml").read_text()
    if "python3 tests/semantic_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute semantic vectors, not only register them")
    if "python3 tests/result_domain_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute result-domain vectors")
    if "python3 tests/mene_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute mene time and continuity vectors")
    if "python3 tests/negation_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute negation and absence vectors")
    if "python3 tests/quantification_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute quantification and membership vectors")
    if "python3 tests/measurement_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute measurement and threshold vectors")
    if "python3 tests/composition_vector_test.py" not in workflow_text:
        errors.append("Pages workflow must execute composite situation and criteria vectors")
    if "python3 tests/p1_payload_test.py" not in workflow_text:
        errors.append("Pages workflow must execute complete END-P1 payload vectors")
    if "python3 tests/source_manifest_test.py" not in workflow_text:
        errors.append("Pages workflow must execute END-SRCM source manifest vectors")
    for exact_exclusion in ("  - experiments/", "  - spec/", "  - vectors/"):
        if exact_exclusion not in config_text:
            errors.append(f"_config.yml: missing exact exclusion {exact_exclusion.strip()!r}")
    if re.search(r"^\s*-\s+(?:experiments|spec|vectors)\s*$", config_text, re.MULTILINE):
        errors.append(
            "_config.yml: bare spec/vectors exclusions can also hide prefix-matching public routes"
        )

    public_contracts = {
        "specifications/index.html": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "END-P1",
            "spec/endem-core.md",
            "spec/endem-format.md",
            "spec/profiles/end-p1.json",
            "spec/registry.json",
            "vectors/semantic",
            "vectors/result-domains",
            "vectors/mene",
            "vectors/negation",
            "vectors/quantification",
            "vectors/measurement",
            "vectors/composition",
            "vectors/wire",
            "spec/endem-threat-model.md",
            "spec/endem-scenarios.md",
            "非规范设计审查材料",
            "不是 .endem 物理格式",
        ),
        "specifications/endem.html": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "END-P1",
            "spec/endem-core.md",
            "spec/endem-format.md",
            "spec/endem-scenarios.md",
            "自然语言场景怎样检验六个语义面",
            "五个结果域分别回答什么",
            "ADR-0015",
            "ADR-0016",
            "ADR-0017",
            "ADR-0018",
            "ADR-0019",
            "ADR-0020",
            "ADR-0019",
            "时间范围和连续性政策",
            "否定与缺席怎样判断",
            "量化目标怎样固定成员范围",
            "测量目标怎样固定口径和阈值",
            "观察不足是",
            "求值过程失败为",
            "两个 Endem",
            "条款 ID",
            "尚非稳定 ABI",
        ),
        "docs/specifications-reference.md": (
            "END-CORE 0.1.0-draft",
            "END-FMT 0.1.0-draft",
            "spec/endem-core.md",
            "spec/endem-format.md",
            "机器可读登记",
            "spec/endem-threat-model.md",
            "spec/endem-scenarios.md",
            "不属于上述规范义务",
            "ADR-0015",
            "ADR-0016",
            "ADR-0017",
            "ADR-0018",
            "ADR-0019",
        ),
        "architecture/adr-0012-rust-core-language.html": (
            "Rust 1.97.0",
            "forbid(unsafe_code)",
            "10,000 次 libFuzzer",
            "experiments/p0-language/results.json",
            "Theor 必须另写解析结构和错误路径",
            "不是生产实现",
        ),
        "architecture/adr-0013-end-p1-payload.html": (
            "END-P1",
            "profile_id=2",
            "spec/profiles/end-p1.json",
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
            "met / unmet / agno / fault",
            "accepted / rejected / deferred",
            "completed / failed / interrupted",
            "valid / invalid / revoked",
            "sufficient / insufficient",
            "不新增 END-P1 字段",
            "没有 Praxor",
        ),
        "architecture/adr-0016-mene-time-model.html": (
            "fixed",
            "elapsed",
            "[start, end)",
            "strict",
            "budgeted",
            "采样",
            "agno",
            "fault",
            "RFC 3339",
            "RFC 9557",
            "GNU C Library",
            "GNU Coreutils",
            "W3C OWL-Time",
            "OpenTelemetry Metrics",
            "不增加 END-P1 字段",
            "没有计时器、监控器或求值组件",
        ),
        "architecture/adr-0017-negation-and-absence.html": (
            "同一关系、同一角色",
            "negative",
            "agno",
            "fault",
            "封闭观察范围",
            "W3C OWL 2 Primer",
            "W3C SHACL",
            "SPARQL 1.1 NOT EXISTS",
            "GNU grep",
            "OpenTelemetry Logs",
            "不增加 END-P1 字段",
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
            "不表示 Poiet、Praxor、求值器或 CLI 已经实现",
        ),
        "architecture/adr-0019-measurement-and-thresholds.html": (
            "测量谓词必须同时固定构念",
            "fixed",
            "generalized",
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
            "不表示遥测采集器、基准运行器、统计引擎、Praxor 或求值器已经实现",
        ),
        "architecture/adr-0020-composite-situations-and-criteria.html": (
            "第一阶段只允许用",
            "all_of",
            "any_of",
            "decisive-basis",
            "evaluation-coverage",
            "未求值叶不是",
            "GNU Coreutils test",
            "GNU Bash Lists",
            "SHACL 1.2 Core",
            "不表示 Poiet、Theor、Praxor、CLI 或求值器已经实现",
        ),
        "development/implementation-roadmap.html": (
            "Rust 1.97.0",
            "C/Rust 双原型",
            "P1-W1 安全核心",
            "尚未开始",
            "等待用户明确开启代码开发阶段",
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
        spec_text = (
            CORE_SPEC_PATH.read_text() + "\n" + FORMAT_SPEC_PATH.read_text()
            + "\n" + SOURCE_MANIFEST_SPEC_PATH.read_text()
        )
    except OSError as exc:
        errors.append(f"spec sources: cannot read: {exc}")
        spec_text = ""
    try:
        threat_text = THREAT_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-threat-model.md: cannot read: {exc}")
        threat_text = ""
    try:
        scenario_text = SCENARIO_CORPUS_PATH.read_text()
    except OSError as exc:
        errors.append(f"spec/endem-scenarios.md: cannot read: {exc}")
        scenario_text = ""

    scenario_ids = SCENARIO_HEADING.findall(scenario_text)
    if scenario_ids != [f"SCN-{index:03d}" for index in range(1, 28)]:
        errors.append("spec/endem-scenarios.md: scenario IDs must be unique and ordered SCN-001 through SCN-027")
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
        "PASS: END-CORE, END-FMT and END-SRCM 0.1.0-draft have unique clauses, explicit "
        "maturity, traceable evidence, 15 registered threats, executed semantic "
        "vectors, 27 natural-language design scenarios, 12 result-domain vectors, "
        "12 mene time and continuity vectors, 12 negation and absence vectors, "
        "12 quantification and membership vectors, "
        "12 measurement and threshold vectors, "
        "12 composite situation and criteria vectors, "
        "END-P1 payload/source vectors, "
        "and P0-LANG-001 historical language evidence"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
