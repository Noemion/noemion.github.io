---
layout: spec
title: "Diagnostic Core Specification · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/diagnostics-core.html"
summary: "规定诊断至少要说明哪个操作检查哪个输入、为何失败、发生在哪里，以及满足什么条件后才能继续。"
document_status: "规范草案"
---
# Diagnostic Core Specification

- 规范 ID：`DIA-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0025 已接受的跨对象诊断内容边界
- 物理编码：未定义；本规范不创建诊断文件格式、扩展名、媒体类型或稳定 ABI
- 实现状态：仅有规范提案向量检查器；诊断生产器、渲染器、SARIF/HTTP/MCP 适配器和 CLI 均未实现

## 1. 范围

本规范定义 producer、inspector、runner、`endem` 动作以及未来协议适配器产生的诊断至少必须保留哪些机器可读内容。它覆盖 Endem、closure、contract、evidence、来源清单、物理容器、政策、后端和外部协议，但不改变这些对象自己的规范与结果域。

诊断回答“哪个操作在检查哪个精确输入时，因哪条规范、哪个位置和什么可恢复条件停止或提示”。诊断不是 Endem、evidence、满足结果、最终决定、run 会话结果、权限、重试命令或实现堆栈。诊断可以被后续 evidence 引用，但它的存在、数量或严重度不能证明目标满足、证据充分或决定已经获得授权。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

符合性声明 `MUST` 固定 `DIA-CORE`、适用对象规范和诊断目录的精确版本。当前没有物理诊断 Profile；文本、JSON、SARIF、RFC 9457 Problem Details、JSON-RPC 或 MCP 结果都只是未来呈现或传输候选，不能自称为规范诊断字节。

## 3. 诊断内容

### DIA-IDN-001 — 机器身份与人类消息必须分开

**要求：**每项诊断 `MUST` 使用已登记且在目录版本内唯一的机器码，并绑定短稳定标题。人类消息、颜色、语言、换行、建议和本地化 `MUST` 只作为呈现；消费者 `MUST NOT` 解析消息文本来决定错误类别、权限、重试或结果。呈现器 `MUST NOT` 改写机器码、规范层次和阻断状态。

**失败：**只有自由文本、同一码表示多个不相容原因、消息措辞变化导致自动化行为改变，或 SARIF/HTTP/MCP 适配器重新分类诊断时，该诊断无效。

**验证：**`DIA-SCN-001`、`DIA-SCN-002`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-identity-rendering` 组件测试。

### DIA-PIN-001 — 诊断必须固定生产语境

**要求：**每项诊断 `MUST` 绑定生产者身份与版本、操作或动作、实际输入的精确身份或受限临时引用、适用规范/Profile/目录版本，以及能够区分本次发生的关联身份。路径、显示名、当前目录、模型会话名和“最新规范” `MUST NOT` 替代这些绑定。发生时间、线程号和随机关联值 `MUST NOT` 进入机器码或规范结果身份。

**失败：**无法判断哪一版规则检查了哪个输入、缓存诊断被复用到不同字节、或时间与随机值改变同一输入的主诊断时，诊断不可作为可靠自动化依据。

**验证：**`DIA-SCN-003`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-context-pin` 组件测试。

### DIA-LAY-001 — 失败层次与结果域必须正交

**要求：**诊断 `MUST` 明确属于 `source`、`structure`、`profile`、`semantic`、`closure`、`session`、`evidence`、`policy`、`protocol`、`backend` 或 `internal` 之一，并记录实际执行到哪一层。协议错误、工具执行错误、后端失败、政策拒绝和规范拒绝 `MUST` 保持来源层次。诊断 `MUST NOT` 自动映射为 `met/unmet/undetermined/fault`、`accepted/rejected/deferred`、`completed/failed/stopped`、evidence 有效性或覆盖度。

**失败：**MCP `isError` 被解释为目标 `unmet`，HTTP 状态被解释为权威拒绝，解析失败被解释为 `fault` 求值结果，或会话失败覆盖原满足判断时，映射必须拒绝。

**验证：**`DIA-SCN-004`、`DIA-SCN-005`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-layer-result-separation` 组件测试。

### DIA-LOC-001 — 位置必须类型化、有界且可安全显示

**要求：**诊断位置 `MUST` 使用适合其层次的类型化位置：来源范围、字节范围、记录身份、语义路径、图路径、会话绑定、证据引用或外部请求关联。范围端点、路径深度和字符串长度 `MUST` 在读取与分配前受限；攻击者控制的文件名、终端控制字符、URL、提示正文和外部消息 `MUST` 转义或省略。缺少安全位置时 `MAY` 只报告精确主体和条款，不得伪造位置。

**失败：**位置越界、路径遍历或控制字符进入终端、未检查范围触发大分配，或任意外部文本被当作语义路径时，诊断生成必须关闭失败。

**验证：**`DIA-SCN-006`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-location-bounds` 组件测试。

### DIA-PRI-001 — 主诊断选择必须确定且可解释

**要求：**一个失败操作 `MUST` 产生且只产生一个主阻断诊断。主诊断按“最早安全失败层 → 对应规范列出的优先级 → 规范位置顺序 → 稳定机器码”确定；线程完成顺序、哈希遍历、外部返回顺序、消息语言和模型判断 `MUST NOT` 参与选择。相关诊断 `MAY` 附加，但必须保持父子关系、稳定顺序和有限数量。

**失败：**同一输入在重复运行中得到不同主码、最后到达的 Agent 错误覆盖更早结构失败，或诊断数量改变主诊断时，结果不确定。

**验证：**`DIA-SCN-007`、`DIA-SCN-008`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-primary-determinism` 组件测试。

