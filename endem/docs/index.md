---
layout: manual
title: "endem 使用手册 · Noemion"
page_role: docs-index
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/index.html"
manual_id: "endem"
manual_group: "start"
manual_order: 0
manual_is_index: true
nav_title: "手册首页"
hero_title: "endem 使用手册"
hero_description: "说明一个命令怎样形成、检查、绑定、发布、独立查看和隔离运行目标制品。"
summary: "Endem 格式、组合、安全、运行和命令参考的连续手册。"
manual_index_heading: "endem 手册目录"
badges: ["Single CLI", "Design Stage"]
---

## 这套手册解决什么问题

`endem` 是 Noemion 唯一公开命令行入口。它围绕同一件 Endem 制品提供 `form`、`check`、`bind`、`pack`、`seal`、`see`、`run` 和 `test`，不要求用户先理解一组仿照传统对象工具命名的程序。

> 当前没有可执行程序。命令名称、职责和 `.endem` 扩展名已经采用，参数、退出状态、安装包和稳定 ABI 尚未冻结。本手册定义处理边界，不提供可以直接复制执行的命令示例。

## 推荐阅读顺序

1. 阅读[格式与成形](format.html)，理解一个根 `case` 和 `say/mean/case/when/open`。
2. 阅读[绑定与组合](binding.html)，理解 open Endem 怎样成为 bound Endem 或 Weave。
3. 阅读[安全与独立检查](safety.html)，区分生产 `check` 与独立 `see`。
4. 阅读[发布与运行](running.html)，理解 `pack`、外部签名、`seal`、Frame 和 Witness。
5. 最后使用[参考索引](reference.html)查找八个入口、状态、制品和稳定失败类别。

## 最短主线

Source Card 先经过确定性投影规则或具名决定，再由 `form` 形成 open Endem。`check` 运行生产验证；`see` 使用另一套直接 Reader 观察同一字节。需要跨对象引用时，`bind` 形成 bound Endem 或 Weave。发布时，`pack` 冻结候选并请求外部签名，`seal` 核对回填。`run` 在隔离域建立 Frame，并把环境观察与决定写入 Witness。

## 当前实施范围

第一条实现切片只包括 `form`、`check`、`see` 和 `test`。只有最小格式、两条读取路径、恶意语料和字节复现稳定后，才实现 `bind`、`pack`、`seal` 与 `run`。
