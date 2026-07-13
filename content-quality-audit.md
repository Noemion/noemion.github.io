# Noemion 内容、系统闭环与路由审计

状态：Noemion 项目层与 Endem 工程词汇分层后的权威审计基线
范围：`sitemap.md` 登记的全部正式 HTML 路由

## 结论边界

Noemion 已经接受以 Endem 为核心制品的工程词汇、单一应用拓扑和 END-FMT 实验性编码，但尚未进入组件代码开发阶段。当前没有 Poiet、Theor、Praxor、`endem` CLI、安全核心、安装包或实现 CI；Python 检查器只核对规范、登记和向量之间的一致性。Endem 当前仍是中等风险的候选名：精确包名未登记，但 GitHub 已存在第三方同名对象，正式商标和法律门禁尚未完成。页面与资料测试存在不等于软件已经实现，也不证明性能、研究结论、知识产权或标准化状态。

## 审计问题

每条路由按自身角色回答以下问题，不用同一模板衡量门户、规范、应用与手册：

1. 读者进入页面要解决什么问题，首屏是否给出直接结论？
2. 该页面、组件、制品或子命令是否有独立消费者、权威、权限、生命周期或失败责任？
3. 输入由谁产生，输出由谁消费；若没有消费者，是否应删除或合并？
4. 来源忠实、结构有效、语义有效、闭包完整、签名真实、环境授权、证据充分和任务满足是否分别判断？
5. 候选、开放问题、已接受决定和实现证据是否明确分开？
6. 链接、目录、上下页、移动布局、键盘操作和正文宽度是否可用？

## 当前领域闭环

```text
来源表达 ─ poie ─► Endem ─ pleko ─► Synem ─ praxe ─► Dromen ─► phain / Tekmor ─► 最终决定
                         │                 │
                         └──── theor ──────┘
```

### 正式名词

| 名词 | 存在价值 | 生产者 | 消费者 | 省略条件 |
| --- | --- | --- | --- | --- |
| Endem | 保存一个根期望终态及 rhem/semion/skena/telis/krin/apor | Poiet 的 `poie` | elenk、theor、pleko、注册表与人工审查 | 不可省略；它是最小原语 |
| Synem | 固定多 Endem 引用、依赖、冲突结论与发布范围 | Poiet 的 `pleko/tasse/sphra` | Praxor、部署与审计 | 单一自包含 Endem 或没有组合消费者时省略 |
| Dromen | 封存一次 Praxe 会话的精确主体、政策、环境、能力、预算和证据责任 | Praxor 的 `praxe` | Praxor 控制面、最小能力域与实现后端 | 不作为磁盘制品、凭据包或可恢复权限 |
| Tekmor | 把事件、观察、证据范围、环境、策略与决定绑定 | Praxor 与具名决定权威 | 用户、CI、审计与离线评估 | 只有权威或保密边界确实不同时才拆伴随记录 |

调试伴随记录与外部签名请求、响应可以独立，因为它们具有不同的访问控制和权威。临时诊断、绑定映射、覆盖记录、追踪与运行报告默认只是类型化记录，不为流程对称单独造格式。

### 三个实现域

| 实现域 | 不可替代边界 | 禁止合并的内容 |
| --- | --- | --- |
| Poiet | 唯一规范写入器、生产读取器、来源绑定、elenk、pleko、tasse 与签名请求核对 | 模型不得写规范字节；Poiet 不持有私钥或实时能力 |
| Theor | 独立解析任意不可信字节，为差分和安全审查提供第二条证据链 | 不复用生产读取器，不产生生产验证句柄，不修复输入 |
| Praxor | 重新验证实际 Synem，建立 Dromen，控制能力与反馈，形成 Tekmor | 模型不持有句柄、不扩大权限、不自我验收 |

一个公开 CLI `endem` 只统一用户入口，不统一上述信任域。

## 应用存在性审计

