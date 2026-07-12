# Endem Container Format

- 规范 ID：`END-FMT`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：实验性格式草案；由 ADR-0011 采用，尚不是稳定 ABI
- 适用 Profile：`END-P0`（编号 `1`，结构实验）与 `END-P1`（编号 `2`，首个封闭语义载荷）
- 实现状态：首个本地 Rust 候选含 Poiet 生产侧检查与独立 Theor；尚未形成公开符合性声明

## 1. 范围与接受层次

本规范定义 `.endem` 第一阶段容器的固定前导、记录目录、记录范围、确定性载荷子集和结构诊断。它负责让读取器在解释自然语言语义前，安全地回答“这些字节怎样分段、是否越界、是否使用已知 Profile、是否可以继续解释”。

符合本格式只表示字节通过结构层和 Profile 层，不表示六个语义面已经满足 `END-CORE`，更不表示目标为真、可运行或已经完成。读取器 `MUST`（必须）依次区分三个结果：

1. **结构接受**：固定前导、目录、范围和载荷编码合法；
2. **Profile 接受**：对象没有超过 `END-P0` 的有限预算和允许能力；
3. **语义接受**：六个记录进一步满足 `END-CORE` 的来源、投影、事态、方向、判断和未决信息条款。

END-P0 字节只覆盖前两层。`WV-STRUCT-ACCEPT-001` 中的六个空映射会被结构层接受，但语义层必须因内容缺失而拒绝；它不是最小有效 Endem。END-P1 另有两个完整语义接受和五个语义拒绝字节向量；第二个接受向量实际保存非空 `apor`，首个 Rust 候选已同时执行这些向量。

## 2. 数据表示

所有整数使用无符号定宽整数和小端字节序。所有偏移都从文件第一个字节开始计数。格式不使用位域、指针、宿主结构体填充、宿主字节序、文件系统元数据或当前时间。

读取器对下列运算 `MUST` 使用受检算术：

- `directory_offset + record_count × directory_entry_size`；
- `record_offset + stored_length`；
- 对齐上取整；
- 所有计数到内存大小的换算；
- CBOR 长度、容器成员数和累计分配。

### END-FMT-001 — 固定格式身份

**要求：**文件前 8 字节 `MUST` 是 `45 4e 44 45 4d 00 0d 0a`，即 ASCII `ENDEM`、NUL、CR、LF。`format_major` 与 `format_minor` `MUST` 精确匹配读取器声明支持的 `END-FMT` 版本；当前值分别是 `0` 与 `1`。

**失败：**前导截断、魔数不同或版本不受支持时，读取器必须在读取目录前原子失败。

**验证：**`WV-STRUCT-ACCEPT-001`、`WV-REJECT-MAGIC-001`。

### END-FMT-002 — 固定宽度与字节序

**要求：**`byte_order` `MUST` 是 `1`，表示小端；`header_size` `MUST` 是 `64`；`directory_entry_size` `MUST` 是 `48`。读取器 `MUST NOT` 把磁盘字节直接强制转换为宿主结构体。

**失败：**宽度、字节序或结构大小不同必须报告格式不受支持，而不是猜测宿主布局。

**验证：**格式表复核；未来跨大小端变异测试。

### END-FMT-003 — 文件大小与保留位精确

**要求：**`file_size` `MUST` 等于实际输入字节数；头部 `flags` 和 24 个保留字节 `MUST` 全部为零。尾随字节、隐式截断和非零保留位 `MUST` 被拒绝。

**失败：**声明大小与实际大小不同或保留区非零时，读取器必须停止，且不得返回部分可信视图。

**验证：**未来 `peira:wire-size-and-reserved` 向量。

## 3. 64 字节固定前导

| 偏移 | 大小 | 字段 | `END-P0` 值或含义 |
| ---: | ---: | --- | --- |
| 0 | 8 | `magic` | `45 4e 44 45 4d 00 0d 0a` |
| 8 | 2 | `format_major` | `0` |
| 10 | 2 | `format_minor` | `1` |
| 12 | 2 | `header_size` | `64` |
| 14 | 2 | `directory_entry_size` | `48` |
| 16 | 1 | `byte_order` | `1`，小端 |
| 17 | 1 | `profile_id` | `1` 为 `END-P0`；`2` 为 `END-P1` |
| 18 | 1 | `state` | `0`，即 `nascent`；其他值在本 Profile 中拒绝 |
| 19 | 1 | `flags` | `0` |
| 20 | 4 | `record_count` | 记录目录项数量 |
| 24 | 8 | `directory_offset` | 当前固定为 `64` |
| 32 | 8 | `file_size` | 完整输入字节数 |
| 40 | 24 | `reserved` | 全零 |

