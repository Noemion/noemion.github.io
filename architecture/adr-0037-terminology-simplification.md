---
layout: "architecture-decision"
title: "ADR-0037 · 用职责名称替代不必要的造词 · Noemion"
page_role: "content"
footer_text: "Noemion · ADR-0037"
permalink: "/architecture/adr-0037-terminology-simplification.html"
summary: "把对象、角色、动作和语义字段改成能直接说明职责的普通词，并用版本化关键字语料检查机器标识。"
decision_id: "ADR-0037"
decision_date: "2026-07-18"
previous_url: "/architecture/adr-0036-source-bearing-and-stripped-release.html"
previous_label: "ADR-0036"
---

## 决定

Noemion 保留项目名 `Noemion` 和核心制品名 `Endem`，其余没有独立品牌职责的造词改用直白名称。当前规范、页面、字段、向量和测试直接采用新名称，不提供旧路由、别名、兼容字段或双写格式。

对象使用 `closure`、`contract` 和 `evidence`。三个信任职责使用 `producer`、`inspector` 和 `runner`。公开动作使用 `form`、`lint`、`compose`、`inspect` 和 `run`。

六项语义职责使用 `source`、`meaning`、`situation`、`direction`、`criteria` 和 `unresolved`；观察输入使用 `observation`。规范中的 `source_expression` 等精确字段名属于机器标识，不登记为人类术语，也不能在读者界面中冒充名称。

## 为什么要改

旧名称要求读者先记住词源，再回到规范寻找职责。其中一些拼写包含不自然的辅音组合或无法从普通英语读法恢复的写法；有些对象名彼此近似，却承担不同的信任责任。专名没有带来独立消费者、协议或品牌价值，只增加了朗读、听写、检索和代码评审的成本。

普通职责词也不能只因为“看起来熟悉”就采用。每个替代词仍须满足三项条件：定义能恢复对象与失败责任；与相邻概念有明确反例；对应机器标识不与当前声明的语言关键字语料发生精确冲突。

## 不同名称使用不同检查

| 名称类别 | 当前处理 | 不再重复的工作 |
| --- | --- | --- |
| `Noemion`、`Endem` 两个自造名称 | 检查完整拼写、自然读法、听写恢复、相邻名称混淆和适用语言范围 | 不能用维护者指定读法、词源或自动转写代替真实使用证据 |
| `closure`、`evidence`、`compose`、`source`、`profile`、`time`、`scope`、`coverage`、`guard`、`signed`、`view` 等普通英语词 | 检查词首是否能按通常英语自然起音，并保留约定俗成的词中、词尾拼写和读法 | 不因词中、词尾正字法或缺少专门人类实验而判为未通过 |
| `closure`、`contract`、`evidence`、`producer`、`inspector`、`runner` 等普通单词 | 检查词首，并核对对象、消费者、信任与失败责任 | 不把职责短语重新包装成名称，也不建立独立发行读音审查 |
| CORE、Profile、字段、枚举和动作机器值 | 检查规范职责、精确拼写、版本化关键字语料和相邻接口冲突 | 机器文档 ID 不承担口头品牌职责；普通词机器值不需要“官方发音” |

名称冲突检查只对记录的时间、范围和资料负责。搜索未命中不能证明包名、仓库名、协议名或权利永久可用；大小写变化也不能消除同一命令或相邻职责的混淆。新增自造名称前必须先证明普通职责词不足，普通词足够时停止造词。

## 关键替换

| 原设计名 | 当前名称 | 读者应直接理解的职责 |
| --- | --- | --- |
| Synem | closure | 多个 Endem 的完整解析闭包 |
| Dromen | contract | 一次运行的主体、政策、环境、能力、预算与证据责任 |
| Iknem | evidence | 一项有主体、范围、方法、结果和限制的证据记录 |
| Ktisor | producer | 只从获准输入确定性写入制品 |
| Theor | inspector | 用独立且只读的路径检查实际制品 |
| Drasor | runner | 只在本次会话允许的范围内尝试动作 |
| ktise / elenk / pleko / theor / drase | form / lint / compose / inspect / run | 形成、生产侧检查、组合、独立检查和有界运行 |
| rhem / semion / skena | source / meaning / situation | 来源、已确认意义投影和可能事态 |
| telis / krin / apor / phain | direction / criteria / unresolved / observation | 目标方向、判据、待确认意义和观察输入 |

上表保存本次迁移的完整公开关系；机器登记保存现行名称、职责和状态，[开发指南](../docs/development-guide.html#使用现行名称)说明开发者怎样书写和引用这些名称。项目不另建术语审查页面、结果报告或内部迁移登记。

## 关键字冲突怎样处理

检查覆盖 C23、C++23、Rust、Go 1.26、Python 3.14、Java 25、ECMAScript 2026、Swift、Kotlin、C# 和 PostgreSQL SQL 的声明版本。发现的现行冲突包括 SQL `grant`、`all`、`some`，Go 与 Swift `defer`，以及 C# `fixed`。

因此授权结果改用 `allowed / denied / pending`，时间范围改用 `utc_window / elapsed_window`，量化改用 `every / at_least_one`。生产侧检查使用 `lint`，没有采用会与 SQL `CHECK` 冲突的 `check`。

这项检查只对声明的版本化语料负责。它不声称覆盖所有语言，也不保证未来语言不会增加同名关键字；发行检查必须重新运行并记录语料版本。

## 规范身份与兼容边界

对象和条款前缀同步改为 `CLOSURE-CORE`、`SESSION-CORE` 和 `EVIDENCE-CORE`。保留来源的六记录 Profile 使用 `END-P2` 与 `profile_id = 3`；旧 `END-P1` 身份不继续使用。字段、枚举或 Profile 身份变化会改变符合性判断，因此不能把新旧数据当作同一格式的两种拼写。

历史 ADR 保留原文件名和当时的决定语境，只作为演进证据。当前导航、首页卡片、规范页面、机器登记、向量和测试只使用新名称。

## 仍然没有证明什么

这项决定不证明组件已经实现，也不证明两个自造名称适合所有语言和口音。`Noemion` 与 `Endem` 仍须在首次发行前完成真实人类朗读、听写和职责匹配测试；机器关键字检查、词典证据、TTS 或 ASR 都不能替代这项人类验证。普通英语单词已经按词首起音规则接受，不再因缺少同类人类实验而标为待定。

## 验证要求

每次术语变更必须同时通过以下检查：

1. 机器登记中的每个人类术语都是一个完整单词，并且有职责、状态和定义。
2. 当前机器标识不与声明的关键字语料精确冲突。
3. 当前页面、规范和研究提案不再使用已退役名称；只有历史 ADR 与本决定的迁移对照保留旧词。
4. 首页卡片只指向对应的现行项目页面，退役审查页和研究提案不提供兼容入口。
5. 规范、Profile、向量、测试、导航和公开说明保持同一词表。
