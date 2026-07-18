---
layout: content
title: 外部协议适配规范
page_role: content
footer_text: Noemion · External Protocol Adapters
permalink: "/specifications/adapters.html"
summary: 说明 Noemion 调用 MCP、A2A、HTTP 或模型服务时，哪些返回值可以记录，哪些身份、授权和目标结论仍须重新核对。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 外部协议适配
page_lead: 当 Noemion 通过 MCP、A2A、HTTP 或模型服务调用外部系统时，说明哪些信息可以带入，哪些远端说法必须留作待核对输入。
badges:
- ADP-CORE 0.1.0-draft
- 当前策略
- 物理格式不适用
- 尚无适配器
previous_url: diagnostics.html
previous_label: 结构化诊断
next_url: "../architecture/adr-0026-external-protocol-adapters.html"
next_label: ADR-0026
---

## 先看一次发布怎样调用外部系统

发布会话需要调用外部 Agent 或工具时，适配器只负责把一次已经受限的本地调用连接到精确协议操作，并把外部回应连同来源带回来。

1. 固定协议与对端
2. 能力与 contract 求交
3. 绑定本地调用身份
4. 执行外部操作
5. 保留原状态与损失
6. 本地观察和决定

| 调用阶段 | 开发者必须固定 | 信息不足时怎样停止 |
| --- | --- | --- |
| 发现与绑定 | 协议修订、绑定、传输、扩展、端点、认证主体、受众和租户 | 版本、对端或受众含糊时不得开始调用 |
| 发起调用 | 本地调用身份、精确输入、能力交集、预算、截止点、幂等分类和观察责任 | 外部 request、task、message 或 trace ID 不能替代本地调用身份 |
| 取得状态或产物 | 原协议状态、映射版本、信息损失、生产调用、媒体类型和内容身份 | 远端产物先成为有来源的不可信候选，不能直接成为目标、证据或接受结果 |
| 取消、断线或重试 | 取消请求、对端确认、后续观察、历史缺口、副作用未知区间、去重证据和剩余预算 | 断流不证明回滚；没有幂等或去重证据时停止自动重试 |

**协议状态不能越过本地判断：**A2A `completed`、HTTP 2xx、MCP ToolResult、模型停止原因或连接关闭只说明外部协议发生了什么。本地系统仍要分别核对精确身份、动作授权、evidence 覆盖、目标满足和最终接受。

> **当前策略：**`ADP-CORE 0.1.0-draft` 只定义协议无关的抽象责任。物理格式不适用，当前尚无适配器、协议 Profile、凭据代理、重试引擎或 runner 实现。

## 按十二项责任检查一次调用

| 规范责任 | 开发者必须固定 | 失败处理 |
| --- | --- | --- |
| `ADP-PIN-001`<br>版本与绑定 | 协议、规范、绑定、schema、传输和扩展版本 | 拒绝 `latest`、默认版本、未知扩展和兼容猜测 |
| `ADP-PEE-001`<br>对端与信任 | 发现来源、声明主体、端点、认证主体、受众、租户和政策 | Agent Card、工具清单或 TLS 连接不能自行授予身份和权限 |
| `ADP-CAP-001`<br>能力交集 | 协议、对端、适配器、contract 和政策的共同能力 | 遇到未知能力时拒绝继续，协商和错误建议不得扩大当前会话 |
| `ADP-INV-001`<br>调用语境 | 主体、输入、操作、预算、截止点、幂等分类和观察责任 | 外部 task 或 trace ID 不得替代本地调用身份 |
| `ADP-MAP-001`<br>映射损失 | 原协议事实、映射版本和有限损失清单 | 静默丢字段、降精度或伪造通用等价时映射无效 |
| `ADP-STA-001`<br>状态分离 | request、tool、task、message、artifact、HTTP 和 SDK 的原状态 | 外部状态不得直接提升为本地五类结果 |
| `ADP-ART-001`<br>候选产物 | 生产调用、对端、媒体类型、内容身份、大小和披露限制 | 远端名称、签名或完成状态不能直接形成可信对象 |
| `ADP-ERR-001`<br>错误来源 | 传输、协议、工具、任务、业务和本地错误层次 | 自由错误消息不得改变权限、结果域或重试策略 |
| `ADP-CAN-001`<br>取消与终态 | 取消请求、对端确认和后续观察三个事实 | 取消、超时或断流不能冒充副作用已经停止或回滚 |
| `ADP-RTY-001`<br>重试 | 幂等或去重证据、分类权威、预算、截止点和取消状态 | 结果不确定时不得自动重复非幂等副作用 |
| `ADP-DEL-001`<br>异步交付 | 授权、序列、去重、乱序窗口、缺口、终结条件和资源预算 | 流关闭、通知缺失或轮询超时不能冒充完成 |
| `ADP-SEC-001`<br>安全包络 | 凭据受众、网络目标、披露范围和资源上限 | 发现令牌透传、SSRF、跨租户枚举或无界保留时必须拒绝继续 |

