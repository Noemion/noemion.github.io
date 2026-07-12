---
layout: manual
title: "格式与成形 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/format.html"
manual_id: "endem"
manual_group: "format"
manual_order: 1
nav_title: "格式与成形"
hero_title: "格式与成形"
hero_description: "从 Goal Card 的五组语义形成具有一个根 aim 的 open Endem。"
summary: "Goal Card、五组语义、候选绑定、确定性 form 与 open 状态。"
badges: ["form", "One Root Aim"]
---

## 最小目标卡

Goal Card 是面向人的来源表达。它至少需要明确以下五组内容：

| 字段组 | 读者要回答的问题 | 不能省略的边界 |
| --- | --- | --- |
| `say` | 实际表达了什么？ | 原文或摘要、语言、来源和精确范围 |
| `aim` | 什么结果才是目标？ | 唯一根目标、结果种类和产物角色 |
| `must` | 哪些条件绝不能违反？ | 硬约束、能力上限、禁止项和未知策略 |
| `done` | 怎样判断已经完成？ | 验收条件、必需 Witness 和决定权威 |
| `open` | 哪些意思还没确定？ | 替代解释、冲突、风险和允许的解决方式 |

一个 Endem 必须且只能有一个根 `aim`。两个可独立完成和验收的目标应分别形成 Endem，再通过 Weave 表达关系。

## 非规范性示意

下面只展示信息职责，不是已经冻结的输入语法：

```yaml
say: "为项目生成一份安全评审报告"
aim: "produce security-review"
must:
  - "不得披露凭据"
  - "只引用已登记来源"
done:
  - "输出包含威胁、影响和可复查依据"
open:
  - "目标读者尚未确认"
```

正式语法仍需决定字段编码、引用、注释、包含关系和版本演进。实现不得因为示例类似 YAML 就假定采用 YAML。

## 候选不能直接成形

自然语言模型或外部系统可以提出目标、约束、验收和替代解释，但这些内容始终是不可信候选。`form` 只接受以下三种处理结果：

1. 由版本化确定性规则从来源重新推导；
2. 绑定到明确授权、范围有限且可撤销的决定；
3. 继续保留在 `open`，不伪装成确认语义。

无法落入其中任一类时，`form` 必须失败并定位来源范围。

## form 的失败原子性

`form` 在完成全部来源、结构、类型、约束和资源检查前，不写出部分可信 Endem。失败至少区分：

- 来源无效或摘要不符；
- 根 `aim` 缺失或不唯一；
- `must` 与 `done` 冲突；
- 候选无权关闭 `open`；
- 引用、计数、大小或深度超限；
- 规范版本或关键特性未知。

## 确定性

相同规范化 Goal Card、绑定决定、配置、依赖和 Core 版本必须产生相同 open Endem 字节。时间、工作目录、哈希表遍历、并发完成顺序和模型随机性不得进入规范字节。
