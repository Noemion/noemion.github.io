---
layout: "manual"
title: "工具参考指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 工具参考指南"
permalink: "/docs/tools-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 5
nav_title: "工具参考指南"
hero_title: "Noemion 工具参考指南"
hero_description: "按对象生命周期查找 23 个规划工具的职责、开发阶段和现有资料。"
summary: "按对象生命周期查找工具职责、开发阶段和相关资料。"
badges: ["23 Tools", "Project Pages", "Unreleased"]
---

## 工具链总览

每个工具入口都是项目说明页，不表示已有可执行程序。命令行接口、参数和文件扩展名尚未冻结。

工具按“规范与对象 → 文本 IR → 编译链接 → 发布运行 → 模型工程”组织。每个工具都说明输入、输出、关键不变量、失败边界、开发依赖和验证目标。不要仅根据工具名称推断命令或格式。完整分类见[工具目录](../tools/)。

### 生命周期矩阵

| Phase | 工具 | 主要输入 | 正式输出 | 直接下游 |
| --- | --- | --- | --- | --- |
| 0 / 8 | [noemcertify](../tools/noemcertify/) | 规范、测试语料库、Toolchain Build | Conformance Report、发布资格证据 | CI、规范评审、发布评审 |
| 1 | [theoria](../tools/theoria/) | NOBJ、HOBJ、Signed Package | Text / Structured View | 开发者、noemvalidate |
| 1 / 5 / 6 | [noemvalidate](../tools/noemvalidate/) | 对象、配置、Trust Material | Layered Verdict、Verified Object Handle | archive、link、bundle、Object System |
| 1 | [noemtransform](../tools/noemtransform/) | Source Object、Transform Plan | Transformed Object、Change Manifest | compare、validate、reduce |
| 1 / 5 / 6 | [noembudget](../tools/noembudget/) | 对象、包、Baseline | Budget Verdict、Delta Report | CI、Package 配置、Execution Profile |
| 2 | [morphe](../tools/morphe/) | Text NIR Source Package | Relocatable NOBJ、Assembly Evidence Ledger | decode、coverage、link |
| 2 | [noemdecode](../tools/noemdecode/) | NOBJ / HOBJ | Canonical Text NIR、Pretty / JSON View | assemble、compare、开发者 |
| 2 / 3 | [noemformat](../tools/noemformat/) | NSL / Text NIR | Formatted Text、Format Diff | compile、assemble、CI |
| 2 / 5 | [noemcompare](../tools/noemcompare/) | 两个文本或对象产物 | Classified Diff、Semantic Verdict | reduce、validate、发布审计 |
| 3 / 7 | [noesis](../tools/noesis/) | NSL 或 Candidate Envelope、绑定决定 | Relocatable NOBJ、证据账本、Build Manifest | analyze、archive、link、coverage |
| 3 | [noemanalyze](../tools/noemanalyze/) | NSL / Text NIR、Reviewed Baseline | Diagnostics、Baseline Candidate | 开发者、CI、compile |
| 4 | [noemarchive](../tools/noemarchive/) | 已验证 NOBJ Members | Noemion Archive、Member Listing | symbols、link |
| 4 | [noemsymbols](../tools/noemsymbols/) | NOBJ、Archive、HOBJ、Package | Symbol Listing、ABI Snapshot | link、compare、开发者 |
| 4 / 5 | [synthesis](../tools/synthesis/) | NOBJ、Archive、HOBJ、Link Request | Linked Object / HOBJ、Link Map | validate、reduce |
| 5 | [noemreduce](../tools/noemreduce/) | Development NOBJ / HOBJ | Release Object、Debug Companion、等价证据 | coverage、validate、bundle |
| 5 / 6 | [noemcoverage](../tools/noemcoverage/) | 来源/对象映射或 Run Evidence | Release Coverage Proof / Evidence Closure Report | bundle / execute finalize |
| 5 | [noembundle](../tools/noembundle/) | Release 闭包、模型资格、外部签名响应 | Signed Noemion Package | noemexecute、下载发布 |
| 6 | [noemexecute](../tools/noemexecute/) | Signed Package、Execution Profile | Run Evidence、Run Result、Acceptance Decision | observe、coverage、evaluate |
| 6 | [noemobserve](../tools/noemobserve/) | Trace Stream、Integrity Metadata | Normalized Trace、Trace Integrity Report | coverage、evaluate |
| 7 | [noemdataset](../tools/noemdataset/) | Source Registry、Annotation Package | Dataset Snapshot、Lineage、Leakage Report | train、evaluate |
| 7 | [noemtrain](../tools/noemtrain/) | 数据快照、配方、Base Model | Checkpoint Candidate、Training Manifest | noemevaluate |
| 7 / 8 | [noemevaluate](../tools/noemevaluate/) | 模型候选或 Final Run Evidence | Model Qualification / Scenario Evaluation | quantize、bundle、回归评审 |
| 7 | [noemquantize](../tools/noemquantize/) | 合格 Checkpoint Candidate | Model Package Candidate、量化与设备报告 | noemevaluate、noembundle |

