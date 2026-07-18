from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registry.json"
AUDIT_PATH = ROOT / "spec" / "terminology-audit.json"
CORPUS_PATH = ROOT / "spec" / "keyword-corpus.json"

MACHINE_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
RETIRED_TERM = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"Synem|Dromen|Iknem|Ktisor|Theor|Drasor|"
    r"ktise|elenk|pleko|theor|drase|"
    r"rhem|semion|skena|telis|krin|apor|phain|kine|mene|agno|aseme"
    r")(?![A-Za-z0-9_])",
    re.IGNORECASE,
)

HISTORICAL_OR_RESEARCH = (
    re.compile(r"^architecture/adr-[0-9]{4}-.+\.html$"),
    re.compile(r"^architecture/adr-0037-terminology-simplification\.md$"),
    re.compile(r"^spec/.+-proposal\.md$"),
    re.compile(r"^design-system/name-audit\.md$"),
    re.compile(r"^content-quality-audit\.md$"),
    re.compile(r"^spec/terminology-audit\.json$"),
)

CURRENT_ROUTES = {
    "specifications/endem-closure.html": "specifications/endem-closure.html",
    "specifications/session-contract.html": "specifications/session-contract.html",
    "specifications/evidence-entry.html": "specifications/evidence-entry.html",
    "components/producer.html": "components/producer.html",
    "components/inspector.html": "components/inspector.html",
    "components/runner.html": "components/runner.html",
    "spec/endem-closure-core.html": "spec/endem-closure-core.md",
    "spec/session-contract-core.html": "spec/session-contract-core.md",
    "spec/evidence-entry-core.html": "spec/evidence-entry-core.md",
}

RETIRED_CURRENT_ROUTES = (
    "specifications/synem.html",
    "specifications/dromen.html",
    "specifications/iknem.html",
    "components/ktisor.html",
    "components/theor.html",
    "components/drasor.html",
)


def load(path, errors):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot load JSON: {exc}")
        return {}


def normalize(term):
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", term.casefold())).strip("_")


def is_historical_or_research(relative):
    return any(pattern.fullmatch(relative) for pattern in HISTORICAL_OR_RESEARCH)


def main():
    errors = []
    registry = load(REGISTRY_PATH, errors)
    audit = load(AUDIT_PATH, errors)
    corpus = load(CORPUS_PATH, errors)

    if registry.get("updated") != "2026-07-18":
        errors.append("spec/registry.json: terminology migration date must be 2026-07-18")
    terms = registry.get("terms")
    if not isinstance(terms, list) or not terms:
        errors.append("spec/registry.json: terms must be a non-empty list")
        terms = []
    names = []
    for index, entry in enumerate(terms):
        if not isinstance(entry, dict):
            errors.append(f"spec/registry.json: term[{index}] must be an object")
            continue
        for field in ("term", "kind", "decision_status", "definition"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"spec/registry.json: term[{index}] missing {field}")
        if isinstance(entry.get("term"), str):
            names.append(entry["term"])
    folded = [name.casefold() for name in names]
    if len(folded) != len(set(folded)):
        errors.append("spec/registry.json: terminology entries must be unique case-insensitively")

    if audit.get("registry") != "spec/registry.json" or audit.get("keyword_corpus") != "spec/keyword-corpus.json":
        errors.append("spec/terminology-audit.json: audit must bind the registry and keyword corpus")
    proper_names = audit.get("retained_proper_names", [])
    if {item.get("term") for item in proper_names} != {"Noemion", "Endem"}:
        errors.append("spec/terminology-audit.json: Noemion and Endem must be the only retained coined proper names")
    for item in proper_names:
        if item.get("status") != "human-pronunciation-validation-required":
            errors.append(f"{item.get('term')}: retained coined name must require human pronunciation validation")

    sources = corpus.get("sources")
    expected_languages = {"C", "C++", "Rust", "Go", "Python", "Java", "ECMAScript", "Swift", "Kotlin", "C#", "PostgreSQL SQL"}
    if not isinstance(sources, list) or {item.get("language") for item in sources} != expected_languages:
        errors.append("spec/keyword-corpus.json: versioned language corpus is incomplete")
    for source in sources or []:
        if not all(isinstance(source.get(field), str) and source[field] for field in ("language", "edition", "url")):
            errors.append("spec/keyword-corpus.json: every language source needs language, edition and URL")
    keywords = corpus.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        errors.append("spec/keyword-corpus.json: keywords must be a non-empty list")
        keywords = []
    keyword_set = {word.casefold() for word in keywords if isinstance(word, str)}
    for required_collision in ("grant", "defer", "fixed", "all", "some"):
        if required_collision not in keyword_set:
            errors.append(f"spec/keyword-corpus.json: missing demonstrated collision {required_collision}")

    machine_terms = audit.get("current_machine_identifiers")
    if not isinstance(machine_terms, list) or not machine_terms:
        errors.append("spec/terminology-audit.json: current_machine_identifiers must be a non-empty list")
        machine_terms = []
    normalized_registry = {normalize(name) for name in names}
    for identifier in machine_terms:
        if not isinstance(identifier, str) or MACHINE_IDENTIFIER.fullmatch(identifier) is None:
            errors.append(f"invalid current machine identifier: {identifier!r}")
            continue
        if identifier.casefold() in keyword_set:
            errors.append(f"current machine identifier collides with the versioned keyword corpus: {identifier}")
        if identifier not in normalized_registry:
            errors.append(f"current machine identifier is not represented by spec/registry.json: {identifier}")
    retained = {normalize(item["term"]) for item in proper_names if isinstance(item.get("term"), str)}
    for name in names:
        identifier = normalize(name)
        if identifier and identifier not in retained and identifier in keyword_set:
            errors.append(f"registered term collides with the versioned keyword corpus after normalization: {name}")

    migrations = audit.get("migrations")
    if not isinstance(migrations, list) or len(migrations) < 20:
        errors.append("spec/terminology-audit.json: project-wide migration evidence is incomplete")
    else:
        migrated_from = " ".join(item.get("from", "") for item in migrations)
        for required in ("Synem", "Dromen", "Iknem", "Ktisor", "Theor", "Drasor", "rhem", "semion", "skena", "telis", "krin", "apor", "phain"):
            if required not in migrated_from:
                errors.append(f"spec/terminology-audit.json: missing migration for {required}")

    skipped = {".git", "_site", "vendor", ".bundle"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or skipped.intersection(path.parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith("tests/") or is_historical_or_research(relative):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        current_text = re.sub(
            r"(?:https://noemion\.github\.io/|(?:\.\./)*)?(?:architecture/)?adr-[0-9]{4}-[^\s\"')>]+",
            "",
            text,
        )
        match = RETIRED_TERM.search(current_text)
        if match:
            errors.append(f"{relative}: retired current terminology remains: {match.group(0)}")

    for route, source in CURRENT_ROUTES.items():
        path = ROOT / source
        if not path.exists():
            errors.append(f"current route source is missing: {source}")
        if source.endswith(".md") and f'permalink: "/{route}"' not in path.read_text():
            errors.append(f"{source}: permalink must publish /{route}")
    for route in RETIRED_CURRENT_ROUTES:
        if (ROOT / route).exists():
            errors.append(f"retired current route must not remain as an alias: {route}")

    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PASS: audited {len(names)} registered terms and {len(machine_terms)} current machine identifiers "
        f"against {len(keyword_set)} versioned keywords; retained coined names still require human validation"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
