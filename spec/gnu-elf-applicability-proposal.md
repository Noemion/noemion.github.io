---
layout: spec
title: "GNU 与 ELF 机制适用性研究提案 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/gnu-elf-applicability-proposal.html"
summary: "说明 Noemion 可以借鉴 ELF 与 GNU 工具的哪些职责分离方法，以及为什么目标制品不是另一种机器目标文件。"
document_status: "非规范研究提案"
---
# GNU 与 ELF 机制适用性研究提案

状态：非规范研究提案  
日期：2026-07-13  
适用范围：非组件研究

## 直接结论

Noemion 可以借鉴 ELF 与 GNU Binutils 已经验证了数十年的职责分离思想，但不能把以自然语言表达的目标写成“另一种机器目标文件”。两者处理的对象、信任问题和失败后果不同。

本提案不构成 ADR、CORE 规范、内容 Profile 或实现要求。它不创建新制品、文件格式、扩展名、命令、组件或稳定接口，也不进入 `registry.json`。这里出现的“采用”只表示值得继续研究的工程不变量，不表示规范已经冻结。

当前结论可以压缩为四点：

1. 借结构、职责、失败边界和独立验证，不借机器地址与指令语义。
2. 把每项可用思想交给现有规范，不为了类比创造一套新对象。
3. 拒绝环境搜索、弱绑定、默认版本、静默裁剪和带错输出成为可信制品。
4. 任何未来规范化都要先证明真实生产者、消费者和失败责任。

## 类比不能越过的边界

| 容易形成的类比 | 实际边界 |
| --- | --- |
| Endem 是 ELF object | Endem 表达一个期望终态；ELF object 组织机器相关代码与数据。固定前导和目录只是容器机制相似。 |
| Synem 是 executable 或 shared object | Synem 是精确 Endem 的完整传递闭包，不是可装载机器映像。 |
| session contract 是 segment 或 process image | session contract 是一次会话的只读执行契约，永远不是文件、内存映像或持久状态。 |
| `semion` 是 linker symbol | `semion` 保存获授权的意义投影；链接符号主要定位程序实体。名字相同不表示职责相同。 |
| 精确绑定是 relocation | Noemion 绑定选择精确内容身份；ELF relocation 修正地址或数值位置。 |
| Iknem 是 debug information | Iknem 是有范围、有来源和有限主张的证据。调试信息只是一种可能输入，不能代表证据整体。 |
| Drasor 是 dynamic loader | Drasor 是受限执行域。动态装载只是可能被研究的运行机制之一，不定义其权限边界。 |

## 职责适用性矩阵

