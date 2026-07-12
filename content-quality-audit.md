# Noemion 站点内容、系统闭环与逐页研究审计

## 审计目标与结论边界

本清单覆盖 `sitemap.md` 登记的全部 69 条正式 HTML 路由。审计不只判断页面是否存在，还逐项检查页面承担的读者任务、内容准确性、组件存在价值、上下游关系、产物生产者与消费者、职责与信任边界、验收决定权威、版式可读性和页面跳转。

当前结论只表示站点已经在设计阶段形成可追踪的信息架构和系统关系，不表示 Noemion 已经发布可执行程序，也不表示候选规范、算法、ABI、实验、论文、专利、软件著作权或标准化成果已经形成。实现、测试、实验和第三方互操作证据出现后，相关页面必须重新审计，不能用设计文本替代真实结果。

## 审计方法

每条路由按自身角色选择适用问题，不用同一章节模板衡量门户、目录、专题、规范、工具和手册。

1. **读者问题：**页面服务谁，读者为什么进入，首屏能否给出直接结论。
2. **存在必要性：**组件、工具、视觉区块或导航入口解决什么不可替代的问题；删除后会失去什么能力；能否先与相邻模块共用实现。
3. **自身价值：**页面或组件是否产生独立决策、对象、证据或理解增量，而不是只重复相邻内容。
4. **上下游关系：**每个输入由谁产生，每个输出由谁读取，身份、版本和失败怎样跨边界传递。
5. **职责边界：**编译、对象、装载、会话控制、生成式求解、观察、覆盖、验收和离线评估是否由正确主体承担。
6. **信任属性：**结构合法、来源忠实、签名真实、策略授权、环境一致、证据完整和任务满足必须分别判断，不能压缩成单一“可信度”。
7. **验收闭环：**Candidate Assessment、Evidence Closure Report 与 Acceptance Decision 是否区分；最终决定是否绑定对象、配置、环境、后端、策略、证据和决定权威。
8. **内容准确性：**已确认原则、候选规范、开放问题、开发计划和已验证结果是否明确分开；哲学来源是否只作为问题框架与工程类比。
9. **证据与成熟度：**关键主张是否给出规范、ADR、测试、实验或人工复核的后续位置；尚无证据时是否如实说明。
10. **布局与可读性：**标题、正文、表格、流程、目录、状态栏和图片是否服务阅读；技术长文是否保持可读行宽和层级；移动端是否按语义顺序折叠。
11. **导航与发现：**每页是否能回到直接上级，是否把读者送到下一项真实任务，链接文字是否说明目标而不是只写“更多”。

## 路由与权威源基线

- 正式 HTML 路由：69 条。
- 页面角色：`portal` 1、`section` 10、`content` 22、`tool-project` 23、`docs-index` 1、`docs-topic` 12。
- 权威源：49 个普通 HTML 正文源，20 个 Markdown 手册或指南源；Jekyll 把两类来源统一生成正式 HTML。
- Markdown 权威源包括 7 个跨项目指南和 13 个 `noemlink` 手册页面；目录、分页、面包屑、页头和页脚由共享布局生成。
- `sitemap.md` 是正式路由注册表；目录引擎、入口页、手册索引和上下页导航必须与它共同保持可达，不在 README 或页面正文复制第二套路由表。

## 系统闭环与逐页研究审计

### 组件存在必要性、自身价值与关联

