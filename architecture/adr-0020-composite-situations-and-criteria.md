---
layout: architecture-decision
title: ADR-0020 · 组合条件不能吞掉未知与故障
page_role: content
footer_text: Noemion · ADR-0020
permalink: "/architecture/adr-0020-composite-situations-and-criteria.html"
summary: 说明多个条件怎样组合已有结果，以及为什么组合和提前停止都不能把未知、故障或未检查条件改成真假。
decision_id: ADR-0020
page_heading: ADR-0020 · 组合条件不能吞掉 · 未知与故障
page_lead: 多个条件组合判断时，每个条件必须先得到自己的结果。提前停止可以减少不必要的检查，但不能把未知、故障或未检查条件改成普通真假。
badges:
- 当前策略
- 四值组合
- 不改变线格式
- 尚未实现
previous_url: adr-0019-measurement-and-thresholds.html
previous_label: ADR-0019
next_url: adr-0021-closure-and-activation.html
next_label: ADR-0021
---

## 用一次发布检查读懂复合判据

“接口可达、响应结构正确且 p95 延迟不高于 300 毫秒”可以描述同一个服务发布终态，但三项条件必须先分别得到结果。

1. 确认同一终态与验收责任
2. 固定三个关系叶及独立判据
3. 分别形成四值叶结果
4. 按 all_of组合结果
5. 记录决定依据与检查覆盖

| 检查阶段 | 本例必须保存 | 禁止简化 |
| --- | --- | --- |
| 目标边界 | 一个服务发布终态、同一方向、同一验收责任。 | 只因原句出现“并且”就合成一个 Endem。 |
| 叶定义 | 可达性、响应结构和延迟各自的关系、判据与证据范围。 | 把自由文本、脚本或模型总分直接放进组合节点。 |
| 叶结果 | 每个条件独立产生 `met / unmet / undetermined / fault`。 | 在组合前把未知和故障折叠成 `false`。 |
| 总体结果 | `all_of` 按固定优先级组合叶结果。 | 由执行顺序、界面颜色或退出码决定。 |
| 检查覆盖 | 已检查叶、未检查叶、所用 evidence、决定依据和停止原因。 | 把没有检查的叶写成 `undetermined` 或删除已见故障。 |

## 先判断一个终态还是多个目标

组合节点只适用于不能独立实现、替换或接受的同一终态。能够独立失败的目标必须成为多个 Endem，再由 closure 说明关系。

| 边界问题 | 一个复合 Endem | 多个 Endem 与 closure |
| --- | --- | --- |
| 终态身份 | 所有叶共同描述同一个终态。 | 每一部分都有自己的终态。 |
| 目标方向 | 共享一个到达或持续方向。 | 方向或时间责任可以不同。 |
| 生命周期 | 只能共同实现、替换和验收。 | 可以独立版本化、替换或停止。 |
| 权威与失败 | 共享同一最终决定边界。 | 可以由不同主体独立接受或失败。 |
| 发布示例 | 接口可达且响应结构正确。 | 发布报告完成且服务已经部署。 |

自然语言中的“并且”和“或者”只是线索，不是边界算法。判断必须落到终态身份、消费者、权威、生命周期和失败责任。

## 事态结构与判据拓扑必须一致

第一阶段只允许用 `all_of` 和 `any_of` 组合判据。组合的是叶结果，不是原始数值、自然语言或可执行表达式。

| 结构 | 必须满足 | 确定拒绝 |
| --- | --- | --- |
| 事态根 | `situation` 显示有限、无环的关系叶和组合节点。 | 循环引用、重复叶或多个无共同终态的目标。 |
| 组合节点 | 只能使用 `all_of` 或 `any_of`，并至少有两个不同子节点。 | `not / if / iff / xor / xone` 或任意表达式。 |
| 叶判据 | `satisfaction_criteria` 为每个关系叶给出独立判据。 | 缺叶、额外叶或用一个总分代替多个判断。 |
| 拓扑对齐 | `satisfaction_criteria` 使用与 `situation` 相同的组合拓扑。 | 在判断阶段悄悄改变分组或操作符。 |
| 观察绑定 | `structured_observation` 与关系叶、角色位置和实际 evidence 对齐。 | 把外部状态、脚本成功或模型回答直接当作总体结果。 |

