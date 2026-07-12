---
layout: manual
title: "NOBJ 生成与 Section 映射 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/nobj-emission.html"
manual_id: "noesis"
manual_group: "object"
manual_order: 4
nav_title: "NOBJ 生成与 Section 映射"
hero_title: "NOBJ 生成与 Section 映射"
hero_description: "说明规范化 NIR 怎样进入前置目录、Section 载荷、符号和来源记录。"
summary: "从 NIR 记录到 NOBJ Header、Section Directory 和载荷的确定性映射。"
badges: ["noesis", "NOBJ"]
---

## 生成顺序

`noesis` 在全部语义检查完成后才建立对象布局：

1. 冻结规范版本、Profile、必需特性、输入和依赖摘要。
2. 为字符串、类型、结构定义和稳定符号建立规范排序。
3. 规范排序 NIR 记录并分配对象内局部索引。
4. 规划 Section、符号和重定位，不立即写入最终缓冲区。
5. 验证所有偏移、长度、计数、对齐、引用和资源预算。
6. 序列化 Preamble、目录和载荷，计算 Section 摘要与对象摘要。
7. 重新解析生成字节并与规范化 NIR 比较；通过后才原子提交。

## 物理排布

```text
Preamble + Header
Load Directory (optional)
Section Directory
String / Type / Schema dictionaries
NIR core records
Symbols / Relocations / Dependencies / Policies
Origins / Build evidence
Debug source (optional)
Integrity directory and digest material
```

目录前置允许读取器先验证文件结构，再读取大型或压缩 Section。任何载荷都必须由目录中的 offset、stored size、logical size 和 alignment 限定。

## NIR 到 Section 的映射

| NIR 内容 | 逻辑 Section | 说明 |
| --- | --- | --- |
| 类型与结构定义 | `nir.types` | 记录类型、结构定义和验证结构。 |
| Node / Edge | `nir.nodes` / `nir.edges` | 图节点和类型化关系。 |
| Constraint / Ambiguity | `nir.constraints` / `nir.ambiguities` | 约束强度、未知策略和替代解释。 |
| Acceptance | `nir.acceptance` | 结果结构、评价器、证据和决定权威。 |
| Capability Requirement | `nir.capabilities` | 需求、参数结构、风险与授权上限。 |
| Artifact Expectation | `nir.artifacts` | 输出媒体类型、结构、编码和消费者角色。 |
| 稳定名称与外部定义 | `strings` / `symbols` | 显示名称、导入导出、可见性和版本。 |
| 待链接引用 | `relocations` | 来源字段、目标符号、类型和变换。 |
| 来源绑定 | `origins` | 最小来源摘要、跨度、推导和决定引用。 |
| 编译输入与工具身份 | `build` | 不进入 Runtime 语义的构建证据。 |
| 原文与完整候选 | `debug.source` | 可裁剪或外置的调试资料。 |

## 链接、装载与证据记录

生成器不能只写 Section 载荷而把关联关系留给下游猜测。Symbol 至少携带 kind、binding、visibility、definition state、section/record/type/version 引用、origin 和 stable-key digest；Relocation 至少携带 target section/record/field、kind、symbol、expected type、encoding/width、addend、overflow policy 与 origin；Dependency 使用内容摘要、版本约束、必需特性和解析策略锁定正式依赖。

需要装载视图时，Load Directory 明确 Segment kind/version、权限、Section 集合、logical size/alignment、policy/budget 与 integrity 引用，但不保存机器虚拟地址。Origin、Build Evidence 与 Integrity 分别保存来源决定、可复现输入闭包和字节覆盖关系；构建时间与 invocation ID 只能进入非语义运行元数据。

## 不允许的写入

- 把自然语言原文作为唯一运行载荷。
- 把 Candidate Envelope 原样放进核心 NIR Section 并标为确认语义。
- 使用当前时间、绝对路径、随机 ID 或哈希表遍历顺序决定对象字节。
- 在写入一半后修改语义记录或 Source Binding Decision。
- 让模型选择 Section 顺序、偏移、对齐、字段宽度或重定位编码。

## 下游

Relocatable NOBJ 先由 [theoria](../../theoria/index.html) 检查结构视图并由 [noemvalidate](../../noemvalidate/index.html)执行独立验证；需要组合多个对象时进入 [synthesis](../../synthesis/index.html)。编译器自检不能替代独立验证结论。
