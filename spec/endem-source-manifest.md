# Endem Source Manifest

- 规范 ID：`END-SRCM`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：实验性 Poiet 输入草案；由 ADR-0014 采用
- 对象关系：只映射到 `END-P1`；不是 `.endem` 线格式，也不是稳定源语言
- 实现状态：仅有来源样例与资料检查器；没有 Poiet 解析实现

## 1. 范围

来源清单让已经获得授权的来源、投影和判断契约进入确定性 Poiet。它同时保存解码并处理转义后的自然语言表达和结构化决定，但不负责自然语言理解。模型、界面或人工流程只能位于清单上游；Poiet 不调用模型补字段，也不把候选自动升级为确认语义。

清单采用 UTF-8、逐行、制表符分列的有限语法。它只服务首个 END-P1 纵向切片；以后若建立正式来源语言，应删除这一入口，不保留兼容垫片。

### END-SRCM-001 — 输入身份与编码有限

**要求：**输入 `MUST` 是 UTF-8，文件上限为 16 MiB，单行上限为 1 MiB。实现 `MAY` 接受 LF 或 CRLF，但必须把两者解释为相同的行边界。空行和第一个字节为 `#` 的行忽略；不得隐式裁剪其他空白。

**失败：**编码无效、文件或单行超限时，Poiet 必须在解析指令前拒绝，不能产生部分 Endem。

**验证：**`tests/source_manifest_test.py`；未来 Poiet 与 Theor 的边界测试需在代码阶段开启后建立。

**来源保真边界：**LF 与 CRLF 被解释为相同行边界，字段转义会被解码。因此 END-SRCM 只承诺把提交后的解码表达映射到 `rhem.content`，不能声称逐字节保留原始 `.ends` 文件。若未来需要核对原始来源字节，必须另行绑定原始文件身份、解码 Profile、变换链和损失清单；当前 END-P1 不新增这些字段。

### END-SRCM-002 — 指令集合封闭

**要求：**每个非注释行由制表符分隔为指令和参数。只允许下表指令；未知指令、参数数量不符或单例重复必须拒绝。

| 指令 | 参数 | 基数 |
| --- | --- | ---: |
| `rhem` | source_id, subject, media_type, language, version, content, range_start, range_length | 1 |
| `symbol` | id, kind, source_ref | 1..n |
| `relation` | id, predicate, projection_kind, projection_id, role_name=symbol... | 1..n；至少一个 role |
| `situation` | id, relation, polarity | 1..n |
| `root` | situation_id | 1 |
| `telis` | mode | 1；END-P1 仅 `kine` |
| `phain` | relation, match | 0..n；END-P1 仅 `same-roles` |
| `iknem` | evidence_requirement_id | 0..n |
| `krin` | on_missing, on_error, decision_authority | 1；END-P1 仅 `agno`, `fault` |
| `apor` | id, source_ref, conflict, decision_authority, candidates(csv), impact_scope(csv), resolutions(csv) | 0..n |

**失败：**指令或基数不符合时返回来源层诊断，并定位行号。

**验证：**`vectors/source/minimal.ends`；未知指令、错误参数数量和重复单例变异。

### END-SRCM-003 — 转义与复合字段无歧义

**要求：**字段只解释 `\\n`、`\\r`、`\\t` 与 `\\\\` 四种转义。role 必须写成 `name=symbol`。CSV 只用于标识符或登记枚举的有序输入；空字段表示空数组。标识符本身不得含制表符、换行、逗号或等号。

**失败：**未知或不完整转义、role 缺少等号、CSV 元素不符合 END-P1 类型时必须拒绝。

**验证：**`tests/source_manifest_test.py`；未来来源解析器单元测试需在代码阶段开启后建立。

### END-SRCM-004 — 输入顺序不决定对象字节

**要求：**Poiet 必须先验证身份唯一性和引用闭包，再按 END-P1 规范顺序形成记录。`symbol`、`relation`、role、`situation`、`phain`、`iknem` 与 `apor` 的输入行顺序不得改变输出；重复身份不能靠后项覆盖。

**失败：**相同规范集合因输入顺序产生不同 `.endem` 字节，或重复身份被静默接受，均不符合本规范。

**验证：**`tests/source_manifest_test.py` 把最小清单映射到 `SV-VALID-MINIMAL-001`，并由资料检查器逐字节比较 `WV-P1-SEMANTIC-ACCEPT-001`。

### END-SRCM-005 — 来源、候选与授权不能混合

**要求：**`rhem` 保存来源文本；`symbol/relation/situation/root/telis/krin` 只保存确定性规则或具名权威已确认的投影。存在多个可表达候选但尚无权选择时，输入者必须写入 `apor`。模型输出不能直接充当 projection、decision_authority 或通过结论。

**失败：**没有允许投影时返回 `aseme`；存在选择但未记录 `apor` 时按 `END-APR-001` 拒绝；Poiet 不尝试猜测。

**验证：**END-CORE 语义向量与人工授权边界复核。

### END-SRCM-006 — 失败原子且不扩大 Profile

**要求：**清单解析、END-P1 语义验证和对象写入必须形成单一事务边界。任何来源、类型、引用、排序或资源错误都不得留下部分 `.endem`。清单不能提高 END-P1 的字符串、图、嵌套或累计分配上限。

**失败：**任一阶段失败时只返回诊断，不返回部分可信模型或字节。

**验证：**当前使用 END-P1 正反向量与资料检查器；未来 Poiet 与 Theor 的实现测试需在代码阶段开启后建立。

### END-SRCM-007 — 实验入口不得冒充正式语言

**要求：**工具、文档和发行材料必须把 `.ends` 描述为实验性来源清单。它不是自然语言编译标准、不是 Endem 身份的一部分，也不承诺向后兼容。正式来源语言只有在具备注释、包含、版本演进、歧义、错误恢复和正反语料后才能取代它。

**失败：**任何稳定 ABI、通用自然语言理解或兼容性声明必须被发布检查拒绝。

**验证：**公开内容检查与具名规范维护者复核。

## 2. 最小示例

最小接受样例位于 `vectors/source/minimal.ends`。它表达“为已登记项目生成安全评审报告”的来源文本、两个符号、一条关系、一个根事态和一个比较契约。该示例应确定性映射到语义向量 `SV-VALID-MINIMAL-001`，再由 Poiet 生成 `WV-P1-SEMANTIC-ACCEPT-001`。

`vectors/source/with-apor.ends` 在同一目标上增加“目标读者尚未确认”的未决项，明确列出候选读者、受影响关系、允许的解决方式与决定权威。它必须生成含一个非空 `apor` 的 `WV-P1-APOR-ACCEPT-001`；Poiet 不得替用户选择读者，也不得因为仍有未决项而丢弃整个目标。

## 3. 未决内容

本草案没有冻结注释元数据、包含、模块、宏、变量、量化、时间、单位、求值表达式、错误恢复、格式化器或 IDE 协议。出现真实消费者前，不为这些能力预留语法。
