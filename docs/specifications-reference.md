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
hero_title: "Noemion 规范参考指南"
hero_description: "理解 Endem、Weave、Witness、成熟度标记与 ADR 的权威顺序。"
summary: "理解 Endem、Weave、Witness、成熟度标记与 ADR 的权威顺序。"
badges: ["Authority", "Maturity", "ADR"]
---

## 权威顺序

1. 版本化规范定义“必须是什么”。
2. Accepted ADR 定义为什么选择该边界以及怎样变更。
3. 架构页解释制品和组件关系。
4. 指南提供阅读路径；FAQ 和示例不建立实现义务。

> “已接受”表示项目当前采用的工程决定；“待验证设计”表示可评审候选；“尚待确定”表示没有唯一答案；“后续计划”表示不能提前依赖。

每个规范“必须/不得/只有”都应关联机器测试或具名人工权威。实现、论文、专利、演示和模型输出不能反向替代规范。

## Endem

[Endem 规范](../specifications/endem.html)定义一个根 `case`、五组投影语义、形式显示、来源确认、显式未知、身份和规范编码边界。当前已接受语义骨架与 `.endem` 工程扩展名；magic、字段宽度、记录编号、求值语言、摘要算法和扩展 registry 尚未冻结。

## Weave

[Weave 规范](../specifications/weave.html)定义多 Endem 引用解析、固定依赖、冲突、能力交集、发布范围和外部签名主体。Weave 只有在真实组合消费者存在时才实现；单一自包含 Endem 不需要额外封装。

## Frame 与 Witness

Frame 是 Runner 内部不可变加载态，不是磁盘格式。[Witness 规范](../specifications/witness.html)定义对象、环境、策略、事件、证据范围和 Acceptance Decision 的不可变记录。模型的 Candidate Assessment 只能是其中一项不可信输入。

## ADR 与开放问题

[ADR-0008](../architecture/adr-0008-endem-system.html)是当前词汇与应用拓扑决定；更早的名称决定只作为被替代的历史记录。编码、实现语言、扩展 registry、远端协议 gateway 和发行治理等未决事项集中在[开放问题](../architecture/open-questions.html)。

面向标准化时，规范还需关联互操作 profile、正反向量、一致性测试、安全分析和版本演进；面向研究与知识产权时，应关联假设、现有技术、实验、贡献与公开披露记录。
