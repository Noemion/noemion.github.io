---
layout: "manual"
title: "命令行调用 · noemlink 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemlink documentation"
permalink: "/tools/noemlink/docs/invocation.html"
manual_id: "noemlink"
manual_group: "start"
manual_order: 3
nav_title: "命令行调用"
hero_title: "命令行调用"
hero_description: "说明命令行调用模型，并标出尚未确定的参数和退出语义。"
summary: "说明命令行调用模型，并标出尚未确定的参数和退出语义。"
badges: ["noemlink", "Phase 4 / Phase 5"]
---

## 调用模型

CLI 只是链接契约的一种前端。无论未来由命令行、构建系统还是库接口调用，都必须解析为同一个显式 Link Request：声明输入序列、规范化内容身份、Link 配置、依赖锁定、输出意图和诊断策略。输入序列用于记录显式优先级，顺序无关集合摘要用于证明无关排列不改变结果；环境变量、当前目录或网络状态不得暗中改变 Deterministic Profile 结果。

| 意图 | 语义 | 必要输出 |
| --- | --- | --- |
| 最终链接 | 形成供 noemvalidate 独立验证的封闭产物候选。 | Linked Object、链接映射、内部自检摘要。 |
| 共享 HOBJ | 保留规范允许的导入导出和披露边界。 | HOBJ、导出表、依赖闭包。 |
| 可重定位合并 | 合并局部对象但保留后续链接需要的类型化引用。 | 可重定位 NOBJ、ID 映射和剩余引用。 |
| 只检查 | 执行验证与解析计划，不提交链接产物。 | 诊断、候选链接映射，不可装载标记。 |

## 候选调用示例

```text
noemlink [MAIN_OBJECT] [DOMAIN_ARCHIVE] --output [LINKED_OBJECT]
noemlink --shared [INPUT_OBJECTS] --lock [DEPENDENCY_LOCK] --output [HORIZON_OBJECT]
noemlink --relocatable [PARTIAL_OBJECTS] --output [COMBINED_OBJECT]
```

> 上述方括号内容表示语义占位符，不是文件名或扩展名。最终参数、扩展名和组合规则必须由 CLI 规范 ADR 冻结。

## 结果与退出语义

CLI 规范应为“成功”“输入或契约错误”“安全验证失败”“资源上限”“内部故障”定义稳定类别，并允许构建系统通过机器可读诊断区分。退出码只表达顶层类别，精确原因由结构化诊断承载；人类可读文本可以改进措辞，但不得成为自动化依赖的唯一接口。

- 成功必须意味着产物已经完整提交并通过链接后自检。
- 失败不得覆盖既有有效输出；临时文件须原子清理或明确隔离。
- 响应文件、通配展开和路径解析若被支持，必须规定编码、排序、重复项和递归上限。
- 敏感路径、密钥和受限元数据不得因详细诊断默认泄漏。

## 可复现调用记录

每次正式构建应能导出已规范化的链接请求，包含工具与规范版本、输入摘要、解析后的配置、锁文件摘要和输出摘要。论文实验或一致性测试应保存该记录，而不是只保存一段可能依赖本机环境的 shell 命令。
