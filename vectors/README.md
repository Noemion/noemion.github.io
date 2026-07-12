# Noemion 规范向量

本目录保存可由 Poiet、生产读取器、独立 Theor 和 `peira` 共同消费的规范向量。

当前只有 `semantic/`：它验证 Endem 语义结构、授权边界和失败定位。每个文件都是 `noemion.semantic-vector.v1` 测试外壳，不是 `.endem`，不定义线格式，也不能改名后交给运行时。

向量外壳由 [`vector.schema.json`](vector.schema.json) 约束。该 Schema 使用 JSON Schema 2020-12，只验证测试资料的结构；它不验证 Endem 语义，也不成为 Endem ABI。

- JSON Schema 2020-12：https://json-schema.org/draft/2020-12/json-schema-core

## 向量要求

- `id` 在仓库内唯一；
- `spec` 固定规范 ID 与精确版本；
- `expect.result` 只能是 `accept` 或 `reject`；
- 拒绝向量至少给出一个稳定错误类别、主条款 ID 和 JSON Pointer 位置；
- `clauses` 只能引用 `spec/registry.json` 中存在的条款；
- 任何新增向量都必须被 `tests/spec_contract_test.py` 读取。

向量只证明当前外壳与预期一致，不能证明未来实现已经正确。实现出现后，同一向量必须分别由 Poiet/生产路径和独立 Theor 消费，并比较逐字段解释与失败分类。

