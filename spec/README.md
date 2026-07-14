# Noemion 规范源

本目录保存实现可以逐条引用的规范源。公开 HTML 负责直白解释和阅读入口；本目录负责版本、条款 ID、规范强度与验证映射。二者冲突时，先停止实现并通过 ADR 修正文档，不能由当前代码行为反向改写规范。

## 当前规范

| 规范 | 版本 | 状态 | 已覆盖 | 明确未覆盖 |
| --- | --- | --- | --- | --- |
| [`endem-core.md`](endem-core.md) | `0.1.0-draft` | 通用内容标准草案；已接受语义与规范分层的条款化表达 | Endem 最小性、六个语义面、内容 Profile、分层符合性、事态与方向分离、单变量量化、测量阈值、复合判据、未知状态、确定性、安全读取、身份分层与验证责任 | 量化、测量与组合物理字段、嵌套或多变量量化、条件适用性、时间、求值、摘要与签名物理 Profile |
| [`endem-format.md`](endem-format.md) | `0.1.0-draft` | 已采用的实验性容器草案；尚非稳定 ABI | 固定前导、定宽目录、确定性 CBOR、END-P0 结构实验与 END-P1 封闭内容 Profile | coherent/attested、签名、压缩、Synem 和跨版本承诺 |
| [`endem-source-manifest.md`](endem-source-manifest.md) | `0.1.0-draft` | 实验性 Ktisor 输入；正式来源语言出现后删除 | UTF-8 逐行指令、转义、基数、授权边界和 END-P1 映射 | 注释元数据、包含、模块、量化、时间、求值语言和兼容承诺 |
| [`synem-core.md`](synem-core.md) | `0.1.0-draft` | 草案；已接受组合闭包边界的第一份条款化表达 | 完整闭包、精确绑定、有限无环、权限交集、成员结果分离与会话激活 | 物理容器、版本范围语法、符号、调度、远程仓库和稳定 ABI |
| [`dromen-core.md`](dromen-core.md) | `0.1.0-draft` | 草案；已接受一次会话契约的第一份条款化表达 | 精确主体、政策与环境绑定、能力和预算求交、秘密外置、观察责任、只读失效与销毁 | 运行 API、沙箱、凭据代理、事件编码、恢复策略和组件实现；永远不建立 Dromen 文件 |
| [`iknem-core.md`](iknem-core.md) | `0.1.0-draft` | 草案；已接受证据与评估边界的第一份条款化表达 | 主体范围、溯源、phain 对齐、证据类别、完整性、有效性、覆盖、决定分离与最小披露 | 物理容器、签名算法、透明日志、撤销分发、时钟归并、隐私策略和稳定 ABI |
| [`adapter-core.md`](adapter-core.md) | `0.1.0-draft` | 草案；已接受外部协议适配边界的第一份条款化表达 | 版本、对端、能力、调用、映射、状态、产物、错误、取消、重试、交付与安全边界 | 具体协议 Profile、适配器 API、物理字段、凭据代理、事件存储和组件实现 |
| [`identity-core.md`](identity-core.md) | `0.1.0-draft` | 草案；已接受跨制品精确身份与签名边界的第一份条款化表达 | 身份域、精确字节、不可变引用、算法政策、短显示、签名陈述、验证包络、权威、截止点、可复现性与派生关系 | 发行算法、摘要语法、签名物理 Profile、证书、透明日志、撤销分发、Semantic Key 和组件实现 |
| [`text-identifier-core.md`](text-identifier-core.md) | `0.1.0-draft` | 草案；已接受跨制品文本与标识符边界的第一份条款化表达 | 文本槽、严格 UTF-8、来源溯源、ASCII 标识符、规范化、比较、范围、双向显示、隐藏字符、元数据、模型输入与输出视图 | Unicode 标识符、来源重写、分词、搜索排序、tokenizer 协议、原始字节字段和组件实现 |
| [`authority-core.md`](authority-core.md) | `0.1.0-draft` | 草案；已接受跨制品权威与授权决定边界的第一份条款化表达 | 权威语境、主体资格、封闭范围、语义授权、委托、同意、多人决定、时效、重放、能力交集与结果分离 | 权威目录、角色与政策语言、物理编码、同意 UI Profile、凭据、撤销分发和组件实现 |

