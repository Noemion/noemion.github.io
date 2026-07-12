---
layout: manual
title: "NOBJ 布局与字段 · morphe 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/object-layout.html"
manual_id: "morphe"
manual_group: "encoding"
manual_order: 2
nav_title: "NOBJ 布局与字段"
hero_title: "NOBJ 布局与字段"
hero_description: "从汇编器视角说明 Header、目录、Section 载荷和完整性材料的排布。"
summary: "NOBJ 的前置目录、Header、Section Directory、记录载荷与完整性字段。"
badges: ["morphe", "Object Layout"]
---

## 排布顺序

```text
Preamble + Header
Load Directory (optional)
Section Directory
String / Type / Schema dictionaries
NIR record sections
Symbols / Relocations / Dependencies / Policies
Origins / Build evidence
Debug sections
Integrity material
```

目录位于载荷之前，使读取器能够在读取大 Section 前检查全部范围。Section Directory 本身的偏移、数量和表项大小来自固定 Header；二者必须先通过 checked arithmetic 验证。

## Header

| 字段组 | 逻辑字段 |
| --- | --- |
| 身份 | magic、format major/minor、header size、object kind。 |
| 编码 | encoding profile、flags、required features。 |
| Section | directory offset、count、entry size、string table index。 |
| Segment | load directory offset、count、entry size。 |
| 完整性 | integrity section index、integrity profile；不保存递归覆盖自身的完整文件摘要。 |

当前原型候选使用小端、64 位 offset/length 与 32 位索引，但这些宽度尚未冻结。读取器不能按本机指针宽度解释对象。

## Section Directory

| 字段 | 验证 |
| --- | --- |
| name reference | 字符串表索引有效，名称不决定类型。 |
| kind / schema version | 识别载荷结构；未知 required 类型失败。 |
| flags | required、alloc、readonly、merge、debug、compressed 等组合合法。 |
| file offset / stored size | 文件范围有效且不非法重叠。 |
| logical size | 解压或解码后的大小不超限。 |
| alignment | 规范值、无上取整溢出、实际偏移满足。 |
| entry size / count | 与固定记录载荷字节数一致。 |
| link section / info | 指向正确类别的关联 Section。 |
| digest reference | 摘要存在并覆盖实际载荷。 |

## Section 家族

核心 NIR 使用 `nir.types`、`nir.nodes`、`nir.edges`、`nir.constraints`、`nir.ambiguities`、`nir.acceptance`、`nir.capabilities` 和 `nir.artifacts`。链接元数据使用 `strings`、`symbols`、`relocations`、`dependencies` 和 `policies`。来源与构建使用 `origins` 和 `build`；原文和完整候选进入 `debug.source`；摘要材料进入 `integrity`。

这些名称是逻辑职责，不是已冻结 Section 字节名称或编号。

## Load、Symbol 与 Relocation 记录

可装载对象的 Load Directory 每项至少描述 segment kind/version、权限 flags、Section 集合引用、logical size、alignment、policy/budget 引用和 integrity 引用。它不保存机器虚拟地址；Segment 权限不能比成员 Section 或策略更宽。

| 记录 | 汇编器必须写明 |
| --- | --- |
| Symbol | namespace/name ref、kind、local/export/import、visibility、definition state、section/record/type/version ref、resolution/missing policy、size or arity、origin ref、stable-key digest。 |
| Relocation | target section/record/field、kind、symbol ref、expected type、encoding/width、optional addend、overflow policy、origin ref。 |
| Dependency | kind、content digest、version constraint、required features、resolution policy、optional flag、origin ref。 |
| Origin | subject range、source digest、source unit/span、derivation class、rule/model identity、decision digest、authority、evidence refs。 |
| Build Evidence | build type、input roots、parameter/config digest、resolved dependencies、toolchain identity/digest、reproducibility profile、output digest。 |
| Integrity Entry | subject kind/index、stored/logical coverage、algorithm/profile、digest、tree parent/path ref、coverage flags。 |

这些字段同样只冻结职责。写入器不能因为字段宽度和数值枚举尚未确定，就省略类型、来源、溢出策略或摘要覆盖范围。

## 摘要域不能自引用

完整 NOBJ 的 Exact File Digest 由对象外部对全部字节计算，不能写回自己覆盖的文件。对象内的 `integrity` Section 只按 Profile 覆盖 Header/目录职责字段和其他 Section 的 stored/logical digest；`integrity` Section 的目录项不得通过 digest reference 指向自身，根记录及其存储字节也不进入自身覆盖域。

Exact File Digest、内部 Integrity Root、尚未定义的 Semantic Identity 与发布包签名是四种不同属性。写入器必须输出明确的覆盖描述，不能用 build ID、CRC 或签名存在代替结构与语义验证。裸 NOBJ 的内部根只证明对象自洽；来源真实性和抗恶意篡改必须由受信外部 Exact File Digest、Package Subject Digest 或签名绑定。

## 记录编码

固定表声明 entry size/count；可扩展语义记录带 record kind、schema version、flags、record size、local ID、type reference 和 origin reference。未知可选记录可以按 record size 跳过；影响语义、链接、权限或验收的未知记录必须失败。
