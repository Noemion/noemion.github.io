---
layout: "manual"
title: "装载与安全 · noemld 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemld documentation"
permalink: "/tools/noemld/docs/loader-security.html"
manual_id: "noemld"
manual_group: "security"
manual_order: 8
nav_title: "装载与安全"
hero_title: "装载与安全"
hero_description: "Segment、Merkle、签名、AI-NX 与 AI-RELRO"
summary: "Segment、Merkle、签名、AI-NX 与 AI-RELRO"
badges: ["noemld", "Phase 4 / Phase 5"]
---

## 信任转换与职责分界

`noemld` 负责生成可验证的 Segment 计划、绑定和完整性材料；Loader/GRT 负责在实际环境中重新验证并装载。链接成功不等于允许执行，签名有效也不等于内容安全。对象、依赖、模型包和外部资源在每个边界都继续按不可信输入处理。

## 威胁模型

- 伪造或截断 Header、Section、Segment、符号和重定位表以触发越界或混淆解析。
- 替换依赖、重放旧版本或利用未覆盖字段绕过签名与策略。
- 借重定位或权限合并把数据、外部内容或未签名资产提升到高权限执行域。
- 利用超大图、深依赖、压缩炸弹或诊断洪泛消耗资源。
- 在验证后、冻结前修改绑定，造成检查与使用时不一致。

## Loader / GRT 流程

1. 在分配前检查 Magic、版本、文件总长、Header、表边界、计数和 Profile 上限。
2. 验证签名策略、回滚策略与待加载 Segment 的 Merkle Proof，并确认覆盖范围。
3. 先建立不可执行的暂存映射，再按类型构造符号表、模型表和调用表。
4. 完成允许的装载时重定位，复核段属性、权限、策略和依赖身份。
5. 冻结关键绑定与只读区域，清除暂存写权限，最后才交给 Runtime Lowering。

任一步失败都销毁本次装载事务，不暴露半初始化实例，也不降级到更宽松 Profile。

## 完整性与签名

签名范围覆盖 Header、Program/Section Header、入口、符号、重定位、权限、策略和模型要求；按需加载时验证对应数据块与 Merkle 路径。

签名方案还必须规定算法标识、密钥身份、吊销与轮换、时间或单调版本策略，以及未知算法的失败行为。Merkle 根、块大小和缺失块语义必须进入签名范围，避免验证正确的数据却使用错误的解释。

## AI-NX 与 AI-RELRO

- 数据段不得提升为高权限指令段。
- 不可信外部内容不得覆盖可信策略。
- 未签名代码不得进入执行段。
- 重定位后冻结符号绑定、策略、权限和入口。

> **候选安全概念：**AI-NX 与 AI-RELRO 当前用于表达“不可信语义资产不可提升”和“关键绑定在验证后冻结”的设计方向，名称、覆盖对象与强制规则尚需威胁分析、规范条款和 ADR 冻结。

## 放行证据

安全设计放行需要结构化模糊测试、恶意对象语料、签名覆盖变异测试、TOCTOU 场景、权限单调性测试、资源耗尽测试和装载失败原子性验证。论文或标准主张应明确攻击模型与剩余风险，不能以“使用签名”代替完整安全论证。
