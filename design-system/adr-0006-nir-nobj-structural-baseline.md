# ADR-0006：NIR 逻辑记录与 NOBJ 结构基线

- 状态：已接受为详细设计基线；数值 ABI、字段宽度和 Section 编号未冻结
- 日期：2026-07-12
- 影响范围：Noesis Core、NIR/NOBJ 规范、`noesis`、`morphe`、`theoria`、`synthesis`、验证器与测试语料

## 问题

现有设计已经区分目标、约束、歧义、验收、Section、符号与重定位，但仍缺少三个可以共同实现的契约：自然语言候选怎样升级为 NIR；NIR 记录最低包含哪些字段；NOBJ 怎样排布这些记录，使编译器、汇编器、检查器、链接器和验证器得到同一解释。

如果直接让模型输出 NIR 或二进制布局，模型置信度会被误当成来源忠实性，字段顺序、默认值和引用也会随模型变化。若只使用通用树形序列化，又难以安全表达图引用、链接、重定位、独立裁剪和装载视图。

## 决定一：自然语言只产生受约束候选

自然语言路径固定为：

`Source Package → Source Unit → Candidate Envelope → 确定性重推导或 Source Binding Decision → 规范化 NIR → NOBJ`

- Source Package 保存来源制品身份、摘要、媒体类型、语言、版本和许可；Source Unit 使用父单元、跨度与内容摘要定位最小可追溯片段。
- Candidate Envelope 保存候选主张、替代解释、证据、置信信息、模型与窗口指纹和未决状态。它不是 NIR。
- Noesis Core 只把能够由版本化规则重推导、绑定获授权 Source Binding Decision，或明确保留为歧义/未决状态的内容写入 NIR。
- Source Binding Decision 作为独立、可验证制品进入构建输入；NIR 与 NOBJ 只保存其摘要和受影响记录引用，不把临时对话当作授权。

## 决定二：NIR 使用图记录与显式来源

每个可扩展记录具有共同逻辑头：`record_kind`、`schema_version`、`flags`、`record_size`、`local_id`、`type_ref` 与 `origin_ref`。`record_size` 允许读取器跳过规范声明为可选的未知记录；未知且影响语义、链接、权限或验收的记录必须拒绝。

| 记录家族 | 最低逻辑字段 | 不能隐含的内容 |
| --- | --- | --- |
| Module | NIR 版本、命名空间、Profile、根目标、默认作用域、必需特性、验收根 | 当前工作目录、时间戳或模型默认提示 |
| Node | kind、type、symbol、modality、polarity、resolution state、payload、origin | 由名称猜测的实体身份 |
| Edge | relation type、source、target、scope、qualifiers、origin | 无类型整数引用 |
| Constraint | strength、operator、operands、scope、priority、conflict policy、unknown policy、origin | 把硬约束静默降级为偏好 |
| Ambiguity | subject、alternatives、evidence、risk、state、resolution policy、binding decision | 只保存最高置信候选 |
| Acceptance | subject goals、result schema、evaluator、evidence requirements、authority、unknown behavior、result states | 把评价器分数直接当成最终验收 |
| Capability Requirement | capability type、parameter schema、risk class、authorization ceiling、preconditions | 实时能力句柄或会话凭据 |
| Artifact Expectation | media type、schema、encoding、cardinality、destination role、required properties | 未说明消费者的输出 |
| Origin | semantic records、source artifact digest、span、derivation class、rule/model identity、decision digest、authority | 无来源的确认语义 |

引用在逻辑层使用“记录类别 + 局部索引”或稳定符号；不得把文件偏移当作语义身份。链接时可重编号局部索引，但稳定符号、来源摘要和验收身份不能因布局变化而改变。

## 决定三：NOBJ 采用前置目录与长度限定 Section

物理顺序采用：

1. 固定大小 Preamble 与 Header；
2. 可选 Load Directory；
3. Section Directory；
4. 字符串、类型和结构定义字典；
5. NIR 核心记录 Section；
6. 符号、重定位、依赖和策略 Section；
7. 来源映射与构建证据 Section；
8. 可裁剪调试 Section；
9. 完整性目录与分层摘要材料。

目录前置使读取器可以在读取任意大型载荷前检查计数、偏移、长度、对齐、重叠和资源预算。Section 载荷必须长度限定；固定记录 Section 声明 `entry_size` 和 `entry_count`，可扩展记录 Section 中每条记录自带 `record_size`。

### Header 逻辑字段

