---
layout: manual
title: "Text NIR 输入契约 · morphe 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/text-nir-contract.html"
manual_id: "morphe"
manual_group: "start"
manual_order: 1
nav_title: "Text NIR 输入契约"
hero_title: "Text NIR 输入契约"
hero_description: "定义文本输入必须显式表达的结构、引用、来源和错误状态。"
summary: "Text NIR 语法层应显式承载的 NIR 记录、依赖和来源信息。"
badges: ["morphe", "Explicit Semantics"]
---

## 输入组成

Text NIR Source Package 至少包含规范化 UTF-8 文本、来源根、内容摘要、include 清单、结构定义依赖和目标编码 Profile。include 必须位于允许根目录或内容寻址存储中，并绑定摘要；文件系统搜索路径不能静默改变输入闭包。

## 必须显式声明

| 内容 | 要求 |
| --- | --- |
| Module | NIR 版本、命名空间、Profile、根目标与必需特性。 |
| Node / Edge | 记录类别、类型、局部 ID、关系类型、作用域与引用。 |
| Constraint | 硬软强度、操作符、操作数、冲突和 unknown 处理。 |
| Ambiguity | 替代项、状态和解决策略；不能只用注释描述。 |
| Acceptance | 结果结构、评价器、证据、unknown 行为和决定权威。 |
| Capability / Artifact | 参数结构、授权上限、输出结构和消费者角色。 |
| Origin | 需要保留的来源摘要、跨度和决定引用。 |
| Imports | 外部符号类别、版本范围和强弱依赖。 |

## 汇编器不会推断

- 缺失类型、作用域或符号版本。
- 某个约束应当是 hard 还是 soft。
- unknown 应当拒绝、继续还是请求人工判断。
- 未声明的外部资源、评价器、模型、策略或能力。
- 自然语言注释中暗示但没有结构化声明的规则。

## 规范化前置条件

文本必须先通过语法和 Unicode 验证，再建立记录。禁止使用重复定义、不可见控制字符、混淆标识符、未声明编码、路径穿越 include、循环 include 或超出深度/总量预算的展开。

## 错误定位

每条诊断必须指向来源文件身份、跨度单位、起点和长度，并给出稳定错误类别。错误恢复只能用于继续发现更多诊断，不能让带错误的记录进入对象写入计划。
