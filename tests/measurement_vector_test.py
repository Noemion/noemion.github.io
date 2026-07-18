from pathlib import Path
import json
import math
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "measurement" / "cases.json"
CASE_ID = re.compile(r"^MV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {"END-MSR-001", "END-MSR-002", "END-MSR-003", "END-MSR-004"}
RESULTS = {"met", "unmet", "undetermined", "fault"}
REDUCERS = {"point", "count", "sum", "min", "max", "arithmetic_mean", "fraction", "quantile", "model_estimate"}
COMPARATORS = {"lt", "le", "gt", "ge", "eq"}
UNIT_DIMENSIONS = {"ms": "time", "s": "time", "1": "dimensionless", "%": "dimensionless", "byte": "information"}
UNIT_SCALE = {"ms": 0.001, "s": 1.0, "1": 1.0, "%": 0.01, "byte": 1.0}


def text(value):
    return isinstance(value, str) and bool(value)


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_target(target):
    if not isinstance(target, dict):
        return "END-MSR-001"
    construct = target.get("construct")
    if not isinstance(construct, dict) or any(not text(construct.get(k)) for k in ("id", "relation", "value_role", "authority", "scope")):
        return "END-MSR-001"
    procedure = target.get("procedure")
    if not isinstance(procedure, dict) or any(not text(procedure.get(k)) for k in ("id", "producer", "version", "window", "inclusion", "exclusion", "unit", "dimension")):
        return "END-MSR-001"
    if procedure.get("population") not in {"fixed_population", "generalized_population"}:
        return "END-MSR-001"
    if procedure["population"] == "generalized_population" and (not text(procedure.get("statistical_model")) or not text(procedure.get("assumptions"))):
        return "END-MSR-001"
    unit = procedure["unit"]
    if UNIT_DIMENSIONS.get(unit) != procedure["dimension"]:
        return "END-MSR-002"
    if not isinstance(procedure.get("min_count"), int) or isinstance(procedure.get("min_count"), bool) or procedure["min_count"] <= 0:
        return "END-MSR-003"
    if procedure.get("missing") != "undetermined":
        return "END-MSR-003"
    reducer = procedure.get("reducer")
    if not isinstance(reducer, dict) or reducer.get("mode") not in REDUCERS:
        return "END-MSR-003"
    mode = reducer["mode"]
    if mode == "arithmetic_mean" and not text(reducer.get("weighting")):
        return "END-MSR-003"
    if mode == "fraction" and (not text(reducer.get("numerator")) or not text(reducer.get("denominator"))):
        return "END-MSR-003"
    if mode == "quantile":
        if not finite_number(reducer.get("q")) or not 0 < reducer["q"] < 1 or not text(reducer.get("method")) or not finite_number(reducer.get("max_error")) or reducer["max_error"] < 0:
            return "END-MSR-003"
    if mode == "model_estimate" and not text(reducer.get("estimand")):
        return "END-MSR-003"
    comparison = target.get("comparison")
    if not isinstance(comparison, dict) or comparison.get("op") not in COMPARATORS:
        return "END-MSR-004"
    threshold = comparison.get("threshold")
    if not isinstance(threshold, dict) or not finite_number(threshold.get("value")) or not text(threshold.get("unit")):
        return "END-MSR-004"
    if UNIT_DIMENSIONS.get(threshold["unit"]) != procedure["dimension"]:
        return "END-MSR-002"
    rounding = comparison.get("rounding")
    if rounding != "none":
        if not isinstance(rounding, dict) or rounding.get("stage") != "display-only" or not text(rounding.get("mode")) or not isinstance(rounding.get("digits"), int):
            return "END-MSR-002"
    if comparison.get("uncertainty") != "interval":
        return "END-MSR-004"
    return None


def normalize(value, unit):
    return value * UNIT_SCALE[unit]


def classify(target, observation):
    if not isinstance(observation, dict) or observation.get("status") not in {"complete", "incomplete", "fault"}:
        return None, "END-MSR-003"
    if observation["status"] == "fault":
        return "fault", None
    count = observation.get("count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        return None, "END-MSR-003"
    if observation["status"] == "incomplete" or count < target["procedure"]["min_count"]:
        return "undetermined", None
    if not finite_number(observation.get("value")) or not text(observation.get("unit")):
        return None, "END-MSR-002"
    if UNIT_DIMENSIONS.get(observation["unit"]) != target["procedure"]["dimension"]:
        return None, "END-MSR-002"
    interval = observation.get("interval")
    if not isinstance(interval, list) or len(interval) != 2 or not all(finite_number(x) for x in interval) or interval[0] > interval[1]:
        return None, "END-MSR-004"
    low, high = (normalize(x, observation["unit"]) for x in interval)
    threshold = target["comparison"]["threshold"]
    boundary = normalize(threshold["value"], threshold["unit"])
    op = target["comparison"]["op"]
    if op == "le":
        return ("met" if high <= boundary else "unmet" if low > boundary else "undetermined"), None
    if op == "lt":
        return ("met" if high < boundary else "unmet" if low >= boundary else "undetermined"), None
    if op == "ge":
        return ("met" if low >= boundary else "unmet" if high < boundary else "undetermined"), None
    if op == "gt":
        return ("met" if low > boundary else "unmet" if high <= boundary else "undetermined"), None
    if low == high == boundary:
        return "met", None
    if high < boundary or low > boundary:
        return "unmet", None
    return "undetermined", None


def proposal_violation(case):
    violation = validate_target(case.get("target"))
    if violation:
        return violation
    result, violation = classify(case["target"], case.get("observation"))
    if violation:
        return violation
    if case.get("proposed_result") not in RESULTS or case["proposed_result"] != result:
        return "END-MSR-004"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read measurement vectors: {exc}")
        return 1
    if document.get("vector_format") != "end-core.measurement-vector.v1":
        errors.append("measurement vectors must use end-core.measurement-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("measurement vectors must pin END-CORE 0.1.0-draft")
    if "not a telemetry collector, benchmark runner, statistical engine, runner, evaluator, or component implementation" not in document.get("description", ""):
        errors.append("measurement vectors must state their non-implementation boundary")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("measurement vectors require exactly 12 proposal cases")
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
        if not isinstance(expect, dict) or expect.get("result") not in counts or expect.get("clause") not in CLAUSES:
            errors.append(f"{case_id or label}: invalid expectation")
            continue
        violation = proposal_violation(case)
        actual = "reject" if violation else "accept"
        counts[actual] += 1
        if violation:
            rejected_clauses.add(violation)
        if actual != expect["result"]:
            errors.append(f"{case_id}: expected {expect['result']}, evaluated {actual}")
        if violation and violation != expect["clause"]:
            errors.append(f"{case_id}: expected clause {expect['clause']}, evaluated {violation}")
    if counts != {"accept": 6, "reject": 6}:
        errors.append(f"measurement vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(f"measurement reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 12 measurement vectors (6 accepted classifications, 6 deterministic rejects across 4 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
