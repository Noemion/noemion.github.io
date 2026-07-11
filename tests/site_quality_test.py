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
SOURCE_SITEMAP = SOURCE_ROOT / "sitemap.md"
DIRECTORY_CSS = ROOT / "assets" / "directory.css"
SOURCE_HTML_FILES = sorted(
    path
    for path in SOURCE_ROOT.rglob("*.html")
    if "_site" not in path.parts and not any(part.startswith("_") for part in path.parts)
)
MANUAL_MARKDOWN_FILES = sorted(
    [*SOURCE_ROOT.glob("docs/*.md"), *SOURCE_ROOT.glob("tools/*/docs/*.md")]
)
SOURCE_PAGE_FILES = sorted([*SOURCE_HTML_FILES, *MANUAL_MARKDOWN_FILES])
TOOL_IDS = sorted(path.parent.name for path in SOURCE_ROOT.glob("tools/*/index.html"))
HTML_FILES = SOURCE_HTML_FILES if SOURCE_ONLY else sorted(ROOT.rglob("*.html"))
RAW_AMP = re.compile(r"&(?![A-Za-z][A-Za-z0-9]+;|#[0-9]+;|#x[0-9A-Fa-f]+;)")
HREF_LITERAL = re.compile(r'href:\s*"([^"]+)"')
EXTERNAL_ANCHOR = re.compile(
    r'<a\s+[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
HTML_TAG = re.compile(r"<[^>]+>")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SITEMAP_ROUTE_ENTRY = re.compile(
    r"^- \[([^\]]+)\]\(https://noemion\.github\.io/([A-Za-z0-9_./-]+\.html)\) — (.+)$",
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
HOME_HEADINGS = [
    "意义还没有成为工程对象",
    "把一次性上下文变成可验证对象",
    "当前设计焦点",
    "从理解行为到可信装载",
    "先理解边界再阅读对象",
    "证据优先于主张",
    "Noemion 是什么也不是什么",
    "只有证据通过能力才进入下一阶段",
    "选择下一步",
]
INTELLECTUAL_FOUNDATIONS_HEADINGS = [
    "为什么阅读这些著作",
    "阅读与采用方法",
    "核心思想与工程问题",
    "《逻辑哲学论》的第一批检查点",
    "对 GSIR 的设计提案",
    "核心书目与资源状态",
    "思想采用的验证要求",
]
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
    "当前状态：尚未发布可执行版本，命令行界面、参数和文件扩展名仍在设计中。"
)
PUBLIC_META_PHRASES = (
    "本轮",
    "用户提供版本",
    "逐一 review",
    "页面仅说明",
    "专题文档拆分条件",
    "专题文档应",
    "本页不虚构",
    "本页只定义项目边界",
    "项目设计说明",
    "用于设计评审",
    "评审输入",
    "旧蓝图",
    "当前蓝图",
    "工程蓝图",
    "蓝图示例",
    "只完成页面",
    "后续文档将",
    "页面不得提前",
    "本页",
    "当前内容属于",
    "已确认内容限于",
    "尚未冻结的接口包括",
    "阶段门",
    "证据门",
    "退出证据",
    "放行",
    "IPD",
    "Codex",
    "ChatGPT",
    "subagent",
)
NORMATIVE_ROUTES = (
    "specifications/gsir.html",
    "specifications/gobj.html",
    "specifications/sso.html",
)
CONTENT_LAYOUT_ROUTES = (
    "about/background.html",
    "about/intellectual-foundations.html",
    "architecture/object-lifecycle.html",
    "architecture/open-questions.html",
    "components/compiler-core.html",
    "components/linker-loader.html",
    "components/nsfe.html",
    "development/implementation-roadmap.html",
    "development/testing.html",
    "specifications/gobj.html",
    "specifications/gsir.html",
    "specifications/sso.html",
)
CONTENT_LAYOUT_CLASSES = {
    "content-split",
    "content-stack",
    "content-band",
    "content-wide",
    "content-grid",
    "content-rows",
}


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
        self.manual_article_text = []
        self.active_section = None
        self.active_h2 = None
        self.page_role = None
        self.tool_id = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        classes = set(data.get("class", "").split())
        ancestor_classes = set().union(*(item[1] for item in self.stack), set())
        if (
            self.active_section is not None
            and self.stack
            and self.stack[-1][0] == "section"
        ):
            self.active_section["direct_children"].append((tag, classes))
        for name in classes:
            self.class_counts[name] += 1
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "body" and data.get("data-page-role"):
            self.page_role = data["data-page-role"]
            self.tool_id = data.get("data-tool-id")
        if tag == "a" and "href" in data:
            href = data["href"]
            self.links.append(href)
            if "breadcrumbs" in ancestor_classes:
                self.breadcrumb_links.append(href)
            if href == "#main-content" and "skip-link" in classes:
                self.skip_links += 1
            for scope in ("manual-toc", "manual-index-links", "manual-nav-top", "manual-nav-bottom"):
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
            ancestor_tags = [item[0] for item in self.stack]
            self.active_section = {
                "heading": [],
                "text": [],
                "classes": classes,
                "direct_children": [],
                "direct_main_child": bool(ancestor_tags and ancestor_tags[-1] == "main"),
            }
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
        if "manual-article" in ancestor_classes:
            self.manual_article_text.append(data)
        if "breadcrumbs" in ancestor_classes:
            self.breadcrumb_text.append(data)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text())
    return parser


