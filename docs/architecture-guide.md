---
layout: "manual"
title: "架构指南 · Noemion 文档"
page_role: "content"
footer_text: "Noemion · 架构指南"
permalink: "/docs/architecture-guide.html"
manual_id: "docs"
manual_group: "guides"
manual_order: 3
nav_title: "架构指南"
hero_title: "Noemion 架构指南"
hero_description: "从语义来源到可信执行，理解各层职责、对象流转和信任边界。"
summary: "从语义来源到可信执行，理解各层职责、对象流转和信任边界。"
badges: ["Architecture", "Objects", "Trust Boundaries"]
---

## 系统分层

Noema Object 负责组织、链接、装载和完整性；Fulfillment Runtime 负责求解目标并产生可验收结果。两者承担不同的失败责任，不能合并成含义模糊的“模型执行层”。

> **阅读方法：**先确认每层接收什么、产出什么、失败时由谁负责，再阅读具体算法。只要输入输出或失败责任不清楚，就不能用流程图中的箭头推定接口已经成立。

数据依次经过来源或 Horizon Engine、Noesis Core、Noema IR、Noema Object、链接器和装载器。进入动态求解后，Agent Harness 组织上下文、受限能力和反馈循环，Fulfillment Runtime 产生可验收结果。每一步只能增加经过验证的结构或信任，不能绕过前一步的失败。

这套分层首先保障确定性、可组合性、可验证性和失败即拒绝。单次生成质量属于运行或模型评测指标，不能替代对象与信任检查。组件职责见[系统组件](../components/)。

## 对象生命周期

1. 源输入先被解析为保留歧义和证据来源的受约束结构。
2. 确定性 Noesis Core 执行类型检查、规范化、覆盖检查和对象布局。
3. Noema Object 暴露 Section、符号和类型化重定位，对象工具和链接器据此读取文件。
4. 链接器解析依赖并构造可验证闭包，必要时输出 Horizon Object。
5. 装载器验证结构、签名、策略和 Segment 属性，再把不可变句柄交给 Fulfillment Runtime。
6. Agent Harness 根据执行配置建立隔离会话，逐步披露上下文并验证每次能力调用。
7. Fulfillment Runtime 求解目标并产生具体结果，不回写已经签名的对象。

详细生命周期见[对象生命周期与信任边界](../architecture/noema-lifecycle.html)。

## 编译与链接边界

- Horizon Engine 或其他模型只能提出候选语义，不能直接生成 NOBJ。
- Noesis Core 决定类型、规范化结果、覆盖结论和确定性布局。
- 链接器解析符号、重映射 ID、应用类型化重定位并合并依赖闭包。
- 遇到硬约束、权限或接口冲突时必须失败，不调用模型“猜一个答案”。

具体编译阶段、符号版本模型和重定位编号仍待规范确定。

## 装载与运行边界

- 装载器负责安全解析、完整性验证、内存映射和重定位后冻结。
- Fulfillment Runtime 只读取已经验证的对象和显式运行配置。
- 将对象转换为模型输入只是可能的实现方式之一，不属于对象格式本身。
- 运行期派生产物必须与签名对象分离并记录来源。
- Agent Harness 只能暴露显式授权的类型化能力；模型提出参数，但确定性策略决定是否执行。
- UI、日志、指标、追踪和测试结果作为结构化观察返回会话，不能由模型陈述替代。
- 验收契约、预算、停止条件和人工升级条件在执行前确定，模型不能自行宣布任务完成。

链接、装载和运行职责见[Noema Object System](../components/noema-object-system.html)。
智能体控制面的上下文、能力和反馈边界见[Agent Harness](../components/agent-harness.html)。

## 信任边界

- **不可信输入：**模型输出、外部对象、归档成员、清单、调试伴随文件和依赖声明。
- **确定性核心：**解析、类型检查、布局、重定位、哈希、签名范围和策略验证。
- **受限模型能力：**候选提取、层级聚合、检索路由和封闭任务头，不拥有对象写入权。
- **显式授权：**权限扩大、动态依赖、外部能力和披露预算必须由配置或策略授权。
- **可观察执行：**能力调用、环境变化、拒绝、恢复和验收结论必须关联到会话、对象和环境指纹。

## 尚待确定的接口

**尚待确定：**消费端 ABI、动态依赖、长上下文状态同步、对象扩展名、连续表示互操作和模型包格式仍需证据、规范或 ADR。

架构主张需要分别用确定性构建、畸形样例/模糊测试、链接冲突矩阵、篡改与回滚、跨 Fulfillment Runtime 等价和目标设备资源实验验证。当前架构图是待验证的概要设计，不是性能或产业可行性证明。

**后续计划：**第一阶段安全二进制核心稳定后，才评估 Horizon Engine 训练、量化和跨设备 Fulfillment Runtime。

[查看完整开放问题清单](../architecture/open-questions.html)
