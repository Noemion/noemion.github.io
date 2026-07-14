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
NAVIGATION_HREF = re.compile(r"\bhref:\s*[\"']?(/[^,}\s\"']+)")
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
    "specifications/synem.html",
    "specifications/dromen.html",
    "specifications/iknem.html",
    "specifications/diagnostics.html",
    "specifications/adapters.html",
    "specifications/identity.html",
    "specifications/text-and-identifiers.html",
    "specifications/authority.html",
    "architecture/endem-lifecycle.html",
    "architecture/adr-0010-native-lexicon.html",
    "architecture/adr-0011-endem-container.html",
    "architecture/adr-0012-rust-core-language.html",
    "architecture/adr-0013-end-p1-payload.html",
    "architecture/adr-0014-source-manifest.html",
    "architecture/adr-0015-result-domains.html",
    "architecture/adr-0016-mene-time-model.html",
    "architecture/adr-0017-negation-and-absence.html",
    "architecture/adr-0018-quantification-and-membership.html",
    "architecture/adr-0019-measurement-and-thresholds.html",
    "architecture/adr-0020-composite-situations-and-criteria.html",
    "architecture/adr-0021-synem-closure-and-activation.html",
    "architecture/adr-0022-iknem-evidence-and-appraisal.html",
    "architecture/adr-0023-endem-content-standard.html",
    "architecture/adr-0024-dromen-session-contract.html",
    "architecture/adr-0025-structured-diagnostics.html",
    "architecture/adr-0026-external-protocol-adapters.html",
    "architecture/adr-0027-exact-identity-and-attestation.html",
    "architecture/adr-0028-text-and-identifier-boundaries.html",
    "architecture/adr-0029-authority-and-authorization-decisions.html",
    "architecture/adr-0030-endem-content-and-authorization-companions.html",
    "architecture/adr-0031-release-name-collision-gate.html",
    "architecture/adr-0032-deterministic-maker-name-collision.html",
    "architecture/adr-0033-text-identifier-specification-name.html",
    "architecture/adr-0034-pronunciation-and-oral-distinction.html",
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html",
    "components/ktisor.html",
    "components/theor.html",
    "components/drasor.html",
}
DOC_GUIDE_ORDER = [
    "docs/getting-started.html",
    "docs/installation-and-usage.html",
    "docs/terminology-and-pronunciation.html",
    "docs/architecture-guide.html",
    "docs/development-guide.html",
    "docs/endem-reference.html",
    "docs/specifications-reference.html",
]
DOC_GUIDE_HEADINGS = {
    "docs/getting-started.html": [
        "从这里开始", "先看一个 Agent 工作", "六个语义面", "四个名词", "一个应用", "这些名字怎样读", "推荐阅读路径", "当前状态",
    ],
    "docs/installation-and-usage.html": [
        "当前可用性", "未来职责流程", "发布原则", "命名发布条件",
    ],
    "docs/terminology-and-pronunciation.html": [
        "直接结论", "读音待定时怎样协作", "证据适用边界", "两阶段验证", "任务与材料", "通过与停止规则",
        "证据记录", "人工智能只做辅助探针", "当前状态",
    ],
    "docs/architecture-guide.html": [
        "最小系统图", "用一次 Agent 工作读图", "三个实现域", "形成与语义确认", "组合与发布", "装载与运行", "信任不是单一分数",
    ],
    "docs/development-guide.html": [
        "先定义变更主张", "当前范围", "规范与 ADR 先行", "变更工作流", "建议仓库边界", "审查清单", "模型与协议",
    ],
    "docs/endem-reference.html": [
        "应用总览", "Ktisor 子命令", "theor 的独立性", "drase 的隔离性", "不建设独立模型平台",
    ],
    "docs/specifications-reference.html": [
        "按工程问题找资料", "权威顺序", "资料状态与使用边界", "Endem", "Synem", "Dromen、Iknem 与横切边界", "ADR 与开放问题",
    ],
}
HOME_HEADINGS = [
    "项目名与工程名各自负责",
    "六项职责保持语义边界",
    "只保留有独立生命周期的名词",
    "一个入口不等于一个信任域",
    "先证明最小纵向切片",
    "借鉴工具链思想不复制工具数量",
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
    "当前没有可执行组件",
    "参数",
    "稳定 ABI",
    "尚待确定",
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
    "用户明确开启",
    "只有用户开启",
    "等待用户接受",
    "用户决定接受",
    "用户以后明确开启",
    "尚未进入代码开发阶段",
    "尚未进入组件代码阶段",
    "组件代码开发尚未开启",
    "代码阶段开启后",
    "代码阶段开启时",
    "内部符合性门禁",
    "内部一致性门禁",
    "资料检查器",
    "页面负责解释",
    "本手册只解释",
    "当前公开仓库只维护",
    "项目提示词",
    "采用决定",
    "未决边界",
    "成熟度边界",
    "等待决定",
    "研究中的研究",
    "当前仍未冻结",
    "仍未冻结的内容",
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
RETIRED_RELEASE_TERMS = re.compile(
    r"\b(?:praxor|praxe|tekmor|poiet|poie)\b|\bTEK(?:-[A-Z0-9]+)+\b|\bTK-[A-Z0-9-]+\b|\btek-core\b",
    re.IGNORECASE,
)
RETIRED_RELEASE_EVIDENCE_PATHS = {
    "architecture/adr-0031-release-name-collision-gate.html",
    "architecture/adr-0032-deterministic-maker-name-collision.html",
    "design-system/name-audit.md",
}
RETIRED_TEXT_SPEC_TERMS = re.compile(
    r"\bTXT(?:-[A-Z]+)*\b|"
    r"spec/(?:text-core|text-threat-model|text-scenarios)\.md|"
    r"vectors/text(?!-identifier)|tests/text_vector_test\.py|"
    r"specifications/text\.html"
)
RETIRED_TEXT_SPEC_EVIDENCE_PATHS = {
    "architecture/adr-0033-text-identifier-specification-name.html",
    "architecture/adr-0034-pronunciation-and-oral-distinction.html",
    "design-system/name-audit.md",
}
RETIRED_ACTION_TERMS = re.compile(r"\b(?:tasse|sphra|peira)\b", re.IGNORECASE)
RETIRED_ACTION_EVIDENCE_PATHS = {
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html",
    "design-system/name-audit.md",
}
NORMATIVE_ROUTES = (
    "specifications/endem.html",
    "specifications/synem.html",
    "specifications/dromen.html",
    "specifications/iknem.html",
    "specifications/diagnostics.html",
    "specifications/adapters.html",
    "specifications/identity.html",
    "specifications/text-and-identifiers.html",
    "specifications/authority.html",
)
CONTENT_LAYOUT_ROUTES = (
    "about/background.html",
    "about/intellectual-foundations.html",
    "architecture/endem-lifecycle.html",
    "architecture/decisions.html",
    "architecture/agent-system-boundaries.html",
    "architecture/adr-0008-endem-system.html",
    "architecture/adr-0009-propositional-kernel.html",
    "architecture/adr-0010-native-lexicon.html",
    "architecture/adr-0011-endem-container.html",
    "architecture/adr-0012-rust-core-language.html",
    "architecture/adr-0013-end-p1-payload.html",
    "architecture/adr-0014-source-manifest.html",
    "architecture/adr-0015-result-domains.html",
    "architecture/adr-0016-mene-time-model.html",
    "architecture/adr-0017-negation-and-absence.html",
    "architecture/adr-0018-quantification-and-membership.html",
    "architecture/adr-0019-measurement-and-thresholds.html",
    "architecture/adr-0020-composite-situations-and-criteria.html",
    "architecture/adr-0021-synem-closure-and-activation.html",
    "architecture/adr-0022-iknem-evidence-and-appraisal.html",
    "architecture/adr-0023-endem-content-standard.html",
    "architecture/adr-0024-dromen-session-contract.html",
    "architecture/adr-0025-structured-diagnostics.html",
    "architecture/adr-0026-external-protocol-adapters.html",
    "architecture/adr-0027-exact-identity-and-attestation.html",
    "architecture/adr-0028-text-and-identifier-boundaries.html",
    "architecture/adr-0029-authority-and-authorization-decisions.html",
    "architecture/adr-0030-endem-content-and-authorization-companions.html",
    "architecture/adr-0031-release-name-collision-gate.html",
    "architecture/adr-0032-deterministic-maker-name-collision.html",
    "architecture/adr-0033-text-identifier-specification-name.html",
    "architecture/adr-0034-pronunciation-and-oral-distinction.html",
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html",
    "architecture/open-questions.html",
    "components/ktisor.html",
    "components/theor.html",
    "components/drasor.html",
    "development/implementation-roadmap.html",
    "development/testing.html",
    "specifications/endem.html",
    "specifications/synem.html",
    "specifications/dromen.html",
    "specifications/iknem.html",
    "specifications/diagnostics.html",
    "specifications/adapters.html",
    "specifications/identity.html",
    "specifications/text-and-identifiers.html",
    "specifications/authority.html",
)
CONTENT_LAYOUT_CLASSES = {
    "content-split",
    "content-stack",
    "content-band",
    "content-wide",
    "content-grid",
    "content-rows",
}
INTRODUCTION_CLASSES = {
    "portal-introduction",
    "section-introduction",
    "content-introduction",
    "application-introduction",
    "manual-introduction",
}
DEPRECATED_LAYOUT_TERM = "he" + "ro"

CURRENT_DOMAIN_IDENTIFIERS = {
    "endem", "rhem", "semion", "skena", "telis", "krin", "apor", "phain",
    "synem", "dromen", "iknem", "ktisor", "theor", "drasor",
    "ktise", "elenk", "pleko", "theor", "drase",
}
MAINSTREAM_LANGUAGE_KEYWORDS = {
    # C, C++, Java, ECMAScript, Go, Rust, Swift, Kotlin and Python keyword union.
    "alignas", "alignof", "and", "as", "asm", "assert", "async", "await", "auto",
    "become", "bool", "boolean", "break", "byte", "case", "catch", "char", "class",
    "compl", "concept", "const", "const_cast", "consteval", "constexpr", "constinit",
    "continue", "co_await", "co_return", "co_yield", "decltype", "default", "defer",
    "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export",
    "extends", "extern", "false", "final", "finally", "float", "fn", "for", "friend",
    "from", "fun", "goto", "if", "implements", "import", "in", "inline", "instanceof",
    "int", "interface", "internal", "is", "let", "long", "match", "module", "mutable",
    "namespace", "native", "new", "noexcept", "nonlocal", "not", "null", "nullptr",
    "object", "open", "operator", "or", "out", "override", "package", "pass", "private",
    "protected", "public", "register", "reinterpret_cast", "requires", "return", "sealed",
    "short", "signed", "sizeof", "static", "static_assert", "static_cast", "strictfp",
    "struct", "super", "switch", "synchronized", "template", "this", "thread_local",
    "throw", "throws", "trait", "transient", "true", "try", "typealias", "typedef",
    "typeid", "typename", "typeof", "union", "unsafe", "unsigned", "use", "using", "var",
    "virtual", "void", "volatile", "wchar_t", "when", "where", "while", "with", "yield",
}
REMOVED_PUBLIC_ROUTES = {
    "specifications/weave.html", "specifications/witness.html",
    "components/core.html", "components/reader.html", "components/runner.html",
    "specifications/tekmor.html", "components/praxor.html",
    "architecture/adr-0022-tekmor-evidence-and-appraisal.html",
}

REQUIRED_ARCHITECTURE_ROUTES = {
    "architecture/decisions.html": "architecture/index.html",
    "architecture/agent-system-boundaries.html": "architecture/index.html",
    "components/drasor.html": "components/index.html",
}

SYSTEM_BOUNDARY_CONTRACTS = {
    "architecture/index.html": {
        "required": (
            "Endem",
            "Synem",
            "Iknem",
            "Dromen",
            "Ktisor",
            "Theor",
            "Drasor",
            "形成侧检查和",
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
            "身份不等于权威",
            "外部状态不等于本地结果",
            "能力声明不等于实时句柄",
            "Iknem 证据与评估",
            "ADR-0015",
            "判断与运行结果分层",
        ),
    },
    "architecture/agent-system-boundaries.html": {
        "required": (
            "Non-normative Guide",
            "三种状态不得混写",
            "一次运行怎样穿过边界",
            "运行事实应该放在哪里",
            "十三条最危险的越级路径",
            "当前 Agent 技术趋势改变了什么",
            "GNU 技术与软件自由提供的十一个约束",
            "什么时候才值得增加新对象",
            "十三项研究怎样回到现有规范",
            "模型输出是候选，不是规范内容",
            "模型评审也只是有范围的候选测量",
            "反馈记录也不等于模型学习",
            "旧 Dromen、秘密或权限",
            "Task 完成，也不证明目标满足",
            "研究中",
            "不增加 ADR、CORE、Profile、对象、命令或组件",
        ),
        "forbidden_patterns": (
            r"handoff.*自动.*(?:授权|权限)",
            r"Task.*completed.*(?:等于|成为).*met",
            r"检查点(?:能够|可以|会)恢复旧 Dromen",
        ),
    },
    "components/ktisor.html": {
        "required": (
            "Ktisor",
            "Endem",
            "确定性",
            "模型",
            "不可信",
            "checked arithmetic",
        ),
    },
    "components/theor.html": {
        "required": (
            "Theor",
            "theor",
            "独立",
            "只读",
            "形成侧解析器",
            "不共享",
            "checked arithmetic",
        ),
    },
    "components/drasor.html": {
        "required": (
            "Drasor",
            "Dromen",
            "drase",
            "类型化能力请求",
            "Iknem",
            "accepted",
            "deferred",
            "completed / failed / interrupted",
            "决定权威",
            "不能给自己的记录",
            "具名权威再形成",
            "模型",
            "不可信",
        ),
    },
    "specifications/endem.html": {
        "required": (
            ".endem",
            "rhem",
            "semion",
            "skena",
            "telis",
            "krin",
            "apor",
            "phain",
            "aseme",
            "agno",
            "fault",
            "logical_form",
            "checked arithmetic",
        ),
    },
    "specifications/synem.html": {
        "required": (
            "Synem",
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
    "specifications/iknem.html": {
        "required": (
            "Iknem",
            "phain",
            "精确证据主体",
            "主张",
            "原始观察",
            "model-candidate",
            "完整性",
            "sufficient / insufficient",
            "最终决定",
            "当前草案",
            "非规范场景",
            "仅检查资料一致性",
            "正在研究",
        ),
        "forbidden_patterns": (
            r">draft</td>",
            r">non-normative</td>",
            r">vector-checker-only</td>",
            r">awaiting-decision</td>",
        ),
    },
    "specifications/dromen.html": {
        "required": (
            "Dromen",
            "只读执行契约",
            "DRO-CORE 0.1.0-draft",
            "精确制品",
            "能力只能",
            "有限且带单位的预算",
            "不保存令牌",
            "实质漂移",
            "不能序列化",
        ),
    },
    "specifications/diagnostics.html": {
        "required": (
            "DIA-CORE 0.1.0-draft",
            "稳定机器码",
            "生产语境",
            "主阻断诊断",
            "不得授予权限",
            "不保存令牌",
            "有限预算",
            "部分可信对象",
        ),
    },
    "specifications/adapters.html": {
        "required": (
            "ADP-CORE 0.1.0-draft",
            "ADP-PIN-001",
            "ADP-PEE-001",
            "ADP-CAP-001",
            "ADP-INV-001",
            "ADP-MAP-001",
            "ADP-STA-001",
            "ADP-ART-001",
            "ADP-ERR-001",
            "ADP-CAN-001",
            "ADP-RTY-001",
            "ADP-DEL-001",
            "ADP-SEC-001",
            "不可信候选",
            "当前没有具体协议 Profile",
        ),
    },
    "specifications/identity.html": {
        "required": (
            "ID-CORE 0.1.0-draft",
            "ID-DOM-001",
            "ID-BYT-001",
            "ID-REF-001",
            "ID-ALG-001",
            "ID-DSP-001",
            "ID-EQV-001",
            "ID-STM-001",
            "ID-ENV-001",
            "ID-AUT-001",
            "ID-VAL-001",
            "ID-REP-001",
            "ID-REL-001",
            "不是新制品",
            "待定内容",
        ),
    },
    "specifications/text-and-identifiers.html": {
        "required": (
            "TEXT-IDENTIFIER-CORE 0.1.0-draft",
            "TEXT-SLT-001",
            "TEXT-ENC-001",
            "TEXT-SRC-001",
            "TEXT-IDN-001",
            "TEXT-NRM-001",
            "TEXT-CMP-001",
            "TEXT-RNG-001",
            "TEXT-BID-001",
            "TEXT-HID-001",
            "TEXT-MET-001",
            "TEXT-AIM-001",
            "TEXT-OUT-001",
            "待定内容",
        ),
    },
    "specifications/authority.html": {
        "required": (
            "AUT-CORE 0.1.0-draft",
            "AUT-CTX-001",
            "AUT-PRN-001",
            "AUT-SCP-001",
            "AUT-SEM-001",
            "AUT-DEC-001",
            "AUT-DEL-001",
            "AUT-MUL-001",
            "AUT-CNS-001",
            "AUT-TIM-001",
            "AUT-RPL-001",
            "AUT-CAP-001",
            "AUT-SEP-001",
            "待定内容",
        ),
    },
    "architecture/adr-0030-endem-content-and-authorization-companions.html": {
        "required": (
            "END-CON-006",
            "END-AUT-002",
            "END-ID-002",
            "END-FMT-015",
            "单文件最高只能声称 Profile 接受",
            "待定内容",
        ),
    },
    "architecture/adr-0031-release-name-collision-gate.html": {
        "required": (
            "Iknem",
            "Drasor",
            "drase",
            "IKN-CORE",
            "一次性迁移",
            "不保留别名、重定向、双写或兼容垫片",
            "Praxor Lab",
            "tekmor.xyz",
        ),
    },
    "architecture/adr-0032-deterministic-maker-name-collision.html": {
        "required": (
            "Ktisor",
            "ktise",
            "PFA Open Inference Engine",
            "大小写不能形成可靠区分",
            "不保留别名、重定向、双写或兼容垫片",
            "动作名称不等于实现优先级",
            "一致性与互操作验证",
        ),
    },
    "architecture/adr-0033-text-identifier-specification-name.html": {
        "required": (
            "TEXT-IDENTIFIER-CORE",
            "TXT-CORE",
            "不是 <code>.txt</code> 文件格式",
            "TEXT-CORE",
            "TIB-CORE",
            "不保留旧路径、别名、重定向、双写或兼容垫片",
            "text-identifier-core.md",
            "vectors/text-identifier/",
        ),
    },
    "architecture/adr-0034-pronunciation-and-oral-distinction.html": {
        "required": (
            "当前审查",
            "四项独立审查",
            "BCP 47",
            "成对混淆矩阵",
            "首次朗读",
            "听写回填",
            "W3C Pronunciation Lexicon Specification 1.0",
            "GNU Coding Standards：Names",
            "OpenAI Realtime API",
            "Iknem",
            "Ktisor",
            "kine",
            "No Voice Interface",
        ),
    },
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html": {
        "required": (
            "Five Actions",
            "ktise",
            "elenk",
            "pleko",
            "theor",
            "drase",
            "GNU Binutils",
            "GNU objcopy",
            "MCP Tasks",
            "A2A Specification",
            "OpenAI Agents SDK handoffs",
            "conformance:",
            "不是公开动作",
            "不保留旧入口、别名、重定向、双写或兼容垫片",
        ),
    },
    "docs/terminology-and-pronunciation.html": {
        "required": (
            "ISO 704:2022",
            "ISO 9241-11:2018",
            "RFC 5646 / BCP 47",
            "W3C Pronunciation Lexicon Specification 1.0",
            "ITU-T P.800",
            "ITU-T P.808",
            "NISTIR 8429",
            "至少 24 名",
            "至少收集 60 个",
            "rule of three",
            "5 至 15 个刺激",
            "误选成另一个现行名称",
            "参与者标识必须假名化",
            "尚未执行上述人类研究",
            "读音待定时怎样协作",
            "有范围的证据记录（现行设计名",
            "自动转写只保存一次机器观察",
            "只有声音或转写结果不能触发执行",
        ),
    },
    "endem/docs/safety.html": {
        "required": (
            "checked arithmetic",
            "theor",
            "独立 Theor",
            "形成侧解析器",
            "绑定精确字节",
            "不是 CLI 输出",
            "不能跨入 Theor",
            "不可信",
        ),
    },
    "endem/docs/running.html": {
        "required": (
            "Dromen",
            "外部签名",
            "私钥始终留在外部签名系统",
            "签名包络",
            "Iknem",
            "phain",
            "accepted",
            "deferred",
            "completed",
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
        self.docs_layout = False
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
            self.docs_layout = data.get("data-docs-layout") == "true"
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
    content_script = root / "assets" / "modules" / "content-enhancements.mjs"
    navigation_data = SOURCE_ROOT / "_data" / "navigation.yml"
    style = root / "assets" / "style.css"
    directory_style = root / "assets" / "directory.css"

    if content_script.exists() and navigation_data.exists():
        behavior_text = content_script.read_text()
        navigation_text = navigation_data.read_text()
        for token in (
            'querySelectorAll(".manual-article table")',
            'wrapper.className = "table-wrap manual-table-wrap"',
            'this.main.querySelector(":scope > .content-introduction")',
            'insertAdjacentElement("afterend", outline)',
        ):
            if token not in behavior_text:
                errors.append(
                    f"content enhancement module missing readability contract: {token}"
                )
        for token in (
            "href: /architecture/index.html",
            "href: /architecture/decisions.html",
            "label: 指南",
            "href: /docs/architecture-guide.html",
            "href: /docs/endem-reference.html",
            "href: /docs/specifications-reference.html",
            "href: /news/index.html",
            "href: /faq/index.html",
            "href: /development/implementation-roadmap.html",
        ):
            if token not in navigation_text:
                errors.append(f"navigation data missing readability contract: {token}")
    else:
        errors.append("missing content enhancement module or navigation data")

    if style.exists() and directory_style.exists():
        style_text = style.read_text()
        directory_text = directory_style.read_text()
        if 'body[data-docs-layout="true"] .manual-introduction::before{top:auto;right:auto;bottom:28px;left:50%;width:130px;height:104px;transform:translateX(-50%)}' not in style_text:
            errors.append("mobile manual introduction visual must be centered on its standalone row")
        css_patterns = {
            "desktop documentation rail must share the header canvas basis": (
                directory_text,
                r"\.docs-rail\s*\{[^}]*left:max\(18px,calc\(\(100%\s*-\s*1200px\)/2\)\)"
            ),
            "desktop documentation content must share the header canvas basis": (
                style_text,
                r"body\[data-docs-layout=\"true\"\]\s+main\s*\{[^}]*"
                r"calc\(\(100%\s*-\s*1200px\)/2\)"
            ),
            "open mobile directory must align with the shared eight pixel canvas": (
                directory_text,
                r"html\.mobile-directory-open\s+\.global-directory-panel\s+nav\s*\{"
                r"[^}]*right:8px;[^}]*left:8px;width:auto"
            ),
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
            "current stage summary must use readable body text": (
                style_text,
                r"\.current-stage-panel>p\{[^}]*font-size:16px;[^}]*line-height:1\.75"
            ),
            "timeline descriptions must use readable body text": (
                style_text,
                r"\.timeline-copy p\{[^}]*font-size:16px;[^}]*line-height:1\.7"
            ),
            "FAQ answers must preserve the readable line length": (
                style_text,
                r"\.faq-list\s+details>p\s*\{[^}]*max-width:760px;"
                r"[^}]*font-size:17px;[^}]*line-height:1\.75"
            ),
            "tool project must collapse before a tablet canvas clips its status panel": (
                style_text,
                r"@media\(max-width:1217px\)\s*\{"
                r"[^}]*body\[data-page-role=\"tool-project\"\]\s+\.tool-project-body"
                r"\s*\{\s*display:block"
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
        if re.search(
            r'(?:body\[data-docs-layout="true"\]\s+(?:main|\.site-footer)|\.docs-rail)\s*\{[^}]*100vw',
            style_text + "\n" + directory_text,
            re.DOTALL,
        ):
            errors.append("desktop documentation canvas must not use viewport width positioning")
        if re.search(
            r'\.global-directory-panel(?:\[open\])?\s+nav\s*\{[^}]*100vw',
            directory_text,
            re.DOTALL,
        ):
            errors.append("mobile directory must not use viewport width positioning")
        if re.search(
            r'html\.mobile-directory-open[^{}]*\.global-directory-panel\s+nav\s*\{'
            r'[^}]*(?<!max-)height:calc\(var\(--mobile-directory-viewport-height',
            directory_text,
            re.DOTALL,
        ):
            errors.append("open mobile directory height must follow its content instead of filling the viewport")
    else:
        if not style.exists():
            errors.append("missing assets/style.css")
        if not directory_style.exists():
            errors.append("missing assets/directory.css")
    return errors


def validate_prose_readability_contracts():
    errors = []
    historical_routes = {
        "architecture/adr-0008-endem-system.html",
        "architecture/adr-0009-propositional-kernel.html",
    }
    current_prose_forbidden = (
        r"\.weave\b",
        r"\bRhem Source\b",
        r"\bHarness\b",
        r"\bAcceptance Decision\b",
        r"\bSemion Decision\b",
        r"\bVerified Handle\b",
        r"\bweave-binding-release\b",
        r"SAY\s*→\s*DONE",
        r"生产(?:验证|读取|解析)",
        r"(?:生产|可信|内部)验证句柄",
    )

    for path in SOURCE_PAGE_FILES:
        source_text = path.read_text()
        source_match = FRONT_MATTER.match(source_text)
        if source_match is None:
            continue
        permalink = front_matter_value(source_match.group(1), "permalink")
        route = permalink.lstrip("/") if permalink else path.relative_to(SOURCE_ROOT).as_posix()
        body = source_text[source_match.end():]

        if route not in historical_routes:
            for pattern in current_prose_forbidden:
                if re.search(pattern, body):
                    errors.append(f"{route}: current prose retains unexplained or obsolete wording {pattern!r}")

        if path.suffix == ".html":
            prose_blocks = re.findall(r"<p\b[^>]*>(.*?)</p>", body, re.DOTALL | re.IGNORECASE)
        else:
            prose_blocks = [
                block
                for block in re.split(r"\n\s*\n", body)
                if not block.lstrip().startswith((
                    "#", "- ", "1. ", "2. ", "3. ", "4. ", "5. ",
                    "6. ", "7. ", "8. ", "9. ", "|", "```", ">",
                ))
            ]
        for block in prose_blocks:
            visible = re.sub(r"https?://[^\s<)]+", "", block)
            visible = re.sub(r"{%.*?%}|{{.*?}}", " ", visible, flags=re.DOTALL)
            visible = re.sub(r"<[^>]+>|[`*_#>|\[\]()]", " ", visible)
            visible = " ".join(visible.split())
            for sentence in re.split(r"[。！？；]+", visible):
                cjk_count = len(re.findall(r"[\u4e00-\u9fff]", sentence))
                if cjk_count > 70:
                    errors.append(
                        f"{route}: prose sentence exceeds 70 Chinese characters and should be split: {sentence[:80]!r}"
                    )

    foundations = (SOURCE_ROOT / "about" / "intellectual-foundations.html").read_text()
    for token in (
        "事态由对象的结合构成。",
        "图像通过要素与对象的对应",
        "图示者与被图示者必须共享可对应形式",
        "名称指向对象",
        "理解一个命题意味着知道若命题为真事情该是怎样的。",
        "4.062–4.064",
        "5.6 与 7",
        "贺绍甲译《逻辑哲学论》",
        "不直接决定软件规范",
    ):
        if token not in foundations:
            errors.append(f"intellectual foundations missing checked proposition boundary {token!r}")
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
        if not label or label == href or label.startswith(("http://", "https://")):
            errors.append(
                f"{route}: external resource link must use a descriptive label instead of the raw URL {href!r}"
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
        if not relative.startswith("tests/") and relative not in RETIRED_RELEASE_EVIDENCE_PATHS:
            retired_match = RETIRED_RELEASE_TERMS.search(text)
            if retired_match:
                errors.append(
                    f"{relative}: retired release terminology remains outside accepted naming evidence "
                    f"{retired_match.group(0)!r}"
                )
        if not relative.startswith("tests/") and relative not in RETIRED_TEXT_SPEC_EVIDENCE_PATHS:
            retired_text_match = RETIRED_TEXT_SPEC_TERMS.search(text)
            if retired_text_match:
                errors.append(
                    f"{relative}: retired text specification terminology remains outside ADR-0033 and the name audit "
                    f"{retired_text_match.group(0)!r}"
                )
        if not relative.startswith("tests/") and relative not in RETIRED_ACTION_EVIDENCE_PATHS:
            retired_action_match = RETIRED_ACTION_TERMS.search(text)
            if retired_action_match:
                errors.append(
                    f"{relative}: retired public action remains outside ADR-0035 and the name audit "
                    f"{retired_action_match.group(0)!r}"
                )
        if DEPRECATED_LAYOUT_TERM in text.lower():
            errors.append(f"{relative}: retains the deprecated generic lead-layout term")
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
    workflow_files = sorted(
        path.name for path in (SOURCE_ROOT / ".github" / "workflows").glob("*.yml")
    )
    if workflow_files != ["pages.yml"]:
        errors.append(
            "design stage permits only the documentation Pages workflow, "
            f"got {workflow_files}"
        )
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
        for script in (
            "assets/site.mjs",
            "assets/theme.js",
            "assets/mobile-directory-guard.js",
        ):
            if f"node --check {script}" not in workflow_text:
                errors.append(f"Pages workflow must syntax-check {script}")
        if "assets/modules/*.mjs" not in workflow_text:
            errors.append("Pages workflow must syntax-check every front-end module")
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
            "python3 tests/spec_contract_test.py",
            "python3 tests/wire_vector_test.py",
            "python3 tests/site_quality_test.py",
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

    context_proposal = SOURCE_ROOT / "spec" / "model-context-assembly-proposal.md"
    if not context_proposal.exists():
        errors.append("missing non-normative model context assembly research proposal")
    else:
        proposal_text = context_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件或稳定接口",
            "无模型、无检索或纯确定性路径直接省略",
            "候选责任的唯一主归属",
            "可证伪的同权威冲突案例",
            "供应商不可观察变换案例",
            "威胁到责任的映射",
            "失败域与结果隔离",
            "等待决定",
            "model-context-assembly-proposal.md",
        ):
            if token not in proposal_text and token not in (SOURCE_ROOT / "spec" / "README.md").read_text():
                errors.append(f"model context proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "model-context-assembly" in registry_text:
            errors.append("non-normative model context proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "spec/model-context-assembly-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the model context research proposal"
                )

    gnu_elf_proposal = SOURCE_ROOT / "spec" / "gnu-elf-applicability-proposal.md"
    if not gnu_elf_proposal.exists():
        errors.append("missing non-normative GNU and ELF applicability research proposal")
    else:
        proposal_text = gnu_elf_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件或稳定接口",
            "Endem 是 ELF object",
            "Dromen 是 segment 或 process image",
            "职责适用性矩阵",
            "Symbol versioning",
            "`objcopy` / `strip` / debug link",
            "带错继续和部分输出",
            "未来采用的证据门",
            "不进入 `registry.json`",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"GNU and ELF applicability proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "gnu-elf-applicability" in registry_text:
            errors.append("non-normative GNU and ELF proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "gnu-elf-applicability-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the GNU and ELF research proposal"
                )

    planning_proposal = SOURCE_ROOT / "spec" / "planning-and-replanning-proposal.md"
    if not planning_proposal.exists():
        errors.append("missing non-normative planning and replanning research proposal")
    else:
        proposal_text = planning_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域或稳定接口",
            "不进入 `registry.json`",
            "五个对象不能混为一谈",
            "计划步骤何时不是 Endem",
            "来自 GNU Make 的可用边界",
            "A2A 1.0.0",
            "MCP 2025-11-25 Tasks",
            "OpenAI Agents SDK",
            "重规划触发矩阵",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"planning proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "planning-and-replanning" in registry_text:
            errors.append("non-normative planning proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "planning-and-replanning-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the planning research proposal"
                )

    equivalence_proposal = SOURCE_ROOT / "spec" / "semantic-equivalence-and-migration-proposal.md"
    if not equivalence_proposal.exists():
        errors.append("missing non-normative semantic equivalence and migration research proposal")
    else:
        proposal_text = equivalence_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域或稳定接口",
            "不进入 `registry.json`",
            "Noemion 不应建立一个跨对象、跨 Profile、跨版本通用的“语义等价”布尔值",
            "五类关系必须分开",
            "派生处理的当前边界",
            "W3C RDF Dataset Canonicalization",
            "GNU BFD canonical object-file format",
            "Sentence-BERT",
            "NIST AI 800-3",
            "支持案例与反例",
            "威胁到失败责任的映射",
            "候选责任的唯一主归属",
            "Semantic Key 的进入条件",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"semantic equivalence proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "semantic-equivalence-and-migration" in registry_text:
            errors.append("non-normative semantic equivalence proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "semantic-equivalence-and-migration-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the semantic equivalence research proposal"
                )

    causation_proposal = SOURCE_ROOT / "spec" / "state-change-and-causal-attribution-proposal.md"
    if not causation_proposal.exists():
        errors.append("missing non-normative state change and causal attribution research proposal")
    else:
        proposal_text = causation_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "五类主张必须分开",
            "GNU Make",
            "W3C PROV-DM",
            "CloudEvents",
            "OpenTelemetry",
            "终态满足",
            "动作发生",
            "状态转变",
            "因果归因",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"causation proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "state-change-and-causal-attribution" in registry_text:
            errors.append("non-normative causation proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "endem.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "state-change-and-causal-attribution-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the causation research proposal"
                )

    telis_terms_proposal = SOURCE_ROOT / "spec" / "telis-release-terms-proposal.md"
    if not telis_terms_proposal.exists():
        errors.append("missing non-normative telis release terms research proposal")
    else:
        proposal_text = telis_terms_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求",
            "不进入 `registry.json`",
            "`kine / mene` 不适合作为首次正式发行的拼写",
            "`reach / maintain` 作为第一组人类验证候选",
            "语义先于拼写",
            "桌面门禁只能排除明显不合格候选",
            "不改 END-TEL-001",
            "不增加别名、双写、自动规范化、重定向或兼容读音",
            "Iknem",
            "Ktisor/ktise",
            "Endem/Synem",
        ):
            if token not in proposal_text:
                errors.append(f"telis release terms proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "telis-release-terms" in registry_text:
            errors.append("non-normative telis release terms proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "design-system" / "name-audit.md",
            SOURCE_ROOT / "docs" / "terminology-and-pronunciation.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
        ):
            if "telis-release-terms-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the telis release terms proposal"
                )

    release_terms_proposal = SOURCE_ROOT / "spec" / "release-terminology-simplification-proposal.md"
    if not release_terms_proposal.exists():
        errors.append("missing non-normative release terminology simplification proposal")
    else:
        proposal_text = release_terms_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定与人类验证",
            "不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求",
            "不进入 `registry.json`",
            "只有确实需要独立公共身份、且普通术语无法准确承担职责时，才创造专名",
            "保留 Endem 进入人类读音验证",
            "Endem closure（Endem 闭包）",
            "session contract（会话契约）",
            "scoped evidence record（有范围证据记录）",
            "deterministic producer（确定性生产边界）",
            "independent inspector（独立检查边界）",
            "bounded runner（有界运行边界）",
            "`form`、`check`、`compose`、`inspect` 与 `run`",
            "ISO 704:2022",
            "GNU Coding Standards 的 Names 规则",
            "MCP 2025-11-25 工具定义",
            "A2A AgentSkill",
            "NIST Dictionary of Algorithms and Data Structures",
            "W3C PROV-DM",
            "RFC 9334 RATS Architecture",
            "候选普通词不是别名、重定向或兼容入口",
            "标准 ID 的具体新拼写、条款前缀和机器对象种类不能由本提案提前冻结",
            "仍需单独按语义面逐项审查",
        ):
            if token not in proposal_text:
                errors.append(f"release terminology proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "release-terminology-simplification" in registry_text:
            errors.append("non-normative release terminology proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "design-system" / "name-audit.md",
            SOURCE_ROOT / "design-system" / "language-and-naming.md",
            SOURCE_ROOT / "docs" / "terminology-and-pronunciation.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "release-terminology-simplification-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the release terminology proposal"
                )
        for current_interface in (
            SOURCE_ROOT / "endem" / "index.html",
            SOURCE_ROOT / "endem" / "docs" / "reference.md",
            SOURCE_ROOT / "endem" / "docs" / "format.md",
            SOURCE_ROOT / "endem" / "docs" / "running.md",
        ):
            interface_text = current_interface.read_text()
            for candidate_command in (
                "`endem form`",
                "`endem check`",
                "`endem compose`",
                "`endem inspect`",
                "`endem run`",
            ):
                if candidate_command in interface_text:
                    errors.append(
                        f"{current_interface.relative_to(SOURCE_ROOT)} exposes non-normative command candidate {candidate_command}"
                    )

    facet_terms_proposal = SOURCE_ROOT / "spec" / "semantic-facet-terminology-proposal.md"
    if not facet_terms_proposal.exists():
        errors.append("missing non-normative semantic facet terminology proposal")
    else:
        proposal_text = facet_terms_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定与人类验证",
            "不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求",
            "不进入 `registry.json`",
            "六个语义面与结构化观察的职责继续成立，不能合并",
            "没有通过专名必要性桌面门禁",
            "`source_expression`",
            "`meaning_projection`",
            "`situation`",
            "`goal_direction`",
            "`satisfaction_criteria`",
            "`unresolved_meaning`",
            "`structured_observation`",
            "ISO 704:2022",
            "GNU Coding Standards 的 Names 规则",
            "ISO/IEC/IEEE 29148:2018",
            "MCP 2025-11-25 Schema",
            "A2A Agent Discovery",
            "NIST AI RMF Core",
            "W3C PROV-DM",
            "W3C SOSA/SSN",
            "候选普通词不是字段别名、兼容键、自动规范化结果或现行接口",
            "数字记录布局",
            "新的规范与 Profile 身份",
        ):
            if token not in proposal_text:
                errors.append(f"semantic facet terminology proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "semantic-facet-terminology" in registry_text:
            errors.append("non-normative semantic facet terminology proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "design-system" / "name-audit.md",
            SOURCE_ROOT / "design-system" / "language-and-naming.md",
            SOURCE_ROOT / "docs" / "terminology-and-pronunciation.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "semantic-facet-terminology-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the semantic facet terminology proposal"
                )
        for current_interface in (
            SOURCE_ROOT / "spec" / "endem-core.md",
            SOURCE_ROOT / "spec" / "endem-format.md",
            SOURCE_ROOT / "spec" / "profiles" / "end-p1.json",
            SOURCE_ROOT / "endem" / "docs" / "format.md",
        ):
            interface_text = current_interface.read_text()
            for candidate_field in (
                "source_expression",
                "meaning_projection",
                "goal_direction",
                "satisfaction_criteria",
                "unresolved_meaning",
                "structured_observation",
            ):
                if candidate_field in interface_text:
                    errors.append(
                        f"{current_interface.relative_to(SOURCE_ROOT)} exposes non-normative facet candidate {candidate_field}"
                    )

    lifecycle_terms_proposal = SOURCE_ROOT / "spec" / "lifecycle-and-result-terminology-proposal.md"
    if not lifecycle_terms_proposal.exists():
        errors.append("missing non-normative lifecycle and result terminology proposal")
    else:
        proposal_text = lifecycle_terms_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：对象边界桌面审查完成；语义迁移与发行命名分别等待决定",
            "不构成 ADR、CORE 规范、内容 Profile、登记项、迁移决定或实现要求",
            "不进入 `registry.json`",
            "停止把 `attested` 作为 Endem 生命周期状态",
            "`content state: formed / resolved`",
            "signed-statement binding",
            "`satisfaction: met / unmet / undetermined / fault`",
            "`no_allowed_projection`",
            "`session: completed / failed / stopped`",
            "RFC 9334 RATS Architecture",
            "in-toto Attestation Framework",
            "GNU Automake",
            "MCP 2025-11-25 Tasks",
            "A2A 最新规范",
            "W3C SCXML",
            "NIST AI RMF Core",
            "候选词不是别名、兼容值或规范化结果",
            "subject.attested",
            "每次内容变化产生新身份",
            "## 两条迁移轴必须分开",
            "A · 对象边界",
            "B · 发行命名",
            "A 轴不引入 `formed`、`resolved` 或其他候选词",
            "### Dromen 主体准入需要显式关系集",
            "外部陈述集合",
            "验证记录",
            "依赖方判断",
            "至少一项由具名政策要求且在截止点适用的外部陈述",
            "### 主体准入反例矩阵",
            "### A 轴威胁清单",
            "多签截断",
            "内容自证",
            "### A 轴：对象边界修正",
            "暂时保留 `nascent / coherent`",
            "### B 轴：发行命名",
            "### 可验证的完成条件",
            "现行接口不再出现 Endem `attested` 或 Dromen `subject.attested`",
            "原有 `0.1` 内容静默改成另一套语义",
            "用户可以单独接受 A 轴",
            "这些结论不会在本轮改变任何现行规范值",
        ):
            if token not in proposal_text:
                errors.append(f"lifecycle terminology proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "lifecycle-and-result-terminology" in registry_text:
            errors.append("non-normative lifecycle terminology proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "design-system" / "name-audit.md",
            SOURCE_ROOT / "design-system" / "language-and-naming.md",
            SOURCE_ROOT / "docs" / "terminology-and-pronunciation.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "lifecycle-and-result-terminology-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the lifecycle terminology proposal"
                )
        for current_interface in (
            SOURCE_ROOT / "spec" / "endem-core.md",
            SOURCE_ROOT / "spec" / "dromen-core.md",
            SOURCE_ROOT / "spec" / "profiles" / "end-p1.json",
            SOURCE_ROOT / "vectors" / "dromen" / "cases.json",
            SOURCE_ROOT / "architecture" / "endem-lifecycle.html",
        ):
            interface_text = current_interface.read_text()
            for candidate_value in (
                "content state: formed",
                "content state: resolved",
                "satisfaction: undetermined",
                "no_allowed_projection",
                "session: stopped",
                "signed-statement binding",
            ):
                if candidate_value in interface_text:
                    errors.append(
                        f"{current_interface.relative_to(SOURCE_ROOT)} exposes non-normative lifecycle candidate {candidate_value}"
                    )

    preview_proposal = SOURCE_ROOT / "spec" / "preview-simulation-and-approval-proposal.md"
    if not preview_proposal.exists():
        errors.append("missing non-normative preview, simulation, and approval research proposal")
    else:
        proposal_text = preview_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "六类事实必须分开",
            "GNU Make",
            "MCP 2025-11-25",
            "A2A 1.0.0",
            "OpenAI Agents SDK",
            "NIST AI 600-1",
            "预览",
            "模拟或 dry-run",
            "授权决定",
            "执行尝试",
            "事后观察",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"preview and approval proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "preview-simulation-and-approval" in registry_text:
            errors.append("non-normative preview and approval proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "authority.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "preview-simulation-and-approval-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the preview and approval research proposal"
                )

    memory_proposal = SOURCE_ROOT / "spec" / "memory-checkpoint-and-resumption-proposal.md"
    if not memory_proposal.exists():
        errors.append("missing non-normative memory, checkpoint, and resumption research proposal")
    else:
        proposal_text = memory_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "八类状态必须分开",
            "OpenAI Agents SDK",
            "MCP 2025-11-25 Tasks",
            "2026-07-28 发布候选",
            "A2A 1.0",
            "GNU Make",
            "GNU Guix",
            "恢复必须是重新验证，不是复活",
            "继续、重放、重试与回滚必须分开",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "等待决定",
        ):
            if token not in proposal_text:
                errors.append(f"memory and resumption proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "memory-checkpoint-and-resumption" in registry_text:
            errors.append("non-normative memory and resumption proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "dromen.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
        ):
            if "memory-checkpoint-and-resumption-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the memory and resumption research proposal"
                )

    capability_proposal = SOURCE_ROOT / "spec" / "capability-discovery-and-negotiation-proposal.md"
    if not capability_proposal.exists():
        errors.append("missing non-normative capability discovery and negotiation research proposal")
    else:
        proposal_text = capability_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "六类事实必须分开",
            "MCP 2025-11-25 生命周期",
            "A2A 1.0 规范",
            "RFC 8707",
            "GNU Autoconf 2.73",
            "新能力不能扩写旧 Dromen",
            "候选责任的唯一主归属",
            "十二个案例",
            "变化处理矩阵",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "不创建 `CAP-CORE`、能力制品或新专名",
            "这些结论不会在本轮改变任何现行规范条款、登记、向量、Dromen 字段或结果值",
        ):
            if token not in proposal_text:
                errors.append(f"capability discovery proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "capability-discovery-and-negotiation" in registry_text or '"CAP-CORE"' in registry_text:
            errors.append("non-normative capability discovery proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "adapters.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "capability-discovery-and-negotiation-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the capability discovery research proposal"
                )

    parallel_proposal = SOURCE_ROOT / "spec" / "parallel-and-speculative-execution-proposal.md"
    if not parallel_proposal.exists():
        errors.append("missing non-normative parallel and speculative execution research proposal")
    else:
        proposal_text = parallel_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "并行调度、分支完成、候选结果、提交授权、外部副作用和目标满足是六种不同事实",
            "不构成 ADR、CORE 规范、Profile 或实现要求",
            "不创建并行制品、事务格式、分支对象、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "七个阶段必须分开",
            "MCP 2025-11-25 Tasks",
            "MCP Sampling 草案",
            "MCP `2026-07-28` 发布候选",
            "A2A 1.0 版本化规范",
            "GNU Make jobserver",
            "RFC 9110 第 13.1.1 节",
            "取消失败分支只能请求停止尚未发生的工作",
            "操作类别与并行资格",
            "案例十四：孤儿副作用",
            "提交前重新核对矩阵",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "不建立 `PAR-CORE`、分支制品或事务格式",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"parallel execution proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "parallel-and-speculative-execution" in registry_text or '"PAR-CORE"' in registry_text:
            errors.append("non-normative parallel execution proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "adapters.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "parallel-and-speculative-execution-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the parallel execution research proposal"
                )

    isolation_proposal = SOURCE_ROOT / "spec" / "model-adapter-isolation-proposal.md"
    if not isolation_proposal.exists():
        errors.append("missing non-normative model, adapter and capability isolation research proposal")
    else:
        proposal_text = isolation_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "隔离不是单一开关、进程或产品名称",
            "不构成 ADR、CORE 规范、Profile 或实现要求",
            "不创建隔离制品、沙箱格式、部署对象、命令、组件、结果域、稳定接口或哲学专名",
            "不创建 `ISO-CORE`、`SANDBOX-CORE`",
            "不进入 `registry.json`",
            "十个责任面必须分开",
            "MCP Security Best Practices",
            "A2A 1.0 版本化规范",
            "Linux `no_new_privs`",
            "Seccomp 不是完整沙箱",
            "Landlock",
            "cgroup v2",
            "GNU Guix",
            "GNU Coreutils `timeout`",
            "十六个案例",
            "隔离控制矩阵",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"model adapter isolation proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "model-adapter-isolation" in registry_text
            or '"ISO-CORE"' in registry_text
            or '"SANDBOX-CORE"' in registry_text
        ):
            errors.append("non-normative isolation proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "dromen.html",
            SOURCE_ROOT / "specifications" / "adapters.html",
            SOURCE_ROOT / "components" / "drasor.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "model-adapter-isolation-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the model adapter isolation research proposal"
                )

    model_evaluation_proposal = SOURCE_ROOT / "spec" / "model-assisted-evaluation-proposal.md"
    if not model_evaluation_proposal.exists():
        errors.append("missing non-normative model-assisted evaluation research proposal")
    else:
        proposal_text = model_evaluation_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "评测至少包含九种不同事实",
            "不构成 ADR、CORE 规范、Profile、登记项或实现要求",
            "不创建评测制品、裁判对象、评分格式、基准格式、命令、组件、结果域、稳定接口或哲学专名",
            "不建立 `EVAL-CORE`、`JUDGE-CORE`",
            "不进入 `registry.json`",
            "九种事实必须分开",
            "NIST AI 800-2 Initial Public Draft",
            "NIST AI 800-3",
            "NeurIPS 2023 的 LLM-as-a-Judge 研究",
            "ICLR 2025 的系统偏差研究",
            "NeurIPS 2025 的偏差检测研究",
            "GNU Diffutils",
            "GNU Coreutils 随机来源",
            "什么时候可以使用模型评审",
            "偏差与稳健性探针",
            "十六个案例",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"model-assisted evaluation proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "model-assisted-evaluation" in registry_text
            or '"EVAL-CORE"' in registry_text
            or '"JUDGE-CORE"' in registry_text
        ):
            errors.append("non-normative model-assisted evaluation proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "iknem.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "development" / "testing.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "model-assisted-evaluation-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the model-assisted evaluation research proposal"
                )

    model_training_proposal = SOURCE_ROOT / "spec" / "model-training-and-update-boundaries-proposal.md"
    if not model_training_proposal.exists():
        errors.append("missing non-normative model training and update research proposal")
    else:
        proposal_text = model_training_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "至少十一种事实必须分开",
            "不构成 ADR、CORE 规范、Profile、登记项或实现要求",
            "不创建模型制品、数据集格式、训练清单格式、反馈格式、模型仓库、训练平台、命令、组件、结果域、稳定接口或哲学专名",
            "不建立 `TRAIN-CORE`、`MODEL-CORE` 或 `FEEDBACK-CORE`",
            "不进入 `registry.json`",
            "会话、检索、提示与训练不是同一更新",
            "反馈先是记录，之后才可能成为训练输入",
            "可复现环境不等于可复现模型",
            "NIST AI 600-1 Generative AI Profile",
            "NIST SP 800-218A",
            "NeurIPS 2022 的 RLHF 研究",
            "NeurIPS 2023 的 DPO 研究",
            "Nature 2024 的递归生成数据研究",
            "GNU Guix 参考手册",
            "GNU Diffutils",
            "支持案例与反例",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "术语和读音边界",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"model training proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "model-training-and-update" in registry_text
            or '"TRAIN-CORE"' in registry_text
            or '"MODEL-CORE"' in registry_text
            or '"FEEDBACK-CORE"' in registry_text
        ):
            errors.append("non-normative model training proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "identity.html",
            SOURCE_ROOT / "specifications" / "iknem.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "development" / "testing.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "model-training-and-update-boundaries-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the model training and update research proposal"
                )

    model_openness_proposal = SOURCE_ROOT / "spec" / "model-openness-and-software-freedom-boundaries-proposal.md"
    if not model_openness_proposal.exists():
        errors.append("missing non-normative model openness and software freedom research proposal")
    else:
        proposal_text = model_openness_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "至少十二种事实必须分开",
            "不构成 ADR、CORE 规范、Profile、登记项、法律意见或实现要求",
            "不建立 `OPEN-MODEL-CORE`、`LICENSE-CORE`",
            "不进入 `registry.json`",
            "GNU 软件自由适用于软件，不自动解决模型全栈",
            "OSI Open Source AI Definition 1.0 的采用边界",
            "开放完整性、许可和复现是三条证据轴",
            "NIST AI 600-1",
            "NIST SP 800-218A",
            "Linux Foundation Model Openness Framework Specification",
            "Apache License 2.0",
            "开放权重",
            "首选修改形式",
            "支持案例与反例",
            "威胁到失败责任的映射",
            "候选责任的唯一主归属",
            "术语和读音边界",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"model openness proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "model-openness-and-software-freedom" in registry_text
            or '"OPEN-MODEL-CORE"' in registry_text
            or '"LICENSE-CORE"' in registry_text
        ):
            errors.append("non-normative model openness proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "downloads" / "index.html",
            SOURCE_ROOT / "faq" / "index.html",
            SOURCE_ROOT / "docs" / "installation-and-usage.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "model-openness-and-software-freedom-boundaries-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the model openness research proposal"
                )

    hosted_service_proposal = SOURCE_ROOT / "spec" / "hosted-ai-service-and-user-control-boundaries-proposal.md"
    if not hosted_service_proposal.exists():
        errors.append("missing non-normative hosted AI service and user control research proposal")
    else:
        proposal_text = hosted_service_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "结论状态：桌面审查完成；等待用户决定",
            "至少十六种事实必须分开",
            "不构成 ADR、CORE 规范、Profile、登记项、许可选择、部署决定或实现要求",
            "不建立 `SERVICE-CORE`、`CLOUD-CORE`、`PORTABILITY-CORE`",
            "不进入 `registry.json`",
            "先分开三种网络关系",
            "GNU 对他人服务替代用户计算的质疑",
            "AGPL 提供源码，不提供服务实例控制",
            "MCP 2025-11-25 Sampling",
            "MCP 2025-11-25 Authorization",
            "NIST AI 600-1",
            "NIST SP 800-218A",
            "数据控制是逐端点、逐功能的",
            "支持案例与反例",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "采用托管路径前的最小问题清单",
            "术语和读音边界",
            "等待用户决定",
        ):
            if token not in proposal_text:
                errors.append(f"hosted AI service proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "hosted-ai-service-and-user-control" in registry_text
            or '"SERVICE-CORE"' in registry_text
            or '"CLOUD-CORE"' in registry_text
            or '"PORTABILITY-CORE"' in registry_text
        ):
            errors.append("non-normative hosted AI service proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "spec" / "model-openness-and-software-freedom-boundaries-proposal.md",
            SOURCE_ROOT / "downloads" / "index.html",
            SOURCE_ROOT / "faq" / "index.html",
            SOURCE_ROOT / "docs" / "installation-and-usage.md",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.html",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "content-quality-audit.md",
        ):
            if "hosted-ai-service-and-user-control-boundaries-proposal.md" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the hosted AI service research proposal"
                )

    agent_boundaries = SOURCE_ROOT / "architecture" / "agent-system-boundaries.html"
    if not agent_boundaries.exists():
        errors.append("missing public Agent system boundary guide")
    else:
        boundary_text = agent_boundaries.read_text()
        for token in (
            "三种状态不得混写",
            "运行事实应该放在哪里",
            "十三条最危险的越级路径",
            "当前 Agent 技术趋势改变了什么",
            "GNU 技术与软件自由提供的十一个约束",
            "十三项研究怎样回到现有规范",
            "2025-11-25",
            "2026-07-28",
            "A2A 1.0 版本化规范",
            "OpenAI Agents SDK handoffs",
            "OpenAI Agents SDK human-in-the-loop",
            "OpenAI Agents SDK sessions",
            "OpenAI Agents SDK tracing",
            "Make target、prerequisite 与 recipe",
            "Guix profile generations",
            "Autoconf feature checks",
            "Make parallel execution",
            "Guix shell",
            "Coreutils timeout",
            "沙箱名称替代隔离证据",
            "模型评分替代测量与决定",
            "反馈替代训练资格与发布决定",
            "可下载替代自由与可修改性",
            "服务可用替代用户控制",
            "NIST AI 800-2 初稿",
            "NIST AI 600-1",
            "NIST SP 800-218A",
            "Guix channel、manifest 与 time-machine",
            "Diffutils",
            "随机来源",
            "GNU 自由软件四项自由",
            "OSI Open Source AI Definition 1.0",
            "Model Openness Framework",
            "他人服务替代用户计算",
            "AGPL 边界",
        ):
            if token not in boundary_text:
                errors.append(f"Agent boundary guide missing cross-domain contract: {token}")
        for proposal_name in (
            "model-context-assembly-proposal.md",
            "planning-and-replanning-proposal.md",
            "state-change-and-causal-attribution-proposal.md",
            "preview-simulation-and-approval-proposal.md",
            "memory-checkpoint-and-resumption-proposal.md",
            "capability-discovery-and-negotiation-proposal.md",
            "parallel-and-speculative-execution-proposal.md",
            "model-adapter-isolation-proposal.md",
            "model-assisted-evaluation-proposal.md",
            "model-training-and-update-boundaries-proposal.md",
            "model-openness-and-software-freedom-boundaries-proposal.md",
            "hosted-ai-service-and-user-control-boundaries-proposal.md",
            "semantic-equivalence-and-migration-proposal.md",
        ):
            if proposal_name not in boundary_text:
                errors.append(f"Agent boundary guide must link research input: {proposal_name}")
        for public_source in (
            SOURCE_ROOT / "architecture" / "index.html",
            SOURCE_ROOT / "architecture" / "open-questions.html",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "development" / "implementation-roadmap.html",
            SOURCE_ROOT / "README.md",
            SOURCE_ROOT / "sitemap.md",
            SOURCE_ROOT / "_data" / "navigation.yml",
        ):
            if "agent-system-boundaries" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the Agent system boundary guide"
                )

    verification_page = SOURCE_ROOT / "development" / "testing.html"
    verification_text = verification_page.read_text()
    for token in (
        "形成、变换与复现必须分开",
        "来源与文本变换",
        "确定性形成",
        "显示与导出",
        "回转与迁移",
        "独立复现",
        "当前没有通用 round-trip 或跨 Profile 语义等价要求",
        "GNU Guix challenge",
        "GNU BFD canonical form",
        "RFC 8785 JSON Canonicalization Scheme",
        "OpenAI Structured Outputs",
        "schema 合规只证明形状",
        "模型参与评测必须限定用途",
        "模型评分是有版本、有偏差且可能漂移的候选测量",
        "偏差探针",
        "model-assisted-evaluation-proposal.md",
        "NIST AI 800-2 初稿",
        "GNU Diffutils",
        "模型更新必须重新建立证据链",
        "训练完成、损失下降、固定种子或部署回滚",
        "model-training-and-update-boundaries-proposal.md",
        "NIST AI 600-1",
        "NIST SP 800-218A",
        "GNU Guix",
    ):
        if token not in verification_text:
            errors.append(f"testing guide missing bounded verification claim: {token}")
    forbidden_round_trip_claims = {
        SOURCE_ROOT / "development" / "testing.html": (
            "规范文本 → Endem → 规范文本往返保持规范化等价",
        ),
        SOURCE_ROOT / "spec" / "endem-core.md": (
            "相同的规范化来源",
        ),
        SOURCE_ROOT / "endem" / "docs" / "format.md": (
            "相同的规范化来源",
        ),
    }
    for source, forbidden_phrases in forbidden_round_trip_claims.items():
        source_text = source.read_text()
        for phrase in forbidden_phrases:
            if phrase in source_text:
                errors.append(
                    f"{source.relative_to(SOURCE_ROOT)} retains an overclaimed round-trip boundary: {phrase}"
                )

    semantic_vector_count = len(list((SOURCE_ROOT / "vectors" / "semantic").glob("*.json")))
    p0_wire_count = len(
        json.loads((SOURCE_ROOT / "vectors" / "wire" / "manifest.json").read_text())["vectors"]
    )
    p1_wire_count = len(
        json.loads((SOURCE_ROOT / "vectors" / "wire" / "p1" / "manifest.json").read_text())["vectors"]
    )
    downloads_text = (SOURCE_ROOT / "downloads" / "index.html").read_text()
    for token in (
        f"{semantic_vector_count} 个 Endem 语义 JSON 向量",
        f"{p0_wire_count} 个 END-P0 结构字节",
        f"{p1_wire_count} 个 END-P1 字节",
    ):
        if token not in downloads_text:
            errors.append(f"downloads page has stale vector inventory: expected {token}")
    for token in (
        "先把变更写成可验证主张",
        "当前最多能声称",
        "Chrome 阅读检查",
        "外部成功不等于本地满足或接受",
        "各向量集合的精确数量和执行结果以机器可读条款登记与对应测试输出为准",
        "不在说明页重复容易漂移的计数",
    ):
        if token not in verification_text:
            errors.append(f"testing guide missing change-to-evidence boundary: {token}")
    for stale_count in ("十五个 Iknem", "十八个 Iknem"):
        if stale_count in verification_text:
            errors.append("testing guide must not copy drift-prone Iknem vector counts")
    development_guide_text = (SOURCE_ROOT / "docs" / "development-guide.md").read_text()
    for token in (
        "先写一句可被反例推翻的主张",
        "当前没有适配器实现",
        "未执行不能写成通过",
        "最多只能声称规范和案例保持一致",
    ):
        if token not in development_guide_text:
            errors.append(f"development guide missing falsifiable change boundary: {token}")
    for source in (
        SOURCE_ROOT / "components" / "ktisor.html",
        SOURCE_ROOT / "development" / "testing.html",
        SOURCE_ROOT / "development" / "implementation-roadmap.html",
    ):
        source_text = source.read_text()
        for phrase in ("相同规范化输入", "前后六个语义面、依赖与披露行为保持规范等价"):
            if phrase in source_text:
                errors.append(
                    f"{source.relative_to(SOURCE_ROOT)} retains an undefined verification claim: {phrase}"
                )
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

    content_audit = SOURCE_ROOT / "content-quality-audit.md"
    if not content_audit.exists():
        errors.append("missing content-quality-audit.md")
    else:
        audit_text = content_audit.read_text()
        inventory_match = re.search(
            r"## 公共页面结构审计.*?\n(.*?)\n## 全站逐页可读性复核",
            audit_text,
            re.DOTALL,
        )
        if inventory_match is None:
            errors.append("content quality audit missing bounded HTML source inventory")
        else:
            audit_rows = re.findall(r"\| `([^`]+\.html)` \|", inventory_match.group(1))
            audited_pages = [row for row in audit_rows if not row.startswith("_")]
            expected_pages = [path.relative_to(SOURCE_ROOT).as_posix() for path in SOURCE_HTML_FILES]
            if len(audited_pages) != len(set(audited_pages)):
                errors.append("content quality audit contains duplicate HTML page rows")
            if set(audited_pages) != set(expected_pages):
                errors.append(
                    "content quality audit HTML inventory mismatch: "
                    f"missing={sorted(set(expected_pages) - set(audited_pages))}, "
                    f"extra={sorted(set(audited_pages) - set(expected_pages))}"
                )
        if f"当前共有 {len(SOURCE_HTML_FILES)} 个 HTML 正文源" not in audit_text:
            errors.append("content quality audit HTML source count is stale")
        if f"登记的 {len(registered)} 条正式路由" not in audit_text:
            errors.append("content quality audit formal route count is stale")
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
    errors.extend(validate_prose_readability_contracts())

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
        if re.search(r"(?:尚|仍)待(?:确认|确)定定", body):
            errors.append(f"{route}: contains duplicated wording in a pending-status sentence")
        for obsolete_phrase in ("设计提案", "未来阶段", "阶段门", "证据门", "退出证据", "放行"):
            if obsolete_phrase in body:
                errors.append(f"{route}: retains internal or obsolete status wording {obsolete_phrase!r}")
        if re.search(r"供[^。；<\n]{0,40}消费", body):
            errors.append(f"{route}: uses mechanical '供...消费' wording instead of naming the reader")
        errors.extend(validate_public_html(route, body))
        if forbidden_shell.search(body):
            errors.append(f"{route}: page shell must come from the Jekyll layout")
        if is_manual_markdown:
            for key in ("manual_id", "manual_group", "manual_order", "nav_title", "page_heading", "page_lead"):
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
        homepage_text = homepage_source.read_text()
        for token in (
            'title: "Noemion · 人工智能时代的自然语言目标规范"',
            '<h1 id="portal-title"><span class="portal-title-brand">Noemion</span><strong><span>定义人工智能时代的</span><span>自然语言目标规范</span><span class="portal-title-foundation">奠定可验证智能的工程基石</span></strong></h1>',
            '<p class="portal-introduction-summary">Noemion 正在定义一套面向人工智能时代的目标制品、组合规则与验收边界，让自然语言目标能够被确定地表达、受控地实现并由有范围的证据检验。Endem 是这套体系中的最小目标制品。</p>',
            '<span>了解 Noemion</span>',
            '<span>查看 Noemion 架构</span>',
            '<strong>Noemion</strong> 是整个项目、新领域与社区的名称',
        ):
            if token not in homepage_text:
                errors.append(f"index.html: missing Noemion project ownership contract: {token}")
        for forbidden in (
            "Noemion 只是项目",
            "而成为 Endem",
            "认识 Endem",
            "六个短词",
        ):
            if forbidden in homepage_text:
                errors.append(f"index.html: Endem must not replace the Noemion project identity: {forbidden}")
        expression_visual_match = re.search(
            r'<span class="feature-visual feature-visual-expression".*?</span>',
            homepage_text,
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
        for token in (
            'class="portal-focus-card focus-card-endem" href="specifications/endem.html"',
            'class="portal-focus-card focus-card-synem" href="specifications/synem.html"',
            'class="portal-focus-card focus-card-dromen" href="specifications/dromen.html"',
            'class="portal-focus-card focus-card-iknem" href="specifications/iknem.html"',
        ):
            if token not in homepage_text:
                errors.append(f"index.html: missing independent homepage object card: {token}")
        if homepage_text.count('class="portal-focus-card ') != 4:
            errors.append("index.html: FOUR NOUNS must render four independent object cards")

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
            "{% include docs-rail.html %}",
            "{{ '/assets/style.css' | relative_url }}",
            "{{ '/assets/directory.css' | relative_url }}",
            "{{ '/assets/theme.js' | relative_url }}",
            "{{ '/assets/mobile-directory-guard.js' | relative_url }}",
            "{{ '/assets/site.mjs' | relative_url }}",
            'type="module"',
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
            "data-directory-backdrop",
            "data-site-timeline",
            "<span>导航</span>",
            'class="directory-loading-status" role="status"',
            "正在载入目录…",
            "global-timeline-value",
            "site.data.site_header.timeline",
            "header_timeline.href",
            "header_timeline.aria_label",
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
            "global-stage-",
            "global-timeline-mark",
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

    directory_guard = SOURCE_ROOT / "assets/mobile-directory-guard.js"
    if not directory_guard.exists():
        errors.append("missing assets/mobile-directory-guard.js")
    else:
        guard_text = directory_guard.read_text()
        for token in (
            'document.addEventListener("click"',
            'window.matchMedia("(max-width: 999px)")',
            '".global-directory-panel > summary"',
            "event.preventDefault()",
            'data-mobile-directory-pending-open',
            '".global-directory-panel[open]"',
            "shouldContainScrollGesture",
            'document.addEventListener("wheel", containWheel, { passive: false, capture: true })',
            'document.addEventListener("touchstart", rememberTouch, { passive: false, capture: true })',
            'document.addEventListener("touchmove", containTouch, { passive: false, capture: true })',
            'document.addEventListener("touchend", forgetTouch, { passive: true, capture: true })',
            'document.addEventListener("touchcancel", forgetTouch, { passive: true, capture: true })',
            'document.addEventListener("keydown", containKeyboardScroll, { capture: true })',
            'const pageScrollKeys = new Set([',
            'window.visualViewport?.addEventListener("resize", syncViewportHeight, { passive: true })',
            'window.addEventListener("orientationchange", syncViewportHeight, { passive: true })',
            'window.visualViewport?.height || window.innerHeight',
            'root.style.setProperty(viewportHeightProperty, `${Math.round(viewportHeight)}px`)',
            "if (touchY === null)",
            'panel.open = pendingOpen',
            'window.noemionMobileDirectoryScroll = Object.freeze',
            'root.classList.add("mobile-directory-open")',
            'root.classList.remove("mobile-directory-open")',
            'root.style.removeProperty(viewportHeightProperty)',
            'toggleAttribute("aria-busy", pendingOpen)',
            'panel.dispatchEvent(new CustomEvent("noemion:directoryrequest"))',
        ):
            if token not in guard_text:
                errors.append(f"mobile directory first-open guard missing contract: {token}")
        for forbidden in (
            "scrollPositionAttribute",
            "scrollOffsetProperty",
            "holdLockedPagePosition",
            "--mobile-directory-scroll-offset",
            "window.scrollTo(0, scrollY)",
            "document.body.scrollTop = scrollY",
        ):
            if forbidden in guard_text:
                errors.append(f"mobile directory guard must not reposition page content: {forbidden}")

    style = SOURCE_ROOT / "assets/style.css"
    directory_style = SOURCE_ROOT / "assets/directory.css"
    if style.exists() and directory_style.exists():
        stylesheet_texts = {
            "style.css": style.read_text(),
            "directory.css": directory_style.read_text(),
        }
        shared_css = "".join(stylesheet_texts.values())

        def media_block_ranges(css, marker):
            ranges = []
            search_from = 0
            while True:
                marker_start = css.find(marker, search_from)
                if marker_start < 0:
                    break
                block_start = css.find("{", marker_start + len(marker))
                if block_start < 0:
                    break
                depth = 1
                cursor = block_start + 1
                while cursor < len(css) and depth:
                    if css[cursor] == "{":
                        depth += 1
                    elif css[cursor] == "}":
                        depth -= 1
                    cursor += 1
                if depth:
                    break
                ranges.append((block_start + 1, cursor - 1))
                search_from = cursor
            return ranges

        hover_media = "@media(hover:hover) and (pointer:fine)"
        for stylesheet_name, stylesheet_text in stylesheet_texts.items():
            hover_ranges = media_block_ranges(stylesheet_text, hover_media)
            if not hover_ranges:
                errors.append(f"{stylesheet_name} must define capability-scoped hover feedback")
                continue
            escaped_hover_positions = [
                match.start()
                for match in re.finditer(r"(?<![A-Za-z0-9_-]):hover\b", stylesheet_text)
                if not any(start <= match.start() < end for start, end in hover_ranges)
            ]
            if escaped_hover_positions:
                errors.append(f"{stylesheet_name} exposes hover feedback to touch scrolling")

        for token in (
            "@media(hover:none) and (pointer:coarse)",
            "-webkit-tap-highlight-color:transparent",
        ):
            if token not in shared_css:
                errors.append(f"shared styles missing touch-scroll feedback guard: {token}")

        for token in (
            'body[data-page-role="tool-project"]',
            'body[data-docs-layout="true"]',
            ".global-nav-menu",
            ".global-nav-visual",
            "calc(var(--nav-order) * 45ms)",
            "prefers-reduced-motion:reduce",
            "body .global-brand .portal-brand-mark{color:#10261e;background:#f0f6f3}",
            ".global-timeline-value{",
            "width:100%;height:100%;min-width:96px;min-height:64px",
            "background:transparent;border-left:1px solid var(--rule)",
            "background:color-mix(in srgb,var(--nav-bg) 78%,var(--accent-soft))",
            ".content-split{",
            ".content-split-reverse{",
            'body[data-page-role="content"]:not([data-docs-layout="true"]) main:not(.current-stage-page)>section :is(p,li,blockquote)',
            ".content-stack",
            ".content-band{",
            ".content-wide",
            ".content-grid{",
            ".content-rows",
            'body:not([data-page-role="portal"]) .page-link:nth-child(2n)',
            'a:visited:not(.portal-button)',
            ".portal-button-primary:visited",
            ".portal-button-secondary:visited",
            '@media(max-width:999px)',
            'body:not([data-page-role="portal"]) .global-directory-panel',
            'transition-duration:180ms;transition-timing-function:cubic-bezier(.2,0,0,1);transition-delay:0s',
            '.site-header .directory-panel.is-closing nav',
            'html.mobile-directory-open{overscroll-behavior:none}',
            'background:color-mix(in srgb,var(--paper) 98%,transparent);backdrop-filter:none;-webkit-backdrop-filter:none',
            '.global-directory-panel[open]>.mobile-directory-backdrop{',
            'position:fixed;inset:0;z-index:1;display:block;background:transparent',
            'transition-property:opacity,transform,visibility',
            'will-change:opacity,transform;contain:layout paint;backface-visibility:hidden',
            'height:auto;max-height:calc(var(--mobile-directory-viewport-height,100dvh) - 72px)',
            'html.mobile-directory-open body:not([data-page-role="portal"]) .global-directory-panel nav{',
            'height:auto;max-height:calc(var(--mobile-directory-viewport-height,100dvh) - 120px)',
            'touch-action:pinch-zoom',
            'isolation:isolate',
            'overflow-anchor:none;overscroll-behavior:none',
            '.nav-section-links{min-height:0;overflow:hidden;overflow:clip}',
            '.directory-loading-status{display:none',
            'nav[aria-busy="true"] .directory-loading-status',
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
            "clip-path:var(--module-introduction-clip)",
            "clip-path:var(--module-card-clip)",
            "radial-gradient(circle at var(--module-node-1)",
            'body[data-docs-layout="true"] .manual-introduction::before{',
            "clip-path:polygon(0 0,74% 0,100% 26%,100% 100%,0 100%)",
            'body .global-brand{grid-column:1;min-width:0;overflow:hidden',
            'body .global-brand>span:last-child{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
            'body[data-page-role="portal"] .global-header-inner{grid-template-columns:minmax(0,1fr) clamp(102px,30vw,124px) 84px}',
            'body[data-page-role="portal"] .global-timeline-link{width:100%;min-width:0;padding:0}',
            'body[data-page-role="portal"] .global-timeline-value{width:100%;min-width:0;padding-inline:7px;font-size:10px;letter-spacing:.04em}',
            '.portal-focus-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))',
            '.focus-card-dromen .focus-art',
            '.focus-card-iknem .focus-art',
            'text-decoration-color:color-mix(in srgb,var(--portal-coral) 54%,var(--portal-amber))',
            'text-decoration-thickness:.1em;text-underline-offset:.12em;text-decoration-skip-ink:none',
        ):
            if token not in shared_css:
                errors.append(f"shared styles missing site-wide design contract: {token}")
        if re.search(r"transition\s*:\s*all\b", shared_css):
            errors.append("shared styles must not use transition: all")
        if re.search(r"html\.mobile-directory-open\s+body\s*\{", shared_css):
            errors.append("mobile directory must not replace body layout while the overlay is open")
        if re.search(r"html\.mobile-directory-open\s*\{[^}]*overflow\s*:", shared_css):
            errors.append("mobile directory must not change root overflow while the overlay is open")
        if re.search(
            r"\.site-header\s+\.directory-panel(?:\:not\(\[open\]\)|\.is-closing)?\s+nav\s*\{[^}]*filter:",
            shared_css,
            re.DOTALL,
        ):
            errors.append("mobile directory overlay must not animate a full-panel blur filter")
        if "max-height:calc(100vh - 72px)" in shared_css:
            errors.append("mobile directory must use the dynamic viewport height on iOS")
        if "-webkit-overflow-scrolling:touch" in shared_css:
            errors.append("mobile directory must not restore the obsolete WebKit momentum-scrolling workaround")
        if "@media(min-width:840px) and (max-width:999px)" in shared_css:
            errors.append("compact layouts must not restore hover navigation on iPhone landscape widths")
        if ".focus-card-core" in shared_css:
            errors.append("homepage object visuals must not retain the obsolete unmatched focus-card-core selector")
        if re.search(r"\.global-timeline-link\s*\{[^}]*background\s*:\s*#fff", shared_css):
            errors.append("TIMELINE must use the theme navigation surface instead of pure white")
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
            "global-stage-",
            "global-stage-pulse",
            "global-stage-text-flow",
            "global-stage-sheen",
            "global-timeline-mark",
        ):
            if obsolete_stage_motion in shared_css:
                errors.append(
                    f"shared styles retain obsolete stage animation: {obsolete_stage_motion}"
                )
        if re.search(
            r'body\[data-docs-layout="true"\]\s+\.manual-introduction::before,\s*'
            r'body\[data-docs-layout="true"\]\s+\.manual-introduction::after\s*\{display:none\}',
            shared_css,
        ):
            errors.append("manual introductions must preserve their folded-page geometry")
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

    navigation_config = SOURCE_ROOT / "_data/navigation.yml"
    if navigation_config.exists():
        declared = {
            href.lstrip("/")
            for href in NAVIGATION_HREF.findall(navigation_config.read_text())
        }
        registered_set = set(registered)
        manual_routes = {route for route, path in source_entries if path.suffix == ".md"}
        if not declared <= registered_set:
            errors.append("navigation data contains links outside the formal route registry")
        missing_static = sorted((registered_set - manual_routes) - declared)
        if missing_static:
            errors.append(f"navigation data does not cover non-manual routes: {missing_static}")
    else:
        errors.append("missing _data/navigation.yml")

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
        "frontend-architecture": "frontend-architecture.md",
    }
    design_root = SOURCE_ROOT / "design-system"
    protocol_reference_files = [*SOURCE_PAGE_FILES, *design_root.glob("*.md")]
    for protocol_reference_file in protocol_reference_files:
        protocol_reference_text = protocol_reference_file.read_text()
        if "a2a-protocol.org/latest/" in protocol_reference_text:
            errors.append(
                f"{protocol_reference_file.relative_to(SOURCE_ROOT)}: A2A evidence must use a versioned specification URL"
            )
        if re.search(r"\bA2A\s+1\.0\.1\b", protocol_reference_text):
            errors.append(
                f"{protocol_reference_file.relative_to(SOURCE_ROOT)}: A2A patch version labels must not be presented as the negotiated protocol version"
            )

    external_boundary_contracts = {
        "architecture/decisions.html": (
            "A2A 1.0 版本化规范",
            "补丁号不进入协议协商",
            "github.com/open-telemetry/semantic-conventions-genai",
            "MCP 2025-11-25 稳定规范",
            "GNU Automake 测试结果语义",
            "后续版本在正式发布",
            "敏感内容不得默认导出",
            "NIST AI RMF 与 GenAI Profile",
            "外部协议适配不变量",
            "身份不等于权威",
            "外部状态不等于本地结果",
            "能力声明不等于实时句柄",
            "遥测单向外送",
            "撤销与重放显式",
        ),
        "components/drasor.html": (
            "A2A 1.0 版本化规范",
            "令牌必须绑定目标资源",
            "github.com/open-telemetry/semantic-conventions-genai",
            "默认不导出正文",
            "completed / failed / interrupted",
            "不得推成",
        ),
        "development/implementation-roadmap.html": (
            "补丁号不进入协议协商",
            "5 月 21 日",
            "不作为当前符合性基线",
            "任何后续正式版本",
            "默认脱敏的导出器",
            "不进入 Endem 编码、Iknem 身份或最终决定",
            "扩大范围前需要的证据",
            "不再扩大或需要合并的条件",
        ),
        "endem/docs/running.md": (
            "A2A 1.0 版本化规范",
            "后续正式版本",
            "默认不导出正文",
            "不构成 Iknem 身份",
        ),
        "architecture/adr-0016-mene-time-model.html": (
            "RFC 3339",
            "RFC 9557",
            "GNU C Library 时钟说明",
            "GNU Coreutils 相对日期说明",
            "W3C OWL-Time",
            "OpenTelemetry Metrics 数据模型",
            "A2A 1.0",
            "不会直接进入 Endem",
        ),
        "architecture/adr-0017-negation-and-absence.html": (
            "W3C OWL 2 Primer",
            "W3C SHACL 封闭约束",
            "SPARQL 1.1 NOT EXISTS",
            "GNU grep 输出控制",
            "OpenTelemetry Logs 数据模型",
            "不把 OWL 个体、SHACL Shape 或 RDF 数据集直接变成 Endem 字段",
            "查询没有匹配只说明该查询范围",
            "一次无匹配不能越过搜索范围成为普遍否定",
            "这份数据模型本身不证明日志流完整",
        ),
        "architecture/adr-0018-quantification-and-membership.html": (
            "SHACL 2017 Recommendation",
            "SHACL 1.2",
            "2026 Working Draft",
            "OWL 2",
            "COUNT(DISTINCT",
            "GNU",
            "一次文件搜索不能自行证明",
            "Noemion 的结果域、空集合政策和信任边界仍由 END-CORE 自己规定",
        ),
        "architecture/adr-0019-measurement-and-thresholds.html": (
            "NIST AI 800-2 Initial Public Draft",
            "NIST AI 800-3",
            "固定基准准确率与泛化准确率",
            "OpenTelemetry Metrics 数据模型",
            "Prometheus 直方图与摘要指南",
            "GNU Units 手册",
            "遥测流本身不选择",
            "不能决定业务总体、聚合器或阈值",
        ),
        "architecture/adr-0020-composite-situations-and-criteria.html": (
            "W3C SHACL Recommendation",
            "SHACL 1.2 Core",
            "Working Draft",
            "GNU Coreutils test",
            "GNU Bash Lists",
            "NIST AI 800-2 Initial Public Draft",
            "不采用 RDF Shape 或二值符合性",
            "只借鉴减少不必要工作的机制",
        ),
        "architecture/adr-0021-synem-closure-and-activation.html": (
            "GNU ld 文件命令",
            "GNU Guix 参考手册",
            "GNU make 条件指令",
            "W3C SHACL",
            "MCP 2025-11-25 工具规范",
            "正式绑定必须记录精确身份",
            "不能改变 Synem 闭包或直接授予权限",
        ),
    }
    for relative_path, required_tokens in external_boundary_contracts.items():
        boundary_text = (SOURCE_ROOT / relative_path).read_text()
        for token in required_tokens:
            if token not in boundary_text:
                errors.append(
                    f"{relative_path}: missing external technology boundary {token!r}"
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
        if "name-audit.md" not in design_index_text:
            errors.append("design routing index must route release-facing names to name-audit.md")

    name_audit = design_root / "name-audit.md"
    naming_standard = design_root / "language-and-naming.md"
    naming_adr = SOURCE_ROOT / "architecture" / "adr-0010-native-lexicon.html"
    if not name_audit.exists():
        errors.append("missing dated release-name conflict screening")
    else:
        name_audit_text = name_audit.read_text()
        if not re.search(r"证据时间：\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", name_audit_text):
            errors.append("name audit must record an ISO 8601 evidence time with timezone")
        for token in (
            "工程责任：首次发行负责人",
            "法律责任：目标法域的合格知识产权专业人员",
            "不是法律意见",
            "中等风险",
            "https://pypi.org/pypi/endem/json",
            "https://registry.npmjs.org/endem",
            "https://crates.io/api/v1/crates/endem",
            "https://api.github.com/search/repositories?q=endem+in%3Aname&per_page=100",
            "shivangx/Endem",
            "parmarjh/endem",
            "klu2200031072/endem",
            "github.com/endem",
            "IANA 媒体类型登记表",
            "正式商标门禁仍未完成",
            "必须停止或改名的条件",
            "Iknem",
            "Drasor",
            "drase",
            "旧名 Praxor",
            "旧名 Tekmor",
            "ADR-0031",
            "旧名 Poiet",
            "PFA Open Inference Engine",
            "Ktisor",
            "ktise",
            "ADR-0032",
            "TEXT-IDENTIFIER-CORE",
            "TXT-CORE",
            "TEXT-CORE",
            "TIB-CORE",
            "ADR-0033",
            "ADR-0034",
            "ADR-0035",
            "读音与口头区分证据",
            "BCP 47",
            "首次朗读",
            "听写回填",
            "成对混淆",
            "https://www.w3.org/TR/pronunciation-lexicon/",
            "https://www.gnu.org/prep/standards/html_node/Names.html",
        ):
            if token not in name_audit_text:
                errors.append(f"name audit missing evidence or boundary: {token!r}")
    for naming_path in (naming_standard, naming_adr):
        if not naming_path.exists() or "name-audit.md" not in naming_path.read_text():
            errors.append(
                f"{naming_path.relative_to(SOURCE_ROOT)} must defer current conflict evidence to name-audit.md"
            )
    if naming_adr.exists():
        naming_adr_text = naming_adr.read_text()
        for token in (
            "用六项职责分开来源表达",
            "本决定确定六项语义职责",
            "词源只作记忆辅助",
            "ADR-0034",
        ):
            if token not in naming_adr_text:
                errors.append(f"ADR-0010 missing responsibility-first naming boundary: {token}")
        if "六个短词" in naming_adr_text:
            errors.append("ADR-0010 must not present short field names as the value of the decision")

    manual_config = SOURCE_ROOT / "_data/manuals.yml"
    manual_layout = SOURCE_ROOT / "_layouts/manual.html"
    docs_rail_include = SOURCE_ROOT / "_includes/docs-rail.html"
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
    if not docs_rail_include.exists():
        errors.append("missing _includes/docs-rail.html")
    else:
        docs_rail_text = docs_rail_include.read_text()
        for token in (
            'where: "manual_id", page.manual_id',
            'sort: "manual_order"',
            "data-docs-rail",
            "data-directory-group",
            'aria-current="page"',
        ):
            if token not in docs_rail_text:
                errors.append(f"server-rendered manual rail missing contract: {token}")

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

    site_script = SOURCE_ROOT / "assets/site.mjs"
    module_root = SOURCE_ROOT / "assets/modules"
    if site_script.exists() and module_root.exists():
        module_text = "\n".join(path.read_text() for path in sorted(module_root.glob("*.mjs")))
        site_text = site_script.read_text()
        navigation_text = navigation_config.read_text() if navigation_config.exists() else ""
        global_navigation_text = navigation_text.split("\nmodules:", 1)[0]
        global_navigation_labels = re.findall(
            r"^    label:\s*(.+?)\s*$", global_navigation_text, re.MULTILINE
        )
        if global_navigation_labels != ["项目", "规范", "应用", "指南", "开发"]:
            errors.append(
                "global navigation must use project task labels and keep Endem inside the application group"
            )
        for phrase in PUBLIC_META_PHRASES:
            if phrase in navigation_text:
                errors.append(
                    f"navigation data exposes internal production phrase {phrase!r} in visible copy"
                )
        for token in (
            "directoryFromDocsRail",
            'trigger.setAttribute("aria-expanded", "false")',
            'item.addEventListener("mouseenter"',
            'item.classList.toggle("is-menu-open", expanded)',
            "setTimeout(() => this.#setExpanded(item, true), 40)",
            "setTimeout(() => this.#setExpanded(item, false), 120)",
            'document.addEventListener("click"',
            'event.key === "Escape"',
            "window.noemionMobileDirectoryScroll",
            "scrollLock?.lock()",
            "scrollLock?.unlock()",
            "open() {",
            'matchMedia("(max-width: 999px)")',
            "NavigationStore",
            "DirectoryNavigation",
            "MobileDirectoryController",
        ):
            if token not in module_text:
                errors.append(f"front-end modules missing interaction contract: {token}")
        for token in (
            "setTimeout(() => this.#finishClose(), 180)",
            'classList.add("is-closing")',
            'if (this.panel.classList.contains("is-closing")) return this.open()',
            'querySelector("[data-directory-backdrop]")',
            'this.backdrop?.addEventListener("click", () => this.close())',
        ):
            if token not in module_text:
                errors.append(f"mobile directory must synchronize its interruptible 180ms animation: {token}")
        for token in (
            'const mobileLayout = matchMedia("(max-width: 999px)")',
            'const desktopLayout = matchMedia("(min-width: 1000px)")',
            'const precisePointer = matchMedia("(hover: hover) and (pointer: fine)")',
            'if (event.key === "Tab") keyboardNavigation = true',
            "keyboardNavigation = false",
            "if (mobileLayout.matches) ensureDirectory()",
            'mobileLayout.addEventListener("change"',
            "if (event.matches) ensureDirectory()",
            "if (!globalRoot || !desktopLayout.matches) return",
            "if (precisePointer.matches) requestGlobalNavigation(event)",
            "if (precisePointer.matches || keyboardNavigation) requestGlobalNavigation(event)",
            'if (!desktopLayout.matches || precisePointer.matches) return',
            'event.target.closest?.(".global-nav-trigger")',
            'item.classList.contains("is-menu-open")',
            "event.preventDefault()",
            'const coverUrl = new URL("nav-covers.svg", scriptUrl).href',
        ):
            if token not in site_text:
                errors.append(f"site entry missing device-specific navigation contract: {token}")
        layout_text = layout.read_text() if layout.exists() else ""
        for eager_resource in ('rel="modulepreload"', 'rel="preload" href="{{ \'/assets/navigation-data.json\''):
            if eager_resource in layout_text:
                errors.append(f"default layout must not eagerly load both navigation modes: {eager_resource}")
        if re.search(r"^ensureDirectory\(\);$", site_text, re.MULTILINE):
            errors.append("site entry must not build the mobile directory unconditionally")
        for token in (
            "@media(hover:none) and (pointer:coarse)",
            ".endem-object-visual,.object-orbit-two,.portal-reveal{animation:none!important}",
        ):
            if token not in style.read_text():
                errors.append(f"touch devices missing static portal animation contract: {token}")
        for deferred_trigger in (
            'addEventListener("pointerdown", ensureDirectory',
            'addEventListener("keydown", ensureDirectory',
        ):
            if deferred_trigger in site_text:
                errors.append(f"site entry must not defer mobile directory loading: {deferred_trigger}")
        for forbidden in (
            "this.lockedScrollY",
            "scrollTo(0, this.lockedScrollY)",
            "this.previousScrollY",
            'window.addEventListener("scroll"',
            'document.addEventListener("touchmove"',
            'document.addEventListener("wheel"',
        ):
            if forbidden in module_text:
                errors.append(f"front-end modules retain viewport-shifting mobile menu lock: {forbidden}")
        for token in (
            'import(moduleUrl("global-navigation"))',
            'import(moduleUrl("directory-navigation"))',
            'import(moduleUrl("content-enhancements"))',
            "needsTableScroller || longContent",
            'directoryPanel.dataset.mobileDirectoryReady = "true"',
            'directoryPanel?.addEventListener("noemion:directoryrequest", ensureDirectory)',
            'if (pendingOpen) mobile.open()',
            'window.noemionMobileDirectoryScroll?.unlock()',
        ):
            if token not in site_text:
                errors.append(f"site entry missing progressive loading contract: {token}")
        if re.search(r'^import\s+.+?from\s+["\']\./modules/', site_text, re.MULTILINE):
            errors.append("site entry must propagate its build version to route-model imports")
        for module_name in ("global-navigation.mjs", "directory-navigation.mjs"):
            dependency_text = (module_root / module_name).read_text()
            if "new URL(import.meta.url).search" not in dependency_text or "dom-factory.mjs${version}" not in dependency_text:
                errors.append(f"{module_name} must propagate its build version to shared dependencies")
        if "portal-nav-link" in module_text:
            errors.append("global navigation must not emit the obsolete portal-nav-link alias")

        expected_nav_covers = {
            "background", "architecture", "foundations", "faq",
            "endem-spec", "synem", "dromen", "iknem",
            "endem", "theor", "format", "drase",
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
        configured_cover_entries = re.findall(r'\bcover:\s*([^,}\s]+)', navigation_text)
        configured_covers = set(configured_cover_entries)
        if len(configured_cover_entries) != 22 or configured_covers != expected_nav_covers:
            errors.append("global navigation entries must route to unique project covers")

    timeline_config = SOURCE_ROOT / "_data/project_timeline.yml"
    site_header_config = SOURCE_ROOT / "_data/site_header.yml"
    timeline_include = SOURCE_ROOT / "_includes/project-timeline.html"
    if not site_header_config.exists():
        errors.append("missing _data/site_header.yml")
    else:
        site_header_text = site_header_config.read_text()
        for token in (
            "timeline:",
            "label: TIMELINE",
            "href: /development/current-stage.html",
            "aria_label: 查看 Noemion 项目时间线",
            "title: 查看项目进度时间线",
        ):
            if token not in site_header_text:
                errors.append(f"site header timeline configuration missing: {token}")
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
        if re.search(r"^header:\s*$", timeline_text, re.MULTILINE):
            errors.append("project timeline must not expose a global header stage interface")
        for overview_key in (
            "completed_label", "active_label", "planned_label",
            "current_label", "roadmap_label", "roadmap_href",
        ):
            if not re.search(rf"^  {overview_key}:\s*.+$", timeline_text, re.MULTILINE):
                errors.append(f"project timeline overview requires {overview_key}")
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
            'src="../assets/images/secure-endem-ktisor.svg"',
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
            "组件代码开发尚未开启",
        ):
            if forbidden in current_stage_text:
                errors.append(f"current stage page exposes internal workflow copy: {forbidden}")
    for phrase in PUBLIC_META_PHRASES:
        if phrase in timeline_text:
            errors.append(
                f"project timeline exposes internal production phrase {phrase!r} in visible copy"
            )

    image_contracts = {
        "assets/images/secure-endem-ktisor.svg": (20_000, 'src="../assets/images/secure-endem-ktisor.svg"'),
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
    else:
        endem_text = endem_source.read_text()
        if endem_text.count('class="tool-project-body"') != 1:
            errors.append("Endem application page must define one bounded sticky body")
        elif re.search(
            r'class="tool-project-body">\s*<section\b.*?'
            r'<section class="tool-status-panel"',
            endem_text,
            re.DOTALL,
        ) is None:
            errors.append(
                "Endem application sections must participate directly in the responsive grid"
            )
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
    keyword_collisions = sorted(CURRENT_DOMAIN_IDENTIFIERS & MAINSTREAM_LANGUAGE_KEYWORDS)
    if keyword_collisions:
        errors.append(f"current domain identifiers collide with mainstream language keywords: {keyword_collisions}")
    numbered_domain_identifiers = sorted(
        identifier for identifier in CURRENT_DOMAIN_IDENTIFIERS
        if any(character.isdigit() for character in identifier)
    )
    if numbered_domain_identifiers:
        errors.append(
            "coined domain identifiers must not contain digits: "
            + ", ".join(numbered_domain_identifiers)
        )
    naming_standard_text = (SOURCE_ROOT / "design-system" / "language-and-naming.md").read_text()
    for token in (
        "## 无数字词汇原则",
        "不得添加数字后缀表示“新版”",
        "数字只在它确实承担精确引用时保留",
        "为什么纯文字名称不足",
        "## 读音与口头区分门禁",
        "BCP 47",
        "首次看到拼写的朗读结果",
        "成对混淆矩阵",
        "语音合成、自动转写和语音模型",
        "共享文字频道粘贴精确标识或逐字母确认",
    ):
        if token not in naming_standard_text:
            errors.append(f"language and naming standard missing no-digit boundary: {token}")
    release_name_adr_text = (
        SOURCE_ROOT / "architecture" / "adr-0031-release-name-collision-gate.html"
    ).read_text()
    if "短、可发音" in release_name_adr_text:
        errors.append(
            "ADR-0031 must not describe a name as pronounceable without ADR-0034 human evidence"
        )
    getting_started_text = (SOURCE_ROOT / "docs" / "getting-started.md").read_text()
    for token in (
        "具体发行拼写和读音仍需完成 ADR-0034 的人类验证",
        "不用临时读法冒充正式读法",
        "不会成为第二套命令、机器别名或语义权威",
        "先看一个 Agent 工作",
        "MCP 2025-11-25 Tasks",
        "A2A 1.0 规范",
        "外部 Task 显示 `completed`",
        "这个例子只解释职责顺序",
        "| 职责 | 现行字段 | 不得混入 |",
        "| 来源表达 | `rhem` | 授权后的意义投影 |",
        "| 待确认意义 | `apor` | 观察不足",
    ):
        if token not in getting_started_text:
            errors.append(f"getting started guide missing pronunciation status boundary: {token}")
    architecture_guide_text = (SOURCE_ROOT / "docs" / "architecture-guide.md").read_text()
    for token in (
        "用一次 Agent 工作读图",
        "MCP/A2A 状态保留外部来源",
        "`completed` 不直接映射为满足结果",
        "先形成 `met / unmet / agno / fault`",
        "Agent 系统边界图",
    ):
        if token not in architecture_guide_text:
            errors.append(f"architecture guide missing developer walkthrough: {token}")
    specifications_reference_text = (
        SOURCE_ROOT / "docs" / "specifications-reference.md"
    ).read_text()
    for token in (
        "不必先记住全部项目术语",
        "| 要回答的问题 | 先读 | 再核对 |",
        "`completed` 只说明外部请求执行状态",
        "研究资料不能作为现行字段、命令、状态或互操作接口的依据",
        "向量通过也只说明已登记案例与草案一致",
        "机器可读登记",
    ):
        if token not in specifications_reference_text:
            errors.append(f"specifications reference missing task lookup boundary: {token}")
    terminology_guide_text = (
        SOURCE_ROOT / "docs" / "terminology-and-pronunciation.md"
    ).read_text()
    for token in (
        "两个阶段不能使用同一批人",
        "同一参与者不能为同一名称重复贡献判断",
        "不证明所有人、口音、设备和环境下都不会出错",
        "不能进入人类样本数",
        "Noemion 尚未执行上述人类研究",
        "### 当前资料的阅读约定",
        "## 读音待定时怎样协作",
        "直白解释不是机器别名",
        "口述的近似声音不能选择命令",
        "原始转写不能直接改写 schema、命令、授权范围或研究结果",
    ):
        if token not in terminology_guide_text:
            errors.append(f"terminology guide missing human-evidence boundary: {token}")
    name_maturity_contracts = {
        "about/background.html": (
            "当前策略已确定 Endem 所指的最小制品职责",
            "现行拼写和读音仍须通过发行名称审查",
        ),
        "specifications/index.html": (
            "当前策略",
            "待定内容",
        ),
        "docs/installation-and-usage.md": (
            "Endem 只通过了有日期的精确工程名初筛",
            "术语与读音验证指南",
        ),
        "docs/specifications-reference.md": (
            "固定术语职责",
            "没有证明现行拼写或读音已经通过",
        ),
        "design-system/tool-project.md": (
            "只承担已接受的设计职责",
            "具体发行拼写和读音仍受 ADR-0034 约束",
        ),
    }
    for relative_path, required_tokens in name_maturity_contracts.items():
        contract_text = (SOURCE_ROOT / relative_path).read_text()
        for token in required_tokens:
            if token not in contract_text:
                errors.append(f"{relative_path} missing name-maturity boundary: {token}")
    for relative_path, forbidden in {
        "about/background.html": "已接受 Endem 词汇",
        "specifications/index.html": "名称、职责、六个语义面",
        "docs/installation-and-usage.md": "Endem 已通过互联网",
        "docs/specifications-reference.md": "固定现行词汇",
        "design-system/tool-project.md": "子命令名是已接受词汇",
    }.items():
        if forbidden in (SOURCE_ROOT / relative_path).read_text():
            errors.append(f"{relative_path} retains overclaimed name maturity: {forbidden}")
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

    stale_routes = sorted(REMOVED_PUBLIC_ROUTES & set(actual_routes))
    if stale_routes:
        errors.append(f"removed public routes must not survive as aliases or redirects: {stale_routes}")

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

    manual_ids = {"docs", *MANUAL_ROUTE_ORDERS}
    for manual_id in manual_ids:
        expected_manual_routes = [
            entry["route"] for entry in read_manual_source_entries(manual_id)
        ]
        for route in expected_manual_routes:
            manual_path = ROOT / route
            if not manual_path.exists():
                errors.append(f"missing rendered manual page {route}")
                continue
            rail_match = re.search(
                rf'<nav data-docs-rail data-manual-id="{re.escape(manual_id)}".*?</nav>',
                manual_path.read_text(),
                re.DOTALL,
            )
            if rail_match is None:
                errors.append(f"{route}: missing server-rendered manual rail")
                continue
            link_groups = re.findall(
                r'<div class="docs-rail-links">(.*?)</div>',
                rail_match.group(0),
                re.DOTALL,
            )
            rendered_routes = [
                urlsplit(href).path.lstrip("/")
                for group in link_groups
                for href in re.findall(r'<a href="([^"]+)"', group)
            ]
            if rendered_routes != expected_manual_routes:
                errors.append(
                    f"{route}: manual rail must contain its manual routes once in manual_order"
                )
            if rail_match.group(0).count("data-directory-group open") != len(link_groups):
                errors.append(f"{route}: every desktop manual group must start open")

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
            "Noemion", "Endem", "Synem", "Dromen", "Iknem", "rhem", "semion", "skena", "telis",
            "krin", "apor", "phain", "一个根", "模型", "不可信",
        ):
            if term not in visible_text:
                errors.append(f"index.html: homepage must explain {term}")
        home_source = home.read_text()
        if '<h1 id="portal-title"><span class="portal-title-brand">Noemion</span><strong><span>定义人工智能时代的</span><span>自然语言目标规范</span><span class="portal-title-foundation">奠定可验证智能的工程基石</span></strong></h1>' not in home_source:
            errors.append("index.html: rendered portal must identify Noemion before Endem")
        if home_source.count('class="portal-chapter-title"') != len(HOME_HEADINGS):
            errors.append("index.html: every homepage chapter heading must use the shared symbolic title treatment")
        for token in (
            "ENDEM / NASCENT",
            "dataflow-lane-rhem",
            "dataflow-lane-semion",
            "dataflow-lane-skena",
            "dataflow-lane-telis",
            "dataflow-lane-krin",
            "dataflow-lane-apor",
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
            "不得直接推出", "思想采用的验证要求", "六个语义面",
            "事态", "目标方向", "phain", "aseme", "agno", "fault",
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
        expected_introduction = (
            "portal-introduction"
            if row["kind"] == "portal"
            else "manual-introduction"
            if parser.docs_layout
            else "application-introduction"
            if row["kind"] in {"app", "tool"}
            else "section-introduction"
            if row["kind"] == "section"
            else "content-introduction"
        )
        introduction_counts = {
            name: parser.class_counts[name]
            for name in INTRODUCTION_CLASSES
            if parser.class_counts[name]
        }
        if introduction_counts != {expected_introduction: 1}:
            errors.append(
                f"{row['route']}: expected one {expected_introduction}, "
                f"got {introduction_counts}"
            )

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
        if "当前策略" not in visible_text:
            errors.append(f"{route}: normative page must explain the current strategy")
        if not any(
            marker in visible_text
            for marker in ("仍需", "仍待确定", "尚待确定", "待定内容", "正在研究", "开放问题")
        ):
            errors.append(f"{route}: normative page must explain pending content")

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
        site_header_source_text = (SOURCE_ROOT / "_data/site_header.yml").read_text()
        configured_timeline_label_match = re.search(
            r"^  label:\s*(.+?)\s*$", site_header_source_text, re.MULTILINE
        )
        configured_timeline_label = (
            configured_timeline_label_match.group(1)
            if configured_timeline_label_match is not None
            else ""
        )
        for token in (
            'data-timeline-id="noemion-project-progress"',
            'aria-label="查看 Noemion 项目时间线"',
            'href="/development/current-stage.html"',
            f'<strong class="global-timeline-value">{configured_timeline_label}</strong>',
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

    site_script = ROOT / "assets/site.mjs"
    route_module = ROOT / "assets/modules/route-model.mjs"
    directory_module = ROOT / "assets/modules/directory-navigation.mjs"
    navigation_data = ROOT / "assets/navigation-data.json"
    theme_script = ROOT / "assets/theme.js"
    directory_guard = ROOT / "assets/mobile-directory-guard.js"
    favicon = ROOT / "assets/favicon.svg"
    for path in (site_script, route_module, directory_module, navigation_data, directory_guard):
        if not path.exists():
            errors.append(f"missing built front-end asset {path.relative_to(ROOT)}")
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
        if text.count('data-global-nav-item=') != 5:
            errors.append(f"{rel}: server-rendered primary navigation must expose five task links")
        no_script_match = re.search(r"<noscript>(.*?)</noscript>", text, re.DOTALL)
        if no_script_match is None or "/sitemap.md" not in no_script_match.group(1):
            errors.append(f"{rel}: no-script navigation must expose the complete route registry")
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
        site_scripts = [
            script
            for script in parser.scripts
            if urlsplit(script).path.endswith("assets/site.mjs")
        ]
        if len(site_scripts) != 1:
            errors.append(f"{rel}: missing shared module entry")
        elif not urlsplit(site_scripts[0]).query:
            errors.append(f"{rel}: shared module entry must include a build cache key")
        guard_scripts = [
            script
            for script in parser.scripts
            if urlsplit(script).path.endswith("assets/mobile-directory-guard.js")
        ]
        if len(guard_scripts) != 1:
            errors.append(f"{rel}: missing mobile directory first-open guard")
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

    if navigation_data.exists() and route_module.exists() and directory_module.exists() and route_rows:
        try:
            navigation_payload = json.loads(navigation_data.read_text())
        except json.JSONDecodeError as error:
            errors.append(f"built navigation data is invalid JSON: {error}")
            navigation_payload = {}
        declared = {
            urlsplit(item.get("href", "")).path.lstrip("/")
            for module in navigation_payload.get("modules", {}).values()
            for group in module.get("groups", [])
            for item in group.get("items", [])
        }
        declared.update(
            urlsplit(group.get("href", "")).path.lstrip("/")
            for group in navigation_payload.get("global", [])
        )
        declared.update(
            urlsplit(item.get("href", "")).path.lstrip("/")
            for group in navigation_payload.get("global", [])
            for item in group.get("items", [])
        )
        declared.discard("")
        registered_set = set(registered)
        manual_routes = {
            route for route in registered
            if route.startswith("docs/") or route.startswith("endem/docs/")
        }
        if not declared <= registered_set:
            errors.append("built navigation data contains links outside the formal route registry")
        missing_static = sorted((registered_set - manual_routes) - declared)
        if missing_static:
            errors.append(f"built navigation data does not cover non-manual routes: {missing_static}")
        directory_source = directory_module.read_text()
        for token in ("DirectoryNavigation", "nav-section-toggle", 'toggleAttribute("inert"'):
            if token not in directory_source:
                errors.append(f"directory module missing contract: {token}")
        dom_factory_source = (ROOT / "assets/modules/dom-factory.mjs").read_text()
        global_navigation_source = (ROOT / "assets/modules/global-navigation.mjs").read_text()
        if 'createElementNS("http://www.w3.org/2000/svg"' not in dom_factory_source:
            errors.append("navigation covers must create nodes in the SVG namespace")
        if 'createSvgElement("svg"' not in global_navigation_source or 'createSvgElement("use"' not in global_navigation_source:
            errors.append("global navigation must render both SVG and use nodes through the SVG factory")
        if "routeModel.isCurrent(item.href)" not in directory_source:
            errors.append("directory current-page state must use exact URL matching")
        node = shutil.which("node")
        if node is None:
            errors.append("node is required to execute directory active-item behavior tests")
        else:
            active_cases = [
                ["endem/index.html", "https://site.test/endem/index.html", True],
                ["endem/index.html", "https://site.test/endem/", True],
                ["endem/index.html", "https://site.test/endem/docs/safety.html", False],
                ["docs/index.html", "https://site.test/docs", True],
                ["docs/index.html", "https://site.test/docs/getting-started.html", False],
                ["docs/index.html", "https://site.test/docs-old/guide.html", False],
            ]
            module_cases = [
                ["index.html", "project"],
                ["about/background.html", "project"],
                ["about/intellectual-foundations.html", "project"],
                ["architecture/endem-lifecycle.html", "architecture"],
                ["architecture/decisions.html", "architecture"],
                ["architecture/agent-system-boundaries.html", "architecture"],
                ["specifications/endem.html", "architecture"],
                ["components/ktisor.html", "architecture"],
                ["components/theor.html", "architecture"],
                ["components/drasor.html", "architecture"],
                ["docs/getting-started.html", "docs"],
                ["downloads/index.html", "resources"],
                ["faq/index.html", "resources"],
                ["development/testing.html", "development"],
                ["news/index.html", "development"],
                ["endem/index.html", "endem"],
                ["endem/docs/safety.html", "endem"],
            ]
            behavior_script = (
                "const api = await import(process.argv[1]);"
                "const { RouteModel, resolveDirectoryModule } = api;"
                "const cases = JSON.parse(process.argv[2]);"
                "const active = cases.map(([itemHref, current]) => "
                "new RouteModel('https://site.test/', current).isCurrent(itemHref));"
                "const moduleCases = JSON.parse(process.argv[3]);"
                "const modules = moduleCases.map(([route]) => resolveDirectoryModule(route));"
                "const baseModel = new RouteModel('https://site.test/project/', 'https://site.test/project/docs/a.html');"
                "const basePaths = [baseModel.absolute('/project/docs/index.html'),baseModel.absolute('/docs/index.html')];"
                "process.stdout.write(JSON.stringify({active, modules, basePaths}));"
            )
            completed = subprocess.run(
                [
                    node,
                    "--input-type=module",
                    "-e",
                    behavior_script,
                    route_module.as_uri(),
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
                expected_active = [case[2] for case in active_cases]
                expected_modules = [case[1] for case in module_cases]
                if actual["active"] != expected_active:
                    errors.append(
                        "directory exact-current behavior mismatch: "
                        f"expected {expected_active}, got {actual['active']}"
                    )
                if actual["modules"] != expected_modules:
                    errors.append(
                        "directory module routing mismatch: "
                        f"expected {expected_modules}, got {actual['modules']}"
                    )
                if actual["basePaths"] != [
                    "https://site.test/project/docs/index.html",
                    "https://site.test/project/docs/index.html",
                ]:
                    errors.append("route model must not duplicate a configured base path")

            scroll_cases = [
                [{"scrollTop": 0, "scrollHeight": 400, "clientHeight": 400}, 120, True],
                [{"scrollTop": 0, "scrollHeight": 400, "clientHeight": 400}, -120, True],
                [{"scrollTop": 0, "scrollHeight": 900, "clientHeight": 400}, -120, True],
                [{"scrollTop": 0, "scrollHeight": 900, "clientHeight": 400}, 120, False],
                [{"scrollTop": 250, "scrollHeight": 900, "clientHeight": 400}, -120, False],
                [{"scrollTop": 250, "scrollHeight": 900, "clientHeight": 400}, 120, False],
                [{"scrollTop": 500, "scrollHeight": 900, "clientHeight": 400}, 120, True],
                [{"scrollTop": 500, "scrollHeight": 900, "clientHeight": 400}, -120, False],
                [{"scrollTop": 250, "scrollHeight": 900, "clientHeight": 400}, 0, False],
            ]
            scroll_script = (
                "const { readFileSync } = await import('node:fs');"
                "const { runInNewContext } = await import('node:vm');"
                "const listeners = {};const windowListeners = {};"
                "const noop = () => {};"
                "const classes=new Set();const attrs=new Map();"
                "const root = {classList:{contains:(v)=>classes.has(v),add:(v)=>classes.add(v),remove:(v)=>classes.delete(v)},"
                "style:{scrollBehavior:'',setProperty:noop,removeProperty:noop},"
                "setAttribute:(k,v)=>attrs.set(k,v),getAttribute:(k)=>attrs.get(k),removeAttribute:(k)=>attrs.delete(k),scrollTop:0};"
                "const nav = {scrollTop:0,scrollHeight:900,clientHeight:400,contains:(target)=>target.inside};"
                "const panel = {open:true,querySelector:()=>nav};"
                "const document = {documentElement:root,body:{scrollTop:0},"
                "querySelector:(selector)=>selector==='.global-directory-panel[open]'?panel:null,"
                "addEventListener:(type,handler)=>{listeners[type]=handler;}};"
                "const window = {matchMedia:()=>({matches:true}),scrollX:0,scrollY:180,innerHeight:852,"
                "scrollTo:(x,y)=>{window.scrollX=x;window.scrollY=y;},"
                "addEventListener:(type,handler)=>{windowListeners[type]=handler;}};"
                "runInNewContext(readFileSync(process.argv[1],'utf8'),{window,document,CustomEvent:function(){}});"
                "const cases = JSON.parse(process.argv[2]);"
                "const api = window.noemionMobileDirectoryScroll;"
                "const boundaries = cases.map(([metrics,deltaY])=>api.shouldContainScrollGesture(metrics,deltaY));"
                "const move = (inside,y,touches=1)=>{let prevented=false;listeners.touchmove({target:{inside},"
                "touches:Array.from({length:touches},(_,i)=>({clientY:y+i})),preventDefault:()=>{prevented=true;}});return prevented;};"
                "const start = (inside,y,touches=1)=>listeners.touchstart({target:{inside},"
                "touches:Array.from({length:touches},(_,i)=>({clientY:y+i}))});"
                "nav.scrollTop=250;const untracked=move(true,100);const untrackedTop=nav.scrollTop;listeners.touchend();"
                "nav.scrollTop=250;start(true,100);const middle=move(true,80);const middleTop=nav.scrollTop;listeners.touchend();"
                "nav.scrollTop=0;start(true,100);const top=move(true,120);const topValue=nav.scrollTop;listeners.touchend();"
                "nav.scrollTop=500;start(true,100);const bottom=move(true,80);const bottomValue=nav.scrollTop;listeners.touchend();"
                "const outside=move(false,80);start(true,100,2);const pinch=move(true,80,2);"
                "const wheel=(inside,deltaY)=>{let prevented=false;listeners.wheel({target:{inside},deltaY,"
                "preventDefault:()=>{prevented=true;}});return prevented;};"
                "nav.scrollTop=250;const wheelInside=wheel(true,80);const wheelInsideTop=nav.scrollTop;"
                "const wheelOutside=wheel(false,80);const wheelOutsideTop=nav.scrollTop;"
                "const before=[window.scrollX,window.scrollY];api.lock();const locked=[window.scrollX,window.scrollY];"
                "api.unlock();const restored=[window.scrollX,window.scrollY];"
                "process.stdout.write(JSON.stringify({boundaries,touch:[untracked,middle,top,bottom,outside,pinch],"
                "positions:[untrackedTop,middleTop,topValue,bottomValue],"
                "wheel:[wheelInside,wheelOutside,wheelInsideTop,wheelOutsideTop],before,locked,restored}));"
            )
            scroll_completed = subprocess.run(
                [
                    node,
                    "--input-type=module",
                    "-e",
                    scroll_script,
                    directory_guard.as_posix(),
                    json.dumps(scroll_cases),
                ],
                capture_output=True,
                text=True,
            )
            if scroll_completed.returncode != 0:
                errors.append(
                    "mobile directory scroll-boundary behavior test could not execute: "
                    + scroll_completed.stderr.strip()
                )
            else:
                actual_scroll_results = json.loads(scroll_completed.stdout)
                expected_scroll_results = [case[2] for case in scroll_cases]
                if actual_scroll_results["boundaries"] != expected_scroll_results:
                    errors.append(
                        "mobile directory scroll-boundary behavior mismatch: "
                        f"expected {expected_scroll_results}, got {actual_scroll_results['boundaries']}"
                    )
                expected_touch_results = [True, True, True, True, True, False]
                if actual_scroll_results["touch"] != expected_touch_results:
                    errors.append(
                        "mobile directory touch containment mismatch: "
                        f"expected {expected_touch_results}, got {actual_scroll_results['touch']}"
                    )
                if actual_scroll_results["positions"] != [250, 270, 0, 500]:
                    errors.append(
                        "mobile directory manual scroll position mismatch: "
                        f"got {actual_scroll_results['positions']}"
                    )
                if actual_scroll_results["wheel"] != [True, True, 330, 330]:
                    errors.append(
                        "mobile directory wheel containment mismatch: "
                        f"got {actual_scroll_results['wheel']}"
                    )
                if actual_scroll_results["before"] != [0, 180]:
                    errors.append("mobile directory behavior harness must start at the expected page position")
                if actual_scroll_results["locked"] != [0, 180]:
                    errors.append("mobile directory must not reposition the page when its overlay opens")
                if actual_scroll_results["restored"] != [0, 180]:
                    errors.append("mobile directory must leave the page position unchanged when it closes")

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
        ".portal-feature-row:hover .portal-arrow i{transform:rotate(-45deg)}",
        ".portal-feature-row:focus-visible .portal-arrow i{transform:rotate(-45deg)}",
    ):
        if token not in style:
            errors.append(f"style.css missing animation contract: {token}")
    portal_arrow_markup = '<span class="portal-arrow" aria-hidden="true"><i>→</i></span>'
    if (ROOT / "index.html").read_text().count(portal_arrow_markup) != 4:
        errors.append("index.html must render four right-pointing portal arrows before interaction")
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