[`endem-threat-model.md`](endem-threat-model.md) 把单个 Endem 的不可信输入与失败责任映射到规范条款；[`synem-threat-model.md`](synem-threat-model.md) 单独处理依赖替换、闭包截断、循环、权限放大、结果洗白与激活竞态；[`dromen-threat-model.md`](dromen-threat-model.md) 处理主体替换、陈旧政策、环境漂移、能力放大、秘密持久化、预算逃逸和会话复活；[`iknem-threat-model.md`](iknem-threat-model.md) 处理范围漂白、循环自证、观察升级、撤销失明、覆盖伪造、决定越权和泄密。[`profiles/end-p0.json`](profiles/end-p0.json) 给出第一组跨实现实验的有限上限；这些数值不是生产规模证明，提高时必须采用新的 Profile 身份。

[`diagnostics-core.md`](diagnostics-core.md) 定义跨对象诊断内容边界，[`diagnostic-catalog.md`](diagnostic-catalog.md) 登记草案机器码。[`registry.json`](registry.json) 是机器可读的规范、术语、条款、威胁、成熟度与验证登记。`../vectors/semantic/` 保存 JSON 语义外壳；`../vectors/diagnostics/` 保存诊断资料一致性提案；`../vectors/wire/` 保存真实字节的十六进制表达。这些向量都不表示组件已经实现。

[`adapter-threat-model.md`](adapter-threat-model.md) 与 [`adapter-scenarios.md`](adapter-scenarios.md) 分别保存外部协议适配威胁和非规范设计场景。`../vectors/adapters/cases.json` 保存 ADP-CORE 的提案向量；`../tests/adapter_vector_test.py` 只检查十二条抽象规则，不实现 MCP、A2A、HTTP、SDK、凭据、重试、Webhook、Drasor 或运行时。精确场景与向量范围以对应源文件和测试输出为准。

[`identity-threat-model.md`](identity-threat-model.md) 与 [`identity-scenarios.md`](identity-scenarios.md) 分别保存精确身份与签名威胁和十五个非规范设计场景。`../vectors/identity/cases.json` 保存 ID-CORE 的二十四个提案向量；`../tests/identity_vector_test.py` 只检查十二条抽象规则，不实现摘要器、签名器、验证器、证书、透明日志、撤销分发、可复现构建或发布系统。

[`text-identifier-threat-model.md`](text-identifier-threat-model.md) 与 [`text-identifier-scenarios.md`](text-identifier-scenarios.md) 分别保存文本与标识符威胁和十五个非规范设计场景。`../vectors/text-identifier/cases.json` 保存 TEXT-IDENTIFIER-CORE 的二十四个提案向量；`../tests/text_identifier_vector_test.py` 只检查十二条抽象规则，不实现 UTF-8 解码器、规范化器、双向显示器、同形检测器、文本编辑器或模型输入网关。

[`authority-threat-model.md`](authority-threat-model.md) 与 [`authority-scenarios.md`](authority-scenarios.md) 分别保存权威与授权决定威胁和十五个非规范设计场景。`../vectors/authority/cases.json` 保存 AUT-CORE 的二十四个提案向量；`../tests/authority_vector_test.py` 只检查十二条抽象规则，不实现身份提供方、权威目录、政策求值器、同意界面、能力代理或决定服务。

[`model-context-assembly-proposal.md`](model-context-assembly-proposal.md) 研究模型调用前的输入选择、角色、权威、顺序、变换、截断、缓存和损失边界。它只比较 TEXT-IDENTIFIER、AUT、ADP、DRO、IKN 与 DIA 的现有责任是否留下横切缺口，不是 ADR、CORE 规范、Profile、制品、命令或组件，也不进入 `registry.json`。当前首选是把未来唯一条款归还现有规范；只有真实消费者和验证证明职责无法清晰分担时，才重新讨论独立规范。

[`gnu-elf-applicability-proposal.md`](gnu-elf-applicability-proposal.md) 把 ELF 与 GNU Binutils 的 Section/Segment、符号、重定位、链接脚本、形成映射、裁剪、调试分离、Build ID、独立读取和 BFD 信息损失逐项映射到现有 Noemion 责任。它是非规范研究资料，不创建“自然语言 ELF”、新制品、格式、命令或组件，也不进入 `registry.json`。未来只有在真实生产者、消费者、失败责任、反例和正反向量齐备后，相关机制才可以提出 ADR。

