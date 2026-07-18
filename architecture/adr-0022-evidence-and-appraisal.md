---
layout: architecture-decision
title: ADR-0022 · 先问证据能证明什么
page_role: content
footer_text: Noemion · ADR-0022
permalink: "/architecture/adr-0022-evidence-and-appraisal.html"
summary: 说明一项记录必须写明观察对象、方法、环境、时间和限制；缺少这些信息时，记录不能成为最终接受的依据。
decision_id: ADR-0022
page_heading: ADR-0022 · 先问证据 · 能证明什么
page_lead: 一项记录只有绑定精确对象、产生方法、运行环境、观察时间和已知限制，才能支持有限主张。来源可信、内容完整、验证有效、覆盖充分、目标满足和最终接受必须分别判断。
badges:
- 当前策略
- EVIDENCE-CORE 0.1.0-draft
- 尚无物理格式
- 尚未实现
previous_url: adr-0021-closure-and-activation.html
previous_label: ADR-0021
next_url: adr-0023-endem-content-standard.html
next_label: ADR-0023
---

## 用一次发布检查读懂证据链

团队准备发布一个服务。构建系统报告产物已经生成，测试平台报告用例通过，探针报告预发布环境可以访问；这些记录都重要，但没有任何一项能单独证明“可以发布”。

1. 固定发布对象与检查范围
2. 保留原始观察和产生方法
3. 形成有限主张与溯源关系
4. 按具名政策评估有效性
5. 对照全部判据计算覆盖度
6. 分别作出满足与接受决定

| 发布输入 | 最多支持的主张 | 不能直接推出 |
| --- | --- | --- |
| 构建记录 | 指定输入、构建器和环境生成了精确产物。 | 产物安全、测试充分或已经获准发布。 |
| 测试报告 | 指定版本在给定数据、方法和截止点下得到相应结果。 | 未测试环境、真实总体或未来运行仍有相同表现。 |
| 健康探针 | 指定端点在观察窗口内返回了约定响应。 | 所有实例持续健康，或业务目标已经满足。 |
| 模型评估摘要 | 指定模型、提示、样本和评估方法得到候选结论。 | 模型说明是直接观察，或统计结果自动取得决定权。 |
| 发布决定记录 | 具名权威在给定依据和政策下作出了决定。 | 决定本身证明所有依据真实，或授予新的权限。 |

这种有明确范围的证据记录，现行设计名称是 evidence。它不是日志包装、可信分数、数学证明或最终验收决定。

## 一项记录先要限定主体和主张

证据不能只凭自身宣告为真。开发者必须能够把记录与它声称描述的对象、产生过程和实际观察相比较；这一认识只提供设计方向，不能替代身份、溯源、撤销和权威规则。

| 记录责任 | 最低内容 | 常见错误 |
| --- | --- | --- |
| `EVIDENCE-SCP-001`<br>主体与范围 | 精确主体身份、有限主张、适用时间和声明范围。 | 只写名称、路径、“当前版本”或“系统正常”。 |
| `EVIDENCE-PRV-001`<br>生产与溯源 | 生产者、方法、版本、参数、环境、输入、父记录和有限无环派生图。 | 隐藏未知输入，或让记录循环引用自己来证明自己。 |
| `EVIDENCE-OBS-001`<br>观察与主张 | 分别保存原始观察引用、变换、结构化 `structured_observation` 和有限主张。 | 把推断、模型说明或工具成功冒充原始观察。 |
| `EVIDENCE-INT-001`<br>完整性 | 内容身份、生产者认证、序列与签名关系。 | 把签名有效理解为事实正确、覆盖充分或已经授权。 |
| `EVIDENCE-PRI-001`<br>披露与限制 | 丢失、过滤、脱敏、外部引用范围、时间边界和已知缺口。 | 保存令牌正文、实时能力句柄，或隐去信息损失。 |

主体、方法、环境或截止点变化时，原记录仍可作为历史事实，但不能无条件延伸到新对象和新条件。

## 观察、派生与来源类别不能互换

| 记录或来源 | 它说明什么 | 不能怎样升级 |
| --- | --- | --- |
| `observation`<br>`direct-observation` | 工具或传感过程直接取得指定对象的观察。 | 覆盖有限不能因记录量增加而变成总体事实。 |
| `derivation`<br>`deterministic-derivation` | 公开、可复现的变换从已知输入得到结果。 | 确定性不能补齐未知或不可信输入。 |
| `attestation`<br>`external-assertion` | 外部主体对有限事实作出可认证声明。 | 签名不能把外部声明变成直接观察。 |
| `appraisal`<br>`human-judgment` | 人员或机构依据具名政策给出评估。 | 职位、声誉或置信度不能扩大观察范围。 |
| `model-candidate` | 模型生成一项带来源、输入和限制的候选说明。 | 流畅文本、评分或重复采样不能让候选结论自证。 |
| `decision-record` | 记录具名权威已经作出的决定事件及其依据。 | 创建记录不会产生决定权，也不会改变历史依据。 |

