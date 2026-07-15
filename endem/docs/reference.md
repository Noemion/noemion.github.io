---
layout: manual
title: "参考索引 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/reference.html"
manual_id: "endem"
manual_group: "reference"
manual_order: 5
manual_index_entry: true
nav_title: "参考索引"
page_heading: "参考索引"
page_lead: "按用户要做的事情查找计划中的命令动作，并核对每一步读什么、产出什么、失败时返回什么。"
summary: "查找五个动作、四类对象、状态、失败原因和对应规范来源。"
badges: ["参考", "CLI 待定"]
---

## 子命令索引

| 子命令 | 主要输入 | 主要输出 | 权限边界 |
| --- | --- | --- | --- |
| `ktise` | 受控来源、投影候选与具名决定 | nascent Endem、Ktise Iknem | 唯一规范写入入口 |
| `elenk` | 原始制品、层、限制和信任材料 | 分层结论、Elenk Iknem | Ktisor 的制品形成侧检查路径 |
| `pleko` | Endem、组合策略和依赖锁 | coherent Endem/Synem、Pleko Iknem | 不读取环境隐式依赖 |
| `theor` | 任意原始制品、视图和预算 | 只读视图、差分、诊断 | 独立 Theor，不生成 Ktisor 内部检查通过引用 |
| `drase` | 精确发布制品、适用外部陈述、验证政策、执行策略、后端与能力 | Dromen、会话结果和 Iknem | 隔离 Drasor，不拥有写入器；依赖方与具名权威分别决定准入和接受 |

**当前策略：**Endem 文件使用 `.endem` 扩展名。**待定内容：**参数、选项、退出码、Synem/Iknem 扩展名和安装接口。因此目前不能编写依赖具体参数的脚本。

## 制品与视图

| 名称 | 定义 |
| --- | --- |
| Endem | 具有一个根 `skena` 和六个语义面的最小目标制品 |
| Synem | 两个或更多 Endem 的已解析组合闭包 |
| Dromen | Drasor 为一次 Drase 会话封存的只读执行契约，不是文件或可恢复权限 |
| Iknem | 封装 phain、来源、范围、方法、限制或决定依据的证据记录 |

Endem 的规范分为三层：END-CORE 定义通用内容标准，END-P1 定义来源保留的形成 Profile，END-FMT 定义实验性物理容器。容器接受、Profile 接受和内容接受必须分别报告；最终发布还需要 ADR-0036 所要求的独立 Profile。详见 [ADR-0023](../../architecture/adr-0023-endem-content-standard.html) 与 [ADR-0036](../../architecture/adr-0036-source-bearing-and-stripped-release.html)。

## 状态索引

| 对象 | 状态 | 含义 |
| --- | --- | --- |
| Endem | `nascent` | 结构合法，但仍可能有 apor、引用或确认事项 |
| Endem | `coherent` | 必需引用、冲突、能力和验收关系已解析 |
| Endem | `attested`（现行草案） | 草案用一个值概括发布见证；实际签名陈述、主体摘要、验证政策、截止点、撤销和依赖方判断必须作为外部关系分别保存 |
| 满足判断 | `met / unmet / agno / fault` | skena 相对 phain 和 krin 的满足判断 |
| 权威决定 | `accepted` | krin 结果为 met、必需 Iknem 有效且覆盖充分，并且决定权威匹配 |
| 权威决定 | `rejected` | 具名权威依据 unmet 或预先登记政策作出否定决定 |
| 权威决定 | `deferred` | 尚无获授权的最终决定，或 agno、fault 与授权缺口仍未解决 |
| Drase 会话 | `completed` | 按声明终止规则结束；不说明目标是否满足 |
| Drase 会话 | `failed` | 系统、策略、对象、求值器或后端使会话无法继续 |
| Drase 会话 | `interrupted` | 取消、预算、环境、输入或授权条件使会话中断 |
| Iknem 有效性 | `valid / invalid / revoked` | 验证者在精确政策、参考值、环境和截止点下形成的外部评估 |
| 证据覆盖度 | `sufficient / insufficient` | 一组有效 Iknem 是否覆盖指定 krin 与观察责任；不按记录数量计算 |

