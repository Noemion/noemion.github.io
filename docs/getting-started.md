---
layout: "manual"
title: "入门指南 · Noemion 文档"
page_role: "content"
footer_text: "Noemion · 入门指南"
permalink: "/docs/getting-started.html"
manual_id: "docs"
manual_group: "start"
manual_order: 1
nav_title: "入门指南"
hero_title: "Noemion 入门指南"
hero_description: "从项目为什么存在开始，理解 Noema IR、Noema Object、Horizon Object 和确定性信任边界。"
summary: "从项目为什么存在开始，理解 Noema IR、Noema Object、Horizon Object 和确定性信任边界。"
badges: ["Getting Started", "Design Stage", "No Release Yet"]
---

## 从这里开始

Noemion 不是把提示词、文本或 Skill 包换一种二进制编码，而是为生成式计算建立可机器分析、验证、重定位、链接和执行的目标与约束对象体系。

它试图解决的不是“如何写出更好的单次提示”，而是目标、约束、证据、歧义、依赖和权限如何成为可检查、可组合、可复现的长期工程对象。第一次接触 Noemion 时，建议先阅读[项目背景与边界](../about/background.html)，再依次了解对象、架构和工具链。

## 核心对象

- **[Noema IR（NIR）](../specifications/noema-ir.html)：**表达目标、解空间、硬约束、软偏好、歧义、推断权限、证据要求和验收条件。
- **[Noema Object（NOBJ）](../specifications/noema-object.html)：**把 NIR 封装为带符号、类型化引用和完整性信息的可重定位对象。
- **[Horizon Object（HOBJ）](../specifications/horizon-object.html)：**保存可以按任务和权限逐步披露的共享知识与依赖，不等同于压缩提示词。

## 信任与确定性

- Deterministic Profile 不调用模型，结果确定且可复现。
- 只有确定性的 Noesis Core 能生成 NIR/NOBJ。
- 模型输出和所有对象输入均视为不可信。
- 歧义是一等信息；宁可保留未决语义，也不能制造错误确定性。
- 偏移、长度、计数、索引和对齐计算必须使用 checked arithmetic。

完整生命周期见[对象生命周期与信任边界](../architecture/noema-lifecycle.html)。

## 推荐阅读路径

1. 从[项目背景](../about/)理解问题、非目标和可证伪命题。
2. 阅读[架构指南](architecture-guide.html)建立端到端系统图和信任边界。
3. 进入[规范参考](specifications-reference.html)区分现行设计、待验证设计和尚待确定的事项。
4. 通过[工具参考](tools-reference.html)理解各阶段工具职责。
5. 准备参与实现、研究或标准化时阅读[开发指南](development-guide.html)及其中的证据和治理要求。

研究者应追踪假设、基线、实验和失败案例；实现者应追踪规范、ADR、测试和版本；标准评审者应追踪术语、规范性条款、配置和互操作证据。

## 当前项目状态

> **设计阶段：**当前重点是规范与安全二进制核心，尚未发布可执行编译器、Fulfillment Runtime 或正式安装包。工具名称表示计划中的职责边界，不代表存在可调用命令或稳定接口。

目前已经明确问题范围、架构关系、工具职责和部分规范不变量，但还没有性能、互操作性、跨模型等价或产业价值的实现证据。CLI、扩展名、ABI、重定位编号和模型工程细节仍需规范、ADR、原型和实验确定。

## 下一步

**后续计划：**规范、安全读取器/对象写入器、验证器和确定性 Noesis Core 完成实现与验证后，项目才会准备可安装工具和 Fulfillment Runtime。

- [继续阅读架构指南](architecture-guide.html)：了解对象如何编译、链接、装载和执行。
- [查看使用与获取状态](installation-and-usage.html)：了解当前能获取什么，以及正式发布前不能做什么。
