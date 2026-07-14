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
summary: "按工程问题定位规范源，并区分现行要求、解释材料、研究资料与验证证据。"
badges: ["Authority", "Lookup", "Status"]
---

## 按工程问题找资料

不必先记住全部项目术语。先确认你要回答的问题，再进入对应规范。

| 要回答的问题 | 先读 | 再核对 |
| --- | --- | --- |
| 一项目标怎样表达，哪些意义仍未解决 | [Endem 规范](../specifications/endem.html) | END-CORE、END-P1，以及 ADR-0015 至 ADR-0020 |
| 多项目标怎样解析引用、权限和冲突 | [Synem 规范](../specifications/synem.html) | SYN-CORE 与 ADR-0021 |
| 一次运行可以用哪些主体、环境、能力和预算 | [Dromen 会话契约](../specifications/dromen.html) | DRO-CORE 与 ADR-0024 |
| 观察能支持什么判断，覆盖还缺什么 | [Iknem 规范](../specifications/iknem.html) | IKN-CORE 与 ADR-0022 |
| 失败怎样取得稳定机器码和精确位置 | [结构化诊断规范](../specifications/diagnostics.html) | DIA-CORE、DIA-CAT 与 ADR-0025 |
| MCP、A2A、HTTP 或 SDK 状态怎样进入本地边界 | [外部协议适配规范](../specifications/adapters.html) | ADP-CORE 与 ADR-0026 |
| 摘要、签名和不可变引用究竟绑定什么 | [精确内容身份与签名规范](../specifications/identity.html) | ID-CORE 与 ADR-0027 |
| UTF-8、标识符、显示文本和模型输入怎样区分 | [文本与标识符边界规范](../specifications/text-and-identifiers.html) | TEXT-IDENTIFIER-CORE 与 ADR-0028 |
| 网页、工具返回、历史、摘要或附件进入模型时，哪些内容可以提供指令 | [文本与标识符边界规范](../specifications/text-and-identifiers.html)与[权威与授权决定规范](../specifications/authority.html) | TEXT-IDENTIFIER-CORE、AUT-CORE，以及[非规范上下文装配研究](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-context-assembly-proposal.md) |
| 谁可以确认候选、解决歧义或授予动作权限 | [权威与授权决定规范](../specifications/authority.html) | AUT-CORE、ADR-0029 与 ADR-0030 |

例如，外部 Agent Task 显示 `completed`，开发者仍不能据此发布结果。先用 ADP-CORE 保存协议状态和来源，再用 DRO-CORE 检查本次会话的能力上限。随后用 IKN-CORE 判断证据范围，并按 END-CORE 的 `krin` 形成满足结果。最后由 AUT-CORE 所描述的具名权威作出适用决定。`completed` 只说明外部请求执行状态，不直接等于 `met` 或 `accepted`。

同样，网页或工具返回即使自称 `system` 或 `admin`，也仍是带来源的资料。TEXT-IDENTIFIER-CORE 约束模型实际输入和变换，AUT-CORE 决定谁能提供指令或授予动作。上下文装配研究只提供检查路径，不建立新的接口或实现义务。

## 权威顺序

1. 版本化 Markdown 条款源定义实现必须满足什么。
2. 标为“当前策略”的 ADR 解释项目为什么采用这条边界，以及怎样变更。
3. 威胁模型说明不可信输入、滥用方式和失败责任，但不另建义务。
4. 架构页和规范 HTML 解释对象关系，便于开发者理解条款所在位置。
5. 指南提供阅读路径；FAQ、场景、研究资料和示例不建立实现义务。

> “当前策略”表示项目目前采用的做法；“正在研究”表示已有候选但尚未形成结论；“待定内容”表示目前没有唯一答案；“后续计划”表示尚不能依赖。

每个规范中的“必须”“不得”和“只有”都应关联机器测试或具名人工权威。实现、论文、专利、演示和模型输出不能反向替代规范。

当前权威源包括作为通用内容标准的 [END-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-core.md)、当前封闭内容 Profile [END-P1](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p1.json)、实验性容器 [END-FMT 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-format.md)，以及组合、会话、证据、诊断、适配、身份、文本和授权边界的各 CORE 草案。权威与授权决定以 [AUT-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/authority-core.md)为准；全部条款与状态由[机器可读登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)连接。公开 HTML 只负责直白解释，不复制第二套条款。

不可信输入和失败责任由对应模型说明，包括 [Endem 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-threat-model.md)与[授权威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/authority-threat-model.md)。威胁模型不创造新的规范义务。

[END-SCEN 自然语言场景语料](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-scenarios.md)用支持案例、反例和边界场景寻找规范缺口，但不属于上述规范义务。只有案例转化为唯一条款、登记验证方式并形成正反向量后，对应判断才可能进入符合性要求。场景和向量的精确范围以源文件、[机器可读登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)和版本化验证结果为准。

[SYN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-scenarios.md)、[DRO-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-scenarios.md)、[IKN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/iknem-scenarios.md)与[AUT-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/authority-scenarios.md)分别检查组合闭包、会话契约、证据及授权边界，同样不属于上述规范义务。

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

[Endem 规范](../specifications/endem.html)解释一个根 `skena`、六个语义面、形式显示、来源确认、显式未知、身份和安全边界。ADR-0023 明确 END-CORE 是通用内容标准、END-P1 是封闭内容 Profile、END-FMT 是物理容器；容器接受、Profile 接受和内容接受必须分别报告。ADR-0014 另以 [END-SRCM](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-source-manifest.md)固定首个来源清单。正式来源语言、求值语言、摘要算法、扩展注册表和稳定 ABI 尚待确定。