| 子命令 | 独立消费者 | 失败责任 | 当前阶段 |
| --- | --- | --- | --- |
| poie | 作者、CI、pleko | 未授权语义、类型或约束、布局、非确定性 | 第 1 阶段 |
| elenk | Poiet、Praxor、发行流程 | 结构、引用、语义、资源、完整性 | 第 1 阶段 |
| theor | 开发者、安全审查、差分 CI | 畸形输入、未知关键结构、资源超限 | 第 1 阶段，独立实现 |
| peira | 规范与发布评审 | 条款、向量、实现差异与复现失败 | 第 1 阶段 |
| pleko | 多 Endem 消费者 | 引用、版本、冲突、权限与闭包 | 第 2 阶段，有真实案例才实现 |
| tasse | 发行流程 | 裁剪等价、发布范围、调试伴随记录 | 第 3 阶段 |
| sphra | 外部签名系统与发行流程 | 请求、响应或主体不匹配 | 第 3 阶段 |
| praxe | 用户、CI、审计 | 装载、能力、预算、漂移、证据与升级 | 第 4 阶段，独立进程 |

通用 transform、archive、strip、符号程序、预算程序、数据程序、训练程序、评估程序和量化程序不再作为独立应用承诺。相应职责进入有语义约束的子命令、测试模块或外部成熟工具适配器。

## 内容与成熟度规则

- “已接受”只能用于 ADR 已冻结的术语、边界和不变量。
- “待验证设计”用于尚无实现或实验的机制；“尚待确定”用于没有唯一候选；“后续计划”不得承诺日期。
- 历史术语只允许出现在被替代的 ADR 中；正文、路由、导航、样式 ID 与测试都使用当前词汇。
- Noemion 始终承担项目、新领域与社区总名；Endem 只承担最小制品、对应规范、生命周期、应用和 CLI 职责，不得替代项目名。
- 哲学来源只提出问题和反例；工程正文使用 Endem 与直白动作，不让来源术语决定 ABI。
- 所有对象输入、模型输出、远端协议描述和工具返回均视为不可信。

## 路由质量基线

- `sitemap.md` 是正式路由注册表；测试不得把某个固定数量当作产品不变量。
- 当前稳定家族为门户、about、architecture、specifications、components、endem、docs、development、downloads、faq 与 news。
- 旧应用和旧制品路由没有重定向、别名或隐藏导航入口。
- 每条手册路由由 `_data/manuals.yml` 登记，并由共享布局生成目录、面包屑和上下页。
- 源码测试和 `_site` 成品测试都必须通过；外链状态与内部链接状态分别报告。

## 公共页面结构审计 · 2026-07-12

以下 44 个 HTML 源文件已逐个阅读；检查范围包括页面职责、现行术语、历史标记、链接关系、共享布局、移动目录与可访问性。Markdown 生成的手册页面另由路由测试和构建产物审计覆盖。

