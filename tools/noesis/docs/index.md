---
layout: manual
title: "noesis 使用手册 · Noemion"
page_role: docs-index
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/index.html"
manual_id: "noesis"
manual_group: "start"
manual_order: 0
manual_is_index: true
nav_title: "手册首页"
hero_title: "noesis 使用手册"
hero_description: "说明自然语言候选怎样经过来源绑定形成 NIR，并由确定性核心生成可重定位 NOBJ。"
summary: "自然语言候选、来源绑定、NIR 记录、NOBJ 生成与构建证据的连续手册。"
manual_index_heading: "noesis 手册目录"
badges: ["noesis", "Source → NIR → NOBJ"]
---

## 这套手册解决什么问题

`noesis` 是 Noesis Core 的编译驱动工具。它可以接收受控 Noesis Source，也可以接收模型或外部系统产生的 Candidate Envelope；无论来源是什么，只有确定性核心能够确认语义、建立 NIR 记录并决定 NOBJ 的字节布局。

> 模型可以提出解释，但不能直接输出 NIR/NOBJ。结构合法、类型正确或模型置信度高，都不能证明候选忠实于自然语言来源。

## 推荐阅读顺序

1. 从[来源与候选输入](source-and-candidates.html)理解自然语言怎样被定位和切分。
2. 阅读[来源绑定与语义提升](semantic-binding.html)，判断候选何时能进入 NIR。
3. 使用[NIR 记录模型](nir-record-model.html)核对目标、约束、歧义、验收和来源字段。
4. 阅读[NOBJ 生成与 Section 映射](nobj-emission.html)，理解逻辑记录怎样进入对象文件。
5. 使用[证据与确定性](evidence-and-determinism.html)区分运行语义、编译证据和构建来源。
6. 最后查看[端到端示例](worked-example.html)和[参考索引](reference-index.html)。

## 当前成熟度

本手册记录已经采用的职责边界和详细设计基线，但不是已发布 CLI 或稳定 ABI。命令参数、文本语法、魔数、Section 编号、重定位编号和文件扩展名仍未冻结；结构示例只能用于评审、实现原型和测试设计。
