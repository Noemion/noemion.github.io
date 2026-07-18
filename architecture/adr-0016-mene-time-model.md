---
layout: architecture-decision
title: ADR-0016 · 持续目标必须绑定时间证据
page_role: content
footer_text: Noemion · ADR-0016
permalink: "/architecture/adr-0016-mene-time-model.html"
summary: 说明持续目标必须同时明确时间范围、时钟来源、连续性规则和观察覆盖，零散时间戳不能代替这些条件。
decision_id: ADR-0016
page_heading: ADR-0016 · 持续目标必须绑定 · 时间证据
page_lead: "“保持成立”只有在时间范围、时钟来源、连续性政策和观察覆盖同时明确时才可判断；系统当前时间、任务时间戳或零散采样都不能替代这些条件。"
badges:
- 当前策略
- maintain
- 不改变线格式
- 尚未实现
previous_url: adr-0015-result-domains.html
previous_label: ADR-0015
next_url: adr-0017-negation-and-absence.html
next_label: ADR-0017
---

## 用一次部署检查读懂持续目标

“部署完成后十分钟内保持健康，允许累计中断不超过三十秒”不是一个定时器参数，而是一项需要形成、观察和判断的持续目标。

1. 保留原句确认目标意义
2. 绑定起始事件选择经过时长
3. 声明连续政策固定违约预算
4. 收集区间证据保留覆盖缺口
5. 比较判据形成四值结果

| 开发者要固定的事实 | 本例 | 缺少时怎样停止 |
| --- | --- | --- |
| 目标方向 | 现行草案值 `maintain`：事态在一段时间内持续成立。 | 只写“健康”不能推出持续要求。 |
| 时间范围 | 起始事件 `deploy.completed#42` 后 600 秒。 | 事件不唯一或时长含糊时保留待确认意义。 |
| 连续政策 | `budgeted`：累计 30 秒、单次 10 秒、最多 3 次。 | 任何预算项缺失都不能开始求值。 |
| 观察覆盖 | 由同一时钟域说明哪些区间被观察、哪些区间违约或缺失。 | 采样点之间没有保证时，不能补写成连续正常。 |
| 满足结果 | 完整覆盖且未超预算才是 `met`。 | 缺口为 `undetermined`，时钟契约失败为 `fault`。 |

> **当前名称：**`reach / maintain` 已作为直白、可恢复职责的普通英语枚举采用，并已通过词首、职责和关键字语料检查；它们不再设置完整人类读音门槛。

## 先决定固定时刻还是经过时长

| 范围 | 必须绑定 | 适用问题 | 确定拒绝 |
| --- | --- | --- | --- |
| 固定区间 `utc_window` | 开始、结束、具名时间决定权威，以及原始时间表达和解析依据。 | 发布窗口、维护时段或跨系统共享的确定区间。 | 默认本地时区、当前系统时间、相对日期、开始不早于结束。 |
| 经过时长 `elapsed_window` | 具名起始事件、正的固定长度、单调时钟域、时钟生产者和重启边界。 | 部署完成后十分钟、授权事件后三十秒等有界过程。 | 日历月或年、民用时钟差值、未声明的跨重启时钟值。 |

`utc_window` 在当前策略中使用 RFC 3339 的 UTC `Z` 形式保存确定瞬间；RFC 9557 的时区名、原始偏移、解析规则和数据库版本留在来源或决定依据中。`elapsed_window` 的单调时钟只能测量同一声明域内的经过时间，不能转换成绝对时刻或跨越未声明的重启边界。

## 再声明连续性与违约预算

| 政策 | 语义 | 最低声明 | 不能替代它的事实 |
| --- | --- | --- | --- |
| 严格连续 `strict` | 目标事态在整个范围内都成立。 | 目标范围、覆盖方法、适用时钟与最大不确定度。 | 健康采样点、一次成功探测或 Agent completed。 |
| 预算连续 `budgeted` | 只允许显式上限内的有限违约。 | 最大累计时长、最大单次时长、最大违约次数。 | 遥测缺口、丢失数据或未观察时间。 |

