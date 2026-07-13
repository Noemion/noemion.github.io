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

当前资料还没有冻结 Noemion、Endem 和其他领域词的发行读音。此前的名称审查主要排查软件、包、命令、标准和权利冲突，不能证明一个词在中文或英语交流中读得顺、听得清、写得回。

[ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html) 已把目标语言读音和词表内口头区分设为独立门禁。`Iknem`、`Ktisor/ktise` 与 `kine/mene` 属于优先复核项；Endem 与 Synem 还要做成对听辨。项目完成 IPA、普通拼读提示、首次朗读和听写证据前，不用临时读法冒充正式读法。

[术语与读音验证指南](terminology-and-pronunciation.html)说明怎样招募独立参与者、组织材料、统计关键混淆并记录隐私边界。当前只有方案，没有人类研究结果。

这不会妨碍理解资料：每个专名第一次出现时都应先给出直白职责。读音提示将来只帮助人类交流，不会成为第二套命令、机器别名或语义权威。

## 六个语义面

| 字段 | 含义 |
| --- | --- |
| `rhem` | 来源实际出现的记号、语言和来源绑定 |
| `semion` | 记号到符号、指称、关系和作用域的已授权投影 |
| `skena` | 一个根对象—关系图，描述不带目标力量的中性可能事态 |
| `telis` | 目标要求事态达到成立（kine）还是持续成立（mene） |
| `krin` | 满足条件、观察类型、必需证据、未知处理和判断权威 |
| `apor` | 未决投影、冲突、测量和解决权限 |

一个 Endem 只有一个根 `skena`。只有没有未决项的 `apor` 可以为空；模型置信度不能把 `apor` 静默改成确定事实。结构无意义返回 `aseme`，观察不足返回 `agno`，二者不能混入 `apor`。

## 四个名词

- **[Endem](../specifications/endem.html)：**最小目标制品。
- **[Synem](../specifications/synem.html)：**两个或更多 Endem、固定依赖和发布范围形成的已解析闭包；单个自包含 Endem 不需要 Synem。
- **[Dromen](../specifications/dromen.html)：**Drasor 为一次 Drase 会话从精确制品、政策、环境、能力、预算和证据责任封存的只读执行契约；不是文件格式或可恢复权限。
- **[Iknem](../specifications/iknem.html)：**绑定目标、环境、方法和声明范围的证据记录；它不是数学证明，也不自动形成最终验收决定。

## 一个应用

唯一公开命令是 `endem`：

```text
endem ktise    endem elenk    endem pleko
endem theor    endem drase
```

一个命令入口不等于一个信任域。`theor` 背后必须使用不共享 Ktisor 生产解析代码的独立实现；`drase` 背后必须是隔离的最小权限进程。私钥位于外部签名系统，模型只提交候选和能力请求。

## 推荐阅读路径

1. [背景与边界](../about/background.html)：理解 Endem 与 Prompt、Skill 包、传统目标文件的区别。
2. [架构设计指南](architecture-guide.html)：理解 Endem → Synem → Dromen → Iknem。
3. [规范参考指南](specifications-reference.html)：区分已接受决定、待验证设计和开放问题。
4. [Endem 应用参考](endem-reference.html)：查看五个动作的消费者、失败责任和实施阶段。
5. [开发指南](development-guide.html)：了解最小纵向切片、Ktisor/Theor 差分和验证条件。

## 当前状态

> 词汇所指的职责与应用拓扑已经接受；具体发行拼写和读音仍受 ADR-0034 门禁约束。规范编码和实现尚未发布，也没有可安装的 `endem`、稳定扩展机制、ABI 或正式软件版本。

第一实现阶段只建设 `ktise`、`elenk`、独立 `theor` 和必需的内部符合性门禁。组合、发布、受控运行和模型适配必须等待前一阶段的安全与复现证据。
