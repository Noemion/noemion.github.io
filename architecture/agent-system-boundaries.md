---
layout: content
title: Agent 系统边界图 · Noemion
page_role: content
footer_text: Noemion · Agent 系统边界图
permalink: "/architecture/agent-system-boundaries.html"
summary: 沿一次工具调用分开目标、行动者、授权、会话、外部事实、证据与最终决定。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 架构设计
  url: index.html
page_heading: Agent 系统边界图
page_lead: 一次 Agent 调用会同时产生目标、身份、授权、会话、协议状态、观察和决定。开发者必须分别保存这些事实，不能用一个“成功”状态概括整条责任链。
badges:
- 非规范说明
- 开发者路径
- 尚无运行组件
- 复核于 2026-07-16
previous_url: decisions.html
previous_label: 架构决策
next_url: open-questions.html
next_label: 开放问题
---

## 用一次依赖升级完成边界判断

假设一个 Agent 要把仓库依赖升级到经过允许的新版本。目标是兼容且可验证的仓库状态，编辑文件、调用包管理器和运行测试只是实现路径。开发者按下面的顺序记录一次调用，任何一步缺失都只停止对应结论。

1. 目标内容
2. 行动者与授权
3. 会话上限
4. 外部调用
5. 观察与证据
6. 满足判断
7. 最终决定

| 阶段 | 本例需要固定什么 | 失败时怎样处理 |
| --- | --- | --- |
| 1. 目标内容（Endem / closure） | 期望版本、兼容条件、验证判据、依赖闭包和仍未解决的意义 | 目标含义未确认时停止形成；计划和可变步骤不进入目标身份 |
| 2. 行动者与授权 | 请求主体、实际行动者、被代表主体、仓库、分支、依赖、允许版本、目的和截止点 | 登录、Agent 名称、工具清单或 scope 不能补齐逐动作授权 |
| 3. 一次会话的上限 | 实际目标制品、政策、环境、文件、网络目标、工具、能力交集、预算和证据责任 | 环境或授权实质变化时开始新会话；后来发现的能力不扩写旧 contract |
| 4. 外部调用与错误 | 协议与对端版本、包管理器请求、退出码、远端 Task、错误、取消、重试和已知副作用 | 保留外部状态和未知副作用；退出码为零或 Task 完成只说明该次外部调用 |
| 5. 观察与证据（structured_observation / evidence） | 锁文件差异、构建结果、测试范围、来源限制、方法、环境和未观察区域 | 证据只支持声明范围；日志数量、Span Ok 或模型评分不能补齐覆盖缺口 |
| 6. 满足判断（satisfaction_criteria） | 精确目标、适用观察、判据和四值结果 | 外部成功不直接成为 `met`，观察不足继续保留为 `undetermined` |
| 7. 最终决定（具名权威） | 适用政策、证据范围、风险容限、决定者和决定时间 | 评测者、协议对端、工具或模型都不能自行产生 `accepted` |

并行尝试多个版本时，各分支只产生候选。提交路径仍要重新核对当前分支、授权、预算和副作用；取消慢分支不证明远端工作已经回滚。

## 六类问题由不同责任域回答

开发者不需要为每个 SDK 名词建立新对象。先问事实回答什么，再把它交给现行责任域。

| 开发者问题 | 现行责任域 | 需要保留的事实 | 结论边界 |
| --- | --- | --- | --- |
| 期望终态是什么？ | Endem / closure | 目标身份、依赖闭包、方向、判据和待确认意义 | 目标不保存工作流、提示词或执行计划 |
| 目标只要求结果，还是还要求动作、转变或因果？ | Endem / evidence | 结果型目标只判断后态；更强主张还要绑定动作、同一对象的前后态、竞争活动、方法和限制 | 时间先后与单一轨迹不自动形成因果结论 |
| 谁代表谁执行什么动作？ | 精确身份与授权决定 | 模型、Agent 定义、工作负载、运行实例、实际行动者、被代表主体、对象、动作和目的 | 名称、认证、签名和能力声明只是授权输入 |
| 本次运行最多能做什么？ | contract / 外部协议适配 | 协议、对端、环境、能力交集、预算、凭据域和证据责任 | 发现、协商与可调用性不扩大已封闭会话 |
| 外部系统实际报告了什么？ | 外部协议适配 / 结构化诊断 | 精确调用、Task、Message、Artifact、返回、错误、取消、交付和副作用 | 外部状态保持在外部域，不提前改写本地结果 |
| 什么证据支持哪项结论？ | evidence / 目标判据 / 授权决定 | 观察范围、方法、限制、有效性、覆盖度、满足判断和具名决定 | 证据记录、满足判断与最终决定分别保留输入和权威 |

> 当前策略让目标、组合、一次会话、证据、诊断、外部协议、精确身份、文本解释与授权分别承担自己的责任。控制平面、适配器、存储、隔离和运行组件尚未实现。

## 先识别越级，再定位缺失事实

