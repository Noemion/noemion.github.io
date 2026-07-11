from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import shutil
import subprocess
import sys


SOURCE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ONLY = len(sys.argv) == 1 or sys.argv[1] == "--source-only"
ROOT = SOURCE_ROOT if SOURCE_ONLY else Path(sys.argv[1]).resolve()
README = SOURCE_ROOT / "README.md"
DIRECTORY_CSS = ROOT / "assets" / "directory.css"
SOURCE_HTML_FILES = sorted(
    path
    for path in SOURCE_ROOT.rglob("*.html")
    if "_site" not in path.parts and not any(part.startswith("_") for part in path.parts)
)
HTML_FILES = SOURCE_HTML_FILES if SOURCE_ONLY else sorted(ROOT.rglob("*.html"))
RAW_AMP = re.compile(r"&(?![A-Za-z][A-Za-z0-9]+;|#[0-9]+;|#x[0-9A-Fa-f]+;)")
HREF_LITERAL = re.compile(r'href:\s*"([^"]+)"')
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
ROUTE_ROW = re.compile(
    r"^\| `([^`]+\.html)` \| (portal|section|content|tool|docs|topic) \| `([^`]*)` \| ([0-9]+) \| ([^|]+) \|$",
    re.MULTILINE,
)
NUMBERED_NAME = re.compile(r"(^|/)[0-9]+[-_]")
NUMBERED_ROUTE_SEGMENT = re.compile(r"(^|/)[0-9][^/]*(?:/|$)")
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
PORTAL_ROUTES = [
    "index.html",
    "about/index.html",
    "architecture/index.html",
    "specifications/index.html",
    "components/index.html",
    "tools/index.html",
    "docs/index.html",
    "downloads/index.html",
    "faq/index.html",
    "development/index.html",
    "news/index.html",
]
NOEMLD_DOC_ORDER = [
    "tools/noemld/docs/index.html",
    "tools/noemld/docs/contract.html",
    "tools/noemld/docs/inputs-outputs.html",
    "tools/noemld/docs/invocation.html",
    "tools/noemld/docs/pipeline.html",
    "tools/noemld/docs/symbol-resolution.html",
    "tools/noemld/docs/relocations.html",
    "tools/noemld/docs/sso-linking.html",
    "tools/noemld/docs/loader-security.html",
    "tools/noemld/docs/diagnostics.html",
    "tools/noemld/docs/testing.html",
    "tools/noemld/docs/dependencies.html",
    "tools/noemld/docs/reference-index.html",
]
DOC_GUIDE_ORDER = [
    "docs/getting-started.html",
    "docs/installation-and-usage.html",
    "docs/architecture-guide.html",
    "docs/development-guide.html",
    "docs/tools-reference.html",
    "docs/specifications-reference.html",
]
DOC_GUIDE_HEADINGS = {
    "docs/getting-started.html": [
        "从这里开始", "核心对象", "信任与确定性", "推荐阅读路径", "当前项目状态", "下一步",
    ],
    "docs/installation-and-usage.html": [
        "当前可用性", "未来使用流程", "输入与产物边界", "安装与发布原则", "安全检查", "开放问题",
    ],
    "docs/architecture-guide.html": [
        "系统分层", "对象生命周期", "编译与链接边界", "装载与运行边界", "信任边界", "开放问题",
    ],
    "docs/development-guide.html": [
        "第一阶段范围", "规范与 ADR 先行", "实现工作流", "测试与 Fuzz", "贡献与报告", "未来阶段",
    ],
    "docs/tools-reference.html": [
        "工具链总览", "规范与对象工具", "编译与链接", "发布与运行", "模型工程", "文档状态",
    ],
    "docs/specifications-reference.html": [
        "如何判断权威性", "成熟度标记", "GSIR", "GOBJ", "SSO", "开放问题与 ADR",
    ],
}
ROLE_BY_KIND = {
    "portal": "portal",
    "section": "section",
    "content": "content",
    "tool": "tool-project",
    "docs": "docs-index",
    "topic": "docs-topic",
}
TOOL_PROJECT_SECTIONS = [
    "工具简介",
    "当前状态",
    "主要能力",
    "输入与产物",
    "处理边界",
    "相关资源",
]
TOOL_PROJECT_STATUS_DECLARATION = (
    "设计阶段：当前未发布可执行程序；命令行接口、参数和文件扩展名尚未冻结。"
)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.stylesheets = []
        self.scripts = []
        self.icons = []
        self.directory_containers = 0
        self.skip_links = 0
        self.main_targets = 0
        self.class_counts = defaultdict(int)
        self.scoped_links = defaultdict(list)
        self.manual_roles = defaultdict(dict)
        self.breadcrumb_links = []
        self.breadcrumb_text = []
        self.h2_texts = []
        self.sections = []
        self.active_section = None
        self.active_h2 = None
        self.page_role = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        classes = set(data.get("class", "").split())
        ancestor_classes = set().union(*(item[1] for item in self.stack), set())
        for name in classes:
            self.class_counts[name] += 1
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "body" and data.get("data-page-role"):
            self.page_role = data["data-page-role"]
        if tag == "a" and "href" in data:
            href = data["href"]
            self.links.append(href)
            if "breadcrumbs" in ancestor_classes:
                self.breadcrumb_links.append(href)
            if href == "#main-content" and "skip-link" in classes:
                self.skip_links += 1
            for scope in ("manual-toc", "manual-nav-top", "manual-nav-bottom"):
                if scope in ancestor_classes:
                    self.scoped_links[scope].append(href)
                    role = data.get("data-manual-role")
                    if role:
                        self.manual_roles[scope][role] = href
            if "doc-guide-links" in ancestor_classes:
                self.scoped_links["doc-guide-links"].append(href)
        if (
            tag == "main"
            and data.get("id") == "main-content"
            and data.get("tabindex") == "-1"
        ):
            self.main_targets += 1
        if tag == "nav" and "data-directory" in data:
            self.directory_containers += 1
        if tag == "link" and data.get("rel") == "stylesheet":
            self.stylesheets.append(data.get("href"))
        if tag == "link" and "icon" in data.get("rel", "").split():
            self.icons.append(data.get("href"))
        if tag == "script" and data.get("src"):
            self.scripts.append(data["src"])
        if tag == "section":
            self.active_section = {"heading": [], "text": []}
            self.sections.append(self.active_section)
        if tag == "h2":
            self.active_h2 = []
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag):
        if tag == "h2" and self.active_h2 is not None:
            heading = " ".join("".join(self.active_h2).split())
            self.h2_texts.append(heading)
            if self.active_section is not None:
                self.active_section["heading"] = heading
            self.active_h2 = None
        if tag == "section":
            self.active_section = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if self.active_h2 is not None:
            self.active_h2.append(data)
        if self.active_section is not None:
            self.active_section["text"].append(data)
        ancestor_classes = set().union(*(item[1] for item in self.stack), set())
        if "breadcrumbs" in ancestor_classes:
            self.breadcrumb_text.append(data)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text())
    return parser


