---
layout: "manual"
title: "架构设计指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 架构设计指南"
permalink: "/docs/architecture-guide.html"
manual_id: "docs"
manual_group: "guides"
manual_order: 4
nav_title: "架构设计指南"
page_heading: "Noemion 架构设计指南"
page_lead: "从 Endem 到 Iknem，理解三个实现域、四个名词和每道信任边界。"
summary: "从 Endem 到 Iknem，理解三个实现域、四个名词和每道信任边界。"
badges: ["Architecture", "Endem", "Trust Boundaries"]
---

## 最小系统图

```text
受控来源表达
      │ ktise
      ▼
    Endem ── pleko ──► Synem ── drase ──► Dromen
      │                 │                    │
      └── theor ────────┴── theor            ▼
                                           Iknem
```

这四个名词有不同生命周期。Endem 是最小目标制品；Synem 是解析后的组合闭包；Dromen 是一次 Drase 会话的只读执行契约；Iknem 是有范围的证据记录。中间报告只有在权威、权限、保密或生命周期确实不同时，才成为独立伴随记录。

## 三个实现域

| 域 | 输入 | 输出 | 失败责任 |
| --- | --- | --- | --- |
| **Ktisor** | 来源绑定、Endem、固定依赖、发布策略 | Endem、Synem、签名请求、分层诊断 | 来源不明、语义未授权、格式/引用/约束冲突、非确定性、闭包不完整 |
| **Theor** | 任意不可信 Endem、Synem 或 Iknem 字节 | 有界只读视图、差异、引用、大小和跟踪信息 | 畸形输入、未知关键结构、资源超限、无法比较；不能产生生产验证句柄 |
| **Drasor** | Synem、运行配置、验收策略和能力目录 | Dromen、Iknem 和最终决定 | 签名或闭包失败、能力拒绝、预算耗尽、状态漂移、证据缺失和人工升级 |

公开 CLI 都叫 `endem`，但 `theor` 必须单独构建，`drase` 必须单独进程。用户心智模型可以简洁，内部信任边界不能因此合并。

## 形成与语义确认

`ktise` 只接受两类可确认语义：可以由确定性规则从 `rhem` 重推导的内容，或由具名权威确认的语义决定。模型、检索器和外部前端只能提交候选；它们不能写规范字节、选择布局或关闭 `apor`。

一个 Endem 只允许一个根 `skena`。计划、思维链、采样参数、实时能力句柄、私钥和运行历史不属于 Endem。

## 组合与发布

`pleko` 解析 Endem 引用、固定依赖、检查约束可满足性并构造 Synem。能力合并只能保持或收窄权限；硬约束或验收冲突必须失败，不能调用模型“猜一个折中”。

当前没有可执行的裁剪等价规范。未来只有在版本化关系明确列出必须保留的 semion、skena、telis、krin、apor、依赖和披露属性，并具备正反向量后，对应制品生产者才能执行允许的类型化变换；否则保留内容或失败。外部签名集成核对不可变签名请求与响应；Ktisor 永不持有私钥。

## 装载与运行

Drasor 不信任路径名、缓存结论或 `theor` 输出，而是重新读取实际 Endem 字节并核对 Synem 的精确成员闭包。全部结构、绑定、摘要、签名、政策、环境、能力、预算和证据责任通过后，才按 [DRO-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)封存 Dromen；Synem 物理格式尚未定义。

Drasor 外侧的控制平面持有实时能力句柄。模型提出类型化能力请求，确定性策略决定执行或拒绝。真实界面、日志、测试和工具返回形成环境观察；模型只能给出候选和建议性评价。

“发现了工具”不等于“本会话可以调用”。Agent Card、工具列表与 schema 是声明，协议初始化形成协商结果，AUT 形成动作授权，Dromen 固定会话上限，调用前还要检查即时端点、预算、配额与输入。完整边界见[能力发现、协商与调用研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/capability-discovery-and-negotiation-proposal.md)；它当前非规范，不创建 `CAP-CORE` 或能力制品。

“多个分支正在并行”也不等于“多个分支都能提交”。分支只从同一 Dromen 上限取得能力子集和预算份额；候选进入外部副作用前，必须重新核对当前对象身份、授权、协议和交付前提。取消失败分支不能撤销已经发生或未知的效果，最快完成和模型评分也不能决定提交。完整边界见[并行、推测执行与提交边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/parallel-and-speculative-execution-proposal.md)；它当前非规范，不创建 `PAR-CORE`、事务制品或调度器。

“运行在容器里”也不等于“模型、凭据和副作用已经隔离”。模型输入、控制面、授权、凭据与实时句柄、协议适配、文件、网络、资源终止、观察和外部目标必须分别说明强制机制、覆盖范围、有效状态与失败责任；模型永不接收原始凭据和实时句柄，强制控制不可用时对应能力关闭失败。完整边界见[模型、适配器与能力域隔离研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-adapter-isolation-proposal.md)；它当前非规范，不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品或部署对象。

“模型给出高分”也不等于“测量有效或目标满足”。评测目的、构念、评分说明、题目、协议、模型评审调用、原始输出、统计汇总和使用决定必须分开。模型评审结果保持 `model-candidate`；多个模型投票、排行榜和自报置信度都不能自动成为独立证据、统计区间或最终接受。完整边界见[模型参与评测与裁判边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-assisted-evaluation-proposal.md)；它当前非规范，不创建评测 CORE、裁判服务或新专名。

`krin`、验收策略、预算、停止条件和人工升级条件在运行前确定。Iknem 绑定事件、证据范围、对象身份、环境和策略。系统先区分 `met / unmet / agno / fault`，再由具名权威形成 `accepted / rejected / deferred`；Drase 会话另行记录 `completed / failed / interrupted`。这些结果不能互相替代。

若 `telis` 为 `mene`，时间范围还必须区分 `fixed` 确定 UTC 区间与 `elapsed` 具名事件经过时长。连续性使用 `strict` 或完整 `budgeted`；采样点之间没有覆盖保证时保持 `agno`，不能因为没有告警而推成 `met`。

否定目标仍使用同一关系、角色和顺序，只改变 `skena` 极性。查询未命中或日志为空默认保持 `agno`；只有具名权威证明有限观察范围完整封闭时，缺席才可支持 `met`。观察器故障为 `fault`，同构正反例为 `unmet`。

## 信任不是单一分数

每一步只增加特定范围的证据：来源、结构、语义、闭包、完整性、环境授权或验收。一个结构有效的 Endem 仍可能语义未确认；一个签名正确的 Synem 仍可能不适合当前策略；一个高质量模型候选仍不是 accepted。

[查看完整生命周期](../architecture/endem-lifecycle.html) · [查看 Agent 系统边界图](../architecture/agent-system-boundaries.html) · [查看结果分层决定](../architecture/adr-0015-result-domains.html) · [查看 mene 时间决定](../architecture/adr-0016-mene-time-model.html) · [查看否定与缺席决定](../architecture/adr-0017-negation-and-absence.html) · [查看组件职责](../components/) · [查看测试要求](../development/testing.html)
