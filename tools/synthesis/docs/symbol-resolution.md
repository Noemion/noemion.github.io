---
layout: "manual"
title: "符号解析 · synthesis 使用手册 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · synthesis 使用手册"
permalink: "/tools/synthesis/docs/symbol-resolution.html"
manual_id: "synthesis"
manual_group: "linking"
manual_order: 6
nav_title: "符号解析"
hero_title: "符号解析"
hero_description: "说明链接器怎样根据 local/export/import、版本、可见性、类型和显式策略解析符号。"
summary: "说明 local/export/import、必需与可选导入、冲突和稳定选择规则。"
badges: ["synthesis", "Phase 4 / Phase 5"]
---

## 设计目标

符号解析负责把“谁需要什么定义”转化为唯一、可解释的绑定。名称相同并不代表语义相同；命名空间、版本、类型、可见性、local/export/import 和显式 resolution policy 都属于解析条件。任何未写进对象的输入顺序偏好都会破坏复现，也会让攻击者通过排列对象影响最终行为。

## 解析规则

- 扫描显式对象和归档索引，建立全局符号表。
- local 定义只在所属对象或规范作用域内可见；export 才能满足外部 import。
- required import 必须解析；optional import 必须声明缺失状态和下游行为。
- 只拉入满足当前未解析 required import 所需的归档成员。
- 链接顺序不得改变规范允许范围之外的结果。
- 不采用 ELF weak symbol 的隐式优先级；歧义和替代选择必须使用显式候选集合与 resolution policy。

## 候选解析键与选择顺序

> 下列字段与优先级是详细设计候选，最终形式必须由符号与版本规范冻结。

1. 以命名空间、规范化名称、符号种类、版本要求和目标配置构造查询键。
2. 过滤不可见、版本不满足、类型不兼容或来自未准入依赖的定义。
3. 按 local/export/import 和 required/optional 状态形成候选集合；不能用文件遍历顺序打破平局。
4. 一个兼容 export 可以满足 import；多个 export 只有在规范明确允许合并且内容身份一致时才能合并，否则产生冲突。
5. optional import 缺失时只执行对象中登记的 missing policy；策略缺失、越权或改变必需语义时失败。
6. 将选择、缺失状态、被拒候选和原因写入链接映射，再驱动归档成员闭包扩展。

## 冲突矩阵

| 情况 | 候选结果 | 必须记录 |
| --- | --- | --- |
| 一个兼容 export | 选择该定义。 | 定义来源、版本、可见性、类型和内容身份。 |
| 多个 export | 失败；仅当规范允许且内容身份一致时合并。 | 全部候选、身份比较和冲突字段。 |
| required import 无定义 | 失败。 | 引用链、搜索过的依赖和版本约束。 |
| optional import 无定义 | 只按已登记 missing policy 继续。 | 缺失状态、策略版本及下游行为。 |
| 显式替代集合 | 按对象登记的 resolution policy 选择或保持未决。 | 全部替代项、证据、策略和选择理由。 |
| 同名但类型不兼容 | 失败，不允许名称匹配掩盖类型冲突。 | 期望类型、实际类型和来源。 |

## 失败条件

- 未解析 required import 必须失败。
- 版本不匹配必须失败。
- optional import 没有明确缺失行为时必须失败。
- 多个冲突 export 不得静默选择最后写入者。

归档成员选择应以不动点算法终止，并由配置约束扫描轮数、成员数和符号数。循环别名、版本回退链和恶意碰撞必须有专门的负向测试向量。

## 验证证据

解析算法验收需要证明：输入排列不改变结果；显式对象与归档索引得到一致的定义语义；local/export/import、required/optional、版本、可见性和类型组合的冲突矩阵全部覆盖；每次选择或缺失处理都能从链接映射回溯到规范规则。若未来提供增量链接，其结果还必须与完整重链接等价。
