# Text and Identifier Core Specification

- 规范 ID：`TEXT-IDENTIFIER-CORE`
- 版本：`0.1.0-draft`
- 日期：2026-07-13
- 状态：草案；条款化表达 ADR-0028 已接受的跨制品文本与标识符边界
- 物理编码：不创建新文件、对象、字段或命令；当前只约束现有文本槽怎样解释
- 实现状态：仅有规范提案向量检查器；没有 Unicode 处理器、规范化器、同形检测器或模型输入网关

## 1. 范围

本规范定义 Endem、Synem、Dromen、Iknem、诊断、外部适配和模型候选怎样区分原始来源文本、结构标识符、登记词、描述文本与显示视图。它回答“机器实际取得哪些码点、哪些变换已经发生、两个字符串按什么规则比较，以及人和模型看到的是否是同一份内容”。

`TEXT-IDENTIFIER-CORE` 不是自然语言理解规范，也不创造语义等价、Unicode 标识符或文本制品。相同字形不表示相同字节、相同码点或相同 `semion`；不同字形也不自动表示不同意义。当前 END-P1 的结构标识符继续只允许 ASCII。来源文本可以使用 Unicode，但任何规范化、大小写折叠、双向重排、同形检测和不可见字符处理都必须保持在自己的职责层。

文本用于授权、同意或多人决定时，安全显示视图和精确机器请求还必须固定并符合 `AUT-CORE` 的精确版本。TEXT-IDENTIFIER-CORE 只证明显示与机器内容怎样对应，不证明观看者具有决定权。

大写的 `MUST`（必须）、`MUST NOT`（不得）、`SHOULD`（应当）、`SHOULD NOT`（不应）与 `MAY`（可以）按 BCP 14 解释：

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

## 2. 文本与标识符条款

### TEXT-SLT-001 — 每个文本槽必须先声明职责

**要求：**每个字符串字段 `MUST` 绑定精确规范版本和一种槽类别：`source-content`、`structural-identifier`、`registered-token`、`descriptive-text` 或 `display-message`。槽定义 `MUST` 指定允许编码、字符集合、比较方式、变换、长度单位、显示责任和失败影响。同一字符串不得仅因复制到另一字段而继承原槽的比较或信任规则。

**失败：**实现把来源正文当作标识符、把本地化消息当作机器码、把显示别名当作内容引用，或在未声明槽类别时使用字符串作授权与绑定，必须拒绝该用途。

**验证：**`TEXT-SCN-001`；`vectors/text-identifier/cases.json`；未来 `peira:text-slot-classification` 组件测试。

### TEXT-ENC-001 — 解码必须唯一且先于任何变换

**要求：**当前交换文本 `MUST` 使用 RFC 3629 定义的 UTF-8。解码器 `MUST` 拒绝无效起始字节、无效续字节、过长编码、代理项和大于 U+10FFFF 的值，并在规范化、转义、分词或字段解析前原子失败。字节顺序标记、NUL、非字符和控制字符的允许性由具体槽 Profile 决定，不能由实现默认接受或删除。

**失败：**替换无效字节后继续形成对象、多个字节序列解码为同一标量、先规范化再发现解码错误，或把平台本地编码作为隐式输入，均不符合本规范。

**验证：**`TEXT-SCN-002`、`TEXT-SCN-003`；`vectors/text-identifier/cases.json`；未来 `peira:utf8-unique-decode` 组件测试。

### TEXT-SRC-001 — 原始字节、解码文本与变换结果必须分开

**要求：**声称保留来源时，记录 `MUST` 分开绑定原始来源字节身份、字符编码、解码 Profile、解码后的 Unicode 标量序列、全部后续变换和损失。规范化、换行统一、转义展开、去 BOM、裁剪或脱敏后的文本 `MUST` 取得自己的身份，并以显式关系指向输入。当前 END-SRCM 只能把转义展开后的 `rhem.content` 映射进 END-P1；没有外部原始字节身份时，它 `MUST NOT` 声称保留了 `.ends` 文件的逐字节原貌。

**失败：**把 CRLF 与 LF 输入称为同一原始文件、转义展开后仍沿用输入字节身份、隐式删除不可见字符，或无法说明变换前后范围关系时，来源声明不足。

**验证：**`TEXT-SCN-004`、`TEXT-SCN-005`；`vectors/text-identifier/cases.json`；未来 `peira:source-byte-text-provenance` 组件测试。

### TEXT-IDN-001 — 结构标识符保持封闭 ASCII

**要求：**END-P1、规范条款 ID、机器诊断码、关系 ID、符号 ID 和其他安全绑定标识符 `MUST` 使用各自现行 Profile 登记的 ASCII 语法，按原始字节区分大小写，且不受区域设置影响。实现 `MUST NOT` 对它们执行 Unicode 规范化、大小写折叠、宽度映射、同形骨架匹配或本地排序。未来若允许国际化标识符，必须建立绑定精确 Unicode 版本、UAX #31 Profile、UTS #39 限制和迁移规则的新内容 Profile。