现行规范值尚未迁移，因此参考索引仍列出 `attested`。开发者不得据此实现内容内布尔标志，也不得让签名存在直接产生会话准入；完整限制见 [Endem 生命周期](../../architecture/endem-lifecycle.html)与[生命周期及结果词边界研究提案](https://github.com/Noemion/noemion.github.io/blob/main/spec/lifecycle-and-result-terminology-proposal.md)。

## mene 时间索引

| 类别 | 值 | 含义 |
| --- | --- | --- |
| 时间范围 | `fixed` | 具名权威解析的 UTC 半开区间 `[start,end)` |
| 时间范围 | `elapsed` | 从具名事件开始、由单调时钟测量的固定经过时长 |
| 连续性 | `strict` | skena 在整个目标区间都必须成立 |
| 连续性 | `budgeted` | 只允许在累计、单次和次数预算内违约 |
| 覆盖缺口 | `agno` | 判据明确，但观测区间不完整或时间不确定度过大 |
| 时钟故障 | `fault` | 时钟、同步、适配器或求值器没有按契约完成 |

这些值由 ADR-0016 锁定为抽象语义，不是 END-P1 字段、CLI 参数或稳定 ABI。

## 测量与阈值索引

| 契约部分 | 必须固定 | 不能替代它的内容 |
| --- | --- | --- |
| 构念与总体 | 被判断关系、值角色、用途、固定或推广总体 | 基准名、排行榜、模型裁判 |
| 测量程序 | 生产者、版本、窗口、单位、纳入规则、最小样本、聚合器 | 仪表盘显示值、隐式单位、最新方法 |
| 阈值判断 | 比较器、阈值、有效不确定区间 | 比较前舍入、点估计、置信度标签 |
| 结果分类 | 区间一侧为 `met/unmet`，跨界为 `agno`，契约故障为 `fault` | 会话成功、证据数量、签名存在 |

这些边界由 ADR-0019 固定为抽象语义，不是 END-P1 字段或已实现求值器。

## 复合判断索引

- `all_of`：任一有效 `unmet` 决定总体 `unmet`；否则依次保留 `fault`、`agno`，全部 `met` 才满足。
- `any_of`：任一有效 `met` 决定总体 `met`；否则依次保留 `fault`、`agno`，全部 `unmet` 才反驳。
- `decisive-basis`：足以决定结果的已求值叶。
- `evaluation-coverage`：已求值叶、未求值叶、停止原因和所用 Iknem。

这些边界由 ADR-0020 固定为抽象语义，不是 END-P1 字段或已实现求值器。

## 否定与缺席索引

| 证据情况 | 结果 | 含义 |
| --- | --- | --- |
| 显式负观察 | 可支持 `met` | 保留目标的关系、角色和顺序，只改变极性 |
| 同构正反例 | `unmet` | 目标要求关系不成立，但观察表明关系成立 |
| 查询未命中 | 默认 `agno` | 只说明给定输入和查询中没有匹配 |
| 封闭范围内完整缺席 | 可支持 `met` | 权威、全集、路径、时间、枚举与损失边界全部有效 |
| 观察契约故障 | `fault` | 观察器、适配器或日志链没有按契约完成 |

这些分类由 ADR-0017 锁定为抽象语义。END-P1 只有原子负极性规范字节，没有封闭声明字段、CLI 参数或运行实现。

## 稳定失败类别

DIA-CAT 0.1 已登记跨对象诊断、END-P0 结构错误和首组 END-P1 语义错误；完整 CLI 诊断 ABI 尚待确定。未来实现还必须稳定区分以下更高层失败：

每项诊断都必须遵守 [DIA-CORE](../../specifications/diagnostics.html)：消息不承担机器身份，外部错误不直接成为本地结果，恢复分类不授予权限，阻断诊断不伴随部分可信成功。

- source invalid；
- contract incomplete；
- malformed object；
- unsupported required feature；
- resource limit exceeded；
- pleko unresolved；
- pleko conflict；
- permission widening；
- derivation preservation unproven；
- signature mismatch；
- load rejected；
- capability denied；
- backend failed；
- state drift；
- Iknem insufficient；
- implementation disagreement；
- reproducibility failed。

## 权威页面

- [Endem 规范](../../specifications/endem.html)
- [Synem 规范](../../specifications/synem.html)
- [Iknem 规范](../../specifications/iknem.html)
- [Endem 生命周期](../../architecture/endem-lifecycle.html)
- [ADR-0010](../../architecture/adr-0010-native-lexicon.html)
- [ADR-0015 判断与运行结果分层](../../architecture/adr-0015-result-domains.html)
- [ADR-0016 mene 时间与连续性模型](../../architecture/adr-0016-mene-time-model.html)
- [ADR-0017 否定事态与缺席证据](../../architecture/adr-0017-negation-and-absence.html)
- [ADR-0018 量化范围与集合成员资格](../../architecture/adr-0018-quantification-and-membership.html)
- [ADR-0019 测量谓词与阈值契约](../../architecture/adr-0019-measurement-and-thresholds.html)
- [ADR-0020 复合事态与判据组合](../../architecture/adr-0020-composite-situations-and-criteria.html)
- [ADR-0022 Iknem 证据范围与评估边界](../../architecture/adr-0022-iknem-evidence-and-appraisal.html)
- [ADR-0023 Endem 内容标准分层](../../architecture/adr-0023-endem-content-standard.html)
- [ADR-0024 Dromen 会话契约](../../architecture/adr-0024-dromen-session-contract.html)
- [Ktisor、Theor 与 Drasor](../../components/index.html)

## 外部工程资料

这些资料只提供机制先例，不定义 Endem ABI：

- [GNU `readelf` 手册](https://www.sourceware.org/binutils/docs/binutils/readelf.html)
- [GNU BFD 手册](https://sourceware.org/binutils/docs/bfd.html)
- [MCP 2025-11-25 当前修订（Current）](https://modelcontextprotocol.io/specification/2025-11-25)
- [A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)
- [OpenTelemetry 语义约定 1.43.0](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry GenAI 语义约定独立仓库](https://github.com/open-telemetry/semantic-conventions-genai)
- [智能体控制平面工程实践](https://openai.com/index/harness-engineering/)
