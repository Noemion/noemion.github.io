---
layout: "manual"
title: "规范参考指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范参考指南"
permalink: "/docs/specifications-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 7
nav_title: "规范参考指南"
page_heading: "Noemion 规范参考指南"
page_lead: "遇到目标、组合、运行、证据、协议、身份、文本或授权问题时，先定位权威源，再区分现行要求与研究资料。"
summary: "遇到工程问题时找到应当遵守的规范，并分清现行要求、解释文章、研究提案和实际验证。"
badges: ["权威", "查询", "状态"]
---

## 按工程问题找资料

不必先记住全部项目术语。先写下你正在判断的事实，以及它来自哪一层。

例如，外部 Agent Task 显示 `completed`，但团队要决定服务能否发布。开发者应按下面的顺序查询：

| 先回答 | 查什么 | 读哪份权威源 | 何时停止 |
| --- | --- | --- | --- |
| 外部系统实际报告了什么 | 协议版本、对端、Task、状态和候选产物 | ADP-CORE | 来源或版本不明时，不做本地映射 |
| 这次运行原本允许什么 | 主体、环境、能力、预算和证据责任 | SESSION-CORE | 外部动作超出会话上限时，拒绝继续 |
| 观察能支持多大范围的结论 | 主体、方法、环境、截止点、覆盖和限制 | EVIDENCE-CORE | 覆盖不足时保持未知，不补写成功 |
| 目标判据得到什么结果 | `satisfaction_criteria` 与 `met / unmet / undetermined / fault` | END-CORE | 判据未固定或证据不适用时，不形成满足结论 |
| 谁能决定发布 | 决定者、对象、范围、依据和截止点 | AUT-CORE | 没有适用的具名权威时，保持 `pending` |

`completed` 只说明外部请求执行状态，不直接等于 `met` 或 `accepted`。这条查询链也不要求把五份规范合并成一个对象；每份规范继续只约束自己的责任。

其他问题可以直接从下表进入：

