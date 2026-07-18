---
layout: architecture-decision
title: ADR-0008 · Endem 与单一入口（历史记录）
page_role: content
footer_text: Noemion · ADR-0008
permalink: "/architecture/adr-0008-endem-system.html"
summary: 解释项目为什么保留 Endem、.endem 和单一应用入口，以及旧对象、字段和动作为什么不再属于现行接口。
decision_id: ADR-0008
page_heading: ADR-0008 · Endem 与单一入口 · 历史记录
page_lead: 解释项目为什么保留 Endem、.endem 和单一 endem 应用与命令入口；旧对象、字段、状态和动作均不再构成现行接口。
badges:
- 历史记录
- 部分保留
- 当前边界另有依据
- 尚无组件
next_url: adr-0009-propositional-kernel.html
next_label: ADR-0009
---

## 先确认这份记录还能约束什么

开发者只能从 ADR-0008 继承三项结果：核心制品继续称为 Endem，文件扩展名继续使用 `.endem`，项目只提供一个名为 `endem` 的应用与命令入口。

| 阅读内容 | 当前效力 | 现行依据 |
| --- | --- | --- |
| Endem、`.endem` 与单一 `endem` 入口 | 继续有效，但仍是设计阶段名称与接口边界 | [ADR-0010 语义职责](adr-0010-native-lexicon.html)、[ADR-0035 公开动作](adr-0035-public-actions-and-internal-responsibilities.html) |
| 旧制品、运行对象和五组字段 | 已经取代，不是别名，也不能进入新文件或 API | ADR-0010 的六个语义面，以及 CLOSURE-CORE、SESSION-CORE、EVIDENCE-CORE |
| 旧内容状态和签名内嵌关系 | 已经取代；内容形成、外部陈述、验证和决定必须分开 | [ADR-0015 结果分层](adr-0015-result-domains.html)、[ADR-0036 发布边界](adr-0036-source-bearing-and-stripped-release.html) |
| 旧命令清单 | 已经取代，不提供兼容命令或重定向 | ADR-0035 的 `ktise / elenk / pleko / theor / drase` |
| 实现状态 | 当前只有规范、ADR、威胁、场景和向量资料 | 没有 CLI、解析器、形成器、独立检查器或运行时 |

> **阅读限制：**历史名称只用于解释设计来路。它们不能反向约束当前字段、动作、结果、Profile、ABI 或实现。

## 它当时解决了什么问题

早期设计为每一层建立对象和命令，开发者必须先理解内部组件数量，才能表达一个目标。ADR-0008 把用户入口收敛为一个目标制品和一个应用表面，这是仍然有效的改进。

以“把服务依赖更新到批准版本，并在测试通过后发布”为例，用户只需要提交一个可判断的目标。形成、生产侧检查、独立读取、组合和受限运行可以共享入口，但仍要由不同的信任职责承担。ADR-0008 的问题在于，它随后又为中间阶段创造了对象、状态和动作，并把外部签名写进内容状态；后续决定已经拆开这些责任。

| 早期材料 | ADR-0008 当时保留的判断 | 当前怎样处理 |
| --- | --- | --- |
| ADR-0001 与 ADR-0005 的对象和命令词表 | 减少并列产品，统一用户入口 | 只保留 Endem、`.endem` 和单一入口；当前动作由 ADR-0035 另行确定 |
| ADR-0002 与 ADR-0004 的控制和候选边界 | 模型候选不等于事实，能力声明不等于实时权限，证据不等于接受 | 分别由 AUT-CORE、SESSION-CORE、ADP-CORE 与 EVIDENCE-CORE 约束 |
| ADR-0003 的多制品流水线 | 减少没有独立消费者的中间制品 | 只保留最小目标、组合闭包、一次会话契约和有范围证据的独立责任 |
| ADR-0006 与 ADR-0007 的结构和纵向切片 | 安全读取、显式引用、受检算术和差分检查继续必要 | 格式改由 END-FMT 与 END-P2 约束；未来实现仍须单独授权 |

## 当前架构保留了哪些原则