| 文件 | 审计角色 | 结论 |
| --- | --- | --- |
| `_includes/docs-rail.html` | 服务端手册目录 | 通过 |
| `_includes/project-timeline.html` | 阶段时间线 | 通过 |
| `_includes/site-footer.html` | 全站页脚 | 通过 |
| `_includes/site-header.html` | 全站页头与目录容器 | 通过 |
| `_layouts/default.html` | 通用页面外壳 | 通过 |
| `_layouts/manual.html` | 手册页面外壳 | 通过 |
| `index.html` | 项目门户与六语义面总览 | 通过 |
| `about/index.html` | 项目背景入口 | 通过 |
| `about/background.html` | 问题与工程边界 | 通过 |
| `about/intellectual-foundations.html` | 哲学来源与采用界线 | 通过 |
| `architecture/index.html` | 架构总览 | 通过 |
| `architecture/endem-lifecycle.html` | Endem 生命周期 | 通过 |
| `architecture/decisions.html` | 决策权威顺序 | 通过 |
| `architecture/adr-0008-endem-system.html` | 已取代的历史决定 | 通过，显式标记 Superseded |
| `architecture/adr-0009-propositional-kernel.html` | 已取代的历史语义 | 通过，显式标记 Superseded |
| `architecture/adr-0010-native-lexicon.html` | 现行词汇与事态模型 | 通过 |
| `architecture/adr-0011-endem-container.html` | 实验性容器格式 | 通过 |
| `architecture/adr-0012-rust-core-language.html` | 安全核心语言选择 | 通过 |
| `architecture/adr-0013-end-p1-payload.html` | END-P1 封闭载荷 | 通过 |
| `architecture/adr-0014-source-manifest.html` | 首个 Poiet 来源清单 | 通过 |
| `architecture/adr-0015-result-domains.html` | 判断与运行结果分层 | 通过 |
| `architecture/adr-0016-mene-time-model.html` | mene 时间与连续性 | 通过 |
| `architecture/adr-0017-negation-and-absence.html` | 否定与缺席证据 | 通过 |
| `architecture/adr-0018-quantification-and-membership.html` | 量化范围与成员资格 | 通过 |
| `architecture/adr-0019-measurement-and-thresholds.html` | 测量与阈值契约 | 通过 |
| `architecture/adr-0020-composite-situations-and-criteria.html` | 复合事态与判据组合 | 通过 |
| `architecture/adr-0021-synem-closure-and-activation.html` | Synem 组合闭包与条件激活 | 通过 |
| `architecture/open-questions.html` | 未冻结问题 | 通过 |
| `specifications/index.html` | 规范入口 | 通过 |
| `specifications/endem.html` | 六语义面与最小制品 | 通过 |
| `specifications/synem.html` | 多 Endem 组合闭包 | 通过 |
| `specifications/tekmor.html` | phain 与有范围证据 | 通过 |
| `components/index.html` | 三实现域入口 | 通过 |
| `components/poiet.html` | 确定性生产域 | 通过 |
| `components/theor.html` | 独立只读解释域 | 通过 |
| `components/praxor.html` | 隔离实现域 | 通过 |
| `endem/index.html` | 唯一公开应用 | 通过 |
| `development/index.html` | 开发入口 | 通过 |
| `development/current-stage.html` | 当前阶段与证据要求 | 通过 |
| `development/implementation-roadmap.html` | 分阶段实施路线 | 通过 |
| `development/testing.html` | 验证体系 | 通过 |
| `downloads/index.html` | 真实可用性 | 通过 |
| `faq/index.html` | 关键概念答疑 | 通过 |
| `news/index.html` | 可核验进展 | 通过 |

## 全站逐页可读性复核 · 2026-07-13

本轮逐一复核 `sitemap.md` 登记的 57 条正式路由，包括 44 个 HTML 正文源和 13 个由 Markdown 生成的页面。复核重点不是统一文风，而是让每种页面先完成自己的读者任务：门户给出项目定义，目录给出选择依据，专题给出结论与边界，应用给出状态与输入输出，手册给出连续操作逻辑。

| 页面家族 | 已逐页复核的正式路由 | 本轮处理 |
| --- | --- | --- |
| 门户（1） | `/index.html` | 保持 Noemion 为项目主语；把控制平面和下一步入口改为无需内部术语即可理解的表达。 |
| 项目背景（3） | `/about/index.html`、`/about/background.html`、`/about/intellectual-foundations.html` | 把核心问题拆成形成、组合、实现、验收四步；集中加入《逻辑哲学论》五条短引文，并逐条说明工程启发与不采用部分。 |
| 架构与 ADR（22） | `/architecture/index.html`、`/architecture/endem-lifecycle.html`、`/architecture/decisions.html`、`/architecture/adr-0008-endem-system.html` 至 `/architecture/adr-0025-structured-diagnostics.html`、`/architecture/open-questions.html` | 生命周期先解释每阶段回答什么；历史 ADR 首屏标明怎样阅读和哪些名称已经失效；ADR-0011 至 0025 依次固定容器、候选语言、内容 Profile、来源清单、结果域、时间、否定、量化、测量、复合判断、Synem、Tekmor、内容分层、Dromen 与结构化诊断边界；开放问题只保留未冻结的物理格式和实施问题。 |
| 组件（4） | `/components/index.html`、`/components/poiet.html`、`/components/theor.html`、`/components/praxor.html` | 首段先解释三个组件为什么不能合并；把写入器、读取器、策略、句柄和请求等职责说清楚，只保留必要接口标识。 |
| 规范（6） | `/specifications/index.html`、`/specifications/endem.html`、`/specifications/synem.html`、`/specifications/dromen.html`、`/specifications/tekmor.html`、`/specifications/diagnostics.html` | 先给直白定义，再给规范词；诊断页面明确消息不是机器身份、外部错误不是本地结果、恢复不等于权限。 |
| 跨项目指南（7） | `/docs/index.html`、`/docs/getting-started.html`、`/docs/installation-and-usage.html`、`/docs/architecture-guide.html`、`/docs/development-guide.html`、`/docs/endem-reference.html`、`/docs/specifications-reference.html` | 删除未冻结却看似可执行的 `.weave` 命令示例；统一用中文解释候选、控制平面、验证句柄、签名材料和最终决定。 |
| Endem 应用与手册（7） | `/endem/index.html`、`/endem/docs/index.html`、`/endem/docs/format.html`、`/endem/docs/binding.html`、`/endem/docs/safety.html`、`/endem/docs/running.html`、`/endem/docs/reference.html` | 应用页先说明唯一入口解决什么问题；手册按来源、形成、组合、独立读取、发布和受控实现展开，移除未解释的 Rhem Source、Profile、Manifest 等表达。 |
| 开发（4） | `/development/index.html`、`/development/current-stage.html`、`/development/implementation-roadmap.html`、`/development/testing.html` | 阶段名称、验证条件和停止条件全部改为用户可读表达；当前只完善规范 Profile 与验证方案，不建立组件工作区。 |
| 资源与支持（3） | `/downloads/index.html`、`/faq/index.html`、`/news/index.html` | 下载页直说为什么不能发布；FAQ 拆开 Synem、Dromen、Tekmor 定义；项目动态只陈述可核对进展。 |

