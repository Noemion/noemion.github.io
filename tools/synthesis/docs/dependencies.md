---
layout: "manual"
title: "上下游依赖 · synthesis 使用手册 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · synthesis 使用手册"
permalink: "/tools/synthesis/docs/dependencies.html"
manual_id: "synthesis"
manual_group: "reference"
manual_order: 12
nav_title: "上下游依赖"
hero_title: "上下游依赖"
hero_description: "说明 synthesis 从哪些工具接收输入，以及输出交给哪些工具。"
summary: "说明 synthesis 从哪些工具接收输入，以及输出交给哪些工具。"
badges: ["synthesis", "Phase 4 / Phase 5"]
---

## 依赖边界

`synthesis` 处在对象生产、归档、验证、裁剪、打包和装载之间。工具名称上的相邻关系不构成契约；每条边都必须说明对象类型、版本、内容身份、失败责任和权威规范。Deterministic 链接不得通过隐式网络访问补齐依赖。

## 上游

- [noesis](../../noesis/index.html) 产生待链接 NOBJ；其输出必须先满足格式与目标配置。
- [noemarchive](../../noemarchive/index.html) 提供内容可寻址归档与可验证成员索引。
- [noemsymbols](../../noemsymbols/index.html) 读取同一符号模型，用于人工检查但不替代链接器解析。
- [noemvalidate](../../noemvalidate/index.html) 在链接前后执行独立对象验证。

## 下游

- [noemreduce](../../noemreduce/index.html) 对链接对象执行允许的发布裁剪并产生调试伴随文件。
- [noemcoverage](../../noemcoverage/index.html) 为最终 Release Object、来源与运行证据建立覆盖证明。
- [noembundle](../../noembundle/index.html) 绑定验证结论、依赖锁定和覆盖证明，经过外部签名回填后形成 Signed Noemion Package。
- [noemexecute](../../noemexecute/index.html) 消费签名包，依次驱动 Noema Object System、Agent Harness 与 Fulfillment Runtime；它不直接执行裸链接产物。

## 依赖锁定契约

| 信息 | 目的 | 失败边界 |
| --- | --- | --- |
| 内容摘要与对象种类 | 避免同名替换，确保解析到预期字节和解释。 | 摘要不符或种类不符立即失败。 |
| 版本与配置 | 约束格式、ABI、导出接口和兼容范围。 | 未知必需版本或不兼容配置失败。 |
| 来源与信任声明 | 支持供应链审计，不把来源信任误当结构信任。 | 策略要求但信息缺失时失败。 |
| 强弱与可选性 | 区分必须闭合的依赖和有明确缺失语义的依赖。 | 强依赖缺失失败；可选依赖按规范记录。 |

## 依赖图规则

- 按内容身份去重，路径、镜像地址和文件名只作为来源元数据。
- 强依赖必须形成完整锁定闭包；弱依赖缺失的运行语义必须由配置明确。
- 循环依赖只有在相关对象种类和初始化语义明确允许时才可接受，否则生成包含完整环路的诊断。
- 上游结构定义或规范版本变化必须触发重新验证，不通过旧缓存静默沿用。

每个链接映射应记录实际消费的依赖子图、未使用锁条目和选择理由，便于构建复现、供应链审计和影响分析。

## 跨工具验收

发布前应建立最小封闭流水线：编译对象、建立归档、符号检查、链接、独立验证、语义保持裁剪、覆盖证明、外部签名回填、受控装载与运行证据。任一工具对共同字段的解释不一致，都应回到规范解决，而不是加入转换兼容层。

运行证据继续沿 `noemexecute → noemobserve → noemcoverage(run) → noemexecute finalize` 形成 Acceptance Decision；noemevaluate 只在此后做离线场景评估。该尾链不是 synthesis 的直接消费者，但用于证明链接产物进入完整系统后仍能保持身份与契约。
