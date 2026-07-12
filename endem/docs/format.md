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
page_heading: "格式与成形"
page_lead: "从 Rhem Source 的六个语义面形成具有一个根 skena 的 nascent Endem。"
summary: "来源、意义、可能事态、目标方向、满足判据、未决边界与确定性 poie。"
badges: ["poie", "One Root Skena"]
---

## 最小来源卡

Rhem Source 是面向人的来源表达。进入 Endem 前必须形成以下六个语义面：

| 语义面 | 读者要回答的问题 | 不能省略的边界 |
| --- | --- | --- |
| `rhem` | 来源出现了哪些记号？ | 原文或摘要、语言、主体、来源和精确范围 |
| `semion` | 这些记号怎样取得意义？ | 符号、指称、关系、作用域、极性、时间和来源映射 |
| `skena` | 哪一种中性可能事态构成目标内容？ | 一个根对象—关系图、组合与极性 |
| `telis` | 目标要求事态变化还是持续？ | kine 或 mene、适用时间边界；不重复表达否定 |
| `krin` | 怎样把 phain 与 skena 比较？ | 结构比较、Tekmor 类型、agno/fault 处理和决定权威 |
| `apor` | 哪些投影还没确定？ | 替代解释、冲突、测量、风险和允许的解决方式 |

一个 Endem 必须且只能有一个根 `skena`。两个可独立完成和验收的目标应分别形成 Endem，再通过 Synem 表达关系。

## 非规范性示意

下面只展示信息职责，不是已经冻结的输入语法：

```yaml
rhem: "为项目生成一份安全评审报告"
semion:
  - "project := 已登记项目主体"
  - "security-review := 具备威胁、影响和依据关系的报告"
skena:
  root: "produced(security-review, project)"
telis:
  mode: "kine"
krin:
  - "met if required phain relations have scoped Tekmor records"
apor:
  - "目标读者尚未确认"
```

正式语法仍需决定字段编码、引用、注释、包含关系和版本演进。实现不得因为示例类似 YAML 就假定采用 YAML。

## 候选不能直接成形

自然语言模型或外部系统可以提出意义、关系、目标方向、满足条件和替代解释，但这些内容始终是不可信候选。`poie` 只接受以下三种处理结果：

1. 由版本化确定性规则从来源重新推导；
2. 绑定到明确授权、范围有限且可撤销的决定；
3. 继续保留在 `apor`，不伪装成确认语义。

违反 Profile 或没有任何允许投影时，`poie` 必须以 `aseme` 失败并定位来源范围；存在多个可表达候选但无法选择时才进入 `apor`。

## poie 的失败原子性

`poie` 在完成全部来源、结构、类型、约束和资源检查前，不写出部分可信 Endem。失败至少区分：

- 来源无效或摘要不符；
- 根 `skena` 缺失或不唯一；
- `semion` 与 `skena` 的符号或关系位置不一致；
- `telis` 缺失、重复表达否定或时间边界无效；
- `skena` 与 `krin` 冲突，或 phain 没有可比较映射；
- 候选无权关闭 `apor`；
- 引用、计数、大小或深度超限；
- 规范版本或关键特性未知。

## 确定性

相同规范化 Rhem Source、投影决定、配置、依赖和 Poiet 版本必须产生相同 nascent Endem 字节。时间、工作目录、哈希表遍历、并发完成顺序和模型随机性不得进入规范字节。