| 越级路径 | 常见输入 | 应当补查什么 |
| --- | --- | --- |
| 候选上下文取得指令权 | 检索片段、网页、工具返回、历史对话或模型摘要进入上下文后被当作命令 | 来源、文本变换、目标意义确认、动作授权和实际模型输入 |
| 显示名称或能力声明替代授权 | Agent 名称、Agent Card、工具列表、schema、scope、签名或工作负载身份 | 实际行动者、代表关系、精确对象、动作、目的、期限和决定权威 |
| 运行状态替代目标判断 | HTTP 成功、handoff、MCP/A2A Task 完成、退出码为零或 SDK completed | 状态来源、映射损失、适用观察、目标判据和本地结果域 |
| 记忆、检查点或轨迹替代当前事实 | 过期指导、恢复句柄、工作区快照、Span Ok 或日志数量 | 当前政策、重新准入、能力有效性、历史完整性、因果方法和覆盖缺口 |
| 隔离机制名称替代有效限制 | 容器、沙箱、seccomp、超时或“本地运行”标签 | 文件、网络、秘密、资源、终止、子进程、远端效果和信息流的实际覆盖 |
| 单项信号替代完整结论 | 模型评分、训练损失、开放权重、AGPL、导出成功或删除收据 | 评测总体、数据资格、对象范围、实例控制、数据路径、备份和派生物 |

无法取得某项事实时，记录未知范围并停止依赖它的结论。产品名称、协议状态和机制标签不能替开发者推定缺失信息。

## 外部生态改变输入，不改变责任

截至 2026-07-16，Agent 框架和协议继续把委托、审批、状态、任务、身份和观察显式化。这些机制提高了可追踪性，但不会自动取得 Noemion 中的语义、授权或决定权威。

