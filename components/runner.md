---
layout: content
title: bounded runner · 受限运行边界
page_role: content
footer_text: Noemion · bounded runner
permalink: "/components/runner.html"
summary: 介绍未来的受限运行者怎样为一次会话限制模型能力、收集实际观察，并把运行结果与最终决定分开。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 系统组件
  url: index.html
page_heading: 受限运行边界
page_lead: bounded runner 未来负责把一个已检查的目标放进一次性会话，限制模型能请求的能力，并把实际观察与最终决定分开记录。
badges:
- 受限运行边界
- 一次性会话
- 最小能力
- 尚未实现
previous_url: inspector.html
previous_label: independent inspector
next_url: "../architecture/endem-lifecycle.html"
next_label: Endem 生命周期
---

## 用一次依赖更新理解 bounded runner

假设目标是“更新服务依赖，并确认当前版本可以发布”。模型可以建议改动、请求读取清单或运行测试，但它既没有默认文件权限，也不能把“命令退出成功”直接写成“目标已经满足”。

1. 精确 Endem / Endem closure 与外部陈述
2. 政策、环境、能力与预算求交
3. 封存一次 session contract
4. 模型提出补丁或类型化能力请求
5. 控制面授权并调用适配器
6. 实际观察形成 evidence entry
7. satisfaction_criteria 判断满足情况
8. 具名权威另行决定

测试服务报告完成，只能证明一次外部任务到达其终态；本地仍要核对锁文件、目标平台、安全政策和判据要求。bounded runner 记录这条责任链，却不能给自己的记录填写“真实”“覆盖充分”或“最终接受”，也不能代替决定权威。

> **名称状态：**bounded runner 是由普通英语词组成的设计阶段职责名称，已经按逐词词首、职责和关键字语料接受。它不表示运行组件已经实现；首次说明时先写“受限运行边界”，再用 bounded runner 指向这里的定义。

## 先把模型、控制面、适配器和决定者分开

模型输出是不可信候选，不是权限、观察或决定。若同一模型进程同时持有凭据、执行工具、解释返回并宣布完成，提示注入、工具描述污染或后端故障就会跨过全部防线。

| 参与者 | 可以做什么 | 不能自行决定什么 |
| --- | --- | --- |
| 模型或求解器 | 提出候选改动、解释和类型化能力请求 | 实际权限、工具结果真实性、目标满足或最终接受 |
| bounded runner 控制面 | 检查请求、政策、预算与当前状态，执行或拒绝已登记能力 | 改写 Endem、扩大授权来源或代替具名决定权威 |
| 能力适配器 | 在单一能力边界内访问文件、网络、进程或外部协议 | 把远端描述当成本地授权，把返回文本当成已验证事实 |
| 判断与决定责任 | 依据 `satisfaction_criteria` 和有范围的 evidence entry 形成满足结果；具名权威再形成决定 | 由模型评分、会话成功或证据数量替代政策 |

## 运行前形成一次只读会话契约

bounded runner 先重新验证实际输入，再把本次会话允许看见和使用的部分求交为只读 session contract。它不会把制品、凭据和工具列表一起塞进提示词。

| 封闭内容 | 来源 | 变化后的处理 |
| --- | --- | --- |
| 精确目标与依赖闭包 | Endem 精确字节；如适用，则为已固定且重新检查的 Endem closure 成员闭包 | 身份或闭包变化使旧会话失效，不能在会话中偷偷下载新成员 |
| 适用外部陈述 | 绑定精确主体的签名、来源、验证政策、截止点、撤销和验证结果 | 到期、撤销或政策变化后重新验证，不复用旧结论 |
| 能力与环境 | 具名政策、能力目录、目标资源、后端和适配器身份 | 新增权限或 step-up 授权建立新会话，不原地扩大 session contract |
| 预算与停止条件 | 时间、调用数、输出量、重试、副作用和终止策略 | 预算耗尽按预注册策略中断，不能让模型无限重试 |
| 观察与决定责任 | `satisfaction_criteria`、所需 evidence entry 范围和具名决定权威 | 判据、观察范围或决定者变化时重新建立会话 |

session contract 只保存本次运行需要的非秘密语义与能力描述，不包含 Bearer token、文件描述符、网络连接或其他实时句柄。SESSION-CORE 分别核对 `resolved` 内容、外部陈述、验证政策、截止点、撤销状态和依赖方准入，不把这些关系压成内容自身的布尔状态。完整契约见 [SESSION-CORE](../specifications/session-contract.html) 与 [ADR-0024](../architecture/adr-0024-dromen-session-contract.html)。

## 一次能力请求怎样穿过边界

1. **验证会话：** 检查实际对象、外部陈述、当前政策和环境；关键条件失败时原子拒绝，不留下部分 session contract。
2. **提出请求：** 模型只看见当前步骤所需的语义和能力说明，并返回候选或结构化请求，不能直接取得实时句柄。
3. **决定是否调用：** 控制面检查参数、调用者授权、目标资源绑定、预算、副作用、幂等与会话状态，再交给单一职责适配器或拒绝。
4. **保存实际返回：** 适配器保留原始返回和来源；确定性变换形成可比较的 `structured_observation` ，模型解释仍标为 `model-candidate` 。
5. **分开结果：** evidence entry 保存有范围的记录； `satisfaction_criteria` 形成 `met / unmet / undetermined / fault` ，具名权威形成 `accepted / rejected / deferred` ，会话终止另记为 `completed / failed / stopped` 。