**失败：**`A` 与 `a` 被默认合并、全角字符映射进 ASCII ID、土耳其语区域设置改变比较、视觉同形字符选择同一对象，或未升级 Profile 就接受 Unicode ID，必须拒绝。

**验证：**`TEXT-SCN-006`、`TEXT-SCN-007`；`vectors/text-identifier/cases.json`；未来 `peira:ascii-identifier-closure` 组件测试。

### TEXT-NRM-001 — 规范化必须绑定槽与版本

**要求：**Unicode 规范化 `MUST` 由版本化变换 Profile 明确指定输入槽、Unicode 版本、NFC/NFD/NFKC/NFKD 或 `none`、输出用途和身份影响。当前 `source-content`、精确内容身份和 END-P1 结构标识符一律使用 `none`；实现 `MUST NOT` 静默规范化后接受。NFKC/NFKD 会消除兼容差异，`MUST NOT` 盲目应用于任意来源文本。原始输入和变换关系必须可追溯。

**失败：**不同实现自行选择 NFC 或 NFKC、规范化后覆盖原文、拼接已规范化片段却不重新核对，或把规范化结果当作语义等价证明，均不符合本规范。

**验证：**`TEXT-SCN-008`、`TEXT-SCN-009`；`vectors/text-identifier/cases.json`；未来 `peira:text-normalization-profile` 组件测试。

### TEXT-CMP-001 — 比较必须声明比较域

**要求：**每次机器比较 `MUST` 固定操作数槽、比较 Profile、Unicode 与变换版本，并明确采用精确字节、Unicode 标量、具名规范化结果、大小写映射、语言相关排序或同形风险检测中的哪一种。比较结果只能支持声明域中的结论。区域排序、搜索匹配、同形骨架和模型相似度 `MUST NOT` 替代内容身份、结构标识符相等或 `semion` 等价。

**失败：**界面搜索命中被当作精确引用、NFC 相等被当作原始字节相同、同形检测被当作同一对象，或未固定区域设置就产生规范顺序，比较无效。

**验证：**`TEXT-SCN-010`；`vectors/text-identifier/cases.json`；未来 `peira:text-comparison-domain` 组件测试。

### TEXT-RNG-001 — 范围必须绑定主体、单位与变换

**要求：**文本范围 `MUST` 绑定精确文本主体身份、表示版本、半开区间和单位。当前 END-P1 的 `rhem.range` 只使用 Unicode 标量索引；字节、UTF-16 code unit、扩展字素簇、屏幕列和模型 token `MUST NOT` 冒充标量。任何会改变标量序列的变换都必须产生范围映射或使旧范围失效；范围计算使用受检算术。

**失败：**把用户可见字符数写成标量长度、规范化后复用旧范围、组合字符中间被当作稳定界面选区，或范围主体不明时，定位必须拒绝或降为非权威显示。

**验证：**`TEXT-SCN-011`、`TEXT-SCN-012`；`vectors/text-identifier/cases.json`；未来 `peira:text-range-unit-binding` 组件测试。

### TEXT-BID-001 — 存储逻辑顺序与显示顺序必须分开

**要求：**文本身份、范围和解析 `MUST` 使用 Unicode 逻辑顺序。支持双向文字的显示器 `MUST` 遵守绑定版本的 UAX #9，并按字段或词法槽隔离方向；显示顺序 `MUST NOT` 回写或参与身份比较。来源正文中的方向控制可以保留，但安全审查视图必须显示其位置与名称；当前 ASCII 结构字段不得包含方向控制。

**失败：**复制视觉顺序覆盖逻辑顺序、方向覆盖符让分隔符或字段边界看似移动、不同渲染器改变规范解析，或审查界面隐藏安全相关控制，均不符合本规范。

**验证：**`TEXT-SCN-013`、`TEXT-SCN-014`；`vectors/text-identifier/cases.json`；未来 `peira:bidi-storage-display-separation` 组件测试。

### TEXT-HID-001 — 不可见字符与同形风险不能静默处理

**要求：**来源、候选和描述文本 `MUST` 能生成绑定 Unicode 版本的不可见字符、默认可忽略字符、变体选择符、连接符、非 ASCII 空白、混合脚本和同形风险清单。安全审查视图 `MUST` 能显式呈现这些位置。清单或 UTS #39 骨架只支持风险提示与复核，`MUST NOT` 合并身份、自动改写来源或单独证明恶意。结构标识符继续由 ASCII Profile 在解析前关闭此风险。

**失败：**静默删除零宽字符、把混合脚本警告当作确定攻击、按同形骨架选择账户或对象，或审核者无法看到模型实际接收的不可见序列时，处理无效。

