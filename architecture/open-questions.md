---
layout: content
title: 开放问题 · 现在还缺什么证据
page_role: content
footer_text: Noemion · 开放问题
permalink: "/architecture/open-questions.html"
summary: 帮助开发者判断现有资料能否支持下一步；若不能，指出还缺哪种发布定义、运行证据或名称研究。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 架构设计
  url: index.html
page_heading: 开放问题 · 现在还缺什么证据
page_lead: 先确认现行规范允许依赖什么，再判断下一步缺少的是 Profile、运行证据还是名称研究。
badges:
- 当前策略
- 核心责任已确定
- 物理 Profile 待定
- 组件未实现
previous_url: adr-0036-source-bearing-and-stripped-release.html
previous_label: ADR-0036
next_url: "../development/implementation-roadmap.html"
next_label: 开发路线图
---

## 先判断问题处于哪一层

开发者先确定自己要改变的是抽象语义、物理格式、运行机制、公开名称还是实现主张。每一层都需要自己的证据；实现便利不能反向改写已经固定的语义边界。

| 现有材料 | 开发者现在怎么做 | 不能据此声称 |
| --- | --- | --- |
| CORE、Profile 或现行 ADR | 固定精确版本，定位主责任、失败条件和受影响向量 | 规范资料已经成为组件，或不同实现已经互操作 |
| 非规范研究提案 | 提取反例、威胁和候选责任，再回到现有规范寻找唯一归属 | 提案已经增加字段、命令、制品、接口或结果值 |
| 仍待确定的物理 Profile | 说明真实消费者、字节身份、失败责任、版本和正反向量 | 本地 schema、SDK 类型或外部协议对象可以直接代表 Noemion |
| 未来实现与运行证据 | 分别固定平台、输入、工具链、政策、资源限制、对抗条件和实际结果 | 文档构建、概念案例或一次演示已经证明安全、性能或生产可用性 |

现行 CORE 与 ADR 已经划分目标内容、组合闭包、会话契约、有范围证据、诊断、协议适配、身份、文本以及权威决定的责任。END-P2 是含来源的形成与评审 Profile；END-FMT 0.1.0-draft 才是实验性物理容器。closure、evidence、授权事件、受控来源伴随资料和裁剪发布仍没有物理 Profile。

> **停止条件：**当前没有 inspector、政策求值器、权威目录或其他运行组件。缺少物理 Profile 或实现证据时，停在明确的待定边界；不要用 JSON 草图、退出码或构建成功补齐它。

## 用一次字段变更检查是否可以继续

假设开发者准备给 END-P2 增加 `signing_algorithm`，理由是未来发布物需要签名。先不要分配字段号，而要依次回答：

1. **这是谁的责任？** Endem 保存确定内容；ID-CORE、ADR-0027 与 ADR-0035 把签名陈述、外置包络、验证政策、截止点和撤销留在内容身份之外。
2. **现有表示为什么不足？** 签名算法不改变 Endem 的六个语义面，也不是 END-P2 解码所必需，因此不能进入现有内容容器。
3. **真正缺少什么？** 有真实消费者的外部签名 Profile，以及待签字节、算法基线、多签政策、密钥体系、时间来源、撤销和离线包络。
4. **什么证据才能继续？** 消费者、威胁模型、规范字节、错误分层、版本策略、正反向量和独立验证路径。
5. **当前怎样处理？** 保留抽象责任和研究问题，不修改 END-P2，也不增加占位字段。

> 时间、Unicode、摘要、授权事件、协议任务和运行日志都遵循同一顺序：先证明独立消费者与失败责任，再讨论物理字段。

## 按四个问题域继续研究

本节链接的研究提案均为非规范资料：它们帮助开发者定位反例和候选责任，不创建新的 CORE、Profile、制品、命令或组件。展开与当前问题直接相关的一组即可。

### 内容、格式与迁移缺少什么？

