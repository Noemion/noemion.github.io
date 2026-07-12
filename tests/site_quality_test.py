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
    if "_site" not in path.parts
    and "vendor" not in path.parts
    and not any(part.startswith("_") for part in path.parts)
)
MANUAL_MARKDOWN_FILES = sorted(
    [*SOURCE_ROOT.glob("docs/*.md"), *SOURCE_ROOT.glob("endem/docs/*.md")]
)
SOURCE_PAGE_FILES = sorted([*SOURCE_HTML_FILES, *MANUAL_MARKDOWN_FILES])
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
    "docs/index.html",
    "downloads/index.html",
    "faq/index.html",
    "development/index.html",
    "news/index.html",
]
APPLICATION_ROUTES = ["endem/index.html"]
MANUAL_ROUTE_ORDERS = {
    "endem": [
        "endem/docs/index.html",
        "endem/docs/format.html",
        "endem/docs/binding.html",
        "endem/docs/safety.html",
        "endem/docs/running.html",
        "endem/docs/reference.html",
    ],
}
REQUIRED_CORE_ROUTES = {
    "endem/index.html",
    *MANUAL_ROUTE_ORDERS["endem"],
    "specifications/endem.html",
    "specifications/weave.html",
    "specifications/witness.html",
    "architecture/endem-lifecycle.html",
    "components/core.html",
    "components/reader.html",
    "components/runner.html",
}
DOC_GUIDE_ORDER = [
    "docs/getting-started.html",
    "docs/installation-and-usage.html",
    "docs/architecture-guide.html",
    "docs/development-guide.html",
    "docs/endem-reference.html",
    "docs/specifications-reference.html",
]
DOC_GUIDE_HEADINGS = {
    "docs/getting-started.html": [
        "从这里开始", "五组投影", "四个名词", "一个应用", "推荐阅读路径", "当前状态",
    ],
    "docs/installation-and-usage.html": [
        "当前可用性", "计划中的使用流程", "发布原则", "命名发布门",
    ],
    "docs/architecture-guide.html": [
        "最小系统图", "三个实现域", "形成与语义确认", "组合与发布", "装载与运行", "信任不是单一分数",
    ],
    "docs/development-guide.html": [
        "第一阶段范围", "规范与 ADR 先行", "实现工作流", "建议仓库边界", "审查清单", "模型与协议",
    ],
    "docs/endem-reference.html": [
        "应用总览", "Core 子命令", "see 的独立性", "run 的隔离性", "不建设独立模型平台",
    ],
    "docs/specifications-reference.html": [
        "权威顺序", "Endem", "Weave", "Frame 与 Witness", "ADR 与开放问题",
    ],
}
HOME_HEADINGS = [
    "不是给旧对象格式换前缀",
    "五个短词形成命题投影",
    "只保留有独立生命周期的名词",
    "一个入口不等于一个信任域",
    "先证明最小纵向切片",
    "借鉴工具链思想，不复制工具数量",
    "继续阅读",
]
INTELLECTUAL_FOUNDATIONS_HEADINGS = [
    "为什么阅读这些著作",
    "研究方法与采用边界",
    "核心思想与工程问题",
    "Noemion 名称怎样形成",
    "《逻辑哲学论》与工程设计相关的命题",
    "Endem 语义核与后续验证",
    "核心书目与资源状态",
    "思想采用的验证要求",
]
ROLE_BY_KIND = {
    "portal": "portal",
    "section": "section",
    "content": "content",
    "tool": "tool-project",
    "app": "tool-project",
    "docs": "docs-index",
    "topic": "docs-topic",
}
SITE_MODULES = {
    "project", "about", "architecture", "specifications", "components",
    "endem", "docs", "development", "resources", "support",
}
APPLICATION_PROJECT_SECTIONS = [
    "它解决什么问题",
    "当前状态",
    "它怎样工作",
    "它读取什么，产生什么",
    "它不会做什么",
    "继续阅读",
]
APPLICATION_STATUS_DISCLOSURES = (
    "设计阶段",
    "尚未提供可执行程序",
    "参数",
    "稳定 ABI",
    "尚未冻结",
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
UNCLEAR_CHINESE_UI_TERMS = re.compile(
    r"架构决定|文档中心|文档首页|架构指南|工具参考(?!指南)|"
    r"规范登记(?:页)?|架构入口|使用与获取|新闻与进展|实施路线图|"
    r"路线图语境|黄金圈定位|第一批检查点|当前设计：|"
    r"尚待确定：|概要设计："
)
LEGACY_PUBLIC_TERMS = re.compile(
    r"\b(?:G(?:SIR|OBJ|SL)|S(?:SO)|N(?:SFE|IR|OBJ|SL)|H(?:OBJ))\b|"
    r"\bNo(?:esis|ema)\b|\b(?:Hori(?:zon)|Fulfill(?:ment))\b|"
    r"\bnoem(?!ion\b)[a-z]+\b|\b(?:morph(?:e)|theor(?:ia)|synth(?:esis))\b|"
    r"(?:compiler-core|linker-loader|nsfe|gsir|gobj|sso|noem(?:a)-ir|"
    r"noem(?:a)-object|horizon-object|noesis-core|noem(?:a)-object-system|"
    r"horizon-engine|agent-harness|fulfillment-runtime|noem(?:a)-lifecycle)\.html|"
    r"(?:^|[/\"'])tools/"
)
LEGACY_ADR_ALLOWLIST = re.compile(
    r"^design-system/adr-000[1-7]-[^/]+\.md$"
)
NORMATIVE_ROUTES = (
    "specifications/endem.html",
    "specifications/weave.html",
    "specifications/witness.html",
)
CONTENT_LAYOUT_ROUTES = (
    "about/background.html",
    "about/intellectual-foundations.html",
    "architecture/endem-lifecycle.html",
    "architecture/decisions.html",
    "architecture/adr-0008-endem-system.html",
    "architecture/adr-0009-propositional-kernel.html",
    "architecture/open-questions.html",
    "components/core.html",
    "components/reader.html",
    "components/runner.html",
    "development/implementation-roadmap.html",
    "development/testing.html",
    "specifications/endem.html",
    "specifications/weave.html",
    "specifications/witness.html",
)
CONTENT_LAYOUT_CLASSES = {
    "content-split",
    "content-stack",
    "content-band",
    "content-wide",
    "content-grid",
    "content-rows",
}

REQUIRED_ARCHITECTURE_ROUTES = {
    "architecture/decisions.html": "architecture/index.html",
    "components/runner.html": "components/index.html",
}

SYSTEM_BOUNDARY_CONTRACTS = {
    "architecture/index.html": {
        "required": (
            "Endem",
            "Weave",
            "Witness",
            "Frame",
            "Core",
            "Reader",
            "Runner",
            "生产验证和",
            "不共享",
            "模型候选",
            "不可信",
            "最终决定",
        ),
        "forbidden_patterns": (
            r"每一步只能增加(?:信任|可信度)",
            r"信任(?:必须|只能|会)?单调(?:增加|提高|上升)",
        ),
    },
    "architecture/decisions.html": {
        "required": (
            "外部签名",
            "候选不等于事实",
            "能力声明不等于句柄",
            "Witness 不等于验收",
        ),
    },
    "components/core.html": {
        "required": (
            "Core",
            "Endem",
            "确定性",
            "模型",
            "不可信",
            "checked arithmetic",
        ),
    },
    "components/reader.html": {
        "required": (
            "Reader",
            "see",
            "独立",
            "只读",
            "生产解析器",
            "不共享",
            "checked arithmetic",
        ),
    },
    "components/runner.html": {
        "required": (
            "Runner",
            "Frame",
            "run",
            "Capability Request",
            "Witness",
            "accepted",
            "pending-review",
            "决定权威",
            "模型",
            "不可信",
        ),
    },
    "specifications/endem.html": {
        "required": (
            ".endem",
            "say",
            "mean",
            "case",
            "when",
            "open",
            "no-sense",
            "unknown",
            "logical_form",
            "checked arithmetic",
        ),
    },
    "specifications/weave.html": {
        "required": (
            "Weave",
            "局部命名空间",
            "导入",
            "导出",
            "必需依赖",
            "可选依赖",
        ),
        "forbidden_patterns": (
            r"按强定义、弱定义",
            r"弱引用无定义",
        ),
    },
    "specifications/witness.html": {
        "required": (
            "Witness",
            "subject",
            "claim",
            "basis",
            "strength",
            "integrity",
            "证据闭包",
            "最终决定",
        ),
    },
    "endem/docs/safety.html": {
        "required": (
            "checked arithmetic",
            "see",
            "独立 Reader",
            "生产 Reader",
            "不可信",
        ),
    },
    "endem/docs/running.html": {
        "required": (
            "Frame",
            "外部签名",
            "私钥始终留在外部签名系统",
            "Signature Envelope",
            "Witness",
            "accepted",
            "pending-review",
            "决定权威",
        ),
    },
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
        self.site_module = None
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
            self.site_module = data.get("data-site-module")
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
        elif route == "endem/index.html":
            kind = "app"
            parent = "index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        elif route == "endem/docs/index.html":
            kind = "docs"
            parent = "endem/index.html"
            order = 0
        elif re.fullmatch(r"endem/docs/[^/]+\.html", route):
            kind = "topic"
            parent = "endem/docs/index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
        elif route in PORTAL_ROUTES[1:]:
            kind = "section"
            parent = "index.html"
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


def expected_manual_roles(manual_id, index):
    routes = MANUAL_ROUTE_ORDERS[manual_id]
    roles = {
        "previous": "/" + routes[index - 1],
        "up": f"/{manual_id}/docs/index.html",
        "index": "/" + routes[-1],
    }
    if index + 1 < len(routes):
        roles["next"] = "/" + routes[index + 1]
    return roles


def normalize_visible_text(text):
    return " ".join(text.split())


def validate_required_text_contracts(root):
    errors = []
    for route, contract in SYSTEM_BOUNDARY_CONTRACTS.items():
        path = root / route
        if not path.exists() and root == SOURCE_ROOT:
            for manual_source in MANUAL_MARKDOWN_FILES:
                source_match = FRONT_MATTER.match(manual_source.read_text())
                if source_match is None:
                    continue
                permalink = front_matter_value(source_match.group(1), "permalink")
                if permalink and permalink.lstrip("/") == route:
                    path = manual_source
                    break
        if not path.exists():
            errors.append(f"missing system-closure page {route}")
            continue
        text = path.read_text()
        for token in contract.get("required", ()):
            if token not in text:
                errors.append(f"{route}: missing system-closure contract {token!r}")
        for pattern in contract.get("required_patterns", ()):
            if re.search(pattern, text) is None:
                errors.append(
                    f"{route}: missing system-closure pattern {pattern!r}"
                )
        for pattern in contract.get("forbidden_patterns", ()):
            if re.search(pattern, text):
                errors.append(
                    f"{route}: contradicts system-closure contract with {pattern!r}"
                )
    return errors


def validate_readability_behavior_contracts(root):
    errors = []
    directory_script = root / "assets" / "directory.js"
    style = root / "assets" / "style.css"
    directory_style = root / "assets" / "directory.css"

    if directory_script.exists():
        directory_text = directory_script.read_text()
        for token in (
            'document.querySelectorAll(".manual-article table")',
            'wrapper.className = "table-wrap manual-table-wrap"',
            'contentMain.querySelectorAll(":scope > section > h2")',
            "contentHeadings.length >= 6",
            'outline.className = "page-outline"',
            'outline.setAttribute("aria-label", "章节导航")',
            'contentMain.querySelector(":scope > .hero")',
            'insertAdjacentElement("afterend", outline)',
            '{ href: "architecture/index.html", label: "架构设计" }',
            '{ href: "architecture/decisions.html", label: "架构决策" }',
            'title: "指南与参考"',
            '{ href: "docs/architecture-guide.html", label: "架构设计指南" }',
            '{ href: "docs/endem-reference.html", label: "Endem 应用参考" }',
            '{ href: "docs/specifications-reference.html", label: "规范参考指南" }',
            '{ href: "news/index.html", label: "项目动态" }',
            '{ href: "faq/index.html", label: "常见问题" }',
            '{ href: "development/implementation-roadmap.html", label: "开发路线图" }',
        ):
            if token not in directory_text:
                errors.append(
                    f"directory.js missing readability behavior contract: {token}"
                )
    else:
        errors.append("missing assets/directory.js")

    if style.exists() and directory_style.exists():
        style_text = style.read_text()
        directory_text = directory_style.read_text()
        css_patterns = {
            "docs content must become a centered single column from 1217px": (
                style_text,
                r"@media\(min-width:1000px\)\s+and\s+\(max-width:1217px\)\s*\{"
                r"[^}]*body\[data-docs-layout=\"true\"\]\s+main,"
                r"\s*body\[data-docs-layout=\"true\"\]\s+\.site-footer\s*\{"
                r"[^}]*width:min\(1000px,calc\(100%\s*-\s*36px\)\)"
            ),
            "documentation rail must disappear at 1217px": (
                directory_text,
                r"@media\(max-width:1217px\)\s*\{\s*\.docs-rail\s*\{\s*display:none"
            ),
            "project progress summary must remain sticky on desktop": (
                style_text,
                r"\.project-progress-summary\s*\{[^}]*position:sticky;[^}]*top:88px"
            ),
            "FAQ answers must preserve the readable line length": (
                style_text,
                r"\.faq-list\s+details>p\s*\{[^}]*max-width:760px;"
                r"[^}]*font-size:17px;[^}]*line-height:1\.75"
            ),
            "mobile manual navigation targets must be at least 44px square": (
                style_text,
                r"\.manual-nav\s+a\s*\{[^}]*min-width:44px;"
                r"[^}]*min-height:44px"
            ),
        }
        for label, (css_text, pattern) in css_patterns.items():
            if re.search(pattern, css_text, re.DOTALL) is None:
                errors.append(f"shared styles missing readability contract: {label}")
    else:
        if not style.exists():
            errors.append("missing assets/style.css")
        if not directory_style.exists():
            errors.append("missing assets/directory.css")
    return errors


def validate_public_html(route, text):
    errors = []
    for phrase in PUBLIC_META_PHRASES:
        if phrase in text:
            errors.append(f"{route}: public HTML exposes internal production phrase {phrase!r}")
    unclear_match = UNCLEAR_CHINESE_UI_TERMS.search(text)
    if unclear_match:
        errors.append(
            f"{route}: retains unclear Chinese information-architecture term "
            f"{unclear_match.group(0)!r}"
        )
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


def validate_legacy_source_vocabulary():
    errors = []
    skipped_parts = {".git", "_site", "vendor", ".bundle"}
    for path in SOURCE_ROOT.rglob("*"):
        if not path.is_file() or skipped_parts.intersection(path.parts):
            continue
        relative = path.relative_to(SOURCE_ROOT).as_posix()
        if LEGACY_ADR_ALLOWLIST.fullmatch(relative):
            continue
        legacy_path_match = LEGACY_PUBLIC_TERMS.search(relative)
        if legacy_path_match:
            errors.append(
                f"{relative}: legacy vocabulary remains in path "
                f"{legacy_path_match.group(0)!r}"
            )
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        legacy_text_match = LEGACY_PUBLIC_TERMS.search(text)
        if legacy_text_match:
            errors.append(
                f"{relative}: legacy vocabulary remains outside superseded ADRs "
                f"{legacy_text_match.group(0)!r}"
            )
    return errors


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
    errors.extend(validate_legacy_source_vocabulary())
    ruby_version = SOURCE_ROOT / ".ruby-version"
    gem_lock = SOURCE_ROOT / "Gemfile.lock"
    gitignore = SOURCE_ROOT / ".gitignore"
    pages_workflow = SOURCE_ROOT / ".github" / "workflows" / "pages.yml"
    if not ruby_version.exists() or ruby_version.read_text().strip() != "3.4.10":
        errors.append(".ruby-version must pin the local Jekyll build baseline to 3.4.10")
    if not gem_lock.exists() or "BUNDLED WITH\n   2.6.9" not in gem_lock.read_text():
        errors.append("Gemfile.lock must pin Bundler 2.6.9 for the local build baseline")
    if gitignore.exists() and re.search(r"^Gemfile\.lock$", gitignore.read_text(), re.MULTILINE):
        errors.append(".gitignore must not ignore the tracked Jekyll application lockfile")
    if not pages_workflow.exists():
        errors.append("missing .github/workflows/pages.yml")
    else:
        workflow_text = pages_workflow.read_text()
        for script in ("assets/directory.js", "assets/theme.js"):
            if f"node --check {script}" not in workflow_text:
                errors.append(f"Pages workflow must syntax-check {script}")
        action_refs = re.findall(
            r"uses:\s+([A-Za-z0-9_-]+/[A-Za-z0-9_-]+)@([^\s#]+)", workflow_text
        )
        expected_actions = {
            "actions/checkout",
            "ruby/setup-ruby",
            "actions/configure-pages",
            "actions/upload-pages-artifact",
            "actions/deploy-pages",
        }
        if {action_name for action_name, _ in action_refs} != expected_actions:
            errors.append("Pages workflow must declare exactly the five reviewed build and deploy Actions")
        for action_name, action_ref in action_refs:
            if not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                errors.append(f"Pages workflow must pin {action_name} to a full commit SHA")
        for workflow_contract in (
            "bundler-cache: true",
            'bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"',
            "JEKYLL_ENV: production",
        ):
            if workflow_contract not in workflow_text:
                errors.append(f"Pages workflow missing locked build contract: {workflow_contract}")
        if "actions/jekyll-build-pages" in workflow_text:
            errors.append("Pages workflow must not use the implicit Jekyll dependency environment")
        dependabot = SOURCE_ROOT / ".github" / "dependabot.yml"
        if not dependabot.exists() or "package-ecosystem: github-actions" not in dependabot.read_text():
            errors.append("Dependabot must track immutable GitHub Actions pins")
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
    missing_core_routes = sorted(REQUIRED_CORE_ROUTES - set(source_routes))
    if missing_core_routes:
        errors.append(f"missing required Endem topology routes: {missing_core_routes}")
    for route, parent in REQUIRED_ARCHITECTURE_ROUTES.items():
        row = registry.get(route)
        if row is None or row["kind"] != "content" or row["parent"] != parent:
            errors.append(
                f"{route}: must be registered as content under {parent}"
            )
    errors.extend(validate_required_text_contracts(SOURCE_ROOT))
    errors.extend(validate_readability_behavior_contracts(SOURCE_ROOT))

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
        legacy_match = LEGACY_PUBLIC_TERMS.search(body)
        if legacy_match:
            errors.append(f"{route}: retains obsolete public name {legacy_match.group(0)!r}")
        if re.search(r"[\u4e00-\u9fff] +[\u4e00-\u9fff]", body):
            errors.append(f"{route}: contains broken spacing inside Chinese prose")
        if "****" in body:
            errors.append(f"{route}: contains an empty emphasis marker")
        for obsolete_phrase in ("设计提案", "未来阶段", "阶段门", "证据门", "退出证据", "放行"):
            if obsolete_phrase in body:
                errors.append(f"{route}: retains internal or obsolete status wording {obsolete_phrase!r}")
        if re.search(r"供[^。；<\n]{0,40}消费", body):
            errors.append(f"{route}: uses mechanical '供...消费' wording instead of naming the reader")
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
            normalized_headings = [heading.replace("`", "") for heading in headings]
            if route in DOC_GUIDE_HEADINGS and normalized_headings != DOC_GUIDE_HEADINGS[route]:
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
            "{{ '/assets/style.css' | relative_url }}",
            "{{ '/assets/directory.css' | relative_url }}",
            "{{ '/assets/theme.js' | relative_url }}",
            "{{ '/assets/directory.js' | relative_url }}",
            "site.github.build_revision",
            "?v={{ asset_version | escape }}",
            'data-page-role="{{ page.page_role }}"',
            'data-site-module="{{ page_site_module }}"',
            "page_site_module = 'resources'",
            "page_site_module = 'support'",
            "page_description = page.summary | default: page.description | default: site.description",
            '<meta name="description"',
            '<link rel="canonical"',
            '<meta property="og:title"',
            '<meta property="og:url"',
            '<meta name="twitter:card" content="summary">',
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

    if footer.exists():
        footer_text = footer.read_text()
        if "site-footer-meta" in footer_text:
            errors.append("site footer retains obsolete trailing status band")
        for token in (
            "site-footer-grid",
            "site-footer-bottom",
            "site-footer-links",
            "data-theme-picker",
            "data-theme-trigger",
            "data-theme-menu",
            'data-theme-option="light"',
            'data-theme-option="dark"',
            'data-theme-option="system"',
            "sitemap.md",
            "Browse All",
            "Documentation",
            "Endem",
            "Development",
        ):
            if token not in footer_text:
                errors.append(f"site footer missing global discovery/theme contract: {token}")

    theme_script = SOURCE_ROOT / "assets/theme.js"
    if not theme_script.exists():
        errors.append("missing assets/theme.js")
    else:
        theme_text = theme_script.read_text()
        for token in (
            'const STORAGE_KEY = "noemion-theme"',
            'window.localStorage.setItem(STORAGE_KEY, selected)',
            'window.localStorage.getItem(STORAGE_KEY)',
            'window.matchMedia("(prefers-color-scheme: dark)")',
            'root.dataset.resolvedTheme = resolved',
            'root.style.colorScheme = resolved',
            'role="menuitemradio"',
            'event.key === "Escape"',
            'event.key === "ArrowDown"',
        ):
            if token not in theme_text and token not in footer.read_text():
                errors.append(f"theme picker missing behavior contract: {token}")

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
            ".global-stage-progress::after",
            "width:38px;height:4px",
            "@keyframes global-stage-progress-loop",
            ".global-stage-progress::after{animation:none!important;opacity:1;transform:translateX(108%) scaleX(.74)}",
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
            'html.mobile-directory-open body',
            'position:fixed',
            'overscroll-behavior:contain',
            ':root[data-resolved-theme="dark"]',
            ".site-footer-grid",
            ".site-theme-trigger",
            '.site-theme-menu[data-state="open"]',
            ".theme-icon-sun",
            ".theme-icon-moon",
            'body[data-site-module="about"]',
            'body[data-site-module="architecture"]',
            'body[data-site-module="specifications"]',
            'body[data-site-module="components"]',
            'body[data-site-module="tools"]',
            'body[data-site-module="docs"]',
            'body[data-site-module="development"]',
            'body[data-site-module="resources"]',
            'body[data-site-module="support"]',
            "clip-path:var(--module-hero-clip)",
            "clip-path:var(--module-card-clip)",
            "radial-gradient(circle at var(--module-node-1)",
            'body[data-docs-layout="true"] .hero::before{',
            "clip-path:polygon(0 0,74% 0,100% 26%,100% 100%,0 100%)",
        ):
            if token not in shared_css:
                errors.append(f"shared styles missing site-wide design contract: {token}")
        if re.search(r"transition\s*:\s*all\b", shared_css):
            errors.append("shared styles must not use transition: all")
        if re.search(r'\.page-links\s*\{[^}]*background\s*:\s*var\(--portal-line\)', shared_css):
            errors.append("page-link grids must not expose the separator color in empty cells")
        if not re.search(r'body\[data-page-role="tool-project"\]\s+main\s*\{[^}]*overflow\s*:\s*clip', shared_css):
            errors.append("tool project main must preserve the sticky status panel scroll range")
        if not re.search(r'body:not\(\[data-page-role="portal"\]\)\s+main\s*\{[^}]*overflow\s*:\s*clip', shared_css):
            errors.append("non-portal main must not create a scroll container that disables sticky summaries")
        docs_base_index = shared_css.find('body[data-docs-layout="true"] main{')
        docs_medium_index = shared_css.rfind('@media(min-width:1000px) and (max-width:1217px)')
        if docs_base_index < 0 or docs_medium_index < docs_base_index:
            errors.append("1000-1217px documentation override must follow the base desktop docs layout")
        if "margin-left:300px" in shared_css:
            errors.append("content pages must not reserve a meaningless fixed 300px left gap")
        for obsolete_stage_motion in (
            "global-stage-pulse",
            "global-stage-text-flow",
            "global-stage-sheen",
        ):
            if obsolete_stage_motion in shared_css:
                errors.append(
                    f"shared styles retain obsolete stage animation: {obsolete_stage_motion}"
                )
        if re.search(
            r'body\[data-docs-layout="true"\]\s+\.hero::before,\s*'
            r'body\[data-docs-layout="true"\]\s+\.hero::after\s*\{display:none\}',
            shared_css,
        ):
            errors.append("documentation heroes must preserve their folded-page geometry")
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
        "geometric-layouts": "geometric-layouts.md",
        "philosophical-visual-language": "philosophical-visual-language.md",
    }
    design_root = SOURCE_ROOT / "design-system"
    protocol_reference_files = [*SOURCE_PAGE_FILES, *design_root.glob("*.md")]
    for protocol_reference_file in protocol_reference_files:
        if "a2a-protocol.org/latest/" in protocol_reference_file.read_text():
            errors.append(
                f"{protocol_reference_file.relative_to(SOURCE_ROOT)}: A2A evidence must use a versioned specification URL"
            )
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
    manual_directory_data = SOURCE_ROOT / "_includes/manual-directory-data.html"
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
    if not manual_directory_data.exists():
        errors.append("missing _includes/manual-directory-data.html")
    else:
        manual_directory_text = manual_directory_data.read_text()
        if 'sort: "permalink"' not in manual_directory_text:
            errors.append(
                "manual directory data must use the unique permalink as its stable build order"
            )
        if 'sort: "manual_order"' in manual_directory_text:
            errors.append(
                "manual directory data must not sort unrelated manuals by colliding manual_order values"
            )

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
            'document.documentElement.classList.add("mobile-directory-open")',
            'document.documentElement.style.setProperty("--mobile-directory-scroll-top"',
            'document.addEventListener("wheel", containOpenMenuGesture, { passive: false })',
            'document.addEventListener("touchmove", containOpenMenuGesture, { passive: false })',
            'window.scrollTo(0, lockedScrollY)',
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
            "endem-spec", "weave", "witness", "components",
            "endem", "see", "format", "run",
            "getting-started", "architecture-guide", "application-reference",
            "spec-reference", "endem-manual", "current-stage", "roadmap", "testing",
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
        if (
            header_value_match is None
            or not header_value_match.group(1).endswith("阶段")
            or len(header_value_match.group(1)) > 16
        ):
            errors.append("project timeline header value must remain concise and end with 阶段")
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
            'src="../assets/images/secure-object-core.svg"',
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
        "assets/images/secure-object-core.svg": (20_000, 'src="../assets/images/secure-object-core.svg"'),
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
        if image_path.suffix == ".svg" and image_path.exists():
            svg_text = image_path.read_text()
            if 'width="1440" height="960" viewBox="0 0 1440 960"' not in svg_text:
                errors.append(f"site SVG must preserve its declared intrinsic canvas: {image_route}")
            if re.search(
                r"<(?:script|foreignObject)\b|\son[a-z]+\s*=|(?:href|xlink:href)\s*=\s*[\"'](?:https?:|//)",
                svg_text,
                re.IGNORECASE,
            ):
                errors.append(f"site SVG must not contain executable or external content: {image_route}")
    obsolete_image = ROOT / "assets" / "images" / "secure-object-core.jpg"
    if obsolete_image.exists():
        errors.append("obsolete secure-object-core.jpg must not remain in source or built output")

    style_text = style.read_text() if style.exists() else ""
    if (SOURCE_ROOT / "tools").exists():
        errors.append("the retired multi-tool source tree must not remain")
    endem_source = SOURCE_ROOT / "endem" / "index.html"
    if not endem_source.exists():
        errors.append("missing Endem application page")
    elif endem_source.read_text().count('class="tool-project-body"') != 1:
        errors.append("Endem application page must define one bounded sticky body")
    if 'body[data-site-module="endem"]' not in style_text:
        errors.append("missing shared Endem application visual signature")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(source_routes)} Jekyll source pages use the shared layout contract")
    return 0