**验证：**`TEXT-SCN-015`、`TEXT-SCN-016`；`vectors/text-identifier/cases.json`；未来 `peira:hidden-confusable-inventory` 组件测试。

### TEXT-MET-001 — 语言与媒体元数据只是声明

**要求：**语言标签、媒体类型、字符编码、书写方向和区域设置 `MUST` 分别验证并绑定声明来源。BCP 47 标签和媒体类型只能描述预期解释，`MUST NOT` 证明内容确实属于某语言、允许某种规范化或取得语义权威。规范排序、标识符、摘要和对象形成不得依赖进程默认 locale。任何语言相关分词、大小写或排序必须使用独立版本化 Profile。

**失败：**根据自报 `language` 静默小写、用默认 locale 排序规范数组、媒体类型触发未登记转码，或把语言检测模型输出当作事实字段，必须拒绝规范用途。

**验证：**`TEXT-SCN-017`；`vectors/text-identifier/cases.json`；未来 `peira:text-metadata-locale` 组件测试。

### TEXT-AIM-001 — 模型输入必须绑定机器实际接收的文本

**要求：**任何提交给模型、检索器或 tokenizer 的文本候选 `MUST` 绑定输入内容身份、全部预处理变换、不可见与同形风险清单、模型和 tokenizer 身份，以及供人复核的显示视图身份。显示视图与实际输入不同 `MUST` 明示差异。模型输出继续保持 `model-candidate`，不得因清洗、规范化、重复采样或置信分数而取得投影权威、规范字节写入权或隐藏字符删除权。

**失败：**审核者看到清洗文本而模型接收含变体选择符的另一序列、服务端隐式改写输入、日志只存显示摘要，或模型把不可见内容静默带入确认投影时，候选链不可信。

**验证：**`TEXT-SCN-016`、`TEXT-SCN-018`；`vectors/text-identifier/cases.json`；未来 `peira:model-text-view-binding` 组件测试。

### TEXT-OUT-001 — 显示、复制与导出必须披露变换

**要求：**显示、诊断、日志、导出和复制视图 `MUST` 绑定来源身份与视图 Profile，并声明转义、截断、脱敏、规范化、方向隔离和控制字符可视化。人类显示可以为了安全增加标记，但 `MUST NOT` 成为安全引用。界面涉及绑定或授权时，必须同时提供精确机器值或明确的安全复制路径；截断与脱敏对判断和证据覆盖的影响必须保留。

**失败：**用户从短显示复制出安全引用、转义文本看似原文、日志截断后仍用于复现、脱敏隐藏决定性差异，或显示警告反向改变对象内容时，输出不符合本规范。

**验证：**`TEXT-SCN-018`；`vectors/text-identifier/cases.json`；未来 `peira:text-display-export-provenance` 组件测试。

## 3. 思想来源与采用限制

维特根斯坦在《逻辑哲学论》3.32 写道：“记号是一个符号中可以被感官感知到的东西。”3.321 又指出，同一个记号可以被不同符号共有。这里的工程启发是：可见文字、编码序列和已授权意义必须分层，使用位置与关系结构不能被字形替代。它不能直接决定 UTF-8、NFC、标识符语法或安全策略；这些仍由本规范、Profile、威胁和向量定义。

## 4. 权威依据与采用边界

- RFC 3629 定义 UTF-8 的有效范围与唯一编码，并提醒可见“同一内容”可能存在不同字符序列。Noemion 先唯一解码，再按槽决定是否允许后续变换。
- Unicode 17、UAX #15、UAX #31、UAX #9、UTS #39 与 UTS #55 分别提供字符模型、规范化、标识符、双向显示、同形检测和安全审查机制。本规范引用具体职责，不把某个 Unicode 算法提升为语义判断。
- RFC 8264 要求国际化字符串 Profile 明确映射、大小写、规范化、方向和比较规则，并警告不要无限增加 Profile。Noemion 因此保留当前 ASCII 结构标识符，只在真实消费者出现后讨论国际化标识符。
- GNU libunistring 分开 UTF-8/16/32 表示、规范化、大小写、字素、词和行处理。Noemion 借鉴这种职责分离，不在当前阶段引入库或实现。
- 近期模型研究表明，不可见字符、同形替换和变体选择符可能改变模型分词与安全行为。它们只构成威胁建模依据；单篇论文、单个模型或攻击成功率不成为规范真理。

## 5. 当前未定义

本规范不冻结 Unicode 国际化结构标识符、NFC 来源重写、自然语言语义等价、语言检测、分词、字素级编辑、搜索排序、拼写校正、字体信任、模型 tokenizer 协议、同形自动处置、双向编辑器、原始来源字节字段或稳定文本 Profile。END-P1 不新增字段；要把原始字节身份、变换清单或国际化标识符写入制品，必须由真实生产者和消费者、独立 ADR、新 Profile、规范字节与正反向量另行证明。
