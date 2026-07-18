---
layout: architecture-decision
title: ADR-0012 · 未来 deterministic producer 的 Rust 评审基线
page_role: content
footer_text: Noemion · ADR-0012
permalink: "/architecture/adr-0012-rust-core-language.html"
summary: 说明为什么 Rust 1.97.0 只是未来结构核心的评审起点，而不是已经实现的组件或独立检查器语言决定。
decision_id: ADR-0012
page_heading: ADR-0012 · 未来 deterministic producer · Rust 评审基线
page_lead: 历史字节实验支持把 Rust 1.97.0 作为未来 deterministic producer 首个结构核心的重新评审起点；它没有建立生产组件，也没有替independent
  inspector 决定语言。
badges:
- 当前策略
- Rust 1.97.0
- 历史实验
- 尚未进入代码阶段
previous_url: adr-0011-endem-container.html
previous_label: ADR-0011
next_url: adr-0013-end-p1-payload.html
next_label: ADR-0013
---

## 先分清已经决定与尚未决定

ADR-0012 记录一项有前提的实现策略：只有项目另行进入代码阶段时，未来 deterministic producer 的首个结构核心才从 Rust 1.97.0 开始复核。

| 层次 | 当前结论 | 不能据此声称 |
| --- | --- | --- |
| 历史实验 | C17 与安全 Rust 读取同一组 END-P0 结构字节，并保留可复核结果。 | 实验原型已经实现 END-P2、deterministic producer、independent inspector 或正式 CLI。 |
| 未来 deterministic producer | `ktise` 与制品形成侧 `elenk` 的结构核心以 Rust 1.97.0 为评审起点。 | 已经存在生产工具链、源码仓库、稳定 ABI 或发行承诺。 |
| independent inspector | 必须另写解析结构和错误路径，并建立独立验证目标；实现语言继续待定。 | 同样使用 Rust 就自然获得实现独立性。 |
| 其他边界 | 协议适配器、界面、外部工具和未来运行系统按各自消费者重新选择语言。 | Noemion 全部软件只能使用 Rust。 |

`deterministic producer` 是已经按普通词规则接受的设计职责，不是已发布组件或命令。历史自造词 `ktise` 与 `elenk` 已被替换；语言选择既不能恢复旧名称，也不能替代未来自造名称的读音与口头区分验证。

## 历史实验实际回答了什么

| 检查 | 观察结果 | 声明上限 |
| --- | --- | --- |
| 6 个 END-P0 结构向量 | C 与 Rust 得到相同的接受或首错结果。 | 只覆盖固定前导、目录、范围、对齐、记录基数和空映射。 |
| 144 个确定性变异 | 两个原型给出相同首错类别，没有崩溃。 | 不代表错误优先级、CBOR 或 END-CORE 已被穷举。 |
| C 动态检查 | 当前语料通过 AddressSanitizer 与 UndefinedBehaviorSanitizer；Linux 完成 10,000 次 libFuzzer 运行。 | 有限语料和有限轮次不能证明没有内存缺陷。 |
| 同机重复构建 | 相同源码、工具链和主机生成相同二进制摘要。 | 不等于跨系统复现，也不证明供应链完整。 |
| 源码与二进制尺寸 | 记录了两个小型原型的非空行数、文件大小和动态依赖。 | 尺寸受工具链、目标、符号和裁剪方式影响，不单独决定语言。 |

