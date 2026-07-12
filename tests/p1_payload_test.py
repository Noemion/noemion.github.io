from pathlib import Path
import copy
import json
import re
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "spec" / "profiles" / "end-p1.json"
SOURCE_PATH = ROOT / "vectors" / "semantic" / "minimal-valid.json"
MANIFEST_PATH = ROOT / "vectors" / "wire" / "p1" / "manifest.json"
ERROR_CATALOG_PATH = ROOT / "spec" / "endem-errors.md"
MAGIC = b"ENDEM\x00\r\n"
HEADER_SIZE = 64
ENTRY_SIZE = 48
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9._:/#-]{0,254}$")
MEDIA_TYPE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$")
LANGUAGE_TAG = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")


class P1Error(Exception):
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
    raise P1Error(code, clause, path, layer)


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
            raise ValueError("P1 CBOR map keys must be unsigned integers")
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
    rhem = model["rhem"]
    semion = model["semion"]
    skena = model["skena"]
    telis = model["telis"]
    krin = model["krin"]
    projection_kind = {"rule": 0, "named-authority": 1}
    polarity = {"positive": 0, "negative": 1}

    symbols = [
        {1: item["id"], 2: item["kind"], 3: item["source_ref"]}
        for item in sorted(semion["symbols"], key=lambda item: item["id"])
    ]
    relations = []
    for item in sorted(semion["relations"], key=lambda item: item["id"]):
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
        for item in sorted(skena["situations"], key=lambda item: item["id"])
    ]
    phain = [
        {1: item["relation"], 2: 0}
        for item in sorted(krin["required_phain"], key=lambda item: item["relation"])
    ]
    tekmor = sorted(krin["required_tekmor"], key=encode_cbor)
    apor_items = []
    for item in sorted(model["apor"], key=lambda value: value["id"]):
        apor_items.append({
            1: item["id"],
            2: item["source_ref"],
            3: sorted(item["candidates"], key=encode_cbor),
            4: item["conflict"],
            5: sorted(item["impact_scope"], key=encode_cbor),
            6: sorted(projection_kind[value] for value in item["allowed_resolutions"]),
            7: item["decision_authority"],
        })
    return {
        1: {1: rhem["source_id"], 2: rhem["subject"], 3: rhem["media_type"], 4: rhem["language"], 5: rhem["version"], 6: rhem["content"], 7: {1: 0, 2: rhem["range"]["start"], 3: rhem["range"]["length"]}},
        2: {1: symbols, 2: relations},
        3: {1: skena["roots"][0], 2: situations},
        4: {1: 0 if telis["mode"] == "kine" else 1},
        5: {1: phain, 2: tekmor, 3: 0, 4: 0, 5: krin["decision_authority"]},
        6: {1: apor_items},
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
        MAGIC, 0, 1, HEADER_SIZE, ENTRY_SIZE, 1, 2, 0, 0, 6,
        HEADER_SIZE, file_size, bytes(24),
    )
    directory = bytearray()
    for kind in range(1, 7):
        length = len(payloads[kind])
        directory.extend(struct.pack("<HHIQQQIIII", kind, 1, kind, offsets[kind], length, length, 8, 0, 0, 0))
    return header + bytes(directory) + bytes(body)


