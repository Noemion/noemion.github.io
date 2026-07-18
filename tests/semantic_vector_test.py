from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_ROOT = ROOT / "vectors" / "semantic"
ERROR_CATALOG = ROOT / "spec" / "diagnostic-catalog.md"
FACETS = ("source_expression", "meaning_projection", "situation", "goal_direction", "satisfaction_criteria", "unresolved_meaning")
TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9._:/#-]{0,254}$")


class SemanticError(Exception):
    def __init__(self, code, clause, location):
        super().__init__(code)
        self.diagnostic = {
            "code": code,
            "clause": clause,
            "location": location,
        }


def fail(code, clause, location):
    raise SemanticError(code, clause, location)


def require_mapping(value, location):
    if not isinstance(value, dict):
        fail("endem.semantic.facet.type", "END-CORE-002", location)
    return value


def require_list(value, location):
    if not isinstance(value, list):
        fail("endem.semantic.facet.type", "END-CORE-002", location)
    return value


def require_text(value, clause, location, *, token=False):
    if not isinstance(value, str) or not value:
        fail("endem.semantic.field.text", clause, location)
    if token and TOKEN.fullmatch(value) is None:
        fail("endem.semantic.field.token", clause, location)
    return value


def validate_primary_rejections(model):
    situation = require_mapping(model.get("situation"), "/input/situation")
    roots = require_list(situation.get("roots"), "/input/situation/roots")
    if len(roots) != 1:
        index = 0 if not roots else 1
        fail("endem.root.not_unique", "END-CORE-001", f"/input/situation/roots/{index}")

    situations = require_list(situation.get("situations"), "/input/situation/situations")
    for index, situation in enumerate(situations):
        situation = require_mapping(situation, f"/input/situation/situations/{index}")
        if "force" in situation:
            fail(
                "endem.situation.contains_goal_force",
                "END-SIT-001",
                f"/input/situation/situations/{index}/force",
            )

    meaning_projection = require_mapping(model.get("meaning_projection"), "/input/meaning_projection")
    relations = require_list(meaning_projection.get("relations"), "/input/meaning_projection/relations")
    for index, relation in enumerate(relations):
        relation = require_mapping(relation, f"/input/meaning_projection/relations/{index}")
        projection = relation.get("projection")
        if isinstance(projection, dict) and projection.get("kind") not in {
            "rule", "named-authority"
        }:
            fail(
                "endem.projection.authority_untrusted",
                "END-AUT-001",
                f"/input/meaning_projection/relations/{index}/projection",
            )

    candidates = meaning_projection.get("projection_candidates", [])
    unresolved_meaning = require_list(model.get("unresolved_meaning"), "/input/unresolved_meaning")
    if isinstance(candidates, list) and len(candidates) > 1 and not unresolved_meaning:
        fail(
            "endem.unresolved_meaning.unrecorded_projection_choice",
            "END-UNRESOLVED-001",
            "/input/unresolved_meaning",
        )

    source_expression = require_mapping(model.get("source_expression"), "/input/source_expression")
    content = source_expression.get("content")
    source_range = source_expression.get("range")
    if isinstance(content, str) and isinstance(source_range, dict):
        start = source_range.get("start")
        length = source_range.get("length")
        if (
            not isinstance(start, int)
            or isinstance(start, bool)
            or not isinstance(length, int)
            or isinstance(length, bool)
            or start < 0
            or length < 0
            or start + length > len(content)
        ):
            fail(
                "endem.source_expression.range_out_of_bounds",
                "END-SRC-001",
                "/input/source_expression/range",
            )


def validate_source(source_expression):
    source_id = require_text(source_expression.get("source_id"), "END-SRC-001", "/input/source_expression/source_id", token=True)
    for field in ("subject", "media_type", "language"):
        require_text(source_expression.get(field), "END-SRC-001", f"/input/source_expression/{field}", token=True)
    require_text(source_expression.get("version"), "END-SRC-001", "/input/source_expression/version")
    content = require_text(source_expression.get("content"), "END-SRC-001", "/input/source_expression/content")
    source_range = require_mapping(source_expression.get("range"), "/input/source_expression/range")
    if source_range.get("unit") != "unicode-scalar":
        fail("endem.source_expression.range_unit", "END-SRC-001", "/input/source_expression/range/unit")
    start = source_range.get("start")
    length = source_range.get("length")
    if (
        not isinstance(start, int)
        or isinstance(start, bool)
        or not isinstance(length, int)
        or isinstance(length, bool)
        or start < 0
        or length < 0
        or start + length > len(content)
    ):
        fail("endem.source_expression.range_out_of_bounds", "END-SRC-001", "/input/source_expression/range")
    return source_id


