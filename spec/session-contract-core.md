---
layout: spec
title: "contract 核心规范 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/session-contract-core.html"
summary: "规定一次受控会话怎样重新核对目标、政策、环境、能力和预算，并在任一关键条件变化后立即停止使用旧权限。"
document_status: "规范草案"
---
# contract 核心规范

- 规范 ID：`SESSION-CORE`
- 版本：`0.1.0-draft`
- 当前状态：规范草案；已经写明会话职责与条款，尚无组件实现
- 实现状态：只有提案向量；没有 runner、装载器、沙箱、能力代理或运行时
- 线格式状态：不适用；contract 不是持久对象，也没有文件格式

## 1. 目的

contract 只在一次运行中有效，建立后不能修改。runner 建立 contract 前，必须重新验证身份固定且内容已经确认的 Endem 或 closure，并核对必需的外部陈述、政策、截止点和撤销状态。

runner 还必须取得目标限制、当前政策、环境支持、授权、可用能力和预算的交集。任一必需条件缺失时，本次会话不能开始。

contract 把持久目标与会话运行时的可变环境分开。它不保存实时凭据、打开的句柄、可变观察、模型记忆或最终结果。运行事件和观察可以形成 evidence；目标是否满足、权威决定和会话为何终止仍分别判断。

任何权威、同意、委托、授权决定或能力授予都 `MUST` 绑定并符合适用的精确 `AUT-CORE` 版本。`SESSION-CORE` 只规定怎样求出本次会话允许使用的交集，不重新定义谁有权授权这些输入。

`MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT` 与 `MAY` 使用大写时，具有 BCP 14 规定的规范强度。

## 2. 在生命周期中的位置

```text
已解决的 Endem 或 closure
        + 必需的外部陈述
        + 陈述政策、截止点、有效性和撤销状态
        + 具名政策与决定者
        + 环境与适配器绑定
        + 有上限的能力和预算
        + 观察与披露任务
                         |
                         v
             只服务本次运行的只读 contract
                         |
                         v
     运行事件与结构化观察 -> evidence -> 评估 -> 决定
```

尚未核对的输入提案不是 contract。只有全部必需绑定通过检查并固定为只读后，提案才成为 contract。任何关键条件变化都必须产生新的会话提案；系统不能修改或恢复旧 contract。

## 3. 规范条款

### SESSION-SUB-001 — 会话主体和外部陈述必须精确且经过本次重新验证

**要求：**contract `MUST` 用精确内容身份和 Profile 绑定且仅绑定一个 `resolved` Endem 或 closure。它 `MUST` 分别绑定每项必需外部陈述的类型、主体摘要、验证政策、验证结果、具名截止点、撤销状态和依赖方适用决定。runner 建立 contract 前 `MUST` 重新检查容器、Profile、内容、闭包和每项外部关系。显示名称、搜索结果、可变路径、最新版本、缓存成功、签名存在标记或外部 Task 标识 `MUST NOT` 代替这些检查。

**失败：**主体尚未解决、缺失、含糊或已经变化，或者必需陈述缺失、无效、已撤销、超出范围或不适用当前政策时，建立失败。系统不能创建 contract 或满足结果。

**验证：**`SESSION-SCN-001`、`SESSION-SCN-002`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-subject-revalidation` 组件检查。

### SESSION-POL-001 — 建立会话前必须固定政策、决定者和截止点

**要求：**contract `MUST` 绑定用于建立本次会话的精确政策集合、政策版本或身份、决定者、升级处理者、适用同意、截止点和到期时间。影响授权且仍未解决的冲突或 `unresolved_meaning` 项 `MUST` 使建立失败，除非具名政策证明它不属于本次会话范围。模型、适配器、工具描述或远端 Agent `MUST NOT` 仅因出现在上下文中就成为政策或决定者。

**失败：**隐式默认值、可变的最新政策、缺少决定者、范围内仍有歧义或政策冲突时，建立失败。

**验证：**`SESSION-SCN-003`、`SESSION-SCN-004`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-policy-closure` 组件检查。

### SESSION-ENV-001 — 环境和后端假设必须成为显式绑定

**要求：**contract `MUST` 声明目标和政策所需的环境事实，包括适用平台、地区设置、时间权威、隔离 Profile、适配器、协议版本，以及模型或规则后端身份。每项绑定 `MUST` 区分声明的标识和实际观察到的属性，并指出用于确认属性的观察。未声明的环境状态和远端自述 `MUST NOT` 被视为已经验证。

**失败：**缺少必需绑定、协议不受支持、环境声明未经验证或存在关键不一致时，建立失败。建立后的关键环境漂移按 `SESSION-IMM-001` 使 contract 失效。

**验证：**`SESSION-SCN-005`、`SESSION-SCN-006`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-environment-binding` 组件检查。

### SESSION-CAP-001 — 会话能力只能取交集或继续减少

**要求：**contract 的能力集合 `MUST` 取目标与 closure 限制、当前政策、操作者授权、环境支持和适配器上限的交集。每项允许能力 `MUST` 绑定动作、资源或受众、范围、约束、授予者、到期时间和撤销检查。缺少必需能力时建立失败；可选能力消失时，只能依据已经声明的 guard 停用固定的 closure 成员。提升或扩大权限 `MUST` 创建新的运行会话提案，`MUST NOT` 修改当前 contract。

**失败：**合并权限、退回环境默认权限、展开通配符、透传令牌、替换受众或运行时自行提权时，提案无效；已经建立的会话必须中断。

**验证：**`SESSION-SCN-007`、`SESSION-SCN-008`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-capability-intersection` 组件检查。

