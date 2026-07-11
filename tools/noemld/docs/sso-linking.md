---
layout: "manual"
title: "SSO 链接 · noemld 文档 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · noemld documentation"
permalink: "/tools/noemld/docs/sso-linking.html"
manual_id: "noemld"
manual_group: "linking"
manual_order: 7
nav_title: "SSO 链接"
hero_title: "SSO 链接"
hero_description: "约束、权限、Disclosure Graph 与依赖闭包"
summary: "约束、权限、Disclosure Graph 与依赖闭包"
badges: ["noemld", "Phase 4 / Phase 5"]
---

## 组合问题

SSO 把可共享语义资产与每次运行的私有状态分离。链接时必须证明多个 SSO 的 Contract、权限、披露条件和依赖能够共同成立，而不是简单拼接或覆盖。越靠后的输入不能天然拥有更高优先级，模型也不能替代确定性的合并规则。

## 共享与私有状态

```text
只读语义图、工作流和 Contract       多 Agent 共享
只读知识子 SSO 与语义原型           多 Agent 共享
披露状态、记忆和上下文               每会话私有
调用表、符号绑定和权限状态           每实例私有
```

共享表示内容可复用，不表示权限、信任或运行状态自动共享。任何从共享资产到私有上下文的绑定都必须由 Runtime 在实例边界重新验证。

## 合并规则

- 硬约束和接口冲突导致链接失败。
- 权限取更严格交集，扩大必须显式授权。
- 软偏好按显式优先级合并。
- 强依赖必须形成内容寻址、版本锁定的完整闭包。
- 调试剥离不得改变运行语义哈希。

披露层级与覆盖证书仍以 [SSO 与渐进式披露](../../../specifications/sso.html)为权威来源。

## 候选合并代数

| 对象 | 默认组合 | 拒绝条件 |
| --- | --- | --- |
| 硬约束 | 逻辑合取，全部必须成立。 | 不可同时满足或求值域不兼容。 |
| 权限 | 取允许能力的交集和限制的并集。 | 产物所需能力被移除，或请求未授权扩大。 |
| 软偏好 | 仅按显式优先级与稳定平局规则合并。 | 优先级循环或同级冲突无规范解。 |
| Artifact Contract | 接口、schema、前后置条件逐项兼容。 | 输入输出、效果或版本承诺不相容。 |
| Disclosure Graph | 合并节点后重新计算可达性与覆盖。 | 出现未授权披露、覆盖缺口或循环超限。 |

> 该表表达待规范化的设计方向，不是已经冻结的形式代数。每类对象仍需给出数据模型、判定算法和反例。

## 依赖闭包与验证证据

强依赖闭包以内容身份和版本约束为节点，以必需关系为边，按稳定顺序求不动点。循环并非一律非法，但必须由 Profile 明确允许，并证明初始化、权限和披露语义有唯一结果；否则拒绝。

验证至少包括合并交换或顺序独立性测试、权限不扩大证明、Contract 冲突矩阵、Disclosure Graph 覆盖反例，以及剥离前后运行语义哈希等价测试。
