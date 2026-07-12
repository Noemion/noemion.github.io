---
layout: manual
title: "NIR 与来源视图 · theoria 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · theoria 使用手册"
permalink: "/tools/theoria/docs/nir-and-origin-views.html"
manual_id: "theoria"
manual_group: "views"
manual_order: 2
nav_title: "NIR 与来源视图"
hero_title: "NIR 与来源视图"
hero_description: "查看目标、约束、歧义、验收和来源绑定，而不重新解释自然语言。"
summary: "NIR 记录、类型化引用、Origin、Candidate 和调试来源的只读视图。"
badges: ["theoria", "NIR / Origin"]
---

## NIR 视图

NIR 视图按 Module、Node、Edge、Constraint、Ambiguity、Acceptance、Capability Requirement、Artifact Expectation 和 Origin 分类。每条记录显示公共头、类型化字段和引用状态；图视图只是这些记录的投影，不建立新的语义。

## 约束视图

约束行至少显示 strength、operator、operands、scope、priority、conflict policy、unknown policy 和 origin。硬约束使用明确文本标识，不能只依赖颜色。若操作数或来源无法解析，显示 unresolved reference，而不是省略该约束。

## 歧义视图

Ambiguity 视图同时显示所有 alternatives、evidence、risk、state、resolution policy 和 Source Binding Decision 摘要。默认排序使用对象中的规范顺序，不按模型置信度隐藏低分替代项。

## 验收视图

Acceptance 视图区分 result schema、evaluator、evidence requirements、authority、unknown behavior 与 result states。它不能显示当前任务是否已完成，因为 NOBJ 保存的是验收契约，不是一次运行的 Acceptance Decision。

## 来源视图

Origin 视图回答：

- 记录来自哪个 Source Package 与 Source Unit；
- 使用什么跨度单位和范围；
- 语义由 explicit、structural、contextual、tool-derived、model-candidate 还是 authority-bound 路径形成；
- 使用了哪个规则、模型/窗口指纹或决定制品摘要；
- 原始来源是否在 `debug.source`、外部 Debug Companion 或仅以摘要存在。

## 不重新解释来源

`theoria` 可以显示可选原文和 Candidate Envelope，但不能调用模型重新解释、补全缺失字段或把显示结果写回对象。需要改变语义时应回到来源和 `noesis`，生成具有新身份的新对象。
