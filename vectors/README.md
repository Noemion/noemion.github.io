# Noemion 规范向量

本目录保存可由 Poiet、生产读取器、独立 Theor 和 `peira` 共同消费的规范向量。

`semantic/` 验证 Endem 语义结构、授权边界和失败定位。每个 JSON 文件都是 `noemion.semantic-vector.v1` 测试外壳，不是 `.endem`，也不能改名后交给运行时。

`wire/` 保存 END-FMT 0.1.0-draft 的规范十六进制字节。顶层清单属于 END-P0，只证明结构合法；`wire/p1/` 属于 END-P1，使用完整六记录载荷并实际运行字段、排序、引用和来源范围判断。两组都不是稳定 ABI。

向量外壳由 [`vector.schema.json`](vector.schema.json) 约束。该 Schema 使用 JSON Schema 2020-12，只验证测试资料的结构；它不验证 Endem 语义，也不成为 Endem ABI。

- JSON Schema 2020-12：https://json-schema.org/draft/2020-12/json-schema-core

## 向量要求

- `id` 在仓库内唯一；
- `spec` 固定规范 ID 与精确版本；
- `expect.result` 只能是 `accept` 或 `reject`；
- 拒绝向量至少给出一个稳定错误类别、主条款 ID 和 JSON Pointer 位置；
- `clauses` 只能引用 `spec/registry.json` 中存在的条款；
- 任何新增向量都必须被 `tests/spec_contract_test.py` 读取。
- 线格式向量必须固定 END-FMT 与精确 Profile。END-P0 由 `tests/wire_vector_test.py` 读取；END-P1 由 `tests/p1_payload_test.py` 从语义源确定性编码、逐字段解码并比较预期。禁止只比较预生成摘要。

向量只证明列出的行为，不证明实现没有其他缺陷。首个 Rust 候选已由 Poiet 生成两个接受对象，并由生产侧结构路径和独立 Theor 消费全部九个 END-P1 向量；后续实现仍必须重复逐字段解释、失败分类和资源边界比较。
