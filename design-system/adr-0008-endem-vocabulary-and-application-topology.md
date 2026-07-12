# ADR-0008：Endem 词汇与应用拓扑

- 状态：Accepted
- 日期：2026-07-12
- 影响范围：公开术语、对象规范、组件、应用、CLI、路由、手册、实现切片与测试
- 取代：ADR-0001、ADR-0003、ADR-0005、ADR-0006、ADR-0007
- 部分保留并重新映射：ADR-0002、ADR-0004

## 问题

旧设计围绕多层中间表示、对象家族、五个组件和 23 个工具职责展开。它虽然为每项内部操作写明了边界，却让传统对象工具的分工反过来决定生成式计算产品：用户需要先理解一组格式、转换、符号、归档、裁剪、覆盖、跟踪和模型工程名称，才能表达最基本的自然语言目标。

Noemion 要建立的新底层不是 GNU 工具的生成式复刻，而是让一项自然语言目标成为持久、可组合、可受控运行并可按证据验收的最小制品。因此需要冻结更少的对象、组件和应用名称，并把只读观察与隔离运行落实为实现和权限边界，而不是继续扩大公开命令数量。

## 决定一：Endem 是唯一根制品

采用 **Endem · 最小目标制品**。一个 Endem 必须且只能有一个根 `aim`，并保存五组规范语义：

| 字段组 | 职责 |
| --- | --- |
| `say` | 精确保存用户或权威来源实际表达的内容、身份、语言、范围和版本。 |
| `aim` | 保存唯一根目标、结果种类和预期产物角色。 |
| `must` | 保存硬约束、能力上限、禁止事项、作用域、冲突与未知处理。 |
| `done` | 保存结果结构、验收条件、必需 Witness、失败状态和决定权威。 |
| `open` | 保存替代解释、冲突、缺口、风险、解决策略和有权绑定的主体。 |

任意自然语言或模型输出不能直接成为 Endem。候选只有在能够由版本化规则重新推导、绑定明确授权决定，或继续显式保留为 `open` 时，才能进入确定性成形路径。

Endem 不保存思维链、模型权重、运行计划、实时能力句柄、凭据、私钥或会话内存。正式文件扩展名采用 `.endem`；扩展名只标识制品入口，不替代魔数、版本和结构验证。

## 决定二：同一 Endem 沿三个状态演进

同一制品使用 `open → bound → sealed` 状态，不再通过平行对象家族表达每个中间阶段：

- `open`：结构合法，但仍含未决语义、引用或确认事项；不能直接发布运行。
- `bound`：必需引用、冲突、能力上限和验收关系已经取得确定结论；不表示来源可信或任务完成。
- `sealed`：发布载荷冻结，并与外部 Signature Response 精确绑定；不表示当前环境授权或语义正确。

状态变化保持 Endem 的来源链和规范语义身份，但产生新的精确文件摘要。seal 后不得原地改写被签载荷。

## 决定三：Weave、Frame 与 Witness

采用三个直白职责术语：

1. **Weave · 多目标解析闭包**：两个或更多 Endem 通过显式 Binding Policy 和内容寻址依赖形成的已解析组合。每个成员继续只有一个根 `aim`；权限只能保持或收紧。单一自包含 Endem 不需要 Weave。
2. **Frame · 运行时只读视图**：Runner 针对一次会话从 sealed Endem/Weave、执行策略、当前环境和授权能力建立。Frame 不是文件、包成员、对象种类或可跨会话复用的句柄；它不得包含实时凭据或能力句柄。
3. **Witness · 可定位证据记录**：对来源、检查、绑定、签名、运行或决定作出范围有限的主张，并绑定对象、环境、生产者、规则和完整性材料。Witness 不等于数学证明、事实自动为真或 Acceptance Decision。

## 决定四：唯一公开应用和 CLI

唯一公开应用与命令行入口都叫 `endem`。只冻结以下八个动作：

| 动作 | 职责 | 不得跨越的边界 |
| --- | --- | --- |
| `form` | 把 Goal Card 或已授权候选确定性形成 open Endem。 | 模型不能决定确认语义或物理布局。 |
| `check` | 用生产读取路径分层检查结构、语义、状态、完整性与策略。 | 未执行层不得显示为通过。 |
| `bind` | 解析引用和冲突，形成 bound Endem 或 Weave。 | 不读取环境隐式路径，不扩大权限。 |
| `pack` | 冻结发布闭包、调试伴随内容和 Signing Request。 | 裁剪不得改变 aim/must/done/open。 |
| `seal` | 核对外部 Signature Response，并附加签名封装。 | 不持有私钥，不修改被签载荷。 |
| `see` | 用独立直接 Reader 查看、比较和导出有界视图。 | 不共享生产解析，不生成 Verified Handle。 |
| `run` | 在隔离 Runner 中重新验证、建立 Frame、调用后端和形成 Witness。 | 不拥有 Core Writer，不让后端持有实时句柄或自行验收。 |
| `test` | 运行规范向量、双 Reader 差分、恶意语料和复现检查。 | 不冒充第三方认证、发布授权或任务验收。 |

