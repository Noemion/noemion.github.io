---
layout: manual
title: "自然语言到对象的端到端示例 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/worked-example.html"
manual_id: "noesis"
manual_group: "reference"
manual_order: 6
nav_title: "端到端示例"
hero_title: "自然语言到对象的端到端示例"
hero_description: "用一条带隐私约束和人工复核条件的请求说明候选、NIR 与 NOBJ 的连续转换。"
summary: "从自然语言来源到 Candidate Envelope、NIR 记录和 NOBJ Section 的非规范示例。"
badges: ["noesis", "Worked Example"]
---

## 来源

> 生成一份 JSON 报告，必须隐藏输出中的邮箱地址；如果无法确认所有输出邮箱已经脱敏，停止并请求人工检查。

这条来源包含产物类型、硬约束、未知处理和人工决定，但没有定义 JSON 结构、邮箱识别规则或报告消费者。编译器不能补出这些内容。

## 候选阶段

模型前端可以提出以下候选：

| 候选 | 来源 | 状态 |
| --- | --- | --- |
| 产物是 JSON 报告 | “JSON 报告” | 可由字面规则重推导。 |
| 输出中的邮箱必须脱敏 | “必须隐藏输出中的邮箱地址” | 可由字面规则重推导为硬约束。 |
| “所有输出邮箱”包括嵌套字段和自由文本 | 没有明确说明 | 必须保留为歧义。 |
| 无法确认时请求人工检查 | 原句后半段 | 可建立 unknown → pending-review 规则。 |

如果项目配置要求使用指定 JSON Schema 和邮箱识别规则，它们必须作为锁定依赖进入编译输入，而不能由模型临时选择。

## 非规范 NIR 结构示意

下面只展示逻辑字段，不是已冻结 Text NIR 语法：

```yaml
module:
  profile: deterministic
  root_goals: [goal.report]

nodes:
  - id: goal.report
    kind: artifact_goal
    type: report
    origin: source.unit.1

artifacts:
  - id: artifact.report
    media_type: application/json
    schema: external.symbol.report_schema
    cardinality: exactly_one
    consumer_role: report_consumer

constraints:
  - id: constraint.redact_email
    strength: hard
    operator: redact_matches
    operands: [artifact.report, external.symbol.email_detector]
    scope: output
    unknown_policy: pending_review
    origin: source.unit.1

ambiguities:
  - id: ambiguity.email_scope
    subject: constraint.redact_email
    alternatives: [structured_fields_only, all_string_values]
    state: unresolved
    resolution_policy: require_binding_decision

acceptance:
  - id: acceptance.report
    subject_goals: [goal.report]
    result_schema: external.symbol.report_schema
    evidence_requirements: [json_parse, schema_validation, email_scan]
    unknown_behavior: pending_review
    authority: configured_reviewer
```

## NOBJ Section 映射

| Section | 示例内容 |
| --- | --- |
| `nir.types` | report、artifact_goal 和引用结构定义。 |
| `nir.nodes` | `goal.report`。 |
| `nir.constraints` | `constraint.redact_email`。 |
| `nir.ambiguities` | 尚未解决的邮箱范围替代项。 |
| `nir.acceptance` | JSON 解析、结构验证、邮箱扫描和 pending-review 规则。 |
| `nir.artifacts` | JSON 报告的媒体类型、结构和消费者角色。 |
| `symbols` | 外部 JSON Schema、邮箱检测器和 reviewer policy。 |
| `relocations` | 指向外部结构定义、检测器与策略的类型化引用。 |
| `origins` | 记录到原句跨度和确定性规则的映射。 |
| `build` | 来源摘要、规则版本、锁定依赖和工具版本。 |
| `debug.source` | 可选原句和完整 Candidate Envelope。 |

## 必须失败的变化

- 模型自行决定只扫描顶层字段，并关闭歧义。
- 将“必须隐藏”编码为软偏好。
- 邮箱检测器没有版本和内容摘要。
- 缺少报告消费者或 JSON Schema，却仍标记验收契约完整。
- 邮箱扫描返回 unknown 时仍将结果标为 accepted。

这个示例说明 NIR 保存的是目标、边界和验收条件，而不是一段重新包装的提示词；NOBJ 保存可链接结构和来源证据，而不是模型直接生成的字节。
