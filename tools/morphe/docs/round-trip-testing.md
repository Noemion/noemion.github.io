---
layout: manual
title: "往返与负例测试 · morphe 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/round-trip-testing.html"
manual_id: "morphe"
manual_group: "validation"
manual_order: 4
nav_title: "往返与负例测试"
hero_title: "往返与负例测试"
hero_description: "定义 Text NIR、对象字节和解码视图之间必须保持的关系。"
summary: "规范化往返、畸形对象、属性测试和独立验证要求。"
badges: ["morphe", "Round Trip"]
---

## 两条往返关系

```text
Canonical Text NIR → morphe → NOBJ → noemdecode → Canonical Text NIR
NOBJ → noemdecode → Canonical Text NIR → morphe → NOBJ
```

第一条证明文本的显式语义可以稳定编码和恢复；第二条证明可再次汇编的对象视图不会改变规范字节。原始注释、空白、来源文件拆分和可裁剪调试信息可以不可逆，但损失必须明确分类。

## 测试矩阵

| 类别 | 必须覆盖 |
| --- | --- |
| Golden | 每种记录与 Section 的最小合法对象、组合对象和完整示例。 |
| Malformed | 截断 Header、计数乘法溢出、偏移加法溢出、错误对齐、重叠和非法索引。 |
| Schema | 未知 required 类型、错误记录版本、entry size/count 不一致。 |
| Reference | 悬空局部 ID、错误目标类别、符号版本冲突和重定位溢出。 |
| Determinism | 目录、线程、缓存、区域设置、时区和输入发现顺序变化。 |
| Fuzz | Preamble、目录、压缩载荷、可变记录和字符串解码。 |
| Resource | 最大 Section、记录、字符串、依赖深度、解压大小和诊断预算。 |

## 独立验证

`morphe` 生成后必须重新解析并自检，但这不替代 [noemvalidate](../../noemvalidate/index.html) 的独立 Layered Verdict。自检回答“写入器是否生成自己能够解释的对象”，独立验证回答“对象是否满足共享规范和策略”。

## Assembly Evidence Ledger

每项 Text NIR 声明必须映射到 NIR 记录、对象 Section/记录和调试位置。Ledger 还记录忽略的注释、规范化变化、include 依赖和无法保留的表示信息。发布覆盖工具消费该账本，但账本完整不等于任务已经满足。

## 失败原子性

任一语法、类型、引用、布局或自检错误都不得留下看似有效的 NOBJ。调试中间产物必须带不可装载状态和输入摘要，不能进入链接或发布目录。
