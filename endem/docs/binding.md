---
layout: manual
title: "绑定与组合 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/binding.html"
manual_id: "endem"
manual_group: "binding"
manual_order: 2
nav_title: "绑定与组合"
page_heading: "绑定与组合"
page_lead: "解析 Endem 的待确认引用与跨目标关系，形成 coherent Endem 或 Synem。"
summary: "pleko 输入、内容寻址、冲突、能力收敛、Synem 和 Pleko Iknem。"
badges: ["pleko", "Synem"]
---

## 什么时候需要 pleko

单个 Endem 可以在不依赖其他制品时独立进入 coherent 状态。只有出现跨 Endem 定义、产物、能力、约束或验收引用时，`pleko` 才建立 Synem。

> Synem 是至少两个精确 Endem 的完整传递闭包，不是普通文件归档，也不是为模型自动扩展上下文的知识包。规范边界见 [SYN-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/synem-core.md) 与 [ADR-0021](../../architecture/adr-0021-synem-closure-and-activation.html)。

## 正式输入

`pleko` 读取：

- 两个或更多通过所需生产 `elenk` 的 Endem；
- 声明命名空间、冲突、缺失、循环和权限规则的组合策略；
- 以内容摘要锁定外部对象的依赖锁；
- 关闭高风险 `apor` 项时所需的授权决定。

它不得把当前工作目录、环境变量、目录枚举顺序、网络搜索结果或“最新版本”当作隐式输入。

## 解析顺序

1. 验证成员身份、状态、规范版本和必需特性。
2. 展开全部必需传递依赖，收集跨对象引用、产物、能力与验收依赖。
3. 只从锁定候选中解析唯一精确内容身份；名称和范围不能替代最终绑定。
4. 检查硬约束冲突、能力上限、缺失行为和循环。
5. 为每项选择或拒绝产生 Pleko Iknem。
6. 稳定排序成员与解析记录，重新运行生产 `elenk`。

## 不变量

| 维度 | pleko 必须保持 |
| --- | --- |
| `semion` | 符号、指称、关系位置和作用域不能静默改写 |
| `skena` | 每个 Endem 继续只有一个根中性事态，组合与极性不被改写 |
| `telis` | kine/mene 与时间边界只能保持或收紧 |
| `krin` | 组合不能让满足条件更容易或丢失决定权威 |
| `apor` | 每项都被授权决定、继续阻断 coherent 状态或导致失败；不得改写为 agno |
| 能力 | 多对象组合只能保持或收紧授权上限 |
| 身份 | 相同锁定输入和策略得到相同解析结果 |
| 结果 | 成员判断与决定保持各自身份，不产生隐式总体 met、accepted 或 completed |

## 循环与可选依赖

第一版拒绝必需依赖循环。未来只有在固定点语义、资源上限、披露顺序、验收顺序和跨实现向量都明确后，才可以增加受限循环。

可选依赖必须声明缺失时的可观察行为。若缺失会改写 `semion`、削弱 `skena`、简化 `krin` 或扩大能力，它就不能标为可选。

## 条件激活

形成时条件若决定成员是否进入闭包，必须在 Synem 身份形成前解析。会话期条件只能选择固定闭包中的成员，并使用 `active / inactive / unresolved / error` 独立状态；未激活成员没有本次满足结果，激活也不授予能力。当前没有可执行守卫语法或 Drasor 实现。

## Pleko Iknem

Pleko Iknem 记录输入成员、候选集合、选择规则、冲突、拒绝和结果摘要。它使组合过程可重放，但不证明依赖将永久可用，也不证明组合任务已经完成。
