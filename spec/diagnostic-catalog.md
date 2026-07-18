---
layout: spec
title: "诊断码目录 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/diagnostic-catalog.html"
summary: "列出稳定机器诊断码及其适用层次，让程序依据代码而不是本地化消息识别失败。"
document_status: "规范目录草案"
---
# 诊断码目录

- 登记 ID：`DIA-CAT`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：与 `DIA-CORE 0.1.0-draft` 配套的跨对象诊断目录草案

## 1. 目录规则

每项诊断码使用小写 ASCII 点分段，并在本目录版本内保持唯一。首段表示受影响的工程对象或诊断系统本身；后续段从稳定领域逐步缩小到原因。Noemion 品牌不进入诊断码。

每个拒绝结果至少包含稳定 `code`、主 `clause`、验证 `layer`，以及 DIA-CORE 要求的生产语境。可用位置包括 `source_range`、`byte_range`、`record_id`、`semantic_path`、`graph_path`、`session_binding`、`evidence_ref` 与 `external_request`。人类消息可以改进或本地化，程序不得依赖消息文本。

一个操作可以在安全和预算范围内附加后续诊断，但主阻断诊断必须按 DIA-PRI-001 稳定选择。任何诊断集合都不能携带部分可信对象、能力，或可被下游当作检查已经通过的内部引用。

## 2. 诊断系统错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `diagnostic.identity.unregistered` | `DIA-IDN-001` | internal | 生产者使用未登记、冲突或仅由消息构造的机器码 |
| `diagnostic.context.unpinned` | `DIA-PIN-001` | internal | 缺少生产者、操作、精确主体或规范/目录版本 |
| `diagnostic.layer.coerced` | `DIA-LAY-001` | internal | 外部错误或诊断被强制转换为其他结果域 |
| `diagnostic.location.invalid` | `DIA-LOC-001` | internal | 位置无类型、越界、超限或未安全显示 |
| `diagnostic.primary.nondeterministic` | `DIA-PRI-001` | internal | 主诊断受并发、返回顺序、语言或模型判断影响 |
| `diagnostic.recovery.unauthorized` | `DIA-REC-001` | policy | 恢复建议扩大权限、跳过检查或脱离预算重试 |
| `diagnostic.external.unmapped` | `DIA-EXT-001` | protocol | 外部错误缺少来源、协议版本或受限本地映射 |
| `diagnostic.disclosure.secret` | `DIA-SEC-001` | internal | 诊断暴露秘密、句柄、隐私数据或未授权正文 |
| `diagnostic.budget.exceeded` | `DIA-BND-001` | internal | 诊断数量、深度、位置或总输出超过 Profile 上限 |
| `diagnostic.atomicity.partial_success` | `DIA-ATM-001` | internal | 阻断诊断同时返回部分可信结果或成功状态 |

## 3. Endem 结构与 Profile 错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `endem.wire.header.truncated` | `END-FMT-001` | structure | 输入不足 64 字节，无法读取固定前导 |
| `endem.wire.header.magic` | `END-FMT-001` | structure | 8 字节格式身份不同 |
| `endem.wire.header.version` | `END-FMT-001` | structure | 格式主次版本不受支持 |
| `endem.wire.header.layout` | `END-FMT-002` | structure | 字节序、头大小或目录项大小不同 |
| `endem.wire.header.size` | `END-FMT-003` | structure | 声明文件大小与实际字节数不同 |
| `endem.wire.header.reserved` | `END-FMT-003` | structure | 头标志或保留字节非零 |
| `endem.wire.directory.out_of_bounds` | `END-FMT-004` | structure | 目录乘加溢出、覆盖头部或超出文件 |
| `endem.wire.directory.order` | `END-FMT-005` | structure | 条目未按 `(kind, record_id)` 排序 |
| `endem.wire.record.id` | `END-FMT-005` | structure | 记录编号为零或重复 |
| `endem.wire.record.range` | `END-FMT-006` | structure | 记录端点溢出、越界或覆盖头部/目录 |
| `endem.wire.record.alignment` | `END-FMT-006` | structure | 记录偏移不满足对齐或对齐值不受支持 |
| `endem.wire.record.overlap` | `END-FMT-006` | structure | 两个非空记录范围重叠 |
| `endem.wire.record.padding` | `END-FMT-006` | structure | 记录间填充含非零字节，或最后记录后仍有尾随填充 |
| `endem.wire.record.unknown_kind` | `END-FMT-007` | profile | END-P2 出现未登记记录种类 |
| `endem.wire.record.flags` | `END-FMT-007` | profile | END-P2 记录没有精确关键标志 `1` |
| `endem.wire.facet.cardinality` | `END-FMT-008` | profile | 六种记录缺失、重复或出现额外记录 |
| `endem.wire.payload.cbor` | `END-FMT-009` | structure | CBOR 不良构、非确定或使用禁用类型 |
| `endem.wire.payload.not_map` | `END-FMT-009` | structure | 记录载荷根不是确定长度映射 |
| `endem.wire.profile.unknown` | `END-FMT-010` | profile | Profile 编号未知或没有精确登记 |
| `endem.wire.profile.limit` | `END-FMT-010` | profile | 任一资源超过当前有效上限 |
| `endem.wire.profile.feature` | `END-FMT-011` | profile | END-P2 出现压缩、加密、更高状态或其他未登记能力 |