头部故意不保存时间戳、构建路径、用户、组、文件模式、模型名称或随机标识。这些环境信息不能改变规范字节；需要审计时由外部 Tekmor 绑定。

## 4. 记录目录

目录从 `directory_offset` 开始，包含 `record_count` 个 48 字节条目。目录结束后的第一个记录按自身 `alignment` 对齐；记录之间允许全零填充，填充字节不得参与记录载荷。

| 条目偏移 | 大小 | 字段 | 含义 |
| ---: | ---: | --- | --- |
| 0 | 2 | `kind` | 记录种类 |
| 2 | 2 | `flags` | 当前必须为 `1`，表示关键记录 |
| 4 | 4 | `record_id` | 文件内唯一、非零编号 |
| 8 | 8 | `offset` | 记录载荷文件偏移 |
| 16 | 8 | `stored_length` | 当前存储字节数 |
| 24 | 8 | `logical_length` | 解码前逻辑字节数；P0 必须等于存储长度 |
| 32 | 4 | `alignment` | 当前必须为 `8` |
| 36 | 4 | `link` | 当前必须为 `0` |
| 40 | 4 | `info` | 当前必须为 `0` |
| 44 | 4 | `reserved` | 必须为 `0` |

### END-FMT-004 — 目录范围先于分配

**要求：**读取器 `MUST` 在分配目录数组或读取任一条目前，验证目录乘法、端点、文件范围和 Profile 记录数上限。目录 `MUST` 从偏移 `64` 开始并完整位于文件内。

**失败：**乘法溢出、目录越界、目录覆盖固定头部或记录数超限必须返回单一稳定错误。

**验证：**`WV-REJECT-DIRECTORY-BOUNDS-001`。

### END-FMT-005 — 目录顺序与编号唯一

**要求：**目录项 `MUST` 按 `(kind, record_id)` 升序排列；`record_id` `MUST` 非零且文件内唯一。Poiet `MUST NOT` 使用输入顺序、哈希表遍历顺序或并发完成顺序决定目录。

**失败：**乱序、重复编号或编号为零必须拒绝，不得在读取时重新排序后假装对象规范。

**验证：**未来 `peira:wire-directory-order` 向量。

### END-FMT-006 — 记录范围不重叠

**要求：**每个 `offset` `MUST` 满足声明对齐；`offset + stored_length` `MUST` 受检并位于文件内；非空记录的范围 `MUST NOT` 与头部、目录或另一记录重叠。记录间填充 `MUST` 为零，最后一个记录的端点 `MUST` 等于 `file_size`，不得保留尾随填充。

**失败：**越界、回绕、未对齐、重叠或非零填充必须原子拒绝。

**验证：**`WV-REJECT-OVERLAP-001`。

### END-FMT-007 — P0 不开放未知记录

**要求：**`END-P0` 中每个目录项 `flags` `MUST` 等于 `1`，每个 `kind` `MUST` 是本规范登记的六种之一。当前 Profile `MUST NOT` 跳过未知种类，也没有供应商私有范围。

**失败：**未知种类、未知标志位或把关键记录改成可选必须关闭失败。

**验证：**`WV-REJECT-UNKNOWN-KIND-001`。

## 5. P0 记录种类

| `kind` | 记录 | 数量 | 语义职责 |
| ---: | --- | ---: | --- |
| `1` | `rhem` | 恰好 1 | 来源与可重定位范围 |
| `2` | `semion` | 恰好 1 | 已授权投影 |
| `3` | `skena` | 恰好 1 | 一个根的中性事态 |
| `4` | `telis` | 恰好 1 | `kine` 或 `mene` 方向 |
| `5` | `krin` | 恰好 1 | 观察、比较、证据与权威契约 |
| `6` | `apor` | 恰好 1 | 显式未决投影集合，可为空 |

### END-FMT-008 — 六个语义记录完整且单一

**要求：**`END-P0` 文件 `MUST` 恰好包含上述六个记录，每种一次；目录顺序因此固定为 `rhem`、`semion`、`skena`、`telis`、`krin`、`apor`。结构层只验证记录存在和载荷根类型；语义层仍必须验证每个映射的必需字段和关系。

