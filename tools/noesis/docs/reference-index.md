---
layout: manual
title: "参考索引 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/reference-index.html"
manual_id: "noesis"
manual_group: "reference"
manual_order: 7
manual_index_entry: true
nav_title: "参考索引"
hero_title: "参考索引"
hero_description: "按对象、字段、信任状态和外部设计依据查找权威入口。"
summary: "noesis 的对象、字段、信任状态、规范和研究资料索引。"
badges: ["noesis", "Reference"]
---

## 对象与状态

| 术语 | 说明入口 |
| --- | --- |
| Source Package / Source Unit | [来源与候选输入](source-and-candidates.html) |
| Candidate Envelope | [来源与候选输入](source-and-candidates.html) |
| Source Binding Decision | [来源绑定与语义提升](semantic-binding.html) |
| NIR 公共记录头 | [NIR 记录模型](nir-record-model.html) |
| NOBJ Section 映射 | [NOBJ 生成](nobj-emission.html) |
| Compiler Evidence Ledger | [证据与确定性](evidence-and-determinism.html) |
| 端到端示例 | [自然语言到对象](worked-example.html) |

## 权威项目资料

- NIR 规范：https://noemion.github.io/specifications/noema-ir.html
- NOBJ 规范：https://noemion.github.io/specifications/noema-object.html
- Noesis Core：https://noemion.github.io/components/noesis-core.html
- 对象生命周期：https://noemion.github.io/architecture/noema-lifecycle.html
- 架构开放问题：https://noemion.github.io/architecture/open-questions.html

## 外部设计依据

- OpenAI, Harness Engineering：https://openai.com/zh-Hans-CN/index/harness-engineering/
- ELF Object File Format：https://gabi.xinuos.com/elf/
- WebAssembly Binary Modules：https://webassembly.github.io/spec/core/binary/modules.html
- RFC 8949, CBOR：https://www.rfc-editor.org/rfc/rfc8949.html
- SLSA Build Provenance：https://slsa.dev/spec/v1.2/build-provenance
- GNU Binutils 工具集合：https://www.gnu.org/software/binutils/binutils.html

## 成熟度

逻辑记录职责、自然语言候选边界和 NOBJ 排布顺序属于当前详细设计基线。数值 ABI、Text NIR 语法、魔数、字段宽度、Section/重定位编号、文件扩展名和 CLI 参数仍未冻结。
