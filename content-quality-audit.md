# Noemion 内容、系统闭环与路由审计

状态：Noemion 项目层与 Endem 工程词汇分层后的权威审计基线
范围：`sitemap.md` 登记的全部正式 HTML 路由

## 结论边界

Noemion 已经接受以 Endem 为核心制品的职责、单一应用拓扑和 END-FMT 实验性编码，但尚未进入组件代码开发阶段。具体发行拼写与读音尚未通过人类验证；后续[发行术语去专名化研究提案](spec/release-terminology-simplification-proposal.md)又建议先证明专名必要性，并把 Endem 之外的现行对象称呼、信任角色和公开动作同直白职责候选比较。[语义面与观察词提案](spec/semantic-facet-terminology-proposal.md)进一步保留七项职责，却建议以直白字段名替换 `rhem/semion/skena/telis/krin/apor/phain` 进入验证。[生命周期与结果词提案](spec/lifecycle-and-result-terminology-proposal.md)又发现 `attested` 把外部签名和证明关系误写成内容状态，并把对象边界修正与 `nascent/coherent/agno/aseme/interrupted` 的发行名称验证分开。三项建议都尚未成为 ADR 或迁移决定。当前没有 Ktisor、Theor、Drasor、`endem` CLI、安全核心、安装包或实现 CI；Python 检查器只核对规范、登记和向量之间的一致性。Endem 当前仍是中等风险的候选名：精确包名未登记，但 GitHub 已存在第三方同名对象，正式商标、法律和口头区分门禁尚未完成。页面与资料测试存在不等于软件已经实现，也不证明性能、研究结论、知识产权、读音可用性或标准化状态。

[能力发现、协商与调用提案](spec/capability-discovery-and-negotiation-proposal.md)继续检查 Agent 运行边界。它把能力声明、协议协商、授权决定、Dromen 会话上限、即时可调用性与调用事实分开，拒绝让动态工具列表扩写旧会话，也拒绝让端点可达、scope、签名或一次成功调用变成长期权限、`met` 或 `accepted`。这仍是等待用户决定的非规范研究，不创建 `CAP-CORE`、能力制品、组件或新专名。

[软件 Agent 身份、委托与责任链提案](spec/software-agent-identity-and-accountability-boundaries-proposal.md)补齐“Agent 名称替代行动者”的审计缺口。它把模型、Agent 定义、部署、工作负载、运行实例、会话、凭据、主体委托和一次动作分开，拒绝让产品名、服务账户、SVID、单点登录或 Agent Card 同时承担认证、授权与责任。这仍是等待用户决定的非规范研究，不创建 Agent 身份 CORE、制品、目录、服务、组件或新专名。

[并行、推测执行与提交边界提案](spec/parallel-and-speculative-execution-proposal.md)继续补齐多 Agent 与并行工具调用的高风险缺口。它把分支准入、候选结果、提交选择、当前前提、已发生副作用和后验观察分开，要求所有分支共享同一 Dromen 上限，并拒绝让最快完成、模型评分、取消或外部 Task 状态越过授权与结果域。这仍是等待用户决定的非规范研究，不创建 `PAR-CORE`、事务制品、调度器、组件或新专名。

[模型、适配器与能力域隔离提案](spec/model-adapter-isolation-proposal.md)补齐部署责任无法审查的高风险缺口。它把模型输入、控制面、授权、凭据与实时句柄、协议适配、文件、网络、资源终止、观察和外部目标分开，拒绝让容器、seccomp、超时或提示词名称冒充完整隔离证据，也拒绝把原始凭据交给模型。这仍是等待用户决定的非规范研究，不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、部署对象、组件或新专名。

[模型参与评测与裁判边界提案](spec/model-assisted-evaluation-proposal.md)补齐模型评分与人工智能基准的证据缺口。它把评测目的、构念、可观察标准、题目与候选、协议、模型调用、原始输出、统计汇总和使用决定分开，并要求位置、冗长、格式、来源、注入、相关评审者与漂移反例。模型评审输出继续是 `model-candidate`；多个模型投票、排行榜和自报置信度不能成为独立证据、统计区间、`met` 或 `accepted`。这仍是等待用户决定的非规范研究，不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品、裁判服务、组件或新专名。

[模型训练与更新边界提案](spec/model-training-and-update-boundaries-proposal.md)补齐训练数据、反馈、微调、适配权重、派生模型、复现、发布和回滚之间的责任缺口。它拒绝把会话记忆写成模型学习，也拒绝让用户点击、模型裁判、训练完成、固定种子、相同环境或回滚指针直接成为数据资格、权重复现、用途适合、`met` 或 `accepted`。这仍是等待用户决定的非规范研究，只使用直白职责短语，不创建 `TRAIN-CORE`、`MODEL-CORE`、`FEEDBACK-CORE`、模型制品、训练平台、组件或新专名。

[模型开放性与软件自由边界提案](spec/model-openness-and-software-freedom-boundaries-proposal.md)补齐托管 API、开放权重、源码可见、开源软件、自由软件、Open Source AI、发布完整性与可复现模型之间的术语缺口。它依据 GNU 四项自由、OSI Open Source AI Definition 1.0、Linux Foundation Model Openness Framework 与 NIST 供应链资料，要求逐项列出参数、代码、数据说明、数据、文档、许可和首选修改形式。Apache-2.0、模型卡、SBOM、签名和外部开放等级都不能替代对象清单或互相升级。这仍是等待用户决定的非规范研究，不创建 `OPEN-MODEL-CORE`、`LICENSE-CORE`、模型发行格式、合规服务、组件或新专名。