| 组件 | 为什么存在 | 独立价值 | 直接上游与下游 | 可合并或省略的边界 |
| --- | --- | --- | --- | --- |
| Noesis Core | 把来源或受控候选转换为可验证的 NIR/NOBJ，并隔离模型输出与确定性对象形成 | 提供确定性语法、类型、约束、来源绑定和对象布局边界 | 上游是 Noesis Source、Candidate Envelope 与 Source Binding Decision；下游是检查、归档、链接和对象系统 | 逻辑边界不可删除；早期可以作为共享库而不是独立服务。Deterministic Profile 不需要模型组件 |
| Noema Object System | 统一解析、验证、链接、重定位、装载和不可变 Loaded State，防止每个工具重复实现危险对象逻辑 | 把 checked arithmetic、完整性、符号、依赖和装载授权集中在同一可信边界 | 上游是 NOBJ、HOBJ、Release Object 与 Signed Noemion Package；下游是工具链和 Agent Harness | 可以以库形态嵌入工具，但不能让 Runtime 或各工具各自实现不一致的装载与校验 |
| Agent Harness | 在对象与不可信求解后端之间管理会话、上下文、会话级能力、策略、预算、观察和人工升级 | 把 Capability Requirement 与实时句柄分开，并形成可追踪的 Evidence Closure 输入 | 上游是 Loaded State、运行配置和 Capability Request；下游是 Capability Observation、运行证据、覆盖检查与最终决定流程 | 纯静态编译、查看、链接和发布任务不需要完整 Harness；只要任务涉及动态能力或多轮环境反馈，该控制边界就不能交给模型或 Runtime |
| Fulfillment Runtime | 把已装载目标与约束实现为候选结果，并对候选运行局部评价 | 用统一 Runtime Request、Candidate Assessment 和失败分类隔离模型、规则求解器或其他后端差异 | 上游是 Harness 提供的只读语义视图、验收契约、后端配置与 Capability Observation；下游是候选、Capability Request 和 Candidate Assessment | 编译、对象检查、链接与发布不需要 Runtime；具体后端可以替换，但受限请求和候选结果协议不能消失 |
| Horizon Engine | 研究大规模来源聚合、检索路由、稀疏语义图和封闭任务头是否能提升候选解释质量 | 只产生可追溯 Candidate Envelope，为歧义保留和来源绑定提供候选信息 | 上游是版本化语料、Source Graph 和训练数据；下游是 Noesis Core 的确定性复核 | 第一阶段和 Deterministic Profile 均可省略；只有独立证据证明优于确定性规则或外部模型时，才值得形成独立实现 |

这些名称表示必须保持的责任边界，不要求第一版就部署为五个进程。是否拆成独立二进制、库或服务，应由安全隔离、独立版本、资源边界和复用价值决定。Horizon Engine 是候选语义研究组件，Horizon Object（HOBJ）是共享依赖与按视域披露的对象；两者名称相关，但不能互相替代，也不存在“Engine 直接生成 HOBJ”的隐含关系。

### 正式产物的生产者与消费者

