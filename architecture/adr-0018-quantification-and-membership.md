---
layout: architecture-decision
title: ADR-0018 · 先固定成员，再判断数量
page_role: content
footer_text: Noemion · ADR-0018
permalink: "/architecture/adr-0018-quantification-and-membership.html"
summary: 说明判断“全部”“至少”或“刚好”之前，为什么必须先固定成员范围、身份、权威和截止点。
decision_id: ADR-0018
page_heading: ADR-0018 · 先固定成员 · 再判断数量
page_lead: "“全部”“至少”“最多”和“刚好”只能对有权威、有截止点、身份唯一的成员集合求值；搜索结果、分页响应和重复记录都不能自行定义全集。"
badges:
- 当前策略
- 成员范围先于计数
- 不改变线格式
- 尚未实现
previous_url: adr-0017-negation-and-absence.html
previous_label: ADR-0017
next_url: adr-0019-measurement-and-thresholds.html
next_label: ADR-0019
---

## 用一次发布检查读懂量化

一个量化目标不是“对监控查询结果做计数”。“所有本次发布涉及的生产节点都健康”要求开发者先知道哪些节点属于“本次发布”。

1. 保留原句确认关系模板
2. 固定被量化角色成员资格权威
3. 锁定截止点建立唯一身份
4. 逐成员求值保留证据链接
5. 按量词聚合形成四值结果

| 开发者要固定的事实 | 本例 | 不能怎样补写 |
| --- | --- | --- |
| 关系与被量化角色 | `healthy(node)` 中只量化 `node`。 | 混入另一关系、环境或角色位置。 |
| 集合身份与权威 | 发布负责人确认的 `production-nodes`。 | 让监控查询、模型或 Agent 返回值定义集合。 |
| 模式与截止点 | 发布开始时锁定的 `enumerated` 清单。 | 求值期间静默加入或删除节点。 |
| 成员身份 | 按稳定 `node-id` 比较不同成员。 | 按日志行、显示名称或证据数量计数。 |
| 空集合政策 | 默认拒绝；只有具名权威可明确允许。 | 利用空真值自动得到 `met`。 |

## 成员集合必须先回答六个问题

| 范围契约 | 必须回答 | 失败方式 |
| --- | --- | --- |
| 关系模板与角色 | 判断哪个关系，且仅哪一个角色被量化。 | 谓词混合、角色错位或多变量绑定。 |
| 集合身份与权威 | 谁有权决定成员属于哪个集合。 | 查询结果或运行工具成为事实权威。 |
| 成员模式 | `enumerated` 完整清单，或 `rule-bound` 确定规则。 | 同时使用两种模式，或规则依赖未记录环境。 |
| 截止点 | 成员资格在哪个确定时点锁定。 | 分页过程中集合漂移，仍声称同一轮求值。 |
| 身份规则 | 怎样规范化并比较两个成员是否相同。 | 重复成员被静默去重，掩盖输入错误。 |
| 空集合政策 | 具名权威是否明确允许空集合参与判断。 | 缺少政策时沿用形式逻辑默认值。 |

`enumerated / rule-bound` 是现行草案的机器标签，不是新的哲学专名。人类界面应先显示“完整清单”或“确定规则”等职责说明；普通词只检查词首、职责和关键字冲突，只有新增自造名称才需要完整读音与口头区分验证。

## 五种量词怎样提前或延后决定

| 量词 | 可以提前决定 | 必须等待封闭范围 |
| --- | --- | --- |
| 全部 `all` | 一个不同成员的有效 `unmet` 决定总体 `unmet`。 | 全部成员为 `met` 才能决定总体 `met`。 |
| 任一 `some` | 一个不同成员的有效 `met` 决定总体 `met`。 | 全部成员为 `unmet` 才能决定总体 `unmet`。 |
| 至少 `at_least k` | `k` 个不同成员为 `met` 时决定总体 `met`。 | 少于 `k` 只有在完整求值后才能决定 `unmet`。 |
| 最多 `at_most k` | `k+1` 个不同成员为 `met` 时决定总体 `unmet`。 | 不超过 `k` 只有在完整求值后才能决定 `met`。 |
| 刚好 `exactly k` | 超过 `k` 个不同成员为 `met` 时决定总体 `unmet`。 | 恰好或少于 `k` 都必须等待完整求值。 |

