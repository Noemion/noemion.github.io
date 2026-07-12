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

当前 Endem 条款源是 END-CORE 0.1.0-draft：[https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-core.md](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-core.md)。机器可读登记保存术语、条款、成熟度、实现状态和验证引用：[https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)。威胁模型把不可信输入和失败责任映射到条款：[https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-threat-model.md](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-threat-model.md)。公开 HTML 提供直白解释，不复制第二套条款。

## Endem

[Endem 规范](../specifications/endem.html)解释一个根 `skena`、六个语义面、形式显示、来源确认、显式未知、身份和安全边界。当前已接受语义骨架与 `.endem` 工程扩展名；魔数、字段宽度、记录编号、求值语言、摘要算法和扩展注册表尚未冻结。

## Synem

[Synem 规范](../specifications/synem.html)定义多 Endem 引用解析、固定依赖、冲突、能力交集、发布范围和外部签名主体。Synem 只有在真实组合消费者存在时才实现；单一自包含 Endem 不需要额外封装。

## Dromen 与 Tekmor

Dromen 是 Praxor 为一次受控实现建立的会话状态，不是磁盘格式。[Tekmor 规范](../specifications/tekmor.html)定义对象、环境、策略、事件、证据范围和最终决定记录。模型评价只能作为其中一项不可信输入。

## ADR 与开放问题

[ADR-0010](../architecture/adr-0010-native-lexicon.html)是当前词汇、六语义面与事态分层决定；ADR-0008 和 ADR-0009 只保存已被取代的设计历史。编码、实现语言、扩展注册表、远端协议适配和发行治理等未决事项集中在[开放问题](../architecture/open-questions.html)。

面向标准化时，规范还需关联互操作配置、正反向量、一致性测试、安全分析和版本演进。面向研究与知识产权时，还应关联假设、现有技术、实验、贡献与公开披露记录。