| 产物或状态 | 直接生产者 | 直接消费者 | 闭环要求 |
| --- | --- | --- | --- |
| 格式化来源与静态诊断 | `noemformat`、`noemanalyze` | 作者、`noemcompile`、测试与审查流程 | 格式化不能改变语义；诊断必须绑定来源位置和规则版本 |
| Candidate Envelope | Horizon Engine 或经授权的外部模型适配器 | Noesis Core | 绑定来源身份、精确跨度、候选、替代项、证据、置信信息和未决状态；它不是 NIR |
| Source Binding Decision | 授权的确定性规则或人工决定流程 | Noesis Core | 结构合法不能替代来源忠实；无法建立依据时拒绝或保留未决语义 |
| NIR / 可重定位 NOBJ | `noemcompile` 或 `noemassemble` | `noeminspect`、`noemvalidate`、`noemcompare`、`noembudget`、`noemarchive`、`noemlink` | 只有确定性的 Noesis 边界可以形成正式 NIR/NOBJ；Assembly/Compiler Evidence Ledger 伴随来源与转换证据 |
| Archive 与 Symbol View | `noemarchive`、`noemsymbols` | `noemlink`、诊断与人工检查 | 归档成员顺序、符号身份和选择规则必须确定且可复现 |
| Linked Object / HOBJ 闭包 | `noemlink` | `noemvalidate`、`noemreduce`、后续发布流程 | 链接只解析符号、重定位、约束和依赖闭包，不装载裸对象，也不签名 |
| Release Object、Debug Companion 与等价证据 | `noemreduce` | `noemvalidate`、`noemcoverage`、`noembundle`、调试工具 | 删除信息必须证明运行相关语义未变；旧签名在字节变化后失效 |
| Release Coverage Proof | `noemcoverage` 的发布模式 | `noembundle`、审查流程 | 说明发布对象与来源/编译证据的覆盖关系，不等同于签名授权或运行结果正确 |
| Model Qualification Record | `noemevaluate` 对浮点候选或量化包执行离线评估 | `noemquantize`、`noembundle` | 必须绑定模型、数据、基线、评估配置和资格状态；只有 `eligible-for-bundle` 记录可以进入候选发布包 |
| Unsigned Package Candidate 与 Signing Request | `noembundle prepare` | 外部签名系统、`noembundle finalize` | 候选载荷不可变；Signing Request 必须绑定候选摘要、算法、策略和签名范围 |
| Signature Response | 外部签名系统 | `noembundle finalize` | 私钥不进入 Noemion 工具；响应必须绑定原请求、候选身份、签名者和策略版本 |
| Signed Noemion Package | `noembundle finalize` | `noemexecute` 与 Noema Object System | Signature Envelope 只能附加在被签载荷之外；签名只证明来源与完整性，不证明语义正确或运行获准 |
| Loaded State | Noema Object System，在 `noemexecute` 驱动下形成 | Agent Harness | 只包含不可变语义、能力需求与授权上限，不保存实时能力句柄 |
| 候选、Candidate Assessment 与 Capability Request | Fulfillment Runtime | Agent Harness | 仍按不可信结果处理；Harness 校验并执行或拒绝能力请求，再返回 Capability Observation |
| Run Record、Session State、Run Report、Trace Stream 与 Trace Integrity Metadata | `noemexecute` 驱动的 Object System、Harness 与 Runtime 会话 | `noemobserve`、`noemcoverage`、人工诊断 | 全部记录绑定同一对象、配置、环境、后端、策略与会话身份；采样、丢失和截断不得隐藏 |
| Normalized Trace 与 Trace Integrity Report | `noemobserve` | `noemcoverage`、离线诊断 | 规范化不能提升证据强度；必须保留生产者、哈希链、顺序、丢失、采样和截断信息 |
| Evidence Closure Report | `noemcoverage` 的运行模式 | `noemexecute finalize` | 只判断每项验收契约是否有可定位证据，不自动判断主张为真 |
| Run Result 与 Acceptance Decision | `noemexecute finalize` 按执行前固定的 Acceptance Policy 形成 | 开发者、发布流程、人工决定权威与后续离线评估 | 只在必需条款可判定、证据闭合且满足时使用 `accepted`；需要外部判断时保持 `pending-review` |
| 场景或模型离线评估 | `noemevaluate` | 回归分析、模型资格与发布决策 | 不反向修改同一次会话的 Acceptance Decision，也不成为同一次运行覆盖的循环输入 |
| 跨工具一致性报告 | `noemcertify` | 开发者、规范与发布审查 | 检查产物与报告是否符合约定，但不替代签名授权、发布决定或会话验收 |

### 职责、信任与验收闭环

- 工具链按“来源 → NOBJ → 链接对象/HOBJ → Release Object → Release Coverage Proof → Unsigned Package Candidate → 外部签名回填 → Signed Noemion Package → Loaded State → 运行记录 → Evidence Closure Report → Acceptance Decision”形成主链；模型工程是可选支线，只通过带资格状态的 Model Qualification Record 进入发布候选。
- 信任不是沿流水线单调增加的分数。解析验证结构安全，Source Binding 约束来源忠实，签名验证字节来源与完整性，装载策略验证当前环境授权，运行证据记录真实执行，Acceptance Decision 判断任务契约；任何一步都不能替代其他属性。
- Candidate Envelope 不是 NIR，Capability Requirement 不是实时句柄，Candidate Assessment 不是 Acceptance Decision。Runtime、离线评估器和跨工具认证工具都不能自行宣告会话最终成功。
- Agent Harness 可以汇总证据和执行确定性策略，但遇到人工专属判断时必须保持 `pending-review`，由配置指定的外部权威作出决定。
- 所有正式输入都要有生产者，所有正式输出都要有消费者或明确标注只服务人工检查。新增产物还要说明身份绑定、版本、失败责任、签名范围和失效条件。

### 工具与页面是否值得独立存在

23 个工具路由登记的是责任单元和未来用户入口，不等于已经决定发布 23 个独立可执行文件。核心转换与安全边界需要稳定独立契约；只读查询、格式化、预算、符号查看和比较能力可以先共享解析库或作为子命令实现。只有当某项能力具备独立安全权限、发布节奏、资源边界、可复用输出或显著不同的用户任务时，才应升级为独立程序。每个工具页必须继续明确“尚未发布”，避免把路由存在误解成软件已经可安装。

### 内容准确性、布局与导航共同标准

