---
layout: "manual"
title: "入门指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 入门指南"
permalink: "/docs/getting-started.html"
manual_id: "docs"
manual_group: "start"
manual_order: 1
nav_title: "入门指南"
page_heading: "Noemion 入门指南"
page_lead: "用一个依赖升级案例，分清目标、协议状态、运行权限、证据和最终决定。"
summary: "用一个依赖升级案例，理解 Noemion 与 Agent 协议、授权和服务控制的边界。"
badges: ["Getting Started", "Noemion", "No Release Yet"]
---

## 从这里开始

Noemion 把自然语言目标变成可以持久保存、组合和独立检查的工程对象。它不替代 Prompt、Agent 工作流、MCP、A2A、身份系统或政策引擎；这些系统负责生成、编排、通信或授权，Noemion 负责固定“究竟要达到什么”和“依据什么接受结果”。

项目创造的核心词是 **Endem**：由 *end* 与表示“最小区别单位”的 *-eme* 合成，定义为“最小、独立有效、可验证的期望终态单元”。它不是缩写，也不是 `OBJ` 的新前缀。

Agent 正在从一次回答走向长时运行、工具调用和跨系统协作。2026 年启动的 [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)把互操作、安全、身份和授权列为重点；这些问题已经进入公开标准化议程，但连接成功仍不等于目标定义正确。