[托管人工智能服务与用户控制边界提案](spec/hosted-ai-service-and-user-control-boundaries-proposal.md)补齐软件权利、实际执行控制、数据控制和服务可移植性之间的运行关系缺口。它分开第三方托管、自主管理、设备内执行和通信服务，并逐项检查执行者、隐藏变换、数据外发、保留、下游服务、状态、导出、切换、停服、观察和复现。GNU 的服务批评与 AGPL、MCP 的控制拓扑、NIST 供应链审查和供应商数据控制都不能单独证明用户控制服务实例。这仍是等待用户决定的非规范研究，不创建服务 CORE、网关、云平台、导出格式、组件或新专名。

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
| Ktisor | 唯一规范写入器、制品形成侧读取器、来源绑定、elenk 与 pleko | 模型不得写规范字节；Ktisor 不持有私钥或实时能力 |
| Theor | 独立解析任意不可信字节，为差分和安全审查提供第二条证据链 | 不复用形成侧读取器，不产生 Ktisor 内部检查通过引用，不修复输入 |
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

以下清单记录初次逐页审计，并在后续新增 ADR-0022 至 ADR-0035、Dromen、诊断、适配、精确身份、文本、授权、伴随关系、名称门禁和动作收敛页面时继续按同一标准复核。当前共有 59 个 HTML 正文源；Markdown 生成页面另由路由测试和构建产物审计覆盖。

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

本轮逐一复核 `sitemap.md` 登记的 73 条正式路由，包括 59 个 HTML 正文源和 14 个由 Markdown 生成的页面。复核重点不是统一文风，而是让每种页面先完成自己的读者任务：门户给出项目定义，目录给出选择依据，专题给出结论与边界，应用给出状态与输入输出，手册给出连续操作逻辑。

| 页面家族 | 已逐页复核的正式路由 | 本轮处理 |
| --- | --- | --- |
| 门户（1） | `/index.html` | 保持 Noemion 为项目主语；把控制平面和下一步入口改为无需内部术语即可理解的表达。 |
| 项目背景（3） | `/about/index.html`、`/about/background.html`、`/about/intellectual-foundations.html` | 把核心问题拆成形成、组合、实现、验收四步；集中加入《逻辑哲学论》五条短引文，并逐条说明工程启发与不采用部分。 |
| 架构与 ADR（33） | `/architecture/index.html`、`/architecture/endem-lifecycle.html`、`/architecture/decisions.html`、`/architecture/agent-system-boundaries.html`、`/architecture/adr-0008-endem-system.html` 至 `/architecture/adr-0035-public-actions-and-internal-responsibilities.html`、`/architecture/open-questions.html` | 生命周期解释每阶段回答什么；Agent 边界图把规范、研究和运行事实分层；历史 ADR 标明失效名称；现行 ADR 固定语义、格式、判断、信任、命名、口头区分与公开动作边界。 |
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

全站画布已经居中，但部分普通正文在限制为 700–760px 后仍保留左侧起点，剩余宽度全部堆在右侧，形成看似缺失内容的空栏。问题来自共享行宽与水平外边距没有共同定义，不是段落内容、浏览器缩放或单个页面模板造成。

当前共享样式把普通专题的 `content-stack`、`content-wide` 论述、`content-grid` 导语、`content-rows` 行组、目录页正文、手册阅读列和 FAQ 答案放在各自画布的居中阅读轴上。宽表格、流程、卡片、代码和对象映射继续使用完整可用宽度；带真实图形、摘要职责或双栏论证的引言、`content-split`、`content-band` 和时间线保留其结构，不把有内容的第二栏误判为空白。

Chrome 背景测试组逐页测量 `sitemap.md` 登记的 73 个正式页面：受限阅读列的左右空间均保持对称容差，整页横向溢出为零。共享 CSS 契约同时进入站点回归，后续页面不再依赖逐页补丁。

## 软件 Agent 身份与责任链复核 · 2026-07-15

现有 AUT-CORE 已经分开请求主体、实际行动者和被代表主体，但公开资料仍常用一个 Agent 名或服务账户指代模型、软件定义、认证工作负载和精确运行副本。多模型路由、弹性副本、服务账户委托、企业 MCP 接入和跨 Agent handoff 会让这种简写失去审计能力：认证成功不能说明哪一个实例发起动作，也不能证明被代表主体授予了该动作。

当前说明改为九个职责层次：模型、Agent 定义、部署、工作负载、运行实例、会话、凭据、主体委托和一次动作。身份、认证、授权与责任分别判断；实际行动者需要关联工作负载、运行实例、Dromen 与调用，委托需要保留中间行动者并绑定精确活动。公开页面使用这些直白短语，不引入新造词或读音负担。

