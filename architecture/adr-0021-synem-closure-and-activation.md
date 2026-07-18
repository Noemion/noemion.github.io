---
layout: architecture-decision
title: ADR-0021 · 依赖必须先固定，权限只能收窄
page_role: content
footer_text: Noemion · ADR-0021
permalink: "/architecture/adr-0021-synem-closure-and-activation.html"
summary: 说明多个目标共同交付时怎样先固定全部成员与依赖，并确保运行时只能收窄、不能扩大共同权限。
decision_id: ADR-0021
page_heading: ADR-0021 · 依赖必须先固定 · 权限只能收窄
page_lead: 多个目标共同交付时，先固定全部成员、传递依赖和精确身份，再计算共同允许的权限。运行时发现不能换入新目标，也不能扩大能力。
badges:
- 当前策略
- CLOSURE-CORE 0.1.0-draft
- 尚无物理格式
- 尚未实现
previous_url: adr-0020-composite-situations-and-criteria.html
previous_label: ADR-0020
next_url: adr-0022-iknem-evidence-and-appraisal.html
next_label: ADR-0022
---

## 用一次发布流程读懂组合闭包

发布服务既要得到符合要求的构建产物，也要让部署后的服务通过健康检查。两个终态可以独立失败，因此分别形成 Endem，再进入同一个 Endem 组合闭包。

1. 识别两个独立终态
2. 选择种子Endem
3. 展开全部必需依赖
4. 唯一绑定精确身份
5. 对成员权限继续求交
6. 会话只激活固定成员

| 处理阶段 | 发布示例 | 必须停止的情况 |
| --- | --- | --- |
| 划分目标 | 构建产物和服务健康各有自己的判据与决定。 | 把两个可独立失败的终态塞进一个 Endem。 |
| 展开依赖 | 从两个种子成员递归加入全部必需 Endem。 | 还有闭包外必需引用，或只收集当前目录中的文件。 |
| 绑定身份 | 每个引用唯一绑定规范、Profile 与完整内容身份。 | 使用名称、路径、版本范围、搜索顺序或 `latest`。 |
| 收窄权限 | 成员上限、组合策略与会话政策只取交集。 | 某成员需要网络，就让所有成员取得网络能力。 |
| 进入会话 | 守卫只决定固定成员本次是否生效。 | 运行时下载新成员、改写闭包身份或直接授予权限。 |

组合闭包的现行设计名称是 Endem closure。它不是文件包、搜索结果、模型上下文、对话记忆或动态工具列表。

## 先判断同一终态还是多个目标

| 边界问题 | Endem 复合根 | Endem 组合闭包（Endem closure） |
| --- | --- | --- |
| 终态身份 | 多个关系共同描述一个不可分终态。 | 至少两个终态能够独立实现和失败。 |
| 判断与决定 | 共享一个目标方向和验收责任。 | 每个成员保留自己的满足结果与最终决定。 |
| 组合关系 | 叶结果使用 `all_of / any_of`。 | 显示必需依赖、精确绑定和会话激活关系。 |
| 内容身份 | 一个 Endem 拥有一个内容身份。 | 完整成员集与关系共同决定闭包身份。 |
| 缺失处理 | 按该 Endem 的形成或判断规则失败。 | 必需成员缺失时原子拒绝，不能以后补入。 |

自然语言中的“还要”“依赖”或“如果”不能自行决定对象边界。开发者必须检查终态、消费者、生命周期、权威和失败责任。

## 成员、引用和权限怎样形成闭包

| 规范责任 | 必须固定 | 确定拒绝 |
| --- | --- | --- |
| `CLOSURE-CLS-001`<br>完整成员 | 至少两个不同 Endem，以及从种子可达的全部必需传递成员。 | 单成员、截断闭包、重复身份或闭包外必需引用。 |
| `CLOSURE-RES-001`<br>唯一绑定 | 引用方、被引用方、规范、Profile、精确内容身份与解析依据。 | 歧义、冲突、环境搜索或输入顺序改变解析结果。 |
| `CLOSURE-GRF-001`<br>有限关系 | 有限无环图、资源预算，以及可选项缺失时的可观察行为。 | 循环、无界遍历，或可选项缺失会降低语义和判据。 |
| `CLOSURE-AUT-001`<br>权限交集 | 成员上限、组合策略和会话政策的共同允许范围。 | 权限并集、继承最宽成员能力或由依赖产生授权。 |
| `CLOSURE-STA-001`<br>成员结果 | 成员结果保持各自身份；闭包级决定另行绑定策略、范围与权威。 | 把成员结果折叠为布尔值或隐式总体结果。 |

同一正式输入必须产生同一成员集、关系与绑定。成员顺序、当前目录、区域设置、模型推荐和网络最新版本都不能改变结果。

