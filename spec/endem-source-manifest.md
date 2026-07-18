---
layout: spec
title: "Endem 实验来源清单 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/endem-source-manifest.html"
summary: "规定实验来源清单怎样记录人确认过的原文、解释和判断条件，再供未来 producer 形成含来源的 Endem；模型不能自行补字段。"
document_status: "实验性来源设计"
---
# Endem 实验来源清单

- 规范 ID：`END-SRCM`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：实验性 producer 输入草案；由 ADR-0014 采用
- 对象关系：只映射到 `END-P2`；不是 `.endem` 线格式，也不是稳定源语言
- 实现状态：只有来源样例；没有 producer 解析实现

## 1. 范围

来源清单记录未来 producer 需要的三类输入：解码并处理转义后的人的自然语言表达、已经确认的意义和判断条件，以及作出确认的主体与适用范围。它只保存已经形成的决定，不负责理解自然语言。

具名主体确认候选意义时，记录必须绑定来源、候选内容、语义位置、适用范围和截止点。AUT-CORE 把这项外部记录称为语义授权绑定；它只确认意义，不授予动作权限。

清单只产生含来源的 END-P2 形成制品，不定义最终发布 Profile 或裁剪结果。模型、界面和人工流程只能提出或确认上游输入；producer 不调用模型补字段，也不把候选自动升级为已确认意义。

清单采用 UTF-8、逐行、制表符分列的有限语法。它只服务首个 END-P2 纵向切片；以后若建立正式来源语言，应删除这一入口，不保留兼容垫片。

### END-SRCM-001 — 输入身份与编码有限

**要求：**输入 `MUST` 是 UTF-8，文件上限为 16 MiB，单行上限为 1 MiB。实现 `MAY` 接受 LF 或 CRLF，但必须把两者解释为相同的行边界。空行和第一个字节为 `#` 的行忽略；不得隐式裁剪其他空白。

**失败：**编码无效、文件或单行超限时，producer 必须在解析指令前拒绝，不能产生部分 Endem。

**验证依据：**合法 UTF-8、无效编码、超限文件、超限行、LF 与 CRLF 输入案例；未来实现还必须证明 producer 与 inspector 的边界。

**来源保真边界：**LF 与 CRLF 被解释为相同行边界，字段转义会被解码。因此 END-SRCM 只承诺把提交后的解码表达映射到 `source_expression.content`，不能声称逐字节保留原始 `.ends` 文件。若未来需要核对原始来源字节，必须另行绑定原始文件身份、解码 Profile、变换链和损失清单；当前 END-P2 不新增这些字段。

### END-SRCM-002 — 指令集合封闭

**要求：**每个非注释行由制表符分隔为指令和参数。只允许下表指令；未知指令、参数数量不符或单例重复必须拒绝。

| 指令 | 参数 | 基数 |
| --- | --- | ---: |
| `source_expression` | source_id, subject, media_type, language, version, content, range_start, range_length | 1 |
| `symbol` | id, kind, source_ref | 1..n |
| `relation` | id, predicate, projection_kind, projection_id, role_name=symbol... | 1..n；至少一个 role |
| `situation` | id, relation, polarity | 1..n |
| `root` | situation_id | 1 |
| `goal_direction` | mode | 1；END-P2 仅 `reach` |
| `structured_observation` | relation, match | 0..n；END-P2 仅 `same-roles` |
| `evidence_entry` | evidence_requirement_id | 0..n |
| `satisfaction_criteria` | on_missing, on_error, decision_authority | 1；END-P2 仅 `undetermined`, `fault` |
| `unresolved_meaning` | id, source_ref, conflict, decision_authority, candidates(csv), impact_scope(csv), resolutions(csv) | 0..n |

**失败：**指令或基数不符合时返回来源层诊断，并定位行号。

**验证：**`vectors/source/minimal.ends`；未知指令、错误参数数量和重复单例变异。

### END-SRCM-003 — 转义与复合字段无歧义

**要求：**字段只解释 `\\n`、`\\r`、`\\t` 与 `\\\\` 四种转义。role 必须写成 `name=symbol`。CSV 只用于标识符或登记枚举的有序输入；空字段表示空数组。标识符本身不得含制表符、换行、逗号或等号。

