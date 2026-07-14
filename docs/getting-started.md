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
page_lead: "先理解 Noemion 为什么存在，再认识 Endem 及目标的形成、组合、装载与验收。"
summary: "先理解 Noemion 为什么存在，再认识 Endem 及目标的形成、组合、装载与验收。"
badges: ["Getting Started", "Noemion", "No Release Yet"]
---

## 从这里开始

Noemion 为自然语言目标建立持久、可组合、可独立检查的工程基础。传统目标文件提供了重要类比，但项目不会照搬它的术语、机器指令语义或工具数量。

项目创造的核心词是 **Endem**：由 *end* 与表示“最小区别单位”的 *-eme* 合成，定义为“最小、独立有效、可验证的期望终态单元”。它不是缩写，也不是 `OBJ` 的新前缀。

## 这些名字怎样读

Noemion、Endem 和其他领域词还没有正式发行读音。现有名称审查主要排查软件、包、命令、标准和权利冲突；它不能证明一个词在中文或英语交流中容易朗读、听辨和复述。

[ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html) 要求分别检查职责、书写冲突、读音稳定性和相邻名称的口头区分。`kine/mene` 没有通过桌面筛查，现行规范值暂时保留；`reach/maintain` 只是待人类验证的候选。`Iknem`、`Ktisor/ktise`、Endem 与 Synem 也仍需人类测试。项目取得 IPA、普通拼读提示、首次朗读和听写证据前，不用临时读法冒充正式读法。

[术语与读音验证指南](terminology-and-pronunciation.html)说明怎样招募独立参与者、组织材料、统计关键混淆并记录隐私边界。当前只有方案，没有人类研究结果。

这不会妨碍理解资料：每个专名第一次出现时都应先给出直白职责。读音提示将来只帮助人类交流，不会成为第二套命令、机器别名或语义权威。

## 六个语义面

下表先写职责，再列现行字段名。字段名仍处于发行术语审查中；中文解释帮助阅读，不是别名或替代键。

| 字段 | 含义 |
| --- | --- |
| `rhem` | 来源实际出现的记号、语言和来源绑定 |
| `semion` | 记号到符号、指称、关系和作用域的已授权投影 |
| `skena` | 一个根对象—关系图，描述不带目标力量的中性可能事态 |
| `telis` | 目标要求事态达到成立（kine）还是持续成立（mene） |
| `krin` | 满足条件、观察类型、必需证据、未知处理和判断权威 |
| `apor` | 待确认投影、冲突、测量和解决权限 |

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

## 推荐阅读路径

1. [背景与边界](../about/background.html)：理解 Endem 与 Prompt、Skill 包、传统目标文件的区别。
2. [架构设计指南](architecture-guide.html)：理解 Endem → Synem → Dromen → Iknem。
3. [规范参考指南](specifications-reference.html)：区分当前策略、正在研究和待定内容。
4. [Endem 应用参考](endem-reference.html)：查看五个动作的消费者、失败责任和实施阶段。
5. [开发指南](development-guide.html)：了解最小纵向切片、Ktisor/Theor 差分和验证条件。

## 当前状态

> 项目已经定义主要职责和应用结构；具体发行拼写和读音仍需完成 ADR-0034 的人类验证。规范编码和软件实现尚未发布；目前没有可安装的 `endem`、稳定扩展机制、ABI 或正式软件版本。

第一实现阶段只建设 `ktise`、`elenk`、独立 `theor` 和必需的一致性验证。组合、发布、受控运行和模型适配必须等待前一阶段的安全与复现证据。