开发者可以复核[实验协议与源码](https://github.com/Noemion/noemion.github.io/tree/main/experiments/p0-language)、[机器可读结果](https://github.com/Noemion/noemion.github.io/blob/main/experiments/p0-language/results.json)和[Linux 实验记录](https://github.com/Noemion/noemion.github.io/actions/runs/29205071270)。

> **证据边界：**这些原型不是生产实现，也不产生规范 Endem。它们只比较当前结构切片的失败行为。

## 为什么只把 Rust 作为 deterministic producer 起点

deterministic producer 掌握唯一规范写入路径，因此首个读取与写入核心应先缩小内存破坏面。independent inspector 承担独立读取，价值来自不同代码和错误路径，而不是共享实现后再运行一次。

1. 受控来源
2. deterministic producerktise 形成
3. deterministic producerelenk 检查
4. END-P2 字节
5. independent inspector独立读取
6. 外部判断

| 责任方 | 语言结论 | 必须保持的隔离 |
| --- | --- | --- |
| deterministic producer 结构核心 | 以安全 Rust 作为未来评审起点。 | 写入、回读、受检算术和失败原子性仍须由规范与测试约束。 |
| independent inspector | 语言尚未决定。 | 不得复用 deterministic producer 的解析代码、生成代码或错误分类实现。 |
| C 历史原型 | 只保留为非生产差分材料。 | 不得链接进 deterministic producer、independent inspector 或 CLI，也不获得发行权限。 |
| 协议与运行侧 | 由真实消费者和部署边界另行决定。 | 不能因为 deterministic producer 使用 Rust，就继承其信任或满足结论。 |

## 安全 Rust 仍然不能证明什么

| 机制 | 能够降低的风险 | 仍需显式处理 |
| --- | --- | --- |
| 所有权与借用检查 | 安全代码不能任意解引用裸指针或制造悬空引用。 | 逻辑错误、资源耗尽、错误语义和确定性不会自动正确。 |
| `#![forbid(unsafe_code)]` | 拒绝被该 lint 覆盖的项目代码直接使用 unsafe 构造。 | 标准库、工具链和未来依赖不因此变成无 unsafe 的整体。 |
| 切片边界检查 | 越界访问不会成为未定义内存访问。 | 索引仍可 panic；不可信字节路径必须使用可失败访问并返回诊断。 |
| `checked_add` 与 `checked_mul` | 把整数溢出变成可处理的失败。 | 每条偏移、长度、计数、对齐和累计分配路径都要实际使用。 |
| 发行构建溢出检查 | 为遗漏的普通整数运算增加失败保护。 | Cargo 的 release 默认关闭该检查，必须显式设置；它也不能代替受检算术。 |

[Rust 所有权说明](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)支持内存管理边界，[Rustonomicon 的 panic 说明](https://doc.rust-lang.org/nomicon/exception-safety.html)则明确越界索引等安全代码仍可终止当前路径。项目采用这两项机制，但不把“安全 Rust”写成“解析器安全”。

[Cargo 工作区 lint](https://doc.rust-lang.org/stable/cargo/reference/workspaces.html#the-lints-table)需要成员显式继承；[Cargo profile](https://doc.rust-lang.org/cargo/reference/profiles.html)也显示 release 默认关闭 `overflow-checks`。因此这两项都必须成为可检查配置，而不是口头约定。

## 进入代码阶段前怎样重新评审

[Rust 1.97.0](https://blog.rust-lang.org/releases/1.97.0/)于 2026 年 7 月 9 日成为 stable，这使历史实验使用了当时的稳定版本。版本新旧本身不构成安全结论。

| 检查顺序 | 进入下一步前必须满足 | 失败时怎样处理 |
| --- | --- | --- |
| 1 · 阶段与范围 | 用户另行确认代码阶段、目标仓库、组件和消费者。 | 继续停留在规范、威胁与验证方案，不创建实现仓库。 |
| 2 · 工具链 | 重新核对 1.97.0、目标平台、已知安全问题和最低支持版本。 | 版本已不合适时先更新 ADR 和实验，不静默使用 latest。 |
| 3 · 依赖与配置 | 固定工具链，提交 `Cargo.lock`，CI 使用 `--locked`；工作区成员继承 unsafe 禁止。 | 锁文件缺失、解析变化或 lint 未覆盖时构建失败。 |
| 4 · 不可信输入 | 所有范围和算术可失败，无 panic 路径，并执行资源上限与稳定诊断。 | 任一畸形输入只能得到原子拒绝，不能输出部分可信对象。 |
| 5 · 独立证据 | deterministic producer 与 independent inspector 分别通过 END-P2 向量、畸形语料、模糊目标和跨平台检查。 | 共同成功不能掩盖共享假设；需要增加异构预言机或重新选语言。 |

[Cargo `--locked`](https://doc.rust-lang.org/cargo/commands/cargo.html#manifest-options) 会在锁文件缺失或依赖解析变化时失败；仅提交 `Cargo.lock` 不会自动建立这项保证。离线构建、源码供应与可执行文件复现仍是另外的验证问题。

[GNU GCC 插桩](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)与[LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html)继续提供 C 差分和畸形输入验证机制。它们只能增加观测证据，不能证明缺陷不存在。

## 什么情况会改变这一基线

| 触发条件 | 需要重新比较什么 |
| --- | --- |
| Rust 无法覆盖真实目标平台、审计或部署边界 | 用同一规范、语料、资源上限和失败分类比较 C 或其他候选语言。 |
| 无第三方 crate 无法满足确定性 CBOR 或平台要求 | 先证明依赖的必要消费者、维护状态、许可证、供应链和删除条件。 |
| independent inspector 的独立性审计发现共同编译器或库假设过强 | 评估不同语言、不同解析结构或更强的外部测试预言机。 |
| 未来实现无法保持无 panic、受检算术或稳定拒绝 | 不得降低 END-FMT 与 END-CORE；重新打开语言和组件边界。 |

> **当前限制：**项目尚未进入代码阶段。这里没有 deterministic producer、independent inspector、CLI、稳定命令、构建配置或实现级符合性结论。

- [先看字节读取边界](adr-0011-endem-container.html) — 区分格式、Profile、内容与外部判断。
- [继续看 END-P2](adr-0013-end-p1-payload.html) — 了解未来结构核心实际需要读取的字段与引用。
- [查看实现路线](../development/implementation-roadmap.html) — 确认何种证据允许项目进入下一层。
- [查看验证职责](../development/testing.html) — 区分格式符合性、安全性质、互操作和研究实验。