### DIA-REC-001 — 恢复建议不能成为权限或无限重试

**要求：**恢复分类只允许 `fix-input`、`refresh-binding`、`obtain-authority`、`retry-transient`、`operator-review` 或 `do-not-retry`。建议 `MUST` 声明前置条件和影响范围；重试必须受 contract 预算与取消约束。诊断及其建议 `MUST NOT` 授予能力、关闭 `unresolved_meaning`、修改已签制品、自动批准 step-up、跳过未执行层或命令模型执行具有外部副作用的修复。

**失败：**权限拒绝触发自动提权、相同确定性输入被无限重试、模型依据自由文本执行删除或发布，或“可重试”被解释为会话可以继续时，恢复关系无效。

**验证：**`DIA-SCN-009`、`DIA-SCN-010`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-recovery-authority` 组件测试。

### DIA-EXT-001 — 外部错误必须保留来源并经过本地映射

**要求：**来自 HTTP、JSON-RPC、MCP、A2A、操作系统、模型 SDK 或后端的错误 `MUST` 保留协议版本、远端主体、操作、原始结构化状态和本地映射码。适配器 `MUST` 区分传输、协议、工具执行、业务、政策和本地语义失败；未知外部码 `MUST` 保持未知或进入受限通用码。自由消息、退出码 `0/1` 和远端严重度 `MUST NOT` 单独决定本地语义。

**失败：**远端文本通过字符串匹配变成 `accepted` 或 `unmet`、协议错误冒充工具业务错误、未知码降级为成功，或本地码隐藏原始来源时，映射必须拒绝。

**验证：**`DIA-SCN-004`、`DIA-SCN-011`；`vectors/diagnostics/cases.json`；未来 `conformance:external-error-provenance` 组件测试。

### DIA-SEC-001 — 诊断默认最小披露

**要求：**诊断 `MUST` 只披露定位、修复和审计所需信息。Bearer token、私钥、cookie、能力句柄、未授权提示、完整环境、用户隐私数据、任意栈内存和原始外部正文 `MUST NOT` 进入默认诊断。省略或脱敏 `MUST` 标明所用政策及其对定位、复现和覆盖的影响；高权限调试材料必须留在不同访问域。

**失败：**工具返回中的令牌被回显、堆栈或路径泄露租户数据、脱敏删除决定性身份却仍声称可复现，或调试开关静默扩大公开披露时，诊断不符合要求。

**验证：**`DIA-SCN-012`、`DIA-SCN-013`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-minimal-disclosure` 组件测试。

### DIA-BND-001 — 诊断生成必须有有限预算

**要求：**每个诊断 Profile `MUST` 限制诊断数量、因果深度、位置数量、消息字节、外部正文、建议数量和总输出字节，并在相应分配前检查。达到上限时生成器 `MUST` 保留主诊断、记录截断事实并停止扩展；它 `MUST NOT` 递归格式化自身失败或让错误报告消耗不受限资源。

**失败：**循环图产生无限错误、一个恶意输入放大为无界消息、诊断截断删除主码，或报告器故障递归产生新诊断时，生成器必须原子关闭。

**验证：**`DIA-SCN-008`、`DIA-SCN-014`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-budget` 组件测试。

### DIA-ATM-001 — 阻断诊断不得伴随部分可信成功

**要求：**阻断诊断出现时，相关操作 `MUST NOT` 产生部分可信 Endem、closure、contract、evidence、签名请求、权限、可被下游当作检查已经通过的内部引用或成功状态。未执行层 `MUST` 明确为 `not-run`；可安全取得的只读观察只能作为非权威附属信息。警告和注记也 `MUST NOT` 提升对象状态或掩盖阻断错误。

**失败：**读取器在报错后返回可继续使用的对象、runner 在政策错误后保留能力、部分 closure 被标为完整，或“同时有成功和错误”被自动化解释为成功时，操作必须拒绝。

**验证：**`DIA-SCN-015`；`vectors/diagnostics/cases.json`；未来 `conformance:diagnostic-atomic-failure` 组件测试。

## 4. 适配边界

- GNU GCC 的文本与 SARIF 输出说明同一诊断可以拥有多个呈现出口；Noemion 采用“机器内容与呈现分离”，不复制 GCC 选项或把 SARIF 作为核心格式。
- SARIF 的规则身份、位置和相关位置适合未来静态检查导出；它不能表达 Noemion 的权限、满足或决定语义。
- RFC 9457 的问题类型、具体发生与人类详情分离适合未来 HTTP 适配；其 HTTP `status` 不能代替本地层次和主码。
- MCP 区分 JSON-RPC 协议错误与 `isError: true` 的工具执行错误；runner 外缘必须保留这一区分，再映射到本地诊断，而不是让模型依据消息文本改写目标结果。

## 5. 当前未定义

本规范不确定诊断 JSON、CBOR、SARIF、Problem Details、JSON-RPC 或 CLI 文本编码，不定义进程退出状态、颜色、终端布局、网络媒体类型、持久日志、遥测 schema、堆栈格式、修复补丁语法或跨进程关联协议。它们必须由真实消费者、独立 ADR、威胁分析、正反向量与实现证据共同支持后才能进入稳定接口。