| 外部变化 | 官方资料说明什么 | Noemion 怎样接入 |
| --- | --- | --- |
| 控制权转移与人工批准 | [OpenAI Agents SDK 编排说明](https://developers.openai.com/api/docs/guides/agents/orchestration)分开 handoff 和由管理者把 Agent 作为工具调用；[人工参与机制](https://openai.github.io/openai-agents-python/human_in_the_loop/)允许在工具审批前暂停并恢复运行。 | 答复所有权、运行暂停和动作授权分别记录；批准必须绑定安全显示后的精确请求。 |
| 会话、记忆与轨迹 | [Agents SDK 会话策略](https://developers.openai.com/api/docs/guides/agents/running-agents#choose-one-conversation-strategy)、[跨运行记忆](https://developers.openai.com/api/docs/guides/agents/sandboxes#persist-memory-across-runs)和[运行轨迹](https://openai.github.io/openai-agents-python/tracing/)分别保存不同状态。 | 每类状态绑定身份、期限和来源；记忆与快照不恢复旧 contract，trace 只作为有范围观察。 |
| 协议任务与动态能力 | [MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 2025-11-25 标为 Current；[2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)含破坏性变化且计划于 7 月 28 日定稿。[A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)仍是最新发布规范。 | 适配 Profile 固定正式版本、绑定和对端。能力声明只参与交集；Task、Message 和 Artifact 保持外部身份。 |
| Agent 身份、安全与互操作研究 | [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)分别推进产业标准、开放协议、身份和安全评测；[NIST AI 800-5](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai)汇总 Agent 安全征询意见，不是实现规范。 | 身份、授权、协议符合性和安全证据继续分开；研究共识不能替代项目条款或组件测试。 |

## GNU 先例只提供工程约束

| 工程问题 | GNU 先例 | 使用上限 |
| --- | --- | --- |
| 目标、依赖、步骤和预检怎样分开？ | [Make target、prerequisite 与 recipe](https://www.gnu.org/software/make/manual/html_node/Rule-Syntax.html)，以及[dry-run](https://www.gnu.org/software/make/manual/html_node/Instead-of-Execution.html)和[Autoconf 特性检查](https://www.gnu.org/software/autoconf/manual/autoconf.html) | 目标不保存可变步骤，外部工具在使用前核对特性；文件时间、预览和配置探测不定义 Endem 或授权。 |
| 并行、中断和有限预算怎样处理？ | [Make 并行与 jobserver](https://www.gnu.org/software/make/manual/html_node/Parallel.html)、[错误处理](https://www.gnu.org/software/make/manual/html_node/Errors.html)和[中断处理](https://www.gnu.org/software/make/manual/html_node/Interrupts.html) | 嵌套工作共享有限配额，中断后的目标按可能不完整处理；job slot 不是授权，取消也不是副作用回滚。 |
| 环境、版本和恢复对象怎样具名？ | [Guix profile generations](https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html)、[Guix shell、channel、manifest 与 time-machine](https://guix.gnu.org/manual/devel/en/guix.pdf) | 软件闭包和恢复目标可以复核；配置回滚不恢复凭据、外部状态或旧 contract，相同环境也不证明模型行为等价。 |
| 差异、随机性和终止怎样观察？ | [GNU Diffutils](https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html)、[随机来源](https://www.gnu.org/software/coreutils/manual/html_node/Random-sources.html)、[sort](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)与[Coreutils timeout](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html) | 分别保留相同、不同、比较故障、随机输入和终止结果；固定种子或主进程退出不能选择正确结果。 |
| 软件自由、服务控制和数据清除怎样分开？ | [GNU 自由软件定义](https://www.gnu.org/philosophy/free-sw.en.html)、[服务替代用户计算的分析](https://www.gnu.org/philosophy/who-does-that-server-really-serve.html)、[AGPL 边界](https://www.gnu.org/licenses/why-affero-gpl.html.en)与[Coreutils `shred`](https://www.gnu.org/software/coreutils/manual/html_node/shred-invocation.html) | 逐对象检查权利、执行者、实例控制、数据路径和存储介质；源码、许可或清除命令都不能概括整个托管系统。 |

> 这些资料帮助构造工程反例，不定义 Noemion 字段、结果域、协议 Profile 或伦理结论。

## 遇到更强问题时再进入研究
{: #research-map}

现行责任足以处理一次普通工具调用。只有问题要求更强主张时，才进入对应非规范提案。

| 更强问题 | 继续阅读 | 当前停止条件 |
| --- | --- | --- |
| 哪些来源进入模型，目标与计划怎样分开，迁移后是否仍是同一语义？ | [模型上下文装配](https://noemion.github.io/spec/model-context-assembly-proposal.html)、[目标、计划与重规划](https://noemion.github.io/spec/planning-and-replanning-proposal.html)、[语义等价与迁移](https://noemion.github.io/spec/semantic-equivalence-and-migration-proposal.html) | 候选输入、计划和等价主张继续由现有文本、身份、目标、会话与证据责任处理。 |
| 谁在行动、当前能做什么、并行分支怎样提交、隔离失效时谁负责？ | [能力发现、协商与调用](https://noemion.github.io/spec/capability-discovery-and-negotiation-proposal.html)、[软件 Agent 身份与责任链](https://noemion.github.io/spec/software-agent-identity-and-accountability-boundaries-proposal.html)、[并行与推测执行](https://noemion.github.io/spec/parallel-and-speculative-execution-proposal.html)、[模型、适配器与能力域隔离](https://noemion.github.io/spec/model-adapter-isolation-proposal.html) | 能力、身份、授权、会话和协议保持分开，不创建通用 Agent 权限对象。 |
| 动作是否发生、预览是否可信、恢复了什么、模型评审能支持什么？ | [状态变化与因果归因](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html)、[预览、模拟与批准](https://noemion.github.io/spec/preview-simulation-and-approval-proposal.html)、[记忆、检查点与恢复](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html)、[模型参与评测](https://noemion.github.io/spec/model-assisted-evaluation-proposal.html) | 动作、后态、因果、恢复状态、候选测量和最终决定分别保留证据。 |
| 反馈能否训练，更新后的模型怎样发布，数据何时真正删除？ | [模型训练与更新边界](https://noemion.github.io/spec/model-training-and-update-boundaries-proposal.html)、[数据使用、保留与删除边界](https://noemion.github.io/spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.html) | 反馈、用途授权、模型派生、评测、发布、保留和清除不压成一条状态线。 |
| 模型开放到什么程度，用户能否控制实际服务与数据路径？ | [模型开放性与软件自由边界](https://noemion.github.io/spec/model-openness-and-software-freedom-boundaries-proposal.html)、[托管人工智能服务与用户控制边界](https://noemion.github.io/spec/hosted-ai-service-and-user-control-boundaries-proposal.html) | 对象权利、复现范围、实例控制、数据路径和退出能力分别陈述。 |

### 完成一次边界评审

1. 写下期望终态，并说明是否还要求动作、状态转变或因果。
2. 固定请求主体、实际行动者、被代表主体、对象、动作、目的和截止点。
3. 封闭会话的环境、能力交集、预算、凭据域和证据责任。
4. 保留工具、handoff、Task、取消、重试、交付和副作用的外部身份。
5. 让证据只支持声明范围，再分别形成满足结果与最终决定。
6. 看不见的事实记录为未知，不用机制名称或产品声明补齐。

只有一项责任同时具备现有对象无法表达的身份与不变量、独立生命周期、真实生产者和消费者，以及可重现的失败责任，才值得讨论新对象。当前研究主题均未达到这一条件。

- [架构决策](decisions.html) — 查看现行责任和待定接口。
- [开放问题](open-questions.html) — 查看研究提案仍需关闭的证据。
- [外部协议适配](../specifications/adapters.html) — 查看版本、能力、任务、重试和交付边界。
- [权威与授权决定](../specifications/authority.html) — 查看主体、委托、同意、撤销和能力交集。
- [会话契约（contract）](../specifications/session-contract.html) — 查看一次运行怎样封闭环境、能力、预算和证据责任。
