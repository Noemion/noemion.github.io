---
layout: manual
title: "Header 与 Section 视图 · theoria 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · theoria 使用手册"
permalink: "/tools/theoria/docs/header-and-sections.html"
manual_id: "theoria"
manual_group: "views"
manual_order: 1
nav_title: "Header 与 Section 视图"
hero_title: "Header 与 Section 视图"
hero_description: "说明对象容器头、目录字段、范围检查和结构化显示。"
summary: "Preamble、Header、Load Directory、Section Directory 和 Section 载荷视图。"
badges: ["theoria", "Container View"]
---

## 读取顺序

1. 在固定小缓冲区中读取 Preamble 与 Header。
2. 验证格式版本、Header 大小、编码 Profile 和必需特性。
3. 使用 checked arithmetic 验证目录偏移、数量和表项大小。
4. 读取 Section Directory，并在访问载荷前验证所有范围、对齐和重叠。
5. 只有用户选择某个视图后才读取对应 Section，避免默认展开大对象。

## Header 视图

Header 视图显示 identity、encoding、section directory、load directory 和 integrity 五组字段。原始数值与解释结果必须分栏，不能用解释文本覆盖损坏的原始声明。

| 组 | 典型字段 |
| --- | --- |
| Identity | magic、format major/minor、header size、object kind。 |
| Encoding | encoding profile、flags、required features。 |
| Sections | directory offset/count/entry size、string table index。 |
| Load | segment directory offset/count/entry size。 |
| Integrity | integrity index、object digest。 |

## Section 视图

每行显示 index、name、kind/schema、flags、offset、stored/logical size、alignment、entry size/count、link/info 和 digest 状态。字段无法解释时保留原始值并附诊断，不猜测一个最接近的已知类型。

## Load 与链接记录视图

Load 视图显示 Segment 的 kind/version、权限 flags、Section 集合、logical size、alignment、policy/budget 与 integrity 引用，并将 Segment 权限和每个成员 Section 权限并排比较。对象中不存在 Load Directory 时显示“无装载视图”，不能从 Section 名称推测一个。

Symbol 与 Relocation 视图必须显示原始引用和解析结果：Symbol 的 binding、visibility、definition state、section/record/type/version 引用及 stable-key digest；Relocation 的 target section/record/field、kind、symbol、expected type、encoding/width、addend、overflow policy 与 origin。解析失败时保留目标字段与原始索引，不输出伪造的符号名称。

Dependency、Origin、Build Evidence 和 Integrity 视图分别回答“对象依赖什么”“语义来自哪里”“哪些输入产生了这些字节”“哪些字节被何种摘要覆盖”。单次构建时间和 invocation ID 只能作为非语义运行元数据显示，不能与可复现输入闭包混为一栏。

## 范围状态

| 状态 | 含义 |
| --- | --- |
| declared | 只显示对象声明值，尚未检查。 |
| bounded | 偏移、长度、对齐和文件范围成立。 |
| decoded | Section 载荷符合其通用编码。 |
| schema-valid | 记录符合 Section 结构定义。 |
| policy-unchecked | 尚未执行语义、权限或信任判断。 |

`theoria` 默认不得显示“valid object”这一笼统结论；需要分层结论时调用 noemvalidate。

## 大对象策略

Section 列表可以完整显示，但载荷、字符串、图和十六进制视图必须受用户选择和输出预算限制。压缩 Section 在分配前检查 logical size，默认只显示元数据，不自动解压全部载荷。
