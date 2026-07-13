from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VECTOR_ROOT = ROOT / "vectors" / "semantic"
ERROR_CATALOG = ROOT / "spec" / "diagnostic-catalog.md"
FACETS = ("rhem", "semion", "skena", "telis", "krin", "apor")
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
    skena = require_mapping(model.get("skena"), "/input/skena")
    roots = require_list(skena.get("roots"), "/input/skena/roots")
    if len(roots) != 1:
        index = 0 if not roots else 1
        fail("endem.root.not_unique", "END-CORE-001", f"/input/skena/roots/{index}")

    situations = require_list(skena.get("situations"), "/input/skena/situations")
    for index, situation in enumerate(situations):
        situation = require_mapping(situation, f"/input/skena/situations/{index}")
        if "force" in situation:
            fail(
                "endem.skena.contains_goal_force",
                "END-SIT-001",
                f"/input/skena/situations/{index}/force",
            )

    semion = require_mapping(model.get("semion"), "/input/semion")
    relations = require_list(semion.get("relations"), "/input/semion/relations")
    for index, relation in enumerate(relations):
        relation = require_mapping(relation, f"/input/semion/relations/{index}")
        projection = relation.get("projection")
        if isinstance(projection, dict) and projection.get("kind") not in {
            "rule", "named-authority"
        }:
            fail(
                "endem.projection.authority_untrusted",
                "END-AUT-001",
                f"/input/semion/relations/{index}/projection",
            )

    candidates = semion.get("projection_candidates", [])
    apor = require_list(model.get("apor"), "/input/apor")
    if isinstance(candidates, list) and len(candidates) > 1 and not apor:
        fail(
            "endem.apor.unrecorded_projection_choice",
            "END-APR-001",
            "/input/apor",
        )

    rhem = require_mapping(model.get("rhem"), "/input/rhem")
    content = rhem.get("content")
    source_range = rhem.get("range")
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
                "endem.rhem.range_out_of_bounds",
                "END-SRC-001",
                "/input/rhem/range",
            )


def validate_rhem(rhem):
    source_id = require_text(rhem.get("source_id"), "END-SRC-001", "/input/rhem/source_id", token=True)
    for field in ("subject", "media_type", "language"):
        require_text(rhem.get(field), "END-SRC-001", f"/input/rhem/{field}", token=True)
    require_text(rhem.get("version"), "END-SRC-001", "/input/rhem/version")
    content = require_text(rhem.get("content"), "END-SRC-001", "/input/rhem/content")
    source_range = require_mapping(rhem.get("range"), "/input/rhem/range")
    if source_range.get("unit") != "unicode-scalar":
        fail("endem.rhem.range_unit", "END-SRC-001", "/input/rhem/range/unit")
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
        fail("endem.rhem.range_out_of_bounds", "END-SRC-001", "/input/rhem/range")
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


def validate_semion(semion, source_id, context):
    symbols = require_list(semion.get("symbols"), "/input/semion/symbols")
    relations = require_list(semion.get("relations"), "/input/semion/relations")
    if not symbols or not relations:
        fail("endem.semion.empty_projection", "END-SEM-001", "/input/semion")

    symbol_ids = set()
    for index, symbol in enumerate(symbols):
        symbol = require_mapping(symbol, f"/input/semion/symbols/{index}")
        symbol_id = require_text(symbol.get("id"), "END-SEM-001", f"/input/semion/symbols/{index}/id", token=True)
        if symbol_id in symbol_ids:
            fail("endem.semion.duplicate_symbol", "END-SEM-001", f"/input/semion/symbols/{index}/id")
        symbol_ids.add(symbol_id)
        require_text(symbol.get("kind"), "END-SEM-001", f"/input/semion/symbols/{index}/kind", token=True)
        source_ref = require_text(symbol.get("source_ref"), "END-SEM-001", f"/input/semion/symbols/{index}/source_ref", token=True)
        if not source_ref.startswith(source_id):
            fail("endem.semion.source_ref", "END-SEM-001", f"/input/semion/symbols/{index}/source_ref")

    relation_ids = set()
    for index, relation in enumerate(relations):
        relation = require_mapping(relation, f"/input/semion/relations/{index}")
        relation_id = require_text(relation.get("id"), "END-SEM-001", f"/input/semion/relations/{index}/id", token=True)
        if relation_id in relation_ids:
            fail("endem.semion.duplicate_relation", "END-SEM-001", f"/input/semion/relations/{index}/id")
        relation_ids.add(relation_id)
        require_text(relation.get("predicate"), "END-SEM-001", f"/input/semion/relations/{index}/predicate", token=True)
        roles = require_list(relation.get("roles"), f"/input/semion/relations/{index}/roles")
        if not roles:
            fail("endem.semion.empty_roles", "END-STR-001", f"/input/semion/relations/{index}/roles")
        role_names = set()
        for role_index, role in enumerate(roles):
            role = require_mapping(role, f"/input/semion/relations/{index}/roles/{role_index}")
            role_name = require_text(role.get("name"), "END-STR-001", f"/input/semion/relations/{index}/roles/{role_index}/name", token=True)
            if role_name in role_names:
                fail("endem.semion.duplicate_role", "END-STR-001", f"/input/semion/relations/{index}/roles/{role_index}/name")
            role_names.add(role_name)
            symbol_id = require_text(role.get("symbol"), "END-STR-001", f"/input/semion/relations/{index}/roles/{role_index}/symbol", token=True)
            if symbol_id not in symbol_ids:
                fail("endem.semion.unknown_symbol", "END-STR-001", f"/input/semion/relations/{index}/roles/{role_index}/symbol")
        projection = require_mapping(relation.get("projection"), f"/input/semion/relations/{index}/projection")
        if projection.get("kind") not in {"rule", "named-authority"}:
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"/input/semion/relations/{index}/projection")
        require_text(projection.get("id"), "END-SEM-001", f"/input/semion/relations/{index}/projection/id", token=True)
        validate_external_authorization(context, projection, f"/input/semion/relations/{index}/projection")
    return relation_ids


