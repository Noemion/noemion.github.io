# Noemion 内容、系统闭环与路由审计

状态：Noemion 项目层与 Endem 工程词汇分层后的权威审计基线
范围：`sitemap.md` 登记的全部正式 HTML 路由

## 结论边界

Noemion 已经接受以 Endem 为核心制品的职责、单一应用拓扑和 END-FMT 实验性编码，但尚未进入组件代码开发阶段。具体发行拼写与读音尚未通过人类验证；后续[发行术语去专名化研究提案](spec/release-terminology-simplification-proposal.md)又建议先证明专名必要性，并把 Endem 之外的现行对象称呼、信任角色和公开动作同直白职责候选比较。[语义面与观察词提案](spec/semantic-facet-terminology-proposal.md)进一步保留七项职责，却建议以直白字段名替换 `rhem/semion/skena/telis/krin/apor/phain` 进入验证。[生命周期与结果词提案](spec/lifecycle-and-result-terminology-proposal.md)又发现 `attested` 把外部签名和证明关系误写成内容状态，并把对象边界修正与 `nascent/coherent/agno/aseme/interrupted` 的发行名称验证分开。三项建议都尚未成为 ADR 或迁移决定。当前没有 Ktisor、Theor、Drasor、`endem` CLI、安全核心、安装包或实现 CI；Python 检查器只核对规范、登记和向量之间的一致性。Endem 当前仍是中等风险的候选名：精确包名未登记，但 GitHub 已存在第三方同名对象，正式商标、法律和口头区分门禁尚未完成。页面与资料测试存在不等于软件已经实现，也不证明性能、研究结论、知识产权、读音可用性或标准化状态。

[能力发现、协商与调用提案](spec/capability-discovery-and-negotiation-proposal.md)继续检查 Agent 运行边界。它把能力声明、协议协商、授权决定、Dromen 会话上限、即时可调用性与调用事实分开，拒绝让动态工具列表扩写旧会话，也拒绝让端点可达、scope、签名或一次成功调用变成长期权限、`met` 或 `accepted`。这仍是尚未进入规范的研究，不创建 `CAP-CORE`、能力制品、组件或新专名。

[软件 Agent 身份、委托与责任链提案](spec/software-agent-identity-and-accountability-boundaries-proposal.md)补齐“Agent 名称替代行动者”的审计缺口。它把模型、Agent 定义、部署、工作负载、运行实例、会话、凭据、主体委托和一次动作分开，拒绝让产品名、服务账户、SVID、单点登录或 Agent Card 同时承担认证、授权与责任。这仍是尚未进入规范的研究，不创建 Agent 身份 CORE、制品、目录、服务、组件或新专名。

[并行、推测执行与提交边界提案](spec/parallel-and-speculative-execution-proposal.md)继续补齐多 Agent 与并行工具调用的高风险缺口。它把分支准入、候选结果、提交选择、当前前提、已发生副作用和后验观察分开，要求所有分支共享同一 Dromen 上限，并拒绝让最快完成、模型评分、取消或外部 Task 状态越过授权与结果域。这仍是尚未进入规范的研究，不创建 `PAR-CORE`、事务制品、调度器、组件或新专名。

[模型、适配器与能力域隔离提案](spec/model-adapter-isolation-proposal.md)补齐部署责任无法审查的高风险缺口。它把模型输入、控制面、授权、凭据与实时句柄、协议适配、文件、网络、资源终止、观察和外部目标分开，拒绝让容器、seccomp、超时或提示词名称冒充完整隔离证据，也拒绝把原始凭据交给模型。这仍是尚未进入规范的研究，不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、部署对象、组件或新专名。

[模型参与评测与裁判边界提案](spec/model-assisted-evaluation-proposal.md)补齐模型评分与人工智能基准的证据缺口。它把评测目的、构念、可观察标准、题目与候选、协议、模型调用、原始输出、统计汇总和使用决定分开，并要求位置、冗长、格式、来源、注入、相关评审者与漂移反例。模型评审输出继续是 `model-candidate`；多个模型投票、排行榜和自报置信度不能成为独立证据、统计区间、`met` 或 `accepted`。这仍是尚未进入规范的研究，不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品、裁判服务、组件或新专名。

[模型训练与更新边界提案](spec/model-training-and-update-boundaries-proposal.md)补齐训练数据、反馈、微调、适配权重、派生模型、复现、发布和回滚之间的责任缺口。它拒绝把会话记忆写成模型学习，也拒绝让用户点击、模型裁判、训练完成、固定种子、相同环境或回滚指针直接成为数据资格、权重复现、用途适合、`met` 或 `accepted`。这仍是尚未进入规范的研究，只使用直白职责短语，不创建 `TRAIN-CORE`、`MODEL-CORE`、`FEEDBACK-CORE`、模型制品、训练平台、组件或新专名。

[模型开放性与软件自由边界提案](spec/model-openness-and-software-freedom-boundaries-proposal.md)补齐托管 API、开放权重、源码可见、开源软件、自由软件、Open Source AI、发布完整性与可复现模型之间的术语缺口。它依据 GNU 四项自由、OSI Open Source AI Definition 1.0、Linux Foundation Model Openness Framework 与 NIST 供应链资料，要求逐项列出参数、代码、数据说明、数据、文档、许可和首选修改形式。Apache-2.0、模型卡、SBOM、签名和外部开放等级都不能替代对象清单或互相升级。这仍是尚未进入规范的研究，不创建 `OPEN-MODEL-CORE`、`LICENSE-CORE`、模型发行格式、合规服务、组件或新专名。

[托管人工智能服务与用户控制边界提案](spec/hosted-ai-service-and-user-control-boundaries-proposal.md)补齐软件权利、实际执行控制、数据控制和服务可移植性之间的运行关系缺口。它分开第三方托管、自主管理、设备内执行和通信服务，并逐项检查执行者、隐藏变换、数据外发、保留、下游服务、状态、导出、切换、停服、观察和复现。GNU 的服务批评与 AGPL、MCP 的控制拓扑、NIST 供应链审查和供应商数据控制都不能单独证明用户控制服务实例。这仍是尚未进入规范的研究，不创建服务 CORE、网关、云平台、导出格式、组件或新专名。

## 审计问题

每条路由按自身角色回答以下问题，不用同一模板衡量门户、规范、应用与手册：

1. 读者进入页面要解决什么问题，首屏是否给出直接结论？
2. 该页面、组件、制品或子命令是否有独立消费者、权威、权限、生命周期或失败责任？
3. 输入由谁产生，输出由谁消费；若没有消费者，是否应删除或合并？
4. 来源忠实、结构有效、语义有效、闭包完整、签名真实、环境授权、证据充分和任务满足是否分别判断？
5. 候选、开放问题、已接受决定和实现证据是否明确分开？
6. 链接、目录、上下页、移动布局、键盘操作和正文宽度是否可用？
7. 页面是否把术语职责已接受、设计阶段拼写和发行名称通过错误合并？
8. 专名是否具有普通技术术语无法承担的独立对象、真实消费者和失败责任；若没有，是否应改用直白职责名？
9. 页面说“开放”“开源”“自由”或“可复现”时，是否给出对象、定义版本、许可证、限制和证据范围？
10. 页面说“本地”“私有”“云”“主权”或“可移植”时，是否明确实际执行者、控制平面、数据路径、未知范围和退出条件？

## 当前领域闭环

```text
来源表达 ─ ktise ─► Endem ─ pleko ─► Synem ─ drase ─► Dromen ─► phain / Iknem ─► 最终决定
                         │                 │
                         └──── theor ──────┘
```

### 正式名词

| 名词 | 存在价值 | 生产者 | 消费者 | 省略条件 |
| --- | --- | --- | --- | --- |
| Endem | 保存一个根期望终态及 rhem/semion/skena/telis/krin/apor | Ktisor 的 `ktise` | elenk、theor、pleko、注册表与人工审查 | 不可省略；它是最小原语 |
| Synem | 固定多 Endem 引用、依赖、冲突结论与发布范围 | Ktisor 的 `pleko` | Drasor、外部发布系统与审计 | 单一自包含 Endem 或没有组合消费者时省略 |
| Dromen | 封存一次 Drase 会话的精确主体、政策、环境、能力、预算和证据责任 | Drasor 的 `drase` | Drasor 控制面、最小能力域与实现后端 | 不作为磁盘制品、凭据包或可恢复权限 |
| Iknem | 把事件、观察、证据范围、环境、策略与决定绑定 | Drasor 与具名决定权威 | 用户、CI、审计与离线评估 | 只有权威或保密边界确实不同时才拆伴随记录 |

调试伴随记录与外部签名请求、响应可以独立，因为它们具有不同的访问控制和权威。临时诊断、绑定映射、覆盖记录、追踪与运行报告默认只是类型化记录，不为流程对称单独造格式。

### 三个实现域

| 实现域 | 不可替代边界 | 禁止合并的内容 |
| --- | --- | --- |
| Ktisor | Endem/Synem 的唯一规范字节生产边界、制品形成侧读取器、来源绑定、elenk 与 pleko | 模型不得写规范字节；Ktisor 不接收外部签名响应，也不持有私钥或实时能力 |
| Theor | 独立读取已有物理格式的实际不可信字节，为差分和安全审查提供第二条解释路径 | 不复用形成侧读取器，不产生生产检查通过结论，不修复输入；未定义物理格式的对象不猜测字段 |
| Drasor | 重新验证实际 Synem，建立 Dromen，控制能力与反馈，形成 Iknem | 模型不持有句柄、不扩大权限、不自我验收 |

一个公开 CLI `endem` 只统一用户入口，不统一上述信任域。

## 应用存在性审计

| 子命令 | 独立消费者 | 失败责任 | 当前阶段 |
| --- | --- | --- | --- |
| ktise | 作者、CI、pleko | 未授权语义、类型或约束、布局、非确定性 | 第 1 阶段 |
| elenk | Ktisor、Drasor、发行流程 | 结构、引用、语义、资源、完整性 | 第 1 阶段 |
| theor | 开发者、安全审查、差分 CI | 畸形输入、未知关键结构、资源超限 | 第 1 阶段，独立实现 |
| 发布前验证 | 规范与发布评审 | 条款、向量、实现差异与复现失败 | 验证责任，不是公开动作 |
| pleko | 多 Endem 消费者 | 引用、版本、冲突、权限与闭包 | 第 2 阶段，有真实案例才实现 |
| 派生制品责任 | 对应制品生产者 | 版本化保留关系、发布范围、调试伴随记录；当前不能证明时保留或失败 | 有真实裁剪消费者和正反向量才实现 |
| 外部签名集成 | 外部签名系统与发行流程 | 请求、响应或主体不匹配 | 包络 Profile 与真实消费者冻结后 |
| drase | 用户、CI、审计 | 装载、能力、预算、漂移、证据与升级 | 第 4 阶段，独立进程 |

通用 transform、archive、strip、符号程序、预算程序、数据程序、训练程序、评估程序和量化程序不再作为独立应用承诺。相应职责进入有语义约束的子命令、测试模块或外部成熟工具适配器。

## 内容与成熟度规则

- “已接受”只能用于 ADR 已冻结的职责、边界、不变量或门禁方法；在 ADR-0034 完成人类证据前，不能用于具体发行拼写或读音。
- 专名先证明必要性，再接受冲突与读音审查；Endem closure、session contract、scoped evidence record、deterministic producer、independent inspector、bounded runner 与 `form/check/compose/inspect/run` 当前都只是人类验证候选，不得写入现行规范、CLI、别名或重定向。
- “待验证设计”用于尚无实现或实验的机制；“尚待确定”用于没有唯一候选；“后续计划”不得承诺日期。
- 历史术语只允许出现在被替代的 ADR 中；正文、路由、导航、样式 ID 与测试都使用当前词汇。
- Noemion 始终承担项目、新领域与社区总名；Endem 只承担最小制品、对应规范、生命周期、应用和 CLI 职责，不得替代项目名。
- 哲学来源只提出问题和反例；工程正文使用 Endem 与直白动作，不让来源术语决定 ABI。
- 新造的工具、组件、制品、动作和关键术语不使用数字；ADR、条款、Profile、协议版本和向量编号仅作为精确引用，不能替代读者可理解的职责名称。
- 所有对象输入、模型输出、远端协议描述和工具返回均视为不可信。

## 路由质量基线

- `sitemap.md` 是正式路由注册表；测试不得把某个固定数量当作产品不变量。
- 当前稳定家族为门户、about、architecture、specifications、components、endem、docs、development、downloads、faq 与 news。
- 旧应用和旧制品路由没有重定向、别名或隐藏导航入口。
- 每条手册路由由 `_data/manuals.yml` 登记，并由共享布局生成目录、面包屑和上下页。
- 源码测试和 `_site` 成品测试都必须通过；外链状态与内部链接状态分别报告。

## 公共页面结构审计 · 2026-07-12

以下清单记录初次逐页审计，并在后续新增 ADR-0022 至 ADR-0036、Dromen、诊断、适配、精确身份、文本、授权、伴随关系、名称门禁、动作收敛和裁剪发布页面时继续按同一标准复核。当前共有 60 个 HTML 正文源；Markdown 生成页面另由路由测试和构建产物审计覆盖。

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
| `architecture/agent-system-boundaries.html` | Agent 运行事实与 Noemion 责任映射 | 通过，显式区分规范、研究与未来实现 |
| `architecture/adr-0008-endem-system.html` | 已取代的历史决定 | 通过，显式标记 Superseded |
| `architecture/adr-0009-propositional-kernel.html` | 已取代的历史语义 | 通过，显式标记 Superseded |
| `architecture/adr-0010-native-lexicon.html` | 现行词汇与事态模型 | 通过 |
| `architecture/adr-0011-endem-container.html` | 实验性容器格式 | 通过 |
| `architecture/adr-0012-rust-core-language.html` | 安全核心语言选择 | 通过 |
| `architecture/adr-0013-end-p1-payload.html` | END-P1 封闭载荷 | 通过 |
| `architecture/adr-0014-source-manifest.html` | 首个 Ktisor 来源清单 | 通过 |
| `architecture/adr-0015-result-domains.html` | 判断与运行结果分层 | 通过 |
| `architecture/adr-0016-mene-time-model.html` | mene 时间与连续性 | 通过 |
| `architecture/adr-0017-negation-and-absence.html` | 否定与缺席证据 | 通过 |
| `architecture/adr-0018-quantification-and-membership.html` | 量化范围与成员资格 | 通过 |
| `architecture/adr-0019-measurement-and-thresholds.html` | 测量与阈值契约 | 通过 |
| `architecture/adr-0020-composite-situations-and-criteria.html` | 复合事态与判据组合 | 通过 |
| `architecture/adr-0021-synem-closure-and-activation.html` | Synem 组合闭包与条件激活 | 通过 |
| `architecture/adr-0022-iknem-evidence-and-appraisal.html` | Iknem 证据与评估 | 通过 |
| `architecture/adr-0023-endem-content-standard.html` | Endem 内容标准分层 | 通过 |
| `architecture/adr-0024-dromen-session-contract.html` | Dromen 会话契约 | 通过 |
| `architecture/adr-0025-structured-diagnostics.html` | 结构化诊断边界 | 通过 |
| `architecture/adr-0026-external-protocol-adapters.html` | 外部协议适配边界 | 通过 |
| `architecture/adr-0027-exact-identity-and-attestation.html` | 精确内容身份与签名边界 | 通过 |
| `architecture/adr-0028-text-and-identifier-boundaries.html` | 文本与标识符边界 | 通过 |
| `architecture/adr-0029-authority-and-authorization-decisions.html` | 权威与授权决定边界 | 通过 |
| `architecture/adr-0030-endem-content-and-authorization-companions.html` | 内容与授权伴随关系 | 通过 |
| `architecture/adr-0031-release-name-collision-gate.html` | 发布名称冲突门禁 | 通过 |
| `architecture/adr-0032-deterministic-maker-name-collision.html` | 确定性制作名称冲突 | 通过 |
| `architecture/adr-0033-text-identifier-specification-name.html` | 文本与标识符标准命名 | 通过 |
| `architecture/adr-0034-pronunciation-and-oral-distinction.html` | 术语读音与口头区分门禁 | 通过 |
| `architecture/adr-0035-public-actions-and-internal-responsibilities.html` | 公开动作与内部职责收敛 | 通过 |
| `architecture/adr-0036-source-bearing-and-stripped-release.html` | 来源保留与裁剪发布边界 | 通过 |
| `architecture/open-questions.html` | 未冻结问题 | 通过 |
| `specifications/index.html` | 规范入口 | 通过 |
| `specifications/endem.html` | 六语义面与最小制品 | 通过 |
| `specifications/synem.html` | 多 Endem 组合闭包 | 通过 |
| `specifications/iknem.html` | phain 与有范围证据 | 通过 |
| `specifications/dromen.html` | 一次会话执行契约 | 通过 |
| `specifications/diagnostics.html` | 跨对象结构化诊断 | 通过 |
| `specifications/adapters.html` | 外部协议适配规则 | 通过 |
| `specifications/identity.html` | 精确内容身份与签名规则 | 通过 |
| `specifications/text-and-identifiers.html` | 文本与标识符边界规则 | 通过 |
| `specifications/authority.html` | 权威与授权决定规则 | 通过 |
| `components/index.html` | 三实现域入口 | 通过 |
| `components/ktisor.html` | 确定性生产域 | 通过 |
| `components/theor.html` | 独立只读解释域 | 通过 |
| `components/drasor.html` | 隔离实现域 | 通过 |
| `endem/index.html` | 唯一公开应用 | 通过 |
| `development/index.html` | 开发入口 | 通过 |
| `development/current-stage.html` | 当前阶段与证据要求 | 通过 |
| `development/implementation-roadmap.html` | 分阶段实施路线 | 通过 |
| `development/testing.html` | 验证体系 | 通过 |
| `downloads/index.html` | 真实可用性 | 通过，逐对象区分仓库许可、API、参数、代码、数据、开放主张与服务控制 |
| `faq/index.html` | 关键概念答疑 | 通过，明确开放权重、软件自由、托管执行与用户控制不是同一结论 |
| `news/index.html` | 可核验进展 | 通过 |

## 全站逐页可读性复核 · 2026-07-13

本轮逐一复核 `sitemap.md` 登记的 74 条正式路由，包括 60 个 HTML 正文源和 14 个由 Markdown 生成的页面。复核重点不是统一文风，而是让每种页面先完成自己的读者任务：门户给出项目定义，目录给出选择依据，专题给出结论与边界，应用给出状态与输入输出，手册给出连续操作逻辑。

