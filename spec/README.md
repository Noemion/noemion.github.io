# Noemion 规范源

本目录保存实现可以逐条引用的规范源。公开 HTML 负责直白解释和阅读入口；本目录负责版本、条款 ID、规范强度与验证映射。二者冲突时，先停止实现并通过 ADR 修正文档，不能由当前代码行为反向改写规范。

## 当前规范

| 规范 | 版本 | 状态 | 已覆盖 | 明确未覆盖 |
| --- | --- | --- | --- | --- |
| [`endem-core.md`](endem-core.md) | `0.1.0-draft` | 通用内容标准草案；已接受语义与规范分层的条款化表达 | Endem 最小性、六个语义面、内容 Profile、分层符合性、事态与方向分离、单变量量化、测量阈值、复合判据、未知状态、确定性、安全读取、身份分层与验证责任 | 量化、测量与组合物理字段、嵌套或多变量量化、条件适用性、时间、求值、摘要与签名物理 Profile |
| [`endem-format.md`](endem-format.md) | `0.1.0-draft` | 已采用的实验性容器草案；尚非稳定 ABI | 固定前导、定宽目录、确定性 CBOR、END-P0 结构实验与 END-P1 封闭内容 Profile | coherent/attested、签名、压缩、Synem 和跨版本承诺 |
| [`endem-source-manifest.md`](endem-source-manifest.md) | `0.1.0-draft` | 实验性 Poiet 输入；正式来源语言出现后删除 | UTF-8 逐行指令、转义、基数、授权边界和 END-P1 映射 | 注释元数据、包含、模块、量化、时间、求值语言和兼容承诺 |
| [`synem-core.md`](synem-core.md) | `0.1.0-draft` | 草案；已接受组合闭包边界的第一份条款化表达 | 完整闭包、精确绑定、有限无环、权限交集、成员结果分离与会话激活 | 物理容器、版本范围语法、符号、调度、远程仓库和稳定 ABI |
| [`dromen-core.md`](dromen-core.md) | `0.1.0-draft` | 草案；已接受一次会话契约的第一份条款化表达 | 精确主体、政策与环境绑定、能力和预算求交、秘密外置、观察责任、只读失效与销毁 | 运行 API、沙箱、凭据代理、事件编码、恢复策略和组件实现；永远不建立 Dromen 文件 |
| [`iknem-core.md`](iknem-core.md) | `0.1.0-draft` | 草案；已接受证据与评估边界的第一份条款化表达 | 主体范围、溯源、phain 对齐、证据类别、完整性、有效性、覆盖、决定分离与最小披露 | 物理容器、签名算法、透明日志、撤销分发、时钟归并、隐私策略和稳定 ABI |
| [`adapter-core.md`](adapter-core.md) | `0.1.0-draft` | 草案；已接受外部协议适配边界的第一份条款化表达 | 版本、对端、能力、调用、映射、状态、产物、错误、取消、重试、交付与安全边界 | 具体协议 Profile、适配器 API、物理字段、凭据代理、事件存储和组件实现 |
| [`identity-core.md`](identity-core.md) | `0.1.0-draft` | 草案；已接受跨制品精确身份与签名边界的第一份条款化表达 | 身份域、精确字节、不可变引用、算法政策、短显示、签名陈述、验证包络、权威、截止点、可复现性与派生关系 | 发行算法、摘要语法、签名物理 Profile、证书、透明日志、撤销分发、Semantic Key 和组件实现 |
| [`text-core.md`](text-core.md) | `0.1.0-draft` | 草案；已接受跨制品文本与标识符边界的第一份条款化表达 | 文本槽、严格 UTF-8、来源溯源、ASCII 标识符、规范化、比较、范围、双向显示、隐藏字符、元数据、模型输入与输出视图 | Unicode 标识符、来源重写、分词、搜索排序、tokenizer 协议、原始字节字段和组件实现 |
| [`authority-core.md`](authority-core.md) | `0.1.0-draft` | 草案；已接受跨制品权威与授权决定边界的第一份条款化表达 | 权威语境、主体资格、封闭范围、语义授权、委托、同意、多人决定、时效、重放、能力交集与结果分离 | 权威目录、角色与政策语言、物理编码、同意 UI Profile、凭据、撤销分发和组件实现 |

