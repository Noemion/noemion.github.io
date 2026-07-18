from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "session-contract" / "cases.json"
CASE_ID = re.compile(r"^SESSION-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "SESSION-SUB-001", "SESSION-POL-001", "SESSION-ENV-001", "SESSION-CAP-001",
    "SESSION-SEC-001", "SESSION-BUD-001", "SESSION-ACT-001", "SESSION-OBS-001",
    "SESSION-IMM-001", "SESSION-LIF-001",
}


def proposal_violation(case):
    proposal = case.get("proposal")
    if not isinstance(proposal, dict):
        return "SESSION-SUB-001"
    subject = proposal.get("subject")
    if (
        not isinstance(subject, dict)
        or not subject.get("id")
        or subject.get("kind") not in {"endem", "endem_closure"}
        or subject.get("content_state") != "resolved"
        or subject.get("revalidated") is not True
        or not subject.get("profile")
        or subject.get("mutable_selector") is not False
    ):
        return "SESSION-SUB-001"
    statement_check = subject.get("statement_check")
    if (
        not isinstance(statement_check, dict)
        or not isinstance(statement_check.get("ids"), list)
        or not statement_check.get("ids")
        or not statement_check.get("policy")
        or not statement_check.get("cutoff")
        or statement_check.get("valid") is not True
        or statement_check.get("revoked") is not False
        or statement_check.get("applicable") is not True
    ):
        return "SESSION-SUB-001"
    policy = proposal.get("policy")
    if (
        not isinstance(policy, dict)
        or not isinstance(policy.get("ids"), list)
        or not policy.get("ids")
        or policy.get("closed") is not True
        or not policy.get("authority")
        or not policy.get("cutoff")
        or not policy.get("expiry")
        or policy.get("unresolved_in_scope") is not False
    ):
        return "SESSION-POL-001"
    environment = proposal.get("environment")
    if (
        not isinstance(environment, dict)
        or not isinstance(environment.get("bindings"), list)
        or not environment.get("bindings")
        or environment.get("observed") is not True
        or environment.get("declared_only") is not False
        or environment.get("drift") is not False
    ):
        return "SESSION-ENV-001"
    capability = proposal.get("capability")
    if (
        not isinstance(capability, dict)
        or capability.get("intersection") is not True
        or capability.get("required_available") is not True
        or capability.get("ambient") is not False
        or capability.get("union") is not False
        or capability.get("step_up_new_session") is not True
    ):
        return "SESSION-CAP-001"
    secrets = proposal.get("secrets")
    if (
        not isinstance(secrets, dict)
        or secrets.get("live_material") is not False
        or secrets.get("handles_external") is not True
        or secrets.get("context_bound") is not True
    ):
        return "SESSION-SEC-001"
    budgets = proposal.get("budgets")
    if (
        not isinstance(budgets, dict)
        or budgets.get("finite") is not True
        or budgets.get("typed") is not True
        or budgets.get("children_subset") is not True
        or budgets.get("cancellation_bound") is not True
    ):
        return "SESSION-BUD-001"
    activation = proposal.get("activation")
    if (
        not isinstance(activation, dict)
        or activation.get("fixed_closure") is not True
        or activation.get("adds_members") is not False
        or activation.get("status_domain_separate") is not True
        or activation.get("grants_capability") is not False
    ):
        return "SESSION-ACT-001"
    observation = proposal.get("observation")
    if (
        not isinstance(observation, dict)
        or observation.get("responsibilities_complete") is not True
        or observation.get("result_domains_separate") is not True
        or observation.get("external_success_promotes") is not False
    ):
        return "SESSION-OBS-001"
    immutability = proposal.get("immutability")
    if (
        not isinstance(immutability, dict)
        or immutability.get("sealed") is not True
        or immutability.get("mutable") is not False
        or immutability.get("drift_action") != "invalidate"
        or immutability.get("append_event") is not True
    ):
        return "SESSION-IMM-001"
    lifecycle = proposal.get("lifecycle")
    if (
        not isinstance(lifecycle, dict)
        or lifecycle.get("session_count") != 1
        or lifecycle.get("persistent") is not False
        or lifecycle.get("transferable") is not False
        or lifecycle.get("resumable") is not False
        or lifecycle.get("disposal") is not True
    ):
        return "SESSION-LIF-001"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read session contract vectors: {exc}")
        return 1
    if document.get("vector_format") != "session-core.vector.v1":
        errors.append("session contract vectors must use session-core.vector.v1")
    if document.get("spec") != {"id": "SESSION-CORE", "version": "0.1.0-draft"}:
        errors.append("session contract vectors must pin SESSION-CORE 0.1.0-draft")
    if "not a loader, sandbox, capability broker, credential store, runtime, event system, or component implementation" not in document.get("description", ""):
        errors.append("session contract vectors must state their non-implementation boundary")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 20:
        errors.append("session contract vectors require exactly 20 proposal cases")
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
    if counts != {"accept": 10, "reject": 10}:
        errors.append(f"session contract vectors require 10 accepts and 10 rejects, got {counts}")
    if rejected != CLAUSES:
        errors.append(f"session contract reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 20 session contract vectors (10 accepted contracts, 10 deterministic rejects across 10 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
