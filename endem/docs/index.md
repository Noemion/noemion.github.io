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
page_lead: "从人写下目标开始，说明计划中的 endem 命令会怎样保存原意、报告歧义、检查文件并为受限运行做准备。"
summary: "按一项目标的处理顺序阅读格式、组合、安全、运行和命令参考。"
manual_index_heading: "endem 手册目录"
badges: ["单一命令入口", "实验核心"]
---

## 这套手册解决什么问题

`endem` 是 Noemion 计划中的唯一公开命令行入口。用户围绕同一项目标工作：先把已经确认的解释写成文件，再检查文件、连接依赖，并在真正运行前重新核对权限。五个动作负责这些不同步骤，不要求用户安装或记住一组互不相干的程序。

> `ktise/elenk/theor` 目前只有职责与未来契约，没有可执行实现、安装包或稳定命令接口，因此不提供虚构的运行步骤。

## 推荐阅读顺序

1. 阅读[格式与成形](format.html)，理解一个根 `skena` 和 `rhem/semion/skena/telis/krin/apor`。
2. 阅读[绑定与组合](binding.html)，理解 nascent Endem 怎样成为 coherent Endem 或 Synem。
3. 阅读[安全与独立检查](safety.html)，区分生产 `elenk` 与独立 `theor`。
4. 阅读[发布与运行](running.html)，理解生产者封装、外部签名、Dromen 和 Iknem。
5. 最后使用[参考索引](reference.html)按工作查动作、对象、结果域、目标约束和诊断来源。

## 最短主线

人写下的目标先进入来源保留的形成版。只有解释已经按规则确认，`ktise` 才把它写成初始 Endem；含义不清时必须停止并报告问题。最终发布版按独立 Profile 移除原文，并以新身份重新验证来源绑定。`elenk` 从写入一侧检查实际字节，`theor` 再用独立代码读取同一文件。目标需要引用其他目标时，`pleko` 固定全部依赖。外部系统可以对精确发布内容签名；真正运行前，`drase` 还要重新核对环境、能力和预算，并把观察写入 Iknem。

## 当前实施范围

项目尚未进入组件开发。未来最先验证的范围只包括 `ktise`、`elenk`、独立 `theor` 和必需的一致性检查；最小格式、两条读取路径、恶意输入和逐字节复现得到实现证据后，才会评估 `pleko`、外部发布集成与 `drase`。
