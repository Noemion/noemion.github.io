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
page_heading: "endem 使用手册"
page_lead: "说明一个命令怎样形成、检查、组合、发布并在最小权限下实现目标制品。"
summary: "Endem 格式、组合、安全、运行和命令参考的连续手册。"
manual_index_heading: "endem 手册目录"
badges: ["Single CLI", "Experimental Core"]
---

## 这套手册解决什么问题

`endem` 是 Noemion 唯一公开命令行入口。八个动作沿同一件 Endem 制品的生命周期分工，不再要求用户先理解一组仿照传统对象工具命名的程序。

> 项目尚未进入代码开发阶段，`ktise/elenk/theor/peira` 目前只有职责与未来契约，没有可执行实现、安装包或稳定命令接口。本手册只解释处理边界，不提供虚构的运行步骤。

## 推荐阅读顺序

1. 阅读[格式与成形](format.html)，理解一个根 `skena` 和 `rhem/semion/skena/telis/krin/apor`。
2. 阅读[绑定与组合](binding.html)，理解 nascent Endem 怎样成为 coherent Endem 或 Synem。
3. 阅读[安全与独立检查](safety.html)，区分生产 `elenk` 与独立 `theor`。
4. 阅读[发布与运行](running.html)，理解 `tasse`、外部签名、`sphra`、Dromen 和 Iknem。
5. 最后使用[参考索引](reference.html)查找八个入口、状态、制品和稳定失败类别。

## 最短主线

受控来源表达先经过确定性投影规则或具名决定，再由 `ktise` 形成 nascent Endem。`elenk` 运行生产验证，`theor` 使用另一套实现观察同一字节。需要跨对象引用时，`pleko` 形成 coherent Endem 或 Synem。发布时，`tasse` 冻结候选并请求外部签名，`sphra` 核对响应。最后，`drase` 在隔离域建立 Dromen，把环境观察规范化为 phain，并写入 Iknem。

## 当前实施范围

第一条实现切片只包括 `ktise`、`elenk`、独立 `theor` 和必需的一致性门禁。`peira` 是否成为公开动作仍需证明；只有最小格式、两条读取路径、恶意语料和字节复现稳定后，才实现 `pleko`、`tasse`、`sphra` 与 `drase`。