def validate_external_authorization(context, projection, location):
    if not isinstance(context, dict):
        fail("endem.projection.authorization_binding_missing", "END-AUT-002", location)
    preconditions = context.get("external_preconditions")
    if not isinstance(preconditions, list):
        fail("endem.projection.authorization_binding_missing", "END-AUT-002", location)
    matches = [item for item in preconditions if isinstance(item, dict) and item.get("subject") == location]
    if not matches:
        fail("endem.projection.authorization_binding_missing", "END-AUT-002", location)
    if len(matches) != 1:
        fail("endem.projection.authorization_binding_mismatch", "END-AUT-002", location)
    binding = matches[0]
    expected = {
        "spec_id": "AUT-CORE",
        "version": "0.1.0-draft",
        "clause": "AUT-SEM-001",
        "projection_id": projection.get("id"),
        "status": "satisfied",
    }
    if any(binding.get(key) != value for key, value in expected.items()):
        fail("endem.projection.authorization_binding_mismatch", "END-AUT-002", location)
    require_text(binding.get("evidence_ref"), "END-AUT-002", f"{location}/@authorization/evidence_ref", token=True)


def validate_meaning(meaning_projection, source_id, context):
    symbols = require_list(meaning_projection.get("symbols"), "/input/meaning_projection/symbols")
    relations = require_list(meaning_projection.get("relations"), "/input/meaning_projection/relations")
    if not symbols or not relations:
        fail("endem.meaning_projection.empty_projection", "END-MEANING-001", "/input/meaning_projection")

    symbol_ids = set()
    for index, symbol in enumerate(symbols):
        symbol = require_mapping(symbol, f"/input/meaning_projection/symbols/{index}")
        symbol_id = require_text(symbol.get("id"), "END-MEANING-001", f"/input/meaning_projection/symbols/{index}/id", token=True)
        if symbol_id in symbol_ids:
            fail("endem.meaning_projection.duplicate_symbol", "END-MEANING-001", f"/input/meaning_projection/symbols/{index}/id")
        symbol_ids.add(symbol_id)
        require_text(symbol.get("kind"), "END-MEANING-001", f"/input/meaning_projection/symbols/{index}/kind", token=True)
        source_ref = require_text(symbol.get("source_ref"), "END-MEANING-001", f"/input/meaning_projection/symbols/{index}/source_ref", token=True)
        if not source_ref.startswith(source_id):
            fail("endem.meaning_projection.source_ref", "END-MEANING-001", f"/input/meaning_projection/symbols/{index}/source_ref")

    relation_ids = set()
    for index, relation in enumerate(relations):
        relation = require_mapping(relation, f"/input/meaning_projection/relations/{index}")
        relation_id = require_text(relation.get("id"), "END-MEANING-001", f"/input/meaning_projection/relations/{index}/id", token=True)
        if relation_id in relation_ids:
            fail("endem.meaning_projection.duplicate_relation", "END-MEANING-001", f"/input/meaning_projection/relations/{index}/id")
        relation_ids.add(relation_id)
        require_text(relation.get("predicate"), "END-MEANING-001", f"/input/meaning_projection/relations/{index}/predicate", token=True)
        roles = require_list(relation.get("roles"), f"/input/meaning_projection/relations/{index}/roles")
        if not roles:
            fail("endem.meaning_projection.empty_roles", "END-STR-001", f"/input/meaning_projection/relations/{index}/roles")
        role_names = set()
        for role_index, role in enumerate(roles):
            role = require_mapping(role, f"/input/meaning_projection/relations/{index}/roles/{role_index}")
            role_name = require_text(role.get("name"), "END-STR-001", f"/input/meaning_projection/relations/{index}/roles/{role_index}/name", token=True)
            if role_name in role_names:
                fail("endem.meaning_projection.duplicate_role", "END-STR-001", f"/input/meaning_projection/relations/{index}/roles/{role_index}/name")
            role_names.add(role_name)
            symbol_id = require_text(role.get("symbol"), "END-STR-001", f"/input/meaning_projection/relations/{index}/roles/{role_index}/symbol", token=True)
            if symbol_id not in symbol_ids:
                fail("endem.meaning_projection.unknown_symbol", "END-STR-001", f"/input/meaning_projection/relations/{index}/roles/{role_index}/symbol")
        projection = require_mapping(relation.get("projection"), f"/input/meaning_projection/relations/{index}/projection")
        if projection.get("kind") not in {"rule", "named-authority"}:
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"/input/meaning_projection/relations/{index}/projection")
        require_text(projection.get("id"), "END-MEANING-001", f"/input/meaning_projection/relations/{index}/projection/id", token=True)
        validate_external_authorization(context, projection, f"/input/meaning_projection/relations/{index}/projection")
    return relation_ids