这项调整没有建立 Agent 身份目录、凭据格式、责任制品、身份服务或运行时，也没有修改 AUT-CORE。NIST 2026 概念工作仍是研究问题，SPIFFE 只提供工作负载身份基础，MCP 企业管理授权只集中组织接入；精确物理绑定仍需真实消费者、协议 Profile、规范字节和对抗验证。

## 外部技术依据复核 · 2026-07-15

外部资料只支持具体机制，不进入 Noemion 的规范身份。任何适配都必须固定版本、保留原始输入身份，并在外部规范升级时重新验证。

| 权威资料 | 当前观察 | 采用的机制 | 明确排除 | 重新复核触发条件 |
| --- | --- | --- | --- | --- |
| ISO 704:2022、GNU Names、MCP Tools、A2A AgentSkill、NIST transitive closure、W3C PROV-DM 与 RFC 9334 RATS | 术语工作分开对象、概念、定义和指称；工程名称应提供有用意义；机器标识、可读名称、描述和 schema 可以分开；传递闭包、provenance bundle、Evidence、Attestation Result 与依赖方决定各有边界 | 在冲突和读音门禁之前增加专名必要性门禁；非规范提案比较直白对象名、信任角色和普通动作，并保留闭包、证据、会话、权限和结果分离 | 不因词源、稀有拼写或词族整齐保留专名；不把 bundle 当完整依赖闭包；不把 evidence record 当真实性、充分性或最终决定；不提前改现行接口 | 用户接受去专名化方向、人类职责与口头验证形成证据，或标准术语、真实消费者和 CLI 任务发生变化 |
| ELF gABI、GNU Binutils 2.46.1 发行与 2.46 手册 | 项目页列出的最新发行是 2.46.1，在线手册标注 2.46；`readelf` 独立于 BFD，BFD canonical form 可能丢失格式特有信息 | 非规范适用性矩阵已把结构/装载、符号/绑定、形成映射、裁剪/伴随关系、Build ID 和独立读取归还现有规范 | 自然语言 ELF、机器地址、弱符号、默认版本、环境搜索、静默裁剪、BFD 通用内部表示和带错可信输出 | GNU 发行或手册、ELF gABI、Endem/Synem 物理编码，或真实裁剪与调试消费者变化 |
| ELF gABI、RFC 8949、in-toto Attestation 1.2、TUF 1.0.27、DSSE、GNU Guix 与 MCP 2025-11-25 | ELF 以显式关键标志控制未知内容拒绝；确定性 CBOR 需要协议冻结具体形式；供应链陈述、签名包络、授权元数据和会话授权分别绑定对象与语境 | END-P1 的封闭关键结构、确定性编码、Endem 内容身份与外部授权伴随分离、精确对象与政策绑定 | 权威名称、签名、证据、任务状态或界面接受直接成为内容、授权、满足或最终决定 | 授权伴随物理 Profile、签名 Profile、外部协议版本或 END-P1 结构变化 |
| MCP 2025-11-25 当前修订（Current）与 2026-07-28 候选版 | 截至 2026-07-15，2025-11-25 仍是 Current；官方已于 5 月 21 日锁定并公开以计划最终发布日期命名的候选版，最终版计划于 7 月 28 日发布 | 版本化外缘适配、错误来源分离、最小能力、受众校验、拒绝和观察记录；候选版只作为漂移证据 | 服务器说明、工具 schema、OAuth 身份、`isError` 和远端结果都不能直接成为本地授权、满足或验收事实；候选版不能冒充当前符合性基线 | 候选版转为最终版，或授权、传输、工具结构变化 |
| GNU GCC 诊断、SARIF 2.1.0 与 RFC 9457 | 同一失败可以拥有稳定规则身份、类型化位置、机器出口与人类解释；问题类型和具体发生应分开，错误响应可能泄密 | DIA-CORE 的机器码与消息分离、生产语境、位置、主错误、外部来源、最小披露与有界输出 | 不复制编译器严重度，不把 HTTP 状态、SARIF 或消息文本当作本地结果与权限 | 诊断物理编码、CLI/SARIF/MCP 映射或稳定 ABI 被提出时 |
| A2A 1.0 | Task、Message、Artifact、多协议绑定和主次版本协商服务跨系统交换；Agent Card 可以使用 JWS 签名 | 交换带来源的任务状态、消息和候选产物，核对声明发布者 | 不让补丁号进入协议协商；不让签名 Agent Card 自动成为语义权威；不让外部 Task/Artifact 成为 Endem 身份、生命周期或最终决定 | A2A 主次版本、任务状态机、安全对象或签名规则变化 |
| MCP 2025-11-25 Lifecycle/Tools、A2A 1.0、RFC 8707 与 GNU Autoconf 2.73 | 协议能力、动态工具列表、自描述技能、scope、目标资源、具体特性探测和调用结果属于不同阶段；声明支持仍可能未配置或此刻不可用 | 非规范研究提案分开能力声明、协议协商、授权决定、Dromen 会话上限、即时可调用性与调用事实，并把唯一义务归还现有规范 | 不创建 `CAP-CORE`、能力制品或新专名；不让 Agent Card、schema、签名、scope、版本、缓存探测、端点健康和一次成功调用成为完整授权、持续可用、`met` 或 `accepted` | 用户接受责任分配，或动态发现缓存、具体 MCP/A2A Profile、Drasor 能力门、健康与配额策略被提出时 |
| MCP 2025-11-25 Tasks 与 Sampling 草案、A2A 1.0、GNU Make jobserver 与中断处理、RFC 9110 | 并行任务、模型工具请求、外部 Task、共享 job slot、取消和强前提各有边界；完成顺序与取消都不能撤销已经发生的外部效果 | 非规范研究提案分开分支准入、尝试、候选、提交、外部副作用与观察，要求共享 Dromen 上限、提交前重验与未知效果保留 | 不创建 `PAR-CORE`、并行制品、事务格式或新专名；不让最快完成、模型评分、Task completed、取消或多数一致成为提交权、`met` 或 `accepted` | 用户接受责任分配，或真实并行控制面、外部副作用提交器、MCP/A2A Profile 与调度证据被提出时 |
| MCP Security Best Practices 与传输规范、A2A 1.0、Linux no_new_privs/seccomp/Landlock/cgroup v2、GNU Guix shell、Coreutils timeout 与 Make jobserver | token 透传、SSRF、本地服务暴露、链式凭据、系统调用、文件、网络、资源、后代进程和日志秘密是正交风险；内核文档明确 seccomp 不是完整沙箱 | 非规范研究提案分开十个部署责任面，要求模型不接收原始凭据、控制不可用时对应能力关闭失败，并以配置、有效状态、对抗反例、能力专项和漂移形成证据 | 不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、部署对象或新专名；不让容器、seccomp、超时、配置标签或一次成功演示成为完整隔离证明 | 用户接受责任分配，或真实 Drasor、凭据代理、适配进程、平台拓扑与对抗验证获准设计时 |
| NIST AI 800-2 初稿、NIST AI 800-3、NeurIPS 2023、ICLR 2025、NeurIPS 2025、GNU Diffutils 与 Coreutils | 自动基准与模型裁判正在成为常用评测机制，但目的、协议设置、模型版本、位置、冗长、格式、自偏好、随机性、依赖、污染和统计外推都会改变分数含义 | 非规范研究提案分开九种评测事实，要求确定性检查优先、模型输出保持 `model-candidate`，并以偏差探针、人工校准、依赖审查、区间和漂移限定用途 | 不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品或裁判服务；不让一致率、多个模型票数、排行榜、模型置信度、固定种子或一次偏差探针通过成为满足、充分证据或最终接受 | 用户接受责任分配，或真实开放式评测、人工校准材料、模型服务 Profile、统计程序与发布决定被提出时 |
| NIST AI Agent Standards Initiative 与 Agent 身份授权概念工作 | 2026 年的 Agent 标准化重点已经明确覆盖身份、授权、安全和互操作；协议身份、代表关系、动作授权与目标满足仍是不同判断 | Agent 系统边界图面向开发者解释请求主体、实际行动者、被代表主体、对象、动作、受众和会话能力上限 | 不创建 Agent 身份制品或新 CORE；不把认证、Agent Card、协议握手或工具可达升级为动作授权、`met` 或 `accepted` | NIST 发布正式指南、身份授权 Profile，或项目提出真实 Agent 协议适配时 |
| NIST NCCoE Agent 身份授权概念论文、SPIFFE、RFC 8693、W3C PROV-DM、MCP 企业管理授权与 GNU Coreutils `id` | 模型、软件定义、工作负载、运行实例、凭据、主体、代表关系、活动和有效身份拥有不同生命周期；工作负载认证与组织接入都不能唯一定位一次动作 | 非规范研究提案分开九个身份与关系层次，要求实际行动者关联实例、会话和调用，委托绑定精确活动，并把唯一义务归还现有规范 | 不创建 Agent 身份 CORE、制品、目录、服务或新专名；不把产品名、服务账户、SVID、单点登录、令牌主体或不可变日志提升为逐动作授权和责任结论 | 用户接受责任分配，或 NIST 正式指南、工作负载身份 Profile、企业 MCP 接入、真实多副本或跨 Agent 消费者被提出时 |
| OpenAI Agents SDK 编排、RFC 8693、MCP 授权、A2A 1.0 与 GNU Make jobserver | handoff 与主管调用分配不同的答复所有权；委托要分开被代表主体与实际行动者；下游凭据需要绑定资源和受众；嵌套工作不能逃离顶层预算 | 架构指南新增开发者交接检查表，固定三类主体、控制方式、输入变换、能力与预算子集、凭据域、返回结果和证据责任 | 不创建 handoff 制品或新 CORE；不让控制权转移、历史过滤、令牌透传、子任务预算重置或下游 completed 成为授权、完整上下文、`met` 或 `accepted` | SDK 交接语义、OAuth 委托、MCP/A2A 授权 Profile，或真实 Drasor 多 Agent 实现被提出时 |
| NIST AI 600-1、NIST SP 800-218A、NeurIPS RLHF/DPO、Nature 递归生成数据研究、GNU Guix 与 Diffutils | 训练、微调和偏好优化会把数据与反馈变成新模型派生物；投毒、权利、合成数据递归、基础模型漂移、数值非确定性和评测污染都会改变更新含义 | 非规范研究提案分开十一种事实，要求精确数据与模型身份、训练活动、反馈资格、环境和随机状态、独立复现、行为评测、发布与监测分别记录 | 不创建训练或模型 CORE、制品、清单格式、平台或新专名；不让人工在环、模型评分、相同环境、固定种子、损失下降、流水线成功或回滚指针成为数据资格、模型安全、met 或 accepted | 用户接受责任分配，或真实外部训练服务、模型仓库、反馈采集、适配器发布、撤销与监测 Profile 被提出时 |
| GNU 自由软件定义、OSI Open Source AI Definition 1.0、Linux Foundation Model Openness Framework 与 OpenMDW 1.1、NIST AI 600-1 与 SP 800-218A | 软件用户自由、AI 首选修改形式、模型发布完整性、供应链来源、许可覆盖对象和技术复现回答不同问题；模型许可仍在快速演进 | 非规范研究提案分开十二种事实，要求逐对象披露 API、参数、代码、数据说明、数据、文档、许可、修改形式、复现和外部决定 | 不创建开放模型或许可 CORE、制品、分类器和新专名；不让 API、开放权重、公开仓库、Apache-2.0、OpenMDW、模型卡、SBOM、签名或外部等级成为全栈开放、自由、安全、met 或 accepted | 用户接受责任分配，或真实模型发行、外部许可选择、开放符合性审查与长期复核流程被提出时 |
| GNU SaaSS 分析与 AGPL 边界、MCP 2025-11-25 Sampling/Authorization、NIST AI 600-1 与 SP 800-218A、模型服务数据控制 | 软件许可、真实服务执行控制、数据外发、下游服务、导出和切换回答不同问题；协议可以调整模型与凭据的控制位置，但不能创造用户对托管实例的控制 | 非规范研究提案分开十六种事实，要求逐执行者、端点、功能、区域和截止点披露已知事实与未知内部路径，并让切换建立新身份、会话、评测和决定 | 不创建服务 CORE、网关、云平台、导出格式或新专名；不让 AGPL、Sampling、OAuth、数据驻留、零保留、API 兼容、导出或调用成功成为实例控制、完整复现、met 或 accepted | 用户接受责任分配，或真实托管模型消费者、自主管理部署、供应商政策、MCP Profile、导出与降级路径被提出时 |
| NIST Privacy Framework 1.0、NIST AI 600-1、NIST SP 800-88 Rev. 2、RFC 6973、W3C DPV 2.1、MCP Elicitation、GNU Coreutils `shred` 与 Guix 垃圾回收 | 访问、使用、披露、存储、保留、逻辑删除、介质清除、验证、确认、备份和派生物传播回答不同问题；协议和工具通常不能证明下游用途与物理残留 | [非规范研究提案](spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.md)分开十八种事实，要求按精确对象、目的、接收方、截止点、操作、介质、关系闭包、证据和未知范围陈述数据生命周期 | 不创建数据、隐私或删除 CORE、制品、服务和新专名；不让授权、TTL、逻辑删除、退出状态、供应商收据或训练退出成为全部副本不可恢复、历史从未处理、met 或 accepted | 用户接受责任分配，或真实数据政策、存储拓扑、下游服务、清除方法、训练数据去除和证据生产者被提出时 |
| OpenTelemetry 语义约定 1.43.0 与 GenAI 独立仓库 | 1.43.0 总入口已把 GenAI 与 MCP 内容指向独立官方仓库；截至 2026-07-15，独立仓库尚无发布版，README 的 Schema URL 字段仍为 `TODO`；输入、输出、工具参数和结果可能含敏感信息 | 形成可固定基线后使用带版本、默认脱敏、可替换的运行观测导出器 | 外部字段进入 Endem 编码、Iknem 身份或验收规则 | 独立仓库发布版本、Schema URL、字段稳定性或隐私建议变化 |
| W3C PROV、RFC 9334、SLSA 1.2 与 GNU Guix challenge | 溯源需要分开实体、活动和责任；证据、验证结果与依赖方决定是不同步骤；外部参数不可信；逐字节差异不能自行裁定哪份输出正确 | Iknem 的有限无环溯源、外部有效性评估、相对 krin 的覆盖度和决定权威分离 | 签名、证据数量、构建证明、差异或模型评分自动成为事实、充分覆盖或最终接受 | IKN-CORE Profile、撤销分发、透明日志或跨生产者归并被提出时 |
| RFC 6920、RFC 9052、DSSE、Sigstore Bundle、SLSA 1.2、GNU ld 与 Guix challenge | 完整摘要只绑定名称与字节；签名必须保护类型和关键上下文；key ID 只是提示；build ID 不是当前文件校验和；可复现性需要逐字节比较 | ID-CORE 的身份域、完整引用、有类型签名陈述、外置验证材料、权威分离、截止点与独立产出比较 | 摘要相同成为语义真值，签名或日志包含成为授权，短摘要或 build ID 选择对象，单次重跑成为可复现证明 | 发行算法、签名 Profile、证书、透明日志、撤销或 Semantic Key 被提出时 |
| RFC 3629、Unicode UAX #9/#15/#31、UTS #39/#55、RFC 8264 与 GNU libunistring | UTF-8 解码、规范化、标识符、双向显示、同形风险和文本处理属于不同职责；可见相同不等于字节、标量或意义相同 | TEXT-IDENTIFIER-CORE 的文本槽、严格解码、来源溯源、ASCII 标识符、显式比较域、范围、隐藏字符审查、模型输入与显示视图 | 盲目规范化来源、同形骨架合并身份、显示顺序参与解析、语言标签或模型相似度取得语义权威 | Unicode 版本、国际化标识符、来源字节字段、tokenizer Profile 或文本处理实现被提出时 |
| RFC 9396、RFC 8693、RFC 9470、RFC 9700、MCP、A2A、GNU Guix 与 GnuPG | 细粒度授权、委托与冒充、重新认证、受众限制、本地信任和 Agent 链式请求属于不同判断 | AUT-CORE 的完整语境、主体资格、封闭范围、委托收窄、同意绑定、重放防护、能力交集与结果分离 | scope、签名、登录、step-up、Agent Card 或界面点击自动成为语义或最终权威 | 权威目录、政策语言、授权事件编码、同意 UI Profile 或外部协议映射被提出时 |
| ELF 装载视图、Linux capabilities/no_new_privs/Landlock 与 MCP 会话授权 | 持久文件与动态运行表示不同；能力可以设置不可增长上界；任务与令牌必须绑定授权上下文和目标资源 | DRO-CORE 的一次会话主体、环境、能力交集、秘密外置、只读失效和销毁 | 把 Dromen 写成文件、进程映像或凭据包，或把 Linux 与协议名称当成隔离证明 | Drasor API、沙箱、凭据代理、预算计数器、事件编码或恢复机制被提出时 |
| RFC 3339 / RFC 9557、GNU 时间工具、W3C OWL-Time 与 OpenTelemetry Metrics | 绝对时刻、附加时区信息、单调经过时长、相对日期歧义、瞬间/区间/时长与遥测窗口分别有明确边界 | `fixed` UTC 半开区间、`elapsed` 具名事件与单调时钟、显式覆盖缺口、`strict/budgeted` 连续政策 | 默认本地时区、`now/tomorrow`、墙钟测量时长、离散采样冒充连续成立，或把外部时间类型直接写入 END-P1 | 时间 Profile、闰秒策略、跨重启关联、时区数据库封装或多生产者归并被提出时 |
| W3C OWL 2、SHACL、SPARQL 1.1、GNU grep 与 OpenTelemetry Logs | 开放世界中的未陈述不等于假；封闭约束、无匹配查询和无匹配文件都只对指定范围成立；日志区分发生时间与观察时间 | 同一关系的显式极性、空结果默认 `agno`、有限封闭范围与完整性责任 | 空日志、部分搜索、模型“未发现”或单条遥测记录成为普遍负事实 | 封闭声明 Profile、跨生产者完整性、迟到窗口、撤销传播或复合否定被提出时 |
| NIST AI RMF 与 GenAI Profile | AI RMF 1.0 正在修订；AIRC 继续把测试、评估、验证与确认作为风险管理资源 | 风险登记、具名责任、TEVV 和高风险模型/工具检查清单 | 风险框架定义 Endem 字段、合格阈值、ABI 或软件符合性 | AI RMF 修订版、GenAI Profile 或关键基础设施 Profile 正式更新 |
| OpenAI Model Spec、NIST AI 100-2e2025 与 CAISI、MCP 安全条款、GNU ld link map | 工具返回、引文和外部数据默认不能自行取得指令权；不可信内容与高信任提示拼接会产生劫持风险；上下文截断、工具注解、会话注入和装配损失必须显式处理 | 非规范研究提案已形成十四个案例、唯一责任归属、八类威胁和失败域矩阵；开发者指南把来源、用途、变换、截断、冲突、缓存和动作复核写成任务检查表 | 不复制供应商消息角色，不依赖模型自行识别注入，不把链接顺序、位置或标签当作权威，也不建立新制品或“自然语言链接器” | 用户接受责任分配，或模型、tokenizer、Drasor 控制平面、检索策略、上下文缓存与模型 SDK Profile 被提出时 |
| GNU Make、ReAct、A2A 1.0.0、MCP 2025-11-25 Tasks 与 OpenAI Agents SDK | target、依赖和 recipe 可以分离；Agent 会交替推理、行动、观察、handoff 和重规划；外部 Task 与轨迹各有自己的生命周期 | 非规范研究提案已形成十二个支持/反例、重规划矩阵、十类威胁和唯一责任归属；目标、计划、外部任务、证据与最终决定保持分离 | 不建立计划制品或 `PLAN-CORE`，不把 recipe、步骤、Task completed、handoff、轨迹或模型计划直接变成 Endem、met、Iknem 充分覆盖或 accepted | 用户接受责任分配，或计划需要跨会话身份、物理事件格式、具体 A2A/MCP Profile 与 Drasor 规划实现时 |
| W3C RDFC-1.0、RFC 8785、Unicode UAX #15、RFC 7950、GNU BFD/objcopy、GNU Guix challenge、OpenAI Structured Outputs、Sentence-BERT、LLM-as-a-Judge 与 NIST AI 800-3 | 规范化只在封闭对象域与关系中成立；跨格式和兼容规范化可能丢失信息；逐字节复现只比较精确输出；schema 合规只证明结构；模型相似度与裁判带有任务、模型、偏差和不确定度 | END-DET-001 已改用封闭形成输入；公开测试页分开来源变换、确定性形成、派生显示、回转/迁移与独立复现；非规范研究提案继续分开精确身份、结构同构、观察等价、迁移、强化/弱化和模型相似度 | 不建立通用等价布尔值、万能 Semantic Key、等价制品或迁移组件，不让回转成功、schema 合规、裁剪、迁移、相似度、签名、证据或相同结果继承身份、权限与接受状态 | 用户接受责任分配，或真实裁剪/迁移消费者、关系代数、跨 Profile 映射和正反向量出现时 |
| GNU Make、Kubernetes Controllers、W3C PROV、CloudEvents、OpenTelemetry、RFC 9110、ReAct 与 A2A | 终态、更新动作、活动、事件、操作状态、幂等与外部任务各有自己的语义；使用和生成链对派生仍然不充分 | 非规范研究提案已把终态满足、动作发生、状态转变、因果归因、授权责任与最终决定分开，并形成十六个案例、十二类威胁和唯一责任归属 | 不把后态成立、recipe、控制器调节、事件、Span Ok、幂等 no-op、模型自述或 Task completed 提升为动作、因果、责任、met 或 accepted | 用户接受 `kine` 的目标方向解释，或动作/转变关系、因果方法、观察 Profile 与真实 Agent 消费者被提出时 |
| GNU Make、MCP 2025-11-25、A2A 1.0.0、OpenAI Agents SDK 与 NIST AI 600-1 | dry-run 可能保留执行例外；敏感工具需要可拒绝的确认；批准后到执行前仍有时序漂移；人机配置存在自动化偏见与过度依赖 | 非规范研究提案已分开预览、模拟、授权、执行尝试、事后观察、满足和最终决定，并形成十二个案例、十类威胁和唯一责任归属 | 不把打印 recipe、模型计划、确认按钮、RunState、Task 状态、工具成功或人工在环标签提升为无副作用、持续授权、met 或 accepted | 用户接受责任分配，或真实高风险工具、同意 UI Profile、模拟方法、长时审批和正反向量被提出时 |
| OpenAI Agents SDK 对话状态策略、OpenAI Sandbox Agents 跨运行记忆、MCP 当前版与发布候选、A2A 1.0、GNU Make 与 GNU Guix | 对话历史、提炼指导、运行暂停、工作区恢复、外部 Task、流式续接、文件保留和 generation 回滚是不同机制；历史与记忆可能压缩、陈旧或缺失，通知可能重复，失败目标也可能残留 | 非规范研究提案已分开九类状态、继续/恢复/重试/重放/回滚/补偿，并形成十三个案例、十三类威胁和唯一责任归属；开发者指南新增跨会话恢复检查清单 | 不把 session、跨运行记忆、摘要、检查点、Task completed、缓存命中、保留文件或回滚提升为事实、证据、权限、完整历史、met 或 accepted | 用户接受责任分配，或持久记忆、检查点、跨设备恢复、具体 Tasks Profile、工作区快照与恢复实现被提出时 |
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

