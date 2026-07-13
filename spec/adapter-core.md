# External Protocol Adapter Core Specification

- 规范 ID：`ADP-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0026 已接受的 Praxor 外部协议适配边界
- 物理编码：未定义；本规范不创建适配器文件、扩展名、媒体类型、网络协议或稳定 ABI
- 实现状态：仅有规范提案向量检查器；MCP、A2A、HTTP、模型 SDK、工具和 Agent 适配器均未实现

## 1. 范围

本规范定义外部工具、Agent、模型服务、任务系统和网络协议进入 Praxor 边界时必须保持的不变量。它适用于 MCP、A2A、HTTP API、操作系统调用、模型 SDK 与未来协议，但不复制任何协议的数据模型，也不把某个协议设为 Noemion 的身份或权限来源。

协议适配只把一次已经受 Dromen 限制的调用连接到一个精确外部操作。它必须保留外部事实、声明映射损失、收窄能力、控制副作用，并把观察交给 Tekmor 与本地判断规则。适配层不是 Endem、Synem、Dromen、Tekmor、决定权威、凭据包、模型上下文或新的结果域。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

符合性声明 `MUST` 固定 `ADP-CORE`、DRO-CORE、DIA-CORE、AUT-CORE、适用对象规范和外部协议的精确版本。外部 scope、凭据、Agent 状态或 step-up 只能成为授权输入或上限，不能替代本地授权决定。当前没有 MCP 或 A2A Profile；JSON-RPC、HTTP、Protocol Buffers、SSE、Webhook 与 SDK 对象只是未来映射候选，不能自称为 Noemion 规范字节。

## 3. 适配内容

### ADP-PIN-001 — 协议版本与绑定必须精确固定

**要求：**每个适配绑定 `MUST` 固定协议身份、规范版本、协议绑定、schema 或接口版本、传输模式和已启用扩展。`latest`、自动升级、服务端默认、SDK 包版本和兼容猜测 `MUST NOT` 替代协议版本。版本或扩展变化 `MUST` 使原绑定失效并重新通过政策检查；候选版和实验扩展 `MUST` 明确标记，不能冒充稳定规范。

**失败：**同一配置随远端默认版本改变行为、MCP 候选版被当作稳定版、A2A 主次版本未固定，或未知扩展被静默接受时，适配不得开始调用。

**验证：**`ADP-SCN-001`、`ADP-SCN-002`；`vectors/adapters/cases.json`；未来 `peira:adapter-version-pin` 组件测试。

### ADP-PEE-001 — 对端声明不能替代对端身份与信任

**要求：**适配绑定 `MUST` 分开记录发现来源、声明主体、网络端点、已认证主体、租户或资源受众和政策决定。Agent Card、工具清单、模型名称、TLS 连接、签名或注册表条目只能成为声明证据；它们 `MUST NOT` 自动成为语义权威、能力授权或验收主体。端点重定向、DNS 或发现结果变化 `MUST` 重新核对身份与授权语境。

**失败：**适配器仅凭自报名称选择对端、把 Agent Card 中的技能当作已授权能力、跨租户复用远端任务 ID，或重定向后继续使用原受众令牌时，绑定无效。

**验证：**`ADP-SCN-003`、`ADP-SCN-004`；`vectors/adapters/cases.json`；未来 `peira:adapter-peer-binding` 组件测试。

### ADP-CAP-001 — 外部能力必须与 Dromen 求交

**要求：**可调用操作、输入输出媒体类型、流式、任务、回调、采样、文件、网络和其他功能 `MUST` 由“协议声明能力 ∩ 对端声明能力 ∩ 本地适配器能力 ∩ Dromen 能力 ∩ 当前政策”得到。缺失、未知或后来新增的能力 `MUST` 默认不可用。协议能力协商、工具注解和远端 scope 挑战 `MUST NOT` 扩大当前 Dromen；step-up `MUST` 形成新的授权决定和新会话。

**失败：**远端新增工具即可调用、MCP task capability 绕过本地政策、A2A streaming 声明自动打开网络回调，或错误建议触发当前会话扩权时，调用必须拒绝。

**验证：**`ADP-SCN-005`；`vectors/adapters/cases.json`；未来 `peira:adapter-capability-intersection` 组件测试。

### ADP-INV-001 — 每次外部调用必须绑定一次精确调用语境

**要求：**每次调用 `MUST` 绑定 Dromen 会话、调用身份、精确主体、对端绑定、操作、规范化输入身份、能力依据、预算、截止点、幂等分类和预期观察责任。外部 request、task、message、context 或 trace ID `MAY` 作为附加关联，但 `MUST NOT` 替代本地调用身份。调用身份 `MUST` 在重试、流式事件、回调和最终结果中保持可追溯。

**失败：**只用模型对话 ID 关联副作用、多个 Dromen 共用一个远端 task、重试产生无法区分的重复操作，或调用无法追溯到精确输入时，适配必须关闭失败。

**验证：**`ADP-SCN-006`；`vectors/adapters/cases.json`；未来 `peira:adapter-invocation-binding` 组件测试。

### ADP-MAP-001 — 映射必须保留原始事实并声明信息损失

**要求：**适配器 `MUST` 保存受披露约束的原始协议种类、字段身份、状态、错误、顺序和对端引用，并使用显式映射版本生成本地视图。无法无损表示的字段 `MUST` 进入有限损失清单，说明省略、合并、降精度或未知处理；适配器 `MUST NOT` 为追求统一结构而伪造等价。映射版本、原始身份和损失清单 `MUST` 可被 Tekmor 引用。

**失败：**MCP 与 A2A 的不同任务状态被折叠成一个 success 布尔值、时间或媒体类型精度被静默丢失、未知字段被删除却声称完整，或只保留本地对象而无法追溯原协议时，映射无效。

**验证：**`ADP-SCN-007`、`ADP-SCN-008`；`vectors/adapters/cases.json`；未来 `peira:adapter-loss-map` 组件测试。

### ADP-STA-001 — 外部状态必须与本地结果域分开

**要求：**外部 request、tool、task、message、artifact、HTTP 和 SDK 状态 `MUST` 保持在外部状态域。适配器 `MUST NOT` 把 `completed`、`failed`、`cancelled`、`rejected`、`input-required`、HTTP 成功或模型停止原因直接映射为满足、决定、Praxe 会话或证据结果。只有本地 `krin`、适用 Tekmor、会话规则和具名决定权威可以产生这些结果。

**失败：**A2A task completed 直接产生 `accepted`、MCP tool error 直接产生 `unmet`、HTTP 200 产生 Tekmor `valid`，或外部取消被当作 Praxe 已停止时，映射必须拒绝。

**验证：**`ADP-SCN-009`、`ADP-SCN-010`；`vectors/adapters/cases.json`；未来 `peira:adapter-result-separation` 组件测试。

### ADP-ART-001 — 外部消息与产物只能作为有来源候选

**要求：**外部文本、文件、结构化数据、Message、Artifact、ToolResult 和模型输出 `MUST` 视为不可信候选。适配器 `MUST` 绑定生产调用、对端、媒体类型、声明身份、内容身份或受限临时引用、大小、完整性状态和披露限制。远端名称、artifact ID、签名或完成状态 `MUST NOT` 使候选自动成为 Endem、Synem、Tekmor、规范来源、已验收输出或“最新”版本。

**失败：**远端 Artifact 直接替换已签制品、模型文本直接成为 Endem 字节、相同文件名覆盖本地接受版本，或未检查媒体类型和大小即进入观察路径时，候选必须隔离或拒绝。

**验证：**`ADP-SCN-011`、`ADP-SCN-012`；`vectors/adapters/cases.json`；未来 `peira:adapter-artifact-candidate` 组件测试。

### ADP-ERR-001 — 协议错误必须通过 DIA-CORE 保留来源

**要求：**传输、协议、输入验证、工具执行、远端政策、任务、业务和本地适配错误 `MUST` 分开，并按 DIA-CORE 生成诊断。机器映射 `MUST` 使用登记字段，不能解析自由消息；未知外部错误 `MUST` 保留原始版本和码并进入受限通用诊断。错误建议 `MUST NOT` 扩权、改变结果域或触发未授权副作用。

**失败：**JSON-RPC 错误与工具执行错误合并、A2A TaskNotFound 被解释为目标不存在、错误消息中的 permission 字样触发 step-up，或未知码降级为成功时，适配必须拒绝该解释。

**验证：**`ADP-SCN-013`；`vectors/adapters/cases.json`；未来 `peira:adapter-diagnostic-provenance` 组件测试。

### ADP-CAN-001 — 取消与终态不能伪造回滚或复活

**要求：**取消 `MUST` 记录为有身份的请求、对端确认和后续观察三个可分离事实。对端 `cancelled`、流关闭或本地超时 `MUST NOT` 单独证明远端副作用已停止、回滚或不可见。外部终态 `MUST` 按协议保持不可变；后续修订 `MUST` 建立新的本地调用，不得复活旧调用、旧 Dromen 或旧权限。

**失败：**发送取消即释放审计责任、任务终态后继续追加同一工作、断流被当作远端停止、或恢复日志重新创建旧会话能力时，生命周期处理无效。

**验证：**`ADP-SCN-010`、`ADP-SCN-014`；`vectors/adapters/cases.json`；未来 `peira:adapter-cancellation-finality` 组件测试。

### ADP-RTY-001 — 重试必须由幂等证据与预算共同允许

**要求：**每次调用 `MUST` 分类为 `read-only`、`idempotent`、`deduplicated` 或 `non-idempotent`，并固定分类权威。自动重试只允许前三类，且必须满足协议语义、去重键或事后核对、剩余 Dromen 预算、截止点和取消状态。传输失败、未收到响应、模型建议和 HTTP 方法名本身 `MUST NOT` 证明副作用未发生；自动重试失败后 `MUST NOT` 无限递归重试。

**失败：**连接断开后自动重复付款、没有去重依据却重放工具、每次重试生成新调用身份而隐藏重复，或轮询与重试不共享预算时，重试必须停止并升级复核。

**验证：**`ADP-SCN-015`、`ADP-SCN-016`；`vectors/adapters/cases.json`；未来 `peira:adapter-idempotent-retry` 组件测试。

### ADP-DEL-001 — 流式推送与轮询必须形成可审计交付证据

**要求：**流式事件、SSE、Webhook、推送通知和轮询 `MUST` 固定交付模式、授权语境、序列或版本权威、去重规则、最大乱序窗口、缺口处理、终结条件和资源预算。回调 `MUST` 重新认证并绑定原调用；重复、迟到、缺失和未知事件 `MUST` 显式处理。流关闭、最后一条消息、通知缺失或轮询超时 `MUST NOT` 单独证明操作完成。

**失败：**重复事件重复执行副作用、跨租户 Webhook 注入状态、缺失中间事件却声称完整、无限轮询，或流关闭直接产生本地 completed 时，交付视图不完整。

**验证：**`ADP-SCN-017`；`vectors/adapters/cases.json`；未来 `peira:adapter-delivery-evidence` 组件测试。

### ADP-SEC-001 — 凭据网络目标披露和资源必须最小化

**要求：**凭据 `MUST` 留在独立能力域，绑定明确受众、主体、scope、期限和本次会话；token passthrough、静态秘密嵌入 Agent Card/工具 schema/消息和跨对端复用 `MUST NOT` 允许。网络目标 `MUST` 经过 SSRF、重定向、Origin、DNS 变化和私有地址政策；输入、输出、历史、任务列表、回调和诊断 `MUST` 使用最小披露与有限大小、数量、并发、TTL、轮询和重试预算。

**失败：**上游令牌透传给下游、Webhook 指向本地元数据服务、列任务泄露其他租户、无限 TTL 保留敏感输出，或模型看到实时能力句柄时，适配必须关闭失败并按 DIA-CORE 报告。

**验证：**`ADP-SCN-004`、`ADP-SCN-018`；`vectors/adapters/cases.json`；未来 `peira:adapter-security-envelope` 组件测试。

## 4. 权威依据与采用边界

- 截至 2026 年 7 月 13 日，MCP 官方版本说明仍把 2025-11-25 标为 Current；其工具错误、授权受众、实验 Tasks 和能力协商为本规范提供反例与约束。官方于 5 月 21 日锁定并公开以计划最终发布日期命名的 2026-07-28 候选版，最终版计划于 7 月 28 日发布。候选版把协议核心改为无状态并把 Tasks 移到扩展，证明 Noemion 不能绑定握手、会话或任务的单一外部形态；它只作为版本漂移证据，不是当前符合性基线。
- A2A 1.0 的 Agent Card、Task、Message、Artifact、流式、推送、终态不可变和版本头适合跨 Agent 交换；它们不替代 Endem 身份、Dromen 权限、Tekmor 证据或决定权威。
- RFC 9110 规定只有具备幂等语义或能够证明原请求未应用时才适合自动重试；Noemion 进一步要求重试共享 Dromen 预算并保留调用身份。
- GNU BFD 明确说明不同格式经统一 canonical form 可能丢失信息；Noemion 因此要求保留协议来源与显式损失清单，而不是建立一个宣称无损的万能 Agent 对象。

## 5. 当前未定义

本规范不冻结 MCP、A2A、HTTP、模型 SDK 或操作系统 Profile，不定义 adapter API、进程模型、JSON/CBOR/Protocol Buffers 字段、网络端口、凭据代理、重试实现、事件存储、Webhook 服务、沙箱、遥测 schema 或部署拓扑。具体协议映射必须在稳定版本、真实消费者、独立威胁分析、正反向量和用户明确开启代码阶段后的实现证据共同支持时另行建立。
