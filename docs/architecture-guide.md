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

**已确认原则：**对象格式负责组织、链接、装载和完整性；Runtime 负责生成式求解与 Lowering。二者不能用一个模糊“模型执行层”合并。

> **阅读方法：**先确认每层接收什么、产出什么、失败时由谁负责，再阅读具体算法。只要输入输出或失败责任不清楚，就不能用流程图中的箭头推定接口已经成立。

处理路径依次为：Source / NSFE → Compiler Core → GSIR / GOBJ → Linker / SSO → Loader / Runtime。

分层优先保障确定性、可组合、可验证、关闭失败和可演进；单次生成质量属于 Runtime 或模型评测指标，不能覆盖对象与信任边界。组件职责入口见[系统组件](../components/)。

## 对象生命周期

1. 源输入先被解析为保留歧义和证据来源的受约束结构。
2. 确定性 Compiler Core 执行类型检查、规范化、覆盖检查和对象布局。
3. GOBJ 暴露 Section、符号和类型化重定位，供对象工具与链接器消费。
4. Linker 解析依赖并构造可验证闭包，必要时输出 SSO。
5. Loader 验证结构、签名、策略和 Segment 属性，再交给 Runtime。
6. Runtime 求解目标并 Lowering 到具体执行表面，不反写已签名对象。

详细生命周期见[对象生命周期与信任边界](../architecture/object-lifecycle.html)。

## 编译与链接边界

- NSFE 或其他模型只能提出候选语义，不能直接生成 GOBJ。
- Compiler Core 决定类型、规范化结果、覆盖结论和确定性布局。
- Linker 解析符号、重映射 ID、应用类型化重定位并合并依赖闭包。
- 遇到硬约束、权限或接口冲突时必须失败，不调用模型“猜一个答案”。

**设计提案：**具体 Pass 划分、符号版本模型和重定位编号仍待规范冻结。

## 装载与运行边界

- Loader 负责安全解析、完整性验证、映射和重定位后冻结。
- Runtime 只消费已验证对象和显式 Run Profile。
- Prompt Rendering 是可能的 Lowering 目标之一，但不是对象格式本身。
- 运行期派生产物必须与签名对象分离并记录来源。

链接装载组件说明见[Linker、Loader 与 Runtime](../components/linker-loader.html)。

## 信任边界

- **不可信输入：**模型输出、外部对象、归档成员、Manifest、调试伴随文件和依赖声明。
- **确定性核心：**解析、类型检查、布局、重定位、哈希、签名范围和策略验证。
- **受限模型能力：**候选提取、层级聚合、检索路由和封闭任务头，不拥有对象写入权。
- **显式授权：**权限扩大、动态依赖、外部能力与披露预算必须由 Profile 或策略授权。

## 开放问题

**开放问题：**消费端 ABI、动态依赖、长上下文状态同步、最终对象命名、连续表示互操作和模型包格式仍需证据、规范或 ADR。

架构主张需要分别用确定性构建、Malformed/Fuzz、链接冲突矩阵、篡改与回滚、跨 Runtime 等价和目标设备资源实验验证。当前架构图是待验证的概要设计，不是性能或产业可行性证明。

**未来阶段：**第一阶段安全二进制核心稳定后，才评估 NSFE 训练、量化和跨设备 Runtime。

[查看完整开放问题清单](../architecture/open-questions.html)