本轮同时加入自动回归规则：现行页面不得出现旧扩展名、旧来源名、旧口号或未解释的内部英文职责名；普通段落中的单句不得超过 70 个汉字；外部资料必须使用能说明内容的链接文字，不能把整段网址塞进正文。思想基础页还必须保留经核对的作者、译者、书名、命题编号、短引文和“不直接决定软件规范”的采用边界。

二次响应式复核发现：Endem 应用页在 1024px 平板视口隐藏了状态信息，却仍保留桌面双栏的最小宽度，造成正文右侧空列。现已把应用页单栏边界调整为 1218px，并加入样式契约检查；1217px 以下按 DOM 语义顺序显示“当前状态”，1218px 以上只有在约 800px 主栏与约 380px 信息栏都能完整容纳时才保留双栏。

本轮在 393×852、768×1024、1024×768 与 1440×900 视口复核首页和 Dromen 指南：页面均无横向溢出，Noemion 品牌与 TIMELINE 不重叠，移动端目录可以展开，没有坏图、偏离居中的独立图片或控制台错误。导航资料检查同时要求二十二个入口使用唯一封面，并为 Dromen 配置独立封面资源。

同一组视口已复核结构化诊断规范、ADR-0025 与规范入口：页面无整页横向溢出，表格只在自身容器内滚动，Noemion 与 TIMELINE 不重叠，移动目录显示 ADR-0025 和结构化诊断入口，独立图片没有偏离居中，控制台没有错误。

## 外部技术依据复核 · 2026-07-13

外部资料只支持具体机制，不进入 Noemion 的规范身份。任何适配都必须固定版本、保留原始输入身份，并在外部规范升级时重新验证。

