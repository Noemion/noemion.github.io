# Noemion 语言与命名规范

本规范适用于所有正式页面、手册、组件名称、对象名称、工具名称、目录、文件名和导航标签。它解决两个问题：让中文技术文档像开发者之间的正常说明，而不是项目内部提纲；让 Noemion 的专有名称形成可解释、可检索、可长期维护的体系。

## 写作原则

1. 先回答读者要解决什么问题，再说明对象、命令或规则。不要以项目缩写开头要求读者自行推断用途。
2. 使用主动语态和现在时。写“链接器解析符号并报告冲突”，不写“符号将会被解析并给出相关报告”。
3. 一个句子只表达一个主要判断。超过三个并列动作时改用步骤或列表。
4. 主语必须明确。避免“进行处理”“完成支持”“实现相关能力”“提供相应功能”等缺少执行者和对象的说法。
5. 直接描述输入、动作、结果和失败。工具页优先使用“读取什么—检查什么—输出什么—何时拒绝”的顺序。
6. 专业词第一次出现时给出中文直释，再给英文名或缩写。后文只在能够减少歧义时使用缩写。
7. 规范使用“必须、不得、应当、可以”；说明性文字使用“会、用于、负责”。不要用“赋能、打造、沉淀、闭环、拉通、抓手”等宣传或管理套话。
8. 状态说明只写已经完成、正在设计、尚未提供和下一项工作。不要把内部评审问题、提示词或验证清单写给读者。
9. 示例必须说明前提和可观察结果。尚未冻结的命令、扩展名、字段和编号不得写成可直接执行的接口。
10. 手册按任务组织，而不是按实现文件组织；参考章节仍应完整列出对象、选项、错误和索引。

上述规则采用 GNU 文档的长期可读性原则：面向不了解主题的读者、先基础后进阶、首次定义专门术语、按用户问题而非功能清单组织，并优先使用主动语态和现在时。

## 哲学术语的中文用法

| 术语 | 本项目采用的中文 | 使用边界 |
| --- | --- | --- |
| noesis | 意向活动 | 只说明“表达被分析并形成可检验意义”的工程类比；不把软件处理等同于意识活动。 |
| noema | 意向相关项 | 说明同一对象可以通过不同表达方式被给予；工程名称使用 `Noema`，正文首次出现时解释其含义。 |
| intentionality | 意向性 | 表示表达总是关于某个对象、状态或行动；不得简化为日常语言中的主观“意图”。 |
| mode of givenness | 被给予方式 | 用于解释来源表达、上下文和视图如何呈现同一对象，不表示对象由软件任意创造。 |
| identity | 对象同一性 | 表示跨表达、版本和重定位仍可核对的身份关系，不等同于字符串相等或稳定编号。 |
| horizon | 视域 | 表示当前未展开但与解释相关的背景、依赖和可能状态；工程名称使用 `Horizon`。 |
| fulfillment | 充实 | 哲学论述中表示意向与直观相合；面向开发者的工程正文优先写“验收”或“实现结果”，避免生造术语。 |
| constitution | 构成 | 只描述对象意义如何在关系中得到规定；不得暗示编译器创造外部事实。 |

## 核心名称

| 旧称 | 当前名称 | 中文说明 | 正式标识或路由 |
| --- | --- | --- | --- |
| Compiler Core | Noesis Core | 确定性意向编译核 | `components/noesis-core.html` |
| GSL | Noesis Source | 受控的声明式来源语言 | `NSL` |
| GSIR | Noema IR | 意向相关项中间表示 | `NIR`、`specifications/noema-ir.html` |
| GOBJ | Noema Object | 可链接的意向对象文件 | `NOBJ`、`specifications/noema-object.html` |
| SSO | Horizon Object | 按视域逐步披露的共享对象 | `HOBJ`、`specifications/horizon-object.html` |
| Linker / Loader | Noema Object System | 解析、链接、验证和装载对象的系统 | `components/noema-object-system.html` |
| Runtime | Fulfillment Runtime | 在约束下求解并产生可验收结果的运行时 | `components/fulfillment-runtime.html` |
| NSFE | Horizon Engine | 结合来源图、检索和封闭任务头的模型工程组件 | `components/horizon-engine.html` |
| — | Agent Harness | 组织智能体上下文、受限能力、反馈循环与验收证据的外侧控制平面 | `components/agent-harness.html` |
| Strict mode | Deterministic Profile | 不调用模型、结果可复现的确定性配置 | 正文不再使用 `Strict` 作为未解释标签 |
| Assisted mode | Model-assisted Profile | 模型只能提出候选、不能决定对象布局的辅助配置 | 必须同时说明不可信边界 |
| Lowering | realization | 把已验证目标落实为具体执行或产物 | 中文写“实现化”或直接说明具体动作 |
| Satisfaction Contract | Acceptance Contract | 定义结果如何接受或拒绝 | 中文写“验收契约” |
| Coverage Ledger | Evidence Ledger | 记录约束、证据与验收覆盖关系 | 中文写“证据账本” |

