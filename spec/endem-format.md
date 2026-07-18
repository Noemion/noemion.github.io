---
layout: spec
title: "Endem Container Format · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/endem-format.html"
summary: "规定 .endem 字节怎样安全分段和有界读取；格式通过只说明结构可解释，不代表目标有效或可运行。"
document_status: "实验性格式草案"
---
# Endem Container Format

- 规范 ID：`END-FMT`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：实验性格式草案；由 ADR-0011 采用，尚不是稳定 ABI
- 适用 Profile：`END-P0`（编号 `1`，结构实验）与 `END-P2`（编号 `2`，首个封闭内容 Profile）
- 实现状态：仅有实验字节与一致性检查工具；没有生产写入器或independent inspector

## 1. 范围与接受层次

本规范定义 `.endem` 第一阶段容器的固定前导、记录目录、记录范围、确定性载荷子集和结构诊断。它负责让读取器在解释自然语言语义前，安全地回答“这些字节怎样分段、是否越界、是否使用已知 Profile、是否可以继续解释”。

符合本格式只表示字节通过结构层和 Profile 层，不表示六个语义面已经满足 `END-CORE`，更不表示目标为真、可运行或已经完成。读取器 `MUST`（必须）依次区分三个结果：

1. **结构接受**：固定前导、目录、范围和载荷编码合法；
2. **Profile 接受**：对象满足头部声明 Profile 的字段、枚举、排序、引用和有限预算；
3. **内容接受**：六个记录满足 `END-CORE` 的来源、投影、事态、方向、判断和未决信息条款，并且全部外部前置条件已经按精确版本核对。

END-P0 字节只覆盖结构实验。`WV-STRUCT-ACCEPT-001` 中的六个空映射会被结构层接受，但 Profile 层必须因内容缺失而拒绝；它不是最小有效 Endem。END-P2 有三个 Profile 接受和十一项确定拒绝；接受结果统一报告为 `profile-accept / external-prerequisites-not-evaluated`，因为当前检查器只验证封闭字段、引用、来源范围和资源边界，没有核对 AUT-CORE 授权决定。当前一致性检查工具会读取这些向量，没有 Rust 组件执行它们。

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

**验证：**未来 `conformance:wire-size-and-reserved` 向量。

## 3. 64 字节固定前导

| 偏移 | 大小 | 字段 | `END-P0` 值或含义 |
| ---: | ---: | --- | --- |
| 0 | 8 | `magic` | `45 4e 44 45 4d 00 0d 0a` |
| 8 | 2 | `format_major` | `0` |
| 10 | 2 | `format_minor` | `1` |
| 12 | 2 | `header_size` | `64` |
| 14 | 2 | `directory_entry_size` | `48` |
| 16 | 1 | `byte_order` | `1`，小端 |
| 17 | 1 | `profile_id` | `1` 为 `END-P0`；`3` 为 `END-P2`；`2` 已随旧术语 Profile 退出当前规范 |
| 18 | 1 | `state` | `0`，即 `formed`；其他值在本 Profile 中拒绝 |
| 19 | 1 | `flags` | `0` |
| 20 | 4 | `record_count` | 记录目录项数量 |
| 24 | 8 | `directory_offset` | 当前固定为 `64` |
| 32 | 8 | `file_size` | 完整输入字节数 |
| 40 | 24 | `reserved` | 全零 |

头部故意不保存时间戳、构建路径、用户、组、文件模式、模型名称或随机标识。这些环境信息不能改变规范字节；需要审计时由外部 evidence entry 绑定。

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

**要求：**目录项 `MUST` 按 `(kind, record_id)` 升序排列；`record_id` `MUST` 非零且文件内唯一。deterministic producer `MUST NOT` 使用输入顺序、哈希表遍历顺序或并发完成顺序决定目录。

**失败：**乱序、重复编号或编号为零必须拒绝，不得在读取时重新排序后假装对象规范。

**验证：**未来 `conformance:wire-directory-order` 向量。

### END-FMT-006 — 记录范围不重叠

**要求：**每个 `offset` `MUST` 满足声明对齐；`offset + stored_length` `MUST` 受检并位于文件内；非空记录的范围 `MUST NOT` 与头部、目录或另一记录重叠。记录间填充 `MUST` 为零，最后一个记录的端点 `MUST` 等于 `file_size`，不得保留尾随填充。

**失败：**越界、回绕、未对齐、重叠或非零填充必须原子拒绝。

**验证：**`WV-REJECT-OVERLAP-001`。

### END-FMT-007 — P0 不开放未知记录

**要求：**`END-P0` 中每个目录项 `flags` `MUST` 等于 `1`，每个 `kind` `MUST` 是本规范列出的六种之一。当前 Profile `MUST NOT` 跳过未知种类，也没有供应商私有范围。

**失败：**未知种类、未知标志位或把关键记录改成可选必须关闭失败。

**验证：**`WV-REJECT-UNKNOWN-KIND-001`。

## 5. P0 记录种类