def validate_situation(situation, relation_ids):
    roots = require_list(situation.get("roots"), "/input/situation/roots")
    if len(roots) != 1:
        fail("endem.root.not_unique", "END-CORE-001", "/input/situation/roots")
    root = require_text(roots[0], "END-CORE-001", "/input/situation/roots/0", token=True)
    situations = require_list(situation.get("situations"), "/input/situation/situations")
    situation_ids = set()
    for index, situation in enumerate(situations):
        situation = require_mapping(situation, f"/input/situation/situations/{index}")
        situation_id = require_text(situation.get("id"), "END-SIT-001", f"/input/situation/situations/{index}/id", token=True)
        if situation_id in situation_ids:
            fail("endem.situation.duplicate_situation", "END-SIT-001", f"/input/situation/situations/{index}/id")
        situation_ids.add(situation_id)
        relation = require_text(situation.get("relation"), "END-STR-001", f"/input/situation/situations/{index}/relation", token=True)
        if relation not in relation_ids:
            fail("endem.situation.unknown_relation", "END-STR-001", f"/input/situation/situations/{index}/relation")
        if situation.get("polarity") not in {"positive", "negative"}:
            fail("endem.situation.polarity", "END-SIT-001", f"/input/situation/situations/{index}/polarity")
        if "force" in situation:
            fail("endem.situation.contains_goal_force", "END-SIT-001", f"/input/situation/situations/{index}/force")
    if root not in situation_ids:
        fail("endem.root.missing_situation", "END-CORE-001", "/input/situation/roots/0")


def validate_direction(goal_direction):
    mode = goal_direction.get("mode")
    if mode not in {"reach", "maintain"}:
        fail("endem.goal_direction.mode", "END-DIRECTION-001", "/input/goal_direction/mode")
    if mode == "maintain" and not isinstance(goal_direction.get("interval"), dict):
        fail("endem.goal_direction.interval", "END-DIRECTION-001", "/input/goal_direction/interval")


def validate_criteria(satisfaction_criteria, relation_ids):
    required_observations = require_list(satisfaction_criteria.get("required_observations"), "/input/satisfaction_criteria/required_observations")
    if not required_observations:
        fail("endem.satisfaction_criteria.empty_observation", "END-CRITERIA-001", "/input/satisfaction_criteria/required_observations")
    for index, requirement in enumerate(required_observations):
        requirement = require_mapping(requirement, f"/input/satisfaction_criteria/required_observations/{index}")
        relation = require_text(requirement.get("relation"), "END-CRITERIA-001", f"/input/satisfaction_criteria/required_observations/{index}/relation", token=True)
        if relation not in relation_ids:
            fail("endem.satisfaction_criteria.unknown_relation", "END-STR-001", f"/input/satisfaction_criteria/required_observations/{index}/relation")
        if requirement.get("match") != "same-roles":
            fail("endem.satisfaction_criteria.match", "END-CRITERIA-001", f"/input/satisfaction_criteria/required_observations/{index}/match")
    required_evidence = require_list(satisfaction_criteria.get("required_evidence"), "/input/satisfaction_criteria/required_evidence")
    if not required_evidence:
        fail("endem.satisfaction_criteria.empty_evidence", "END-CRITERIA-001", "/input/satisfaction_criteria/required_evidence")
    for index, evidence in enumerate(required_evidence):
        require_text(evidence, "END-CRITERIA-001", f"/input/satisfaction_criteria/required_evidence/{index}", token=True)
    if satisfaction_criteria.get("on_missing_observation") != "undetermined":
        fail("endem.satisfaction_criteria.missing_policy", "END-CRITERIA-001", "/input/satisfaction_criteria/on_missing_observation")
    if satisfaction_criteria.get("on_evaluation_error") != "fault":
        fail("endem.satisfaction_criteria.error_policy", "END-CRITERIA-001", "/input/satisfaction_criteria/on_evaluation_error")
    require_text(satisfaction_criteria.get("decision_authority"), "END-CRITERIA-001", "/input/satisfaction_criteria/decision_authority", token=True)