- 入口页先用普通开发者能理解的语言说明问题，再引入 NIR、NOBJ、HOBJ、Agent Harness、Fulfillment Runtime 等术语；规范页随后给出精确定义、规范强度、失败语义和成熟度。
- 哲学来源、工程类比、正式规范与验证事实分别标注。Noema、Noesis、Horizon 和 Fulfillment 只提供问题结构，工程含义由 ADR、数据结构、不变量与测试决定。
- 1200px 是页面画布，不是段落宽度。技术正文保持约 700–760px 阅读列、17–18px 字号和约 1.75–1.8 行高；右侧粘性栏只在持续承载目录、状态、关键对象、输入输出或下一入口时使用。
- 六个及以上二级标题的长专题应提供自动页面目录；宽表格使用自身滚动容器；工具状态摘要只在桌面阅读范围内粘性定位；中小屏幕恢复单列，不能保留无意义空栏。
- 门户、目录、专题、工具项目和手册使用不同信息密度。视觉组件必须承担定位、状态、关系或操作价值；只为填空而存在的图片、边框、卡片和侧栏应删除。
- 非门户页至少提供直接上级入口；手册同时提供动态目录与上下页；聚合页提供分组和快速跳转；链接文字说明点击后能解决的问题。

## 69 条正式路由逐页结论

以下清单按 `sitemap.md` 的内容家族排列。每一行同时记录页面存在价值、与系统或相邻页面的关系，以及内容、布局与跳转的主要检查结论。

### 项目、背景与常见问题（5）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `index.html` | 统一回答 Noemion 解决什么问题、当前形成了什么和从哪里开始阅读；把背景、对象、架构、工具与开发状态串成首条路径 | 保持门户叙事而不是规范堆叠；首屏、核心入口、对象生命周期和当前状态均应指向权威专题，移动端图形不得遮挡主张 |
| `about/index.html` | 作为背景模块目录，区分动机、范围、非目标和思想基础 | 只承担内容地图与边界摘要，不重复三个专题；返回项目门户并分流到背景与思想来源 |
| `about/background.html` | 解释一次性表达为什么不足以支撑可验证、可链接、可重放的机器对象 | 从现实问题进入工程缺口，避免把项目术语当作前提；后续链接到生命周期和 NIR/NOBJ 规范 |
| `about/intellectual-foundations.html` | 记录 Husserl、Frege、Russell 与 Wittgenstein 等思想来源，以及 Noemion 采用和拒绝的工程类比 | 原始来源、版本信息、工程映射和正式语义分开；书目链接可见，类比不充当技术证明 |
| `faq/index.html` | 直接回答名称、对象、Harness/Runtime、可用性和非目标等高频问题 | 问答正文限制阅读宽度，答案先给结论再链接权威页；不在 FAQ 重新定义规范 |

### 架构与组件（10）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `architecture/index.html` | 给出确定性工具链、对象系统、Harness 与 Runtime 的全局关系 | 已区分发布产物链和运行反馈环；信任按属性分别验证，页面目录把读者送到生命周期、决定和开放问题 |
| `architecture/noema-lifecycle.html` | 追踪来源、对象、发布包、装载、运行证据和最终决定的连续身份 | 生命周期覆盖外部签名回填、Capability Request/Observation 和 Evidence Closure；流程与检查点表必须在窄屏独立滚动 |
| `architecture/decisions.html` | 集中登记已采用的跨组件原则，避免同一边界在多页产生不同版本 | 明确“原则已采用”不等于 ABI 已稳定；连接四项 ADR 主题、被排除的捷径和仍需规范的接口 |
| `architecture/open-questions.html` | 保存尚无充分证据的选择，防止实现便利被静默写成既成结论 | 已覆盖候选升级、HOBJ 关系、Runtime 协议、Loaded State、验收权威、身份链和撤销；每项问题指向所影响规范或组件 |
| `components/index.html` | 用统一矩阵解释五个组件为何存在、怎样协作以及删除或合并的后果 | 组件卡片不能只复述名称；入口明确 HOBJ 与 Horizon Engine 的区别，并链接各责任专题 |
| `components/noesis-core.html` | 定义确定性语义提升和 NIR/NOBJ 形成边界 | Candidate Envelope、Source Binding Decision 与未决语义处理分开；类型合法不被误写为来源忠实 |
| `components/noema-object-system.html` | 定义对象解析、链接、装载、完整性和不可变 Loaded State 的共同安全边界 | 不持有签名私钥，也不把实时能力句柄交给 Runtime；Loaded State 交给 Harness 建立受限会话视图 |
| `components/horizon-engine.html` | 记录可选模型研究组件的架构、输入、输出、失败和证据要求 | 当前成熟度与第一阶段边界清楚；只输出 Candidate Envelope，不直接形成 HOBJ 或正式对象 |
| `components/agent-harness.html` | 定义对象系统与不可信求解器之间的会话控制平面 | 输入输出协议覆盖 Capability Request/Observation、预算、观察与人工升级；最终决定权威不属于模型 |
| `components/fulfillment-runtime.html` | 独立说明受限求解、候选评价、能力请求和停止条件，避免与 Harness 混为一体 | 页面明确 Runtime 只输出候选与 Candidate Assessment；仅在需要实现化时启用，并链接装载、观察、覆盖与执行工具 |

