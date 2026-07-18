---
layout: "manual"
title: "术语审查结果 · Noemion"
page_role: "content"
footer_text: "Noemion · 术语审查结果"
permalink: "/docs/terminology-audit.html"
manual_id: "docs"
manual_group: "guides"
manual_order: 3
nav_title: "术语审查结果"
page_heading: "术语审查结果"
page_lead: "逐项说明当前对象、角色、动作、字段和高风险枚举为什么保留或改名，以及关键字检查覆盖到哪里。"
summary: "查看当前词表、已退役名称、编程语言关键字冲突和仍需真实人类验证的名称。"
badges: ["123 个登记术语", "35 个机器标识", "2026-07-18"]
---

## 直接结论

当前机器登记包含 123 个术语。当前审查另外把 35 个会直接进入字段、动作、角色或高风险枚举的机器标识单独列出，并与 11 个声明版本的语言关键字语料作精确比较。当前机器标识没有命中该语料。

`Noemion` 与 `Endem` 是仅保留的两个造词。它们承担项目品牌和核心制品身份，仍未取得人类读音验证。其余没有独立品牌职责的对象、角色和动作改用普通职责名称。

## 现在应该怎样称呼

| 类型 | 当前名称 | 一句话解释 |
| --- | --- | --- |
| 项目 | Noemion | 研究领域、项目与社区总名 |
| 核心制品 | Endem | 一项独立有效、可检查的期望终态单元 |
| 组合对象 | Endem closure | 两个或更多 Endem 的完整解析闭包 |
| 会话对象 | session contract | 一次运行允许使用什么、受哪些政策和预算限制 |
| 证据对象 | evidence entry | 一项观察或推导能够支持什么范围的主张 |
| 写入责任 | deterministic producer | 只从获准输入确定性地产生制品 |
| 读取责任 | independent inspector | 用独立、只读且有界的路径检查实际制品 |
| 运行责任 | bounded runner | 只在本次会话允许的能力和预算内尝试动作 |

公开动作是 `form`、`lint`、`compose`、`inspect` 和 `run`。这些词分别表示形成目标、生产侧检查、形成闭包、独立检查和有界运行；它们不是已经实现的命令。

## 六个字段不再要求读者记词源

| 当前字段 | 保存什么 | 不保存什么 |
| --- | --- | --- |
| `source_expression` | 原始表达、媒介、语言和可重定位范围 | 系统采用的解释 |
| `meaning_projection` | 经规则或具名权威确认的符号、指称和关系 | 动作授权 |
| `situation` | 中性、可比较的可能事态 | 目标方向和实际观察 |
| `goal_direction` | 要求事态达到还是保持成立 | 谁执行、是否已经完成 |
| `satisfaction_criteria` | 观察、证据、未知处理和决定责任 | 观察结果本身 |
| `unresolved_meaning` | 尚不能唯一确认的意义缺口 | 观察不足或运行故障 |

`structured_observation` 保存结构化观察输入。它不同于 `evidence entry`：前者记录看到了什么，后者还必须说明主体、范围、方法、来源、有效性和限制。

## 哪些冲突已经被消除

| 原值或候选 | 冲突 | 当前名称 |
| --- | --- | --- |
| `grant` | PostgreSQL SQL 关键字 | `allowed` |
| `defer` | Go 与 Swift 关键字 | `pending` |
| `fixed` | C# 关键字 | `utc_window` |
| `all` | PostgreSQL SQL 关键字 | `every` |
| `some` | Swift 与 PostgreSQL SQL 关键字 | `at_least_one` |
| `check` | PostgreSQL SQL 关键字 | `lint` |

授权结果完整写作 `allowed / denied / pending`。时间范围写作 `utc_window / elapsed_window`。量化写作 `every / at_least_one`。这些替换同时提高了字段自解释性，而不只是躲开关键字。

## 检查覆盖到哪里

当前语料覆盖 C23、C++23、Rust、Go 1.26、Python 3.14、Java 25、ECMAScript 2026、Swift、Kotlin、C# 和 PostgreSQL 18。机器检查采用大小写无关的精确标识比较，并把人类短语转换为 snake_case 后再比较。

这不是“永远不会与任何编程语言冲突”的保证。语言会演进，项目也可能增加新的目标平台；每次发行必须记录实际语料版本并重新检查。完整语料及来源保存在[关键字语料登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/keyword-corpus.json)中。

## 旧名称怎样处理

旧名称只保留在历史 ADR、名称审查和研究提案中，用来解释为什么改变。当前规范、字段、首页卡片、导航和测试不提供旧名称别名，也不把旧路由重定向到新页面。

完整迁移决定见 [ADR-0037](../architecture/adr-0037-terminology-simplification.html)。机器可读的逐项替换和原因见[术语审查登记](https://github.com/Noemion/noemion.github.io/blob/main/spec/terminology-audit.json)。

## 仍待真实人类验证

人类口头验证尚未完成。

`Noemion` 与 `Endem` 仍须让未接触项目的人完成朗读、听写和职责匹配。通过关键字检查、能写出 IPA、TTS 发音自然或 ASR 转写正确，都不能证明真实会议中的口头区分已经通过。

在验证完成前，公开说明先写职责，再给精确拼写。例如先说“最小目标制品（Endem）”，不要假设听者已经知道名称怎样读。
