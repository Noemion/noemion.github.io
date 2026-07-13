from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "negation" / "cases.json"
CASE_ID = re.compile(r"^NV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
RESULTS = {"met", "unmet", "agno", "fault"}
CLAUSES = {"END-NEG-001", "END-NEG-002", "END-NEG-003"}


def nonempty_text(value):
    return isinstance(value, str) and bool(value)


def valid_roles(value):
    return (
        isinstance(value, dict)
        and bool(value)
        and all(nonempty_text(key) and nonempty_text(item) for key, item in value.items())
    )


def validate_target(target):
    if not isinstance(target, dict):
        return "END-NEG-001"
    if not nonempty_text(target.get("relation")) or not valid_roles(target.get("roles")):
        return "END-NEG-001"
    if target.get("polarity") != "negative":
        return "END-NEG-001"
    return None


def validate_closure(closure):
    if not isinstance(closure, dict):
        return False
    required = {
        "authority", "universe", "interval", "method", "cutoff",
        "dropped_count", "known_exclusions", "all_paths",
    }
    if set(closure) != required:
        return False
    if not all(nonempty_text(closure[field]) for field in (
        "authority", "universe", "interval", "method", "cutoff",
    )):
        return False
    if (
        not isinstance(closure["dropped_count"], int)
        or isinstance(closure["dropped_count"], bool)
        or closure["dropped_count"] != 0
        or not isinstance(closure["known_exclusions"], list)
        or closure["known_exclusions"]
        or closure["all_paths"] is not True
    ):
        return False
    return True


def classify(target, observation):
    if not isinstance(observation, dict):
        return None, "END-NEG-002"
    if observation.get("status") == "fault":
        return "fault", None
    if observation.get("status") != "valid":
        return None, "END-NEG-002"

    mode = observation.get("mode")
    if mode == "direct":
        if (
            observation.get("relation") != target["relation"]
            or observation.get("roles") != target["roles"]
            or observation.get("polarity") not in {"positive", "negative"}
            or not nonempty_text(observation.get("authority"))
        ):
            return None, "END-NEG-002"
        return ("met" if observation["polarity"] == "negative" else "unmet"), None

    if mode not in {"event-log", "closed-enumeration"}:
        return None, "END-NEG-002"
    count = observation.get("matching_positive_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        return None, "END-NEG-002"
    if count > 0:
        return "unmet", None
    if mode == "event-log":
        return "agno", None
    if not validate_closure(observation.get("closure")):
        return None, "END-NEG-003"
    return "met", None


def proposal_violation(case):
    violation = validate_target(case.get("target"))
    if violation:
        return violation
    actual, violation = classify(case["target"], case.get("observation"))
    if violation:
        return violation
    proposed = case.get("proposed_result")
    if proposed not in RESULTS or proposed != actual:
        observation = case.get("observation", {})
        if observation.get("status") == "fault":
            return "END-NEG-002"
        mode = observation.get("mode")
        return "END-NEG-003" if mode in {"event-log", "closed-enumeration"} else "END-NEG-002"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read negation vectors: {exc}")
        return 1

    if document.get("vector_format") != "end-core.negation-vector.v1":
        errors.append("negation vectors must use end-core.negation-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("negation vectors must pin END-CORE 0.1.0-draft")
    if "not a policy engine, log collector, Drasor, or evaluator implementation" not in document.get("description", ""):
        errors.append("negation vectors must state their non-implementation boundary")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("negation vectors require exactly 12 proposal cases")
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
        errors.append(f"negation vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(
            f"negation reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}"
        )

    if errors:
        print("\n".join(errors))
        return 1
    print(
        "PASS: executed 12 negation vectors "
        "(6 accepted classifications, 6 deterministic rejects across 3 clauses)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
