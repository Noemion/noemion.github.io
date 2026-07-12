---
layout: manual
title: "参考索引 · theoria 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · theoria 使用手册"
permalink: "/tools/theoria/docs/reference-index.html"
manual_id: "theoria"
manual_group: "reference"
manual_order: 4
manual_index_entry: true
nav_title: "参考索引"
hero_title: "参考索引"
hero_description: "按容器、Section、NIR、来源、符号、重定位和安全状态查找视图。"
summary: "theoria 的对象视图、来源视图、安全读取与外部格式资料索引。"
badges: ["theoria", "Reference"]
---

## 视图索引

| 视图 | 入口 |
| --- | --- |
| Preamble / Header | [Header 与 Section](header-and-sections.html) |
| Load / Section Directory | [Header 与 Section](header-and-sections.html) |
| NIR Node / Edge / Constraint | [NIR 与来源](nir-and-origin-views.html) |
| Ambiguity / Acceptance | [NIR 与来源](nir-and-origin-views.html) |
| Origin / Source Binding Decision | [NIR 与来源](nir-and-origin-views.html) |
| checked arithmetic / budgets | [安全读取](safe-reading.html) |
| raw / derived / verdict | [安全读取](safe-reading.html) |

## 权威资料

- NOBJ 规范：https://noemion.github.io/specifications/noema-object.html
- NIR 规范：https://noemion.github.io/specifications/noema-ir.html
- ELF Object File Format：https://gabi.xinuos.com/elf/
- GNU readelf：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- GNU objdump：https://www.sourceware.org/binutils/docs/binutils/objdump.html
- RFC 8949 CBOR Validity：https://www.rfc-editor.org/rfc/rfc8949.html

## 结论边界

`theoria` 的结构化输出是观察结果，不是 Layered Verdict、Loaded State 或 Acceptance Decision。字段和视图名称仍处于开发阶段；自动化消费者必须绑定明确的输出结构版本。