全部入口当前都是设计阶段。Phase 只表示预计开发顺序，不表示对应工具已经实现。

## 规范与对象工具

- [noemcertify](../tools/noemcertify/)：执行规范条款、基准样例、畸形样例和跨工具一致性测试。
- [theoria](../tools/theoria/)：只读查看 Header、Section、符号、重定位和语义图。
- [noemvalidate](../tools/noemvalidate/)：分层验证结构、语义、覆盖、策略和信任链。
- [noemtransform](../tools/noemtransform/)：受约束地复制、抽取、删除和重建对象内容。
- [noembudget](../tools/noembudget/)：分析 Section、Segment、闭包和披露预算占用。

## 编译与链接

- [morphe](../tools/morphe/)：将规范文本 NIR 确定性汇编为对象。
- [noemdecode](../tools/noemdecode/)：将对象反汇编为规范文本表示。
- [noemformat](../tools/noemformat/)：规范化 NSL 与文本 NIR 的表现形式。
- [noemcompare](../tools/noemcompare/)：区分布局、调试、信任元数据和运行语义差异。
- [noesis](../tools/noesis/)：驱动前端并由确定性 Noesis Core 生成 NIR/NOBJ。
- [noemanalyze](../tools/noemanalyze/)：检查语义、覆盖和策略问题，不生成对象。
- [noemarchive](../tools/noemarchive/)：建立确定性对象归档和符号索引。
- [noemsymbols](../tools/noemsymbols/)：检查符号定义、引用、版本和可见性。
- [synthesis](../tools/synthesis/)：解析符号、应用重定位、合并依赖闭包并输出链接对象或 HOBJ。

## 发布与运行

- [noemreduce](../tools/noemreduce/)：分离开发调试信息并证明发布语义不变。
- [noemcoverage](../tools/noemcoverage/)：分别建立 Release Coverage Proof 与 Run Evidence Closure。
- [noembundle](../tools/noembundle/)：冻结发布闭包，生成签名请求，并核对外部签名响应后封装最终包。
- [noemexecute](../tools/noemexecute/)：验证签名包，驱动 Harness / Runtime 循环，并在证据闭合后形成 Acceptance Decision。
- [noemobserve](../tools/noemobserve/)：规范化运行事件，并报告 Trace 完整性、事件丢失与证据强度。

## 模型工程

**后续计划：**以下工具只在确定性核心稳定后进入实施，模型输出始终视为不可信。

- [noemdataset](../tools/noemdataset/)：构造有许可、有血缘、无泄漏的数据集快照。
- [noemtrain](../tools/noemtrain/)：编排 Horizon Engine 适配、多任务训练和教师蒸馏。
- [noemevaluate](../tools/noemevaluate/)：先为浮点 Checkpoint Candidate 建立量化资格，量化后重新评估 Model Package Candidate；另在 Acceptance Decision 之后离线评估 Agent 场景。
- [noemquantize](../tools/noemquantize/)：只导出、量化并测量未签名 Model Package Candidate，质量资格仍由 noemevaluate 形成。

## 相关资料状态

**当前范围：**四个承担格式边界的工具已经建立独立使用手册：[noesis 使用手册](../tools/noesis/docs/)解释自然语言候选、来源绑定、NIR 记录和 NOBJ 生成；[morphe 使用手册](../tools/morphe/docs/)解释 Text NIR、对象排布、确定性编码和往返验证；[theoria 使用手册](../tools/theoria/docs/)解释 Header、Section、NIR 来源视图和安全读取；[synthesis 使用手册](../tools/synthesis/docs/)解释对象准入、符号、重定位、依赖闭包与链接安全。其他工具目前提供用途、输入输出、处理边界和开发计划，尚无独立使用手册。

工具只有在契约、流程、安全、测试或参考内容能够独立维护，并且不会重复权威规范时，才建立自己的 `docs/` 区域。文档数量不代表实现成熟度；是否可用仍以发布物、版本说明和验证证据为准。

**待定事项：**各工具的 CLI、扩展名和稳定输入输出结构尚未冻结。Phase 0–8、主产物顺序和验证责任已经作为当前架构边界采用，但具体研究方法、阈值与发布授权流程仍需规范、ADR 和真实证据。
