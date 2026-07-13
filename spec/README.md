# Noemion 规范源

本目录保存实现可以逐条引用的规范源。公开 HTML 负责直白解释和阅读入口；本目录负责版本、条款 ID、规范强度与验证映射。二者冲突时，先停止实现并通过 ADR 修正文档，不能由当前代码行为反向改写规范。

## 当前规范

| 规范 | 版本 | 状态 | 已覆盖 | 明确未覆盖 |
| --- | --- | --- | --- | --- |
| [`endem-core.md`](endem-core.md) | `0.1.0-draft` | 草案；已接受语义边界的第一份条款化表达 | Endem 最小性、六个语义面、事态与方向分离、单变量量化、测量阈值、复合判据、未知状态、确定性、安全读取、身份分层与验证责任 | 量化、测量与组合物理字段、嵌套或多变量量化、条件适用性、时间、求值、摘要与签名 |
| [`endem-format.md`](endem-format.md) | `0.1.0-draft` | 已采用的实验性草案；尚非稳定 ABI | 固定前导、定宽目录、确定性 CBOR、END-P0 结构实验与 END-P1 封闭语义载荷 | coherent/attested、签名、压缩、Synem 和跨版本承诺 |
| [`endem-source-manifest.md`](endem-source-manifest.md) | `0.1.0-draft` | 实验性 Poiet 输入；正式来源语言出现后删除 | UTF-8 逐行指令、转义、基数、授权边界和 END-P1 映射 | 注释元数据、包含、模块、量化、时间、求值语言和兼容承诺 |
| [`synem-core.md`](synem-core.md) | `0.1.0-draft` | 草案；已接受组合闭包边界的第一份条款化表达 | 完整闭包、精确绑定、有限无环、权限交集、成员结果分离与会话激活 | 物理容器、版本范围语法、符号、调度、远程仓库和稳定 ABI |

[`endem-threat-model.md`](endem-threat-model.md) 把单个 Endem 的不可信输入与失败责任映射到规范条款；[`synem-threat-model.md`](synem-threat-model.md) 单独处理依赖替换、闭包截断、循环、权限放大、结果洗白与激活竞态。[`profiles/end-p0.json`](profiles/end-p0.json) 给出第一组跨实现实验的有限上限；这些数值不是生产规模证明，提高时必须采用新的 Profile 身份。

[`endem-errors.md`](endem-errors.md) 登记结构与 Profile 错误码。[`registry.json`](registry.json) 是机器可读的规范、术语、条款、威胁、成熟度与验证登记。`../vectors/semantic/` 保存 JSON 语义外壳；`../vectors/wire/` 保存真实字节的十六进制表达。结构接受向量不等于语义有效 Endem。

[`endem-scenarios.md`](endem-scenarios.md) 是非规范性的自然语言设计审查语料。它用二十七个场景检查达到成立、持续保持、否定事态、指称歧义、观察不足、求值故障、授权不足、多根拆分、结果域、时间范围、缺席推断、量化范围、测量阈值与复合判断是否能被现行体系解释。它不规定语法或字节，也不是可执行测试；案例暴露的缺口必须回到 ADR、规范条款或开放问题。

[`synem-scenarios.md`](synem-scenarios.md) 用十个非规范场景检查闭包、绑定、可选依赖、权限、成员结果和激活边界。它同样不是语法、解析器或组件证据。

`../vectors/result-domains/cases.json` 保存 ADR-0015 的十二个正反提案向量；`../tests/result_domain_vector_test.py` 只执行结果域约束，不实现 Praxor、求值器或决定引擎。向量通过只能证明当前矩阵和条款一致，不能证明运行组件存在。

`../vectors/mene/cases.json` 保存 ADR-0016 的十二个时间与连续性提案向量；`../tests/mene_vector_test.py` 只执行 fixed/elapsed 范围、strict/budgeted 政策和覆盖分类，不实现时钟、监控器、Praxor 或求值器。

`../vectors/negation/cases.json` 保存 ADR-0017 的十二个否定与缺席提案向量；`../tests/negation_vector_test.py` 只执行显式负观察、空结果、封闭范围、正反例和观察故障分类，不实现日志收集器、Praxor 或求值器。

`../vectors/quantification/cases.json` 保存 ADR-0018 的十二个量化与成员资格提案向量；`../tests/quantification_vector_test.py` 只检查成员范围、空集合、不同成员计数和决定性聚合，不实现 Poiet、Praxor、成员目录或求值器。

`../vectors/measurement/cases.json` 保存 ADR-0019 的十二个测量与阈值提案向量；`../tests/measurement_vector_test.py` 只检查构念、总体、单位、程序、聚合器、不确定区间与阈值分类，不实现采集器、统计引擎、Praxor 或求值器。

`../vectors/composition/cases.json` 保存 ADR-0020 的十二个复合事态与判据提案向量；`../tests/composition_vector_test.py` 只检查单根边界、有限无环拓扑、叶对齐、四结果传播和决定性短路，不实现解析器、Praxor、运行时或求值器。

`../vectors/synem/cases.json` 保存 ADR-0021 的十二个闭包与条件激活提案向量；`../tests/synem_vector_test.py` 只检查六条 SYN-CORE 规则，不实现解析器、Pleko、Praxor、运行时或求值器。

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
