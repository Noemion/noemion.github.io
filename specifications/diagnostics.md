---
layout: content
title: 结构化诊断规范 · Noemion
page_role: content
footer_text: Noemion · 结构化诊断规范
permalink: "/specifications/diagnostics.html"
summary: 说明处理目标失败时，怎样同时告诉开发者和程序检查了什么、失败在哪里、依据什么规则以及如何继续。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 结构化诊断 · 让人和机器理解同一失败
page_lead: 当处理目标的某一步停止时，分别告诉开发者和调用程序：检查了什么、失败发生在哪里、依据哪条规则，以及满足什么条件后才能继续。
badges:
- DIA-CORE 0.1.0-draft
- DIA-CAT
- 物理格式待定
- 尚无运行组件
previous_url: evidence-entry.html
previous_label: evidence entry
next_url: "../architecture/adr-0025-structured-diagnostics.html"
next_label: ADR-0025
---

## 先看一次发布为什么停止

服务发布请求已经送到外部系统，但连接在响应前中断。此时无法证明副作用是否发生；诊断只能说明本地为何停止、还缺什么材料，不能猜测发布成功，也不能自行再执行一次。

1. 固定实际调用
2. 记录失败来源
3. 选择主阻断诊断
4. 标记后续未执行
5. 限制披露与数量
6. 另行决定恢复

| 诊断内容 | 本例记录 | 开发者怎样使用 |
| --- | --- | --- |
| 稳定机器码与消息 | `adapter.retry.not_authorized`、主条款 `ADP-RTY-001`，另附可本地化说明 | 自动化依赖登记码和条款，不解析“超时”或“请重试”等措辞 |
| 生产语境 | 生产者、适配器版本、操作、精确发布输入、协议/Profile、DIA-CAT 版本和本次调用身份 | 防止把这次诊断缓存或套用到另一个输入和调用 |
| 层次、位置与执行范围 | `policy` 层、外部请求关联；重试检查后的步骤标为 `not-run` | 保留传输事实，同时区分“检查失败”和“尚未检查” |
| 主诊断与恢复分类 | 唯一主阻断诊断；`operator-review`，前置条件是取得去重或事后核对证据 | 当前不自动重试；恢复继续受 session contract 预算和具名授权约束 |
| 披露、预算与结果边界 | 公开消息脱敏，只保留有限相关项，不返回部分可信对象 | 诊断不产生 `unmet`、`accepted`、回滚完成或新的权限 |

**当前策略：**结构化诊断是一份有限、可定位、机器可读的失败说明。它可以帮助人和人工智能系统选择下一步，但不得替代目标结果、证据判断、最终决定、权限或自动修复命令。

## 诊断必须保持哪些边界

| 规则 | 开发者应做什么 | 必须拒绝什么 |
| --- | --- | --- |
| `DIA-IDN-001` | 把登记机器码、稳定标题和人类消息分开 | 程序解析消息、颜色或本地化措辞取得机器语义 |
| `DIA-PIN-001` | 固定生产者、操作、实际输入、规范/Profile/目录版本和本次发生 | 用文件名、当前目录、“latest”或模型会话名代替精确语境 |
| `DIA-LAY-001` | 保留来源、结构、语义、会话、证据、政策、协议和后端层次 | 把任一错误强制转换为目标、会话、证据或决定结果 |
| `DIA-LOC-001` | 使用有类型、有限且可安全显示的位置 | 越界范围、无限路径或未转义的外部文本进入终端和日志 |
| `DIA-PRI-001` | 按失败层、规则优先级、规范位置和机器码选择唯一主诊断 | 并发完成顺序、外部返回顺序、语言或模型判断改变主诊断 |
| `DIA-REC-001` | 恢复分类声明前置条件、影响范围并继续受会话预算约束 | 诊断不得授予权限、触发无限重试或直接执行具有副作用的修复 |
| `DIA-EXT-001` | 保留协议版本、远端主体、原始结构化状态和受限本地映射 | 未知外部码降级为成功，或消息文本改变本地结果 |
| `DIA-SEC-001` | 默认最小披露，并说明脱敏对定位和复现的影响 | 不保存令牌、私钥、cookie、能力句柄、未授权正文或跨租户数据 |
| `DIA-BND-001` | 用有限预算在分配前限制数量、深度、位置、消息、建议和总输出 | 诊断风暴、递归自报错误，或截断时丢失主诊断 |
| `DIA-ATM-001` | 阻断错误使本次操作原子失败，并把后续层标为 `not-run` | 同时返回部分可信对象、成功状态或可继续使用的内部引用 |