def read_route_rows():
    rows = []
    for route, kind, parent, order, purpose in ROUTE_ROW.findall(README.read_text()):
        rows.append(
            {
                "route": route,
                "kind": kind,
                "parent": parent,
                "order": int(order),
                "purpose": purpose.strip(),
            }
        )
    return rows


def resolve_local_path(path, url_path):
    if url_path.startswith("/"):
        return (ROOT / unquote(url_path).lstrip("/")).resolve()
    return (path.parent / unquote(url_path)).resolve()


def resolved_routes(path, hrefs):
    routes = []
    for href in hrefs:
        parts = urlsplit(href)
        if parts.scheme or href.startswith(("#", "mailto:", "tel:")):
            continue
        routes.append(resolve_local_path(path, parts.path).relative_to(ROOT).as_posix())
    return routes


def expected_manual_roles(index):
    roles = {
        "previous": Path(NOEMLD_DOC_ORDER[index - 1]).name,
        "up": "index.html",
        "index": "reference-index.html",
    }
    if index + 1 < len(NOEMLD_DOC_ORDER):
        roles["next"] = Path(NOEMLD_DOC_ORDER[index + 1]).name
    return roles


def normalize_visible_text(text):
    return " ".join(text.split())


def front_matter_value(block, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.MULTILINE)
    if match is None:
        return None
    value = match.group(1).strip()
    if value.startswith('"'):
        return json.loads(value)
    return value