## 形成时选择与会话激活必须分开

形成条件决定谁属于制品，会话守卫只决定固定成员本次是否生效。两者的身份、失败后果和结果域不同。

| 状态或阶段 | 回答的问题 | 不得推出 |
| --- | --- | --- |
| 形成时选择 | 某个 Endem 是否进入成员集合；必须在闭包身份形成前解析。 | 把未解析条件留到运行时，或保持原闭包身份。 |
| 本次生效<br>`activation=active` | 固定守卫已经匹配，本成员进入后续政策检查。 | `met`、最终接受或能力授权。 |
| 本次不生效<br>`activation=inactive` | 守卫已经确定不匹配，本次不判断该成员。 | `met / unmet / undetermined`。 |
| 激活依据未就绪<br>`activation=unresolved` | 所需精确结果事件或其他依据尚不可用。 | 满足结果 `undetermined`。 |
| 激活检查失败<br>`activation=error` | 守卫解析、截止点或检查契约发生故障。 | 满足结果 `fault`。 |
| 依据变化 | 追加新激活事件，并重新检查或使当前会话失效。 | 覆盖旧事件、加入新成员或扩大权限。 |

机器结果域仍是 `active / inactive / unresolved / error`。裸状态词在日志和口头交流中容易脱离结果域，必须写明 `activation=`；人类界面先使用表中的中文职责。

> **名称边界：**“闭包”可能被理解为程序闭包或流程结束，首次说明应写“Endem 组合闭包”。Endem closure 已按普通词的词首和职责规则接受；它仍是设计阶段名称，不表示物理格式或组件已经存在。

## 外部依赖与 Agent 清单只能提供什么

**复核日期：**2026-07-16。外部机制可以提供解析、构建或发现事实，但正式绑定必须记录精确身份，并遵守 Noemion 自己的权限与结果边界。

| 外部资料 | 可采用的机制 | Noemion 不继承 |
| --- | --- | --- |
| [NIST 传递闭包定义](https://xlinux.nist.gov/dads/HTML/transitiveClosure.html) | 若关系包含 `(a,b)` 与 `(b,c)`，传递扩展也包含 `(a,c)`。 | 数学定义不提供内容身份、无环政策、权限或接受语义。 |
| [GNU ld 文件命令](https://sourceware.org/binutils/docs/ld/File-Commands.html) | 展示当前目录、`-L` 和 `SEARCH_DIR` 怎样影响链接时搜索。 | 环境搜索结果不能成为正式闭包绑定。 |
| [GNU Guix 参考手册](https://guix.gnu.org/manual/en/guix.pdf) | 递归导出可以包含 store item 的依赖闭包、引用和派生元数据。 | 不采用 Guix Store 路径、包权限或归档格式。 |
| [GNU make 条件指令](https://www.gnu.org/software/make/manual/html_node/Conditionals.html) | 条件在读取 makefile 时决定哪些文本可见，不控制 recipe 执行时状态。 | 形成时成员选择不能冒充会话期激活。 |
| [W3C SHACL](https://www.w3.org/TR/shacl/#deactivated) | 停用的 Shape 不产生验证结果。 | 空结果不等于符合、满足或权限授予。 |
| [MCP 2025-11-25 工具规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | `tools/list` 与变更通知表明运行时工具集合可以变化。 | 动态清单不能改变 Endem closure 闭包或直接授予权限。 |
| [A2A 1.0 Agent Card](https://a2a-protocol.org/v1.0.0/specification/) | 声明 Agent 能力、技能、接口和安全要求。 | 远端声明不能决定本地成员、精确身份或闭包级接受。 |

## 当前还不能编码或执行什么

现行十二个 Endem closure 提案向量覆盖六个允许分类和六个确定拒绝，只检查 CLOSURE-CORE 六条抽象规则。END-CORE、END-FMT 和 END-P2 保持不变。

这项决定不表示 deterministic producer、independent inspector、bounded runner、CLI、解析器或运行时已经实现。Endem closure 也没有物理容器、文件扩展名、魔数、稳定 ABI 或版本范围语法。

符号与重定位、执行顺序、并行调度、受限循环、远程对象仓库、跨会话缓存和规范字节仍需真实消费者、新 Profile、威胁分析与组件证据。

- [查看组合闭包规范](../specifications/endem-closure.html) — 按开发者任务查询 CLOSURE-CORE 六项责任。
- [查看单目标复合判据](adr-0020-composite-situations-and-criteria.html) — 先判断一个终态还是多个独立目标。
- [查看一次会话契约](../specifications/session-contract.html) — 理解固定闭包怎样进入受限运行。
- [查看权限决定边界](../specifications/authority.html) — 区分成员需求、能力上限与实际授权。
