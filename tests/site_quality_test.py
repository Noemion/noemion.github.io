from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
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
SPEC_MARKDOWN_FILES = sorted(SOURCE_ROOT.glob("spec/*.md"))
ARCHITECTURE_MARKDOWN_FILES = sorted(SOURCE_ROOT.glob("architecture/*.md"))
CONTENT_MARKDOWN_FILES = sorted([
    *SOURCE_ROOT.glob("about/*.md"),
    *SOURCE_ROOT.glob("components/*.md"),
    *SOURCE_ROOT.glob("development/*.md"),
    *SOURCE_ROOT.glob("specifications/*.md"),
])
PAGE_DIRECTORY_MARKDOWN_FILES = sorted(SOURCE_ROOT.glob("pages/*.md"))
SOURCE_PAGE_FILES = sorted([
    *SOURCE_HTML_FILES,
    *MANUAL_MARKDOWN_FILES,
    *SPEC_MARKDOWN_FILES,
    *ARCHITECTURE_MARKDOWN_FILES,
    *CONTENT_MARKDOWN_FILES,
    *PAGE_DIRECTORY_MARKDOWN_FILES,
])
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
    "pages/index.html",
]
APPLICATION_ROUTES = ["endem/index.html"]
ALLOWED_HANDWRITTEN_HTML_ROUTES = {
    "index.html",
    "about/index.html",
    "architecture/index.html",
    "architecture/decisions.html",
    "components/index.html",
    "development/index.html",
    "development/current-stage.html",
    "downloads/index.html",
    "endem/index.html",
    "faq/index.html",
    "specifications/index.html",
}
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
    "specifications/endem-closure.html",
    "specifications/session-contract.html",
    "specifications/evidence-entry.html",
    "specifications/diagnostics.html",
    "specifications/adapters.html",
    "specifications/identity.html",
    "specifications/text-and-identifiers.html",
    "specifications/authority.html",
    "architecture/endem-lifecycle.html",
    "architecture/adr-0010-native-lexicon.html",
    "architecture/adr-0011-endem-container.html",
    "architecture/adr-0013-source-profile.html",
    "architecture/adr-0014-source-manifest.html",
    "architecture/adr-0015-result-domains.html",
    "architecture/adr-0016-time-evidence.html",
    "architecture/adr-0017-negation-and-absence.html",
    "architecture/adr-0018-quantification-and-membership.html",
    "architecture/adr-0019-measurement-and-thresholds.html",
    "architecture/adr-0020-composite-situations-and-criteria.html",
    "architecture/adr-0021-closure-and-activation.html",
    "architecture/adr-0022-evidence-and-appraisal.html",
    "architecture/adr-0023-endem-content-standard.html",
    "architecture/adr-0024-session-contract.html",
    "architecture/adr-0025-structured-diagnostics.html",
    "architecture/adr-0026-external-protocol-adapters.html",
    "architecture/adr-0027-exact-identity-and-attestation.html",
    "architecture/adr-0028-text-and-identifier-boundaries.html",
    "architecture/adr-0029-authority-and-authorization-decisions.html",
    "architecture/adr-0030-endem-content-and-authorization-companions.html",
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html",
    "architecture/adr-0036-source-bearing-and-stripped-release.html",
    "components/producer.html",
    "components/inspector.html",
    "components/runner.html",
}
DOC_GUIDE_ORDER = [
    "docs/getting-started.html",
    "docs/architecture-guide.html",
]
DOC_GUIDE_HEADINGS = {
    "docs/getting-started.html": [
        "先把一句要求写完整", "沿一条责任链工作", "“安全使用”必须逐层检查", "相邻系统继续负责什么", "按问题继续学习", "当前可以验证什么",
    ],
    "docs/architecture-guide.html": [
        "先用一张责任图定位问题", "用一次 Agent 工作读图", "看到终态后按主张强度继续核对", "委托或恢复时重新建立边界", "三个实现域不能合并", "按问题进入进阶资料", "当前可以证明什么",
    ],
}
HOME_HEADINGS = [
    "人工智能系统开始行动，人的目标仍困在对话里",
    "把目标拆成六类可检查的信息",
    "四类对象各自回答一个问题",
    "一组动作名称三项安全责任仍须分开",
    "当前先完成规范和安全边界",
    "借鉴成熟工具让结果可以复核",
    "继续阅读",
]
ABOUT_INDEX_HEADINGS = [
    "先看一个真实任务",
    "Noemion 研究的不是自然语言生成代码",
    "为什么目标要成为独立对象",
    "相邻系统继续负责什么",
    "当前做到哪里",
]
ARCHITECTURE_INDEX_HEADINGS = [
    "从一次依赖升级定位架构",
    "看到成功后继续检查",
    "三个信任域为什么不能合并",
    "对象只在需要的阶段出现",
    "当前可以证明什么",
    "按问题继续",
]
DEVELOPMENT_INDEX_HEADINGS = [
    "当前先完成可以被独立核对的设计",
    "按问题继续阅读",
]
INTELLECTUAL_FOUNDATIONS_HEADINGS = [
    "从一次依赖升级看清问题",
    "把思想转换成可验证问题",
    "按开发者问题查思想来源",
    "《逻辑哲学论》的有限采用",
    "名字、规范与证据各自承担什么",
]
ADR_0011_READING_HEADINGS = [
    "先分清格式能够证明什么",
    "开发者应按什么顺序读取",
    "END-P2 与发布版分别做什么",
    "为什么采用固定目录与受限 CBOR",
    "权威机制怎样限定本决定",
    "当前限制与开发入口",
]
ADR_0011_READING_BOUNDARIES = (
    "不能证明目标已经满足、制品已经获准运行或最终发布",
    "用一个 valid=true 合并这些层次",
    "容器层可以完成字节检查，但 END-P2 必须因必需字段缺失而拒绝",
    "读取器不能把空载荷补成默认目标",
    "最终发布不能只删除 source_expression.content",
    "当前规范与已执行向量不是 producer、inspector 或正式独立读取组件",
    "well-formed、valid 和 application-expected",
    "删除一个记录或字段就能得到安全、闭合、可发布的 Endem",
    "当前不能生成",
)
ADR_0013_PROFILE_HEADINGS = [
    "先确定 END-P2 是什么",
    "开发者应按什么顺序检查",
    "六个记录分别回答什么",
    "封闭 schema 怎样失败",
    "外部标准只约束哪些机制",
    "当前不能发布或实现什么",
]
ADR_0013_PROFILE_BOUNDARIES = (
    "来源保留的形成与评审 Profile",
    "单文件最高只能声称 Profile 接受",
    "publishable=false",
    "相同字节",
    "投影选择器仍是不可信标识",
    "空记录也必须显式编码",
    "完整登记有效性、首选值替换和规范化算法仍未固定",
    "最终发布版必须使用新的封闭 Profile",
)
ADR_0014_SOURCE_HEADINGS = [
    "先判断来源清单能够证明什么",
    "一项输入怎样进入 END-P2",
    "十种指令为什么保持封闭",
    "语义确认与动作授权怎样分开",
    "确定性、来源保真和失败怎样验证",
    "何时删除这一实验入口",
]
ADR_0014_SOURCE_BOUNDARIES = (
    "它把解码后的自然语言和已确认结构放进封闭映射",
    "范围有限的语义授权绑定",
    "禁止模型直接生成规范对象",
    "不是 Endem 身份、正式源语言或已经通过读音验证的发行名称",
    "语义确认扩张为一般动作授权",
    "不得声称保存原始来源字节",
    "不保留别名、兼容解析或自动迁移",
    "没有 producer 解析器、实现仓库、稳定命令",
)
ADR_0015_RESULT_HEADINGS = [
    "用一次依赖升级看五类结果",
    "五个结果域分别由谁产生",
    "满足结果为什么必须是四值",
    "最终决定怎样消费而不改写满足结果",
    "外部机制只能提供哪一层事实",
    "当前仍缺哪些可执行接口",
]
ADR_0015_RESULT_BOUNDARIES = (
    "它们可以同时成立，也可以各自失败",
    "completed 不等于 met 或 accepted",
    "单份 valid 不等于整体 sufficient",
    "不再设置完整人类读音门槛",
    "外部签名陈述、验证政策、截止点、撤销状态和依赖方判断必须分别记录",
    "新观察或规则只能产生新结果",
    "不得回写或覆盖输入事实",
    "协议版本或外部状态变化只要求适配器重新记录映射",
    "没有 runner、决定引擎、结果事件编码或组件测试",
)
ADR_0016_TIME_HEADINGS = [
    "用一次部署检查读懂持续目标",
    "先决定固定时刻还是经过时长",
    "再声明连续性与违约预算",
    "证据覆盖怎样产生四类结果",
    "外部时钟与 Agent 状态只提供什么",
    "当前还不能编码或运行什么",
]
ADR_0016_TIME_BOUNDARIES = (
    "不是一个定时器参数",
    "reach / maintain 已作为直白、可恢复职责的普通英语枚举采用",
    "不再设置完整人类读音门槛",
    "单调时钟只能测量同一声明域内的经过时间",
    "所有目标范围统一采用项目定义的半开区间 [start, end)",
    "“采样”只说明证据怎样取得，不是第三种连续性政策",
    "其聚合区间端点规则不同，Gauge 只表示采样值",
    "远端时间戳和 completed 都不是本地时钟权威",
    "本决定不增加 END-P2 字段",
    "没有计时器、监控器或求值组件",
)
ADR_0017_NEGATION_HEADINGS = [
    "用一次越权检查区分四种情况",
    "否定仍保留同一关系与角色",
    "无匹配为什么默认是未知",
    "缺席证据必须先封闭什么",
    "外部查询与日志机制只证明什么",
    "当前还不能实现哪些缺席判断",
]
ADR_0017_NEGATION_BOUNDARIES = (
    "审计日志里没有匹配行，只能说明当前查询没有找到记录",
    "不能自动证明没有实际读取事件",
    "关系成立与不成立都谈论同一组对象",
    "更多空查询不能抵消反例",
    "外部 Agent、MCP 工具、检索器或模型的“未发现”只是一项带来源的运行声明",
    "封闭的是一项有限观察任务，不是现实世界",
    "1 表示无选中行，2 表示错误",
    "工具成功、空结果或模型总结不产生负事实、完整性或动作授权",
    "本决定不增加 END-P2 字段",
    "没有日志收集器、策略引擎或求值器",
)
ADR_0018_QUANTIFICATION_HEADINGS = [
    "用一次发布检查读懂量化",
    "成员集合必须先回答六个问题",
    "五种量词怎样提前或延后决定",
    "不完整、重复与空集合怎样失败",
    "外部查询和 Agent 列表只提供什么",
    "当前还不能编码或执行什么",
]
ADR_0018_QUANTIFICATION_BOUNDARIES = (
    "一个量化目标不是“对监控查询结果做计数”",
    "开发者先知道哪些节点属于“本次发布”",
    "enumerated / rule-bound 是现行草案的机器标签，不是新的哲学专名",
    "只有新增自造名称才需要完整读音与口头区分验证",
    "提前决定只减少不必要的求值，不降低证据要求",
    "不得静默去重后把错误输入伪装成合法集合",
    "证据数量不是成员数量",
    "翻完分页只得到外部接收方可见列表",
    "本决定不增加 END-P2 字段",
    "不表示 producer、runner、求值器或 CLI 已经实现",
)
ADR_0019_MEASUREMENT_HEADINGS = [
    "用一次延迟检查读懂测量链",
    "先定义测量什么和适用于谁",
    "再固定程序、单位与聚合器",
    "阈值必须连同不确定区间比较",
    "AI 基准和遥测工具只提供什么",
    "当前还不能编码或执行什么",
]
ADR_0019_MEASUREMENT_BOUNDARIES = (
    "不是一条仪表盘查询",
    "测量谓词必须同时固定构念、适用总体、可观察标准、预期用途和具名权威",
    "population=fixed_population 或 time_scope=utc_window",
    "目标统计量（estimand）",
    "不把难读的英文单独作为人类界面标签",
    "测量记录是关于事态的证据，不是事态本身",
    "不会自动产生最终接受或动作授权",
    "舍入只能发生在比较完成后的显示阶段",
    "295–305ms，不能决定位于哪一侧",
    "初始公开草案不是字段标准",
    "单点逆函数检查不保证换算全域正确",
    "不表示遥测采集器、基准运行器、统计引擎、runner 或求值器已经实现",
)
GENERIC_ENGLISH_BADGES = {
    "Motivation", "Scope", "Non-goals", "Why", "Evidence",
    "Content State", "External Statements", "Endem First", "One CLI",
    "Three Components", "Fail Closed", "Design Stage", "Specification",
    "Roadmap", "Testing", "Contribution", "Claim", "Failure", "Integrity",
    "Supply Chain", "Application Design", "Actions Specified", "Security",
    "Development", "No Release Yet",
    "Native Lexicon",
    "Experimental Input", "Replaceable", "Result Domains", "No Wire Change",
    "Negative Evidence", "No Wire Schema Change",
    "Quantified Goals", "Measurement Semantics", "Composite Criteria",
    "No Wire Format", "Layered Conformance", "Session Only", "Failure First",
    "Protocol Independent", "No Adapter Code", "Algorithm Agnostic",
    "No Crypto Code", "Unicode Boundaries", "No Unicode Code",
    "No Policy Engine", "END-CORE Clarification", "Identity Stable",
    "No New Artifact", "No new format", "No Voice Interface",
    "Five Actions",
    "Unreleased", "Endem CLI", "Integrity First", "5 Verbs",
    "Architecture", "Trust Boundaries", "Guides", "Endem Manual",
    "Reference", "Getting Started", "Claim First", "Spec First",
    "Evidence Boundaries", "Authority", "Lookup", "Status",
    "Naming Review", "Human Evidence", "Pronunciation Pending",
    "External Signing", "No Runtime", "Single CLI",
    "Experimental Core",
}
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
    "先确认当前可用性",
    "用一次依赖升级理解应用边界",
    "按工作选择设计入口",
    "一条任务怎样经过不同信任边界",
    "什么时候必须停止或交接",
    "外部先例只提供局部纪律",
    "继续阅读",
]
APPLICATION_STATUS_DISCLOSURES = (
    "当前不能安装或运行",
    "最终工具数量",
    "参数",
    "稳定 ABI",
    "必须确定",
)
APPLICATION_TASK_BOUNDARIES = (
    "不让模型选择一个最可能的解释",
    "其他对象等待物理格式",
    "不产生生产检查通过结论",
    "最终裁剪发布 Profile 尚未确定",
    "协议成功不能代替本地意义确认、动作授权、目标满足或最终决定",
    "Noemion 与 Endem 的完整读音和口头区分仍需独立人类证据",
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
    "桌面审查",
    "桌面资料审查",
    "结论状态",
    "门禁",
    "冻结",
    "尚未进入代码开发阶段",
    "尚未进入组件代码阶段",
    "组件代码开发尚未开启",
    "代码阶段开启后",
    "代码阶段开启时",
    "内部符合性门禁",
    "内部一致性门禁",
    "资料检查器",
    "Markdown 唯一正文源",
    "自动生成 HTML",
    "查看 Markdown 源",
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
PUBLIC_RESEARCH_PROCESS_PHRASES = (
    "等待用户决定",
    "等待用户接受",
    "用户接受本提案",
    "若用户接受",
    "在用户接受",
    "用户接受责任分配",
    "用户明确开启代码",
    "等待用户明确开启",
    "用户开启代码阶段",
    "用户没有明确开启",
    "若接受后的",
    "等待决定",
)
UNCLEAR_CHINESE_UI_TERMS = re.compile(
    r"架构决定|文档中心|文档首页|架构指南|工具参考(?!指南)|"
    r"规范登记(?:页)?|架构入口|使用与获取|新闻与进展|实施路线图|"
    r"路线图语境|黄金圈定位|第一批检查点|当前设计：|"
    r"尚待确定：|概要设计："
)
NORMATIVE_ROUTES = (
    "specifications/endem.html",
    "specifications/endem-closure.html",
    "specifications/session-contract.html",
    "specifications/evidence-entry.html",
    "specifications/diagnostics.html",
    "specifications/adapters.html",
    "specifications/identity.html",
    "specifications/text-and-identifiers.html",
    "specifications/authority.html",
)
CONTENT_LAYOUT_ROUTES = (
    "about/intellectual-foundations.html",
    "architecture/endem-lifecycle.html",
    "architecture/decisions.html",
    "architecture/agent-system-boundaries.html",
    "architecture/adr-0010-native-lexicon.html",
    "architecture/adr-0011-endem-container.html",
    "architecture/adr-0013-source-profile.html",
    "architecture/adr-0014-source-manifest.html",
    "architecture/adr-0015-result-domains.html",
    "architecture/adr-0016-time-evidence.html",
    "architecture/adr-0017-negation-and-absence.html",
    "architecture/adr-0018-quantification-and-membership.html",
    "architecture/adr-0019-measurement-and-thresholds.html",
    "architecture/adr-0020-composite-situations-and-criteria.html",
    "architecture/adr-0021-closure-and-activation.html",
    "architecture/adr-0022-evidence-and-appraisal.html",
    "architecture/adr-0023-endem-content-standard.html",
    "architecture/adr-0024-session-contract.html",
    "architecture/adr-0025-structured-diagnostics.html",
    "architecture/adr-0026-external-protocol-adapters.html",
    "architecture/adr-0027-exact-identity-and-attestation.html",
    "architecture/adr-0028-text-and-identifier-boundaries.html",
    "architecture/adr-0029-authority-and-authorization-decisions.html",
    "architecture/adr-0030-endem-content-and-authorization-companions.html",
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html",
    "architecture/adr-0036-source-bearing-and-stripped-release.html",
    "architecture/open-questions.html",
    "components/producer.html",
    "components/inspector.html",
    "components/runner.html",
    "development/implementation-roadmap.html",
    "specifications/endem.html",
    "specifications/endem-closure.html",
    "specifications/session-contract.html",
    "specifications/evidence-entry.html",
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
HERO_SECTION_CLASSES = {
    "portal-introduction",
    "section-introduction",
    "content-introduction",
    "application-introduction",
    "manual-introduction",
}

CURRENT_DOMAIN_IDENTIFIERS = {
    "endem", "source_expression", "meaning_projection", "situation", "goal_direction", "satisfaction_criteria", "unresolved_meaning", "structured_observation",
    "endem_closure", "session_contract", "evidence_entry", "producer", "inspect", "runner",
    "form", "lint", "compose", "inspect", "run",
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
REQUIRED_ARCHITECTURE_ROUTES = {
    "architecture/decisions.html": "architecture/index.html",
    "architecture/agent-system-boundaries.html": "architecture/index.html",
    "components/runner.html": "components/index.html",
}

SYSTEM_BOUNDARY_CONTRACTS = {
    "architecture/index.html": {
        "required": (
            "Endem",
            "closure",
            "evidence",
            "contract",
            "producer",
            "inspector",
            "runner",
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
            "先从一个变更定位责任",
            "开发者问题",
            "停止条件",
            "按职责核对全部决定",
            "status-columns",
            "现行 ADR 与对应 CORE、Profile",
            "Endem 语义、格式与判断",
            "组合、会话、证据与信任",
            "名称、读音与公开动作",
            "形成版与发布派生",
            "常见输入怎样进入当前架构",
            "外部资料怎样进入设计",
            "决定变化时要同步什么",
            "目标语言读音",
            "身份不等于权威",
            "外部状态不等于本地结果",
            "能力声明不等于实时句柄",
            "现有证据覆盖了哪些条件",
            "ADR-0015",
            "五类结果不可互换",
        ),
        "forbidden_patterns": (
            r"<h2>按编号核对决定状态</h2>",
            r"<th>状态</th><th>当前解释</th>",
            r"<h2>当前策略</h2>",
            r"<h2>排除的捷径</h2>",
            r"<span class=\"badge\">Design Stage</span>",
        ),
    },
    "architecture/agent-system-boundaries.html": {
        "required": (
            "非规范说明",
            "用一次依赖升级完成边界判断",
            "目标内容（Endem / closure）",
            "行动者与授权",
            "一次会话的上限",
            "外部调用与错误",
            "观察与证据（structured_observation / evidence）",
            "满足判断（satisfaction_criteria）",
            "最终决定（具名权威）",
            "六类问题由不同责任域回答",
            "目标只要求结果，还是还要求动作、转变或因果？",
            "先识别越级，再定位缺失事实",
            "外部生态改变输入，不改变责任",
            "GNU 先例只提供工程约束",
            "遇到更强问题时再进入研究",
            "完成一次边界评审",
            "工作负载身份",
            "运行实例",
            "外部成功不直接成为 <code>met</code>",
            "记忆与快照不恢复旧 contract",
            "尚未实现",
        ),
        "forbidden_patterns": (
            r"handoff.*自动.*(?:授权|权限)",
            r"Task.*completed.*(?:等于|成为).*met",
            r"检查点(?:能够|可以|会)恢复旧 contract",
            r"<h2>运行事实先按责任归类</h2>",
            r"<h2>先判断是哪一种越级</h2>",
            r"<h2>行业变化只改变外部机制</h2>",
            r"<h2>GNU 先例怎样约束工程判断</h2>",
            r"<h2[^>]*>研究问题按开发者问题路由</h2>",
        ),
    },
    "components/producer.html": {
        "required": (
            "producer",
            "为什么需要独立生产边界",
            "用一次依赖更新理解 producer",
            "三个生产动作各自交付什么",
            "发布、签名和证据为什么不能混入",
            "只生产 Endem / closure",
            "名称状态",
            "具有精确范围的语义授权",
            "不授予动作权限",
            "Endem",
            "确定性",
            "模型",
            "不可信",
            "checked arithmetic",
            "外部签名响应不是 producer 输入",
            "形成记录的 evidence 物理格式仍未定义",
            "closure 规范字节必须等待真实消费者与物理 Profile",
            "现有规范与向量只能证明已登记关系一致",
            "GNU <code>objcopy</code>",
            "SLSA 1.2 Provenance",
        ),
        "forbidden_patterns": (
            r"<td>发布配置</td>",
            r"<td>外部签名响应</td>",
            r"<h2>权威输入与生产者</h2>",
            r"<h2>输出与消费者</h2>",
            r"<h2>关键不变量</h2>",
            r"<h2>失败与拒绝责任</h2>",
        ),
    },
    "components/inspector.html": {
        "required": (
            "inspector",
            "为什么第二条读取路径仍然必要",
            "用一次依赖更新理解 inspector",
            "一次检查怎样保留主张范围",
            "独立、只读和有界分别约束什么",
            "分歧和失败后怎样继续",
            "当前可以证明什么",
            "名称状态",
            "inspect",
            "独立",
            "只读",
            "形成侧解析器",
            "不共享",
            "checked arithmetic",
            "当前只有 Endem 具有实验性物理字节规范",
            "不产生生产检查通过结论",
            "模型摘要不能进入规范视图",
            "GNU BFD 的信息损失说明",
            "NIST AI 600-1",
            "已登记关系一致",
        ),
        "forbidden_patterns": (
            r"<h2>为什么需要inspector</h2>",
            r"<h2>输入、输出与消费者</h2>",
            r"<h2>实现独立性</h2>",
            r"<h2>安全读取顺序</h2>",
            r"<h2>GNU 机制的采用边界</h2>",
            r"<h2>失败责任</h2>",
            r"<h2>当前状态与待确定接口</h2>",
        ),
    },
    "components/runner.html": {
        "required": (
            "runner",
            "用一次依赖更新理解 runner",
            "名称状态",
            "先把模型、控制面、适配器和决定者分开",
            "运行前形成一次只读会话契约",
            "一次能力请求怎样穿过边界",
            "会话结束后仍要守住两条边界",
            "实现前还要回答三个研究问题",
            "终态出现后不要立即归给本次动作",
            "会话开始前目标已经成立",
            "动作确实造成变化，但没有有效授权",
            "隔离必须证明什么",
            "外部 Agent 协议只提供带来源的事实",
            "contract",
            "run",
            "类型化能力请求",
            "evidence",
            "accepted",
            "deferred",
            "completed / failed / stopped",
            "决定权威",
            "不能给自己的记录",
            "具名权威再形成",
            "模型",
            "不可信",
            "失败位置",
        ),
        "forbidden_patterns": (
            r"maintain 的时钟与覆盖责任",
            r"负观察与封闭范围责任",
            r"量化聚合责任",
            r"测量判断责任",
            r"复合判断责任",
            r"closure 激活责任",
        ),
    },
    "specifications/endem.html": {
        "required": (
            ".endem",
            "用一个健康目标读懂 Endem",
            "普通职责词已接受",
            "先分清内容、Profile 与容器",
            "六项职责共同维持什么不变量",
            "先区分形成失败、待确认与判断失败",
            "五个结果域分别回答什么",
            "复杂目标从哪个问题进入",
            "安全读取与当前状态",
            "source_expression",
            "meaning_projection",
            "situation",
            "goal_direction",
            "satisfaction_criteria",
            "unresolved_meaning",
            "structured_observation",
            "no_allowed_projection",
            "undetermined",
            "fault",
            "logical_form",
            "checked arithmetic",
            "现行形成分类怎样阅读",
            "内容形成 + 外部关系",
            "形成版",
            "发布版",
            "受控伴随资料",
            "后态不能单独证明动作发生、状态转变或因果归属",
            "SCN-028–030",
        ),
        "forbidden_patterns": (
            r"<h2>状态机</h2>",
            r"三十个场景当前登记",
            r"END-P2 包含 3 个语义接受和 11 个预期拒绝",
        ),
    },
    "specifications/endem-closure.html": {
        "required": (
            "closure",
            "组合闭包（设计阶段名称 closure）",
            "先判断它是不是两个目标",
            "按四步形成固定闭包",
            "成员结果与会话激活不能合并",
            "外部机制不能替代闭包",
            "规范来源与当前上限",
            "依赖制品 Endem",
            "服务健康 Endem",
            "名称状态",
            "局部命名空间",
            "导入",
            "导出",
            "必需依赖",
            "可选依赖",
            "CLOSURE-CLS-001",
            "CLOSURE-RES-001",
            "CLOSURE-GRF-001",
            "CLOSURE-AUT-001",
            "CLOSURE-STA-001",
            "CLOSURE-ACT-001",
            "active / inactive / unresolved / error",
            "尚无物理格式",
            "尚未实现",
            "草案允许与拒绝的组合案例",
            "复核日期：</strong>2026-07-16",
            "GNU make",
            "GNU Guix",
            "MCP 2025-11-25",
            "notifications&#47;tools&#47;list_changed",
            "A2A 1.0 Agent Card",
        ),
        "forbidden_patterns": (
            r"按强定义、弱定义",
            r"弱引用无定义",
            r"<h2>先给直白定义</h2>",
            r"<h2>用一次服务发布理解组合闭包</h2>",
            r"<h2>六条规范不变量</h2>",
            r"<h2>绑定怎样形成</h2>",
            r"<h2>条件激活回答另一个问题</h2>",
            r"<h2>规范源与证据边界</h2>",
            r"<h2>当前状态</h2>",
        ),
    },
    "specifications/evidence-entry.html": {
        "required": (
            "evidence",
            "有范围证据记录（设计阶段名称 evidence）",
            "先判断一项信息能支持什么",
            "按四步形成并评估一项记录",
            "固定对象与主张",
            "四个结果不能合并",
            "外部机制只提供有范围输入",
            "规范来源与当前上限",
            "名称状态",
            "structured_observation",
            "精确对象",
            "主张",
            "原始观察",
            "model-candidate",
            "完整性",
            "sufficient / insufficient",
            "最终决定",
            "EVIDENCE-SCP-001",
            "EVIDENCE-PRV-001",
            "EVIDENCE-OBS-001",
            "EVIDENCE-CLS-001",
            "EVIDENCE-INT-001",
            "EVIDENCE-VAL-001",
            "EVIDENCE-COV-001",
            "EVIDENCE-DEC-001",
            "EVIDENCE-PRI-001",
            "当前草案",
            "非规范场景",
            "仅检查资料一致性",
            "正在研究",
            "复核日期：</strong>2026-07-16",
            "Schema URL 也不等于稳定发布",
            "W3C PROV-DM",
            "RFC 9334 RATS",
            "SLSA 1.2",
            "GNU Guix",
        ),
        "forbidden_patterns": (
            r">draft</td>",
            r">non-normative</td>",
            r">vector-checker-only</td>",
            r">awaiting-decision</td>",
            r"规范化与有损变换",
            r"<h2>先用一次发布判断理解它</h2>",
            r"<h2>按九项责任建立一项记录</h2>",
            r"<h2>四个结果必须分别保存</h2>",
            r"<h2>外部输入只按原身份进入</h2>",
            r"<h2>相邻问题按需要继续展开</h2>",
            r"<h2>轨迹怎样支持动作、转变与因果主张</h2>",
            r"<h2>历史与检查点何时能支持证据</h2>",
            r"<h2>删除操作成功不等于清除证据充分</h2>",
            r"<h2>开发者按这条顺序处理证据</h2>",
            r"<h2>一项记录至少说明这些事实</h2>",
            r"<h2>记录种类和来源类别解决不同问题</h2>",
            r"<h2>模型、Agent 协议和遥测先保持原来的身份</h2>",
            r"<h2>开放标准和 GNU 工具说明了哪些边界</h2>",
            r"<h2>规范条款与研究资料</h2>",
        ),
    },
    "specifications/session-contract.html": {
        "required": (
            "contract",
            "一次会话的只读执行契约（设计阶段名称 contract）",
            "按五步建立本次边界",
            "名称状态",
            "只读执行契约",
            "SESSION-CORE 0.1.0-draft",
            "精确制品",
            "能力只能",
            "有限且带单位的预算",
            "不保存令牌",
            "实质漂移",
            "不能序列化",
        ),
        "forbidden_patterns": (
            r"<h2>先给直白定义</h2>",
            r"<h2>用同一次发布理解会话契约</h2>",
            r"<h2>它从哪里来又流向哪里</h2>",
            r"<h2>一次会话必须固定什么</h2>",
            r"<h2>它保存什么又绝不保存什么</h2>",
            r"<h2>环境变化怎样处理</h2>",
            r"<h2>它与 Agent 协议的关系</h2>",
            r"<h2>权威规范和验证资料</h2>",
            r"<h2>当前状态</h2>",
        ),
    },
    "specifications/diagnostics.html": {
        "required": (
            "DIA-CORE 0.1.0-draft",
            "先看一次发布为什么停止",
            "adapter.retry.not_authorized",
            "operator-review",
            "不产生 <code>unmet</code>",
            "稳定机器码",
            "生产语境",
            "主阻断诊断",
            "不得授予权限",
            "不保存令牌",
            "有限预算",
            "部分可信对象",
            "不同输出怎样保留同一失败事实",
            "RFC 9457 Problem Details",
            "GNU GCC 诊断输出",
            "MCP 仍把",
            "A2A 1.0.0",
            "结构化诊断提案向量",
            "规范来源与当前上限",
        ),
        "forbidden_patterns": (
            r"<h2>先给直白定义</h2>",
            r"<h2>用同一次发布理解一次失败</h2>",
            r"<h2>一项完整诊断包含什么</h2>",
            r"<h2>为什么不能只返回一段错误文字</h2>",
            r"<h2>外部 Agent 错误怎样进入本地边界</h2>",
            r"<h2>诊断目录怎样组织</h2>",
            r"<h2>权威规范和验证资料</h2>",
            r"<h2>当前状态</h2>",
        ),
    },
    "specifications/adapters.html": {
        "required": (
            "ADP-CORE 0.1.0-draft",
            "先看一次发布怎样调用外部系统",
            "固定协议与对端",
            "本地调用身份",
            "信息损失",
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
            "协议状态不能越过本地判断",
            "按十二项责任检查一次调用",
            "遇到更强问题时再查外部资料",
            "规范来源与当前上限",
            "协议基线怎样选择",
            "MCP 2025-11-25",
            "MCP 2026-07-28 发布候选",
            "A2A 1.0 版本化规范",
            "GenAI Schema URL 1.42.0",
            "复核快照 93a59e4",
            "仓库提交、Schema URL 和各字段稳定性",
            "候选版只进入迁移研究",
            "旧 Task 句柄只帮助重新定位",
            "GNU BFD 信息损失说明",
            "当前没有具体协议 Profile",
        ),
        "forbidden_patterns": (
            r"<h2>它解决什么问题</h2>",
            r"<h2>用同一次发布理解一次外部调用</h2>",
            r"<h2>适配器必须保持哪些边界</h2>",
            r"<h2>符合性材料</h2>",
            r"<h2>协议基线怎样选择</h2>",
            r"<h2>断线后只恢复定位，不恢复权限</h2>",
            r"<h2>待定内容</h2>",
        ),
    },
    "specifications/identity.html": {
        "required": (
            "ID-CORE 0.1.0-draft",
            "先看一次发布怎样确认",
            "建立完整身份",
            "有类型签名陈述",
            "按十二项责任检查身份与签名",
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
            "形成版、裁剪发布版与验证材料怎样连接",
            "受控来源伴随资料",
            "没有伴随资料的验证者",
            "RFC 6920",
            "DSSE 1.0.2",
            "Sigstore Bundle 0.3.2",
            "SLSA 1.2 制品验证",
            "GNU <code>ld</code> build ID",
            "GNU Guix challenge",
            "精确身份提案向量",
            "规范来源与当前上限",
            "不是新制品",
            "待定内容",
        ),
        "forbidden_patterns": (
            r"<h2>它解决什么问题</h2>",
            r"<h2>用同一次发布理解精确身份</h2>",
            r"<h2>当前策略</h2>",
            r"<h2>身份、签名与派生必须怎样分开</h2>",
            r"<h2>符合性材料</h2>",
            r"<h2>待定内容</h2>",
        ),
    },
    "specifications/text-and-identifiers.html": {
        "required": (
            "TEXT-IDENTIFIER-CORE 0.1.0-draft",
            "先看一段文本怎样进入发布",
            "原始来源字节",
            "提交后的来源表达",
            "安全显示视图",
            "模型实际输入",
            "按十二项责任检查每个文本槽",
            "文本与标识符必须怎样处理",
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
            "遇到更强问题时再查对应资料",
            "ADR-0037",
            "Unicode 17.0",
            "GNU libunistring",
            "文本与标识符提案向量",
            "待定内容",
        ),
        "forbidden_patterns": (
            r"<h2>它解决什么问题</h2>",
            r"<h2>用同一次发布理解文本边界</h2>",
            r"<h2>先分清五类文本职责</h2>",
            r"<h2>当前怎样处理来源表达</h2>",
            r"<h2>为什么模型输入需要单独约束</h2>",
            r"<h2>符合性材料</h2>",
            r"<h2>待定内容</h2>",
        ),
    },
    "specifications/authority.html": {
        "required": (
            "AUT-CORE 0.1.0-draft",
            "用同一次发布理解一次授权决定",
            "发布请求者、具体 CI 运行实例",
            "部分授予形成缩小后的新范围",
            "授权允许一次声明范围内的行动",
            "遇到“已授权”先问对象是什么",
            "不能只保存一个 <code>authorized: true</code>",
            "谁可以确认这个意义候选",
            "候选进入确认的 <code>meaning_projection</code>",
            "谁可以尝试这个动作",
            "当前 run 会话的能力上限",
            "自然语言候选怎样获得意义确认",
            "它不授予调用工具、修改对象或部署服务的动作权限",
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
            "Agent 名称为什么不能代替实际行动者",
            "模型身份",
            "工作负载身份",
            "运行实例与调用身份",
            "把自然语言、Agent 与权限升级接到同一条边界",
            "形成请求",
            "处理多人关系",
            "使用决定",
            "解释结果",
            "外部机制能提供什么",
            "更强问题应当进入哪份研究",
            "当前状态与限制条件",
            "截至 2026-07-15",
            "software-agent-identity-and-accountability-boundaries-proposal.html",
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
    "architecture/adr-0035-public-actions-and-internal-responsibilities.html": {
        "required": (
            "用户任务不是内部职责清单",
            "五项公开职责",
            "form",
            "lint",
            "compose",
            "inspect",
            "run",
            "form / lint / compose / inspect / run",
            "GNU Command-Line Interfaces",
            "Git glossary：porcelain 与 plumbing",
            "MCP 2025-11-25 Tools",
            "A2A 1.0 版本化规范",
            "OpenAI Agents SDK Tools",
            "conformance:",
            "普通动作词已接受",
            "动作名称不等于实现优先级",
            "没有可执行 <code>endem</code>",
            "接口不提供多套名称或兼容入口",
        ),
    },
    "architecture/adr-0036-source-bearing-and-stripped-release.html": {
        "required": (
            "移除原文，就得到另一份制品",
            "形成版保留原始自然语言",
            "最终发布版移除原文",
            "source_ref",
            "GNU GDB：Separate Debug Files",
            "GNU strip",
            "GNU objcopy",
            "SLSA 1.2 Provenance",
            "NIST AI 600-1",
            "END-P2",
            "END-PUB-001",
            "新身份与新验证",
            "摘要猜测",
            "没有受控伴随资料",
            "删除、重写、保留和外置不是一回事",
            "裁剪只能移除一类输入和披露风险",
            "没有可执行的裁剪命令",
        ),
    },
    "endem/docs/safety.html": {
        "required": (
            "checked arithmetic",
            "inspect",
            "inspector",
            "形成侧解析器",
            "绑定精确字节",
            "不是 CLI 输出",
            "不能跨入 inspector",
            "不可信",
        ),
    },
    "endem/docs/running.html": {
        "required": (
            "contract",
            "外部签名",
            "私钥始终留在外部签名系统",
            "签名包络",
            "evidence",
            "structured_observation",
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
        if "manual-article" in ancestor_classes and tag == "table":
            self.class_counts["table-wrap"] += 1
        if "manual-article" in ancestor_classes and tag == "ol":
            self.class_counts["flow"] += 1
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
                "direct_main_child": bool(
                    ancestor_tags
                    and (
                        ancestor_tags[-1] == "main"
                        or "summary-rail-main" in self.stack[-1][1]
                    )
                ),
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


def content_visible_text(parser):
    if parser.manual_article_text:
        return normalize_visible_text("".join(parser.manual_article_text))
    return normalize_visible_text(
        " ".join("".join(section["text"]) for section in parser.sections)
    )


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
        elif route == "spec/index.html":
            kind = "content"
            parent = "specifications/index.html"
            sibling_orders[parent] += 1
            order = sibling_orders[parent]
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


def contains_source_token(text, token):
    normalized_text = re.sub(r"<code\b[^>]*>", "`", text)
    normalized_text = normalized_text.replace("</code>", "`")
    variants = {token, html.unescape(token)}
    for variant in tuple(variants):
        markdown = re.sub(r"<code>(.*?)</code>", r"`\1`", variant)
        markdown = markdown.replace("<strong>", "**").replace("</strong>", "**")
        variants.add(markdown)
    return any(variant in text or variant in normalized_text for variant in variants)


def validate_required_text_contracts(root):
    errors = []
    for route, contract in SYSTEM_BOUNDARY_CONTRACTS.items():
        path = source_path_for_route(route) if root == SOURCE_ROOT else root / route
        if not path.exists():
            errors.append(f"missing system-closure page {route}")
            continue
        text = path.read_text()
        for token in contract.get("required", ()):
            if not contains_source_token(text, token):
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
        if route == "architecture/decisions.html":
            linked_adrs = {
                int(value)
                for value in re.findall(r'href="adr-(\d{4})-[^"]+\.html"', text)
            }
            expected_adrs = {10, 11, *range(13, 31), 35, 36, 37}
            if linked_adrs != expected_adrs:
                missing = sorted(expected_adrs - linked_adrs)
                unexpected = sorted(linked_adrs - expected_adrs)
                errors.append(
                    "architecture/decisions.html: grouped decision index must link "
                    f"the retained ADR set exactly; missing={missing}, "
                    f"unexpected={unexpected}"
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
            'querySelectorAll(".table-wrap, pre")',
            'region.scrollWidth > region.clientWidth + 1',
            'region.tabIndex = 0',
            'region.setAttribute("role", "region")',
            'document.fonts?.ready.then(updateAll)',
            'window.addEventListener("resize", updateAll',
            'this.main.querySelector(":scope > .content-introduction")',
            'insertAdjacentElement("afterend", outline)',
            'label.textContent = "章节"',
        ):
            if token not in behavior_text:
                errors.append(
                    f"content enhancement module missing readability contract: {token}"
                )
        if ".manual-article .manual-table-wrap td code{overflow-wrap:normal;word-break:normal}" not in style.read_text():
            errors.append("manual table code identifiers can collapse into character-by-character wrapping")
        for token in (
            "href: /architecture/index.html",
            "href: /architecture/decisions.html",
            "label: 指南",
            "href: /docs/architecture-guide.html",
            "href: /endem/docs/reference.html",
            "href: /specifications/index.html",
            "href: /development/current-stage.html",
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
                r"\.docs-rail\s*\{[^}]*left:var\(--site-frame-left\)"
            ),
            "desktop documentation content must share the header canvas basis": (
                style_text,
                r"body\[data-docs-layout=\"true\"\]\s+main\s*\{[^}]*"
                r"calc\(var\(--site-frame-left\)\s*\+\s*var\(--docs-rail-width\)\)"
            ),
            "open mobile directory must align with the shared eight pixel canvas": (
                directory_text,
                r"html\.mobile-directory-open\s+\.global-directory-panel\s+nav\s*\{"
                r"[^}]*right:var\(--site-frame-edge\);[^}]*left:var\(--site-frame-edge\);width:auto"
            ),
            "docs content must become a centered single column from 1217px": (
                style_text,
                r"@media\(min-width:1000px\)\s+and\s+\(max-width:1217px\)\s*\{"
                r"[^}]*body\[data-docs-layout=\"true\"\]\s+main,"
                r"\s*body\[data-docs-layout=\"true\"\]\s+\.site-footer\s*\{"
                r"[^}]*width:min\(1000px,var\(--site-frame-width\)\)"
            ),
            "documentation rail must disappear at 1217px": (
                directory_text,
                r"@media\(max-width:1217px\)\s*\{\s*\.docs-rail\s*\{\s*display:none"
            ),
            "summary rail must become sticky only after a measured split": (
                style_text,
                r'\.summary-rail-layout\[data-summary-layout="split"\]>\.summary-rail\s*\{'
                r"[^}]*position:sticky;[^}]*top:var\(--summary-rail-top\)"
            ),
            "split summary rail must scroll only for real vertical overflow": (
                style_text,
                r'\.summary-rail-layout\[data-summary-layout="split"\]>\.summary-rail\s*\{'
                r"[^}]*max-height:calc\(100dvh\s*-\s*var\(--summary-rail-top\)\s*-\s*24px\);"
                r"[^}]*overflow-x:hidden;overflow-y:auto"
            ),
            "project progress decoration must remain inside its scroll boundary": (
                style_text,
                r"\.summary-rail--progress::before\s*\{[^}]*right:0;bottom:0;"
            ),
            "breadcrumbs must be compact while retaining a forty pixel link target": (
                style_text,
                r'body:not\(\[data-page-role="portal"\]\)\s+\.breadcrumbs\s*\{'
                r"[^}]*min-height:40px;[^}]*font-size:11px;[^}]*line-height:1\.35"
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
                r"[^}]*margin-right:auto;margin-left:0;"
                r"[^}]*font-size:17px;[^}]*line-height:1\.75"
            ),
            "manual reading columns must remain left anchored": (
                style_text,
                r"\.manual-article>:is\(h3,h4,p,ul,ol,blockquote\)\s*\{"
                r"[^}]*max-width:760px;[^}]*margin-right:auto;margin-left:0"
            ),
            "section reading columns must remain left anchored": (
                style_text,
                r'body\[data-page-role="section"\]:not\(\[data-page-role="portal"\]\)\s+'
                r'main>section>:is\(h2,p,ul,ol,blockquote\)\s*\{'
                r"[^}]*max-width:760px;[^}]*margin-right:auto;margin-left:0"
            ),
            "compact page padding must follow available width": (
                style_text,
                r"--site-content-inline:clamp\(14px,4vw,56px\)"
            ),
            "tool project must collapse before a tablet canvas clips its status panel": (
                style_text,
                r"@media\(max-width:1217px\)\s*\{"
                r"[^}]*body\[data-page-role=\"tool-project\"\]\s+\.tool-project-body"
                r"\s*\{\s*display:flex;flex-direction:column;align-items:stretch"
            ),
            "mobile manual navigation targets must be at least 44px square": (
                style_text,
                r"\.manual-nav\s+a\s*\{[^}]*min-width:44px;"
                r"[^}]*min-height:44px"
            ),
            "mobile footer and theme menu targets must be at least 44px tall": (
                style_text,
                r"@media\(max-width:999px\)\s*\{[^}]*"
                r"\.site-footer-grid\s+a,\.site-footer-links\s+a\s*\{"
                r"[^}]*min-width:44px;[^}]*min-height:44px\}[^}]*"
                r"\.site-theme-trigger\s*\{[^}]*min-height:44px\}[^}]*"
                r"\.site-theme-menu>button\s*\{[^}]*min-height:44px"
            ),
            "long inline code must wrap inside the reading column": (
                style_text,
                r"code\s*\{[^}]*overflow-wrap:anywhere"
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

        for pattern in current_prose_forbidden:
            if re.search(pattern, body):
                errors.append(f"{route}: current prose retains unexplained wording {pattern!r}")

        if path.suffix == ".html":
            prose_blocks = re.findall(
                r"<(?:p|li|td)\b[^>]*>(.*?)</(?:p|li|td)>",
                body,
                re.DOTALL | re.IGNORECASE,
            )
        else:
            prose_blocks = []
            in_fence = False
            for line in body.splitlines():
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence or not line.strip():
                    continue
                if line.lstrip().startswith("|"):
                    prose_blocks.extend(cell for cell in line.split("|") if cell.strip())
                else:
                    prose_blocks.append(
                        re.sub(r"^\s*(?:#{1,6}|>|[-*+] |\d+\. )\s*", "", line)
                    )
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

    foundations = source_path_for_route("about/intellectual-foundations.html").read_text()
    for token in (
        "2.01 与 2.1–2.172",
        "3.203–3.21",
        "4.024 与 4.062–4.064",
        "5.6 与 7",
        "贺绍甲译《逻辑哲学论》",
        "它们不是软件错误分类",
        "后期著作反过来批评早期分析框架",
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
    internal_work_package = re.search(r"\bP\d+-W\d+\b", text)
    if internal_work_package:
        errors.append(
            f"{route}: public HTML exposes internal work-package label {internal_work_package.group(0)!r}"
        )
    maintenance_patterns = {
        r"tests/[A-Za-z0-9_./-]+\.py": "internal test path",
        r"(?:资料一致性检查|资料检查|仓库内容检查|公开内容检查|具名规范维护者复核|测试输出|版本化验证结果)": "maintenance process",
        r"(?:规范提案向量检查器|规范向量检查器|一致性检查工具)": "repository checker",
        r"(?:治理边界|采用门槛|当前决定边界|关闭决定|决策门|正式 ADR|进入代码开发阶段|当前仍未进入代码开发阶段|proposal-vector checker only|for maintainers|current contribution scope|reporting routes|unfrozen)": "internal governance wording",
        r"(?:唯一公开 CLI|唯一公开命令|单一命令入口|只提供一个命令入口|只有三个组件|规划三个组件|统一 CLI)": "premature tool packaging claim",
        r"(?:开发与贡献|测试与验证)": "maintenance page wording",
    }
    for pattern, label in maintenance_patterns.items():
        match = re.search(pattern, text)
        if match:
            errors.append(
                f"{route}: public HTML exposes {label} {match.group(0)!r}"
            )
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


def source_path_for_route(route):
    direct = SOURCE_ROOT / route
    if direct.exists():
        return direct
    for source_path in SOURCE_PAGE_FILES:
        source_match = FRONT_MATTER.match(source_path.read_text())
        if source_match is None:
            continue
        permalink = front_matter_value(source_match.group(1), "permalink")
        if permalink and permalink.lstrip("/") == route:
            return source_path
    return direct


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
    for removed_maintenance_source in (
        SOURCE_ROOT / "development" / "testing.md",
        SOURCE_ROOT / "docs" / "development-guide.md",
    ):
        if removed_maintenance_source.exists():
            errors.append(
                "public maintenance page must remain removed: "
                + str(removed_maintenance_source.relative_to(SOURCE_ROOT))
            )
    readme_text = README.read_text()
    if len(readme_text.splitlines()) > 100:
        errors.append("README.md must remain a concise developer entry under 100 lines")
    for token in (
        "sitemap.md",
        "tests/site_quality_test.py",
    ):
        if token not in readme_text:
            errors.append(f"README.md missing essential developer entry: {token}")
    for token in ("## Jekyll 源码模型", "-proposal.md", "ADR-0010"):
        if token in readme_text:
            errors.append(f"README.md duplicates detailed maintenance material: {token}")
    public_research_files = [
        SOURCE_ROOT / "README.md",
        *sorted((SOURCE_ROOT / "spec").glob("*.md")),
    ]
    for path in public_research_files:
        text = path.read_text()
        for phrase in PUBLIC_RESEARCH_PROCESS_PHRASES:
            if phrase in text:
                errors.append(
                    f"{path.relative_to(SOURCE_ROOT)} exposes internal project process phrase {phrase!r}"
                )
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
            "python3 tests/p2_payload_test.py",
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

    contribution_contracts = {
        SOURCE_ROOT / ".github" / "ISSUE_TEMPLATE" / "01-documentation.yml": (
            "资料与网站问题",
            "事实或术语错误",
            "公开范围确认",
        ),
        SOURCE_ROOT / ".github" / "ISSUE_TEMPLATE" / "02-research.yml": (
            "研究与规范问题",
            "可证伪主张",
            "术语与读音",
            "研究提案不等于已实现能力或现行接口",
        ),
        SOURCE_ROOT / ".github" / "pull_request_template.md": (
            "案例、反例与失败责任",
            "验证与声明上限",
            "术语检查",
        ),
    }
    for path, required_tokens in contribution_contracts.items():
        if not path.exists():
            errors.append(f"missing contributor contract: {path.relative_to(SOURCE_ROOT)}")
            continue
        contract_text = path.read_text()
        for token in required_tokens:
            if token not in contract_text:
                errors.append(
                    f"{path.relative_to(SOURCE_ROOT)} missing contributor boundary: {token}"
                )
    issue_config = SOURCE_ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    if not issue_config.exists() or "blank_issues_enabled: false" not in issue_config.read_text():
        errors.append("structured issue forms must disable unscoped blank issues")

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
            "待定内容",
            "model-context-assembly-proposal.md",
        ):
            if token not in proposal_text and token not in (SOURCE_ROOT / "spec" / "README.md").read_text():
                errors.append(f"model context proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "model-context-assembly" in registry_text:
            errors.append("non-normative model context proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "architecture" / "open-questions.md",
        ):
            if "spec/model-context-assembly-proposal.html" not in public_source.read_text():
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
            "contract 是 segment 或 process image",
            "职责适用性矩阵",
            "Symbol versioning",
            "`objcopy` / `strip` / debug link",
            "带错继续和部分输出",
            "未来采用的证据要求",
            "不进入 `registry.json`",
            "进入规范前的条件",
        ):
            if token not in proposal_text:
                errors.append(f"GNU and ELF applicability proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "gnu-elf-applicability" in registry_text:
            errors.append("non-normative GNU and ELF proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
        ):
            if "gnu-elf-applicability-proposal.html" not in public_source.read_text():
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
            "进入规范前的条件",
        ):
            if token not in proposal_text:
                errors.append(f"planning proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "planning-and-replanning" in registry_text:
            errors.append("non-normative planning proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
        ):
            if "planning-and-replanning-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
        ):
            if token not in proposal_text:
                errors.append(f"semantic equivalence proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "semantic-equivalence-and-migration" in registry_text:
            errors.append("non-normative semantic equivalence proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
        ):
            if "semantic-equivalence-and-migration-proposal.html" not in public_source.read_text():
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
            "日期：2026-07-15",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "五类主张必须分开",
            "GNU Make",
            "W3C PROV-DM",
            "CloudEvents",
            "OpenTelemetry",
            "https://a2a-protocol.org/v1.0.0/specification/",
            "终态满足",
            "动作发生",
            "状态转变",
            "因果归因",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "当前策略：正在研究；尚未进入规范",
        ):
            if token not in proposal_text:
                errors.append(f"causation proposal missing governance boundary: {token}")
        if "a2a-protocol.org/latest/" in proposal_text:
            errors.append("causation proposal must use the versioned A2A specification URL")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "state-change-and-causal-attribution" in registry_text:
            errors.append("non-normative causation proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "endem.md",
            SOURCE_ROOT / "specifications" / "evidence-entry.md",
            SOURCE_ROOT / "components" / "runner.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
        ):
            if "state-change-and-causal-attribution-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the causation research proposal"
                )

    lifecycle_page_text = source_path_for_route("architecture/endem-lifecycle.html").read_text()
    if lifecycle_page_text:
        for token in (
            "四类对象各自有界",
            "先用一次发布看懂四类对象",
            "含来源形成版",
            "没有受控伴随资料时，不能证明它忠实对应原始表达",
            "开发者按七步处理",
            "后一步不能弥补前一步的失败",
            "裁剪不是删除一个字段",
            "发布 Profile 必须定义不泄露原文的来源绑定",
            "GNU GDB 的独立调试文件",
            "装载前重新决定能否执行",
            "END-CORE 的内容状态只保留 `formed / resolved`",
            "规范来源与当前上限",
            "RFC 9334 RATS",
            "in-toto Statement",
            "SLSA 1.2",
            "MCP 2025-11-25 Tasks",
            "截至 2026-07-16 仍为实验能力",
            "当前没有 producer、inspector、runner、裁剪发布器",
        ):
            if token not in lifecycle_page_text:
                errors.append(f"Endem lifecycle page missing two-axis attestation boundary: {token}")
        for stale_lifecycle_claim in (
            "Endem 在 formed、resolved、attested 三个状态之间演进",
            "<h2>resolved → attested</h2>",
            "<h2>attested → contract → evidence</h2>",
            "<tr><td>attested → run</td>",
            "这五个结果域由",
            "<h2>先分开内容状态与外部关系</h2>",
            "<h2>开发者应怎样读主流程</h2>",
            "<h2>阶段、消费者与失败</h2>",
            "<h2>formed → resolved</h2>",
            "<h2>内容形成与发布陈述不能压成一个状态</h2>",
            "<h2>外部陈述复核 → contract → evidence</h2>",
            "<h2>现行结果域与草案限制</h2>",
            "<h2>为什么采用两条轴</h2>",
            "<h2>未来实现顺序</h2>",
        ):
            if stale_lifecycle_claim in lifecycle_page_text:
                errors.append(
                    f"Endem lifecycle page retains a linear attestation overclaim: {stale_lifecycle_claim}"
                )
        lifecycle_explainer_requirements = {
            SOURCE_ROOT / "architecture" / "index.html": (
                "来源表达、已确认意义投影、一个根可能事态、目标方向、满足判据和待确认意义",
                "意义确认不授予工具或运行权限",
                "外部陈述绑定内容身份",
                "签名、验证或撤销不会原地改写内容身份",
            ),
            source_path_for_route("components/runner.html"): (
                "适用外部陈述",
                "验证政策、截止点、撤销",
                "不把这些关系压成内容自身的布尔状态",
            ),
            source_path_for_route("specifications/session-contract.html"): (
                "外部陈述与验证记录",
                "内容只使用 `formed / resolved` 状态",
                "内容形成与外部关系的两轴模型",
            ),
            SOURCE_ROOT / "endem" / "index.html": (
                "精确发布制品、适用外部陈述与验证记录",
                "内容形成、外部陈述、会话准入和最终决定怎样保持分离",
            ),
            SOURCE_ROOT / "endem" / "docs" / "running.md": (
                "绑定精确主体的外部陈述与验证记录",
                "任何一项都不能让内容获得永久可信状态",
            ),
            SOURCE_ROOT / "endem" / "docs" / "reference.md": (
                "外部陈述、验证政策、截止点、撤销状态与依赖方判断已移出内容状态",
                "不得实现内容内的签名通过布尔标志",
            ),
            SOURCE_ROOT / "endem" / "docs" / "safety.md": (
                "`formed / resolved` 内容形成责任",
                "外部陈述的主体摘要、类型、签名范围、验证政策与撤销材料",
            ),
            source_path_for_route("architecture/adr-0010-native-lexicon.html"): (
                "外部签名与证明不能成为内容自身状态",
            ),
            source_path_for_route("architecture/adr-0015-result-domains.html"): (
                "`formed / resolved` 只描述内容",
                "不能压成第三个内容状态",
            ),
            source_path_for_route("architecture/adr-0024-session-contract.html"): (
                "只接受精确的 `resolved` Endem 或 closure",
                "内容状态不能证明会话准入",
            ),
        }
        for source, required_tokens in lifecycle_explainer_requirements.items():
            source_text = source.read_text()
            for token in required_tokens:
                if token not in source_text:
                    errors.append(
                        f"{source.relative_to(SOURCE_ROOT)} missing developer-facing attestation boundary: {token}"
                    )
        stale_attestation_teaching = {
            SOURCE_ROOT / "endem" / "index.html": (
                "attested 制品、运行策略",
                "改写 attested 制品",
                "六个语义面和状态机",
            ),
            SOURCE_ROOT / "endem" / "docs" / "running.md": (
                "形成 attested Endem/closure",
                "重新验证实际 attested 字节",
                "精确 attested Endem 或 closure",
                "修改 attested 制品",
            ),
        }
        for source, stale_tokens in stale_attestation_teaching.items():
            source_text = source.read_text()
            for token in stale_tokens:
                if token in source_text:
                    errors.append(
                        f"{source.relative_to(SOURCE_ROOT)} retains stale attestation teaching: {token}"
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
            "当前策略：正在研究；尚未进入规范",
        ):
            if token not in proposal_text:
                errors.append(f"preview and approval proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "preview-simulation-and-approval" in registry_text:
            errors.append("non-normative preview and approval proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "authority.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
        ):
            if "preview-simulation-and-approval-proposal.html" not in public_source.read_text():
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
            "九类状态必须分开",
            "OpenAI Agents SDK",
            "OpenAI Sandbox Agents",
            "跨运行记忆",
            "MCP 2025-11-25 Tasks",
            "2026-07-28 发布候选",
            "A2A 1.0",
            "GNU Make",
            "GNU Guix",
            "截至 2026 年 7 月 15 日",
            "恢复必须是重新验证，不是复活",
            "继续、重放、重试与回滚必须分开",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "当前策略：正在研究；尚未进入规范",
        ):
            if token not in proposal_text:
                errors.append(f"memory and resumption proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "memory-checkpoint-and-resumption" in registry_text:
            errors.append("non-normative memory and resumption proposal must not enter the specification registry")
        if "精确 Endem 或 closure 及其 attest 状态" in proposal_text:
            errors.append("memory and resumption proposal must not collapse attestation relations into content state")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "session-contract.md",
            SOURCE_ROOT / "specifications" / "adapters.md",
            SOURCE_ROOT / "specifications" / "evidence-entry.md",
            SOURCE_ROOT / "components" / "runner.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "memory-checkpoint-and-resumption-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the memory and resumption research proposal"
                )
        memory_teaching_requirements = {
            SOURCE_ROOT / "docs" / "architecture-guide.md": (
                "逐项重验适用的外部陈述、验证记录和依赖方准入判断",
                "不从检查点反序列化权限",
            ),
            SOURCE_ROOT / "specifications" / "adapters.md": (
                "旧 Task 句柄只帮助重新定位",
                "历史缺口和未知副作用",
                "恢复时重新核对对端、租户、当前授权",
            ),
            SOURCE_ROOT / "specifications" / "evidence-entry.md": (
                "历史与检查点何时能支持证据？",
                "保存状态只说明生产者保留了什么",
                "不恢复旧权限或补齐未知副作用",
            ),
            SOURCE_ROOT / "components" / "runner.md": (
                "从检查点继续必须建立新会话",
                "重新完成会话准入",
                "不能合并成“Agent 已恢复”",
            ),
        }
        for source, required_tokens in memory_teaching_requirements.items():
            source_text = source.read_text()
            for token in required_tokens:
                if token not in source_text:
                    errors.append(
                        f"{source.relative_to(SOURCE_ROOT)} missing developer-facing memory boundary: {token}"
                    )

    capability_proposal = SOURCE_ROOT / "spec" / "capability-discovery-and-negotiation-proposal.md"
    if not capability_proposal.exists():
        errors.append("missing non-normative capability discovery and negotiation research proposal")
    else:
        proposal_text = capability_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "当前策略：正在研究；尚未进入规范",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建新制品、文件格式、扩展名、命令、组件、结果域、稳定接口或哲学专名",
            "不进入 `registry.json`",
            "六类事实必须分开",
            "MCP 2025-11-25 生命周期",
            "A2A 1.0 版本化规范",
            "RFC 8707",
            "GNU Autoconf 2.73",
            "新能力不能扩写旧 contract",
            "候选责任的唯一主归属",
            "十二个案例",
            "变化处理矩阵",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "不创建 `CAP-CORE`、能力制品或新专名",
            "这些结论当前不会改变任何现行规范条款、登记、向量、contract 字段或结果值",
        ):
            if token not in proposal_text:
                errors.append(f"capability discovery proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "capability-discovery-and-negotiation" in registry_text or '"CAP-CORE"' in registry_text:
            errors.append("non-normative capability discovery proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "adapters.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "capability-discovery-and-negotiation-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the capability discovery research proposal"
                )

    agent_identity_proposal = SOURCE_ROOT / "spec" / "software-agent-identity-and-accountability-boundaries-proposal.md"
    if not agent_identity_proposal.exists():
        errors.append("missing non-normative software Agent identity and accountability research proposal")
    else:
        proposal_text = agent_identity_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "当前策略：正在研究；尚未进入规范",
            "不构成 ADR、CORE 规范、内容 Profile 或实现要求",
            "不创建 Agent 身份制品",
            "不进入 `registry.json`",
            "九个身份与关系层次必须分开",
            "身份、认证、授权与责任不是一条等级线",
            "NIST 2026 概念工作",
            "SPIFFE",
            "RFC 8693",
            "W3C PROV",
            "MCP Enterprise-Managed Authorization",
            "GNU Coreutils",
            "十二个支持案例与反例",
            "候选义务的唯一主归属",
            "失败域与结果隔离",
            "不创建 `AGENT-IDENTITY-CORE`",
        ):
            if token not in proposal_text:
                errors.append(f"software Agent identity proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "software-agent-identity-and-accountability-boundaries" in registry_text
            or '"AGENT-IDENTITY-CORE"' in registry_text
        ):
            errors.append("non-normative software Agent identity proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "authority.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
        ):
            if "software-agent-identity-and-accountability-boundaries-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the software Agent identity research proposal"
                )

    parallel_proposal = SOURCE_ROOT / "spec" / "parallel-and-speculative-execution-proposal.md"
    if not parallel_proposal.exists():
        errors.append("missing non-normative parallel and speculative execution research proposal")
    else:
        proposal_text = parallel_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
        ):
            if token not in proposal_text:
                errors.append(f"parallel execution proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if "parallel-and-speculative-execution" in registry_text or '"PAR-CORE"' in registry_text:
            errors.append("non-normative parallel execution proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "adapters.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "parallel-and-speculative-execution-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
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
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "session-contract.md",
            SOURCE_ROOT / "specifications" / "adapters.md",
            SOURCE_ROOT / "components" / "runner.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "model-adapter-isolation-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
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
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "evidence-entry.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "model-assisted-evaluation-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
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
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "identity.md",
            SOURCE_ROOT / "specifications" / "evidence-entry.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
        ):
            if "model-training-and-update-boundaries-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
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
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "downloads" / "index.html",
            SOURCE_ROOT / "faq" / "index.html",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
        ):
            if "model-openness-and-software-freedom-boundaries-proposal.html" not in public_source.read_text():
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
            "当前策略：正在研究；尚未进入规范",
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
            "尚未进入规范",
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
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "spec" / "model-openness-and-software-freedom-boundaries-proposal.md",
            SOURCE_ROOT / "downloads" / "index.html",
            SOURCE_ROOT / "faq" / "index.html",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
        ):
            if "hosted-ai-service-and-user-control-boundaries-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the hosted AI service research proposal"
                )

    data_lifecycle_proposal = (
        SOURCE_ROOT / "spec" / "software-agent-data-use-retention-and-deletion-boundaries-proposal.md"
    )
    if not data_lifecycle_proposal.exists():
        errors.append("missing non-normative software Agent data lifecycle research proposal")
    else:
        proposal_text = data_lifecycle_proposal.read_text()
        for token in (
            "状态：非规范研究提案",
            "当前策略：正在研究；尚未进入规范",
            "至少十八种事实必须分开",
            "不构成 ADR、CORE 规范、Profile、登记项、法律结论或实现要求",
            "不建立 `DATA-CORE`、`PRIVACY-CORE` 或 `DELETION-CORE`",
            "不进入 `registry.json`",
            "访问、使用、保留与删除不是一条状态线",
            "NIST Privacy Framework 1.0",
            "NIST SP 800-88 Rev. 2",
            "RFC 6973",
            "DPV 2.1",
            "MCP 2025-11-25 Elicitation",
            "GNU Coreutils `shred`",
            "至少十六个支持案例与反例",
            "威胁到失败责任的映射",
            "失败域与结果隔离",
            "候选责任的唯一主归属",
            "开发者最小检查清单",
            "术语与读音边界",
            "不创建新专名",
        ):
            if token not in proposal_text:
                errors.append(f"software Agent data lifecycle proposal missing governance boundary: {token}")
        registry_text = (SOURCE_ROOT / "spec" / "registry.json").read_text()
        if (
            "software-agent-data-use-retention-and-deletion-boundaries" in registry_text
            or '"DATA-CORE"' in registry_text
            or '"PRIVACY-CORE"' in registry_text
            or '"DELETION-CORE"' in registry_text
        ):
            errors.append("non-normative data lifecycle proposal must not enter the specification registry")
        for public_source in (
            SOURCE_ROOT / "spec" / "README.md",
            SOURCE_ROOT / "specifications" / "authority.md",
            SOURCE_ROOT / "specifications" / "evidence-entry.md",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "architecture" / "agent-system-boundaries.md",
        ):
            if "software-agent-data-use-retention-and-deletion-boundaries-proposal.html" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the data lifecycle research proposal"
                )

    agent_boundaries = SOURCE_ROOT / "architecture" / "agent-system-boundaries.md"
    if not agent_boundaries.exists():
        errors.append("missing public Agent system boundary guide")
    else:
        boundary_text = agent_boundaries.read_text()
        for token in (
            "用一次依赖升级完成边界判断",
            "一次 Agent 调用会同时产生目标、身份、授权、会话、协议状态、观察和决定",
            "期望终态是什么？",
            "目标只要求结果，还是还要求动作、转变或因果？",
            "谁代表谁执行什么动作？",
            "本次运行最多能做什么？",
            "外部系统实际报告了什么？",
            "什么证据支持哪项结论？",
            "退出码为零或 Task 完成只说明该次外部调用",
            "先识别越级，再定位缺失事实",
            "外部生态改变输入，不改变责任",
            "GNU 先例只提供工程约束",
            "遇到更强问题时再进入研究",
            "完成一次边界评审",
            "2025-11-25",
            "2026-07-28",
            "A2A 1.0.0",
            "OpenAI Agents SDK 编排说明",
            "人工参与机制",
            "Agents SDK 会话策略",
            "跨运行记忆",
            "运行轨迹",
            "Make target、prerequisite 与 recipe",
            "Guix profile generations",
            "Autoconf 特性检查",
            "Make 并行与 jobserver",
            "Guix shell",
            "Coreutils timeout",
            "隔离机制名称替代有效限制",
            "单项信号替代完整结论",
            "显示名称或能力声明替代授权",
            "记忆、检查点或轨迹替代当前事实",
            "NIST AI Agent Standards Initiative",
            "NIST AI 800-5",
            "Guix shell、channel、manifest 与 time-machine",
            "GNU Diffutils",
            "随机来源",
            "GNU 自由软件定义",
            "服务替代用户计算的分析",
            "AGPL 边界",
            "Coreutils `shred`",
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
            "software-agent-identity-and-accountability-boundaries-proposal.md",
            "parallel-and-speculative-execution-proposal.md",
            "model-adapter-isolation-proposal.md",
            "model-assisted-evaluation-proposal.md",
            "model-training-and-update-boundaries-proposal.md",
            "model-openness-and-software-freedom-boundaries-proposal.md",
            "hosted-ai-service-and-user-control-boundaries-proposal.md",
            "software-agent-data-use-retention-and-deletion-boundaries-proposal.md",
            "semantic-equivalence-and-migration-proposal.md",
        ):
            if proposal_name.replace(".md", ".html") not in boundary_text:
                errors.append(f"Agent boundary guide must link research input: {proposal_name}")
        for mechanical_heading in (
            "十六条最危险的越级路径",
            "GNU 技术与软件自由提供的十二个约束",
            "十五项研究怎样回到现有规范",
            "运行事实先按责任归类",
            "行业变化只改变外部机制",
            "GNU 先例怎样约束工程判断",
        ):
            if mechanical_heading in boundary_text:
                errors.append(
                    "Agent boundary guide hard-codes a drifting inventory count in visible copy: "
                    + mechanical_heading
                )
        for public_source in (
            SOURCE_ROOT / "architecture" / "index.html",
            SOURCE_ROOT / "architecture" / "open-questions.md",
            SOURCE_ROOT / "docs" / "architecture-guide.md",
            SOURCE_ROOT / "sitemap.md",
            SOURCE_ROOT / "_data" / "navigation.yml",
        ):
            if "agent-system-boundaries" not in public_source.read_text():
                errors.append(
                    f"{public_source.relative_to(SOURCE_ROOT)} must link the Agent system boundary guide"
                )

    forbidden_round_trip_claims = {
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

    downloads_text = (SOURCE_ROOT / "downloads" / "index.html").read_text()
    for token in (
        "机器可读登记",
        "向量源",
        "不是稳定 ABI 或组件运行结果",
    ):
        if token not in downloads_text:
            errors.append(f"downloads page missing authoritative evidence inventory link: {token}")
    volatile_inventory_pages = (
        SOURCE_ROOT / "specifications" / "index.html",
        SOURCE_ROOT / "specifications" / "adapters.md",
        SOURCE_ROOT / "specifications" / "evidence-entry.md",
        SOURCE_ROOT / "specifications" / "endem-closure.md",
        SOURCE_ROOT / "specifications" / "session-contract.md",
        SOURCE_ROOT / "specifications" / "authority.md",
        SOURCE_ROOT / "development" / "implementation-roadmap.md",
        SOURCE_ROOT / "downloads" / "index.html",
    )
    volatile_inventory_pattern = re.compile(
        r"(?:[0-9]+|[一二三四五六七八九十百]+)\s*(?:个|类|项|组)\s*(?:"
        r"[^。；，<\n]{0,16}(?:场景|威胁)|"
        r"[^。；，<\n]{0,12}(?:提案|语义|字节|规范)向量"
        r")|[0-9]+\s*个\s*(?:evidence|contract|Endem|closure|诊断|适配|身份|文本|授权)"
    )
    for source in volatile_inventory_pages:
        match = volatile_inventory_pattern.search(source.read_text())
        if match:
            errors.append(
                f"{source.relative_to(SOURCE_ROOT)} copies a drift-prone evidence inventory: {match.group(0)}"
            )
    for source in (
        SOURCE_ROOT / "components" / "producer.md",
        SOURCE_ROOT / "development" / "implementation-roadmap.md",
    ):
        source_text = source.read_text()
        for phrase in ("相同规范化输入", "前后六个语义面、依赖与披露行为保持规范等价"):
            if phrase in source_text:
                errors.append(
                    f"{source.relative_to(SOURCE_ROOT)} retains an undefined verification claim: {phrase}"
                )
    producer_text = (SOURCE_ROOT / "components" / "producer.md").read_text()
    for stale_phrase in ("根据已授权语义决定形成", "已授权的投影决定", "已授权 `meaning_projection`"):
        if stale_phrase in producer_text:
            errors.append(f"public developer guidance retains ambiguous semantic authorization wording: {stale_phrase}")
    producer_boundary_pages = {
        "components/index.html": (SOURCE_ROOT / "components" / "index.html").read_text(),
        "endem/index.html": (SOURCE_ROOT / "endem" / "index.html").read_text(),
        "endem/docs/reference.md": (SOURCE_ROOT / "endem" / "docs" / "reference.md").read_text(),
        "docs/architecture-guide.md": (SOURCE_ROOT / "docs" / "architecture-guide.md").read_text(),
    }
    for page, source_text in producer_boundary_pages.items():
        for stale_phrase in (
            "所有规范制品都必须通过 producer",
            "外部签名响应验证接口",
            "签名请求、分层诊断",
            "没有外部签名响应时只能保留未签候选",
        ):
            if stale_phrase in source_text:
                errors.append(f"{page} retains a stale producer boundary: {stale_phrase}")
    for page, token in {
        "components/index.html": "contract、evidence、外部签名与最终决定仍由各自责任域产生",
        "endem/index.html": "外部签名响应由独立集成核对，不作为 producer 输入",
        "endem/docs/reference.md": "Endem 规范字节的唯一生产入口",
        "docs/architecture-guide.md": "未来物理 Profile 确定后的 closure 与发布派生",
    }.items():
        if token not in producer_boundary_pages[page]:
            errors.append(f"{page} missing the precise producer boundary: {token}")
    inspector_boundary_pages = {
        "components/index.html": (SOURCE_ROOT / "components" / "index.html").read_text(),
        "endem/index.html": (SOURCE_ROOT / "endem" / "index.html").read_text(),
        "endem/docs/reference.md": (SOURCE_ROOT / "endem" / "docs" / "reference.md").read_text(),
        "endem/docs/safety.md": (SOURCE_ROOT / "endem" / "docs" / "safety.md").read_text(),
        "docs/architecture-guide.md": (SOURCE_ROOT / "docs" / "architecture-guide.md").read_text(),
    }
    for page, source_text in inspector_boundary_pages.items():
        for stale_phrase in (
            "任意不可信 Endem、closure 或 evidence 字节",
            "任意原始制品字节、视图和预算",
            "| `inspect` | 任意原始制品、视图和预算",
            "一致性验证对合法、边界和畸形向量分别运行 producer 与 inspector",
            "独立只读检查器（inspector）",
        ):
            if stale_phrase in source_text:
                errors.append(f"{page} retains a stale inspector boundary: {stale_phrase}")
    for page, token in {
        "components/index.html": "不产生生产检查通过结论",
        "endem/index.html": "其他对象等待物理格式",
        "endem/docs/reference.md": "不修复、不写回，也不生成生产检查通过结论",
        "endem/docs/safety.md": "生产侧 `lint` 路径与 inspector",
        "docs/architecture-guide.md": "closure、evidence 与发布制品等待物理格式",
    }.items():
        if token not in inspector_boundary_pages[page]:
            errors.append(f"{page} missing the precise inspector boundary: {token}")
    endem_reference_text = inspector_boundary_pages["endem/docs/reference.md"]
    for token in (
        "## 按工作查动作",
        "## 按对象查职责",
        "## 按结果域查状态",
        "## 按目标类型查约束",
        "## 按失败层查诊断",
        "## 按问题进入权威源",
        "## 当前可以证明什么",
        "集合身份、成员资格权威、截止点和身份规则",
        "`END-QNT-001` 至 `END-QNT-003`",
        "只有 [DIA-CAT]",
        "人类消息可以改写或本地化，但程序不得依赖其文本",
        "不是发行 ABI",
        "尚未发布为真实命令",
    ):
        if token not in endem_reference_text:
            errors.append(f"Endem reference missing task-oriented developer boundary: {token}")
    for obsolete_token in (
        "## 子命令索引",
        "## maintain 时间索引",
        "## 测量与阈值索引",
        "## 复合判断索引",
        "## 否定与缺席索引",
        "## 稳定失败类别",
        "source invalid",
        "contract incomplete",
        "malformed object",
        "implementation disagreement",
        "reproducibility failed",
    ):
        if obsolete_token in endem_reference_text:
            errors.append(f"Endem reference retains an obsolete inventory or free-form failure identity: {obsolete_token}")
    open_questions_text = source_path_for_route("architecture/open-questions.html").read_text()
    for token in (
        "现在还缺什么证据",
        "先判断问题处于哪一层",
        "现有材料",
        "开发者现在怎么做",
        "不能据此声称",
        "非规范研究提案",
        "仍待确定的物理 Profile",
        "未来实现与运行证据",
        "核心责任已确定",
        "END-P2 是含来源的形成与评审 Profile",
        "END-FMT 0.1.0-draft 才是实验性物理容器",
        "用一次字段变更检查是否可以继续",
        "signing_algorithm",
        "真正缺少什么？",
        "Agent 与运行研究怎样继续",
        "本节链接的研究提案均为非规范资料",
        "缺少物理 Profile 或实现证据时，停在明确的待定边界",
        "按四个问题域继续研究",
        "展开与当前问题直接相关的一组即可",
        "内容、格式与迁移缺少什么？",
        "组合、发布与外部决定怎样分开？",
        "ADR-0036 与 `END-PUB-001`",
        "删除、重写、保留与外置内容",
        "名称与实现怎样进入发行？",
        "统一规定现行名称、普通词规则、自造名称证据和机器关键字边界",
        "外部资料只决定证据类型",
        "GNU Manuals",
        "GNU BFD 信息损失",
        "NIST AI Agent Standards Initiative",
        "NIST AI 800-3",
        "物理 Profile 待定",
        "组件未实现",
        "怎样关闭一个开放问题",
    ):
        if token not in open_questions_text:
            errors.append(f"open questions guide missing developer decision boundary: {token}")
    for proposal_name in (
        "semantic-equivalence-and-migration-proposal.md",
        "model-assisted-evaluation-proposal.md",
        "gnu-elf-applicability-proposal.md",
        "software-agent-identity-and-accountability-boundaries-proposal.md",
        "model-context-assembly-proposal.md",
        "capability-discovery-and-negotiation-proposal.md",
        "parallel-and-speculative-execution-proposal.md",
        "planning-and-replanning-proposal.md",
        "state-change-and-causal-attribution-proposal.md",
        "preview-simulation-and-approval-proposal.md",
        "memory-checkpoint-and-resumption-proposal.md",
        "model-adapter-isolation-proposal.md",
        "model-training-and-update-boundaries-proposal.md",
        "model-openness-and-software-freedom-boundaries-proposal.md",
        "hosted-ai-service-and-user-control-boundaries-proposal.md",
        "software-agent-data-use-retention-and-deletion-boundaries-proposal.md",
    ):
        if proposal_name.replace(".md", ".html") not in open_questions_text:
            errors.append(f"open questions guide must route the research proposal: {proposal_name}")
    for old_heading in (
        "<h2>内容与物理格式</h2>",
        "<h2>组合、发布与外部决定</h2>",
        "<h2>Agent 与运行研究怎样继续</h2>",
        "<h2>术语与实现发布</h2>",
    ):
        if old_heading in open_questions_text:
            errors.append(f"open questions guide retains a flat research inventory: {old_heading}")
    specification_reader_contracts = {
        "specifications/endem-closure.html": (
            "按四步形成固定闭包",
            "尚无物理格式",
            "尚未实现",
        ),
        "specifications/session-contract.html": ("按五步建立本次边界",),
        "specifications/evidence-entry.html": (
            "按四步形成并评估一项记录",
            "尚无物理格式",
            "尚未实现",
        ),
        "specifications/diagnostics.html": (
            "诊断必须保持哪些边界",
            "物理格式待定",
            "尚无运行组件",
        ),
        "specifications/adapters.html": (
            "按十二项责任检查一次调用",
            "物理格式不适用",
            "尚无适配器",
        ),
        "specifications/identity.html": (
            "按十二项责任检查身份与签名",
            "尚无密码实现",
        ),
        "specifications/text-and-identifiers.html": (
            "文本与标识符必须怎样处理",
            "Unicode Profile 待定",
            "尚无文本处理组件",
        ),
        "specifications/authority.html": (
            "权威与授权必须怎样判断",
            "尚无政策引擎",
        ),
    }
    for route, required_tokens in specification_reader_contracts.items():
        specification_text = source_path_for_route(route).read_text()
        for token in required_tokens:
            if token not in specification_text:
                errors.append(f"{route} missing developer-oriented specification label: {token}")
        for pattern in (
            r'<span class="badge">(?:\d+ (?:Clauses|Vectors)|No [^<]+|Wire Not Applicable)</span>',
            r"<h2>(?:十条核心规则|十二条适配规则|十二条身份与签名规则|十二条文本规则|十二条权威与授权规则)</h2>",
        ):
            if re.search(pattern, specification_text):
                errors.append(f"{route} exposes a drifting specification inventory instead of a reader task")
    for route, stale_inventory in {
        "specifications/diagnostics.html": (
            "十五个支持案例",
            "二十个资料一致性提案",
            "用十条核心规则定义诊断内容",
        ),
        "specifications/identity.html": (
            "12 类身份混淆",
            "18 个支持",
            "24 个提案",
            "用十二条核心规则定义",
        ),
        "specifications/text-and-identifiers.html": (
            "12 类编码",
            "18 个支持",
            "24 个提案",
            "十二条规则分开处理",
        ),
    }.items():
        specification_text = source_path_for_route(route).read_text()
        for phrase in stale_inventory:
            if phrase in specification_text:
                errors.append(f"{route} copies a drift-prone source count into public guidance: {phrase}")
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
    handwritten_html_routes = {
        path.relative_to(SOURCE_ROOT).as_posix() for path in SOURCE_HTML_FILES
    }
    if handwritten_html_routes != ALLOWED_HANDWRITTEN_HTML_ROUTES:
        errors.append(
            "hand-written HTML must be limited to approved interface pages; "
            f"missing={sorted(ALLOWED_HANDWRITTEN_HTML_ROUTES - handwritten_html_routes)}, "
            f"unexpected={sorted(handwritten_html_routes - ALLOWED_HANDWRITTEN_HTML_ROUTES)}"
        )

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
    errors.extend(validate_prose_readability_contracts())

    forbidden_shell = re.compile(
        r"<!doctype|<html\b|<head\b|<body\b|class=\"site-header\"|<footer\b",
        re.IGNORECASE,
    )
    if len(source_routes) != len(set(source_routes)):
        errors.append("multiple source files generate the same formal route")

    summary_owners = defaultdict(list)
    generic_page_summaries = {
        "版本化规范源，记录条款、责任、成熟度与验证边界。",
        "非规范设计场景，记录支持案例、反例与待确认边界。",
        "威胁模型，记录攻击面、失败责任与采用限制。",
        "非规范研究提案，记录问题边界、证据、反例与停止条件。",
    }
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
        is_manual_markdown = path in MANUAL_MARKDOWN_FILES
        is_spec_markdown = path in SPEC_MARKDOWN_FILES
        is_architecture_decision = (
            path in ARCHITECTURE_MARKDOWN_FILES and path.name.startswith("adr-")
        )
        is_page_directory_markdown = path in PAGE_DIRECTORY_MARKDOWN_FILES
        expected = {
            "layout": (
                "manual" if is_manual_markdown
                else "spec" if is_spec_markdown
                else "architecture-decision" if is_architecture_decision
                else "page-directory" if is_page_directory_markdown
                else "content" if path in CONTENT_MARKDOWN_FILES or path in ARCHITECTURE_MARKDOWN_FILES
                else "default"
            ),
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
        if is_spec_markdown:
            document_status = front_matter_value(metadata, "document_status")
            allowed_document_statuses = {
                "规范源目录", "规范草案", "规范目录草案",
                "实验性格式草案", "实验性来源设计",
                "非规范设计场景", "威胁模型", "非规范研究提案",
            }
            if document_status not in allowed_document_statuses:
                errors.append(
                    f"{route}: spec Markdown requires a reader-facing document_status"
                )
        page_summary = front_matter_value(metadata, "summary") or ""
        if not page_summary:
            errors.append(f"{route}: every formal page requires a reader-facing summary")
        else:
            summary_owners[page_summary].append(route)
            if len(page_summary) < 20 or len(page_summary) > 120:
                errors.append(
                    f"{route}: page summary must stay between 20 and 120 characters"
                )
            if page_summary in generic_page_summaries:
                errors.append(
                    f"{route}: page summary must name its concrete reader problem"
                )
        body = text[match.end():]
        entry_text = page_summary
        abstract_entry_terms = (
            "制品", "闭包", "投影", "权威", "边界", "结果域", "信任域", "语义",
            "授权", "身份", "Profile", "伴随", "符合性", "不变量",
        )
        entry_abstract_hits = sorted({
            term for term in abstract_entry_terms if term in entry_text
        })
        if len(entry_abstract_hits) >= 4:
            errors.append(
                f"{route}: introduction stacks abstract terms before a plain-language problem: "
                + ", ".join(entry_abstract_hits)
            )
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
        if path.suffix == ".md":
            body_without_autolinks = re.sub(
                r"<(?:https?://|mailto:)[^>]+>", "", body, flags=re.IGNORECASE
            )
            body_without_autolinks = re.sub(
                r'<span id="[A-Za-z][A-Za-z0-9_-]*"></span>',
                "",
                body_without_autolinks,
            )
            body_without_autolinks = re.sub(
                r"<br\s*/?>", "", body_without_autolinks, flags=re.IGNORECASE
            )
            if re.search(r"</?[A-Za-z][^>]*>", body_without_autolinks):
                errors.append(f"{route}: Markdown body must not contain raw HTML")
            for attribute_line in re.findall(r"^\s*\{:[^\n]+$", body, re.MULTILINE):
                if re.fullmatch(r"\s*\{:\s*#[A-Za-z][A-Za-z0-9_-]*\s*}", attribute_line) is None:
                    errors.append(
                        f"{route}: Markdown body uses an unsupported Kramdown attribute {attribute_line!r}"
                    )
            if is_manual_markdown:
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

    for summary, owners in summary_owners.items():
        if len(owners) > 1:
            errors.append(
                "formal pages must not share a generic summary: "
                f"{summary!r} used by {sorted(owners)}"
            )

    homepage_source = SOURCE_ROOT / "index.html"
    if homepage_source.exists():
        homepage_text = homepage_source.read_text()
        for token in (
            'title: "Noemion · 让每个人编译自己的意图"',
            '<h1 id="portal-title"><span class="portal-title-brand">Noemion</span><strong><span>人工智能时代</span><span class="portal-title-foundation">每个人都应该能编译自己的意图</span></strong></h1>',
            '<p class="portal-introduction-summary">Noemion 研究如何让每个人以自然语言表达意图，并将其形成供人工智能系统安全使用的目标制品。发布制品只保留经过确认的目标结构，并在使用前核对授权边界，防止人工智能系统改变目标含义，或执行未经授权的越权行为。</p>',
            '<span>从开发者案例开始</span>',
            '<span>查看 Endem 生命周期</span>',
            '<strong>Noemion</strong> 是项目与研究领域的名称',
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
        style_text = (SOURCE_ROOT / "assets" / "style.css").read_text()
        for token in (
            ".portal-introduction h1 .portal-title-foundation",
            "text-decoration-style:solid",
            "text-decoration-thickness:.06em",
        ):
            if token not in style_text:
                errors.append(f"assets/style.css: homepage title must retain the single underline contract: {token}")
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
            'class="portal-focus-card focus-card-closure" href="specifications/endem-closure.html"',
            'class="portal-focus-card focus-card-session" href="specifications/session-contract.html"',
            'class="portal-focus-card focus-card-evidence" href="specifications/evidence-entry.html"',
        ):
            if token not in homepage_text:
                errors.append(f"index.html: missing independent homepage object card: {token}")
        if homepage_text.count('class="portal-focus-card ') != 4:
            errors.append("index.html: FOUR NOUNS must render four independent object cards")
        homepage_card_routes = (
            'class="portal-feature-row" href="specifications/endem.html#source_expression"',
            'class="portal-feature-row" href="specifications/endem.html#situation"',
            'class="portal-feature-row" href="specifications/endem.html#satisfaction_criteria"',
            'class="portal-feature-row" href="specifications/endem.html#unresolved_meaning"',
            'class="portal-focus-card focus-card-endem" href="specifications/endem.html"',
            'class="portal-focus-card focus-card-closure" href="specifications/endem-closure.html"',
            'class="portal-focus-card focus-card-session" href="specifications/session-contract.html"',
            'class="portal-focus-card focus-card-evidence" href="specifications/evidence-entry.html"',
            '<a href="endem/#action-map"><span class="lifecycle-number">01</span>',
            '<a href="components/inspector.html"><span class="lifecycle-number">02</span>',
            '<a href="components/runner.html"><span class="lifecycle-number">03</span>',
            '<a href="endem/"><small>01</small><strong>Endem 应用</strong>',
            '<a href="specifications/"><small>02</small><strong>规范</strong>',
            '<a href="architecture/"><small>03</small><strong>架构</strong>',
            '<a href="components/"><small>04</small><strong>组件</strong>',
            '<a href="development/current-stage.html"><small>05</small><strong>项目进展</strong>',
            '<a href="docs/"><small>06</small><strong>指南与参考</strong>',
        )
        for contract in homepage_card_routes:
            if homepage_text.count(contract) != 1:
                errors.append(
                    "index.html: each homepage card must keep one explicit target: "
                    f"{contract}"
                )

    source_release_contracts = {
        "architecture/index.html": ("来源保留的形成版", "最终发布版移除原文", "独立 Profile 重写来源绑定"),
        "about/index.html": ("形成版保存一项目标的来源", "最终发布版移除原文"),
        "faq/index.html": ("来源保留的形成版分开六项职责", "发布时再按独立 Profile 移除原文和可逆重建材料"),
        "endem/docs/index.md": ("来源保留的形成版", "最终发布版按独立 Profile 移除原文", "精确发布内容签名"),
    }
    for relative_path, tokens in source_release_contracts.items():
        page_text = source_path_for_route(relative_path).read_text()
        for token in tokens:
            if token not in page_text:
                errors.append(f"{relative_path}: missing source-bearing and stripped-release boundary: {token}")

    safe_artifact_contracts = {
        "_config.yml": (
            "形成供人工智能系统安全使用的目标制品",
            "发布制品只保留经过确认的目标结构",
            "在使用前核对授权边界",
        ),
        "docs/getting-started.md": (
            "这里的“安全”不是文件自带的布尔属性",
            "形成与发布",
            "内容完整性",
            "意义确认",
            "动作授权",
            "证据与满足",
            "最终决定",
        ),
        "faq/index.html": (
            "文件本身已经获准执行",
            "发布版只保留经过确认的目标结构",
            "运行完成后还要分开证据有效性、对判据的覆盖度、满足结果与最终决定",
            "它不会给自己签发工具调用、修改、部署或跨会话权限",
            "本次能力只取授权决定、contract、环境与预算的交集",
        ),
        "architecture/index.html": (
            "计划中的 <code>endem</code> 入口承载五项公开职责",
            "五个现行标识不是已经发布的子命令",
            "当前还没有可执行 CLI",
            "证据集合相对精确 <code>satisfaction_criteria</code> 形成覆盖度",
            "具名权威才形成最终决定",
        ),
    }
    for relative_path, tokens in safe_artifact_contracts.items():
        artifact_text = source_path_for_route(relative_path).read_text()
        for token in tokens:
            if token not in artifact_text:
                errors.append(f"{relative_path}: missing developer safe-artifact boundary: {token}")

    obsolete_safe_artifact_phrases = {
        "_config.yml": ("目标结构与授权边界可验证",),
        "docs/getting-started.md": ("可持久保存、组合和独立检查的工程制品",),
        "faq/index.html": ("持久、可检查的工程制品",),
        "architecture/index.html": (
            "<code>endem</code> 提供五个固定子命令",
            "<code>satisfaction_criteria</code> 形成覆盖与满足判断",
        ),
    }
    for relative_path, phrases in obsolete_safe_artifact_phrases.items():
        artifact_text = source_path_for_route(relative_path).read_text()
        for phrase in phrases:
            if phrase in artifact_text:
                errors.append(f"{relative_path}: retains ambiguous safe-artifact wording: {phrase}")

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
            "jekyll.environment == 'production'",
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
        if 'class="skip-link"' in layout_text or "跳到正文" in layout_text:
            errors.append("default layout must not render the removed skip-to-content entry")

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
            "'/pages/index.html'",
            "全部页面",
            "文档",
            "Endem",
            "开发",
            "常见问题",
            "许可证",
            'href="https://github.com/Noemion"',
            ">GitHub·Pages<",
            "跟随系统",
            "浅色",
            "深色",
        ):
            if token not in footer_text:
                errors.append(f"site footer missing global discovery/theme contract: {token}")
        for obsolete_label in (
            "PROJECT", "READ", "BUILD", "DISCOVERY", "Browse All",
            "Documentation", "Development", "License", ">Theme<",
            ">Light<", ">Dark<", ">System<",
        ):
            if obsolete_label in footer_text:
                errors.append(
                    "site footer must not retain generic English interface label: "
                    f"{obsolete_label}"
                )
        for forbidden_footer_entry in ("sitemap.md",):
            if forbidden_footer_entry in footer_text:
                errors.append(
                    "site footer must link reader-facing HTML pages instead of exposing "
                    f"{forbidden_footer_entry!r}"
                )
        browse_section = re.search(
            r"<section>\s*<h3>浏览</h3>(.*?)</section>",
            footer_text,
            re.DOTALL,
        )
        if not browse_section or "'/pages/index.html'" not in browse_section.group(1) or "全部页面" not in browse_section.group(1):
            errors.append("site footer must place the reader page directory in the Browse column")
        footer_bottom = re.search(
            r'<div class="site-footer-bottom">(.*)<div class="site-theme-picker"',
            footer_text,
            re.DOTALL,
        )
        if footer_bottom and ("'/pages/index.html'" in footer_bottom.group(1) or "全部页面" in footer_bottom.group(1)):
            errors.append("site footer must not present the reader page directory as a bottom-bar action")
        if "site-footer-directory-button" in footer_text:
            errors.append("site footer must not restore a standalone page-directory button")

    page_directory_source = SOURCE_ROOT / "pages" / "index.md"
    page_directory_layout = SOURCE_ROOT / "_layouts" / "page-directory.html"
    page_directory_module = SOURCE_ROOT / "assets" / "modules" / "page-directory.mjs"
    for path, tokens in {
        page_directory_source: (
            'layout: page-directory',
            'permalink: "/pages/index.html"',
            'page_heading: "全部页面"',
        ),
        page_directory_layout: (
            '<table class="page-directory-table">',
            '<th scope="col">页面</th>',
            '<label class="page-directory-column-filter"><span>栏目</span>',
            '<th scope="col">路径</th>',
            '<th scope="col">说明</th>',
            "data-page-directory-query",
            "data-page-directory-group-select",
            "data-page-directory-item",
        ),
        page_directory_module: (
            "connectPageDirectory",
            "item.dataset.pageDirectorySearch",
            'item.hidden = !matches',
            'count.textContent = String(visible)',
            'groupSelect.addEventListener("change", update)',
        ),
    }.items():
        if not path.exists():
            errors.append(f"missing reader page directory source: {path.relative_to(SOURCE_ROOT)}")
            continue
        page_directory_text = path.read_text()
        for token in tokens:
            if token not in page_directory_text:
                errors.append(
                    f"{path.relative_to(SOURCE_ROOT)} missing reader directory contract: {token}"
                )
    page_directory_style_text = (SOURCE_ROOT / "assets" / "style.css").read_text()
    if "site-footer-directory-button" in page_directory_style_text:
        errors.append("shared styles must not retain the removed standalone footer directory button")
    for token in (
        ".page-directory-controls{\n  display:block",
        ".page-directory-table",
        ".page-directory-column-filter",
        ".page-directory-main .page-directory-table tbody tr",
        ".page-directory-main .page-directory-table tbody tr[hidden]{display:none}",
        "grid-template-columns:minmax(0,1fr) auto",
    ):
        if token not in page_directory_style_text:
            errors.append(f"shared styles missing responsive page directory contract: {token}")
    for forbidden_token in (
        "data-page-directory-filter",
        ".page-directory-filter",
    ):
        for path in (page_directory_layout, page_directory_module, SOURCE_ROOT / "assets" / "style.css"):
            if path.exists() and forbidden_token in path.read_text():
                errors.append(
                    f"{path.relative_to(SOURCE_ROOT)} must not restore standalone directory filter buttons: "
                    f"{forbidden_token}"
                )

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
            'const MODE_LABELS = { light: "浅色", dark: "深色", system: "跟随系统" }',
            'trigger.setAttribute("aria-label", `主题：${name.textContent}`)',
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
            "calc(var(--nav-order) * 15ms)",
            "prefers-reduced-motion:reduce",
            "body .global-brand .portal-brand-mark{color:#10261e;background:#f0f6f3}",
            ".global-timeline-value{",
            "width:100%;height:100%;min-width:96px;min-height:var(--site-header-height)",
            "background:transparent;border-left:1px solid var(--rule)",
            "background:color-mix(in srgb,var(--nav-bg) 78%,var(--accent-soft))",
            ".content-split{",
            ".content-split-reverse{",
            'body[data-page-role="content"]:not([data-docs-layout="true"]) :is(main:not(.current-stage-page),.summary-rail-main)>section :is(p,li,blockquote)',
            ".content-stack",
            ".content-band{",
            ".content-wide",
            ".content-grid{",
            ".content-rows",
            ".content-stack>*,",
            ".content-wide>:is(h2,p,ul,ol,blockquote,.lead,.note,.callout)",
            ".content-grid>:is(h2,p,ul:not(.grid):not(.status-grid):not(.resource-list),ol,blockquote)",
            'body[data-page-role="section"]:not([data-page-role="portal"]) main>section>:is(h2,p,ul,ol,blockquote)',
            ".manual-article>:is(h3,h4,p,ul,ol,blockquote)",
            ".faq-list details>p{max-width:760px;margin-right:auto;margin-left:0",
            "margin-right:auto;margin-left:0",
            'body:not([data-page-role="portal"]) .page-links{',
            '--site-frame-max:1200px',
            '--site-frame-edge:18px',
            '--site-frame-inset:36px',
            '--site-frame-width:min(var(--site-frame-max),calc(100% - var(--site-frame-inset)))',
            '--site-frame-left:max(var(--site-frame-edge),calc((100% - var(--site-frame-max))/2))',
            '--site-header-height:64px',
            '--site-mobile-directory-row-height:48px',
            '--docs-rail-width:320px',
            '--docs-content-width:880px',
            ':root{--site-frame-edge:8px;--site-frame-inset:16px}',
            '--responsive-grid-min:420px;gap:1px;margin:28px calc(-1 * var(--site-content-inline)) -62px;background:var(--portal-line)',
            'a:visited:not(.portal-button)',
            ".portal-button-primary:visited",
            ".portal-button-secondary:visited",
            '@media(max-width:999px)',
            'body .site-header .global-directory-panel{',
            'body[data-mobile-directory-stacked]:not([data-page-role="portal"]) .global-header-inner',
            'body[data-mobile-directory-stacked]:not([data-page-role="portal"]) .global-directory-panel',
            'body[data-mobile-directory-stacked]:not([data-page-role="portal"]) .breadcrumbs{padding-right:102px}',
            'transition-duration:180ms;transition-timing-function:cubic-bezier(.2,0,0,1);transition-delay:0s',
            '.site-header .directory-panel.is-closing nav',
            'html.mobile-directory-open{overscroll-behavior:none}',
            'background:color-mix(in srgb,var(--paper) 98%,transparent);backdrop-filter:none;-webkit-backdrop-filter:none',
            '.global-directory-panel[open]>.mobile-directory-backdrop{',
            'position:fixed;inset:0;z-index:1;display:block;background:transparent',
            'transition-property:opacity,transform,visibility',
            'will-change:opacity,transform;contain:layout paint;backface-visibility:hidden',
            'height:auto;max-height:calc(var(--mobile-directory-viewport-height,100dvh) - var(--site-header-height) - var(--site-frame-edge))',
            'html.mobile-directory-open body:not([data-page-role="portal"]) .global-directory-panel nav{',
            'height:auto;max-height:calc(var(--mobile-directory-viewport-height,100dvh) - var(--site-header-height) - var(--site-mobile-directory-row-height) - var(--site-frame-edge))',
            'touch-action:pinch-zoom',
            'isolation:isolate',
            'overflow-anchor:none;overscroll-behavior:none',
            '.nav-section-links{min-height:0;overflow:hidden;overflow:clip}',
            '.directory-loading-status{display:none',
            'nav[aria-busy="true"] .directory-loading-status',
            ':root[data-resolved-theme="dark"]',
            '--bg:#030a08',
            '--paper:#060f0d',
            '--paper-subtle:#091813',
            '--paper-raised:#0d2019',
            '--nav-bg:#071510',
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
            '--module-introduction-clip:polygon(0 0,80% 0,100% 100%,20% 100%)',
            '--module-card-clip:polygon(0 0,88% 0,100% 100%,12% 100%)',
            '--module-marker-clip:polygon(16% 0,100% 0,84% 100%,0 100%)',
            "clip-path:var(--module-introduction-clip)",
            "clip-path:var(--module-card-clip)",
            "radial-gradient(circle at var(--module-node-1)",
            'body[data-docs-layout="true"] .manual-introduction::before{',
            "clip-path:polygon(0 0,74% 0,100% 26%,100% 100%,0 100%)",
            'body .global-brand{grid-column:1;min-width:0;overflow:hidden',
            'body .global-brand>span:last-child{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
            'body[data-page-role="portal"] .global-header-inner{grid-template-columns:minmax(0,1fr) clamp(102px,30vw,124px) 84px}',
            'body[data-page-role="portal"] .global-timeline-link{width:100%;min-width:0;padding:0}',
            'body[data-page-role="portal"] .global-timeline-value{width:100%;min-width:0;padding-inline:7px;font-size:11px;letter-spacing:.04em}',
            '.portal-focus-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))',
            '.status-columns{column-width:340px;column-gap:18px}',
            '.status-columns>.status-item{break-inside:avoid;margin:0 0 18px}',
            '.focus-card-session .focus-art',
            '.focus-card-evidence .focus-art',
            'text-decoration-color:color-mix(in srgb,var(--portal-coral) 54%,var(--portal-amber))',
            'text-decoration-thickness:.06em;text-underline-offset:.13em;text-decoration-skip-ink:none',
        ):
            if token not in shared_css:
                errors.append(f"shared styles missing site-wide design contract: {token}")
        if re.search(r"transition\s*:\s*all\b", shared_css):
            errors.append("shared styles must not use transition: all")
        for duplicated_frame_formula in (
            "width:min(1200px,calc(100% - 36px))",
            "width:calc(100% - 16px)",
            "left:max(18px,calc((100% - 1200px)/2))",
        ):
            if duplicated_frame_formula in shared_css:
                errors.append(
                    f"shared styles must consume the global frame tokens instead of {duplicated_frame_formula}"
                )
        if re.search(r"html\.mobile-directory-open\s+body\s*\{", shared_css):
            errors.append("mobile directory must not replace body layout while the overlay is open")
        if re.search(r"html\.mobile-directory-open\s*\{[^}]*overflow\s*:", shared_css):
            errors.append("mobile directory must not change root overflow while the overlay is open")
        if 'body:not([data-page-role="portal"]) .global-header-inner{grid-template-columns:' in shared_css:
            errors.append("non-portal mobile header must not force a fixed two-column layout")
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
        if re.search(r'body:not\(\[data-page-role="portal"\]\) \.page-link:nth-child', shared_css):
            errors.append("page-link separators must not depend on a fixed column count")
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

    protocol_reference_files = SOURCE_PAGE_FILES
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
            "GNU Binutils 2.46.1",
            "A2A 1.0 版本化规范",
            "补丁号不进入协议协商",
            "OpenTelemetry 语义约定 1.43.0",
            "github.com/open-telemetry/semantic-conventions-genai",
            "MCP 2025-11-25 当前修订（Current）",
            "GenAI Schema URL 1.42.0",
            "Schema URL 或仓库活动都不等于稳定发布",
            "GNU Automake 测试结果语义",
            "后续版本在正式发布",
            "敏感内容不得默认导出",
            "NIST AI RMF 与 GenAI Profile",
            "NIST AI Agent 标准化工作",
            "外部协议适配不变量",
            "身份不等于权威",
            "外部状态不等于本地结果",
            "能力声明不等于实时句柄",
            "遥测单向外送",
            "撤销与重放显式",
        ),
        "components/runner.html": (
            "A2A 1.0",
            "MCP 2025-11-25 当前修订",
            "目标资源绑定",
            "OpenTelemetry 语义约定 1.43.0",
            "GenAI Schema URL 1.42.0",
            "Schema URL 不等于稳定发布",
            "Development",
            "默认不导出敏感正文",
            "completed / failed / stopped",
            "不能把工具故障改写为目标不满足",
        ),
        "development/implementation-roadmap.html": (
            "当前可以推进什么",
            "进入下一层需要什么证据",
            "何时停止或返回",
            "进入实现前先证明一条验证切片",
            "现行设计标识，不是已发布接口",
            "普通英语词已经通过词首、职责和关键字检查",
            "GNU 技术提供哪些工程纪律",
            "外部 Agent 与模型何时接入",
            "候选版在正式发布前只作为迁移风险",
            "OpenTelemetry 语义约定 1.43.0",
            "已把 GenAI 约定移至独立仓库",
            "默认脱敏的单向导出",
            "不进入 Endem 编码、evidence 身份、授权决定或最终接受",
        ),
        "endem/docs/running.md": (
            "A2A 1.0 版本化规范",
            "只有正式发布并完成",
            "OpenTelemetry 语义约定 1.43.0",
            "GenAI Schema URL 1.42.0",
            "仍无 GitHub release 或 tag",
            "Schema URL 不等于稳定发布",
            "默认不导出正文",
            "不构成 evidence 身份",
        ),
        "architecture/adr-0016-time-evidence.html": (
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
            "GNU grep 退出状态",
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
        "architecture/adr-0021-closure-and-activation.html": (
            "GNU ld 文件命令",
            "GNU Guix 参考手册",
            "GNU make 条件指令",
            "W3C SHACL",
            "MCP 2025-11-25 工具规范",
            "正式绑定必须记录精确身份",
            "不能改变 closure 闭包或直接授予权限",
        ),
    }
    for relative_path, required_tokens in external_boundary_contracts.items():
        boundary_text = source_path_for_route(relative_path).read_text()
        for token in required_tokens:
            if token not in boundary_text:
                errors.append(
                    f"{relative_path}: missing external technology boundary {token!r}"
                )
    roadmap_text = (SOURCE_ROOT / "development" / "implementation-roadmap.md").read_text()
    for stale_heading in (
        "四条长期原则",
        "未来第一条组件路径",
        "外部 Agent 技术只决定适配边界",
        "研究主题怎样回到开发决策",
    ):
        if stale_heading in roadmap_text:
            errors.append(
                f"development/implementation-roadmap.html: stale duplicate roadmap section {stale_heading!r}"
            )
    stale_protocol_phrases = (
        "MCP 2025-11-25 稳定规范",
        "A2A 最新规范",
        "github.com/a2aproject/A2A/blob/main/docs/specification.md",
        "Schema URL 待定",
        "Schema URL 仍待确定",
        "Schema URL 字段仍为",
    )
    for protocol_reference_file in protocol_reference_files:
        protocol_reference_text = protocol_reference_file.read_text()
        for phrase in stale_protocol_phrases:
            if phrase in protocol_reference_text:
                errors.append(
                    f"{protocol_reference_file.relative_to(SOURCE_ROOT)}: stale protocol baseline phrase {phrase!r}"
                )
    naming_adr = source_path_for_route("architecture/adr-0010-native-lexicon.html")
    if naming_adr.exists():
        naming_adr_text = naming_adr.read_text()
        for token in (
            "把人实际说过的话、系统采用的解释",
            "本决定确定六项语义职责",
            "ADR-0037",
            "范围有限具名权威确认",
            "规范称其为语义授权，但它不授予动作权限",
        ):
            if token not in naming_adr_text:
                errors.append(f"ADR-0010 missing responsibility-first naming boundary: {token}")
        if "六个短词" in naming_adr_text:
            errors.append("ADR-0010 must not present short field names as the value of the decision")

    spec_layout = SOURCE_ROOT / "_layouts/spec.html"
    if not spec_layout.exists():
        errors.append("missing _layouts/spec.html")
    else:
        spec_layout_text = spec_layout.read_text()
        for token in (
            "{{ page.summary }}",
            "{{ page.document_status }}",
            "返回规范源目录",
        ):
            if token not in spec_layout_text:
                errors.append(f"spec layout missing reader-facing contract: {token}")
        for forbidden in (
            "Markdown 唯一正文源", "自动生成 HTML", "查看 Markdown 源",
            "github.com/Noemion/noemion.github.io/blob/main",
        ):
            if forbidden in spec_layout_text:
                errors.append(
                    f"spec layout exposes publication process instead of content status: {forbidden}"
                )

    manual_config = SOURCE_ROOT / "_data/manuals.yml"
    manual_layout = SOURCE_ROOT / "_layouts/manual.html"
    docs_rail_include = SOURCE_ROOT / "_includes/docs-rail.html"
    manual_pagination_include = SOURCE_ROOT / "_includes/manual-pagination.html"
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
            'include manual-pagination.html position="top"',
            'include manual-pagination.html position="bottom"',
        ):
            if token not in manual_layout_text:
                errors.append(f"manual layout missing dynamic contract: {token}")
    if not manual_pagination_include.exists():
        errors.append("missing _includes/manual-pagination.html")
    else:
        manual_pagination_text = manual_pagination_include.read_text()
        for token in (
            'manual-nav-{{ include.position }}',
            'data-manual-role="previous"',
            'data-manual-role="up"',
            'data-manual-role="next"',
            'data-manual-role="index"',
        ):
            if token not in manual_pagination_text:
                errors.append(f"shared manual pagination missing contract: {token}")
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
        if global_navigation_labels != ["项目", "规范", "应用", "指南", "进展"]:
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
            "setTimeout(() => this.#setExpanded(item, true), 20)",
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
            "MobileHeaderLayout",
            "SummaryRailLayout",
            "shouldSplitSummaryRail",
            "connectSummaryRailLayouts",
            "shouldStackMobileDirectory",
            "LayoutObserver",
            "cssNumber",
            "ResizeObserver",
            'document.body.toggleAttribute("data-mobile-directory-stacked", stacked)',
            'document.fonts?.ready.then(this.schedule)',
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
            'const precisePointer = matchMedia("(hover: hover) and (pointer: fine)")',
            'if (event.key === "Tab") keyboardNavigation = true',
            "keyboardNavigation = false",
            "if (mobileLayout.matches) ensureDirectory()",
            "if (mobileLayout.matches) ensureMobileHeaderLayout()",
            'mobileLayout.addEventListener("change"',
            "if (event.matches) {",
            "} else if (precisePointer.matches) {",
            "if (!globalRoot || mobileLayout.matches) return",
            "if (precisePointer.matches) requestGlobalNavigation(event)",
            "if (precisePointer.matches || keyboardNavigation) requestGlobalNavigation(event)",
            'if (mobileLayout.matches || precisePointer.matches) return',
            'event.target.closest?.(".global-nav-trigger")',
            'item.classList.contains("is-menu-open")',
            "event.preventDefault()",
            'const coverUrl = new URL("nav-covers.svg", scriptUrl).href',
            "const prepareGlobalNavigation = () =>",
            "if (!mobileLayout.matches && precisePointer.matches) prepareGlobalNavigation()",
            'precisePointer.addEventListener("change"',
            'void fetch(coverUrl, { credentials: "same-origin" }).catch(() => {})',
        ):
            if token not in site_text:
                errors.append(f"site entry missing device-specific navigation contract: {token}")
        if site_text.count('matchMedia("(max-width: 999px)")') != 1:
            errors.append("site entry must expose exactly one shared compact-layout media state")
        if 'matchMedia("(min-width: 1000px)")' in site_text:
            errors.append("site entry must derive desktop navigation from the shared compact-layout state")
        layout_text = layout.read_text() if layout.exists() else ""
        for eager_resource in ('rel="modulepreload"', 'rel="preload" href="{{ \'/assets/navigation-data.json\''):
            if eager_resource in layout_text:
                errors.append(f"default layout must not eagerly load both navigation modes: {eager_resource}")
        if re.search(r"^ensureDirectory\(\);$", site_text, re.MULTILINE):
            errors.append("site entry must not build the mobile directory unconditionally")
        for token in (
            "@media(hover:none) and (pointer:coarse)",
            ".portal-reveal{animation:none!important}",
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
            'import(moduleUrl("mobile-header-layout"))',
            'import(moduleUrl("content-enhancements"))',
            'import(moduleUrl("summary-rail-layout"))',
            'import(moduleUrl("page-directory"))',
            'document.querySelector("[data-summary-rail-layout]")',
            'document.querySelector("[data-page-directory]")',
            'const needsScrollFocus = Boolean(document.querySelector(".table-wrap, pre"))',
            "needsTableScroller || needsScrollFocus || longContent",
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
        for token in (
            "this.groupsByKey = new Map",
            "#ensureMenu(item)",
            'item.querySelector(":scope > .global-nav-menu")',
            "if (group) item.append(this.#buildMenu(group))",
        ):
            if token not in module_text:
                errors.append(f"global navigation missing per-group lazy rendering contract: {token}")
        for obsolete_timing in (
            "calc(var(--nav-order) * 45ms)",
            "setTimeout(() => this.#setExpanded(item, true), 40)",
        ):
            if obsolete_timing in module_text or obsolete_timing in shared_css:
                errors.append(f"global navigation retains obsolete delayed timing: {obsolete_timing}")

        expected_nav_covers = {
            "background", "architecture", "foundations", "faq",
            "endem-spec", "closure", "session", "evidence",
            "endem", "inspector", "format", "runner",
            "getting-started", "architecture-guide", "application-reference",
            "spec-reference", "endem-manual", "current-stage", "roadmap",
            "downloads",
        }
        nav_cover_asset = SOURCE_ROOT / "assets/nav-covers.svg"
        if not nav_cover_asset.exists():
            errors.append("missing assets/nav-covers.svg")
        else:
            cover_ids = set(re.findall(
                r'id="nav-cover-([^"]+)"', nav_cover_asset.read_text()
            ))
            if cover_ids != expected_nav_covers:
                errors.append("navigation cover sprite must define 20 unique project covers")
        configured_cover_entries = re.findall(r'\bcover:\s*([^,}\s]+)', navigation_text)
        configured_covers = set(configured_cover_entries)
        if len(configured_cover_entries) != 20 or configured_covers != expected_nav_covers:
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
            "label: 进展",
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
            "project-progress-summary\"",
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
            'src="../assets/images/secure-endem-producer.svg"',
            'width="1440" height="960"',
            'class="current-stage-panel"',
            'class="project-progress-section"',
            "include project-timeline.html timeline=timeline",
        ):
            if token not in current_stage_text:
                errors.append(f"current stage page missing contract: {token}")
        timeline_include_text = (SOURCE_ROOT / "_includes/project-timeline.html").read_text()
        for token in (
            "data-summary-rail-layout",
            'data-summary-layout="stacked"',
            "summary-rail-layout project-progress-layout",
            "summary-rail summary-rail--progress project-progress-summary",
            "summary-rail-main project-timeline-block",
        ):
            if token not in timeline_include_text:
                errors.append(f"project timeline must consume the shared summary rail: {token}")
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

    summary_rail_pages = {
        "architecture/decisions.html": (
            'aria-label="决策阅读概览"',
            'href="#current-decisions"',
            'href="#adoption-boundaries"',
            'href="#change-rules"',
        ),
    }
    for route, page_tokens in summary_rail_pages.items():
        page_text = source_path_for_route(route).read_text()
        for token in (
            "data-summary-rail-layout",
            'data-summary-layout="stacked"',
            'class="summary-rail summary-rail--article"',
            'class="summary-rail-main"',
            *page_tokens,
        ):
            if token not in page_text:
                errors.append(f"{route}: missing shared summary rail contract: {token}")

    image_contracts = {
        "assets/images/secure-endem-producer.svg": (20_000, 'src="../assets/images/secure-endem-producer.svg"'),
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
    style_text = style.read_text() if style.exists() else ""
    endem_source = SOURCE_ROOT / "endem" / "index.html"
    if not endem_source.exists():
        errors.append("missing Endem application page")
    else:
        endem_text = endem_source.read_text()
        if endem_text.count('class="tool-project-body"') != 1:
            errors.append("Endem application page must define one bounded sticky body")
        elif (
            endem_text.count('class="tool-status-panel"') != 1
            or endem_text.count('class="tool-project-main"') != 1
            or re.search(
                r'class="tool-project-body">\s*<section class="tool-status-panel".*?'
                r'<div class="tool-project-main">',
                endem_text,
                re.DOTALL,
            ) is None
        ):
            errors.append(
                "Endem application must separate its semantic status panel from the task-reading column"
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
        errors.append("expected one semantic availability panel")
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
        "invalid order": [
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
    terminology_adr_text = source_path_for_route(
        "architecture/adr-0037-terminology-simplification.html"
    ).read_text()
    for token in (
        "不同名称使用不同检查",
        "每个人类名称都是一个完整单词",
        "不把职责短语重新包装成名称",
        "普通英语单词已经按词首起音规则接受",
        "Noemion",
        "Endem",
    ):
        if token not in terminology_adr_text:
            errors.append(f"ADR-0037 missing consolidated terminology rule: {token}")
    getting_started_text = (SOURCE_ROOT / "docs" / "getting-started.md").read_text()
    for token in (
        "## 先把一句要求写完整",
        "## 沿一条责任链工作",
        "## “安全使用”必须逐层检查",
        "## 相邻系统继续负责什么",
        "## 按问题继续学习",
        "## 当前可以验证什么",
        "软件工程长期把程序员写的形式代码编译给机器",
        "这里的“编译”不是自然语言生成代码",
        "没有可安装编译器或组件",
        "最终发布版按独立 Profile 移除原始自然语言",
        "截至 2026-07-16",
        "NIST AI Agent Standards Initiative",
        "MCP 2025-11-25 的实验 Tasks",
        "官方 Tasks 扩展提案",
        "不具备线格式兼容性",
        "A2A 1.0",
        "外部任务显示",
        "Noemion 增加的是目标责任层",
        "后一步不能弥补前一步的失败",
        "当前主体、对象、动作、目的、范围和截止点",
        "覆盖不足返回 `undetermined`，观察故障返回 `fault`",
        "SLSA 1.2 制品验证",
        "GNU Guix 的 `guix challenge`",
        "项目已经发布架构说明、规范草案、实验性 Endem 字节格式和机器可读示例",
        "普通名称先确认是一个完整单词，再检查词首、职责和机器冲突",
        "两个自造名称仍需发行前的人类朗读、听写和职责匹配证据",
        "不会成为第二套命令、机器别名或语义权威",
    ):
        if token not in getting_started_text:
            errors.append(f"getting started guide missing task-oriented learning boundary: {token}")
    for obsolete_heading in (
        "## 从这里开始",
        "## 安全目标制品怎样检查",
        "## 先看一个 Agent 工作",
        "## 六个语义面",
        "## 四个对象分别回答什么",
        "## 计划中的命令入口",
        "## 这些名字怎样读",
        "## 接下来按问题继续",
        "## 当前状态",
    ):
        if obsolete_heading in getting_started_text:
            errors.append(f"getting started guide retains a duplicated topic inventory: {obsolete_heading}")
    developer_entry_contracts = {
        "index.html": (
            "从开发者案例开始",
            "每个人都应该能编译自己的意图",
            "提出目标的人应当能够检查自己的表达怎样被解释",
            "这里的“编译”是一条可复核的形成路径",
            "最终发布版移除原文",
            "没有可执行程序或安装包",
            "当前用 <code>endem</code> 组织计划中的公开动作",
            "当前还没有可执行程序",
        ),
        "docs/index.md": (
            "先按问题选择入口",
            "GNU-Manuals.html",
            "| 你现在要回答什么 | 先读 | 读完以后 |",
            "Noemion 解决什么问题，与 Agent 协议有什么区别",
            "某个工程问题由哪份条款约束",
            "引用和状态",
        ),
        "faq/index.html": (
            "开始之前",
            "现在可以安装或试用吗",
            "为什么人工智能时代需要 Noemion",
            "Noemion 是自然语言写代码工具吗",
            "第一次接触项目应该先读什么",
            "不必先记住全部项目术语",
            "Endem 是传统目标文件的新名字吗",
            "为什么当前使用一个命令命名空间",
            "供人工智能系统安全使用的目标制品，是否意味着文件本身已经获准执行",
            "最终发布版会移除原始自然语言",
            "producer 只消费已经具备精确语义授权绑定的输入",
            "它不替具名权威选择意义，也不授予动作权限",
            "NIST AI Agent Standards Initiative",
            "OpenAI Agent 编排说明",
            "GNU 对他人服务替代用户计算的分析",
            "名称何时适合正式发行",
            "计划中的首个可实现范围是什么",
        ),
        "specifications/index.html": (
            "怎样找到需要的规范",
            "不必先记住全部对象名",
            "规范草案",
            "权威源",
            "无组件实现",
            "按对象和工程问题进入",
            "实现者应以规范源与机器可读登记",
            "每类资料只回答一种问题",
            "哪些边界还不能从规范推出",
            "开始一次规范查询",
            "正式条款",
            "设计材料",
            "验证资料",
            "实现证据",
            "截至 2026-07-15",
            "声明不超过现有证据",
        ),
    }
    for relative_path, required_tokens in developer_entry_contracts.items():
        entry_text = source_path_for_route(relative_path).read_text()
        for token in required_tokens:
            if token not in entry_text:
                errors.append(f"{relative_path} missing developer-first entry boundary: {token}")
    obsolete_entry_phrases = {
        "index.html": (
            "项目名与工程名各自负责",
            "公开应用只有",
            "先证明最小纵向切片",
        ),
        "docs/getting-started.md": (
            "自然语言目标",
            "第一实现阶段只建设",
            "最小纵向切片",
        ),
        "faq/index.html": (
            "某某 OBJ",
            "23 个独立用户",
            "为什么只保留一个 CLI",
            "只有 producer 能依据确定性规则或具名语义决定形成规范字节",
        ),
        "specifications/index.html": (
            '<span class="badge">END-CORE</span>',
            '<span class="badge">AUT-CORE</span>',
        ),
    }
    for relative_path, forbidden_phrases in obsolete_entry_phrases.items():
        entry_text = source_path_for_route(relative_path).read_text()
        for phrase in forbidden_phrases:
            if phrase in entry_text:
                errors.append(f"{relative_path} retains implementation-first entry phrase: {phrase}")
    for relative_path in (
        "index.html",
        "about/index.html",
        "faq/index.html",
        "docs/getting-started.md",
        "specifications/index.html",
        "_data/navigation.yml",
        "assets/images/noemion-verifiable-goal-field.svg",
        "spec/gnu-elf-applicability-proposal.md",
        "spec/planning-and-replanning-proposal.md",
    ):
        if "自然语言目标" in source_path_for_route(relative_path).read_text():
            errors.append(
                f"{relative_path} must distinguish the human natural-language expression "
                "from the resulting goal artifact"
            )
    architecture_guide_text = (SOURCE_ROOT / "docs" / "architecture-guide.md").read_text()
    for token in (
        "用一次 Agent 工作读图",
        "MCP/A2A 状态保留外部来源",
        "`completed` 不直接映射为满足结果",
        "先形成 `met / unmet / undetermined / fault`",
        "看到终态后按主张强度继续核对",
        "本次动作是否造成变化？",
        "会话开始前已经使用目标版本",
        "状态变化与因果归因边界研究提案",
        "Agent 系统边界图",
        "委托另一个 Agent 时保留身份与上限",
        "请求主体",
        "实际行动者",
        "被代表主体",
        "能力与预算",
        "下游完成仍只是候选运行事实",
        "权威与授权决定规范",
        "跨会话继续时先分清保存对象",
        "选择一种对话状态策略",
        "跨运行记忆",
        "恢复必须重新验证",
        "记忆、检查点与恢复边界研究提案",
    ):
        if token not in architecture_guide_text:
            errors.append(f"architecture guide missing developer walkthrough: {token}")
    for obsolete_heading in (
        "## 最小系统图",
        "## 委托另一个 Agent 时保留身份与上限",
        "## 跨会话继续时先分清保存对象",
        "## 形成与语义确认",
        "## 组合与发布",
        "## 装载与运行",
        "## 信任不是单一分数",
    ):
        if obsolete_heading in architecture_guide_text:
            errors.append(
                "architecture guide retains a duplicated implementation or research section: "
                + obsolete_heading
            )
    specifications_reference_text = (
        SOURCE_ROOT / "specifications" / "index.html"
    ).read_text()
    for token in (
        "先写下你要判断的事实",
        "用一个外部“已完成”状态走完整条查询链",
        "每份规范继续只约束自己的责任",
        "completed</code> 只说明外部请求走到了某个执行状态",
        "网页、工具返回、历史、摘要或附件进入模型时",
        "自称 <code>system</code> 或 <code>admin</code>",
        "研究资料不能作为现行字段、命令、状态或互操作接口的依据",
        "向量通过也只说明已登记案例与草案一致",
        "按什么顺序判断资料的权威性",
        "机器可读登记",
    ):
        if token not in specifications_reference_text:
            errors.append(f"specifications reference missing task lookup boundary: {token}")
    endem_reference_text = (SOURCE_ROOT / "endem" / "docs" / "reference.md").read_text()
    for token in (
        "从开发者要完成的工作出发",
        "三个能够分别失败、分别验证的实现边界",
        "这些字节在精确规则和预算下怎样显示、哪里不同或为何停止",
    ):
        if token not in endem_reference_text:
            errors.append(f"Endem application reference missing precise formation wording: {token}")
    if "来源绑定、规范化、确定性写入" in endem_reference_text:
        errors.append("Endem application reference retains undefined normalization wording")
    terminology_guide_text = (SOURCE_ROOT / "architecture" / "adr-0037-terminology-simplification.md").read_text()
    for token in (
        "项目名 `Noemion` 和核心制品名 `Endem`",
        "其余没有独立品牌职责的对象、角色和动作使用直白名称",
        "普通职责词也不能只因为“看起来熟悉”就采用",
        "普通英语词",
        "词首是否能按通常英语自然起音",
        "不把职责短语重新包装成名称",
        "当前名称与职责",
        "仍须在首次发行前完成真实人类朗读、听写和职责匹配测试",
    ):
        if token not in terminology_guide_text:
            errors.append(f"terminology decision missing current-name boundary: {token}")
    name_maturity_contracts = {
        "about/index.html": (
            "现行设计名称是 Endem",
            "这些普通英语字段已经按词首、职责和关键字语料接受",
        ),
        "specifications/index.html": (
            "当前策略",
            "待定内容",
            "普通职责词已按词首、职责和关键字语料接受",
            "Noemion 与 Endem 两个自造名称仍需发行前的人类读音证据",
        ),
        "downloads/index.html": (
            "Endem 目前只是设计阶段名称",
            "术语简化决定",
        ),
    }
    for relative_path, required_tokens in name_maturity_contracts.items():
        contract_text = source_path_for_route(relative_path).read_text()
        for token in required_tokens:
            if token not in contract_text:
                errors.append(f"{relative_path} missing name-maturity boundary: {token}")
    for relative_path, forbidden in {
        "about/index.html": "已接受 Endem 词汇",
        "specifications/index.html": "名称、职责、六个语义面",
        "downloads/index.html": "Endem 已通过互联网",
        "specifications/index.html": "固定现行词汇",
    }.items():
        if forbidden in source_path_for_route(relative_path).read_text():
            errors.append(f"{relative_path} retains overclaimed name maturity: {forbidden}")
    directory_css = DIRECTORY_CSS.read_text()
    if ".skip-link" in directory_css:
        errors.append("directory.css must not retain styles for the removed skip-to-content entry")
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

    for internal_output in (
        "CONTRIBUTING.md",
        "content-quality-audit.md",
        "homepage-design.md",
        "sitewide-design-system.md",
        "spec/terminology-audit.json",
        "development/testing.html",
        "docs/development-guide.html",
        "design-system",
    ):
        if (ROOT / internal_output).exists():
            errors.append(f"built output must not publish internal maintenance source: {internal_output}")

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
        visible_text = content_visible_text(parser)
        for term in (
            "Noemion", "Endem", "closure", "contract", "evidence", "source_expression", "meaning_projection", "situation", "goal_direction",
            "satisfaction_criteria", "unresolved_meaning", "模型", "原始表达", "实际观察", "没有可执行程序",
        ):
            if term not in visible_text:
                errors.append(f"index.html: homepage must explain {term}")
        home_source = home.read_text()
        if '<section class="portal-thesis portal-reveal">' in home_source:
            errors.append(
                "index.html: first chapter must not animate its framed surface away from the cover"
            )
        if '<h1 id="portal-title"><span class="portal-title-brand">Noemion</span><strong><span>人工智能时代</span><span class="portal-title-foundation">每个人都应该能编译自己的意图</span></strong></h1>' not in home_source:
            errors.append("index.html: rendered portal must identify Noemion before Endem")
        if home_source.count('class="portal-chapter-title"') != len(HOME_HEADINGS):
            errors.append("index.html: every homepage chapter heading must use the shared symbolic title treatment")
        for token in (
            'class="portal-introduction-visual"',
            "data-progressive-image",
            "data-progressive-image-stage",
            "data-progressive-image-source",
            "noemion-verifiable-goal-field.svg",
            "noemion-verifiable-goal-field-base.jpg",
            "noemion-verifiable-goal-field-base-preview.avif",
            "noemion-verifiable-goal-field-base-preview.webp",
            "noemion-verifiable-goal-field-base-preview.jpg",
            "noemion-verifiable-goal-field-base-balanced.avif",
            "noemion-verifiable-goal-field-base-balanced.webp",
            "noemion-verifiable-goal-field-base-balanced.jpg",
            "noemion-verifiable-goal-field-base-detail.avif",
            "noemion-verifiable-goal-field-base-detail.webp",
            'class="portal-art-base"',
            'class="portal-art-motion"',
            'fetchpriority="high"',
            "人的自然语言表达经过六个语义面形成 Endem",
        ):
            if token not in home_source:
                errors.append(f"index.html: homepage animated brand visual missing {token}")
        home_style_path = ROOT / "assets" / "style.css"
        home_style = home_style_path.read_text() if home_style_path.exists() else ""
        for selector in (
            ".portal-introduction::after", ".portal-introduction-visual", ".portal-introduction-visual img",
            ".portal-art-preview", ".portal-art-stage", '.portal-art-stage[data-image-state="loading"]',
        ):
            if selector not in home_style:
                errors.append(f"style.css missing homepage visual selector {selector}")
        for token in (
            ".portal-introduction::before{",
            "text-decoration-style:solid;text-decoration-thickness:.06em",
            "--portal-cover-edge:var(--paper)",
            "--portal-cover-edge:#060f0d",
            "background:var(--portal-cover-bottom-gradient)",
            "background:linear-gradient(to bottom,var(--portal-cover-edge) 0 80%,var(--paper) 100%)!important",
            ".portal-introduction-visual::after{",
            ".portal-thesis{--portal-thesis-inline:clamp(20px,3.8vw,34px);grid-template-columns:1fr;min-height:0}",
            ".portal-thesis-title{padding:72px var(--portal-thesis-inline) 48px",
            ".portal-thesis-copy{padding:50px var(--portal-thesis-inline) 58px}",
            ".portal-thesis-copy p{width:min(100%,590px);margin-right:auto;margin-left:0}",
            ".portal-thesis{--portal-thesis-inline:var(--site-content-inline)}",
            'body[data-page-role="portal"] .portal-main>.portal-thesis{border-top:1px solid var(--portal-line)}',
            "--site-content-inline:clamp(14px,4vw,56px)",
            ':is(main,.summary-rail-main)>section{padding:44px var(--site-content-inline)}',
            '.manual-article{padding:0 var(--site-content-inline) 40px}',
            ".portal-thesis-copy p{text-wrap:wrap}",
            ".portal-thesis-copy .portal-lead{font-size:18px;line-height:1.65;font-weight:560;letter-spacing:-.01em}",
            "transition:opacity 420ms var(--ease)",
            "animation:portal-visual-enter 320ms 40ms var(--ease) both",
        ):
            if token not in home_style:
                errors.append(f"style.css missing homepage surface continuity contract: {token}")
        portal_art = ROOT / "assets/images/noemion-verifiable-goal-field.svg"
        if not portal_art.exists():
            errors.append("homepage animated brand visual is missing")
        else:
            portal_art_source = portal_art.read_text()
            for token in (
                'viewBox="0 0 1600 900"',
                "SIX SEMANTIC FACETS",
                "SOURCE", "MEANING", "SITUATION", "DIRECTION", "CRITERIA", "UNRESOLVED",
                "ENDEM", "EVIDENCE",
                "@keyframes route-flow", "@keyframes scan-pass",
                "@media(prefers-reduced-motion:reduce)",
            ):
                if token not in portal_art_source:
                    errors.append(f"homepage animated brand visual missing contract: {token}")
        progressive_image_contracts = {
            "noemion-verifiable-goal-field-base-preview.avif": 20_000,
            "noemion-verifiable-goal-field-base-preview.webp": 35_000,
            "noemion-verifiable-goal-field-base-preview.jpg": 60_000,
            "noemion-verifiable-goal-field-base-balanced.avif": 35_000,
            "noemion-verifiable-goal-field-base-balanced.webp": 55_000,
            "noemion-verifiable-goal-field-base-balanced.jpg": 100_000,
            "noemion-verifiable-goal-field-base-detail.avif": 85_000,
            "noemion-verifiable-goal-field-base-detail.webp": 110_000,
        }
        for filename, maximum_bytes in progressive_image_contracts.items():
            image_path = ROOT / "assets" / "images" / filename
            if not image_path.exists():
                errors.append(f"missing progressive homepage image: {filename}")
            elif image_path.stat().st_size > maximum_bytes:
                errors.append(f"progressive homepage image exceeds {maximum_bytes} bytes: {filename}")
        progressive_module = ROOT / "assets" / "modules" / "progressive-image.mjs"
        if not progressive_module.exists():
            errors.append("progressive homepage image controller is missing")
        else:
            progressive_source = progressive_module.read_text()
            for token in ("ProgressiveImageStage", "requestAnimationFrame", 'dataset.imageState = "loaded"'):
                if token not in progressive_source:
                    errors.append(f"progressive homepage image controller missing contract: {token}")

    about_index = ROOT / "about/index.html"
    if about_index.exists():
        parser = parse(about_index)
        if parser.h2_texts != ABOUT_INDEX_HEADINGS:
            errors.append(
                "about/index.html: project-purpose sequence must be "
                f"{ABOUT_INDEX_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in (
            "人工智能系统可以规划步骤和调用工具",
            "研究的不是自然语言生成代码",
            "形成版保存一项目标的来源",
            "最终发布版移除原文",
            "两种制品具有不同的精确身份",
            "它们也可以长期存储",
            "TASK_STATE_COMPLETED",
            "make 的 goal",
            "NIST AI Agent Standards Initiative",
            "当前没有编译器、CLI、解析器、协议适配器或运行时",
            "读音能否区分",
            "现有规范与示例只能说明已覆盖的设计关系",
        ):
            if term not in visible_text:
                errors.append(f"about/index.html: missing project-purpose boundary {term}")
        if (
            parser.page_role != "section"
            or parser.class_counts["flow"] != 1
            or parser.class_counts["table-wrap"] != 3
            or parser.class_counts["page-link"] != 3
            or parser.class_counts["status-item"] != 4
        ):
            errors.append(
                "about/index.html: must keep one formation flow, three boundary tables, "
                "three routed links, and four current-status items"
            )
        for obsolete_heading in (
            "一个新的软件边界", "项目定义哪些工程责任",
            "哪些责任由外部系统承担", "如何推进",
        ):
            if obsolete_heading in parser.h2_texts:
                errors.append(
                    "about/index.html: must not restore inventory-style heading "
                    f"{obsolete_heading!r}"
                )

    architecture_index = ROOT / "architecture/index.html"
    if architecture_index.exists():
        parser = parse(architecture_index)
        if parser.h2_texts != ARCHITECTURE_INDEX_HEADINGS:
            errors.append(
                "architecture/index.html: developer responsibility sequence must be "
                f"{ARCHITECTURE_INDEX_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in (
            "这一层回答什么",
            "必须停止的情况",
            "协议终态不能直接成为 met",
            "END-P2 是来源保留的形成与评审 Profile",
            "END-FMT 0.1.0-draft 是实验性物理容器",
            "一次会话的只读执行契约",
            "Noemion 与 Endem 两个自造名称尚缺发行前的人类读音证据",
            "MCP 2025-11-25 Tasks",
            "GNU readelf",
        ):
            if term not in visible_text:
                errors.append(
                    f"architecture/index.html: missing developer architecture boundary {term}"
                )
        if (
            parser.class_counts["flow"] != 1
            or parser.class_counts["table-wrap"] != 3
            or parser.class_counts["page-link"] != 7
        ):
            errors.append(
                "architecture/index.html: must keep one task flow, three scoped tables, "
                "and seven routed links"
            )
        for obsolete_heading in (
            "架构的直接结论", "系统关系", "三个组件",
            "制品与非制品", "信任边界", "继续阅读",
        ):
            if obsolete_heading in parser.h2_texts:
                errors.append(
                    "architecture/index.html: must not restore inventory-style heading "
                    f"{obsolete_heading!r}"
                )

    development_index = ROOT / "development/index.html"
    if development_index.exists():
        parser = parse(development_index)
        if parser.h2_texts != DEVELOPMENT_INDEX_HEADINGS:
            errors.append(
                "development/index.html: project progress sequence must be "
                f"{DEVELOPMENT_INDEX_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in (
            "Noemion 目前处于规范与架构设计阶段",
            "不表示编译器、检查工具、运行器或安装包已经存在",
            "自然语言语义抽取",
            "最终工具数量",
            "当前没有 producer、inspector、runner、可执行 CLI、软件包或生产互操作声明",
            "项目现在进展到哪里",
            "后续准备验证什么",
            "哪些问题尚无结论",
            "现在可以获得什么",
        ):
            if term not in visible_text:
                errors.append(
                    f"development/index.html: missing project progress boundary {term}"
                )
        if (
            parser.class_counts["status-item"] != 4
            or parser.class_counts["page-link"] != 4
        ):
            errors.append(
                "development/index.html: must keep four reader-facing status items and four routed links"
            )
        for obsolete_heading in (
            "开发原则", "实施与验证", "源代码与构建",
            "贡献与报告", "开发流程", "研究、知识产权与标准化",
        ):
            if obsolete_heading in parser.h2_texts:
                errors.append(
                    "development/index.html: must not restore generic lifecycle heading "
                    f"{obsolete_heading!r}"
                )

    foundations = ROOT / "about/intellectual-foundations.html"
    if foundations.exists():
        parser = parse(foundations)
        breadcrumb = normalize_visible_text("".join(parser.breadcrumb_text))
        breadcrumb_routes = resolved_routes(foundations, parser.breadcrumb_links)
        if (
            parser.page_role != "content"
            or parser.class_counts["breadcrumbs"] != 1
            or breadcrumb_routes != ["index.html", "about/index.html"]
            or not all(label in breadcrumb for label in ("项目", "项目与边界", "思想与方法基础"))
        ):
            errors.append("about/intellectual-foundations.html: invalid project / about / current breadcrumbs")
        if parser.h2_texts != INTELLECTUAL_FOUNDATIONS_HEADINGS:
            errors.append(
                "about/intellectual-foundations.html: reasoning sequence must be "
                f"{INTELLECTUAL_FOUNDATIONS_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in (
            "不得直接推出", "把思想转换成可验证问题", "六个语义面",
            "NIST AI Agent Standards Initiative", "读音",
            "事态", "目标方向", "structured_observation", "no_allowed_projection", "undetermined", "fault",
        ):
            if term not in visible_text:
                errors.append(f"about/intellectual-foundations.html: must preserve {term}")
        for obsolete_heading in (
            "核心思想与工程问题",
            "Endem 语义核与后续验证",
            "核心书目与资源状态",
            "哲学怎样进入工程设计",
            "按开发者问题选择思想工具",
            "当前规范怎样回答这些问题",
            "按工程问题继续研究",
            "思想进入规范前必须留下什么",
        ):
            if obsolete_heading in parser.h2_texts:
                errors.append(
                    "about/intellectual-foundations.html: must not restore "
                    f"inventory-style heading {obsolete_heading!r}"
                )

    adr_0011 = ROOT / "architecture/adr-0011-endem-container.html"
    if adr_0011.exists():
        parser = parse(adr_0011)
        if parser.h2_texts != ADR_0011_READING_HEADINGS:
            errors.append(
                "architecture/adr-0011-endem-container.html: developer reading sequence "
                f"must be {ADR_0011_READING_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0011_READING_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0011-endem-container.html: missing format reading "
                    f"boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0011-endem-container.html: must preserve five boundary "
                "tables, one ordered reading flow and four developer reading links"
            )

    adr_0013 = ROOT / "architecture/adr-0013-source-profile.html"
    if adr_0013.exists():
        parser = parse(adr_0013)
        if parser.h2_texts != ADR_0013_PROFILE_HEADINGS:
            errors.append(
                "architecture/adr-0013-source-profile.html: Profile reading sequence "
                f"must be {ADR_0013_PROFILE_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0013_PROFILE_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0013-source-profile.html: missing source-bearing "
                    f"Profile boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0013-source-profile.html: must preserve five "
                "boundary tables, one reading flow and four developer reading links"
            )

    adr_0014 = ROOT / "architecture/adr-0014-source-manifest.html"
    if adr_0014.exists():
        parser = parse(adr_0014)
        if parser.h2_texts != ADR_0014_SOURCE_HEADINGS:
            errors.append(
                "architecture/adr-0014-source-manifest.html: source reading sequence "
                f"must be {ADR_0014_SOURCE_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0014_SOURCE_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0014-source-manifest.html: missing source or "
                    f"authority boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0014-source-manifest.html: must preserve five "
                "boundary tables, one formation flow and four developer reading links"
            )

    adr_0015 = ROOT / "architecture/adr-0015-result-domains.html"
    if adr_0015.exists():
        parser = parse(adr_0015)
        if parser.h2_texts != ADR_0015_RESULT_HEADINGS:
            errors.append(
                "architecture/adr-0015-result-domains.html: result-domain reading sequence "
                f"must be {ADR_0015_RESULT_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0015_RESULT_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0015-result-domains.html: missing result-domain "
                    f"boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0015-result-domains.html: must preserve five "
                "boundary tables, one task flow and four developer reading links"
            )

    adr_0016 = ROOT / "architecture/adr-0016-time-evidence.html"
    if adr_0016.exists():
        parser = parse(adr_0016)
        if parser.h2_texts != ADR_0016_TIME_HEADINGS:
            errors.append(
                "architecture/adr-0016-time-evidence.html: time-evidence reading sequence "
                f"must be {ADR_0016_TIME_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0016_TIME_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0016-time-evidence.html: missing time, evidence, "
                    f"or naming boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0016-time-evidence.html: must preserve five "
                "boundary tables, one task flow and four developer reading links"
            )

    adr_0017 = ROOT / "architecture/adr-0017-negation-and-absence.html"
    if adr_0017.exists():
        parser = parse(adr_0017)
        if parser.h2_texts != ADR_0017_NEGATION_HEADINGS:
            errors.append(
                "architecture/adr-0017-negation-and-absence.html: negation reading sequence "
                f"must be {ADR_0017_NEGATION_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0017_NEGATION_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0017-negation-and-absence.html: missing negation, "
                    f"absence, or external-tool boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0017-negation-and-absence.html: must preserve five "
                "boundary tables, one task flow and four developer reading links"
            )

    adr_0018 = ROOT / "architecture/adr-0018-quantification-and-membership.html"
    if adr_0018.exists():
        parser = parse(adr_0018)
        if parser.h2_texts != ADR_0018_QUANTIFICATION_HEADINGS:
            errors.append(
                "architecture/adr-0018-quantification-and-membership.html: quantification "
                f"reading sequence must be {ADR_0018_QUANTIFICATION_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0018_QUANTIFICATION_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0018-quantification-and-membership.html: missing "
                    f"membership, counting, naming, or Agent-list boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0018-quantification-and-membership.html: must preserve "
                "five boundary tables, one task flow and four developer reading links"
            )

    adr_0019 = ROOT / "architecture/adr-0019-measurement-and-thresholds.html"
    if adr_0019.exists():
        parser = parse(adr_0019)
        if parser.h2_texts != ADR_0019_MEASUREMENT_HEADINGS:
            errors.append(
                "architecture/adr-0019-measurement-and-thresholds.html: measurement "
                f"reading sequence must be {ADR_0019_MEASUREMENT_HEADINGS}, got {parser.h2_texts}"
            )
        visible_text = content_visible_text(parser)
        for term in ADR_0019_MEASUREMENT_BOUNDARIES:
            if term not in visible_text:
                errors.append(
                    "architecture/adr-0019-measurement-and-thresholds.html: missing "
                    f"measurement, uncertainty, terminology, or tool boundary {term}"
                )
        if (
            parser.class_counts["table-wrap"] != 5
            or parser.class_counts["flow"] != 1
        ):
            errors.append(
                "architecture/adr-0019-measurement-and-thresholds.html: must preserve "
                "five boundary tables, one task flow and four developer reading links"
            )

    for row in route_rows:
        path = ROOT / row["route"]
        if not path.exists():
            continue
        parser = parse(path)
        source = path.read_text()
        actual_badges = re.findall(r'<span class="badge">([^<]+)</span>', source)
        generic_badges = [label for label in actual_badges if label in GENERIC_ENGLISH_BADGES]
        if generic_badges:
            errors.append(
                f"{row['route']}: replace generic English template badges with "
                f"reader-facing tasks, boundaries, or status: {generic_badges}"
            )
        if parser.page_role != ROLE_BY_KIND[row["kind"]]:
            errors.append(f"{row['route']}: page role does not match registry kind")
        route_head = row["route"].split("/", 1)[0]
        expected_module = (
            "project" if row["route"] == "index.html"
            else "project" if route_head == "pages"
            else "resources" if route_head in {"downloads", "news"}
            else "support" if route_head == "faq"
            else "architecture" if route_head == "spec"
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
            for name in HERO_SECTION_CLASSES
            if parser.class_counts[name]
        }
        if introduction_counts != {expected_introduction: 1}:
            errors.append(
                f"{row['route']}: expected one role-appropriate Hero Section "
                f"using {expected_introduction}, "
                f"got {introduction_counts}"
            )
        hero_match = re.search(
            rf'<header\b[^>]*class="[^"]*\b{re.escape(expected_introduction)}\b[^"]*"[^>]*>(.*?)</header>',
            source,
            re.DOTALL,
        )
        if hero_match is None:
            errors.append(
                f"{row['route']}: Hero Section must use a semantic header element"
            )
        else:
            hero_body = hero_match.group(1)
            hero_text = normalize_visible_text(HTML_TAG.sub(" ", hero_body))
            if len(re.findall(r"<h1\b", hero_body)) != 1:
                errors.append(f"{row['route']}: Hero Section must contain exactly one h1")
            if not re.search(r"<p\b[^>]*>.*?\S.*?</p>", hero_body, re.DOTALL):
                errors.append(f"{row['route']}: Hero Section must contain a non-empty lead")
            expected_status_class = (
                "portal-introduction-meta"
                if row["kind"] == "portal"
                else "badges"
            )
            if not re.search(
                rf'class="[^"]*\b{re.escape(expected_status_class)}\b[^"]*"',
                hero_body,
            ):
                errors.append(
                    f"{row['route']}: Hero Section must expose a real status group"
                )
            if not hero_text:
                errors.append(f"{row['route']}: Hero Section must contain visible orientation text")
        if parser.docs_layout:
            hero_position = source.find(f'class="{expected_introduction}')
            top_pagination_position = source.find('class="manual-nav manual-nav-top"')
            if (
                top_pagination_position >= 0
                and (hero_position < 0 or hero_position > top_pagination_position)
            ):
                errors.append(
                    f"{row['route']}: manual Hero Section must precede top pagination"
                )

    for route in NORMATIVE_ROUTES:
        path = ROOT / route
        if not path.exists():
            errors.append(f"missing normative page {route}")
            continue
        parser = parse(path)
        visible_text = content_visible_text(parser)
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
        status_sections = [
            section for section in parser.sections
            if "tool-status-panel" in section["classes"]
        ]
        status_texts = ["".join(section["text"]) for section in status_sections]
        contract_errors = validate_application_project_contract(
            parser.h2_texts,
            status_texts,
            parser.class_counts,
        )
        errors.extend(f"{row['route']}: {error}" for error in contract_errors)
        visible_text = content_visible_text(parser)
        for token in APPLICATION_TASK_BOUNDARIES:
            if token not in visible_text:
                errors.append(f"{row['route']}: missing task boundary {token}")
        if (
            parser.class_counts["tool-project-main"] != 1
            or parser.class_counts["tool-status-panel"] != 1
            or parser.class_counts["flow"] != 1
            or parser.class_counts["table-wrap"] != 4
            or parser.class_counts["tool-status-list"] != 1
            or parser.class_counts["tool-action-id"] != 5
            or parser.class_counts["page-link"] != 4
        ):
            errors.append(
                f"{row['route']}: must keep one semantic status panel, one task column, "
                "one responsibility flow, one availability list, four decision tables "
                "with stable action IDs, "
                "and four reading links"
            )
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

    page_directory_output = ROOT / "pages/index.html"
    if page_directory_output.exists():
        page_directory_output_text = page_directory_output.read_text()
        if 'aria-label="无单独说明"' in page_directory_output_text:
            errors.append("page directory must show a concrete summary for every route")
        if page_directory_output_text.count("data-page-directory-item") != len(registered):
            errors.append("page directory must render every registered route exactly once")

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
            "project-progress-summary\"",
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
    summary_layout_module = ROOT / "assets/modules/summary-rail-layout.mjs"
    layout_observer_module = ROOT / "assets/modules/layout-observer.mjs"
    navigation_data = ROOT / "assets/navigation-data.json"
    theme_script = ROOT / "assets/theme.js"
    directory_guard = ROOT / "assets/mobile-directory-guard.js"
    favicon = ROOT / "assets/favicon.svg"
    for path in (site_script, route_module, directory_module, summary_layout_module, layout_observer_module, navigation_data, directory_guard):
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
    rendered_descriptions = []
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
            else:
                rendered_descriptions.extend(description_matches)
            if og_url_matches != [expected_public_url]:
                errors.append(f"{rel}: Open Graph URL must exactly match its formal route")
        if RAW_AMP.search(text):
            errors.append(f"{rel}: contains an unescaped ampersand")
        if text.count('data-global-nav-item=') != 5:
            errors.append(f"{rel}: server-rendered primary navigation must expose five task links")
        no_script_match = re.search(r"<noscript>(.*?)</noscript>", text, re.DOTALL)
        if no_script_match is None or "/docs/index.html" not in no_script_match.group(1):
            errors.append(f"{rel}: no-script navigation must expose a reader-facing HTML directory")
        elif "/sitemap.md" in no_script_match.group(1):
            errors.append(f"{rel}: no-script navigation must not expose the Markdown route registry")
        if parser.directory_containers != 1:
            errors.append(f"{rel}: expected one data-directory nav")
        for section in parser.sections:
            section_text = normalize_visible_text("".join(section["text"]))
            if section["heading"] and len(section_text) < 24:
                errors.append(
                    f"{rel}: section {section['heading']!r} is too thin for public documentation"
                )
        if parser.skip_links != 0 or parser.main_targets != 1:
            errors.append(f"{rel}: unexpected skip link or missing unique main target")
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
    if len(rendered_descriptions) != len(set(rendered_descriptions)):
        errors.append("rendered page descriptions must be unique across formal routes")

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
        generated_markdown_routes = {
            route for route in registered
            if route.startswith("docs/")
            or route.startswith("endem/docs/")
            or route.startswith("spec/")
        }
        if not declared <= registered_set:
            errors.append("built navigation data contains links outside the formal route registry")
        missing_static = sorted((registered_set - generated_markdown_routes) - declared)
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
        for token in (
            'className: "global-nav-card-arrow"',
            'class: "global-nav-card-arrow-ring"',
            'class: "global-nav-card-arrow-progress"',
            'createElement("i", { text: "→" })',
        ):
            if token not in global_navigation_source:
                errors.append(f"global navigation missing right-arrow motion contract: {token}")
        if 'text: "↗"' in global_navigation_source:
            errors.append("global navigation cards must point right before interaction")
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
                ["about/index.html", "project"],
                ["about/intellectual-foundations.html", "project"],
                ["architecture/endem-lifecycle.html", "architecture"],
                ["architecture/decisions.html", "architecture"],
                ["architecture/agent-system-boundaries.html", "architecture"],
                ["specifications/endem.html", "architecture"],
                ["components/producer.html", "architecture"],
                ["components/inspector.html", "architecture"],
                ["components/runner.html", "architecture"],
                ["docs/getting-started.html", "docs"],
                ["downloads/index.html", "resources"],
                ["faq/index.html", "resources"],
                ["development/index.html", "development"],
                ["development/current-stage.html", "development"],
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
        "@property --spectrum-angle",
        "conic-gradient(from var(--spectrum-angle)",
        "@keyframes spectrum-trace{to{--spectrum-angle:360deg}}",
        "animation:spectrum-trace 4.8s linear infinite",
        "--portal-coral:#c43b1b",
        "--portal-coral:#ff805c",
        "--number-muted:#61766c",
        ':is(.table-wrap,pre):focus-visible{outline:3px solid var(--focus-ring);outline-offset:-3px}',
        ".portal-feature-row::before{padding:5px}",
        ".portal-chapter-title>span{min-width:0;text-align:center}",
        "transition-duration:550ms,160ms",
        ".portal-introduction-visual img",
        "aspect-ratio:16/9",
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
    if "spectrum-trace 4.8s linear 1 forwards" in style:
        errors.append("spectrum traces must loop instead of stopping after one cycle")
    if style.count("animation:spectrum-trace 4.8s linear infinite") != 2:
        errors.append("portal and page-link spectrum traces must both retain the looping contract")

    directory_style = (ROOT / "assets/directory.css").read_text()
    for token in (
        ".global-nav-card-arrow-progress",
        ".global-nav-card-arrow-ring{",
        "pointer-events:none;transform:rotate(-90deg)",
        "stroke-dasharray:100;stroke-dashoffset:100",
        "transition-duration:280ms,180ms",
        ".global-nav-card:hover .global-nav-card-copy{transform:translateX(4px)}",
        ".global-nav-card:hover .global-nav-card-arrow-progress{stroke-dashoffset:0;opacity:1}",
        ".global-nav-card:focus-visible .global-nav-card-arrow-progress{stroke-dashoffset:0;opacity:1}",
        "conic-gradient(from var(--spectrum-angle)",
        "animation:spectrum-trace 4.8s linear infinite",
    ):
        if token not in directory_style:
            errors.append(f"directory.css missing global navigation card motion contract: {token}")
    if "spectrum-trace 4.8s linear 1 forwards" in directory_style:
        errors.append("global navigation spectrum traces must loop instead of stopping after one cycle")
    if directory_style.count("animation:spectrum-trace 4.8s linear infinite") != 3:
        errors.append("current, focused and hovered navigation spectrum traces must all loop")
    for forbidden in (
        ".global-nav-item.is-menu-open .global-nav-card:hover{transform:translateX(4px)}",
        ".global-nav-item:focus-within .global-nav-card:hover{transform:translateX(4px)}",
        ".global-nav-item.is-menu-open .global-nav-card[aria-current=\"page\"]{transform:translateX(4px)}",
    ):
        if forbidden in directory_style:
            errors.append("global navigation card outer frame must not move horizontally")

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