def read_container(data, profile):
    if len(data) < HEADER_SIZE or data[:8] != MAGIC:
        fail("endem.wire.header.magic", "END-FMT-001", "/", "structure")
    fields = struct.unpack_from("<8sHHHHBBBBIQQ24s", data, 0)
    _, major, minor, header_size, entry_size, byte_order, profile_id, state, flags, count, directory, file_size, reserved = fields
    if (major, minor, header_size, entry_size, byte_order, profile_id, state, flags, count, directory) != (0, 1, 64, 48, 1, 2, 0, 0, 6, 64):
        fail("endem.wire.profile.feature", "END-FMT-010", "/", "profile")
    if file_size != len(data) or reserved != bytes(24):
        fail("endem.wire.header.size", "END-FMT-003", "/", "structure")
    records = {}
    budget = Budget()
    for index in range(6):
        base = 64 + index * 48
        kind, record_flags, record_id, offset, stored, logical, alignment, link, info, entry_reserved = struct.unpack_from("<HHIQQQIIII", data, base)
        if (kind, record_flags, record_id, logical, alignment, link, info, entry_reserved) != (index + 1, 1, index + 1, stored, 8, 0, 0, 0):
            fail("endem.wire.profile.feature", "END-FMT-010", "/", "profile")
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
    rhem = exact_map(records[1], range(1, 8), "/rhem")
    source_id = identifier(rhem[1], "/rhem/1")
    identifier(rhem[2], "/rhem/2")
    if not isinstance(rhem[3], str) or MEDIA_TYPE.fullmatch(rhem[3]) is None:
        fail("endem.semantic.field.media_type", "END-FMT-013", "/rhem/3")
    if not isinstance(rhem[4], str) or LANGUAGE_TAG.fullmatch(rhem[4]) is None:
        fail("endem.semantic.field.language", "END-FMT-013", "/rhem/4")
    if not isinstance(rhem[5], str) or not isinstance(rhem[6], str):
        fail("endem.semantic.field.type", "END-FMT-013", "/rhem")
    source_range = exact_map(rhem[7], (1, 2, 3), "/rhem/7")
    start, length = source_range[2], source_range[3]
    if source_range[1] != 0 or not isinstance(start, int) or not isinstance(length, int) or start < 0 or length < 0 or start + length > len(rhem[6]):
        fail("endem.rhem.range_out_of_bounds", "END-SRC-001", "/rhem/7")

    semion = exact_map(records[2], (1, 2), "/semion")
    symbols, relations = semion[1], semion[2]
    ordered_unique(symbols, lambda item, index: identifier(exact_map(item, (1, 2, 3), f"/semion/symbols/{index}")[1], f"/semion/symbols/{index}/id"), "/semion/symbols")
    symbol_ids = {item[1] for item in symbols}
    for index, item in enumerate(symbols):
        identifier(item[2], f"/semion/symbols/{index}/kind")
        if not anchors_source(identifier(item[3], f"/semion/symbols/{index}/source_ref"), source_id):
            fail("endem.semantic.reference", "END-FMT-014", f"/semion/symbols/{index}/source_ref")
    ordered_unique(relations, lambda item, index: identifier(exact_map(item, (1, 2, 3, 4), f"/semion/relations/{index}")[1], f"/semion/relations/{index}/id"), "/semion/relations")
    relation_ids = set()
    for index, relation in enumerate(relations):
        relation_ids.add(relation[1])
        identifier(relation[2], f"/semion/relations/{index}/predicate")
        roles = relation[3]
        ordered_unique(roles, lambda item, role_index: identifier(exact_map(item, (1, 2), f"/semion/relations/{index}/roles/{role_index}")[1], f"/semion/relations/{index}/roles/{role_index}/name"), f"/semion/relations/{index}/roles")
        for role_index, role in enumerate(roles):
            if identifier(role[2], f"/semion/relations/{index}/roles/{role_index}/symbol") not in symbol_ids:
                fail("endem.semantic.reference", "END-FMT-014", f"/semion/relations/{index}/roles/{role_index}/symbol")
        projection = exact_map(relation[4], (1, 2), f"/semion/relations/{index}/projection")
        if projection[1] not in (0, 1):
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"/semion/relations/{index}/projection")
        identifier(projection[2], f"/semion/relations/{index}/projection/id")

    skena = exact_map(records[3], (1, 2), "/skena")
    root = identifier(skena[1], "/skena/root")
    situations = skena[2]
    ordered_unique(situations, lambda item, index: identifier(exact_map(item, (1, 2, 3), f"/skena/situations/{index}")[1], f"/skena/situations/{index}/id"), "/skena/situations")
    situation_ids = set()
    for index, situation in enumerate(situations):
        situation_ids.add(situation[1])
        if identifier(situation[2], f"/skena/situations/{index}/relation") not in relation_ids:
            fail("endem.semantic.reference", "END-FMT-014", f"/skena/situations/{index}/relation")
        if situation[3] not in (0, 1):
            fail("endem.skena.polarity", "END-SIT-001", f"/skena/situations/{index}/polarity")
    if root not in situation_ids:
        fail("endem.semantic.reference", "END-FMT-014", "/skena/root")

    telis = exact_map(records[4], (1,), "/telis")
    if telis[1] != 0:
        fail("endem.telis.mode", "END-TEL-001", "/telis/mode")

    krin = exact_map(records[5], (1, 2, 3, 4, 5), "/krin")
    if krin[3] != 0 or krin[4] != 0:
        fail("endem.krin.policy", "END-KRN-001", "/krin")
    identifier(krin[5], "/krin/decision_authority")
    ordered_unique(
        krin[1],
        lambda requirement, index: identifier(
            exact_map(requirement, (1, 2), f"/krin/required_phain/{index}")[1],
            f"/krin/required_phain/{index}/relation",
        ),
        "/krin/required_phain",
    )
    for index, requirement in enumerate(krin[1]):
        requirement = exact_map(requirement, (1, 2), f"/krin/required_phain/{index}")
        if identifier(requirement[1], f"/krin/required_phain/{index}/relation") not in relation_ids:
            fail("endem.semantic.reference", "END-FMT-014", f"/krin/required_phain/{index}/relation")
        if requirement[2] != 0:
            fail("endem.krin.match", "END-KRN-001", f"/krin/required_phain/{index}/match")
    ordered_unique(
        krin[2],
        lambda evidence, index: encode_cbor(identifier(evidence, f"/krin/required_tekmor/{index}")),
        "/krin/required_tekmor",
    )

    apor = exact_map(records[6], (1,), "/apor")
    ordered_unique(
        apor[1],
        lambda item, index: identifier(
            exact_map(item, (1, 2, 3, 4, 5, 6, 7), f"/apor/items/{index}")[1],
            f"/apor/items/{index}/id",
        ),
        "/apor/items",
    )
    for index, item in enumerate(apor[1]):
        path = f"/apor/items/{index}"
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
            fail("endem.apor.unrecorded_projection_choice", "END-APR-001", f"{path}/allowed_resolutions")
        if any(not isinstance(value, int) or isinstance(value, bool) or value not in (0, 1) for value in item[6]):
            fail("endem.projection.authority_untrusted", "END-AUT-001", f"{path}/allowed_resolutions")
        if item[6] != sorted(item[6]) or len(item[6]) != len(set(item[6])):
            fail("endem.semantic.field.order", "END-FMT-013", f"{path}/allowed_resolutions")
        identifier(item[7], f"{path}/decision_authority")
    return {"result": "semantic-accept", "profile": "END-P1"}


