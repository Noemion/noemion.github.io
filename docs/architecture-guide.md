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
page_lead: "用一次依赖升级定位目标、制品、会话、外部动作、观察和决定；每一步只承担自己能够证明的主张。"
summary: "沿一次 Agent 工作判断信息由谁产生、谁能修改、何时停止，以及谁有权作出最后决定。"
badges: ["开发者路径", "责任边界", "主张范围"]
---

## 先用一张责任图定位问题

Noemion 不把“Agent 完成了任务”当作单一事实。开发者先判断自己正在处理目标内容、确定性制品、一次运行、外部动作、环境观察，还是最终决定：

```text
来源表达 + 已确认的意义
          │
          ▼
        deterministic producer ──► Endem ──► Endem closure 组合闭包
                     │
                     └── independent inspector  当前只独立读取 Endem 字节

精确发布输入 + 当前授权 ──► bounded runner ──► session contract
                                      │
                                      ▼
                              受限动作与环境观察
                                      │
                                      ▼
                         evidence entry ─支持─► 满足结果 ─► 具名决定
```

Endem 保存一个根目标；Endem closure 固定多个 Endem 的完整依赖闭包；session contract 只约束一次受限会话；evidence entry 保存有范围的观察、方法、来源和限制。当前只有 Endem 具有实验性物理字节规范，图中的 Endem closure、session contract 和 evidence entry 不表示已经存在文件格式或组件实现。

## 用一次 Agent 工作读图

以“更新服务依赖，并确认当前版本可以发布”为例。架构顺序不是一串工具调用，而是一组不能互相代替的责任：

| 开发者正在做什么 | 负责的边界 | 到哪里必须停止 |
| --- | --- | --- |
| 解释团队要求 | 来源、文本与意义确认 | 服务、版本、范围或判据没有唯一解释时，保留待确认项 |
| 固定目标内容 | deterministic producer 与 Endem | 模型建议仍是候选；只有确定性规则或具名意义决定可以进入制品 |
| 检查实际字节 | 生产侧 `lint` 与independent inspector | 两条路径分歧时保存最小复现，不能改写输入制造一致 |
| 准备一次运行 | bounded runner 与 session contract | 对象、政策、环境、能力、预算或观察责任未闭合时，不建立会话 |
| 调用工具或远端 Agent | 控制平面与协议适配 | MCP/A2A 状态保留外部来源；`completed` 不直接映射为满足结果 |
| 形成环境事实 | `structured_observation` 与 evidence entry | 工具返回、日志或模型说明缺少主体、方法、范围或限制时，不能扩大主张 |
| 判断能否发布 | `satisfaction_criteria` 与具名权威 | 先形成 `met / unmet / undetermined / fault`，再独立形成 `accepted / rejected / deferred` |

这条主线能解释常见的“成功但不能发布”：工具调用可以完成，当前目标仍可能没有满足；测试可以通过，证据范围仍可能不足；满足结果可以是 `met`，具名权威仍可以依据独立政策拒绝发布。

## 看到终态后按主张强度继续核对

当仓库已经显示目标版本时，不要立刻把终态归因给本次 Agent。先选择真正要回答的问题：

| 要回答的问题 | 最低材料 | 可以形成的结论 |
| --- | --- | --- |
| 目标关系现在是否成立？ | 精确仓库、分支、锁文件、目标版本和适用测试的当前观察 | 满足结果；不说明谁做过什么 |
| 指定动作是否发生？ | 调用身份、实际行动者、精确输入、开始、结束和外部返回 | 动作事实；不说明状态一定变化 |
| 同一对象是否发生状态变化？ | 同一对象的可信前态、后态、观察窗口和缺口 | 有范围的转变事实；不说明变化原因 |
| 本次动作是否造成变化？ | 动作与前后态的关联、影响窗口、并发活动和具名判断方法 | 只形成方法覆盖范围内的因果主张 |
| 谁可以行动或接受结果？ | 逐动作授权、委托链、政策、决定语境和具名权威 | 授权或决定；不倒写动作、转变和因果事实 |

会话开始前已经使用目标版本时，结果型目标可以是 `met`，但不能声称本次会话执行了升级。另一个自动化程序并发提交目标版本时，后态可以成立，也不能归因给本次失败的调用。完整反例和进入规范前的条件见[状态变化与因果归因边界研究提案](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html)。

## 委托或恢复时重新建立边界

**委托另一个 Agent 时保留身份与上限。** **跨会话继续时先分清保存对象。** 两种情况都不能因为界面上仍显示同一个任务，就继承旧权限或把摘要当成完整事实：

| 重新检查什么 | 委托另一个 Agent | 恢复后续会话 |
| --- | --- | --- |
| 主体 | 同时保存请求主体、实际行动者、被代表主体和每一级委托 | 重新绑定当前请求者、运行实例、会话与适用政策 |
| 输入 | 固定精确对象、过滤、摘要、字段删除和不可见内容 | 区分消息历史、跨运行记忆、检查点、工作区快照与外部任务句柄 |
| 能力与预算 | 只分配当前 session contract 的严格子集，共享或细分总预算 | 重新取得最小凭据和实时句柄，不从检查点反序列化权限 |
| 当前有效性 | 下游开始前重新核对对象、授权、协议和截止点 | 逐项重验适用的外部陈述、验证记录和依赖方准入判断 |
| 返回内容 | 下游完成仍只是候选运行事实，满足与接受继续独立判断 | 保存的控制位置只说明此前认为进行到哪里，不证明动作完成 |

