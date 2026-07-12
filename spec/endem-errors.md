# Endem Diagnostic Catalog

- 登记 ID：`END-ERRCAT`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：与 `END-FMT 0.1.0-draft` 配套的结构诊断草案

## 1. 诊断结构

每个拒绝结果至少包含：稳定 `code`、主 `clause`、验证 `layer`，以及可用时的 `byte_range`、`record_id`、`semantic_path`、`limit` 与 `actual`。人类可读消息可以改进措辞，但程序不得依赖消息文本。

第一阶段 `layer` 只有 `structure`、`profile` 与 `semantic`。一个操作可以在安全范围内附加后续诊断，但第一个阻断错误必须稳定；任何诊断集合都不能携带部分可信 Endem。

## 2. 结构与 Profile 错误码

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
| `endem.wire.record.unknown_kind` | `END-FMT-007` | profile | P0 出现未登记记录种类 |
| `endem.wire.record.flags` | `END-FMT-007` | profile | P0 记录没有精确关键标志 `1` |
| `endem.wire.facet.cardinality` | `END-FMT-008` | profile | 六种记录缺失、重复或出现额外记录 |
| `endem.wire.payload.cbor` | `END-FMT-009` | structure | CBOR 不良构、非确定或使用禁用类型 |
| `endem.wire.payload.not_map` | `END-FMT-009` | structure | 记录载荷根不是确定长度映射 |
| `endem.wire.profile.unknown` | `END-FMT-010` | profile | Profile 编号未知或没有精确登记 |
| `endem.wire.profile.limit` | `END-FMT-010` | profile | 任一资源超过当前有效上限 |
| `endem.wire.profile.feature` | `END-FMT-011` | profile | P0 出现压缩、加密、更高状态或其他未登记能力 |

## 3. 稳定性边界

上述错误码只在 `END-FMT 0.1.0-draft` 的向量与实验中稳定，尚不构成发行 ABI。提升为稳定接口前必须完成：

1. Poiet 与独立 Theor 对同一畸形语料给出相同主错误类别；
2. 边界值、截断、乱序、重复、非最短 CBOR 和资源耗尽向量齐全；
3. 模糊测试证明所有拒绝路径原子失败；
4. CLI 退出状态与结构化诊断格式另行冻结。