def validate_skena(skena, relation_ids):
    roots = require_list(skena.get("roots"), "/input/skena/roots")
    if len(roots) != 1:
        fail("endem.root.not_unique", "END-CORE-001", "/input/skena/roots")
    root = require_text(roots[0], "END-CORE-001", "/input/skena/roots/0", token=True)
    situations = require_list(skena.get("situations"), "/input/skena/situations")
    situation_ids = set()
    for index, situation in enumerate(situations):
        situation = require_mapping(situation, f"/input/skena/situations/{index}")
        situation_id = require_text(situation.get("id"), "END-SIT-001", f"/input/skena/situations/{index}/id", token=True)
        if situation_id in situation_ids:
            fail("endem.skena.duplicate_situation", "END-SIT-001", f"/input/skena/situations/{index}/id")
        situation_ids.add(situation_id)
        relation = require_text(situation.get("relation"), "END-STR-001", f"/input/skena/situations/{index}/relation", token=True)
        if relation not in relation_ids:
            fail("endem.skena.unknown_relation", "END-STR-001", f"/input/skena/situations/{index}/relation")
        if situation.get("polarity") not in {"positive", "negative"}:
            fail("endem.skena.polarity", "END-SIT-001", f"/input/skena/situations/{index}/polarity")
        if "force" in situation:
            fail("endem.skena.contains_goal_force", "END-SIT-001", f"/input/skena/situations/{index}/force")
    if root not in situation_ids:
        fail("endem.root.missing_situation", "END-CORE-001", "/input/skena/roots/0")


def validate_telis(telis):
    mode = telis.get("mode")
    if mode not in {"kine", "mene"}:
        fail("endem.telis.mode", "END-TEL-001", "/input/telis/mode")
    if mode == "mene" and not isinstance(telis.get("interval"), dict):
        fail("endem.telis.interval", "END-TEL-001", "/input/telis/interval")


def validate_krin(krin, relation_ids):
    required_phain = require_list(krin.get("required_phain"), "/input/krin/required_phain")
    if not required_phain:
        fail("endem.krin.empty_observation", "END-KRN-001", "/input/krin/required_phain")
    for index, requirement in enumerate(required_phain):
        requirement = require_mapping(requirement, f"/input/krin/required_phain/{index}")
        relation = require_text(requirement.get("relation"), "END-KRN-001", f"/input/krin/required_phain/{index}/relation", token=True)
        if relation not in relation_ids:
            fail("endem.krin.unknown_relation", "END-STR-001", f"/input/krin/required_phain/{index}/relation")
        if requirement.get("match") != "same-roles":
            fail("endem.krin.match", "END-KRN-001", f"/input/krin/required_phain/{index}/match")
    required_iknem = require_list(krin.get("required_iknem"), "/input/krin/required_iknem")
    if not required_iknem:
        fail("endem.krin.empty_evidence", "END-KRN-001", "/input/krin/required_iknem")
    for index, evidence in enumerate(required_iknem):
        require_text(evidence, "END-KRN-001", f"/input/krin/required_iknem/{index}", token=True)
    if krin.get("on_missing_observation") != "agno":
        fail("endem.krin.missing_policy", "END-KRN-001", "/input/krin/on_missing_observation")
    if krin.get("on_evaluation_error") != "fault":
        fail("endem.krin.error_policy", "END-KRN-001", "/input/krin/on_evaluation_error")
    require_text(krin.get("decision_authority"), "END-KRN-001", "/input/krin/decision_authority", token=True)


def validate_apor(apor):
    for index, item in enumerate(apor):
        item = require_mapping(item, f"/input/apor/{index}")
        for field in ("id", "source_ref", "conflict", "decision_authority"):
            require_text(item.get(field), "END-APR-001", f"/input/apor/{index}/{field}", token=field != "conflict")
        candidates = require_list(item.get("candidates"), f"/input/apor/{index}/candidates")
        if len(candidates) < 2:
            fail("endem.apor.candidates", "END-APR-001", f"/input/apor/{index}/candidates")
        for candidate_index, candidate in enumerate(candidates):
            require_text(candidate, "END-APR-001", f"/input/apor/{index}/candidates/{candidate_index}", token=True)
        resolutions = require_list(item.get("allowed_resolutions"), f"/input/apor/{index}/allowed_resolutions")
        if not resolutions or any(value not in {"rule", "named-authority"} for value in resolutions):
            fail("endem.apor.resolution", "END-APR-001", f"/input/apor/{index}/allowed_resolutions")


def validate_model(model, context):
    if not isinstance(model, dict) or set(model) != set(FACETS):
        fail("endem.semantic.facets", "END-CORE-002", "/input")
    validate_primary_rejections(model)
    source_id = validate_rhem(require_mapping(model["rhem"], "/input/rhem"))
    relation_ids = validate_semion(require_mapping(model["semion"], "/input/semion"), source_id, context)
    validate_skena(require_mapping(model["skena"], "/input/skena"), relation_ids)
    validate_telis(require_mapping(model["telis"], "/input/telis"))
    validate_krin(require_mapping(model["krin"], "/input/krin"), relation_ids)
    validate_apor(require_list(model["apor"], "/input/apor"))


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
