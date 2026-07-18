---
layout: content
title: evidence entry 有范围证据规范
page_role: content
footer_text: Noemion · evidence entry
permalink: "/specifications/evidence-entry.html"
summary: 说明一项有范围证据必须记录谁在何时、用什么方法观察了哪个对象，以及最多能支持什么结论。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 有范围证据记录 · evidence entry
page_lead: 记录谁在何时、用什么方法观察了哪个精确对象，并限定这项观察最多支持什么结论。
badges:
- EVIDENCE-CORE 0.1.0-draft
- 主张必须有范围
- 尚无物理格式
- 尚未实现
previous_url: session-contract.html
previous_label: session contract 会话契约
next_url: diagnostics.html
next_label: 结构化诊断
---

## 先判断一项信息能支持什么

有范围证据记录（设计阶段名称 evidence entry）说明生产者通过已声明的方法，对一个精确对象观察到了什么，以及这项记录最多支持哪一句主张。

假设目标是“更新服务依赖，并确认当前版本可以发布”。锁文件、部署接口、健康探针和模型说明都能提供信息，但它们的对象、方法和时间不同，不能压成一个“发布成功”。

| 取得的信息 | 当前可以支持 | 仍然不能推出 |
| --- | --- | --- |
| 锁文件中的版本与摘要 | 指定解析器从这个精确文件读到了哪些值 | 实际部署对象或运行状态 |
| 部署接口返回成功 | 指定接口在该时刻接受了请求 | 变更已经生效或目标实例正确 |
| 精确实例的健康探针响应 | 该实例在声明方法和时刻满足探针条件 | 完整观察窗口或全部发布判据已经覆盖 |
| 模型对日志的解释 | 保存为待核查的 `model-candidate` | 直接观察、事实真值、满足结果或最终决定 |

`satisfaction_criteria` 说明目标需要哪些观察；evidence entry 保留有限主张；验证者判断记录是否有效；具名权威最后决定是否接受。任何一层都不能替代下一层。

## 按四步形成并评估一项记录

1. 固定对象与主张
2. 保留观察与变换
3. 外部评估有效性
4. 计算判据覆盖度
5. 判断目标是否满足
6. 由权威作出决定

| 处理步骤与条款 | 开发者必须固定 | 失败时怎样处理 |
| --- | --- | --- |
| 1. 确定主张<br>`EVIDENCE-SCP-001` · `EVIDENCE-PRV-001` | 精确对象、有限主张、生产者及权限、方法、环境、时间、活动、输入、父记录和有限无环的派生关系 | 主体、方法或输入含糊时缩小或拒绝主张；路径、名称、当前对象和循环自证都不能补齐溯源 |
| 2. 保留观察<br>`EVIDENCE-OBS-001` · `EVIDENCE-CLS-001` · `EVIDENCE-INT-001` | 原始观察、解析、过滤、聚合、脱敏、模型解释、信息损失和结构化 `structured_observation`；记录种类、来源类别、内容身份与签名关系分别保存 | 推断不得冒充观察；签名、分数、数量或生产者自述不能把外部声明、人工判断或模型候选升级为更强类别 |
| 3. 外部评估<br>`EVIDENCE-VAL-001` · `EVIDENCE-PRI-001` | 验证者、政策、参考值、信任根、环境、截止点、撤销，以及外置对象、脱敏范围和对主张的影响 | `valid` 不是记录给自己的标签；政策或依据变化后重新评估，实时令牌、私钥、cookie 和能力句柄不得进入记录 |
| 4. 覆盖与决定<br>`EVIDENCE-COV-001` · `EVIDENCE-DEC-001` | 精确 `satisfaction_criteria`、关系位置、主体集合、时间范围、不同观察责任、满足结果、决定规则和具名权威 | 缺失路径、未知损失、开放集合或时间空洞输出 `insufficient`；`decision-record` 只记录已发生的决定，不创造决定权限 |

## 四个结果不能合并

| 结果域 | 允许值 | 回答的问题 |
| --- | --- | --- |
| evidence entry 有效性 | `valid / invalid / revoked` | 验证者是否在指定政策、环境和截止点下接受这项记录 |
| 证据覆盖度 | `sufficient / insufficient` | 适用记录是否覆盖精确 `satisfaction_criteria` 的全部观察责任 |
| 满足判断 | `met / unmet / undetermined / fault` | 目标要求与结构化观察比较后得到什么结果 |
| 权威决定 | `accepted / rejected / deferred` | 具名权威依据结果和决定规则作出什么决定 |

