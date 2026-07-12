---
layout: manual
title: "morphe 使用手册 · Noemion"
page_role: docs-index
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/index.html"
manual_id: "morphe"
manual_group: "start"
manual_order: 0
manual_is_index: true
nav_title: "手册首页"
hero_title: "morphe 使用手册"
hero_description: "说明规范化 Text NIR 怎样确定性编码为可重定位 NOBJ。"
summary: "Text NIR 输入、对象布局、确定性编码、往返测试与字段参考。"
manual_index_heading: "morphe 手册目录"
badges: ["morphe", "Text NIR → NOBJ"]
---

## 工具边界

`morphe` 只把已经显式化的 Text NIR 编码为对象形式。它不理解自然语言、不提出替代解释，也不补全缺失目标、约束或验收条件；需要自然语言编译时使用 [noesis](../../noesis/docs/index.html)。

> Text NIR 是可评审、可规范化、可往返测试的输入，不是允许汇编器重新解释的提示词。

## 阅读顺序

1. [Text NIR 输入契约](text-nir-contract.html)
2. [NOBJ 布局与字段](object-layout.html)
3. [确定性编码](deterministic-encoding.html)
4. [往返与负例测试](round-trip-testing.html)
5. [参考索引](reference-index.html)

## 当前成熟度

手册描述逻辑字段、排布和失败边界。Text NIR 的正式语法、文件扩展名、魔数、数值字段宽度、Section 编号与 CLI 尚未冻结，示例不能直接复制为命令或实现接口。
