---
layout: architecture-decision
title: ADR-0024 · 权限只属于这一次会话
page_role: content
footer_text: Noemion · ADR-0024
permalink: "/architecture/adr-0024-session-contract.html"
summary: 说明持久目标为什么不携带永久权限，以及每次尝试怎样重新固定目标、环境、能力、预算和观察责任。
decision_id: ADR-0024
page_heading: ADR-0024 · 权限只属于 · 这一次会话
page_lead: 可长期保存的目标不携带永久权限。每次尝试都要重新固定精确目标、当前政策与环境，再把能力、预算和观察责任收窄到本次会话。
badges:
- 当前策略
- SESSION-CORE 0.1.0-draft
- 仅限一次会话
- 尚未实现
previous_url: adr-0023-endem-content-standard.html
previous_label: ADR-0023
next_url: adr-0025-structured-diagnostics.html
next_label: ADR-0025
---

## 用一次受限发布会话理解 contract

某个 closure 固定了构建制品与服务健康目标的完整闭包，但它没有授予部署权，也没有指定本次运行可以访问哪个环境。runner 只有重新核对全部会话条件，才能建立一次会话的只读执行契约（设计阶段名称 contract）。

1. 固定精确目标及完整闭包
2. 重验外部陈述与撤销状态
3. 固定政策、环境和决定权威
4. 求能力交集分配有限预算
5. 建立本次contract
6. 运行、观察终止并销毁

| 发布步骤 | 本次会话明确固定 | 不能依赖的隐含信息 |
| --- | --- | --- |
| 选择目标 | 精确 closure 身份、Profile 和全部成员闭包 | 文件名、分支名、缓存记录或远端 `latest` |
| 核对前置条件 | 适用外部陈述、验证记录、政策截止点、撤销状态与依赖方判断 | 单一可信布尔值、签名外观或上次通过 |
| 关闭运行边界 | 仅限预发布环境、具名适配器、协议版本、时钟和后端 | 当前目录、机器默认值或工具自行发现的环境 |
| 分配权限与预算 | 仓库只读、预发布环境写入、十分钟、二十次调用、两次重试和一个子任务 | 操作者的全部权限、每个子任务一份新配额或模型提出的扩权 |
| 运行与观察 | 每项 `satisfaction_criteria` 的观察者、方法、时间、披露和决定责任 | 工具成功、Task 完成或日志数量直接代表目标满足 |
| 结束会话 | 保留有范围事件和 evidence，销毁实时能力与秘密 | 用检查点复活旧权限，或把旧 contract 用于下一次运行 |

contract 的“只读”表示建立后不能原地修改，并不表示会话没有计划、事件、重试或终止状态。任何需要扩大权限或改变实质绑定的继续运行，都必须重新建立会话。

## 目标、会话契约、运行者和证据各自负责什么

| 对象 | 开发者用它回答什么 | 不得承担什么 |
| --- | --- | --- |
| Endem 或 closure | 期望哪种终态，单个目标或多个目标怎样形成固定闭包 | 不携带当前机器、实时凭据或一次会话权限 |
| contract | 这个精确目标在本次尝试中受哪些政策、环境、能力、预算和观察责任约束 | 不保存可变计划、工具返回、实时秘密、最终结果或可恢复权限 |
| runner | 谁重新验证输入、建立契约、控制能力并执行一次会话 | 不改写目标、不自行扩权，也不替验收权威作出决定 |
| evidence 与决定记录 | 实际观察支持什么有限主张，以及具名权威作出什么决定 | 存在记录不表示会话可恢复，也不能反向改变目标或契约 |

这个边界使持久目标与临时权力分离：Endem 和 closure 可以长期保存，contract 只属于一次授权上下文中的尝试。运行历史可以成为下一次会话的输入，却不是下一次会话的准入证明。

## 建立前必须封闭哪些边界

| 条款组 | 必须精确绑定 | 拒绝建立的情况 |
| --- | --- | --- |
| 主体<br>`SESSION-SUB-001` | 精确内容、Profile、闭包、适用外部陈述、验证记录、政策截止点和撤销状态 | 主体含糊、内容变化、类型不符、陈述失效或记录无法关联 |
| 政策与权威<br>`SESSION-POL-001` | 政策身份、决定与升级权威、适用 consent、截止点和有效期 | 默认采用最新政策、权威未具名，或范围内仍有待确认项 |
| 环境<br>`SESSION-ENV-001` | 平台、时钟、隔离配置、适配器、协议以及模型或规则后端身份 | 缺少必需绑定、只依赖远端自述，或实际环境与声明不一致 |
| 观察责任<br>`SESSION-OBS-001` | 每项判据的观察生产者、方法、时间、evidence 类别、披露和决定权威 | 关键观察无人负责，或准备在运行结束后再猜测证据范围 |
| 不可变与生命周期<br>`SESSION-IMM-001` · `SESSION-LIF-001` | 失效条件、中断策略、事件保存范围、实时能力销毁和新会话规则 | 允许原地修补、跨会话转移、恢复旧秘密或复用一次性授权 |

现行 SESSION-CORE 只接受精确的 `resolved` Endem 或 closure。内容状态不能证明会话准入；适用外部陈述、验证政策、截止点、撤销状态与依赖方判断必须逐项绑定并重新核对。

> **现行草案限制：**这些关系已经同步进入条款、登记、威胁、场景和正反向量，但仍没有 contract 文件格式或运行实现。

## 能力、预算和秘密只能收窄