`Noemion` 保持为项目名。它由 `Noema` 衍生，但不是缩写。哲学名称提供问题结构，规范、数据结构、不变量和测试提供工程定义。

## 工具命名

Noemion 是项目与对象体系的品牌，不是每个工具命令的强制前缀。命令可以使用直白动作词，也可以使用能够准确说明工程角色的哲学名称；独立名称必须满足可读、可发音、可检索、无明显命令冲突，并在标题和 `--help` 中同时给出直白职责。不能为了系列感给所有工具强造希腊词，也不能让命令名称进入对象魔数、Section 类型或 ABI 身份。

当前先为来源编译、对象成形、只读观察和全局组合四个边界采用独立名称；其他 `noem*` 工具继续保留动作型工作名，直到新的名称确实能提高理解且经过 ADR 记录。

| 旧命令 | 当前命令 | 主要动作 |
| --- | --- | --- |
| `noemconform` | `noemcertify` | 运行一致性测试并生成可复查报告 |
| `noemobj` | `theoria` | 查看对象结构、符号和来源 |
| `noemverify` | `noemvalidate` | 验证结构、完整性和策略 |
| `noemcopy` | `noemtransform` | 执行受控对象变换 |
| `noemsize` | `noembudget` | 统计空间占用和预算 |
| `noemas` | `morphe` | 把 Noema IR 文本汇编为对象 |
| `noemdis` | `noemdecode` | 把对象解码为规范文本视图 |
| `noemfmt` | `noemformat` | 规范化 Noema IR 文本格式 |
| `noemdiff` | `noemcompare` | 比较对象与语义差异 |
| `noemc` | `noesis` | 执行确定性意向编译 |
| `noemlint` | `noemanalyze` | 执行静态语义和策略分析 |
| `noemar` | `noemarchive` | 创建和查看对象归档 |
| `noemnm` | `noemsymbols` | 列出符号、绑定和版本 |
| `noemld` | `synthesis` | 解析依赖并链接对象 |
| `noemstrip` | `noemreduce` | 删除允许移除的开发信息 |
| `noemcov` | `noemcoverage` | 分析证据与验收覆盖 |
| `noempack` | `noembundle` | 生成可验证发布包 |
| `noemrun` | `noemexecute` | 安全装载并执行对象 |
| `noemtrace` | `noemobserve` | 记录执行、证据和来源映射 |
| `noemdata` | `noemdataset` | 构建和验证训练数据 |
| `noemtrain` | `noemtrain` | 训练 Horizon Engine |
| `noemeval` | `noemevaluate` | 评估模型与任务头 |
| `noemquant` | `noemquantize` | 量化并封装模型 |

| 当前命令 | 哲学线索 | 工程职责 | 正式路由 |
| --- | --- | --- | --- |
| `noesis` | 意向活动、理解与判断 | 把受控来源或有来源约束的候选交给确定性 Noesis Core，形成 NIR/NOBJ。 | `tools/noesis/` |
| `morphe` | 形式、结构 | 把显式 Text NIR 确定性编码为对象形式，不解释自然语言。 | `tools/morphe/` |
| `theoria` | 观察、考察 | 只读检查 Header、Section、NIR 记录、符号、重定位与来源。 | `tools/theoria/` |
| `synthesis` | 综合、组合 | 把多个局部对象、符号和约束组合为全局一致对象。 | `tools/synthesis/` |

## 文件与路由

