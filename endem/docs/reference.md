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
page_lead: "按开发任务查动作、对象、结果域、目标约束和诊断来源；该索引只说明现行设计，不提供尚未发布的命令参数。"
summary: "按开发任务查找形成、检查、组合和运行动作，以及各种结果、目标限制、错误说明和权威来源。"
badges: ["开发者索引", "CLI 待定"]
---

## 按工作查动作

| 要做的工作 | 动作 | 读取什么 | 产出与停止边界 |
| --- | --- | --- | --- |
| 从已确认解释形成目标制品 | `form` | 受控来源、投影候选与具名决定 | 形成来源保留的 formed Endem；它是 Endem 规范字节的唯一生产入口；意义未确认时停止 |
| 从生产侧检查制品 | `lint` | 原始制品、检查层、限制和信任材料 | 返回分层结论；不替代独立读取，也不产生外部接受决定 |
| 固定多个目标的组合闭包 | `compose` | Endem、组合策略和依赖锁 | 形成完整组合闭包；引用未解析、存在冲突或权限扩大时停止 |
| 独立查看实际字节 | `inspect` | 当前为实际 Endem 字节、精确规范/Profile、视图和预算；其他对象等待物理格式 | 返回带范围的只读视图、差分和诊断；independent inspector 不修复、不写回，也不生成生产检查通过结论 |
| 建立一次受限会话 | `run` | 精确发布制品、外部陈述、验证政策、执行策略、后端与能力 | 形成 session contract、会话结果和 evidence entry；bounded runner 不拥有写入器，准入与接受由各自具名权威决定 |

`endem` 计划作为唯一公开命令入口，表中的五个名称是动作标识，不是已经发布的 CLI。当前只确定 Endem 使用 `.endem` 扩展名；参数、选项、退出状态、安装接口以及 Endem closure 和 evidence entry 的物理格式仍待确定，开发者不能据此编写自动化脚本。

## 按对象查职责

| 对象 | 保存什么 | 不负责什么 | 当前物理状态 |
| --- | --- | --- | --- |
| Endem | 一个根 `situation` 及 `source_expression/meaning_projection/situation/goal_direction/satisfaction_criteria/unresolved_meaning` 六个语义面 | 不保存会话能力、最终接受或运行观察 | END-FMT 已有实验容器；END-P2 已有来源保留 Profile |
| Endem closure | 两个或更多 Endem 的已解析组合闭包 | 不在运行时补依赖或扩大成员权限 | 只有抽象语义，物理格式待定 |
| session contract | 一次 run 会话的只读执行契约 | 不是可转移文件，也不保存实时秘密或可恢复权限 | 只有抽象语义，序列化被明确禁止 |
| evidence entry | 有范围的观察、来源、方法、限制或决定依据 | 不自证有效，不替代满足判断与具名决定 | 只有抽象语义，物理格式待定 |

Endem 的通用内容、来源保留 Profile 和实验容器分别由 END-CORE、END-P2 与 END-FMT 负责。容器接受、Profile 接受和内容接受必须分开报告；最终发布还需要 ADR-0036 所要求的独立 Profile。详见 [Endem 内容标准分层](../../architecture/adr-0023-endem-content-standard.html)与[来源保留和裁剪发布](../../architecture/adr-0036-source-bearing-and-stripped-release.html)。

## 按结果域查状态

| 开发者要回答的问题 | 状态 | 不能据此推出 |
| --- | --- | --- |
| Endem 的结构和引用处理到哪一步 | `formed / resolved` | 目标已经满足、会话可以开始或权威已经接受 |
| 目标相对观察与判据是否成立 | `met / unmet / undetermined / fault` | 权威接受、会话完成或证据有效 |
| 具名权威作出了什么决定 | `accepted / rejected / deferred` | 目标真值、证据数量或运行成功 |
| run 会话怎样终止 | `completed / failed / stopped` | 目标已经满足或制品已经接受 |
| 一项 evidence entry 在精确政策和截止点下是否可用 | `valid / invalid / revoked` | 证据覆盖已经充分或主张为真 |
| 一组有效 evidence entry 是否覆盖指定判断责任 | `sufficient / insufficient` | 按记录数量投票或自动形成最终决定 |

外部陈述、验证政策、截止点、撤销状态与依赖方判断已移出内容状态。开发者不得实现内容内的签名通过布尔标志，也不得让签名存在直接产生会话准入；完整限制见 [Endem 生命周期](../../architecture/endem-lifecycle.html)。

## 按目标类型查约束

| 目标类型 | 形成前必须固定 | 何时保留不确定或故障 | 现行来源 |
| --- | --- | --- | --- |
| 固定时间或经过时间 | UTC 半开区间或具名事件与单调时钟，以及 `strict/budgeted` 连续性 | 覆盖不足为 `undetermined`；时钟、同步或求值契约失败为 `fault` | [ADR-0016](../../architecture/adr-0016-mene-time-model.html) |
| 否定关系或缺席 | 原关系的角色与顺序；证明缺席时还需权威、全集、路径、时间和损失边界 | 普通查询未命中默认为 `undetermined`；观察契约失败为 `fault` | [ADR-0017](../../architecture/adr-0017-negation-and-absence.html) |
| 量化与成员资格 | 关系模板、被量化角色、集合身份、成员资格权威、截止点和身份规则 | 范围不完整或成员观察不足为 `undetermined`；成员求值契约失败为 `fault` | `END-QNT-001` 至 `END-QNT-003`、[ADR-0018](../../architecture/adr-0018-quantification-and-membership.html) |
| 测量与阈值 | 构念与总体、程序与版本、窗口、单位、聚合器、阈值和不确定区间 | 样本或覆盖不足为 `undetermined`；程序、生产者或统计契约失败为 `fault` | [ADR-0019](../../architecture/adr-0019-measurement-and-thresholds.html) |
| 复合条件 | `all_of/any_of` 结构、每个叶的判据、决定性依据和求值覆盖 | 没有决定性结果时保留叶级 `fault`、`undetermined` 和未运行原因 | [ADR-0020](../../architecture/adr-0020-composite-situations-and-criteria.html) |

