from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "composition" / "cases.json"
CASE_ID = re.compile(r"^CV-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {"END-CMP-001", "END-CMP-002", "END-CMP-003", "END-CMP-004"}
RESULTS = {"met", "unmet", "agno", "fault"}
OPERATORS = {"all_of", "any_of"}


def validate_target(target):
    if not isinstance(target, dict):
        return None, None, "END-CMP-001"
    if target.get("same_terminal") is not True or target.get("shared_telis") is not True or target.get("shared_authority") is not True or target.get("independent_lifecycle") is not False:
        return None, None, "END-CMP-001"
    nodes = target.get("nodes")
    root = target.get("root")
    if not isinstance(nodes, dict) or not isinstance(root, str) or root not in nodes:
        return None, None, "END-CMP-002"
    leaves = []
    visiting = set()
    visited = set()

    def walk(node_id):
        if node_id in visiting or node_id not in nodes:
            return False
        if node_id in visited:
            return False
        visiting.add(node_id)
        node = nodes[node_id]
        if not isinstance(node, dict):
            return False
        kind = node.get("kind")
        if kind == "leaf":
            criterion_id = node.get("criterion_id")
            if not isinstance(criterion_id, str) or not criterion_id:
                return False
            leaves.append(criterion_id)
        elif kind in OPERATORS:
            children = node.get("children")
            if not isinstance(children, list) or len(children) < 2 or len(children) != len(set(children)):
                return False
            for child in children:
                if not isinstance(child, str) or not walk(child):
                    return False
        else:
            return False
        visiting.remove(node_id)
        visited.add(node_id)
        return True

    if not walk(root) or visited != set(nodes) or len(leaves) != len(set(leaves)):
        return None, None, "END-CMP-002"
    krin_leaves = target.get("krin_leaves")
    if not isinstance(krin_leaves, list) or len(krin_leaves) != len(set(krin_leaves)) or set(krin_leaves) != set(leaves):
        return None, None, "END-CMP-002"
    return nodes, leaves, None


def evaluate_node(node_id, nodes, leaf_results):
    node = nodes[node_id]
    if node["kind"] == "leaf":
        result = leaf_results.get(node["criterion_id"])
        return result if result in RESULTS else None
    results = [evaluate_node(child, nodes, leaf_results) for child in node["children"]]
    if any(result is None for result in results):
        return None
    if node["kind"] == "all_of":
        if "unmet" in results:
            return "unmet"
        if "fault" in results:
            return "fault"
        if "agno" in results:
            return "agno"
        return "met"
    if "met" in results:
        return "met"
    if "fault" in results:
        return "fault"
    if "agno" in results:
        return "agno"
    return "unmet"


def proposal_violation(case):
    nodes, leaves, violation = validate_target(case.get("target"))
    if violation:
        return violation
    evaluation = case.get("evaluation")
    proposal = case.get("proposal")
    if not isinstance(evaluation, dict) or not isinstance(proposal, dict):
        return "END-CMP-004"
    leaf_results = evaluation.get("leaf_results")
    order = evaluation.get("order")
    if not isinstance(leaf_results, dict) or set(leaf_results) != set(leaves) or any(result not in RESULTS for result in leaf_results.values()):
        return "END-CMP-003"
    if not isinstance(order, list) or len(order) != len(set(order)) or set(order) != set(leaves):
        return "END-CMP-004"
    expected = evaluate_node(case["target"]["root"], nodes, leaf_results)
    evaluated = proposal.get("evaluated")
    unevaluated = proposal.get("unevaluated")
    basis = proposal.get("decisive_basis")
    if not all(isinstance(value, list) for value in (evaluated, unevaluated, basis)):
        return "END-CMP-004"
    if len(evaluated) != len(set(evaluated)) or len(unevaluated) != len(set(unevaluated)) or set(evaluated).intersection(unevaluated) or set(evaluated).union(unevaluated) != set(leaves):
        return "END-CMP-004"
    if evaluated != order[:len(evaluated)]:
        return "END-CMP-004"
    root_kind = nodes[case["target"]["root"]]["kind"]
    decisive_result = "unmet" if root_kind == "all_of" else "met"
    if evaluation.get("short_circuit") is True:
        if not unevaluated or proposal.get("result") != decisive_result or not basis or not set(basis).issubset(evaluated):
            return "END-CMP-004"
        if any(leaf_results[item] != decisive_result for item in basis):
            return "END-CMP-004"
    elif evaluation.get("short_circuit") is False:
        if unevaluated or evaluated != order or basis:
            return "END-CMP-004"
    else:
        return "END-CMP-004"
    if expected is None or proposal.get("result") != expected:
        return "END-CMP-003"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read composition vectors: {exc}")
        return 1
    if document.get("vector_format") != "end-core.composition-vector.v1":
        errors.append("composition vectors must use end-core.composition-vector.v1")
    if document.get("spec") != {"id": "END-CORE", "version": "0.1.0-draft"}:
        errors.append("composition vectors must pin END-CORE 0.1.0-draft")
    if "not a parser, Drasor, evaluator, runtime, or component implementation" not in document.get("description", ""):
        errors.append("composition vectors must state their non-implementation boundary")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 12:
        errors.append("composition vectors require exactly 12 proposal cases")
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
        errors.append(f"composition vectors require 6 accepts and 6 rejects, got {counts}")
    if rejected_clauses != CLAUSES:
        errors.append(f"composition reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected_clauses)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 12 composition vectors (6 accepted classifications, 6 deterministic rejects across 4 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
