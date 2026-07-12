---
layout: "manual"
title: "规范参考 · Noemion 文档"
page_role: "content"
footer_text: "Noemion · 规范参考"
permalink: "/docs/specifications-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 6
nav_title: "规范参考"
hero_title: "Noemion 规范参考"
hero_description: "理解权威来源、成熟度标记，以及 Noema IR、Noema Object、Horizon Object 和 ADR 的阅读顺序。"
summary: "理解权威来源、成熟度标记，以及 Noema IR、Noema Object、Horizon Object 和 ADR 的阅读顺序。"
badges: ["Authority", "Maturity", "ADR"]
---

## 如何判断权威性

正式规范定义“必须是什么”；架构资料解释对象关系；指南提供阅读路径；FAQ 回答常见问题。发生冲突时，以已批准规范和 ADR 为准。

> **快速判断：**“现行设计”表示项目当前采用的边界，“待验证设计”表示仍可改变，“尚待确定”表示没有唯一结论。只有带版本的规范条款和经批准的 ADR 才能建立实现义务。

- 规范性要求使用必须、不得、只有等明确约束，并能对应测试或明确说明不可自动判定。
- 待验证设计不能因为出现在示例、工具页、论文草稿或 FAQ 中而升级为规范。
- 相同定义只保留一份权威规范，其他资料通过链接引用。
- 实现行为、实验结果和专利文本都不能反向替代规范定义。

[进入规范与成熟度登记](../specifications/)

## 成熟度标记

| 标记 | 含义 | 使用要求 |
| --- | --- | --- |
| 现行设计 | 项目当前采用的边界 | 变更需更新规范，必要时记录 ADR |
| 待验证设计 | 可评审的候选结构或流程 | 不得作为稳定接口依赖 |
| 尚待确定 | 证据不足或存在多个候选 | 保持未决，不制造默认答案 |
| 后续计划 | 超出当前实施范围 | 不得提前引入依赖或承诺发布日期 |

## Noema IR

Noema IR（NIR）表达目标、约束、偏好、歧义、推断权限、证据和验收条件。它不是二进制化提示词，也不是代理关键词表。

**尚待确定：**最小核心类型集、连续表示互操作、评价器接口和模型原生载荷边界尚未冻结。

[阅读 NIR 规范](../specifications/noema-ir.html)

## Noema Object

Noema Object（NOBJ）把 NIR 封装为可重定位对象。它包含可安全解析的 Header、Section、符号、类型化引用、完整性信息和装载视图。

**当前设计：**Section/Segment 双视图借鉴 ELF 工程策略，但不照搬传统机器指令语义。

**尚待确定：**最终对象名称、ABI 字段、Section 编号和重定位标识尚未冻结。

[阅读 NOBJ 规范](../specifications/noema-object.html)

## Horizon Object

Horizon Object（HOBJ）使用内容寻址依赖闭包、验收契约和披露图保存共享内容。Agent Harness 提交披露请求，Noema Object System 根据依赖、权限和策略建立只读视图，Fulfillment Runtime 只消费已经授权的视图。

调试剥离不得改变运行语义哈希；权限扩大必须显式授权；硬约束冲突必须失败。

[阅读 HOBJ 规范](../specifications/horizon-object.html)

## 开放问题与 ADR

开放问题集中保存在[架构开放问题](../architecture/open-questions.html)。格式、类型系统、执行语义、CLI、ABI、信任边界和兼容性选择一旦决定，应记录 ADR，说明背景、候选、决定、后果和替代方案。

当前公开架构已分别说明 [Agent Harness 的控制平面边界](../components/agent-harness.html)、[Fulfillment Runtime 的求解边界](../components/fulfillment-runtime.html)以及[发布包到运行证据的产物链](../architecture/noema-lifecycle.html)。这些解释帮助阅读，但具体结构定义、字段与行为仍需由正式规范和 ADR 冻结。

面向标准化时，规范条款还需关联互操作配置、正反样例、一致性测试、安全分析和版本演进规则；面向研究和知识产权时，应关联假设、现有技术、实验结果、贡献与公开披露记录。

**后续计划：**随着 Markdown 正式规范建立，HTML 将继续作为项目门户、解释层和阅读入口，而不承担唯一规范源。
