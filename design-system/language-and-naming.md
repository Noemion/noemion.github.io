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

命令统一使用小写 `noem` 前缀和能够直接说明动作的英文动词。只有已经足够明确的名称保留；传统工具缩写不再作为 Noemion 的公开主名称。

| 旧命令 | 当前命令 | 主要动作 |
| --- | --- | --- |
| `noemconform` | `noemcertify` | 运行一致性测试并生成认证报告 |
| `noemobj` | `noeminspect` | 查看对象结构、符号和来源 |
| `noemverify` | `noemvalidate` | 验证结构、完整性和策略 |
| `noemcopy` | `noemtransform` | 执行受控对象变换 |
| `noemsize` | `noembudget` | 统计空间占用和预算 |
| `noemas` | `noemassemble` | 把 Noema IR 文本汇编为对象 |
| `noemdis` | `noemdecode` | 把对象解码为规范文本视图 |
| `noemfmt` | `noemformat` | 规范化 Noema IR 文本格式 |
| `noemdiff` | `noemcompare` | 比较对象与语义差异 |
| `noemc` | `noemcompile` | 执行确定性意向编译 |
| `noemlint` | `noemanalyze` | 执行静态语义和策略分析 |
| `noemar` | `noemarchive` | 创建和查看对象归档 |
| `noemnm` | `noemsymbols` | 列出符号、绑定和版本 |
| `noemld` | `noemlink` | 解析依赖并链接对象 |
| `noemstrip` | `noemreduce` | 删除允许移除的开发信息 |
| `noemcov` | `noemcoverage` | 分析证据与验收覆盖 |
| `noempack` | `noembundle` | 生成可验证发布包 |
| `noemrun` | `noemexecute` | 安全装载并执行对象 |
| `noemtrace` | `noemobserve` | 记录执行、证据和来源映射 |
| `noemdata` | `noemdataset` | 构建和验证训练数据 |
| `noemtrain` | `noemtrain` | 训练 Horizon Engine |
| `noemeval` | `noemevaluate` | 评估模型与任务头 |
| `noemquant` | `noemquantize` | 量化并封装模型 |

## 文件与路由

- 文件和目录使用完整的规范名或工具名，不使用已经废止的缩写。
- 正式路由只登记当前名称；不保留旧路由、重定向或兼容别名。
- 手册目录与所属工具同名。例如链接器手册位于 `tools/noemlink/docs/`。
- 路由、导航、页面标题、交叉链接、测试、设计文档和配置必须在同一变更中更新。

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

- GNU Coding Standards, GNU Manuals: https://www.gnu.org/prep/standards/html_node/GNU-Manuals.html
- GNU Coding Standards, Manual Structure Details: https://www.gnu.org/prep/standards/html_node/Manual-Structure-Details.html
- GNU Hello manual: https://www.gnu.org/software/hello/manual/hello.html
- 全国哲学社会科学工作办公室，《逻辑研究》——现象学的始基: http://www.nopss.gov.cn/GB/219506/219508/219511/14639916.html
- 南京大学实践与文本，《生活世界现象学导论》: https://ptext.nju.edu.cn/info/1283/7690.htm