## 4. Endem 内容错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `endem.root.not_unique` | `END-CORE-001` | semantic | 根事态缺失或多于一个 |
| `endem.source_expression.range_out_of_bounds` | `END-SRC-001` | semantic | 来源 Unicode 标量范围超过实际内容 |
| `endem.situation.contains_goal_force` | `END-SIT-001` | semantic | 中性事态混入目标方向或力量 |
| `endem.unresolved_meaning.unrecorded_projection_choice` | `END-UNRESOLVED-001` | semantic | 存在多个允许投影但未记录未决选择 |
| `endem.projection.authority_untrusted` | `END-AUT-001` | semantic | 模型自述或其他不可信来源试图确认投影 |
| `endem.projection.authorization_binding_missing` | `END-AUT-002` | semantic | 投影没有对应的外部授权前置条件，不能继续声明内容接受 |
| `endem.projection.authorization_binding_mismatch` | `END-AUT-002` | semantic | 外部授权前置条件没有精确绑定当前投影位置或候选 |
| `endem.semantic.field.type` | `END-FMT-013` | semantic | END-P2 字段值不是登记的数据类型 |
| `endem.semantic.field.missing` | `END-FMT-013` | semantic | END-P2 映射缺少必需字段 |
| `endem.semantic.field.identifier` | `END-FMT-013` | semantic | 标识符为空、过长或含禁用字符 |
| `endem.semantic.field.media_type` | `END-FMT-013` | semantic | 来源媒体类型不符合受限格式 |
| `endem.semantic.field.language` | `END-FMT-013` | semantic | 来源语言标签不符合受限格式 |
| `endem.semantic.field.order` | `END-FMT-013` | semantic | 需要规范排序且不重复的集合发生乱序或重复 |
| `endem.semantic.field.unknown` | `END-FMT-013` | semantic | END-P2 映射出现未登记字段键 |
| `endem.semantic.reference` | `END-FMT-014` | semantic | END-P2 出现悬空 symbol、relation、situation 或 source 引用 |
| `endem.situation.polarity` | `END-SIT-001` | semantic | 事态极性不是已登记值 |
| `endem.goal_direction.mode` | `END-DIRECTION-001` | semantic | 目标模式不是当前 Profile 唯一允许的 `reach` |
| `endem.satisfaction_criteria.policy` | `END-CRITERIA-001` | semantic | 缺失观察或评估错误政策不是当前 Profile 的固定值 |
| `endem.satisfaction_criteria.match` | `END-CRITERIA-001` | semantic | 观察关系匹配方式不是当前 Profile 的固定值 |

## 5. 实验来源清单错误码

这些错误发生在实验来源清单进入确定性语义映射之前，不属于 `.endem` 对象 ABI。

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `endem.source.utf8` | `END-SRCM-001` | source | 源文件不是有效 UTF-8 |
| `endem.source.limit` | `END-SRCM-001` | source | 文件或单行超过来源清单上限 |
| `endem.source.directive` | `END-SRCM-002` | source | 行首指令未登记 |
| `endem.source.arity` | `END-SRCM-002` | source | 指令字段数不符合其固定形状 |
| `endem.source.duplicate` | `END-SRCM-002` | source | 单例指令重复出现 |
| `endem.source.integer` | `END-SRCM-002` | source | 范围字段不是无符号十进制整数 |
| `endem.source.escape` | `END-SRCM-003` | source | 使用了未登记或不完整的转义 |
| `endem.source.role` | `END-SRCM-003` | source | `relation` 角色缺少名称、等号或 symbol 标识符 |