| 权威资料 | 当前观察 | 采用的机制 | 明确排除 | 重新复核触发条件 |
| --- | --- | --- | --- | --- |
| ELF 对象格式与 GNU Binutils 2.46.1 | 最新发行是 2.46.1；GNU `readelf` 可不经 BFD 读取对象，BFD 的通用转换可能丢失格式特有信息 | 结构与装载分离、显式引用、格式专用的独立第二读取路径 | 机器地址、指令、弱符号默认选择、BFD 通用内部表示 | GNU 主次版本、ELF 格式或 Endem 物理编码变化 |
| MCP 2025-11-25 稳定规范 | 工具调用区分协议错误与工具执行错误，并要求输入校验、访问控制、超时和日志 | 版本化外缘适配、错误来源分离、最小能力、受众校验、拒绝和观察记录 | 服务器说明、工具 schema、OAuth 身份、`isError` 和远端结果都不能直接成为本地授权、满足或验收事实 | 出现正式新版本，或授权、传输、工具结构变化 |
| GNU GCC 诊断、SARIF 2.1.0 与 RFC 9457 | 同一失败可以拥有稳定规则身份、类型化位置、机器出口与人类解释；问题类型和具体发生应分开，错误响应可能泄密 | DIA-CORE 的机器码与消息分离、生产语境、位置、主错误、外部来源、最小披露与有界输出 | 不复制编译器严重度，不把 HTTP 状态、SARIF 或消息文本当作本地结果与权限 | 诊断物理编码、CLI/SARIF/MCP 映射或稳定 ABI 被提出时 |
| A2A 1.0 | Task、Message、Artifact、多协议绑定和主次版本协商服务跨系统交换；Agent Card 可以使用 JWS 签名 | 交换带来源的任务状态、消息和候选产物，核对声明发布者 | 不让补丁号进入协议协商；不让签名 Agent Card 自动成为语义权威；不让外部 Task/Artifact 成为 Endem 身份、生命周期或最终决定 | A2A 主次版本、任务状态机、安全对象或签名规则变化 |
| OpenTelemetry GenAI 语义约定 | 已迁入独立仓库，Schema URL 仍待确定；输入、输出、工具参数和结果可能含敏感信息 | 带版本、默认脱敏、可替换的运行观测导出器 | 外部字段进入 Endem 编码、Tekmor 身份或验收规则 | 首次稳定发布、Schema URL 或隐私建议变化 |
| W3C PROV、RFC 9334、SLSA 1.2 与 GNU Guix challenge | 溯源需要分开实体、活动和责任；证据、验证结果与依赖方决定是不同步骤；外部参数不可信；逐字节差异不能自行裁定哪份输出正确 | Tekmor 的有限无环溯源、外部有效性评估、相对 krin 的覆盖度和决定权威分离 | 签名、证据数量、构建证明、差异或模型评分自动成为事实、充分覆盖或最终接受 | TEK-CORE Profile、撤销分发、透明日志或跨生产者归并被提出时 |
| ELF 装载视图、Linux capabilities/no_new_privs/Landlock 与 MCP 会话授权 | 持久文件与动态运行表示不同；能力可以设置不可增长上界；任务与令牌必须绑定授权上下文和目标资源 | DRO-CORE 的一次会话主体、环境、能力交集、秘密外置、只读失效和销毁 | 把 Dromen 写成文件、进程映像或凭据包，或把 Linux 与协议名称当成隔离证明 | Praxor API、沙箱、凭据代理、预算计数器、事件编码或恢复机制被提出时 |
| RFC 3339 / RFC 9557、GNU 时间工具、W3C OWL-Time 与 OpenTelemetry Metrics | 绝对时刻、附加时区信息、单调经过时长、相对日期歧义、瞬间/区间/时长与遥测窗口分别有明确边界 | `fixed` UTC 半开区间、`elapsed` 具名事件与单调时钟、显式覆盖缺口、`strict/budgeted` 连续政策 | 默认本地时区、`now/tomorrow`、墙钟测量时长、离散采样冒充连续成立，或把外部时间类型直接写入 END-P1 | 时间 Profile、闰秒策略、跨重启关联、时区数据库封装或多生产者归并被提出时 |
| W3C OWL 2、SHACL、SPARQL 1.1、GNU grep 与 OpenTelemetry Logs | 开放世界中的未陈述不等于假；封闭约束、无匹配查询和无匹配文件都只对指定范围成立；日志区分发生时间与观察时间 | 同一关系的显式极性、空结果默认 `agno`、有限封闭范围与完整性责任 | 空日志、部分搜索、模型“未发现”或单条遥测记录成为普遍负事实 | 封闭声明 Profile、跨生产者完整性、迟到窗口、撤销传播或复合否定被提出时 |
| NIST AI RMF 与 GenAI Profile | AI RMF 1.0 正在修订；AIRC 继续把测试、评估、验证与确认作为风险管理资源 | 风险登记、具名责任、TEVV 和高风险模型/工具检查清单 | 风险框架定义 Endem 字段、合格阈值、ABI 或软件符合性 | AI RMF 修订版、GenAI Profile 或关键基础设施 Profile 正式更新 |
| NIST AI 800-2/800-3、OpenTelemetry Metrics、Prometheus 与 GNU Units | 评估目标必须先声明构念和用途；固定基准与推广 estimand 不同；指标流、窗口、分位数方法、单位与换算都会改变比较含义 | 构念、总体、程序、窗口、聚合器、单位、区间和阈值分别冻结；比较前不舍入 | 基准名、仪表盘、点估计、模型置信度或机器单位库自动成为满足依据 | NIST 草案定稿、统计模型登记、测量 Profile、复合单位或多生产者归并被提出时 |
| W3C SHACL、GNU Coreutils test、GNU Bash Lists 与 NIST AI 800-2 | 逻辑约束可以显式组合；不符合与检查错误必须分开；决定性条件可以短路；AI 评估标准应直接可观察 | 单根复合边界、all_of/any_of、四结果传播、决定依据和求值覆盖 | RDF Shape、shell 退出码、任意表达式或模型指令直接成为 Endem 判断语义 | 条件、排他析取、组合 Profile、物理字段或新的稳定 SHACL 版本被提出时 |
| OpenAI 智能体控制平面工程实践 | 强调清晰环境、可读工具、真实反馈与机械检查 | 仓库内规范、诊断、测试和反馈闭环 | 文章直接决定格式、组件、权限或成熟度 | 实现经验与本项目验证结果发生冲突 |

