from pathlib import Path
import copy
import json
import re
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "spec" / "profiles" / "end-p2.json"
SOURCE_PATH = ROOT / "vectors" / "semantic" / "minimal-valid.json"
MANIFEST_PATH = ROOT / "vectors" / "wire" / "p2" / "manifest.json"
ERROR_CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"
MAGIC = b"ENDEM\x00\r\n"
HEADER_SIZE = 64
ENTRY_SIZE = 48
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9._:/#-]{0,254}$")
MEDIA_TYPE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$")
LANGUAGE_TAG = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")


class P2Error(Exception):
    def __init__(self, code, clause, path, layer="semantic"):
        super().__init__(code)
        self.result = {
            "result": "reject",
            "code": code,
            "clause": clause,
            "layer": layer,
            "semantic_path" if layer == "semantic" else "path": path,
        }


def fail(code, clause, path, layer="semantic"):
    raise P2Error(code, clause, path, layer)


def encode_head(major, value):
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    if value <= 0xFFFFFFFFFFFFFFFF:
        return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")
    raise ValueError("CBOR argument exceeds u64")


def encode_cbor(value):
    if isinstance(value, bool):
        return bytes([0xF5 if value else 0xF4])
    if value is None:
        return b"\xF6"
    if isinstance(value, int) and not isinstance(value, bool):
        if value < 0:
            return encode_head(1, -1 - value)
        return encode_head(0, value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        return encode_head(3, len(raw)) + raw
    if isinstance(value, list):
        return encode_head(4, len(value)) + b"".join(encode_cbor(item) for item in value)
    if isinstance(value, dict):
        if any(not isinstance(key, int) or isinstance(key, bool) or key < 0 for key in value):
            raise ValueError("P2 CBOR map keys must be unsigned integers")
        encoded = []
        for key in sorted(value, key=lambda item: encode_cbor(item)):
            encoded.append(encode_cbor(key))
            encoded.append(encode_cbor(value[key]))
        return encode_head(5, len(value)) + b"".join(encoded)
    raise TypeError(f"unsupported CBOR value {type(value)!r}")


class Budget:
    def __init__(self):
        self.items = 0
        self.allocated = 0
        self.edges = 0


class Decoder:
    def __init__(self, data, profile, budget):
        self.data = data
        self.profile = profile
        self.budget = budget

    def take(self, position, length):
        end = position + length
        if end > len(self.data):
            fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
        return self.data[position:end], end

    def argument(self, position, additional):
        if additional < 24:
            return additional, position
        widths = {24: 1, 25: 2, 26: 4, 27: 8}
        width = widths.get(additional)
        if width is None:
            fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
        raw, position = self.take(position, width)
        value = int.from_bytes(raw, "big")
        minimum = {1: 24, 2: 256, 4: 65536, 8: 4294967296}[width]
        if value < minimum:
            fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
        return value, position

    def item(self, position=0, depth=0):
        self.budget.items += 1
        if self.budget.items > self.profile["limits"]["max_graph_nodes"]:
            fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
        if depth > self.profile["limits"]["max_nesting_depth"]:
            fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
        raw, position = self.take(position, 1)
        major = raw[0] >> 5
        additional = raw[0] & 0x1F
        if major in (0, 1):
            value, position = self.argument(position, additional)
            return (value if major == 0 else -1 - value), position
        if major == 3:
            length, position = self.argument(position, additional)
            if length > self.profile["limits"]["max_string_bytes"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
            raw, position = self.take(position, length)
            self.budget.allocated += length
            if self.budget.allocated > self.profile["limits"]["max_total_allocation_bytes"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
            try:
                return raw.decode("utf-8"), position
            except UnicodeDecodeError:
                fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
        if major == 4:
            length, position = self.argument(position, additional)
            if length > self.profile["limits"]["max_graph_edges"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
            self.budget.edges += length
            if self.budget.edges > self.profile["limits"]["max_graph_edges"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
            values = []
            for _ in range(length):
                value, position = self.item(position, depth + 1)
                values.append(value)
            return values, position
        if major == 5:
            length, position = self.argument(position, additional)
            if length > self.profile["limits"]["max_graph_edges"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/", "profile")
            self.budget.edges += length
            if self.budget.edges > self.profile["limits"]["max_graph_edges"]:
                fail("endem.wire.profile.limit", "END-FMT-010", "/")
            mapping = {}
            prior_key = None
            for _ in range(length):
                key_start = position
                key, position = self.item(position, depth + 1)
                key_bytes = self.data[key_start:position]
                if not isinstance(key, int) or key < 0 or (prior_key is not None and key_bytes <= prior_key):
                    fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
                prior_key = key_bytes
                if key in mapping:
                    fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
                mapping[key], position = self.item(position, depth + 1)
            return mapping, position
        fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")


def identifier(value, path):
    if not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None:
        fail("endem.semantic.field.identifier", "END-FMT-013", path)
    return value


def anchors_source(reference, source_id):
    return reference == source_id or reference.startswith(source_id + "#/")


def exact_map(value, keys, path):
    if not isinstance(value, dict):
        fail("endem.semantic.field.type", "END-FMT-013", path)
    unknown = sorted(set(value) - set(keys))
    if unknown:
        fail("endem.semantic.field.unknown", "END-FMT-013", f"{path}/{unknown[0]}")
    missing = sorted(set(keys) - set(value))
    if missing:
        fail("endem.semantic.field.missing", "END-FMT-013", f"{path}/{missing[0]}")
    return value


def ordered_unique(items, key, path):
    if not isinstance(items, list):
        fail("endem.semantic.field.type", "END-FMT-013", path)
    values = [key(item, index) for index, item in enumerate(items)]
    if values != sorted(values) or len(values) != len(set(values)):
        fail("endem.semantic.field.order", "END-FMT-013", path)


def source_to_records(model):
    source_expression = model["source_expression"]
    meaning_projection = model["meaning_projection"]
    situation = model["situation"]
    goal_direction = model["goal_direction"]
    satisfaction_criteria = model["satisfaction_criteria"]
    projection_kind = {"rule": 0, "named-authority": 1}
    polarity = {"positive": 0, "negative": 1}

    symbols = [
        {1: item["id"], 2: item["kind"], 3: item["source_ref"]}
        for item in sorted(meaning_projection["symbols"], key=lambda item: item["id"])
    ]
    relations = []
    for item in sorted(meaning_projection["relations"], key=lambda item: item["id"]):
        roles = [
            {1: role["name"], 2: role["symbol"]}
            for role in sorted(item["roles"], key=lambda role: role["name"])
        ]
        relations.append({
            1: item["id"],
            2: item["predicate"],
            3: roles,
            4: {1: projection_kind[item["projection"]["kind"]], 2: item["projection"]["id"]},
        })
    situations = [
        {1: item["id"], 2: item["relation"], 3: polarity[item["polarity"]]}
        for item in sorted(situation["situations"], key=lambda item: item["id"])
    ]
    structured_observation = [
        {1: item["relation"], 2: 0}
        for item in sorted(satisfaction_criteria["required_observations"], key=lambda item: item["relation"])
    ]
    evidence_entry = sorted(satisfaction_criteria["required_evidence"], key=encode_cbor)
    unresolved_items = []
    for item in sorted(model["unresolved_meaning"], key=lambda value: value["id"]):
        unresolved_items.append({
            1: item["id"],
            2: item["source_ref"],
            3: sorted(item["candidates"], key=encode_cbor),
            4: item["conflict"],
            5: sorted(item["impact_scope"], key=encode_cbor),
            6: sorted(projection_kind[value] for value in item["allowed_resolutions"]),
            7: item["decision_authority"],
        })
    return {
        1: {1: source_expression["source_id"], 2: source_expression["subject"], 3: source_expression["media_type"], 4: source_expression["language"], 5: source_expression["version"], 6: source_expression["content"], 7: {1: 0, 2: source_expression["range"]["start"], 3: source_expression["range"]["length"]}},
        2: {1: symbols, 2: relations},
        3: {1: situation["roots"][0], 2: situations},
        4: {1: 0 if goal_direction["mode"] == "reach" else 1},
        5: {1: structured_observation, 2: evidence_entry, 3: 0, 4: 0, 5: satisfaction_criteria["decision_authority"]},
        6: {1: unresolved_items},
    }


def build_container(records, payload_overrides=None):
    payloads = {kind: encode_cbor(records[kind]) for kind in range(1, 7)}
    payloads.update(payload_overrides or {})
    directory_end = HEADER_SIZE + 6 * ENTRY_SIZE
    offsets = {}
    position = directory_end
    body = bytearray()
    for kind in range(1, 7):
        padding = (-position) % 8
        body.extend(bytes(padding))
        position += padding
        offsets[kind] = position
        body.extend(payloads[kind])
        position += len(payloads[kind])
    file_size = position
    header = struct.pack(
        "<8sHHHHBBBBIQQ24s",
        MAGIC, 0, 1, HEADER_SIZE, ENTRY_SIZE, 1, 3, 0, 0, 6,
        HEADER_SIZE, file_size, bytes(24),
    )
    directory = bytearray()
    for kind in range(1, 7):
        length = len(payloads[kind])
        directory.extend(struct.pack("<HHIQQQIIII", kind, 1, kind, offsets[kind], length, length, 8, 0, 0, 0))
    return header + bytes(directory) + bytes(body)


def read_container(data, profile):
    if len(data) < HEADER_SIZE:
        fail("endem.wire.header.truncated", "END-FMT-001", "/", "structure")
    if data[:8] != MAGIC:
        fail("endem.wire.header.magic", "END-FMT-001", "/", "structure")
    fields = struct.unpack_from("<8sHHHHBBBBIQQ24s", data, 0)
    _, major, minor, header_size, entry_size, byte_order, profile_id, state, flags, count, directory, file_size, reserved = fields
    if (major, minor, header_size, entry_size, byte_order, profile_id, state, flags, count, directory) != (0, 1, 64, 48, 1, 3, 0, 0, 6, 64):
        fail("endem.wire.profile.feature", "END-FMT-010", "/", "profile")
    if file_size != len(data) or reserved != bytes(24):
        fail("endem.wire.header.size", "END-FMT-003", "/", "structure")
    records = {}
    budget = Budget()
    for index in range(6):
        base = 64 + index * 48
        kind, record_flags, record_id, offset, stored, logical, alignment, link, info, entry_reserved = struct.unpack_from("<HHIQQQIIII", data, base)
        if (kind, record_id) != (index + 1, index + 1):
            fail("endem.wire.directory.order", "END-FMT-005", f"/directory/{index}", "structure")
        if (record_flags, logical, alignment, link, info, entry_reserved) != (1, stored, 8, 0, 0, 0):
            fail("endem.wire.profile.feature", "END-FMT-011", f"/directory/{index}", "profile")
        end = offset + stored
        if offset % 8 or end > len(data):
            fail("endem.wire.record.range", "END-FMT-006", "/", "structure")
        decoder = Decoder(data[offset:end], profile, budget)
        value, consumed = decoder.item()
        if consumed != stored or not isinstance(value, dict):
            fail("endem.wire.payload.cbor", "END-FMT-009", "/", "structure")
        records[kind] = value
    return records


def validate_records(records):
    source_expression = exact_map(records[1], range(1, 8), "/source_expression")
    source_id = identifier(source_expression[1], "/source_expression/1")
    identifier(source_expression[2], "/source_expression/2")
    if not isinstance(source_expression[3], str) or MEDIA_TYPE.fullmatch(source_expression[3]) is None:
        fail("endem.semantic.field.media_type", "END-FMT-013", "/source_expression/3")
    if not isinstance(source_expression[4], str) or LANGUAGE_TAG.fullmatch(source_expression[4]) is None:
        fail("endem.semantic.field.language", "END-FMT-013", "/source_expression/4")
    if not isinstance(source_expression[5], str) or not isinstance(source_expression[6], str):
        fail("endem.semantic.field.type", "END-FMT-013", "/source_expression")
    source_range = exact_map(source_expression[7], (1, 2, 3), "/source_expression/7")
    start, length = source_range[2], source_range[3]
    if source_range[1] != 0 or not isinstance(start, int) or not isinstance(length, int) or start < 0 or length < 0 or start + length > len(source_expression[6]):
        fail("endem.source_expression.range_out_of_bounds", "END-SRC-001", "/source_expression/7")

    meaning_projection = exact_map(records[2], (1, 2), "/meaning_projection")
    symbols, relations = meaning_projection[1], meaning_projection[2]
    ordered_unique(symbols, lambda item, index: identifier(exact_map(item, (1, 2, 3), f"/meaning_projection/symbols/{index}")[1], f"/meaning_projection/symbols/{index}/id"), "/meaning_projection/symbols")
    symbol_ids = {item[1] for item in symbols}
    for index, item in enumerate(symbols):
        identifier(item[2], f"/meaning_projection/symbols/{index}/kind")
        if not anchors_source(identifier(item[3], f"/meaning_projection/symbols/{index}/source_ref"), source_id):
            fail("endem.semantic.reference", "END-FMT-014", f"/meaning_projection/symbols/{index}/source_ref")
    ordered_unique(relations, lambda item, index: identifier(exact_map(item, (1, 2, 3, 4), f"/meaning_projection/relations/{index}")[1], f"/meaning_projection/relations/{index}/id"), "/meaning_projection/relations")
    relation_ids = set()
    for index, relation in enumerate(relations):
        relation_ids.add(relation[1])
        identifier(relation[2], f"/meaning_projection/relations/{index}/predicate")
        roles = relation[3]
        ordered_unique(roles, lambda item, role_index: identifier(exact_map(item, (1, 2), f"/meaning_projection/relations/{index}/roles/{role_index}")[1], f"/meaning_projection/relations/{index}/roles/{role_index}/name"), f"/meaning_projection/relations/{index}/roles")
        for role_index, role in enumerate(roles):
            if identifier(role[2], f"/meaning_projection/relations/{index}/roles/{role_index}/symbol") not in symbol_ids:
                fail("endem.semantic.reference", "END-FMT-014", f"/meaning_projection/relations/{index}/roles/{role_index}/symbol")
        projection = exact_map(relation[4], (1, 2), f"/meaning_projection/relations/{index}/projection")
        if projection[1] not in (0, 1):
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"/meaning_projection/relations/{index}/projection")
        identifier(projection[2], f"/meaning_projection/relations/{index}/projection/id")

    situation = exact_map(records[3], (1, 2), "/situation")
    root = identifier(situation[1], "/situation/root")
    situations = situation[2]
    ordered_unique(situations, lambda item, index: identifier(exact_map(item, (1, 2, 3), f"/situation/situations/{index}")[1], f"/situation/situations/{index}/id"), "/situation/situations")
    situation_ids = set()
    for index, situation in enumerate(situations):
        situation_ids.add(situation[1])
        if identifier(situation[2], f"/situation/situations/{index}/relation") not in relation_ids:
            fail("endem.semantic.reference", "END-FMT-014", f"/situation/situations/{index}/relation")
        if situation[3] not in (0, 1):
            fail("endem.situation.polarity", "END-SIT-001", f"/situation/situations/{index}/polarity")
    if root not in situation_ids:
        fail("endem.semantic.reference", "END-FMT-014", "/situation/root")

    goal_direction = exact_map(records[4], (1,), "/goal_direction")
    if goal_direction[1] != 0:
        fail("endem.goal_direction.mode", "END-DIRECTION-001", "/goal_direction/mode")

    satisfaction_criteria = exact_map(records[5], (1, 2, 3, 4, 5), "/satisfaction_criteria")
    if satisfaction_criteria[3] != 0 or satisfaction_criteria[4] != 0:
        fail("endem.satisfaction_criteria.policy", "END-CRITERIA-001", "/satisfaction_criteria")
    identifier(satisfaction_criteria[5], "/satisfaction_criteria/decision_authority")
    ordered_unique(
        satisfaction_criteria[1],
        lambda requirement, index: identifier(
            exact_map(requirement, (1, 2), f"/satisfaction_criteria/required_observations/{index}")[1],
            f"/satisfaction_criteria/required_observations/{index}/relation",
        ),
        "/satisfaction_criteria/required_observations",
    )
    for index, requirement in enumerate(satisfaction_criteria[1]):
        requirement = exact_map(requirement, (1, 2), f"/satisfaction_criteria/required_observations/{index}")
        if identifier(requirement[1], f"/satisfaction_criteria/required_observations/{index}/relation") not in relation_ids:
            fail("endem.semantic.reference", "END-FMT-014", f"/satisfaction_criteria/required_observations/{index}/relation")
        if requirement[2] != 0:
            fail("endem.satisfaction_criteria.match", "END-CRITERIA-001", f"/satisfaction_criteria/required_observations/{index}/match")
    ordered_unique(
        satisfaction_criteria[2],
        lambda evidence, index: encode_cbor(identifier(evidence, f"/satisfaction_criteria/required_evidence/{index}")),
        "/satisfaction_criteria/required_evidence",
    )

    unresolved_meaning = exact_map(records[6], (1,), "/unresolved_meaning")
    ordered_unique(
        unresolved_meaning[1],
        lambda item, index: identifier(
            exact_map(item, (1, 2, 3, 4, 5, 6, 7), f"/unresolved_meaning/items/{index}")[1],
            f"/unresolved_meaning/items/{index}/id",
        ),
        "/unresolved_meaning/items",
    )
    for index, item in enumerate(unresolved_meaning[1]):
        path = f"/unresolved_meaning/items/{index}"
        source_ref = identifier(item[2], f"{path}/source_ref")
        if not anchors_source(source_ref, source_id):
            fail("endem.semantic.reference", "END-FMT-014", f"{path}/source_ref")
        ordered_unique(
            item[3],
            lambda value, value_index: encode_cbor(identifier(value, f"{path}/candidates/{value_index}")),
            f"{path}/candidates",
        )
        if not isinstance(item[4], str):
            fail("endem.semantic.field.type", "END-FMT-013", f"{path}/conflict")
        ordered_unique(
            item[5],
            lambda value, value_index: encode_cbor(identifier(value, f"{path}/impact_scope/{value_index}")),
            f"{path}/impact_scope",
        )
        if not isinstance(item[6], list) or not item[6]:
            fail("endem.unresolved_meaning.unrecorded_projection_choice", "END-UNRESOLVED-001", f"{path}/allowed_resolutions")
        if any(not isinstance(value, int) or isinstance(value, bool) or value not in (0, 1) for value in item[6]):
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"{path}/allowed_resolutions")
        if item[6] != sorted(item[6]) or len(item[6]) != len(set(item[6])):
            fail("endem.semantic.field.order", "END-FMT-013", f"{path}/allowed_resolutions")
        identifier(item[7], f"{path}/decision_authority")
    return {
        "result": "profile-accept",
        "profile": "END-P2",
        "content": "external-prerequisites-not-evaluated",
    }


def mutate_records(records, vector_id):
    records = copy.deepcopy(records)
    if vector_id.startswith("WV-P2-UNRESOLVED-MEANING-"):
        records[6][1] = [{
            1: "unresolved_meaning:audience",
            2: "source:request-001#/range",
            3: sorted(["audience:security", "audience:executive"], key=encode_cbor),
            4: "目标读者尚未确认",
            5: ["rel:produced"],
            6: [0, 1],
            7: "authority:requester",
        }]
    if vector_id == "WV-P2-REJECT-UNKNOWN-FIELD-001":
        records[1][8] = 0
    elif vector_id == "WV-P2-REJECT-DANGLING-REFERENCE-001":
        records[2][2][0][3][0][2] = "sym:missing"
    elif vector_id == "WV-P2-REJECT-SOURCE-RANGE-001":
        records[1][7][3] = 16
    elif vector_id == "WV-P2-UNRESOLVED-MEANING-REJECT-DUPLICATE-RESOLUTION-001":
        records[6][1][0][6] = [0, 0]
    elif vector_id == "WV-P2-UNRESOLVED-MEANING-REJECT-SOURCE-REFERENCE-001":
        records[6][1][0][2] = "source:request-001-copy#/range"
    return records


def build_vector(records, vector_id):
    mutated = mutate_records(records, vector_id)
    if vector_id == "WV-P2-REJECT-NON-MINIMAL-CBOR-001":
        canonical = encode_cbor(mutated[1])
        if canonical[0] != 0xA7:
            raise AssertionError("source_expression root must be a seven-entry map")
        return build_container(mutated, {1: b"\xb8\x07" + canonical[1:]})
    if vector_id == "WV-P2-REJECT-EDGE-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01\x9a\x00\x04\x00\x01"})
    if vector_id == "WV-P2-REJECT-DEPTH-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01" + b"\x81" * 17 + b"\x00"})
    if vector_id == "WV-P2-REJECT-STRING-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01\x7a\x00\x10\x00\x01"})
    if vector_id == "WV-P2-REJECT-TRUNCATED-HEADER-001":
        return build_container(mutated)[:63]
    if vector_id == "WV-P2-REJECT-DIRECTORY-ORDER-001":
        data = bytearray(build_container(mutated))
        first = bytes(data[HEADER_SIZE:HEADER_SIZE + ENTRY_SIZE])
        second = bytes(data[HEADER_SIZE + ENTRY_SIZE:HEADER_SIZE + 2 * ENTRY_SIZE])
        data[HEADER_SIZE:HEADER_SIZE + ENTRY_SIZE] = second
        data[HEADER_SIZE + ENTRY_SIZE:HEADER_SIZE + 2 * ENTRY_SIZE] = first
        return bytes(data)
    return build_container(mutated)


