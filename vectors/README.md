# Noemion 规范向量

本目录保存可由 Ktisor、制品形成侧读取器、独立 Theor 和资料一致性检查共同消费的规范向量。

`semantic/` 验证 Endem 语义结构、授权边界和失败定位。每个 JSON 文件都是 `end-core.semantic-vector.v2` 测试外壳，不是 `.endem`，也不能改名后交给运行时。`context.external_preconditions` 只给检查器提供文件外的测试前置条件，不属于 Endem 规范字节；改变授权、证据或决定语境不得改变同一输入的内容身份。向量外壳使用规范 ID，不使用 Noemion 品牌前缀。

`wire/` 保存 END-FMT 0.1.0-draft 的规范十六进制字节。顶层清单属于 END-P0，只证明结构合法；`wire/p1/` 属于 END-P1，使用完整六记录载荷并实际运行字段、排序、引用和来源范围判断。两组都不是稳定 ABI。

`result-domains/`、`mene/`、`negation/`、`quantification/`、`measurement/`、`composition/`、`synem/`、`dromen/`、`iknem/`、`diagnostics/`、`adapters/`、`identity/`、`text/` 与 `authority/` 分别保存判断结果、时间连续性、否定缺席、量化成员资格、测量阈值、复合判据、Synem 闭包激活、Dromen 会话契约、Iknem 证据评估、结构化诊断、外部协议适配、精确身份、文本解释以及权威与授权决定的提案矩阵。它们用于检查设计规则之间是否一致，不是任何制品或事件的物理字节，也不证明运行组件存在。`authority/` 只描述抽象决定提案，不是身份、政策、同意或授权组件。

向量外壳由 [`vector.schema.json`](vector.schema.json) 约束。该 Schema 使用 JSON Schema 2020-12，只验证测试资料的结构；它不验证 Endem 语义，也不成为 Endem ABI。

- JSON Schema 2020-12：https://json-schema.org/draft/2020-12/json-schema-core

## 向量要求

- `id` 在仓库内唯一；
- `spec` 固定规范 ID 与精确版本；
- `context.external_preconditions` 只描述测试语境，不得被编码为 Endem 内容；
- `identity_equivalence_group` 用相同输入和不同外部语境检查内容身份不变；
- `expect.result` 只能是 `accept` 或 `reject`；
- 拒绝向量至少给出一个稳定错误类别、主条款 ID 和 JSON Pointer 位置；
- `clauses` 只能引用 `spec/registry.json` 中存在的条款；
- 任何新增向量都必须被 `tests/spec_contract_test.py` 读取。
- 线格式向量必须固定 END-FMT 与精确 Profile。END-P0 由 `tests/wire_vector_test.py` 读取；END-P1 由 `tests/p1_payload_test.py` 从语义源确定性编码、逐字段解码并比较预期。禁止只比较预生成摘要。

向量只定义列出的预期行为，不证明任何组件已经实现。当前 Python 检查器只核对字节、字段、失败分类和登记关系；未来 Ktisor、制品形成侧读取器与独立 Theor 必须各自消费全部十四个 END-P1 向量，不能复用检查脚本冒充实现。