所有目标范围统一采用项目定义的半开区间 `[start, end)`。相邻范围共享端点但不重叠；空区间、开放端点、循环日历和闰秒词法仍不受支持。“采样”只说明证据怎样取得，不是第三种连续性政策。

## 证据覆盖怎样产生四类结果

| 观察与求值事实 | 结果 | 不得怎样改写 |
| --- | --- | --- |
| 覆盖完整、时钟有效，且没有违约或仍在全部预算内。 | `met` | 不能只因任务完成或最后一个采样健康而产生。 |
| 覆盖完整，观察到严格违约或任一预算上限被超过。 | `unmet` | 不能用后续恢复覆盖原违约区间。 |
| 存在覆盖空洞、只有离散采样，或不确定度跨越关键边界。 | `undetermined` | 不能插值为正常，也不能降成 `unmet`。 |
| 时钟、同步、适配器或求值器没有履行声明契约。 | `fault` | 不能把求值故障写成目标为假。 |

覆盖区间依照同一端点规则形成规范并集。可证明不改变含义的重叠、乱序和重复可以规范化；每个空洞都必须保留。时钟域、分辨率、不确定度、同步、重启、观察方法和覆盖保证属于 evidence entry 评价上下文，不是 Endem 自证字段。

## 外部时钟与 Agent 状态只提供什么

| 外部资料 | 可采用的机制 | Noemion 必须保留的边界 |
| --- | --- | --- |
| [RFC 3339](https://www.rfc-editor.org/info/rfc3339/) 与 [RFC 9557](https://www.rfc-editor.org/info/rfc9557/) | 可互操作的时刻表示，以及时区等附加信息。 | 项目自行选择 UTC 规范形式；时区解析不由运行机器默认值决定。 |
| [GNU C Library 时钟说明](https://www.gnu.org/software/libc/manual/html_node/Getting-the-Time.html)与[GNU Coreutils 相对日期说明](https://www.gnu.org/software/coreutils/manual/html_node/Relative-items-in-date-strings.html) | 单调时钟适合经过时长；相对日期受夏令时和日历语义影响。 | 单调时钟不能表示绝对时间，`now / today / tomorrow` 不能成为规范输入。 |
| [W3C OWL-Time](https://www.w3.org/TR/owl-time/) | 区分瞬间、区间、时长与时间参考系统。 | OWL 类和关系不会直接进入 Endem。 |
| [OpenTelemetry Metrics 数据模型](https://opentelemetry.io/docs/specs/otel/metrics/data-model/) | 数据点时间窗、重置、缺口和明确无记录状态。 | 其聚合区间端点规则不同，Gauge 只表示采样值；二者都不能直接证明本地连续覆盖。 |
| [MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) 与 [A2A 1.0](https://a2a-protocol.org/v1.0.0/specification/) | 任务创建、更新时间与外部生命周期状态。 | 远端时间戳和 completed 都不是本地时钟权威、evidence entry 覆盖或 `maintain` 满足结果。 |

## 当前还不能编码或运行什么

现行十二个 `maintain` 提案向量覆盖六个允许分类和六个确定拒绝，只证明抽象矩阵与三条 END-TIM 条款一致。本决定不增加 END-P2 字段，也没有计时器、监控器或求值组件。

物理字段、数值宽度、亚秒精度、闰秒时间尺度、循环日历和开放区间仍待设计。跨重启关联、时区数据库封装、观测压缩和多生产者归并也需要新 Profile、威胁分析、正反字节向量与两个独立解释路径。

- [查看结果域](adr-0015-result-domains.html) — 区分未知、故障、未满足与最终决定。
- [查看证据边界](../specifications/evidence-entry.html) — 理解时钟和覆盖为什么需要独立评价。
- [查看未来运行责任](../components/runner.html) — 定位会话时钟与目标判断之间的边界。
- [查看现行名称规则](adr-0037-terminology-simplification.html) — 区分普通时间词与自造名称的检查范围。
