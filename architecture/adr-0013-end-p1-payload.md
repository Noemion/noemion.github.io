---
layout: architecture-decision
title: ADR-0013 · 来源保留 END-P2 Profile
page_role: content
footer_text: Noemion · ADR-0013
permalink: "/architecture/adr-0013-end-p1-payload.html"
summary: 说明 END-P2 怎样保存原始语言和已确认目标结构，以及为什么这种形成制品不能直接作为发布制品。
decision_id: ADR-0013
page_heading: ADR-0013 · 来源保留 · END-P2 Profile
page_lead: END-P2 把原始自然语言、六个语义面和封闭引用写入同一形成制品，供评审与实验验证；它不可直接发布，也不能单独证明内容已经接受。
badges:
- 当前策略
- END-P2 0.1.0-draft
- Profile 3
- 不可发布
previous_url: adr-0012-rust-core-language.html
previous_label: ADR-0012
next_url: adr-0014-source-manifest.html
next_label: ADR-0014
---

## 先确定 END-P2 是什么

`profile_id=3` 精确绑定 END-P2。它是来源保留的形成与评审 Profile，不是最终发布 Profile，也不是稳定 ABI。

| 问题 | 当前答案 | 声明上限 |
| --- | --- | --- |
| 为什么不再使用 END-P0 | END-P0 只有六个空映射，只能验证容器结构。 | 不能把结构接受称为有效 Endem。 |
| END-P2 保存什么 | 保存原始自然语言、来源范围、语义关系、目标方向、判据和待确认项。 | 单文件最高只能声称 Profile 接受。 |
| 谁使用它 | 未来由 deterministic producer 形成和回读，再由 independent inspector 沿独立路径解释相同字节。 | 当前没有 deterministic producer、independent inspector 或 CLI 实现。 |
| 能否作为发布物 | 不能；`publishable=false` 是 Profile 的明确属性。 | 不能直接删除原文后继续声称 END-P2。 |

## 开发者应按什么顺序检查

1. END-FMT字节结构
2. Profile 3能力上限
3. 六个记录精确字段
4. 排序与引用封闭
5. 外部前提内容接受
6. 未来发布另行派生

| 停止位置 | 必须检查 | 失败后不得继续声称 |
| --- | --- | --- |
| 容器 | 头部、目录、范围、资源上限和确定性 CBOR。 | Profile 接受。 |
| Profile | 记录种类、状态、标志、字段集合和功能禁用项。 | 字段或引用有效。 |
| 内容结构 | 类型、规范排序、重复项、来源范围和交叉引用。 | 内容已经由权威接受。 |
| 外部前提 | 意义确认、权威绑定和适用的内容规则。 | 目标满足、动作授权或最终接受。 |
| 发布派生 | 新 Profile、引用重写、损失、泄露边界、新身份和重新验证。 | 形成制品已经变成可发布制品。 |

## 六个记录分别回答什么

| 记录 | 开发者问题 | END-P2 边界 |
| --- | --- | --- |
| `source_expression` | 原始表达来自哪里，哪一段进入解释？ | 保存内容、语言、媒体类型、版本和 Unicode 标量范围。 |
| `meaning_projection` | 哪些符号、关系与角色得到怎样的意义投影？ | 投影选择器仍是不可信标识，不自证语义授权。 |
| `situation` | 唯一根事态由哪些正负关系构成？ | 只表达结构，不记录观察或满足结果。 |
| `goal_direction` | 目标要求达到还是保持该事态？ | 当前只编码 `reach`；`maintain` 等待新 Profile。 |
| `satisfaction_criteria` | 需要哪些观察，缺失和求值错误怎样返回？ | 选择器不等于证据存在，也不等于决定权威有效。 |
| `unresolved_meaning` | 哪些歧义、候选和决定责任仍未关闭？ | 空记录也必须显式编码，不能用缺失冒充没有问题。 |

## 封闭 schema 怎样失败

| 检查 | 接受条件 | 拒绝条件 |
| --- | --- | --- |
| 映射键 | 只出现登记键，并包含全部必需键。 | 未知、缺失、重复或错误类型的键。 |
| 数组 | 按登记的身份或确定性编码值排序。 | 输入顺序、哈希遍历顺序或重复身份。 |
| 来源范围 | 以 Unicode 标量计数，且落在实际 `source_expression.content` 内。 | 混用字节、UTF-16 code unit、字素或越界范围。 |
| 交叉引用 | 符号、关系、角色、事态和来源引用都能在对象内解析。 | 悬空引用、错绑角色或跨来源伪装。 |
| 功能范围 | 只使用 END-P2 已登记的 `reach` 与功能集合。 | 把时间、量化、测量、签名或加密塞入未登记字段。 |

完整键号、枚举、排序和资源上限见[机器可读 END-P2 Profile](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p2.json)。它与 END-FMT 共同构成字段权威源，页面摘要不能替代它们。

## 外部标准只约束哪些机制

| 资料 | END-P2 采用 | 不采用为 |
| --- | --- | --- |
| [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html) | 分层接受、受限数据模型与确定性编码。 | 通用 CBOR 解码成功等于 END-P2 接受。 |
| [BCP 47](https://www.rfc-editor.org/rfc/rfc5646.html) | 语言标签的 ASCII 结构与语义。 | 语言标签证明来源真实，或已完成登记查询与规范化。 |
| [RFC 6838](https://www.rfc-editor.org/rfc/rfc6838.html) | 媒体类型的基本结构。 | 媒体类型证明内容安全或投影正确。 |
| [Unicode 17](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-2/) | 区分编码单元、标量值和字素；范围使用标量值。 | 自动获得稳定显示、规范等价或安全标识符。 |

现行字节向量只执行语言标签与媒体类型的基本语法检查。完整登记有效性、首选值替换和规范化算法仍未固定，不能写成已经“标准化”。

## 当前不能发布或实现什么

END-P2 不定义量化、时间字段、单位换算、摘要、签名、授权决定、Endem closure、压缩、加密、来源裁剪或稳定 ABI。抽象语义已有决定时，也必须等待新的物理 Profile 和正反字节向量。

最终发布版必须使用新的封闭 Profile，重写来源引用，披露损失并取得新身份。END-P2 当前只有规范、Profile 和字节向量；这些资料不是生产组件或符合性声明。

- [查看读取顺序](adr-0011-endem-container.html) — 先区分容器、Profile、内容和外部判断。
- [查看内容接受](adr-0030-endem-content-and-authorization-companions.html) — 了解为什么权威选择器不能自证授权。
- [查看裁剪发布](adr-0036-source-bearing-and-stripped-release.html) — 确认新 Profile、新身份和引用重写要求。
- [查看验证职责](../development/testing.html) — 区分字节向量、实现证据和符合性声明。