- 正式来源语言仍需处理注释、包含、版本、歧义和错误恢复；END-P2 的新增语义必须先有消费者、Profile 与正反字节向量。
- `xor / xone` 、复杂条件和循环需要固定语义、预算和失败原子性；自由脚本不能进入目标格式。
- [语义等价与迁移研究](https://noemion.github.io/spec/semantic-equivalence-and-migration-proposal.html) 分开字节相同、结构同构、有范围观察等价、迁移、强化和弱化；当前没有通用等价布尔值。
- Unicode 结构标识符与原始来源字节需要独立 Profile； [模型参与评测研究](https://noemion.github.io/spec/model-assisted-evaluation-proposal.html) 则把评测目的、构念、调用、原始输出、统计汇总和使用决定分开。

### 组合、发布与外部决定怎样分开？

- closure 的可读名称和版本范围只能定位候选，最终仍需精确绑定； [GNU 与 ELF 适用性研究](https://noemion.github.io/spec/gnu-elf-applicability-proposal.html) 只支持显式引用、形成映射、独立读取和损失披露。
- ADR-0036 与 `END-PUB-001` 已要求含来源形成版和无原文发布版取得不同身份。真正待定的是发布 Profile：它必须逐项定义删除、重写、保留与外置内容，以及来源引用闭包、伴随关系、披露政策和失败原子性。
- 签名验证、行动授权与最终决定分别绑定不同对象、政策、截止点和撤销关系；当前规范已把外部陈述与验证移出 Endem 内容状态。

### Agent 与运行研究怎样继续？

| 开发者问题 | 继续阅读 | 当前可以依赖的边界 |
| --- | --- | --- |
| 模型看到什么，目标和计划怎样保持分离？ | [上下文装配](https://noemion.github.io/spec/model-context-assembly-proposal.html)、[计划与重规划](https://noemion.github.io/spec/planning-and-replanning-proposal.html) | 外部数据没有指令权；目标保持固定，计划只属于受会话契约约束的控制面 |
| 谁在行动，声明能力何时可用，谁能提交副作用？ | [身份与责任链](https://noemion.github.io/spec/software-agent-identity-and-accountability-boundaries-proposal.html)、[能力发现与协商](https://noemion.github.io/spec/capability-discovery-and-negotiation-proposal.html)、[并行与提交](https://noemion.github.io/spec/parallel-and-speculative-execution-proposal.html) | 实际行动者、授权、会话能力、即时可调用性和提交权分别判断 |
| 预览、动作、因果、记忆和恢复能支持什么结论？ | [预览与批准](https://noemion.github.io/spec/preview-simulation-and-approval-proposal.html)、[状态变化与因果](https://noemion.github.io/spec/state-change-and-causal-attribution-proposal.html)、[记忆与恢复](https://noemion.github.io/spec/memory-checkpoint-and-resumption-proposal.html) | 预览不是执行，终态不是因果，检查点不恢复旧会话、秘密或权限 |
| 隔离、训练和发布怎样形成证据？ | [模型与适配隔离](https://noemion.github.io/spec/model-adapter-isolation-proposal.html)、[训练与更新](https://noemion.github.io/spec/model-training-and-update-boundaries-proposal.html) | 机制名称不能替代有效限制；反馈先是记录，派生模型需要新身份、评测和发布决定 |
| 开放模型、托管服务和数据删除怎样陈述？ | [模型开放性与软件自由](https://noemion.github.io/spec/model-openness-and-software-freedom-boundaries-proposal.html)、[托管服务与用户控制](https://noemion.github.io/spec/hosted-ai-service-and-user-control-boundaries-proposal.html)、[数据使用、保留与删除](https://noemion.github.io/spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.html) | 逐对象说明软件权利、服务实例控制、数据路径、导出、保留和清除 |

### 名称与实现怎样进入发行？

- [ADR-0037](adr-0037-terminology-simplification.html) 统一规定现行名称、普通词规则、自造名称证据和机器关键字边界。
- `reach / maintain`、六项语义名称和五个动作都使用单词级普通词规则：检查词首、职责和机器冲突，不因缺少专门人类实验而标为未通过。职责短语只用于说明，不作为登记名称。
- `Noemion` 与 `Endem` 两个自造名称在发行前继续验证完整读音、听写恢复、相邻名称混淆和适用语言范围。
- inspector 仍需自己的数据结构、解码器、验证器、错误路径、差分测试、模糊测试和跨平台证据；可复现构建还需独立产出路径与逐字节比较。

## 外部资料只决定证据类型

**复核日期：**2026-07-16。外部规范和工具帮助确定应收集什么证据，但不会替 Noemion 关闭本地语义、格式或实现问题。

| 资料 | 可以支持 | 不能替代 |
| --- | --- | --- |
| [GNU Manuals](https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html) | 按用户的概念与问题组织教程和参考，不把功能库存当作阅读结构 | Noemion 的规范权威、对象定义或已形成结论 |
| [GNU BFD 信息损失](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html) | 格式转换需要说明源格式、目标格式、不能表示的信息和损失处理 | 跨 Profile 语义等价、无损承诺或物理 Profile |
| [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) | 把产业标准、开放协议、身份基础设施与安全评价作为不同工作轴 | Noemion 的 Agent 对象、授权模型、协议 Profile 或安全结论 |
| [NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models) | 要求模型评测明确目标、适用总体、统计假设和不确定性 | 一次分数自动成为目标满足、证据充分或最终接受 |

## 怎样关闭一个开放问题

1. 写清会改变的对象、使用者、主张和失败后果。
2. 定位现有 CORE、Profile 与 ADR 的唯一主责任，并说明现有表示为什么不足。
3. 给出支持案例、反例、威胁、资源上限和不会采用的替代方案。
4. 涉及物理格式时，提供版本、规范字节、正反向量、错误分层和迁移身份。
5. 涉及组件行为、安全、性能或互操作时，提供对应平台与跨实现运行证据。
6. 涉及普通公开名称时确认它是单个完整单词，再检查词首、相邻职责和冲突；涉及自造名称时再完成目标语言读音与口头区分验证。
7. 由权威规范或 ADR 记录结论、适用范围、替代内容和仍然未知的部分。

**当前策略：**论文、模型指标、概念演示、单一实现行为和文档一致性检查都可以提供输入，但不能单独关闭物理接口或运行主张。

- [架构决策](decisions.html) — 按开发者问题查找现行 ADR、CORE 与停止条件。
- [ADR-0036 · 移除原文，就得到另一份制品](adr-0036-source-bearing-and-stripped-release.html) — 区分已经确定的发布边界与仍待定义的发布 Profile。
- [Agent 系统边界图](agent-system-boundaries.html) — 从一次工具调用检查身份、授权、会话、证据与决定。
- [开发路线图](../development/implementation-roadmap.html) — 查看进入实现前仍需满足的证据条件。
