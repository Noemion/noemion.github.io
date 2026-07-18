---
layout: spec
title: "Noemion 发行术语去专名化研究提案 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/release-terminology-simplification-proposal.html"
summary: "检查现有专名是否真的不可替代，并优先比较读者能直接恢复职责的普通词，减少记忆和口头混淆。"
document_status: "非规范研究提案"
---
# Noemion 发行术语去专名化研究提案

状态：非规范研究提案
日期：2026-07-14
结论状态：桌面审查完成；尚待人类验证
适用范围：Endem 之外的制品称呼、信任角色、公开动作、标准 ID、页面路由与未来 CLI

本提案不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求，不进入 `registry.json`。它不改写现行制品、字段、对象种类、结果域、权限、不变量、规范字节或测试向量，也不创建组件实现。现行 Synem、Dromen、Iknem、Ktisor、Theor、Drasor 与五个动作在迁移决定前仍是设计阶段标识；候选普通词不是别名、重定向或兼容入口。

## 直接结论

Noemion 当前的主要传播问题不是缺少一份“官方读音表”，而是承担相邻职责的新造词过多。读者必须先记住词源和拼写，才能知道对象或动作做什么；这与项目“先给直白结论”的写作原则相冲突，也增加口头混淆面。

建议采用一项更严格的发行原则：**只有确实需要独立公共身份、且普通术语无法准确承担职责时，才创造专名。**

按这项原则进行桌面审查后：

- **保留 Endem 进入人类读音验证。**它同时绑定最小目标制品、`.endem` 扩展名、`endem` CLI、内容标准和社区核心对象，具有不可由一句普通职责短语完全替代的公共身份。保留不表示读音、权利或发行条件已经通过。
- **Synem 不应作为发行专名。**它的决定性不变量就是至少两个精确 Endem 的完整传递闭包；首选直白称呼是 **Endem closure（Endem 闭包）**，不能简化成普通 bundle。
- **Dromen 不应作为发行专名。**它不是持久制品，而是一次会话的只读执行契约；首选称呼是 **session contract（会话契约）**。去掉制品式专名还能减少把它误当文件、凭据包或可恢复会话的风险。
- **Iknem 不应作为发行专名。**它的首选称呼是 **scoped evidence record（有范围证据记录）**，正文可以在边界已明确后简称 evidence record。这个称呼不把记录升级为证明、有效证据、充分覆盖或最终决定。
- **Ktisor、Theor 与 Drasor 不应在组件尚未实现时占用产品式专名。**它们分别改用 **deterministic producer（确定性生产边界）**、**independent inspector（独立检查边界）**与 **bounded runner（有界运行边界）**。这些是信任角色，不是新品牌。
- **五个公开动作改用普通英语动词进入人类验证：**`form`、`check`、`compose`、`inspect` 与 `run`。它们分别对应当前 `ktise`、`elenk`、`pleko`、`theor` 与 `drase` 的职责，不改变输入、输出或失败责任。

这是一项候选迁移方案，不是已接受命名。若后续证据支持该方向，项目还必须通过人类首次朗读、听写回填、职责匹配和成对混淆验证，再以 ADR 一次性迁移现行资料；当前不修改任何规范标识。

## 为什么先审查“是否需要专名”