### SESSION-SEC-001 — 实时秘密和句柄必须留在 contract 之外

**要求：**contract `MUST` 只保存非秘密的能力描述和审计所需的不可逆引用。Bearer token、refresh token、私钥、会话 cookie、文件描述符、socket、进程句柄和提供方原生能力句柄 `MUST NOT` 进入 contract、evidence 或持久日志。独立的最小能力域可以保存实时材料，但 `MUST` 把材料绑定到精确运行会话、预期资源或受众、范围和到期时间。保持描述不变的轮换 `MAY` 在 contract 外发生；范围、受众或授权变化必须创建新会话。

**失败：**提案含有秘密、句柄没有绑定、引用能够跨会话复用或令牌被透传时，建立失败或会话失效。

**验证：**`SESSION-SCN-009`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-secret-separation` 组件检查。

### SESSION-BUD-001 — 预算、时间和取消必须有限且注明类型

**要求：**contract `MUST` 为会话可能消耗的每类资源绑定有限上限，包括适用的经过时间、调用、重试、token、字节、存储、进程和成本。每项上限 `MUST` 说明单位、计数者、重置规则和耗尽后的动作。重试、子任务、模型委托和协议适配器 `MUST` 消耗同一外层预算或其严格子集。运行前 `MUST` 确定取消和截止时间怎样传递。

**失败：**必需资源没有上限、单位不兼容、计数被隐藏重置、子任务逃逸预算或取消被忽略时，建立失败或会话中断。预算耗尽不表示目标 `unmet`。

**验证：**`SESSION-SCN-010`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-budget-envelope` 组件检查。

### SESSION-ACT-001 — closure 激活只能发生在固定成员内，且不能代替满足判断

**要求：**主体为 closure 时，contract `MUST` 绑定精确的封闭成员集合、激活 guard、输入事件身份、截止点，以及初始 `active / inactive / unresolved / error` 分类。运行时 `MAY` 只按已绑定的 guard 和 evidence 规则重新判断激活事件；它 `MUST NOT` 增加成员、改变 closure 身份、授予能力或修改 contract。激活状态 `MUST NOT` 直接映射为 `met / unmet / undetermined / fault`。

**失败：**运行时发现新依赖、查找最新版本、通过激活增加权限、缺少 guard 依据或把激活状态转换成满足结果时，建立失败或受影响的会话路径失效。

**验证：**`SESSION-SCN-011`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-activation-boundary` 组件检查。

### SESSION-OBS-001 — 必须指定观察、评估、披露和决定责任

**要求：**contract `MUST` 为每项适用的 `satisfaction_criteria` 指定获准的观察生产者、方法、环境和时间范围、预期 `structured_observation` 关系位置、所需 evidence 类别、披露规则、评估政策和具名决定者。映射 `MUST` 分开实际观察、目标满足、evidence 有效性、覆盖度、最终决定和会话终止。模型输出和外部协议状态只能作为有类型的候选或带来源事件。

**失败：**必需观察无人负责、缺少决定者、披露损失被隐藏，或者工具或 Agent 成功被直接写成 `met` 或 `accepted` 时，建立失败。

**验证：**`SESSION-SCN-012`、`SESSION-SCN-013`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-observation-plan` 组件检查。

### SESSION-IMM-001 — 建立后 contract 只读，关键条件漂移使其失效

**要求：**contract 建立后 `MUST` 保持只读。主体身份、外部陈述、验证结果、撤销状态、政策、决定者、必需环境、能力描述、预算、激活 guard、观察任务或披露政策发生变化时，`MUST` 使 contract 失效，并按预先声明的规则停止或终止运行。实现 `MUST` 追加一项说明影响范围的事件并保留已有 evidence；它 `MUST NOT` 修改旧 contract 或删除漂移记录。

**失败：**原位修改、静默刷新为更大权限、关键条件漂移后继续运行，或覆盖旧 evidence，都违反会话要求。

**验证：**`SESSION-SCN-014`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-drift-invalidation` 组件检查。

### SESSION-LIF-001 — contract 不持久化、不转移，也不恢复

**要求：**contract `MUST` 只属于一次运行和一个授权语境。它 `MUST NOT` 拥有扩展名、可移植线格式、全局内容身份、包坐标或跨会话复用机制。诊断快照 `MAY` 把脱敏后的描述记录为 evidence 或会话事件，但 `MUST NOT` 据此重建、转移或复活 contract。完成、失败、停止或失效后，全部实时能力材料 `MUST` 变得不可访问，并触发已经声明的清理程序。

**失败：**把 contract 序列化为可复用对象、把复制的会话标识当作权限、使用过期句柄恢复会话，或根据日志重建会话时，系统必须拒绝。

**验证：**`SESSION-SCN-015`；`vectors/session-contract/cases.json`；未来 `conformance:session_contract-session-disposal` 组件检查。

## 4. 当前不定义的内容

本规范不定义 contract 文件、扩展名、魔数、序列化、稳定 ABI、运行 API、能力代理、沙箱、事件编码、进程模型、恢复协议或实现语言。它也不选择 Linux namespace、seccomp、Landlock、容器、虚拟机或模型 SDK。未来组件只有在独立证据证明这些机制提供了所需隔离和失效行为后，才能用它们满足相应实现义务。