> **术语边界：**`quantifier=every` 表示 ADR-0018 的“全部成员”，`combiner=all_of` 表示复合判据的“全部条件”。代码和日志必须带域名；口头说明先说中文，不得只说易混淆的 `all`。

`any_of` 在人类界面先写“任一条件”。这个由普通英语词组成的下划线机器标识不承担发行名称，只检查词首、职责和关键字冲突，不设置完整人类朗读和听写验证。

## 四种叶结果怎样组合

| 组合方式 | 决定性结果 | 没有决定性结果时 |
| --- | --- | --- |
| 全部条件 `all_of` | 任一有效叶为 `unmet`，总体即为 `unmet`。 | 有 `fault` 则为 `fault`；否则有 `undetermined` 则为 `undetermined`；全部为 `met` 才是 `met`。 |
| 任一条件 `any_of` | 任一有效叶为 `met`，总体即为 `met`。 | 有 `fault` 则为 `fault`；否则有 `undetermined` 则为 `undetermined`；全部为 `unmet` 才是 `unmet`。 |

`fault` 只在没有决定性满足或反驳时优先于 `undetermined`。这条总体优先级不能删除叶结果，也不能把故障解释成条件不成立。

`not` 继续由关系叶的显式极性承担。跨 Endem 的条件适用性由会话激活关系表达，不得用 `undetermined` 冒充。

## 短路与外部规则只能做什么

`all_of` 遇到有效 `unmet`，或 `any_of` 遇到有效 `met` 后，可以停止检查其余叶。记录必须保存决定依据 `decisive-basis` 和检查覆盖 `evaluation-coverage`。

检查覆盖包括已求值叶、实际 evidence、未求值叶身份和停止原因。未求值叶不是 `undetermined`；它还没有得到判断。短路前已经出现的故障也必须保留。

| 外部资料 | 可采用的机制 | Noemion 不继承 |
| --- | --- | --- |
| [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/) | 显式表达逻辑约束，并分开数据不符合与验证过程失败。 | 不采用 RDF Shape 或二值符合性作为制品语义。 |
| [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) Working Draft | 把 `intent` 与 `agentInstruction` 列为不影响验证的特征。 | 草案不是稳定依赖，也不让 AI 指令进入形式判据。 |
| [GNU Coreutils test](https://www.gnu.org/software/coreutils/manual/html_node/test-invocation.html) | 退出状态 0、1、2 分别表达真、假和错误。 | 不采用 shell 表达式、进程退出码或二值结果域。 |
| [GNU Bash Lists](https://www.gnu.org/software/bash/manual/html_node/Lists.html) | `&&` 与 `\|\|` 展示决定性短路。 | 只借鉴减少不必要工作的机制，不采用副作用或左结合语义。 |
| [NIST AI 800-2 Initial Public Draft](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf) | 先说明评估目的与可直接观察的测量标准。 | 模型总分不能替代叶定义，也不能隐藏证据缺口。 |

## 当前还不能编码或执行什么

现行十二个复合判据提案向量覆盖六个允许分类和六个确定拒绝，只检查 END-CMP 四条抽象规则。当前策略不增加 END-P2 字段。

这项决定不表示 producer、inspector、runner、CLI 或求值器已经实现。物理字段、规范排序、引用、深度预算、排他析取、跨叶变量绑定和规范字节仍需新 Profile。

条件适用性、时间组合和量化组合还必须分别服从已有边界。外部规则语言或模型代码不能借复合节点取得执行权限。

- [查看目标与判据](../specifications/endem.html) — 定位关系叶、观察和四值结果。
- [查看多目标组合](../specifications/endem-closure.html) — 判断何时必须拆成多个 Endem。
- [查看成员量化](adr-0018-quantification-and-membership.html) — 区分全部成员与全部条件。
- [查看叶级测量](adr-0019-measurement-and-thresholds.html) — 先固定测量程序，再产生可组合结果。