`EVIDENCE-CLS-001` 要求记录种类与来源类别同时保留。它们分别回答“这项记录做了什么”和“依据怎样产生”，不能靠签名、置信度或人工确认互相替代。

## 有效、充分、满足与接受分别回答什么

| 判断层次 | 机器结果域 | 回答的问题 | 必须绑定 |
| --- | --- | --- | --- |
| 完整性与来源认证 | 由所选机制表达 | 内容是否改变，声明是否来自所称生产者？ | 内容身份、密钥、签名范围和认证政策。 |
| evidence 有效性 | `validity=valid / invalid / revoked` | 验证者当前是否允许这项记录进入后续判断？ | 验证政策、信任根、参考值、环境与截止点。 |
| 证据覆盖度 | `coverage=sufficient / insufficient` | 有效记录集合是否覆盖精确 `satisfaction_criteria` 的全部观察责任？ | 目标判据、不同责任、缺口、重复项和截止点。 |
| 目标满足 | `met / unmet / undetermined / fault` | `situation` 相对结构化观察得到什么结果？ | 比较契约、方向、范围和失败分类。 |
| 权威决定 | `accepted / rejected / deferred` | 具名权威是否接受、拒绝或推迟当前事项？ | 决定者身份、权限、依据、政策和决定范围。 |

`valid` 不是记录给自己的标签，而是外部评估结果；重复相同记录也不会增加覆盖责任。覆盖不足必须得到 `coverage=insufficient`，不能为了形成确定答案而降格为目标不满足。

> **名称与口头边界：**首次面向开发者应写“有范围证据记录（evidence）”。`valid / invalid` 与 `sufficient / insufficient` 只在前缀处有细小差异，日志必须带 `validity=` 或 `coverage=`，中文界面先使用“当前评估可用 / 评估无效 / 已撤回”和“覆盖完整 / 覆盖不足”。这些普通词已经按词首规则接受，精确日志仍需完整字段名避免职责混淆。

## 外部证明、遥测和模型评估只能提供什么

**复核日期：**2026-07-16。外部标准可以提供溯源、远程证明、构建来源、遥测字段和评估方法，但不能替 Noemion 决定本地主体、覆盖范围或最终权威。

| 外部资料 | 可采用的机制 | Noemion 不继承 |
| --- | --- | --- |
| [NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models) 与 [NIST AI 800-4](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation) | 区分评估构念、总体假设与部署后持续观察；受控评测不能替代真实环境监测。 | 不采用某种统计模型作为唯一方法，也不让基准结果自动覆盖生产环境。 |
| [W3C PROV Data Model](https://www.w3.org/TR/prov-dm/) | 分开 entity、activity、agent、派生和责任关系。 | 溯源图不证明主张真实，不采用 PROV 物理编码。 |
| [RFC 9334 RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html) | 分开 Evidence、验证者的 Attestation Result 与依赖方决定。 | 验证者不能替应用权威作出最终接受。 |
| [SLSA 1.2 Provenance](https://slsa.dev/spec/v1.2/provenance) | 记录构建定义、外部参数、解析后的依赖、运行细节和输出主体。 | 构建来源不能充当软件安全、行为正确或发布授权的通用证明。 |
| [GNU Guix 的 guix challenge](https://guix.gnu.org/manual/en/html_node/Invoking-guix-challenge.html) | 比较独立构建是否得到逐位相同的输出，可暴露不可复现或替代服务器风险。 | 结果不同不能单独判定哪一方正确。 |
| [OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/) 与 [OpenTelemetry GenAI 语义约定独立仓库](https://github.com/open-telemetry/semantic-conventions-genai) | 提供 Agent、模型、工具与 MCP 遥测字段，并提示参数和结果可能包含敏感信息。 | 遥测字段不定义证据身份、因果真实性或覆盖充分性。 |
| [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) | 禁止 token passthrough，并要求受众校验、范围限制和最小权限。 | evidence 不保存令牌正文或实时能力句柄，调用成功也不产生授权。 |

## 当前还不能编码或执行什么

现行十八个 evidence 提案向量覆盖九个允许分类与九个确定拒绝，只检查 EVIDENCE-CORE 九条抽象责任。它们不验证真实签名、遥测完整性、生产者可靠性或决定质量。

这项决定不表示采集器、验证器、归并器、决定引擎、inspector 或 runner 已经实现。evidence 也没有物理容器、文件扩展名、字段编号、摘要与签名算法、撤销分发或透明日志协议。

远程查询、跨生产者时钟归并、隐私政策语言、长期归档和实际消费者仍待研究。没有新 Profile、威胁证据与互操作实验前，不为了形式对称而创建格式。

- [查看证据规范](../specifications/evidence-entry.html) — 按开发者任务查询 EVIDENCE-CORE 九项责任。
- [查看测量与阈值](adr-0019-measurement-and-thresholds.html) — 先固定总体、方法、单位和不确定度。
- [查看组合闭包](adr-0021-closure-and-activation.html) — 理解证据所对应的精确目标和成员身份。
- [查看权威边界](../specifications/authority.html) — 区分证据评估、目标满足和最终决定。
