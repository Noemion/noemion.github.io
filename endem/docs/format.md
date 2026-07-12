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
hero_description: "从 Source Card 的五组投影语义形成具有一个根 case 的 open Endem。"
summary: "来源记号、意义投影、可能事态、满足条件、未决边界与确定性 form。"
badges: ["form", "One Root Case"]
---

## 最小来源卡

Source Card 是面向人的来源表达。进入 Endem 前必须形成以下五组内容：

| 字段组 | 读者要回答的问题 | 不能省略的边界 |
| --- | --- | --- |
| `say` | 来源出现了哪些记号？ | 原文或摘要、语言、主体、来源和精确范围 |
| `mean` | 这些记号怎样取得意义？ | 符号、指称、关系、作用域、极性、时间、力量和来源映射 |
| `case` | 若满足，事情应当怎样？ | 一个根对象—关系图与 seek、keep、avoid 力量 |
| `when` | 怎样从观察判断满足？ | 满足条件、Witness 类型、unknown/error 处理和决定权威 |
| `open` | 哪些投影还没确定？ | 替代解释、冲突、测量、风险和允许的解决方式 |

一个 Endem 必须且只能有一个根 `case`。两个可独立完成和验收的目标应分别形成 Endem，再通过 Weave 表达关系。

## 非规范性示意

下面只展示信息职责，不是已经冻结的输入语法：

```yaml
say: "为项目生成一份安全评审报告"
mean:
  - "project := 已登记项目主体"
  - "security-review := 具备威胁、影响和依据关系的报告"
case:
  root: "seek produced(security-review, project)"
when:
  - "met when required observations have scoped Witness records"
open:
  - "目标读者尚未确认"
```

正式语法仍需决定字段编码、引用、注释、包含关系和版本演进。实现不得因为示例类似 YAML 就假定采用 YAML。

## 候选不能直接成形

自然语言模型或外部系统可以提出意义、关系、力量、满足条件和替代解释，但这些内容始终是不可信候选。`form` 只接受以下三种处理结果：

1. 由版本化确定性规则从来源重新推导；
2. 绑定到明确授权、范围有限且可撤销的决定；
3. 继续保留在 `open`，不伪装成确认语义。

违反 Profile 或没有任何允许投影时，`form` 必须以 `no-sense` 失败并定位来源范围；存在多个可表达候选但无法选择时才进入 `open`。

## form 的失败原子性

`form` 在完成全部来源、结构、类型、约束和资源检查前，不写出部分可信 Endem。失败至少区分：

- 来源无效或摘要不符；
- 根 `case` 缺失或不唯一；
- `mean` 与 `case` 的符号或关系位置不一致；
- `case` 与 `when` 冲突或缺少满足映射；
- 候选无权关闭 `open`；
- 引用、计数、大小或深度超限；
- 规范版本或关键特性未知。

## 确定性

相同规范化 Source Card、投影决定、配置、依赖和 Core 版本必须产生相同 open Endem 字节。时间、工作目录、哈希表遍历、并发完成顺序和模型随机性不得进入规范字节。
