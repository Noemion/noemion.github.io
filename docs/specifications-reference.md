---
layout: "manual"
title: "规范参考指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范参考指南"
permalink: "/docs/specifications-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 6
nav_title: "规范参考指南"
page_heading: "Noemion 规范参考指南"
page_lead: "理解 Endem、Synem、Dromen、Tekmor、成熟度标记与 ADR 的权威顺序。"
summary: "理解 Endem、Synem、Dromen、Tekmor、成熟度标记与 ADR 的权威顺序。"
badges: ["Authority", "Maturity", "ADR"]
---

## 权威顺序

1. 版本化 Markdown 条款源定义“必须是什么”。
2. 状态为“已接受”的 ADR 解释为什么选择该边界，以及以后怎样变更。
3. 架构页解释制品和组件关系。
4. 指南提供阅读路径；FAQ 和示例不建立实现义务。

> “已接受”表示项目当前采用的工程决定；“待验证设计”表示可评审候选；“尚待确定”表示没有唯一答案；“后续计划”表示不能提前依赖。

每个规范“必须/不得/只有”都应关联机器测试或具名人工权威。实现、论文、专利、演示和模型输出不能反向替代规范。

当前权威源包括作为通用内容标准的 [END-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-core.md)、作为当前封闭内容 Profile 的 [END-P1](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p1.json)、作为实验性容器的 [END-FMT 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-format.md)、[SYN-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md)、[DRO-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)、[TEK-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/tekmor-core.md)与[机器可读登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)。四类对象的不可信输入与失败责任分别见[Endem 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-threat-model.md)、[Synem 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-threat-model.md)、[Dromen 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-threat-model.md)与[Tekmor 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/tekmor-threat-model.md)。公开 HTML 只负责直白解释，不复制第二套条款。

[END-SCEN 自然语言场景语料](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-scenarios.md)用二十七个案例寻找规范缺口，但不属于上述规范义务。只有案例转化为唯一条款、登记验证方式并形成正反向量后，对应判断才可能进入符合性要求。

[SYN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-scenarios.md)、[DRO-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-scenarios.md)与[TEK-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/tekmor-scenarios.md)分别用十个、十五个和十四个场景检查组合闭包、会话契约及证据边界，同样不属于上述规范义务。

## Endem

[Endem 规范](../specifications/endem.html)解释一个根 `skena`、六个语义面、形式显示、来源确认、显式未知、身份和安全边界。ADR-0023 明确 END-CORE 是通用内容标准、END-P1 是封闭内容 Profile、END-FMT 是物理容器；容器接受、Profile 接受和内容接受必须分别报告。ADR-0014 另以 [END-SRCM](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-source-manifest.md)固定首个来源清单。正式来源语言、求值语言、摘要算法、扩展注册表和稳定 ABI 尚未冻结。

判断扩展按问题分别读取：[ADR-0015](../architecture/adr-0015-result-domains.html)分开结果域，[ADR-0016](../architecture/adr-0016-mene-time-model.html)定义持续时间，[ADR-0017](../architecture/adr-0017-negation-and-absence.html)定义否定与缺席，[ADR-0018](../architecture/adr-0018-quantification-and-membership.html)定义量化范围，[ADR-0019](../architecture/adr-0019-measurement-and-thresholds.html)定义测量与阈值，[ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)定义复合事态。它们当前都只冻结抽象内容边界，没有增加 END-P1 物理字段。

## Synem

[Synem 规范](../specifications/synem.html)解释完整闭包、精确绑定、有限无环、权限交集、成员结果分离和条件激活。规范源是 [SYN-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md)；[SYN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-scenarios.md)不属于上述规范义务。当前没有物理 Synem 格式或组件实现。

## Dromen 与 Tekmor

[Dromen 会话契约](../specifications/dromen.html)解释精确会话主体、政策封闭、环境绑定、能力与预算上限、观察责任、只读失效和销毁。规范源是 [DRO-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)；[DRO-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-scenarios.md)不属于上述规范义务。Dromen 永远不是磁盘格式、凭据包或可恢复会话，当前也没有 Praxor 或运行时实现。

[Tekmor 规范](../specifications/tekmor.html)解释主体范围、有限无环溯源、结构化观察、证据类别、完整性、外部有效性评估、相对 `krin` 的覆盖度、决定分离与最小披露。规范源是 [TEK-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/tekmor-core.md)；模型评价只能保持 `model-candidate`。当前没有物理 Tekmor 格式或组件实现。

[结构化诊断规范](../specifications/diagnostics.html)解释稳定机器码、生产语境、失败层次、类型化位置、确定性主错误、受限恢复、外部来源、最小披露、资源预算与原子失败。规范源是 [DIA-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/diagnostics-core.md)，草案机器码见 [DIA-CAT](https://github.com/Noemion/noemion.github.io/blob/main/spec/diagnostic-catalog.md)。诊断不是目标结果、证据、权限或自动修复命令；当前没有物理编码或组件实现。

[外部协议适配规范](../specifications/adapters.html)解释协议版本、对端、能力、调用、映射、状态、产物、错误、取消、重试、交付和安全边界。规范源是 [ADP-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/adapter-core.md)。MCP、A2A、HTTP 与 SDK 对象只保持外部来源；当前没有具体协议 Profile、适配器 API 或组件实现。

允许保留的运行观察、失效原因和决定关系进入 Tekmor 或带范围的会话事件。它们不能重新创建 Dromen 或恢复旧权限。

## ADR 与开放问题

[ADR-0010](../architecture/adr-0010-native-lexicon.html)至 [ADR-0014](../architecture/adr-0014-source-manifest.html)固定现行词汇、Endem 格式、Profile 与来源清单；[ADR-0015](../architecture/adr-0015-result-domains.html)至 [ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)固定判断、时间、否定、量化、测量与复合边界；[ADR-0021](../architecture/adr-0021-synem-closure-and-activation.html)至 [ADR-0026](../architecture/adr-0026-external-protocol-adapters.html)固定 Synem、Tekmor、内容标准分层、Dromen、诊断和外部协议适配边界。ADR-0008 和 ADR-0009 只保存被取代的公开设计历史。具体协议 Profile、物理编码与发行治理集中在[开放问题](../architecture/open-questions.html)。

面向标准化时，规范还需关联互操作配置、正反向量、一致性测试、安全分析和版本演进。面向研究与知识产权时，还应关联假设、现有技术、实验、贡献与公开披露记录。
