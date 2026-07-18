---
layout: architecture-decision
title: ADR-0014 · 实验来源清单边界
page_role: content
footer_text: Noemion · ADR-0014
permalink: "/architecture/adr-0014-source-manifest.html"
summary: 说明实验来源清单怎样把已确认的原文、解释和判断条件映射到 END-P2，而不让模型直接写入规范对象。
decision_id: ADR-0014
page_heading: ADR-0014 · 实验来源清单 · 输入与权威边界
page_lead: END-SRCM 用有限的逐行语法把已确认来源、意义投影和判断契约映射到 END-P2；它不是自然语言编译器，也不允许模型直接生成规范对象。
badges:
- 当前策略
- END-SRCM 0.1.0-draft
- 实验输入
- 无解析组件
previous_url: adr-0013-end-p1-payload.html
previous_label: ADR-0013
next_url: adr-0015-result-domains.html
next_label: ADR-0015
---

## 先判断来源清单能够证明什么

这份实验性来源清单只描述形成输入。它把解码后的自然语言和已确认结构放进封闭映射，不理解文本，也不决定动作权限。

| 层次 | 来源清单能够提供 | 不能据此声称 |
| --- | --- | --- |
| 来源表达 | UTF-8 文本、来源身份、版本和解码后的范围。 | 逐字节保留原始 `.ends` 文件。 |
| 意义投影 | 确定性规则确认的投影，或范围有限的语义授权绑定。 | 形成器有权替主体选择意义。 |
| 判断契约 | 观察要求、缺失政策、错误政策和决定权威选择器。 | 证据已经存在、目标已经满足或决定已经接受。 |
| 形成输入 | 确定映射到来源保留 END-P2 所需的封闭字段。 | 已经存在 deterministic producer、稳定 CLI 或最终发布物。 |

## 一项输入怎样进入 END-P2

1. 自然语言原始候选
2. 规则或主体确认意义
3. 未决选择保留 unresolved_meaning
4. END-SRCM封闭输入
5. END-P2确定映射
6. 独立读取另行验证

| 输入方式 | 为什么不能直接写入 | 当前处理 |
| --- | --- | --- |
| 自由 Prompt | 来源、候选解释、指令权和未决问题混在同一文本中。 | 原文进入 `source_expression`；已确认投影与 `unresolved_meaning` 分开记录。 |
| 模型 JSON | 结构合法仍可能事实错误、引用悬空、默认值漂移或越权。 | 模型只能在上游提出候选，禁止模型直接生成规范对象。 |
| 手写 CBOR | 可以绕过字段、排序、来源范围和引用检查。 | 来源清单不接受偏移、长度、记录 ID 或 CBOR 键等布局指令。 |
| 通用中间表示 | 会引入没有消费者的类型、扩展和隐式转换。 | 只保留当前 END-P2 向量能够验证的有限输入。 |

[MCP Sampling](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling)允许模型请求和工具循环，同时要求保留人工审查能力；它支持把模型输出留在候选层，不赋予候选规范写入权。

## 十种指令为什么保持封闭

| 输入职责 | 指令 | 封闭条件 |
| --- | --- | --- |
| 来源与符号 | `source_expression / symbol` | 一个来源记录；符号必须绑定来源范围。 |
| 关系与事态 | `relation / situation / root` | 关系至少有一个角色；事态与唯一根引用必须闭合。 |
| 目标与判据 | `goal_direction / structured_observation / iknem / satisfaction_criteria` | 当前只允许 END-P2 已登记的 `reach`、匹配方式和政策。 |
| 未决意义 | `unresolved_meaning` | 候选、冲突、影响范围、允许解决方式和决定主体必须显式。 |

每个非注释行使用制表符分列。字段只解释 `\n`、`\r`、`\t` 和 `\\`；未知指令、参数数量错误、重复单例或未知转义都必须拒绝。

> **名称边界：**“来源清单”是直白工程名称。`.ends` 只是机器可见的实验后缀，不是 Endem 身份、正式源语言或已经通过读音验证的发行名称。

## 语义确认与动作授权怎样分开

| 对象 | 谁能够确认 | 确认后仍不能做什么 |
| --- | --- | --- |
| 确定性投影 | 登记且适用的规则。 | 不能据此调用工具或发布制品。 |
| 需要判断的意义 | 对该来源、范围和截止点有权的具名主体。 | 不能把语义确认扩张为一般动作授权。 |
| 多个可表达候选 | 来源清单不选择；必须写入 `unresolved_meaning`。 | 模型、形成器和默认值都不能替主体关闭问题。 |
| 动作执行 | 未来 AUT-CORE 决定结合 session contract、政策和环境重新判断。 | 来源清单中的 `decision_authority` 选择器不能充当授权证明。 |

[NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)把自信但错误的生成内容列为生成式人工智能风险。该风险支持保留候选、确认者和失败责任，不定义 Noemion 的字段或授权结果。

## 确定性、来源保真和失败怎样验证

| 检查 | 必须成立 | 失败结果 |
| --- | --- | --- |
| 输入身份 | UTF-8、文件与单行上限先通过。 | 解析任何指令前原子拒绝。 |
| 输入顺序 | 相同规范集合按 END-P2 规则生成相同字节。 | 输入顺序改变字节即不符合 END-SRCM。 |
| 来源保真 | 明确 LF/CRLF 等价和转义展开造成的表示损失。 | 不得声称保存原始来源字节。 |
| 引用与资源 | 身份唯一、引用闭合，并保持 END-P2 全部上限。 | 不返回部分可信模型或部分 `.endem`。 |
| 现行证据 | 两个来源样例分别映射到已登记 END-P2 接受向量。 | 只能说明资料和向量一致，不是解析组件证据。 |

[GNU make 的规则模型](https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html)把 prerequisite、target 和 recipe 分开。Noemion 只采用“输入、产出和形成动作不得混写”的工程纪律，不把文件时间或 recipe 语义带入目标满足。

## 何时删除这一实验入口

正式来源语言必须先有真实消费者，并定义注释、包含、版本演进、歧义、错误恢复、格式化和正反语料。届时直接删除 END-SRCM 与 `.ends`，不保留别名、兼容解析或自动迁移。

若新任务无法由当前十种指令表达，应先回到 END-CORE 与新 Profile 判断职责；不得用隐式默认、自由脚本或模型补全扩大来源清单。

> **当前限制：**这里只有 END-SRCM 规范、两个来源样例和映射向量。没有 deterministic producer 解析器、实现仓库、稳定命令、通用自然语言编译或最终发布 Profile。

- [查看 END-P2 边界](adr-0013-end-p1-payload.html) — 确认来源清单实际能够映射哪些字段。
- [查看动作授权](adr-0029-authority-and-authorization-decisions.html) — 区分意义确认、能力与动作决定。
- [查看发布派生](adr-0036-source-bearing-and-stripped-release.html) — 理解为什么不能直接删除来源后发布。
- [查看验证职责](../development/testing.html) — 区分向量一致、实现证据与符合性声明。