| 页面家族 | 已逐页复核的正式路由 | 本轮处理 |
| --- | --- | --- |
| 门户（1） | `/index.html` | 保持 Noemion 为项目主语；把控制平面和下一步入口改为无需内部术语即可理解的表达。 |
| 项目背景（3） | `/about/index.html`、`/about/background.html`、`/about/intellectual-foundations.html` | 从依赖升级案例分开来源、协议任务、工具调用、授权、观察与满足判断；再按开发者问题说明工程责任、相邻层、思想启发、当前规范与采用限制。 |
| 架构与 ADR（34） | `/architecture/index.html`、`/architecture/endem-lifecycle.html`、`/architecture/decisions.html`、`/architecture/agent-system-boundaries.html`、`/architecture/adr-0008-endem-system.html` 至 `/architecture/adr-0036-source-bearing-and-stripped-release.html`、`/architecture/open-questions.html` | 生命周期解释每阶段回答什么；Agent 边界图把规范、研究和运行事实分层；历史 ADR 标明失效名称；现行 ADR 固定语义、格式、判断、信任、命名、口头区分、公开动作与裁剪发布边界。 |
| 组件（4） | `/components/index.html`、`/components/ktisor.html`、`/components/theor.html`、`/components/drasor.html` | 首段先解释三个组件为什么不能合并；把写入器、读取器、策略、句柄和请求等职责说清楚，只保留必要接口标识。 |
| 规范（10） | `/specifications/index.html`、`/specifications/endem.html`、`/specifications/synem.html`、`/specifications/dromen.html`、`/specifications/iknem.html`、`/specifications/diagnostics.html`、`/specifications/adapters.html`、`/specifications/identity.html`、`/specifications/text-and-identifiers.html`、`/specifications/authority.html` | 先给直白定义，再给规范词；授权页明确登录、签名、Agent 状态与点击都不能自行产生语义或最终决定权。 |
| 跨项目指南（8） | `/docs/index.html`、`/docs/getting-started.html`、`/docs/installation-and-usage.html`、`/docs/terminology-and-pronunciation.html`、`/docs/architecture-guide.html`、`/docs/development-guide.html`、`/docs/endem-reference.html`、`/docs/specifications-reference.html` | 删除尚未确定却看似可执行的命令示例；解释候选、控制平面、Ktisor 内部检查通过引用、签名材料和最终决定；新增真实人类读音证据、跨会话恢复、Agent 委托和模型上下文装配检查表。 |
| Endem 应用与手册（7） | `/endem/index.html`、`/endem/docs/index.html`、`/endem/docs/format.html`、`/endem/docs/binding.html`、`/endem/docs/safety.html`、`/endem/docs/running.html`、`/endem/docs/reference.html` | 应用页先说明唯一入口解决什么问题；手册按来源、形成、组合、独立读取、发布和受控实现展开，移除未解释的 Rhem Source、Profile、Manifest 等表达。 |
| 开发（4） | `/development/index.html`、`/development/current-stage.html`、`/development/implementation-roadmap.html`、`/development/testing.html` | 阶段名称、验证条件和停止条件全部改为用户可读表达；当前只完善规范 Profile 与验证方案，不建立组件工作区。 |
| 资源与支持（3） | `/downloads/index.html`、`/faq/index.html`、`/news/index.html` | 下载页直说为什么不能发布；FAQ 拆开 Synem、Dromen、Iknem 定义；项目动态只陈述可核对进展。 |

本轮同时加入自动回归规则：现行页面不得出现旧扩展名、旧来源名、旧口号或未解释的内部英文职责名；普通段落中的单句不得超过 70 个汉字；外部资料必须使用能说明内容的链接文字，不能把整段网址塞进正文。思想基础页还必须保留经核对的作者、译者、书名、命题编号、短引文和“不直接决定软件规范”的采用边界。

二次响应式复核发现：Endem 应用页在 1024px 平板视口隐藏了状态信息，却仍保留桌面双栏的最小宽度，造成正文右侧空列。现已把应用页单栏边界调整为 1218px，并加入样式契约检查；1217px 以下按 DOM 语义顺序显示“当前状态”，1218px 以上只有在约 800px 主栏与约 380px 信息栏都能完整容纳时才保留双栏。

本轮在 393×852、768×1024、1024×768 与 1440×900 视口复核首页和 Dromen 指南：页面均无横向溢出，Noemion 品牌与 TIMELINE 不重叠，移动端目录可以展开，没有坏图、偏离居中的独立图片或控制台错误。导航资料检查同时要求二十二个入口使用唯一封面，并为 Dromen 配置独立封面资源。

同一组视口已复核结构化诊断规范、ADR-0025 与规范入口：页面无整页横向溢出，表格只在自身容器内滚动，Noemion 与 TIMELINE 不重叠，移动目录显示 ADR-0025 和结构化诊断入口，独立图片没有偏离居中，控制台没有错误。

外部协议适配、精确身份、文本边界、权威授权、内容伴随规范及 ADR-0026 至 ADR-0034 与更新后的规范入口继续使用同一组视口验收；它们必须保持表格局部滚动、移动目录可达、标题自然换行和零控制台错误。

Agent 系统边界图在 393×852、1024×768 与 1440×900 视口完成单独复核。桌面普通正文保持 760px、18px 与约 1.78 行高；移动端正文按可读性规则降为 17px，五张宽表只在自身容器滚动。标题使用平衡换行，页面没有整页横向溢出或控制台错误。

首页与移动目录的回归复核进一步覆盖“滚动后再展开”场景：滚动锁不得把吸顶导航随页面负向位移，目录展开后必须仍位于当前视口。首页的项目级入口以 Noemion 为主语；第 03 节将 Endem、Synem、Dromen 与 Iknem 分成四张具有独立目标页和可见概念图的卡片。上述行为已在 393×852、768×1024、1024×768 与 1440×900 视口验证，均无整页横向溢出或控制台错误。

## 开发者学习路径复核 · 2026-07-14

正式页面已经基本清除内部授权、资料制作和验收过程话术，但入门指南此前仍从词源直接进入读音、六个字段、四个名词和五个动作。首次接触项目的开发者缺少一个能够贯穿目标、Agent 会话、外部任务、观察和最终决定的具体问题，术语表因此承担了本应由教程承担的解释责任。

本轮以“更新服务依赖并确认可以发布”为非规范示例，先展示开发者实际需要补齐的对象、范围、检查环境、判据和决定权威，再引出 Noemion 的职责。入门指南说明 MCP/A2A Task completed 只属于外部请求执行状态；架构指南沿同一案例逐步定位 Ktisor、Dromen、协议适配、Iknem、满足判断和最终决定。读音说明移到读者理解核心职责之后，仍保留真人验证边界。