def mutate_records(records, vector_id):
    records = copy.deepcopy(records)
    if vector_id.startswith("WV-P1-APOR-"):
        records[6][1] = [{
            1: "apor:audience",
            2: "source:request-001#/range",
            3: sorted(["audience:security", "audience:executive"], key=encode_cbor),
            4: "目标读者尚未确认",
            5: ["rel:produced"],
            6: [0, 1],
            7: "authority:requester",
        }]
    if vector_id == "WV-P1-REJECT-UNKNOWN-FIELD-001":
        records[1][8] = 0
    elif vector_id == "WV-P1-REJECT-DANGLING-REFERENCE-001":
        records[2][2][0][3][0][2] = "sym:missing"
    elif vector_id == "WV-P1-REJECT-SOURCE-RANGE-001":
        records[1][7][3] = 16
    elif vector_id == "WV-P1-APOR-REJECT-DUPLICATE-RESOLUTION-001":
        records[6][1][0][6] = [0, 0]
    elif vector_id == "WV-P1-APOR-REJECT-SOURCE-REFERENCE-001":
        records[6][1][0][2] = "source:request-001-copy#/range"
    return records


def build_vector(records, vector_id):
    mutated = mutate_records(records, vector_id)
    if vector_id == "WV-P1-REJECT-NON-MINIMAL-CBOR-001":
        canonical = encode_cbor(mutated[1])
        if canonical[0] != 0xA7:
            raise AssertionError("rhem root must be a seven-entry map")
        return build_container(mutated, {1: b"\xb8\x07" + canonical[1:]})
    if vector_id == "WV-P1-REJECT-EDGE-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01\x9a\x00\x04\x00\x01"})
    if vector_id == "WV-P1-REJECT-DEPTH-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01" + b"\x81" * 17 + b"\x00"})
    if vector_id == "WV-P1-REJECT-STRING-LIMIT-001":
        return build_container(mutated, {1: b"\xa1\x01\x7a\x00\x10\x00\x01"})
    return build_container(mutated)