量化只允许 `all`、`some`、`at_least`、`at_most` 和 `exactly`，并按不同成员身份计数。空集合必须由具名权威明确允许；量化 `maintain`、嵌套量化和物理字段仍未确定。以上五类约束目前都是抽象语义，不是 END-P2 字段、CLI 参数或已实现求值器。

## 按失败层查诊断

| 先判断哪里失败 | 开发者应核对什么 | DIA-CAT 登记码示例 |
| --- | --- | --- |
| 来源 `source` | 编码、来源清单、范围和有损变换 | `endem.source.utf8`、`text.source.provenance_incomplete` |
| 结构与 Profile `structure/profile` | 固定前导、目录范围、记录形状、Profile 和预算 | `endem.wire.header.truncated`、`endem.wire.profile.limit` |
| 语义与闭包 `semantic/closure` | 六个语义面、引用、结果域和完整依赖 | `endem.semantic.reference`、`closure.closure.incomplete` |
| 会话与政策 `session/policy` | 主体、能力交集、预算、漂移、权威和截止点 | `session.environment.drift`、`authority.scope.amplified` |
| 证据与协议 `evidence/protocol` | evidence entry 范围、外部来源、协议版本、映射损失和取消语义 | `evidence.scope.unbound`、`adapter.error.provenance_lost` |
| 诊断系统 `internal` | 机器身份、主错误选择、披露、预算和原子失败 | `diagnostic.identity.unregistered`、`diagnostic.atomicity.partial_success` |

只有 [DIA-CAT](https://noemion.github.io/spec/diagnostic-catalog.html) 登记的机器码才能承担诊断身份。人类消息可以改写或本地化，但程序不得依赖其文本；外部错误也必须保留来源和协议版本，再映射到受限的本地诊断。阻断诊断只返回原子失败，后续层标为未运行；恢复分类不授予权限，也不执行副作用。

DIA-CAT 当前版本是 `0.1.0-draft`，只在绑定的规范、目录和提案向量中保持草案稳定，不是发行 ABI。CLI 退出状态、结构化编码、文本格式和持久日志均未确定。完整内容边界见 [DIA-CORE](../../specifications/diagnostics.html)与[ADR-0025](../../architecture/adr-0025-structured-diagnostics.html)。

## 按问题进入权威源

| 问题 | 先读哪里 |
| --- | --- |
| Endem 六个语义面、来源和实验字节 | [Endem 规范](../../specifications/endem.html)、[格式与成形](format.html) |
| 组合闭包和成员激活 | [Endem closure 规范](../../specifications/endem-closure.html)、[绑定与组合](binding.html) |
| 独立读取、生产检查和签名边界 | [安全与独立检查](safety.html)、[deterministic producer、independent inspector 与 bounded runner](../../components/index.html) |
| 会话建立、观察和受限运行 | [发布与运行](running.html)、[session contract 会话契约](../../architecture/adr-0024-dromen-session-contract.html) |
| 证据范围、有效性和覆盖度 | [evidence entry 规范](../../specifications/evidence-entry.html)、[ADR-0022](../../architecture/adr-0022-iknem-evidence-and-appraisal.html) |
| 结果域和生命周期限制 | [ADR-0015](../../architecture/adr-0015-result-domains.html)、[Endem 生命周期](../../architecture/endem-lifecycle.html) |
| 诊断内容、登记码和呈现边界 | [DIA-CORE](../../specifications/diagnostics.html)、[DIA-CAT](https://noemion.github.io/spec/diagnostic-catalog.html) |

[GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html)支持按开发者面对的问题组织参考资料，并要求专门术语在首次出现时得到说明；[GNU Errors](https://www.gnu.org/prep/standards/html_node/Errors.html)说明人类错误信息应提供程序、来源和位置语境。这些资料只提供文档与错误呈现原则，不定义 Noemion 的对象、结果域、机器码或 ABI。

## 当前可以证明什么

- 资料检查可以证明页面、规范、ADR、登记和提案向量没有已知引用冲突，不能证明组件已经实现。
- 当前只有 Endem 有实验性物理字节；Endem closure 与 evidence entry 仍不能交给 independent inspector 作实际字节读取。
- 五个动作的参数、退出状态和安装接口尚未发布，诊断目录也未成为稳定 ABI。
- `form`、`lint`、`compose`、`inspect`、`run` 仍是现行设计标识，尚无真实使用者读音、听辨和生态冲突证据。
- 项目尚未进入组件开发阶段，没有 deterministic producer、independent inspector、bounded runner、求值器或可执行 `endem` 可供安装。
