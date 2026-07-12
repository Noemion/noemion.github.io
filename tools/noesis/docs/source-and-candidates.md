---
layout: manual
title: "来源与候选输入 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/source-and-candidates.html"
manual_id: "noesis"
manual_group: "start"
manual_order: 1
nav_title: "来源与候选输入"
hero_title: "来源与候选输入"
hero_description: "定义 Source Package、Source Unit 和 Candidate Envelope 的边界与最低字段。"
summary: "定义自然语言来源、精确跨度和不可信候选怎样进入编译流程。"
badges: ["noesis", "Untrusted Input"]
---

## 输入链

自然语言路径固定为：

```text
Source Package
  → Source Unit
  → Candidate Envelope
  → deterministic derivation / Source Binding Decision
  → Normalized NIR
```

Source Package 证明“读取的是哪份材料”，Source Unit 证明“候选对应哪段材料”，Candidate Envelope 只说明“某个前端提出了什么解释”。三者都不能单独证明解释正确。

## Source Package

| 字段职责 | 说明 |
| --- | --- |
| `artifact_id` | 当前编译请求中的稳定制品引用。 |
| `content_digest` | 对原始字节计算的内容摘要。 |
| `media_type` | 文本、Markdown、结构化数据或其他受支持类型。 |
| `language` | 文本语言或明确的未指定状态。 |
| `version` | 来源版本、提交或外部制品版本。 |
| `license` | 使用、复制和生成派生材料的许可信息。 |
| `byte_length` | 在分配和读取前检查的字节长度。 |

文件路径、URL 和显示名称可以作为定位信息，但内容身份必须由摘要与版本共同约束。网络位置不能替代锁定后的来源身份。

## Source Unit

| 字段职责 | 说明 |
| --- | --- |
| `unit_id` | 当前 Source Package 内的稳定单元标识。 |
| `artifact_ref` | 指回 Source Package。 |
| `parent_unit` | 表示章节、段落、句子或结构节点的包含关系。 |
| `span_kind` | byte、Unicode scalar、token 或结构节点；必须明确。 |
| `start` / `length` | 使用 checked arithmetic 定位来源范围。 |
| `unit_digest` | 防止相同位置在来源变化后被误用。 |

不得混用 UTF-8 字节偏移和字符偏移。前端必须声明跨度单位，并在来源解码失败时停止，而不是用替换字符继续绑定。

## Candidate Envelope

| 字段职责 | 说明 |
| --- | --- |
| `candidate_id` | 候选制品内的局部标识。 |
| `source_units` | 一个或多个精确来源单元。 |
| `proposed_kind` | 候选目标、关系、约束、行为、实体或验收项类别。 |
| `payload` | 类型化候选内容，不是任意自由文本槽。 |
| `alternatives` | 仍有可能成立的替代解释。 |
| `evidence_refs` | 支持或反对候选的来源与工具证据。 |
| `confidence` | 模型校准信息，只供排序和诊断，不能确认语义。 |
| `model_identity` / `window_fingerprint` | 产生候选的模型、配置和上下文窗口身份。 |
| `state` | proposed、ambiguous、conflicted、unsupported 等候选状态。 |

## 准入拒绝

- 来源摘要、版本或跨度不匹配。
- Candidate Envelope 引用不存在的 Source Unit。
- 候选只给结论，没有可定位来源或替代解释。
- 前端用自然语言字符串绕过类型化候选结构。
- 模型身份、候选协议版本或限制配置无法识别。
- 输入数量、嵌套深度、字符串长度或诊断预算超限。
