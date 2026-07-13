---
layout: "manual"
title: "架构设计指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 架构设计指南"
permalink: "/docs/architecture-guide.html"
manual_id: "docs"
manual_group: "guides"
manual_order: 3
nav_title: "架构设计指南"
page_heading: "Noemion 架构设计指南"
page_lead: "从 Endem 到 Tekmor，理解三个实现域、四个名词和每道信任边界。"
summary: "从 Endem 到 Tekmor，理解三个实现域、四个名词和每道信任边界。"
badges: ["Architecture", "Endem", "Trust Boundaries"]
---

## 最小系统图

```text
受控来源表达
      │ poie
      ▼
    Endem ── pleko ──► Synem ── praxe ──► Dromen
      │                 │                    │
      └── theor ────────┴── theor            ▼
                                           Tekmor
```

这四个名词有不同生命周期。Endem 是最小目标制品；Synem 是解析后的组合闭包；Dromen 是一次会话的实现态；Tekmor 是有范围的证据记录。中间报告只有在权威、权限、保密或生命周期确实不同时，才成为独立伴随记录。

## 三个实现域

| 域 | 输入 | 输出 | 失败责任 |
| --- | --- | --- | --- |
| **Poiet** | 来源绑定、Endem、固定依赖、发布策略 | Endem、Synem、签名请求、分层诊断 | 来源不明、语义未授权、格式/引用/约束冲突、非确定性、闭包不完整 |
| **Theor** | 任意不可信 Endem、Synem 或 Tekmor 字节 | 有界只读视图、差异、引用、大小和跟踪信息 | 畸形输入、未知关键结构、资源超限、无法比较；不能产生生产验证句柄 |
| **Praxor** | Synem、运行配置、验收策略和能力目录 | Dromen、Tekmor 和最终决定 | 签名或闭包失败、能力拒绝、预算耗尽、状态漂移、证据缺失和人工升级 |

公开 CLI 都叫 `endem`，但 `theor` 必须单独构建，`praxe` 必须单独进程。用户心智模型可以简洁，内部信任边界不能因此合并。

## 形成与语义确认

`poie` 只接受两类可确认语义：可以由确定性规则从 `rhem` 重推导的内容，或由具名权威确认的语义决定。模型、检索器和外部前端只能提交候选；它们不能写规范字节、选择布局或关闭 `apor`。

一个 Endem 只允许一个根 `skena`。计划、思维链、采样参数、实时能力句柄、私钥和运行历史不属于 Endem。

## 组合与发布

`pleko` 解析 Endem 引用、固定依赖、检查约束可满足性并构造 Synem。能力合并只能保持或收窄权限；硬约束或验收冲突必须失败，不能调用模型“猜一个折中”。

`tasse` 只执行规范定义的类型化裁剪，并证明 semion、skena、telis、krin、apor、依赖和披露行为保持等价。`sphra` 生成不可变签名请求，核对外部签名响应；Poiet 永不持有私钥。

## 装载与运行

Praxor 不信任路径名、缓存结论或 `theor` 输出，而是重新读取实际 Synem 字节。全部结构、闭包、摘要、签名、策略与能力上限通过后才建立 Dromen。

Praxor 外侧的控制平面持有实时能力句柄。模型提出类型化能力请求，确定性策略决定执行或拒绝。真实界面、日志、测试和工具返回形成环境观察；模型只能给出候选和建议性评价。

`krin`、验收策略、预算、停止条件和人工升级条件在运行前确定。Tekmor 绑定事件、证据范围、对象身份、环境和策略。系统先区分 `met / unmet / agno / fault`，再由具名权威形成 `accepted / rejected / deferred`；Praxe 会话另行记录 `completed / failed / interrupted`。这些结果不能互相替代。

若 `telis` 为 `mene`，时间范围还必须区分 `fixed` 确定 UTC 区间与 `elapsed` 具名事件经过时长。连续性使用 `strict` 或完整 `budgeted`；采样点之间没有覆盖保证时保持 `agno`，不能因为没有告警而推成 `met`。

## 信任不是单一分数

每一步只增加特定范围的证据：来源、结构、语义、闭包、完整性、环境授权或验收。一个结构有效的 Endem 仍可能语义未确认；一个签名正确的 Synem 仍可能不适合当前策略；一个高质量模型候选仍不是 accepted。

[查看完整生命周期](../architecture/endem-lifecycle.html) · [查看结果分层决定](../architecture/adr-0015-result-domains.html) · [查看 mene 时间决定](../architecture/adr-0016-mene-time-model.html) · [查看组件职责](../components/) · [查看测试要求](../development/testing.html)
