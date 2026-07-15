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
page_lead: "用一次依赖升级说明：人提出的目标、模型建议、工具调用、运行权限、观察记录和最终接受为什么必须由不同职责处理。"
summary: "沿一次 Agent 工作判断每类信息由谁产生、谁能修改，以及谁有权作出最后决定。"
badges: ["架构", "Endem", "信任边界"]
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

## 用一次 Agent 工作读图

仍以“更新服务依赖并确认可以发布”为例。架构图不是工具调用顺序，而是责任不能越过的边界：

| 工作时刻 | 主责任 | 必须保留的边界 |
| --- | --- | --- |
| 解释团队要求 | 来源、文本和授权边界 | 模型只提出候选；未确认的服务、版本、范围和判据继续保留 |
| 形成 Endem 或 Synem | Ktisor | 目标身份与实现计划分开；确定性规则或具名决定才进入规范内容 |
| 准备一次运行 | Drasor 与 Dromen | 重新核对实际对象、政策、环境、能力、预算和证据责任 |
| 调用工具或远端 Agent | 控制平面与协议适配 | MCP/A2A 状态保留外部来源；`completed` 不直接映射为满足结果 |
| 收集测试与运行观察 | `phain` 与 Iknem | 记录主体、方法、环境、范围、截止点和限制，不把日志数量当充分性 |
| 判断能否发布 | `krin` 与具名权威 | 先形成 `met / unmet / agno / fault`，再独立形成 `accepted / rejected / deferred` |

这条路径说明为什么单一 Agent 对象、工作流状态或“成功”标志不能覆盖整个系统。需要评审外部协议、并行、记忆、模型评测或托管服务时，继续使用[Agent 系统边界图](../architecture/agent-system-boundaries.html)定位责任。

## 看到终态后按主张强度继续核对

依赖升级工具返回 `completed`，随后测试也通过，仍然只得到几项需要分别验证的事实。开发者应当先判断自己要陈述的是当前结果、一次动作、一次状态变化，还是该动作造成了变化：

| 要回答的问题 | 最低材料 | 可以形成的结论 |
| --- | --- | --- |
| 目标关系现在是否成立？ | 精确仓库、分支、锁文件、目标版本和适用测试的当前观察 | 由 `krin` 形成 `met / unmet / agno / fault`；不说明谁做了什么 |
| 指定动作是否发生？ | 有身份的调用、实际行动者、输入、开始、结束和外部返回 | 说明升级请求或工具调用怎样结束；不说明仓库发生了变化 |
| 同一对象是否发生状态变化？ | 同一仓库与分支的可信前态、后态、观察窗口和缺口 | 说明旧版本关系变为新版本关系；不说明变化由哪个动作造成 |
| 本次动作是否造成变化？ | 动作与前后态的精确关联、影响窗口、并发提交、其他控制器和具名判断方法 | 只形成方法适用范围内的因果主张；竞争解释未排除时保持未知 |
| 谁可以行动、承担责任或接受结果？ | 逐动作授权、委托链、政策、决定语境和具名权威 | 分别形成授权与最终决定；不能倒写动作、转变或因果事实 |

这套顺序会给出看似矛盾但正确的结果：仓库在会话开始前已经使用目标版本时，结果型目标可以是 `met`，但不能声称本次会话执行了升级；工具调用结束而锁文件未变时，动作记录可以完整，目标仍可能是 `unmet` 或 `agno`；另一个自动化程序并发提交新版本时，后态可以成立，但不能把变化归给本次失败的调用；未经授权的动作即使确实造成了变化，因果记录也不能把它改写成获准或已接受。

完整案例、竞争解释和进入规范前的条件见[状态变化与因果归因边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/state-change-and-causal-attribution-proposal.md)。它是非规范研究；当前不增加字段、结果域、组件或因果检查器，现行 Profile 无法表达的转变与因果要求必须保留为未解决边界或拒绝形成。

## 委托另一个 Agent 时保留身份与上限

