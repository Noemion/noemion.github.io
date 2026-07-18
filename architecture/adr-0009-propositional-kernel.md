---
layout: architecture-decision
title: ADR-0009 · 表达与事态分离（历史记录）
page_role: content
footer_text: Noemion · ADR-0009
permalink: "/architecture/adr-0009-propositional-kernel.html"
summary: 解释为什么必须把来源表达、采用的意义、可能事态、目标方向、判断方法和未决问题分开保存。
decision_id: ADR-0009
page_heading: ADR-0009 · 表达与事态分离 · 历史记录
page_lead: 解释项目为什么把来源表达、意义、可能事态、目标方向、满足判据和未决问题分开；旧五字段、状态与动作均不再构成现行接口。
badges:
- 历史记录
- 职责部分保留
- 现行语义另有依据
- 尚无组件
previous_url: adr-0008-endem-system.html
previous_label: ADR-0008
next_url: adr-0010-native-lexicon.html
next_label: ADR-0010
---

## 先确认这份记录还能说明什么

开发者只能从 ADR-0009 继承职责分离，不能继承字段拼写：原文不等于解释，解释不等于事态，事态不等于目标，满足判据不等于观察，语义未决也不等于观察不足。

| 仍然有效的区分 | 开发者需要保留什么 | 现行依据 |
| --- | --- | --- |
| 来源与解释 | 实际进入形成过程的表达，以及规则或具名主体确认的意义投影 | ADR-0010 的来源表达与意义投影 |
| 解释与事态 | 符号怎样指向对象、关系和角色，以及这些关系构成的一个根事态 | ADR-0010 的意义投影与中性事态 |
| 事态与目标 | 先描述什么可能成立，再说明要使其成立或保持成立 | ADR-0010 的中性事态与目标方向 |
| 判据与观察 | 先固定怎样判断，再保存实际观察、范围、方法和来源 | ADR-0010、EVIDENCE-CORE 与 ADR-0022 |
| 未决意义与观察不足 | 分别记录尚未确定的解释，以及意义已定但外部事实不足的情况 | ADR-0010 的未决问题与 ADR-0015 的 `undetermined` |
| 结构与自我声明 | 由字段关系、顺序和规范约束显示结构，不接受载荷自报“有效”或“真实” | END-CORE、Profile 与独立读取责任 |

> **阅读限制：**`say / mean / case / when / open` 及其旧结果只用于解释设计来路，不是现行字段、别名、迁移输入或兼容接口。

## 它当时纠正了什么问题

早期设计把自然语言要求分进几个文本栏目，却没有要求开发者说明对象之间究竟是什么关系，也没有把目标方向和外部观察分开。ADR-0009 首次把这些问题改写为结构责任。

以“把服务依赖更新到批准版本，并在测试通过后发布”为例，仅保存“目标、约束、完成条件”三个文本框并不够。开发者还要确定“服务”“依赖”“批准版本”和“测试通过”分别指向什么，并分开版本关系、期望方向、检查方法与尚待确认的环境。模型即使生成结构完整的 JSON，也只能提供候选解释。

| 早期缺口 | ADR-0009 的贡献 | 当前怎样表达 |
| --- | --- | --- |
| 原文和解释混在一起 | 要求保存来源记号，并单独记录经过确认的意义 | 来源表达与意义投影分别承担 |
| 目标只是实体或标签清单 | 要求用对象、关系和角色组成一个根事态 | 中性事态保存关系结构 |
| 事态同时携带“想要什么” | 发现描述现实可能性与表达目标方向是不同责任 | 中性事态和目标方向分离 |
| 判断规则、观察和接受混在一起 | 要求先固定满足条件，再取得外部观察 | 满足判据、evidence、满足结果和最终决定分别处理 |
| 所有未知共用一个状态 | 发现解释未决、观察不足和执行故障必须区分 | 未决问题、`undetermined` 与 `fault` 分属不同层次 |

## 当前开发者应怎样拆开一个目标

1. 保留实际表达
2. 确认词语所指
3. 形成中性事态
4. 声明目标方向
5. 固定满足判据
6. 保留未决问题
7. 观察、判断与决定