[`planning-and-replanning-proposal.md`](planning-and-replanning-proposal.md) 研究 Endem/Synem 目标、Dromen 会话边界、可变计划、外部 Task、行动轨迹、Iknem 与最终决定怎样保持分离。它用 GNU Make 的 target/prerequisite/recipe 分离、ReAct、A2A 1.0.0、MCP experimental Tasks 和 OpenAI Agents SDK 核对现实 Agent 工作流，但不创建计划制品、计划格式、计划命令、计划组件或 `PLAN-CORE`，也不进入 `registry.json`。当前首选是把未来唯一义务归还现有 END、SYN、DRO、IKN、AUT、ADP、DIA 与 TEXT-IDENTIFIER 责任。

[`semantic-equivalence-and-migration-proposal.md`](semantic-equivalence-and-migration-proposal.md) 研究精确身份、封闭结构同构、有范围观察等价、版本化迁移、强化/弱化和模型相似度怎样分开。它用 W3C RDFC-1.0、RFC 8785、Unicode UAX #15、YANG 更新规则、GNU BFD/objcopy、Sentence-BERT、LLM-as-a-Judge 与 NIST AI 800-3 检查规范化和模型判断的适用域。它不创建等价制品、迁移格式、Semantic Key、命令、组件或 CORE，也不进入 `registry.json`；当前首选是把未来唯一义务归还现有 ID、END、SYN、TEXT-IDENTIFIER、AUT、IKN、ADP、DIA 与 DRO 责任。

[`state-change-and-causal-attribution-proposal.md`](state-change-and-causal-attribution-proposal.md) 研究 `kine`、终态满足、动作发生、状态转变、因果归因、授权责任与最终决定怎样分开。它用 GNU Make、Kubernetes 控制器、W3C PROV、CloudEvents、OpenTelemetry、RFC 9110、ReAct 与 A2A 检查现实执行边界。它不改写 END-TEL-001，不创建因果制品、动作格式、命令、组件或 CORE，也不进入 `registry.json`；当前建议把 `kine` 理解为目标方向，强行动或因果主张必须由结构和有范围证据显示。

[`telis-release-terms-proposal.md`](telis-release-terms-proposal.md) 分开 `telis` 已接受的两个目标方向与尚未通过的发行拼写。权威词典、GNU Names 原则和职责透明度已经足以排除 `kine/mene` 作为首次正式发行拼写；现行规范值暂不改变，`reach/maintain` 只取得进入独立人类朗读、听写、职责匹配和反例验证的资格。提案不是 ADR、CORE、Profile 或登记项，不建立别名，也不提前改写 END-TEL-001。

[`release-terminology-simplification-proposal.md`](release-terminology-simplification-proposal.md) 先审查对象、角色和动作是否真的需要专名，再比较 Endem closure、session contract、scoped evidence record、deterministic producer、independent inspector、bounded runner 与 `form/check/compose/inspect/run`。它保留现行职责、结果域、权限和测试边界，不进入 `registry.json`，也不提前修改 SYN-CORE、DRO-CORE、IKN-CORE、字段、路由或 CLI；接受方向后仍须经过独立人类验证和单独迁移 ADR。

[`semantic-facet-terminology-proposal.md`](semantic-facet-terminology-proposal.md) 把同一必要性门禁应用到 `rhem/semion/skena/telis/krin/apor/phain`。它建议保留全部语义与观察边界，同时用 `source_expression/meaning_projection/situation/goal_direction/satisfaction_criteria/unresolved_meaning/structured_observation` 进入人类验证。提案不进入 `registry.json`，不提前修改 END-CORE、END-FMT、END-P1、来源清单、诊断或向量；即使数字记录布局不变，未来迁移也必须显式处理新规范与 Profile 身份。

[`lifecycle-and-result-terminology-proposal.md`](lifecycle-and-result-terminology-proposal.md) 审查 `nascent/coherent/attested` 与各结果词。它判定 `attested` 不应继续把外部签名或证明关系伪装成内容自身状态，并把迁移拆成对象边界修正与发行命名验证两条轴。前者设计精确内容、外部陈述集合、逐项验证、截止点、撤销和依赖方政策的显式关系；后者才比较 `formed/resolved/undetermined/no_allowed_projection/stopped`，仍须人类证据。提案不进入 `registry.json`，也不提前改写 END-CORE、DRO-CORE 或向量。

