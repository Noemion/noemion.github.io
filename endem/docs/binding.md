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
hero_title: "绑定与组合"
hero_description: "解析 Endem 的未决引用与跨目标关系，形成 bound Endem 或 Weave。"
summary: "bind 输入、内容寻址、冲突、能力收敛、Weave 和 Binding Witness。"
badges: ["bind", "Weave"]
---

## 什么时候需要 bind

单个 Endem 可以在不依赖其他制品时独立进入 bound 状态。只有出现跨 Endem 定义、产物、能力、约束或验收引用时，`bind` 才建立 Weave。

> Weave 是多个 Endem 的已解析闭包，不是普通文件归档，也不是为模型自动扩展上下文的知识包。

## 正式输入

`bind` 读取：

- 两个或更多通过所需生产 `check` 的 Endem；
- 声明命名空间、冲突、缺失、循环和权限规则的 Binding Policy；
- 以内容摘要锁定外部对象的 Dependency Lock；
- 关闭高风险 `open` 项时所需的授权决定。

它不得把当前工作目录、环境变量、目录枚举顺序、网络搜索结果或“最新版本”当作隐式输入。

## 解析顺序

1. 验证成员身份、状态、规范版本和必需特性。
2. 收集跨对象引用、产物、能力与验收依赖。
3. 只从锁定候选中执行类型和版本匹配。
4. 检查硬约束冲突、能力上限、缺失行为和循环。
5. 为每项选择或拒绝产生 Binding Witness。
6. 稳定排序成员与解析记录，重新运行生产 `check`。

## 不变量

| 维度 | bind 必须保持 |
| --- | --- |
| `mean` | 符号、指称、关系位置和作用域不能静默改写 |
| `case` | 每个 Endem 继续只有一个根事态；keep/avoid 不降级 |
| `when` | 组合不能让满足条件更容易或丢失决定权威 |
| `open` | 每项都被绑定、明确保留为运行时未知或导致失败 |
| 能力 | 多对象组合只能保持或收紧授权上限 |
| 身份 | 相同锁定输入和策略得到相同解析结果 |

## 循环与可选依赖

第一版拒绝必需依赖循环。未来只有在固定点语义、资源上限、披露顺序、验收顺序和跨实现向量都明确后，才可以增加受限循环。

可选依赖必须声明缺失时的可观察行为。若缺失会改写 `mean`、削弱 `case`、简化 `when` 或扩大能力，它就不能标为可选。

## Binding Witness

Binding Witness 记录输入成员、候选集合、选择规则、冲突、拒绝和结果摘要。它使绑定过程可重放，但不证明依赖将永久可用，也不证明组合任务已经完成。
