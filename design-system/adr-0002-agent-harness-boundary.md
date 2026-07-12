# ADR-0002：Agent Harness 的职责与信任边界

- 状态：Retained in part by ADR-0008
- 日期：2026-07-12
- 影响范围：组件、工具职责、开发工作流、测试与公开说明

## 问题

模型可以规划步骤、选择工具并根据反馈继续工作，但模型本身不能证明工具调用安全、结果正确或任务已经完成。只描述模型与对象格式，无法回答以下工程问题：

- 智能体从哪里取得当前任务所需的最小上下文；
- 哪些工具和数据可以访问，权限如何限制；
- 工具结果怎样回到下一步推理，而不依赖人工复制；
- 失败、预算耗尽、环境漂移和需要人工判断时怎样停止；
- 一次执行怎样留下可复查、可比较和可验收的证据。

## 决定

Noemion 引入 **Agent Harness** 作为 Fulfillment Runtime 外侧的控制平面。它负责装配上下文、暴露类型化能力、驱动观察—行动—验证循环，并把运行证据交给验收与审计工具。

Agent Harness 不属于确定性可信核心，也不是新的对象编译器。它必须遵守以下边界：

1. 模型只产生计划、候选参数和下一步建议；每次能力调用都由确定性策略检查。
2. 能力以最小、类型化、可发现的接口暴露；默认没有 Shell、网络、文件写入或凭据访问权。
3. 上下文按任务逐步披露；仓库内版本化资料是权威来源，临时对话不能静默覆盖规范。
4. 每次执行绑定对象、配置、工具、模型、环境和输入指纹，并记录调用、观察、拒绝与验收结果。
5. 验收契约、预算、停止条件和人工升级条件在执行前确定；模型不得自行宣告成功或扩大权限。
6. Agent Harness 不直接生成 NIR/NOBJ，不修改签名对象，不绕过 Noesis Core、对象验证或装载策略。

## 外部协议、结构化输出与遥测适配

MCP、A2A、供应商工具调用和结构化输出只作为 Agent Harness 外缘的互操作输入，不能定义 Noemion 内部能力、任务、事件或验收 ABI：

1. 适配器必须显式绑定协议版本，把远端 Tool、Agent Card、Task、schema 和结果翻译为 Noemion 自有的 Capability Catalog、Runtime Request、Capability Request/Observation、Evidence 与 Policy 结构。
2. 远端工具说明、行为注解、Agent Card、输出 schema 和模型生成参数均视为不可信声明。模式合法只证明结构，不证明参数授权、值语义、工具行为或结果正确。
3. Bearer token、刷新令牌、私钥和实时能力句柄不得进入模型上下文、NIR/NOBJ 或可重放 Trace。HTTP 适配器必须执行访问令牌 audience/resource 限制、token passthrough 禁止和 SSRF 防护；采用 OAuth Authorization Code Grant 时，public client 必须使用 PKCE，confidential client 按 RFC 9700 建议使用 PKCE。不得把只适用于授权码流程的 PKCE 错写成所有凭证模式的通用机制。
4. OpenTelemetry GenAI 等外部遥测语义只能由带版本、默认脱敏的导出器生成；Noemion 的稳定事件身份和最终决定不能依赖仍在演进的外部字段。
5. 协议缺失能力、版本不兼容或未知必需字段时关闭失败，不把降级后的远端任务状态静默映射为 Noemion 的 accepted、authorized 或 complete。

截至 2026-07-13，实施基线只把 MCP 2025-11-25 稳定版与 A2A 1.0（文档快照路径 v1.0.1）视为后续适配候选；第一阶段不引入任何外部智能体协议。MCP 2026-07-28 发布候选包含破坏性变化，正式发布并通过跨版本、恶意结构、重放、取消、幂等、权限代理混淆和令牌受众测试前不采用。A2A 补丁号不进入协议协商。

## 工具映射

- `noesis`：把受控来源或模型候选交给 Noesis Core，产生确定性对象与证据账本。
- `noemexecute`：驱动对象系统建立不可变 Loaded State，由 Harness 建立会话级能力绑定、预算与隔离环境，并调用 Runtime；运行阶段只留下候选和运行记录。
- `noemobserve`：把同一会话的能力调用、观察、策略拒绝和状态转换规范化为带完整性声明的 Trace。
- `noemcoverage`：分别检查发布来源映射和运行证据闭包；证据齐全不等于任务已经满足。
- `noemexecute finalize`：按执行前固定的 Acceptance Policy 和 Evidence Closure Report 形成最终 Acceptance Decision。
- `noemevaluate`：评估模型候选资格，也在 Acceptance Decision 之后离线评估完整任务场景；它不修改单次会话决定。

## 采用边界

本决定吸收智能体工程中“环境、工具和反馈回路比单次提示更重要”的经验，但不采用以下做法：

- 不把高吞吐量作为降低对象安全、确定性或发布检查的理由；
- 不把智能体自审视为独立验证；
- 不要求模型生成项目全部实现；
- 不假定某个代码仓库中的自治水平可以迁移到不同任务、权限和风险环境。

## 后果

Agent Harness 成为必要的逻辑控制边界，但不要求独立进程或单独部署：简单的确定性任务可以把最小 Harness 实现为 `noemexecute` 内部适配层；只有动态能力、多步观察或外部判断存在时才需要完整会话控制。后续规范必须分别冻结能力结构定义、执行配置、事件结构定义、上下文清单、策略拒绝、状态快照、Evidence Closure 和 Acceptance Decision；在这些契约形成前，不提供可执行程序或稳定 ABI。

## 依据

- OpenAI, “工程技术：在智能体优先的世界中利用 Codex”: https://openai.com/zh-Hans-CN/index/harness-engineering/
- MCP 2025-11-25 规范与工具安全边界：https://modelcontextprotocol.io/specification/2025-11-25 和 https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- A2A 1.0 规范，文档快照 v1.0.1：https://a2a-protocol.org/v1.0.1/specification/
- OAuth 安全与资源绑定：https://www.rfc-editor.org/info/rfc9700/、https://www.rfc-editor.org/rfc/rfc9728.html 和 https://www.rfc-editor.org/info/rfc8707/
- OpenTelemetry GenAI 语义约定（Development）：https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai
- OpenTelemetry GenAI 独立语义仓库：https://github.com/open-telemetry/semantic-conventions-genai
- JSON Schema 2020-12：https://json-schema.org/draft/2020-12
