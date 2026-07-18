from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registry.json"
CORPUS_PATH = ROOT / "spec" / "keyword-corpus.json"
PUBLIC_GUIDE_PATH = ROOT / "docs" / "development-guide.md"

COINED_PRONUNCIATIONS = {
    "Noemion": {
        "segments": ("No", "e", "mi", "on"),
        "ipa": "/noʊˈiː.mi.ən/",
        "plain_hint": "noh-EE-mee-uhn",
    },
    "Endem": {
        "segments": ("En", "dem"),
        "ipa": "/ˈɛn.dɛm/",
        "plain_hint": "EN-dem",
    },
}

MACHINE_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
MACHINE_TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:[-_:][A-Za-z0-9]+)*$")
HUMAN_TERM = re.compile(r"^[A-Za-z]+$")
TERM_WORD = re.compile(r"[A-Za-z]+")
DISALLOWED_INITIAL_CLUSTERS = ("gn", "kn", "mn", "pn", "ps", "pt", "rh", "wr")
SILENT_INITIAL_WORDS = {
    "heir", "herb", "honest", "honor", "honour", "hour", "who", "whole",
}
RETIRED_TERM = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"Synem|Dromen|Iknem|Ktisor|Theor|Drasor|"
    r"ktise|elenk|pleko|theor|drase|"
    r"rhem|semion|skena|telis|krin|apor|phain|kine|mene|agno|aseme"
    r")(?![A-Za-z0-9_])",
    re.IGNORECASE,
)

HISTORICAL_DOCUMENT = (
    re.compile(r"^architecture/adr-[0-9]{4}-.+\.md$"),
)

CURRENT_ROUTES = {
    "specifications/endem-closure.html": "specifications/endem-closure.md",
    "specifications/session-contract.html": "specifications/session-contract.md",
    "specifications/evidence-entry.html": "specifications/evidence-entry.md",
    "components/producer.html": "components/producer.md",
    "components/inspector.html": "components/inspector.md",
    "components/runner.html": "components/runner.md",
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


def is_historical_document(relative):
    return any(pattern.fullmatch(relative) for pattern in HISTORICAL_DOCUMENT)


def iter_structured_tokens(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from iter_structured_tokens(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_structured_tokens(item)
    elif isinstance(value, str):
        yield value


def main():
    errors = []
    registry = load(REGISTRY_PATH, errors)
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
            if HUMAN_TERM.fullmatch(entry["term"]) is None:
                errors.append(
                    f"spec/registry.json: human term must be one complete word: {entry['term']}"
                )
    folded = [name.casefold() for name in names]
    if len(folded) != len(set(folded)):
        errors.append("spec/registry.json: terminology entries must be unique case-insensitively")

    identifiers = registry.get("identifiers")
    if not isinstance(identifiers, list) or not identifiers:
        errors.append("spec/registry.json: identifiers must be a non-empty list")
        identifiers = []
    for index, entry in enumerate(identifiers):
        if not isinstance(entry, dict) or not isinstance(entry.get("identifier"), str):
            errors.append(f"spec/registry.json: identifier[{index}] must preserve an exact machine token")
            continue
        if MACHINE_TOKEN.fullmatch(entry["identifier"]) is None:
            errors.append(
                f"spec/registry.json: identifier[{index}] does not follow declared token syntax: "
                f"{entry['identifier']}"
            )

    current_words = {
        word.casefold()
        for name in names
        for word in TERM_WORD.findall(name)
    }
    for word in sorted(current_words):
        if word in SILENT_INITIAL_WORDS or word.startswith(DISALLOWED_INITIAL_CLUSTERS):
            errors.append(
                f"registered terminology has a silent or unstable word start: {word}"
            )

    formal_tokens = set()
    for directory in (ROOT / "spec", ROOT / "vectors"):
        for path in sorted(directory.rglob("*.json")):
            if path == CORPUS_PATH:
                continue
            data = load(path, errors)
            for token in iter_structured_tokens(data):
                if MACHINE_TOKEN.fullmatch(token) is None:
                    continue
                formal_tokens.add(token)
                for word in TERM_WORD.findall(token):
                    folded_word = word.casefold()
                    if (folded_word in SILENT_INITIAL_WORDS
                            or folded_word.startswith(DISALLOWED_INITIAL_CLUSTERS)):
                        errors.append(
                            f"{path.relative_to(ROOT)}: formal token has a silent or unstable "
                            f"word start: {token}"
                        )

    if not set(COINED_PRONUNCIATIONS).issubset(names):
        errors.append("spec/registry.json: Noemion and Endem must remain registered")
    for term, pronunciation in COINED_PRONUNCIATIONS.items():
        if "".join(pronunciation["segments"]).casefold() != term.casefold():
            errors.append(f"{term}: candidate pronunciation must preserve every written letter")
        for field in ("ipa", "plain_hint"):
            if not pronunciation[field]:
                errors.append(f"{term}: candidate pronunciation missing {field}")

    for removed_source in (
        ROOT / "docs" / "terminology-audit.md",
        ROOT / "docs" / "terminology-and-pronunciation.md",
        ROOT / "spec" / "goal_direction-release-terms-proposal.md",
        ROOT / "spec" / "lifecycle-and-result-terminology-proposal.md",
        ROOT / "spec" / "release-terminology-simplification-proposal.md",
        ROOT / "spec" / "semantic-facet-terminology-proposal.md",
    ):
        if removed_source.exists():
            errors.append(f"{removed_source.relative_to(ROOT)}: maintenance material must not generate a public page")

    public_guide_text = PUBLIC_GUIDE_PATH.read_text()
    for token in (
        "只保留两个自造名称",
        "`No-e-mi-on`",
        "`En-dem`",
        "/noʊˈiː.mi.ən/",
        "/ˈɛn.dɛm/",
        "每个字母，没有静音字母",
        "普通英语工程词沿用通常拼写",
        "每个人类名称都是一个完整单词",
        "职责短语只能用于说明",
        "字段、枚举、路由、文件路径和规范编号是机器标识",
        "替换项必须是一个完整单词",
        "首次朗读与听辨结果尚未形成",
    ):
        if token not in public_guide_text:
            errors.append(f"docs/development-guide.md: missing developer naming boundary {token!r}")

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

    normalized_registry = [normalize(name) for name in names]
    if len(normalized_registry) != len(set(normalized_registry)):
        errors.append("spec/registry.json: normalized human terms must remain unique")
    for name in names:
        normalized = normalize(name)
        if not normalized or MACHINE_IDENTIFIER.fullmatch(normalized) is None:
            errors.append(f"registered term has no valid normalized reference: {name}")
    for entry in identifiers:
        identifier = entry.get("identifier") if isinstance(entry, dict) else None
        if not isinstance(identifier, str):
            continue
        normalized = normalize(identifier)
        if normalized in keyword_set:
            errors.append(
                f"registered machine identifier collides with the versioned keyword corpus: {identifier}"
            )

    skipped = {".git", "_site", "vendor", ".bundle"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or skipped.intersection(path.parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith("tests/") or is_historical_document(relative):
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
        f"PASS: audited {len(names)} registered terms, {len(current_words)} word components and "
        f"{len(formal_tokens)} structured tokens "
        f"against {len(keyword_set)} versioned keywords; every current word has a direct start, "
        "and 2 retained coined names map every written letter into candidate pronunciations "
        "that still require human validation"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
