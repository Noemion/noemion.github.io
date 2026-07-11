---
layout: "manual"
title: "命令行调用 · noemld 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemld documentation"
permalink: "/tools/noemld/docs/invocation.html"
manual_id: "noemld"
manual_group: "start"
manual_order: 3
nav_title: "命令行调用"
hero_title: "命令行调用"
hero_description: "调用形式与尚未冻结的参数边界"
summary: "调用形式与尚未冻结的参数边界"
badges: ["noemld", "Phase 4 / Phase 5"]
---

## 调用模型

CLI 只是链接契约的一种前端。无论未来由命令行、构建系统还是库接口调用，都必须解析为同一个显式 Link Request：有序输入声明、内容身份、Link Profile、Dependency Lock、输出意图和诊断策略。环境变量、当前目录或网络状态不得暗中改变 Strict 模式结果。

| 意图 | 语义 | 必要输出 |
| --- | --- | --- |
| 最终链接 | 形成供 Loader 验证的封闭产物候选。 | Linked Object、Link Map、验证摘要。 |
| 共享 SSO | 保留规范允许的导入导出和披露边界。 | SSO、导出表、依赖闭包。 |
| 可重定位合并 | 合并局部对象但保留后续链接需要的类型化引用。 | 可重定位 GOBJ、ID 映射和剩余引用。 |
| 只检查 | 执行验证与解析计划，不提交链接产物。 | 诊断、候选 Link Map，不可装载标记。 |

## 候选调用示例

```text
noemld main.gobj libdomain.noema -o task.noemx
noemld -shared skill/*.gobj --lock deps.lock -o skill.dev.sso
noemld -r part-a.gobj part-b.gobj -o combined.gobj
```

> 最终参数名、扩展名和组合规则必须由 CLI 规范 ADR 冻结；这里仅记录能力边界。

## 结果与退出语义

CLI 规范应为“成功”“输入或契约错误”“安全验证失败”“资源上限”“内部故障”定义稳定类别，并允许构建系统通过机器可读诊断区分。退出码只表达顶层类别，精确原因由结构化诊断承载；人类可读文本可以改进措辞，但不得成为自动化依赖的唯一接口。

- 成功必须意味着产物已经完整提交并通过链接后自检。
- 失败不得覆盖既有有效输出；临时文件须原子清理或明确隔离。
- 响应文件、通配展开和路径解析若被支持，必须规定编码、排序、重复项和递归上限。
- 敏感路径、密钥和受限元数据不得因详细诊断默认泄漏。

## 可复现调用记录

每次正式构建应能导出已规范化的 Link Request，包含工具与规范版本、输入摘要、解析后的 Profile、锁文件摘要和输出摘要。论文实验或一致性测试应保存该记录，而不是只保存一段可能依赖本机环境的 shell 命令。