def validate_application_project_contract(h2_texts, status_texts, manual_counts=None):
    errors = []
    if list(h2_texts) != APPLICATION_PROJECT_SECTIONS:
        errors.append(
            "application-project h2 sequence must be exactly "
            f"{APPLICATION_PROJECT_SECTIONS}, got {list(h2_texts)}"
        )

    manual_counts = manual_counts or {}
    for class_name in ("manual-toc", "manual-nav-top", "manual-nav-bottom"):
        if manual_counts.get(class_name, 0):
            errors.append(f"{class_name} is forbidden on tool project pages")

    if len(status_texts) != 1:
        errors.append("expected one 当前状态 section")
    else:
        status_text = normalize_visible_text(status_texts[0])
        missing = [token for token in APPLICATION_STATUS_DISCLOSURES if token not in status_text]
        if missing:
            errors.append(
                "Endem current-state section is missing disclosures: "
                + ", ".join(missing)
            )
    return errors


def application_project_validator_self_test():
    errors = []
    valid_status = ["；".join(APPLICATION_STATUS_DISCLOSURES)]
    if validate_application_project_contract(APPLICATION_PROJECT_SECTIONS, valid_status):
        errors.append("application-project validator rejects the valid reference contract")

    negative_cases = {
        "wrong order": [
            ["当前状态", "应用简介", *APPLICATION_PROJECT_SECTIONS[2:]],
            valid_status,
        ],
        "duplicate section": [
            [*APPLICATION_PROJECT_SECTIONS[:2], "当前状态", *APPLICATION_PROJECT_SECTIONS[2:]],
            valid_status,
        ],
        "extra numbered chapter": [
            [*APPLICATION_PROJECT_SECTIONS, "第七章 依赖与文档拆分"],
            valid_status,
        ],
        "reversed release wording": [
            APPLICATION_PROJECT_SECTIONS,
            ["已经发布可执行版本，参数与稳定 ABI 已经确定。"],
        ],
    }
    for name, (headings, statuses) in negative_cases.items():
        if not validate_application_project_contract(headings, statuses):
            errors.append(f"application-project validator failed to reject {name}")
    return errors


