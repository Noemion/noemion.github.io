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
hero_title: "Noemion 入门指南"
hero_description: "从 Endem 这个最小原语开始，理解目标怎样被形成、组合、装载与验收。"
summary: "从 Endem 这个最小原语开始，理解目标怎样被形成、组合、装载与验收。"
badges: ["Getting Started", "Endem", "No Release Yet"]
---

## 从这里开始

Noemion 试图为自然语言目标建立一种像目标文件之于传统计算那样持久、可组合、可独立检查的工程基础，但不会把传统对象术语和工具数量照搬过来。

项目创造的核心词是 **Endem**：由 *end* 与表示“最小区别单位”的 *-eme* 合成，定义为“最小、独立有效、可验证的期望终态单元”。它不是缩写，也不是 `OBJ` 的新前缀。

## 五组投影

| 字段 | 含义 |
| --- | --- |
| `say` | 来源实际出现的记号、语言和来源绑定 |
| `mean` | 记号到符号、指称、关系、作用域和力量的已授权投影 |
| `case` | 一个根对象—关系图，描述应成为、保持或避免的可能事态 |
| `when` | 满足条件、观察类型、必需证据、未知处理和判断权威 |
| `open` | 未决投影、冲突、测量和解决权限 |

一个 Endem 只有一个根 `case`。只有没有未决项的 `open` 可以为空；模型置信度不能把 `open` 静默改成确定事实。结构无意义返回 `no-sense`，观察不足返回 `unknown`，二者不能混入 `open`。

## 四个名词

- **[Endem](../specifications/endem.html)：**最小目标制品。
- **[Weave](../specifications/weave.html)：**两个或更多 Endem、固定依赖和发布范围形成的已解析闭包；单个自包含 Endem 不需要 Weave。
- **Frame：**sealed Endem 或 Weave 经 Runner 重新验证后形成的不可变加载态；不是文件格式。
- **[Witness](../specifications/witness.html)：**与 Endem/Weave、环境和策略绑定的证据与决定记录；不声称数学证明。

## 一个应用

唯一公开命令是 `endem`：

```text
endem form   endem check   endem bind   endem pack
endem seal   endem see     endem run    endem test
```

一个命令入口不等于一个信任域。`see` 背后必须使用与生产 Reader 不共享解析代码的独立实现；`run` 背后必须是隔离的最小权限进程。私钥位于外部签名系统，模型只提交候选和能力请求。

## 推荐阅读路径

1. [背景与边界](../about/background.html)：理解 Endem 与 Prompt、Skill 包、传统目标文件的区别。
2. [架构设计指南](architecture-guide.html)：理解 Endem → Weave → Frame → Witness。
3. [规范参考指南](specifications-reference.html)：区分已接受决定、待验证设计和开放问题。
4. [Endem 应用参考](endem-reference.html)：查看八个子命令的消费者、失败责任和实施阶段。
5. [开发指南](development-guide.html)：了解最小纵向切片、双 Reader 和验证条件。

## 当前状态

> 词汇与应用拓扑已经接受；规范编码和实现尚未发布。没有可安装的 `endem`、稳定扩展机制、ABI 或正式软件版本。

第一实现阶段只建设 `form`、`check`、`see` 和 `test`。组合、发布、受控运行和模型适配必须等待前一阶段的安全与复现证据。