| `kind` | 记录 | 数量 | 语义职责 |
| ---: | --- | ---: | --- |
| `1` | `source_expression` | 恰好 1 | 来源与可重定位范围 |
| `2` | `meaning_projection` | 恰好 1 | 已授权投影 |
| `3` | `situation` | 恰好 1 | 一个根的中性事态 |
| `4` | `goal_direction` | 恰好 1 | `reach` 或 `maintain` 方向 |
| `5` | `satisfaction_criteria` | 恰好 1 | 观察、比较、证据与权威契约 |
| `6` | `unresolved_meaning` | 恰好 1 | 显式未决投影集合，可为空 |

### END-FMT-008 — 六个语义记录完整且单一

**要求：**`END-P0` 文件 `MUST` 恰好包含上述六个记录，每种一次；目录顺序因此固定为 `source_expression`、`meaning_projection`、`situation`、`goal_direction`、`satisfaction_criteria`、`unresolved_meaning`。结构层只验证记录存在和载荷根类型；语义层仍必须验证每个映射的必需字段和关系。

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

**要求：**deterministic producer `MUST` 只写上述确定性子集；读取器 `MUST` 拒绝同一值的非最短表示、重复或乱序映射键、非确定长度项及禁用类型。读取器不得“规范化后接受”非规范字节。

**失败：**载荷不是允许的 CBOR、根不是映射或编码不唯一时，必须定位记录 ID 与字节范围。

**验证：**`WV-REJECT-PAYLOAD-ROOT-001`；未来非最短与键顺序向量。

## 7. END-P2 封闭内容 Profile

END-P2 使用与 END-P0 相同的头部、目录、六个记录 kind 和确定性 CBOR 子集，但不接受空语义映射。机器可读字段登记维护在 `spec/profiles/end-p2.json`；该文件与本节共同构成 Profile 2 的权威字段源。END-P2 包含原始自然语言，只承担形成与审查，不是最终发布 Profile；发布裁剪不能直接删除记录后继续声称符合 END-P2。

每个 map 只允许登记键且必须包含全部 required key。标识符是 1–255 字节 ASCII 文本，匹配 `^[A-Za-z][A-Za-z0-9._:/#-]{0,254}$`。普通来源内容和冲突说明可以使用 UTF-8；语言标签与媒体类型必须是 ASCII 文本，并分别遵守 BCP 47 与媒体类型基本语法。

| 记录 | 根映射键 | 主要嵌套结构 |
| --- | --- | --- |
| source_expression | 1 source_id；2 subject；3 media_type；4 language；5 version；6 content；7 range | range：1 unit=0（Unicode scalar）；2 start；3 length |
| meaning_projection | 1 symbols；2 relations | symbol：id/kind/source_ref；relation：id/predicate/roles/projection；role：name/symbol；projection：kind/id |
| situation | 1 root；2 situations | situation：id/relation/polarity；polarity 0 positive、1 negative |
| goal_direction | 1 mode | END-P2 只允许 0 reach；maintain 等待含时间字段的新 Profile |
| satisfaction_criteria | 1 required_observations；2 required_evidence；3 on_missing_observation；4 on_evaluation_error；5 decision_authority | relation match 只允许 same-roles；缺观察为 undetermined；求值失败为 fault |
| unresolved_meaning | 1 items | item：id/source_ref/candidates/conflict/impact_scope/allowed_resolutions/decision_authority |

### END-FMT-013 — P2 字段闭包与规范排序

**要求：**`profile_id=3` `MUST` 精确绑定 END-P2 0.1.0-draft。每个 map `MUST` 拒绝未知、缺失、重复或错误类型的键。symbols、relations、roles、situations、required_observations 与 unresolved_meaning items `MUST` 按各自 ASCII 稳定 ID 的原始字节升序排列；其余集合按确定性 CBOR 编码字节排序。身份相同的重复项 `MUST` 拒绝，不能靠后项覆盖。

**失败：**字段集合、类型、枚举、顺序或重复不符合登记时，读取器必须在语义层原子失败并定位记录和路径。

**验证：**END-P2 完整接受与未知字段拒绝字节向量；`tests/p2_payload_test.py`。

### END-FMT-014 — P2 引用闭包与来源范围

**要求：**source_expression 范围端点 `MUST` 以受检算术落在 content 的 Unicode 标量数量内。meaning_projection 角色 `MUST` 引用已登记 symbol；situation root `MUST` 引用唯一 situation，situation 与 satisfaction_criteria `MUST` 引用已登记 relation。每个 source_ref `MUST` 等于当前 source_expression source_id，或以该完整 ID 后紧接 `#/` 的片段开头；仅有相同字符串前缀不算锚定。P2 只允许受信规则或具名授权投影、reach 方向和显式 unresolved_meaning items。

**失败：**任何范围越界、悬空引用、不可信投影、未登记方向或未记录歧义都必须语义拒绝，不能返回部分可信 Endem。

**验证：**END-P2 完整接受、悬空引用与来源范围拒绝字节向量；`tests/p2_payload_test.py`。

### END-FMT-015 — P2 权威字段只是待解析选择器

