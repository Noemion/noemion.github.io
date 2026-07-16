---
layout: spec
title: "Synem Core Specification · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/synem-core.html"
summary: "版本化规范源，记录条款、责任、成熟度与验证边界。"
---
# Synem Core Specification

- 规范 ID：`SYN-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0021 已接受的组合闭包与条件激活边界
- 物理编码：未定义；本规范不创建 Synem 文件格式、扩展名、魔数或稳定 ABI
- 实现状态：仅有规范提案向量检查器；Ktisor、Theor、Drasor 与 CLI 均未实现

## 1. 范围

本规范定义两个或更多 Endem 怎样形成一个可重放的组合闭包，以及依赖、权限、成员结果和会话期条件激活必须保持的边界。它约束未来 `pleko`、制品形成侧读取器、独立 Theor、Drasor 与规范向量，但不规定物理容器、版本范围语法、远程仓库协议、符号表、动态链接或执行调度。

Synem 不是文件列表、目录扫描结果、对话上下文、模型记忆或运行时发现的工具集合。一个符合本规范的闭包不能因当前目录、搜索路径、网络“最新版本”、区域设置、模型选择或会话中的动态工具发现而改变。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

符合性声明 `MUST` 固定 `SYN-CORE`、精确版本以及每个成员使用的 END-CORE、END-FMT 和 Profile 身份。当前没有 Synem 物理 Profile，因此任何工具都不得声称产生稳定 Synem 字节。

## 3. 组合闭包

### SYN-CLS-001 — 闭包必须完整且至少包含两个不同 Endem

**要求：**Synem `MUST` 包含至少两个按精确内容身份区分的 Endem。闭包 `MUST` 包含所有种子成员以及经必需依赖关系可达的全部传递成员；成员和关系必须共同得到完整描述。文件列表、目录内容、未解析名称或运行时临时补入对象 `MUST NOT` 被称为 Synem 闭包。

**失败：**只有一个不同成员、必需传递成员缺失、闭包外仍存在必需引用，或相同身份被重复伪装成多个成员时，形成操作必须原子拒绝。

**验证：**`SYN-SCN-001`、`SYN-SCN-002`；`vectors/synem/cases.json`；未来 `conformance:synem-complete-closure` 组件测试。

### SYN-RES-001 — 每个必需引用必须得到唯一且可重放的精确绑定

**要求：**每个必需引用 `MUST` 解析为恰好一个允许的内容身份，并固定适用规范、Profile、引用方、被引用方与解析依据。解析 `MUST` 与输入顺序无关；名称、版本范围、路径或仓库位置只能帮助定位候选，不能替代精确内容身份。当前目录、环境搜索路径、网络“最新版本”、模型推荐、区域设置和运行时工具列表 `MUST NOT` 成为正式解析输入。

**失败：**引用缺失、歧义、指向冲突身份、依赖未登记环境，或同一正式输入因成员顺序改变而得到不同闭包时，形成操作必须原子拒绝，且不得输出部分可信 Synem。

**验证：**`SYN-SCN-003`；`vectors/synem/cases.json`；未来 `conformance:synem-exact-binding` 组件测试。

### SYN-GRF-001 — 依赖图必须有限无环且可选项不能削弱要求

**要求：**第一阶段必需依赖图与会话激活图 `MUST` 有限、无环并遵守显式资源预算。可选依赖 `MUST` 声明缺失时的可观察行为；缺失 `MUST NOT` 改写成员语义、删除 `apor`、降低 `krin`、满足必需引用或扩大权限。若不能证明缺失分支保持这些不变量，该依赖 `MUST` 归类为必需项。

**失败：**出现循环、未受限遍历、可选项承担必需语义，或缺失分支让目标更容易满足时，形成操作必须拒绝。

**验证：**`SYN-SCN-004`、`SYN-SCN-005`；`vectors/synem/cases.json`；未来 `conformance:synem-bounded-graph` 组件测试。

### SYN-AUT-001 — 权限只能通过交集与显式收紧收敛

**要求：**Synem 的能力上限 `MUST` 由成员上限、组合策略与会话政策的交集形成。成员的能力需求只是请求，不是授权；依赖、激活、满足、签名或外部 Agent 的能力声明 `MUST NOT` 扩大任何成员或整个闭包的权限。互相冲突且无法同时满足的能力边界 `MUST` 关闭失败。

**失败：**采用并集、继承最宽成员权限、因某成员需要网络而向全部成员授予网络，或由激活结果直接创建句柄时，形成或会话准备必须拒绝。

**验证：**`SYN-SCN-006`；`vectors/synem/cases.json`；未来 `conformance:synem-authority-intersection` 组件测试。

## 4. 成员结果与条件激活

### SYN-STA-001 — 成员结果保持各自身份且不得伪造总体结果

**要求：**每个 Endem 的生命周期、`met/unmet/agno/fault`、`accepted/rejected/deferred`、会话终止和 Iknem 状态 `MUST` 保持成员身份与原结果域。Synem `MUST NOT` 因一个成员 `met`、`accepted` 或 `completed` 而产生隐式的总体 `met`、`accepted` 或 `completed`。任何闭包级发布或运行决定 `MUST` 使用另行具名的策略、成员集合、截止点与决定权威，并保留全部成员依据。

**失败：**成员结果被折叠为一个布尔值、会话成功冒充目标满足、签名或证据数量冒充接受，或未给聚合策略却发布总体结果时，该结果无效。

**验证：**`SYN-SCN-007`；`vectors/synem/cases.json`；未来 `conformance:synem-member-result-separation` 组件测试。

### SYN-ACT-001 — 条件激活必须使用独立状态并保持固定闭包

**要求：**形成时条件若决定成员是否进入闭包，`MUST` 在 Synem 身份形成前解析，并改变闭包身份。会话期条件只能针对固定闭包中的成员，并 `MUST` 引用具名成员、精确结果事件、结果域、期望值、截止点与授权策略。会话期激活只允许 `active`、`inactive`、`unresolved` 或 `error`：条件匹配为 `active`，确定不匹配为 `inactive`，依据尚不可用为 `unresolved`，检查契约失败为 `error`。

`inactive` 成员没有本次满足判断，`MUST NOT` 记录为 `met`、`unmet` 或 `agno`；`unresolved` 不是满足结果 `agno`；`error` 不是满足结果 `fault`。激活 `MUST NOT` 修改闭包身份、成员内容或权限上限。激活依据变化、撤销或过期时，当前会话 `MUST` 重新检查或失效，旧事件保持追加记录，不得被改写。被激活成员仍 `MUST` 独立通过策略、能力与决定权威检查。

**失败：**会话中动态加入成员、使用裸状态字符串而不声明结果域、把未激活写成满足、以激活扩大权限、忽略依据撤销，或用模型自行判断条件时，该激活或会话必须拒绝。

**验证：**`SYN-SCN-008` 至 `SYN-SCN-010`；`vectors/synem/cases.json`；未来 `conformance:synem-session-activation` 组件测试。

## 5. 当前未定义

本规范不冻结 Synem 的物理清单、文件扩展名、魔数、版本约束语法、符号和重定位模型、可选分支编码、执行顺序、并行调度、受限循环、远程对象仓库或跨会话缓存。它们必须由真实消费者、独立 ADR、新 Profile、威胁分析、正反向量与规范字节共同支持后才能进入实现。
