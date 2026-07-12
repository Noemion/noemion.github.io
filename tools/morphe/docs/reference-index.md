---
layout: manual
title: "参考索引 · morphe 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/reference-index.html"
manual_id: "morphe"
manual_group: "reference"
manual_order: 5
manual_index_entry: true
nav_title: "参考索引"
hero_title: "参考索引"
hero_description: "按 Text NIR、Header、Section、确定性编码和测试查找说明。"
summary: "morphe 的输入、对象布局、编码和验证索引。"
badges: ["morphe", "Reference"]
---

## 手册索引

| 主题 | 入口 |
| --- | --- |
| Text NIR 显式语义 | [输入契约](text-nir-contract.html) |
| Header / Section Directory | [对象布局](object-layout.html) |
| Section 家族 | [对象布局](object-layout.html) |
| 规范排序与环境隔离 | [确定性编码](deterministic-encoding.html) |
| Canonical Text NIR 往返 | [往返测试](round-trip-testing.html) |
| Assembly Evidence Ledger | [往返测试](round-trip-testing.html) |

## 权威资料

- NIR 规范：https://noemion.github.io/specifications/noema-ir.html
- NOBJ 规范：https://noemion.github.io/specifications/noema-object.html
- ELF Sections：https://gabi.xinuos.com/elf/03-sheader.html
- ELF Symbols：https://gabi.xinuos.com/elf/05-symtab.html
- ELF Relocation：https://gabi.xinuos.com/elf/06-reloc.html
- WebAssembly Binary Modules：https://webassembly.github.io/spec/core/binary/modules.html
- RFC 8949 Deterministic Encoding：https://www.rfc-editor.org/rfc/rfc8949.html

## 当前状态

逻辑字段、排布顺序、Section 职责和失败层次是当前详细设计基线；具体 Text NIR 语法、魔数、编号、字段宽度、摘要算法、压缩算法、扩展名和 CLI 仍待冻结。
