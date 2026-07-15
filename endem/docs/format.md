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
page_lead: "把受控来源表达分解为六个语义面，并形成只有一个根 skena 的 nascent Endem。"
summary: "来源、意义、可能事态、目标方向、满足判据、待确认事项与确定性 ktise。"
badges: ["ktise", "单一根事态"]
---

## 最小来源表达

受控来源表达是面向人的原始输入。Ktisor 形成 Endem 前，必须把它映射为以下六个语义面：

| 语义面 | 读者要回答的问题 | 不能省略的边界 |
| --- | --- | --- |
| `rhem` | 来源出现了哪些记号？ | 原文或摘要、语言、主体、来源和精确范围 |
| `semion` | 这些记号怎样取得意义？ | 符号、指称、关系、作用域、极性、时间和来源映射 |
| `skena` | 哪一种中性可能事态构成目标内容？ | 一个根对象—关系图、组合与极性 |
| `telis` | 目标要求事态变化还是持续？ | kine 或 mene；mene 还需 fixed/elapsed 范围与 strict/budgeted 连续性；不重复表达否定 |
| `krin` | 怎样把 phain 与 skena 比较？ | 结构比较、Iknem 类型、agno/fault 处理和决定权威 |
| `apor` | 哪些投影还没确定？ | 替代解释、冲突、测量、风险和允许的解决方式 |

一个 Endem 必须且只能有一个根 `skena`。两个可独立完成和验收的目标应分别形成 Endem，再通过 Synem 表达关系。

## 非规范性示意

下面只展示信息职责，不是已经锁定的输入语法：

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
  - "met if required phain relations have scoped Iknem records"
apor:
  - "目标读者尚未确认"
```

[ADR-0014](../../architecture/adr-0014-source-manifest.html) 已为未来 Ktisor 设计逐行来源清单；上面的 YAML 仍只是职责示意，不是该语法。正式来源语言仍需解决注释、包含关系、版本演进和错误恢复。实验性 `.endem` 容器由 END-FMT 0.1 定义；END-P1 已固定未来首条实现路径评审所需的字段、枚举、排序和引用闭包，但它仍不是稳定 ABI。

精确容器义务见 [END-FMT 条款源](https://github.com/Noemion/noemion.github.io/blob/main/spec/endem-format.md)。END-P0 只保留为结构实验；首条实现路径必须从 [END-P1 设计 Profile](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p1.json) 开始评审，只允许 nascent、kine、六个关键记录和无压缩载荷。

## 候选不能直接成形

自然语言模型或外部系统可以提出意义、关系、目标方向、满足条件和替代解释，但这些内容始终是不可信候选。`ktise` 只接受以下三种处理结果：

1. 由版本化确定性规则从来源重新推导；
2. 绑定到明确授权、范围有限且可撤销的决定；
3. 继续保留在 `apor`，不伪装成确认语义。

违反 Profile 或没有任何允许投影时，`ktise` 必须以 `aseme` 失败并定位来源范围；存在多个可表达候选但无法选择时才进入 `apor`。

## ktise 的失败原子性

`ktise` 在完成全部来源、结构、类型、约束和资源检查前，不写出部分可信 Endem。失败至少区分：

- 来源无效或摘要不符；
- 根 `skena` 缺失或不唯一；
- `semion` 与 `skena` 的符号或关系位置不一致；
- `telis` 缺失、重复表达否定或时间边界无效；
- `skena` 与 `krin` 冲突，或 phain 没有可比较映射；
- 候选无权关闭 `apor`；
- 引用、计数、大小或深度超限；
- 规范版本或关键特性未知。

## 确定性

确定性先要求输入闭合。形成操作必须固定实际进入 `rhem` 的解码文本与文本槽、严格解码 Profile、显式变换和损失，以及投影决定、配置、依赖、END-CORE、内容 Profile、END-FMT 与 Ktisor 版本。相同的封闭形成输入必须产生相同规范结果；在同一精确格式草案和 Profile 内，还必须产生逐字节相同的 nascent Endem。

这项保证不使用“规范化来源”作为捷径。END-SRCM 会把 LF 与 CRLF 解释为同一行边界，也会展开转义；因此两个来源文件可能产生相同的解码输入，却仍有不同的原始字节身份。显示文本、调试导出或重新排版的来源都是派生视图，除非另有锁定的变换与保留关系，否则不能作为原文件的逆变换或语义等价证明。

Noemion 当前也不提出通用 round-trip 要求。只有精确声明源域、目标域、变换、保留属性、损失和失败责任后，回转测试才能证明这些已声明属性；它不能证明所有字节、意义、授权、证据或接受状态都相同。
