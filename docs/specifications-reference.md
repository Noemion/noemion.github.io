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
page_lead: "理解 Endem、Synem、Tekmor、成熟度标记与 ADR 的权威顺序。"
summary: "理解 Endem、Synem、Tekmor、成熟度标记与 ADR 的权威顺序。"
badges: ["Authority", "Maturity", "ADR"]
---

## 权威顺序

1. 版本化 Markdown 条款源定义“必须是什么”。
2. 状态为“已接受”的 ADR 解释为什么选择该边界，以及以后怎样变更。
3. 架构页解释制品和组件关系。
4. 指南提供阅读路径；FAQ 和示例不建立实现义务。

> “已接受”表示项目当前采用的工程决定；“待验证设计”表示可评审候选；“尚待确定”表示没有唯一答案；“后续计划”表示不能提前依赖。

每个规范“必须/不得/只有”都应关联机器测试或具名人工权威。实现、论文、专利、演示和模型输出不能反向替代规范。

当前权威源包括 [END-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-core.md)、[END-FMT 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-format.md)、[SYN-CORE 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md)与[机器可读登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)。Endem 和 Synem 的不可信输入与失败责任分别见[Endem 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-threat-model.md)与[Synem 威胁模型](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-threat-model.md)。公开 HTML 只负责直白解释，不复制第二套条款。

[END-SCEN 自然语言场景语料](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-scenarios.md)用二十七个案例寻找规范缺口，但不属于上述规范义务。只有案例转化为唯一条款、登记验证方式并形成正反向量后，对应判断才可能进入符合性要求。

## Endem

[Endem 规范](../specifications/endem.html)解释一个根 `skena`、六个语义面、形式显示、来源确认、显式未知、身份和安全边界。ADR-0011 已采用实验性容器，ADR-0013 以 END-P1 固定载荷，ADR-0014 又以 [END-SRCM](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-source-manifest.md)固定首个来源清单。正式来源语言、求值语言、摘要算法、扩展注册表和稳定 ABI 尚未冻结。

## Synem

[Synem 规范](../specifications/synem.html)解释完整闭包、精确绑定、有限无环、权限交集、成员结果分离和条件激活。规范源是 [SYN-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md)；[SYN-SCEN](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-scenarios.md)不属于上述规范义务。当前没有物理 Synem 格式或组件实现。

## Dromen 与 Tekmor

Dromen 是 Praxor 为一次受控实现建立的会话状态，不是磁盘格式。[Tekmor 规范](../specifications/tekmor.html)定义对象、环境、策略、事件、证据范围和最终决定记录。模型评价只能作为其中一项不可信输入。

## ADR 与开放问题

[ADR-0010](../architecture/adr-0010-native-lexicon.html)至 [ADR-0014](../architecture/adr-0014-source-manifest.html)固定现行词汇、Endem 格式、Profile 与来源清单；[ADR-0015](../architecture/adr-0015-result-domains.html)、[ADR-0016](../architecture/adr-0016-mene-time-model.html)、[ADR-0017](../architecture/adr-0017-negation-and-absence.html)、[ADR-0018](../architecture/adr-0018-quantification-and-membership.html)、[ADR-0019](../architecture/adr-0019-measurement-and-thresholds.html)与 [ADR-0020](../architecture/adr-0020-composite-situations-and-criteria.html)固定判断、时间、否定、量化、测量与复合边界；[ADR-0021](../architecture/adr-0021-synem-closure-and-activation.html)固定 Synem 组合闭包与条件激活。ADR-0008 和 ADR-0009 只保存被取代的设计历史。其余扩展、远端协议适配和发行治理集中在[开放问题](../architecture/open-questions.html)。

面向标准化时，规范还需关联互操作配置、正反向量、一致性测试、安全分析和版本演进。面向研究与知识产权时，还应关联假设、现有技术、实验、贡献与公开披露记录。