| 边界 | contract 可以记录 | 必须留在外部能力域 |
| --- | --- | --- |
| 能力<br>`SESSION-CAP-001` | 动作、资源或受众、范围、约束、授予者、有效期与撤销检查；只取目标、政策、环境和调用者上限的交集 | 操作者的完整权限、协议服务器公开的全部工具，以及运行中新增的 scope |
| 秘密<br>`SESSION-SEC-001` | 非秘密描述、受众和句柄类别 | Bearer token、刷新令牌、私钥、cookie、文件描述符、socket 和供应商原生句柄 |
| 预算<br>`SESSION-BUD-001` | 时间、调用、重试、令牌、字节、存储、进程和成本的有限、带单位上限 | 无限默认值、子任务重新计数或无法传播的取消 |
| 闭包激活<br>`SESSION-ACT-001` | 固定 closure 成员的会话期激活规则 | 运行中发现的新成员、扩大后的成员能力，或把激活状态当成满足结果 |

[MCP 2025-11-25 授权规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)要求令牌面向目标资源并按需请求权限；其[安全实践](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)进一步说明会话标识不是认证，令牌也不得穿透转发。Noemion 采用资源、受众和最小权限的边界，但不把 OAuth 令牌、MCP Session ID 或 Task ID 放进 contract。

预算耗尽只说明本次尝试不能在现有上限内继续，不自动产生目标 `unmet`。资源限制、会话终止、证据充分性、目标满足和最终接受仍使用各自的结果域。

## 漂移、取消和恢复为什么必须开始新会话

模型版本、适配器、协议、政策、能力、决定权威或隔离配置发生实质变化时，旧 contract 失效。runner 保存已经发生的事件和有范围证据，再按预先固定的策略中断或失败；不能把新值覆盖到旧契约上。

检查点、外部任务句柄和脱敏报告可以成为新会话的候选输入，但恢复仍要重新核对主体、外部陈述、政策、环境、能力和剩余预算。取消请求也只是一项事件：在远端状态或副作用无法确认时，系统必须保留未知，而不是声称工作从未发生。

| 外部机制 | 可以借鉴什么 | 不能据此推出什么 |
| --- | --- | --- |
| [ELF gABI 程序装载](https://gabi.xinuos.com/elf/07-pheader.html) | 区分持久文件与系统据此建立的进程映像 | contract 不是段、内存映像、进程或可执行格式 |
| [Linux capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) | 拆分特权并以能力上界限制执行后可获得的权限 | Linux 能力不可移植，单一能力也不能证明完整隔离；过宽的 `CAP_SYS_ADMIN` 尤其不能作为最小权限证明 |
| [Linux no_new_privs](https://www.kernel.org/doc/html/latest/userspace-api/no_new_privs.html) 与 [Landlock](https://docs.kernel.org/userspace-api/landlock.html) | 提供执行后不新增权限和进程自我收窄的候选机制 | 两者都不是完整沙箱，也不覆盖网络、模型、协议和外部服务权限 |
| [GNU C Library 资源限制](https://www.gnu.org/software/libc/manual/html_node/Limits-on-Resources.html) | 区分软上限与硬上限，并说明进程怎样继承和收窄限制 | 进程限制不覆盖工具调用、模型令牌、供应商成本或分布式任务预算 |
| [GNU make 中断处理](https://www.gnu.org/software/make/manual/html_node/Interrupts.html) | 中断后删除可能只完成一部分的目标，避免把半成品误当成最新结果 | 清理动作本身可能失败；发出取消或销毁请求不证明副作用已经消失 |
| [MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) | 持久任务必须绑定授权上下文，并受期限、并发和清理规则约束 | 外部 Task 可恢复，不表示 Noemion 会话或实时权限可以恢复 |
| [A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/) | Task、Message、Artifact、状态与取消语义保持分离 | Task 终态、取消结果或上下文标识不能直接成为本地满足、证据充分或授权决定 |

**复核日期：**2026-07-16。外部协议和操作系统机制只提供设计证据；正式实现仍需固定平台、版本、威胁假设、降级行为和可重复测试。

## 当前还不能承诺哪种运行时或沙箱

本决定建立 `SESSION-CORE 0.1.0-draft` 的解释边界，但不建立 contract 文件、序列化格式、API、运行时、进程模型、沙箱、凭据代理、预算器、事件编码、恢复格式或销毁实现，也不表示 runner 已经实现。

现有十条条款、十项威胁、十五个自然语言场景以及十个允许和十个确定拒绝向量，只检查规范资料的一致性。它们不能证明隔离有效、秘密已经销毁、取消成功、协议互操作或任何平台达到生产安全要求。

> **名称与口头边界：**contract 与 runner 各自都是一个完整的普通英语单词，已经按词首、职责和关键字语料接受；首次出现仍先写“一次会话的只读契约”或“受限运行边界”，防止读者混淆责任。日志不得用裸露的 `active=true` 合并目标激活、会话存活和权限有效。

- [查看 contract 开发者规范](../specifications/session-contract.html) — 按五步核对 SESSION-CORE 的会话建立责任。
- [查看权威与授权决定](../specifications/authority.html) — 区分长期授权、一次能力和最终决定。
- [查看有范围证据边界](adr-0022-evidence-and-appraisal.html) — 理解运行事件怎样进入证据与判断。
- [查看外部协议适配](adr-0026-external-protocol-adapters.html) — 固定 MCP、A2A 与远端任务的输入边界。