当前指南改为从一次工具调用回答五个问题：期望终态、实际行动者与代表关系、会话能力上限、外部系统实际报告、证据与决定。依赖升级案例继续把目标、授权、Dromen、包管理器退出码、Iknem、满足判断和最终决定逐项对齐。常见风险按越级机制合并，不再重复运行事实表中的每一行；评审结尾改为可以按顺序执行的检查步骤。

NIST AI Agent Standards Initiative 继续支持身份、授权、安全和互操作议题；NIST AI 800-2 明确保留初始公开草案状态；MCP 2026-07-28 仍是计划于 7 月 28 日定稿的候选版；A2A 1.0 继续分开 Task、Message、Artifact、版本和授权；GNU Make 继续分开 target、prerequisite、recipe、并行配额与中断后的目标状态。这些资料只校验分层方法和时效，不直接定义 Noemion 字段或结果。

语言规范同时增加两项质量约束：综合指南先给正向判断顺序或具体案例，再列禁止事项；研究、趋势和风险标题不写死会漂移的清单数量。测试改为核对职责覆盖和案例链，不再要求保留阶段性计数。

## Endem 基础规范学习路径复核 · 2026-07-15

Endem 规范说明是开发者理解整个项目的基础页面，却直接从定义进入标准分层、六字段表、五类结果和完整场景清单。页面逐行复制 END-SCEN 的非规范语料，既造成高密度否定句，也让代表性教学与版本化案例库承担相同职责。后段继续以“状态机”描述 <code>nascent / coherent / attested</code>，没有像生命周期页那样先说明精确内容与外部陈述是两条不同的轴。ADR-0011 还残留内部工作包标签。

