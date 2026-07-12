from pathlib import Path
import copy
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "vectors" / "source" / "minimal.ends"
APOR_SOURCE_PATH = ROOT / "vectors" / "source" / "with-apor.ends"
SEMANTIC_PATH = ROOT / "vectors" / "semantic" / "minimal-valid.json"
SPEC_PATH = ROOT / "spec" / "endem-source-manifest.md"


class SourceError(Exception):
    pass


def unescape(value):
    output = []
    index = 0
    escapes = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\"}
    while index < len(value):
        if value[index] != "\\":
            output.append(value[index])
            index += 1
            continue
        index += 1
        if index >= len(value) or value[index] not in escapes:
            raise SourceError("invalid escape")
        output.append(escapes[value[index]])
        index += 1
    return "".join(output)


def exact(parts, count):
    if len(parts) != count:
        raise SourceError("wrong directive arity")


def csv(value):
    return [] if value == "" else value.split(",")


def parse(source):
    singletons = {}
    symbols = []
    relations = []
    situations = []
    phain = []
    tekmor = []
    apor = []
    for raw in source.splitlines():
        if raw == "" or raw.startswith("#"):
            continue
        parts = [unescape(value) for value in raw.split("\t")]
        directive = parts[0]
        if directive == "rhem":
            exact(parts, 9)
            value = {
                "source_id": parts[1], "subject": parts[2],
                "media_type": parts[3], "language": parts[4],
                "version": parts[5], "content": parts[6],
                "range": {"unit": "unicode-scalar", "start": int(parts[7]), "length": int(parts[8])},
            }
            set_once(singletons, directive, value)
        elif directive == "symbol":
            exact(parts, 4)
            symbols.append({"id": parts[1], "kind": parts[2], "source_ref": parts[3]})
        elif directive == "relation":
            if len(parts) < 6:
                raise SourceError("relation requires a role")
            roles = []
            for value in parts[5:]:
                if "=" not in value:
                    raise SourceError("invalid role")
                name, symbol = value.split("=", 1)
                roles.append({"name": name, "symbol": symbol})
            relations.append({
                "id": parts[1], "predicate": parts[2], "roles": roles,
                "projection": {"kind": parts[3], "id": parts[4]},
            })
        elif directive == "situation":
            exact(parts, 4)
            situations.append({"id": parts[1], "relation": parts[2], "polarity": parts[3]})
        elif directive in ("root", "telis"):
            exact(parts, 2)
            set_once(singletons, directive, parts[1])
        elif directive == "phain":
            exact(parts, 3)
            phain.append({"relation": parts[1], "match": parts[2]})
        elif directive == "tekmor":
            exact(parts, 2)
            tekmor.append(parts[1])
        elif directive == "krin":
            exact(parts, 4)
            set_once(singletons, directive, {
                "on_missing_observation": parts[1],
                "on_evaluation_error": parts[2],
                "decision_authority": parts[3],
            })
        elif directive == "apor":
            exact(parts, 8)
            apor.append({
                "id": parts[1], "source_ref": parts[2], "conflict": parts[3],
                "decision_authority": parts[4], "candidates": csv(parts[5]),
                "impact_scope": csv(parts[6]), "allowed_resolutions": csv(parts[7]),
            })
        else:
            raise SourceError("unknown directive")
    for required in ("rhem", "root", "telis", "krin"):
        if required not in singletons:
            raise SourceError(f"missing {required}")
    return {
        "rhem": singletons["rhem"],
        "semion": {"symbols": symbols, "relations": relations},
        "skena": {"roots": [singletons["root"]], "situations": situations},
        "telis": {"mode": singletons["telis"]},
        "krin": {"required_phain": phain, "required_tekmor": tekmor, **singletons["krin"]},
        "apor": apor,
    }


def set_once(singletons, key, value):
    if key in singletons:
        raise SourceError(f"duplicate {key}")
    singletons[key] = value


def normalize(model):
    model = copy.deepcopy(model)
    model["semion"]["symbols"].sort(key=lambda item: item["id"])
    model["semion"]["relations"].sort(key=lambda item: item["id"])
    for relation in model["semion"]["relations"]:
        relation["roles"].sort(key=lambda item: item["name"])
    model["skena"]["situations"].sort(key=lambda item: item["id"])
    model["krin"]["required_phain"].sort(key=lambda item: item["relation"])
    model["krin"]["required_tekmor"].sort()
    model["apor"].sort(key=lambda item: item["id"])
    for item in model["apor"]:
        item["candidates"].sort()
        item["impact_scope"].sort()
        item["allowed_resolutions"].sort()
    return model


def must_reject(source, description):
    try:
        parse(source)
    except (SourceError, ValueError):
        return
    raise AssertionError(f"must reject {description}")


def main():
    source = SOURCE_PATH.read_text()
    expected = json.loads(SEMANTIC_PATH.read_text())["input"]
    actual = parse(source)
    if normalize(actual) != normalize(expected):
        print("minimal source manifest does not map to SV-VALID-MINIMAL-001")
        return 1
    with_apor = parse(APOR_SOURCE_PATH.read_text())
    if with_apor["apor"] != [{
        "id": "apor:audience",
        "source_ref": "source:request-001#/range",
        "conflict": "目标读者尚未确认",
        "decision_authority": "authority:requester",
        "candidates": ["audience:security", "audience:executive"],
        "impact_scope": ["rel:produced"],
        "allowed_resolutions": ["rule", "named-authority"],
    }]:
        print("apor source manifest did not preserve the unresolved audience choice")
        return 1
    must_reject(source + "\nunknown\tvalue\n", "unknown directive")
    must_reject(source + next(line for line in source.splitlines() if line.startswith("rhem")) + "\n", "duplicate singleton")
    must_reject(source.replace("kine", "bad\\q", 1), "unknown escape")
    must_reject(source.replace("root\tsituation:report-produced", "root", 1), "wrong arity")
    spec = SPEC_PATH.read_text()
    for token in ("16 MiB", "1 MiB", "LF 或 CRLF", "END-SRCM-007", "不是 `.endem` 线格式"):
        if token not in spec:
            print(f"source manifest spec missing {token!r}")
            return 1
    print("PASS: END-SRCM mapped minimal and apor source manifests and rejected 4 deterministic mutations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
