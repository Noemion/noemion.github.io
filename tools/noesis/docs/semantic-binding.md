---
layout: manual
title: "来源绑定与语义提升 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/semantic-binding.html"
manual_id: "noesis"
manual_group: "translation"
manual_order: 2
nav_title: "来源绑定与语义提升"
hero_title: "来源绑定与语义提升"
hero_description: "说明候选何时可以进入 NIR，何时必须保留为歧义或拒绝。"
summary: "候选升级、Source Binding Decision、歧义保留和失败语义。"
badges: ["noesis", "Fail Closed"]
---

## 三条允许路径

Candidate Envelope 只有通过以下一种路径才能影响 NIR：

1. **确定性重推导：**版本化规则可以从受控语法或结构化来源重新得到同一主张。
2. **显式来源绑定：**候选绑定经过授权、可追溯的 Source Binding Decision。
3. **保留未决：**候选以 ambiguity、unresolved 或 requires-confirmation 状态进入 NIR，不被写成已确认事实。

任何候选如果不能满足其中一条，都必须被拒绝或留在诊断产物中。

## Source Binding Decision

Source Binding Decision 是独立输入制品，不是编译器内部布尔值。

| 字段职责 | 说明 |
| --- | --- |
| `decision_id` | 决定制品中的稳定标识。 |
| `candidate_ref` | 指向被确认、拒绝或限定范围的候选。 |
| `authority` | 有权确认该类语义的主体或策略身份。 |
| `decision` | confirm、reject、narrow、defer。 |
| `scope` | 决定影响的来源、记录、版本和使用范围。 |
| `reason` / `evidence_refs` | 可复查理由与证据。 |
| `artifact_digest` | 进入 Build Manifest 和 Origin 记录的制品摘要。 |

时间、界面会话和临时身份可以留在决定制品的审计元数据中，但不能成为 NIR 语义或对象确定性排序键。

## 升级矩阵

| 情形 | NIR 处理 | 原因 |
| --- | --- | --- |
| 受控 NSL 明确声明硬约束 | 由确定性规则建立 Constraint | 可重推导。 |
| 模型识别出可能存在的隐私约束 | 建立 Ambiguity 或等待决定 | 模型置信度不能确认来源含义。 |
| 授权主体确认候选并限定到输出字段 | 建立带决定摘要的 Constraint | 具有可追溯授权和明确范围。 |
| 多个解释都合理且风险不同 | 保留 alternatives 与 risk | 不能选择最高分支制造确定性。 |
| 类型正确但来源跨度不存在 | 拒绝 | 内部一致不等于来源忠实。 |
| 候选要求超出授权上限的能力 | 拒绝或收窄 | 语义绑定不能扩大运行权限。 |

## 推断来源等级

NIR Origin 至少区分 explicit、structural、contextual、tool-derived、model-candidate 和 authority-bound。不同等级具有不同的可撤销性和确认权；它们不能共享一个模糊的 `generated=true` 标志。

## 失败结果

失败必须定位到来源单元、候选、规则或决定制品，并区分：来源错误、候选结构错误、类型错误、授权错误、歧义未解决、覆盖缺口和资源超限。编译器不得用通用“无法理解”掩盖可定位原因。
