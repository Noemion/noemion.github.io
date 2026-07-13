from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "quantification" / "cases.json"
CASE_ID = re.compile(r"^QV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
RESULTS = {"met", "unmet", "agno", "fault"}
QUANTIFIERS = {"all", "some", "at_least", "at_most", "exactly"}
CLAUSES = {"END-QNT-001", "END-QNT-002", "END-QNT-003"}


def nonempty_text(value):
    return isinstance(value, str) and bool(value)


def validate_target(target):
    if not isinstance(target, dict):
        return "END-QNT-001"
    if not nonempty_text(target.get("relation")) or not nonempty_text(target.get("bound_role")):
        return "END-QNT-001"
    collection = target.get("collection")
    if not isinstance(collection, dict):
        return "END-QNT-001"
    for field in ("id", "authority", "cutoff", "identity"):
        if not nonempty_text(collection.get(field)):
            return "END-QNT-001"
    if collection.get("empty") not in {"allow", "reject"}:
        return "END-QNT-002"
    mode = collection.get("mode")
    if mode == "enumerated":
        members = collection.get("members")
        if not isinstance(members, list) or not all(nonempty_text(item) for item in members):
            return "END-QNT-001"
        if len(members) != len(set(members)):
            return "END-QNT-001"
        if not members and collection["empty"] != "allow":
            return "END-QNT-002"
    elif mode == "rule-bound":
        if not nonempty_text(collection.get("rule")):
            return "END-QNT-001"
    else:
        return "END-QNT-001"

    quantifier = target.get("quantifier")
    if not isinstance(quantifier, dict) or quantifier.get("mode") not in QUANTIFIERS:
        return "END-QNT-002"
    qmode = quantifier["mode"]
    threshold = quantifier.get("threshold")
    if qmode in {"at_least", "at_most", "exactly"}:
        if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 0:
            return "END-QNT-002"
        if qmode == "at_least" and threshold == 0:
            return "END-QNT-002"
    elif set(quantifier) != {"mode"}:
        return "END-QNT-002"
    return None


def classify(target, member_results):
    if not isinstance(member_results, list):
        return None, "END-QNT-003"
    seen = set()
    by_result = {result: 0 for result in RESULTS}
    collection = target["collection"]
    members = collection.get("members") if collection["mode"] == "enumerated" else None
    for item in member_results:
        if not isinstance(item, dict) or set(item) != {"member", "result"}:
            return None, "END-QNT-003"
        member = item.get("member")
        result = item.get("result")
        if not nonempty_text(member) or result not in RESULTS or member in seen:
            return None, "END-QNT-003"
        if members is not None and member not in members:
            return None, "END-QNT-003"
        seen.add(member)
        by_result[result] += 1

    closed = members is not None and seen == set(members)
    qmode = target["quantifier"]["mode"]
    threshold = target["quantifier"].get("threshold")

    if qmode == "all":
        if by_result["unmet"]:
            return "unmet", None
        if collection["mode"] != "enumerated":
            return "agno", None
        if not closed:
            return "agno", None
        if by_result["fault"]:
            return "fault", None
        if by_result["agno"]:
            return "agno", None
        return "met", None

    if qmode == "some":
        if by_result["met"]:
            return "met", None
        if by_result["fault"]:
            return "fault", None
        if collection["mode"] != "enumerated" or not closed or by_result["agno"]:
            return "agno", None
        return "unmet", None

    if qmode == "at_least":
        if by_result["met"] >= threshold:
            return "met", None
        if by_result["fault"]:
            return "fault", None
        if collection["mode"] != "enumerated" or not closed or by_result["agno"]:
            return "agno", None
        return "unmet", None

    if qmode == "at_most":
        if by_result["met"] > threshold:
            return "unmet", None
        if by_result["fault"]:
            return "fault", None
        if collection["mode"] != "enumerated" or not closed or by_result["agno"]:
            return "agno", None
        return "met", None

    if by_result["met"] > threshold:
        return "unmet", None
    if by_result["fault"]:
        return "fault", None
    if collection["mode"] != "enumerated" or not closed or by_result["agno"]:
        return "agno", None
    return ("met" if by_result["met"] == threshold else "unmet"), None


def proposal_violation(case):
    violation = validate_target(case.get("target"))
    if violation:
        return violation
    actual, violation = classify(case["target"], case.get("member_results"))
    if violation:
        return violation
    proposed = case.get("proposed_result")
    if proposed not in RESULTS or proposed != actual:
        target = case["target"]
        if target["quantifier"]["mode"] == "all" and target["collection"]["mode"] != "enumerated":
            return "END-QNT-002"
        return "END-QNT-003"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read quantification vectors: {exc}")
        return 1

    if document.get("vector_format") != "end-core.quantification-vector.v1":
        errors.append("quantification vectors must use end-core.quantification-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("quantification vectors must pin END-CORE 0.1.0-draft")
    if "not a collection resolver, Praxor, evaluator, or component implementation" not in document.get("description", ""):
        errors.append("quantification vectors must state their non-implementation boundary")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("quantification vectors require exactly 12 proposal cases")
        cases = []

    seen = set()
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
        elif case_id in seen:
            errors.append(f"{label}: duplicate id {case_id}")
        else:
            seen.add(case_id)

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
            errors.append(f"{case_id}: expected {expect['result']}, evaluated {actual_result}")
        if actual_result == "reject" and violation != expect["clause"]:
            errors.append(f"{case_id}: expected clause {expect['clause']}, evaluated {violation}")

    if counts != {"accept": 6, "reject": 6}:
        errors.append(f"quantification vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(
            f"quantification reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}"
        )

    if errors:
        print("\n".join(errors))
        return 1
    print(
        "PASS: executed 12 quantification vectors "
        "(6 accepted classifications, 6 deterministic rejects across 3 clauses)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
