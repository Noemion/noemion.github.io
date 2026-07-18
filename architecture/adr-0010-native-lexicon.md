---
layout: architecture-decision
title: ADR-0010 · 原生词汇与事态分层
page_role: content
footer_text: Noemion · ADR-0010
permalink: "/architecture/adr-0010-native-lexicon.html"
summary: 把原话、系统采用的解释、期望状态、判断方法和未解决问题分别保存，防止一次模型解释覆盖人的原意。
decision_id: ADR-0010
page_heading: ADR-0010 · 原生词汇与事态分层
page_lead: 把人实际说过的话、系统采用的解释、想达到的状态、判断方法和仍未解决的问题分别保存，避免一次模型解释覆盖原意。
badges:
- 当前策略
- '2026-07-12'
- 原生词汇
- 接口待定
next_url: adr-0011-endem-container.html
next_label: ADR-0011
---

## 直接结论

本决定确定六项语义职责，并采用 `source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning` 作为现行设计字段。职责分层继续有效；这些普通英语字段已经按词首、职责和关键字语料接受，新增自造名称才需要完整读音审查。

> **结构底线：**一个 Endem 只有一个根 `situation`。`meaning_projection`、`situation` 与观察中的 `structured_observation` 使用可比较的符号和关系位置；形式由结构显示，制品不能用自填标签证明自己有效。

[ADR-0037](adr-0037-terminology-simplification.html) 规定全部现行名称的检查方式。名称调整只能替换精确标识，不能合并本决定分开的职责；普通词逐词检查词首，两个自造名称另行验证完整读音。

## 六个语义面

| 工程职责 | 现行字段 | 必须保持的边界 |
| --- | --- | --- |
| 保存来源表达、主体、媒介、范围、版本和可重定位位置。 | `source_expression` | 来源事实不等于意义已经确认。 |
| 保存由确定性规则或范围有限具名权威确认的记号到符号、指称、关系、角色和作用域投影。规范称其为语义授权，但它不授予动作权限。 | `meaning_projection` | 意义投影不授予工具或运行权限。 |
| 保存一个根、中性且可比较的可能事态图。 | `situation` | 事态结构不携带期望、观察或满足结果。 |
| 保存目标对事态的变化或保持方向，不改写事态内容。 | `goal_direction` | 方向必须与事态内容分别版本化。 |
| 规定观察、结构比较、证据强度、未知处理和决定权威。 | `satisfaction_criteria` | 判据不能由模型评分或制品自填结果替代。 |
| 保存仍可表达但尚未获授权决定的有限缺口。 | `unresolved_meaning` | 未确认内容不得静默丢弃或默认补全。 |

## 事态、目标和观察不再混合

1. source_expression · 来源
2. meaning_projection · 投影
3. situation · 可能事态
4. goal_direction · 目标方向
5. satisfaction_criteria · 比较契约
6. structured_observation · 结构化观察
7. evidence · 有范围证据

- `situation` 只描述对象怎样关联，不携带“希望、保持、禁止”等力量。
- `goal_direction` 第一阶段只区分 `reach` （使事态达到成立）和 `maintain` （使事态持续成立）。
- 禁止事项由 `situation` 的显式否定表达，不再与独立 `avoid` 值重复编码。
- `structured_observation` 是 evidence 内的结构化观察；无法与 `situation` 比较的自由文本或模型评分不能独自支持满足判断。

## 制品、组件与动作

| 类别 | 直白职责 | 现行设计名称 |
| --- | --- | --- |
| 系统名词 | 最小目标制品、组合闭包、一次会话的非文件只读执行契约、有范围证据。 | Endem / closure / contract / evidence |
| 组件 | 确定性制作、独立观察、隔离实行。 | producer / inspector / runner |
| 动作 | 依次负责形成、制品形成侧检查、组合、独立只读观察和受控实现。 | `form / lint / compose / inspect / run` |
| 内容状态 | 结构已经形成，或必需投影、引用、冲突与能力上限已经收敛。 | `formed / resolved` |
| 外部关系 | 陈述、验证政策、截止点、撤销和依赖方判断。 | 不写成内容自身的状态或布尔值。 |

每个名称首次出现时必须给出直白职责。真正含义由数据结构、不变量、权限和测试决定。

外部签名与证明不能成为内容自身状态；它们必须作为有类型的外部关系，分别绑定主体、声明、验证政策、截止点和撤销状态。

## 名称审计

当前关键字语料覆盖 C/C++、Rust、Go、Python、Java、ECMAScript、Swift、Kotlin、C# 与 PostgreSQL SQL 的声明版本。现行领域词没有登记中的精确关键字冲突；该结果只降低工程混淆，不构成商标或未来包名可用性保证。现行命名与复核边界统一见 [ADR-0037](adr-0037-terminology-simplification.html)。

关键字集合分别核对 [Rust Reference](https://doc.rust-lang.org/stable/reference/keywords.html)、[Go Specification](https://go.dev/ref/spec#Keywords)、[Python Reference](https://docs.python.org/3/reference/lexical_analysis.html#keywords)、[Swift Reference](https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html) 与 [Kotlin Reference](https://kotlinlang.org/docs/keyword-reference.html)。

## 待定内容

当前策略包括 ADR-0011 的实验性容器、ADR-0013 的 END-P2 记录字段、ADR-0014 的首个来源清单，以及 ADR-0016、0018 与 0019 的时间、量化和测量规则。正式来源语言、`structured_observation` 编码、对应物理字段、`satisfaction_criteria` 求值语言、扩展注册表、摘要与签名算法和稳定 ABI 仍需独立规范与对抗测试。
