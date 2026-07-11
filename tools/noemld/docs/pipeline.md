---
layout: "manual"
title: "处理流程 · noemld 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemld documentation"
permalink: "/tools/noemld/docs/pipeline.html"
manual_id: "noemld"
manual_group: "linking"
manual_order: 4
nav_title: "处理流程"
hero_title: "处理流程"
hero_description: "从输入验证到完整链接对象的确定性流程"
summary: "从输入验证到完整链接对象的确定性流程"
badges: ["noemld", "Phase 4 / Phase 5"]
---

## 流程设计原则

链接采用“验证—规划—提交”事务模型。前置阶段只读取和建立不可变中间表示；所有会影响最终对象的选择都写入 Link Plan；只有全局验证通过后才序列化并原子提交产物。这样可以使失败可回滚、决策可审计，并避免半成品进入下游。

## 端到端流程

1. **准入验证：**验证输入结构、版本、目标 ABI、Profile、锁文件和资源预算。
2. **索引扫描：**扫描显式对象与归档索引，构建候选全局符号表；见 [符号解析](symbol-resolution.html)。
3. **定义选择：**按可见性、版本、强弱规则和兼容类型选择定义，记录选择理由。
4. **闭包扩展：**以稳定次序拉入所需归档成员并计算强依赖闭包，直到不动点。
5. **结构合并：**规划兼容 Section、字符串、GSIR 图和 Contract 的目标位置。
6. **ID 与引用修正：**建立双向映射并应用类型化重定位；见 [重定位](relocations.html)。
7. **语义合并：**按类型代数合并约束、权限与披露图；见 [SSO 链接](sso-linking.html)。
8. **布局与封存：**构建 Segment、哈希和 Link Map，执行独立验证后原子提交；见 [装载与安全](loader-security.html)。

## 阶段检查点

| 检查点 | 必须成立 | 可保存证据 |
| --- | --- | --- |
| 输入冻结 | 所有内容身份、Profile 和上限确定。 | Input Manifest、规范化 Link Request。 |
| 解析闭包 | 强引用已解析，归档选择达到不动点。 | 符号选择表、成员拉入理由。 |
| 合并计划 | Section、ID、重定位、权限和约束无冲突。 | 未提交的 Link Plan。 |
| 产物提交 | 序列化对象通过全量结构与语义自检。 | Linked Object、Link Map、验证摘要。 |

## 确定性与复杂度约束

- 哈希表或并发执行的迭代顺序不得影响选择结果；所有集合输出采用规范稳定序。
- 归档闭包、图合并和冲突聚合必须有 Profile 限定的工作量、深度和诊断数量上限。
- 缓存只能复用绑定相同输入摘要、规范版本和 Profile 的中间结果，缓存命中与否不得改变输出。
- 任一阶段发现不一致时终止提交；不得尝试用模型、随机规则或最后写入者恢复。

算法、排序键与复杂度目标仍需在规范或 ADR 中冻结，并用输入排列、并发度和缓存状态变化测试证明结果不变。