## 6. closure 错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `closure.closure.incomplete` | `CLOSURE-CLO-001` | closure | 成员不足、传递依赖遗漏或运行时才补全闭包 |
| `closure.binding.unresolved` | `CLOSURE-BND-001` | closure | 引用缺失、歧义、冲突或使用可变选择器 |
| `closure.graph.invalid` | `CLOSURE-GRF-001` | closure | 图不有限、存在循环或可选缺失削弱要求 |
| `closure.authority.amplified` | `CLOSURE-AUT-001` | policy | 组合权限使用并集或成员不能收窄 |
| `closure.result.coerced` | `CLOSURE-RES-001` | semantic | 成员结果被洗白、折叠或跨结果域转换 |
| `closure.activation.invalid` | `CLOSURE-ACT-001` | session | 激活添加成员、授予能力或映射为满足结果 |

## 7. contract 错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `session.subject.unbound` | `SESSION-SUB-001` | session | 主体不是精确且已解析的制品，或必需外部陈述没有按当前政策和截止点重新验证 |
| `session.policy.unclosed` | `SESSION-POL-001` | policy | 政策、权威、截止点或有效期未封闭 |
| `session.environment.drift` | `SESSION-ENV-001` | session | 环境只靠自述、缺少绑定或发生实质漂移 |
| `session.capability.amplified` | `SESSION-CAP-001` | policy | 能力使用并集、环境权限或原地 step-up |
| `session.secret.embedded` | `SESSION-SEC-001` | session | 契约包含实时秘密或能力句柄 |
| `session.budget.invalid` | `SESSION-BUD-001` | session | 预算无界、无单位、子任务逃逸或取消不传播 |
| `session.activation.outside_closure` | `SESSION-ACT-001` | session | 激活发现新成员、授予能力或改写结果域 |
| `session.observation.incomplete` | `SESSION-OBS-001` | evidence | satisfaction_criteria 观察、证据、披露或决定责任缺失 |
| `session.contract.mutated` | `SESSION-IMM-001` | session | 建立后被修改，或关键条件变化后仍原地修补 |
| `session.lifecycle.reused` | `SESSION-LIF-001` | session | 契约被序列化、转移、恢复或跨会话复用 |

## 8. evidence 错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `evidence.scope.unbound` | `EVIDENCE-SCP-001` | evidence | 主体、生产者、方法、环境、时间、主张或限制未固定 |
| `evidence.provenance.invalid` | `EVIDENCE-PRV-001` | evidence | 溯源悬空、循环、自证或隐藏动态输入 |
| `evidence.observation.unaligned` | `EVIDENCE-OBS-001` | evidence | structured_observation 无法对齐关系位置或有损变换未披露 |
| `evidence.classification.upgraded` | `EVIDENCE-CLS-001` | evidence | 记录种类或来源类别被自评、签名、数量或分数提升 |
| `evidence.integrity.overclaimed` | `EVIDENCE-INT-001` | evidence | 完整性、签名或时间戳被解释为事实正确或授权 |
| `evidence.validity.self_asserted` | `EVIDENCE-VAL-001` | evidence | 记录自填有效性或评估缺少政策、参考值与截止点 |
| `evidence.coverage.invalid` | `EVIDENCE-COV-001` | evidence | 覆盖脱离精确 satisfaction_criteria、重复计数或隐藏空洞 |
| `evidence.decision.unauthorized` | `EVIDENCE-DEC-001` | policy | 评估、模型、runner 或记录本身替代具名决定权威 |
| `evidence.disclosure.secret` | `EVIDENCE-PRI-001` | evidence | 记录包含实时秘密，或脱敏损失没有披露 |