### 规范（4）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `specifications/index.html` | 区分对象规范草案、已采用架构原则和其他说明性页面的权威级别 | 成熟度与规范来源可定位，入口链接 NIR、NOBJ、HOBJ 和架构决定，不把原则登记误写为稳定编码 |
| `specifications/noema-ir.html` | 定义目标、约束、歧义、来源绑定、验证计划和验收语义 | 三态评价与 Acceptance Policy 分开，公式只作非规范说明；记录关系不再被误称为四个独立身份 |
| `specifications/noema-object.html` | 定义 NOBJ 的 section、symbol、relocation、dependency、完整性与局部标识 | 区分对象格式、Object System 与 Runtime；说明 HOBJ、生产工具和消费者，并把最终签名范围留给发布包 |
| `specifications/horizon-object.html` | 定义共享依赖、披露触发、闭包计算与可撤销视域 | HOBJ 由链接和对象系统处理，不与 Horizon Engine 混同；披露层、请求、触发和任务拆分条件可追踪 |

### 跨项目指南（7）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `docs/index.html` | 根据“理解项目、理解架构、参与设计、查工具、查规范”组织任务型入口 | Markdown 索引由 Jekyll 生成，目录动态读取正式指南；不复制规范正文 |
| `docs/getting-started.html` | 为首次阅读者建立问题、对象、组件和建议阅读顺序 | 先解释对象化的必要性，再进入 NIR/NOBJ/HOBJ；下一步链接真实专题而非假安装步骤 |
| `docs/installation-and-usage.html` | 如实说明当前没有可安装程序，以及未来发布应满足的签名、验证和使用条件 | 不提供虚构命令、版本或下载；与 downloads、roadmap 和工具目录保持一致 |
| `docs/architecture-guide.html` | 把系统层、主产物链、运行反馈环和信任属性压缩为可读导览 | 不替代架构专题和 ADR；流程名称必须与生命周期和工具页一致 |
| `docs/development-guide.html` | 说明规范优先、ADR、测试、安全审查和贡献路径 | 用实际开发动作和完成标准表达，不把计划写成已实现能力；链接 testing 与 roadmap |
| `docs/tools-reference.html` | 用统一生命周期表说明 23 个工具的输入、输出和直接下游 | 主链与模型支线分开；每个正式产物有生产者和消费者，工具名与各项目页一致 |
| `docs/specifications-reference.html` | 说明规范、ADR、成熟度和阅读顺序 | 只提供权威导航与判读方法，不复制第二套字段定义；架构原则与对象规范草案分开 |

### 开发与资源（6）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `development/index.html` | 聚合当前工作、路线图、测试和参与方式 | 使用已完成、正在进行和后续规划等产品状态；卡片直接进入当前状态、路线图和测试 |
| `development/current-stage.html` | 展示历史完成项、当前设计工作和未来规划 | 时间线来自统一数据配置；左侧/侧栏只保留真实摘要与关键对象，滚动时粘性信息不制造空白 |
| `development/implementation-roadmap.html` | 按依赖顺序说明从规范与安全核心到发布、运行和可选模型工程的实施路线 | 每段列明产物、完成标准和下游使用者；可选分支不阻塞第一阶段，也不承诺日期 |
| `development/testing.html` | 定义确定性、畸形输入、fuzz、互操作、运行证据和验收状态的验证范围 | 测试类型与实际责任主体关联；安全测试不被单一成功样例或离线分数替代 |
| `downloads/index.html` | 作为版本、安装资源、签名、校验、SBOM、撤回与归档状态的唯一公开入口 | 当前明确无发布制品；没有虚构按钮、校验值或平台包，未来资源必须附完整元数据 |
| `news/index.html` | 只记录有日期、有范围、有依据的项目进展 | 当前使用可核对的进展入口而不制造公告历史；每条记录链接状态、规范成熟度或验证计划 |

