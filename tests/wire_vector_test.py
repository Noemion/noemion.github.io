from pathlib import Path
import json
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "vectors" / "wire" / "manifest.json"
PROFILE_PATH = ROOT / "spec" / "profiles" / "end-p0.json"
REGISTRY_PATH = ROOT / "spec" / "registry.json"
ERROR_CATALOG_PATH = ROOT / "spec" / "diagnostic-catalog.md"

MAGIC = b"ENDEM\x00\r\n"
HEADER_SIZE = 64
ENTRY_SIZE = 48
U64_MAX = (1 << 64) - 1
KINDS = frozenset(range(1, 7))
EXPECTED_LIMITS = {
    "max_artifact_bytes": 16777216,
    "max_record_count": 64,
    "max_graph_nodes": 65536,
    "max_graph_edges": 262144,
    "max_nesting_depth": 64,
    "max_string_bytes": 1048576,
    "max_decompressed_bytes": 16777216,
    "max_total_allocation_bytes": 67108864,
}

ERROR_CLAUSES = {
    "endem.wire.header.truncated": ("END-FMT-001", "structure"),
    "endem.wire.header.magic": ("END-FMT-001", "structure"),
    "endem.wire.header.version": ("END-FMT-001", "structure"),
    "endem.wire.header.layout": ("END-FMT-002", "structure"),
    "endem.wire.header.size": ("END-FMT-003", "structure"),
    "endem.wire.header.reserved": ("END-FMT-003", "structure"),
    "endem.wire.directory.out_of_bounds": ("END-FMT-004", "structure"),
    "endem.wire.directory.order": ("END-FMT-005", "structure"),
    "endem.wire.record.id": ("END-FMT-005", "structure"),
    "endem.wire.record.range": ("END-FMT-006", "structure"),
    "endem.wire.record.alignment": ("END-FMT-006", "structure"),
    "endem.wire.record.overlap": ("END-FMT-006", "structure"),
    "endem.wire.record.padding": ("END-FMT-006", "structure"),
    "endem.wire.record.unknown_kind": ("END-FMT-007", "profile"),
    "endem.wire.record.flags": ("END-FMT-007", "profile"),
    "endem.wire.facet.cardinality": ("END-FMT-008", "profile"),
    "endem.wire.payload.cbor": ("END-FMT-009", "structure"),
    "endem.wire.payload.not_map": ("END-FMT-009", "structure"),
    "endem.wire.profile.unknown": ("END-FMT-010", "profile"),
    "endem.wire.profile.limit": ("END-FMT-010", "profile"),
    "endem.wire.profile.feature": ("END-FMT-011", "profile"),
}


class WireError(Exception):
    def __init__(self, code, start=None, end=None):
        super().__init__(code)
        self.code = code
        self.clause, self.layer = ERROR_CLAUSES[code]
        self.byte_range = None if start is None else [start, end]


def fail(code, start=None, end=None):
    raise WireError(code, start, end)


def checked_add(left, right, code):
    value = left + right
    if left < 0 or right < 0 or value > U64_MAX:
        fail(code)
    return value


def checked_mul(left, right, code):
    value = left * right
    if left < 0 or right < 0 or value > U64_MAX:
        fail(code)
    return value


class CborReader:
    def __init__(self, data, profile, budget):
        self.data = data
        self.profile = profile
        self.budget = budget

    def take(self, position, length):
        end = position + length
        if length < 0 or end > len(self.data):
            fail("endem.wire.payload.cbor")
        return self.data[position:end], end

    def argument(self, position, additional):
        if additional < 24:
            return additional, position
        widths = {24: 1, 25: 2, 26: 4, 27: 8}
        width = widths.get(additional)
        if width is None:
            fail("endem.wire.payload.cbor")
        raw, position = self.take(position, width)
        value = int.from_bytes(raw, "big")
        minimum = {1: 24, 2: 256, 4: 65536, 8: 4294967296}[width]
        if value < minimum:
            fail("endem.wire.payload.cbor")
        return value, position

    def item(self, position=0, depth=0):
        self.budget["items"] += 1
        if self.budget["items"] > self.profile["max_graph_nodes"]:
            fail("endem.wire.profile.limit")
        if depth > self.profile["max_nesting_depth"]:
            fail("endem.wire.profile.limit")
        initial_raw, position = self.take(position, 1)
        initial = initial_raw[0]
        major = initial >> 5
        additional = initial & 0x1F

        if major in (0, 1):
            value, position = self.argument(position, additional)
            return ("uint" if major == 0 else "nint", value), position

        if major in (2, 3):
            length, position = self.argument(position, additional)
            if length > self.profile["max_string_bytes"]:
                fail("endem.wire.profile.limit")
            raw, position = self.take(position, length)
            self.budget["allocated"] += length
            if self.budget["allocated"] > self.profile["max_total_allocation_bytes"]:
                fail("endem.wire.profile.limit")
            if major == 3:
                try:
                    raw.decode("utf-8")
                except UnicodeDecodeError:
                    fail("endem.wire.payload.cbor")
            return ("bytes" if major == 2 else "text", raw), position

        if major in (4, 5):
            length, position = self.argument(position, additional)
            if length > self.profile["max_graph_edges"]:
                fail("endem.wire.profile.limit")
            self.budget["edges"] += length
            if self.budget["edges"] > self.profile["max_graph_edges"]:
                fail("endem.wire.profile.limit")
            if major == 4:
                values = []
                for _ in range(length):
                    value, position = self.item(position, depth + 1)
                    values.append(value)
                return ("array", values), position

            pairs = []
            prior_key_bytes = None
            for _ in range(length):
                key_start = position
                key, position = self.item(position, depth + 1)
                if key[0] != "uint":
                    fail("endem.wire.payload.cbor")
                key_bytes = self.data[key_start:position]
                if prior_key_bytes is not None and key_bytes <= prior_key_bytes:
                    fail("endem.wire.payload.cbor")
                prior_key_bytes = key_bytes
                value, position = self.item(position, depth + 1)
                pairs.append((key[1], value))
            return ("map", pairs), position

        if major == 7 and additional in (20, 21, 22):
            return ("simple", additional), position

        fail("endem.wire.payload.cbor")