def validate_unresolved(unresolved_meaning):
    for index, item in enumerate(unresolved_meaning):
        item = require_mapping(item, f"/input/unresolved_meaning/{index}")
        for field in ("id", "source_ref", "conflict", "decision_authority"):
            require_text(item.get(field), "END-UNRESOLVED-001", f"/input/unresolved_meaning/{index}/{field}", token=field != "conflict")
        candidates = require_list(item.get("candidates"), f"/input/unresolved_meaning/{index}/candidates")
        if len(candidates) < 2:
            fail("endem.unresolved_meaning.candidates", "END-UNRESOLVED-001", f"/input/unresolved_meaning/{index}/candidates")
        for candidate_index, candidate in enumerate(candidates):
            require_text(candidate, "END-UNRESOLVED-001", f"/input/unresolved_meaning/{index}/candidates/{candidate_index}", token=True)
        resolutions = require_list(item.get("allowed_resolutions"), f"/input/unresolved_meaning/{index}/allowed_resolutions")
        if not resolutions or any(value not in {"rule", "named-authority"} for value in resolutions):
            fail("endem.unresolved_meaning.resolution", "END-UNRESOLVED-001", f"/input/unresolved_meaning/{index}/allowed_resolutions")


def validate_model(model, context):
    if not isinstance(model, dict) or set(model) != set(FACETS):
        fail("endem.semantic.facets", "END-CORE-002", "/input")
    validate_primary_rejections(model)
    source_id = validate_source(require_mapping(model["source_expression"], "/input/source_expression"))
    relation_ids = validate_meaning(require_mapping(model["meaning_projection"], "/input/meaning_projection"), source_id, context)
    validate_situation(require_mapping(model["situation"], "/input/situation"), relation_ids)
    validate_direction(require_mapping(model["goal_direction"], "/input/goal_direction"))
    validate_criteria(require_mapping(model["satisfaction_criteria"], "/input/satisfaction_criteria"), relation_ids)
    validate_unresolved(require_list(model["unresolved_meaning"], "/input/unresolved_meaning"))


def main():
    errors = []
    catalog = ERROR_CATALOG.read_text()
    vectors = sorted(VECTOR_ROOT.glob("*.json"))
    accept_count = 0
    reject_count = 0
    identity_groups = {}

    for path in vectors:
        vector = json.loads(path.read_text())
        expected = vector["expect"]
        try:
            validate_model(vector["input"], vector.get("context"))
            actual = {"result": "accept", "diagnostics": []}
        except SemanticError as exc:
            actual = {"result": "reject", "diagnostics": [exc.diagnostic]}

        expected_result = expected["result"]
        expected_diagnostics = expected["diagnostics"]
        if actual != {"result": expected_result, "diagnostics": expected_diagnostics}:
            errors.append(
                f"{path.relative_to(ROOT)}: expected "
                f"{expected_result}/{expected_diagnostics}, got {actual}"
            )
        if expected_result == "accept":
            accept_count += 1
        else:
            reject_count += 1
        for diagnostic in expected_diagnostics:
            if f"`{diagnostic['code']}`" not in catalog:
                errors.append(
                    f"{path.relative_to(ROOT)}: diagnostic catalog missing "
                    f"{diagnostic['code']}"
                )
        identity_group = vector.get("identity_equivalence_group")
        if identity_group is not None:
            identity_groups.setdefault(identity_group, []).append(
                (path, json.dumps(vector["input"], sort_keys=True, separators=(",", ":")), json.dumps(vector.get("context"), sort_keys=True))
            )

    for group_id, members in identity_groups.items():
        if len(members) < 2:
            errors.append(f"{group_id}: identity equivalence group requires at least two vectors")
            continue
        if len({member[1] for member in members}) != 1:
            errors.append(f"{group_id}: external context variants must preserve identical Endem input content")
        if len({member[2] for member in members}) != len(members):
            errors.append(f"{group_id}: external context variants must use distinct companion evidence")

    if accept_count < 1 or reject_count < 5:
        errors.append("semantic execution requires at least one accept and five rejects")
    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PASS: executed {accept_count + reject_count} semantic vectors "
        f"({accept_count} accept, {reject_count} deterministic rejects, "
        f"{len(identity_groups)} external-context identity group)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