## 第 0 阶段规范证据审计 · 2026-07-13

此前公开页面能够解释规则，却缺少实现可逐条引用的规范源。当前已经建立以下仓库证据：

| 工作包 | 已形成证据 | 当前结论 | 剩余缺口 |
| --- | --- | --- | --- |
| P0-W1 权威规范 | 七份核心规范源、101 个唯一条款 ID、END-P0/END-P1 与 `spec/registry.json` | Endem、Synem、Dromen、Tekmor 与诊断边界分层登记；实现、线格式和证据状态独立 | 代码阶段前继续用真实自然语言案例与反例修订；独立实现验证等待用户开启代码阶段 |
| P0-W2 威胁与限制 | Endem、Synem、Dromen、Tekmor 与诊断威胁模型、`spec/diagnostic-catalog.md` 和 `spec/profiles/end-p0.json` | 已建立 50 类威胁、8 项 END-P0 有限上限和跨对象诊断目录 | 仍需边界规模、最坏复杂度和目标平台实验验证数值 |
| P0-W3 场景与规范向量 | 81 个非规范自然语言场景、7 个 Endem 语义 JSON 向量、七组各 12 个专题向量、20 个 Dromen、18 个 Tekmor、20 个诊断向量、6 个 END-P0 与 14 个 END-P1 字节 | 场景覆盖语义、判断、组合、闭包、会话、证据和诊断边界；所有提案矩阵均执行允许与拒绝分类 | 场景和提案向量不是组件证据；仍缺未来物理编码、协议映射和平台证据 |
| P0-W4 语言研究 | C/Rust 历史原型、6 个规范向量、差分变异、Sanitizer、有限 fuzz 与重复构建记录 | ADR-0012 据此把 Rust 1.97.0 记为未来候选；这些材料不是组件实现，也不自动授权继续编码 | 代码阶段开启前重新审查是否保留及是否需要复现 |
| P1-W1 来源与安全核心 | 尚未开始；当前只有 2 个 END-SRCM 来源样例、14 个 END-P1 规范字节向量和未来验证条件 | 没有 Poiet、Elenk、Theor、CLI、实现级 fuzz 或跨平台构建证据 | 等待用户明确开启代码开发阶段并重新确认仓库与范围 |

`tests/spec_contract_test.py` 检查规范版本、条款唯一性、成熟度、威胁映射和向量登记；`tests/source_manifest_test.py` 把来源清单映射到语义接受向量；`tests/semantic_vector_test.py` 执行 JSON 语义外壳；各专题检查器执行结果域、时间、否定、量化、测量、复合、Synem、Dromen 和 Tekmor 提案矩阵；`tests/wire_vector_test.py` 读取 END-P0 结构字节；`tests/p1_payload_test.py` 确定性编码并解码 END-P1。它们证明当前公开规范资料与这些案例一致，不证明未来稳定发行没有其他缺陷。

## 重新审计条件

- 新增正式制品、子命令、进程或仓库。
- 冻结编码、ABI、扩展 registry 或签名 profile。
- 第一次发布 Endem Poiet、Theor、Praxor 或规范版本。
- 接入模型、MCP/A2A、远端能力或外部签名服务。
- 页面不再能明确区分候选、决定和证据，或路由开始为历史兼容而膨胀。