def validate_payload(payload, profile, budget, file_offset):
    reader = CborReader(payload, profile, budget)
    value, end = reader.item()
    if end != len(payload):
        fail("endem.wire.payload.cbor")
    if value[0] != "map":
        fail("endem.wire.payload.not_map", file_offset, file_offset + len(payload))


def validate_wire(data, profile_document):
    limits = profile_document["limits"]
    if len(data) < HEADER_SIZE:
        fail("endem.wire.header.truncated", 0, len(data))
    if data[:8] != MAGIC:
        fail("endem.wire.header.magic", 0, 8)

    (
        _, major, minor, header_size, entry_size, byte_order, profile_id,
        state, flags, record_count, directory_offset, file_size, reserved,
    ) = struct.unpack_from("<8sHHHHBBBBIQQ24s", data, 0)

    if (major, minor) != (0, 1):
        fail("endem.wire.header.version", 8, 12)
    if (header_size, entry_size, byte_order) != (HEADER_SIZE, ENTRY_SIZE, 1):
        fail("endem.wire.header.layout", 12, 17)
    if file_size != len(data):
        fail("endem.wire.header.size", 32, 40)
    if flags != 0 or reserved != bytes(24):
        fail("endem.wire.header.reserved", 19, 64)

    directory_bytes = checked_mul(record_count, entry_size, "endem.wire.directory.out_of_bounds")
    directory_end = checked_add(directory_offset, directory_bytes, "endem.wire.directory.out_of_bounds")
    if directory_offset != HEADER_SIZE or directory_end > len(data):
        fail("endem.wire.directory.out_of_bounds", 20, 32)

    if profile_id != profile_document["profile_id"]:
        fail("endem.wire.profile.unknown", 17, 18)
    if len(data) > limits["max_artifact_bytes"] or record_count > limits["max_record_count"]:
        fail("endem.wire.profile.limit")
    if state not in profile_document["allowed_states"]:
        fail("endem.wire.profile.feature", 18, 19)

    entries = []
    seen_ids = set()
    prior_order = None
    for index in range(record_count):
        entry_offset = directory_offset + index * entry_size
        entry = struct.unpack_from("<HHIQQQIIII", data, entry_offset)
        kind, record_flags, record_id, offset, stored, logical, alignment, link, info, entry_reserved = entry
        order = (kind, record_id)
        if prior_order is not None and order <= prior_order:
            fail("endem.wire.directory.order", entry_offset, entry_offset + 8)
        prior_order = order
        if record_id == 0 or record_id in seen_ids:
            fail("endem.wire.record.id", entry_offset + 4, entry_offset + 8)
        seen_ids.add(record_id)
        if record_flags not in profile_document["allowed_record_flags"]:
            fail("endem.wire.record.flags", entry_offset + 2, entry_offset + 4)
        if kind not in KINDS:
            fail("endem.wire.record.unknown_kind", entry_offset, entry_offset + 2)
        if alignment != 8 or offset % alignment:
            fail("endem.wire.record.alignment", entry_offset + 8, entry_offset + 36)
        end = checked_add(offset, stored, "endem.wire.record.range")
        if offset < directory_end or end > len(data):
            fail("endem.wire.record.range", entry_offset + 8, entry_offset + 32)
        if stored != logical or link != 0 or info != 0 or entry_reserved != 0:
            fail("endem.wire.profile.feature", entry_offset + 16, entry_offset + 48)
        entries.append((kind, record_id, offset, end))

    if [entry[0] for entry in entries] != list(profile_document["required_record_kinds"]):
        fail("endem.wire.facet.cardinality")

    by_range = sorted(entries, key=lambda entry: (entry[2], entry[3]))
    previous_end = directory_end
    for _, _, start, end in by_range:
        if start < previous_end:
            fail("endem.wire.record.overlap", start, end)
        if any(data[previous_end:start]):
            fail("endem.wire.record.padding", previous_end, start)
        previous_end = end
    if previous_end != len(data):
        fail("endem.wire.record.padding", previous_end, len(data))

    budget = {"items": 0, "edges": 0, "allocated": 0}
    for _, _, start, end in entries:
        validate_payload(data[start:end], limits, budget, start)
    return {"result": "structural-accept", "semantic": "not-evaluated"}


