---
layout: spec
title: "Endem Core Content Standard · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/endem-core.html"
summary: "规定一件 Endem 在编码前必须满足的内容结构、意义确认、状态、身份和安全读取要求，并限制 Profile 能表达什么。"
document_status: "规范草案"
---
# Endem Core Content Standard

- 规范 ID：`END-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：内容标准草案；条款化表达 ADR-0010 至 ADR-0023 已接受的语义、安全与规范分层边界
- 物理编码：存在 `END-FMT 0.1.0-draft` 实验性草案；尚非稳定 ABI
- 实现状态：仅有规范向量检查器；Ktisor、Theor、Drasor 与 CLI 均未实现

## 1. 范围

本规范是 Endem 的通用内容标准。它定义一个 Endem 在进入物理编码之前必须满足的最小语义、授权、状态、身份和安全读取要求，并约束任何 Profile 能够表达什么、不得改写什么。它约束未来 Ktisor、制品形成侧读取器、独立 Theor 与规范向量，但不选择文本语法、二进制布局、魔数、字段宽度、记录编号、摘要算法、签名算法或稳定 ABI。

本规范不定义模型提示、推理过程、训练方法、运行计划、实时能力句柄或最终人工价值判断。模型只能提供候选，不能成为规范写入器或唯一验收权威。凡声称 `semion` 已获授权、`apor` 已被解决或决定主体具有权限，还必须固定并符合 `AUT-CORE` 的精确版本；END-CORE 不重复定义主体、委托、同意或重放规则。

### 1.1 规范分层与权威顺序

Endem 采用三层规范，不把容器合法、字段闭合和内容成立混成一种“有效”：

1. `END-CORE` 是通用内容标准，定义六个语义面、关系不变量、授权、状态、结果和信任边界；
2. `END-FMT` 是容器标准，定义固定前导、记录目录、确定性编码和有界读取；
3. `END-P*` 是内容 Profile，定义某个版本实际允许的字段、枚举、组合、资源上限和规范顺序。当前 `END-P1` 是首个封闭内容 Profile。

ADR 只记录为何采用这些边界；`spec/registry.json` 只登记精确版本、条款与验证关系；场景和向量只提供审查与符合性证据。它们都不得建立第二套内容语义。发生冲突时，Profile `MUST NOT` 放宽或改写 `END-CORE`；它只能在声明版本内收窄能力、补齐字段和增加可验证约束。

### 1.2 内容对象

一个 Endem 内容对象由且仅由一个版本化 Profile 下的六个语义面及其闭合引用构成。精确内容身份来自指定身份域中的规范字节，不来自授权决定、文件名、路径、模型会话、签名者声誉或容器解码成功。物理文件是内容对象的确定性序列化；授权、签名、证据和最终决定只能通过精确伴随关系解释该对象，不能反向改写其字节身份。

每个内容 Profile `MUST` 明确列出：适用的 `END-CORE` 与 `END-FMT` 精确版本、必需和允许字段、字段类型与枚举、规范排序、引用闭包、资源上限、允许状态、拒绝未知能力的规则，以及对应正反向量。没有这些信息的字段集合只是内部数据结构，不得被称为 Endem 内容标准。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

一个实现只有在固定本规范 ID、精确版本和适用 Profile，并满足所有适用 `MUST` 与 `MUST NOT` 条款后，才能声明符合性。END-P0 只支持结构实验；END-P1 是首个封闭内容 Profile，但两者都不得声明稳定字节互操作。

### END-CON-001 — 固定规范身份

**要求：**符合性声明 `MUST` 绑定 `END-CORE`、精确版本与适用 Profile；`MUST NOT` 使用“最新版本”、环境搜索或未记录的默认值解析正式输入。

**失败：**规范、版本或 Profile 缺失、未知或不匹配时，读取或形成操作必须失败，且不得产生部分可信 Endem。

**验证：**注册表一致性检查；未来 `conformance:conformance-identity` 测试。

### END-CON-002 — 不虚构线格式兼容

**要求：**在线格式成为稳定 ABI 前，实现 `MUST NOT` 把语义向量 JSON、内部结构、调试导出、示例 YAML 或 END-FMT 实验字节声称为稳定 `.endem` 编码。

**失败：**任何发布或互操作声明若不能定位到已冻结格式规范，必须被发布检查拒绝。

**验证：**仓库内容检查；具名规范维护者复核。

### END-CON-003 — 接受层次不得互相提升

**要求：**符合性报告 `MUST` 分别说明容器接受、Profile 接受与 `END-CORE` 内容接受；任何一层未执行、失败或版本不匹配时，`MUST NOT` 宣称后续层已经通过。内容接受也 `MUST NOT` 被解释为目标已满足、制品已签署、会话可运行或权威已接受。

**失败：**通用 CBOR 解码、目录检查、字段闭包或签名验证被单独描述为“有效 Endem”时，发布检查必须拒绝该符合性声明。

**验证：**`tests/spec_contract_test.py` 的规范层次契约；未来 `conformance:layered-conformance-report` 测试。

### END-CON-004 — 内容 Profile 必须封闭

**要求：**每个内容 Profile `MUST` 绑定精确规范版本并封闭字段、类型、枚举、规范顺序、引用、资源上限、状态和未知能力处理。Profile `MUST NOT` 重新定义六个语义面的职责、把可选扩展静默升级为必需能力，或依赖未登记的环境默认值完成解释。

**失败：**同一 Profile 身份在不同实现、时间或环境下接受不同字段含义，或未知字段被忽略后仍宣称完整内容接受时，必须拒绝。

**验证：**`spec/profiles/end-p1.json`、`tests/p1_payload_test.py` 与 `tests/spec_contract_test.py`；未来 `conformance:profile-semantic-closure` 测试。

### END-CON-005 — 扩展必须证明消费者与失败边界

**要求：**新增内容字段、枚举、记录、组合或 Profile 前，提案 `MUST` 说明不可替代价值、上游生产者、下游消费者、信任与失败责任、规范化规则、未知能力行为、资源上限、威胁、支持案例、反例和正反向量。没有真实消费者或不能确定性验证的扩展 `MUST NOT` 进入现行内容标准。

**失败：**仅为名称对称、未来想象、模型便利或内部实现细节增加正式内容时，规范评审必须停止或删除该扩展。

**验证：**登记与资料一致性检查；具名规范维护者复核；未来每个新 Profile 的独立向量集。

### END-CON-006 — 外部前置条件必须显式报告

**要求：**符合性报告 `MUST` 分开记录由当前 `.endem` 字节直接证明的容器与 Profile 结论，以及依赖外部规则、授权、身份、签名或 Iknem 的内容结论。未取得、未执行、版本不匹配、已撤销或无法精确绑定的外部前置条件 `MUST` 标为未满足或未求值；`MUST NOT` 由文件内名称、环境搜索、缓存成功或调用者断言补齐。一个 Profile 若不能单独承载完整内容接受所需的前置条件，`MUST` 明确声明其单文件最高可声称层次。

**失败：**读取器把 `projection.id`、`decision_authority`、`required_iknem`、签名者名称或本地 ACL 命中解释为外部义务已经完成，或在报告中省略未执行层次时，内容接受声明无效。

**验证：**`SCN-028` 至 `SCN-030`；语义向量的外部前置条件矩阵；`spec/profiles/end-p1.json` 的声明上限；未来 `conformance:external-conformance-prerequisites` 测试。

## 3. 最小语义结构

### END-CORE-001 — 一个根事态

**要求：**一个 Endem `MUST` 具有且只能具有一个根 `skena`。两个能够独立实现、验收或失败的根目标 `MUST` 分成两个 Endem，再由 Synem 表达关系。

**失败：**根缺失、根不唯一或无法确定根时，形成操作必须拒绝并定位根集合。

**验证：**`SV-VALID-001`、`SV-REJECT-ROOTS-001`。

### END-CORE-002 — 六个语义面

**要求：**Endem `MUST` 按 `rhem`、`semion`、`skena`、`telis`、`krin`、`apor` 的固定逻辑顺序表达六个语义面。没有未决项时，`apor` `MUST` 是显式空集合，不得省略。

**失败：**任一语义面缺失、重复或被另一语义面代替时，形成操作必须拒绝。

**验证：**`SV-VALID-001`；未来 `conformance:facet-presence` 测试。

### END-SRC-001 — 来源可重定位

**要求：**`rhem` `MUST` 保存来源主体、媒介、语言、版本与可重定位绑定。含来源的形成 Profile `MUST` 保存实际进入形成过程的解码内容；最终发布 Profile `MUST NOT` 保存原始自然语言或足以无损重建它的内容，并 `MUST` 明确采用何种分离来源绑定。来源身份、外部引用或伴随资料存在 `MUST NOT` 被解释为投影正确性的证明。

**失败：**来源范围越界、摘要不匹配、编码无效、形成 Profile 不能按声明重放，或发布 Profile 仍泄露原始自然语言、留下悬空来源引用或声称单文件可以核对已分离来源时，必须拒绝。

**验证：**`SV-VALID-001`；ADR-0036 设计复核；未来 `conformance:source-range-and-digest` 与 `conformance:source-stripped-release-profile` 测试。

### END-PUB-001 — 形成制品与裁剪发布制品分离

**要求：**包含原始自然语言的形成制品与移除来源内容的发布制品 `MUST` 是两个精确对象。裁剪发布 Profile `MUST` 定义保留的语义结构、被删除或降精度的全部文本槽、来源引用的重写规则、资源上限、披露边界和失败责任；它 `MUST NOT` 直接删除 `rhem.content` 后沿用含来源 Profile、让 `semion` 或 `apor` 引用悬空，或把外部来源伴随资料当作运行所需权限。当前 END-P1 只承担含来源的形成与审查，不是最终发布 Profile。

**失败：**裁剪后对象沿用来源身份、签名、Iknem、接受状态或能力，发布文件仍含原始自然语言或可逆副本，运行语义依赖被删除范围，或没有来源材料时仍声称已经独立核对原始表达到目标结构的忠实性，发布必须拒绝。

**验证：**ADR-0036、ID-REL-001 与 `vectors/identity/cases.json`；未来发布 Profile 的正反字节向量、两条独立裁剪路径和 `conformance:source-stripped-release-profile` 组件测试。

### END-SEM-001 — 投影必须获得授权

**要求：**`semion` `MUST` 把来源记号映射到稳定符号、指称、关系、角色、作用域和来源位置。每项确认投影 `MUST` 可追溯到确定性规则或范围有限的具名授权。

**失败：**候选投影没有授权、指称没有来源或作用域依赖默认推断时，不能进入确认的 `semion`。

**验证：**`SV-VALID-001`、`SV-REJECT-AUTHORITY-001`。

### END-SIT-001 — 事态保持中性

**要求：**`skena` `MUST` 只表达对象、关系、角色、组合、极性与适用范围；`MUST NOT` 混入希望、保持、禁止、优先级或模型置信度等目标力量。

**失败：**事态节点包含目标力量，或只有实体而没有可比较关系时，形成操作必须拒绝。

**验证：**`SV-VALID-001`、`SV-REJECT-FORCE-001`。

### END-CMP-001 — 复合根仍必须是一个不可分终态

**要求：**一个复合根中的所有关系叶 `MUST` 共同描述同一个终态，使用同一 `telis`，并共享不能独立拆开的实现、替换、授权、验收与失败责任。任一部分若能独立版本化、实现、替换、接受、拒绝或失败，就 `MUST` 形成独立 Endem，再由 Synem 表达依赖和组合。自然语言中的“并且”或“或者” `MUST NOT` 单独决定边界。

**失败：**两个独立交付物、不同验收权威或不同生命周期目标被包进一个复合根，或一个不可分终态被任意拆分以绕过整体判据时，形成操作必须拒绝并定位边界冲突。

**验证：**`SCN-024` 与 `SCN-025` 设计审查；`vectors/composition/cases.json`；未来 `conformance:composite-root-boundary` 组件测试。

### END-CMP-002 — 组合结构必须有限无环并与叶判据对齐

**要求：**第一阶段复合节点只允许 `all_of` 与 `any_of`，每个节点 `MUST` 有至少两个不同子节点；整个结构 `MUST` 有限、无环且不得重复引用同一叶。子节点顺序 `MUST NOT` 承载语义。每个 `skena` 关系叶 `MUST` 在 `krin` 中有且只有一个对齐的叶判据，`krin` 的组合拓扑 `MUST` 与 `skena` 一致。原始 `phain` `MUST` 先按叶判据产生叶结果，再进行组合。`not`、`if`、`iff`、`xor/xone`、任意算术、查询语言、策略语言、shell 或模型代码 `MUST NOT` 成为第一阶段组合节点。

**失败：**结构为空或只有一个子项、存在环或重复叶、判据增删或错配事态分支、子项顺序改变语义，或自由表达式被嵌入组合节点时，形成操作必须拒绝。

**验证：**`SCN-024` 与 `SCN-027` 设计审查；`vectors/composition/cases.json`；未来 `conformance:composition-topology-alignment` 组件测试。

### END-CMP-003 — 四种叶结果必须确定性组合

**要求：**`all_of` 中任一有效 `unmet` `MUST` 决定总体 `unmet`；否则存在 `fault` 时总体 `MUST` 为 `fault`，再否则存在 `agno` 时总体 `MUST` 为 `agno`，只有全部为 `met` 时总体才 `MAY` 为 `met`。`any_of` 中任一有效 `met` `MUST` 决定总体 `met`；否则存在 `fault` 时总体 `MUST` 为 `fault`，再否则存在 `agno` 时总体 `MUST` 为 `agno`，只有全部为 `unmet` 时总体才 `MAY` 为 `unmet`。组合 `MUST` 保留全部已求值叶结果；故障或未知不得静默改写为真假。

**失败：**求值顺序改变完整结果、`agno` 或 `fault` 被当作 `unmet`、`all_of` 在已有反例时返回故障、`any_of` 在已有满足见证时返回故障，或叶故障被从记录中删除时，该组合结果无效。

**验证：**`SCN-024` 与 `SCN-026` 设计审查；`vectors/composition/cases.json`；未来 `conformance:four-result-composition` 组件测试。

### END-CMP-004 — 短路必须保存决定依据与求值覆盖

**要求：**只有在 `all_of` 已得到有效 `unmet` 或 `any_of` 已得到有效 `met` 后，求值才 `MAY` 短路。结果 `MUST` 保存决定依据、所有已求值叶及所用 Iknem、未求值叶身份与停止原因。未求值叶 `MUST NOT` 被记录为 `agno`。不同求值顺序可以改变求值覆盖，但 `MUST NOT` 改变已经出现决定性结果后的总体分类；短路前已经观察到的故障 `MUST` 保留。

**失败：**在结果仍依赖未求值叶时提前停止、没有记录未求值叶、把未执行等同于观察不足、只保留总体布尔值，或通过先求值有利分支隐藏已发生故障时，该结果无效。

**验证：**`SCN-026` 设计审查；`vectors/composition/cases.json`；未来 `conformance:decisive-short-circuit-provenance` 组件测试。

### END-TEL-001 — 目标方向独立

**要求：**第一阶段 `telis.mode` `MUST` 是 `kine` 或 `mene`。`kine` 表示使事态达到成立，`mene` 表示在声明区间保持成立；禁止事项 `MUST` 由 `skena` 的显式否定表达，不得用第三种方向重复编码。

**失败：**方向缺失、未知、与事态极性重复，或 `mene` 没有适用区间时，必须拒绝。

**验证：**`SV-VALID-001`；未来 `conformance:telis-mode` 测试。

### END-QNT-001 — 量化必须固定成员范围

**要求：**量化 `skena` `MUST` 固定一个关系模板和且仅一个被量化角色，并绑定集合身份、具名成员资格权威、`enumerated` 或 `rule-bound` 成员模式、确定截止点、成员身份规则，以及完整成员清单或确定性成员规则。`enumerated` 成员 `MUST` 按规范身份唯一；重复成员必须拒绝，不得静默去重。模型、查询结果、搜索路径或运行工具 `MUST NOT` 在求值时另选有利子集。

**失败：**成员资格权威、截止点、身份规则或被量化角色缺失，集合同时使用两种模式，成员规则依赖未记录环境，或同一成员以重复记录出现时，形成操作必须拒绝。

**验证：**`SCN-016`、`SCN-018` 与 `SCN-019` 设计审查；`vectors/quantification/cases.json`；未来 `conformance:quantified-collection-scope` 组件测试。

### END-QNT-002 — 量词与闭包条件必须显式

**要求：**第一阶段量词只允许 `all`、`some`、`at_least`、`at_most` 与 `exactly`；后三者 `MUST` 绑定非负整数阈值。支持全称满足、上界满足或精确数量满足的集合 `MUST` 是截止点已封闭的 `enumerated` 范围，除非已有足以反驳或满足该结论的决定性成员证据。空集合 `MUST` 绑定具名权威明确授权的 `allow` 政策；不得以默认空集和形式逻辑的空真值静默产生 `met`。量化 `mene` 在成员变更政策、成员有效区间和滚动闭包冻结前不受支持。

**失败：**量词未知、阈值缺失或为负、开放集合被用于证明 `all`、`at_most` 或 `exactly` 已满足、空集合政策缺失，或动态成员集合被用于持续目标时，形成或求值必须拒绝相应确定结论。

**验证：**`SCN-016`、`SCN-017` 与 `SCN-019` 设计审查；`vectors/quantification/cases.json`；未来 `conformance:quantifier-closure` 组件测试。

### END-QNT-003 — 聚合只按不同成员身份计数

**要求：**量化求值 `MUST` 按规范化后的不同成员身份聚合成员级 `met/unmet/agno/fault`，不得按日志行、观察次数、证据数量或模型提及次数计数。决定性结果可以提前形成：`all` 的一个有效 `unmet`、`some` 的一个有效 `met`、`at_least k` 的 `k` 个不同 `met`、`at_most k` 的 `k+1` 个不同 `met`、`exactly k` 的 `k+1` 个不同 `met`。没有决定性结果时，未封闭或观察不足产生 `agno`，成员求值契约故障产生 `fault`，只有封闭范围的完整成员结果才可形成其余 `met` 或 `unmet`。聚合结果 `MUST` 保留实际成员结果与所用 Iknem 的可追溯链接。

**失败：**重复见证被累计、一个成员的多条日志被当成多个成员、未知成员被当作未满足、故障被当作反例，或在不完整范围内产生非决定性的确定结果时，该聚合结果无效。

**验证：**`SCN-016` 至 `SCN-018` 设计审查；`vectors/quantification/cases.json`；未来 `conformance:distinct-cardinality-aggregation` 组件测试。

### END-MSR-001 — 测量构念与目标总体必须先于分数

**要求：**可测量 `krin` `MUST` 固定被判断的关系和值角色、测量构念、适用主体或项目总体、具名语义权威、预期用途，以及直接可观察的测量标准。固定项目或样本上的结果 `MUST` 标记为 `fixed`；推广到未实际测试总体的结果 `MUST` 标记为 `generalized`，并绑定预注册的统计模型、总体定义、抽样假设和适用限制。基准、模型裁判、代理指标或仪表盘名称 `MUST NOT` 自行替代构念。

**失败：**“质量”“智能”“安全”“合理”等构念没有获得授权的可观察标准，固定基准分数被声称为普遍能力，事后选择有利样本或用途，或代理任务与目标构念的关系没有被声明时，形成操作必须拒绝或把缺口保留在 `apor`。

**验证：**`SCN-007`、`SCN-021` 与 `SCN-023` 设计审查；`vectors/measurement/cases.json`；未来 `conformance:measurement-construct-and-population` 组件测试。

### END-MSR-002 — 数值域、单位与换算必须确定

**要求：**测量程序 `MUST` 固定有限数值域、量纲、规范单位、观察单位、换算规则及其权威与版本。只有量纲兼容且在声明域内确定、单调并具有已知误差的换算才 `MAY` 在比较前执行；非线性或分段换算 `MUST` 固定方向、定义域、值域和误差。NaN、无穷、未定义逆、隐式百分比缩放、区域格式和比较前舍入 `MUST NOT` 成为规范值。舍入若存在，只能用于比较后的显示，并固定模式和精度。

**失败：**阈值与观察量纲不兼容、单位缺失、换算依赖机器单位库“最新版本”、非单调函数被反向使用、百分数与比例混淆，或先把 `0.76` 显示舍入为 `0.8` 再与 `0.8` 比较时，形成或求值必须拒绝。

**验证：**`SCN-020` 与 `SCN-022` 设计审查；`vectors/measurement/cases.json`；未来 `conformance:numeric-unit-conversion` 组件测试。

### END-MSR-003 — 测量程序与聚合器必须可重放

**要求：**测量程序 `MUST` 固定生产者、方法身份与版本、观察窗口、总体模式、纳入与排除规则、最小有效样本数、缺失和删失处理，以及一个登记聚合器。第一阶段抽象聚合器限于 `point`、`count`、`sum`、`min`、`max`、`arithmetic_mean`、`fraction`、`quantile` 与 `model_estimate`。均值 `MUST` 固定权重；比例 `MUST` 固定分子与分母；分位数 `MUST` 固定 q、排序/插值方法和最大误差；模型估计 `MUST` 固定 estimand、模型、假设和不确定度方法。数据不完整或样本不足 `MUST` 产生 `agno`；程序、生产者或统计契约失败 `MUST` 产生 `fault`。

**失败：**平均值被事后换成 p95、失败请求被静默排除、时间窗口滑动、不同分桶边界被无损合并、重复试验被当作独立项目、样本不足仍给出确定结论，或统计模型和假设不能定位时，该结果无效。

**验证：**`SCN-020`、`SCN-021` 与 `SCN-023` 设计审查；`vectors/measurement/cases.json`；未来 `conformance:measurement-procedure-replay` 组件测试。

### END-MSR-004 — 比较边界与不确定度必须共同决定结果

**要求：**阈值契约 `MUST` 固定 `lt/le/gt/ge/eq` 比较器、阈值及单位和 `interval` 不确定度政策。观察的有效不确定区间完全落在满足一侧时才 `MAY` 产生 `met`，完全落在反驳一侧时才 `MAY` 产生 `unmet`；区间与边界重叠 `MUST` 产生 `agno`。点估计、仪表盘显示值、排名或置信度标签 `MUST NOT` 越过区间单独决定结果。比较结果 `MUST` 绑定原始观察、换算、聚合器、阈值、区间和实际使用的 Iknem。

**失败：**`<` 与 `<=` 被视为相同、误差条被隐藏、点估计越线但区间跨线仍宣称满足、多个阈值中只报告通过项，或模型输出的自报置信度被当作统计不确定度时，该判断必须拒绝。

**验证：**`SCN-020`、`SCN-021` 与 `SCN-023` 设计审查；`vectors/measurement/cases.json`；未来 `conformance:threshold-uncertainty-classification` 组件测试。

### END-NEG-001 — 否定必须作用于同一关系与角色位置

**要求：**负极性 `skena` `MUST` 引用 `semion` 中已经授权的关系身份和同一组具名角色，并把极性显式编码为 `negative`。实现 `MUST NOT` 以删除关系节点、构造 `not_` 前缀谓词、交换角色、增加 `avoid/forbid` 方向或依赖空集合来表达否定。END-P1 当前只编码原子关系极性；复合否定与双重否定规范化仍不受支持。

**失败：**负目标缺少关系或角色、否定只存在于来源文本、负极性同时改写谓词身份，或同一禁止要求又被 `telis` 重复编码时，形成操作必须拒绝。

**验证：**`SCN-003` 与 `SCN-013` 设计审查；`vectors/semantic/negative-relation-valid.json`；`vectors/negation/cases.json`；END-P1 负极性规范字节；未来 `conformance:negative-relation-identity` 组件测试。

### END-NEG-002 — 缺失观察不得冒充否定观察

**要求：**负极性 `phain` `MUST` 显式绑定与目标相同的关系、角色、主体范围、观察方法、生产者权威和适用截止点。没有匹配记录、工具没有返回、日志为空、请求被单一路径拒绝或模型声称“未发现” `MUST NOT` 单独构成负极性观察。有效的正极性反例 `MUST` 反驳对应负目标；观察缺失 `MUST` 产生 `agno`，观察或适配契约故障 `MUST` 产生 `fault`。

**失败：**求值器把空查询结果写成负事实、把一次拒绝推广为所有路径都不可达、把正反角色错位的观察用于比较，或把采集器故障写成 `unmet` 时，必须拒绝该结果。

**验证：**`SCN-003`、`SCN-014` 与 `SCN-015` 设计审查；`vectors/negation/cases.json`；未来 `conformance:negative-observation-basis` 组件测试。

### END-NEG-003 — 缺席推断必须绑定封闭观察范围

**要求：**只有在 Iknem 声明封闭观察范围并证明覆盖充分时，缺少正极性反例才 `MAY` 支持负目标。封闭声明 `MUST` 固定具名权威、被枚举的主体与关系全集、全部适用角色路径、时间区间与截止点、完整枚举方法、丢失/过滤/去重/迟到记录计数和已知排除项。任何字段缺失、路径未覆盖、丢失量未知或证据覆盖不足时，结果 `MUST` 是 `agno`；观察系统违反声明契约时 `MUST` 是 `fault`。

**失败：**实现把开放世界数据集、部分日志、缓存、搜索索引、外部 Agent 历史或一次 `grep` 无匹配结果当作现实世界不存在的证明，或在发现正极性反例后仍返回 `met` 时，必须拒绝该结果。

**验证：**`SCN-014` 与 `SCN-015` 设计审查；`vectors/negation/cases.json`；未来 `conformance:closed-observation-scope` 组件测试。

### END-TIM-001 — mene 必须绑定明确时间范围与时钟权威

**要求：**`mene` `MUST` 使用 `fixed` 或 `elapsed` 时间范围。`fixed` `MUST` 绑定开始早于结束的确定 UTC 瞬间、半开区间 `[start,end)` 和具名时间决定权威；`elapsed` `MUST` 绑定具名起始事件、正的固定长度时长、单调时钟域、时钟生产者与重启边界。相对日期、本地默认时区、未授权时区解析、日历月或年以及当前系统时间 `MUST NOT` 成为规范输入。

**失败：**起止缺失或倒置、来源仍含未解析的“现在”“明天”等相对表达、时间依赖运行机器默认时区、经过时长由可回拨民用时钟测量，或单调时钟跨未声明重启复用时，形成操作必须拒绝或把决定缺口保留在 `apor`。

**验证：**`SCN-010` 与 `SCN-012` 设计审查；`vectors/mene/cases.json` 提案向量；未来 `conformance:mene-time-scope` 组件测试。

### END-TIM-002 — 连续性政策必须显式

**要求：**每个 `mene` `MUST` 使用 `strict` 或 `budgeted` 连续性政策。`strict` 要求 `skena` 在整个目标区间成立；`budgeted` `MUST` 声明最大累计违约时长、最大单次违约时长与最大违约次数。遥测缺口、缺少采样或时钟不确定性 `MUST NOT` 作为允许违约消耗预算。

**失败：**政策缺失、预算字段不完整或为负、实现把离散采样当作第三种连续性政策，或把未观察时间解释为预算内正常时，求值结论无效。

**验证：**`SCN-010` 与 `SCN-011` 设计审查；`vectors/mene/cases.json` 提案向量；未来 `conformance:mene-continuity-policy` 组件测试。

### END-TIM-003 — 时间覆盖缺口不得被插值为满足

**要求：**用于 `mene` 的 Iknem `MUST` 声明覆盖区间、观测方法、时钟域、分辨率、不确定度与已知缺口，并按半开区间形成规范覆盖并集。覆盖完整且违约未发生或仍在显式预算内才 `MAY` 产生 `met`；覆盖完整且观察到严格违约或预算超限 `MUST` 产生 `unmet`；覆盖存在空洞、只有离散采样或不确定度跨越关键边界 `MUST` 产生 `agno`；时钟、同步、适配器或求值器违反契约 `MUST` 产生 `fault`。

**失败：**实现以“没有告警”“最后一次采样健康”、线性插值、远端 Task 时间戳或当前墙钟填补覆盖空洞，或把时钟故障写成 `unmet` 时，必须拒绝该结果。

**验证：**`SCN-011` 与 `SCN-012` 设计审查；`vectors/mene/cases.json` 提案向量；未来 `conformance:mene-coverage-classification` 组件测试。

### END-KRN-001 — 判断契约不能自证

**要求：**`krin` `MUST` 指定可接受的 `phain` 结构、关系比较、必需 Iknem、未知处理与决定权威。自由文本结论、单一模型评分或制品自填的 `true`、`valid`、`logical_form` 字段 `MUST NOT` 独自支持满足判断。

**失败：**观察不能对齐关系位置、证据类型不明或决定权威缺失时，结果必须是观察不足、求值故障或待外部判断，不得成为已满足。

**验证：**`SV-VALID-001`；未来 `conformance:krin-no-self-proof` 测试。

### END-KRN-002 — 满足结果必须区分反驳、未知与故障

**要求：**一次完整求值 `MUST` 产生且只产生 `met`、`unmet`、`agno` 或 `fault`。结果 `MUST` 绑定被判断的 Endem 身份、`krin` 版本、观察截止点、实际使用的 Iknem 和稳定原因。`met` 与 `unmet` `MUST` 只在必需观察齐全、有效、适用且比较已完整执行时产生；观察缺失、过期、越出范围或覆盖不足 `MUST` 产生 `agno`；求值器、规则、依赖或观察适配过程未按契约完成 `MUST` 产生 `fault`。

**失败：**实现从无日志、超时、权限缺失或执行错误推出 `unmet`，从工具成功或外部任务完成推出 `met`，或用新观察原地改写旧结果时，该结果无效。

**验证：**`SCN-005`、`SCN-006` 与 `SCN-009` 设计审查；`vectors/result-domains/cases.json` 提案向量；未来 `conformance:satisfaction-result-separation` 组件测试。

### END-APR-001 — 未决投影不得消失

**要求：**可表达但尚未获授权选择的投影 `MUST` 保存在 `apor`，并记录候选、冲突、影响范围、允许的解决方式和具名决定主体。

**失败：**实现只保留最高置信候选、以默认值关闭歧义或在状态变化中丢弃未决项时，必须拒绝。

**验证：**`SV-REJECT-APOR-001`；未来 `conformance:apor-preservation` 测试。

### END-UNK-001 — 四类未知与失败分离

**要求：**实现 `MUST` 区分：没有任何允许投影的 `aseme`、存在允许候选但未获授权选择的 `apor`、观察不足的 `agno` 与求值过程故障的 `fault`。

**失败：**任意两类被合并，或未知被静默提升为确定结果时，必须拒绝该结论。

**验证：**`SV-REJECT-APOR-001`；未来 `conformance:unknown-state-separation` 测试。

### END-STR-001 — 形式由结构显示

**要求：**`semion`、`skena` 与适用 `phain` `MUST` 共享可比较的符号身份、关系身份和角色位置。逻辑形式 `MUST` 由关系拓扑和组合边显示，不得由载荷自我宣称。

**失败：**符号悬空、角色数量不符、关系位置无法对齐或只有六段文本时，必须拒绝。

**验证：**`SV-VALID-001`；未来 Ktisor/Theor 逐字段差分。

## 4. 权威与确定性

### END-AUT-001 — 模型只能提出候选

**要求：**模型、远端 Agent 或外部工具输出 `MUST` 视为不可信候选；它们 `MUST NOT` 决定规范字节、关闭 `apor`、修改已封装或已签名制品、扩大能力或宣告最终验收。

**失败：**授权来源是模型自述，或候选没有经过确定性规则、具名权威或显式未决处理时，形成操作必须拒绝。

**验证：**`SV-REJECT-AUTHORITY-001`；未来 `conformance:model-candidate-boundary` 测试。

### END-AUT-002 — 权威标识不能自证授权

**要求：**`projection.kind`、`projection.id`、`decision_authority` 和其他权威名称只能标识待核对的规则、角色或主体，`MUST NOT` 充当授权决定本身。确认 `semion` 或解决 `apor` 的内容接受 `MUST` 取得满足精确 `AUT-CORE` 版本的外部绑定，并至少覆盖来源身份、候选内容、语义位置、安全显示、授权主体、范围、截止点、决定结果和剩余未决项。该绑定 `MUST` 指向当前精确内容候选；`deny`、`defer`、缺失、错绑、过期或撤销均不能产生已授权投影。

**失败：**仅因字符串看似属于可信人员、规则或组织就接受投影，或把另一个来源、候选、语义位置、租户、目的或截止点的授权决定重用于当前对象时，内容接受必须拒绝或保持未求值，且不得提升生命周期状态。

**验证：**`SCN-028` 与 `SCN-029`；`SV-REJECT-AUTHORIZATION-BINDING-001` 与语义接受向量；未来 `conformance:projection-authorization-companion` 测试。

### END-DEC-001 — 最终决定必须保留满足结果与权威

**要求：**最终决定 `MUST` 是 `accepted`、`rejected` 或 `deferred`，并 `MUST` 绑定输入满足结果、适用 Iknem 的有效性与覆盖度、决定规则、具名权威和声明范围。`accepted` `MUST` 同时要求 `met`、有效且未撤销的必需 Iknem、充分覆盖和获授权决定；`rejected` `MUST` 来自具名权威依据 `unmet` 或预先登记政策作出的否定决定；尚无获授权最终决定时 `MUST` 使用 `deferred`。

**失败：**模型、Drasor、工具返回、外部 Task 状态或证据数量直接产生最终决定，决定不保存原满足结果，或 `agno`、`fault` 被静默提升为 `accepted` 时，该决定无效。

**验证：**`SCN-009` 设计审查；`vectors/result-domains/cases.json` 提案向量；未来 `conformance:decision-authority-and-basis` 组件测试。

### END-DET-001 — 同一封闭输入产生同一规范结果

**要求：**Ktisor `MUST` 先绑定封闭形成输入：实际进入 `rhem` 的解码文本及其文本槽、严格解码 Profile、显式变换结果与损失，以及授权决定、配置、依赖、END-CORE、内容 Profile 和格式版本。对同一封闭输入，Ktisor `MUST` 产生同一规范结果；精确 END-FMT 与内容 Profile 冻结后，还 `MUST` 产生逐字节相同的 Endem。实现 `MUST NOT` 通过未声明的 Unicode 规范化、大小写折叠、换行改写、空白裁剪或模型改写自行构造“相同来源”。

**失败：**输入闭包或显式变换链未固定，或者时间、当前目录、区域设置、哈希表遍历、并发完成顺序、未记录默认值或模型随机性改变规范结果时，符合性测试必须失败。来源经过有损变换后只比较输出却声称保留原始来源或证明语义等价，也必须拒绝该主张。

**验证：**未来 `conformance:determinism-same-input` 与双环境复现测试。

## 5. 状态与身份

### END-STA-001 — 状态不能越级推导

**要求：**`nascent` 只表示结构已形成；`coherent` 只表示必需投影、引用、冲突、能力上限和判断关系已收敛；`attested` 只表示冻结载荷与外部签名响应精确绑定。

**失败：**实现把签名、状态名、Iknem 数量或模型自述解释为语义正确、环境授权或任务完成时，必须拒绝该推导。

**验证：**未来 `conformance:state-non-implication` 测试。

### END-STA-002 — 五个结果域不得互相强制转换

**要求：**实现 `MUST` 分别保存制品生命周期、满足判断、权威决定、会话终止和证据状态。会话终止只允许 `completed`、`failed` 或 `interrupted`；Iknem 身份与适用性只允许 `valid`、`invalid` 或 `revoked`，证据集合覆盖度 `MUST` 另行表示为 `sufficient` 或 `insufficient`。任何适配器 `MUST NOT` 把一个结果域的值强制转换为另一个结果域的值。

**失败：**`completed` 被解释为 `met` 或 `accepted`，`failed` 被解释为 `unmet`，Iknem `valid` 被解释为覆盖充分，或外部协议状态覆盖本地结果时，必须拒绝该推导。

**验证：**`SCN-009` 设计审查；`vectors/result-domains/cases.json` 提案向量；未来 `conformance:orthogonal-result-domains` 组件笛卡尔测试。

### END-ID-001 — 精确身份与语义等价分离

**要求：**完整字节摘要、语义等价键、签名包络与 Iknem 关联 `MUST` 是不同属性。语义等价规则冻结前，程序 `MUST NOT` 生成或信任所谓 Semantic Key。

**失败：**实现用名称、短校验值、构建 ID 或签名替代完整内容摘要，或用精确摘要冒充语义等价时，必须拒绝。

**验证：**未来 `conformance:identity-domain-separation` 测试；格式规范复核。

### END-ID-002 — 外部决定不得改变内容身份

**要求：**对同一 Profile 与同一规范字节，授权主体、授权决定、签名、验证材料、撤销状态、Iknem、满足结果和最终决定变化时，Endem 的精确内容身份 `MUST` 保持不变；变化只产生新的伴随关系或相对具名截止点的新评估。任何必须改变六个语义面或规范字节的语义修订 `MUST` 形成新的内容身份，不能伪装成授权状态更新。

**失败：**两个不同授权者确认同一字节却得到两个 Endem 内容身份，授权撤销导致历史字节身份变化，或改变语义字段后继续沿用旧身份时，身份或伴随关系无效。

**验证：**`SCN-030`；语义向量的内容身份等价组；未来 `conformance:identity-independent-of-external-decisions` 测试。

## 6. 不可信输入与失败语义

### END-SAF-001 — 所有结构计算受检

**要求：**对不可信输入执行的偏移加法、计数乘法、对齐上取整、区间端点、索引换算、累计大小与解压大小 `MUST` 使用受检算术。任何溢出或下溢 `MUST` 成为稳定错误。

**失败：**计算溢出、回绕、越界或依赖未定义行为时，读取必须原子失败。

**验证：**未来 `conformance:checked-arithmetic` 边界向量与模糊测试。

### END-SAF-002 — 资源上限先于分配

**要求：**每个读取 Profile `MUST` 提供有限、非零且可记录的文件、记录、图节点、图边、嵌套深度、字符串、解压和累计内存上限。读取器 `MUST` 在大规模分配或递归解释前检查相应上限。

**失败：**Profile 缺少必需上限、使用“无限”值或输入超过任一上限时，必须拒绝。END-P0 与 END-P1 都登记有限实验数值；它们不能从示例或环境默认值改写，也不构成生产规模证明。

**验证：**未来 `conformance:resource-limit-before-allocation` 测试；Profile ADR。

### END-SAF-003 — 未知关键结构关闭失败

**要求：**未知且可能影响六个语义面、状态、权限、绑定、身份或完整性的结构 `MUST` 被视为关键并拒绝。只有明确登记为可选且不改变规范含义的记录 `MAY` 跳过。

**失败：**读取器跳过未知关键结构或因跳过而提升状态时，必须拒绝整个对象。

**验证：**未来 `conformance:unknown-critical-record` 测试；格式注册表复核。

### END-ERR-001 — 失败原子且可定位

**要求：**解析、形成或验证失败 `MUST NOT` 产生部分可信 Endem。诊断 `MUST` 包含稳定错误类别、主条款 ID，以及可用时的来源范围、语义路径或字节范围。

**失败：**实现返回一部分可继续使用的可信状态，或只返回无法关联条款与位置的自由文本错误时，不符合本规范。

**验证：**所有拒绝向量；未来 Ktisor/Theor 诊断差分。

## 7. 独立验证

### END-VER-001 — 两条读取路径不能共享故障根

**要求：**制品形成侧读取路径与 Theor `MUST` 分别解释同一规范和向量。Theor `MUST NOT` 复用形成侧解析器、写入器、绑定器、生成代码或错误分类实现。如果 Ktisor 为下游保存绑定精确输入、规范/Profile、检查配置和已完成层次的内部引用，Theor `MUST NOT` 接收或产生该引用。该引用 `MUST NOT` 被解释为 CLI 输出、Iknem、签名、授权、内容身份、满足结果或最终决定。

**失败：**两条路径共享会使同一错误同时成为写入、读取和验收依据的实现依赖时，独立性声明无效。

**验证：**未来仓库依赖检查、变异测试和故障注入。

### END-VER-002 — 规范要求必须可追溯

**要求：**每个规范条款 `MUST` 在 `registry.json` 中登记成熟度、失败责任和验证方式。`covered-by-repo` `MUST` 指向当前仓库实际存在并被自动检查读取的证据；未实现验证 `MUST` 标为 `planned`。

**失败：**条款未登记、ID 重复、验证引用缺失或计划被写成已覆盖时，规范检查必须失败。

**验证：**`tests/spec_contract_test.py`。

## 8. 当前未决接口

以下内容仍为开放问题，不能从本规范或语义向量中推导：

- 受控来源文本语法与规范化规则；
- END-P1 之外的量化、mene 时间、测量、复合判断、求值事件字段和扩展字段；
- END-P0 数值的生产规模证据与后续 Profile 协商；
- 量化、测量与组合字段编码、跨叶测量约简、单位字典、统计模型登记、闰秒与循环日历、叶判据物理表示，以及结果事件的编码、聚合与重放；
- 压缩、摘要、签名与撤销算法；
- 授权伴随关系、规则登记、权威目录和符合性报告的物理编码；
- Semantic Key 与跨布局等价规则；
- 稳定错误码、CLI 参数、退出状态与 ABI。

固定前导、记录目录、第一组 Profile 数值和结构错误码由 `END-FMT 0.1.0-draft` 定义，但仍可在开发阶段直接修订。其余接口只有在 ADR、正反向量、至少两个独立解释路径和对抗测试同时存在后才可以冻结。