公开路由采用 `/endem/index.html` 与 `/endem/docs/`，不保留旧工具路由、别名或重定向。

## 决定五：三个组件

只保留三个具有不同信任、权限和失败责任的组件：

- **Core · 确定性制品核心**：唯一能够写规范 Endem/Weave；承担 form、生产 check、bind、pack 和 seal。
- **Reader · 独立只读检查器**：为 see 提供不共享 Core Reader/Writer、绑定器、生成代码或错误实现的第二条直接读取路径。
- **Runner · 隔离实现运行器**：为 run 重新验证 sealed 字节、建立 Frame、控制会话级能力、隔离后端并形成 Witness 与决定。

三个组件可以随同一发行包提供，但 Reader 的代码独立和 Runner 的权限隔离必须由依赖检查、进程/沙箱边界和测试机械保证。模型工程、训练、量化和协议适配不是第一阶段组件；没有超出现有平台的不可替代价值时不建设重复系统。

## 决定六：命名检索与正式商标 gate

Endem、Weave、Frame、Witness、`.endem` 与 `endem` 命令已作为项目内部名称冻结。冻结不等于商标可注册、域名可取得或不存在第三方权利。

命名采用两级检查：

1. 开发阶段执行命令、包管理器、GitHub、语言生态、域名、公司和近似产品的字面检索，记录日期、范围和冲突候选。
2. 公开发行前执行正式 gate：目标法域商标数据库、相同及近似类别、软件和开发工具类别、包名与域名，以及律师或合格知识产权人员复核。

正式 gate 未通过时，名称变更必须进入新的命名 ADR；名称调整不得静默改变五组语义、状态机、对象身份或 ABI。

## 外部机制的采用边界

- GNU `readelf` 独立于 BFD 的做法用于证明第二条直接读取路径的价值；Reader 不复制 ELF 地址或机器指令语义：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- BFD 的多格式 canonical form 不进入第一阶段可信核心，Core 与 Reader 都使用格式专用、有界、可逐字段审计的实现：https://sourceware.org/binutils/docs/bfd.html
- MCP 只作为 Runner 外缘的工具、资源和上下文交换协议；远端声明、注解和结果不是权限或事实：https://modelcontextprotocol.io/specification/2025-11-25
- A2A 的 Task 与 Artifact 只用于跨系统任务交换，不定义 Endem、Frame、Witness 或最终验收：https://a2a-protocol.org/v1.0.1/specification/
- OpenAI Harness Engineering 提供版本化知识、环境可读性、反馈循环和机械边界的实践依据，不决定 Endem 格式或成熟度：https://openai.com/index/harness-engineering/

## 被取代与保留的决定

| 旧 ADR | 状态 | 当前处理 |
| --- | --- | --- |
| ADR-0001 | Superseded | 旧四层对象和组件公开命名由 Endem 词汇取代。 |
| ADR-0002 | Retained in part | 模型不可信、能力句柄隔离、预算和人工升级原则进入 Runner。 |
| ADR-0003 | Superseded | 多份平行主产物收敛为 Endem/Weave、外部签名材料与 Witness。 |
| ADR-0004 | Retained in part | 候选不等于事实、能力声明不等于句柄、证据不等于验收继续有效。 |
| ADR-0005 | Superseded | 多工具名称收敛为 `endem` 与八个动作。 |
| ADR-0006 | Superseded | 保留安全解析原则，格式围绕五组 Endem 语义重新设计。 |
| ADR-0007 | Superseded | 首条切片改为 Goal Card → form → Endem → check/see → test。 |

## 第一条实现切片

第一阶段只实现：

```text
Goal Card
  → endem form
  → open .endem
  → endem check（生产 Reader）
  → endem see（独立 Reader）
  → endem test（差分、恶意语料与复现）
```

`bind`、Weave、`pack`、`seal`、Runner、Frame、运行 Witness、模型和外部智能体协议，必须等待最小格式、两条读取路径、恶意语料和字节复现稳定后再进入。

## 后果与未冻结内容

- 旧规格、组件、工具页面和路由直接删除，不保留兼容入口。
- 所有公开说明、导航、手册、测试和样例使用同一词汇与状态机。
- 名称、五组语义、一个根 aim、三个状态、`.endem`、八个动作与三组件拓扑已经冻结。
- 魔数、字段宽度、记录编号、Goal Card 文本语法、Weave/Witness 扩展名、摘要与签名算法、Frame API、Witness 编码、退出状态、安装包和稳定 ABI 仍未冻结。