判断扩展按问题分别读取：[ADR-0015](../architecture/adr-0015-result-domains.html)分开结果域，[ADR-0016](../architecture/adr-0016-mene-time-model.html)定义持续时间，[ADR-0017](../architecture/adr-0017-negation-and-absence.html)定义否定与缺席，[ADR-0018](../architecture/adr-0018-quantification-and-membership.html)定义量化范围，[ADR-0019](../architecture/adr-0019-measurement-and-thresholds.html)定义测量与阈值，[ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)定义复合事态。它们当前都只确定抽象内容边界，没有增加 END-P1 物理字段。

## Synem

[Synem 规范](../specifications/synem.html)解释完整闭包、精确绑定、有限无环、权限交集、成员结果分离和条件激活。规范源是 [SYN-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md)；[SYN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-scenarios.md)不属于上述规范义务。当前没有物理 Synem 格式或组件实现。

## Dromen、Iknem 与横切边界

[Dromen 会话契约](../specifications/dromen.html)解释精确会话主体、政策封闭、环境绑定、能力与预算上限、观察责任、只读失效和销毁。规范源是 [DRO-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)；[DRO-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-scenarios.md)不属于上述规范义务。Dromen 永远不是磁盘格式、凭据包或可恢复会话，当前也没有 Drasor 或运行时实现。

[Iknem 规范](../specifications/iknem.html)解释主体范围、有限无环溯源、结构化观察、证据类别、完整性、外部有效性评估、相对 `krin` 的覆盖度、决定分离与最小披露。规范源是 [IKN-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/iknem-core.md)；模型评价只能保持 `model-candidate`。当前没有物理 Iknem 格式或组件实现。

[结构化诊断规范](../specifications/diagnostics.html)解释稳定机器码、生产语境、失败层次、类型化位置、确定性主错误、受限恢复、外部来源、最小披露、资源预算与原子失败。规范源是 [DIA-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/diagnostics-core.md)，草案机器码见 [DIA-CAT](https://github.com/Noemion/noemion.github.io/blob/main/spec/diagnostic-catalog.md)。诊断不是目标结果、证据、权限或自动修复命令；当前没有物理编码或组件实现。

[外部协议适配规范](../specifications/adapters.html)解释协议版本、对端、能力、调用、映射、状态、产物、错误、取消、重试、交付和安全边界。规范源是 [ADP-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/adapter-core.md)。MCP、A2A、HTTP 与 SDK 对象只保持外部来源；当前没有具体协议 Profile、适配器 API 或组件实现。

[精确内容身份与签名规范](../specifications/identity.html)解释身份域、精确字节、不可变引用、算法政策、签名陈述、外置验证材料、权威分离、截止点、撤销、可复现性与伴随制品关系。规范源是 [ID-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/identity-core.md)。当前尚未确定发行算法、签名包络或密码组件；SHA-256 只用于提案向量示例。

[文本与标识符边界规范](../specifications/text-and-identifiers.html)解释文本槽、严格 UTF-8、来源字节与解码文本、ASCII 结构标识符、规范化、比较、范围、双向显示、隐藏字符、语言元数据、模型实际输入与显示视图。规范源是 [TEXT-IDENTIFIER-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/text-identifier-core.md)。END-SRCM 当前只保存解码并处理转义后的 `rhem.content`，不证明原始 `.ends` 文件逐字节保真；当前也没有 Unicode 处理器或模型输入网关。

[权威与授权决定规范](../specifications/authority.html)解释谁可以在什么语境和范围内确认自然语言候选、解决 `apor`、委托 Agent、授予能力或作出授权决定。规范源是 [AUT-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/authority-core.md)。`grant / deny / defer` 只回答当前请求是否获准，不替代真值、满足、证据、最终接受或会话终止；当前没有权威目录、政策求值器、同意界面或决定服务。

允许保留的运行观察、失效原因和决定关系进入 Iknem 或带范围的会话事件。它们不能重新创建 Dromen 或恢复旧权限。

## ADR 与开放问题

[ADR-0010](../architecture/adr-0010-native-lexicon.html)至 [ADR-0014](../architecture/adr-0014-source-manifest.html)固定术语职责、Endem 格式、Profile 与来源清单；[ADR-0015](../architecture/adr-0015-result-domains.html)至 [ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)固定判断、时间、否定、量化、测量与复合边界；[ADR-0021](../architecture/adr-0021-synem-closure-and-activation.html)至 [ADR-0030](../architecture/adr-0030-endem-content-and-authorization-companions.html)固定组合、证据、内容分层、会话、诊断、适配、精确身份、文本解释、授权决定以及 Endem 内容与授权伴随关系。[ADR-0031](../architecture/adr-0031-release-name-collision-gate.html)至 [ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html)固定名称迁移和发行审查，但没有证明现行拼写或读音已经通过。END-P1 内的权威字段只是待解析选择器，独立文件最多达到 Profile 接受；完整内容接受还需要精确绑定的外部授权决定。ADR-0008 和 ADR-0009 只保存被取代的公开设计历史。具体 Profile、物理编码与发行治理集中在[开放问题](../architecture/open-questions.html)，人类名称证据按[术语与读音验证指南](terminology-and-pronunciation.html)形成。

面向标准化时，规范还需关联互操作配置、正反向量、一致性测试、安全分析和版本演进。面向研究与知识产权时，还应关联假设、现有技术、实验、贡献与公开披露记录。
