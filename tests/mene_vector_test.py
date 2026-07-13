from datetime import datetime, timezone
from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "mene" / "cases.json"
CASE_ID = re.compile(r"^MV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
UTC_INSTANT = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-5][0-9]Z$")
RESULTS = {"met", "unmet", "agno", "fault"}
CLAUSES = {"END-TIM-001", "END-TIM-002", "END-TIM-003"}


def parse_utc(value):
    if not isinstance(value, str) or UTC_INSTANT.fullmatch(value) is None:
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return int(parsed.timestamp())


def positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_scope(scope):
    if not isinstance(scope, dict):
        return None, "END-TIM-001"
    kind = scope.get("kind")
    if kind == "fixed":
        start = parse_utc(scope.get("start"))
        end = parse_utc(scope.get("end"))
        authority = scope.get("authority")
        if (
            start is None
            or end is None
            or start >= end
            or not isinstance(authority, str)
            or not authority
            or authority == "system-default"
        ):
            return None, "END-TIM-001"
        return end - start, None
    if kind == "elapsed":
        if (
            not isinstance(scope.get("anchor_event"), str)
            or not scope["anchor_event"]
            or not positive_int(scope.get("duration_seconds"))
            or scope.get("clock_domain") != "monotonic"
            or not isinstance(scope.get("clock_authority"), str)
            or not scope["clock_authority"]
            or not isinstance(scope.get("restart_boundary"), str)
            or not scope["restart_boundary"]
        ):
            return None, "END-TIM-001"
        return scope["duration_seconds"], None
    return None, "END-TIM-001"


def validate_continuity(continuity):
    if not isinstance(continuity, dict):
        return "END-TIM-002"
    kind = continuity.get("kind")
    if kind == "strict":
        return None if set(continuity) == {"kind"} else "END-TIM-002"
    if kind != "budgeted":
        return "END-TIM-002"
    required = {
        "kind",
        "max_total_breach_seconds",
        "max_single_breach_seconds",
        "max_breach_count",
    }
    if set(continuity) != required:
        return "END-TIM-002"
    if not all(nonnegative_int(continuity[field]) for field in required - {"kind"}):
        return "END-TIM-002"
    return None


def normalize_intervals(intervals, duration):
    if not isinstance(intervals, list):
        return None
    parsed = []
    for interval in intervals:
        if (
            not isinstance(interval, list)
            or len(interval) != 2
            or not all(nonnegative_int(value) for value in interval)
            or interval[0] >= interval[1]
            or interval[1] > duration
        ):
            return None
        parsed.append(tuple(interval))
    parsed.sort()
    merged = []
    for start, end in parsed:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def classify(case, duration):
    observation = case.get("observation")
    if not isinstance(observation, dict):
        return None, "END-TIM-003"
    clock_status = observation.get("clock_status")
    if clock_status == "invalid":
        return "fault", None
    if clock_status == "uncertain":
        return "agno", None
    if clock_status != "valid":
        return None, "END-TIM-003"

    coverage = normalize_intervals(observation.get("coverage"), duration)
    breaches = normalize_intervals(observation.get("breaches"), duration)
    if coverage is None or breaches is None:
        return None, "END-TIM-003"
    if coverage != [[0, duration]]:
        return "agno", None

    continuity = case["continuity"]
    if continuity["kind"] == "strict":
        return ("unmet" if breaches else "met"), None

    breach_durations = [end - start for start, end in breaches]
    exceeds = (
        sum(breach_durations) > continuity["max_total_breach_seconds"]
        or max(breach_durations, default=0) > continuity["max_single_breach_seconds"]
        or len(breaches) > continuity["max_breach_count"]
    )
    return ("unmet" if exceeds else "met"), None


def proposal_violation(case):
    duration, violation = validate_scope(case.get("scope"))
    if violation:
        return violation
    violation = validate_continuity(case.get("continuity"))
    if violation:
        return violation
    actual, violation = classify(case, duration)
    if violation:
        return violation
    proposed = case.get("proposed_result")
    if proposed not in RESULTS or proposed != actual:
        return "END-TIM-003"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read mene vectors: {exc}")
        return 1

    if document.get("vector_format") != "end-core.mene-vector.v1":
        errors.append("mene vectors must use end-core.mene-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("mene vectors must pin END-CORE 0.1.0-draft")
    description = document.get("description", "")
    if "not a clock, monitor, Drasor, or evaluator implementation" not in description:
        errors.append("mene vectors must state their non-implementation boundary")

    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("mene vectors require exactly 12 proposal cases")
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
        errors.append(f"mene vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(
            f"mene reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}"
        )

    if errors:
        print("\n".join(errors))
        return 1
    print(
        "PASS: executed 12 mene vectors "
        "(6 accepted classifications, 6 deterministic rejects across 3 clauses)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