### 工具目录与工具项目（24）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `tools/index.html` | 把 23 个工具按对象、编译链接、发布运行和模型工程组织为可搜索目录 | 主链、可选模型支线和 Phase 0–8 顺序一致；分组锚点、筛选和卡片均链接正式工具页 |
| `tools/noemcertify/index.html` | 对规范套件和跨工具报告做一致性检查 | 可先作为测试运行器，不替代发布、签名或会话验收；上下游指向规范、测试和各阶段报告 |
| `tools/noeminspect/index.html` | 提供不改变对象的结构、元数据和发布包查看能力 | 可复用 Object System 解析库；独立只读入口有助于审计，输出面向开发者和诊断流程 |
| `tools/noemvalidate/index.html` | 对对象、候选包和签名包执行分层结构、完整性与策略验证 | 安全核心必须存在，可同时提供库与 CLI；验证结果进入链接、发布或执行前检查，但不证明任务满足 |
| `tools/noemtransform/index.html` | 承担显式、可审计的对象复制和允许转换 | 早期可作为对象库子命令；任何字节变化都要产生新身份并使旧签名失效，不能静默重写 |
| `tools/noembudget/index.html` | 报告 section、依赖、披露和发布对象的大小预算 | 属于分析视图，可先与 inspect 共用实现；独立价值在可比较预算报告和回归阈值 |
| `tools/noemassemble/index.html` | 为低级 Noesis Source 提供确定性 NOBJ 入口 | 是 `noemcompile` 的可选同级生产者，不是模型入口；必须产生 Assembly Evidence Ledger |
| `tools/noemdecode/index.html` | 把对象还原为可检查表示，支持审计、调试和重现 | 可先作为 inspect 模式；不能承诺恢复原始来源，输出必须标明不可逆信息 |
| `tools/noemformat/index.html` | 统一 Noesis Source 的稳定格式，减少无意义差异 | 不属于语义核心，可与前端共享解析；格式化必须幂等且保持语义 |
| `tools/noemcompare/index.html` | 比较来源、对象、发布物或运行结果的身份和语义差异 | 可先进入测试工具；必须区分字节相同、结构等价、契约都满足和不可比较 |
| `tools/noemcompile/index.html` | 把来源或受控候选确定性转换为 NIR/NOBJ | 主链核心生产者；必须处理 Candidate Envelope、Source Binding Decision 和歧义，模型不能直接产出对象 |
| `tools/noemanalyze/index.html` | 在编译前后提供静态规则、约束和来源问题诊断 | 可共享 Noesis 前端；输出反馈给作者、编译和测试，不改变对象身份 |
| `tools/noemarchive/index.html` | 为多对象工程建立确定性归档与成员索引 | 单对象第一阶段可省略；规模化链接需要稳定成员顺序、身份和选择规则 |
| `tools/noemsymbols/index.html` | 提供符号、定义、引用和绑定的只读视图 | 可先作为 inspect 子命令；独立价值在链接诊断和可脚本化 Symbol View |
| `tools/noemlink/index.html` | 解析符号、重定位、约束和 HOBJ 依赖闭包 | 多对象与共享依赖场景的主链核心；输出交给验证、reduce 和发布，不直接签名或装载裸对象 |
| `tools/noemreduce/index.html` | 删除允许移除的开发信息，形成 Release Object 与 Debug Companion | 发布前才需要；必须输出摘要、等价证据和旧签名失效信息，不能删除运行必需语义 |
| `tools/noemcoverage/index.html` | 分别检查发布证据覆盖和运行验收证据闭合 | 两种模式产物不同：Release Coverage Proof 给 bundle，Evidence Closure Report 给 execute finalize；它不作最终决定 |
| `tools/noembundle/index.html` | 建立不可变候选包、签名请求并验证外部签名回填 | 只在分发时需要；prepare/finalize 都绑定同一候选身份，工具不持有私钥也不自行签名授权 |
| `tools/noemexecute/index.html` | 驱动验证、装载、Harness、Runtime、观察记录与最终决定流程 | 运行支持的主入口；Runtime 阶段保持 `pending-evidence`，只有 finalize 可根据 Evidence Closure 和固定策略形成 Acceptance Decision |
| `tools/noemobserve/index.html` | 把原始 Trace Stream 规范化并检查完整性 | 与执行解耦便于离线诊断和多采集器兼容；规范化不掩盖丢失、采样、截断或来源问题 |
| `tools/noemdataset/index.html` | 建立训练/评估数据的版本、许可、谱系、划分和泄漏检查 | 仅服务可选模型支线；第一阶段可省略，输出给训练和评估而不进入确定性对象核心 |
| `tools/noemtrain/index.html` | 产生可追溯 Checkpoint Candidate 与 Training Manifest | 可选研究工具；不能把训练完成当作模型资格，输出必须先进入离线评估 |
| `tools/noemevaluate/index.html` | 对浮点模型、量化包或完成会话做离线基准、回归和资格判断 | 同时服务模型资格与事后场景评估，但不修改单次会话决定；结果绑定数据、基线、配置和对象身份 |
| `tools/noemquantize/index.html` | 把已评估的模型候选转换为 Model Package Candidate 并报告量化影响 | 可选部署工具；不自行批准或签名，量化包必须再次评估后才可能进入 bundle |