- 文件和目录使用完整的规范名或工具名，不使用已经废止的缩写。
- 正式路由只登记当前名称；不保留旧路由、重定向或兼容别名。
- 手册目录与所属工具同名。例如链接器手册位于 `tools/synthesis/docs/`。
- 路由、导航、页面标题、交叉链接、测试、设计文档和配置必须在同一变更中更新。

## 中文信息架构名称

页面名称必须先说明内容类型，再说明主题。中文站点采用以下固定含义：

| 名称 | 使用场景 | 不使用的含糊写法 |
| --- | --- | --- |
| 项目概览 | 项目目的、范围、现状和主要入口 | 单独使用“了解”作为正式页面标题 |
| 架构设计 | 系统分层、组件关系、对象流和信任边界 | 单独使用“架构”作为页面主标题 |
| 架构决策 | 已采用的职责边界、备选方案和后果 | “架构决定” |
| 入门指南 / 获取与使用指南 / 开发指南 | 帮助读者完成一项任务或形成阅读路径 | 用“文档”概括所有任务型内容 |
| 工具参考指南 / 规范参考指南 | 按工具、对象、术语、成熟度或权威来源查找信息 | 单独使用“工具参考”“规范参考”或“参考” |
| 使用手册 | 单个工具的职责、调用、流程、安全、诊断与索引 | 把工具手册统称为“工具文档” |
| 项目动态 | 已发生且可核对的里程碑、规范变化和发布状态 | “新闻与进展”或暗示固定发布节奏的“新闻” |
| 常见问题 | 对高频问题的直接回答 | 仅使用英文缩写“FAQ” |

导航可以为可用空间使用“项目、规范、工具、指南、开发”等短标签，但展开后的卡片、页面标题和链接文字必须使用上表中的完整名称。项目专有名、规范标识、命令名、对象缩写、视觉状态徽标和已经形成稳定交互含义的英文控件可以继续使用英文；要求是中文部分分类准确、句意完整，而不是机械消除英文。

这套区分参考了中文开发者站点的成熟内容类型：任务型内容使用“指南”或“任务”，定义与查表内容使用“参考”，系统关系使用“架构设计”或“体系结构设计”。Noemion 采用更符合本站既有用语的“架构设计”。

## 逐页检查表

每个正式页面都要核对以下项目：

1. 标题和首段是否直接说明读者问题。
2. 每个项目专有词是否在首次出现时解释。
3. 是否存在无主语的被动句、名词堆叠或管理套话。
4. 输入、处理、输出、错误和当前状态是否具体。
5. 思想来源、工程类比、规范要求和验证事实是否分开。
6. 旧名称、旧路由和未解释缩写是否已经清除。
7. 链接文字是否说明目的，导航是否使用当前名称。

## 参考依据

- MDN，《面向开发者的 Web 技术》：https://developer.mozilla.org/zh-CN/docs/Web
- MDN，《文档写作规范》：https://developer.mozilla.org/zh-CN/docs/MDN/Writing_guidelines/Writing_style_guide
- Microsoft Learn，《Azure 体系结构中心》：https://learn.microsoft.com/zh-cn/azure/architecture/
- Kubernetes，《概念》：https://kubernetes.io/zh-cn/docs/concepts/
- Kubernetes，《任务》：https://kubernetes.io/zh-cn/docs/tasks/
- Kubernetes，《中文本地化样式指南》：https://kubernetes.io/zh-cn/docs/contribute/localization_zh/
- GNU Coding Standards, GNU Manuals: https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html
- GNU Coding Standards, Manual Structure Details: https://www.gnu.org/prep/standards/html_node/Manual-Structure-Details.html
- GNU Hello manual: https://www.gnu.org/software/hello/manual/hello.html
- GNU Binutils 工具清单（`as`、`ld`、`objdump`、`readelf` 等工具不以 GNU 作为命令前缀）：https://www.gnu.org/software/binutils/binutils.html
- 全国哲学社会科学工作办公室，《逻辑研究》——现象学的始基: http://www.nopss.gov.cn/GB/219506/219508/219511/14639916.html
- 南京大学实践与文本，《生活世界现象学导论》: https://ptext.nju.edu.cn/info/1283/7690.htm