[A2A 1.0 规范](https://a2a-protocol.org/v1.0.0/specification/)已经分开 Task、Message、Artifact、流式更新和协议版本。[MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)仍是实验性能力；后续 [Tasks 扩展提案](https://modelcontextprotocol.io/seps/2663-tasks-extension)明确说明新设计与这套实验接口不具备线格式兼容性。协议可以演进，目标身份、验收判据和证据责任不能跟着某个外部状态模型漂移。

| 开发者正在处理的层次 | 这一层回答什么 | 不能直接推出什么 |
| --- | --- | --- |
| Prompt 或工作流 | 模型接收什么上下文，下一步调用什么 | 目标已经消除歧义 |
| MCP 或 A2A | 请求、Task、Message、Artifact 和协议状态怎样交换 | 外部 `completed` 等于目标满足 |
| 身份与授权 | 谁可以代表谁，对哪个对象执行什么动作 | 被授权的动作一定产生正确结果 |
| Noemion | 精确目标、约束、判据、证据范围和决定责任怎样保持稳定 | 运行权限、协议连接或服务控制已经具备 |

GNU 对网络服务的分析还提供了另一条必要边界：[客户端软件是否自由，与服务由谁实际运行和控制是两个问题](https://www.gnu.org/philosophy/network-services-arent-free-or-nonfree.html)。Noemion 借用这个区分来要求开发者说明执行者、数据路径、可观察范围和退出条件，不把 GNU 的伦理结论、许可证选择或 `SaaSS` 变成项目字段。开源客户端、成功的 API 调用和可导出数据，都不能单独证明用户控制了那次实际计算。

## 先看一个 Agent 工作

假设团队要求一个 Agent：“把服务依赖更新到安全版本，并确认它可以发布。”这句话适合开始协作，却还不是可验证目标。开发者至少要继续确定服务与仓库、目标版本、允许修改的范围、检查环境、发布判据和最终决定者。

Agent 可以调用 MCP 工具，也可以把工作交给 A2A 对端。协议状态只说明外部请求走到哪一步。即使外部 Task 显示 `completed`，本地仍要检查目标对象、实际改动、测试范围、安全结果和发布权威。

| 发生的事实 | Noemion 负责保留什么 | 还不能推出什么 |
| --- | --- | --- |
| 团队提交自然语言要求 | 原始表达、来源和仍待确认的对象或判据 | 模型猜测就是已确认意义 |
| 确定性形成目标制品 | 精确目标、约束、满足判据和未决信息 | 已获运行权限或工作已经完成 |
| 一次受限会话开始 | 当前对象、政策、环境、能力、预算和证据责任 | Agent 取得长期权限 |
| MCP 或 A2A Task 完成 | 带协议、版本和对端来源的外部状态与候选产物 | 目标已经 `met` 或最终 `accepted` |
| 检查与运行产生观察 | 绑定主体、方法、环境、范围和限制的记录 | 证据天然充分或事实永远有效 |
| 判据与具名权威分别判断 | 满足结果和最终决定各自保留输入与依据 | 一个“成功”覆盖全部结果域 |

这个例子只解释职责顺序，不定义命令参数、文件字段或协议映射。Noemion 当前要解决的核心问题，正是让目标、外部执行状态、观察证据和最终决定可以分别检查。

## 六个语义面

下表先写职责，再列现行字段名。字段名仍处于发行术语审查中；中文职责帮助阅读，不是别名或替代键。

| 职责 | 现行字段 | 不得混入 |
| --- | --- | --- |
| 来源表达 | `rhem` | 授权后的意义投影 |
| 已授权意义 | `semion` | 未经规则或具名权威确认的模型猜测 |
| 可能事态 | `skena` | 达到或保持的目标力量 |
| 目标方向 | `telis` | 事态本身；它只区分达到成立（kine）和持续成立（mene） |
| 满足判据 | `krin` | 命题自证；它必须固定观察、证据、未知处理和判断权威 |
| 待确认意义 | `apor` | 观察不足；它只保留未决投影、冲突、测量和解决权限 |

一个 Endem 只有一个根 `skena`。只有没有待确认项的 `apor` 可以为空；模型置信度不能把 `apor` 静默改成确定事实。结构无意义返回 `aseme`，观察不足返回 `agno`，二者不能混入 `apor`。

## 四个名词

- **[Endem](../specifications/endem.html)：**最小目标制品。
- **[Synem](../specifications/synem.html)：**两个或更多 Endem、固定依赖和发布范围形成的已解析闭包；单个自包含 Endem 不需要 Synem。
- **[Dromen](../specifications/dromen.html)：**Drasor 为一次 Drase 会话从精确制品、政策、环境、能力、预算和证据责任封存的只读执行契约；不是文件格式或可恢复权限。
- **[Iknem](../specifications/iknem.html)：**绑定目标、环境、方法和声明范围的证据记录；它不是数学证明，也不自动形成最终验收决定。

## 一个应用

设计中的命令行只保留一个入口 `endem`。五个动作分别负责形成、检查、组合、独立查看和受限运行；当前没有可执行命令或稳定参数。

| 设计动作 | 直白职责 |
| --- | --- |
| `ktise` | 从已确认的来源与语义形成 Endem |
| `elenk` | 分层检查实际制品字节 |
| `pleko` | 在存在真实多目标需求时形成完整依赖闭包 |
| `theor` | 通过独立读取路径查看和比较不可信制品 |
| `drase` | 在受限能力域中建立一次运行会话 |

一个命令入口不等于一个信任域。`theor` 背后必须使用不共享 Ktisor 形成侧解析代码的独立实现；`drase` 背后必须是隔离的最小权限进程。私钥位于外部签名系统，模型只提交候选和能力请求。

## 这些名字怎样读

Noemion、Endem 和其他领域词还没有正式发行读音。现有名称审查主要排查软件、包、命令、标准和权利冲突；它不能证明一个词在中文或英语交流中容易朗读、听辨和复述。

[ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html) 要求分别检查职责、书写冲突、读音稳定性和相邻名称的口头区分。`kine/mene` 没有通过桌面筛查，现行规范值暂时保留；`reach/maintain` 只是待人类验证的候选。`Iknem`、`Ktisor/ktise`、Endem 与 Synem 也仍需人类测试。项目取得 IPA、普通拼读提示、首次朗读和听写证据前，不用临时读法冒充正式读法。

[术语与读音验证指南](terminology-and-pronunciation.html)说明怎样招募独立参与者、组织材料、统计关键混淆并记录隐私边界。当前只有方案，没有人类研究结果。

这不会妨碍理解资料：每个专名第一次出现时都应先给出直白职责。读音提示将来只帮助人类交流，不会成为第二套命令、机器别名或语义权威。

## 推荐阅读路径

1. [背景与边界](../about/background.html)：理解 Endem 与 Prompt、Skill 包、传统目标文件的区别。
2. [架构设计指南](architecture-guide.html)：理解 Endem → Synem → Dromen → Iknem。
3. [规范参考指南](specifications-reference.html)：区分当前策略、正在研究和待定内容。
4. [Endem 应用参考](endem-reference.html)：查看五个动作的消费者、失败责任和实施阶段。
5. [开发指南](development-guide.html)：了解最小纵向切片、Ktisor/Theor 差分和验证条件。

## 当前状态

> 项目已经定义主要职责和应用结构；具体发行拼写和读音仍需完成 ADR-0034 的人类验证。规范编码和软件实现尚未发布；目前没有可安装的 `endem`、稳定扩展机制、ABI 或正式软件版本。

第一实现阶段只建设 `ktise`、`elenk`、独立 `theor` 和必需的一致性验证。组合、发布、受控运行和模型适配必须等待前一阶段的安全与复现证据。