[`preview-simulation-and-approval-proposal.md`](preview-simulation-and-approval-proposal.md) 研究预览、dry-run、模拟、授权、执行尝试、事后观察、满足与最终决定怎样保持分离。它用 GNU Make、MCP 2025-11-25、A2A 1.0.0、OpenAI Agents SDK 与 NIST AI 600-1 检查当前 Agent 审批流程。它不创建预览制品、模拟格式、批准结果域、命令、组件或 CORE，也不进入 `registry.json`；当前首选是把显示、授权、会话漂移、外部调用、观察和满足义务归还现有 TEXT-IDENTIFIER、AUT、DRO、ADP、IKN、ID、END 与 DIA 责任。

[`memory-checkpoint-and-resumption-proposal.md`](memory-checkpoint-and-resumption-proposal.md) 研究九类状态怎样保持分离，包括会话历史、跨运行记忆或提炼指导、上下文压缩、计划检查点、外部 Task 句柄、持久工作区、恢复、重放与回滚。它用 OpenAI Agents SDK 对话状态策略、OpenAI Sandbox Agents 跨运行记忆、MCP 当前版及发布候选、A2A 1.0、GNU Make 与 GNU Guix 核对现实持久状态机制。它不创建记忆制品、检查点格式、恢复命令、组件或 CORE，也不进入 `registry.json`；当前首选是把变换、身份、新会话、外部任务、授权消费、证据和诊断义务归还现有 TEXT-IDENTIFIER、ID、DRO、ADP、AUT、IKN、DIA、END 与 SYN 责任。

[`capability-discovery-and-negotiation-proposal.md`](capability-discovery-and-negotiation-proposal.md) 研究能力声明、协议协商、授权决定、Dromen 会话上限、即时可调用性与调用事实怎样保持分离。它用 MCP 2025-11-25、A2A 1.0、RFC 8707 与 GNU Autoconf 2.73 核对动态工具列表、受众、scope、schema 漂移和特性探测。它不创建 `CAP-CORE`、能力制品、目录格式、命令、组件或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 ADP、AUT、DRO、DIA、IKN、ID、TEXT-IDENTIFIER 与 END 责任。

[`parallel-and-speculative-execution-proposal.md`](parallel-and-speculative-execution-proposal.md) 研究并行意图、分支准入、执行尝试、候选结果、提交选择、外部副作用和后验观察怎样保持分离。它用 MCP 2025-11-25 Tasks、MCP Sampling 草案、A2A 1.0、GNU Make 并行与 jobserver、中断处理和 RFC 9110 强前提核对现实 Agent 工作流。它不创建 `PAR-CORE`、并行制品、事务格式、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把共享能力与预算、分支授权、提交前提、重叠证据和诊断义务归还现有 DRO、AUT、ADP、ID、IKN、DIA、END 与 SYN 责任。

[`model-adapter-isolation-proposal.md`](model-adapter-isolation-proposal.md) 研究模型输入、确定性控制面、授权、凭据与实时句柄、协议适配、文件、网络、资源终止、观察和外部目标怎样形成可审查的隔离责任。它用 MCP 与 A2A 安全规范、Linux `no_new_privs`、seccomp、Landlock、cgroup v2、GNU Guix shell、Coreutils `timeout` 与 Make jobserver 核对机制覆盖和采用限制。它不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、沙箱格式、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 DRO、AUT、ADP、DIA、IKN、ID 与 TEXT-IDENTIFIER 责任。

[`model-assisted-evaluation-proposal.md`](model-assisted-evaluation-proposal.md) 研究评测目的、构念、可观察标准、题目与候选、协议、模型评审调用、原始输出、统计汇总和使用决定怎样保持分离。它用 NIST AI 800-2 初稿、NIST AI 800-3、NeurIPS 与 ICLR 的模型裁判研究，以及 GNU Diffutils、Coreutils 随机来源和排序规则核对偏差、随机性、依赖、漂移与限定主张。它不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品、裁判对象、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 END、TEXT-IDENTIFIER、ID、ADP、DRO、IKN、AUT 与 DIA 责任。

