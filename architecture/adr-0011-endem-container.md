---
layout: architecture-decision
title: ADR-0011 · Endem 字节边界与读取顺序
page_role: content
footer_text: Noemion · ADR-0011
permalink: "/architecture/adr-0011-endem-container.html"
summary: 说明读取器怎样先检查不可信字节，再检查内容与外部条件；文件格式通过不等于目标有效或可以发布。
decision_id: ADR-0011
page_heading: ADR-0011 · Endem 字节边界 · 与读取顺序
page_lead: 规定读取器怎样先安全地划分不可信字节，再依次检查 Profile、内容语义和外部前置条件；格式通过不等于目标有效或可以发布。
badges:
- 当前策略
- END-FMT 0.1.0-draft
- ABI 未稳定
- 限制条件
previous_url: adr-0010-native-lexicon.html
previous_label: ADR-0010
next_url: adr-0012-rust-core-language.html
next_label: ADR-0012
---

## 先分清格式能够证明什么

END-FMT 只回答“这些字节能否被安全、确定地分段和解码”。它不能证明字段符合某个内容 Profile，不能证明六个语义面成立，也不能证明目标已经满足、制品已经获准运行或最终发布。

假设一个服务收到看似完整的 `.endem` 文件：头部、目录和六个载荷都能解码，但六个载荷只是空映射。读取器必须先承认字节结构可以读取，再明确停止在内容检查之前；它不能补写默认目标，也不能把“没有发现格式错误”显示成“目标有效”。

| 检查层 | 开发者实际检查什么 | 通过后仍不能声称什么 |
| --- | --- | --- |
| 容器接受 | 前导、目录、范围、对齐、填充和受限 CBOR 可以安全读取 | 字段集合与引用已经符合某个 Profile |
| Profile 接受 | 已知字段、枚举、顺序、引用和资源预算符合精确版本 | 意义已经得到具名主体确认，或内容满足 END-CORE |
| 内容接受 | 来源、意义、事态、目标方向、判据和未决问题满足通用内容义务 | 外部事实已经发生，目标已经满足 |
| 外部判断 | 授权、evidence entry、验证政策、撤销、满足结果和具名权威决定分别成立 | 其他时间、环境、主体或用途自动获得相同结论 |

> **关闭失败：**任何工具若用一个 `valid=true` 合并这些层次，或让未执行的后续检查隐式通过，就不符合本决定。

## 开发者应按什么顺序读取

1. 核对格式身份与总大小
2. 受检计算目录范围
3. 拒绝越界、重叠与非零填充
4. 检查 Profile 与能力闭包
5. 解码确定性载荷
6. 验证字段、引用与预算
7. 再进入内容与外部判断

| 读取步骤 | 典型拒绝输入 | 停止位置 |
| --- | --- | --- |
| 固定前导 | 魔数或版本错误、声明文件大小与实际输入不一致、保留位非零 | 读取目录前原子失败 |
| 目录算术 | `offset + count × entry_size` 溢出、目录越界或记录数超限 | 分配目录数组前失败 |
| 记录范围 | 记录回绕、未对齐、互相重叠、覆盖目录、尾随字节或非零填充 | 解释任一载荷前失败 |
| Profile 能力 | 未知 Profile、未知关键记录、压缩、加密或未登记状态 | 不得尝试降级读取 |
| CBOR 与字段 | 非最短整数、乱序或重复键、开放长度、禁用类型、未知字段或悬空引用 | 定位记录和路径后拒绝，不得改写后接受 |
| 内容与外部前置条件 | 意义选择器尚未完成意义确认、证据未取得或发布用途不匹配 | 保留已完成的有限检查，不提升为完整接受 |

例如，一个文件可以具有正确的 64 字节前导、六个 48 字节目录项和六个可解码空映射，因此通过 END-P0 的结构实验；它仍不是内容合格的 Endem。读取器必须报告“结构接受、语义未执行”，而不是把空载荷补成默认目标。

## END-P0、END-P2 与发布版分别做什么

| 对象 | 当前用途 | 明确上限 |
| --- | --- | --- |
| END-FMT | 定义 64 字节固定前导、48 字节目录项、记录范围和确定性载荷子集 | 物理容器；不定义六个语义面的字段意义 |
| END-P0 | 验证固定头部、目录、范围、受限 CBOR 和有限资源预算 | 结构实验；六个空映射不是最小有效 Endem |
| END-P2 | 封闭来源保留的形成与评审字段、枚举、顺序和引用 | 单文件最高只能达到 Profile 接受；不是稳定 ABI，也不可发布 |
| 未来发布 Profile | 保存允许分发和受限运行的已确认结构，并移除原始自然语言 | 字段、编码和来源伴随关系尚未定义；当前不能生成 |

