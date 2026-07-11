---
layout: "manual"
title: "参考索引 · noemlink 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemlink documentation"
permalink: "/tools/noemlink/docs/reference-index.html"
manual_id: "noemlink"
manual_group: "reference"
manual_order: 12
nav_title: "参考索引"
hero_title: "参考索引"
hero_description: "按名称查找命令、对象、重定位候选和安全术语的权威说明。"
summary: "按名称查找命令、对象、重定位候选和安全术语的权威说明。"
badges: ["noemlink", "Phase 4 / Phase 5"]
manual_index_entry: true
---

## 索引使用规则

术语索引帮助定位解释和权威来源，但不取代规范定义。术语只有在对象规范、ADR 或配置中获得稳定定义后，才能被实现和一致性测试作为规范接口使用；仅出现在示例或候选列表中的名称仍可调整。

## 索引

`noemlink`
: [命令行调用](invocation.html)
冲突报告
: [诊断与失败边界](diagnostics.html)
依赖锁定
: [输入与输出](inputs-outputs.html)
NOBJ
: [当前对象格式工程名称与规范状态](../../../specifications/noema-object.html)
链接计划
: [验证—规划—提交中的未提交链接计划](pipeline.html)
披露图
: [HOBJ 链接](horizon-linking.html)
链接映射
: [输出契约](inputs-outputs.html)
R_NIR_*
: [重定位类型候选](relocations.html)
Symbol
: [符号解析](symbol-resolution.html)
AI-NX / AI-RELRO
: [候选装载安全概念](loader-security.html)

## 术语状态

| 类别 | 当前解释 | 权威化条件 |
| --- | --- | --- |
| 工程稳定概念 | Deterministic、NOBJ、NIR、HOBJ、checked arithmetic、内容寻址。 | 仍以对应规范页的成熟度标记为准。 |
| 详细设计对象 | 链接请求、链接计划、链接映射、冲突报告、依赖锁定。 | 需要结构定义、版本策略、诊断和测试向量。 |
| 候选 ABI 名称 | `R_NIR_*`、输出扩展名和具体 CLI 参数。 | 对象格式/CLI 规范和 ADR 冻结编号与布局。 |
| 候选安全术语 | AI-NX、AI-RELRO。 | 威胁分析、适用对象、强制规则和一致性测试获批。 |

## 追溯要求

每个稳定术语必须链接到唯一规范定义、相关 ADR、实现接口、诊断类别和测试向量。别名必须标明首选名称和废止状态；当前开发阶段不保留旧路由或兼容语义。任何解释与规范冲突时，以规范成熟度和经批准决策为准。
