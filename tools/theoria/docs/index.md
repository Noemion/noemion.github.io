---
layout: manual
title: "theoria 使用手册 · Noemion"
page_role: docs-index
footer_text: "Noemion · theoria 使用手册"
permalink: "/tools/theoria/docs/index.html"
manual_id: "theoria"
manual_group: "start"
manual_order: 0
manual_is_index: true
nav_title: "手册首页"
hero_title: "theoria 使用手册"
hero_description: "以只读方式查看 NOBJ/HOBJ 的 Header、Section、NIR、来源、符号与重定位。"
summary: "对象准入、结构视图、NIR 来源视图、安全读取和参考索引。"
manual_index_heading: "theoria 手册目录"
badges: ["theoria", "Read Only"]
---

## 工具边界

`theoria` 提供对象的可观察表面，类似 `readelf` 与 `objdump` 的职责组合，但面向 NIR/NOBJ/HOBJ。它可以显示原始声明和受限解析结果，不能把“能够显示”升级为“验证通过”。

> 查看器、验证器和装载器共享结构定义，但保留不同结论：theoria 显示，noemvalidate 判断，Noema Object System 装载。

## 阅读顺序

1. [Header 与 Section 视图](header-and-sections.html)
2. [NIR 与来源视图](nir-and-origin-views.html)
3. [安全读取与诊断](safe-reading.html)
4. [参考索引](reference-index.html)

## 当前成熟度

视图名称和字段职责来自当前详细设计基线；具体 CLI、输出结构版本、Section 编号和稳定 JSON/CBOR 字段仍未冻结。