[ISO 704:2022](https://www.iso.org/standard/79077.html)把对象、概念、定义和指称的联系作为术语工作的基础，并分别讨论术语和专名的形成。它不要求每个概念都有新造专名。

[GNU Coding Standards 的 Names 规则](https://www.gnu.org/prep/standards/html_node/Names.html)指出，名称像注释一样应提供有用意义，不应为了简短采用晦涩缩写。Noemion 不是 GNU 包，但该原则直接适用于未来 CLI、规范字段和工程协作。

当前 Agent 协议进一步证明“一个神秘短名承担全部语义”不是必要设计：

- [MCP 2025-11-25 工具定义](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)分开唯一 `name`、可读 `title`、职责 `description`、输入输出 schema、行为提示和任务支持声明；提示仍是不可信信息，不能替代授权或隔离。
- [A2A 1.0.0 AgentSkill](https://a2a-protocol.org/v1.0.0/specification/)分开唯一 `id`、人类可读 `name`、详细 `description`、标签、示例和输入输出模态。

Noemion 可以采用这种分离：普通词负责可读性，规范 ID 负责稳定引用，条款和 schema 负责精确语义，权限边界负责强制。专名不能同时替代这四层。

## 专名必要性门禁

一个新的或现行专名只有同时满足下列条件，才值得进入发行词表：

1. **独立对象：**它不是现有对象的角色、视图、状态、闭包或一次会话描述。
2. **真实消费者：**至少一个外部读者或系统必须稳定指称它，而不是只为架构图对称。
3. **普通词不足：**现有标准术语或简短职责短语会造成实质错误，不只是“不够独特”。
4. **语义可恢复：**首次读者从名称和一句职责能够区分相邻对象。
5. **口头可区分：**目标语言中能够顺畅朗读、听写回填，并与完整词表区分。
6. **机器身份分离：**名称变化不会静默改变内容身份、规范语义、权限或结果域。
7. **停止条件明确：**出现更准确普通词、相邻冲突、读音失败或真实消费者消失时，专名退出。

“词源漂亮”“搜索结果较少”“能形成整齐词族”或“已经写进许多页面”都不能单独通过门禁。

## 对象与角色审查

| 现行名称 | 不可变职责 | 专名必要性结论 | 首选候选 | 主要风险与限制 |
| --- | --- | --- | --- | --- |
| Endem | 最小、独立有效且可验证的期望终态单元；绑定扩展名、CLI 与核心标准 | 暂时通过必要性门禁；仍未通过读音、权利和发行门禁 | Endem | `end-em`、`en-dem` 等首次读法仍需真实验证；不得让词源替代六语义面 |
| Synem | 至少两个精确 Endem 的完整传递闭包 | 不通过；普通技术短语已能表达决定性不变量 | Endem closure / Endem 闭包 | `closure` 单独使用会被理解为停止营业、情绪终结或程序闭包，必须保留 Endem 限定并定义传递闭包 |
| Dromen | 一个 Drase 会话中封存的只读执行契约；永不持久化 | 不通过；专名反而诱导读者把它物化成文件或可恢复状态 | session contract / 会话契约 | 必须持续说明契约只属于一次会话，不是凭据包、进程映像或权限载体 |
| Iknem | 绑定主体、范围、方法、环境、观察、结果和限制的记录 | 不通过；普通职责短语更准确 | scoped evidence record / 有范围证据记录 | “evidence” 不能推出真实、有效、充分或 accepted；需保留记录类别和来源类别 |
| Ktisor | 唯一规范写入与确定性形成边界 | 不通过；当前是未实现信任角色，不是需要品牌的产品 | deterministic producer / 确定性生产边界 | 不能把 producer 解释为任意写入器；模型与独立检查路径仍无写权限 |
| Theor | 与生产路径独立实现的只读检查边界 | 不通过；职责短语足够 | independent inspector / 独立检查边界 | “independent” 必须由实现、进程和故障路径证明，名称本身不产生独立性 |
| Drasor | 最小能力域中的有界会话运行边界 | 不通过；职责短语足够 | bounded runner / 有界运行边界 | “bounded” 必须由能力、预算、网络、秘密和销毁机制强制，不是自我声明 |

### Endem 闭包不是普通 bundle

[NIST Dictionary of Algorithms and Data Structures](https://xlinux.nist.gov/dads/HTML/transitiveClosure.html)把 transitive closure 定义为扩展后的二元关系：若 `(a,b)` 与 `(b,c)` 存在，则 `(a,c)` 也在扩展中。Synem 当前要求完整传递闭包、精确绑定、有限无环和权限交集；`bundle`、`collection` 或 `group` 都没有表达这些不变量。

[W3C PROV-DM](https://www.w3.org/TR/prov-dm/)中的 Bundle 是“具名的一组 provenance descriptions”，而 Collection 是具有成员的实体。两者都不能替代 Noemion 的依赖闭包。因此候选必须写成 Endem closure，并由 SYN-CORE 的现行条款继续定义精确绑定和失败责任。

### 有范围证据记录不是 RATS Evidence 或 Attestation Result

[RFC 9334 RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html)分开 Attester 产生的 Evidence、Verifier 依据政策形成的 Attestation Results，以及 Relying Party 的后续决定。Noemion 当前 Iknem 更广：它还区分原始观察、确定性派生、外部断言、人工判断、模型候选和决定记录。

因此候选普通名只描述“这是一项带范围和溯源的证据记录”。外部 RATS Evidence 与 Attestation Result 仍保持来源类别，通过适配规则映射，不能被统称后丢失角色。证据记录的存在也不能自动成为有效性、充分性、满足或最终接受。

## 公开动作候选

普通动词不需要在 PyPI、npm 或 crates.io 全网唯一，因为它们位于唯一顶层命令 `endem` 之下，不是独立包或命令。真正需要取得的发行坐标仍是 `endem`。

| 现行动作 | 首选候选 | 直白职责 | 为什么不用相邻候选 | 不能推出什么 |
| --- | --- | --- | --- | --- |
| `ktise` | `form` | 从受控来源确定性形成一个 Endem | `make/build` 已强烈指向 GNU Make 与构建系统；`create` 太宽，容易掩盖授权投影和规范形成 | form 成功不等于目标满足、签名或 accepted |
| `elenk` | `check` | 按请求层次检查实际制品字节 | `validate` 的常用义包含“批准、使有效”，会混淆 Profile 接受、内容接受和最终决定 | check 通过不等于 met、授权或 accepted |
| `pleko` | `compose` | 把至少两个精确 Endem 解析为完整闭包 | `bundle/group` 不表达完整传递闭包；`link` 容易引入环境搜索与传统链接语义 | compose 不得弱化语义、扩大权限或聚合成员结果 |
| `theor` | `inspect` | 以独立只读路径检查和呈现不可信字节 | `read` 太弱，不能表达独立解析与诊断；`show` 容易被理解为仅格式化 | inspect 不是生产接受，也不能写回 |
| `drase` | `run` | 在有界最小能力域建立一次会话 | `execute` 容易让读者把制品当传统程序；`apply` 暗示直接改变外部状态 | run 完成不等于目标 met 或最终 accepted |

[Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/form)把 `form` 的常用动词义列为“使某物开始存在”或“由多个部分形成整体”；[`check`](https://dictionary.cambridge.org/dictionary/english/check)表示通过检查确认正确、安全或合适；[`compose`](https://dictionary.cambridge.org/dictionary/english/compose)包含“由多个部分组成”。这些词已有登记读音和常用义，桌面风险低于新造动作，但仍必须通过 Noemion 的实际语句听辨和职责匹配。

[`validate`](https://dictionary.cambridge.org/dictionary/english/validate)虽然常见，却也表示使某物正式可接受或获批准，因此不适合承担只到分层检查为止的动作。它会把 ADR-0015 努力分开的检查、满足和最终决定重新混在一个词里。

## 支持案例与反例

| 场景 | 候选表达 | 正确理解 | 失败信号 |
| --- | --- | --- | --- |
| 从受控来源形成最小目标制品 | `endem form` | 只形成符合请求层次的 Endem | 用户以为已签名、已运行或已满足 |
| 检查一个不可信文件 | `endem check` | 返回容器、Profile 与内容层的分开结论 | 用户把“检查通过”听成最终批准 |
| 两个目标存在完整依赖闭包 | Endem closure；`endem compose` | 精确绑定完整闭包，成员结果保持分离 | 用户以为只是把文件打包在一起 |
| 审计者使用独立读取路径 | independent inspector；`endem inspect` | 只读、独立故障路径、无写权限 | 名称被当成已证明独立或可修复文件 |
| 在最小能力域运行会话 | bounded runner；`endem run`；session contract | 重新验证、收窄能力并封存一次会话上限 | 会话完成被写成目标满足或 accepted |
| 保存一项模型评估输出 | scoped evidence record | 类型仍是 model-candidate，范围和限制可见 | “evidence” 被升级为事实或充分覆盖 |
| 接入 RATS Attestation Result | evidence record 的 external-assertion 或适用类别 | 保留 RATS 来源角色、Verifier 和政策 | 外部结果被重新命名后丢失来源与权威边界 |
| 只为图形对称新增第四个组件名 | 不新增专名 | 用职责短语说明责任；无消费者则省略 | 为了词族整齐制造新的难读名称 |

## 人工验证方案

验证必须使用[术语与读音验证指南](../docs/terminology-and-pronunciation.html)的两阶段方法。首轮材料至少包含：

1. Endem 与 Endem closure 的对象选择、听写和职责匹配。
2. scoped evidence record、session contract、deterministic producer、independent inspector 与 bounded runner 的首次朗读和中文技术语境理解。
3. `endem form/check/compose/inspect/run` 的完整命令语句，而不是孤立单词。
4. `check/inspect`、`form/compose` 和 `compose/run` 三组相邻职责反例。
5. “检查通过但未 accepted”“run 完成但目标 unmet”“evidence record 有效但覆盖不足”三类跨域误推导。

候选即使读音完全正确，只要参与者持续匹配到错误职责，也不能通过。普通词的词典读音不能代替项目语境下的人类证据。

## 接受后的迁移清单

若后续证据支持该方向且人类验证通过，后续 ADR 必须一次性完成以下迁移，不保留旧入口：

1. 对象与标准：评估 `SYN-CORE`、`DRO-CORE`、`IKN-CORE` 是否分别改为直白标准 ID，并同步条款前缀、登记、向量目录、诊断域和公开路由。
2. 字段与选择器：直接替换 `required_iknem` 等现行名称；不得双写旧字段或用规范化规则接受旧值。
3. 信任角色：把 Ktisor、Theor、Drasor 的全部现行职责迁移到三个直白角色，保持实现、进程和权限隔离要求。
4. CLI：把五个动作直接迁移为 `form/check/compose/inspect/run`，同步手册、示例、图示、诊断操作名和路线图。
5. 页面与路由：删除旧组件页、旧动作手册路由、旧图片名和旧导航；旧名称只保留在迁移 ADR 与名称审计中。
6. 规范证据：同步支持案例、反例、威胁、正反向量和资料一致性检查；通过只证明新资料一致，不证明组件已经实现。

标准 ID 的具体新拼写、条款前缀和机器对象种类不能由本提案提前冻结。它们必须在迁移 ADR 中逐项证明不会混淆现有 END、SYN、DRO、IKN、DIA、ADP、ID、TEXT-IDENTIFIER 与 AUT 责任。

## 当前决定边界

本提案现在只形成四项候选结论：

1. 发行术语必须先通过专名必要性门禁，再进入冲突和读音门禁。
2. Endem 暂时保留为唯一需要继续验证的新造核心制品名。
3. Synem、Dromen、Iknem、Ktisor、Theor 与 Drasor 应优先去专名化，但现行规范尚未迁移。
4. `form/check/compose/inspect/run` 是公开动作的人类验证候选，不是现行 CLI、别名或实现。

`rhem/semion/skena/telis/krin/apor/phain`、结果词和生命周期词的必要性仍需单独按语义面逐项审查。本提案不以“只保留 Endem”偷渡它们的迁移决定。
