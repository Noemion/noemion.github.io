---
layout: "manual"
title: "工具参考 · Noemion 文档"
page_role: "content"
footer_text: "Noemion · 工具参考"
permalink: "/docs/tools-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 5
nav_title: "工具参考"
hero_title: "Noemion 工具参考"
hero_description: "按对象生命周期整理 23 个工具的职责、阶段和现有文档状态。"
summary: "按对象生命周期整理 23 个工具的职责、阶段和现有文档状态。"
badges: ["23 Tools", "Project Pages", "Unreleased"]
---

## 工具链总览

每个工具入口都是项目说明页，不表示已有可执行程序。命令行接口、参数和文件扩展名尚未冻结。

工具按“规范与对象 → 文本 IR → 编译链接 → 发布运行 → 模型工程”组织。每个工具都说明输入、输出、关键不变量、失败边界、开发依赖和验证目标。不要仅根据工具名称推断命令或格式。完整分类见[工具目录](../tools/)。

## 规范与对象工具

- [noemcertify](../tools/noemcertify/)：执行规范条款、基准样例、畸形样例和跨工具一致性测试。
- [noeminspect](../tools/noeminspect/)：只读查看 Header、Section、符号、重定位和语义图。
- [noemvalidate](../tools/noemvalidate/)：分层验证结构、语义、覆盖、策略和信任链。
- [noemtransform](../tools/noemtransform/)：受约束地复制、抽取、删除和重建对象内容。
- [noembudget](../tools/noembudget/)：分析 Section、Segment、闭包和披露预算占用。

## 编译与链接

- [noemassemble](../tools/noemassemble/)：将规范文本 NIR 确定性汇编为对象。
- [noemdecode](../tools/noemdecode/)：将对象反汇编为规范文本表示。
- [noemformat](../tools/noemformat/)：规范化 NSL 与文本 NIR 的表现形式。
- [noemcompare](../tools/noemcompare/)：区分布局、调试、信任元数据和运行语义差异。
- [noemcompile](../tools/noemcompile/)：驱动前端并由确定性 Noesis Core 生成 NIR/NOBJ。
- [noemanalyze](../tools/noemanalyze/)：检查语义、覆盖和策略问题，不生成对象。
- [noemarchive](../tools/noemarchive/)：建立确定性对象归档和符号索引。
- [noemsymbols](../tools/noemsymbols/)：检查符号定义、引用、版本和可见性。
- [noemlink](../tools/noemlink/)：解析符号、应用重定位、合并依赖闭包并输出链接对象或 HOBJ。

## 发布与运行

- [noemreduce](../tools/noemreduce/)：分离开发调试信息并证明发布语义不变。
- [noemcoverage](../tools/noemcoverage/)：审计来源单元覆盖和发布闭包完整性。
- [noembundle](../tools/noembundle/)：组装签名对象、依赖、策略与模型指纹。
- [noemexecute](../tools/noemexecute/)：可信验证、装载、渐进式披露与 Fulfillment Runtime 执行。
- [noemobserve](../tools/noemobserve/)：关联运行事件、调试伴随文件和源级因果链。

## 模型工程

**后续计划：**以下工具只在确定性核心稳定后进入实施，模型输出始终视为不可信。

- [noemdataset](../tools/noemdataset/)：构造有许可、有血缘、无泄漏的数据集快照。
- [noemtrain](../tools/noemtrain/)：编排 Horizon Engine 适配、多任务训练和教师蒸馏。
- [noemevaluate](../tools/noemevaluate/)：评估错误确定、校准、OOD、切片和部署退化。
- [noemquantize](../tools/noemquantize/)：导出、量化、端侧基准并封装模型包。

## 文档状态

**当前范围：**[noemlink 文档](../tools/noemlink/docs/)已经按契约、输入输出、调用、流程、符号、重定位、HOBJ、安全、诊断、测试、依赖和术语索引拆分。其他工具目前提供用途、输入输出、处理边界和开发计划，尚无独立操作手册。

工具只有在契约、流程、安全、测试或参考内容能够独立维护，并且不会重复权威规范时，才建立自己的 `docs/` 区域。文档数量不代表实现成熟度；是否可用仍以发布物、版本说明和验证证据为准。

**尚待确定：**各工具的 CLI、扩展名、稳定输入输出结构、研究验证方法和发布顺序尚未确定。