**失败：**未知或不完整转义、role 缺少等号、CSV 元素不符合 END-P2 类型时必须拒绝。

**验证依据：**合法转义、未知转义、不完整转义、role 分隔和 CSV 元素拒绝案例。

### END-SRCM-004 — 输入顺序不决定对象字节

**要求：**producer 必须先验证身份唯一性和引用闭包，再按 END-P2 规范顺序形成记录。`symbol`、`relation`、role、`situation`、`structured_observation`、`evidence_entry` 与 `unresolved_meaning` 的输入行顺序不得改变输出；重复身份不能靠后项覆盖。

**失败：**相同规范集合因输入顺序产生不同 `.endem` 字节，或重复身份被静默接受，均不符合本规范。

**验证依据：**最小清单映射到 `SV-VALID-MINIMAL-001`，并与 `WV-P2-SEMANTIC-ACCEPT-001` 的规范字节逐字节比较。

### END-SRCM-005 — 来源、候选与授权不能混合

**要求：**含来源的 END-P2 形成制品中，`source_expression` 保存来源文本；`symbol/relation/situation/root/goal_direction/satisfaction_criteria` 只保存确定性规则确认的投影，或具名主体已经确认候选意义、语义位置、适用范围和截止点的决定。AUT-CORE 把后一种记录称为语义授权绑定。存在多个可表达候选但尚无权选择时，输入者必须写入 `unresolved_meaning`。语义确认不得充当动作授权；模型输出不能直接充当 projection、decision_authority 或通过结论。未来裁剪发布 Profile 必须另行定义来源分离、引用重写和允许损失，不能把本清单的 `source_expression` 记录直接删去后沿用 END-P2 身份。

**失败：**没有允许投影时返回 `no_allowed_projection`；存在选择但未记录 `unresolved_meaning` 时按 `END-UNRESOLVED-001` 拒绝；producer 不尝试猜测。

**验证：**END-CORE 语义向量与人工授权边界复核。

### END-SRCM-006 — 失败原子且不扩大 Profile

**要求：**清单解析、END-P2 语义验证和对象写入必须形成单一事务边界。任何来源、类型、引用、排序或资源错误都不得留下部分 `.endem`。清单不能提高 END-P2 的字符串、图、嵌套或累计分配上限。

**失败：**任一阶段失败时只返回诊断，不返回部分可信模型或字节。

**验证依据：**END-P2 正反向量覆盖原子拒绝和资源上限；未来 producer 与 inspector 还必须分别证明实现行为。

### END-SRCM-007 — 实验入口不得冒充正式语言

**要求：**工具、文档和发行材料必须把 `.ends` 描述为实验性来源清单。它不是自然语言编译标准、不是 Endem 身份的一部分，也不承诺向后兼容。正式来源语言只有在具备注释、包含、版本演进、歧义、错误恢复和正反语料后才能取代它。

**失败：**任何稳定 ABI、通用自然语言理解或兼容性声明必须被发布检查拒绝。

**验证依据：**任何稳定语言、稳定 ABI 或兼容性声明都必须指向已发布的正式来源语言规范；当前不存在这样的规范。

## 2. 最小示例

最小接受样例位于 `vectors/source/minimal.ends`。它表达“为已登记项目生成安全评审报告”的来源文本、两个符号、一条关系、一个根事态和一个比较契约。该示例应确定性映射到语义向量 `SV-VALID-MINIMAL-001`，再由 producer 生成 `WV-P2-SEMANTIC-ACCEPT-001`。

`vectors/source/with-unresolved-meaning.ends` 在同一目标上增加“目标读者尚未确认”的未决项，明确列出候选读者、受影响关系、允许的解决方式与决定权威。它必须生成含一个非空 `unresolved_meaning` 的 `WV-P2-UNRESOLVED-MEANING-ACCEPT-001`；producer 不得替用户选择读者，也不得因为仍有未决项而丢弃整个目标。

## 3. 未决内容

本草案没有确定注释元数据、包含、模块、宏、变量、量化、时间、单位、求值表达式、错误恢复、格式化器或 IDE 协议。出现真实消费者前，不为这些能力预留语法。
