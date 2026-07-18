---
layout: architecture-decision
title: ADR-0026 · 远端完成，不等于本地完成
page_role: content
footer_text: Noemion · ADR-0026
permalink: "/architecture/adr-0026-external-protocol-adapters.html"
summary: 说明 MCP、A2A、HTTP 和模型服务的远端结果怎样保留来源，并与本地身份、授权、证据和目标判断分开。
decision_id: ADR-0026
page_heading: ADR-0026 · 远端完成 · 不等于本地完成
page_lead: MCP、A2A、HTTP 和模型服务只报告自身发生的调用、状态与产物。适配器必须保留这些事实的来源，再由 Noemion 独立核对身份、权限、证据、目标结果和最终决定。
badges:
- 当前策略
- ADP-CORE 0.1.0-draft
- 协议无关
- 尚无适配器
previous_url: adr-0025-structured-diagnostics.html
previous_label: ADR-0025
next_url: adr-0027-exact-identity-and-attestation.html
next_label: ADR-0027
---

## 用一次外部发布调用理解适配边界

一次受限发布会话需要调用外部 Agent。适配器负责把已经受 session contract 限制的本地操作映射成精确协议调用，并把远端回应、状态变化和候选产物连同来源带回来；它不替本地系统解释“发布是否完成”。

1. 固定协议版本绑定与扩展
2. 核对对端身份受众和租户
3. 求能力交集绑定本地调用
4. 执行外部协议操作
5. 保留原状态产物与损失
6. 形成观察再作本地判断

| 调用阶段 | 开发者必须固定 | 信息不足时怎样停止 |
| --- | --- | --- |
| 发现与绑定 | 协议修订、绑定、传输、schema、扩展、端点、声明主体、认证主体、受众和租户 | 版本、对端、受众或租户含糊时不开始调用；Agent Card 和工具清单只作为声明 |
| 限定能力 | 协议、对端、适配器、session contract 和政策共同允许的能力交集 | 未知能力关闭失败；协商结果和错误建议不得扩大当前会话 |
| 绑定调用 | 本地调用身份、精确输入、预算、截止点、幂等分类和观察责任 | 外部 request、task、message 或 trace ID 不能替代本地身份 |
| 接收回应 | 原协议状态、错误来源、映射版本、信息损失、候选产物身份和生产调用 | 远端名称、签名、成功消息或完成状态不能直接形成可信对象 |
| 本地判断 | evidence entry 覆盖、目标满足、会话状态和具名权威决定 | 任何外部状态都不能越过这些独立结果域 |

适配器因此是一个受限翻译边界，不是 Endem、Endem closure、session contract、evidence entry、凭据包、模型上下文或新的结果域。

## 协议版本、对端和能力必须同时固定

| 绑定 | 最低要求 | 为什么不能省略 |
| --- | --- | --- |
| 协议与扩展<br>`ADP-PIN-001` | 协议 ID、精确修订、稳定性、绑定、schema、传输和扩展集合 | `latest`、默认 SDK 行为和未知扩展会静默改变消息与生命周期语义 |
| 对端与信任<br>`ADP-PEE-001` | 发现来源、声明主体、认证主体、端点、受众、租户和适用政策 | TLS 连接、自报名称、Agent Card 或工具列表都不自动取得本地身份和权威 |
| 能力交集<br>`ADP-CAP-001` | 协议、对端、适配器、session contract 和政策能力的严格交集 | 能力取并集会把发现、支持和授权混成同一件事 |
| 调用语境<br>`ADP-INV-001` | 本地主体、精确输入、操作、预算、截止点、幂等分类和观察责任 | 远端 ID 只能关联外部发生，不能成为本地调用或证据身份 |

截至 **2026-07-16**，[MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)列为 Current。官方在 **5 月 21 日**公开并锁定了以计划最终日期命名的 [2026-07-28 候选版](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)；它改变了握手、会话、扩展和 Tasks 边界，但尚未成为当前规范，因此不作为当前符合性基线。

候选版证明协议层会发生实质变化，却不要求 Noemion 提前实现候选字段。未来每个协议 Profile 都必须绑定稳定修订、传输、扩展和真实消费者；迁移研究与现行符合性必须分开。

## 远端对象和本地结果怎样保持分离

| 外部事实 | 本地可以保存 | 不能直接提升为 |
| --- | --- | --- |
| A2A Task `completed` | 精确 A2A 版本、Task 身份、终态、历史范围和远端主体 | 目标 `met`、最终 `accepted` 或 Drase `completed` |
| MCP ToolResult | 工具身份、调用关联、内容、结构化状态和对端来源 | 可信 evidence entry、正确 Endem 或已获授权的外部副作用 |
| MCP 协议错误或工具执行错误 | 各自原始层次、机器码、结构化内容和受限本地映射 | 目标 `unmet`、证据 `invalid` 或永久不可重试 |
| HTTP 2xx 或模型 stop reason | 传输状态或供应商按自身规则结束生成的事实 | 内容正确、观察充分、目标实现或权威接受 |
| 远端 Artifact、Message 或资源 | 生产调用、对端、媒体类型、内容身份、大小和披露限制 | Endem、evidence entry、签名证明或本地身份 |