def load_hex(path):
    try:
        return bytes.fromhex(path.read_text())
    except (OSError, ValueError) as exc:
        raise AssertionError(f"{path.relative_to(ROOT)}: invalid hex vector: {exc}") from exc


def main():
    errors = []
    manifest = json.loads(MANIFEST_PATH.read_text())
    profile = json.loads(PROFILE_PATH.read_text())
    registry = json.loads(REGISTRY_PATH.read_text())
    clause_ids = {clause["id"] for clause in registry.get("clauses", [])}
    error_catalog = ERROR_CATALOG_PATH.read_text()
    if manifest.get("format") != {"id": "END-FMT", "version": "0.1.0-draft"}:
        errors.append("wire manifest must pin END-FMT 0.1.0-draft")
    if manifest.get("profile") != {"id": 1, "name": "END-P0", "version": "0.1.0-draft"}:
        errors.append("wire manifest must pin END-P0 0.1.0-draft")
    if profile.get("limits") != EXPECTED_LIMITS:
        errors.append("END-P0 must provide the exact eight finite experimental limits")
    if profile.get("required_record_kinds") != [1, 2, 3, 4, 5, 6]:
        errors.append("END-P0 must require the six semantic record kinds in order")
    if profile.get("allowed_states") != [0] or profile.get("allowed_record_flags") != [1]:
        errors.append("END-P0 must allow only formed and critical records")
    if profile.get("compression") is not False or profile.get("encryption") is not False:
        errors.append("END-P0 must forbid compression and encryption")

    vector_ids = []
    manifest_hex_paths = set()
    accept_count = 0
    reject_count = 0
    for vector in manifest.get("vectors", []):
        vector_id = vector.get("id")
        vector_ids.append(vector_id)
        path = ROOT / vector.get("hex", "")
        manifest_hex_paths.add(path)
        if not path.is_file():
            errors.append(f"{vector_id}: missing hex file")
            continue
        data = load_hex(path)
        expected = vector.get("expect", {})
        expected_clauses = expected.get("clauses", [])
        if expected.get("clause"):
            expected_clauses = [expected["clause"]]
        for clause_id in expected_clauses:
            if clause_id not in clause_ids:
                errors.append(f"{vector_id}: unknown clause {clause_id}")
        try:
            actual = validate_wire(data, profile)
        except WireError as exc:
            actual = {
                "result": "reject",
                "code": exc.code,
                "clause": exc.clause,
                "layer": exc.layer,
                "byte_range": exc.byte_range,
            }

        if expected.get("result") == "structural-accept":
            accept_count += 1
            comparable = {key: expected[key] for key in ("result", "semantic")}
            if actual != comparable:
                errors.append(f"{vector_id}: expected {comparable}, got {actual}")
        elif expected.get("result") == "reject":
            reject_count += 1
            comparable = {key: expected.get(key) for key in ("result", "code", "clause", "layer", "byte_range")}
            if actual != comparable:
                errors.append(f"{vector_id}: expected {comparable}, got {actual}")
        else:
            errors.append(f"{vector_id}: invalid expected result")

    if len(vector_ids) != len(set(vector_ids)):
        errors.append("wire vector IDs must be unique")
    actual_hex_paths = set((ROOT / "vectors" / "wire").glob("*.hex"))
    if manifest_hex_paths != actual_hex_paths:
        errors.append(
            "wire manifest mismatch: "
            f"unregistered={sorted(str(path.relative_to(ROOT)) for path in actual_hex_paths - manifest_hex_paths)}, "
            f"missing={sorted(str(path.relative_to(ROOT)) for path in manifest_hex_paths - actual_hex_paths)}"
        )
    for code in ERROR_CLAUSES:
        if f"`{code}`" not in error_catalog:
            errors.append(f"diagnostic catalog missing {code}")
    if accept_count < 1 or reject_count < 5:
        errors.append("wire vectors require at least one structural accept and five reject cases")

    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PASS: END-FMT 0.1.0-draft decoded {accept_count + reject_count} byte vectors "
        f"({accept_count} structural accept, {reject_count} deterministic rejects)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
