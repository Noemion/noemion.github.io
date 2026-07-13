from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "iknem" / "cases.json"
CASE_ID = re.compile(r"^IK-(?:VALID|REJECT)-[A-Z0-9-]+-[0-9]{3}$")
CLAUSES = {
    "IKN-SCP-001", "IKN-PRV-001", "IKN-OBS-001", "IKN-CLS-001",
    "IKN-INT-001", "IKN-VAL-001", "IKN-COV-001", "IKN-DEC-001",
    "IKN-PRI-001",
}
RECORD_KINDS = {"observation", "derivation", "attestation", "appraisal", "decision-record"}
SOURCE_CLASSES = {
    "direct-observation", "deterministic-derivation", "external-assertion",
    "human-judgment", "model-candidate",
}


def proposal_violation(case):
    proposal = case.get("proposal")
    if not isinstance(proposal, dict):
        return "IKN-SCP-001"
    producer = proposal.get("producer")
    if (
        not isinstance(proposal.get("subject"), str)
        or not proposal.get("scope")
        or not isinstance(producer, dict)
        or not producer.get("id")
        or not producer.get("authority")
        or not proposal.get("method")
        or not proposal.get("environment")
        or not proposal.get("cutoff")
        or not proposal.get("claim")
        or not isinstance(proposal.get("limitations"), list)
    ):
        return "IKN-SCP-001"
    provenance = proposal.get("provenance")
    if (
        not isinstance(provenance, dict)
        or not isinstance(provenance.get("inputs"), list)
        or not provenance.get("inputs")
        or provenance.get("cycle") is not False
        or provenance.get("hidden_inputs") is not False
    ):
        return "IKN-PRV-001"
    observation = proposal.get("observation")
    if observation is not None and (
        not isinstance(observation, dict)
        or not observation.get("raw_ref")
        or not isinstance(observation.get("transforms"), list)
        or observation.get("phain_aligned") is not True
        or observation.get("inference_as_observation") is not False
    ):
        return "IKN-OBS-001"
    if (
        proposal.get("record_kind") not in RECORD_KINDS
        or proposal.get("source_class") not in SOURCE_CLASSES
        or proposal.get("self_upgrade") is not False
    ):
        return "IKN-CLS-001"
    integrity = proposal.get("integrity")
    if not isinstance(integrity, dict) or integrity.get("truth_separate") is not True:
        return "IKN-INT-001"
    validity = proposal.get("validity")
    if (
        not isinstance(validity, dict)
        or validity.get("external") is not True
        or not validity.get("policy")
        or not validity.get("cutoff")
        or validity.get("state") not in {"valid", "invalid", "revoked"}
        or validity.get("recheck") is not True
    ):
        return "IKN-VAL-001"
    coverage = proposal.get("coverage")
    if (
        not isinstance(coverage, dict)
        or not coverage.get("krin")
        or coverage.get("distinct_responsibilities") is not True
        or coverage.get("duplicate_counts") is not False
        or coverage.get("result") not in {"sufficient", "insufficient"}
        or (coverage.get("gaps") is True and coverage.get("result") != "insufficient")
    ):
        return "IKN-COV-001"
    decision = proposal.get("decision")
    if (
        not isinstance(decision, dict)
        or decision.get("appraisal_separate") is not True
        or decision.get("auto_accept") is not False
        or (proposal.get("record_kind") == "decision-record" and not decision.get("authority"))
    ):
        return "IKN-DEC-001"
    disclosure = proposal.get("disclosure")
    if (
        not isinstance(disclosure, dict)
        or disclosure.get("secrets") is not False
        or disclosure.get("loss_declared") is not True
        or disclosure.get("external_refs_exact") is not True
    ):
        return "IKN-PRI-001"
    return None


def main():
    errors = []
    try:
        document = json.loads(VECTOR_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read Iknem vectors: {exc}")
        return 1
    if document.get("vector_format") != "ikn-core.vector.v1":
        errors.append("Iknem vectors must use ikn-core.vector.v1")
    if document.get("spec") != {"id": "IKN-CORE", "version": "0.1.0-draft"}:
        errors.append("Iknem vectors must pin IKN-CORE 0.1.0-draft")
    if "not a collector, verifier, merger, revocation service, decision engine, runtime, or component implementation" not in document.get("description", ""):
        errors.append("Iknem vectors must state their non-implementation boundary")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 18:
        errors.append("Iknem vectors require exactly 18 proposal cases")
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
    if counts != {"accept": 9, "reject": 9}:
        errors.append(f"Iknem vectors require 9 accepts and 9 rejects, got {counts}")
    if rejected != CLAUSES:
        errors.append(f"Iknem reject coverage must include {sorted(CLAUSES)}, got {sorted(rejected)}")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: executed 18 Iknem vectors (9 accepted classifications, 9 deterministic rejects across 9 clauses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