[GNU BFD 信息损失说明](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)指出，共同内部形式无法穷尽所有外部对象格式，转换时可能没有位置保存原信息。协议适配必须保留原协议事实、映射版本和有限损失清单；通用 `success=true` 或统一状态枚举不能冒充无损等价。

远端候选产物只有经过内容身份核对、独立验证和证据范围评估后，才可能进入后续流程。适配器保存来源，不负责把候选升级为可信对象。

## 取消、断线和重试为什么不能洗掉副作用

发送取消、收到取消确认、观察到远端停止和证明副作用已经回滚，是四个不同事实。连接关闭或轮询超时也只表示本地暂时失去观察，不证明远端操作没有发生。

| 情况与条款 | 允许继续的证据 | 必须停止自动处理的情况 |
| --- | --- | --- |
| 取消与终态<br>`ADP-CAN-001` | 分别保存取消请求、对端确认、后续观察和不可变终态 | 只有断流、超时或确认文本，却声称远端已经停止、回滚或不可见 |
| 只读重试<br>`ADP-RTY-001` | 操作经具名规则判为安全只读，且截止点、取消状态和共享预算仍有效 | 分类权威缺失，或重试会读取不同语境而未重新绑定 |
| 幂等重试<br>`ADP-RTY-001` | 协议语义、精确输入和调用身份共同证明重复应用效果不变 | 仅因 HTTP 方法名、SDK 默认或模型建议就认定幂等 |
| 去重重试<br>`ADP-RTY-001` | 稳定去重键、对端承诺和原调用应用状态核对 | 无法确认原调用是否已经应用，或新尝试逃逸原预算 |
| 流、Webhook 与轮询<br>`ADP-DEL-001` | 授权上下文、序列权威、去重、乱序窗口、缺口策略、终结证据和资源上限 | 流关闭、通知缺失、历史截短或一次轮询超时被写成完成 |

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)只允许客户端在知道请求语义幂等，或能够检测原请求从未应用时自动重试非幂等请求。Noemion 还要求所有尝试共享原本地调用身份、session contract 预算、截止点和取消状态；递归重试不能重置任何上限。

## 网络与凭据安全必须在映射之外关闭

| 攻击面 | 未来实现必须固定 | 关闭失败条件 |
| --- | --- | --- |
| 凭据与受众 | 凭据留在独立能力域，绑定主体、资源受众、scope、期限和本次会话 | 上游令牌透传下游，或静态秘密进入 Agent Card、工具 schema、消息、日志和诊断 |
| 端点与重定向 | 每次连接和重定向重新核对 scheme、host、port、Origin、DNS 结果与私有地址政策 | 用户可控 URL、重定向或 DNS 重绑定绕过网络目标限制 |
| 多租户与发现 | 发现结果、列表、缓存和回调都绑定认证主体、租户、受众与披露政策 | 跨租户枚举、共享缓存泄漏或未授权的工具与资源元数据 |
| 输入与资源 | schema 深度、消息大小、流长度、历史、重排、并发、回调和保留期限上限 | 外部 schema、消息、流或递归 Agent 调用产生无界解析、存储和费用 |
| 外部状态与诊断 | 结构化来源、最小披露和未知码保留 | 字符串匹配改变授权、结果或重试，或原始响应泄露秘密与提示正文 |

[MCP 安全实践](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)明确禁止令牌透传，并要求会话标识不能替代认证。Noemion 采用这些风险边界，但不把 OAuth、MCP Session ID、A2A Task ID 或 TLS 连接本身视为本地身份和权限证明。

## 当前还不能承诺哪个协议 Profile 或适配器

本决定建立 `ADP-CORE 0.1.0-draft` 的协议无关边界。十二项条款、十二类威胁、十八个设计场景，以及十二个允许包络和十二个确定拒绝向量只检查资料一致性；当前没有协议 Profile、适配器 API、网络服务、凭据代理、重试引擎、Webhook 服务、事件存储或 bounded runner 实现。

MCP、A2A 1.0、HTTP、模型 SDK 和操作系统调用仍需各自的物理 Profile，明确字段映射、稳定版本、认证、能力、错误、取消、重试、交付、损失和降级行为。没有真实消费者、威胁证据和互操作测试时，不冻结 JSON-RPC、Protocol Buffers、SSE、Webhook 或 SDK 数据结构。

> **名称与口头边界：**面向开发者先说“外部协议适配器”，再给出 `ADP-CORE` 条款编号。口头交流必须带协议域，例如“A2A Task”“MCP 工具结果”“HTTP 传输状态”和“Noemion 目标结果”；不要只说“任务完成”“工具成功”或“适配成功”。`ADP` 是机器规范 ID，不承担发行读音名称。

- [查看外部协议适配开发者规范](../specifications/adapters.html) — 按十二项责任检查一次受限调用。
- [查看一次会话权限边界](adr-0024-dromen-session-contract.html) — 理解调用能力、预算和实时凭据怎样收窄。
- [查看结构化诊断边界](adr-0025-structured-diagnostics.html) — 区分协议错误、工具错误与本地结果。
- [查看权威与授权决定](adr-0029-authority-and-authorization-decisions.html) — 核对对端身份、能力声明和本地授权。