| 失败位置 | 保存什么 | 声明停在哪里 |
| --- | --- | --- |
| 装载拒绝 | 实际对象身份、失败层、规则与位置 | 不能创建部分 session contract，也不能伪造 `unmet` |
| 能力被拒绝 | 请求摘要、调用者、目标资源、政策版本和拒绝规则 | 不能自动扩大权限；缺少必需观察通常留下 `undetermined` |
| 适配器故障或预算耗尽 | 组件身份、稳定错误类别、预算、停止位置与已知副作用 | 不能把工具故障改写为目标不满足，也不能把 `stopped` 写成完成 |
| 环境漂移或证据不足 | 期望与实际身份、缺失判据、覆盖范围和决定责任 | 旧 session contract 失效；日志、签名或模型评分不能产生 `accepted` |

时间覆盖、负观察、量化集合、测量不确定度和复合判断属于 [Endem 规范](../specifications/endem.html)；evidence entry 的记录、来源与评估分层见 [EVIDENCE-CORE](../specifications/evidence-entry.html)。bounded runner 不复制另一套判断规则。

## 会话结束后仍要守住两条边界

### 终态出现后不要立即归给本次动作

会话开始前目标已经成立时，只记录实际终态，不制造“本次会话完成了目标”的因果叙述。工具失败而另一个控制器改变对象时，分别保存失败调用、外部活动和后态。动作确实造成变化，但没有有效授权时，因果事实、授权拒绝和最终决定仍然可以同时成立。

GNU Make 的 [`-q` 查询](https://www.gnu.org/software/make/manual/html_node/Instead-of-Execution.html)与 [phony target](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html)帮助区分目标状态、是否需要动作和动作入口；完整反例见[非规范因果归因研究](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html)。

### 从检查点继续必须建立新会话

检查点可以保存候选上下文和控制位置，却不能保存一次会话的权限。继续执行时，bounded runner 把保存状态当作新输入，重新完成会话准入，并查询断线前结果未知的外部调用。旧秘密、实时句柄、批准、预算余额和一次性授权消费都不能恢复；历史、快照与新观察不能合并成“Agent 已恢复”。

完整状态分类见[非规范记忆、检查点与恢复研究](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html)。

## 实现前还要回答三个研究问题

### 外部 Agent 协议只提供带来源的事实

截至 2026-07-15，[MCP 2025-11-25 当前修订](https://modelcontextprotocol.io/specification/2025-11-25)仍是正式基线；已发布的 [2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)包含破坏性变化，在最终发布与安全复核前不改变本地适配基线。[A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/) 的 Task、Message、Artifact 与终态仍属于外部域：`completed` 不等于本地 `met`，取消请求也不保证已经取消。适配器必须保留协议版本、对端、目标资源绑定和映射损失。

### 隔离必须证明什么

容器、超时或 seccomp 只是机制名称。未来实现要用拒绝测试证明文件与网络默认不可见、秘密和实时句柄不进入提示或 session contract、资源能够回收、重复提交与结果未知能够关闭失败。GNU [`timeout`](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html)、Make [job slots](https://www.gnu.org/software/make/manual/html_node/Job-Slots.html) 与 Guix [`shell --container`](https://guix.gnu.org/manual/en/guix.html#Invoking-guix-shell)分别提供终止、共享并发预算和先隔离后开放资源的工程纪律；它们都不能单独证明 bounded runner 安全。

### 观察字段不能自行成为证据

[OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)已把 GenAI 约定移到独立仓库；[GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)只标识 schema 演进线，Schema URL 不等于稳定发布，多项相关定义仍是 Development。未来映射必须固定仓库版本、字段稳定性、脱敏与导出政策，并默认不导出敏感正文。[NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)也把互操作、开放协议、身份授权和安全评估分开推进；这支持责任拆分，不定义 Noemion 字段。

> 协议映射遵守 [ADP-CORE](../specifications/adapters.html) 与 [AUT-CORE](../specifications/authority.html)。部署隔离仍由[非规范模型与适配器隔离研究](https://noemion.github.io/spec/model-adapter-isolation-proposal.html)继续检查，当前没有适配器、沙箱或遥测导出器。

## 当前状态与限制条件

**已有成果：**`endem run` 背后的职责边界、session contract 会话契约、evidence entry 记录分层，以及满足结果、会话结果和最终决定的分离。

**限制条件：**当前没有 bounded runner 实现、运行 API、沙箱、能力适配器、预算计数器、遥测导出器或 evidence entry 物理格式。它未来可以调用 deterministic producer 的形成侧检查接口，但不得链接写入器、修改精确制品或处理外部签名私钥；具体隔离能力只有在组件阶段通过对应威胁测试后才能陈述。
