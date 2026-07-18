---
layout: "manual"
title: "指南与参考 · Noemion"
page_role: "section"
footer_text: "Noemion · 指南与参考"
permalink: "/docs/index.html"
manual_id: "docs"
manual_group: "start"
manual_order: 0
nav_title: "指南与参考"
page_heading: "指南与参考"
page_lead: "先说明 Noemion 为什么研究人类目标编译，再按你要解决的问题进入案例、架构、开发、应用或规范资料。"
summary: "从项目目的和具体问题出发，选择适合当前任务的阅读路径。"
badges: ["指南", "Endem 手册", "参考"]
manual_is_index: true
manual_index_heading: "按任务与内容类型查找"
---

## 先按问题选择入口

[GNU Coding Standards 的手册结构原则](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)建议按读者要完成的工作和会提出的问题组织文档，而不是照搬内部实现结构。第一次阅读可从具体案例建立职责顺序；需要约束实现时，再进入版本化规范源。

| 你现在要回答什么 | 先读 | 读完以后 |
| --- | --- | --- |
| Noemion 解决什么问题，与 Agent 协议有什么区别 | [入门指南](getting-started.html) | 能分开目标、外部任务状态、权限、证据和最终决定 |
| 现在能否安装，未来怎样发布 | [资源与获取](../downloads/) | 能分清当前公开资料、尚不存在的软件和未来发行必须提供的证据 |
| 一个名称能否进入正式发行 | [术语与读音验证](terminology-and-pronunciation.html) | 能区分职责审查、首次朗读、听辨和发行决定 |
| 当前究竟采用哪些名称，哪些关键字冲突已经消除 | [术语审查结果](terminology-audit.html) | 能找到对象、角色、动作、字段和高风险枚举的当前拼写与迁移依据 |
| 制品怎样形成、组合和进入一次受限运行 | [架构设计](architecture-guide.html) | 能定位 deterministic producer、independent inspector、bounded runner 及其信任边界 |
| 一项修改需要哪些规范和证据 | [开发指南](development-guide.html) | 能写出可证伪主张并找到失败责任与声明上限 |
| 计划中的命令动作分别服务谁 | [Endem 应用参考](endem-reference.html) | 能判断某项动作应保留、合并还是交给外部工具 |
| 某个工程问题由哪份条款约束 | [规范参考](specifications-reference.html) | 能从问题定位 CORE、Profile、ADR 和验证材料 |

指南负责建立概念和阅读路径，不复制第二套技术定义。标为“待验证设计”“尚待确定”或“后续计划”的内容都不是稳定接口。

## 引用和状态

研究、论文、专利、软著和标准提案引用 Noemion 时，必须记录路由、提交标识、状态和权威来源。愿景不能作为实验结论，候选编码不能作为锁定 ABI，规划流程不能作为已经发布的软件能力。