> **权威边界：**[DIA-CORE 条款源](https://noemion.github.io/spec/diagnostics-core.html)定义规范义务。公开说明只提供开发者检查顺序，不建立第二套诊断字段或失败语义。

## 不同输出怎样保留同一失败事实

| 输出或协议 | 可以承载什么 | 不能改变什么 |
| --- | --- | --- |
| CLI 与人类消息 | 按终端能力显示标题、位置、相关事件、转义内容和修复提示 | 颜色、语言、换行和措辞不能成为机器码、严重度或恢复权限 |
| [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) | 导出规则身份、物理或逻辑位置、相关位置和代码流 | 导出器不得重新分类主诊断，也不能表达 Noemion 的目标、能力或最终决定 |
| [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) | 在 HTTP 中分开问题类型、具体发生、状态提示、标题和详情 | `status` 只是 HTTP 信息；程序不得解析 `detail`，错误正文也不得泄露实现和隐私 |
| MCP 与 A2A | 保留协议版本、错误结构、远端主体，以及协议、工具执行、任务和业务来源 | 模型可用反馈修正候选参数，但消息、`isError` 或远端状态不能授权重试和改写本地结果 |
| 日志、遥测与持久记录 | 在具名 Profile 下保存允许披露的机器内容、关联身份、截断事实和损失 | 记录出口不得扩大正文披露、资源预算、保存期限或稳定 ABI |

[GNU GCC 诊断输出](https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html)允许同一诊断进入文本与 SARIF 等不同出口，说明呈现可以变化而核心问题保持关联。Noemion 只采用这种职责分离，不复制 GCC 选项、严重度或编译器数据模型。

## 规范来源与当前上限

截至 2026 年 7 月 16 日，MCP 仍把 [2025-11-25 工具规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)列入当前修订，并分开 JSON-RPC 协议错误与带 `isError` 的工具执行错误。[A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)仍是最新正式版，要求 JSON-RPC、gRPC 与 HTTP 绑定保留同一错误语义。这些协议规定外部错误怎样表达，不决定 Noemion 的失败层次、主诊断、恢复权限或结果域。

`DIA-CAT` 使用受影响对象或诊断系统作为机器码首段，例如 `endem.*`、`session.*` 与 `diagnostic.*`；Noemion 是项目品牌，不进入机器码。目录版本必须随诊断固定，当前机器码仍是草案接口，不是稳定 ABI。

- [DIA-CAT 诊断目录](https://noemion.github.io/spec/diagnostic-catalog.html) — 登记跨 Endem、Endem closure、session contract、evidence entry 与诊断系统自身的草案机器码。
- [诊断威胁模型](https://noemion.github.io/spec/diagnostic-threat-model.html) — 检查消息解析、状态洗白、主错误竞态、自动提权、泄密、风暴和部分成功。
- [设计场景](https://noemion.github.io/spec/diagnostic-scenarios.html) — 用支持案例、反例和边界场景检查失败责任；场景不是实现或符合性声明。
- [结构化诊断提案向量](https://github.com/Noemion/noemion.github.io/tree/main/vectors/diagnostics) — 检查允许包络与确定拒绝；向量不证明诊断系统已经实现。
- [ADR-0025](../architecture/adr-0025-structured-diagnostics.html) — 说明跨对象诊断、确定主错误和最小披露的背景与采用限制。

**待定内容：**诊断 JSON、CBOR、SARIF、Problem Details、JSON-RPC、MCP、CLI 文本和退出状态映射，以及持久日志、遥测、跨进程关联、堆栈和修复补丁格式都保持开放。当前没有诊断生产器、渲染器、日志服务、重试引擎、协议适配器或 CLI。
