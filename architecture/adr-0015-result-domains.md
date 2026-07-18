---
layout: architecture-decision
title: ADR-0015 · 五类结果不可互换
page_role: content
footer_text: Noemion · ADR-0015
permalink: "/architecture/adr-0015-result-domains.html"
summary: 区分制品状态、目标满足、权威决定、会话终止和证据状态，避免把工具或 Agent 的成功当成最终结论。
decision_id: ADR-0015
page_heading: ADR-0015 · 五类结果 · 不可互换
page_lead: 制品状态、目标满足、权威决定、会话终止和证据状态回答不同问题；外部智能体或运行器的“成功”不能跨层替代任何判断。
badges:
- 当前策略
- 结果域分离
- 不改变线格式
- 尚未实现
previous_url: adr-0014-source-manifest.html
previous_label: ADR-0014
next_url: adr-0016-mene-time-model.html
next_label: ADR-0016
---

## 用一次依赖升级看五类结果

“更新依赖并确认可以发布”至少会产生五类结果。它们可以同时成立，也可以各自失败。

1. 形成目标制品状态
2. 执行更新会话终止
3. 收集测试证据状态
4. 比较判据满足结果
5. 具名主体最终决定

| 事实 | 所属结果域 | 不能替代 |
| --- | --- | --- |
| END-P2 结构和引用通过检查 | 制品生命周期 | 实际环境可运行、目标满足或发布接受。 |
| 外部 Agent 报告 Task completed | 会话终止 | 依赖版本正确、测试充分或目标 `met`。 |
| 测试记录有效但漏掉生产平台 | 证据有效、覆盖不足 | `sufficient`、`met` 或 `accepted`。 |
| 全部固定判据得到适用证据支持 | 满足判断 | 发布主体已经作出接受决定。 |
| 发布负责人在适用政策下批准 | 权威决定 | 改写原满足结果、证据状态或会话历史。 |

## 五个结果域分别由谁产生

| 结果域 | 草案值 | 责任与对象 | 禁止提升 |
| --- | --- | --- | --- |
| 内容状态 | `formed / resolved` | 前者表示六项内容职责已经形成，后者表示内容中的待确认意义已经按适用规则处理。 | 不提升为外部陈述有效、运行准入、目标满足或最终接受。 |
| 满足判断 | `met / unmet / undetermined / fault` | 求值责任比较固定事态、判据和适用观察。 | 不提升为具名权威的最终决定。 |
| 权威决定 | `accepted / rejected / deferred` | 具名规则或主体消费满足结果、证据和政策。 | 不得回写或覆盖输入事实。 |
| 会话终止 | `completed / failed / stopped` | 运行责任说明一次会话怎样结束。 | `completed` 不等于 `met` 或 `accepted`。 |
| 证据状态 | `valid / invalid / revoked`<br>`sufficient / insufficient` | 验证责任分别判断记录有效性和证据集合覆盖度。 | 单份 `valid` 不等于整体 `sufficient`。 |

> **内容与外部关系分开：**`formed / resolved` 只描述内容。外部签名陈述、验证政策、截止点、撤销状态和依赖方判断必须分别记录，不能压成第三个内容状态。

这些普通英语机器标识已经通过词首、职责与关键字语料检查，不再设置完整人类读音门槛。它们仍只是设计值，不表示结果引擎已经实现。

## 满足结果为什么必须是四值

| 结果 | 何时产生 | 常见错误 |
| --- | --- | --- |
| 满足 `met` | 必需观察齐全、有效、适用，完整比较支持目标事态。 | 从工具成功、模型评分或 Task completed 推出。 |
| 未满足 `unmet` | 同样完成观察和比较，但结果反驳目标事态。 | 从无日志、超时、缺少权限或验证器崩溃推出。 |
| 未知 `undetermined` | 意义和判据确定，但观察缺失、过期、越界或覆盖不足。 | 用来保存语义歧义，或静默降成 `unmet`。 |
| 求值故障 `fault` | 规则、依赖、求值器或观察适配没有按声明契约完成。 | 把目标标成未满足，或用重试成功覆盖原故障。 |

每项结果必须绑定 Endem 身份、`satisfaction_criteria` 版本、观察截止点、实际使用的 evidence 和稳定原因。新观察或规则只能产生新结果，不能原地改写旧记录。

## 最终决定怎样消费而不改写满足结果

| 决定 | 最低条件 | 必须保留 |
| --- | --- | --- |
| 接受 `accepted` | `met`、必需 evidence 有效且覆盖充分，并有获授权决定。 | 输入满足结果、证据状态、决定规则、主体、范围和时间。 |
| 拒绝 `rejected` | 具名权威依据 `unmet` 或预先登记政策作出否定决定。 | 拒绝依据；证据不足不能自动写成目标为假。 |
| 延后 `deferred` | 尚无获授权决定，或未知、故障、人工判断和授权缺口未解决。 | 未决原因和恢复责任；不得当成隐式接受。 |

`met` 可以因额外政策被 `rejected` 或 `deferred`。`undetermined` 也可以按预先登记的关闭失败政策被拒绝；这仍不把未知观察改写成 `unmet`。

## 外部机制只能提供哪一层事实

| 外部机制 | 可带入的事实 | Noemion 不继承 |
| --- | --- | --- |
| [GNU Automake 测试](https://www.gnu.org/software/automake/manual/html_node/Generalities-about-Testing.html) | 测试通过、断言失败、跳过和测试环境硬错误是不同结果。 | PASS/FAIL/ERROR 名称和退出码不进入 Endem ABI。 |
| [MCP 工具](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 协议错误与工具执行错误保持可区分。 | 工具成功不产生 `met` 或动作授权。 |
| [A2A 1.0 Task](https://a2a-protocol.org/v1.0.0/specification/) | 完成、失败、拒绝、取消和等待状态属于外部任务生命周期。 | 任何 Task 状态都不能直接成为本地满足或最终决定。 |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | 实体、活动、主体、生成、使用和失效可以保持可追溯关系。 | 溯源关系本身不决定证据有效、覆盖充分或权威接受。 |

[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)截至复核日仍把 2025-11-25 列为 Current。协议版本或外部状态变化只要求适配器重新记录映射，不得覆盖本地结果域。

## 当前仍缺哪些可执行接口

现行十二个结果域向量覆盖允许与拒绝组合，只证明当前条款和案例矩阵一致。本决定不新增 END-P2 字段，也没有 runner、决定引擎、结果事件编码或组件测试。

结果事件的物理 Profile、时间域、重放键、聚合、会话恢复、决定类 evidence 和协议映射表仍待设计。缺少这些材料时只能依赖语义分层和禁止推导。

- [查看结果规范](../specifications/endem.html) — 按结果域查阅现行语义和禁止推导。
- [查看授权决定](adr-0029-authority-and-authorization-decisions.html) — 区分意义确认、动作授权和最终接受。
- [查看证据边界](../specifications/evidence-entry.html) — 理解有效性与覆盖度为什么必须分开。
- [查看 Agent 边界](agent-system-boundaries.html) — 沿一次外部调用定位每类状态。