**要求：**END-P2 中的 `projection.kind`、`projection.id`、`decision_authority` 与 `required_evidence` `MUST` 只解释为内容要求中的有限选择器；它们不内联授权决定、政策、权威目录、签名、evidence entry 实例或验证材料。读取器 `MUST NOT` 通过名称、当前环境、网络查询或默认目录把这些选择器提升为授权或证据已经存在。END-P2 单文件最多支持容器接受与 Profile 接受；完整 `END-CORE` 内容接受还 `MUST` 显式核对外部前置条件。

**失败：**工具仅凭可信外观字符串宣称投影已获授权、证据已取得、最终决定主体有权，或把本地解析结果写回为同一 Profile 的隐式含义时，内容声明必须拒绝，原始字节不得被修改。

**验证：**`spec/profiles/end-p2.json` 的符合性声明上限；语义向量的缺失与错绑前置条件；未来 `conformance:p1-selector-non-self-authentication` 测试。

## 8. Profile 与状态

### END-FMT-010 — Profile 固定且有限

**要求：**`profile_id=1` `MUST` 精确绑定 `spec/profiles/end-p0.json`，`profile_id=3` `MUST` 精确绑定 `spec/profiles/end-p2.json`。调用者可以设置更低的本地预算，但 `MUST NOT` 在不改变 Profile 身份的情况下提高规范上限。所有限制必须在相应循环、分配、递归或输出前检查；节点、边和累计分配预算覆盖整份制品，不得按记录重置。

**失败：**Profile 未知、限制缺失、值为零或无限、或对象超过任一限制时必须拒绝。

**验证：**Profile 登记检查；未来边界值和超限值向量。

### END-FMT-011 — P0/P2 禁止压缩、加密与外部陈述内嵌

**要求：**`END-P0` 与 `END-P2` 中 `stored_length` `MUST` 等于 `logical_length`，记录标志只能为关键位 `1`，`state` 只能为 `0`（`formed`）。压缩、加密、签名包络、外部陈述记录与 `resolved` 内容状态 `MUST NOT` 出现在这两个 Profile。外部陈述、验证政策、截止点、撤销状态和依赖方判断保持为内容之外的多值关系。

**失败：**发现未登记变换或更高状态必须报告不受支持的必需能力，不能降级读取后提升信任。

**验证：**未来 `conformance:p0-feature-closure` 向量。

### END-FMT-012 — 结构接受不提升语义或信任

**要求：**结构检查器、independent inspector 或通用 CBOR 解码器 `MUST NOT` 把结构接受解释为 `END-CORE` 内容接受、`resolved`、外部陈述有效、可执行或目标已满足。诊断 `MUST` 标明停止于结构、Profile 还是内容层，并明确外部前置条件是否执行。

**失败：**任一工具用单一 `valid=true` 合并不同层次，或让未运行的层次隐式通过时，不符合本规范。

**验证：**`WV-STRUCT-ACCEPT-001` 的预期结果明确为 `structural-accept/semantic-not-evaluated`；发布复核。

## 9. 当前未决接口

以下内容没有被 `END-FMT 0.1.0-draft` 冻结：

- END-P2 之外的量化、时间、单位、求值和扩展字段；
- 内容摘要、签名包络、Semantic Key 与 evidence entry 绑定；
- 授权决定、规则登记、权威目录与符合性报告的伴随绑定；
- `resolved`、外部陈述关系、Endem closure 和调试伴随记录；
- 压缩、加密、流式传输、随机访问索引和远程披露；
- 稳定 ABI、MIME 类型和跨版本升级规则。

任何新增记录种类、字段编号、变换或状态都必须先有 ADR、登记、正反字节向量和独立读取实验。当前项目不承诺兼容本草案产生的字节。

## 10. 机制来源与采用边界

- ELF 使用固定头部描述文件路线图，并用节表与程序头形成不同的使用方视图；Endem 只采用“固定前导 + 显式目录 + 使用方边界”，不采用地址、指令、装载段或处理器 ABI：https://gabi.xinuos.com/elf/01-intro.html
- ELF 明确记录偏移、条目大小和数量；Endem 进一步要求所有乘加、端点与对齐使用受检算术：https://gabi.xinuos.com/elf/02-eheader.html
- GNU `readelf` 不依赖 BFD；这支持 deterministic producer 与 independent inspector 采用独立代码路径，而不是共享通用内部表示：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- ELF 的 `SHF_OS_NONCONFORMING` 要求链接器拒绝需要未知特殊知识的节；END-P2 同样不能把未知或未绑定的关键语义当成可忽略扩展：https://gabi.xinuos.com/elf/03-sheader.html
- RFC 8949 给出 CBOR 确定性编码基础，并要求具体协议冻结自己的唯一选择；END-FMT 因而必须同时定义最短编码、确定长度、键排序、字段语义与禁用类型，不能把通用 CBOR 解码成功当成符合性：https://www.rfc-editor.org/rfc/rfc8949.html
- GNU `ar -D` 会清除所有者、组、时间戳等变化来源；Endem 直接不把这些环境元数据写入规范头部：https://sourceware.org/binutils/docs/binutils/ar-cmdline.html