[`model-training-and-update-boundaries-proposal.md`](model-training-and-update-boundaries-proposal.md) 研究训练数据、反馈记录、基础模型、适配权重、训练活动、环境复现、行为评测、发布、回滚与运行观察怎样保持分离。它用 NIST AI 600-1、NIST SP 800-218A、RLHF、DPO、递归生成数据研究、GNU Guix 与 Diffutils 核对来源、资格、投毒、反馈回路、派生身份和复现边界。它不创建 `TRAIN-CORE`、`MODEL-CORE`、`FEEDBACK-CORE`、模型制品、训练清单格式、训练平台、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 TEXT-IDENTIFIER、ID、AUT、IKN、ADP、DRO、DIA 与 END 责任。

[`model-openness-and-software-freedom-boundaries-proposal.md`](model-openness-and-software-freedom-boundaries-proposal.md) 研究托管服务、参数、架构、推理与训练代码、训练数据说明、数据、文档、许可、首选修改形式、复现和外部开放分类怎样保持分离。它用 GNU 自由软件定义、OSI Open Source AI Definition 1.0、Linux Foundation Model Openness Framework、NIST AI 600-1 与 NIST SP 800-218A 核对用户自由、发布完整性、供应链和证据边界。它不创建 `OPEN-MODEL-CORE`、`LICENSE-CORE`、模型发行格式、合规服务、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 ID、AUT、IKN、ADP、TEXT-IDENTIFIER 与 DIA 责任。

[`hosted-ai-service-and-user-control-boundaries-proposal.md`](hosted-ai-service-and-user-control-boundaries-proposal.md) 研究第三方托管执行、自主管理执行、设备内执行和通信服务怎样保持分离，并逐项检查实际执行者、控制平面、数据外发、隐藏变换、保留、下游服务、状态、导出、切换、停服、观察与复现。它用 GNU 对他人服务替代用户计算的分析、AGPL 边界、MCP Sampling 与授权规范、NIST AI 供应链资料和当前模型服务数据控制核对用户控制。它不创建服务 CORE、网关、云平台、导出格式、命令、组件、结果域或新专名，也不进入 `registry.json`；当前首选是把唯一义务归还现有 ID、ADP、AUT、DRO、IKN、TEXT-IDENTIFIER、DIA 与 END 责任。

[`endem-scenarios.md`](endem-scenarios.md) 是非规范性的自然语言设计审查语料。它用三十个场景检查达到成立、持续保持、否定事态、指称歧义、观察不足、求值故障、授权不足、多根拆分、结果域、时间范围、缺席推断、量化范围、测量阈值、复合判断以及内容与授权伴随关系是否能被现行体系解释。它不规定语法或字节，也不是可执行测试；案例暴露的缺口必须回到 ADR、规范条款或开放问题。

[`synem-scenarios.md`](synem-scenarios.md) 用十个非规范场景检查闭包、绑定、可选依赖、权限、成员结果和激活边界。它同样不是语法、解析器或组件证据。

[`iknem-scenarios.md`](iknem-scenarios.md) 用十四个非规范场景检查证据范围、溯源、观察、类别、有效性、覆盖、决定和最小披露。它不是 Iknem 格式、采集器、验证器或决定引擎。

[`dromen-scenarios.md`](dromen-scenarios.md) 用十五个非规范场景检查会话主体、政策、环境、能力、秘密、预算、激活、观察、只读失效和销毁。它不是 Dromen 格式、装载器、沙箱、凭据代理或运行时。

`../vectors/result-domains/cases.json` 保存 ADR-0015 的十二个正反提案向量；`../tests/result_domain_vector_test.py` 只执行结果域约束，不实现 Drasor、求值器或决定引擎。向量通过只能证明当前矩阵和条款一致，不能证明运行组件存在。

`../vectors/mene/cases.json` 保存 ADR-0016 的十二个时间与连续性提案向量；`../tests/mene_vector_test.py` 只执行 fixed/elapsed 范围、strict/budgeted 政策和覆盖分类，不实现时钟、监控器、Drasor 或求值器。