def load_hex(path):
    return bytes.fromhex(path.read_text())


def main():
    errors = []
    catalog = ERROR_CATALOG_PATH.read_text()
    profile = json.loads(PROFILE_PATH.read_text())
    source = json.loads(SOURCE_PATH.read_text())["input"]
    manifest = json.loads(MANIFEST_PATH.read_text())
    if profile.get("profile_id") != 2 or profile.get("name") != "END-P1":
        errors.append("END-P1 must use profile_id 2")
    expected_records = {
        str(kind): {"name": name, "schema": name, "required_keys": keys}
        for kind, name, keys in (
            (1, "rhem", [1, 2, 3, 4, 5, 6, 7]),
            (2, "semion", [1, 2]),
            (3, "skena", [1, 2]),
            (4, "telis", [1]),
            (5, "krin", [1, 2, 3, 4, 5]),
            (6, "apor", [1]),
        )
    }
    if profile.get("records") != expected_records:
        errors.append("END-P1 record roots and required keys drifted")
    expected_enums = {
        "range_unit": {"0": "unicode-scalar"},
        "projection_kind": {"0": "rule", "1": "named-authority"},
        "polarity": {"0": "positive", "1": "negative"},
        "telis_mode": {"0": "kine"},
        "relation_match": {"0": "same-roles"},
        "missing_policy": {"0": "agno"},
        "error_policy": {"0": "fault"},
    }
    if profile.get("enums") != expected_enums:
        errors.append("END-P1 enum registry drifted")
    if profile.get("limits", {}).get("max_record_count") != 6:
        errors.append("END-P1 must allow exactly six records")
    if profile.get("limits", {}).get("max_nesting_depth") != 16:
        errors.append("END-P1 nesting limit must remain 16 until measured again")
    base_records = source_to_records(source)
    seen = set()
    accept_count = 0
    reject_count = 0
    for vector in manifest.get("vectors", []):
        vector_id = vector["id"]
        seen.add(vector_id)
        expected_bytes = build_vector(base_records, vector_id)
        actual_bytes = load_hex(ROOT / vector["hex"])
        if actual_bytes != expected_bytes:
            errors.append(f"{vector_id}: checked-in bytes differ from deterministic source mapping")
            continue
        try:
            actual = validate_records(read_container(actual_bytes, profile))
        except P1Error as exc:
            actual = exc.result
        expected = vector["expect"]
        if expected.get("code") and f"`{expected['code']}`" not in catalog:
            errors.append(f"{vector_id}: diagnostic catalog missing {expected['code']}")
        if actual != expected:
            errors.append(f"{vector_id}: expected {expected}, got {actual}")
        if expected["result"] == "semantic-accept":
            accept_count += 1
        else:
            reject_count += 1
    if len(seen) != len(manifest.get("vectors", [])):
        errors.append("END-P1 vector IDs must be unique")
    if accept_count != 2 or reject_count != 9:
        errors.append("END-P1 requires two semantic accepts and nine deterministic rejects")
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: END-P1 encoded and decoded 11 wire vectors (2 semantic accepts, 9 deterministic rejects)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