把工作交给另一个 Agent（handoff）之前，先确定谁继续拥有面向用户的答复。OpenAI 的[编排与 handoff 指南](https://developers.openai.com/api/docs/guides/agents/orchestration)区分两种模式：handoff 把当前分支的控制权交给专家 Agent；把 Agent 作为工具时，主管 Agent 仍负责最终答复。这个选择只分配运行职责，不会自行产生授权、证据或最终决定。

[RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)进一步区分被代表主体与实际行动者。委托时不能把专家 Agent 伪装成请求者，也不能因控制权转移而隐藏代理链。开发者至少要保留以下内容：

| 检查项 | 交接时要固定什么 | 不得发生什么 |
| --- | --- | --- |
| 请求主体 | 谁提出这次工作，以及请求适用的项目、租户和截止点 | 把收到任务的 Agent 写成原始请求者 |
| 实际行动者 | 当前由哪个 Agent、模型、工具或服务执行精确动作 | 只记录主管 Agent，隐藏中间调用者 |
| 被代表主体 | 行动代表哪个用户、团队或服务，以及代表关系的依据 | 默认冒充主体，或把登录状态当作代表授权 |
| 控制方式 | 是专家接管当前分支，还是主管把专家作为有界工具调用 | 用“handoff”一词掩盖谁负责答复和提交 |
| 输入与损失 | 精确对象、来源、过滤、摘要、字段删除和不可见内容 | 把过滤后的历史称为完整上下文 |
| 动作授权 | 对象、动作、目的、受众、范围、期限和授予权威 | 继承主管的全部权限，或靠工具可达扩权 |
| 能力与预算 | 从当前 Dromen 取得严格子集，并共享或细分调用、时间、字节和成本上限 | 让子任务重置计数器或获得无界资源 |
| 凭据 | 在独立能力域取得绑定资源和受众的最小凭据 | 转交上游 Bearer token、私钥或实时句柄 |
| 返回结果 | 保存外部状态、候选产物、实际观察、错误和限制 | 把下游 `completed` 直接写成 `met` 或 `accepted` |
| 证据记录 | 在 Iknem 中保留实际行动者、方法、环境、范围、变换和未覆盖内容 | 用一段总结替代来源、损失和观察责任 |

[GNU Make jobserver](https://www.gnu.org/software/make/manual/html_node/Job-Slots.html)要求递归工具共享顶层并发额度，并归还实际取得的 job slot。Noemion 借鉴的是“嵌套工作不能逃离总预算”这一纪律，不把 job slot 当作权限，也不照搬 Make 的进程协议。

### 交接检查清单

1. **先选择控制方式。** 需要专家直接接管答复时才使用 handoff；主管仍需汇总和提交时，把专家作为有界工具。
2. **固定三类主体和精确输入。** 同时记录请求主体、实际行动者、被代表主体，以及交接前后的输入变换与损失。
3. **只分配能力和预算子集。** 子 Agent 的动作、资源、受众、期限、调用次数和成本都不能超过当前 Dromen。
4. **把凭据留在独立能力域。** 下游需要访问新资源时，为该资源取得最小凭据；不得透传上游令牌。
5. **按返回内容形成候选或观察。** 下游完成仍只是候选运行事实；满足判断、证据覆盖和最终决定继续由各自规则形成。

例如，主管 Agent 可以把“检查依赖兼容性”交给专家 Agent。专家只取得精确仓库快照、只读测试能力和有限预算，不取得写入、发布或部署令牌。它返回的报告先是有来源的候选；控制平面重新验证测试观察，具名权威再决定能否发布。详细授权条款见[权威与授权决定规范](../specifications/authority.html)，会话上限见 [DRO-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)。

## 跨会话继续时先分清保存对象

“继续”不表示恢复了原来的 Agent 对象。开发者必须先说明跨运行带回了哪一种状态，再决定它能支持什么：

| 保存对象 | 可以支持 | 不能替代 |
| --- | --- | --- |
| 对话状态或历史 | 组织下一次模型输入，并追溯此前收发的消息 | 事实、证据、授权或完整历史 |
| 跨运行记忆或提炼指导 | 复用带来源的偏好、纠正、项目经验和任务摘要 | 当前政策、完整会话、工作区状态或持续有效的决定 |
| 检查点或控制位置 | 说明控制平面在某个截止点认为进行到哪里 | 动作完成、目标满足或旧 Dromen |
| 工作区快照 | 在新运行中重新读取文件和环境状态 | 外部世界回滚、凭据、实时能力或远端对象未变化 |
| 外部任务句柄 | 再次定位精确协议与对端中的任务 | 本地目标、完整任务历史或产物可信度 |

[OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents/running-agents#choose-one-conversation-strategy)把应用自管历史、SDK Session、`conversationId` 和 `previousResponseId` 列为不同的对话状态策略，并提醒混用本地重放与服务端状态可能重复上下文。[OpenAI Sandbox Agents](https://developers.openai.com/api/docs/guides/agents/sandboxes#persist-memory-across-runs)进一步分开消息历史、提炼到文件的跨运行记忆，以及 resume 和 snapshot 保存的工作区状态。产品文档可以把这些机制都称为 memory；Noemion 仍按实际内容、来源、变换、生命周期和重新验证责任分类。

### 恢复检查清单

1. **选择一种对话状态策略。** 若必须组合本地历史与服务端状态，先按消息身份和截止点去重，不能直接拼接。
2. **固定保存对象的来历。** 记录来源运行、提取或压缩变换、损失、适用项目、版本、截止点和输出身份。
3. **重新审查跨运行记忆。** 用当前资料和政策核对提炼指导；陈旧、冲突、跨项目或跨租户内容不能取得权威。
4. **恢复必须重新验证。** 重新绑定精确 Endem 或 Synem 内容，逐项重验适用的外部陈述、验证记录和依赖方准入判断，并核对实际主体、政策、授权、端点、协议、schema、模型、环境、能力、预算、已消费决定和未知副作用。
5. **建立新会话。** 生成新的 Dromen，重新取得秘密和实时句柄；把新观察记录为有范围的 Iknem，不从检查点反序列化权限。

例如，旧记忆写着“默认向测试环境发布”，当前资料却要求生产发布并逐次确认。实现必须采用当前资料并阻断未获确认的发布，不能让记忆文件覆盖环境、政策或授权。同样，摘要遗漏“不得外发”时，恢复应回到原始来源或保持阻断，而不是把缺失解释为允许。

完整案例、威胁和责任分配见[记忆、检查点与恢复边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/memory-checkpoint-and-resumption-proposal.md)。它是非规范研究，不表示已经存在记忆存储、检查点格式、恢复命令或运行时。

## 三个实现域

| 域 | 输入 | 输出 | 失败责任 |
| --- | --- | --- | --- |
| **Ktisor** | 受控来源、意义决定、精确规范与 Profile、固定依赖和生产侧检查配置 | 来源保留的 Endem、分层检查结果；未来物理 Profile 确定后的 Synem 与发布派生 | 来源不明、语义未授权、格式/引用/约束冲突、非确定性、闭包不完整或发布派生保持关系无法证明 |
| **Theor** | 当前为实际 Endem 字节、精确规范/Profile、视图和预算；Synem、Iknem 与发布制品等待物理格式 | 带范围的只读视图、差异和诊断 | 畸形输入、未知关键结构、资源超限或两条路径分歧；不能修复输入或产生生产检查通过结论 |
| **Drasor** | Synem、运行配置、验收策略和能力目录 | Dromen、会话结果和有范围的 Iknem | 签名或闭包失败、能力拒绝、预算耗尽、状态漂移、证据缺失和人工升级；最终决定由具名权威另行作出 |

公开 CLI 都叫 `endem`，但 `theor` 必须单独构建，`drase` 必须单独进程。用户心智模型可以简洁，内部信任边界不能因此合并。

## 形成与语义确认

`ktise` 只接受两类可确认语义：可以由确定性规则从 `rhem` 重推导的内容，或由具名权威确认的语义决定。模型、检索器和外部前端只能提交候选；它们不能写规范字节、选择布局或关闭 `apor`。

一个 Endem 只允许一个根 `skena`。计划、思维链、采样参数、实时能力句柄、私钥和运行历史不属于 Endem。

## 组合与发布

`pleko` 解析 Endem 引用、固定依赖、检查约束可满足性并构造 Synem。能力合并只能保持或收窄权限；硬约束或验收冲突必须失败，不能调用模型“猜一个折中”。

ADR-0036 已确定形成制品保留原始自然语言，最终发布制品移除原文并取得新身份。当前仍没有可执行的裁剪规范；只有发布 Profile 明确来源引用闭包、必须保留的 semion、skena、telis、krin、apor、依赖和披露属性，并具备正反向量后，对应生产者才能执行类型化变换。外部签名集成核对发布字节的不可变签名请求与响应；Ktisor 永不持有私钥。

## 装载与运行

Drasor 不信任路径名、缓存结论或 `theor` 输出，而是重新读取实际 Endem 字节并核对 Synem 的精确成员闭包。全部结构、绑定、摘要、签名、政策、环境、能力、预算和证据责任通过后，才按 [DRO-CORE](https://github.com/Noemion/noemion.github.io/blob/main/spec/dromen-core.md)封存 Dromen；Synem 物理格式尚未定义。

Drasor 外侧的控制平面持有实时能力句柄。模型提出类型化能力请求，确定性策略决定执行或拒绝。真实界面、日志、测试和工具返回形成环境观察；模型只能给出候选和建议性评价。

实现装载与运行路径时，先按观察到的事实选择检查项：

| 观察到的事实 | 继续执行前必须确认 | 研究依据 |
| --- | --- | --- |
| Agent Card、工具列表或 schema 声明了能力 | 协议协商结果、AUT 动作授权、Dromen 会话上限，以及即时端点、预算、配额和输入都有效 | [能力发现、协商与调用](https://github.com/Noemion/noemion.github.io/blob/main/spec/capability-discovery-and-negotiation-proposal.md) |
| 多个候选分支正在并行 | 每个分支只取得 Dromen 的能力子集和预算份额；提交前重新核对对象身份、授权、协议和交付前提 | [并行、推测执行与提交](https://github.com/Noemion/noemion.github.io/blob/main/spec/parallel-and-speculative-execution-proposal.md) |
| 工作负载运行在容器或沙箱中 | 对模型输入、控制面、授权、凭据、实时句柄、文件、网络、资源终止、观察和外部目标分别记录强制机制与失败责任 | [模型、适配器与能力域隔离](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-adapter-isolation-proposal.md) |
| 模型评审给出分数 | 保留评测目的、构念、评分说明、题目、协议、原始输出、统计汇总和使用决定；模型结果只标为 `model-candidate` | [模型参与评测与裁判](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-assisted-evaluation-proposal.md) |
| 系统收到反馈 | 分开会话历史、检索、提示变化、反馈记录、训练数据、权重更新、评测、部署和回滚；只有来源、资格、用途和权威明确的反馈才可能成为训练输入 | [模型训练与更新](https://github.com/Noemion/noemion.github.io/blob/main/spec/model-training-and-update-boundaries-proposal.md) |

这些研究均为非规范材料，不创建新的 CORE、制品、服务或组件。发现能力不是调用授权；分支完成不是提交许可；容器边界不是完整隔离；模型分数不是目标满足；反馈记录也不是模型已经学习。

`krin`、验收策略、预算、停止条件和人工升级条件在运行前确定。Iknem 绑定事件、证据范围、对象身份、环境和策略。系统先区分 `met / unmet / agno / fault`，再由具名权威形成 `accepted / rejected / deferred`；Drase 会话另行记录 `completed / failed / interrupted`。这些结果不能互相替代。

若 `telis` 为 `mene`，时间范围还必须区分 `fixed` 确定 UTC 区间与 `elapsed` 具名事件经过时长。连续性使用 `strict` 或完整 `budgeted`；采样点之间没有覆盖保证时保持 `agno`，不能因为没有告警而推成 `met`。

否定目标仍使用同一关系、角色和顺序，只改变 `skena` 极性。查询未命中或日志为空默认保持 `agno`；只有具名权威证明有限观察范围完整封闭时，缺席才可支持 `met`。观察器故障为 `fault`，同构正反例为 `unmet`。

## 信任不是单一分数

每一步只增加特定范围的证据：来源、结构、语义、闭包、完整性、环境授权或验收。一个结构有效的 Endem 仍可能语义未确认；一个签名正确的 Synem 仍可能不适合当前策略；一个高质量模型候选仍不是 `accepted`。

| 接下来要解决的问题 | 继续阅读 |
| --- | --- |
| 想看完整责任链或 Agent 边界 | [完整生命周期](../architecture/endem-lifecycle.html) · [Agent 系统边界图](../architecture/agent-system-boundaries.html) |
| 想实现结果、时间或否定判断 | [结果分层决定](../architecture/adr-0015-result-domains.html) · [`mene` 时间决定](../architecture/adr-0016-mene-time-model.html) · [否定与缺席决定](../architecture/adr-0017-negation-and-absence.html) |
| 想定位组件责任或验证要求 | [组件职责](../components/) · [测试要求](../development/testing.html) |