## 9. 外部协议适配错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `adapter.protocol.version_unpinned` | `ADP-PIN-001` | protocol | 协议、规范、绑定、schema、传输或扩展版本浮动或未知 |
| `adapter.peer.binding_invalid` | `ADP-PEE-001` | protocol | 发现声明替代认证主体、受众、租户或政策绑定 |
| `adapter.capability.outside_intersection` | `ADP-CAP-001` | policy | 外部调用能力不在协议、对端、适配器、contract 与政策交集内 |
| `adapter.invocation.context_incomplete` | `ADP-INV-001` | session | 调用缺少精确主体、输入、预算、截止点、幂等或观察责任 |
| `adapter.mapping.loss_undeclared` | `ADP-MAP-001` | protocol | 映射没有保留原始身份、版本或显式信息损失 |
| `adapter.state.domain_confused` | `ADP-STA-001` | semantic | 外部请求、任务、消息、产物或 HTTP 状态被提升为本地结果 |
| `adapter.artifact.candidate_unbound` | `ADP-ART-001` | evidence | 外部产物缺少来源、内容身份、边界或被直接提升为可信制品 |
| `adapter.error.provenance_lost` | `ADP-ERR-001` | protocol | 协议、工具、任务与业务错误被合并或通过消息猜测 |
| `adapter.cancellation.finality_unproven` | `ADP-CAN-001` | session | 取消、断流或超时被当作停止、回滚或可复活终态 |
| `adapter.retry.not_authorized` | `ADP-RTY-001` | policy | 自动重试缺少幂等、去重、事后核对、预算或截止点依据 |
| `adapter.delivery.evidence_incomplete` | `ADP-DEL-001` | protocol | 流式、推送或轮询缺少认证、序列、去重、缺口或终结证据 |
| `adapter.security.envelope_invalid` | `ADP-SEC-001` | policy | 令牌透传、网络目标、租户披露或资源预算违反最小权限 |

## 10. 精确身份与签名错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `identity.domain.unbound` | `ID-DOM-001` | identity | 身份缺少对象、规范、表示、Profile 或域语境，或跨语境只比较摘要文本 |
| `identity.bytes.input_undefined` | `ID-BYT-001` | identity | 摘要输入范围、顺序、规范化或排除项不明确、可变或自包含循环 |
| `identity.reference.mutable` | `ID-REF-001` | identity | 安全引用缺少完整身份或依赖名称、路径、URL、latest、build ID 等可变选择器 |
| `identity.algorithm.disallowed` | `ID-ALG-001` | identity | 算法未知、禁用、撤销、参数不完整、用途不匹配或发生静默替换 |
| `identity.display.used_for_binding` | `ID-DSP-001` | identity | 截断摘要、短显示或 build ID 被用于安全比较和对象选择 |
| `identity.equivalence.overclaimed` | `ID-EQV-001` | semantic | 精确身份被提升为真假、语义等价或派生身份继承 |
| `identity.statement.context_incomplete` | `ID-STM-001` | evidence | 签名陈述缺少类型、用途、受众、主体、政策或受保护关键上下文 |
| `identity.envelope.material_incomplete` | `ID-ENV-001` | evidence | 验证包络未绑定陈述、只保存密钥提示、缺少必要材料或继承主体身份 |
| `identity.authority.overclaimed` | `ID-AUT-001` | policy | 签名、证书或日志包含被提升为事实、权限、满足或最终接受 |
| `identity.validity.context_incomplete` | `ID-VAL-001` | evidence | 有效性评估缺少截止点、信任根、政策、撤销或足够新鲜的状态材料 |
| `identity.reproducibility.unproven` | `ID-REP-001` | evidence | 可复现声明缺少精确输入、独立产出、完整输出身份或逐字节比较 |
| `identity.relation.inherited` | `ID-REL-001` | identity | 派生或伴随制品继承来源身份、签名、证据、接受状态、能力或未定义等价 |

