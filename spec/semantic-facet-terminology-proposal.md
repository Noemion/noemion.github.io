---
layout: spec
title: "Noemion 语义面与观察词去专名化研究提案 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/semantic-facet-terminology-proposal.html"
summary: "非规范研究提案，记录问题边界、证据、反例与停止条件。"
---
# Noemion 语义面与观察词去专名化研究提案

状态：非规范研究提案
日期：2026-07-14
结论状态：桌面审查完成；尚待人类验证
适用范围：`rhem / semion / skena / telis / krin / apor / phain` 的人类称呼、规范标识、来源清单、诊断位置、Profile 标签与公开解释

本提案不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求，不进入 `registry.json`。它不删除或合并现行六个语义面，不改变一个根事态、事态与目标方向分离、观察对齐、授权、满足判断、结果域或证据边界，也不创建组件实现。当前拼写在迁移决定前继续有效；候选普通词不是字段别名、兼容键、自动规范化结果或现行接口。

## 直接结论

Noemion 必须保留七项不同职责，但没有证据证明这七项职责必须使用七个希腊化短词。它们不是独立产品、制品或外部协议对象，而是一个 Endem 内部的六个语义面与证据记录中的结构化观察。普通、可组合的工程词能够更直接地恢复职责，并减少首次读者必须先查词源再理解规范的负担。

桌面审查建议把以下直白名称送入人类验证：

| 现行拼写 | 必须保留的职责 | 首选候选 | 中文直白称呼 |
| --- | --- | --- | --- |
| `rhem` | 保存提交给形成过程的来源表达、主体、媒介、版本和可重定位范围 | `source_expression` | 来源表达 |
| `semion` | 保存从来源记号到稳定符号、关系、角色和指称的已授权投影 | `meaning_projection` | 意义投影 |
| `skena` | 保存一个根、中性、可比较的可能事态 | `situation` | 事态 |
| `telis` | 保存目标要求事态达到成立或持续成立的方向 | `goal_direction` | 目标方向 |
| `krin` | 保存观察责任、结构比较、未知与故障处理及决定权威 | `satisfaction_criteria` | 满足判据 |
| `apor` | 保存仍可表达但尚未获授权解决的有限意义缺口 | `unresolved_meaning` | 未决意义 |
| `phain` | 保存由原始观察经显式变换形成、可与事态关系位置比较的结构 | `structured_observation` | 结构化观察 |

这些名称只替换称呼，不允许把七项职责压成 `prompt / intent / state / result` 等模糊字段。若后续证据支持该方向，候选还必须通过首次阅读、朗读、听写、职责匹配和反例验证，再由单独 ADR 一次性迁移现行规范、Profile、来源清单、向量、诊断与公开资料。

## 为什么边界成立不等于拼写成立

