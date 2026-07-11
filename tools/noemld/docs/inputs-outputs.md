---
layout: "manual"
title: "输入与输出 · noemld 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemld documentation"
permalink: "/tools/noemld/docs/inputs-outputs.html"
manual_id: "noemld"
manual_group: "start"
manual_order: 2
nav_title: "输入与输出"
hero_title: "输入与输出"
hero_description: "链接输入、Profile、Lock 与产物契约"
summary: "链接输入、Profile、Lock 与产物契约"
badges: ["noemld", "Phase 4 / Phase 5"]
---

## 输入信任模型

每个对象、归档、锁文件和链接脚本都按不可信输入处理。来源可信或签名有效只说明身份与完整性，不证明结构安全或语义兼容。解析器必须先完成长度、偏移、计数、对齐、索引、编码和资源上限验证，再允许内容进入符号与图合并阶段。

## 输入

| 对象 | 最低契约 | 进入条件 |
| --- | --- | --- |
| Link Inputs | GOBJ、archive、SSO 与候选链接脚本 | 格式版本可识别、内容指纹可计算、目标和 schema 相容。 |
| Link Profile | 产物种类、目标 ABI、资源预算与冲突策略 | Profile 标识稳定，所有默认值显式解析并写入 Link Map。 |
| Dependency Lock | 内容寻址依赖、版本、信任声明和可选性 | 强依赖全部锁定；Strict 模式不允许隐式网络解析。 |

## 输出

| 对象 | 契约 | 消费者 |
| --- | --- | --- |
| Linked Object / SSO | 解析后的符号、类型化引用、运行 Segment 与披露闭包 | noemverify、noemstrip、noempack、Loader。 |
| Link Map | 输入成员、选择原因、ID 映射、Section 计划和产物摘要 | 开发者、审计工具、测试与论文复现实验。 |
| Conflict Report | 未解析、重复定义、约束、权限和资源失败 | 构建系统、开发者和治理评审。 |

## 输出原子性与谱系

成功产物必须绑定输入集合、顺序无关的集合摘要、Profile、Dependency Lock、规范版本和链接器版本。失败时不得发布 Linked Object；Link Map 可作为诊断草稿保留，但必须带有“未完成、不可装载”状态，避免被下游误用。

产物验证应由独立组件执行，不能仅凭 `noemld` 自报成功。Link Map 也不能替代对象本身的完整性校验。

## 资源与拒绝边界

- Profile 必须限定单对象大小、输入总量、Section 数、符号数、图节点与边数、重定位数、依赖深度和诊断上限。
- 所有累计值在分配和相加前检查；不允许先溢出再比较。
- 未知必需特性、版本或重定位类型必须失败；只有规范明确可跳过的可选扩展才可忽略。
- 重复输入、别名路径和归档循环必须按内容身份检测，不能依赖文件名。

> 字段布局、上限数值和扩展名尚未冻结；它们必须进入 GOBJ/SSO 规范或 Profile 文档，不能只存在于实现常量中。