当前页面先用“让登记服务返回健康状态”贯穿来源表达、意义投影、事态、目标方向、满足判据和未决意义，再进入精确定义。场景表改为按开发者问题选择代表案例，完整案例、反例与向量继续由 END-SCEN 保存。形成分类同时明确标出 <code>attested</code> 的现行草案限制，并用“精确内容身份 + 外部陈述 + 验证政策与截止点 + 撤销 + 依赖方判断”解释会话准入；这只是修正读法，不提前改变现行规范值。页面还明确说明字段职责已进入草案，而发行拼写和读音仍在研究。

[GNU 文档规范](https://www.gnu.org/prep/standards/html_node/Documentation.html)要求完整文档同时承担教程与参考职责，[GNU 的手册写作说明](https://www.gnu.org/prep/standards/html_node/Doc-Strings-and-Manuals.html)也反对把孤立条目拼成重复手册。RFC 9334 分开 Evidence、Verifier 产生的 Attestation Results 与 Relying Party 政策；in-toto Statement v1 用摘要绑定不可变 subject；SLSA 1.2 VSA 继续显式保存 verifier、policy、input attestations 和 verification result。这些来源支持教学顺序与外部关系分层，不定义 Endem 字段，也不授权迁移 <code>attested</code>。

全站质量规则因此补充一项约束：规范解释页先给贯穿案例，再选择能区分失败域的代表场景；非规范语料和向量留在版本化权威源。正式 HTML 同时禁止出现内部工作包标识。

## 三个组件的开发者学习路径复核 · 2026-07-15

组件总览此前把 Ktisor 简写为“执行投影”，容易让读者误以为形成器可以代替有权主体选择意义；Ktisor 正文还使用“规范化”和单一“状态机”概括形成责任，与未声明文本规范化不得参与身份比较、内容身份和外部陈述分轴的规则不一致。Theor 与 Ktisor 都缺少具体输入到输出的示例。Drasor 则用多个连续章节重复时间、否定、量化、测量、复合与 Synem 的规范细节，开发者在看到实际能力请求前必须先穿过对象定义清单。

当前组件页统一采用“职责名称（设计阶段名称）”和依赖更新案例。Ktisor 只根据已授权投影确定性形成制品，不自行解释来源；Theor 用独立代码读取同一不可信字节，并把分歧送回规范调查；Drasor 先封闭一次 Dromen，再让模型提出类型化请求，由控制面授权、适配器执行、Iknem 保存实际观察，最后分开满足结果、会话结果与具名权威决定。时间、负观察和聚合等细则继续由 Endem 与 Iknem 规范承担，不在运行器页面复制。

外部资料也按当前成熟度复核：NIST AI Agent Standards Initiative 支持把互操作、身份、授权和安全评估视为独立问题；MCP 2025-11-25 继续要求资源绑定并禁止 token passthrough，2026-07-28 在本次审计日期仍是候选版本；A2A 1.0 的 Task 终态不替代本地满足判断；OpenTelemetry 1.43.0 已把 GenAI 语义约定移入独立仓库，且多项字段仍标为 Development。GNU Coreutils、Make 与 Guix 只提供终止、有限并发和先隔离后开放资源的工程先例，不构成 Drasor 安全实现证据。

这项修订没有新增组件、命令、Profile、物理格式或实现承诺。三个名称的读音流畅度、口头区分度和发布拼写仍需真实使用者验证，因此公开页先说职责，再给设计阶段名称。

## 组合、会话与证据规范学习路径复核 · 2026-07-15

Synem、Dromen 与 Iknem 三个核心说明页此前都直接从定义进入规则表。开发者能够查到条款，却无法用同一个现实任务判断对象为什么分开、会话边界在哪里、某条观察究竟能支持什么。Iknem 还把原始观察到结构化关系之间的步骤概括为“规范化与有损变换”，与项目要求的封闭对象域、显式算法和损失记录不一致；资料索引又出现在最低职责之前，打断了首次阅读路径。

当前三页统一使用依赖升级与服务发布案例：两个可独立失败和接受的终态形成 Synem；Drasor 再为精确闭包、当前政策、环境、能力、预算和观察责任建立一次 Dromen；锁文件摘要、部署响应、健康探针与模型解释分别形成有范围候选，只有对齐精确主体、方法、环境、时间和关系后才可能进入 Iknem。三页先给直白职责，再给设计阶段名称，并明确读音流畅度与相邻名称的口头区分度尚未经过真实使用者验证。

IKN-OBS-001 同步把“规范化步骤”改为实际执行的解析与变换，要求选择、过滤、聚合、换算、舍入、脱敏与模型解释绑定算法或方法版本及信息损失。该修改没有增加 Iknem 字段、物理格式或新结果域，只消除可能掩盖处理步骤的含糊术语。

外部资料基线同时补全。[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)已经把 GenAI 与 MCP 内容指向独立官方仓库；截至本次复核，独立仓库仍没有发布版，README 的 Schema URL 字段仍为 `TODO`。因此正式页面同时引用总入口与独立仓库，并继续要求精确版本、默认脱敏和可替换导出；迁移状态、仓库活跃或字段存在都不能成为稳定 schema、Iknem 身份、满足结果或最终决定。

这项修订没有新增组件、命令、Profile、运行时、物理格式或兼容入口。规范案例只解释当前条款，完整场景与提案向量仍由版本化源文件保存。

## 重新审计条件

- 新增正式制品、子命令、进程或仓库。
- 冻结编码、ABI、扩展 registry 或签名 profile。
- 第一次发布 Endem Ktisor、Theor、Drasor 或规范版本。
- 接入模型、MCP/A2A、远端能力或外部签名服务。
- 页面不再能明确区分候选、决定和证据，或路由开始为历史兼容而膨胀。