def validate_jekyll_sources():
    errors = []
    route_rows = read_route_rows()
    registry = {row["route"]: row for row in route_rows}
    registered = sorted(registry)
    source_routes = sorted(path.relative_to(SOURCE_ROOT).as_posix() for path in SOURCE_HTML_FILES)

    if len(route_rows) != len(registry):
        errors.append("README contains duplicate HTML routes")
    if registered != source_routes:
        errors.append("README routes do not exactly match Jekyll source pages")
    if len(source_routes) != 64:
        errors.append(f"expected 64 Jekyll source pages, found {len(source_routes)}")

    forbidden_shell = re.compile(
        r"<!doctype|<html\b|<head\b|<body\b|class=\"site-header\"|<footer\b",
        re.IGNORECASE,
    )
    for path in SOURCE_HTML_FILES:
        route = path.relative_to(SOURCE_ROOT).as_posix()
        text = path.read_text()
        match = FRONT_MATTER.match(text)
        if match is None:
            errors.append(f"{route}: missing YAML front matter")
            continue
        metadata = match.group(1)
        row = registry.get(route)
        expected_role = ROLE_BY_KIND.get(row["kind"]) if row else None
        expected = {
            "layout": "default",
            "page_role": expected_role,
            "permalink": "/" + route,
        }
        for key, value in expected.items():
            actual = front_matter_value(metadata, key)
            if actual != value:
                errors.append(f"{route}: front matter {key} must be {value!r}, got {actual!r}")
        for key in ("title", "footer_text"):
            if not front_matter_value(metadata, key):
                errors.append(f"{route}: front matter requires {key}")
        body = text[match.end():]
        if forbidden_shell.search(body):
            errors.append(f"{route}: page shell must come from the Jekyll layout")
        parser = parse(path)
        if parser.main_targets != 1:
            errors.append(f"{route}: source must retain one main content target")

    layout = SOURCE_ROOT / "_layouts/default.html"
    header = SOURCE_ROOT / "_includes/site-header.html"
    footer = SOURCE_ROOT / "_includes/site-footer.html"
    for path in (layout, header, footer):
        if not path.exists():
            errors.append(f"missing Jekyll shared shell: {path.relative_to(SOURCE_ROOT)}")
    if layout.exists():
        layout_text = layout.read_text()
        for token in (
            "{{ content }}",
            "{% include site-header.html %}",
            "{% include site-footer.html %}",
            "{{ '/assets/style.css' | relative_url }}",
            "{{ '/assets/directory.js' | relative_url }}",
            'data-page-role="{{ page.page_role }}"',
        ):
            if token not in layout_text:
                errors.append(f"default layout missing contract: {token}")

    directory_script = SOURCE_ROOT / "assets/directory.js"
    if directory_script.exists():
        declared = sorted(set(HREF_LITERAL.findall(directory_script.read_text())))
        if declared != registered:
            errors.append("directory.js module entries do not cover every registered route")
    else:
        errors.append("missing assets/directory.js")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(source_routes)} Jekyll source pages use the shared layout contract")
    return 0


def validate_tool_project_contract(h2_texts, status_texts, manual_counts=None):
    errors = []
    if list(h2_texts) != TOOL_PROJECT_SECTIONS:
        errors.append(
            "tool-project h2 sequence must be exactly "
            f"{TOOL_PROJECT_SECTIONS}, got {list(h2_texts)}"
        )

    manual_counts = manual_counts or {}
    for class_name in ("manual-toc", "manual-nav-top", "manual-nav-bottom"):
        if manual_counts.get(class_name, 0):
            errors.append(f"{class_name} is forbidden on tool project pages")

    if len(status_texts) != 1:
        errors.append("expected one 当前状态 section")
    elif TOOL_PROJECT_STATUS_DECLARATION not in normalize_visible_text(status_texts[0]):
        errors.append(
            "current-state section must contain the complete disclosure: "
            + TOOL_PROJECT_STATUS_DECLARATION
        )
    return errors