[`endem-threat-model.md`](endem-threat-model.md) 把单个 Endem 的不可信输入与失败责任映射到规范条款；[`synem-threat-model.md`](synem-threat-model.md) 单独处理依赖替换、闭包截断、循环、权限放大、结果洗白与激活竞态；[`dromen-threat-model.md`](dromen-threat-model.md) 处理主体替换、陈旧政策、环境漂移、能力放大、秘密持久化、预算逃逸和会话复活；[`iknem-threat-model.md`](iknem-threat-model.md) 处理范围漂白、循环自证、观察升级、撤销失明、覆盖伪造、决定越权和泄密。[`profiles/end-p0.json`](profiles/end-p0.json) 给出第一组跨实现实验的有限上限；这些数值不是生产规模证明，提高时必须采用新的 Profile 身份。

[`diagnostics-core.md`](diagnostics-core.md) 定义跨对象诊断内容边界，[`diagnostic-catalog.md`](diagnostic-catalog.md) 登记草案机器码。[`registry.json`](registry.json) 是机器可读的规范、术语、条款、威胁、成熟度与验证登记。`../vectors/semantic/` 保存 JSON 语义外壳；`../vectors/diagnostics/` 保存诊断资料一致性提案；`../vectors/wire/` 保存真实字节的十六进制表达。这些向量都不表示组件已经实现。

[`adapter-threat-model.md`](adapter-threat-model.md) 与 [`adapter-scenarios.md`](adapter-scenarios.md) 分别保存外部协议适配威胁和十八个非规范设计场景。`../vectors/adapters/cases.json` 保存 ADP-CORE 的二十四个提案向量；`../tests/adapter_vector_test.py` 只检查十二条抽象规则，不实现 MCP、A2A、HTTP、SDK、凭据、重试、Webhook、Drasor 或运行时。

[`identity-threat-model.md`](identity-threat-model.md) 与 [`identity-scenarios.md`](identity-scenarios.md) 分别保存精确身份与签名威胁和十八个非规范设计场景。`../vectors/identity/cases.json` 保存 ID-CORE 的二十四个提案向量；`../tests/identity_vector_test.py` 只检查十二条抽象规则，不实现摘要器、签名器、验证器、证书、透明日志、撤销分发、可复现构建或发布系统。

[`text-threat-model.md`](text-threat-model.md) 与 [`text-scenarios.md`](text-scenarios.md) 分别保存文本与标识符威胁和十八个非规范设计场景。`../vectors/text/cases.json` 保存 TXT-CORE 的二十四个提案向量；`../tests/text_vector_test.py` 只检查十二条抽象规则，不实现 UTF-8 解码器、规范化器、双向显示器、同形检测器、文本编辑器或模型输入网关。

[`authority-threat-model.md`](authority-threat-model.md) 与 [`authority-scenarios.md`](authority-scenarios.md) 分别保存权威与授权决定威胁和十八个非规范设计场景。`../vectors/authority/cases.json` 保存 AUT-CORE 的二十四个提案向量；`../tests/authority_vector_test.py` 只检查十二条抽象规则，不实现身份提供方、权威目录、政策求值器、同意界面、能力代理或决定服务。

[`model-context-assembly-proposal.md`](model-context-assembly-proposal.md) 研究模型调用前的输入选择、角色、权威、顺序、变换、截断、缓存和损失边界。它只比较 TXT、AUT、ADP、DRO、IKN 与 DIA 的现有责任是否留下横切缺口，不是 ADR、CORE 规范、Profile、制品、命令或组件，也不进入 `registry.json`。当前首选是把未来唯一条款归还现有规范；只有真实消费者和验证证明职责无法清晰分担时，才重新讨论独立规范。