恢复实现应先**选择一种对话状态策略**；必须组合本地历史与服务端状态时，按消息身份和截止点去重。**恢复必须重新验证**，并建立新的 session contract，而不是复活旧会话。精确条款见[权威与授权决定规范](../specifications/authority.html)，研究边界见[软件 Agent 身份、委托与责任链提案](https://noemion.github.io/spec/software-agent-identity-and-accountability-boundaries-proposal.html)与[记忆、检查点与恢复边界研究提案](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html)。

## 三个实现域不能合并

一个公开 CLI 可以简化用户入口，但不能让写入、独立读取和受限运行共享同一信任结论：

| 实现域 | 负责什么 | 当前限制 |
| --- | --- | --- |
| deterministic producer | 消费受控来源、意义决定、精确规范和 Profile；确定性形成来源保留的 Endem，以及未来物理 Profile 确定后的 Endem closure 与发布派生 | 不替权威选择意义，不持有私钥或实时能力；发布 Profile 未定义时不执行裁剪派生 |
| independent inspector | 独立读取实际 Endem 字节，在精确规则、视图和预算下输出只读视图、差异与诊断 | Endem closure、evidence entry 与发布制品等待物理格式；不复用形成侧解析实现，不产生生产检查通过结论 |
| bounded runner | 重新核对精确运行输入、外部陈述、政策、环境、能力与预算；建立 session contract 并控制一次会话 | 不信任路径名、缓存结论或 independent inspector 输出，不写制品，也不替具名权威接受结果 |

组件页分别给出 [deterministic producer](../components/producer.html)、[independent inspector](../components/inspector.html)与 [bounded runner](../components/runner.html) 的完整输入、输出、失败责任和停止条件。当前没有三个组件、`endem` CLI、Endem closure 物理格式、session contract 运行时或 evidence entry 物理格式。

## 按问题进入进阶资料

Agent 工程正在同时推进协议互操作、身份授权与安全评估。它们是不同问题轴，不能合成一个“Agent 标准”或单一信任分数。开发者只展开与当前故障直接相关的一组：

| 遇到的问题 | 继续阅读 | 先保留的边界 |
| --- | --- | --- |
| 想先看完整责任链 | [Agent 系统边界图](../architecture/agent-system-boundaries.html) | 规范、非规范研究和未来实现证据分开 |
| 对端声明了新工具或能力 | [能力发现、协商与调用](https://noemion.github.io/spec/capability-discovery-and-negotiation-proposal.html) | 发现、协商、授权、会话上限和即时可调用性分开 |
| 多个 Agent 或分支并行 | [并行、推测执行与提交](https://noemion.github.io/spec/parallel-and-speculative-execution-proposal.html) | 分支共享总上限，完成、取消和提交许可分开 |
| 模型、适配器和工具处于不同权限域 | [模型、适配器与能力域隔离](https://noemion.github.io/spec/model-adapter-isolation-proposal.html) | 秘密留在能力域，容器或超时不冒充完整隔离 |
| 模型参与评价或训练更新 | [模型参与评测与裁判](https://noemion.github.io/spec/model-assisted-evaluation-proposal.html) · [模型训练与更新](https://noemion.github.io/spec/model-training-and-update-boundaries-proposal.html) | 模型评价保持候选；评测结果、训练资格和发布决定分开 |
| 需要跨会话继续 | [记忆、检查点与恢复](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html) | 保存状态不恢复事实、权限或已发生副作用 |

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)要求文档按用户面对的概念与问题组织，而不是复制实现结构。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)也把产业标准、社区协议以及身份与安全研究分为不同工作轴。这里采用的是问题分层方法；这些外部资料不定义 Noemion 字段、结果域、组件或实现状态。

## 当前可以证明什么

**已有成果：**现行 CORE、ADR、Profile 与研究提案已经把目标内容、制品形成、独立读取、会话能力、外部动作、证据和决定分开。机器可读规范清单与向量可以检查资料内部一致性。

**正在研究：**Endem closure 与最终发布制品的物理 Profile、Agent 身份与委托、能力协商、隔离、跨会话恢复、并行提交、模型评测和训练更新仍需独立证据与决定。

**限制条件：**当前没有组件实现、运行时、互操作实验或人类读音发行证据。deterministic producer、independent inspector、bounded runner、Endem、Endem closure、session contract 与 evidence entry 的发行拼写和口头区分度仍处于设计阶段；职责定义不等于名称已经适合传播。

开发规范或实现前，使用[规范与查询](../specifications/)定位权威源，使用[测试策略](../development/testing.html)限定证据能够支持的主张。