def read_route_rows():
    rows = []
    sibling_orders = defaultdict(int)
    for label, route, purpose in SITEMAP_ROUTE_ENTRY.findall(SOURCE_SITEMAP.read_text()):
        if route == "index.html":
            kind = "portal"
            parent = ""
            order = 0
        elif route in PORTAL_ROUTES[1:]:
            kind = "section"
            parent = "index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        elif route == "tools/noemld/docs/index.html":
            kind = "docs"
            parent = "tools/noemld/index.html"
            order = 0
        elif route.startswith("tools/noemld/docs/"):
            kind = "topic"
            parent = "tools/noemld/docs/index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        elif route.startswith("tools/") and route.endswith("/index.html"):
            kind = "tool"
            parent = "tools/index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        else:
            kind = "content"
            parent = f"{route.rsplit('/', 1)[0]}/index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        rows.append(
            {
                "route": route,
                "kind": kind,
                "parent": parent,
                "order": order,
                "purpose": purpose.strip(),
                "label": label.strip(),
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
        "previous": "/" + NOEMLD_DOC_ORDER[index - 1],
        "up": "/tools/noemld/docs/index.html",
        "index": "/tools/noemld/docs/reference-index.html",
    }
    if index + 1 < len(NOEMLD_DOC_ORDER):
        roles["next"] = "/" + NOEMLD_DOC_ORDER[index + 1]
    return roles


def normalize_visible_text(text):
    return " ".join(text.split())


def validate_public_html(route, text):
    errors = []
    for phrase in PUBLIC_META_PHRASES:
        if phrase in text:
            errors.append(f"{route}: public HTML exposes internal production phrase {phrase!r}")
    for href, label_markup in EXTERNAL_ANCHOR.findall(text):
        label = normalize_visible_text(HTML_TAG.sub("", label_markup))
        if label != href:
            errors.append(
                f"{route}: external resource link must display its original URL {href!r}"
            )
    return errors


def front_matter_value(block, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.MULTILINE)
    if match is None:
        return None
    value = match.group(1).strip()
    if value.startswith('"'):
        return json.loads(value)
    return value


def read_manual_source_routes():
    routes = []
    for path in MANUAL_MARKDOWN_FILES:
        match = FRONT_MATTER.match(path.read_text())
        if match is None:
            continue
        permalink = front_matter_value(match.group(1), "permalink")
        if permalink:
            routes.append(permalink.lstrip("/"))
    return sorted(routes)


def read_manual_source_entries(manual_id):
    entries = []
    for path in MANUAL_MARKDOWN_FILES:
        match = FRONT_MATTER.match(path.read_text())
        if match is None:
            continue
        metadata = match.group(1)
        if front_matter_value(metadata, "manual_id") != manual_id:
            continue
        permalink = front_matter_value(metadata, "permalink")
        entries.append({
            "route": permalink.lstrip("/"),
            "order": int(front_matter_value(metadata, "manual_order")),
            "is_index": front_matter_value(metadata, "manual_is_index") == "true",
        })
    return sorted(entries, key=lambda entry: entry["order"])