[`gnu-elf-applicability-proposal.md`](gnu-elf-applicability-proposal.md) 把 ELF 与 GNU Binutils 的 Section/Segment、符号、重定位、链接脚本、形成映射、裁剪、调试分离、Build ID、独立读取和 BFD 信息损失逐项映射到现有 Noemion 责任。它是非规范研究资料，不创建“自然语言 ELF”、新制品、格式、命令或组件，也不进入 `registry.json`。未来只有在真实生产者、消费者、失败责任、反例和正反向量齐备后，相关机制才可以提出 ADR。

[`endem-scenarios.md`](endem-scenarios.md) 是非规范性的自然语言设计审查语料。它用三十个场景检查达到成立、持续保持、否定事态、指称歧义、观察不足、求值故障、授权不足、多根拆分、结果域、时间范围、缺席推断、量化范围、测量阈值、复合判断以及内容与授权伴随关系是否能被现行体系解释。它不规定语法或字节，也不是可执行测试；案例暴露的缺口必须回到 ADR、规范条款或开放问题。

[`synem-scenarios.md`](synem-scenarios.md) 用十个非规范场景检查闭包、绑定、可选依赖、权限、成员结果和激活边界。它同样不是语法、解析器或组件证据。

[`iknem-scenarios.md`](iknem-scenarios.md) 用十四个非规范场景检查证据范围、溯源、观察、类别、有效性、覆盖、决定和最小披露。它不是 Iknem 格式、采集器、验证器或决定引擎。

[`dromen-scenarios.md`](dromen-scenarios.md) 用十五个非规范场景检查会话主体、政策、环境、能力、秘密、预算、激活、观察、只读失效和销毁。它不是 Dromen 格式、装载器、沙箱、凭据代理或运行时。

`../vectors/result-domains/cases.json` 保存 ADR-0015 的十二个正反提案向量；`../tests/result_domain_vector_test.py` 只执行结果域约束，不实现 Drasor、求值器或决定引擎。向量通过只能证明当前矩阵和条款一致，不能证明运行组件存在。

`../vectors/mene/cases.json` 保存 ADR-0016 的十二个时间与连续性提案向量；`../tests/mene_vector_test.py` 只执行 fixed/elapsed 范围、strict/budgeted 政策和覆盖分类，不实现时钟、监控器、Drasor 或求值器。

`../vectors/negation/cases.json` 保存 ADR-0017 的十二个否定与缺席提案向量；`../tests/negation_vector_test.py` 只执行显式负观察、空结果、封闭范围、正反例和观察故障分类，不实现日志收集器、Drasor 或求值器。

`../vectors/quantification/cases.json` 保存 ADR-0018 的十二个量化与成员资格提案向量；`../tests/quantification_vector_test.py` 只检查成员范围、空集合、不同成员计数和决定性聚合，不实现 Poiet、Drasor、成员目录或求值器。

`../vectors/measurement/cases.json` 保存 ADR-0019 的十二个测量与阈值提案向量；`../tests/measurement_vector_test.py` 只检查构念、总体、单位、程序、聚合器、不确定区间与阈值分类，不实现采集器、统计引擎、Drasor 或求值器。

`../vectors/composition/cases.json` 保存 ADR-0020 的十二个复合事态与判据提案向量；`../tests/composition_vector_test.py` 只检查单根边界、有限无环拓扑、叶对齐、四结果传播和决定性短路，不实现解析器、Drasor、运行时或求值器。

`../vectors/synem/cases.json` 保存 ADR-0021 的十二个闭包与条件激活提案向量；`../tests/synem_vector_test.py` 只检查六条 SYN-CORE 规则，不实现解析器、Pleko、Drasor、运行时或求值器。

`../vectors/iknem/cases.json` 保存 ADR-0022 的十八个证据与评估提案向量；`../tests/iknem_vector_test.py` 只检查九条 IKN-CORE 规则，不实现采集器、验证器、归并器、撤销服务、决定引擎或运行时。

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
