---
layout: content
title: 权威与授权决定规范
page_role: content
footer_text: Noemion · Authority and Authorization Decisions
permalink: "/specifications/authority.html"
summary: 说明一次请求必须分别记录谁提出、谁行动、代表谁、操作什么、依据哪项政策，以及授权何时失效。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 权威与授权决定边界
page_lead: 开发者必须分别记录谁提出请求、谁实际行动、代表谁、可以操作哪个对象，以及这次授权何时失效。AUT-CORE 为自然语言意义确认和 Agent
  动作授权规定共同的检查边界。
badges:
- AUT-CORE 0.1.0-draft
- 当前策略
- 物理格式待定
- 尚无政策引擎
previous_url: text-and-identifiers.html
previous_label: 文本与标识符边界
next_url: "../architecture/adr-0029-authority-and-authorization-decisions.html"
next_label: ADR-0029 · 身份已确认，不等于操作已获准
---

## 用同一次发布理解一次授权决定

一项 CI 工作负载请求把精确发布对象部署到生产环境。授权记录不能只写“发布负责人已批准”，它必须让后续控制平面恢复完整请求并判断这份决定是否仍然适用。

1. 固定请求与对象
2. 区分三类主体
3. 核对政策与范围
4. 形成有限决定
5. 求交得到会话能力
6. 另行判断执行与验收

| 检查顺序 | 本例必须记录 | 不满足时怎样处理 |
| --- | --- | --- |
| 固定请求 | 完整内容身份指向的发布对象、生产租户、部署动作、目的、受众、次数和截止点 | 对象仍是 `latest`、名称前缀或未关闭的集合时，停止授权 |
| 区分主体 | 请求维护者、具体 CI 运行实例，以及它所代表的发布团队 | 只有模型名、Agent 名、服务账户或密钥时，不能恢复实际行动者 |
| 核对权威 | 当前政策、权威域、角色来源、认证方法和该角色对此对象与动作的决定权 | 登录、组织成员资格、签名有效或自报能力都不能补足决定权 |
| 形成决定 | `allowed`、`denied` 或 `pending`，以及理由和精确限制；部分授予形成缩小后的新范围 | 不得把模糊“已批准”、静默裁剪或 `pending` 当成允许 |
| 派生能力 | 决定范围与 session contract、制品上限、环境、适配器和预算的交集 | 任何上限缺失或已经漂移时关闭对应能力；扩大范围必须新建会话 |

授权允许一次声明范围内的行动，不证明行动已经发生，也不证明发布目标已经满足。工具结果、证据判断和最终验收继续由各自的结果域负责。