## 遇到更强问题时再查外部资料

| 开发者问题 | 当前资料与机制 | Noemion 的使用边界 |
| --- | --- | --- |
| 协议基线怎样选择 | [MCP 版本说明](https://modelcontextprotocol.io/docs/learn/versioning)仍把 [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)列为 Current；[MCP 2026-07-28 发布候选](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)已锁定但计划 7 月 28 日才形成最终版。[A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)已发布，协议协商使用主次版本 `1.0`。 | **复核日期：**2026-07-16。固定正式修订、绑定和扩展；候选版只进入迁移研究，不能冒充当前符合性基线。 |
| 不同协议怎样映射 | [GNU BFD 信息损失说明](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)表明，统一内部形式无法穷尽所有外部格式，转换时可能没有位置保存原信息。 | 保留原协议身份、映射版本和有限损失清单；不得为了统一结构伪造无损等价。 |
| 何时可以重试或恢复 | [RFC 9110 幂等方法](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)限制非幂等自动重试；A2A 1.0 允许服务端返回少于请求上限的历史，并说明取消只是一项尝试。 | 旧 Task 句柄只帮助重新定位。恢复时重新核对对端、租户、当前授权、历史缺口和未知副作用；详细责任见[非规范恢复研究](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html)。 |
| 遥测字段能支持什么 | [OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)已把 GenAI 内容移到[独立仓库](https://github.com/open-telemetry/semantic-conventions-genai)；[复核快照 93a59e4](https://github.com/open-telemetry/semantic-conventions-genai/tree/93a59e48a9b4ea162a4d76edac4ace2d415a759e)公布了 [GenAI Schema URL 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0)。 | 研究材料同时固定仓库提交、Schema URL 和各字段稳定性；遥测不定义 evidence 身份、目标满足或最终接受。 |
| 能力、并行和隔离怎样接线 | [能力发现与协商](https://noemion.github.io/spec/capability-discovery-and-negotiation-proposal.html)、[并行与提交](https://noemion.github.io/spec/parallel-and-speculative-execution-proposal.html)及[模型与适配器隔离](https://noemion.github.io/spec/model-adapter-isolation-proposal.html)仍是非规范研究。 | 它们只路由更强问题，不修改 ADP-CORE，不创建能力制品、事务层、隔离规范或部署对象。 |

## 规范来源与当前上限

| 资料层级 | 当前覆盖 | 不能证明 |
| --- | --- | --- |
| [ADP-CORE 规范源](https://noemion.github.io/spec/adapter-core.html)与[威胁模型](https://noemion.github.io/spec/adapter-threat-model.html) | 定义十二项实现责任，并覆盖版本、身份、权限、副作用和安全威胁 | 具体协议映射、网络机制或安全控制已经实现 |
| [ADP-SCEN](https://noemion.github.io/spec/adapter-scenarios.html) | 覆盖支持案例、反例与边界条件 | 场景本身成为规范条款或协议互操作测试 |
| [ADP-CORE 向量](https://github.com/Noemion/noemion.github.io/tree/main/vectors/adapters) | 覆盖允许包络与确定拒绝，并与当前条款保持对应 | MCP、A2A、HTTP、SDK、适配器或 runner 已经实现 |

**待定内容：**当前没有具体协议 Profile。MCP、A2A、HTTP、模型 SDK 和操作系统调用的物理 Profile，JSON-RPC、Protocol Buffers、SSE 与 Webhook 字段映射，适配器 API、进程隔离、凭据代理、事件存储、重试实现和部署拓扑仍保持开放。

背景、权衡和权威资料见 [ADR-0026 · 远端完成，不等于本地完成](../architecture/adr-0026-external-protocol-adapters.html)。公开页面只提供开发者阅读路径，不建立第二套条款。