| 要回答的问题 | 先读 | 再核对 |
| --- | --- | --- |
| 一项目标怎样表达，哪些意义仍未解决 | [Endem 规范](../specifications/endem.html) | END-CORE、END-P2，以及 ADR-0015 至 ADR-0020 |
| 多项目标怎样解析引用、权限和冲突 | [Endem closure 规范](../specifications/endem-closure.html) | CLOSURE-CORE 与 ADR-0021 |
| 一次运行可以用哪些主体、环境、能力和预算 | [session contract 会话契约](../specifications/session-contract.html) | SESSION-CORE 与 ADR-0024 |
| 观察能支持什么判断，覆盖还缺什么 | [evidence entry 规范](../specifications/evidence-entry.html) | EVIDENCE-CORE 与 ADR-0022 |
| 失败怎样取得稳定机器码和精确位置 | [结构化诊断规范](../specifications/diagnostics.html) | DIA-CORE、DIA-CAT 与 ADR-0025 |
| MCP、A2A、HTTP 或 SDK 状态怎样进入本地边界 | [外部协议适配规范](../specifications/adapters.html) | ADP-CORE 与 ADR-0026 |
| 摘要、签名和不可变引用究竟绑定什么 | [精确内容身份与签名规范](../specifications/identity.html) | ID-CORE 与 ADR-0027 |
| UTF-8、标识符、显示文本和模型输入怎样区分 | [文本与标识符边界规范](../specifications/text-and-identifiers.html) | TEXT-IDENTIFIER-CORE 与 ADR-0028 |
| 网页、工具返回、历史、摘要或附件进入模型时，哪些内容可以提供指令 | [文本与标识符边界规范](../specifications/text-and-identifiers.html)与[权威与授权决定规范](../specifications/authority.html) | TEXT-IDENTIFIER-CORE、AUT-CORE，以及[非规范上下文装配研究](https://noemion.github.io/spec/model-context-assembly-proposal.html) |
| 谁可以确认候选、解决歧义或授予动作权限 | [权威与授权决定规范](../specifications/authority.html) | AUT-CORE、ADR-0029 与 ADR-0030 |

同样，网页或工具返回即使自称 `system` 或 `admin`，也仍是带来源的资料。TEXT-IDENTIFIER-CORE 约束模型实际输入和变换，AUT-CORE 决定谁能提供指令或授予动作。上下文装配研究只提供检查路径，不建立新的接口或实现义务。

## 权威顺序

1. 先用版本化 CORE、格式条款和 Profile 确认实现义务。
2. 再用标为“当前策略”的 ADR 查明边界理由和变更影响。
3. 用威胁模型、场景和向量寻找反例、滥用方式与验证缺口。
4. 用规范 HTML、架构页和指南建立阅读路径，不从解释页创造新义务。

> “当前策略”表示项目目前采用的做法；“正在研究”表示已有候选但尚未形成结论；“待定内容”表示目前没有唯一答案；“后续计划”表示尚不能依赖。

每个规范中的“必须”“不得”和“只有”都应关联机器测试或具名人工权威。实现、论文、专利、演示和模型输出不能反向替代规范。

| 需要的材料 | 当前入口 | 用法 |
| --- | --- | --- |
| 目标内容与容器 | [END-CORE 0.1.0-draft](https://noemion.github.io/spec/endem-core.html)、[END-P2](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p2.json)、[END-FMT 0.1.0-draft](https://noemion.github.io/spec/endem-format.html) | 分别核对通用内容、封闭 Profile 和实验性容器 |
| 组合、会话与证据 | [CLOSURE-CORE](https://noemion.github.io/spec/endem-closure-core.html)、[SESSION-CORE](https://noemion.github.io/spec/session-contract-core.html)、[EVIDENCE-CORE](https://noemion.github.io/spec/evidence-entry-core.html) | 分别核对闭包、一次运行上限和证据范围 |
| 横切工程边界 | [DIA-CORE](https://noemion.github.io/spec/diagnostics-core.html)、[ADP-CORE](https://noemion.github.io/spec/adapter-core.html)、[ID-CORE](https://noemion.github.io/spec/identity-core.html)、[TEXT-IDENTIFIER-CORE](https://noemion.github.io/spec/text-identifier-core.html) | 核对诊断、外部协议、精确身份和文本解释 |
| 权威与授权 | [AUT-CORE](https://noemion.github.io/spec/authority-core.html) | 核对谁能确认意义、解决歧义或授予动作 |
| 条款与状态索引 | [机器可读登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json) | 连接条款、成熟度、威胁、场景与验证材料 |

威胁模型说明不可信输入和失败责任。例如，[Endem 威胁模型](https://noemion.github.io/spec/endem-threat-model.html)与[授权威胁模型](https://noemion.github.io/spec/authority-threat-model.html)帮助审查滥用路径，但不创造新的规范义务。

场景源用于发现规范缺口：[END-SCEN](https://noemion.github.io/spec/endem-scenarios.html)检查单项目标；[CLOSURE-SCEN](https://noemion.github.io/spec/endem-closure-scenarios.html)、[SESSION-SCEN](https://noemion.github.io/spec/session-contract-scenarios.html)、[EVIDENCE-SCEN](https://noemion.github.io/spec/evidence-entry-scenarios.html)与[AUT-SCEN](https://noemion.github.io/spec/authority-scenarios.html)分别检查组合、会话、证据与授权。这些场景不属于上述规范义务。

只有案例转化为唯一条款、登记验证方式并形成正反向量后，对应判断才可能进入符合性要求。向量通过也只说明已登记案例与草案一致；精确范围以源文件、机器可读登记和版本化验证结果为准。

## 资料状态与使用边界

同一主题可能同时出现 CORE、Profile、ADR、威胁模型、场景和向量。它们回答的问题不同。

| 资料 | 可以回答 | 不能回答 |
| --- | --- | --- |
| CORE、格式条款与已登记 Profile | 当前实现必须接受、拒绝或保持什么 | 尚未写入条款的未来接口 |
| 标为“当前策略”的 ADR | 为什么采用现行边界，变更会影响什么 | 替代对应 CORE 的逐条要求 |
| 威胁模型 | 哪些输入不可信，失败由谁处理 | 单独创造字段、结果或权限 |
| 规范 HTML、架构页与指南 | 概念怎样关联，具体问题应查哪里 | 建立第二套规范义务 |
| 场景与研究资料 | 暴露反例、备选方案和待验证责任 | 作为现行字段、命令、状态或互操作接口的依据 |
| 向量与资料一致性检查 | 已登记案例是否符合当前草案 | 证明组件已经实现、安全或可互操作 |

先看资料标题和状态，再引用内容。研究资料不能作为现行字段、命令、状态或互操作接口的依据。向量通过也只说明已登记案例与草案一致。需要实现义务时，应回到 CORE 条款、Profile 和机器可读登记。

## Endem

[Endem 规范](../specifications/endem.html)解释一个根 `situation`、六个语义面、形式显示、来源确认、显式未知、身份和安全边界。ADR-0023 明确 END-CORE 是通用内容标准、END-P2 是来源保留的形成 Profile、END-FMT 是物理容器；容器接受、Profile 接受和内容接受必须分别报告。ADR-0036 进一步要求最终发布版移除原始自然语言、取得新身份并重新验证来源引用闭包。发布 Profile、正式来源语言、求值语言、摘要算法、扩展注册表和稳定 ABI 尚待确定。

判断扩展按问题分别读取：[ADR-0015](../architecture/adr-0015-result-domains.html)分开结果域，[ADR-0016](../architecture/adr-0016-mene-time-model.html)定义持续时间，[ADR-0017](../architecture/adr-0017-negation-and-absence.html)定义否定与缺席，[ADR-0018](../architecture/adr-0018-quantification-and-membership.html)定义量化范围，[ADR-0019](../architecture/adr-0019-measurement-and-thresholds.html)定义测量与阈值，[ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)定义复合事态。它们当前都只确定抽象内容边界，没有增加 END-P2 物理字段。

## Endem closure

[Endem closure 规范](../specifications/endem-closure.html)解释完整闭包、精确绑定、有限无环、权限交集、成员结果分离和条件激活。规范源是 [CLOSURE-CORE](https://noemion.github.io/spec/endem-closure-core.html)；[CLOSURE-SCEN](https://noemion.github.io/spec/endem-closure-scenarios.html)不属于上述规范义务。当前没有物理 Endem closure 格式或组件实现。

## session contract、evidence entry 与横切边界

[session contract 会话契约](../specifications/session-contract.html)解释精确会话主体、政策封闭、环境绑定、能力与预算上限、观察责任、只读失效和销毁。规范源是 [SESSION-CORE](https://noemion.github.io/spec/session-contract-core.html)；[SESSION-SCEN](https://noemion.github.io/spec/session-contract-scenarios.html)不属于上述规范义务。session contract 永远不是磁盘格式、凭据包或可恢复会话，当前也没有 bounded runner 或运行时实现。

[evidence entry 规范](../specifications/evidence-entry.html)解释主体范围、有限无环溯源、结构化观察、证据类别、完整性、外部有效性评估、相对 `satisfaction_criteria` 的覆盖度、决定分离与最小披露。规范源是 [EVIDENCE-CORE](https://noemion.github.io/spec/evidence-entry-core.html)；模型评价只能保持 `model-candidate`。当前没有物理 evidence entry 格式或组件实现。

[结构化诊断规范](../specifications/diagnostics.html)解释稳定机器码、生产语境、失败层次、类型化位置、确定性主错误、受限恢复、外部来源、最小披露、资源预算与原子失败。规范源是 [DIA-CORE](https://noemion.github.io/spec/diagnostics-core.html)，草案机器码见 [DIA-CAT](https://noemion.github.io/spec/diagnostic-catalog.html)。诊断不是目标结果、证据、权限或自动修复命令；当前没有物理编码或组件实现。

[外部协议适配规范](../specifications/adapters.html)解释协议版本、对端、能力、调用、映射、状态、产物、错误、取消、重试、交付和安全边界。规范源是 [ADP-CORE](https://noemion.github.io/spec/adapter-core.html)。MCP、A2A、HTTP 与 SDK 对象只保持外部来源；当前没有具体协议 Profile、适配器 API 或组件实现。

[精确内容身份与签名规范](../specifications/identity.html)解释身份域、精确字节、不可变引用、算法政策、签名陈述和外置验证材料。它也分开权威、截止点、撤销、可复现性，以及形成版、来源裁剪发布版和受控伴随资料。规范源是 [ID-CORE](https://noemion.github.io/spec/identity-core.html)。当前尚未确定发行算法、签名包络、发布 Profile 或密码组件；SHA-256 只用于提案向量示例。

[文本与标识符边界规范](../specifications/text-and-identifiers.html)解释文本槽、严格 UTF-8、来源字节与解码文本、ASCII 结构标识符、规范化、比较、范围、双向显示、隐藏字符、语言元数据、模型实际输入与显示视图。规范源是 [TEXT-IDENTIFIER-CORE](https://noemion.github.io/spec/text-identifier-core.html)。END-SRCM 当前只保存解码并处理转义后的 `source_expression.content`，不证明原始 `.ends` 文件逐字节保真；当前也没有 Unicode 处理器或模型输入网关。

[权威与授权决定规范](../specifications/authority.html)解释谁可以在什么语境和范围内确认自然语言候选、解决 `unresolved_meaning`、委托 Agent、授予能力或作出授权决定。规范源是 [AUT-CORE](https://noemion.github.io/spec/authority-core.html)。`allowed / denied / pending` 只回答当前请求是否获准，不替代真值、满足、证据、最终接受或会话终止；当前没有权威目录、政策求值器、同意界面或决定服务。

允许保留的运行观察、失效原因和决定关系进入 evidence entry 或带范围的会话事件。它们不能重新创建 session contract 或恢复旧权限。

## ADR 与开放问题

| 先查哪组决定 | 主要回答什么 | 阅读边界 |
| --- | --- | --- |
| [ADR-0010](../architecture/adr-0010-native-lexicon.html) 至 [ADR-0014](../architecture/adr-0014-source-manifest.html) | 固定术语职责、Endem 格式、Profile 与来源清单 | 字段职责已进入草案；发行拼写和读音仍须另行验证 |
| [ADR-0015](../architecture/adr-0015-result-domains.html) 至 [ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html) | 结果、时间、否定、量化、测量与复合事态 | 当前只确定抽象内容边界，不增加 END-P2 物理字段 |
| [ADR-0021](../architecture/adr-0021-synem-closure-and-activation.html) 至 [ADR-0030](../architecture/adr-0030-endem-content-and-authorization-companions.html) | 组合、证据、会话、诊断、适配、身份、文本、授权与伴随关系 | 每个对象继续保持独立身份、生命周期与失败责任 |
| [ADR-0031](../architecture/adr-0031-release-name-collision-gate.html) 至 [ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html) | 名称迁移、冲突审查和口头区分 | 没有证明现行拼写或读音已经通过 |

END-P2 内的权威字段只是待解析选择器。独立文件最多达到 Profile 接受；完整内容接受还需要精确绑定的外部授权决定。ADR-0008 和 ADR-0009 只保存被取代的公开设计历史。

具体 Profile、物理编码与发行治理集中在[开放问题](../architecture/open-questions.html)。人类名称证据按[术语与读音验证指南](terminology-and-pronunciation.html)形成。

面向标准化时，规范还需关联互操作配置、正反向量、一致性测试、安全分析和版本演进。面向研究与知识产权时，还应关联假设、现有技术、实验、贡献与公开披露记录。
