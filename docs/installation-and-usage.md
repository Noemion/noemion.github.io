---
layout: "manual"
title: "使用与获取 · Noemion 文档"
page_role: "content"
footer_text: "Noemion · 使用与获取"
permalink: "/docs/installation-and-usage.html"
manual_id: "docs"
manual_group: "start"
manual_order: 2
nav_title: "使用与获取"
hero_title: "使用与获取"
hero_description: "说明当前可获取资源、未来工具链使用流程和发布完整性要求。"
summary: "说明当前可获取资源、未来工具链使用流程和发布完整性要求。"
badges: ["Unreleased", "Usage Model", "Integrity First"]
---

## 当前可用性

> 当前没有正式版本、二进制安装包或可执行工具。现有工具名用于划分预期职责，不能作为命令执行，也不承诺 CLI、参数或文件扩展名。

资源状态以[下载与资源](../downloads/)为准。正式制品发布后，安装入口必须同时说明版本、平台、校验值、签名和支持范围。

## 计划中的使用流程

工具链成熟后预计采用以下数据流。具体命令、参数、扩展名和 ABI 尚未确定。

整体流程为 Author → Compile → Inspect / Validate → Link → Reduce / Coverage → Bundle / Sign → Execute / Observe → Run Coverage → Execute Finalize → Offline Evaluate。

1. 用受规范约束的来源形式描述目标、约束和验收条件，并记录来源与配置。
2. 由确定性 Noesis Core 生成 NIR 和 NOBJ，同时产生诊断和覆盖证据。
3. 使用对象查看与验证工具检查结构、语义、策略和未决项。
4. 由链接器解析符号、重定位和依赖闭包，生成链接对象、HOBJ、链接映射或冲突报告。
5. 对最终发布对象建立 Release Coverage Proof 和分层验证结论，再由 noembundle 冻结依赖、模型、策略、Manifest 与 SBOM。
6. noembundle 先生成不可变 Unsigned Package Candidate 与 Signing Request；外部签名系统保护私钥并返回 Signature Response；回填阶段必须同时核对候选、请求和响应，才在被签载荷外附加 Signature Envelope 并形成 Signed Noemion Package。
7. noemexecute 重新验证实际包字节，建立 Loaded State 与 Agent Harness 会话，再驱动 Fulfillment Runtime 产生不可信候选、Candidate Assessment 和 Capability Request。
8. noemobserve 形成带完整性声明的 Normalized Trace，noemcoverage 建立 Evidence Closure Report，noemexecute finalize 按预置策略形成 Acceptance Decision；noemevaluate 只在此后离线评估模型资格或端到端场景。

## 输入与产物边界

| 阶段 | 输入 | 产物 | 状态 |
| --- | --- | --- | --- |
| 语义编译 | 规范源、配置、显式上下文 | NIR/NOBJ | 架构已定义，实现未发布 |
| 链接 | NOBJ、归档、锁定依赖 | 链接对象、HOBJ、链接映射 | 契约与流程已有专题说明，实现未发布 |
| 发布 | Release Object、Release Coverage Proof、验证结论、锁定依赖 | Unsigned Package Candidate、Signing Request、Signed Noemion Package | 后续计划 |
| 运行 | Signed Noemion Package、Execution Profile、Runtime Binding | Loaded State、Run Record、Run Report、Trace Stream | 后续计划 |
| 证据与验收 | Run Record、Normalized Trace、Acceptance Policy | Evidence Closure Report、Acceptance Decision | 后续计划 |
| 离线评估 | Checkpoint 或已完成运行的证据与决定 | Model Qualification Record、场景评估结论 | 后续计划 |

## 安装与发布原则

- 正式资源必须提供版本、目标平台或格式、大小、发布日期、校验值和签名信息。
- 安装指南只引用真实存在的制品和仓库，不使用占位 URL。
- 开发快照与正式版本必须明确区分，不能共享含糊的“最新版”入口。
- 依赖必须内容寻址、版本锁定并带有可验证来源。
- 候选版本公开前，需要完成可复现构建、安全测试、许可证核对、SBOM 和互操作验证。

## 安全检查

- 下载后先验证校验值和签名，再解析对象。
- 对象读取器在分配或切片前验证偏移、长度、计数和对齐。
- 验证通过不等于获得无限权限；装载器仍需检查策略、能力和 Segment 属性。
- 模型不得决定二进制布局、签名范围或装载权限。

测试策略见[测试、模糊测试与验证](../development/testing.html)。

## 尚待确定的发布接口

**尚待确定：**首批支持平台、分发格式、包管理集成、源码托管位置、命令行语法和对象扩展名尚未决定。相关决定必须在实际发布前通过规范或 ADR 固化。

发布决策还需要回答支持周期、漏洞响应、密钥轮换、撤回与回滚、许可证组合、长期归档和研究制品引用方式；没有这些生命周期安排时不能把一次构建描述为稳定发行。