def validate_jekyll_sources():
    errors = []
    route_rows = read_route_rows()
    registry = {row["route"]: row for row in route_rows}
    registered = sorted(set(registry) | set(read_manual_source_routes()))
    source_entries = []
    for path in SOURCE_PAGE_FILES:
        source_text = path.read_text()
        source_match = FRONT_MATTER.match(source_text)
        if source_match is None:
            continue
        if path.suffix == ".md":
            permalink = front_matter_value(source_match.group(1), "permalink")
            route = permalink.lstrip("/") if permalink else path.relative_to(SOURCE_ROOT).as_posix()
        else:
            route = path.relative_to(SOURCE_ROOT).as_posix()
        source_entries.append((route, path))
    source_routes = sorted(route for route, _ in source_entries)

    if len(route_rows) != len(registry):
        errors.append("sitemap.md contains duplicate HTML routes")
    if registered != source_routes:
        errors.append("sitemap.md routes do not exactly match Jekyll source pages")
    if len(source_routes) < 65:
        errors.append(f"expected at least 65 Jekyll source pages, found {len(source_routes)}")

    forbidden_shell = re.compile(
        r"<!doctype|<html\b|<head\b|<body\b|class=\"site-header\"|<footer\b",
        re.IGNORECASE,
    )
    if len(source_routes) != len(set(source_routes)):
        errors.append("multiple source files generate the same formal route")

    for route, path in source_entries:
        text = path.read_text()
        match = FRONT_MATTER.match(text)
        if match is None:
            errors.append(f"{route}: missing YAML front matter")
            continue
        metadata = match.group(1)
        row = registry.get(route)
        expected_role = (
            ROLE_BY_KIND.get(row["kind"])
            if row
            else front_matter_value(metadata, "page_role")
        )
        is_manual_markdown = path.suffix == ".md"
        expected = {
            "layout": "manual" if is_manual_markdown else "default",
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
        if not is_manual_markdown:
            errors.extend(validate_public_html(route, body))
        if forbidden_shell.search(body):
            errors.append(f"{route}: page shell must come from the Jekyll layout")
        if is_manual_markdown:
            for key in ("manual_id", "manual_group", "manual_order", "nav_title", "hero_title", "hero_description"):
                if front_matter_value(metadata, key) is None:
                    errors.append(f"{route}: Markdown manual requires {key}")
            body_without_autolinks = re.sub(
                r"<(?:https?://|mailto:)[^>]+>", "", body, flags=re.IGNORECASE
            )
            if re.search(r"</?[A-Za-z][^>]*>", body_without_autolinks):
                errors.append(f"{route}: Markdown body must not contain raw HTML")
            if re.search(r"^\s*\{:", body, re.MULTILINE):
                errors.append(f"{route}: Markdown body must not use Kramdown attributes")
            headings = re.findall(r"^##\s+(.+?)\s*$", body, re.MULTILINE)
            if route in DOC_GUIDE_HEADINGS and headings != DOC_GUIDE_HEADINGS[route]:
                errors.append(
                    f"{route}: Markdown h2 sequence must be {DOC_GUIDE_HEADINGS[route]}, got {headings}"
                )
        else:
            parser = parse(path)
            if parser.main_targets != 1:
                errors.append(f"{route}: source must retain one main content target")
            if route in CONTENT_LAYOUT_ROUTES:
                direct_sections = [
                    section for section in parser.sections if section["direct_main_child"]
                ]
                if not direct_sections:
                    errors.append(f"{route}: content page must contain direct sections")
                for index, section in enumerate(direct_sections, start=1):
                    layout_classes = section["classes"] & CONTENT_LAYOUT_CLASSES
                    if len(layout_classes) != 1:
                        errors.append(
                            f"{route}: section {index} must declare exactly one content layout, "
                            f"got {sorted(layout_classes)}"
                        )
                    if (
                        "content-split-reverse" in section["classes"]
                        and "content-split" not in layout_classes
                    ):
                        errors.append(
                            f"{route}: section {index} uses content-split-reverse without content-split"
                        )

    homepage_source = SOURCE_ROOT / "index.html"
    if homepage_source.exists():
        expression_visual_match = re.search(
            r'<span class="feature-visual feature-visual-expression".*?</span>',
            homepage_source.read_text(),
            re.DOTALL,
        )
        if expression_visual_match is None:
            errors.append("index.html: missing expression feature visual")
        else:
            visible_expression_text = HTML_TAG.sub(" ", expression_visual_match.group(0))
            if re.search(r"[\u3400-\u9fff]", visible_expression_text):
                errors.append(
                    "index.html: expression feature visual labels must use English only"
                )

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
            "data-docs-rail",
            "page.permalink contains '/docs/'",
            'data-tool-id="{{ page_tool_id }}"',
            "{{ '/assets/style.css' | relative_url }}",
            "{{ '/assets/directory.css' | relative_url }}",
            "{{ '/assets/directory.js' | relative_url }}",
            "{{ '/assets/catalog.js' | relative_url }}",
            "site.github.build_revision",
            "?v={{ asset_version | escape }}",
            'data-page-role="{{ page.page_role }}"',
        ):
            if token not in layout_text:
                errors.append(f"default layout missing contract: {token}")

    if header.exists():
        header_text = header.read_text()
        for token in (
            "data-global-nav",
            "global-directory-panel",
            "data-portal-stage",
            "<span>导航</span>",
            "global-stage-value",
            "global-stage-progress",
            "global-stage-text",
            "data-stage-value",
            "site.data.project_timeline",
            "project_timeline.current_stage_id",
            "project_timeline.header.href",
            "current_stage.title",
        ):
            if token not in header_text:
                errors.append(f"site header missing global navigation contract: {token}")
        for legacy_class in (
            "portal-header",
            "portal-header-inner",
            "portal-brand global-brand",
            "portal-primary-nav",
            "portal-stage-link",
            "portal-directory-panel",
        ):
            if legacy_class in header_text:
                errors.append(f"site header retains obsolete portal alias: {legacy_class}")

    style = SOURCE_ROOT / "assets/style.css"
    directory_style = SOURCE_ROOT / "assets/directory.css"
    if style.exists() and directory_style.exists():
        shared_css = style.read_text() + directory_style.read_text()
        for token in (
            'body[data-page-role="tool-project"]',
            'body[data-docs-layout="true"]',
            ".global-nav-menu",
            ".global-nav-visual",
            "calc(var(--nav-order) * 45ms)",
            "@media(min-width:840px) and (max-width:999px)",
            "prefers-reduced-motion:reduce",
            "body .global-brand .portal-brand-mark{color:#10261e;background:#f0f6f3}",
            ".global-stage-value::after",
            "@keyframes global-stage-pulse",
            "@keyframes global-stage-text-flow",
            "@keyframes global-stage-sheen",
            "-webkit-text-fill-color:transparent",
            "background:#fff",
            ".content-split{",
            ".content-split-reverse{",
            ".content-stack",
            ".content-band{",
            ".content-wide",
            ".content-grid{",
            ".content-rows",
            'body:not([data-page-role="portal"]) .page-link:nth-child(2n)',
            'a:visited:not(.portal-button)',
            ".portal-button-primary:visited",
            ".portal-button-secondary:visited",
            '@media(max-width:839px)',
            'body:not([data-page-role="portal"]) .global-directory-panel',
            '.site-header .directory-panel.is-closing nav',
            'html.mobile-directory-open,html.mobile-directory-open body',
            'overscroll-behavior:contain',
        ):
            if token not in shared_css:
                errors.append(f"shared styles missing site-wide design contract: {token}")
        if re.search(r"transition\s*:\s*all\b", shared_css):
            errors.append("shared styles must not use transition: all")
        if re.search(r'\.page-links\s*\{[^}]*background\s*:\s*var\(--portal-line\)', shared_css):
            errors.append("page-link grids must not expose the separator color in empty cells")
        if not re.search(r'body\[data-page-role="tool-project"\]\s+main\s*\{[^}]*overflow\s*:\s*clip', shared_css):
            errors.append("tool project main must preserve the sticky status panel scroll range")
        if "margin-left:300px" in shared_css:
            errors.append("content pages must not reserve a meaningless fixed 300px left gap")
        for legacy_selector in (
            ".portal-header",
            ".portal-header-inner",
            ".portal-brand{",
            ".portal-primary-nav",
            ".portal-nav-link",
            ".portal-stage-link",
            ".portal-directory-panel",
        ):
            if legacy_selector in shared_css:
                errors.append(f"shared styles retain obsolete portal alias: {legacy_selector}")
        for selector in (
            "main>section:not(.project-progress-section):nth-of-type(even)",
            "main>section:has(",
            "ul:has(>li:nth-child(4))",
        ):
            if selector in shared_css:
                errors.append(
                    f"content layout must be explicit instead of inferred by selector: {selector}"
                )

    directory_script = SOURCE_ROOT / "assets/directory.js"
    if directory_script.exists():
        declared = set(HREF_LITERAL.findall(directory_script.read_text()))
        registered_set = set(registered)
        manual_routes = {route for route, path in source_entries if path.suffix == ".md"}
        if not declared <= registered_set:
            errors.append("directory.js contains links outside the formal route registry")
        missing_static = sorted((registered_set - manual_routes) - declared)
        if missing_static:
            errors.append(f"directory.js does not cover non-manual routes: {missing_static}")
    else:
        errors.append("missing assets/directory.js")

    design_routes = {
        "portal": "portal.md",
        "section": "section.md",
        "content": "content.md",
        "tool-project": "tool-project.md",
        "manual": "manual.md",
        "global": "global-shell.md",
        "components": "components-motion.md",
        "images": "images.md",
        "internal-tools": "internal-tools.md",
    }
    design_root = SOURCE_ROOT / "design-system"
    design_index = design_root / "README.md"
    if not design_index.exists():
        errors.append("missing design-system/README.md routing index")
    else:
        design_index_text = design_index.read_text()
        for role, filename in design_routes.items():
            if not (design_root / filename).exists():
                errors.append(f"missing design guidance for {role}: design-system/{filename}")
            if filename not in design_index_text:
                errors.append(f"design routing index does not route {role} to {filename}")

    manual_config = SOURCE_ROOT / "_data/manuals.yml"
    manual_layout = SOURCE_ROOT / "_layouts/manual.html"
    if not manual_config.exists():
        errors.append("missing _data/manuals.yml")
    if not manual_layout.exists():
        errors.append("missing _layouts/manual.html")
    else:
        manual_layout_text = manual_layout.read_text()
        for token in (
            'where: "manual_id", page.manual_id',
            'sort: "manual_order"',
            "manual-generated-index",
            'data-manual-role="previous"',
            'data-manual-role="next"',
        ):
            if token not in manual_layout_text:
                errors.append(f"manual layout missing dynamic contract: {token}")

    manual_records = []
    for path in MANUAL_MARKDOWN_FILES:
        match = FRONT_MATTER.match(path.read_text())
        if match is None:
            continue
        metadata = match.group(1)
        manual_records.append({
            "path": path,
            "manual_id": front_matter_value(metadata, "manual_id"),
            "group": front_matter_value(metadata, "manual_group"),
            "order": front_matter_value(metadata, "manual_order"),
            "is_index": front_matter_value(metadata, "manual_is_index") == "true",
        })
    for manual_id in sorted(set(record["manual_id"] for record in manual_records)):
        records = [record for record in manual_records if record["manual_id"] == manual_id]
        orders = [record["order"] for record in records]
        if len(orders) != len(set(orders)):
            errors.append(f"manual {manual_id}: manual_order values must be unique")
        if sum(record["is_index"] for record in records) != 1:
            errors.append(f"manual {manual_id}: expected exactly one manual_is_index page")
        if manual_config.exists():
            config_text = manual_config.read_text()
            if not re.search(rf"^{re.escape(manual_id)}:\s*$", config_text, re.MULTILINE):
                errors.append(f"manual {manual_id}: missing _data/manuals.yml entry")
            for group in set(record["group"] for record in records):
                if f"    {group}:" not in config_text:
                    errors.append(f"manual {manual_id}: unknown configured group {group}")

    if directory_script.exists():
        directory_text = directory_script.read_text()
        for phrase in PUBLIC_META_PHRASES:
            if phrase in directory_text:
                errors.append(
                    f"directory.js exposes internal production phrase {phrase!r} in visible navigation copy"
                )
        for token in (
            "data-manual-directory-source",
            "readManualDirectory",
            "payload.pages",
            "manualDirectory?.directory",
            "details.open = true;",
            'trigger.setAttribute("aria-expanded", "false")',
            'item.addEventListener("mouseenter"',
            'item.classList.toggle("is-menu-open", expanded)',
            'window.setTimeout(() => setExpanded(true), 40)',
            'window.setTimeout(() => setExpanded(false), 120)',
            'intro.innerHTML = `<small>${group.kicker}</small>',
            'document.addEventListener("pointerdown"',
            'event.key === "Escape"',
            'nextScrollY > previousScrollY + 8',
            'window.setTimeout(finishPanelClose, 180)',
            'document.documentElement.classList.toggle("mobile-directory-open"',
            'setPageScrollLock(true)',
        ):
            if token not in directory_text:
                errors.append(f"directory.js missing dynamic manual contract: {token}")
        if "details.open = containsCurrent || groupIndex === 0;" in directory_text:
            errors.append("desktop documentation rail must not hide non-current groups by default")
        if "item.dataset.navGroup" in directory_text or "link.dataset.navItem" in directory_text:
            errors.append("global navigation must not expose decorative title numbers")
        if "portal-nav-link" in directory_text:
            errors.append("global navigation must not emit the obsolete portal-nav-link alias")

        expected_nav_covers = {
            "background", "architecture", "foundations", "faq",
            "gsir", "gobj", "sso", "components",
            "conform", "inspect", "compile", "link",
            "getting-started", "architecture-guide", "tools-reference",
            "spec-reference", "noemld-manual", "current-stage", "roadmap", "testing",
            "news", "downloads",
        }
        nav_cover_asset = SOURCE_ROOT / "assets/nav-covers.svg"
        if not nav_cover_asset.exists():
            errors.append("missing assets/nav-covers.svg")
        else:
            cover_ids = set(re.findall(
                r'id="nav-cover-([^"]+)"', nav_cover_asset.read_text()
            ))
            if cover_ids != expected_nav_covers:
                errors.append("navigation cover sprite must define 22 unique project covers")
        configured_cover_entries = re.findall(r'cover: "([^"]+)"', directory_text)
        configured_covers = set(configured_cover_entries)
        if len(configured_cover_entries) != 22 or configured_covers != expected_nav_covers:
            errors.append("global navigation entries must route to unique project covers")

    timeline_config = SOURCE_ROOT / "_data/project_timeline.yml"
    timeline_include = SOURCE_ROOT / "_includes/project-timeline.html"
    if not timeline_config.exists():
        errors.append("missing _data/project_timeline.yml")
    else:
        timeline_text = timeline_config.read_text()
        current_id_match = re.search(r"^current_stage_id:\s*([^\s]+)\s*$", timeline_text, re.MULTILINE)
        item_ids = re.findall(r"^  - id:\s*([^\s]+)\s*$", timeline_text, re.MULTILINE)
        item_states = re.findall(r"^    state:\s*([^\s]+)\s*$", timeline_text, re.MULTILINE)
        if current_id_match is None or current_id_match.group(1) not in item_ids:
            errors.append("project timeline current_stage_id must reference an item")
        elif not re.search(
            rf"^  - id:\s*{re.escape(current_id_match.group(1))}\s*$\n    state:\s*current\s*$",
            timeline_text,
            re.MULTILINE,
        ):
            errors.append("project timeline current_stage_id must reference the current item")
        if len(item_ids) != len(set(item_ids)):
            errors.append("project timeline item ids must be unique")
        if len(item_ids) != len(item_states) or item_states.count("current") != 1:
            errors.append("project timeline must define exactly one current state")
        if not set(item_states) <= {"confirmed", "current", "next", "future"}:
            errors.append("project timeline contains an unsupported state")
        if "href: /development/current-stage.html" not in timeline_text:
            errors.append("project timeline header must route to the current stage page")
        for overview_key in (
            "completed_label", "active_label", "planned_label",
            "current_label", "roadmap_label", "roadmap_href",
        ):
            if not re.search(rf"^  {overview_key}:\s*.+$", timeline_text, re.MULTILINE):
                errors.append(f"project timeline overview requires {overview_key}")
        header_value_match = re.search(r"^  value:\s*(.+?)\s*$", timeline_text, re.MULTILINE)
        if header_value_match is None or not 3 <= len(header_value_match.group(1)) <= 4:
            errors.append("project timeline header value must contain three or four characters")
    if not timeline_include.exists():
        errors.append("missing _includes/project-timeline.html")
    else:
        timeline_include_text = timeline_include.read_text()
        for token in (
            "include.timeline",
            "timeline.items",
            "completed_stages.size",
            "planned_stages.size",
            'class="project-progress-summary"',
            'data-stage-id="{{ item.id | escape }}"',
            'data-stage-state="{{ item.state | escape }}"',
        ):
            if token not in timeline_include_text:
                errors.append(f"project timeline include missing contract: {token}")

    current_stage = SOURCE_ROOT / "development/current-stage.html"
    if not current_stage.exists():
        errors.append("missing development/current-stage.html")
    else:
        current_stage_text = current_stage.read_text()
        for token in (
            'timeline_data: "project_timeline"',
            "site.data[page.timeline_data]",
            "current_stage.title",
            'class="current-stage-feature"',
            'class="current-stage-visual"',
            'src="../assets/images/secure-object-core.jpg"',
            'width="1440" height="960"',
            'class="current-stage-panel"',
            'class="project-progress-section"',
            "include project-timeline.html timeline=timeline",
        ):
            if token not in current_stage_text:
                errors.append(f"current stage page missing contract: {token}")
        for forbidden in (
            "当前阶段的进入条件",
            "尚未满足的退出证据",
            "进入下一阶段的判断",
            "时间线不是完成百分比",
        ):
            if forbidden in current_stage_text:
                errors.append(f"current stage page exposes internal workflow copy: {forbidden}")

    image_contracts = {
        "assets/images/secure-object-core.jpg": (400_000, 'src="../assets/images/secure-object-core.jpg"'),
    }
    image_consumers = (SOURCE_ROOT / "index.html").read_text() + (SOURCE_ROOT / "development/current-stage.html").read_text()
    for image_route, (maximum_bytes, source_token) in image_contracts.items():
        image_path = SOURCE_ROOT / image_route
        if not image_path.exists():
            errors.append(f"missing optimized site image: {image_route}")
        elif image_path.stat().st_size > maximum_bytes:
            errors.append(f"site image exceeds {maximum_bytes} bytes: {image_route}")
        if source_token not in image_consumers:
            errors.append(f"site image is not connected to its intended page: {image_route}")

    tool_design = design_root / "internal-tools.md"
    style_text = style.read_text() if style.exists() else ""
    tool_design_text = tool_design.read_text() if tool_design.exists() else ""
    if len(TOOL_IDS) != 23:
        errors.append(f"expected 23 HTML tool project pages, found {len(TOOL_IDS)}")
    for tool_id in TOOL_IDS:
        if (SOURCE_ROOT / "tools" / tool_id / "index.md").exists():
            errors.append(f"tools/{tool_id}/index.md is forbidden; tool project pages remain HTML")
        tool_source = SOURCE_ROOT / "tools" / tool_id / "index.html"
        if tool_source.read_text().count('class="tool-project-body"') != 1:
            errors.append(f"tool project {tool_id} must define one bounded sticky body")
        if f'body[data-tool-id="{tool_id}"]' not in style_text:
            errors.append(f"missing custom visual signature for tool {tool_id}")
        if f"### {tool_id}" not in tool_design_text:
            errors.append(f"missing design guidance for tool {tool_id}")

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
            ["当前状态：已经发布可执行版本，命令行界面、参数和文件扩展名已经确定。"],
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
    registered_rows = [row["route"] for row in route_rows]
    registered = sorted(
        set(registered_rows) | set(read_manual_source_routes())
    )
    actual_routes = [path.relative_to(ROOT).as_posix() for path in HTML_FILES]

    if not route_rows:
        errors.append("sitemap.md has no formal HTML route entries")
    if len(registered_rows) != len(set(registered_rows)):
        errors.append("sitemap.md contains duplicate HTML routes")
    if sorted(registered) != sorted(actual_routes):
        errors.append("sitemap.md routes do not exactly match HTML files")

    sitemap = ROOT / "sitemap.md"
    if not sitemap.exists():
        errors.append("missing public sitemap.md discovery index")
    else:
        sitemap_text = sitemap.read_text()
        if FRONT_MATTER.match(sitemap_text):
            errors.append("sitemap.md must remain a static Markdown file without Front Matter")
        sitemap_routes = set(
            re.findall(r"https://noemion\.github\.io/([A-Za-z0-9_./-]+\.html)", sitemap_text)
        )
        if sitemap_routes != set(registered):
            missing = sorted(set(registered) - sitemap_routes)
            extra = sorted(sitemap_routes - set(registered))
            errors.append(f"sitemap.md route mismatch: missing={missing}, extra={extra}")
        if not SOURCE_ONLY and sitemap_text != SOURCE_SITEMAP.read_text():
            errors.append("the Pages build must copy sitemap.md without Markdown-to-HTML conversion")

    if [row["route"] for row in route_rows if row["kind"] == "portal"] != ["index.html"]:
        errors.append("sitemap.md must register index.html as the only portal")

    section_routes = [row["route"] for row in route_rows if row["kind"] == "section"]
    if sorted(section_routes) != sorted(PORTAL_ROUTES[1:]):
        errors.append("sitemap.md section routes do not match the approved portal architecture")

    home = ROOT / "index.html"
    if home.exists():
        parser = parse(home)
        if parser.h2_texts != HOME_HEADINGS:
            errors.append(
                f"index.html: homepage reasoning sequence must be {HOME_HEADINGS}, "
                f"got {parser.h2_texts}"
            )
        visible_text = normalize_visible_text(
            " ".join("".join(section["text"]) for section in parser.sections)
        )
        for term in ("提示词工程", "Noesis", "Noema", "分析哲学", "工程类比"):
            if term not in visible_text:
                errors.append(f"index.html: homepage must explain {term}")
        home_source = home.read_text()
        if home_source.count('class="portal-chapter-title"') != len(HOME_HEADINGS):
            errors.append("index.html: every homepage chapter heading must use the shared symbolic title treatment")
        for token in (
            "DATAFLOW / ACTIVE",
            "dataflow-lane-source",
            "dataflow-lane-bind",
            "dataflow-lane-reloc",
            "dataflow-lane-verify",
            "portal-arrow-ring",
            "arrow-ring-progress",
        ):
            if token not in home_source:
                errors.append(f"index.html: homepage dataflow visual missing {token}")

    foundations = ROOT / "about/intellectual-foundations.html"
    if foundations.exists():
        parser = parse(foundations)
        breadcrumb = normalize_visible_text("".join(parser.breadcrumb_text))
        breadcrumb_routes = resolved_routes(foundations, parser.breadcrumb_links)
        if (
            parser.page_role != "content"
            or parser.class_counts["breadcrumbs"] != 1
            or breadcrumb_routes != ["index.html", "about/index.html"]
            or not all(label in breadcrumb for label in ("项目", "项目背景", "思想与方法基础"))
        ):
            errors.append("about/intellectual-foundations.html: invalid project / about / current breadcrumbs")
        if parser.h2_texts != INTELLECTUAL_FOUNDATIONS_HEADINGS:
            errors.append(
                "about/intellectual-foundations.html: reasoning sequence must be "
                f"{INTELLECTUAL_FOUNDATIONS_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = normalize_visible_text(
            " ".join("".join(section["text"]) for section in parser.sections)
        )
        for term in (
            "不得直接推出", "思想采用的验证要求", "Source Expression",
            "对象语言", "言语行为", "会话含义",
        ):
            if term not in visible_text:
                errors.append(f"about/intellectual-foundations.html: must preserve {term}")

    for row in route_rows:
        path = ROOT / row["route"]
        if path.exists() and parse(path).page_role != ROLE_BY_KIND[row["kind"]]:
            errors.append(f"{row['route']}: page role does not match registry kind")

    for route in NORMATIVE_ROUTES:
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing normative page {route}")
            continue
        parser = parse(path)
        visible_text = normalize_visible_text(
            " ".join("".join(section["text"]) for section in parser.sections)
        )
        for term in ("直白解释", "已确认原则", "设计提案", "开放问题", "必须", "不得"):
            if term not in visible_text:
                errors.append(f"{route}: normative page must preserve {term}")

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
        if parser.tool_id != tool:
            errors.append(f"{row['route']}: body data-tool-id must be {tool!r}")
        if parser.class_counts["tool-project-body"] != 1:
            errors.append(f"{row['route']}: must preserve one bounded sticky tool body")
        status_sections = [section for section in parser.sections if section["heading"] == "当前状态"]
        status_texts = ["".join(section["text"]) for section in status_sections]
        contract_errors = validate_tool_project_contract(
            parser.h2_texts,
            status_texts,
            parser.class_counts,
        )
        errors.extend(f"{row['route']}: {error}" for error in contract_errors)
        resource_sections = [
            section for section in parser.sections if section["heading"] == "相关资源"
        ]
        if len(resource_sections) == 1:
            resource_children = resource_sections[0]["direct_children"]
            if (
                len(resource_children) != 2
                or resource_children[0][0] != "h2"
                or resource_children[1][0] != "div"
                or "page-links" not in resource_children[1][1]
            ):
                errors.append(
                    f"{row['route']}: related resources must end with the page-links group "
                    "and must not contain an orphan trailing paragraph"
                )

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
            parser.scoped_links["manual-index-links"],
        )
        expected_guides = [
            entry["route"] for entry in read_manual_source_entries("docs")
            if not entry["is_index"]
        ]
        if guide_links != expected_guides:
            errors.append("docs index cards must match Markdown guide order")

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
            " ".join([
                "".join(parser.manual_article_text),
                *("".join(section["text"]) for section in parser.sections),
            ])
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

    if len(actual_routes) != len(registered):
        errors.append(
            f"expected {len(registered)} final HTML routes, found {len(actual_routes)}"
        )

    downloads = ROOT / "downloads/index.html"
    if downloads.exists():
        text = downloads.read_text()
        if 'href=""' in text or 'href="#"' in text or "javascript:" in text:
            errors.append("downloads page contains a fake or empty download link")
        if 'data-resource-state="unreleased"' not in text:
            errors.append("downloads page must expose an explicit unreleased state")

    current_stage_output = ROOT / "development/current-stage.html"
    if current_stage_output.exists():
        current_stage_output_text = current_stage_output.read_text()
        rendered_stages = re.findall(
            r'<li data-stage-id="([^"]+)" data-stage-state="([^"]+)">.*?<h3>([^<]+)</h3>',
            current_stage_output_text,
            re.DOTALL,
        )
        timeline_source_text = (SOURCE_ROOT / "_data/project_timeline.yml").read_text()
        configured_stages = re.findall(
            r"^  - id:\s*([^\s]+)\s*$\n    state:\s*([^\s]+)\s*$\n    label:.*$\n    title:\s*(.+?)\s*$",
            timeline_source_text,
            re.MULTILINE,
        )
        if rendered_stages != configured_stages:
            errors.append("current stage output must match configured timeline order, states, and titles")
        rendered_counts_match = re.search(
            r'<dl class="progress-counts">(.*?)</dl>',
            current_stage_output_text,
            re.DOTALL,
        )
        rendered_counts = (
            [int(value) for value in re.findall(r"<dd>(\d+)</dd>", rendered_counts_match.group(1))]
            if rendered_counts_match is not None
            else []
        )
        expected_counts = [
            sum(state == "confirmed" for _, state, _ in configured_stages),
            sum(state == "current" for _, state, _ in configured_stages),
            sum(state in {"next", "future"} for _, state, _ in configured_stages),
        ]
        if rendered_counts != expected_counts:
            errors.append("current stage overview counts must match configured timeline states")
        configured_current = [stage for stage in configured_stages if stage[1] == "current"]
        current_title = configured_current[0][2] if len(configured_current) == 1 else ""
        configured_header_value_match = re.search(
            r"^  value:\s*(.+?)\s*$", timeline_source_text, re.MULTILINE
        )
        configured_header_value = (
            configured_header_value_match.group(1)
            if configured_header_value_match is not None
            else ""
        )
        for token in (
            'data-timeline-id="noemion-project-progress"',
            f'aria-label="当前阶段：{current_title}"',
            'href="/development/current-stage.html"',
            f'<strong class="global-stage-value" data-stage-value="{configured_header_value}"><span class="global-stage-progress" aria-hidden="true"></span><span class="global-stage-text">{configured_header_value}</span></strong>',
            'class="project-progress-summary"',
            'class="progress-counts"',
            "项目状态概览",
            "正在进行",
            "后续规划",
        ):
            if token not in current_stage_output_text:
                errors.append(f"current stage output missing configured value: {token}")
        for forbidden in (
            "当前阶段的进入条件",
            "尚未满足的退出证据",
            "进入下一阶段的判断",
            "时间线不是完成百分比",
        ):
            if forbidden in current_stage_output_text:
                errors.append(f"current stage output exposes internal workflow copy: {forbidden}")

    directory_script = ROOT / "assets/directory.js"
    catalog_script = ROOT / "assets/catalog.js"
    favicon = ROOT / "assets/favicon.svg"
    if not directory_script.exists():
        errors.append("missing assets/directory.js")
    if not catalog_script.exists():
        errors.append("missing assets/catalog.js")
    if not favicon.exists():
        errors.append("missing assets/favicon.svg")

    for path in HTML_FILES:
        text = path.read_text()
        parser = parse(path)
        rel = path.relative_to(ROOT).as_posix()
        errors.extend(validate_public_html(rel, text))
        if RAW_AMP.search(text):
            errors.append(f"{rel}: contains an unescaped ampersand")
        if parser.directory_containers != 1:
            errors.append(f"{rel}: expected one data-directory nav")
        for section in parser.sections:
            section_text = normalize_visible_text("".join(section["text"]))
            if section["heading"] and len(section_text) < 24:
                errors.append(
                    f"{rel}: section {section['heading']!r} is too thin for public documentation"
                )
        if parser.skip_links != 1 or parser.main_targets != 1:
            errors.append(f"{rel}: missing unique skip link or main target")
        stylesheet_paths = [urlsplit(stylesheet).path for stylesheet in parser.stylesheets]
        if len(parser.stylesheets) != 2 or not stylesheet_paths[0].endswith("assets/style.css") or not stylesheet_paths[1].endswith("assets/directory.css"):
            errors.append(f"{rel}: expected versioned style.css and directory.css stylesheets")
        for stylesheet in parser.stylesheets:
            if not urlsplit(stylesheet).query:
                errors.append(f"{rel}: shared stylesheet must include a build cache key: {stylesheet}")
        directory_scripts = [
            script
            for script in parser.scripts
            if urlsplit(script).path.endswith("assets/directory.js")
        ]
        if len(directory_scripts) != 1:
            errors.append(f"{rel}: missing shared directory script")
        elif not urlsplit(directory_scripts[0]).query:
            errors.append(f"{rel}: shared directory script must include a build cache key")
        for script in parser.scripts:
            if not urlsplit(script).query:
                errors.append(f"{rel}: shared script must include a build cache key: {script}")
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
        declared = set(HREF_LITERAL.findall(directory_source))
        registered_set = set(registered)
        manual_routes = {
            route for route in registered
            if route.startswith("docs/") or re.match(r"^tools/[^/]+/docs/", route)
        }
        if not declared <= registered_set:
            errors.append("directory.js contains links outside the formal route registry")
        missing_static = sorted((registered_set - manual_routes) - declared)
        if missing_static:
            errors.append(f"directory.js does not cover non-manual routes: {missing_static}")
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
                ["about/intellectual-foundations.html", "project"],
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
                "const { isDirectoryItemActive, resolveDirectoryModule, createManualDirectory } = api;"
                "const cases = JSON.parse(process.argv[2]);"
                "const active = cases.map(([itemHref, target, current]) => "
                "isDirectoryItemActive(itemHref, target, current));"
                "const moduleCases = JSON.parse(process.argv[3]);"
                "const modules = moduleCases.map(([route]) => resolveDirectoryModule(route));"
                "const manual = createManualDirectory({"
                "manuals:{demo:{kicker:'Docs',title:'Demo',root:'/docs/index.html',"
                "parent_url:'/index.html',parent_label:'Home',groups:{start:{label:'Start',order:1}}}},"
                "pages:[{manualId:'demo',group:'start',order:2,route:'docs/new.html',label:'New'},"
                "{manualId:'demo',group:'start',order:0,route:'docs/index.html',label:'Home'}]},"
                "'docs/new.html');"
                "process.stdout.write(JSON.stringify({active, modules, manual}));"
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
                manual_items = actual["manual"]["directory"]["groups"][0]["items"]
                if actual["manual"]["moduleKey"] != "manual-demo" or [
                    item["href"] for item in manual_items
                ] != ["docs/index.html", "docs/new.html"]:
                    errors.append("dynamic manual directory does not sort new Markdown pages")

    noemld_index = ROOT / NOEMLD_DOC_ORDER[0]
    if noemld_index.exists():
        parser = parse(noemld_index)
        toc_routes = resolved_routes(noemld_index, parser.scoped_links["manual-index-links"])
        expected_topics = [
            entry["route"] for entry in read_manual_source_entries("noemld")
            if not entry["is_index"]
        ]
        if toc_routes != expected_topics:
            errors.append("noemld index manual TOC does not match Markdown topic order")

    for index, route in enumerate(NOEMLD_DOC_ORDER[1:], start=1):
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing noemld topic page {route}")
            continue
        if NUMBERED_NAME.search(route):
            errors.append(f"{route}: numbered topic filename is forbidden")
        parser = parse(path)
        if parser.tool_id != "noemld":
            errors.append(f"{route}: tool manual must inherit data-tool-id='noemld'")
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
        "@keyframes portal-datafield-shift",
        "@keyframes portal-data-packet",
        ".dataflow-field",
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