### `noemlink` 手册（13）

| 路由 | 存在价值与关联 | 审计结论 |
| --- | --- | --- |
| `tools/noemlink/docs/index.html` | 动态组织 linker 手册阅读顺序、分组和术语入口 | Markdown 权威源通过 Jekyll 生成；目录、移动索引和上下页不手工复制 |
| `tools/noemlink/docs/contract.html` | 定义 noemlink 负责和不负责的稳定责任边界 | 明确只处理解析、重定位、约束和依赖闭包；不渲染提示词、不签名、不执行 Runtime |
| `tools/noemlink/docs/inputs-outputs.html` | 列明接受的 NOBJ、Archive、HOBJ 描述、策略与输出对象/报告 | 裸链接输出只能进入验证、reduce 和发布准备，不能直接当作已签包或 Loaded State |
| `tools/noemlink/docs/invocation.html` | 记录尚未冻结的 CLI 结构、顺序输入和确定性调用约定 | 示例使用中性占位符而非伪造扩展名；参数候选不构成稳定接口 |
| `tools/noemlink/docs/pipeline.html` | 解释摄取、规范化、符号解析、重定位、闭包、布局和发射的内部顺序 | 内部自检与独立 `noemvalidate` 分开；每步失败终止条件可定位 |
| `tools/noemlink/docs/symbol-resolution.html` | 规定定义、引用、可见性、冲突和未解析符号的确定性选择 | 排序与冲突规则绑定稳定键；不依赖文件系统枚举或并行完成顺序 |
| `tools/noemlink/docs/relocations.html` | 说明类型化重定位、范围检查、标识重映射和溢出失败 | 使用 checked arithmetic；未知类型、越界、错位和重复应用都有明确拒绝语义 |
| `tools/noemlink/docs/horizon-linking.html` | 说明 HOBJ 共享依赖、披露请求和闭包形成 | 区分 Disclosure Request、Trigger 与 Task；Object System 负责装载时闭包，不把责任交给 Runtime |
| `tools/noemlink/docs/loader-security.html` | 从链接输出追踪到签名包验证和安全装载 | 明确 loader 只接受 bundle 形成的 Signed Noemion Package；结构、完整性、策略和资源限制分别检查 |
| `tools/noemlink/docs/diagnostics.html` | 统一错误分类、位置、稳定排序和可安全公开的信息 | 诊断既供开发者定位，也可进入自动测试；不得泄漏敏感载荷或依赖非确定顺序 |
| `tools/noemlink/docs/testing.html` | 建立确定性、畸形输入、fuzz、属性、互操作和全链路测试矩阵 | 覆盖链接到验证、reduce、coverage、bundle、execute、observe 和最终决定，不把单元测试当作发布证明 |
| `tools/noemlink/docs/dependencies.html` | 把 noemlink 的上游来源和下游发布/运行证据链集中列明 | 生产者与消费者名称和主产物链一致；避免文档之间形成循环依赖或无人读取的正式输出 |
| `tools/noemlink/docs/reference-index.html` | 为命令、对象、状态和术语提供可扫描索引 | 使用通用 Markdown 表格，术语链接到权威专题；候选名和稳定定义保持区分 |