[GNU 文档原则](https://www.gnu.org/prep/standards/html_node/Documentation.html)要求完整文档同时服务教程与参考用途；[MCP Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)和[A2A 1.0 规范](https://a2a-protocol.org/v1.0.0/specification/)则分别把外部请求执行状态、Task、消息与产物显式建模。这些来源支持“先用实际问题教学，再把协议状态放回来源域”的写法，但不定义 Noemion 字段或结果映射。

MCP 候选版的名称包含计划最终发布日期，容易被误读为已经正式发布。官方页面确认该候选版于 2026 年 5 月 21 日公开，最终版计划于 7 月 28 日发布；Agent 边界页因此同时显示公开日期、命名依据和“尚未成为正式版”，不再只写含糊的“发布候选”。

## 首次阅读入口复核 · 2026-07-15

入门指南已经使用实际 Agent 工作解释职责顺序，首页、指南目录、FAQ 和规范入口仍主要按项目名词与内部模块排列。首页先解释项目名和词源，再说明 Agent 完成状态为何不足；指南目录列出七类资料却没有让读者从问题直接进入；FAQ 还保留“某某 OBJ”和“23 个独立用户”这类依赖历史设计过程的句子。首次接触项目的开发者因此需要先理解内部分类，才能找到与自己的故障或任务相符的入口。

当前入口先回答三件事：Noemion 要阻止哪类错误、现在是否已有可运行软件、读者手上的问题应进入哪份资料。首页用“外部任务完成不等于目标满足”建立问题，再引出 Endem；指南目录按安装、协议状态、命名、架构、修改证据、命令职责和规范条款组织入口；FAQ 把历史命名辩护改成开发者会实际提出的问题；规范入口减少 CORE 缩写堆叠，从协议、签名、文本、权限和证据问题进入权威源。

[GNU Coding Standards 的手册结构原则](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)明确建议围绕使用者心中的概念和问题组织资料，不照搬程序结构，也不把手册写成功能清单。这一原则只支持教程与参考的组织方式，不定义 Noemion 的对象、字段或符合性要求。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把互操作、安全、身份和授权作为 Agent 生态重点；它说明开发者入口需要先分开目标、协议、身份和权威，但不证明 Noemion 已经实现这些机制。

## 规范检索路径复核 · 2026-07-14

规范参考指南此前按 Endem、Synem、Dromen 和 Iknem 展开。它能说明对象，却假设开发者已经知道问题属于哪个专名。场景、威胁模型、向量和研究资料也散布在权威顺序段落中，读者难以判断它们能否约束实现。

当前指南先按九类工程问题定位规范源，再用外部 Agent Task 的例子展示跨规范查询。外部 `completed` 状态先进入协议适配边界，随后分别核对会话能力、证据范围、满足判断和决定权威。页面另用资料状态表分开 CORE、Profile、ADR、威胁模型、解释材料、研究资料和向量，明确研究内容与资料检查都不能替代现行条款或组件证据。

这一结构延续 GNU 文档同时服务教程与参考用途的原则。教程页负责从具体工作建立职责顺序，参考页负责从具体问题定位条款；两者都回到同一套版本化规范源，不复制第二套定义。

## 开发者变更与证据路径复核 · 2026-07-14

测试页此前从解析安全直接进入各类验证，并逐项手写向量数量。开发者仍需自行推断某类变更应从哪份规范开始、最低要提交什么证据，以及通过后最多能作出哪一层声明。手写数量也已经发生漂移：页面写成十五个 Iknem 向量，当前登记和测试实际执行十八个。

当前开发指南先要求写出可证伪的变更主张，再定位消费者、权威依据、失败责任、最低证据和声明上限。测试页新增变更—证据矩阵，分开公开文案、语义、Profile/格式、外部 Agent 协议和未来组件实现。向量数量不再复制到说明正文，精确集合与执行结果回到规范登记和测试输出，避免低价值计数再次漂移。

外部 `completed` 状态继续作为贯穿示例：开发者必须分别核对来源映射、会话能力、证据范围、满足判断和决定权威。规范与案例一致只能支持资料层结论，不能被写成适配器已经实现或协议接入已经完成。

## 当前状态页证据引用复核 · 2026-07-15

前一轮已经从测试指南移除易漂移的向量总数，但规范入口、对象说明、路线图、下载页和开发指南仍保留多份手工计数。Iknem 页面和规范索引写成十五个提案向量，实际向量源包含九个允许案例与九个拒绝案例；ADR-0022 甚至在同一句中同时写出“十五个”和九加九，构成可直接判定的资料错误。

当前状态页现在只说明资料覆盖什么、不能证明什么，并链接机器可读登记、场景或向量源和版本化验证结果。路线图与下载页不再用资料数量暗示成熟度；精确计数由源文件承担。日期明确的新闻和 ADR 可以保留当时的证据快照，但同一句中的总数与分类明细必须一致，历史计数也不能替代当前登记。

## 生命周期与外部陈述教学复核 · 2026-07-15

生命周期研究已经指出 <code>attested</code> 不能把同一内容的多项签名、验证政策、截止点和撤销关系压成 Endem 自身的单值状态，架构入口、生命周期页、Dromen 说明和 Drasor 页面却仍用“coherent → attested → drase”的线性流程教学。开发者容易由此推断内容在签名后原地升级为永久可信对象，与 RFC 9334 的 Evidence / Attestation Result / 依赖方评估、in-toto 的不可变 subject、SLSA VSA 的 verifier / policy / input attestations，以及 GNU Guix 对内容认证和独立结果比较的分工相冲突。

当前公开说明改为两条轴：内容形成只回答精确内容怎样产生和解析；外部关系分别保存陈述、签名者、验证政策、截止点、撤销与依赖方判断。Dromen 会话准入必须重新核对两轴并绑定当前环境、能力和预算。现行 END-CORE 与 DRO-CORE 的 <code>attested</code> 值尚未迁移，因此页面明确标为草案限制，不把研究候选写成规范字段，也不把文档修正描述为组件实现。

## 开发者模型输入路径复核 · 2026-07-14

现有研究已经分析模型调用前的输入选择、权威、变换、截断、缓存和损失，开发者指南却只写了“模型输出是不可信候选”。读者仍需自行推断网页、工具返回、历史、摘要和附件能否提供指令，以及冲突或截断时何时停止。

开发指南现在以依赖升级调研为例，把输入来源、用途与指令权、变换损失、预算截断、同层冲突、缓存边界、动作复核和不可观察变换写成检查表。规范参考指南同时增加任务入口，把实际模型输入归还 TEXT-IDENTIFIER-CORE，把指令权和动作授权归还 AUT-CORE。

这项调整没有建立上下文对象、网关、运行时或新术语。NIST、MCP、OpenAI 和 GNU 资料只支持威胁描述、最小权限与可追溯机制；现行义务仍来自 Noemion 的版本化规范源。

## 全站单列阅读轴复核 · 2026-07-15

这段历史结论曾把“左右空白对称”当成单列正文的默认目标，并据此要求受限阅读列居中。后续真实页面反馈证明，这种规则在 FAQ 卡片、手册和普通专题中会放大内部留白，使文字脱离内容区的自然起点。

现行规则以“外层画布居中、文字列左侧锚定”为准。普通专题、目录正文、手册和 FAQ 答案限制最长行宽，但不再使用左右自动外边距把文字推到中央。宽表格、流程、卡片、代码和对象映射继续使用完整可用宽度；具有真实职责的摘要栏和双栏论证仍按可用空间决定布局。

旧的“左右空间对称容差”不再作为质量目标。当前回归检查文字列左边距为零、共享流式内边距生效且整页没有横向溢出；正式浏览器验收直接使用部署后的线上页面。

## 人类目标编译与项目时代性复核 · 2026-07-15

同名项目仓库重新说明了 Noemion 的出发点：过去的软件主要把程序员书写的形式代码编译给机器；人工智能时代需要研究一种路径，让普通人也能把自己的自然语言目标形成供智能系统使用、可持久且可检查的制品。旧网站已经清楚解释目标满足、证据和协议边界，却把项目意义收缩成“外部完成状态不能直接映射为满足结果”，没有先说明这项研究为什么与普通人有关。

当前首页、项目背景、背景与边界、入门指南和 FAQ 先用人类问题建立主张，再进入 Endem 和六个语义面。网站把“编译”限定为从原始表达到可复核目标制品的研究路径，明确它不是自然语言生成代码，也不表示已经存在编译器。目标只覆盖人希望人工智能系统达到的结果，不扩大成全部人类语言；消费方写作“人工智能系统”，不把责任缩减为单个模型。

[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)把可代表用户行动的 Agent、互操作协议、身份授权和安全评价分别推进，说明人工智能系统正在越过单次回答并进入真实行动环境。[MCP 架构说明](https://modelcontextprotocol.io/docs/learn/architecture)则明确把协议范围限制在上下文交换，不决定应用怎样使用模型或管理目标。[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求文档按用户的问题和概念组织，而不是照抄实现结构。这些来源支持“先说人的目标，再说协议和内部对象”的表达顺序，但不证明 Noemion 的设计正确、规范稳定或组件已经实现。

## 软件 Agent 身份与责任链复核 · 2026-07-15

现有 AUT-CORE 已经分开请求主体、实际行动者和被代表主体，但公开资料仍常用一个 Agent 名或服务账户指代模型、软件定义、认证工作负载和精确运行副本。多模型路由、弹性副本、服务账户委托、企业 MCP 接入和跨 Agent handoff 会让这种简写失去审计能力：认证成功不能说明哪一个实例发起动作，也不能证明被代表主体授予了该动作。

当前说明改为九个职责层次：模型、Agent 定义、部署、工作负载、运行实例、会话、凭据、主体委托和一次动作。身份、认证、授权与责任分别判断；实际行动者需要关联工作负载、运行实例、Dromen 与调用，委托需要保留中间行动者并绑定精确活动。公开页面使用这些直白短语，不引入新造词或读音负担。

这项调整没有建立 Agent 身份目录、凭据格式、责任制品、身份服务或运行时，也没有修改 AUT-CORE。NIST 2026 概念工作仍是研究问题，SPIFFE 只提供工作负载身份基础，MCP 企业管理授权只集中组织接入；精确物理绑定仍需真实消费者、协议 Profile、规范字节和对抗验证。

## 外部技术依据复核 · 2026-07-15

外部资料只支持具体机制，不进入 Noemion 的规范身份。任何适配都必须固定版本、保留原始输入身份，并在外部规范升级时重新验证。

| 权威资料 | 当前观察 | 采用的机制 | 明确排除 | 重新复核触发条件 |
| --- | --- | --- | --- | --- |
| ISO 704:2022、GNU Names、MCP Tools、A2A AgentSkill、NIST transitive closure、W3C PROV-DM 与 RFC 9334 RATS | 术语工作分开对象、概念、定义和指称；工程名称应提供有用意义；机器标识、可读名称、描述和 schema 可以分开；传递闭包、provenance bundle、Evidence、Attestation Result 与依赖方决定各有边界 | 在冲突和读音门禁之前增加专名必要性门禁；非规范提案比较直白对象名、信任角色和普通动作，并保留闭包、证据、会话、权限和结果分离 | 不因词源、稀有拼写或词族整齐保留专名；不把 bundle 当完整依赖闭包；不把 evidence record 当真实性、充分性或最终决定；不提前改现行接口 | 去专名化方向获得人类职责与口头验证证据并形成正式 ADR，或标准术语、真实消费者和 CLI 任务发生变化 |
| ELF gABI、GNU Binutils 2.46.1 发行与 2.46 手册 | 项目页列出的最新发行是 2.46.1，在线手册标注 2.46；`readelf` 独立于 BFD，BFD canonical form 可能丢失格式特有信息 | 非规范适用性矩阵已把结构/装载、符号/绑定、形成映射、裁剪/伴随关系、Build ID 和独立读取归还现有规范 | 自然语言 ELF、机器地址、弱符号、默认版本、环境搜索、静默裁剪、BFD 通用内部表示和带错可信输出 | GNU 发行或手册、ELF gABI、Endem/Synem 物理编码，或真实裁剪与调试消费者变化 |
| ELF gABI、RFC 8949、in-toto Attestation 1.2、TUF 1.0.27、DSSE、GNU Guix 与 MCP 2025-11-25 | ELF 以显式关键标志控制未知内容拒绝；确定性 CBOR 需要协议冻结具体形式；供应链陈述、签名包络、授权元数据和会话授权分别绑定对象与语境 | END-P1 的封闭关键结构、确定性编码、Endem 内容身份与外部授权伴随分离、精确对象与政策绑定 | 权威名称、签名、证据、任务状态或界面接受直接成为内容、授权、满足或最终决定 | 授权伴随物理 Profile、签名 Profile、外部协议版本或 END-P1 结构变化 |
| MCP 2025-11-25 当前修订（Current）与 2026-07-28 候选版 | 截至 2026-07-15，2025-11-25 仍是 Current；官方已于 5 月 21 日锁定并公开以计划最终发布日期命名的候选版，最终版计划于 7 月 28 日发布 | 版本化外缘适配、错误来源分离、最小能力、受众校验、拒绝和观察记录；候选版只作为漂移证据 | 服务器说明、工具 schema、OAuth 身份、`isError` 和远端结果都不能直接成为本地授权、满足或验收事实；候选版不能冒充当前符合性基线 | 候选版转为最终版，或授权、传输、工具结构变化 |
| GNU GCC 诊断、SARIF 2.1.0 与 RFC 9457 | 同一失败可以拥有稳定规则身份、类型化位置、机器出口与人类解释；问题类型和具体发生应分开，错误响应可能泄密 | DIA-CORE 的机器码与消息分离、生产语境、位置、主错误、外部来源、最小披露与有界输出 | 不复制编译器严重度，不把 HTTP 状态、SARIF 或消息文本当作本地结果与权限 | 诊断物理编码、CLI/SARIF/MCP 映射或稳定 ABI 被提出时 |
| A2A 1.0 | Task、Message、Artifact、多协议绑定和主次版本协商服务跨系统交换；Agent Card 可以使用 JWS 签名 | 交换带来源的任务状态、消息和候选产物，核对声明发布者 | 不让补丁号进入协议协商；不让签名 Agent Card 自动成为语义权威；不让外部 Task/Artifact 成为 Endem 身份、生命周期或最终决定 | A2A 主次版本、任务状态机、安全对象或签名规则变化 |
| MCP 2025-11-25 Lifecycle/Tools、A2A 1.0、RFC 8707 与 GNU Autoconf 2.73 | 协议能力、动态工具列表、自描述技能、scope、目标资源、具体特性探测和调用结果属于不同阶段；声明支持仍可能未配置或此刻不可用 | 非规范研究提案分开能力声明、协议协商、授权决定、Dromen 会话上限、即时可调用性与调用事实，并把唯一义务归还现有规范 | 不创建 `CAP-CORE`、能力制品或新专名；不让 Agent Card、schema、签名、scope、版本、缓存探测、端点健康和一次成功调用成为完整授权、持续可用、`met` 或 `accepted` | 责任分配形成正式 ADR，或动态发现缓存、具体 MCP/A2A Profile、Drasor 能力门、健康与配额策略被提出时 |
| MCP 2025-11-25 Tasks 与 Sampling 草案、A2A 1.0、GNU Make jobserver 与中断处理、RFC 9110 | 并行任务、模型工具请求、外部 Task、共享 job slot、取消和强前提各有边界；完成顺序与取消都不能撤销已经发生的外部效果 | 非规范研究提案分开分支准入、尝试、候选、提交、外部副作用与观察，要求共享 Dromen 上限、提交前重验与未知效果保留 | 不创建 `PAR-CORE`、并行制品、事务格式或新专名；不让最快完成、模型评分、Task completed、取消或多数一致成为提交权、`met` 或 `accepted` | 责任分配形成正式 ADR，或真实并行控制面、外部副作用提交器、MCP/A2A Profile 与调度证据被提出时 |
| MCP Security Best Practices 与传输规范、A2A 1.0、Linux no_new_privs/seccomp/Landlock/cgroup v2、GNU Guix shell、Coreutils timeout 与 Make jobserver | token 透传、SSRF、本地服务暴露、链式凭据、系统调用、文件、网络、资源、后代进程和日志秘密是正交风险；内核文档明确 seccomp 不是完整沙箱 | 非规范研究提案分开十个部署责任面，要求模型不接收原始凭据、控制不可用时对应能力关闭失败，并以配置、有效状态、对抗反例、能力专项和漂移形成证据 | 不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、部署对象或新专名；不让容器、seccomp、超时、配置标签或一次成功演示成为完整隔离证明 | 责任分配形成正式 ADR，或真实 Drasor、凭据代理、适配进程、平台拓扑与对抗验证获准设计时 |
| NIST AI 800-2 初稿、NIST AI 800-3、NeurIPS 2023、ICLR 2025、NeurIPS 2025、GNU Diffutils 与 Coreutils | 自动基准与模型裁判正在成为常用评测机制，但目的、协议设置、模型版本、位置、冗长、格式、自偏好、随机性、依赖、污染和统计外推都会改变分数含义 | 非规范研究提案分开九种评测事实，要求确定性检查优先、模型输出保持 `model-candidate`，并以偏差探针、人工校准、依赖审查、区间和漂移限定用途 | 不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品或裁判服务；不让一致率、多个模型票数、排行榜、模型置信度、固定种子或一次偏差探针通过成为满足、充分证据或最终接受 | 责任分配形成正式 ADR，或真实开放式评测、人工校准材料、模型服务 Profile、统计程序与发布决定被提出时 |
| NIST AI Agent Standards Initiative 与 Agent 身份授权概念工作 | 2026 年的 Agent 标准化重点已经明确覆盖身份、授权、安全和互操作；协议身份、代表关系、动作授权与目标满足仍是不同判断 | Agent 系统边界图面向开发者解释请求主体、实际行动者、被代表主体、对象、动作、受众和会话能力上限 | 不创建 Agent 身份制品或新 CORE；不把认证、Agent Card、协议握手或工具可达升级为动作授权、`met` 或 `accepted` | NIST 发布正式指南、身份授权 Profile，或项目提出真实 Agent 协议适配时 |
| NIST NCCoE Agent 身份授权概念论文、SPIFFE、RFC 8693、W3C PROV-DM、MCP 企业管理授权与 GNU Coreutils `id` | 模型、软件定义、工作负载、运行实例、凭据、主体、代表关系、活动和有效身份拥有不同生命周期；工作负载认证与组织接入都不能唯一定位一次动作 | 非规范研究提案分开九个身份与关系层次，要求实际行动者关联实例、会话和调用，委托绑定精确活动，并把唯一义务归还现有规范 | 不创建 Agent 身份 CORE、制品、目录、服务或新专名；不把产品名、服务账户、SVID、单点登录、令牌主体或不可变日志提升为逐动作授权和责任结论 | 责任分配形成正式 ADR，或 NIST 正式指南、工作负载身份 Profile、企业 MCP 接入、真实多副本或跨 Agent 消费者被提出时 |
| OpenAI Agents SDK 编排、RFC 8693、MCP 授权、A2A 1.0 与 GNU Make jobserver | handoff 与主管调用分配不同的答复所有权；委托要分开被代表主体与实际行动者；下游凭据需要绑定资源和受众；嵌套工作不能逃离顶层预算 | 架构指南新增开发者交接检查表，固定三类主体、控制方式、输入变换、能力与预算子集、凭据域、返回结果和证据责任 | 不创建 handoff 制品或新 CORE；不让控制权转移、历史过滤、令牌透传、子任务预算重置或下游 completed 成为授权、完整上下文、`met` 或 `accepted` | SDK 交接语义、OAuth 委托、MCP/A2A 授权 Profile，或真实 Drasor 多 Agent 实现被提出时 |
| NIST AI 600-1、NIST SP 800-218A、NeurIPS RLHF/DPO、Nature 递归生成数据研究、GNU Guix 与 Diffutils | 训练、微调和偏好优化会把数据与反馈变成新模型派生物；投毒、权利、合成数据递归、基础模型漂移、数值非确定性和评测污染都会改变更新含义 | 非规范研究提案分开十一种事实，要求精确数据与模型身份、训练活动、反馈资格、环境和随机状态、独立复现、行为评测、发布与监测分别记录 | 不创建训练或模型 CORE、制品、清单格式、平台或新专名；不让人工在环、模型评分、相同环境、固定种子、损失下降、流水线成功或回滚指针成为数据资格、模型安全、met 或 accepted | 责任分配形成正式 ADR，或真实外部训练服务、模型仓库、反馈采集、适配器发布、撤销与监测 Profile 被提出时 |
| GNU 自由软件定义、OSI Open Source AI Definition 1.0、Linux Foundation Model Openness Framework 与 OpenMDW 1.1、NIST AI 600-1 与 SP 800-218A | 软件用户自由、AI 首选修改形式、模型发布完整性、供应链来源、许可覆盖对象和技术复现回答不同问题；模型许可仍在快速演进 | 非规范研究提案分开十二种事实，要求逐对象披露 API、参数、代码、数据说明、数据、文档、许可、修改形式、复现和外部决定 | 不创建开放模型或许可 CORE、制品、分类器和新专名；不让 API、开放权重、公开仓库、Apache-2.0、OpenMDW、模型卡、SBOM、签名或外部等级成为全栈开放、自由、安全、met 或 accepted | 责任分配形成正式 ADR，或真实模型发行、外部许可选择、开放符合性审查与长期复核流程被提出时 |
| GNU SaaSS 分析与 AGPL 边界、MCP 2025-11-25 Sampling/Authorization、NIST AI 600-1 与 SP 800-218A、模型服务数据控制 | 软件许可、真实服务执行控制、数据外发、下游服务、导出和切换回答不同问题；协议可以调整模型与凭据的控制位置，但不能创造用户对托管实例的控制 | 非规范研究提案分开十六种事实，要求逐执行者、端点、功能、区域和截止点披露已知事实与未知内部路径，并让切换建立新身份、会话、评测和决定 | 不创建服务 CORE、网关、云平台、导出格式或新专名；不让 AGPL、Sampling、OAuth、数据驻留、零保留、API 兼容、导出或调用成功成为实例控制、完整复现、met 或 accepted | 责任分配形成正式 ADR，或真实托管模型消费者、自主管理部署、供应商政策、MCP Profile、导出与降级路径被提出时 |
| NIST Privacy Framework 1.0、NIST AI 600-1、NIST SP 800-88 Rev. 2、RFC 6973、W3C DPV 2.1、MCP Elicitation、GNU Coreutils `shred` 与 Guix 垃圾回收 | 访问、使用、披露、存储、保留、逻辑删除、介质清除、验证、确认、备份和派生物传播回答不同问题；协议和工具通常不能证明下游用途与物理残留 | [非规范研究提案](spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.md)分开十八种事实，要求按精确对象、目的、接收方、截止点、操作、介质、关系闭包、证据和未知范围陈述数据生命周期 | 不创建数据、隐私或删除 CORE、制品、服务和新专名；不让授权、TTL、逻辑删除、退出状态、供应商收据或训练退出成为全部副本不可恢复、历史从未处理、met 或 accepted | 责任分配形成正式 ADR，或真实数据政策、存储拓扑、下游服务、清除方法、训练数据去除和证据生产者被提出时 |
| OpenTelemetry 语义约定 1.43.0 与 GenAI 独立仓库 | 1.43.0 总入口已把 GenAI 与 MCP 内容指向独立官方仓库；截至 2026-07-15，独立仓库没有 GitHub release 或 tag，但 README 已公布 `https://opentelemetry.io/schemas/gen-ai/1.42.0`；Schema 版本、核心依赖版本与仓库发布状态彼此独立；输入、输出、工具参数和结果可能含敏感信息 | 同时固定仓库提交、Schema URL 和字段稳定性后，才使用默认脱敏、可替换的运行观测导出器 | 把 Schema URL 写成稳定发布，或让外部字段进入 Endem 编码、Iknem 身份和验收规则 | 独立仓库发布版本或 tag、Schema URL、字段稳定性、依赖版本或隐私建议变化 |
| W3C PROV、RFC 9334、SLSA 1.2 与 GNU Guix challenge | 溯源需要分开实体、活动和责任；证据、验证结果与依赖方决定是不同步骤；外部参数不可信；逐字节差异不能自行裁定哪份输出正确 | Iknem 的有限无环溯源、外部有效性评估、相对 krin 的覆盖度和决定权威分离 | 签名、证据数量、构建证明、差异或模型评分自动成为事实、充分覆盖或最终接受 | IKN-CORE Profile、撤销分发、透明日志或跨生产者归并被提出时 |
| RFC 6920、RFC 9052、DSSE、Sigstore Bundle、SLSA 1.2、GNU ld 与 Guix challenge | 完整摘要只绑定名称与字节；签名必须保护类型和关键上下文；key ID 只是提示；build ID 不是当前文件校验和；可复现性需要逐字节比较 | ID-CORE 的身份域、完整引用、有类型签名陈述、外置验证材料、权威分离、截止点与独立产出比较 | 摘要相同成为语义真值，签名或日志包含成为授权，短摘要或 build ID 选择对象，单次重跑成为可复现证明 | 发行算法、签名 Profile、证书、透明日志、撤销或 Semantic Key 被提出时 |
| RFC 3629、Unicode UAX #9/#15/#31、UTS #39/#55、RFC 8264 与 GNU libunistring | UTF-8 解码、规范化、标识符、双向显示、同形风险和文本处理属于不同职责；可见相同不等于字节、标量或意义相同 | TEXT-IDENTIFIER-CORE 的文本槽、严格解码、来源溯源、ASCII 标识符、显式比较域、范围、隐藏字符审查、模型输入与显示视图 | 盲目规范化来源、同形骨架合并身份、显示顺序参与解析、语言标签或模型相似度取得语义权威 | Unicode 版本、国际化标识符、来源字节字段、tokenizer Profile 或文本处理实现被提出时 |
| RFC 9396、RFC 8693、RFC 9470、RFC 9700、MCP、A2A、GNU Guix 与 GnuPG | 细粒度授权、委托与冒充、重新认证、受众限制、本地信任和 Agent 链式请求属于不同判断 | AUT-CORE 的完整语境、主体资格、封闭范围、委托收窄、同意绑定、重放防护、能力交集与结果分离 | scope、签名、登录、step-up、Agent Card 或界面点击自动成为语义或最终权威 | 权威目录、政策语言、授权事件编码、同意 UI Profile 或外部协议映射被提出时 |
| ELF 装载视图、Linux capabilities/no_new_privs/Landlock 与 MCP 会话授权 | 持久文件与动态运行表示不同；能力可以设置不可增长上界；任务与令牌必须绑定授权上下文和目标资源 | DRO-CORE 的一次会话主体、环境、能力交集、秘密外置、只读失效和销毁 | 把 Dromen 写成文件、进程映像或凭据包，或把 Linux 与协议名称当成隔离证明 | Drasor API、沙箱、凭据代理、预算计数器、事件编码或恢复机制被提出时 |
| RFC 3339 / RFC 9557、GNU 时间工具、W3C OWL-Time 与 OpenTelemetry Metrics | 绝对时刻、附加时区信息、单调经过时长、相对日期歧义、瞬间/区间/时长与遥测窗口分别有明确边界 | `fixed` UTC 半开区间、`elapsed` 具名事件与单调时钟、显式覆盖缺口、`strict/budgeted` 连续政策 | 默认本地时区、`now/tomorrow`、墙钟测量时长、离散采样冒充连续成立，或把外部时间类型直接写入 END-P1 | 时间 Profile、闰秒策略、跨重启关联、时区数据库封装或多生产者归并被提出时 |
| W3C OWL 2、SHACL、SPARQL 1.1、GNU grep 与 OpenTelemetry Logs | 开放世界中的未陈述不等于假；封闭约束、无匹配查询和无匹配文件都只对指定范围成立；日志区分发生时间与观察时间 | 同一关系的显式极性、空结果默认 `agno`、有限封闭范围与完整性责任 | 空日志、部分搜索、模型“未发现”或单条遥测记录成为普遍负事实 | 封闭声明 Profile、跨生产者完整性、迟到窗口、撤销传播或复合否定被提出时 |
| NIST AI RMF 与 GenAI Profile | AI RMF 1.0 正在修订；AIRC 继续把测试、评估、验证与确认作为风险管理资源 | 风险登记、具名责任、TEVV 和高风险模型/工具检查清单 | 风险框架定义 Endem 字段、合格阈值、ABI 或软件符合性 | AI RMF 修订版、GenAI Profile 或关键基础设施 Profile 正式更新 |
| OpenAI Model Spec、NIST AI 100-2e2025 与 CAISI、MCP 安全条款、GNU ld link map | 工具返回、引文和外部数据默认不能自行取得指令权；不可信内容与高信任提示拼接会产生劫持风险；上下文截断、工具注解、会话注入和装配损失必须显式处理 | 非规范研究提案已形成十四个案例、唯一责任归属、八类威胁和失败域矩阵；开发者指南把来源、用途、变换、截断、冲突、缓存和动作复核写成任务检查表 | 不复制供应商消息角色，不依赖模型自行识别注入，不把链接顺序、位置或标签当作权威，也不建立新制品或“自然语言链接器” | 责任分配形成正式 ADR，或模型、tokenizer、Drasor 控制平面、检索策略、上下文缓存与模型 SDK Profile 被提出时 |
| GNU Make、ReAct、A2A 1.0.0、MCP 2025-11-25 Tasks 与 OpenAI Agents SDK | target、依赖和 recipe 可以分离；Agent 会交替推理、行动、观察、handoff 和重规划；外部 Task 与轨迹各有自己的生命周期 | 非规范研究提案已形成十二个支持/反例、重规划矩阵、十类威胁和唯一责任归属；目标、计划、外部任务、证据与最终决定保持分离 | 不建立计划制品或 `PLAN-CORE`，不把 recipe、步骤、Task completed、handoff、轨迹或模型计划直接变成 Endem、met、Iknem 充分覆盖或 accepted | 责任分配形成正式 ADR，或计划需要跨会话身份、物理事件格式、具体 A2A/MCP Profile 与 Drasor 规划实现时 |
| W3C RDFC-1.0、RFC 8785、Unicode UAX #15、RFC 7950、GNU BFD/objcopy、GNU Guix challenge、OpenAI Structured Outputs、Sentence-BERT、LLM-as-a-Judge 与 NIST AI 800-3 | 规范化只在封闭对象域与关系中成立；跨格式和兼容规范化可能丢失信息；逐字节复现只比较精确输出；schema 合规只证明结构；模型相似度与裁判带有任务、模型、偏差和不确定度 | END-DET-001 已改用封闭形成输入；公开测试页分开来源变换、确定性形成、派生显示、回转/迁移与独立复现；非规范研究提案继续分开精确身份、结构同构、观察等价、迁移、强化/弱化和模型相似度 | 不建立通用等价布尔值、万能 Semantic Key、等价制品或迁移组件，不让回转成功、schema 合规、裁剪、迁移、相似度、签名、证据或相同结果继承身份、权限与接受状态 | 责任分配形成正式 ADR，或真实裁剪/迁移消费者、关系代数、跨 Profile 映射和正反向量出现时 |
| GNU Make、Kubernetes Controllers、W3C PROV、CloudEvents、OpenTelemetry、RFC 9110、ReAct 与 A2A | 终态、更新动作、活动、事件、操作状态、幂等与外部任务各有自己的语义；使用和生成链对派生仍然不充分 | 非规范研究提案已把终态满足、动作发生、状态转变、因果归因、授权责任与最终决定分开，并形成十六个案例、十二类威胁和唯一责任归属 | 不把后态成立、recipe、控制器调节、事件、Span Ok、幂等 no-op、模型自述或 Task completed 提升为动作、因果、责任、met 或 accepted | `kine` 的目标方向解释形成正式 ADR，或动作/转变关系、因果方法、观察 Profile 与真实 Agent 消费者被提出时 |
| GNU Make、MCP 2025-11-25、A2A 1.0.0、OpenAI Agents SDK 与 NIST AI 600-1 | dry-run 可能保留执行例外；敏感工具需要可拒绝的确认；批准后到执行前仍有时序漂移；人机配置存在自动化偏见与过度依赖 | 非规范研究提案已分开预览、模拟、授权、执行尝试、事后观察、满足和最终决定，并形成十二个案例、十类威胁和唯一责任归属 | 不把打印 recipe、模型计划、确认按钮、RunState、Task 状态、工具成功或人工在环标签提升为无副作用、持续授权、met 或 accepted | 责任分配形成正式 ADR，或真实高风险工具、同意 UI Profile、模拟方法、长时审批和正反向量被提出时 |
| OpenAI Agents SDK 对话状态策略、OpenAI Sandbox Agents 跨运行记忆、MCP 当前版与发布候选、A2A 1.0、GNU Make 与 GNU Guix | 对话历史、提炼指导、运行暂停、工作区恢复、外部 Task、流式续接、文件保留和 generation 回滚是不同机制；历史与记忆可能压缩、陈旧或缺失，通知可能重复，失败目标也可能残留 | 非规范研究提案已分开九类状态、继续/恢复/重试/重放/回滚/补偿，并形成十三个案例、十三类威胁和唯一责任归属；开发者指南新增跨会话恢复检查清单 | 不把 session、跨运行记忆、摘要、检查点、Task completed、缓存命中、保留文件或回滚提升为事实、证据、权限、完整历史、met 或 accepted | 责任分配形成正式 ADR，或持久记忆、检查点、跨设备恢复、具体 Tasks Profile、工作区快照与恢复实现被提出时 |
| NIST AI 800-2/800-3、OpenTelemetry Metrics、Prometheus 与 GNU Units | 评估目标必须先声明构念和用途；固定基准与推广 estimand 不同；指标流、窗口、分位数方法、单位与换算都会改变比较含义 | 构念、总体、程序、窗口、聚合器、单位、区间和阈值分别冻结；比较前不舍入 | 基准名、仪表盘、点估计、模型置信度或机器单位库自动成为满足依据 | NIST 草案定稿、统计模型登记、测量 Profile、复合单位或多生产者归并被提出时 |
| W3C SHACL、GNU Coreutils test、GNU Bash Lists 与 NIST AI 800-2 | 逻辑约束可以显式组合；不符合与检查错误必须分开；决定性条件可以短路；AI 评估标准应直接可观察 | 单根复合边界、all_of/any_of、四结果传播、决定依据和求值覆盖 | RDF Shape、shell 退出码、任意表达式或模型指令直接成为 Endem 判断语义 | 条件、排他析取、组合 Profile、物理字段或新的稳定 SHACL 版本被提出时 |
| OpenAI 智能体控制平面工程实践 | 强调清晰环境、可读工具、真实反馈与机械检查 | 仓库内规范、诊断、测试和反馈闭环 | 文章直接决定格式、组件、权限或成熟度 | 实现经验与本项目验证结果发生冲突 |

## 第 0 阶段规范证据审计 · 2026-07-13

此前公开页面能够解释规则，却缺少实现可逐条引用的规范源。当前已经建立以下仓库证据：

| 工作包 | 已形成证据 | 当前结论 | 剩余缺口 |
| --- | --- | --- | --- |
| 权威规范 | 十一份核心与格式规范源、153 个唯一条款 ID、END-P0/END-P1 与 `spec/registry.json` | 对象与诊断、适配、身份、文本、权威授权及伴随边界分层登记；实现、线格式和证据状态独立 | 代码阶段前继续用真实自然语言案例与反例修订；独立实现验证需要在代码阶段另行开展 |
| 威胁与限制 | 对象及诊断、适配、身份、文本、授权与伴随绑定威胁模型、`spec/diagnostic-catalog.md` 和 `spec/profiles/end-p0.json` | 已建立 99 类威胁、8 项 END-P0 有限上限和跨对象诊断目录 | 仍需边界规模、最坏复杂度、目标平台、密码、Unicode 与授权实验证据 |
| 场景与规范向量 | 156 个非规范自然语言场景、10 个 Endem 语义 JSON 向量、七组各 12 个专题向量、20 个 Dromen、18 个 Iknem、20 个诊断、各 24 个适配、身份、文本与授权向量、6 个 END-P0 与 14 个 END-P1 字节 | 场景覆盖语义、判断、组合、闭包、会话、证据和横切边界；所有提案矩阵均执行允许与拒绝分类 | 场景和提案向量不是组件证据；仍缺未来物理编码、协议、签名、Unicode 与授权 Profile 及平台证据 |
| 历史语言研究 | C/Rust 历史原型、6 个规范向量、差分变异、Sanitizer、有限 fuzz 与重复构建记录 | ADR-0012 据此把 Rust 1.97.0 记为未来候选；这些材料不是组件实现，也不自动授权继续编码 | 代码阶段前重新审查是否保留及是否需要复现 |
| 未来来源与安全核心 | 尚未开始；当前只有 2 个 END-SRCM 来源样例、14 个 END-P1 规范字节向量和未来验证条件 | 没有 Ktisor、Elenk、Theor、CLI、实现级 fuzz 或跨平台构建证据 | 需要另行确认代码开发阶段、仓库与实现范围 |

`tests/spec_contract_test.py` 检查规范版本、条款唯一性、成熟度、威胁映射和向量登记；各专题检查器执行结果域、时间、否定、量化、测量、复合、Synem、Dromen、Iknem、诊断、适配、精确身份、文本和授权提案矩阵；字节检查器读取 END-P0 与 END-P1。它们证明当前公开规范资料与这些案例一致，不证明未来稳定发行没有其他缺陷。

## 入门路径与外部协议时效复核 · 2026-07-15

入门指南此前直接引用 MCP 2025-11-25 Tasks，却没有说明它仍是实验性能力。MCP 后续 Tasks 扩展已经明确新旧接口不具备线格式兼容性；开发者可能由此误以为 Noemion 绑定一套稳定的外部任务状态机。

当前入门路径先区分 Prompt/工作流、外部 Agent 协议、身份与授权、Noemion 四个责任层，再用依赖升级案例解释外部 `completed` 为什么不能成为本地 `met` 或最终决定。NIST 2026 Agent 标准化工作只用于说明互操作、安全、身份与授权正在成为行业共同问题；A2A 与 MCP 只用于说明外部协议对象和版本漂移；GNU 网络服务分析只用于分开客户端软件自由与实际服务控制。三类资料都不进入 Noemion 的字段、结果域或伦理结论。

首页状态短语同时从“规范与安全核心”改为“规范与安全边界设计”，避免把当前规范资料误读成已经实现的安全核心。

## 读音研究数据生命周期复核 · 2026-07-15

术语与读音指南已经区分首次朗读、独立听者、自动转写和人类证据，却只用一句话处理录音、转写、语言背景与自由反馈的保存。开发者可以据此组织听测，却无法判断参与同意覆盖哪些用途、外部 ASR 或众包平台是不是新的处理者，以及删除请求、平台收据和介质清除分别能支持什么结论。

当前指南在招募前增加研究数据清单。原始录音、参与者自述、人类响应、自动模型输出、自由反馈和聚合结果分别固定目的、接收方、访问者、保留截止点、删除范围、备份与派生物；外部模型探测不能借用听测同意成为训练用途。删除主张同时区分逻辑删除、平台请求、介质清除、确认和不可观察副本，不用本地命令或供应商响应概括全部数据路径。

资料引用也完成成熟度修正。原页面使用的 NISTIR 8429 仍是初始公开草案，现改用已发布的 NISTIR 7778 解释零错误样本的 rule of three，并明确不借用其生物识别任务与结论。NIST Privacy Framework 1.0、NIST Research Data Framework 2.0 和 NIST SP 800-88 Rev. 2 分别支持数据动作、研究数据生命周期和介质清除边界；GNU Coreutils `shred` 只作为快照、备份、写时复制和 SSD 反例，不成为指定删除命令。

这项修订不建立参与者数据格式、研究平台、语音组件、训练语料或新的 Noemion 对象。它只把读音传播性验证与数据使用、保留和删除责任放在同一条可检查路径上。

## Agent 系统边界学习路径复核 · 2026-07-15

Agent 系统边界指南已经覆盖身份、授权、协议、并行、隔离、评测、训练、开放性、服务控制和数据删除，但首节连续使用十余个否定段落。风险卡、趋势表和研究表又以“十六条”“十二个”“十五项”等阶段性数量命名。开发者能够查到边界，却难以先形成一条可执行的评审顺序；质量测试还把这些数量固化成文案接口，使后续增删主题必须维持机械计数。

当前指南改为从一次工具调用回答六个问题：期望终态、目标是否包含动作或因果、实际行动者与代表关系、会话能力上限、外部系统实际报告、证据与决定。依赖升级案例继续把目标、授权、Dromen、包管理器退出码、Iknem、满足判断和最终决定逐项对齐。原先逐项展开的运行事实改按责任归类，行业变化改按开发者面对的机制组织，GNU 先例改按工程判断组织，十五项研究提案则按开发者问题路由；所有研究入口和结论上限继续保留。常见风险按越级机制合并，不再重复运行事实表中的每一行；评审结尾改为可以按顺序执行的检查步骤。

NIST AI Agent Standards Initiative 继续支持身份、授权、安全和互操作议题；NIST AI 800-2 明确保留初始公开草案状态；MCP 2026-07-28 仍是计划于 7 月 28 日定稿的候选版；A2A 1.0 继续分开 Task、Message、Artifact、版本和授权；GNU Make 继续分开 target、prerequisite、recipe、并行配额与中断后的目标状态。这些资料只校验分层方法和时效，不直接定义 Noemion 字段或结果。

语言规范同时增加两项质量约束：综合指南先给正向判断顺序或具体案例，再列禁止事项；研究、趋势和风险标题不写死会漂移的清单数量。测试改为核对职责覆盖和案例链，不再要求保留阶段性计数。

## Endem 基础规范学习路径复核 · 2026-07-15

Endem 规范说明是开发者理解整个项目的基础页面，却直接从定义进入标准分层、六字段表、五类结果和完整场景清单。页面逐行复制 END-SCEN 的非规范语料，既造成高密度否定句，也让代表性教学与版本化案例库承担相同职责。后段继续以“状态机”描述 <code>nascent / coherent / attested</code>，没有像生命周期页那样先说明精确内容与外部陈述是两条不同的轴。ADR-0011 还残留内部工作包标签。

当前页面先用“让登记服务返回健康状态”贯穿来源表达、意义投影、事态、目标方向、满足判据和未决意义，再进入精确定义。场景表改为按开发者问题选择代表案例，完整案例、反例与向量继续由 END-SCEN 保存。形成分类同时明确标出 <code>attested</code> 的现行草案限制，并用“精确内容身份 + 外部陈述 + 验证政策与截止点 + 撤销 + 依赖方判断”解释会话准入；这只是修正读法，不提前改变现行规范值。页面还明确说明字段职责已进入草案，而发行拼写和读音仍在研究。

[GNU 文档规范](https://www.gnu.org/prep/standards/html_node/Documentation.html)要求完整文档同时承担教程与参考职责，[GNU 的手册写作说明](https://www.gnu.org/prep/standards/html_node/Doc-Strings-and-Manuals.html)也反对把孤立条目拼成重复手册。RFC 9334 分开 Evidence、Verifier 产生的 Attestation Results 与 Relying Party 政策；in-toto Statement v1 用摘要绑定不可变 subject；SLSA 1.2 VSA 继续显式保存 verifier、policy、input attestations 和 verification result。这些来源支持教学顺序与外部关系分层，不定义 Endem 字段，也不授权迁移 <code>attested</code>。

全站质量规则因此补充一项约束：规范解释页先给贯穿案例，再选择能区分失败域的代表场景；非规范语料和向量留在版本化权威源。正式 HTML 同时禁止出现内部工作包标识。

## 三个组件的开发者学习路径复核 · 2026-07-15

组件总览此前把 Ktisor 简写为“执行投影”，容易让读者误以为形成器可以代替有权主体选择意义；Ktisor 正文还使用“规范化”和单一“状态机”概括形成责任，与未声明文本规范化不得参与身份比较、内容身份和外部陈述分轴的规则不一致。Theor 与 Ktisor 都缺少具体输入到输出的示例。Drasor 则用多个连续章节重复时间、否定、量化、测量、复合与 Synem 的规范细节，开发者在看到实际能力请求前必须先穿过对象定义清单。

当前组件页统一采用“职责名称（设计阶段名称）”和依赖更新案例。Ktisor 只根据已确认且具有精确语义授权绑定的投影确定性形成制品，不自行解释来源；Theor 用独立代码读取同一不可信字节，并把分歧送回规范调查；Drasor 先封闭一次 Dromen，再让模型提出类型化请求，由控制面授权、适配器执行、Iknem 保存实际观察，最后分开满足结果、会话结果与具名权威决定。时间、负观察和聚合等细则继续由 Endem 与 Iknem 规范承担，不在运行器页面复制。

外部资料也按当前成熟度复核：NIST AI Agent Standards Initiative 支持把互操作、身份、授权和安全评估视为独立问题；MCP 2025-11-25 继续要求资源绑定并禁止 token passthrough，2026-07-28 在本次审计日期仍是候选版本；A2A 1.0 的 Task 终态不替代本地满足判断；OpenTelemetry 1.43.0 已把 GenAI 语义约定移入独立仓库，且多项字段仍标为 Development。GNU Coreutils、Make 与 Guix 只提供终止、有限并发和先隔离后开放资源的工程先例，不构成 Drasor 安全实现证据。

这项修订没有新增组件、命令、Profile、物理格式或实现承诺。三个名称的读音流畅度、口头区分度和发布拼写仍需真实使用者验证，因此公开页先说职责，再给设计阶段名称。

## 组合、会话与证据规范学习路径复核 · 2026-07-15

Synem、Dromen 与 Iknem 三个核心说明页此前都直接从定义进入规则表。开发者能够查到条款，却无法用同一个现实任务判断对象为什么分开、会话边界在哪里、某条观察究竟能支持什么。Iknem 还把原始观察到结构化关系之间的步骤概括为“规范化与有损变换”，与项目要求的封闭对象域、显式算法和损失记录不一致；资料索引又出现在最低职责之前，打断了首次阅读路径。

当前三页统一使用依赖升级与服务发布案例：两个可独立失败和接受的终态形成 Synem；Drasor 再为精确闭包、当前政策、环境、能力、预算和观察责任建立一次 Dromen；锁文件摘要、部署响应、健康探针与模型解释分别形成有范围候选，只有对齐精确主体、方法、环境、时间和关系后才可能进入 Iknem。三页先给直白职责，再给设计阶段名称，并明确读音流畅度与相邻名称的口头区分度尚未经过真实使用者验证。

IKN-OBS-001 同步把“规范化步骤”改为实际执行的解析与变换，要求选择、过滤、聚合、换算、舍入、脱敏与模型解释绑定算法或方法版本及信息损失。该修改没有增加 Iknem 字段、物理格式或新结果域，只消除可能掩盖处理步骤的含糊术语。

外部资料基线同时补全。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)已经把 GenAI 与 MCP 内容指向独立官方仓库；截至本次复核，独立仓库没有 GitHub release 或 tag，但 README 已公布 [GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)。因此正式页面同时引用总入口、独立仓库与版本化 Schema，并要求固定仓库提交、Schema URL、字段稳定性、默认脱敏和可替换导出；迁移状态、仓库活跃或 Schema URL 都不能成为稳定发布、Iknem 身份、满足结果或最终决定。

这项修订没有新增组件、命令、Profile、运行时、物理格式或兼容入口。规范案例只解释当前条款，完整场景与提案向量仍由版本化源文件保存。

## 开发者查规范与写变更路径复核 · 2026-07-15

全站 74 个正式路由已经共用自适应阅读轴；本轮继续检查页面虽不再偏斜，却仍可能因长段资料罗列而形成视觉空洞或阅读阻塞的问题。最明显的剩余项位于规范参考和开发指南：前者把 CORE、ADR、威胁、场景与向量连续排成链接墙，后者给出变更步骤，却没有展示一条主张怎样落到条款、反例、验证结果和声明上限。Endem 应用参考还用“规范化”概括形成动作，与项目只允许在封闭对象域中声明确定性变换的边界不一致。

规范参考现在从外部 Agent Task 的 `completed` 状态进入，逐项回答来源、会话上限、证据范围、满足结果和发布决定，并在每一步给出停止条件。权威源、场景源和 ADR 改为按开发者要解决的问题组织；参考页仍链接同一套版本化条款，不复制第二套定义。开发指南用同一案例填出可证伪主张、权威依据、支持与拒绝案例、当前证据和声明上限，再把工作流改为“动作—应留下的可复核结果”对照表。Endem 应用参考则明确 `ktise` 绑定来源与已确认意义，并按固定 Profile 确定性写入，不再使用未限定的“规范化”。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求手册既能从头学习，也能按问题查询，并明确反对按实现结构或功能清单组织说明。该原则支持本轮的教程—参考分工和主动语态，不定义 Noemion 的对象、字段、结果或符合性要求。本轮没有新增组件、命令、Profile、物理格式或实现证据。

## 开发状态、贡献与验证路径复核 · 2026-07-15

开发模块仍有三处会误导贡献者。项目时间线把“职责设计已有成果”写得接近“名称和实现已经完成”，并暴露内部研究标识；开发入口声称没有问题跟踪地址，但仓库实际已经启用 GitHub Issues；路线图又把大量 Agent 研究逐条列出，读者很难恢复组件之间的前置依赖。测试页虽然内容完整，也缺少一项变更从主张、权威、反例、证据到声明上限的贯穿示例。

当前状态页改为分别列出可依赖的资料、已有证据和不能据此声称的结论。时间线使用“已有成果、正在进行、后续规划、限制条件”描述客观状态，并明确发行名称、人类读音、组件、安装包和协议 Profile 仍然缺失。路线图不再按固定编号阶段或研究链接墙组织，而是按术语与规范、确定性形成与独立检查、多目标组合与发布、受控运行与证据、模型与外部协议的依赖顺序说明进入证据和停止条件。

仓库现在提供贡献指南、两类结构化 Issue 表单和 Pull Request 模板。贡献者必须先写可证伪主张、权威来源、支持与拒绝案例、失败责任、声明上限，以及新增专名的必要性和读音风险。GitHub Issues 只接收不含敏感材料的公开问题；项目尚未提供私密安全报告渠道，因此公开资料明确禁止披露未公开漏洞、凭据、密钥、个人数据和可被滥用的样本。

测试页新增 A2A Task 状态映射案例：远端 <code>completed</code> 只进入外部协议状态，错误版本或错绑 Artifact 构成反例，本地满足判断继续由 END-CORE 与 <code>krin</code> 负责。原有多组规则清单收敛为来源与意义、组合与发布、会话与证据、模型与协议四类失败责任，完整条款和向量仍由版本化源维护。

[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把互操作、身份、授权和安全评价作为独立议题；[MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)仍是正式最新版，[MCP 2026-07-28 发布候选](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)仍计划于 7 月 28 日定稿；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)继续分开协议对象、版本与授权。它们只用于固定外部适配事实。[GNU 文档规范](https://www.gnu.org/prep/standards/html_node/Documentation.html)要求文档兼顾教程和参考；这一原则支持本轮以案例和读者问题组织开发资料，不定义 Noemion 的工程对象。

这项修订没有新增组件、命令、Profile、物理格式或软件实现。贡献文件和表单只建立公开协作入口；资料检查仍只证明文档、登记和向量关系一致。

## 意义确认与动作授权术语边界复核 · 2026-07-15

公开页面此前多次把 `semion` 简写为“已授权意义”。这符合 END-CORE 使用的“语义授权”精确关系，却会让首次接触项目的开发者把两种不同结论合并：确认一个来源候选可以进入 `semion`，与允许某个主体调用工具、修改对象或部署服务，不是同一授权。模糊写法还会诱导实现者保存一个没有对象、范围和结果域的 `authorized: true`。

当前资料改用四层解释。意义确认把精确来源、候选、语义位置、安全显示、确定性规则或范围有限具名权威绑定起来；AUT-CORE 仍把这项外部关系称为语义授权。动作授权另对精确主体、对象、动作、目的、范围与截止点形成 `grant / deny / defer`。会话能力再同 Dromen、政策、环境、适配器与预算求交；最终决定最后依据满足结果、适用证据和具名权威形成。任一层都不能替代下一层。

[MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)把受保护资源、scope、授权服务器与访问令牌绑定起来；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)要求服务端依据已认证身份与本地政策逐请求授权，并以 `AUTH_REQUIRED` 处理任务内新增授权。[NIST 软件与 AI Agent 身份授权概念论文](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)分别询问最小权限、具体动作、代表关系与人机授权绑定。这些资料支持把动作访问控制写清楚，但不定义自然语言意义或 Noemion 最终决定。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求首次出现时定义专门术语，并优先使用有明确主语的主动语态。本轮据此让入口先写“意义确认”，在规范页再说明“语义授权”，同时保留 AUT-CORE 的规范强度。该修订不改变六个语义面的数据结构、现行字段、结果域、Profile 或向量，也不建立授权组件。

## 开放问题与语义形成边界复核 · 2026-07-15

开放问题页首次复核已经改用“当前策略、已有成果、正在研究、待定内容”，也分开 CORE、Profile、研究提案与运行证据；但主体仍把三十九个折叠问答并列展示。开发者可以查到每个提案，却仍要自行判断问题处于抽象语义、物理格式、运行机制、公开名称还是实现主张，尤其难以判断一个看似合理的新字段为什么必须停止设计。

当前页面先按问题层次给出可依赖材料和主张上限，再用“给 END-P1 增加签名算法字段”的案例演示责任定位：签名属于内容之外的身份与外部包络关系，因此真正缺少的是有消费者、规范字节、错误分层与撤销策略的签名 Profile，而不是 END-P1 字段。后续内容按内容格式、组合发布、Agent 运行、术语与实现发布组织；二十个不同研究提案入口全部保留，Agent 主题按开发者问题归并，页面结尾给出从对象、消费者和失败后果到 ADR 结论的关闭顺序。折叠问题只保留需要就地解释的边界，不再承担完整研究库存。

Ktisor 与语言规范还残留“已授权语义决定”“已授权 semion”的入口写法。当前统一改为“已确认且具有精确语义授权绑定的意义投影”，并在 Ktisor 职责处直接说明：形成器不替有权主体选择意义，也不授予动作权限。该修改只消除授权对象歧义，不改变 AUT-CORE、END-CORE、Profile、字段或结果域。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求手册围绕使用者的问题与概念组织，并在首次出现时解释专门术语；这支持先给材料等级和停止条件，而不是按内部资料库存铺陈。外部时效复核同时确认：[OpenTelemetry 语义约定主仓库 1.43.0](https://github.com/open-telemetry/semantic-conventions)已经把 GenAI 内容移至[独立官方仓库](https://github.com/open-telemetry/semantic-conventions-genai)，后者截至本次复核没有 GitHub release 或 tag，但已经公布 [GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)；[MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)仍明确标为实验性。这些状态只校验站内成熟度说明，不成为 Noemion 的接口或实现证据。

## 规范参考入口与证据库存复核 · 2026-07-15

外部协议适配、权威、诊断、精确身份、文本与标识符等规范解释页已经用发布案例说明规则，却仍在首屏显示 `12 Clauses`、`24 Vectors`、`No Runtime` 等英文库存标签。规则章节继续以“十条核心规则”“十二条适配规则”命名，身份、文本和诊断页还手工复制威胁、场景与向量数量。条款本身没有问题；问题在于公开解释层把容易漂移的资料规模放在开发者任务之前。

当前规范页保留 CORE 版本和每个条款 ID，并把其他徽标改为“当前策略、物理格式待定、尚无适配器、尚无政策引擎”等读者可以直接理解的状态。规则章节改为回答“一次会话必须固定什么”“诊断必须保持哪些边界”“身份、签名与派生必须怎样分开”等问题。符合性材料继续说明覆盖主题和不能证明的结论，但精确数量只由条款源、登记和版本化测试结果给出。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求资料按使用者的概念与问题组织，并同时支持连续学习和按主题查询；[RFC 7322](https://www.rfc-editor.org/rfc/rfc7322.html)把清楚、一致、可读和消除重复表述列为技术编辑目标，同时明确编辑不能改变技术含义。本轮据此只调整公开解释、状态摘要和导航标题，不改变 CORE 条款、条款 ID、Profile、机器登记、场景或向量。

## 架构决定的开发者查询路径复核 · 2026-07-15

架构决策页此前同时维护逐 ADR 状态表和另一张覆盖相同主题的“当前策略”长表。两张库存表重复解释六个语义面、结果分层、组合、会话、证据和格式，开发者仍需自行判断一个具体变更应查哪项决定。“排除的捷径”又用连续否定句列风险，没有说明常见输入应进入哪个受限角色。

当前页面先用外部 A2A Task 或 MCP 工具报告完成的案例定位 ADP、ID、IKN、END 与 AUT 五层责任，再按开发者问题给出 ADR、CORE、Profile 和停止条件。完整 ADR 状态表继续作为精确索引，重复的策略库存表则删除。自然语言、模型 JSON、环境路径、转换工具、成功信号和会话记录改为“允许进入的角色—仍需补足什么”，使约束可以直接指导接线与审查。公开名称相关变更还必须同步目标语言读音和词表内口头区分审查。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求按读者的问题与概念组织手册，并在首次出现时解释专门术语；[RFC 7322](https://www.rfc-editor.org/rfc/rfc7322.html)要求技术文档清楚、一致、可读并消除重复表述。外部事实同时按独立来源复核：OpenTelemetry 主语义约定当前发布版为 1.43.0，而 GenAI 独立仓库没有 GitHub release 或 tag，但 README 已公布 [GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)；NIST 官网明确说明 AI RMF 1.0 正在修订。两类状态都只限制外部机制的采用方式，不定义 Noemion 的字段、结果或 ABI。

这项修订没有新增组件、命令、Profile、物理格式或实现证据。质量契约现在要求问题入口、具体案例、停止条件、正向输入路径和读音复核，并阻止重新引入重复的策略长表、连续否定式捷径章节或英文阶段徽标。

## 思想来源到工程规范的开发者路径复核 · 2026-07-15

思想与方法基础页此前先列九组哲学传统，再列十四条书目及“待精读”状态。两张库存表能够证明资料范围，却不能帮助开发者回答一个模型候选、工具完成状态或外部观察应落在哪层责任。页面还把时间、量化、测量和求值语言写成后续缺口，与 ADR-0015 至 ADR-0020 已经形成的抽象边界不一致。

当前页面从依赖升级案例进入：来源表达、意义确认、期望事态、动作授权、会话能力、证据范围、满足判断和最终决定逐层分开。哲学资料改为按开发者问题选择，并始终同时给出工程落点和不得推出的结论。书目不再展示内部阅读库存，而是按对象同一、结构表示、言语行为、语境不确定性和 AI Agent 责任提供继续研究入口。

页面同步修正规范状态：ADR-0016 至 ADR-0020 已分别定义时间、否定、量化、测量和复合判断的抽象边界；当前缺少的是对应物理字段与组件实现，不是这些问题完全没有规范回答。Noemion、Endem 与其他设计阶段标识也不再因词源或词族形式取得发行正当性；专名必要性、停止条件、目标语言读音和口头区分仍需独立人类证据。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求资料按读者的问题和概念组织、首次定义专门术语并使用主动语态；[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)把 Agent 互操作、身份、授权、安全研究和评价作为不同方向；[Stanford Encyclopedia of Philosophy 的 Speech Acts 词条](https://plato.stanford.edu/entries/speech-acts/)则明确分开内容、言外之力、权威和成功条件。这些资料支持问题分层，不直接定义 Noemion 字段、算法或结果域。

这项修订没有改变 CORE 条款、Profile、向量、字段、组件或接口。质量契约现在要求具体开发案例、当前 AI Agent 责任、读音状态和问题驱动章节，并阻止恢复哲学家清单或书目库存式标题。

## Agent 协议状态与目标满足边界复核 · 2026-07-15

背景页此前从六个语义短词开始，再用 Prompt、Skill、数据容器和传统目标文件四张卡片说明差异。开发者仍需自行推断 MCP 工具成功、A2A Task 完成、CI 通过和遥测记录为什么不能单独证明用户目标已经满足。首屏的 `Motivation / Scope / Non-goals` 也只暴露页面模板，不能说明项目状态或读者任务。

当前页面从一次依赖升级进入，逐项说明 Prompt、MCP 调用、A2A `TASK_STATE_COMPLETED`、包管理器、CI 和遥测分别能够证明什么、没有回答什么。随后把上下文与工具协议、Agent 间任务协议、工作流、身份政策、遥测、目标契约和具名决定者分配到不同责任层。六个现行字段退到直白开发者问题之后，字段名不再充当理解前提。

[MCP 架构说明](https://modelcontextprotocol.io/docs/learn/architecture)明确把范围限定在上下文交换及工具、资源、提示、通知等协议原语；[A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)定义远端 Task、消息、产物与生命周期状态；[OpenTelemetry 语义约定](https://opentelemetry.io/docs/specs/semconv/)定义遥测属性与信号的共同命名；[GNU make Goals](https://www.gnu.org/software/make/manual/html_node/Goals.html)把 goal 定义为需要更新的 target。这些资料支持职责分层，不意味着相邻协议或构建目标已经提供 Noemion 的意义确认、满足判据或最终接受语义。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)同样把协议互操作、身份授权研究和安全评价分开推进，但不构成对项目设计或实现的认可。

项目背景、架构、开发、资源、应用、FAQ 和动态入口同时把通用英文模板徽标改成直白的读者任务、工程边界和项目状态。CORE、Profile、协议名与版本等正式标识继续保留；这项修订没有改变规范值、物理格式、组件、命令或协议 Profile。质量契约现在固定背景页的开发者判断路径、相邻层边界和入口徽标，防止恢复对象库存或模板式首屏。

## 中文状态标签与机器发音边界复核 · 2026-07-15

项目入口改用中文状态后，ADR 首屏仍保留 `Historical Evidence`、`No Wire Change`、`Protocol Independent`、`No Voice Interface` 等自然语言标签。它们不是 CORE、Profile、版本或协议名称，也不提供比“历史依据”“不改变线格式”“协议无关”“不建立语音接口”更精确的工程含义。在根语言为 `zh-CN` 的页面中继续混用这些短语，会让读者在状态与标识之间反复切换，也可能使辅助技术采用错误的语言和发音规则。

当前 ADR 首屏统一把可准确翻译的状态、范围与限制写成中文，同时保留 `END-CORE 0.1.0-draft`、`END-P1`、`DIA-CAT`、`Rust 1.97.0`、Unicode 等正式标识和通行技术词。历史 ADR 直接标为“已由 ADR-0010 取代”；没有物理格式、适配器、密码实现、政策引擎或兼容别名时直接说明缺失对象，不再使用 `No ...` 句式充当状态库存。

[WCAG 2.2 的 Language of Parts](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html)说明，语言变化的程序化标注帮助屏幕阅读器采用相应发音规则，同时把专有名词和技术术语列为例外；[WCAG Pronunciation](https://www.w3.org/WAI/WCAG22/Understanding/pronunciation.html)进一步指出，错误发音可能使口头理解比视觉阅读更困难。[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求资料围绕用户问题组织并使用有明确主语的主动语态。这些依据支持翻译自然语言状态和保留正式标识，但不能证明 Noemion、Endem 或其他专名已经通过人类读音验证。

共享可读性规则现在分别约束页面根语言、外语自然语言片段、技术标识和发行名称证据；自动生成的长页目录改为“章节”，主页的章节提示、职责说明与生命周期说明、手册徽标、共享页脚和主题选择器也改用中文，隐藏的图形符号和正式技术标识继续保留。质量检查扫描全部正式页面，并单独阻止这些共享界面恢复通用英文标签，不再只保护少数入口。该修改没有改变 ADR 结论、CORE、Profile、字段、命令、组件或实现状态。

## 移动端可用宽度与阅读列对齐复核 · 2026-07-15

内容页基础规则此前通过 `:is(main, .summary-rail-main)` 设置 56px 桌面内边距，紧凑视口规则却只选择普通 `main`。由于两者优先级不同，后写的移动规则并未实际覆盖基础值；架构、栏目和部分内容页在 393px 视口中仍把每侧 56px 留给空白。FAQ 回答、手册正文和若干内容布局又把限制行宽的文字列左右自动居中，使宽屏卡片的内部空白进一步放大。

当前共享规则让基础画布继续居中，但用 `clamp(14px, 4vw, 56px)` 根据可用宽度连续计算正文内边距；320px、393px、768px、1024px 与 1440px 不再依靠互不相干的设备固定值。393px 视口中的计算值约为 15.7px，随后随平板和桌面画布逐步增长。架构页、栏目页、普通内容页、手册、工具页、FAQ、摘要栏、页脚和主页区块使用同一变量，卡片内部仍保留较小的独立呼吸空间。限制行宽的段落、列表和标题改为左侧锚定、右侧自然留白，不再用左右 `auto` 强制放在中央。

首页标题使用橙色单下划线。动态封面后的第一章节使用独立高优先级上边线，并取消该章节整块表面的滚动位移，避免动画把边框从封面边缘移开。以上调整只改变布局和界面呈现，不改变规范、术语、组件或实现状态。

## 全站中文第一理解层复核 · 2026-07-15

同名仓库把 Noemion 的目的写得很直接：普通人应当能够把自然语言目标形成供人工智能系统使用、可以长期保存和检查的制品。全站此前虽然已经准确区分对象、协议和结果，但不少页面仍以“确定性形成、解析闭包、结果域、权威边界、受控实现”等内部名词开场。开发者能够查到定义，却要先理解项目架构，才能知道页面在解决什么问题。

本轮逐页检查 `sitemap.md` 登记的 74 个正式路由，并把修改集中在第一理解层。架构页先说明模型解释、远端完成状态和工具成功为什么不能改写人的目标；组件页先说明写入、独立检查和带权限运行为什么不能由同一职责完成；规范页先给文件身份、依赖、外部协议、诊断和证据的实际问题；指南与 Endem 手册则沿“人写下目标—确认解释—写入与检查—固定依赖—受限运行—最终决定”的顺序组织导语。

首页标题进一步采用同名仓库的时代宣言，把主张写成“人工智能时代，每个人都应该能编译自己的意图”。标题只负责建立方向和传播张力；封面摘要改用“以自然语言表达意图”“供 AI 系统安全使用”“发布制品只保留经过确认的目标结构”“在使用前核对授权边界”等简洁学术用语解释价值，并把安全结果说明为防止 AI 改变目标含义，或执行未经授权的越权行为。形成版保留原始自然语言，最终发布版移除原文；二者不再被含混地合称为“可验证的来源”。摘要不再把“长期保存”当作与 AI Skill、提示词文件或普通存储的核心差异，也不再用没有说明检查者和检查对象的“独立检查”代替安全含义。研究状态由相邻状态区承担，尚无组件等反例进入后续正文。

精确定义没有删除。Endem、Synem、Dromen、Iknem、CORE、Profile、条款 ID、结果值和“必须/不得”继续留在第二理解层和权威资料中。改写只要求术语回答具体问题：闭包列出成员与缺失失败，权威说明谁能确认或接受，结果域说明结果回答哪个问题，确定性说明相同输入与规则应产生相同输出。

质量检查现在读取每个正式页面的导语或手册 `page_lead`。如果一句入口同时堆叠四个或更多高风险抽象名词，检查会失败，迫使作者先写参与者、对象、动作和可观察后果。这是防止入口重新退化为内部对象清单的低层保护，不代替人工审读，也不把普通词频当作文体质量的完整证明。

## `attested` 教学残留复核 · 2026-07-15

生命周期页和核心规范说明已经把精确内容与外部陈述分成两条轴，语言规范、Endem 运行与参考手册、应用入口和早期 ADR 的解释层仍残留“形成 attested 制品”“重新验证 attested 字节”和“制品生命周期包含发布见证”等写法。开发者若从这些入口学习，仍可能把签名包络、验证者结论和依赖方准入压成内容自身状态。

当前解释统一改为四步：精确发布内容保持独立身份；一个或多个有类型外部陈述按摘要绑定主体；验证记录固定信任根、政策、截止点和撤销；依赖方再决定本次会话是否准入。现行 END-CORE 与 DRO-CORE 值仍列在参考页中，但必须标成草案限制，不能实现成内容内 `attested=true`，也不能由签名存在直接推出 Dromen。

这一修订延续 [RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html) 的 Evidence、Verifier 结果与依赖方决定分层，[in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) 的不可变主体摘要和陈述类型边界，以及 [SLSA 1.2 制品验证](https://slsa.dev/spec/v1.2/verifying-artifacts) 对包络签名、主体、信任根和调用方期望的逐项检查。它只修正教学和解释，不修改规范、登记、Profile 或向量；正式迁移仍需用户决定、人类命名证据和独立 ADR。

## 记忆、检查点与恢复教学边界复核 · 2026-07-15

架构指南已经区分对话历史、跨运行记忆、检查点、工作区快照和外部任务句柄，但适配器、Iknem 与 Drasor 页面仍要求开发者自行拼接恢复责任。非规范提案还残留“Endem 或 Synem 的 attest 状态”，会把刚刚拆开的精确内容、外部陈述、验证记录和依赖方准入重新压成内容状态。

当前页面统一采用“只恢复声明范围内的状态”这一阅读顺序。适配器先重绑协议、对端、租户、任务与 TTL，再查询历史缺口和未知副作用；Iknem 只让历史、检查点、外部任务记录和快照支持各自有限主张；Drasor 把保存状态当作新输入，重新验证内容、外部陈述、授权、能力和预算，并建立新的 Dromen。旧秘密、实时句柄、批准和一次性授权消费都不能从检查点恢复。

[OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents/running-agents#choose-one-conversation-strategy)明确区分应用历史、SDK Session、`conversationId` 与 `previousResponseId`；[OpenAI Sandbox Agents](https://developers.openai.com/api/docs/guides/agents/sandboxes#persist-memory-across-runs)进一步分开消息历史、提炼指导以及 resume 与 snapshot 的工作区状态。[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为当前版，而[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)说明协议无状态不等于应用无状态；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)则明确允许任务历史截断，并警告断线重连可能漏掉消息。这些事实支持状态分层，不定义 Noemion 的检查点格式或恢复接口。

GNU Make 的 [Errors in Recipes](https://www.gnu.org/software/make/manual/html_node/Errors.html) 与 [Interrupts](https://www.gnu.org/software/make/manual/html_node/Interrupts.html)共同说明：失败或中断后保留的目标可能已经损坏，保留策略本身不能证明状态有效。GNU Guix 的 generation 回滚只选择声明范围内的既有配置，不会让外部服务、网络调用或授权状态倒退。本轮只把这些反例用于教学边界，没有改变 CORE、Profile、登记、向量、组件或实现状态。

## 终态、动作与因果教学边界复核 · 2026-07-15

状态变化研究提案已经区分终态满足、动作发生、状态转变、因果归因和责任决定，但架构指南、Iknem 与 Drasor 页面仍主要告诉读者“它们不相等”，没有给出从一次真实调用逐步增加主张强度的操作顺序。开发者容易在工具返回、后态观察和责任结论之间自行补上因果关系。

当前解释统一从“目标现在是否成立”开始，再依次核对有身份的动作、同一对象的前后态、竞争活动与观察缺口、有范围的因果方法，以及逐动作授权和具名决定。页面用依赖升级、目标原本成立、失败调用遇到外部修复、未经授权但确实产生变化等案例说明：这些结论可以同时存在，并且不能互相覆盖。

[GNU Make 的查询模式](https://www.gnu.org/software/make/manual/html_node/Instead-of-Execution.html)与 [phony target](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html)分开目标状态和动作入口；[Kubernetes 控制器](https://kubernetes.io/docs/concepts/architecture/controller/)分开期望状态、当前状态、调节请求和状态报告；[W3C PROV-DM](https://www.w3.org/TR/prov-dm/)明确指出使用与生成链对派生是必要但不充分的；[OpenTelemetry Tracing API](https://opentelemetry.io/docs/specs/otel/trace/api/)把 Span 状态限定在一次操作语境；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)把 `completed` 定义为 Task 的成功终态。这些资料共同支持分层检查，但不替 Noemion 选择因果方法或责任规则。

[状态变化与因果归因边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/state-change-and-causal-attribution-proposal.md)保存完整案例、威胁与进入规范前的条件。本次修订只改善开发者教学和非规范研究路由，没有改写 END-TEL-001、CORE、Profile、登记或向量，也没有创建因果制品、字段、组件或检查器。现行 Profile 无法表达的动作、转变或因果要求继续保留为未解决边界或明确拒绝。

## 安全目标制品的开发者检查路径复核 · 2026-07-15

首页已经把安全价值写成“发布制品只保留经过确认的目标结构，并在使用前核对授权边界”，站点元数据和门户设计规则却仍写“来源可验证”或“目标结构与授权边界可验证”。最终发布版会移除原始自然语言，这些描述既没有说明还能核对哪种来源关系，也容易让读者把文件完整性、意义确认和动作授权压成一个性质。入门指南又以“持久保存、组合和独立检查”概括项目价值，没有说明检查对象、检查者、失败结果和执行停止条件。

当前入口统一采用同一安全主张。入门指南把形成与发布、内容完整性、意义确认、动作授权、证据与满足、最终决定排成一条失败可关闭的检查顺序；FAQ 直接说明目标文件不能给自己签发工具、部署或跨会话权限。架构入口同时修正当前成熟度和结果责任：五个公开动作属于计划中的单一入口，当前没有 CLI；验证者形成记录有效性，证据集合相对精确 `krin` 形成覆盖度，`krin` 再形成满足判断，具名权威最后作出决定。

[SLSA 1.2 制品验证](https://slsa.dev/spec/v1.2/verifying-artifacts)要求逐项检查签名、陈述主体、信任根和调用方预期，说明内容或溯源完整性不能脱离依赖方政策。[RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html)把 Evidence、验证者的 Attestation Results 和依赖方决定分开。[W3C PROV-DM](https://www.w3.org/TR/prov-dm/)允许把形成版到裁剪发布版表达为两个实体之间的派生关系，但不让发布版重新包含已移除的原文。[GNU Guix 的 `guix challenge`](https://guix.gnu.org/manual/en/html_node/Invoking-guix-challenge.html)通过独立构建比较发现一致或差异，差异仍需判断来自不可复现、损坏还是恶意来源。这些机制支持责任拆分，不替 Noemion 证明语义正确、授权有效或结果应当接受。

本轮只修订公开解释、元数据、设计规则和质量契约，不改变 CORE、Profile、字段、命令、组件、物理格式或实现状态。

## 外部版本状态与 OpenTelemetry 基线复核 · 2026-07-15

全站此前把 OpenTelemetry GenAI 独立仓库的“没有 GitHub release”与“没有可固定 Schema URL”合成一个判断，并继续引用已经失效的 `TODO` 状态。开发者会因此误以为仓库发布、Schema 标识、核心依赖与字段成熟度必须同步变化，也无法判断应固定哪一项。

官方资料显示，[OpenTelemetry 语义约定总入口 1.43.0](https://opentelemetry.io/docs/specs/semconv/)已经把 GenAI 内容移入[独立仓库](https://github.com/open-telemetry/semantic-conventions-genai)。截至复核日，该仓库的[发布列表](https://github.com/open-telemetry/semantic-conventions-genai/releases)为空，也没有 tag；[复核快照 93a59e4](https://github.com/open-telemetry/semantic-conventions-genai/tree/93a59e48a9b4ea162a4d76edac4ace2d415a759e)中的 README 已公布 [GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)，依赖配置所固定的核心语义约定版本则是 1.43.0。这三项状态并不矛盾，也不能互相替代。

当前页面改为要求同时固定仓库提交、Schema URL 和所用字段的稳定性；Schema URL 只标识 schema 演进线，不能冒充稳定发布。A2A 官方仍把 1.0.0 列为最新发布规范，并明确协议协商只使用主次版本 1.0；仓库 1.0.1 补丁发布不改变这一写法。MCP 官方仍把 2025-11-25 列为 Current，2026-07-28 仍是已公开候选版。NIST AI Agent Standards Initiative 继续把行业标准、开放协议以及身份与安全研究分开推进。

语言规范和质量契约现在把复核日期、版本化官方入口、成熟度、协议协商版本、规范补丁号、仓库 release 或 tag、Schema URL、依赖版本与字段稳定性分开检查。该修订只纠正公开资料和验证规则，不建立遥测导出器、协议适配器、组件、Profile 或实现证据。

## Iknem 开发者判断路径复核 · 2026-07-15

Iknem 规范解释此前同时展开核心证据职责、模型评测、训练更新、因果、跨会话恢复和数据删除。页面虽然覆盖了这些研究主题，却重复展示证据处理流程，并让开发者在理解一项记录之前先处理多个尚未进入规范的专题。

当前解释从“更新依赖并判断能否发布”开始。锁文件、部署响应、健康探针和模型说明分别对应有限主张；随后把原先分散在处理顺序、记录事实、分类、结果域和外部机制中的重复义务收敛为一张九项责任清单，再分别展开四个结果域、外部输入、相邻研究和权威来源。页面从 10 个章节、9 张表格和 41 行表体缩减为 6 个章节、6 张表格和 28 行表体；IKN-CORE 的九条现行责任仍可逐项定位，物理格式与实现状态也保持明确。

模型评测与训练、因果、检查点和删除不再各占一个独立论证章节，而是按开发者提出的更强问题路由到对应非规范研究。W3C PROV-DM、RFC 9334、SLSA 1.2、GNU Guix、NIST Agent 标准化工作与 OpenTelemetry 只用于说明外部输入、验证结果和使用方决定为什么不能合并；它们不进入 Iknem 身份，也不替 Noemion 选择物理编码或实现。

## 测试证据层次与模型研究路由复核 · 2026-07-15

测试指南的形成、显示、迁移、复现、解析安全、资源边界和双读取器路径保持成立，但后半部分分别用两张模型表、外部机制表和证据等级表重复“固定输入、保留失败、限制声明”。开发者需要在相近矩阵之间来回比对，才能判断模型评测、模型更新和普通一致性测试分别能支持什么。

当前页面先把模型参与分成评测与更新两条研究路径，再按“构建结果、规范形式、模型输出与评测、训练环境与随机性”四个比较问题组织外部机制。证据等级改为从示例、回归、性质与安全、互操作到研究实验的渐进序列，明确较强材料不会自动扩大对象、平台、版本、总体或决定权威。原有 GNU Guix、GNU Diffutils、GNU BFD、Coreutils、RFC 8785、NIST 与 OpenAI 资料仍保留在其能支持的有限主张旁边。

这次调整减少了重复表格，没有改变测试选择、规范条款、Profile、登记或向量，也没有把资料构建、研究提案或一致性检查描述成组件实现、模型平台或互操作证明。

## 规范模块平行四边形方向复核 · 2026-07-16

规范模块的引言以彩色大平行四边形表示条款、编码和版本沿确定方向映射，面积更小的黑色命题面在同一首屏承担主命题标签，章节标题前的短标再延续模块身份。大形与小形按可见面积和页面职责区分，不按叠放层级混称。

当前共享规则采用两个明确朝向：彩色大形左上贴齐、左下收进；黑色小命题面和章节标题前的短标左下贴齐、左上收进。规范目录页和全部规范专题页通过同一组模块变量继承，不为外部协议适配页面建立特例。形状仍不裁切标题、徽标、链接或正文，也不改变规范含义、成熟度和实现状态。

## FAQ 开发者首问与模型控制边界复核 · 2026-07-15

FAQ 此前先展开名称与定位，安装状态却放在最后一组。新开发者需要先读六个名称问题，才知道当前没有可执行组件；安全与模型一组又同时解释动作授权、确定性形成、开放模型和托管服务，容易把“模型能提出候选”“控制平面能调用工具”“模型材料开放”“用户控制服务实例”误读为同一能力轴。页面还写“只有 Ktisor 能依据确定性规则或具名语义决定形成规范字节”，没有明确形成器消费意义确认结果而不拥有意义决定权。

当前 FAQ 先回答能否安装、为什么需要目标制品、它是否生成代码以及从哪里开始，再进入对象、形成与裁剪发布。安全部分把内容身份、意义确认、动作授权、会话能力、证据覆盖、满足判断和最终决定依次分开；Ktisor 只消费具备精确语义授权绑定的输入并确定性写入，不替权威选择意义，也不授予动作权限。最终发布版移除原始自然语言和可逆重建材料，但这项裁剪不证明形成资料、备份或伴随记录已经删除。

[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)把安全、身份、认证研究与互操作协议分别推进；[OpenAI Agent 编排说明](https://developers.openai.com/api/docs/guides/agents/orchestration)把 handoff 的控制转移与 agents-as-tools 的管理者控制分开。[OSI Open Source AI Definition 1.0](https://opensource.org/ai/open-source-ai-definition)要求修改系统所需的数据说明、训练与运行代码和参数；[GNU 自由软件定义](https://www.gnu.org/philosophy/free-sw.en.html)关注用户对程序的运行、研究、修改与再分发自由；[GNU 对他人服务替代用户计算的分析](https://www.gnu.org/philosophy/who-does-that-server-really-serve.html)进一步指出，服务器软件自由不会自动给予服务用户对运行实例的控制。这些资料支持把 Agent 控制、模型开放性、软件自由与服务控制分开，不定义 Noemion 字段或实现状态。

## Drasor 开发者运行路径二次复核 · 2026-07-15

Drasor 页此前已经加入依赖更新案例和能力请求路径，但后半部分又分别展开因果归因、检查点恢复、外部协议、隔离机制和失败分类。页面累计十个章节、六张表和三十四行矩阵，开发者读完组件职责后仍需穿过多份研究摘要，才能回到当前状态。版本清单还让组件定义承担了会快速漂移的协议跟踪责任。

当前页面按一次会话的实际顺序重排：先分开模型、控制面、适配器和决定者，再形成只读 Dromen，让类型化请求穿过授权与目标资源绑定，最后在发生故障的层次停止声明。终态归因与检查点恢复合并为“会话结束后”的两条边界；协议映射、隔离和观察字段合并为三个实现前研究问题。页面因此收敛为七个章节、三张表和十六行矩阵，同时保留因果反例、恢复时重新准入、秘密外置、结果域分离和失败关闭要求。

外部状态按复核日重新确认：[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为 Current；名为 2026-07-28 的[候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)已于 2026-05-21 发布，计划在 2026-07-28 形成最终版，因此候选名称中的日期不是当前正式基线。[A2A 最新规范](https://a2a-protocol.org/latest/specification/)把 1.0.0 标为最新发行版，并规定协议协商使用 1.0；取消请求只表示尝试取消，Task 终态仍属于协议域。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)继续把 GenAI 约定路由到独立仓库，Schema URL 与字段稳定性必须分开。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)也继续把互操作、开放协议、身份授权与安全评估作为不同工作轴。

GNU Coreutils `timeout`、Make job slots 与 Guix 容器环境只保留为终止、共享并发预算和先隔离后开放资源的工程纪律，不再占用独立机制矩阵，也不构成 Drasor 安全证明。本次修改没有新增运行 API、沙箱、适配器、遥测导出器、Profile、结果域或组件实现。

## 权威与授权的开发者判断路径二次复核 · 2026-07-15

权威与授权规范说明此前拥有十三个章节、五张表和三十一行矩阵。发布案例已经能够分开请求者、实际行动者、被代表主体与有限决定，后续却再次按意义确认、委托、Agent 身份、数据使用、多人同意、外部资料、哲学和符合性材料逐节展开。开发者需要跨多张相近表格恢复同一次请求，页面也把研究提案和权威资料放在 AUT-CORE 的实际使用顺序之前。

当前说明以一次生产发布为主线：固定请求与对象，区分三类主体，核对政策与范围，形成 `grant / deny / defer`，再与 Dromen、制品、环境、适配器和预算求交。意义确认、动作授权、会话能力、证据判断与最终接受由一张表分开；十二条条款按形成请求、多人关系、使用决定和解释结果四个检查阶段定位。自然语言确认、Agent 实际行动者、委托与权限升级合并为同一接线边界，研究提案只在开发者提出更强问题时路由。页面因此收敛为七个章节、三张表和十四行矩阵。

外部状态按复核日固定：[RFC 9396](https://www.rfc-editor.org/rfc/rfc9396.html)只提供精细授权字段和部分授予边界；[RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)分开 delegation、impersonation、subject 与 actor；[MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)要求资源受众绑定并禁止令牌透传；[A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)仍是最新正式版；[NIST 软件与 AI Agent 身份授权概念论文](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)仍把最小权限、具体动作、代表关系和人机授权绑定列为研究问题。GNU Guix 的本地替代服务器授权与 GnuPG 的 trust model 只支持“签名检查不等于本地信任决定”这一工程纪律，不成为 Noemion 的密钥、身份或语义授权模型。

本次修改没有改变 AUT-CORE、条款 ID、结果值、登记、向量、Endem 字段或 Drase 会话规则，也没有创建政策语言、授权事件格式、身份提供方、同意界面、能力代理、协议 Profile 或组件实现。

## 规范入口渐进式披露二次复核 · 2026-07-15

规范入口此前已经提示开发者从问题出发，却紧接着用四十行表格逐项复制 CORE、Profile、威胁模型、场景与向量路径。读者需要先穿过 4,987 个可见字符和两张表，才能判断一项工程问题应由哪类资料回答；页面也让解释入口承担了仓库目录清单的职责。

当前入口先把六类常见判断映射到负责的对象规范与停止条件，再提供对象直达入口。资料关系按正式条款、机器可读登记、Profile、设计材料、验证资料和未来实现证据分开，详细文件继续由精确仓库入口和任务型索引披露。页面保持五个章节和两张表，表格从四十行收敛为十二行，浏览器可见正文降至 2,551 字符；开发者不必先记住仓库结构，否定内容也集中到停止条件和声明边界，不再用重复免责声明承担导航职责。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求手册先照顾初学者、首次使用时定义术语，并按用户概念和问题组织资料，而不是按实现内部结构组织。[RFC 7322](https://www.rfc-editor.org/rfc/rfc7322.html)要求技术文档保持清楚、一致并消除重复或冲突文字；它在这里仅作为写作指南，不是 Noemion 的技术规范。截至复核日，[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)仍把产业标准、社区协议以及身份认证与安全评测研究作为不同工作轴。本轮据此调整公开解释与质量契约，没有改变 CORE、Profile、登记、向量、字段、组件或实现状态。

## Endem 基础规范渐进式披露二次复核 · 2026-07-15

第一次学习路径修订已经用健康目标解释六项职责，并把完整场景留回 END-SCEN；页面后半部分仍分别展开时间、否定、量化、测量、复合判断、结果域、形成分类、身份与安全读取。十八个章节、十二张表和五十四行矩阵使基础页重新承担了全部专题参考职责，开发者很难在首次阅读时区分“必须现在理解的核心”与“遇到特定目标才进入的专题”。

当前页面用同一个健康目标贯穿来源、意义、事态、方向、判据、观察、证据和决定。容器、Profile、内容接受以及形成版、裁剪发布版、受控伴随资料在同一学习阶段说明；<code>aseme / apor / agno / fault</code> 和五个结果域分别回答不同失败问题。时间、缺席、集合、测量、组合、因果与外部授权改成按开发者问题路由的七行表，保留每项停止条件和精确来源。页面因此收敛为九个章节、六张表和二十八行矩阵，同时保留六项职责、单根不变量、结构显示、现行形成分类、读音状态和安全读取边界。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求文档既能顺序教学又能按主题查阅，并按用户问题而不是实现结构组织。[RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html)把 Evidence、Verifier 结果和 Relying Party 决定分开；[in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md)把陈述类型绑定到不可变摘要主体。截至复核日，[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)仍分别推进产业标准、开放协议、身份认证与安全评测研究。这些资料支持把内容、证据、协议和决定分层，但不定义 Endem 字段、状态、Profile 或实现。

本轮只重构公开解释、页面质量契约与审计记录。END-CORE、END-FMT、END-P1、登记、场景、向量、读音候选和组件状态均未改变。

## 架构决定索引渐进式披露二次复核 · 2026-07-16

架构决定总览已经能够从开发者问题定位责任，但随后仍用二十九行表格复制每条 ADR 的状态和解释。每个 ADR 页面才是背景、结论、限制与取代关系的权威入口；总览继续维护第二份解释，会让同一决定产生两个需要同步的公开版本。外部资料部分又以十三行清单逐项排列格式、时间、协议、遥测、文本和评测资料，机制关系被版本库存切断。

当前页面保留 ADR-0008 至 ADR-0036 的全部直接链接，并按历史迁移、Endem 语义格式与判断、组合会话证据与信任、名称读音与公开动作、来源保留与裁剪发布五组进入。开发者先从任务表定位责任，再在分组索引中选择具体决定；完整状态和论证只在对应 ADR 展开。分组按可用宽度自动分栏，每张卡片保持内容自然高度，避免短组被同排长组拉出无效空白；手机和平板在空间不足时自然回到单列。外部资料则按格式读取、结果与缺席、时间与测量、Agent 协议、遥测与文本、AI 风险与评测六类机制合并。页面表格由五张减为四张，表格正文由六十行减为二十四行，同时保留二十九个决定入口、六类常见输入和六条协议适配不变量。

外部状态按复核日重新确认：[GNU Binutils 首页](https://sourceware.org/binutils/)把 2.46.1 标为当前发布，而随 2.46 源码生成的[工具手册](https://sourceware.org/binutils/docs/)标为 2.46，页面因此分开发布版本与手册版本。[MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)仍是当前正式修订，[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)要到计划发布日期后才能重新判断；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)继续用主次版本协商，补丁号不改变协议兼容。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)仍把 GenAI 路由到独立仓库；[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)仍在修订，[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)则把产业标准、社区协议、身份认证和安全评测作为不同工作轴。

本轮只调整公开总览、质量契约和审计记录。ADR、CORE、Profile、登记、向量、名称、读音结论、格式和组件状态均未改变，也没有把外部标准或研究趋势提升为 Noemion 的实现证据。

## 外部协议适配渐进式披露二次复核 · 2026-07-16

外部协议适配页已经用同一次发布调用解释协议边界，但后续又分别用调用阶段、十二项责任、符合性材料、协议基线、断线恢复和待定研究重复版本、状态、取消、重试与安全责任。页面累计七个章节、五张表和二十九行表体；开发者需要跨多个矩阵恢复同一次调用，也容易把协议库存和研究提案误当成当前实现步骤。

当前页面用四个阶段贯穿一次调用：固定协议与对端，绑定受限本地调用，保留外部状态与映射损失，在取消、断线或重试时保存未知副作用。十二条 ADP-CORE 责任集中为一张实现检查表；版本选择、GNU BFD 信息损失、HTTP 幂等、A2A 恢复、OpenTelemetry 遥测以及能力、并行和隔离研究只在开发者遇到对应问题时展开。页面因此收敛为四个章节、四张表和二十四行表体，浏览器可见正文从 3,785 字符降至 2,651 字符。

外部状态按复核日重新确认：[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为 Current；[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)已经锁定，但计划在 7 月 28 日形成最终版，因此只能作为迁移风险。[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)允许服务端返回少于请求上限的任务历史，取消也只表示尝试取消。[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)限制非幂等自动重试；[GNU BFD](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)明确说明 canonicalization 不能穷尽所有外部格式并可能丢失信息。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)继续把 GenAI 约定路由到独立仓库。这些资料支持版本固定、来源保留和失败关闭，不定义 Noemion 的协议 Profile、状态映射或实现。

本轮只重构公开解释、页面质量契约和审计记录。ADP-CORE、十二项条款、威胁模型、场景、登记与向量均未改变，也没有创建适配器、协议 Profile、凭据代理、重试引擎、事件存储或 Drasor 实现。

## 文本与标识符开发者判断路径二次复核 · 2026-07-16

文本与标识符页此前已经用一次发布说明来源字节、解码文本、结构标识符、显示视图和模型输入，但随后又分别按五类文本槽、十二项条款、来源表达、模型输入、符合性材料和待定内容重复同一组边界。页面累计八个章节、四张表和二十五行表体；开发者要跨多个区块恢复一段文本经过解码、变换、比较、显示和模型调用的完整路径。

当前页面从一份包含自然语言、关系 ID 和模型复核输入的 <code>.ends</code> 清单开始，依次固定原始字节、严格 UTF-8 解码、提交后的来源表达、结构标识符与范围、安全显示视图和模型实际输入。五类文本槽在首次使用时定义，十二条 TEXT-IDENTIFIER-CORE 责任集中为一张检查表；原始文件保真、Unicode 标识符、规范化与搜索、双向显示、模型上下文、授权以及名称读音改为按开发问题路由。页面因此收敛为四个章节、三张表和二十四行表体，同时保留全部十二项条款、24 个提案向量、待定边界和无组件状态。

外部状态按复核日重新确认：<a href="https://www.unicode.org/versions/Unicode17.0.0/">Unicode 17.0</a>仍是当前版本，UTS #39 的安全数据与它同步更新；<a href="https://www.unicode.org/reports/tr31/">UAX #31</a>要求实现声明采用的标识符规则或 Profile，并提醒默认标识符仍可能受不可见字符、同形字符和双向重排影响；<a href="https://www.unicode.org/reports/tr39/">UTS #39</a>明确说明同形程度会随字体、书写系统和使用者变化。<a href="https://www.gnu.org/software/libunistring/manual/libunistring.html">GNU libunistring</a>继续把 UTF-8/16/32 表示、规范化、大小写、字素、词和行处理分开。这些资料支持版本固定和职责分离，不把同形风险、规范化或库接口提升为 Noemion 的身份、语义或实现证据。

本轮只重构公开解释、页面质量契约和审计记录。TEXT-IDENTIFIER-CORE、ASCII 标识符策略、十二项条款、登记、威胁模型、场景、向量、Endem 字段和读音结论均未改变，也没有创建 Unicode Profile、原始来源字段、文本格式、处理库、模型输入网关或组件实现。

## 结构化诊断开发者判断路径二次复核 · 2026-07-16

结构化诊断页此前已经用发布中断案例说明机器码、生产语境、层次、恢复与结果边界，后续却又分别用“完整诊断”“错误文字”“外部 Agent 错误”“诊断目录”和“权威资料”重复这些责任。页面累计九个章节、三张表和二十一行表体；开发者需要在同一字段说明和多种输出机制之间往返，才能判断一次失败为什么停止以及是否可以继续。

当前页面从一次副作用未知的发布中断开始，依次固定实际调用、失败来源、唯一主阻断诊断、未执行层、披露预算和恢复决定。十条 DIA-CORE 责任集中为一张开发者检查表；CLI、SARIF、HTTP Problem Details、MCP/A2A 与日志遥测则按输出出口说明可以承载的内容和不能改变的本地边界。页面因此收敛为四个章节、三张表和二十行表体，同时保留稳定机器码、生产语境、主诊断、恢复前置条件、最小披露、有限预算、原子失败、DIA-CAT 草案状态和无组件边界。

外部状态按复核日重新确认：<a href="https://www.rfc-editor.org/rfc/rfc9457.html">RFC 9457</a>把问题类型、具体发生、HTTP 状态提示、标题和详情分开，明确要求消费者不要解析人类 <code>detail</code>，并警告错误正文可能泄露实现和隐私；<a href="https://modelcontextprotocol.io/docs/learn/versioning">MCP 版本说明</a>仍把 2025-11-25 列为 Current，该版<a href="https://modelcontextprotocol.io/specification/2025-11-25/server/tools">工具规范</a>继续区分 JSON-RPC 协议错误和 <code>isError</code> 工具执行错误；<a href="https://a2a-protocol.org/v1.0.0/specification/">A2A 1.0.0</a>仍是最新正式版，并要求不同绑定保留同一错误语义。<a href="https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html">GNU GCC 诊断输出</a>允许同一诊断进入文本和 SARIF 等不同出口。这些资料支持把失败事实、呈现、协议状态和恢复权限分开，不定义 Noemion 的物理诊断格式、主错误算法或结果域。

本轮只重构公开解释、页面质量契约和审计记录。DIA-CORE、DIA-CAT、十项条款、登记、威胁模型、场景、向量、恢复分类和机器码均未改变，也没有创建诊断格式、Profile、生产器、渲染器、日志服务、遥测导出器、重试引擎、协议适配器或 CLI。

## 精确身份与签名开发者判断路径二次复核 · 2026-07-16

精确身份页此前先定义问题，再依次用发布案例、当前策略、十二条规则、符合性材料和待定内容重复“定位不等于身份、签名不等于授权、派生物不继承来源信任”三组责任。页面共有六个章节、三张表和二十行表体；形成版移除原始自然语言后生成裁剪发布版这一关键关系只出现在案例末行和待定段落中，没有成为开发者核对发布对象的主路径。

当前页面从一次含来源形成版到裁剪发布版的发布过程开始：先定位候选，固定精确字节和解释语境，建立完整身份，验证有类型陈述，按具名截止点评估，再另行决定授权。十二条 ID-CORE 责任集中为一张实现检查表；含来源形成版、裁剪发布版、受控来源伴随资料和外置验证包络则按各自保留内容与验证结论上限连接。页面收敛为四个章节、三张表和二十行表体，同时明确没有伴随资料的验证者只能核对发布字节与适用外部陈述，不能声称已经复核原始表达向目标结构的忠实转换。

权威资料按复核日重新确认：<a href="https://www.rfc-editor.org/rfc/rfc6920.html">RFC 6920</a>用算法、长度和完整摘要建立名称与数据绑定，但把具体摘要输入留给采用它的协议；<a href="https://www.rfc-editor.org/rfc/rfc9052.html">RFC 9052</a>明确说明 <code>kid</code> 只是可能不唯一的密钥查找提示；<a href="https://github.com/secure-systems-lab/dsse/blob/master/envelope.md">DSSE 1.0.2</a>要求应用使用与验证时相同的载荷字节。<a href="https://docs.sigstore.dev/about/bundle/">Sigstore Bundle 0.3.2</a>把签名内容与证书、时间戳和透明日志等验证材料组合保存；<a href="https://slsa.dev/spec/v1.2/verifying-artifacts">SLSA 1.2</a>要求匹配陈述主体摘要，并按验证者配置的信任根、构建者和参数检查来源。GNU <code>ld</code> 继续明确 build ID 不是当前文件校验和，GNU Guix challenge 则以独立产出的逐字节比较检查可复现性。这些资料支持对象、陈述、验证材料、授权和复现分层，不替项目选择算法、签名包络或信任根。

本轮只重构公开解释、页面质量契约和审计记录。ID-CORE、十二项条款、登记、威胁模型、场景、向量、身份域、摘要示例和现行结果边界均未改变，也没有创建摘要器、签名器、验证器、证书 Profile、透明日志客户端、可复现构建系统、发布组件或 Semantic Key。

## Endem 生命周期开发者路径二次复核 · 2026-07-16

生命周期页已经把内容形成与外部陈述分成两条轴，但仍以九个章节依次展开状态、主流程、消费者、形成、签名、运行、结果域、外部资料和实现顺序。尚未冻结的发布 Profile 与尚未实现的动作混在完整流程中，容易让开发者误以为形成版会经过现有流水线升级为可运行发布物；形成版、裁剪发布版、外部验证关系和一次会话的身份差异也需要跨多节才能恢复。

当前页面从一次依赖升级发布开始，先区分含来源形成版、裁剪发布版、外部陈述与验证记录、一次会话与运行记录四类对象，再按意义确认、形成、独立检查、裁剪派生、陈述验证、运行授权和观察决定七步说明停止条件。裁剪发布单独说明身份复用、来源引用悬空、低熵摘要枚举、签名权限继承和伴随资料越权风险；装载阶段则按精确对象、陈述验证、动作授权、环境能力和证据责任重新准入。页面收敛为五个章节、五张表和二十五行表体，并明确 END-P1 只服务形成与评审、发布 Profile 尚未冻结、所有动作和组件仍未实现。

权威资料按复核日重新确认：[GNU GDB 的独立调试文件](https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html)与 [GNU Binutils `objcopy`](https://sourceware.org/binutils/docs/binutils/objcopy.html)支持完整对象、裁剪对象和伴随资料分开保存并显式关联，但不定义 Endem 字段、身份或来源证明。[RFC 9334 RATS](https://www.rfc-editor.org/rfc/rfc9334.html)、[in-toto Statement](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md)与 [SLSA 1.2](https://slsa.dev/spec/v1.2/)把不可变主体、外部陈述、验证政策、验证结果和依赖方决定分开；这些资料不证明原始表达到目标结构的忠实性，也不授予运行权限。[MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)截至复核日仍为实验能力，其 <code>completed</code> 只描述被包装请求的外部执行状态。

本轮只重构公开解释、页面质量契约和审计记录。END-CORE、END-P1、ID-CORE、AUT-CORE、DRO-CORE、IKN-CORE、ADR、登记、向量、形成状态和结果域均未改变，也没有创建发布 Profile、裁剪命令、伴随资料格式、签名系统、授权服务、装载器、会话构造器、证据记录器或组件实现。

## 测试证据类型与开发者验证路径二次复核 · 2026-07-16

前次复核把示例、回归、性质与安全、互操作和研究实验排列成从弱到强的渐进序列。这种表达虽然试图限制声明，却把回答不同问题的证据误写成可相互包含的等级：互操作不能覆盖安全性质，研究实验不能覆盖格式符合性，更多回归案例也不能替代畸形输入和资源边界。页面其余章节又按主张、解析、形成、读取器、当前材料、失败责任、模型和外部机制重复同一批验证要求，开发者仍需跨十个章节恢复一次变更的完整论证。

当前页面改为先限定主张，再由变更对象选择证据组合。一次 A2A 状态映射贯穿主张、权威、反例、证据和声明范围；公开资料、语义、格式、确定性形成、运行适配与模型研究分别说明必须回答的问题和结论上限。当前规范资料、登记、场景、向量、构建与浏览器检查同未来组件的读取器、模糊测试、故障注入、复现和发布证据明确分开。页面收敛为六个章节、六张表和二十九行表体；没有通用证据等级，也不再暗示高成本测试能够替代正确的证据类型。

外部资料按其实际问题重新定位：[GNU 标准目标](https://www.gnu.org/prep/standards/html_node/Standard-Targets.html)把构建后自测与安装后检查分开；[GNU Guix challenge](https://guix.gnu.org/manual/en/html_node/Invoking-guix-challenge.html)比较独立构建结果，但不判断哪份结果正确；[GNU Diffutils](https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html)区分相同、不同和比较故障。[NIST AI 800-3](https://doi.org/10.6028/NIST.AI.800-3)要求明确评测目标、总体、假设与不确定性；NIST AI 800-2 截至复核日仍是自动基准评测的初始公开草案；[NIST SP 800-218A](https://doi.org/10.6028/NIST.SP.800-218A)是生成式 AI 与双用途基础模型开发的最终版安全开发实践；[NIST 部署后 AI 监测研究](https://www.nist.gov/news-events/news/2026/03/new-report-challenges-monitoring-deployed-ai-systems)则处理真实环境变化。它们分别支持测试状态、构建比较、模型评测、开发生命周期与上线监测，不定义 Noemion 条款或组件符合性。

本轮只重构公开测试指南、质量契约和审计记录。规范、Profile、登记、向量、字段、命令和组件状态均未改变，也没有创建测试框架、读取器、运行器、适配器、模型平台或监测系统。

## Agent 系统边界开发者路径二次复核 · 2026-07-16

第一次学习路径修订已经从一次调用提出六个问题，但页面随后又分别展开责任路径、八类运行事实、六类越级、行业变化、GNU 先例、研究路由和最终评审步骤。同一项依赖升级需要在九个章节之间往返，现行规范责任、外部机制快照和非规范研究也处在同一披露层级。页面因此成为核心入口中正文最长的一页，开发者容易把“了解全部相邻主题”误认为完成一次普通调用的前置条件。

当前页面直接从依赖升级开始，按目标内容、行动者与授权、会话上限、外部调用、观察与证据、满足判断和最终决定推进。六类开发者问题只负责把事实送回 END、SYN、DRO、IKN、DIA、ADP、ID、TEXT-IDENTIFIER 与 AUT；越级表则只在状态跨越责任域时帮助定位缺失事实。外部趋势、GNU 先例与十五项研究提案分别进入后续三层，普通调用不再先穿过完整研究库存。正文从 6,574 个可见字符收敛为 4,501 个，章节从九个减为六个；六张表的三十三行各自承担调用顺序、责任归属、越级诊断、外部变化、GNU 约束或研究路由，不再复制同一状态清单。

外部状态按复核日重新确认：[OpenAI Agents SDK 编排说明](https://developers.openai.com/api/docs/guides/agents/orchestration)继续分开 handoff 与由管理者调用受限 Agent 工具，[人工参与机制](https://openai.github.io/openai-agents-python/human_in_the_loop/)处理工具审批前的暂停和恢复；这些机制不自行提供逐动作授权。[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为 Current，[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)仍计划于 7 月 28 日定稿并包含破坏性变化；[A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)仍是最新发布规范。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把产业标准、开放协议、身份和安全评测分开；[NIST AI 800-5](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai)是安全征询意见的汇总，不是 Agent 实现标准。

GNU Make 的 target、prerequisite、recipe、并行配额和中断状态，Guix 的环境与代际恢复，以及 Diffutils、Coreutils 和 GNU 软件自由资料继续只作为目标/步骤、预算/授权、环境/权限、比较/决定与软件权利/服务控制的反例来源。它们不定义 Noemion 字段、结果域或实现。此次修订没有改变 ADR、CORE、Profile、登记、向量、名称或读音结论，也没有创建 Agent 对象、控制平面、适配器、隔离机制、存储或运行组件。

## 思想来源与工程权威边界二次复核 · 2026-07-16

思想与方法基础页已经从依赖升级案例进入，但随后用“工程设计步骤”“思想工具”“当前规范”“继续研究”和“进入规范前的材料”重复同一条转换路径。页面累计八个章节和五张表；思想家、书目、现行规范与准入要求分别出现，开发者需要在多处恢复“哲学只能提出问题，规范与证据才改变工程行为”的边界。

当前页面收敛为五个章节。依赖升级先区分来源、意义、事态、授权、证据和决定；随后用“还原问题、提炼区分、改写问题、寻找反例、建立工程权威”形成唯一转换路径。思想来源按开发者问题就地给出，不再另建书目库存。Noemion、Endem 与其他阶段标识仍先解释职责，并保留目标语言读音和口头区分的人类验证要求。

本轮同时修正两项哲学越界。第一，后期维特根斯坦确实批评早期分析框架，但学界对阶段划分和思想连续性仍有争议，因此不再简写为“放弃逻辑原子主义”。第二，《逻辑哲学论》5.6 与 7 讨论哲学意义上的语言边界，不能直接定义 <code>aseme</code>、<code>apor</code> 或其他软件结果；这些状态只能由 Noemion 自己的可观察条件和规范成立。

[SEP 的 Husserl 词条](https://plato.stanford.edu/entries/husserl/)记录了意向活动相关项的竞争解释，说明现象学类比不能直接变成软件类型。[SEP 的 Speech Acts 词条](https://plato.stanford.edu/entries/speech-acts/)说明句子内容不足以单独决定言外之力，语境和成功条件仍需成立。[Wittgenstein Project 编号文本](https://www.wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_%28English%29)用于核对命题范围；[SEP 的 Wittgenstein 词条](https://plato.stanford.edu/entries/wittgenstein/)提供后期批评与解释争议。[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求按用户问题而非实现或功能库存组织资料；[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)则把协议、身份基础设施和安全评价分开推进。这些来源支持问题分层和写作路径，不定义 Noemion 的字段、结果域或实现。

本轮只重构公开解释、站点地图、质量契约和审计记录。ADR、CORE、Profile、登记、向量、字段、名称和读音结论均未改变，也没有创建组件、接口、格式或运行证据。

## 开发路线图的证据入口二次复核 · 2026-07-16

路线图此前分别用长期原则、五层依赖、首条组件路径、GNU 纪律、外部协议快照和研究入口说明后续工作。对象优先、失败关闭与独立证据在前三节重复出现，Agent 基线和研究主题也形成两份相邻清单。页面共有七个章节、五张表和二十一行表体；开发者仍需自己把这些材料还原为“当前能做什么、进入下一层需要什么证据、何时停止”三个实际问题。

当前页面以这三个问题作为唯一主线。五个工作层同时给出当前工作、进入证据和停止条件；第一条验证切片只覆盖受控来源、已确认意义、确定性形成、生产侧检查、独立只读解释与差分复现，不再暗示组件已经进入实施。<code>ktise</code>、<code>elenk</code> 与 <code>theor</code> 首次按直白职责说明，并明确它们只是现行设计标识，尚未通过发行前的读音、生态、包名和目标法域复核。外部协议基线与研究入口合并为协议版本、身份授权、任务副作用、模型数据和遥测五类适配问题。页面因此收敛为五个章节、四张表和十七行表体，可见正文从 3,040 个字符降至 2,732 个字符。

权威资料按复核日重新确认：[GNU `readelf`](https://sourceware.org/binutils/docs/binutils/readelf.html)明确独立于 BFD 读取实际对象，[GNU BFD 信息损失说明](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)指出外部格式进入内部规范形式时可能丢失无法表示的内容，[GNU 手册规范](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求按读者的问题而不是程序结构组织资料。[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为 Current；[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)仍包含破坏性变化并计划在 7 月 28 日形成正式版。[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)继续分开任务、消息、产物、取消、绑定和版本；[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把开放协议、身份基础设施和安全评价作为不同支柱；[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/gen-ai/)已把 GenAI 约定移至独立仓库。这些资料支持独立读取、损失披露、版本固定和职责分离，不定义 Noemion 的对象、接口或实现顺序。

本轮只重构公开路线图、导航摘要、站点地图、质量契约和审计记录。规范、ADR、Profile、登记、向量、名称状态和读音结论均未改变，也没有创建组件、CLI、适配器、遥测导出器、运行时、签名 Profile 或发行物。

## 背景页的独立目标对象边界二次复核 · 2026-07-16

背景与边界页此前先解释目标编译，再分别展开依赖升级、相邻层、持久目标对象、GNU 工具链、责任分配和当前状态。相邻层与责任分配重复列出模型、协议、授权、运行、遥测和决定；“为什么需要一个持久目标对象”还会把工程价值误解为比普通文本或 AI Skill 保存得更久。页面同时使用“最终发布版移除原文”，却没有就地说明发布 Profile、字段映射和向量尚未定义，容易让读者误以为裁剪发布物已经存在。

当前页面先限定项目研究目标形成而不是代码生成，再用一次依赖升级区分自然语言请求、MCP 调用、A2A Task、构建结果和观察记录。独立目标对象的价值改为精确身份、版本化解释规则和失败责任；普通文本、提示词与 AI Skill 同样可以长期保存，不构成差异。含来源形成制品与未来裁剪发布制品明确成为两个精确对象，内容变化不能静默继承签名、证据、授权或接受状态。相邻系统与责任分配合并为一张表，GNU 的依赖和写作纪律就地进入对应开发问题。页面从七个章节、四张表和二十二行表体收敛为五个章节、三张表和十七行表体，可见正文从 3,018 个字符降至 2,571 个字符。

权威资料按复核日重新确认：[GNU make Goals](https://www.gnu.org/software/make/manual/html_node/Goals.html)把 goal 定义为最终要更新的 target，并沿 prerequisite 递归更新其他目标；这支持显式依赖，不支持把文件更新写成业务满足。[GNU 手册规范](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求先定义专门术语，按读者问题而不是程序结构组织资料，并优先使用主动语态。[MCP 架构说明](https://modelcontextprotocol.io/docs/learn/architecture)把自身范围限定在上下文交换协议，不规定人工智能应用怎样使用模型或上下文；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)则继续把 Task、Message、Artifact、绑定和安全对象留在协议域。这些资料支持职责拆分和开发者写作，不定义 Noemion 的目标身份、裁剪关系或结果域。

本轮只重构公开背景页、站点地图、质量契约和审计记录。END-P1、ID-CORE、AUT-CORE、DRO-CORE、IKN-CORE、ADR、Profile、登记、向量、字段和名称状态均未改变，也没有创建发布 Profile、裁剪动作、编译器、组件、协议适配器或发行物。

## Dromen 会话契约开发者路径二次复核 · 2026-07-16

Dromen 页面此前从定义进入发布案例，随后分别用来源流向、十条规则、保存边界、环境变化、Agent 协议、资料入口和当前状态重复主体、能力、预算、漂移与恢复责任。页面共有九个章节、三张表和十九行表体；“已经发布的目标制品”还会暗示尚未冻结的发布 Profile，“密封”则容易被理解为可序列化容器。

当前页面先说明何时需要一次会话契约，再按主体与外部关系、政策与时间、环境能力与秘密、预算与闭包激活、观察与生命周期五步建立边界。十条 DRO-CORE 规则保留原编号，并集中进入一张建立检查表；契约内容与外部状态分开列出，漂移、检查点、MCP、A2A 和中断后半成品则在同一恢复路径中说明。页面收敛为五个章节、三张表和十二行表体，可见正文从 2,894 个字符降至 2,880 个字符；主要改进来自减少重复跳转，而不是删除失败条件。

权威资料按复核日重新确认：[RFC 9334 RATS](https://www.rfc-editor.org/rfc/rfc9334.html)把 Evidence、Verifier 产生的 Attestation Results 与依赖方按自身政策作出的决定分开；[MCP 2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)把协议核心改为无状态，同时明确应用仍可通过显式句柄保持状态，并把 Tasks 移入独立扩展；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)把 Task 定义为有状态对象，允许历史截短且不保证取消成功。[GNU make 中断说明](https://www.gnu.org/software/make/manual/html_node/Interrupts.html)会删除被部分改写的目标以避免半成品被误当成最新，同时说明清理仍可能失败。这些资料支持验证结果、应用准入、协议状态、恢复输入和部分产物分层，不定义 Noemion 的会话格式或运行机制。

此次修订只重构公开解释、导航摘要、站点地图、质量契约和审计记录。DRO-CORE、十项条款、ADR、登记、威胁、场景、向量、字段、名称和读音结论均未改变，也没有创建 Dromen 文件、API、Profile、Drasor、装载器、沙箱、凭据代理、预算器或运行时。

## Iknem 有范围证据开发者路径二次复核 · 2026-07-16

Iknem 页面此前依次用发布案例、九项责任、四个结果域、四类外部输入、四组研究问题和三层规范资料解释同一条证据判断链。页面共有六个章节、六张表和二十八行表体；开发者需要在记录形成、有效性、覆盖度、满足判断与权威决定之间反复往返，外部资料和非规范研究也占用了与现行条款相同的阅读层级。

当前页面从“这项信息最多能支持什么”开始，把九条 IKN-CORE 责任归入确定主张、保留观察、外部评估、覆盖与决定四个处理步骤。有效性、覆盖度、满足结果和权威决定继续保持四个独立结果域；模型评测、协议状态、遥测、溯源、验证结果和独立构建比较则统一作为有范围外部输入。研究入口改为正文后的渐进路由，规范、威胁、场景、向量与 ADR 集中到最后一层。页面因此收敛为五个章节、四张表和十六行表体，可见正文从 3,390 个字符降至 2,699 个字符。

权威资料按复核日重新确认：[NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models)要求明确评测目标、总体、假设与不确定性，[NIST AI 800-4](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation)则说明受控评测不能替代部署后监测。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)仍把 GenAI 内容路由到独立仓库；MCP 2025-11-25 与 A2A 1.0 的协议状态继续只属于外部执行事实。[RFC 9334 RATS](https://www.rfc-editor.org/rfc/rfc9334.html)、[SLSA 1.2](https://slsa.dev/spec/v1.2/verifying-artifacts)与 [GNU Guix challenge](https://guix.gnu.org/manual/en/html_node/Invoking-guix-challenge.html)继续要求验证者、政策、精确主体或独立构建结果保持可区分。这些资料支持有限主张、外部评估和使用方决定分层，不定义 Iknem 编码或最终权威。

此次修订只重构公开说明、导航摘要、站点地图、质量契约和审计记录。IKN-CORE、九项条款、ADR、登记、威胁、场景、向量、结果域、名称和读音结论均未改变，也没有创建 Iknem Profile、采集器、验证器、归并器、撤销服务、决定引擎或稳定格式。

## Synem 组合闭包开发者路径二次复核 · 2026-07-16

Synem 页面此前从直白定义进入服务发布案例，再分别用规范不变量、绑定步骤、条件激活、资料入口和当前状态重复完整闭包、精确绑定、权限收窄与结果分离。七个章节虽然只有 2,310 个可见字符，开发者仍需要在案例表、条款表和步骤列表之间恢复一次闭包形成过程；动态工具清单、构建依赖与目标闭包的差异也没有就地说明。

当前页面先判断两个终态是否能够独立失败和接受，再按展开闭包、解析引用、检查关系、收窄权限四步形成固定闭包。六条 SYN-CORE 责任保留原编号，其中成员结果和会话激活进入同一张边界表；形成时条件改变闭包身份，会话期激活只选择固定成员，并继续使用 `active / inactive / unresolved / error` 独立结果域。页面收敛为五个章节、五张表和十八行表体，可见正文为 2,475 个字符；增加的文字用于解释外部机制边界和当前策略，而不是复制场景库存。

权威资料按复核日重新确认：[GNU make 前置条件类型](https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html)区分同时表达更新依赖与顺序的普通前置条件，以及只表达顺序的 order-only 前置条件；它不定义目标语义或授权。[GNU Guix 递归归档](https://guix.gnu.org/manual/en/guix.pdf)可以导出 store item 的传递闭包、引用和派生信息，但不定义 Endem 语义或 Synem 结果域。[MCP 2025-11-25 工具规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)允许通过 `tools/list` 发现工具，并用 `notifications&#47;tools&#47;list_changed` 表示工具集合变化；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)的 Agent Card 声明能力、技能、接口与安全要求，也可能按认证上下文提供扩展信息。这些动态声明只能成为会话输入，不能改写已经形成的目标闭包、授予行动权限或产生闭包级接受。

此次修订只重构公开解释、导航摘要、站点地图、质量契约和审计记录。SYN-CORE、六项条款、ADR、登记、威胁、场景、向量、成员结果、激活状态、名称和读音结论均未改变，也没有创建 Synem 格式、Profile、解析器、形成器、远程仓库、调度器、Ktisor、Theor、Drasor 或 CLI。

## 开放问题渐进式研究路由二次复核 · 2026-07-16

开放问题页此前已经能够区分抽象语义、物理格式、运行机制、公开名称和实现证据，但后续把内容格式、组合发布、Agent 运行和术语实现拆成十六个独立问答，再用一张表重复路由 Agent 研究。读者仍需在页面内扫描完整研究库存，才能判断哪一项资料与当前问题有关；折叠问答虽然减少视觉长度，却没有减少职责恢复和上下文负担。

当前页面保留字段变更案例，并把后续研究归并为内容格式与迁移、组合发布与外部决定、Agent 与运行、术语与实现四个问题域。每个问题域只说明现行边界、停止条件和精确研究入口，完整论证继续留在对应非规范提案。页面从七个章节、十六个折叠项、两张表和九行表体，收敛为五个章节、四个折叠项、三张表和十三行表体；可见正文从 4,261 个字符降至 3,174 个，同时保留二十项现行研究提案的直接路由。

权威资料按复核日重新确认：[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求文档按用户的概念与问题组织，而不是按功能库存组织，并兼顾顺序教学与主题查阅。[GNU BFD 信息损失](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)说明共同内部形式无法穷尽不同外部格式，转换时必须正视无法表示的信息。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把产业标准、开放协议、身份基础设施与安全评价作为不同工作轴；[NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models)则要求模型评测明确目标、适用总体、统计假设与不确定性。这些资料帮助确定阅读结构和证据种类，但不替 Noemion 关闭语义、格式、授权、评测或实现问题。

此次修订只重构公开研究路由、站点地图、质量契约和审计记录。现行 CORE、Profile、ADR、登记、向量、非规范提案、名称和读音结论均未改变，也没有创建字段、格式、接口、组件、Agent 对象、评测服务或实现证据。

## Ktisor 生产、发布与签名边界二次复核 · 2026-07-16

Ktisor 页面此前把发布配置和外部签名响应列为形成器输入，又把 nascent Endem、Synem 和三类 Iknem 都写成已经确定的物理输出。组件总览、Endem 应用页、参考索引和架构指南还分别使用“所有规范制品都必须通过 Ktisor”“签名请求”和“没有签名响应时保留候选”等表述，容易让开发者把目标制品生产、发布派生、密钥权限、签名包络与证据记录合并成一条写入路径。

当前页面按开发者实际问题收敛为五个章节：先说明为什么需要独立生产边界，再沿依赖更新案例固定封闭输入，随后分别定义 <code>ktise</code>、<code>elenk</code> 与 <code>pleko</code> 的交付和停止条件，最后分开发布派生、外部签名、Iknem 与会话决定。<code>ktise</code> 当前只设计来源保留的 END-P1；<code>pleko</code> 只确定抽象组合闭包，Synem 与 Iknem 物理格式继续保持待定。外部签名响应不再作为 Ktisor 输入，私钥也不进入该边界。页面从 7 个章节、3 张表和 2,309 个可见字符，收敛为 5 个章节、2 张表和 2,529 个可见字符；增加的文字用于把相邻责任写清楚，而不是扩大组件范围。

[GNU <code>objcopy</code>](https://www.sourceware.org/binutils/docs/binutils/objcopy.html)把完整对象、裁剪对象和独立调试资料作为不同输出，并说明不当删除可能使输出不可用；[GNU GDB 的独立调试资料机制](https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html)再用显式关系定位伴随资料。这些资料支持“先形成、再按明确规则派生、最后建立关系”的工程纪律，但不定义 Noemion 的发布字段、Profile、身份或签名范围。[SLSA 1.2 Provenance](https://slsa.dev/spec/v1.2/provenance)把制品的来源与生产方式记录为可验证的外部信息，支持生产记录与制品字节分离；它不定义 Iknem、授权、满足结果或最终决定。

本轮只重构公开解释、组件导航、Endem 应用说明、参考索引、架构指南、站点地图、质量契约和审计记录。END-CORE、END-P1、END-FMT、SYN-CORE、IKN-CORE、ADR、登记、向量、字段、Profile、名称和读音结论均未改变，也没有创建 Ktisor、写入器、发布派生器、签名集成、密钥服务或 Iknem 实现。

## Theor 独立读取与主张范围二次复核 · 2026-07-16

Theor 页面此前已经说明独立、只读和资源有界，但把输入输出、实现独立、安全顺序、GNU 类比与失败责任拆成八个章节。开发者需要自己恢复“实际读取什么、视图最多能说明什么、与生产路径分歧后怎样继续”这条主线。组件总览、Endem 应用页、参考索引和架构指南还使用“任意 Endem、Synem 或 Iknem 字节”等概括，没有就地说明当前只有 Endem 具有实验性物理格式。

当前页面从生产与查看共享错误的反例开始，沿一次依赖更新固定实际字节、精确规范/Profile、视图和预算，再把物理结构、Profile、内容、伴随资料与差分五类主张分开。独立、只读、有界和确定输出进入同一实现责任表；分歧处理明确保存最小复现与双方输出，区分规范歧义和实现缺陷后分别修正并重跑，不能让一方覆盖另一方或改写输入制造一致。页面从 8 个章节、2 张表和 2,151 个可见字符，收敛为 6 个章节、3 张表和 2,477 个可见字符；增加的文字用于限定主张范围和未定义格式，而不是扩大 Theor 能力。

[GNU <code>readelf</code>](https://www.sourceware.org/binutils/docs/binutils/readelf.html)明确独立于 BFD，并为递归和输出提供显式限制；[GNU BFD 信息损失说明](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)指出，共同表示无法保留目标格式不能承载的信息。这些资料支持独立直接读取、资源限制与损失显式化，不定义 Endem 字段或 Theor 接口。[NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)把自信但错误的生成内容及其解释列为虚构风险，因此模型摘要只可留在 Theor 之外作为不可信展示候选，不能进入规范视图、诊断身份或差分依据；该资料不定义 Noemion 的模型接口或结果域。

本轮只重构公开解释、组件导航、Endem 应用页与手册、架构指南、站点地图、质量契约和审计记录。END-CORE、END-P1、END-FMT、DIA-CORE、ADR、登记、向量、字段、Profile、名称和读音结论均未改变，也没有创建 Theor、解码器、独立构建、模糊测试、模型摘要器、Synem/Iknem 格式或发行组件。

## 架构设计指南的责任主线二次复核 · 2026-07-16

架构设计指南此前已经用依赖升级区分目标、动作、状态变化和决定，随后却分别展开 Agent 委托、跨会话恢复、三个组件、形成、组合、装载与多项运行研究。页面达到十个主章节、五十一行表体和 9,181 个 Markdown 源字符；开发者需要穿过两套检查清单和组件页的重复定义，才能回到最初的责任链。

当前页面以一张责任图和同一次依赖升级贯穿来源、Endem、独立读取、Dromen、受限动作、Iknem、满足结果与具名决定。委托和恢复合并为一张重新准入表，组件只保留不可合并的信任边界，能力、并行、隔离、模型评测、训练与记忆改为按问题进入专题资料。页面收敛为七个主章节、三十六行表体和 5,826 个 Markdown 源字符；图中也明确 Theor 当前只读取 Endem 字节，不再让尚无物理格式的 Synem 或 Iknem 看似可直接检查。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求技术手册服务首次阅读者，并按用户面对的概念和问题组织，而不是复制实现结构。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)把产业标准、社区协议、身份基础设施与安全评估作为不同工作轴。页面据此采用渐进式问题路由；这些资料不定义 Noemion 字段、Profile、结果域、组件或实现状态。

本轮只重构公开指南、站点发现摘要、页面质量契约和审计记录。CORE、ADR、Profile、登记、向量、物理格式、名称、读音结论和组件状态均未改变。

## 开发指南的可证伪变更路径二次复核 · 2026-07-16

开发指南此前已经用 A2A 状态映射展示主张、反例和声明上限，后续却再次分别展开当前范围、规范优先、工作流、模型上下文、建议仓库树、通用审查清单和模型协议。八个主章节、四十七行表体和 4,882 个 Markdown 源字符把未来目录结构写得像已确定接口，也重复承担了测试页、开发路线和 ADR 的职责。

当前页面让同一项 A2A 映射变更依次经过可证伪主张、真实消费者、权威依据、支持与拒绝案例、失败责任、验证材料和声明上限。权威源、证据类型与模型实际输入各保留一张必要矩阵；未来 Rust 约束和实现阶段只作状态说明，不再公布尚未决定的工作区树。页面收敛为六个主章节、三十九行表体和 4,474 个 Markdown 源字符，同时保留上下文来源、指令权、变换损失、缓存边界和动作前复核。

[GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html)要求健壮、可靠的软件行为，并以主动语态明确责任主体。[NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)提供可嵌入不同生命周期的高层安全开发实践；[NIST AI 800-5](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai)汇总的公开意见则指出，Agent 安全仍应保留基本网络安全原则，同时针对模型输出连接工具和环境的风险继续调整。这些资料支持“保留基线，再增加 Agent 专项反例”，不定义 Noemion 字段、组件或安全结论。

本轮只重构公开指南、站点发现摘要、页面质量契约和审计记录。CORE、ADR、Profile、登记、向量、实现语言决定、物理格式、名称、读音结论和组件状态均未改变。

## 规范模块平行四边形方向复核 · 2026-07-16

规范专题引言包含三种可见尺度：彩色主映射面、黑色命题面和章节标题前的短标。此前黑色命题面被误归为小形，导致它与短标都采用左下贴齐的方向，削弱了大小层级。

当前设计按实际可见尺寸重新分类：彩色主映射面和黑色命题面均采用左上贴齐、左下收进的前向轮廓；只有章节短标采用左下贴齐、左上收进的反向轮廓。该规则由规范模块的共享 CSS 变量控制，适用于规范目录和全部规范专题，不在“外部协议适配”单页增加例外。本轮只修正公开网站的几何层级，不改变规范、术语、名称、读音、Profile、登记或组件状态。

## Endem 参考索引的开发任务路由二次复核 · 2026-07-16

参考索引此前把时间、测量、复合判断和否定分别列成四个专题库存，却没有纳入已经进入 END-CORE 的量化与成员资格。诊断部分又把十七条自由文本短语称为“稳定失败类别”；这些短语既不在 DIA-CAT 登记，也没有稳定机器身份，开发者可能把人类消息误当作 CLI 或跨进程 ABI。页面共有十个主章节和四十八行表体，长篇权威页面与外部资料清单还重复承担了专题页面的导航职责。

当前页面按工作、对象、结果域、目标类型、失败层和开发问题组织。五个动作继续保留精确输入、产出和停止边界，但明确它们是现行设计标识，不是已经发布的命令参数；量化与成员资格补入目标约束，并固定集合身份、成员资格权威、截止点和成员身份规则。诊断索引只展示 DIA-CAT 已登记的机器码示例，分开机器身份、人类消息、外部错误来源和恢复权限，同时明确目录仍是草案而非发行 ABI。共享手册表格保留局部横向滚动，同时不再把动作名和诊断码压成逐字换行。页面从十个主章节、四十八行表体收敛为七个主章节、三十三行表体；Markdown 源字符从 6,088 增至 6,128，增加部分用于补齐量化约束、物理格式状态、读音证据缺口和诊断稳定性边界。

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求手册既能顺序教学也能按主题查阅，并按使用者的概念和问题组织，而不是复制实现结构或功能库存。[GNU Errors](https://www.gnu.org/prep/standards/html_node/Errors.html)要求非交互错误在适用时保留程序、来源和位置语境。页面据此改进阅读路由和人类错误呈现说明；Noemion 的结果域、诊断层、机器码、原子失败和权限边界仍只由 END-CORE、DIA-CORE 与 DIA-CAT 定义。

本轮只重构公开参考索引、手册入口、站点地图、质量契约和审计记录。CORE、ADR、Profile、登记、向量、字段、动作名称和读音结论均未改变，也没有创建 CLI、诊断编码、求值器、Ktisor、Theor、Drasor 或其他组件。

## 入门指南的单案例学习路径二次复核 · 2026-07-16

入门指南此前已经使用依赖升级案例解释协议完成状态不等于目标满足，但案例被放在第三节。首次阅读者需要先经过项目定义、Agent 趋势、服务控制、六步安全检查和四组外部类比，随后还要分别阅读六个语义面、四个对象、五个动作、读音和当前状态。页面共有九个主章节、五张表和二十七行表体；教程、参考索引、术语说明与应用清单仍在同一阅读层级。

当前页面让“把服务依赖更新到安全版本并确认可以发布”贯穿对象、目标变化、行动范围、验收判据和决定权威，再沿自然语言要求、Endem、一次会话契约、外部任务、Iknem、满足判断和最终决定建立单一责任链。安全检查继续保留形成与发布、内容完整性、意义确认、动作授权、证据与满足、最终决定六层顺序；六个字段、完整对象说明、五个动作和读音实验步骤改由按问题入口渐进披露。页面从九个主章节、五张表和二十七行表体收敛为六个主章节、四张表和二十三行表体，Markdown 源字符从 6,323 降至 4,243。

截至复核日，[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把产业标准、社区协议、Agent 身份基础设施和安全评价分开推进。[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)继续分别建模 Task、Message、Artifact 与任务状态；[MCP 2025-11-25 实验 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)正在迁移到[官方 Tasks 扩展提案](https://modelcontextprotocol.io/seps/2663-tasks-extension)，且两种形态不具备线格式兼容性。[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求入门资料从首次读者的问题开始，按工作而不是实现和功能库存组织，并使用主动语态。这些资料支持单案例结构、协议状态分离和渐进路由，不定义 Noemion 的对象、结果域、字段或实现。

本轮只重构公开入门指南、站点发现摘要、质量契约和审计记录。CORE、ADR、Profile、登记、向量、字段、对象与动作名称、读音结论和未来实现顺序均未改变，也没有创建编译器、CLI、协议适配器、会话运行时或其他组件。

## 架构入口的失败责任路径二次复核 · 2026-07-16

架构入口此前分别列出核心制品、命令入口、读取路径、三个组件、四类对象、信任边界和八个继续阅读入口。六个章节只有一张四行数据表和 1,816 个可见字符，却要求开发者自行把十一张入口卡和一条系统流程还原成一次任务的失败责任；“工具成功以后该检查什么”也散落在信任边界列表中。

当前页面用“把服务依赖更新到安全版本，保持测试通过，经批准后发布”贯穿来源确认、Ktisor 形成、Theor 独立读取、Dromen 准入、外部执行、Iknem、满足判断和具名权威决定。责任表为每一层给出停止条件，成功信号表分别处理协议终态、工具与测试、外部陈述、证据记录和模型候选，对象表只说明生命周期与当前物理状态。页面仍为六个章节，形成三张表和十六行数据，入口卡从十一张降为七张；可见正文增至 2,716 个字符，增加部分只用于补齐失败责任、实现限制和读音证据缺口，不复制条款库存。

截至复核日，[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)继续把技术标准、开放协议、身份基础设施和安全评价分开推进；[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)分别建模 Task、Message、Artifact 与协议状态；[MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)仍标为实验机制。这些资料支持把协议完成与本地满足、授权和决定分开，不定义 Noemion 的结果域。[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求按读者问题而不是实现结构组织文档；[GNU make Goals](https://www.gnu.org/software/make/manual/html_node/Goals.html)只定义目标文件及其前置条件；[GNU readelf](https://www.sourceware.org/binutils/docs/binutils/readelf.html)独立于 BFD，以避免共同库错误同时影响检查路径。这些 GNU 先例支持阅读顺序、显式依赖和独立读取，不构成业务满足语义或组件实现证据。

本轮只重构公开架构入口、站点发现摘要、质量契约和审计记录。CORE、ADR、Profile、登记、向量、字段、对象、动作名称和读音结论均未改变，也没有创建 Ktisor、Theor、Drasor、CLI、发布 Profile、协议适配器或运行时。

## 重新审计条件

- 新增正式制品、子命令、进程或仓库。
- 冻结编码、ABI、扩展 registry 或签名 profile。
- 第一次发布 Endem Ktisor、Theor、Drasor 或规范版本。
- 接入模型、MCP/A2A、远端能力或外部签名服务。
- 页面不再能明确区分候选、决定和证据，或路由开始为历史兼容而膨胀。
