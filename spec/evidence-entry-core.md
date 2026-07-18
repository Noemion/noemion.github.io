---
layout: spec
title: "evidence Core Specification · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/evidence-entry-core.html"
summary: "规定一项证据必须怎样绑定对象、生产者、方法、环境、时间、观察和限制，才能支持有范围的主张。"
document_status: "规范草案"
---
# evidence Core Specification

- 规范 ID：`EVIDENCE-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0022 已接受的证据范围、溯源、有效性、覆盖度与评估边界
- 物理编码：未定义；本规范不创建 evidence 文件格式、扩展名、魔数或稳定 ABI
- 实现状态：仅有规范提案向量检查器；采集器、验证器、归并器、撤销服务和决定引擎均未实现

## 1. 范围

本规范要求每项 evidence 说明提出者、精确对象、方法、环境和时间边界。它还必须记录取得了哪些结构化观察、实际提出什么有限主张，以及哪些限制阻止主张继续外推。溯源、证据类别、完整性、有效性、覆盖度、评估、决定和最小披露之间必须保持明确边界。

evidence 不是日志行、追踪跨度、模型解释、签名包、数学证明或最终验收决定。外部遥测、MCP/A2A 事件、供应链证明和人工记录只有在完成本规范要求的身份、范围、方法、限制与关系对齐后，才可能成为 evidence 的输入；外部字段名和状态不能直接成为 evidence 身份或 Noemion 结果。

## 2. 要求用语与符合性

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

符合性声明 `MUST` 固定 `EVIDENCE-CORE` 的精确版本，以及被引用 Endem、closure、`satisfaction_criteria`、方法、政策和外部规范的版本。涉及决定主体、授权依据、委托或同意时，还 `MUST` 固定并符合 `AUT-CORE` 的精确版本。当前没有 evidence 物理 Profile，任何工具都不得声称产生稳定 evidence 字节。

## 3. 证据记录

### EVIDENCE-SCP-001 — 每项主张必须绑定精确主体和有限范围

**要求：**evidence `MUST` 绑定精确主体身份、记录种类、生产者身份与权限、声明范围、方法与版本、环境身份、适用时间或截止点、实际主张和限制。主体可以是 Endem、closure、contract 会话、发布载荷、能力调用、观察集合或决定事件，但名称、路径、显示标签和“当前对象” `MUST NOT` 替代精确身份。主张 `MUST NOT` 超出生产者权限、方法覆盖或声明范围。

**失败：**主体含糊、方法或环境缺失、截止点未声明、生产者无权提出该类主张，或固定测试结果被外推到未声明总体时，该 evidence 对越界部分无效。

**验证：**`EVIDENCE-SCN-001`、`EVIDENCE-SCN-002`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-scope-binding` 组件测试。

### EVIDENCE-PRV-001 — 溯源图必须完整、有限且不能循环自证

**要求：**evidence `MUST` 显式绑定产生主张的活动、所用输入、派生关系与责任主体。规范输入、外部依赖和父 evidence `MUST` 使用精确身份；图 `MUST` 有限、无环并遵守资源预算。引用另一项 evidence 只能说明依赖，`MUST NOT` 让两项记录互相成为唯一依据。未知、遗漏或动态取得的输入 `MUST` 进入限制或覆盖缺口，不得隐藏在环境名称中。

**失败：**出现循环自证、父记录悬空、输入摘要缺失、运行时依赖未登记，或同一主张因搜索路径与网络最新状态而得到不同依据时，溯源无效。

**验证：**`EVIDENCE-SCN-003`、`EVIDENCE-SCN-004`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-provenance-closure` 组件测试。

### EVIDENCE-OBS-001 — 观察、变换与主张必须分开

**要求：**观察类 evidence `MUST` 把原始观察引用、实际执行的解析与变换、结构化 `structured_observation` 和最终主张分开。`structured_observation` `MUST` 与适用 `situation` 共享可比较的符号身份、关系身份、角色位置、极性和作用域。选择、丢失、过滤、聚合、换算、舍入、脱敏与模型解释 `MUST` 记录为可定位变换，并绑定算法或方法版本及其信息损失。没有声明封闭对象域、算法和等价关系时，形成者 `MUST NOT` 用未定义的“规范化”概括这些步骤。自由文本、工具成功状态、模型置信度或日志数量 `MUST NOT` 自行升级为关系事实。

**失败：**无法把观察对齐到关系位置、把推断伪装成原始观察、遗漏有损变换，或把空查询直接编码为负极性 `structured_observation` 时，该观察主张无效。

**验证：**`EVIDENCE-SCN-005`、`EVIDENCE-SCN-006`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-observation-alignment` 组件测试。

### EVIDENCE-CLS-001 — 记录种类与证据来源类别不得自我升级

**要求：**evidence `MUST` 区分 `observation`、`derivation`、`attestation`、`appraisal` 与 `decision-record` 五种记录种类，并另行标明 `direct-observation`、`deterministic-derivation`、`external-assertion`、`human-judgment` 或 `model-candidate` 来源类别。种类回答记录做了什么，来源类别回答依据怎样产生；两者 `MUST NOT` 由置信分数、签名、重复次数或生产者自述提升。模型输出只能保持 `model-candidate`，直到另一个获授权过程产生自己的独立记录。

