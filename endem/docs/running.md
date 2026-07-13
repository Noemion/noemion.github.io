---
layout: manual
title: "发布与运行 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/running.html"
manual_id: "endem"
manual_group: "running"
manual_order: 4
nav_title: "发布与运行"
page_heading: "发布与运行"
page_lead: "冻结发布载荷、核对外部签名，并在隔离 Praxor 中建立 Dromen 与 Tekmor。"
summary: "tasse、sphra、外部签名、Praxor、Dromen、能力循环与最终决定。"
badges: ["tasse", "sphra", "praxe"]
---

## tasse 冻结什么

`endem tasse` 读取 coherent Endem 或 Synem，以及发布配置、覆盖要求和调试策略。它产生不可变候选载荷、清单、签名请求和 Tasse Tekmor。

它可以外置不影响运行的调试和详细来源内容，但必须证明以下属性未改变：

- 每个根 `skena` 的关系、组合与极性；
- `telis` 的 kine/mene 与时间边界；
- `semion` 中所有符号、关系位置和作用域；
- `krin` 的满足条件、观察、证据和权威；
- 仍需运行处理的 `apor`；
- 绑定结果、能力上限和披露边界。

没有冻结的属性级等价规则时，`tasse` 应保守保留内容或失败。

## 外部签名与 sphra

私钥始终留在外部签名系统。流程为：

1. `tasse` 冻结候选并产生签名请求；
2. 外部系统验证授权并返回签名响应；
3. `sphra` 同时读取原候选、原请求和响应；
4. 验证载荷、算法、签名者和策略版本；
5. 在被签载荷之外附加签名包络，形成 attested Endem/Synem。

任何被签载荷变化都要求重新 tasse 和重新签名。签名有效只证明指定身份对指定字节作出签名，不证明语义正确或当前环境授权。

## praxe 的隔离域

`endem praxe` 是用户入口，实际工作由不拥有 Poiet 写入器的隔离 Praxor 完成。Praxor 先重新验证实际 attested 字节，再读取运行策略、后端绑定和能力目录。

> 预先生成的 Elenk Tekmor 不能替代对实际运行输入的重新检查。

## Dromen

Praxor 按 [ADR-0024](../../architecture/adr-0024-dromen-session-contract.html) 为一次 Praxe 会话封存 Dromen。Dromen 把精确 attested Endem 或 Synem 与政策、环境、非秘密能力描述、有限预算和证据责任绑定在一起；它不是文件，不进入发布包，也不包含凭据、token、文件描述符、网络连接或其他实时句柄。

对象、政策、权威、环境、能力、预算或证据责任发生实质变化时，旧 Dromen 失效。扩大权限必须建立新的 Praxe 会话。会话结束后，Dromen 和绑定的实时能力都不可再用；允许保留的记录不能恢复旧权限。

## 能力与反馈循环

1. 后端读取 Dromen 并返回候选或类型化能力请求。
2. Praxor 检查参数、权限、预算、副作用、幂等和当前状态。
3. Praxor 执行或拒绝请求，把真实结果规范化为 phain，再写入能力观察和 Praxe Tekmor。
4. 后端可以根据观察继续求解，但不能直接持有句柄或修改 attested 制品。
5. 重复失败、预算耗尽、状态漂移或需要价值判断时，Praxor 按预注册策略停止或请求外部权威。

## mene 时间与覆盖

`mene` 的运行时间不能来自隐式当前时间。`fixed` 范围读取具名权威已经解析的 UTC 半开区间；`elapsed` 范围从具名事件开始，并使用单调时钟测量固定时长。

- `strict` 要求整个区间成立；任何有效违约都产生 `unmet`。
- `budgeted` 必须同时声明累计、单次和次数上限；遥测空洞不消耗违约预算。
- Tekmor 保存覆盖区间、方法、时钟域、分辨率、不确定度、同步、重启与回拨事件。
- 覆盖空洞或只有离散采样时为 `agno`；时钟或适配器违反契约时为 `fault`。
- A2A Task、MCP 工具和远端遥测时间戳只作为外部事件，不能成为本地时钟权威。

抽象时间语义见 [ADR-0016](../../architecture/adr-0016-mene-time-model.html)。END-P1 当前只支持 `kine`；手册没有可执行的 mene 参数或时间字段。

## 否定观察与缺席

Praxor 必须把显式负观察、查询未命中和观察器故障分开。空日志、工具“未发现”或模型结论默认产生 `agno`，不能直接生成负极性 `phain`。

