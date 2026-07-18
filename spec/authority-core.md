---
layout: spec
title: "Authority and Authorization Decision Core Specification · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/authority-core.html"
summary: "规定自然语言意义确认、Agent 动作和最终决定在什么范围、政策和截止点下才能称为已授权。"
document_status: "规范草案"
---
# Authority and Authorization Decision Core Specification

- 规范 ID：`AUT-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0029 已接受的权威、授权决定、委托与能力边界
- 物理编码：未定义；本规范不创建制品、文件格式、扩展名、政策语言、令牌格式或稳定 ABI
- 实现状态：仅有规范提案向量检查器；权威目录、政策求值器、同意界面、能力代理和决定服务均未实现

## 1. 范围

本规范定义一项自然语言投影、未决项解决、能力授予或最终决定在什么条件下可以被称为“已获授权”。它统一约束 Endem 的 `meaning_projection` 与 `unresolved_meaning`、closure 的权限收窄、contract 的政策与能力闭包、evidence 的决定记录、签名主体适用性以及外部 Agent 协议的授权请求。

`AUT-CORE` 不是新的工程制品、身份系统、访问令牌、角色数据库、政策脚本或决定引擎。认证只能回答当前主体怎样被识别；签名只能绑定受保护陈述；授权决定只能在精确语境和范围内允许或拒绝特定事项。它们都不能自行证明一句话为真、目标已经满足、证据已经充分或制品最终应被接受。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html)
- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html)

符合性声明 `MUST` 固定 `AUT-CORE`、所用政策、权威目录或规则、主体身份方法、对象规范、作用范围、截止点以及任何外部授权协议的精确版本。当前没有授权决定物理 Profile，任何工具都不得声称产生稳定授权事件、访问令牌或可互操作政策字节。

## 3. 权威语境与决定

### AUT-CTX-001 — 每次授权必须绑定完整权威语境

**要求：**授权检查 `MUST` 绑定精确政策或确定性规则、政策版本、权威域、对象或资源身份、操作、目的、受众、租户或司法范围、适用条件、决定截止点和失败责任。可变的 `latest` 政策、环境默认角色、组织名称或界面所在位置 `MUST NOT` 替代这些绑定。语境任一实质字段变化时，旧检查结果 `MUST` 失效并产生新决定。

**失败：**系统按当前最新政策解释旧点击、在不同租户复用同一角色、用页面路径推断授权域，或没有声明决定适用于什么对象和目的时，授权语境不完整。

**验证：**`AUT-SCN-001`、`AUT-SCN-002`；`vectors/authority/cases.json`；未来 `conformance:authority-context-binding` 组件测试。

### AUT-PRN-001 — 主体认证、角色资格与决定权必须分开

**要求：**授权过程 `MUST` 分别记录请求主体、实际行动者、被代表主体、认证方法与强度、声明角色、角色来源、角色在当前语境中的决定权限和核对依据。认证成功、持有签名密钥、组织成员资格、Agent Card、模型名称或服务账户身份 `MUST NOT` 自动产生决定权。主体身份不确定、角色不可验证或权限不适用时必须关闭失败或 `pending`。

**失败：**任何已登录用户都能批准发布、签名者被当作语义权威、服务账户代表资源所有者却不保留实际行动者，或远端 Agent 自报技能后取得授权时，主体边界无效。

**验证：**`AUT-SCN-003`、`AUT-SCN-004`；`vectors/authority/cases.json`；未来 `conformance:authority-principal-role` 组件测试。

### AUT-SCP-001 — 权限范围必须显式且默认不授予

**要求：**每项授权范围 `MUST` 明确限定允许的对象或资源、动作、语义面或字段、目的、受众、数量或资源上限、时间范围与附加条件。未列出的对象、动作和字段默认不授予；通配符、环境权限、继承角色或名称前缀只有在版本化政策定义其封闭展开和上限时才可使用。范围比较 `MUST` 使用本域规则，不能用字符串包含、JSON 子集或界面分组猜测“更小权限”。

**失败：**“可编辑项目”被解释为可确认全部 `meaning_projection`、读权限隐含写权限、同名前缀扩大资源集合，或未知字段按允许处理时，范围必须拒绝。

**验证：**`AUT-SCN-005`；`vectors/authority/cases.json`；未来 `conformance:authority-scope-closure` 组件测试。

### AUT-SEM-001 — 自然语言候选只能由确定性规则或范围有限的具名权威确认

**要求：**确认 `meaning_projection`、解决 `unresolved_meaning` 或固定构念、阈值、集合、时间和决定主体时，授权 `MUST` 绑定精确来源身份、提交后的解码文本和候选内容身份。授权还 `MUST` 绑定受影响的语义面与关系位置、候选生产方式、显示视图、授权主体、决定理由和剩余未决项。确定性规则必须版本化并只处理声明域；人工决定必须落在当前主体范围内。模型输出、相似度、置信度、结构合法、默认值、批量按钮或未展示差异的单次点击 `MUST NOT` 确认候选。

**失败：**模型最高概率候选直接进入 `meaning_projection`、授权者看到截断文本却批准完整对象、一次“全部接受”消除不同风险的 `unresolved_meaning`，或批准对象与显示对象身份不一致时，候选仍未获授权。

**验证：**`AUT-SCN-006`、`AUT-SCN-007`；`vectors/authority/cases.json`；未来 `conformance:semantic-authorization-binding` 组件测试。

### AUT-DEC-001 — 授权决定必须记录请求、结果与有限后果

**要求：**授权决定 `MUST` 绑定唯一请求身份、请求者、实际行动者、精确对象、请求范围、权威语境、所用依据、决定主体、决定时刻或截止点、理由、限制和结果。结果只允许 `allowed`、`denied` 或 `pending`：`allowed` 只授予记录范围，`denied` 只拒绝该请求，`pending` 表示尚无获授权答案。决定不得静默改写请求，部分授予必须生成精确缩小后的范围并让请求方明确核对。

**失败：**只保存“已批准”、结果没有对象和范围、部分批准仍返回原请求、缺失依据时默认 `allowed`，或 `pending` 被调用方当作允许时，决定无效。

**验证：**`AUT-SCN-008`；`vectors/authority/cases.json`；未来 `conformance:authorization-decision-content` 组件测试。

## 4. 委托、多人决定与同意

### AUT-DEL-001 — 委托必须保留双方身份并严格收窄

**要求：**委托链 `MUST` 显式记录原始授权主体、每一级授予者、受托行动者、被代表主体、可委托标志、范围、目的、受众、期限、剩余深度和撤销来源。链 `MUST` 有限、无环；每一级有效范围、期限、预算和委托深度 `MUST` 是上一层的严格子集或不增加。默认只允许可追踪委托，不允许把行动者伪装成被代表主体；若外部协议支持 impersonation，Noemion 仍必须保存真实行动者并由独立政策明确允许。

**失败：**子 Agent 获得父级未拥有的权限、链中隐藏中间行动者、服务账户冒充用户、委托循环、无限深度或续期扩大范围时，委托无效。

**验证：**`AUT-SCN-009`、`AUT-SCN-010`；`vectors/authority/cases.json`；未来 `conformance:delegation-chain-narrowing` 组件测试。

### AUT-MUL-001 — 多权威规则必须预先固定并抵抗重复与顺序影响

**要求：**需要多人、角色组合、法定人数或否决权时，政策 `MUST` 在请求前固定合格主体集合、不同主体身份规则、所需数量或角色、顺序是否相关、否决与冲突处理、缺席处理和截止点。别名、同一控制主体的多个凭据、重复签名和重放决定只能计为一个主体。未达到规则、出现未解决冲突或无法证明主体独立性时必须 `pending` 或按预注册政策 `denied`，不得取最先、最后或多数界面事件。

**失败：**同一人用三个账户满足三人批准、重复签名增加票数、后到决定覆盖先前否决，或政策在看到投票后改变门槛时，多权威决定无效。

**验证：**`AUT-SCN-011`、`AUT-SCN-012`；`vectors/authority/cases.json`；未来 `conformance:multi-authority-policy` 组件测试。

### AUT-CNS-001 — 同意必须绑定可理解视图且不能替代授权政策

**要求：**需要人类同意时，过程 `MUST` 把人看到的完整安全视图、精确机器对象、请求动作、资源、目的、接收方、期限、可撤销性和后果绑定到同一请求。视图必须遵守 TEXT-IDENTIFIER-CORE，披露截断、规范化、隐藏字符和机器值；默认选中、捆绑无关权限、模糊目的、假紧迫或拒绝路径缺失 `MUST NOT` 产生有效同意。同意只是授权政策的一项输入，不自动证明同意者具有决定权。

**失败：**界面显示“读取报告”而机器请求包含写入、隐藏接收方、拒绝按钮不可达、显示对象与授权对象不同，或任何点击者都被当作资源所有者时，同意无效。

**验证：**`AUT-SCN-013`、`AUT-SCN-014`；`vectors/authority/cases.json`；未来 `conformance:consent-view-binding` 组件测试。

## 5. 时效、重放、能力与结果分离

### AUT-TIM-001 — 授权有效性必须绑定时间、状态与撤销

**要求：**授权使用 `MUST` 核对决定时刻、适用起止、截止点、状态来源、新鲜度、撤销与主体或政策变更。过期、撤销、状态未知或实质语境漂移不得沿用缓存成功。撤销和过期只改变后续适用性，不改写历史决定、来源字节、Endem 身份或已记录 evidence；需要持续授权的会话必须预先声明复核频率和失败动作。

**失败：**永久复用一次批准、离线缓存忽略撤销、角色离职后继续授权、当前时间替代声明截止点，或删除历史决定掩盖撤销时，适用性无效。

**验证：**`AUT-SCN-015`；`vectors/authority/cases.json`；未来 `conformance:authorization-validity-cutoff` 组件测试。

### AUT-RPL-001 — 决定和同意不得跨请求、对象或目的重放

**要求：**可产生副作用或关闭语义未决项的授权请求 `MUST` 绑定唯一请求身份、精确对象、动作、范围、目的、受众、会话、截止点、允许使用次数和重放或幂等规则。一次性决定在消费后不得再次使用；可重复决定也只能在完全相同的声明语境内使用。重试必须保留原请求身份和剩余预算，不能通过新 ID 取得第二次副作用。

**失败：**旧批准用于新版本 Endem、同一点击授权另一个租户、付款同意被重复消费、重试换 ID 绕过去重，或发布批准被用于能力授予时，重放必须拒绝。

**验证：**`AUT-SCN-016`；`vectors/authority/cases.json`；未来 `conformance:authorization-replay-binding` 组件测试。

### AUT-CAP-001 — 能力只能由已授范围与所有本地上限求交得到

**要求：**运行能力 `MUST` 是授权决定、制品或 closure 上限、当前政策、环境支持、contract、适配器与资源预算的交集。授权请求、工具说明、协议 scope 挑战、Agent 技能、凭据存在和环境可访问性只是候选或上限，不是额外授予。能力描述与实时秘密必须分开；扩大动作、对象、受众、期限或预算 `MUST` 产生新授权决定和新 run 会话，不能修补现有 contract。

**失败：**权限使用并集、沿用环境 root、把 token 透传给下游、MCP step-up 原地扩大旧会话，或模型创建子 Agent 后倍增预算时，能力派生无效。

**验证：**`AUT-SCN-017`；`vectors/authority/cases.json`；未来 `conformance:authorized-capability-intersection` 组件测试。

### AUT-SEP-001 — 授权不得洗白其他结果域

**要求：**主体认证、签名验证、角色资格、语义授权、能力授予、证据有效性与覆盖、满足判断、授权决定、最终 `accepted / rejected / deferred` 和 run 会话终止 `MUST` 保持独立主体与结果。`allowed` 只允许执行或确认其声明事项，不证明候选为真、目标 `met`、evidence `valid` 或 `sufficient`、制品 `accepted`、会话 `completed`。模型、runner、外部 Agent、工具或适配器 `MUST NOT` 因执行成功、自报身份或取得令牌而成为语义或最终决定权威。

**失败：**访问授权被解释为事实正确、人工确认投影后直接 `accepted`、A2A `AUTH_REQUIRED` 解决后任务被写成 `met`，或有效签名和授权主体共同替代证据判断时，跨域推导无效。

**验证：**`AUT-SCN-018`；`vectors/authority/cases.json`；未来 `conformance:authority-result-domain-separation` 组件测试。

## 6. 权威依据与采用边界

- [RFC 9396](https://www.rfc-editor.org/rfc/rfc9396.html) 说明粗粒度 scope 不足以表达动作、资源和交易条件，并允许资源所有者只授予请求子集。Noemion 借鉴精细范围和部分授予显式化，不采用 OAuth JSON 作为本地授权格式。
- [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html) 区分 delegation 与 impersonation，并保留 subject、actor 和委托链。Noemion 默认只接受可追踪、逐级收窄的委托，不因外部 token 隐去实际行动者。
- [RFC 9470](https://www.rfc-editor.org/rfc/rfc9470.html) 只规定认证强度不足时的 step-up 挑战；它明确不定义资源的授权要求。Noemion 因此不把“重新认证成功”当作“已经获准当前动作”。
- [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) 要求访问令牌尽量绑定发送者、受众、资源和动作。Noemion 把这些视为外部能力上限，实际能力仍须与本地 contract 和政策求交。
- [MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)要求资源受众绑定并支持增量 scope；[A2A 1.0 规范](https://a2a-protocol.org/v1.0.0/specification/)允许 `AUTH_REQUIRED` 沿 Agent 链继续委托，却把授权模型留给实现。Noemion 固定本地权威、委托和结果分离，不让协议状态成为本地授权。
- [GNU Guix 替代服务器授权](https://guix.gnu.org/manual/devel/en/guix.pdf)要求把允许的签名公钥显式加入本地 ACL，说明“签名存在”与“本地决定信任哪个主体”是两件事。[GnuPG 信任模型](https://www.gnupg.org/documentation/manuals/gnupg/GPG-Configuration-Options.html)也把密钥有效性与用户配置的信任模型分开。Noemion 借鉴本地显式信任，不采用其密钥或 Web of Trust 作为语义授权模型。
- 维特根斯坦在《逻辑哲学论》4.022 写道：“命题显示其意义。命题显示当它为真时事情是怎样的，而且宣称事情就是这样的。”工程上，这支持把候选命题的意义结构与其真假分开；它不能决定谁拥有授权、同意是否有效或多人冲突怎样解决。这些制度与安全关系必须由本规范、政策和证据另行定义。

## 7. 当前未定义

本规范不确定权威目录、主体身份体系、角色语言、政策语言、授权事件物理编码、同意 UI Profile、法定人数算法、凭据格式、OAuth/MCP/A2A 映射、撤销分发、能力代理、审计存储、组织治理或法律效力。它们必须由真实生产者和消费者、独立 Profile、威胁分析、正反向量，以及进入代码开发阶段并明确实现范围后取得的实现证据共同支持。