> **规范边界：**实现义务以 [AUT-CORE 条款源](https://noemion.github.io/spec/authority-core.html)为准。公开说明帮助开发者定位问题，不复制第二套授权格式或政策语言。

## 遇到“已授权”先问对象是什么

开发者不能只保存一个 `authorized: true`。意义确认、动作授权和会话能力回答的是不同问题；证据判断与最终接受又是另外两项决定。

| 实际问题 | 需要核对 | 本层结果 | 不能越级推出 |
| --- | --- | --- | --- |
| 谁可以确认这个意义候选 | 来源、候选、语义位置、安全视图、规则或具名权威 | 候选进入确认的 `meaning_projection`，其余部分留在 `unresolved_meaning` | 候选为真，或主体获得工具权限 |
| 谁可以尝试这个动作 | 政策、主体、对象、动作、目的、受众、范围和截止点 | `allowed / denied / pending` 当前精确请求 | 其他字段、租户、用途或后续版本也获权 |
| 当前会话能调用什么 | 授权与全部本地上限的交集 | 当前 run 会话的能力上限 | 长期权限或协议公开的全部能力 |
| 证据是否足够 | evidence entry 的有效性、覆盖范围和适用判据 | 声明范围内的证据判断 | 授权主体已经最终接受 |
| 最终是否接受 | 满足结果、适用证据、决定规则和具名权威 | `accepted / rejected / deferred` | 由认证、授权、签名或会话完成替代 |

语言哲学只能帮助区分“一个命题表达什么”与“它是否成立”。谁能确认候选、批准动作或接受结果属于额外的制度和安全关系，不能从句子的结构、模型置信度或措辞本身推出。

## 权威与授权必须怎样判断

十二条条款可以按一次请求的四个检查阶段使用。精确失败语义、适用向量和未来符合性要求仍以条款源为准。

| 检查阶段 | 对应条款 | 开发者必须得到的答案 | 典型关闭失败 |
| --- | --- | --- | --- |
| 形成请求 | `AUT-CTX-001`、`AUT-PRN-001`、`AUT-SCP-001`、`AUT-SEM-001`、`AUT-DEC-001` | 语境、三类主体、封闭范围、意义确认依据和有限决定都能独立恢复 | 可变政策、模糊对象、未知字段、未展示差异或只有布尔批准 |
| 处理多人关系 | `AUT-DEL-001`、`AUT-MUL-001`、`AUT-CNS-001` | 委托逐级收窄，多人规则预先固定，人看到的安全视图与机器请求一致 | 隐藏行动者、重复账户计票、默认勾选或不可达拒绝路径 |
| 使用决定 | `AUT-TIM-001`、`AUT-RPL-001`、`AUT-CAP-001` | 时效与撤销仍有效，请求不能跨对象重放，能力只取全部上限的交集 | 永久缓存、重试换 ID、令牌透传、权限并集或旧会话原地扩权 |
| 解释结果 | `AUT-SEP-001` | 认证、授权、能力、证据、满足、最终决定和会话结果各自保留 | 把 `allowed` 写成事实真值、`met`、`accepted` 或 `completed` |

## 把自然语言、Agent 与权限升级接到同一条边界

### 自然语言候选怎样获得意义确认

模型、确定性规则或人都可以产生候选。确认者必须看到候选相对精确来源改变了什么、影响哪些关系、由谁产生，以及还有哪些待确认项。意义确认只覆盖已展示且落在主体职责内的部分；它不授予调用工具、修改对象或部署服务的动作权限。

确定性规则也只能处理版本化的声明域。超出输入域或输出位置的内容继续进入 `unresolved_meaning` 或拒绝，不能借“自动规则”取得新的自然语言判断权。

### Agent 名称为什么不能代替实际行动者

- **模型身份** 说明哪个模型或端点参与生成候选，不说明哪套软件实际行动。
- **Agent 定义身份** 说明软件、配置、提示、工具声明和政策组合，不定位正在运行的副本。
- **工作负载身份** 说明哪个受管理软件主体通过认证，不等于被代表的人或业务主体。
- **运行实例与调用身份** 定位哪个副本在什么会话中发起哪次尝试；授权记录还必须保存实际行动者与被代表主体。

### 委托和权限升级什么时候必须停止旧会话

委托链必须同时保留授予者、实际行动者与被代表主体，并在对象、动作、目的、受众、期限、预算和剩余深度上逐级收窄。外部系统要求新增 scope、写权限、资源或预算时，控制平面只能提出新请求；新决定与新的能力交集成立后，才能开始新的 run 会话。

人类点击只有在安全视图与机器请求一致、目的和接收方清楚、拒绝路径可达、期限与撤销后果明确时，才可能成为同意依据。多人决定还要在请求前固定合格主体、身份去重、门槛、否决、冲突和截止点。

## 外部机制能提供什么

精细授权与委托

[RFC 9396](https://www.rfc-editor.org/rfc/rfc9396.html)提供动作、资源和部分授予边界；[RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)分开委托中的 subject 与 actor。它们不定义 Noemion 的政策格式或最终决定权。

Agent 协议授权

截至 2026-07-15，[MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)要求资源受众绑定并禁止令牌透传；[A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)是最新正式版。协议凭据、状态和 Agent Card 都只是本地决定的输入。

Agent 身份研究

[NIST 概念论文](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)把最小权限、具体动作、代表关系和人机授权绑定列为研究问题；[SPIFFE](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)提供工作负载认证，不提供应用动作授权。

GNU 的本地信任边界

[GNU Guix](https://guix.gnu.org/manual/devel/en/guix.pdf)要求本地显式授权替代服务器公钥；[GnuPG](https://www.gnupg.org/documentation/manuals/gnupg/GPG-Configuration-Options.html)把签名检查与本地 trust model 分开。项目只采用这种分离纪律，不采用其密钥或 Web of Trust 作为语义权威。

## 更强问题应当进入哪份研究

- 预览、模拟、批准与执行之间的关系进入 [预览、模拟与批准研究提案](https://noemion.github.io/spec/preview-simulation-and-approval-proposal.html) 。
- 模型、Agent 定义、工作负载、运行实例、凭据与一次调用的绑定进入 [软件 Agent 身份与责任链研究提案](https://noemion.github.io/spec/software-agent-identity-and-accountability-boundaries-proposal.html) 。
- 访问、使用、披露、保留、删除与清除的不同控制者进入 [数据使用、保留与删除研究提案](https://noemion.github.io/spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.html) 。

这些提案只保存问题分解、反例和进入规范前的条件，不修改 AUT-CORE，也不创建 Agent 身份、数据、隐私或批准制品。

> [AUT-THREAT](https://noemion.github.io/spec/authority-threat-model.html)检查范围放大、委托、同意、重放和结果洗白；[AUT-SCEN](https://noemion.github.io/spec/authority-scenarios.html)保存设计案例；[AUT-CORE 向量](https://github.com/Noemion/noemion.github.io/tree/main/vectors/authority)检查登记中的允许与拒绝关系。它们只提供资料一致性证据，不证明授权组件已经实现。

## 当前状态与限制条件

**当前策略：**每次意义确认或动作授权都绑定完整语境、主体、对象、范围、时效和结果域；条件不足时关闭对应决定或能力。

**已有成果：**AUT-CORE 0.1.0-draft 已规定完整语境、主体分离、封闭范围、意义确认、有限决定、委托、多人规则、同意、时效、重放、能力交集和结果分离。

**待定内容：**权威目录、角色与政策语言、授权事件物理编码、同意 UI Profile、多人算法、凭据格式、协议映射、撤销分发、能力代理、审计存储和法律效力仍保持开放。

**限制条件：**当前只有规范、威胁、场景和提案向量，没有身份提供方、政策求值器、同意界面、能力代理、决定服务或协议授权实现。
