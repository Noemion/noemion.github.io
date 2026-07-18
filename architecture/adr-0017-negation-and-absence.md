---
layout: architecture-decision
title: ADR-0017 · 没有记录不等于没有发生
page_role: content
footer_text: Noemion · ADR-0017
permalink: "/architecture/adr-0017-negation-and-absence.html"
summary: 区分否定事实、查询无结果、日志缺口和观察故障，说明什么证据才足以支持“没有发生”。
decision_id: ADR-0017
page_heading: ADR-0017 · 没有记录 · 不等于没有发生
page_lead: 否定事实、查询无匹配、日志缺口和观察故障回答不同问题；只有显式负观察或有权威、可证明完整的封闭范围，才能支持“没有发生”。
badges:
- 当前策略
- 范围先于缺席推断
- 不改变线格式
- 尚未实现
previous_url: adr-0016-time-evidence.html
previous_label: ADR-0016
next_url: adr-0018-quantification-and-membership.html
next_label: ADR-0018
---

## 用一次越权检查区分四种情况

目标“匿名主体没有读取私有报告”否定的是 `read(actor, resource)` 关系。审计日志里没有匹配行，只能说明当前查询没有找到记录。

1. 保留原句确认被否定关系
2. 固定主体、角色时间与观察范围
3. 区分直接观察缺席或故障
4. 检查封闭声明寻找正极性反例
5. 形成 met / unmetundetermined / fault

| 实际得到的事实 | 可支持的结果 | 理由 |
| --- | --- | --- |
| 具名权威直接确认同一主体没有读取权限。 | 对负极性 `can_read` 目标可为 `met`。 | 这是显式负观察，但不能自动证明没有实际读取事件。 |
| 可用审计日志中没有匹配读取记录。 | `undetermined` | 日志范围、旁路、迟到和丢失仍未封闭。 |
| 全部适用路径被完整枚举，且截止点后仍无匹配。 | 在声明范围内可为 `met`。 | 缺席由有界、充分的完整性证据支持。 |
| 发现同一 actor/resource 的有效读取记录。 | `unmet` | 正极性反例直接反驳负目标。 |
| 采集器、日志链或适配器没有按契约完成。 | `fault` | 求值失败不能改写成目标为假或事件未发生。 |

## 否定仍保留同一关系与角色

| 职责 | 允许表达 | 禁止替代 |
| --- | --- | --- |
| 关系身份 | `meaning_projection` 只登记一次 `read(actor, resource)`。 | 另造 `not_read`、`cannot_read` 或删除关系节点。 |
| 事态极性 | `situation` 引用同一关系，以 `positive / negative` 明确极性。 | 交换 actor/resource、用空列表或自然语言“没有”暗示否定。 |
| 目标方向 | `goal_direction` 仍只使用现行 `reach / maintain` 草案值。 | 再增加 `avoid / forbid`，把否定编码两次。 |
| 当前编码上限 | END-P2 只支持原子关系的显式极性。 | 自行执行复合否定、双重否定或德摩根变换。 |

这一设计保留了哲学上的最小区分：关系成立与不成立都谈论同一组对象，而否定不是一个新对象。工程规则仍由 END-CORE、Profile 和向量决定；局部资料不可能据此冒充“全部世界事实”。

## 无匹配为什么默认是未知

| 输入状态 | 结果 | 必须保留 |
| --- | --- | --- |
| 同一关系、同一角色的有效显式负观察。 | 可支持 `met` | 生产者权威、主体范围、方法和截止点。 |
| 开放数据、部分索引、缓存或模型检索没有返回匹配。 | `undetermined` | 实际查询、数据集身份、分页、过滤和已知缺口。 |
| 观察或适配契约失败。 | `fault` | 故障主体、影响范围、原因和未完成步骤。 |
| 同构的有效正极性反例。 | `unmet` | 原事件与比较依据；更多空查询不能抵消反例。 |

外部 Agent、MCP 工具、检索器或模型的“未发现”只是一项带来源的运行声明。它不能单独成为负极性 `structured_observation`，也不能取得语义确认、证据充分性或最终决定权。

## 缺席证据必须先封闭什么

所谓封闭观察范围，封闭的是一项有限观察任务，不是现实世界。缺少正极性反例只有在下列条件同时成立时，才可支持负目标。

| 封闭项 | 必须证明 | 缺失时 |
| --- | --- | --- |
| 权威与全集 | 谁有权声明封闭；枚举哪些主体、关系、对象和环境。 | `undetermined` |
| 全部角色路径 | 直接访问、代理、缓存、批处理和旁路都已覆盖。 | `undetermined` |
| 时间与截止点 | 观察区间明确，迟到记录在何时不再可能出现。 | `undetermined` |
| 完整枚举方法 | 数据不是采样、部分索引、分页截断或提前结束。 | `undetermined` |
| 损失与排除 | 丢失、过滤、去重、撤销、未知值和明确排除项均可核对。 | 未知为 `undetermined`；契约失效为 `fault`。 |

完整性被撤销、发现旁路或出现迟到反例时，只能追加新评价并使旧结论失效；不得原地删除证据或保留已经不成立的 `met`。

## 外部查询与日志机制只证明什么

| 外部资料 | 可采用的边界 | 不能推出 |
| --- | --- | --- |
| [W3C OWL 2 Primer](https://www.w3.org/TR/owl-primer/#Open_World_Assumption) | 开放世界中未陈述的事实可能只是缺失，而非为假。 | 不把 OWL 个体、SHACL Shape 或 RDF 数据集直接变成 Endem 字段。 |
| [W3C SHACL 封闭约束](https://www.w3.org/TR/shacl/#ClosedConstraintComponent)与 [SPARQL 1.1 NOT EXISTS](https://www.w3.org/TR/sparql11-query/#neg-notexists) | SHACL 只对焦点节点允许的属性作封闭限制；查询没有匹配只说明该查询范围。 | 形状 closed 或图模式无匹配都不证明日志源和现实世界完整。 |
| [GNU grep 退出状态](https://www.gnu.org/s/grep/manual/html_node/Exit-Status.html) | 0 表示有选中行，1 表示无选中行，2 表示错误；输入和选项决定结果含义。 | 一次无匹配不能越过搜索范围成为普遍否定；静默模式也不能替代错误检查。 |
| [OpenTelemetry Logs 数据模型](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | 事件发生时间、观察时间、来源和属性可以分别保存。 | 这份数据模型本身不证明日志流完整。 |
| [MCP 2025-11-25 Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 协议错误、工具执行错误和工具结果保持可区分。 | 工具成功、空结果或模型总结不产生负事实、完整性或动作授权。 |

## 当前还不能实现哪些缺席判断

END-P2 已有 `positive / negative` 枚举和一个负极性规范字节向量；本决定不增加 END-P2 字段。十二个否定提案向量只验证六个允许分类与六个确定拒绝，没有日志收集器、策略引擎或求值器。

复合与量化否定、双重否定规范化、封闭声明物理字段、跨生产者完整性合并、迟到窗口、撤销传播、负观察签名和隐私保护仍需新 Profile、威胁分析与实现证据。

- [查看事态与结果](../specifications/endem.html) — 定位关系、极性、观察与四值判断。
- [查看证据边界](../specifications/evidence-entry.html) — 理解有效性、覆盖度和撤销怎样分开。
- [查看时间证据](adr-0016-time-evidence.html) — 为观察区间和迟到截止点建立边界。
- [查看 Agent 边界](agent-system-boundaries.html) — 避免把工具返回提升为本地事实。