| 保留原则 | 开发者怎样应用 | 不能推出什么 |
| --- | --- | --- |
| 一个目标先形成一个 Endem | 先保存来源，再确认意义投影、一个根事态、目标方向、判断方法和未决问题 | 自然语言或模型 JSON 本身不是 Endem |
| 一个应用入口不等于一个信任域 | `endem` 只负责分派当前五个设计动作；确定性生产、独立读取和受限运行继续隔离 | 共享命令名不能证明共享解析器、写权限或运行权限是安全的 |
| 模型只提出候选 | 具名主体确认意义，确定性生产边界形成规范字节，运行前重新核对动作授权 | 模型不能决定字段、删除未决问题、扩大能力或作出最终接受 |
| 独立读取用于发现共同故障 | independent inspector 直接读取实际字节，不复用 deterministic producer 的形成侧解析代码，也不写回制品 | 一次检查通过不能证明目标满足、证据充分或发布获准 |
| 形成、发布和外部陈述保持分离 | 形成版保留自然语言；未来发布版按独立 Profile 移除原文并取得新身份；签名留在外部关系 | 裁剪、签名或协议完成不能继承原对象的证据、授权和接受状态 |

## 旧名称为什么不能继续使用

| 历史表达 | 被取代的原因 | 当前阅读入口 |
| --- | --- | --- |
| Weave、Frame、Witness | 名称无法让首次读者恢复闭包、会话和证据责任，也容易把运行视图误写成持久对象 | [Endem closure 组合闭包](adr-0021-synem-closure-and-activation.html)、[session contract 会话契约](adr-0024-dromen-session-contract.html)、[evidence entry 有范围证据](adr-0022-iknem-evidence-and-appraisal.html) |
| `say / aim / must / done / open` | 五组字段把来源、事态、目标方向、判断和未知压在一起，不能逐项映射到现行结构 | ADR-0010 的 `source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning` |
| `open / bound / sealed` | 旧状态把引用解析、发布锁定和外部签名放在同一条内容状态线上 | 内容形成、精确身份、外部陈述、验证、满足判断和最终决定分别处理 |
| `form / check / bind / pack / seal / see / run / test` | 动作数量跟随内部步骤，不都具有独立用户任务；普通词本身不需要完整人类读音实验 | 现行公开动作由 ADR-0035 定义；旧命令不构成别名 |
| Runner | 一个通用运行者无法说明会话契约、能力交集、秘密隔离和失败责任 | 受限运行边界（bounded runner）与一次会话契约（session contract） |

名称退出不是职责治理的替代品。现行普通职责词已经按词首、职责和关键字语料接受；Noemion 与 Endem 两个自造名称仍须取得目标语言的首次朗读、听写回填和词表内口头区分证据。历史词较顺口或较常见，不能使它重新成为接口。

## 外部资料怎样限定这份历史记录

| 资料与复核基线 | 支持的局部原则 | 不支持的推导 |
| --- | --- | --- |
| [GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html) | 资料按用户面对的问题组织，而不是照抄程序结构或功能清单 | 内部存在一个步骤，就必须增加一个用户对象、页面或命令 |
| [GNU `readelf`](https://www.sourceware.org/binutils/docs/binutils/readelf.html)<br>[BFD 信息损失](https://sourceware.org/binutils/docs/ld/BFD-information-loss.html) | 独立读取路径可以避开共同实现故障；跨表示转换必须声明无法保留的信息 | 复制 Binutils 的程序数量、字段、对象格式或链接语义 |
| [MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)<br>[2026-07-28 候选版说明](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) | 截至 2026-07-16，2025-11-25 仍是 Current；候选版继续把协议核心、扩展与应用状态分开演进 | 协议工具、任务或能力声明自动成为 Endem 字段、动作授权或本地结果 |
| [A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/)<br>[NIST AI Agent 标准化工作](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) | Task、Message、Artifact、协议互操作、身份基础设施和安全评价属于可区分的责任 | 远端任务完成、Agent Card 或身份声明直接成为本地目标满足与最终接受 |

> **复核日期：**2026-07-16。外部资料只帮助检验职责分离；当前对象、字段、动作和结果仍以 Noemion 的现行 ADR、CORE 与 Profile 为准。

- [查看当前语义职责](adr-0010-native-lexicon.html) — 从来源表达、意义投影、事态、目标方向、判断和未决问题开始。
- [查看当前公开动作](adr-0035-public-actions-and-internal-responsibilities.html) — 理解五个动作为什么保留，以及哪些责任不再形成命令。
- [区分形成版与发布版](adr-0036-source-bearing-and-stripped-release.html) — 核对来源裁剪、新身份、外部陈述和受控伴随资料。
- [按开发任务进入 Endem](../endem/index.html) — 从当前可用性、输入、输出、停止条件和信任边界开始。