def load_hex(path):
    return bytes.fromhex(path.read_text())


def main():
    errors = []
    catalog = ERROR_CATALOG_PATH.read_text()
    profile = json.loads(PROFILE_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    source = json.loads((ROOT / manifest["semantic_source"]).read_text())["input"]
    negative_source = json.loads((ROOT / manifest["negative_semantic_source"]).read_text())["input"]
    if profile.get("profile_id") != 3 or profile.get("name") != "END-P2":
        errors.append("END-P2 must use profile_id 3")
    if profile.get("artifact_role") != "source-bearing-formation" or profile.get("publishable") is not False:
        errors.append("END-P2 must remain a non-publishable source-bearing formation Profile")
    expected_records = {
        str(kind): {"name": name, "schema": name, "required_keys": keys}
        for kind, name, keys in (
            (1, "source_expression", [1, 2, 3, 4, 5, 6, 7]),
            (2, "meaning_projection", [1, 2]),
            (3, "situation", [1, 2]),
            (4, "goal_direction", [1]),
            (5, "satisfaction_criteria", [1, 2, 3, 4, 5]),
            (6, "unresolved_meaning", [1]),
        )
    }
    if profile.get("records") != expected_records:
        errors.append("END-P2 record roots and required keys drifted")
    expected_enums = {
        "range_unit": {"0": "unicode-scalar"},
        "projection_kind": {"0": "rule", "1": "named-authority"},
        "polarity": {"0": "positive", "1": "negative"},
        "goal_direction_mode": {"0": "reach"},
        "relation_match": {"0": "same-roles"},
        "missing_policy": {"0": "undetermined"},
        "error_policy": {"0": "fault"},
    }
    if profile.get("enums") != expected_enums:
        errors.append("END-P2 enum registry drifted")
    if profile.get("limits", {}).get("max_record_count") != 6:
        errors.append("END-P2 must allow exactly six records")
    if profile.get("limits", {}).get("max_nesting_depth") != 16:
        errors.append("END-P2 nesting limit must remain 16 until measured again")
    base_records = source_to_records(source)
    negative_records = source_to_records(negative_source)
    seen = set()
    accept_count = 0
    reject_count = 0
    for vector in manifest.get("vectors", []):
        vector_id = vector["id"]
        seen.add(vector_id)
        source_records = negative_records if vector_id == "WV-P2-NEGATIVE-PROFILE-ACCEPT-001" else base_records
        expected_bytes = build_vector(source_records, vector_id)
        actual_bytes = load_hex(ROOT / vector["hex"])
        if actual_bytes != expected_bytes:
            errors.append(f"{vector_id}: checked-in bytes differ from deterministic source mapping")
            continue
        try:
            actual = validate_records(read_container(actual_bytes, profile))
        except P2Error as exc:
            actual = exc.result
        expected = vector["expect"]
        if expected.get("code") and f"`{expected['code']}`" not in catalog:
            errors.append(f"{vector_id}: diagnostic catalog missing {expected['code']}")
        if actual != expected:
            errors.append(f"{vector_id}: expected {expected}, got {actual}")
        if expected["result"] == "profile-accept":
            accept_count += 1
        else:
            reject_count += 1
    if len(seen) != len(manifest.get("vectors", [])):
        errors.append("END-P2 vector IDs must be unique")
    if accept_count != 3 or reject_count != 11:
        errors.append("END-P2 requires three Profile accepts and eleven deterministic rejects")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: END-P2 encoded and decoded 14 wire vectors (3 Profile accepts with external content prerequisites not evaluated, 11 deterministic rejects)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