完整性只说明内容身份、来源或未检测到的修改；有效性取决于外部验证政策；覆盖度按不同观察责任计算，不按日志、签名或重试次数计算。四者都不能直接产生最终决定。

## 外部机制只提供有范围输入

| 外部机制 | 进入记录时固定什么 | 结论上限 |
| --- | --- | --- |
| [NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models) 与 [NIST AI 800-4](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation) | 评测目标、总体、样本、模型与版本、方法、假设、不确定性，以及部署环境和观察时段 | 基准分数不能外推到未声明总体；受控测试不能替代部署后观察，模型解释仍保持 `model-candidate` |
| [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) 与 [A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/) | 精确协议版本、对端、请求或 Task 身份、原状态、历史缺口、产物和取得时间 | 协议成功、Task `completed` 或流关闭不能直接推出授权、证据充分、本地满足或接受 |
| [OpenTelemetry 1.43.0](https://opentelemetry.io/docs/specs/semconv/) 与 [GenAI 独立仓库](https://github.com/open-telemetry/semantic-conventions-genai) | 仓库提交、Schema URL、字段稳定性、资源身份、时间和脱敏边界 | 遥测不能补齐未观测时段、因果责任或完整覆盖；Schema URL 也不等于稳定发布 |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/)、[RFC 9334 RATS](https://www.rfc-editor.org/rfc/rfc9334.html)、[SLSA 1.2](https://slsa.dev/spec/v1.2/verifying-artifacts)与 [GNU Guix `challenge`](https://guix.gnu.org/manual/en/html_node/Invoking-guix-challenge.html) | 精确实体、活动、责任、主体摘要、验证者、政策、信任根、独立构建结果、截止点和撤销 | 溯源不自行证明因果；验证者不替代依赖方；构建差异不能自动指定哪一方正确 |

**复核日期：**2026-07-16。模型评测、训练反馈、因果归因、检查点恢复和删除证明正在研究，分别见[模型评测](https://noemion.github.io/spec/model-assisted-evaluation-proposal.html)、[训练与更新](https://noemion.github.io/spec/model-training-and-update-boundaries-proposal.html)、[因果归因](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html)、[检查点恢复](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html)和[数据删除](https://noemion.github.io/spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.html)。关于“历史与检查点何时能支持证据？”这一问题，保存状态只说明生产者保留了什么，不恢复旧权限或补齐未知副作用。这些资料不修改 EVIDENCE-CORE。

## 规范来源与当前上限

- [EVIDENCE-CORE 规范源](https://noemion.github.io/spec/evidence-entry-core.html) — 主体、溯源、观察、类别、完整性、有效性、覆盖、决定与披露的唯一现行条款源。
- [当前草案威胁模型](https://noemion.github.io/spec/evidence-entry-threat-model.html) — 检查范围漂白、循环自证、类别升级、撤销失明、数量冒充覆盖和证据泄密。
- [非规范场景](https://noemion.github.io/spec/evidence-entry-scenarios.html) — 用支持案例、反例和边界场景检查九项责任；场景不是规范条款或实现证据。
- [提案向量](https://github.com/Noemion/noemion.github.io/blob/main/vectors/evidence-entry/cases.json) — 仅检查资料一致性，不能证明组件、安全性或稳定格式。
- [ADR-0022](../architecture/adr-0022-iknem-evidence-and-appraisal.html) — 解释采用理由、外部先例、限制和待定内容，不建立第二套条款。

**当前策略：**EVIDENCE-CORE 0.1.0-draft 只定义抽象证据与评估边界。物理容器、字段编号、摘要与签名算法、透明日志、撤销分发、远程查询、时钟归并、隐私语言和长期归档均未冻结。

**名称状态：**evidence entry 是由两个普通英语词组成的设计阶段职责名称，已经按逐词词首、职责和关键字语料接受。它仍不表示组件或物理格式已经实现；开发者首次说明时先写“有范围证据记录”，帮助读者直接理解责任。

**限制条件：**当前没有 evidence entry Profile，也没有相应的采集、验证、归并、撤销或决定实现。`spec/evidence-entry-core.md` 是唯一现行条款源；页面、场景和向量不能作为稳定互操作格式或组件符合性声明。
