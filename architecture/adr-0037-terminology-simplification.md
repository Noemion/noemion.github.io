---
layout: "architecture-decision"
title: "ADR-0037 · 名称必须直白、可读、可核对 · Noemion"
page_role: "content"
footer_text: "Noemion · ADR-0037"
permalink: "/architecture/adr-0037-terminology-simplification.html"
summary: "规定对象、角色、动作和语义字段使用能直接说明职责的普通词，并用版本化关键字语料检查机器标识。"
decision_id: "ADR-0037"
decision_date: "2026-07-18"
previous_url: "/architecture/adr-0036-source-bearing-and-stripped-release.html"
previous_label: "ADR-0036"
---

## 决定

Noemion 使用项目名 `Noemion` 和核心制品名 `Endem`。其余没有独立品牌职责的对象、角色和动作使用直白名称；公开资料只使用现行名称。

对象使用 `closure`、`contract` 和 `evidence`。三个信任职责使用 `producer`、`inspector` 和 `runner`。公开动作使用 `form`、`lint`、`compose`、`inspect` 和 `run`。

六项语义职责使用 `source`、`meaning`、`situation`、`direction`、`criteria` 和 `unresolved`；观察输入使用 `observation`。规范中的 `source_expression` 等精确字段名属于机器标识，不登记为人类术语，也不能在读者界面中冒充名称。

## 名称为什么必须直接说明职责

名称必须让读者从定义恢复对象、消费者与失败责任，并与相邻概念形成明确反例。普通职责词也不能只因为“看起来熟悉”就采用；对应机器标识还必须与当前声明的语言关键字语料进行精确比较。

## 不同名称使用不同检查

| 名称类别 | 当前处理 | 不能替代的证据 |
| --- | --- | --- |
| `Noemion`、`Endem` 两个自造名称 | 检查完整拼写、自然读法、听写恢复、相邻名称混淆和适用语言范围 | 不能用预设读法、词源或自动转写代替真实使用证据 |
| `closure`、`evidence`、`compose`、`source`、`profile`、`time`、`scope`、`coverage`、`guard`、`signed`、`view` 等普通英语词 | 检查词首是否能按通常英语自然起音，并保留约定俗成的词中、词尾拼写和读法 | 不因词中、词尾正字法或缺少专门人类实验而判为未通过 |
| `closure`、`contract`、`evidence`、`producer`、`inspector`、`runner` 等普通单词 | 检查词首，并核对对象、消费者、信任与失败责任 | 不把职责短语重新包装成名称，也不建立独立发行读音审查 |
| CORE、Profile、字段、枚举和动作机器值 | 检查规范职责、精确拼写、版本化关键字语料和相邻接口冲突 | 机器文档 ID 不承担口头品牌职责；普通词机器值不需要“官方发音” |

名称冲突检查只对记录的时间、范围和资料负责。搜索未命中不能证明包名、仓库名、协议名或权利永久可用；大小写变化也不能消除同一命令或相邻职责的混淆。新增自造名称前必须先证明普通职责词不足，普通词足够时停止造词。

## 当前名称与职责

| 当前名称 | 读者应直接理解的职责 |
| --- | --- |
| `closure` | 多个 Endem 的完整解析闭包 |
| `contract` | 一次运行的主体、政策、环境、能力、预算与证据责任 |
| `evidence` | 一项有主体、范围、方法、结果和限制的证据记录 |
| `producer` | 只从获准输入确定性写入制品 |
| `inspector` | 用独立且只读的路径检查实际制品 |
| `runner` | 只在本次会话允许的范围内尝试动作 |
| `form / lint / compose / inspect / run` | 形成、生产侧检查、组合、独立检查和有界运行 |
| `source / meaning / situation / direction / criteria / unresolved / observation` | 来源、已确认意义、可能事态、目标方向、判据、待确认意义和观察输入 |

机器登记保存现行名称、职责和状态；本决定说明开发者怎样书写和引用这些名称。公开页面与机器登记必须使用同一套名称和定义。

## 怎样读写当前名称

项目只保留两个自造名称：**Noemion** 和 **Endem**。Noemion 的候选分段是 `No-e-mi-on`，候选读音为 /noʊˈiː.mi.ən/，也可以按 `noh-EE-mee-uhn` 拼读；Endem 的候选分段是 `En-dem`，候选读音为 /ˈɛn.dɛm/，也可以按 `EN-dem` 拼读。两组提示覆盖每个字母，没有静音字母，但首次朗读与听辨结果尚未形成，因此它们不是已经确认的正式读音。

普通英语工程词沿用通常拼写。每个人类名称都是一个完整单词；职责短语只能用于说明，不能登记成名称。若名称需要替换，替换项必须是一个完整单词，不能使用空格、连字符、下划线或多个单词拼接。字段、枚举、路由、文件路径和规范编号是机器标识，可以遵守各自声明的组合语法，但不作为人类名称展示。

## 关键字冲突怎样处理

检查覆盖 C23、C++23、Rust、Go 1.26、Python 3.14、Java 25、ECMAScript 2026、Swift、Kotlin、C# 和 PostgreSQL SQL 的声明版本。发现的现行冲突包括 SQL `grant`、`all`、`some`，Go 与 Swift `defer`，以及 C# `fixed`。

授权结果使用 `allowed / denied / pending`，时间范围使用 `utc_window / elapsed_window`，量化使用 `every / at_least_one`。生产侧检查使用 `lint`，避免与 SQL `CHECK` 冲突。

这项检查只对声明的版本化语料负责。它不声称覆盖所有语言，也不保证未来语言不会增加同名关键字；发行检查必须重新运行并记录语料版本。

## 规范身份

对象和条款使用 `CLOSURE-CORE`、`SESSION-CORE` 和 `EVIDENCE-CORE`。保留来源的六记录 Profile 使用 `END-P2` 与 `profile_id = 3`。字段、枚举或 Profile 身份变化会改变符合性判断，因此每个草案必须绑定精确身份。

## 仍然没有证明什么

这项决定不证明组件已经实现，也不证明两个自造名称适合所有语言和口音。`Noemion` 与 `Endem` 仍须在首次发行前完成真实人类朗读、听写和职责匹配测试；机器关键字检查、词典证据、TTS 或 ASR 都不能替代这项人类验证。普通英语单词已经按词首起音规则接受，不再因缺少同类人类实验而标为待定。
