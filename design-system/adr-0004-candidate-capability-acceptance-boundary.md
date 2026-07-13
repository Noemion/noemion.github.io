# ADR-0004：候选语义、能力调用与验收决定边界

- 状态：Retained in part by ADR-0010 and ADR-0015；旧对象、状态、结果集合与工具名称已废止
- 日期：2026-07-12
- 影响范围：Horizon Engine、Noesis Core、Noema Object System、Agent Harness、Fulfillment Runtime、运行与评估工具

## 问题

> 历史边界：本记录只保留“候选不等于事实、能力声明不等于句柄、证据不等于最终决定”。下文旧对象名、命令名和 `accepted/unsatisfied/pending-review/failed/interrupted` 混合结果集合均已失效；现行结果域以 ADR-0015 为准。

“模型候选通过类型检查”“Runtime 评价候选”和“运行证据覆盖契约”都不能单独证明任务已经正确完成。如果不区分候选升级、能力请求和最终验收，系统会留下三类危险空白：

- 模型生成的解释可能因为结构合法而被误当成忠实于来源的语义；
- Loaded State 中的能力声明可能被误当成模型或 Runtime 可以直接使用的实时权限；
- Runtime、Agent Harness、覆盖工具和评估工具可能分别宣告成功，没有唯一、可追溯的验收决定。

## 决定一：候选语义不能因结构合法自动升级

Horizon Engine 或外部模型只产生 **Candidate Envelope**。它必须绑定原始来源身份、精确跨度、候选解释、保留的替代项、证据、置信信息和未决状态，但它本身不是 NIR。

Noesis Core 只有在以下任一依据成立时，才能把候选主张写入规范化 NIR：

1. 主张可以由受控语法和版本化确定性规则从来源重新推导；
2. 主张绑定到经过授权、可追溯的 Source Binding Decision；
3. 主张以歧义、待确认或未解决状态进入 NIR，而不是被确认为事实。

类型、约束、覆盖和布局检查只能证明表示内部成立，不能证明自然语言解释忠实于来源。无法建立上述依据时，Noesis Core 必须拒绝编译或保留未决语义。

## 决定二：能力描述与实时句柄分离

- 签名对象和 Loaded State 只保存不可变的能力需求、参数结构、风险分类和授权上限，不保存可直接调用的实时句柄。
- Agent Harness 根据运行配置、当前环境和确定性策略建立会话级 Capability Binding，并持有实际句柄。
- Fulfillment Runtime 和模型只能返回类型化 Capability Request；Agent Harness 负责校验、执行或拒绝，再把 Capability Observation 返回会话。
- Runtime 不能直接访问 Shell、网络、文件、凭据或其他外部能力，也不能把一次会话的句柄带入另一会话。

## 决定三：评价、覆盖和最终验收分层

Noemion 把结果判断拆成三层：

1. **Candidate Assessment：**Fulfillment Runtime 判断候选是否通过当前评价器与硬约束检查，产物仍是不可信候选，不构成任务完成。
2. **Evidence Closure：**Agent Harness 汇总真实环境观察；`noemcoverage` 检查每个验收契约项是否有可定位证据。覆盖完整只说明证据齐全，不自动说明结论为真。
3. **Acceptance Decision：**Agent Harness 只能通过 `noemexecute finalize` 按执行前固定的 Acceptance Policy 形成最终状态。全部必需条款可判定、证据闭合且满足时才可标为 `accepted`；需要人工或外部判断时必须标为 `pending-review`，由配置指定的外部权威签署决定。

`noemevaluate` 产生模型或场景评估结论，用于基准、回归和发布判断，不修改单次会话的 Acceptance Decision。`noemcertify` 检查跨工具一致性，也不替代会话验收、发布授权或签名授权。

## 状态与证据

正式运行至少区分 `accepted`、`unsatisfied`、`pending-review`、`failed` 与 `interrupted`。Acceptance Decision 必须绑定对象、运行配置、环境、模型或求解后端、策略版本、证据闭包和决定权威；任何输入身份变化都使旧决定失效。

## 后果

所有组件页、工具页、架构图和手册必须使用同一边界：Candidate Envelope 不是 NIR，Capability Requirement 不是 Capability Handle，Candidate Assessment 不是 Acceptance Decision。新增评价器、能力或验收类型时，必须说明其权限、证据强度、失败语义和最终决定权威。
