---
layout: manual
title: "确定性编码 · morphe 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · morphe 使用手册"
permalink: "/tools/morphe/docs/deterministic-encoding.html"
manual_id: "morphe"
manual_group: "encoding"
manual_order: 3
nav_title: "确定性编码"
hero_title: "确定性编码"
hero_description: "规定排序、默认值、通用载荷编码和环境隔离怎样保证字节可复现。"
summary: "对象字节稳定所需的规范排序、编码 Profile、填充和环境隔离规则。"
badges: ["morphe", "Deterministic"]
---

## 相同输入的定义

相同输入不仅指 Text NIR 字符串相同，还包括规范版本、结构定义、include 摘要、目标编码 Profile、限制配置和 `morphe`/对象写入器版本相同。任何影响字节的输入都必须进入 Build Manifest。

## 规范排序

- 字符串按规范化 UTF-8 字节排序，不使用区域设置。
- 类型和结构定义按稳定身份排序。
- Node、Edge、Constraint 等记录按记录类别、稳定语义键、来源键和显式定义顺序排序。
- Symbols 先按 binding/visibility 分组，再按命名空间、名称、版本和定义位置排序。
- Relocations 按目标 Section、来源记录/字段、类型、符号和加数排序。
- 可选 Section 采用固定家族顺序；缺失 Section 不用随机空 Section 填充。

## 编码规则

固定 Header 和目录使用规范规定的固定宽度整数。可扩展 Section 如果使用 CBOR 等通用编码，必须选择并记录 Noemion 专用确定性 Profile；“任何合法 CBOR”不能成为规范对象字节。

RFC 8949 指出，同一数据可能有多种合法编码，Map 顺序也不携带应用语义。因此对象格式必须规定最短整数、Map key 排序、浮点表示、NaN/负零、标签、字符串规范化和禁止的 indefinite-length 形式。

原文：https://www.rfc-editor.org/rfc/rfc8949.html

## 禁止进入字节的环境噪声

- 当前时间、时区、绝对路径和临时目录；
- 文件系统枚举、哈希表迭代和并发完成顺序；
- 未锁定网络依赖和缓存命中状态；
- 进程 ID、主机名、用户名和本地语言环境；
- 未显式声明的压缩器、摘要库或随机种子版本。

## 填充与摘要

填充字节使用规范固定值并纳入对象摘要。Section 摘要基于 stored bytes 或 logical bytes 必须由算法字段明确区分；压缩 Section 同时记录 stored size 和 logical size，解压上限在分配前验证。

## 双构建验证

测试应在不同目录、时区、区域设置、线程数、缓存状态和文件发现顺序下重复汇编，并要求对象字节完全相同。若规范允许某种结构等价但字节不同，必须先定义等价规则；在规则形成前不能用“语义相同”解释非确定输出。