`magic`、`format_major`、`format_minor`、`header_size`、`object_kind`、`encoding_profile`、`flags`、`required_features`、Section Directory 的偏移/数量/表项大小、Load Directory 的偏移/数量/表项大小、字符串表索引、完整性 Section 索引和完整性 Profile 标识。Header 不递归保存覆盖自身的完整文件摘要。

当前候选编码 Profile 使用小端、64 位 checked offset/length 和 32 位表索引；这只是实现原型的研究起点，必须通过对象大小上限、跨语言读取器和畸形语料后才能冻结。

### Section Directory 逻辑字段

| 字段 | 作用 |
| --- | --- |
| `name_ref` | 指向受验证字符串表，名称不决定语义。 |
| `section_kind` / `schema_version` | 决定载荷结构及其版本。 |
| `flags` | required、alloc、readonly、merge、debug、compressed 等处理属性。 |
| `file_offset` / `stored_size` / `logical_size` | 定位文件字节并限制解压后大小。 |
| `alignment` | 只允许规范规定的值，计算必须 checked。 |
| `entry_size` / `entry_count` | 固定记录表的交叉检查；非表 Section 为零。 |
| `link_section` / `info` | 显式关联字符串表、符号表、目标 Section 或其他类型特定信息。 |
| `digest_ref` | 指向完整性目录中的载荷摘要。 |

### Load Directory 逻辑字段

Load Directory 只为需要装载视图的对象提供 Segment 级准入与权限映射，不保存机器虚拟地址。每项至少包含 `segment_kind`、`schema_version`、`flags`、`section_set_ref`、`logical_size`、`alignment`、`policy_ref`、`budget_ref` 与 `integrity_ref`。`section_set_ref` 指向经过验证的 Section 索引集合；同一 alloc Section 只能按规范允许的方式进入 Segment。Segment 权限不得比所属 Section 与策略声明更宽，压缩或调试 Section 不得通过 Segment 绕过大小和可执行性限制。

### 链接与证据记录的最低逻辑字段

| 记录 | 最低逻辑字段 | 主要不变量 |
| --- | --- | --- |
| Symbol | namespace/name ref、kind、linkage class（local/export/import）、visibility、definition state、section/record ref、type ref、version ref、resolution/missing policy、size or arity、origin ref、stable-key digest | 名称不是身份；定义状态、记录类别和类型必须一致；可选性与缺失行为显式声明；稳定键不能因 Section 重排改变。 |
| Relocation | target section/record/field、relocation kind、symbol ref、expected type、encoding/width、optional addend、overflow policy、origin ref | 只能修改声明字段；解析前后类型一致；未知类型、溢出、错位或重复应用必须失败。 |
| Dependency | kind、content digest、version constraint、required features、resolution policy、optional flag、origin ref | 正式依赖使用内容身份与锁定结果；文件系统搜索顺序或网络最新版本不能成为隐式输入。 |
| Origin | subject record range、source artifact digest、source unit/span、derivation class、rule/model identity、decision digest、authority、evidence refs | 每项确认语义可追溯；候选、规则推导和授权决定不能共用同一确认等级。 |
| Build Evidence | build type、input roots、external/config parameter digest、resolved dependency set、toolchain identity/digest、reproducibility profile、output digest | 构建输入与单次运行元数据分开；时间、绝对路径和 invocation ID 不进入运行语义或对象确定性身份。 |
| Integrity Entry | subject kind/index、stored/logical coverage、algorithm/profile、digest、tree parent/path ref、coverage flags | 摘要范围无循环定义；压缩前后覆盖语义明确；摘要成功不替代结构与策略验证。 |

### 逻辑 Section 家族

`nir.types`、`nir.nodes`、`nir.edges`、`nir.constraints`、`nir.ambiguities`、`nir.acceptance`、`nir.capabilities`、`nir.artifacts`、`strings`、`symbols`、`relocations`、`dependencies`、`policies`、`origins`、`build`、`debug.source` 与 `integrity`。这些名称描述职责，不冻结最终字节名称或编号。

`origins` 保存确认语义所需的最小来源摘要和决定引用；原始自然语言、注释和完整候选内容进入可裁剪的 `debug.source` 或外部 Debug Companion。`build` 保存输入摘要、配置、工具/模型指纹和已解析依赖，但不进入 Runtime 语义。发布裁剪前必须由覆盖工具证明来源映射仍可追溯。

## 决定四：文件身份、内部完整性与签名域分离

NOBJ 不把“字节相同”“运行语义等价”“来自获授权发布者”和“可以在当前环境运行”压缩成一个摘要或状态：