## 11. 文本与标识符错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `text.slot.untyped` | `TEXT-SLT-001` | semantic | 字符串字段没有绑定来源、标识符、登记词、描述或显示职责 |
| `text.encoding.invalid` | `TEXT-ENC-001` | source | UTF-8 无效、非最短、含代理项或在解码前发生变换 |
| `text.source.provenance_incomplete` | `TEXT-SRC-001` | source | 原始字节、解码文本、变换、损失和身份关系没有分开 |
| `text.identifier.out_of_profile` | `TEXT-IDN-001` | semantic | 结构标识符超出 ASCII Profile 或受到规范化、大小写、locale、同形映射影响 |
| `text.normalization.implicit` | `TEXT-NRM-001` | semantic | 规范化没有绑定槽、Unicode 版本、形式、输出身份和损失 |
| `text.comparison.domain_unbound` | `TEXT-CMP-001` | identity | 搜索、排序、规范化、同形或模型相似比较替代精确身份与结构 ID |
| `text.range.unit_mismatch` | `TEXT-RNG-001` | semantic | 范围主体、表示、单位、半开区间或变换映射缺失或混用 |
| `text.bidi.boundary_hidden` | `TEXT-BID-001` | source | 双向显示改写逻辑顺序、隐藏方向控制或让视觉顺序参与身份 |
| `text.hidden.silent` | `TEXT-HID-001` | source | 不可见、变体、混合脚本或同形风险被静默删除、合并或隐藏 |
| `text.metadata.overclaimed` | `TEXT-MET-001` | semantic | 语言、媒体、方向或模型检测声明被用于隐式规范变换或权威判断 |
| `text.model.view_unbound` | `TEXT-AIM-001` | policy | 模型实际输入、预处理、tokenizer、隐藏字符清单和人工视图没有绑定 |
| `text.output.provenance_missing` | `TEXT-OUT-001` | evidence | 显示、复制、诊断或导出没有披露转义、截断、脱敏、方向与损失 |

## 12. 权威与授权决定错误码

| 错误码 | 主条款 | 层次 | 触发条件 |
| --- | --- | --- | --- |
| `authority.context.unbound` | `AUT-CTX-001` | policy | 政策、权威域、对象、动作、目的、受众、租户、条件或截止点未精确绑定 |
| `authority.principal.unqualified` | `AUT-PRN-001` | policy | 认证、签名、成员资格或自描述被当作当前决定权限 |
| `authority.scope.amplified` | `AUT-SCP-001` | policy | 通配符、前缀、环境权限、未知字段或错误比较扩大授权范围 |
| `authority.semantic.unreviewed` | `AUT-SEM-001` | semantic | 模型候选、置信度、结构合法、截断视图或未区分批量点击确认语义 |
| `authority.decision.incomplete` | `AUT-DEC-001` | policy | 授权决定缺少请求、对象、范围、语境、依据、主体、理由或有限结果 |
| `authority.delegation.amplified` | `AUT-DEL-001` | policy | 委托隐藏行动者、允许冒充、形成循环、超深或扩大范围、期限与预算 |
| `authority.multi.conflicted` | `AUT-MUL-001` | policy | 多权威门槛未预注册、主体重复、冲突未解决或到达顺序改变决定 |
| `authority.consent.unbound` | `AUT-CNS-001` | policy | 人类视图与机器请求不一致、目的或接收方隐藏、拒绝不可达或同意者无权 |
| `authority.validity.stale` | `AUT-TIM-001` | policy | 授权过期、撤销、状态不新鲜、主体或政策漂移，或缓存成功无限复用 |
| `authority.replay.detected` | `AUT-RPL-001` | policy | 决定跨对象、动作、目的、受众或会话使用，或超过允许次数 |
| `authority.capability.outside_intersection` | `AUT-CAP-001` | policy | 能力使用并集、环境权限、token 透传、协议挑战或原地 step-up 扩大旧会话 |
| `authority.result.overclaimed` | `AUT-SEP-001` | policy | 授权被提升为真值、满足、证据充分、最终接受、会话完成或模型权威 |

## 13. 稳定性边界

上述机器码只在当前规范、目录和提案向量中保持草案稳定，尚不构成发行 ABI。提升为稳定接口前必须完成：

1. producer、inspector 与 runner 对共同失败给出相同的主层次与适用机器码；
2. 并发、截断、乱序、重复、资源耗尽、外部协议降级和秘密注入向量齐全；
3. 诊断 Profile 确定数量、深度、位置、消息和总输出预算；
4. 文本、SARIF、HTTP、MCP 与遥测适配前后保持机器语义；
5. CLI 退出状态与结构化物理编码由单独 ADR 和规范字节确定。

当前目录只定义草案机器码及其职责。producer、inspector、runner、诊断生产器、渲染器和协议适配器均未实现。