**失败：**缺失、重复或额外记录必须拒绝。

**验证：**`WV-STRUCT-ACCEPT-001`；未来缺失与重复向量。

## 6. 确定性载荷子集

每个记录载荷使用 RFC 8949 的 CBOR 数据项，但 `END-P0` 只允许以下严格子集：

- 根数据项 `MUST` 是一个确定长度映射；
- 只允许无符号整数、负整数、字节串、UTF-8 文本串、确定长度数组、确定长度映射、`false`、`true` 与 `null`；
- 整数、长度和简单值 `MUST` 使用最短编码；
- 映射键 `MUST` 是无符号整数，按其编码字节升序排列且不得重复；
- `MUST NOT` 使用浮点数、标签、未定义值、break、非确定长度项或无效 UTF-8；
- 容器深度、字符串、成员数和累计分配受 `END-P0` 限制。

读取器在结构层保守地把每个 CBOR 数据项计入 `max_graph_nodes`，把每个数组元素数或映射 pair 数计入 `max_graph_edges`。节点计数、累计分配和其他累计预算作用于整份制品，不能在进入下一记录时清零；读取器必须在按声明数量循环或分配前检查上限。

CBOR 只承担记录内部的无歧义类型编码。记录编号、六个语义面、状态、身份、授权和验收仍由 Endem 规范定义；任何通用 CBOR 文档都不是 Endem。

### END-FMT-009 — 载荷编码唯一

**要求：**Poiet `MUST` 只写上述确定性子集；读取器 `MUST` 拒绝同一值的非最短表示、重复或乱序映射键、非确定长度项及禁用类型。读取器不得“规范化后接受”非规范字节。

**失败：**载荷不是允许的 CBOR、根不是映射或编码不唯一时，必须定位记录 ID 与字节范围。

**验证：**`WV-REJECT-PAYLOAD-ROOT-001`；未来非最短与键顺序向量。

## 7. END-P1 封闭语义载荷

END-P1 使用与 END-P0 相同的头部、目录、六个记录 kind 和确定性 CBOR 子集，但不接受空语义映射。机器可读字段登记维护在 `spec/profiles/end-p1.json`；该文件与本节共同构成 Profile 2 的权威字段源。

每个 map 只允许登记键且必须包含全部 required key。标识符是 1–255 字节 ASCII 文本，匹配 `^[A-Za-z][A-Za-z0-9._:/#-]{0,254}$`。普通来源内容和冲突说明可以使用 UTF-8；语言标签与媒体类型必须是 ASCII 文本，并分别遵守 BCP 47 与媒体类型基本语法。

| 记录 | 根映射键 | 主要嵌套结构 |
| --- | --- | --- |
| rhem | 1 source_id；2 subject；3 media_type；4 language；5 version；6 content；7 range | range：1 unit=0（Unicode scalar）；2 start；3 length |
| semion | 1 symbols；2 relations | symbol：id/kind/source_ref；relation：id/predicate/roles/projection；role：name/symbol；projection：kind/id |
| skena | 1 root；2 situations | situation：id/relation/polarity；polarity 0 positive、1 negative |
| telis | 1 mode | END-P1 只允许 0 kine；mene 等待区间模型 |
| krin | 1 required_phain；2 required_tekmor；3 on_missing_observation；4 on_evaluation_error；5 decision_authority | relation match 只允许 same-roles；缺观察为 agno；求值失败为 fault |
| apor | 1 items | item：id/source_ref/candidates/conflict/impact_scope/allowed_resolutions/decision_authority |

### END-FMT-013 — P1 字段闭包与规范排序

**要求：**`profile_id=2` `MUST` 精确绑定 END-P1 0.1.0-draft。每个 map `MUST` 拒绝未知、缺失、重复或错误类型的键。symbols、relations、roles、situations、required_phain 与 apor items `MUST` 按各自 ASCII 稳定 ID 的原始字节升序排列；其余集合按确定性 CBOR 编码字节排序。身份相同的重复项 `MUST` 拒绝，不能靠后项覆盖。

**失败：**字段集合、类型、枚举、顺序或重复不符合登记时，读取器必须在语义层原子失败并定位记录和路径。

**验证：**END-P1 完整接受与未知字段拒绝字节向量；`tests/p1_payload_test.py`。

### END-FMT-014 — P1 引用闭包与来源范围