def tool_project_validator_self_test():
    errors = []
    valid_status = [TOOL_PROJECT_STATUS_DECLARATION]
    if validate_tool_project_contract(TOOL_PROJECT_SECTIONS, valid_status):
        errors.append("tool-project validator rejects the valid reference contract")

    negative_cases = {
        "wrong order": [
            ["当前状态", "工具简介", *TOOL_PROJECT_SECTIONS[2:]],
            valid_status,
        ],
        "duplicate section": [
            [*TOOL_PROJECT_SECTIONS[:2], "当前状态", *TOOL_PROJECT_SECTIONS[2:]],
            valid_status,
        ],
        "extra numbered chapter": [
            [*TOOL_PROJECT_SECTIONS, "第七章 依赖与文档拆分"],
            valid_status,
        ],
        "reversed release wording": [
            TOOL_PROJECT_SECTIONS,
            ["设计阶段：当前已发布可执行程序；命令行接口、参数和文件扩展名已经冻结。"],
        ],
    }
    for name, (headings, statuses) in negative_cases.items():
        if not validate_tool_project_contract(headings, statuses):
            errors.append(f"tool-project validator failed to reject {name}")
    return errors


def main():
    errors = tool_project_validator_self_test()
    directory_css = DIRECTORY_CSS.read_text()
    unscoped_nav_selectors = re.findall(
        r"(?m)^\s*(nav(?:\s+a)?(?::[\w()-]+|\.[\w-]+)*)\s*\{",
        directory_css,
    )
    if unscoped_nav_selectors:
        errors.append(
            "directory.css contains unscoped navigation selectors: "
            + ", ".join(unscoped_nav_selectors)
        )
    if ".site-header .directory-panel .nav-section-links a{" not in directory_css:
        errors.append("directory.css must scope module-directory links to the site header panel")
    for token in (
        ".nav-section-toggle",
        "grid-template-rows:0fr",
        ".nav-section.is-open>.nav-section-panel",
        "transition-duration:180ms",
        "@media(prefers-reduced-motion:reduce)",
    ):
        if token not in directory_css:
            errors.append(f"directory.css missing modular navigation contract: {token}")

    route_rows = read_route_rows()
    registered = [row["route"] for row in route_rows]
    actual_routes = [path.relative_to(ROOT).as_posix() for path in HTML_FILES]

    if not route_rows:
        errors.append("README has no formal HTML route rows")
    if len(registered) != len(set(registered)):
        errors.append("README contains duplicate HTML routes")
    if sorted(registered) != sorted(actual_routes):
        errors.append("README routes do not exactly match HTML files")

    if [row["route"] for row in route_rows if row["kind"] == "portal"] != ["index.html"]:
        errors.append("README must register index.html as the only portal")

    section_routes = [row["route"] for row in route_rows if row["kind"] == "section"]
    if sorted(section_routes) != sorted(PORTAL_ROUTES[1:]):
        errors.append("README section routes do not match the approved portal architecture")

    for row in route_rows:
        path = ROOT / row["route"]
        if path.exists() and parse(path).page_role != ROLE_BY_KIND[row["kind"]]:
            errors.append(f"{row['route']}: page role does not match registry kind")

    for row in route_rows:
        if row["kind"] != "tool":
            continue
        path = ROOT / row["route"]
        if not path.exists():
            continue
        parser = parse(path)
        tool = Path(row["route"]).parent.name
        breadcrumb = " ".join("".join(parser.breadcrumb_text).split())
        breadcrumb_routes = resolved_routes(path, parser.breadcrumb_links)
        if (
            parser.class_counts["breadcrumbs"] != 1
            or breadcrumb_routes != ["index.html", "tools/index.html"]
            or not all(label in breadcrumb for label in ("项目", "工具", tool))
        ):
            errors.append(f"{row['route']}: must expose 项目 / 工具 / 当前工具 breadcrumbs")
        status_sections = [section for section in parser.sections if section["heading"] == "当前状态"]
        status_texts = ["".join(section["text"]) for section in status_sections]
        contract_errors = validate_tool_project_contract(
            parser.h2_texts,
            status_texts,
            parser.class_counts,
        )
        errors.extend(f"{row['route']}: {error}" for error in contract_errors)

    global_rows = [
        row["route"]
        for row in route_rows
        if row["kind"] in {"portal", "section", "tool"}
    ]
    if route_rows and len(global_rows) != 34:
        errors.append(f"expected 34 global landing routes, found {len(global_rows)}")

    route_registry = {row["route"]: row for row in route_rows}

    for order, route in enumerate(DOC_GUIDE_ORDER, start=1):
        row = route_registry.get(route)
        if (
            row is None
            or row["kind"] != "content"
            or row["parent"] != "docs/index.html"
            or row["order"] != order
        ):
            errors.append(f"{route}: invalid documentation guide registry metadata")

    docs_index = ROOT / "docs/index.html"
    if docs_index.exists():
        parser = parse(docs_index)
        guide_links = resolved_routes(
            docs_index,
            parser.scoped_links["doc-guide-links"],
        )
        if guide_links != DOC_GUIDE_ORDER:
            errors.append("docs index cards must link the six HTML guides in order")

    for route in DOC_GUIDE_ORDER:
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing documentation guide {route}")
            continue
        parser = parse(path)
        breadcrumb = normalize_visible_text("".join(parser.breadcrumb_text))
        breadcrumb_routes = resolved_routes(path, parser.breadcrumb_links)
        if (
            parser.page_role != "content"
            or parser.class_counts["breadcrumbs"] != 1
            or breadcrumb_routes != ["index.html", "docs/index.html"]
            or not all(label in breadcrumb for label in ("项目", "文档"))
        ):
            errors.append(f"{route}: invalid project / docs / current breadcrumbs")
        if parser.h2_texts != DOC_GUIDE_HEADINGS[route]:
            errors.append(
                f"{route}: guide h2 sequence must be {DOC_GUIDE_HEADINGS[route]}, "
                f"got {parser.h2_texts}"
            )
        visible_text = normalize_visible_text(
            " ".join("".join(section["text"]) for section in parser.sections)
        )
        if "已确认原则" not in visible_text or not any(
            marker in visible_text for marker in ("设计提案", "开放问题", "未来阶段")
        ):
            errors.append(f"{route}: guide must distinguish confirmed and non-final content")

    noemld_tool = route_registry.get("tools/noemld/index.html")
    if noemld_tool is None or noemld_tool["kind"] != "tool":
        errors.append("tools/noemld/index.html must be registered as kind tool")
    noemld_docs = route_registry.get(NOEMLD_DOC_ORDER[0])
    if noemld_docs is None or noemld_docs["kind"] != "docs":
        errors.append("tools/noemld/docs/index.html must be registered as kind docs")

    noemld_rows = [row for row in route_rows if row["route"] in NOEMLD_DOC_ORDER]
    if route_rows:
        ordered_noemld = [
            row["route"] for row in sorted(noemld_rows, key=lambda row: row["order"])
        ]
        if ordered_noemld != NOEMLD_DOC_ORDER:
            errors.append("README noemld routes do not match the manual order")

    for route in NOEMLD_DOC_ORDER[1:]:
        row = route_registry.get(route)
        if (
            row is None
            or row["kind"] != "topic"
            or row["parent"] != "tools/noemld/docs/index.html"
        ):
            errors.append(f"{route}: invalid noemld topic registry metadata")

    legacy_noemld_routes = [
        (Path("tools/noemld") / Path(route).name).as_posix()
        for route in NOEMLD_DOC_ORDER[1:]
        if (ROOT / "tools/noemld" / Path(route).name).exists()
    ]
    if legacy_noemld_routes:
        errors.append(
            f"legacy noemld topic routes are forbidden: {legacy_noemld_routes}"
        )

    numbered_routes = [
        route
        for route in actual_routes
        if NUMBERED_NAME.search(route) or NUMBERED_ROUTE_SEGMENT.search(route)
    ]
    if numbered_routes:
        errors.append(f"numbered HTML routes are forbidden: {numbered_routes}")

    if len(actual_routes) != 64:
        errors.append(f"expected 64 final HTML routes, found {len(actual_routes)}")

    downloads = ROOT / "downloads/index.html"
    if downloads.exists():
        text = downloads.read_text()
        if 'href=""' in text or 'href="#"' in text or "javascript:" in text:
            errors.append("downloads page contains a fake or empty download link")
        if 'data-resource-state="unreleased"' not in text:
            errors.append("downloads page must expose an explicit unreleased state")

    directory_script = ROOT / "assets/directory.js"
    favicon = ROOT / "assets/favicon.svg"
    if not directory_script.exists():
        errors.append("missing assets/directory.js")
    if not favicon.exists():
        errors.append("missing assets/favicon.svg")

    for path in HTML_FILES:
        text = path.read_text()
        parser = parse(path)
        rel = path.relative_to(ROOT).as_posix()
        if RAW_AMP.search(text):
            errors.append(f"{rel}: contains an unescaped ampersand")
        if parser.directory_containers != 1:
            errors.append(f"{rel}: expected one data-directory nav")
        if parser.skip_links != 1 or parser.main_targets != 1:
            errors.append(f"{rel}: missing unique skip link or main target")
        if len(parser.stylesheets) != 1:
            errors.append(f"{rel}: expected exactly one stylesheet")
        if len(parser.scripts) != 1 or not parser.scripts[0].endswith("assets/directory.js"):
            errors.append(f"{rel}: missing shared directory script")
        if len(parser.icons) != 1:
            errors.append(f"{rel}: missing unique favicon reference")
        else:
            icon_path = resolve_local_path(path, urlsplit(parser.icons[0]).path)
            if icon_path != favicon.resolve() or not icon_path.exists():
                errors.append(f"{rel}: favicon path does not resolve to assets/favicon.svg")
        duplicates = sorted(name for name in set(parser.ids) if parser.ids.count(name) > 1)
        if duplicates:
            errors.append(f"{rel}: duplicate IDs {duplicates}")
        for href in parser.links:
            parts = urlsplit(href)
            if parts.scheme or href.startswith(("mailto:", "tel:")):
                continue
            target = path if not parts.path else resolve_local_path(path, parts.path)
            if not target.exists():
                errors.append(f"{rel}: broken link {href}")
            elif parts.fragment and target.suffix == ".html":
                if parts.fragment not in parse(target).ids:
                    errors.append(f"{rel}: missing fragment target {href}")

    if directory_script.exists() and route_rows:
        directory_source = directory_script.read_text()
        declared = sorted(set(HREF_LITERAL.findall(directory_source)))
        if declared != sorted(registered):
            errors.append("directory.js module entries do not cover every registered route")
        for token in (
            "DIRECTORY_MODULES",
            "resolveDirectoryModule",
            "nav-section-toggle",
            'setAttribute("aria-expanded"',
            'toggleAttribute("inert"',
        ):
            if token not in directory_source:
                errors.append(f"directory.js missing modular navigation contract: {token}")
        node = shutil.which("node")
        if node is None:
            errors.append("node is required to execute directory active-item behavior tests")
        else:
            active_cases = [
                ["tools/noemld/index.html", "https://site.test/tools/noemld", "https://site.test/tools/noemld/docs", True],
                ["tools/noemld/index.html", "https://site.test/tools/noemld", "https://site.test/tools/noemld/docs/topic.html", True],
                ["tools/noemld/index.html", "https://site.test/tools/noemld", "https://site.test/tools/noemld/docsfoo", False],
                ["tools/noemld/index.html", "https://site.test/tools/noemld", "https://site.test/tools/noemld/docs-old/x", False],
                ["tools/noemld/index.html", "https://site.test/tools/noemld", "https://site.test/tools/noemldx/docs", False],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs/guide", True],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs/getting-started.html", True],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs-old/guide.html", False],
                ["tools/index.html", "https://site.test/tools", "https://site.test/tools/noemobj", False],
            ]
            module_cases = [
                ["index.html", "project"],
                ["about/background.html", "project"],
                ["architecture/object-lifecycle.html", "architecture"],
                ["specifications/gsir.html", "architecture"],
                ["components/nsfe.html", "architecture"],
                ["docs/getting-started.html", "docs"],
                ["downloads/index.html", "resources"],
                ["faq/index.html", "resources"],
                ["development/testing.html", "development"],
                ["news/index.html", "development"],
                ["tools/noemobj/index.html", "tools"],
                ["tools/noemld/index.html", "noemld"],
                ["tools/noemld/docs/contract.html", "noemldDocs"],
            ]
            behavior_script = (
                "const api = require(process.argv[1]);"
                "if (globalThis.NoemionDirectory !== undefined) "
                "throw new Error('directory module must not expose a global API');"
                "if (!Object.isFrozen(api)) throw new Error('directory module API must be frozen');"
                "const { isDirectoryItemActive, resolveDirectoryModule } = api;"
                "const cases = JSON.parse(process.argv[2]);"
                "const active = cases.map(([itemHref, target, current]) => "
                "isDirectoryItemActive(itemHref, target, current));"
                "const moduleCases = JSON.parse(process.argv[3]);"
                "const modules = moduleCases.map(([route]) => resolveDirectoryModule(route));"
                "process.stdout.write(JSON.stringify({active, modules}));"
            )
            completed = subprocess.run(
                [
                    node,
                    "-e",
                    behavior_script,
                    str(directory_script),
                    json.dumps(active_cases),
                    json.dumps(module_cases),
                ],
                capture_output=True,
                text=True,
            )
            if completed.returncode != 0:
                errors.append(
                    "directory active-item behavior test could not execute: "
                    + completed.stderr.strip()
                )
            else:
                actual = json.loads(completed.stdout)
                expected_active = [case[3] for case in active_cases]
                expected_modules = [case[1] for case in module_cases]
                if actual["active"] != expected_active:
                    errors.append(
                        "directory active-item behavior mismatch: "
                        f"expected {expected_active}, got {actual['active']}"
                    )
                if actual["modules"] != expected_modules:
                    errors.append(
                        "directory module routing mismatch: "
                        f"expected {expected_modules}, got {actual['modules']}"
                    )

    noemld_index = ROOT / NOEMLD_DOC_ORDER[0]
    if noemld_index.exists():
        parser = parse(noemld_index)
        toc_routes = resolved_routes(noemld_index, parser.scoped_links["manual-toc"])
        if toc_routes != NOEMLD_DOC_ORDER[1:]:
            errors.append("noemld index manual TOC does not match registered topic order")
        toc_markup = re.search(
            r'<ol class="manual-toc">(.*?)</ol>', noemld_index.read_text(), re.S
        )
        if toc_markup and re.search(r"<a[^>]*>\s*[0-9]+\.", toc_markup.group(1)):
            errors.append("noemld manual TOC must not duplicate ordered-list numbers")

    for index, route in enumerate(NOEMLD_DOC_ORDER[1:], start=1):
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing noemld topic page {route}")
            continue
        if NUMBERED_NAME.search(route):
            errors.append(f"{route}: numbered topic filename is forbidden")
        parser = parse(path)
        for class_name in ("breadcrumbs", "manual-nav-top", "manual-nav-bottom"):
            if parser.class_counts[class_name] != 1:
                errors.append(f"{route}: expected one {class_name}")
        expected = expected_manual_roles(index)
        for scope in ("manual-nav-top", "manual-nav-bottom"):
            if parser.manual_roles[scope] != expected:
                errors.append(f"{route}: invalid {scope} roles {parser.manual_roles[scope]}")

    style = (ROOT / "assets/style.css").read_text()
    for token in (
        "@keyframes page-reveal",
        ".site-header,main",
        "animation:page-reveal 110ms",
        "opacity:.96",
        "@media(prefers-reduced-motion:reduce)",
        "animation:none!important",
    ):
        if token not in style:
            errors.append(f"style.css missing animation contract: {token}")

    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PASS: {len(HTML_FILES)} registered pages, "
        f"{len(global_rows)} global landings, and project portal/noemld docs contract"
    )
    return 0


if __name__ == "__main__":
    sys.exit(validate_jekyll_sources() if SOURCE_ONLY else main())
