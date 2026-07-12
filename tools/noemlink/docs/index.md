---
layout: "manual"
title: "noemlink 文档 · Noemion"
page_role: "docs-index"
footer_text: "Noemion · noemlink documentation"
permalink: "/tools/noemlink/docs/index.html"
manual_id: "noemlink"
manual_group: "start"
manual_order: 0
nav_title: "文档"
hero_title: "noemlink 文档"
hero_description: "职责、调用边界、确定性链接流程、安全规则和验证入口。"
summary: "职责、调用边界、确定性链接流程、安全规则和验证入口。"
badges: ["Documentation", "Phase 4 / Phase 5", "12 Topics"]
manual_is_index: true
manual_index_heading: "文档目录"
---

## 为什么单独建立链接器文档

`noemlink` 位于“多个局部对象”成为“一个可装载整体”的信任转换点。符号选择、ID 重映射、约束合并、权限收敛或依赖闭包中的任何隐式规则，都会影响产物语义、安全边界和复现结果。因此它不是普通文件拼接器，每项决定都必须形成可规范、可测试、可诊断的契约。

`noemlink` 尚未发布可执行版本。当前文档记录已经明确的职责和设计契约，规范性定义以[对象规范](../../../specifications/index.html)、经批准的 ADR 和一致性测试为准；CLI 与命令示例展示预期使用流程，实际接口仍在设计中。

## 建议阅读路径

| 读者任务 | 先读 | 需要回答的问题 |
| --- | --- | --- |
| 理解边界 | [工具契约](contract.html)、[输入与输出](inputs-outputs.html) | 哪些决定属于链接器，输入满足什么条件，输出承诺什么。 |
| 检查算法设计 | [处理流程](pipeline.html)、[符号解析](symbol-resolution.html)、[重定位](relocations.html) | 结果如何保持确定、冲突何时失败、ID 如何安全变换。 |
| 检查语义与安全 | [HOBJ 链接](horizon-linking.html)、[装载与安全](loader-security.html) | 约束与权限怎样合并，链接产物如何进入运行时信任域。 |
| 验证实现 | [诊断](diagnostics.html)、[测试与验收](testing.html) | 失败如何定位，哪些测试足以支持发布或研究结论。 |

## 成熟度与证据边界

> CLI 参数、对象扩展名、重定位类型和具体 ABI 仍需相应规范或 ADR 确定；候选示例不构成已批准规范。

当前可作为设计基线的是：Deterministic Profile 无模型、同一有效输入产生可复现结果、对象输入一律不可信、所有偏移和规模运算采用 checked arithmetic、权限不可静默扩大。尚未完成的是记录布局、算法复杂度上限、诊断编号、互操作配置和独立实现验证。

只有规范条款、参考实现测试向量和至少一个独立消费者形成闭环，相关接口才具备成为实现与一致性参考的证据条件。