END-P2 包含实际进入形成过程的自然语言。最终发布不能只删除 `source_expression.content` 后继续沿用 END-P2：来源引用必须重写或移除，引用闭包必须重新证明，裁剪结果必须取得新身份，并重新生成面向发布字节的声明与验证结果。

> **名称边界：**END-P0 与 END-P2 是版本化 Profile 标识，不是新的哲学对象。页面先写直白职责，是为了让开发者在朗读编号之前先知道两者为何不同；这不替代未来发行名称的口头验证。

## 为什么采用固定目录与受限 CBOR

| 机制 | 解决的问题 | 没有采用的范围 |
| --- | --- | --- |
| 固定前导与显式目录 | 在解释复杂载荷前确定版本、Profile、记录数量、位置和完整输入范围 | 不采用 ELF 的地址、指令、装载段、处理器 ABI 或链接语义 |
| 定宽目录项与受检算术 | 让不同语言的读取器对溢出、截断、越界和重叠得出相同首错 | 不把磁盘字节强制转换为宿主结构体 |
| 确定性 CBOR 子集 | 复用整数、字符串、数组和映射编码，同时冻结最短表示、确定长度与键顺序 | 通用 CBOR、浮点、标签、开放长度和未知字段不能自动进入 Endem |
| 规范与向量共享，读取实现分离 | 未来形成路径与独立读取路径可以发现彼此的解析偏差 | 当前规范与已执行向量不是 deterministic producer、independent inspector 或正式独立读取组件 |

JSON 继续适合保存人类可读的语义案例，却不是规范字节。Protocol Buffers、FlatBuffers 或大型 IR 也没有当前消费者足以证明其生成代码与运行时应进入小型读取边界；若将来只在非可信适配层使用，必须另行说明输入、输出和失败责任。

## 权威机制怎样限定本决定

| 权威资料 | 支持的局部原则 | 不能推出什么 |
| --- | --- | --- |
| [ELF 文件结构](https://gabi.xinuos.com/elf/01-intro.html)<br>[ELF Header](https://gabi.xinuos.com/elf/02-eheader.html) | 固定头部可以成为解释文件的路线图，条目大小、数量与偏移必须显式 | Endem 是机器对象文件，或 ELF 字段可以直接成为 Endem ABI |
| [GNU readelf](https://www.sourceware.org/binutils/docs/binutils/readelf.html)<br>[GNU ar 确定性模式](https://sourceware.org/binutils/docs/binutils/ar-cmdline.html) | 独立读取路径可以不依赖通用对象库；输出可以排除时间、所有者和文件模式等环境差异 | 资料实验已经实现independent inspector，或确定性字节自动取得语义与信任 |
| [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html) | well-formed、valid 和 application-expected 是不同接受层；应用必须定义自己的具体数据模型与确定性规则 | 通用解码成功、通用 CBOR 类型或默认编码选择自动符合 END-P2 |
| [GNU strip](https://sourceware.org/binutils/docs/binutils/strip.html)与 [ADR-0036](adr-0036-source-bearing-and-stripped-release.html) | 完整形成制品与有损裁剪后的发布制品可以有不同用途和身份 | 删除一个记录或字段就能得到安全、闭合、可发布的 Endem |

## 当前限制与开发入口

END-FMT、END-P0 与 END-P2 都是 `0.1.0-draft`，不承诺向后兼容。当前只有规范、机器可读 Profile 和已执行的正反向量；没有正式写入组件、independent inspector、稳定 ABI、MIME 类型、升级协议或发布 Profile。任何新增记录、字段、变换或状态都必须先给出具名消费者、威胁、正反向量和独立读取方案。

- [先理解 Endem 内容职责](../specifications/endem.html) — 从一个目标的来源、意义、事态、方向、判据和未决问题开始。
- [查看 END-P2 字段闭包](adr-0013-end-p1-payload.html) — 确认来源保留的形成 Profile 允许哪些字段和引用。
- [区分内容、Profile 与容器](adr-0023-endem-content-standard.html) — 不要用物理格式替代通用内容义务。
- [查看最终发布边界](adr-0036-source-bearing-and-stripped-release.html) — 了解为什么裁剪结果必须使用新 Profile、新身份和新验证。