| 开发者问题 | 现行设计标识 | 缺失时怎样停止 |
| --- | --- | --- |
| 实际收到的自然语言是什么 | 来源表达（`source_expression`） | 来源无法重定位或内容身份不一致时停止形成 |
| 对象、关系和角色指向什么 | 意义投影（`meaning_projection`） | 模型候选未经规则或具名主体确认时保持候选 |
| 哪一个可能事态需要被判断 | 中性事态（`situation`） | 没有根关系、角色不全或存在多个独立根时拒绝 |
| 要使事态成立还是保持成立 | 目标方向（`goal_direction`） | 方向缺失或与事态极性重复时拒绝 |
| 什么观察足以支持或反驳目标 | 满足判据（`satisfaction_criteria`） | 方法、范围、截止点或决定权威不明确时不得求值 |
| 哪些解释仍不能确定 | 未决问题（`unresolved_meaning`） | 阻断性问题未解决时不得进入受限运行 |
| 实际发生了什么 | 结构化观察（`structured_observation`）与 evidence | 来源、方法或覆盖不足时产生有限结果，不补写事实 |

形成版保留实际进入形成过程的自然语言；未来发布版按独立 Profile 移除原文并取得新身份。裁剪不改变已经确认的目标结构，也不能把模型候选、协议状态或显示文本提升为权威语义。

## 旧字段和状态为什么不能继续使用

| 历史表达 | 主要问题 | 当前处理 |
| --- | --- | --- |
| `say / mean / case / when / open` | 把目标方向压进事态，把判据、观察和决定压进一个栏目 | 由六个语义面、结构化观察和独立结果域取代 |
| `no-sense / open / unknown` | 把非法结构、语义未决和观察不足写成同一对象的并列状态 | `no_allowed_projection` 拒绝、语义未决与 `undetermined` 分别处理 |
| `seek / keep / avoid` | 目标力量与关系极性重叠，且旧词不能映射现行时间和否定语义 | 目标方向与事态极性分离；现行普通词已按词首和职责接受 |
| Witness、Runner 与大写 Decision | 名称混合证据记录、会话运行和最终权威，且已由后续对象边界取代 | evidence、contract、受限运行边界与具名权威决定分别承担 |
| `form` 及旧实现切片 | 内部形成步骤不等于现行公开动作，也没有组件实现 | 当前只使用五个设计动作；历史动作不构成别名 |

`source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning / structured_observation` 是现行设计字段，已经按普通词的词首、职责和关键字语料规则接受。它们不是已实现接口，也不产生别名或第二套字段；Noemion 与 Endem 两个自造名称另行保留发行读音验证。

## 哲学与外部资料怎样限定这份记录

| 资料 | 支持的局部原则 | 不能推出什么 |
| --- | --- | --- |
| [《逻辑哲学论》2.172、4.022、4.12–4.1212](https://www.wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_%28English%29) | 表达需要可辨认的结构；形式不能靠载荷自我声明，而应由结构显示 | 自然语言天然映射现实、Endem 已经为真，或书中命题直接定义字段与编码 |
| [GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)<br>[GNU Names](https://www.gnu.org/prep/standards/html_node/Names.html) | 资料按用户问题组织，专门术语首次使用时定义，名称提供有用意义 | 为了哲学词族整齐而保留字段，或让历史字段库存决定阅读顺序 |
| [NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | 生成式人工智能会自信地产生错误、偏离输入或内部矛盾的内容，因此模型解释只能作为候选 | 模型置信度、解释文本或逻辑步骤自动取得意义确认和事实权威 |
| [MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)<br>[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/) | 截至 2026-07-16，MCP 2025-11-25 仍是 Current；A2A 分开 Message、Task、Artifact 与任务状态 | 协议文本、Task 完成或 Artifact 自动成为本地意义、事态、满足结果或最终接受 |

> **采用边界：**哲学原典用于提出结构问题，外部标准用于检验相邻责任；Noemion 的字段、结果和授权只由现行 ADR、CORE 与 Profile 决定。

- [查看现行语义职责](adr-0010-native-lexicon.html) — 从来源、意义、事态、目标方向、判据和未决问题开始。
- [区分满足与决定结果](adr-0015-result-domains.html) — 不要把语义未决、观察不足、执行故障和最终接受写成一个状态。
- [核对现行名称规则](adr-0037-terminology-simplification.html) — 区分普通职责词、机器值与两个自造名称的检查范围。
- [按开发任务阅读 Endem](../specifications/endem.html) — 从一个目标的输入、结构、停止条件和规范来源进入。