**失败：**模型自评被改成直接观察、外部声明因带签名被改成确定性推导、人工判断冒充环境事实，或生产者给自己声明更高等级时，该分类无效。

**验证：**`EVIDENCE-SCN-006`、`EVIDENCE-SCN-007`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-evidence-class` 组件测试。

### EVIDENCE-INT-001 — 完整性与真实性不能替代事实正确和授权

**要求：**内容身份、序列连续性、生产者认证、签名验证、透明日志包含、时间戳与语义主张 `MUST` 分别表示。完整性检查只能支持“这些字节由声明主体以声明机制产生且未被检测到修改”的有限结论；它 `MUST NOT` 自动证明观察真实、方法适用、目标满足、当前环境授权或最终接受。

**失败：**摘要相同被解释为事实相同、签名有效被解释为主张正确、时间戳存在被解释为新鲜，或记录进入透明日志就获得决定权威时，推导无效。

**验证：**`EVIDENCE-SCN-007`、`EVIDENCE-SCN-008`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-integrity-separation` 组件测试。

## 4. 评估、覆盖与撤销

### EVIDENCE-VAL-001 — 有效性评估必须外置并绑定政策与截止点

**要求：**`valid / invalid / revoked` 是验证者针对一项 evidence、在精确验证政策、参考值、信任根、环境与截止点下形成的有效性评估，不是 evidence 对自己的字段。`valid` 只说明当前评估上下文接受记录身份、完整性、生产者、方法和范围；`invalid` 说明记录从未满足或当前不满足要求；`revoked` 说明此前可用的生产者、密钥、方法、来源或记录已被具名权威撤回。评估依据变化时 `MUST` 重新评估，旧事件保持追加记录。

**失败：**记录自填 `valid`、验证政策或截止点缺失、撤销被忽略、旧评估在主体或环境变化后继续复用，或有效性被映射为覆盖充分时，该评估无效。

**验证：**`EVIDENCE-SCN-008`、`EVIDENCE-SCN-009`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-validity-appraisal` 组件测试。

### EVIDENCE-COV-001 — 覆盖度必须相对精确 satisfaction_criteria 计算

**要求：**`sufficient / insufficient` `MUST` 针对精确 Endem、`satisfaction_criteria` 版本、关系位置、主体集合、时间范围、截止点和必需证据类别计算。覆盖只按已验证、适用且未撤销的不同观察责任计入；记录数量、重复事件、多个签名或同一来源的副本 `MUST NOT` 增加覆盖。缺失路径、未知丢失、开放集合、时间空洞、过期依据和影响判断的脱敏损失 `MUST` 产生 `insufficient`。

**失败：**用数量阈值冒充覆盖、同一观察重复计数、将另一个 `satisfaction_criteria` 的充分集合复用到当前判断，或在存在未知空洞时输出 `sufficient`，覆盖评估无效。

**验证：**`EVIDENCE-SCN-010`、`EVIDENCE-SCN-011`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-coverage` 组件测试。

### EVIDENCE-DEC-001 — 评估结果与最终决定必须保持正交

**要求：**`appraisal` 记录 `MUST` 保存输入 evidence、有效性与覆盖评估、适用政策、参考值、结果和限制。`decision-record` 只记录具名权威已经作出的 `accepted / rejected / deferred` 事件、输入满足结果与决定规则；它本身 `MUST NOT` 创造决定权限，也不得把验证者评估直接映射为最终决定。`met`、`valid`、`sufficient`、会话 `completed` 和外部 Task 成功均 `MUST NOT` 单独产生 `accepted`。

**失败：**验证器替代依赖方作出应用决定、runner 或模型成为默认决定者、决定记录没有具名权威，或循环引用决定记录来证明自身正确时，该决定关系无效。

**验证：**`EVIDENCE-SCN-012`、`EVIDENCE-SCN-013`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-decision-separation` 组件测试。

### EVIDENCE-PRI-001 — 最小披露必须显式记录损失且不得保存实时秘密

**要求：**evidence `MUST` 只保存声明范围、验证和审计所需信息。Bearer token、刷新令牌、私钥、会话 cookie、文件描述符、实时能力句柄、未获授权的提示与工具正文 `MUST NOT` 进入记录。摘要、脱敏、分段披露或外置引用 `MUST` 绑定原对象身份、变换规则、可见范围、不可见范围和对主张及覆盖度的影响。外置对象不可得时，相关依据 `MUST` 视为不可验证。

**失败：**把凭据写入证据、以脱敏标签隐藏关键关系损失、外置引用可变或无摘要，或审计者无法判断省略如何影响结论时，该披露不能支持完整主张。

**验证：**`EVIDENCE-SCN-011`、`EVIDENCE-SCN-014`；`vectors/evidence-entry/cases.json`；未来 `conformance:evidence_entry-minimal-disclosure` 组件测试。

## 5. 当前未定义

本规范不确定 evidence 的物理容器、扩展名、魔数、字段编号、CBOR/JSON 映射、摘要与签名算法、透明日志协议、远程查询、撤销分发、跨生产者时钟归并、隐私策略语言或长期归档格式。它们必须由真实消费者、独立 ADR、新 Profile、威胁分析、正反向量与规范字节共同支持后才能进入实现。