`../vectors/negation/cases.json` 保存 ADR-0017 的十二个否定与缺席提案向量；`../tests/negation_vector_test.py` 只执行显式负观察、空结果、封闭范围、正反例和观察故障分类，不实现日志收集器、Drasor 或求值器。

`../vectors/quantification/cases.json` 保存 ADR-0018 的十二个量化与成员资格提案向量；`../tests/quantification_vector_test.py` 只检查成员范围、空集合、不同成员计数和决定性聚合，不实现 Ktisor、Drasor、成员目录或求值器。

`../vectors/measurement/cases.json` 保存 ADR-0019 的十二个测量与阈值提案向量；`../tests/measurement_vector_test.py` 只检查构念、总体、单位、程序、聚合器、不确定区间与阈值分类，不实现采集器、统计引擎、Drasor 或求值器。

`../vectors/composition/cases.json` 保存 ADR-0020 的十二个复合事态与判据提案向量；`../tests/composition_vector_test.py` 只检查单根边界、有限无环拓扑、叶对齐、四结果传播和决定性短路，不实现解析器、Drasor、运行时或求值器。

`../vectors/synem/cases.json` 保存 ADR-0021 的十二个闭包与条件激活提案向量；`../tests/synem_vector_test.py` 只检查六条 SYN-CORE 规则，不实现解析器、Pleko、Drasor、运行时或求值器。

`../vectors/iknem/cases.json` 保存 ADR-0022 的十五个证据与评估提案向量；`../tests/iknem_vector_test.py` 只检查九条 IKN-CORE 规则，不实现采集器、验证器、归并器、撤销服务、决定引擎或运行时。

`../vectors/dromen/cases.json` 保存 ADR-0024 的二十个会话契约提案向量；`../tests/dromen_vector_test.py` 只检查十条 DRO-CORE 规则，不实现装载器、沙箱、凭据代理、Drasor、事件系统或运行时。

`../vectors/diagnostics/cases.json` 保存 ADR-0025 的二十个结构化诊断提案向量；`../tests/diagnostic_vector_test.py` 只检查十条 DIA-CORE 规则，不实现诊断生产器、渲染器、协议适配器、重试引擎或 CLI。

`registry.json` 还登记非规范实验及其决定链。P0-LANG-001 的协议与结果位于 `../experiments/p0-language/`；它支持 ADR-0012 的首版核心语言决定，但不会改变 END-CORE 或 END-FMT 的条款含义，也不把原型登记为生产实现。

## 规范强度

只有大写的 `MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT` 与 `MAY` 具有规范强度，解释遵循 BCP 14。正文在首次出现时同时给出中文含义。

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

普通中文“必须、不得、可以”用于解释时仍应忠实于相邻条款，但不能替代条款 ID。每条实现义务只能由一个主条款定义；其他文档只能引用，不能复制第二套要求。

## 成熟度维度

规范状态、实现状态与证据状态分开登记：

- `decision_status`：设计边界是否已经由当前 ADR 接受；
- `implementation_status`：是否存在声称符合该条款的实现；
- `evidence_status`：仓库内是否已有覆盖向量或测试；
- `wire_status`：物理编码是否冻结。

`implementation_status` 当前只允许 `unimplemented` 与 `vector-checker-only`。后者表示仓库存在只服务规范资料的检查脚本，不表示项目组件已经实现。`decision_status: accepted` 不表示实现存在，也不表示证据充分；`wire_status: experimental-draft` 只允许草案向量，任何程序都不得声称产生可互操作的稳定 `.endem` 字节。

## 变更规则

1. 改变现有条款含义时，先新增或更新 ADR，再提升规范版本。
2. 新条款必须登记唯一 ID、成熟度、失败责任与验证方式。
3. 删除条款必须保留版本历史，并说明替代条款或删除理由。
4. `covered-by-repo` 只能用于仓库中实际存在且由自动检查读取的证据。
5. `planned` 表示验证尚未实现，不能在公开页面写成已经通过。
6. 格式草案变化必须同步 ADR、END-FMT、Profile、错误目录、登记和正反字节向量；不得把语义向量 JSON 直接改名为 `.endem`。
7. 场景语料变化必须保持非规范状态；只有转化为唯一条款、登记验证方式并形成正反向量后，案例中的判断才可能成为符合性要求。
