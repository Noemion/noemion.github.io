from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "result-domains" / "cases.json"
CASE_ID = re.compile(r"^RV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
SATISFACTION = {"met", "unmet", "agno", "fault", None}
SATISFACTION_SOURCE = {"krin", "session", "external-task", "none"}
SESSION = {"completed", "failed", "interrupted"}
VALIDITY = {"valid", "invalid", "revoked"}
COVERAGE = {"sufficient", "insufficient"}
AUTHORITY = {"authorized", "unavailable"}
AUTHORITY_ACTION = {"accept", "reject", "reject-inconclusive", "defer"}
DECISION = {"accepted", "rejected", "deferred"}
CLAUSES = {"END-KRN-002", "END-DEC-001", "END-STA-002"}


def proposal_violation(case):
    satisfaction = case["satisfaction"]
    source = case["satisfaction_source"]
    decision = case["proposed_decision"]
    action = case["authority_action"]

    if satisfaction is not None and source != "krin":
        return "END-STA-002"
    if satisfaction is None and source != "none":
        return "END-STA-002"

    if decision == "accepted":
        if satisfaction is None:
            return "END-STA-002"
        if satisfaction != "met":
            return "END-KRN-002"
        if (
            case["tekmor_validity"] != "valid"
            or case["coverage"] != "sufficient"
            or case["authority"] != "authorized"
            or action != "accept"
        ):
            return "END-DEC-001"
        return None

    if decision == "rejected":
        if case["authority"] != "authorized":
            return "END-DEC-001"
        if action == "reject" and satisfaction == "unmet":
            return None
        if action == "reject-inconclusive" and satisfaction in {"agno", "fault"}:
            return None
        return "END-DEC-001"

    if action != "defer":
        return "END-DEC-001"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read result-domain vectors: {exc}")
        return 1

    if document.get("vector_format") != "end-core.result-domain-vector.v1":
        errors.append("result-domain vectors must use end-core.result-domain-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("result-domain vectors must pin END-CORE 0.1.0-draft")
    if "not Praxor or decision-engine implementation data" not in document.get("description", ""):
        errors.append("result-domain vectors must state their non-implementation boundary")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("result-domain vectors require exactly 12 design cases")
        cases = []

    seen_ids = set()
    counts = {"accept": 0, "reject": 0}
    rejected_clauses = set()
    for index, case in enumerate(cases):
        label = f"case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or CASE_ID.fullmatch(case_id) is None:
            errors.append(f"{label}: invalid id {case_id!r}")
        elif case_id in seen_ids:
            errors.append(f"{label}: duplicate id {case_id}")
        else:
            seen_ids.add(case_id)

        for field, allowed in (
            ("satisfaction", SATISFACTION),
            ("satisfaction_source", SATISFACTION_SOURCE),
            ("session", SESSION),
            ("tekmor_validity", VALIDITY),
            ("coverage", COVERAGE),
            ("authority", AUTHORITY),
            ("authority_action", AUTHORITY_ACTION),
            ("proposed_decision", DECISION),
        ):
            if case.get(field) not in allowed:
                errors.append(f"{case_id or label}: invalid {field} {case.get(field)!r}")

        expect = case.get("expect")
        if not isinstance(expect, dict) or expect.get("result") not in counts:
            errors.append(f"{case_id or label}: invalid expectation")
            continue
        if expect.get("clause") not in CLAUSES:
            errors.append(f"{case_id or label}: invalid clause {expect.get('clause')!r}")
            continue

        violation = proposal_violation(case)
        actual_result = "reject" if violation else "accept"
        counts[actual_result] += 1
        if violation:
            rejected_clauses.add(violation)
        if actual_result != expect["result"]:
            errors.append(
                f"{case_id}: expected {expect['result']}, evaluated {actual_result}"
            )
        if actual_result == "reject" and violation != expect["clause"]:
            errors.append(
                f"{case_id}: expected clause {expect['clause']}, evaluated {violation}"
            )

    if counts != {"accept": 6, "reject": 6}:
        errors.append(f"result-domain vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(
            f"result-domain reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}"
        )

    if errors:
        print("\n".join(errors))
        return 1
    print(
        "PASS: executed 12 result-domain vectors "
        "(6 accepted proposals, 6 deterministic rejects across 3 clauses)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
