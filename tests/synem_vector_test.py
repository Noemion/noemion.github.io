from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "synem" / "cases.json"
CASE_ID = re.compile(r"^YN-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {"SYN-CLS-001", "SYN-RES-001", "SYN-GRF-001", "SYN-AUT-001", "SYN-STA-001", "SYN-ACT-001"}


def proposal_violation(case):
    proposal = case.get("proposal")
    if not isinstance(proposal, dict):
        return "SYN-CLS-001"
    members = proposal.get("members")
    if not isinstance(members, list) or len(set(members)) < 2 or len(members) != len(set(members)):
        return "SYN-CLS-001"
    required = proposal.get("required")
    if not isinstance(required, list) or any(not isinstance(edge, list) or len(edge) != 2 for edge in required):
        return "SYN-CLS-001"
    member_set = set(members)
    if any(edge[0] not in member_set or edge[1] not in member_set for edge in required):
        return "SYN-CLS-001"
    if proposal.get("bindings") != "exact" or proposal.get("ambient") is not False or proposal.get("order_independent", True) is not True:
        return "SYN-RES-001"
    if proposal.get("cycle") is not False or proposal.get("optional_missing") not in {None, "display-only"}:
        return "SYN-GRF-001"
    if proposal.get("permission") != "intersection":
        return "SYN-AUT-001"
    if proposal.get("aggregate_result") is not False:
        return "SYN-STA-001"
    activation = proposal.get("activation")
    if activation is not None:
        allowed_status = {"active", "inactive", "unresolved", "error"}
        if not isinstance(activation, dict) or activation.get("phase") != "session" or activation.get("fixed_member") is not True or activation.get("domain") not in {"satisfaction-result", "decision-result", "session-result", "evidence-status"} or not activation.get("basis") or activation.get("status") not in allowed_status or activation.get("recheck") is not True or activation.get("grants_permission") is not False or "mapped_satisfaction" in activation:
            return "SYN-ACT-001"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read Synem vectors: {exc}")
        return 1
    if document.get("vector_format") != "noemion.synem-vector-v1":
        errors.append("Synem vectors must use noemion.synem-vector-v1")
    if document.get("spec") != {"id": "SYN-CORE", "version": "0.1.0-draft"}:
        errors.append("Synem vectors must pin SYN-CORE 0.1.0-draft")
    if "not a resolver, parser, Praxor, evaluator, runtime, or component implementation" not in document.get("description", ""):
        errors.append("Synem vectors must state their non-implementation boundary")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("Synem vectors require exactly 12 proposal cases")
        cases = []
    seen = set()
    counts = {"accept": 0, "reject": 0}
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
        violation = proposal_violation(case)
        actual = "reject" if violation else "accept"
        counts[actual] += 1
        if violation:
            rejected.add(violation)
        if actual != expect["result"] or (violation and violation != expect["clause"]):
            errors.append(f"{case_id}: expected {expect}, evaluated {actual}/{violation}")
    if counts != {"accept": 6, "reject": 6}:
        errors.append(f"Synem vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected != CLAUSES:
        errors.append(f"Synem reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 12 Synem vectors (6 accepted classifications, 6 deterministic rejects across 6 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