## 逐类布局、可读性与跳转检查

| 页面角色 | 布局价值 | 可读性检查 | 必要跳转 |
| --- | --- | --- | --- |
| `portal` | 用首屏、主张、对象图形和横向入口建立整体叙事 | 图形不遮挡文本，动画表达数据流且支持减少动态效果；移动端保持主行动可见 | 背景、架构、对象生命周期、文档和当前状态 |
| `section` | 用分组列表和紧凑摘要建立内容地图 | 不复制专题长文；筛选和分组关闭脚本后仍保留全部内容 | 直接上级、全部子页和相关权威入口 |
| `content` | 用编辑式文章、流程、对照表、交错论述和必要侧栏展开一个论点 | 普通正文不占满画布；六个以上二级标题提供页面目录；侧栏无真实内容时回到单列 | 上级目录、论据来源、相邻专题和下一阅读项 |
| `tool-project` | 主阅读列说明六项用户问题，状态摘要持续提供可用性和关键输入输出 | 状态栏只在桌面粘性定位，手机回到正文顺序；表格与长命令不产生整页溢出 | 工具目录、上游规范/组件、直接下游和实际手册 |
| `docs-index` / `docs-topic` | 固定手册目录、阅读区和动态分页支持连续任务 | 正文与表格保持局部滚动；移动目录锁定背景滚动并可点击外部、再次点击、滚动或 Escape 关闭 | 手册上级、动态章节、上一页/下一页和术语索引 |

## 完成判定与持续审计

单条路由只有同时满足以下条件，才能视为达到当前设计阶段的内容质量要求：

- 页面职责不可由相邻页面简单替代，或已明确它只是必要的目录/索引入口；
- 组件和工具说明清楚存在价值、可省略场景、上游输入、下游输出和失败责任；
- 产物名称、生产者、消费者、身份与状态在架构、规范、组件、工具和手册之间一致；
- 规范事实、已采用原则、开放问题、开发计划和已验证结果没有混写；
- 版式服务真实内容，正文、表格、目录、状态栏和移动折叠保持可读；
- 每个非门户页有明确上级路径，关键结论能进入权威来源或下一项实际任务；
- 源码检查、Jekyll 构建、构建产物检查和多宽度浏览器验收均使用同一变更版本完成。

## 2026-07-12 验证记录

- 源码检查逐项核对 69 条正式路由、49 个 HTML 正文源和 20 个 Markdown 权威源；Jekyll 成品检查再次核对 69 个 HTML、34 个全局入口、手册目录和正式路由注册表。
- 浏览器以 1512px 桌面和 390px 手机逐条打开 69 条路由；桌面浅色、桌面深色与手机结果均没有整页横向溢出、空正文区段、缺失标题、图片加载失败或浏览器错误。
- 文档布局额外检查 1218、1217、1100、1000、999、840、839 和 390px：固定目录只在 1218px 及以上显示；1000–1217px 正文归中；839px 及以下菜单按钮与面包屑同排。
- 交互检查覆盖桌面导航悬停展开、卡片逐项进入与封面反馈、5px 循环频谱框线、550ms 箭头圆环、移动目录背景冻结与外部手势收回、主题跨页面保持、长文页内目录跳转、Markdown 表格独立横向滚动、项目摘要和工具状态卡粘性定位。
- 外部书目与工程依据链接重新检查；失效的 Google Books 入口已经替换为出版社或稳定书目记录，访问控制返回 403 的站点仍保留其可由浏览器访问的权威 URL，不误写为站内故障。

当前 69 条路由已完成上述内容与关系审计，形成设计阶段的信息闭环。最终发布仍必须以同一版本的源码检查、Jekyll 构建、构建产物检查、桌面与移动浏览器复核为依据；任何新路由、新工具、新对象、新运行状态或新研究结论都要同步更新 `sitemap.md`、目录与本审计。