**要求：**rhem 范围端点 `MUST` 以受检算术落在 content 的 Unicode 标量数量内。semion 角色 `MUST` 引用已登记 symbol；skena root `MUST` 引用唯一 situation，situation 与 krin `MUST` 引用已登记 relation。每个 source_ref `MUST` 等于当前 rhem source_id，或以该完整 ID 后紧接 `#/` 的片段开头；仅有相同字符串前缀不算锚定。P1 只允许受信规则或具名授权投影、kine 方向和显式 apor items。

**失败：**任何范围越界、悬空引用、不可信投影、未登记方向或未记录歧义都必须语义拒绝，不能返回部分可信 Endem。

**验证：**END-P1 完整接受、悬空引用与来源范围拒绝字节向量；`tests/p1_payload_test.py`。

## 8. Profile 与状态

### END-FMT-010 — Profile 固定且有限

**要求：**`profile_id=1` `MUST` 精确绑定 `spec/profiles/end-p0.json`，`profile_id=2` `MUST` 精确绑定 `spec/profiles/end-p1.json`。调用者可以设置更低的本地预算，但 `MUST NOT` 在不改变 Profile 身份的情况下提高规范上限。所有限制必须在相应循环、分配、递归或输出前检查；节点、边和累计分配预算覆盖整份制品，不得按记录重置。

**失败：**Profile 未知、限制缺失、值为零或无限、或对象超过任一限制时必须拒绝。

**验证：**Profile 登记检查；未来边界值和超限值向量。

### END-FMT-011 — P0/P1 禁止压缩、加密与 attested 状态

**要求：**`END-P0` 与 `END-P1` 中 `stored_length` `MUST` 等于 `logical_length`，记录标志只能为关键位 `1`，`state` 只能为 `0`（`nascent`）。压缩、加密、签名包络、外部记录、`coherent` 与 `attested` `MUST NOT` 出现在这两个 Profile。

**失败：**发现未登记变换或更高状态必须报告不受支持的必需能力，不能降级读取后提升信任。

**验证：**未来 `peira:p0-feature-closure` 向量。

### END-FMT-012 — 结构接受不提升语义或信任

**要求：**结构检查器、Theor 或通用 CBOR 解码器 `MUST NOT` 把结构接受解释为 `END-CORE` 语义接受、`coherent`、`attested`、可执行或目标已满足。诊断 `MUST` 标明停止于结构、Profile 还是语义层。

**失败：**任一工具用单一 `valid=true` 合并不同层次，或让未运行的层次隐式通过时，不符合本规范。

**验证：**`WV-STRUCT-ACCEPT-001` 的预期结果明确为 `structural-accept/semantic-not-evaluated`；发布复核。

## 9. 当前未决接口

以下内容没有被 `END-FMT 0.1.0-draft` 冻结：

- END-P1 之外的量化、时间、单位、求值和扩展字段；
- 内容摘要、签名包络、Semantic Key 与 Tekmor 绑定；
- `coherent`、`attested`、Synem 和调试伴随记录；
- 压缩、加密、流式传输、随机访问索引和远程披露；
- 稳定 ABI、MIME 类型和跨版本升级规则。

任何新增记录种类、字段编号、变换或状态都必须先有 ADR、登记、正反字节向量和独立读取实验。当前项目不承诺兼容本草案产生的字节。

## 10. 机制来源与采用边界

- ELF 以固定头部提供文件路线图，并用节表与程序头提供不同消费者视图；Endem 只采用“固定前导 + 显式目录 + 消费者边界”，不采用地址、指令、装载段或处理器 ABI：https://gabi.xinuos.com/elf/01-intro.html
- ELF 明确记录偏移、条目大小和数量；Endem 进一步要求所有乘加、端点与对齐使用受检算术：https://gabi.xinuos.com/elf/02-eheader.html
- GNU `readelf` 不依赖 BFD；这支持 Poiet 与 Theor 采用独立代码路径，而不是共享通用内部表示：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- GNU `ar -D` 会清除所有者、组、时间戳等变化来源；Endem 直接不把这些环境元数据写入规范头部：https://sourceware.org/binutils/docs/binutils/ar-cmdline.html
- RFC 8949 定义确定性 CBOR 的最短编码、确定长度与键排序要求；Endem 采用更小的子集，并保留自己的应用层有效性：https://www.rfc-editor.org/rfc/rfc8949.html