[ISO 704:2022](https://www.iso.org/standard/79077.html)分别连接对象、概念、定义和指称，并为术语与专名形成提供一般原则。它支持先固定概念边界，再审查用什么名称指称；它没有要求每个概念都使用新造词。

[GNU Coding Standards 的 Names 规则](https://www.gnu.org/prep/standards/html_node/Names.html)把全局名称视为一种注释，要求名称提供有用意义，并限制晦涩缩写。六个语义面会出现在规范、来源清单、诊断位置、手册和未来接口中，不是只在一个局部上下文出现的临时变量，因此不能用“短”抵消职责恢复成本。

[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)把需求工程过程、所需信息项、信息内容和格式分别处理。Noemion 不照搬该标准的数据模型，但它说明“要求的内容结构”和“字段怎样命名、呈现”是可分别治理的问题。

近期 AI 与互操作规范也倾向于用普通词、结构和描述共同承担可读性，而不是要求每个槽位都有专名：

- [MCP 2025-11-25 Schema](https://modelcontextprotocol.io/specification/2025-11-25/schema)分开程序 `name`、面向人的 `title`、`description`、输入输出 schema 与行为提示；提示仍不取得真实行为或授权权威。
- [A2A 1.0.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)用 `id / name / description / inputModes / outputModes / examples` 描述技能，并把 `Message`、`Task`、状态和上下文分开。
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)使用 `Govern / Map / Measure / Manage` 四个普通动词，并用类别、子类别、责任与证据说明精确边界。直白词不会自动造成语义粗糙；缺少定义和约束才会。

Noemion 因而应由普通字段名帮助读者定位，由 END-CORE 条款定义职责，由 Profile 封闭类型和枚举，由授权与信任边界强制约束。希腊词源可以保留在思想史和迁移 ADR 中解释设计来源，但不能继续充当接口可读性的前置条件。

## 七项职责不能合并

去专名化不是去结构化。以下每一对仍必须保持正交：

| 必须分开的内容 | 为什么不能合并 | 合并后的典型错误 |
| --- | --- | --- |
| `source_expression` 与 `meaning_projection` | 来源出现了什么，不等于这些记号已被授权为什么意义 | 把原句、模型解释或检索结果直接当成确认语义 |
| `meaning_projection` 与 `situation` | 符号和指称映射，不等于哪组关系构成可能事态 | 只有实体词表，没有可比较关系结构 |
| `situation` 与 `goal_direction` | 事态保持中性；达到、保持与否定极性分别表达 | 把禁止、希望或优先级混进事态图 |
| `goal_direction` 与 `satisfaction_criteria` | 目标方向只说明达到或持续；判据说明怎样观察和比较 | 把动作完成、单次采样或工具退出码当成满足 |
| `unresolved_meaning` 与观察不足 | 前者是形成时仍待授权的意义缺口；后者是运行时证据覆盖不足 | 用 `agno` 保存语义歧义，或用模型置信度关闭未决意义 |
| `structured_observation` 与证据记录 | 前者是可比较结构；记录还绑定主体、方法、环境、溯源和限制 | 一张关系图自证来源、有效性或充分性 |
| 满足判据与最终决定 | `met / unmet / agno / fault` 不是 `accepted / rejected / deferred` | 只因判据满足就冒充权威接受 |

[W3C PROV-DM](https://www.w3.org/TR/prov-dm/)把实体、活动、责任主体、派生、Bundle 与 Collection 分开，并说明 provenance 信息可用于评估质量、可靠性或可信度，而不是自行产生这些结论。这个边界支持 `source_expression` 继续保存来源与范围，但不让来源身份证明意义正确。

[W3C SOSA/SSN](https://www.w3.org/TR/vocab-ssn-2023/)使用普通词 `Observation`、`Procedure`、`FeatureOfInterest`、`Property` 与 `Result`，并把观察行为、观察对象、程序和结果分别连接。Noemion 的 `structured_observation` 不是 SOSA Observation 的直接同义词；引用该规范只说明“observation”可以保持直白，同时仍由结构、来源、方法和时间关系获得精度。

## 候选逐项审查

### `source_expression`

只用 `source` 会把文档、主体、存储位置、字节和解码文本混成一项；只用 `text` 又排除了非文本媒介和来源元数据。`source_expression` 明确指向进入形成过程的实际表达，同时要求附带主体、媒介、语言、版本和范围。它不能证明投影正确，也不等于原始来源字节。

### `meaning_projection`

只用 `meaning` 容易让载荷自称拥有客观意义；`semantic_mapping` 又容易被读成任意模型映射。`meaning_projection` 保留“从来源记号投向已登记符号、指称和关系位置”的方向性。是否获授权仍由确定性规则或外部权威证明，字段名本身不产生授权。

### `situation`

`state` 容易被理解为某个时刻的实际系统状态；`desired_state` 会把目标力量重新塞进中性关系结构；`scene` 又偏向视觉布景。`situation` 是最短且不预设实际、期望或已满足的候选。END-SIT 条款仍必须规定一个根、对象关系、角色、组合、极性和适用范围。

### `goal_direction`

`intent` 会混淆用户心理状态、授权与目标内容；`mode` 太宽；`force` 容易引入规范性力量。`goal_direction` 只回答事态要达到成立还是持续成立。现行 `kine / mene` 的发行词审查继续独立进行；若两项迁移都被接受，候选完整表达是 `goal_direction: reach / maintain`。

### `satisfaction_criteria`

只用 `criteria` 缺少判断对象；`validation` 常被理解为批准或使其有效；`acceptance_criteria` 又会把满足判断和最终决定合并。`satisfaction_criteria` 明确限制在事态与结构化观察的比较。它仍需保存观察责任、比较规则、未知与故障政策、所需证据类别和决定权威，但不能自行输出最终接受。

### `unresolved_meaning`

`uncertainty` 会混合语义歧义、测量不确定度和观察不足；`open_questions` 会吸收一般研究 TODO；`ambiguity` 又不能覆盖冲突授权与缺失判定责任。`unresolved_meaning` 限定为仍可表达、但尚未获授权选择或解决的有限意义缺口。无法形成任何允许投影仍是 `aseme`；运行观察不足仍是 `agno`。

### `structured_observation`

只用 `observation` 容易让原始事件、观察行为、处理后关系图和最终主张混成一项；`evidence` 又会跳过来源、有效性和覆盖评估。`structured_observation` 明确表示经过可定位变换、可与 `situation` 的关系位置比较的结构。原始观察、变换、记录、有效性、覆盖、满足和决定继续分别保存。

## 支持案例与反例

| 场景 | 候选表达 | 正确理解 | 失败信号 |
| --- | --- | --- | --- |
| 用户提交“服务整段窗口保持健康” | `source_expression` | 保存实际解码内容、来源和范围 | 字段名被理解成已确认目标 |
| 权威把“服务”绑定到登记主体，把“健康”绑定到关系 | `meaning_projection` | 保存有来源、有授权的符号与关系投影 | 模型候选直接写入确认投影 |
| 服务与健康关系构成一个根 | `situation` | 只描述关系与极性，不表达希望或保持 | 名称被解释成已观察到的实际状态 |
| 目标要求整段窗口持续成立 | `goal_direction: maintain` | 方向与时间连续性责任分开但相容 | 一次采样或会话完成被当成持续满足 |
| 判据要求每分钟完整覆盖且无已证实违约 | `satisfaction_criteria` | 预先固定观察责任与结果传播 | “criteria passed” 被解释成最终 accepted |
| “健康”存在两个已允许但未决的测量定义 | `unresolved_meaning` | 在形成阶段保留有限候选与决定责任 | 用 `agno`、多数票或模型置信度静默选一个 |
| 监测事件被映射到同一主体、关系和窗口 | `structured_observation` | 保存可比较结构与显式变换 | 关系图自称来源可信或证据充分 |
| 没有收到监测事件 | 不是 `unresolved_meaning` | 默认属于观察覆盖问题，可能产生 `agno` | 把空日志写成语义已经解决或负目标已满足 |

## 人类验证方案

验证遵守[术语与读音验证指南](../docs/terminology-and-pronunciation.html)，并同时比较“现行短词 + 直白解释”和“直白字段名 + 同一解释”。当前重点不是证明普通英语单词有词典读音，而是证明整组名称能恢复正确职责且不会诱导跨层推断。

发现阶段至少包含：

1. `source_expression / meaning_projection` 的来源与授权反例。
2. `situation / structured_observation` 的目标内容与实际观察反例。
3. `goal_direction / satisfaction_criteria` 的方向、判断和最终接受反例。
4. `unresolved_meaning / agno` 的形成时歧义与运行时观察不足反例。
5. `goal_direction: reach / maintain` 的完整字段和值语句。
6. 七项候选按固定顺序朗读、听写和重新排序，检查多词字段是否形成新的口头负担。

候选出现以下任一情况就不能通过：

- 首次读者持续把 `meaning_projection` 当成无须授权的模型输出；
- 把 `situation` 当成已观察事实或已满足状态；
- 把 `satisfaction_criteria` 当成最终接受条件；
- 把 `unresolved_meaning` 与 `agno`、测量不确定度或一般 TODO 混合；
- 把 `structured_observation` 当成完整证据、有效性或充分覆盖；
- 多词名称在普通技术对话中持续被截短到会改变职责的单词。

词典、TTS、ASR 和语音模型只能用于发现预期读法与异常转写，不能代替独立人类的职责匹配证据。

## 接受后的迁移边界

若后续证据支持该方向且人类验证通过，迁移 ADR 必须一次性处理以下范围，不保留旧入口：

1. 将 END-CORE 六语义面与 `phain` 的规范称呼替换为最终接受的普通名称，并同步条款正文、前缀审查、术语表和错误位置。
2. 发布新的封闭内容 Profile，直接替换来源清单键、语义向量外壳、Profile schema 名、诊断域和公开示例。
3. END-FMT 当前以记录类型码 `1..6` 和数字 map 键表达物理结构；名称迁移不得据此声称旧、新规范具有相同精确内容身份。身份语境包含对象规范与 Profile，迁移关系必须显式。
4. 同步 `required_phain` 等派生字段与 IKN-CORE、DRO-CORE、SYN-CORE、AUT-CORE 中的全部引用；不得双写或在读取器中接受旧键。
5. 更新站点、手册、图示、来源样例、测试路径和诊断目录；旧词只保留在 ADR-0010、迁移 ADR 与名称审计中作为历史证据。
6. 迁移测试只能证明新资料、Profile 与向量一致，不能证明 Ktisor、Theor、Drasor 或 CLI 已经实现。

最终字段拼写、条款前缀、Profile ID、规范版本和身份迁移关系不能由本提案提前冻结。若人类测试表明某个直白候选仍过宽，应优先增加职责限定词，而不是退回难读短词或用说明文档补救接口名称。

## 当前决定边界

本提案只形成四项候选结论：

1. 六个语义面与结构化观察的职责继续成立，不能合并。
2. `rhem / semion / skena / telis / krin / apor / phain` 没有通过专名必要性桌面门禁；词源不是接口可读性的证据。
3. `source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning / structured_observation` 是下一轮人类验证候选，不是现行字段、别名或 Profile。
4. 名称迁移即使不改变现有数字记录布局，也必须按新的规范与 Profile 身份处理，不能静默继承旧内容身份、签名、证据或接受状态。
