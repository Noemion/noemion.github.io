---
layout: manual
title: "NIR 记录模型 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/nir-record-model.html"
manual_id: "noesis"
manual_group: "translation"
manual_order: 3
nav_title: "NIR 记录模型"
hero_title: "NIR 记录模型"
hero_description: "列出目标、关系、约束、歧义、验收、能力、产物和来源记录的最低字段。"
summary: "NIR 公共记录头、类型化引用、字段职责和主要不变量。"
badges: ["noesis", "NIR"]
---

## 公共记录头

每条可扩展记录具有以下逻辑字段：

| 字段 | 作用 |
| --- | --- |
| `record_kind` | 选择记录结构和验证规则。 |
| `schema_version` | 选择该记录类别的结构版本。 |
| `flags` | required、optional、debug 等处理属性。 |
| `record_size` | 限定记录边界并支持跳过允许忽略的未知记录。 |
| `local_id` | 对象内局部索引，可在链接时重编号。 |
| `type_ref` | 指向类型与结构定义注册表。 |
| `origin_ref` | 指向来源、推导和决定记录。 |

文件偏移不是语义身份。链接器可以改变 `local_id`，但稳定符号、来源摘要、硬约束和验收身份必须保持。

## Module 与图记录

| 记录 | 核心字段 |
| --- | --- |
| Module | NIR 版本、命名空间、Profile、根目标、默认作用域、必需特性、验收根。 |
| Node | kind、type、symbol、modality、polarity、resolution state、payload、origin。 |
| Edge | relation type、source、target、scope、qualifiers、origin。 |

Node 不只表示名词实体，也可以表示目标状态、行动、条件、产物或行为请求。Edge 必须声明关系类型，不能用整数边让消费者猜测语义。

## 约束与歧义

| 记录 | 核心字段 |
| --- | --- |
| Constraint | strength、operator、operands、scope、priority、conflict policy、unknown policy、origin。 |
| Ambiguity | subject、alternatives、evidence、risk、state、resolution policy、binding decision。 |

`strength=hard` 的约束在任何编译或实现化阶段都不得降级。`unknown_policy` 必须显式规定拒绝、pending-review 或其他规范状态，不能默认当作通过。

## 验收、能力与产物

| 记录 | 核心字段 |
| --- | --- |
| Acceptance | subject goals、result schema、evaluator、evidence requirements、authority、unknown behavior、result states。 |
| Capability Requirement | capability type、parameter schema、risk class、authorization ceiling、preconditions。 |
| Artifact Expectation | media type、schema、encoding、cardinality、destination role、required properties。 |

Capability Requirement 只描述运行需求和授权上限，不保存 Shell、网络、凭据或文件句柄。Artifact Expectation 必须有消费者和可观察属性，否则只能是诊断建议，不能成为正式输出契约。

## Origin

Origin 把一组 NIR 记录绑定到来源制品摘要、Source Unit 跨度、derivation class、规则或模型身份、Source Binding Decision 摘要与授权主体。它必须能回答：这项语义来自哪里、怎样形成、谁有权确认、哪些替代项仍未解决。

## 未冻结内容

记录名称、字段职责和失败边界已经作为详细设计基线采用；具体枚举值、字段宽度、Text NIR 语法和二进制编号仍须通过格式规范、实现原型和正反样例冻结。