后三种量词的 `k` 必须是非负整数。提前决定只减少不必要的求值，不降低证据要求；聚合结果仍须保存每个实际成员结果和对应 evidence entry。

## 不完整、重复与空集合怎样失败

| 输入或过程 | 处理 | 理由 |
| --- | --- | --- |
| 成员清单重复出现同一规范身份。 | 形成操作拒绝。 | 不得静默去重后把错误输入伪装成合法集合。 |
| 同一成员有多条日志、重试、签名或模型提及。 | 聚合时只按一个成员身份计数。 | 证据数量不是成员数量。 |
| 开放范围尚无决定性见证。 | `undetermined` | 未知成员不能被当作 `unmet`，也不能证明全称或上界。 |
| 成员求值发生故障，且尚无决定性结果。 | `fault` | 故障不是反例；已有决定性见证时仍保留故障成员记录。 |
| 空集合没有具名 `allow` 政策。 | 拒绝确定结论。 | 空集可能来自目录故障、过滤错误或同步延迟。 |
| 动态成员用于持续目标。 | 当前不受支持。 | 成员有效区间、变更政策与滚动闭包尚未固定。 |

## 外部查询和 Agent 列表只提供什么

| 外部资料 | 可采用的机制 | Noemion 不继承 |
| --- | --- | --- |
| [SHACL 2017 Recommendation](https://www.w3.org/TR/2017/REC-shacl-20170720/) 与 [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) | 最小、最大和形状约束提供局部基数机制；后者截至复核日仍是 2026 Working Draft。 | 草案特性不进入现行接口，RDF 值节点也不成为 Endem 成员。 |
| [OWL 2 Structural Specification](https://www.w3.org/TR/owl-syntax/) 与 [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/#Open_World_Assumption) | 精确基数依赖个体同一性，开放世界中的未陈述不等于不存在。 | 本体身份和开放世界推理不替代本地成员资格权威。 |
| [SPARQL 1.1 聚合](https://www.w3.org/TR/sparql11-query/#aggregates) | `COUNT(DISTINCT ...)` 计算查询解中的不同值。 | 查询解不是自动封闭的现实成员全集。 |
| [GNU Findutils 起点规则](https://www.gnu.org/software/findutils/manual/html_node/find_html/Starting-points.html) | 起点、递归、重复输入、提前退出和搜索期间变更都会影响结果。 | 一次文件搜索不能自行证明“所有对象已经检查”。 |
| [MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) | `tasks/list` 使用不透明游标分页，并受请求方授权上下文限制；该能力仍属实验性。 | 翻完分页只得到外部接收方可见列表，不产生本地全集、成员身份或权威。 |

这些标准和工具证明范围、唯一性、分页与完整性必须显式，但 Noemion 的结果域、空集合政策和信任边界仍由 END-CORE 自己规定。

## 当前还不能编码或执行什么

现行十二个量化提案向量覆盖六个允许分类和六个确定拒绝，只验证 END-QNT 三条抽象条款。本决定不增加 END-P2 字段，也不表示 deterministic producer、bounded runner、求值器或 CLI 已经实现。

嵌套量化、多变量绑定、量词与复合否定规范化、动态成员持续目标、超大集合证明、跨生产者成员合并、物理字段和规范字节仍需新 Profile、威胁分析与实现证据。

- [查看事态与量词](../specifications/endem.html) — 定位关系模板、角色和四值结果。
- [查看缺席证据](adr-0017-negation-and-absence.html) — 理解未找到成员或事件为何不等于不存在。
- [查看截止点与持续目标](adr-0016-mene-time-model.html) — 固定成员资格时间并识别动态范围限制。
- [查看组合边界](../specifications/endem-closure.html) — 区分成员计数与制品闭包组合。
