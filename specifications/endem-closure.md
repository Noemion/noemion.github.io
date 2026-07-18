---
layout: content
title: closure · 组合闭包规范
page_role: content
footer_text: Noemion · closure
permalink: "/specifications/endem-closure.html"
summary: 说明多个能够独立失败的目标怎样固定为完整依赖集合，并确保运行时不能换入其他对象或扩大权限。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 组合闭包 · closure
page_lead: 当多个目标能够独立失败，却必须作为同一个完整集合交付时，固定全部成员、依赖和权限边界，防止运行时换入其他对象。
badges:
- CLOSURE-CORE 0.1.0-draft
- 至少两个目标
- 尚无物理格式
- 尚未实现
previous_url: endem.html
previous_label: Endem 规范
next_url: session-contract.html
next_label: contract 会话契约
---

## 先判断它是不是两个目标

一次依赖升级既要产生使用获准依赖的发布制品，也要让部署后的服务通过健康检查。两者能够分别满足、拒绝和重试，因此各自形成 Endem；组合闭包（设计阶段名称 closure）再把它们和全部必需依赖固定为一个交付范围。

1. 依赖制品 Endem
2. 服务健康 Endem
3. 展开必需依赖
4. 固定成员与关系
5. 形成 closure

| 先问什么 | 使用 closure | 继续使用一个 Endem |
| --- | --- | --- |
| 两个终态能否独立失败或接受 | 能；每个终态保留自己的主体、判据和决定 | 不能；它们只是同一不可分终态中的多个关系 |
| 下游是否需要一个固定交付集合 | 需要；消费者必须知道完整成员和依赖关系 | 不需要；单一目标已经自包含 |
| 缺少一个成员时会发生什么 | 整个闭包停止形成，不能运行时补入 | 按 Endem 自己的形成或判断规则失败 |

> **职责边界：**closure 负责组合多个目标，不把文件列表、目录扫描、模型记忆、对话上下文或动态工具清单改称目标闭包。

## 按四步形成固定闭包

| 步骤与条款 | 开发者必须固定 | 停止条件 |
| --- | --- | --- |
| 1. 展开闭包<br>`CLOSURE-CLS-001` | 至少两个精确 Endem，以及从种子成员可达的全部必需依赖 | 单成员、截断闭包、重复伪装或闭包外仍有必需引用时原子拒绝 |
| 2. 解析引用<br>`CLOSURE-RES-001` | 在局部命名空间登记导入、导出、必需依赖和可选依赖；每个必需引用唯一绑定内容身份、规范、Profile 与解析依据 | 名称、路径、版本范围、“最新版本”、搜索顺序或模型推荐不能唯一决定对象时拒绝 |
| 3. 检查关系<br>`CLOSURE-GRF-001` | 有限无环的依赖图、显式资源预算，以及每个可选项缺失时的可观察行为 | 循环、无界遍历，或可选项缺失会删减判据、语义或权限限制时拒绝 |
| 4. 收窄权限<br>`CLOSURE-AUT-001` | 成员上限、组合策略与会话政策的交集；成员需求只作为请求 | 采用权限并集、继承最宽成员权限或由激活直接创建能力时拒绝 |

形成结果保存成员集、关系图、精确绑定和解析依据。这不是物理格式；CLOSURE-CORE 当前没有定义清单语法、文件扩展名、魔数、稳定 ABI、执行顺序或编码。

## 成员结果与会话激活不能合并

| 问题 | 应当保存什么 | 不能推出什么 |
| --- | --- | --- |
| 一个成员得到结果<br>`CLOSURE-STA-001` | 该 Endem 自己的 `met / unmet / undetermined / fault`、决定和依据 | 另一个成员或整个 closure 自动 `met`、`accepted` 或 `completed` |
| 需要闭包级决定 | 另行具名的策略、成员范围、截止点、决定权威和全部成员依据 | 签名数量、证据数量或会话成功可以替代决定 |
| 形成条件决定成员是否存在 | 在闭包身份形成前解析条件；成员变化产生不同闭包身份 | 会话开始后再把新成员加入原闭包 |
| 会话条件决定成员是否生效<br>`CLOSURE-ACT-001` | 固定成员、精确结果事件、结果域、期望值、截止点和授权策略；状态仅为 `active / inactive / unresolved / error` | `inactive` 不是满足结果，`unresolved` 不是 `undetermined`，`error` 不是 `fault` |

> **权限仍需单独核对：**成员被激活只说明它在本次会话生效，不授予能力，也不免除策略、环境、预算和决定权威检查。激活依据撤销、过期或变化时，本次会话必须重新检查或失效。

## 外部机制不能替代闭包

**复核日期：**2026-07-16。下列机制可以解释某一项工程纪律，但都不能直接成为 closure 成员、权限或结果。

| 外部机制 | 可以借鉴 | Noemion 仍需自己定义 |
| --- | --- | --- |
| [GNU make 前置条件类型](https://www.gnu.org/software/make/manual/html_node/Prerequisite-Types.html) | 普通前置条件同时表达执行顺序和更新依赖；order-only 前置条件只约束顺序 | 目标语义、精确内容身份、授权和接受决定，不能从构建依赖推出 |
| [GNU Guix 递归归档](https://guix.gnu.org/manual/en/guix.pdf) | `guix archive --export --recursive`把引用的传递闭包连同 store item 元数据一起导出 | Endem 语义、成员权限、结果域和 closure 的未来物理格式 |
| [MCP 2025-11-25 工具发现](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | `tools/list`和 `notifications/tools/list_changed`明确说明运行时工具集合可以变化 | 动态工具清单只能成为会话输入，不能改写已经形成的闭包或扩大权限 |
| [A2A 1.0 Agent Card](https://a2a-protocol.org/v1.0.0/specification/) | Agent Card 声明能力、技能、接口和安全要求，并可能按认证上下文提供扩展信息 | 远端声明不能决定本地目标成员、精确身份、行动授权或闭包级接受 |

## 规范来源与当前上限

| 资料层级 | 当前作用 | 不能证明 |
| --- | --- | --- |
| [CLOSURE-CORE](https://noemion.github.io/spec/endem-closure-core.html)与[ADR-0021](../architecture/adr-0021-synem-closure-and-activation.html) | 定义完整闭包、精确绑定、有限图、权限交集、成员结果和激活边界 | 物理格式、调度器或运行组件已经存在 |
| [威胁模型](https://noemion.github.io/spec/endem-closure-threat-model.html)与[非规范场景](https://noemion.github.io/spec/endem-closure-scenarios.html) | 检查环境替换、闭包截断、权限放大、结果洗白和激活竞态 | 案例本身成为规范条款或安全证明 |
| [closure 提案向量](https://github.com/Noemion/noemion.github.io/tree/main/vectors/endem-closure) | 执行允许分类与确定拒绝的资料一致性检查 | 解析器、形成器、inspector、runner、远程仓库或组件符合性 |

**当前策略：**CLOSURE-CORE 只定义抽象组合闭包和条件激活。动态清单不得改写闭包，成员结果不得合并，激活状态不得扩大权限。

**名称状态：**closure 是单个普通英语词，已经按词首、职责和关键字语料接受。它仍只是设计对象，不表示组合器或物理格式已经实现；文档首次出现时继续先写“组合闭包”职责。

**待定内容：**物理容器、版本约束语法、符号与重定位模型、可选分支编码、执行顺序、并行调度、受限循环、远程对象仓库和跨会话缓存。当前尚未实现 producer、inspector、runner、closure 读取器或 CLI。