- **Exact File Digest** 由对象外部对完整 NOBJ 字节计算，用于内容寻址、构建比较和包清单。该值不能写回自己覆盖的 NOBJ 字节，也不能替代结构或语义验证。
- **Integrity Root** 位于 `integrity` Section，覆盖规范声明的 Preamble/Header 字段、目录表项和非 `integrity` Section 的 stored/logical digest。`integrity` Section 的目录项不得通过 `digest_ref` 指向自身；根记录及其存储字节不进入自己的覆盖域。它在未由受信外部 Exact File Digest、Package Subject Digest 或签名认证时只能证明对象内部自洽，不是来源真实性或抗恶意篡改的信任锚。
- **Semantic Identity** 只有在规范化表示和等价规则冻结后才能定义。当前阶段只能比较明确登记的目标、约束、权限、验收、依赖和披露属性，不能把布局不同的对象仅凭一个未定义“语义哈希”判为等价。
- **Package Subject Digest 与签名** 属于发布封装。签名覆盖不可变候选载荷和清单，Signature Envelope 位于被签载荷之外；签名验证不证明对象语义正确或当前环境授权。
- **Build ID** 只可作为诊断、缓存或 Debug Companion 查找标识，不是内容完整性证明。Debug Companion 必须用完整内容摘要绑定主对象与伴随文件，不能只依赖名称或 CRC。

摘要算法、树形布局、覆盖描述符编码和包签名格式仍未冻结，但任何候选方案都必须先消除自引用、循环覆盖和可变字段歧义，再进入测试向量。负向向量必须证明：修改载荷后同步重算内部根不能在缺少外部信任绑定时提升可信状态。

## 决定五：确定性、扩展与失败

- 相同规范化输入、配置、依赖和工具版本必须产生相同 Section 顺序、记录顺序、填充和字节摘要；时间、绝对路径、哈希表迭代和并发完成顺序不得进入对象。
- 若 Section 内使用 CBOR 等通用编码，必须声明专用确定性 Profile；通用编码器的任意合法输出不等于 Noemion 规范字节。
- 未知 `required` Section、记录或特性必须拒绝；未知可选调试 Section 可以跳过，但忽略它不能把拒绝变成允许。
- NIR/NOBJ 不复制 ELF weak symbol 的隐式优先级。符号使用 local/export/import 与显式 required/optional resolution policy；多个兼容定义仍不能靠输入顺序或“弱”绑定静默选择。
- Preamble、目录和固定记录使用固定宽度字段；可扩展语义载荷使用长度限定记录。任何 `offset + size`、`count × entry_size`、对齐上取整、解压大小和索引换算都使用 checked arithmetic。
- 结构良好、通用编码有效和 Noemion 语义可接受是三个不同层次；读取器不得把前一层成功当作后一层结论。

## 参考设计的采用边界

- ELF 的 Header、Section/Segment 双视图、Section Directory、Symbol 与 Relocation 关系用于组织和链接，但不照搬机器地址或指令语义：https://gabi.xinuos.com/elf/
- WebAssembly 的长度限定 Section、可跳过自定义 Section 和前置计数帮助单遍验证，但 NOBJ 仍需要 ELF 式随机访问目录与链接视图：https://webassembly.github.io/spec/core/binary/modules.html
- RFC 8949 的确定性编码、well-formed/valid/expected 分层用于约束通用载荷编码，不直接把 NIR 图降为 CBOR 树：https://www.rfc-editor.org/rfc/rfc8949.html
- SLSA Provenance 的 BuildDefinition/RunDetails 分离用于区分构建输入与运行元数据；NIR 运行语义不携带构建时间和临时环境：https://slsa.dev/spec/v1.2/build-provenance
- OpenAI 的 Harness Engineering 说明版本化资料、边界解析、机器可读观察和机械不变量对智能体可靠性的重要性；它支持把结构定义、诊断和测试留在仓库中，但不直接决定 NIR 字段或 NOBJ ABI：https://openai.com/zh-Hans-CN/index/harness-engineering/
- GNU GDB 的 separate debug files 使用 build ID 或 debug link 定位伴随文件，但 build ID 与 CRC 不等于对象内容签名；Noemion 只借鉴主对象与调试伴随文件分离的工作流：https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html

## 后果与未冻结内容

`noesis`、`morphe`、`theoria` 和 `synthesis` 的手册必须使用同一逻辑字段、Section 家族、身份域和失败层次。NIR 文本语法、魔数、最终字段宽度、Section 编号、Symbol/Relocation 数值枚举、压缩算法、摘要算法、文件扩展名和签名封装仍需规范样本、威胁模型、跨实现原型与后续 ADR 冻结。