| GNU / ELF 机制 | 原机制实际解决的问题 | 可迁移的不变量 | Noemion 现有责任归属 | 明确拒绝的类比或行为 | 进入未来 ADR 前还缺什么 |
| --- | --- | --- | --- | --- | --- |
| Section 与 Segment | Section 组织文件内容；Program Header 把内容映射为装载视图 | 持久内容视图与一次运行视图分开 | END-FMT、DRO-CORE、ID-CORE | 把 Dromen 编码成 segment、文件或进程映像 | 真实运行消费者、漂移案例、身份与销毁反例 |
| Symbol | 为链接器提供名称、定义、可见性和引用 | 引用必须有类型、范围和唯一解析结果 | `semion`、SYN-CORE、ID-CORE、TEXT-IDENTIFIER-CORE | 名称即身份、弱符号兜底、全局环境查找、未版本化默认项 | 两个同名不同身份案例、冲突失败语义、规范绑定向量 |
| Relocation | 在输出布局确定后修正地址或数值位置 | 形成结果前保存待绑定位置及其精确目标 | SYN-CORE 的 binding record、ID-CORE | 地址修补、运行期语义漂移、网络 `latest`、顺序依赖选择 | 物理 Synem 消费者、固定引用语法、丢失与循环反例 |
| Linker script | 显式控制输入 Section 到输出和内存布局的映射 | 策略必须显式、封闭、版本化并参与结果身份 | END-P*、SYN-CORE、AUT-CORE | 隐式默认脚本、环境变量、搜索路径或命令顺序取得权威 | 精确政策消费者、规范化规则、身份影响和威胁分析 |
| Link map | 说明哪些输入进入结果、归档成员为何被拉入、符号值如何形成 | 形成过程必须能追溯选择、删除、冲突和最终绑定 | IKN-CORE、DIA-CORE、ID-CORE；模型装配提案 | 把“被包含”当作语义正确、目标满足或最终接受 | 明确记录消费者、最小披露、完整性与可信度边界 |
| `--gc-sections` | 从根出发沿符号和重定位可达性删除未使用 Section | 删除必须有显式根、闭包算法、删除清单和可复查依据 | 制品生产者、SYN-CORE、ID-CORE、Iknem | 静默裁剪 `apor`、语义面、必需成员或失败记录 | 可删除内容分类、等价定义、正反字节向量、停止条件 |
| Symbol versioning | 把符号绑定到版本节点并表达节点依赖 | 绑定契约必须精确版本化，版本选择可审计 | SYN-CORE、ID-CORE、ADP-CORE | 默认版本、兼容范围、旧 ABI 别名和回退选择 | 第一真实跨版本消费者、升级和拒绝矩阵、迁移身份规则 |
| `readelf` 独立于 BFD | 用格式专用路径查看 ELF，避免 BFD 缺陷同时污染两条路径 | 第二读取路径要与生产写入和读取路径独立 | Theor、DIA-CORE、未来符合性检查 | 共享同一解析库后声称独立、把查看成功当内容接受 | 项目进入代码开发阶段并明确实现范围后，才允许独立实现与差分证据 |
| BFD canonical form | 用统一前端处理多种 object 格式 | 统一抽象必须声明不可表示内容和转换损失 | ADP-CORE、TEXT-IDENTIFIER-CORE、ID-CORE | 建立“通用自然语言对象 IR”、静默丢失来源或语义位置 | 第二种真实格式、不可替代消费者、往返损失向量 |
| `objcopy` / `strip` / debug link | 复制、转换、裁剪对象，并把调试内容分离到伴随文件 | 每次实质变换产生新身份，并记录来源、保留内容和损失 | 制品生产者、ID-CORE、Iknem | 原位修改 attested 制品、派生物继承签名或接受状态 | 调试伴随消费者、变换 Profile、逐字节关系证据 |
| Build ID | 为链接输出提供可定位的构建标识，但不是当前文件校验和 | 构建关系与精确内容身份分开 | ID-CORE | 用 build ID、短摘要、路径或名称选择安全对象 | 发行身份 Profile、完整摘要策略、两条独立产出证据 |
| 带错继续和部分输出 | `ld` 为收集更多诊断可继续，某些情况下仍产生输出 | 诊断可以累计，但可信结果必须原子形成 | DIA-CORE、END-FMT、SYN-CORE | 报错后把部分 Endem 或 Synem 标成可信、可运行或已接受 | 每层原子失败案例、主诊断规则、资源上限 |
| 确定性 archive 与可复现发行 | 固定成员顺序、时间等非语义输入可减少输出漂移 | 重复构建要固定输入闭包并逐字节比较 | ID-CORE、未来内部符合性检查 | 单个工具选项、一次重跑或签名成为复现证明 | 两个隔离环境、缓存独立性、差异归因和发布政策 |

## 支持案例与反例

### 案例一：精确闭包可以借鉴链接，但不能借搜索顺序

一个 Synem 引用两个 Endem。形成时，每个引用都绑定完整身份域与摘要。交换输入文件的排列顺序，闭包身份和绑定结果不变。

反例：两个仓库都提供名为 `deploy-ready` 的候选对象。形成过程按搜索路径取先出现者。这个行为应当失败，因为名称和顺序没有选择权威。

### 案例二：绑定记录不是地址重定位

Synem 可以记录“成员 A 的一个必需引用绑定到精确成员 B”。这借鉴了链接器保存引用位置和最终目标的可追溯性。

反例：把 B 的内容换成“兼容版本”，却保持 Synem 身份不变。这等于让运行期重定位改写语义闭包，必须拒绝。

### 案例三：裁剪必须显式说明根与损失

未来制品生产者若删除只服务人类调试的伴随内容，应产生新制品身份，并记录来源、变换、保留项和删除项。

反例：因为某个 `apor` 没有下游机器引用就将其视为“不可达”并删除。`apor` 是未决语义边界，不是无用 Section；删除会伪造确定性。