只有具名权威证明全集、所有角色路径、时间截止、完整枚举、迟到规则与损失边界均已封闭时，完整缺席才能在该有限范围支持 `met`。同构正反例产生 `unmet`；观察器未按契约完成产生 `fault`。完整边界见 [ADR-0017](../../architecture/adr-0017-negation-and-absence.html)。当前没有对应的 CLI 参数、日志收集器或求值实现。

量化目标还必须固定关系模板中的一个量化角色、集合身份、成员资格权威、截止点与身份规则。Praxor 只能按不同成员身份聚合；重复事件或证据不能增加基数，空集合不能默认产生满足。决定性见证或反例可以提前形成有限结论，其余结论需要封闭成员范围。完整边界见 [ADR-0018](../../architecture/adr-0018-quantification-and-membership.html)。当前没有成员目录、聚合器或量化求值实现。

测量目标还必须固定构念、适用总体、生产者、方法版本、观察窗口、单位与换算、纳入规则、最小样本、聚合器、阈值和不确定度政策。固定基准只能支持实际项目；推广结论必须绑定预注册统计模型。区间跨越阈值产生 `agno`，测量程序违约产生 `fault`。完整边界见 [ADR-0019](../../architecture/adr-0019-measurement-and-thresholds.html)。当前没有采集器、统计引擎或测量求值实现。

复合目标先判断是否仍是同一个不可分终态。若是，`skena` 和 `krin` 可以用对齐的 `all_of / any_of` 组合叶结果；若各部分能独立版本化、验收或失败，就必须拆成多个 Endem 与 Synem。决定性短路仍要保存依据、已求值叶、未求值叶、故障和 Tekmor。完整边界见 [ADR-0020](../../architecture/adr-0020-composite-situations-and-criteria.html)。当前没有组合求值实现。

Synem 会话激活只选择固定闭包中的成员，使用 `active / inactive / unresolved / error`，不映射为 `met/unmet/agno/fault`。激活依据必须引用精确结果事件、结果域和截止点；变化或撤销时重新检查或使会话失效。激活不能改变闭包身份或扩大权限。完整边界见 [ADR-0021](../../architecture/adr-0021-synem-closure-and-activation.html)。当前没有激活求值、事件订阅或 Praxor 实现。

MCP 和 A2A 只适合作为 Praxor 外缘的协议适配输入，所有具体映射必须遵守 [ADP-CORE 外部协议适配边界](../../specifications/adapters.html)：

- [MCP 2025-11-25 稳定规范](https://modelcontextprotocol.io/specification/2025-11-25)；后续正式版本只有完成兼容、安全、错误来源、降级和权限复核后才进入新适配基线
- [A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)

远端工具说明、Agent Card、任务状态、参数结构和返回内容均是不可信声明，不能直接成为能力授权、Endem 状态或最终决定。当前没有 MCP 或 A2A Profile 与适配器实现。

运行观测以后可以通过带版本的 [OpenTelemetry GenAI 语义约定独立仓库](https://github.com/open-telemetry/semantic-conventions-genai)导出。该约定仍在演进且 Schema URL 待定；输入、输出和工具数据可能含有敏感信息，因此默认不导出正文，外部字段也不构成 Tekmor 身份。

## Tekmor 与最终决定

Tekmor 记录有限的来源、检查、绑定、签名、运行或决定依据。它不等于数学证明，也不自动证明 claim 为真。每项记录必须绑定精确主体、主张范围和有限无环溯源，并分开原始观察、确定性派生、外部断言、人工判断和模型候选。

`valid / invalid / revoked` 由验证者在精确政策、参考值、环境和截止点下形成，不是记录的自填状态。`sufficient / insufficient` 只相对当前 `krin` 与观察责任计算；重复事件、证据数量、签名或模型评分不能补齐缺失范围。`decision-record` 只记录具名权威已经作出的决定，不产生决定权限。完整边界见 [ADR-0022](../../architecture/adr-0022-tekmor-evidence-and-appraisal.html)。当前没有物理 Tekmor 格式、采集器、验证器、归并器、撤销服务或决定引擎。

满足判断先区分 `met`、`unmet`、`agno` 和 `fault`。具名权威随后形成 `accepted`、`rejected` 或 `deferred`；Praxe 会话另行记录 `completed`、`failed` 或 `interrupted`。只有 `krin` 对适用 phain 的全部必需条件为 `met`、必需 Tekmor 有效且覆盖充分、没有阻断性 `apor` 且决定权威匹配时，才能形成 `accepted`。

这三个结果域不能互相替代。会话 `completed` 只说明运行按终止规则结束；它可以对应 `unmet` 和 `rejected`。验证器或后端故障产生 `fault` 或会话 `failed`，不能冒充目标本身 `unmet`。完整禁止推导见 [ADR-0015](../../architecture/adr-0015-result-domains.html)。
