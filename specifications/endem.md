---
layout: content
title: Endem · 最小目标制品规范
page_role: content
footer_text: Noemion · Endem
permalink: "/specifications/endem.html"
summary: 说明一件最小目标制品怎样保存原始表达、采用的解释、期望状态、判断方法和仍未解决的问题。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: Endem
page_lead: 一件 Endem 说明目标来自哪里、表示什么、期望什么，以及怎样判断是否满足。
badges:
- END-CORE 0.1.0-draft
- END-FMT 0.1.0-draft
- 单一根事态
- 普通职责词已接受
previous_url: index.html
previous_label: 规范参考指南
next_url: endem-closure.html
next_label: closure 规范
---

## Endem 表示什么

一件 Endem 只描述一项能够独立理解和判断的目标。形成版保留实际输入的自然语言，供人检查意义投影与待确认项；最终发布版移除原文，只保留发布 Profile 允许的已确认目标结构。

Endem 不保存模型提示、推理过程或执行计划。它把来源表达、已确认意义、中性可能事态、目标方向、满足判据和未决意义分开，使形成者、检查者、运行系统和决定者能够各自核对自己的责任。

> **权威边界：**通用内容义务与条款 ID 以 [END-CORE 内容标准](https://noemion.github.io/spec/endem-core.html)为准；来源保留字段由 END-P2 定义；实验性容器以 [END-FMT 条款源](https://noemion.github.io/spec/endem-format.html)为准。最终发布 Profile 尚未定义，END-FMT 0.1.0-draft 也尚非稳定 ABI。

> **名称状态：**六项职责与字段已经按词首、职责和关键字语料接受。技术讨论先说直白职责，再给出代码字段；只有 Noemion 与 Endem 两个自造名称继续保留发行前的人类读音验证，详见[术语简化决定](../architecture/adr-0037-terminology-simplification.html)。

## 用一个健康目标读懂 Endem

以“让登记服务返回健康状态”为例。开发者先固定要判断的终态，再回答六个互不替代的问题。

| 直白职责 | 字段 | 这个例子需要确定什么 |
| --- | --- | --- |
| <span id="source_expression"></span>来源表达 | `source_expression` | 哪份需求、哪个版本和哪一段范围提出了目标。 |
| <span id="meaning_projection"></span>意义投影 | `meaning_projection` | “登记服务”“健康状态”和“返回”分别指向哪个对象、值和关系。 |
| <span id="situation"></span>中性事态 | `situation` | 登记服务与健康状态之间应成立什么关系，不在这里混入愿望、计划或置信度。 |
| <span id="goal_direction"></span>目标方向 | `goal_direction` | 要求该事态达到成立；持续目标还要确定时间范围和连续性政策。 |
| <span id="satisfaction_criteria"></span>满足判据 | `satisfaction_criteria` | 接受哪类 `structured_observation` 观察、怎样对齐关系、需要哪些 evidence，以及谁作出最终决定。 |
| <span id="unresolved_meaning"></span>未决意义 | `unresolved_meaning` | 服务实例、健康口径或确认权威仍不明确时，保存候选、冲突与解决责任。 |

1. 受控来源
2. 六项职责
3. 精确 Endem
4. structured_observation 观察
5. evidence 范围
6. 满足判断
7. 具名权威决定

如果“登记服务”仍能指向多个实例，形成过程保留 `unresolved_meaning`；如果没有任何允许的意义投影，则以 `no_allowed_projection` 拒绝。模型可以提出候选，但不能替有权主体选择对象、删除歧义或决定规范字节。

## 先分清内容、Profile 与容器

同一份实验性 `.endem` 必须分别通过容器、Profile 和内容检查。较低一层通过，不会自动提升后续结论。

| 层次 | 负责定义 | 通过后还要检查 |
| --- | --- | --- |
| END-FMT 容器 | 固定前导、记录目录、确定性编码、范围与有界读取 | 字段是否符合固定 Profile，内容关系是否成立 |
| END-P2 形成 Profile | 含原始自然语言的字段、类型、枚举、顺序、引用、状态与资源上限 | 全部 END-CORE 义务与外部前置条件；END-P2 不是最终发布 Profile |
| END-CORE 内容标准 | 六项职责、关系不变量、意义确认、状态、身份和符合性 | 目标是否满足、外部陈述是否有效、会话能否准入以及权威是否接受 |

形成版

保存原始自然语言和可重定位范围，服务确定性形成、人工复核与受控诊断。

发布版

移除原文和可逆重建材料，重新闭合引用并取得新的精确身份；当前 Profile 尚未定义。

受控伴随资料

在获准的审计中关联形成版与发布版，不进入公开包，也不提供运行权限。

[ADR-0023](../architecture/adr-0023-endem-content-standard.html)定义三层接受；[ADR-0036](../architecture/adr-0036-source-bearing-and-stripped-release.html)定义形成版、裁剪发布版与伴随资料的身份关系。形成版签名、证据或接受状态都不能由发布版继承。

## 六项职责共同维持什么不变量

- 一个 Endem 必须且只能有一个根 `situation` 。能够独立实现、验收或失败的目标分别形成 Endem，再由 closure 组合。
- `source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning` 使用固定逻辑顺序；没有待确认项时， `unresolved_meaning` 是显式空集合。
- `meaning_projection` 、 `situation` 与适用 evidence 中的 `structured_observation` 共享可比较的符号身份、关系和角色位置。
- 关系拓扑、角色、极性、作用域和组合边显示逻辑形式。作者填写的 `logical_form` 、 `valid` 或 `true` 不能让内容自行成立。
- 第一阶段 `goal_direction` 只允许 `reach` 与 `maintain` ；禁止事项由 `situation` 的显式否定表达，不再增加重复极性的目标方向。
- producer 未来负责确定性写入，inspector 负责只读检查；两条路径都必须从结构恢复约束，而不是把六项职责当作六段自由文本。

## 先区分形成失败、待确认与判断失败

“没有可采用的意义”“尚无权选择意义”“观察不足”和“检查过程故障”发生在不同阶段。把它们都写成失败，会让后续系统采取错误动作。

| 结果 | 它回答的问题 | 下一步 |
| --- | --- | --- |
| `no_allowed_projection` | 来源范围内没有任何允许的意义投影 | 停止形成并定位来源、规则或授权冲突 |
| `unresolved_meaning` | 存在可表达候选，但当前主体无权或无法唯一选择 | 保留候选与冲突，交给具名权威解决 |
| `undetermined` | 意义和判据已经确定，但观察范围不足以分类 | 补足有范围的观察；不得默认写成不满足 |
| `fault` | 观察器、适配器或求值过程没有按契约完成 | 修复失败层次；不得把组件故障改写成目标为假 |

1. situation · 目标事态
2. goal_direction · 方向
3. structured_observation · 观察
4. evidence · 范围与依据
5. satisfaction_criteria · 比较
6. met / unmet / undetermined / fault

## 五个结果域分别回答什么

同一次工作可以同时出现“会话完成、目标未满足、证据有效但覆盖不足”。每个结果都必须带上自己回答的问题。

| 问题 | 现行结果 | 消费边界 |
| --- | --- | --- |
| 内容形成到哪一步 | `formed / resolved` | 只描述形成分类，不授予运行、发布或接受权限 |
| 目标事态是否满足 | `met / unmet / undetermined / fault` | 不改写权威决定或会话终止 |
| 具名权威怎样决定 | `accepted / rejected / deferred` | 保留原满足结果和决定范围 |
| 一次会话怎样结束 | `completed / failed / stopped` | `completed` 不等于 `met`，`failed` 不等于 `unmet` |
| 证据记录是否有效、集合是否充分 | `valid / invalid / revoked`<br>`sufficient / insufficient` | 有效性与覆盖度分别评价 |

[ADR-0015](../architecture/adr-0015-result-domains.html)固定这些结果域。[RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html)同样把 Evidence、验证者结果和依赖方决定分开；这项外部架构只支持责任分层，不定义 Endem 字段。

## 复杂目标从哪个问题进入

时间、缺席、集合、测量和组合不是附加标签。只要目标涉及这些问题，就先固定相应范围，再形成确定结论。

| 开发者问题 | 先固定 | 何时停止推导 | 精确来源 |
| --- | --- | --- | --- |
| 怎样要求事态持续成立 | `utc_window` 或 `elapsed_window` 时间范围，以及 `strict` 或完整 `budgeted` 连续性政策 | 时钟权威、锚点、覆盖或中断预算仍缺失 | [ADR-0016](../architecture/adr-0016-time-evidence.html) |
| 没有记录能否证明没有发生 | 同一关系的显式负观察，或由具名权威封闭的全集、路径、截止点和损失边界 | 查询未命中或日志为空只能形成 `undetermined` | [ADR-0017](../architecture/adr-0017-negation-and-absence.html) |
| “所有”或数量条件怎样判断 | 集合身份、成员资格权威、截止点、不同成员身份、量词与空集合政策 | 开放集合不能证明全称、上界或精确数量已经满足 | [ADR-0018](../architecture/adr-0018-quantification-and-membership.html) |
| 一个指标超过阈值是否足够 | 构念、总体、单位、方法版本、窗口、样本、聚合器、阈值与不确定度 | 区间跨越阈值为 `undetermined`；测量程序违约为 `fault` | [ADR-0019](../architecture/adr-0019-measurement-and-thresholds.html) |
| 一句话形成一个还是多个目标 | 是否共享不可分终态、目标方向、权威、验收和失败责任 | 能够独立版本化、实现或接受的部分必须形成两个 Endem | [ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html) |
| 终态成立能否证明某动作造成变化 | 有身份的动作、同一对象的前后态、竞争活动、观察缺口和有范围的因果方法 | `met` 只回答终态满足；后态不能单独证明动作发生、状态转变或因果归属 | [非规范因果归因研究](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html) |
| 文件内写了权威名称能否证明授权 | 精确内容身份、外部授权伴随关系、委托、撤销和决定范围 | 文件内选择器、签名存在或本地 ACL 命中都不能补齐外部前置条件 | [ADR-0030](../architecture/adr-0030-endem-content-and-authorization-companions.html)<br>`SCN-028–030` |

完整案例、反例与跨场景不变量保存在 [END-SCEN 自然语言设计语料](https://noemion.github.io/spec/endem-scenarios.html)。这些语料用于发现规范缺口，不是产品演示、可执行测试或组件实现证据。

## 现行形成分类怎样阅读

精确内容不是在原身份中不断升级的可变状态机。六项职责发生变化时会产生新内容身份；签名、证明、验证结论和准入决定作为外部关系绑定该身份。

| 现行草案值 | 当前含义 | 主张上限 |
| --- | --- | --- |
| `formed` | 结构合法，但仍有 `unresolved_meaning`、引用或确认事项 | 只能继续检查或解决，不进入发布与运行 |
| `resolved` | 必需引用、冲突、能力上限和验收关系都取得确定结果 | 不证明来源可信、当前环境授权或目标已经满足 |
| 外部陈述与验证 | 按精确内容身份分别保存陈述、验证政策、截止点、撤销状态与依赖方判断 | 不属于内容状态；签名存在不能自动取得会话准入 |

1. 精确内容身份
2. 有类型外部陈述
3. 验证政策与截止点
4. 撤销状态
5. 依赖方准入判断
6. 新 contract

开发者当前应按“内容形成 + 外部关系”理解这些值。外部陈述的增加、过期或撤销不改变内容字节；修改六项职责则产生新身份与显式派生关系。现行字段和值由 ADR-0037 统一，只使用一套拼写。

## 安全读取与当前状态

1. 固定 END-CORE、END-FMT 与 Profile 的精确版本，不使用“最新”或环境默认值解释正式输入。
2. 先验证目录、范围和资源上限，再分配或解释载荷；offset、length、count、index 与累计预算使用 `checked arithmetic` 。
3. 未知且影响意义、事态、方向、判据、待确认项、权限或完整性的关键记录必须拒绝。
4. 解析失败不产生部分可信 Endem；诊断定位字节范围、记录或字段组，并分别报告容器、Profile 与内容结果。
5. 声明不超过已执行的检查。当前向量只能证明登记案例与草案关系一致，不能证明解析器、运行时或互操作已经实现。

**当前策略：**Endem 使用六项职责和一个根事态，分开事态与方向、形成未知、观察不足、求值故障和五个结果域。

**正在研究：**Noemion 与 Endem 的人类读音验证，以及来源裁剪发布 Profile。

**待定内容：**时间、封闭、量化、测量与组合的物理字段，条件适用性、统计模型登记、压缩、摘要、签名和稳定 ABI。producer、inspector、runner 与两个独立读取实现均不存在。
