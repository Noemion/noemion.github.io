---
layout: "manual"
title: "工具契约 · noemlink 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemlink documentation"
permalink: "/tools/noemlink/docs/contract.html"
manual_id: "noemlink"
manual_group: "start"
manual_order: 1
nav_title: "工具契约"
hero_title: "工具契约"
hero_description: "说明 noemlink 负责什么、拒绝什么，以及哪些边界可以依赖。"
summary: "说明 noemlink 负责什么、拒绝什么，以及哪些边界可以依赖。"
badges: ["noemlink", "Phase 4 / Phase 5"]
---

## 问题与目标

链接阶段要把多个分别有效的对象组合为一个整体有效的对象。局部有效并不推出组合后仍有效：两个对象可能定义同一强符号、提出互斥约束、要求不同 ABI，或在合并后扩大权限。因此 `noemlink` 的目标不是“尽量生成输出”，而是在确定性规则足以证明组合成立时生成输出，否则以结构化证据拒绝。

## 职责

- 验证并合并兼容 Section 与多层 NIR 图。
- 执行强弱符号、版本、可见性与归档成员解析。
- 重映射节点与产物 ID，并应用类型化重定位。
- 按语义规则合并约束、权限、验收契约与披露图。
- 生成链接映射、依赖闭包、运行 Segment 和可验证诊断。

## 明确非职责

- 不调用模型解决语义冲突。
- 不以最后写入者规则覆盖约束或权限。
- 不自动下载未锁定依赖。
- 不负责运行时求解或后端输入适配。
- 不替代[NOBJ 格式验证](../../../specifications/noema-object.html)、Noema Object System 的装载检查、Agent Harness 的会话策略或 Fulfillment Runtime 的候选评价。

## 核心不变量

| 不变量 | 可观察要求 | 失败结果 |
| --- | --- | --- |
| 确定性 | 相同有效输入集合、配置、锁文件和规范版本产生字节相同或规范定义的等价结果。 | 拒绝该产物并记录非确定来源。 |
| 闭包完整 | 所有强引用、强依赖、权限要求和披露要求均可解析。 | 无输出，生成冲突报告。 |
| 权限单调收敛 | 组合默认取更严格权限；扩大必须有显式、可追溯授权。 | 安全失败，不降级为 warning。 |
| 事务性 | 任一阶段失败都不得留下被误认作有效的部分产物。 | 只保留诊断和可标识的调试中间产物。 |
| 边界安全 | 所有偏移、长度、计数、对齐和 ID 运算使用 checked arithmetic。 | 溢出、越界或资源超限立即失败。 |

## 契约验收

进入实现前，应把上述不变量映射到对象格式条款、算法伪代码、诊断类别和正反测试向量。实现验收至少需要确定性重复构建、输入排列不变性、冲突矩阵、恶意对象语料、资源上限测试，以及由 [noemvalidate](../../noemvalidate/index.html) 对最终产物独立验证。

> 本契约确定职责、不变量和验收方向，但不冻结具体符号规则编号、输出扩展名或 ABI。任何实现差异必须由规范或 ADR 解决，不能由单一实现行为反向成为事实标准。
