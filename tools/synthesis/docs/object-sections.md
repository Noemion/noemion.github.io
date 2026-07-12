---
layout: manual
title: "对象 Section 与链接视图 · synthesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · synthesis 使用手册"
permalink: "/tools/synthesis/docs/object-sections.html"
manual_id: "synthesis"
manual_group: "start"
manual_order: 3
nav_title: "对象 Section 与链接视图"
hero_title: "对象 Section 与链接视图"
hero_description: "说明链接器从 NOBJ Header、Section Directory 和 NIR 记录中读取什么。"
summary: "NOBJ 目录字段、Section 家族、关联字段和链接准入检查。"
badges: ["synthesis", "NOBJ Layout"]
---

## 链接器读取的两层结构

`synthesis` 先读取容器层，再读取语义层。容器层回答 Section 在哪里、怎样解码和关联；语义层回答符号、记录和约束能否组合。任何语义处理都必须在容器边界验证后开始。

## Header 与目录准入

| 字段组 | 链接用途 |
| --- | --- |
| format / object kind | 判断是否为可重定位 NOBJ、HOBJ 或允许的归档成员。 |
| encoding profile / required features | 选择读取器并拒绝未知必需特性。 |
| Section Directory offset/count/entry size | 建立有界、随机访问的链接视图。 |
| string table index | 解析显示名称；名称不决定 Section 语义。 |
| integrity index / object digest | 绑定输入身份和缓存，不替代结构验证。 |

Section Directory 的 offset、stored/logical size、alignment、entry size/count、link section、info 和 digest reference 必须全部通过 checked arithmetic 与类型检查。链接器不能为损坏目录猜测边界。

## Section 处理矩阵

| Section 家族 | synthesis 的处理 |
| --- | --- |
| `nir.types` | 合并兼容类型和结构定义；冲突时失败。 |
| `nir.nodes` / `nir.edges` | 分配目标局部索引并建立旧 ID 到新 ID 映射。 |
| `nir.constraints` | 保持硬软强度，执行显式冲突策略。 |
| `nir.ambiguities` | 保留替代项与未决状态，不选择最高置信分支。 |
| `nir.acceptance` | 合并兼容验收契约；决定权威和 unknown 行为冲突必须失败。 |
| `nir.capabilities` | 权限默认收敛到更严格上限，不建立实时句柄。 |
| `nir.artifacts` | 合并输出结构和消费者契约，检测名称或结构冲突。 |
| `symbols` | 执行定义、引用、版本、强弱和可见性选择。 |
| `relocations` | 按来源字段、目标符号、类型和加数应用修正。 |
| `dependencies` / `policies` | 计算强依赖闭包并收敛权限与策略。 |
| `origins` | 重映射记录引用并保持来源摘要、跨度和决定身份。 |
| `build` / `debug.source` | 默认不参与运行语义；按输出策略保留、合并或外置。 |

## `link_section` 与 `info`

目录中的关联字段必须由 Section 类型解释。例如 relocation Section 的 `link_section` 指向符号表，`info` 指向被修正的目标 Section；符号表的 `link_section` 指向字符串表。错误类别、循环关联或目标索引越界必须在扫描阶段失败。

## Symbol、Relocation 与 Dependency 准入

| 记录 | 链接所需字段 | 链接器必须证明 |
| --- | --- | --- |
| Symbol | kind、binding、visibility、definition state、section/record/type/version 引用、origin、stable-key digest | 定义与引用类型一致，选择顺序确定，稳定键不依赖输入文件位置。 |
| Relocation | target section/record/field、kind、symbol、expected type、encoding/width、addend、overflow policy、origin | 目标字段允许重定位，应用一次且不溢出，结果仍符合声明类型。 |
| Dependency | kind、content digest、version constraint、required features、resolution policy、optional flag、origin | 解析结果已锁定且可重放，未知强依赖失败，可选依赖缺失不会改变必需语义。 |

链接器完成 ID 重映射后必须重新验证所有 section/record/field 引用，并重建受影响的摘要材料。名称相同但 stable-key、类型、版本或来源不兼容的 Symbol 不能静默合并。

## 来源、构建与完整性保留

`origins` 的 subject range、source digest/span、derivation class、decision digest 和 authority 必须随重编号更新引用但保持来源身份；`build` 中合并后的输入根、配置摘要、工具链身份与解析依赖必须规范排序；`integrity` 需要区分 stored bytes 与 decoded logical content 的覆盖范围。链接完成不允许删除这些材料，裁剪只能交给发布对象裁剪阶段并附等价与覆盖证据。

## 未知扩展

未知 required Section、记录或特性必须拒绝。只有规范明确为 optional/debug 且忽略后不会改变语义、权限、验收、依赖或完整性结论的扩展才可以跳过。删除或忽略扩展不能把原本的拒绝变成允许。

## 权威格式说明

完整 Header、Section Directory 和 Section 家族职责见 [NOBJ 规范](../../../specifications/noema-object.html)。本章只说明链接器消费方式，不重新定义第二套格式。