def main():
    errors = application_project_validator_self_test()
    directory_css = DIRECTORY_CSS.read_text()
    for token in (
        "background:color-mix(in srgb,var(--paper) 90%,transparent)",
        "border:1px solid color-mix(in srgb,var(--rule) 64%,transparent)",
        "backdrop-filter:blur(12px) saturate(112%)",
    ):
        if token not in directory_css:
            errors.append(f"directory.css missing translucent sticky-header contract: {token}")
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

    if (ROOT / "assets" / "images" / "secure-object-core.jpg").exists():
        errors.append("built output must not retain obsolete secure-object-core.jpg")

    if not route_rows:
        errors.append("sitemap.md has no formal HTML route entries")
    if len(registered_rows) != len(set(registered_rows)):
        errors.append("sitemap.md contains duplicate HTML routes")
    if sorted(registered) != sorted(actual_routes):
        errors.append("sitemap.md routes do not exactly match HTML files")
    missing_core_routes = sorted(REQUIRED_CORE_ROUTES - set(registered))
    if missing_core_routes:
        errors.append(f"missing required Endem topology routes: {missing_core_routes}")
    errors.extend(validate_required_text_contracts(ROOT))
    errors.extend(validate_readability_behavior_contracts(ROOT))

    sitemap = ROOT / "sitemap.md"
    if not sitemap.exists():
        errors.append("missing public sitemap.md discovery index")
    else:
        sitemap_text = sitemap.read_text()
        if FRONT_MATTER.match(sitemap_text):
            errors.append("sitemap.md must remain a static Markdown file without Front Matter")
        if "Version: 3" not in sitemap_text:
            errors.append("sitemap.md must identify the Endem topology as discovery version 3")
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
    app_routes = [row["route"] for row in route_rows if row["kind"] == "app"]
    if sorted(app_routes) != sorted(APPLICATION_ROUTES):
        errors.append("sitemap.md application routes do not match the approved Endem topology")

    manual_payload_page = ROOT / "docs/index.html"
    if not manual_payload_page.exists():
        errors.append("missing docs/index.html for rendered manual directory validation")
    else:
        manual_page_text = manual_payload_page.read_text()
        manual_payload_match = re.search(
            r'<script type="application/json" data-manual-directory-source>\s*'
            r'(\{.*?\})\s*</script>',
            manual_page_text,
            re.DOTALL,
        )
        if manual_payload_match is None:
            errors.append("docs/index.html: missing rendered manual directory data")
        else:
            try:
                manual_payload = json.loads(manual_payload_match.group(1))
                manual_routes = [page["route"] for page in manual_payload["pages"]]
                expected_manual_routes = sorted(read_manual_source_routes())
                if manual_routes != expected_manual_routes:
                    errors.append(
                        "rendered manual directory data must contain every manual route exactly once in formal route order"
                    )
                manual_index_routes = [
                    "docs/index.html",
                    *[routes[0] for routes in MANUAL_ROUTE_ORDERS.values()],
                ]
                for manual_index_route in manual_index_routes:
                    index_path = ROOT / manual_index_route
                    index_match = re.search(
                        r'<script type="application/json" data-manual-directory-source>\s*'
                        r'(\{.*?\})\s*</script>',
                        index_path.read_text() if index_path.exists() else "",
                        re.DOTALL,
                    )
                    if index_match is None:
                        errors.append(f"{manual_index_route}: missing shared manual directory data")
                    elif json.loads(index_match.group(1)) != manual_payload:
                        errors.append(f"{manual_index_route}: manual directory payload diverges from the shared source")
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                errors.append(f"docs/index.html: invalid rendered manual directory data: {exc}")

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
        for term in (
            "Endem", "Weave", "Frame", "Witness", "say", "mean", "case", "when", "open",
            "一个根", "模型", "不可信",
        ):
            if term not in visible_text:
                errors.append(f"index.html: homepage must explain {term}")
        home_source = home.read_text()
        if home_source.count('class="portal-chapter-title"') != len(HOME_HEADINGS):
            errors.append("index.html: every homepage chapter heading must use the shared symbolic title treatment")
        for token in (
            "ENDEM / OPEN",
            "dataflow-lane-source",
            "dataflow-lane-bind",
            "dataflow-lane-reloc",
            "dataflow-lane-verify",
            'class="endem-object-visual"',
            'class="endem-object-title"',
            'class="endem-object-record"',
            'class="endem-object-footer"',
            "compiler-bridge",
        ):
            if token not in home_source:
                errors.append(f"index.html: homepage dataflow visual missing {token}")
        home_style_path = ROOT / "assets" / "style.css"
        home_style = home_style_path.read_text() if home_style_path.exists() else ""
        for selector in (
            ".endem-object-visual", ".endem-object-title",
            ".endem-object-record", ".endem-object-footer",
        ):
            if selector not in home_style:
                errors.append(f"style.css missing homepage visual selector {selector}")

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
            "不得直接推出", "思想采用的验证要求", "五组投影",
            "对象语言", "言语行为", "会话含义", "no-sense", "unknown",
        ):
            if term not in visible_text:
                errors.append(f"about/intellectual-foundations.html: must preserve {term}")

    for row in route_rows:
        path = ROOT / row["route"]
        if not path.exists():
            continue
        parser = parse(path)
        if parser.page_role != ROLE_BY_KIND[row["kind"]]:
            errors.append(f"{row['route']}: page role does not match registry kind")
        route_head = row["route"].split("/", 1)[0]
        expected_module = (
            "project" if row["route"] == "index.html"
            else "resources" if route_head in {"downloads", "news"}
            else "support" if route_head == "faq"
            else route_head
        )
        if expected_module not in SITE_MODULES:
            errors.append(f"{row['route']}: unknown expected site module {expected_module!r}")
        elif parser.site_module != expected_module:
            errors.append(
                f"{row['route']}: data-site-module must be {expected_module!r}, "
                f"got {parser.site_module!r}"
            )
        if row["kind"] != "portal" and parser.class_counts["hero"] != 1:
            errors.append(f"{row['route']}: every non-portal page must expose one module-aware hero")

    for route in NORMATIVE_ROUTES:
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing normative page {route}")
            continue
        parser = parse(path)
        visible_text = normalize_visible_text(
            " ".join("".join(section["text"]) for section in parser.sections)
        )
        for term in ("必须", "不得"):
            if term not in visible_text:
                errors.append(f"{route}: normative page must preserve {term}")
        if not any(
            marker in visible_text
            for marker in ("已经采用", "已接受", "已冻结")
        ):
            errors.append(f"{route}: normative page must state which boundary has been accepted")
        if not any(
            marker in visible_text
            for marker in ("仍需", "仍未冻结", "尚未冻结", "待验证", "开放问题")
        ):
            errors.append(f"{route}: normative page must preserve unfrozen or unresolved boundaries")

    for row in route_rows:
        if row["kind"] != "app":
            continue
        path = ROOT / row["route"]
        if not path.exists():
            continue
        parser = parse(path)
        breadcrumb = " ".join("".join(parser.breadcrumb_text).split())
        breadcrumb_routes = resolved_routes(path, parser.breadcrumb_links)
        if (
            parser.class_counts["breadcrumbs"] != 1
            or breadcrumb_routes != ["index.html"]
            or not all(label in breadcrumb for label in ("项目", "Endem"))
        ):
            errors.append(f"{row['route']}: must expose 项目 / Endem breadcrumbs")
        if parser.class_counts["tool-project-body"] != 1:
            errors.append(f"{row['route']}: must preserve one bounded sticky application body")
        status_sections = [section for section in parser.sections if section["heading"] == "当前状态"]
        status_texts = ["".join(section["text"]) for section in status_sections]
        contract_errors = validate_application_project_contract(
            parser.h2_texts,
            status_texts,
            parser.class_counts,
        )
        errors.extend(f"{row['route']}: {error}" for error in contract_errors)
        resource_sections = [
            section for section in parser.sections if section["heading"] == "继续阅读"
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
        if row["kind"] in {"portal", "section", "app"}
    ]
    expected_global_rows = set(PORTAL_ROUTES) | set(APPLICATION_ROUTES)
    if route_rows and set(global_rows) != expected_global_rows:
        errors.append(
            "global landing routes do not match the Endem information architecture: "
            f"expected={sorted(expected_global_rows)}, got={sorted(global_rows)}"
        )

    route_registry = {row["route"]: row for row in route_rows}

    for route, parent in REQUIRED_ARCHITECTURE_ROUTES.items():
        row = route_registry.get(route)
        if row is None or row["kind"] != "content" or row["parent"] != parent:
            errors.append(
                f"{route}: must be registered as content under {parent}"
            )

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
            or not all(label in breadcrumb for label in ("项目", "指南与参考"))
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
        if not any(
            marker in visible_text
            for marker in ("现行设计", "当前设计", "已经采用", "当前", "必须", "不得", "不能", "只")
        ):
            errors.append(f"{route}: guide must state an adopted boundary")
        if route != "docs/architecture-guide.html" and not any(
            marker in visible_text
            for marker in (
                "待验证", "尚待确定", "待定事项", "后续计划", "尚未", "未发布", "未冻结", "第一阶段", "何时建设",
            )
        ):
            errors.append(f"{route}: guide must identify unfinished work")

    for manual_id, manual_routes in MANUAL_ROUTE_ORDERS.items():
        app_route = f"{manual_id}/index.html"
        app_row = route_registry.get(app_route)
        if app_row is None or app_row["kind"] != "app":
            errors.append(f"{app_route} must be registered as kind app")

        manual_root = manual_routes[0]
        manual_row = route_registry.get(manual_root)
        if manual_row is None or manual_row["kind"] != "docs":
            errors.append(f"{manual_root} must be registered as kind docs")

        manual_rows = [row for row in route_rows if row["route"] in manual_routes]
        if route_rows:
            ordered_routes = [
                row["route"] for row in sorted(manual_rows, key=lambda row: row["order"])
            ]
            if ordered_routes != manual_routes:
                errors.append(f"sitemap {manual_id} routes do not match the manual order")

        for route in manual_routes[1:]:
            row = route_registry.get(route)
            if (
                row is None
                or row["kind"] != "topic"
                or row["parent"] != manual_root
            ):
                errors.append(f"{route}: invalid {manual_id} topic registry metadata")

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
            f'<strong class="global-stage-value" data-stage-value="{configured_header_value}"><span class="global-stage-text">{configured_header_value}</span><span class="global-stage-progress" aria-hidden="true"></span></strong>',
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
    theme_script = ROOT / "assets/theme.js"
    favicon = ROOT / "assets/favicon.svg"
    if not directory_script.exists():
        errors.append("missing assets/directory.js")
    if not theme_script.exists():
        errors.append("missing assets/theme.js")
    if not favicon.exists():
        errors.append("missing assets/favicon.svg")
    style_text = (ROOT / "assets" / "style.css").read_text() if (ROOT / "assets" / "style.css").exists() else ""
    if "scale(.996)" in style_text or "scale(0.996)" in style_text:
        errors.append("style.css press feedback must use the design-system scale(0.96) contract")

    rendered_canonical_urls = []
    for path in HTML_FILES:
        text = path.read_text()
        parser = parse(path)
        rel = path.relative_to(ROOT).as_posix()
        errors.extend(validate_public_html(rel, text))
        if not SOURCE_ONLY:
            for head_token in (
                '<meta name="description" content="',
                '<link rel="canonical" href="https://noemion.github.io/',
                '<meta property="og:title" content="',
                '<meta property="og:url" content="https://noemion.github.io/',
                '<meta name="twitter:card" content="summary">',
            ):
                if head_token not in text:
                    errors.append(f"{rel}: missing rendered discovery metadata {head_token}")
            expected_public_url = f"https://noemion.github.io/{rel}"
            canonical_matches = re.findall(r'<link rel="canonical" href="([^"]+)">', text)
            description_matches = re.findall(r'<meta name="description" content="([^"]*)">', text)
            og_url_matches = re.findall(r'<meta property="og:url" content="([^"]+)">', text)
            if canonical_matches != [expected_public_url]:
                errors.append(f"{rel}: canonical URL must exactly match its formal route")
            else:
                rendered_canonical_urls.extend(canonical_matches)
            if len(description_matches) != 1 or not description_matches[0].strip():
                errors.append(f"{rel}: rendered description metadata must be unique and non-empty")
            if og_url_matches != [expected_public_url]:
                errors.append(f"{rel}: Open Graph URL must exactly match its formal route")
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

    if len(rendered_canonical_urls) != len(set(rendered_canonical_urls)):
        errors.append("rendered canonical URLs must be unique across formal routes")

    if directory_script.exists() and route_rows:
        directory_source = directory_script.read_text()
        declared = set(HREF_LITERAL.findall(directory_source))
        registered_set = set(registered)
        manual_routes = {
            route for route in registered
            if route.startswith("docs/") or route.startswith("endem/docs/")
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
                ["endem/index.html", "https://site.test/endem", "https://site.test/endem/docs", True],
                ["endem/index.html", "https://site.test/endem", "https://site.test/endem/docs/safety.html", True],
                ["endem/index.html", "https://site.test/endem", "https://site.test/endem-old/docs", False],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs/guide", True],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs/getting-started.html", True],
                ["docs/index.html", "https://site.test/docs", "https://site.test/docs-old/guide.html", False],
            ]
            module_cases = [
                ["index.html", "project"],
                ["about/background.html", "project"],
                ["about/intellectual-foundations.html", "project"],
                ["architecture/endem-lifecycle.html", "architecture"],
                ["architecture/decisions.html", "architecture"],
                ["specifications/endem.html", "architecture"],
                ["components/core.html", "architecture"],
                ["components/reader.html", "architecture"],
                ["components/runner.html", "architecture"],
                ["docs/getting-started.html", "docs"],
                ["downloads/index.html", "resources"],
                ["faq/index.html", "resources"],
                ["development/testing.html", "development"],
                ["news/index.html", "development"],
                ["endem/index.html", "endem"],
                ["endem/docs/safety.html", "endem"],
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

    for manual_id, manual_routes in MANUAL_ROUTE_ORDERS.items():
        manual_index = ROOT / manual_routes[0]
        if manual_index.exists():
            parser = parse(manual_index)
            toc_routes = resolved_routes(
                manual_index, parser.scoped_links["manual-index-links"]
            )
            expected_topics = [
                entry["route"] for entry in read_manual_source_entries(manual_id)
                if not entry["is_index"]
            ]
            if toc_routes != expected_topics:
                errors.append(
                    f"{manual_id} index manual TOC does not match Markdown topic order"
                )

        for index, route in enumerate(manual_routes[1:], start=1):
            path = ROOT / route
            if not path.exists():
                errors.append(f"missing {manual_id} topic page {route}")
                continue
            if NUMBERED_NAME.search(route):
                errors.append(f"{route}: numbered topic filename is forbidden")
            parser = parse(path)
            if parser.site_module != "endem":
                errors.append(f"{route}: Endem manual must inherit data-site-module='endem'")
            for class_name in ("breadcrumbs", "manual-nav-top", "manual-nav-bottom"):
                if parser.class_counts[class_name] != 1:
                    errors.append(f"{route}: expected one {class_name}")
            expected = expected_manual_roles(manual_id, index)
            for scope in ("manual-nav-top", "manual-nav-bottom"):
                if parser.manual_roles[scope] != expected:
                    errors.append(
                        f"{route}: invalid {scope} roles {parser.manual_roles[scope]}"
                    )

    style = (ROOT / "assets/style.css").read_text()
    for token in (
        "@keyframes page-reveal",
        "@keyframes portal-datafield-shift",
        "@keyframes portal-data-packet",
        "@property --spectrum-angle",
        "conic-gradient(from var(--spectrum-angle)",
        "@keyframes spectrum-trace{to{--spectrum-angle:360deg}}",
        ".portal-feature-row::before{padding:5px}",
        ".portal-chapter-title>span{min-width:0;text-align:center}",
        "transition-duration:550ms,160ms",
        ".dataflow-field",
        ".site-header,main",
        "animation:page-reveal 110ms",
        "opacity:.96",
        "@media(prefers-reduced-motion:reduce)",
        "animation:none!important",
    ):
        if token not in style:
            errors.append(f"style.css missing animation contract: {token}")
    if "background-position:-220% 0" in style:
        errors.append("style.css must not reset the spectrum frame with a discontinuous background position")

    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PASS: {len(HTML_FILES)} registered pages, "
        f"{len(global_rows)} global landings, {len(MANUAL_ROUTE_ORDERS['endem'])} Endem manual routes, "
        "and deterministic trust-boundary contracts"
    )
    return 0


if __name__ == "__main__":
    sys.exit(validate_jekyll_sources() if SOURCE_ONLY else main())