### 案例四：形成映射只能证明过程，不能证明目标

一份形成映射可以证明某个 Endem 被纳入 Synem，并说明引用为何解析到它。这能支持过程审计。

反例：因为 Endem 出现在映射里，就把它判断为 `met`，或把 Synem 判为 `accepted`。输入包含关系没有满足或决定权威。

### 案例五：调试伴随物不继承信任

一个裁剪后的发行制品与一个详细伴随记录可以通过完整身份建立关系。两者分别签名、分别评估。

反例：伴随记录由受信任构建产生，因此自动继承源制品的签名、Iknem、权限或接受状态。来源关系不能复制信任结论。

### 案例六：诊断累计与可信输出分离

读取器可以在预算内报告多个独立错误，帮助一次修正更多问题。只要存在阻断错误，本次不产生可信 Endem 或 Synem。

反例：解析发现一个未知关键记录后继续输出“基本可用”的对象。错误恢复不能越过结构接受和内容接受边界。

## 未来采用的证据要求

任何一项 GNU 或 ELF 思想只有同时满足以下条件，才可以提出 ADR：

1. 有真实上游生产者和下游消费者，而不是为了工具链外观对称。
2. 能指出唯一主规范归属，且现有规范无法用引用解决时才考虑新规范。
3. 写出至少一个支持案例、一个同构反例和一项待定内容。
4. 说明输入身份、输出身份、规范化、删除与变换怎样影响确定性。
5. 指定信任边界、失败责任、资源上限和阻断诊断。
6. 形成正反向量；涉及物理编码时还要形成规范字节向量。
7. 证明不依赖名称、搜索顺序、默认版本、环境状态或网络最新值。
8. 若涉及组件行为，项目必须先进入代码开发阶段并明确实现范围。

不满足任何一项时，结论保持为研究资料。项目不因已有 ELF 类比而预先承诺物理 Synem、调试伴随格式、符号表、重定位表、动态链接或装载器。

## 权威资料与采用限制

- [ELF gABI Section Header](https://gabi.xinuos.com/v42/elf/03-sheader.html) 与 [Program Loading](https://gabi.xinuos.com/elf/07-loading-intro.html) 用来核对文件组织和装载视图的区分。它们不定义 Noemion 的语义或权限。
- [GNU ld 2.46 手册](https://sourceware.org/binutils/docs/ld/) 与 [Overview](https://sourceware.org/binutils/docs/ld/Overview.html) 用来核对链接、重定位、符号绑定和带错继续行为。
- [GNU ld Options](https://sourceware.org/binutils/docs/ld/Options.html)、[Linker Scripts](https://sourceware.org/binutils/docs/ld/Scripts.html) 与 [VERSION](https://sourceware.org/binutils/docs/ld/VERSION.html) 用来核对形成映射、Section 回收、隐式脚本和符号版本。
- [GNU readelf](https://www.sourceware.org/binutils/docs/binutils/readelf.html) 用来核对格式专用读取路径独立于 BFD 的边界。
- [GNU BFD](https://sourceware.org/binutils/docs/bfd.html) 用来核对跨格式 canonical form 的价值和信息损失风险。
- [GNU objcopy](https://www.sourceware.org/binutils/docs/binutils/objcopy.html) 与 [GNU strip](https://sourceware.org/binutils/docs/binutils/strip.html) 用来核对裁剪、调试信息分离和派生制品关系。
- [GNU Binutils 项目页](https://sourceware.org/binutils/) 当前列出 2.46.1 为最新发行；在线手册本身标注 2.46。版本差异只影响本次资料基线，不进入 Noemion 规范身份。

## 进入规范前的条件

本提案目前只关闭“怎样借鉴”的研究表达，不关闭以下工程问题：

- Synem 是否需要物理容器、符号视图或绑定表；
- 派生或裁剪是否出现不可替代的真实消费者，以及它是否仍由现有生产动作承担；
- 调试伴随记录是否值得成为正式关系 Profile；
- 版本约束是否需要超出精确内容身份；
- 未来 Theor 的独立实现语言与进程边界。

这些问题继续留在开放问题清单。没有真实消费者与反例证据时，默认不增加对象、格式和组件。
