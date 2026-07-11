# Noemion 站点 HTML 内容质量审查清单

## 目标

本清单跟踪 `noemion.github.io/` 仓库全部 HTML 的内容完整性。路由存在、链接有效或测试通过只证明站点结构成立，不证明页面已经达到博士研究、论文、专利、软件著作权或行业标准候选所需的内容深度。

## 审查尺度

本清单中的维度是审查问题库，不是所有 HTML 共用的章节模板。每页先按本仓库 `README.md` 判断模块属性、读者任务和内容规范，再选择与其职责相关的维度；不要求目录、文档、规范、工具、资源、新闻和 FAQ 具有相同结构，也不以关键词、章节数或字符数替代人工判断。

可选审查维度如下：

1. 问题背景：受众、场景、痛点与为什么值得解决。
2. 范围边界：职责、非目标、前置条件和不适用范围。
3. 概要设计：系统关系、主要对象、数据或控制流、信任边界。
4. 详细设计入口：接口、状态、数据结构、算法、错误语义或专题链接。
5. 证据与验证：可测试主张、方法、数据、基线、失败案例和可复现条件。
6. 状态与风险：已确认、提案、开放问题、未来阶段和剩余风险。
7. IPD 治理：当前阶段、进入条件、退出证据和下一决策门。
8. 研究与知识产权：研究问题、可证伪假设、创新点候选、现有技术边界、公开披露与权属风险。
9. 标准化：稳定术语、规范性条款、互操作 Profile、一致性测试和安全分析。
10. 追溯性：页面、规范、ADR、测试、实验、版本与产物之间能够互相定位。

## 基线盘点

- HTML 总数：66。
- 页面角色：`portal` 1、`section` 10、`content` 19、`tool-project` 23、`docs-index` 1、`docs-topic` 12。
- 初始机器辅助扫描仅用于确定审查优先级：明确背景/动机线索 26 页，概要设计线索 16 页，IPD 阶段线索 3 页，研究或标准化线索 2 页。
- 上述数字不是完成率；关键词出现不代表论证充分，关键词缺失也不必然代表页面错误。

## 第一轮已补强，仍需证据审查

- `index.html`
- `about/index.html`
- `architecture/index.html`
- `specifications/index.html`
- `components/index.html`
- `tools/index.html`
- `docs/index.html`
- `downloads/index.html`
- `development/index.html`
- `news/index.html`
- `about/background.html`
- `about/intellectual-foundations.html`
- `architecture/object-lifecycle.html`
- `architecture/open-questions.html`
- `specifications/gsir.html`
- `specifications/gobj.html`
- `specifications/sso.html`
- `components/compiler-core.html`
- `components/linker-loader.html`
- `components/nsfe.html`
- `development/implementation-roadmap.html`
- `development/testing.html`
- `development/current-stage.html`
- `faq/index.html`
- `docs/getting-started.html`
- `docs/installation-and-usage.html`
- `docs/architecture-guide.html`
- `docs/development-guide.html`
- `docs/tools-reference.html`
- `docs/specifications-reference.html`
- `tools/noemconform/index.html`
- `tools/noemobj/index.html`
- `tools/noemverify/index.html`
- `tools/noemcopy/index.html`
- `tools/noemsize/index.html`
- `tools/noemas/index.html`
- `tools/noemdis/index.html`
- `tools/noemfmt/index.html`
- `tools/noemdiff/index.html`
- `tools/noemc/index.html`
- `tools/noemlint/index.html`
- `tools/noemar/index.html`
- `tools/noemnm/index.html`
- `tools/noemld/index.html`
- `tools/noemstrip/index.html`
- `tools/noemcov/index.html`
- `tools/noempack/index.html`
- `tools/noemrun/index.html`
- `tools/noemtrace/index.html`
- `tools/noemdata/index.html`
- `tools/noemtrain/index.html`
- `tools/noemeval/index.html`
- `tools/noemquant/index.html`
- `tools/noemld/docs/index.html`
- `tools/noemld/docs/contract.html`
- `tools/noemld/docs/inputs-outputs.html`
- `tools/noemld/docs/invocation.html`
- `tools/noemld/docs/pipeline.html`
- `tools/noemld/docs/symbol-resolution.html`
- `tools/noemld/docs/relocations.html`
- `tools/noemld/docs/sso-linking.html`
- `tools/noemld/docs/loader-security.html`
- `tools/noemld/docs/diagnostics.html`
- `tools/noemld/docs/testing.html`
- `tools/noemld/docs/dependencies.html`
- `tools/noemld/docs/reference-index.html`

这些页面已增加问题背景、黄金圈定位、概要设计、规范不变量、验证证据、IPD 或研究/标准化治理内容。下一轮仍需检查术语一致性、主张与证据链接、现有技术对比和可验证条款。

项目、架构、规范、组件、治理与任务型文档已全部进入“第一轮已补强”。下一轮按主张逐项检查术语一致性、现有技术对比、规范条款和真实证据链接。

23 个工具项目页均已在既定六个章节内补足具体问题、上游输入、下游消费者、概要流程、关键不变量、失败边界、阶段门、验证证据和详细文档建立条件。下一轮仍须逐项核验工具间的状态术语、输入输出名称和主张—证据链，不把结构完整误判为设计已经冻结。

`noemld` 文档中心及 12 个专题页已补入输入输出契约、状态与数据结构、冲突规则、确定性算法、资源限制、诊断设计、测试矩阵、威胁模型、依赖契约与术语成熟度。具体字段、编号、ABI 和 Profile 仍明确保留为待规范或 ADR 冻结的开放设计。

## 第二轮跨页证据审查结果

- **术语与阶段：**已核对 GOBJ 工程名、AELF/GRO/SRO/ARO 候选名、GSIR、SSO、Strict、Compiler Core 和 Phase 0–8。发现并修正工具目录把 9 个技术 Phase 误写为 8 个的问题。技术 Phase 与 IPD 管理阶段已明确区分。
- **状态表述：**23 个工具项目页均明确“设计阶段、无已发布可执行程序、CLI/参数/扩展名未冻结”；下载、使用、开发、FAQ、新闻和首页没有把未来能力表述为现有制品。
- **研究与知识产权：**页面只登记研究问题、可证伪假设、现有技术比较、论文/专利/软著/标准化证据路线与公开披露纪律，没有声明已经发表、授权、登记或获标准组织采纳。
- **主张与证据：**关键架构和工具主张已映射到规范页面、ADR 要求、阶段门、测试矩阵、威胁模型或明确的未来证据。尚不存在的原型、实验、互操作报告和独立实现被标为未形成，未用设计文本替代真实证据。
- **对象与路由：**README 机器可读注册表、实际 HTML、页面角色、共享目录配置和上级入口一致；66 个路由各登记一次，23 个工具项目页和 noemld 13 页文档子树均可定位。
- **浏览器验收：**66/66 页面均以最新 Jekyll 成品逐页复查。桌面端全部具有唯一正文、标题、活动目录、非空章节、无整页横向溢出和等宽网格；首页保持独立叙事门户，内页继续使用模块目录与正文布局。390px 移动端再次逐页检查，无整页溢出，长表格保持在自身滚动容器内；浏览器控制台无错误或警告。
- **动画与可访问性：**首页首屏按 90ms 间隔分组进入，对象图形使用低频 transform 动画；横向入口增加只在悬停或键盘聚焦时出现的 Noemion 四色频谱描边，并组合图形 1.025 放大、标题与箭头 4px 位移、0.25→1 图标交叉切换。浏览器已验证悬停终态与可中断 transition；CSS 为 `prefers-reduced-motion` 取消描边流动、进入、循环与空间位移动效，并保留 44px 以上行动区域。

当前 HTML 内容架构审查已经完成，但这只表示设计信息、状态边界和证据路线已覆盖，不表示 Noemion 的技术主张已经被实现或验证。未来形成规范条款、ADR、源码、测试、实验、论文、专利材料或互操作报告时，仍应沿现有路由逐项回填真实证据并重新审查。

## 可读性复审基线

几何可读性检查不再只验证横向溢出，同时测量段落实际行宽、字号、行高和粘性信息栏职责。当前成品已把技术专题、工具说明和手册主正文统一到桌面 18px / 32.04px；普通正文保持约 700–760px，工具主阅读列实测 689px，手册阅读列实测 760px。工具 Hero 的右侧视觉列与正文 800px / 400px 双栏重新对齐，状态卡在主内容范围内保持粘性；390px 下恢复单列且无整页横向溢出。

工具目录现提供渐进增强的关键词搜索与对象、编译链接、发布运行、模型工程分组筛选；关闭脚本时仍完整显示 23 个工具。新闻与进展页以三条横向记录行链接项目进度、规范成熟度和验证计划，不生成虚构公告或发布日期。

- 首页采用“直白主张 → 意义对象缺口 → 四条核心阅读路径 → 当前设计焦点 → 对象生命周期 → 证据与治理门 → 名称和方法边界 → 下一步入口”的顺序；内容、图形、状态语言和语义频谱均属于 Noemion。
- 全站入口页应先使用读者语言解释问题，再引入项目术语；专题页可以更技术化，但必须保留前置知识、状态和权威来源。
- Noesis/Noema、意义与指称等思想只用于解释设计视角，正式语义仍以规范、ADR、数据结构、不变量和测试为准。
- 后续逐页评审不仅检查内容是否存在，还要检查论点顺序、术语首次解释、链接预期和思想来源与工程结论是否混淆。

## 完成判定

单页只有同时满足其角色要求、权威边界明确、关键主张有证据路线、风险与未决项未被隐藏，并通过链接与浏览器检查后，才能从“待深审”移入“已完成”。本轮 66 页均已达到设计阶段的 HTML 内容门；任何未来实现或研究成果仍必须以新增的真实证据重新触发对应页面审查。

## 公开读者与规范权威性复审

本轮逐个核对 66 个正式 HTML，受众统一为开发者、普通用户和潜在使用者。公开内容只描述 Noemion 的问题、概念、规范、工具职责、使用场景、真实状态和证据边界，不披露用户指令、内部生成过程、内容补写、幕后 review 或页面制作过程。

| 模块 | 路由数 | 本轮检查重点 | 结论 |
| --- | ---: | --- | --- |
| 项目门户与背景 | 4 | 首次访问者叙事、项目边界、思想来源、研究状态 | 解释与工程结论分开；书目来源保留原始 URL |
| 架构 | 3 | 生命周期、信任转换、开放问题、失败位置 | 继续保留不变量、未决项和可审计证据 |
| 规范 | 4 | 权威性、成熟度、规范强度、编码与语义边界 | GSIR/GOBJ/SSO 增加直白解释，但不削弱“必须/不得”和失败语义 |
| 组件 | 4 | Compiler、Linker、Loader、Runtime、NSFE 的职责隔离 | 候选模型、确定性核心和对象边界保持清楚 |
| 开发、资源与 FAQ | 10 | 当前可用性、贡献渠道、发布纪律、知识产权与证据等级 | 删除推测入口和制作过程表述，保留真实未发布状态 |
| 工具项目页 | 23 | 使用问题、状态、输入输出、阶段门、处理边界、未冻结接口 | 全部工具页改为面向使用者的产品状态，不再讨论页面或文档制作 |
| noemld 文档 | 13 | 契约、流程、算法、安全、诊断、测试、依赖和术语权威性 | 设计契约与已发布手册严格区分，候选示例不构成稳定 ABI |
| **合计** | **65** | 公开表达、技术严谨性、导航与证据边界 | **通过源码与 Jekyll 成品检查** |

自动检查禁止已知幕后词语进入正式 HTML；所有外部书目、论文、规范、下载和资源链接必须把原始 URL 作为可见链接文字；三个核心规范页必须同时具有“直白解释”、成熟度区分、规范性措辞和开放问题。每个有标题的正文区段还必须达到最低信息量，防止只留下标题或占位句。

## 全站产品化文案复审

- 已逐项扫描当前 66 个正式页面的 HTML 与 Markdown 权威源，覆盖门户、目录、专题、23 个工具项目页、6 个跨项目指南和 13 个 noemld 手册页面。
- 公开界面不再使用“本页”“阶段门”“证据门”“放行”“退出证据”、未解释的 IPD 或“已确认内容限于”等内部制作与研发管理措辞；自动检查会阻止这些词重新进入最终 HTML。
- 23 个工具项目页统一以“当前状态”说明是否可用，以“开发计划”或“开发顺序”说明依赖和下一步，以具体测试目标说明如何验证；未发布状态、输入输出和安全边界保持不变。
- 开发、下载、FAQ、新闻和路线图已改为直接展示当前工作、资源开放顺序、开发流程、完成标准和近期里程碑，不再向访问者展示内部决策流程。
- noemld 手册继续保留确定性、安全、规范性要求和研究验证等专业内容，但将管理式“放行”术语改为“测试与验收”“安全验证”“发布验收标准”等开发者可直接理解的名称。
- 学术论证、正式规范、安全约束和测试术语不做非技术化删减；专业名词首次出现仍应配合直白解释，避免以项目内部缩写替代实际含义。

## 全站布局与代码复审

- 66 个 Jekyll 路由按 `portal` 1、`section` 10、`content` 19、`tool-project` 23、`docs-topic` 12、`docs-index` 1 六种角色逐页检查；1512px 桌面和 390px 手机成品均无整页横向溢出、空正文区段或控制台错误。
- 12 个普通 HTML 专题的 79 个直接章节全部改为显式版式：`content-stack` 9、`content-grid` 6、`content-rows` 18、`content-band` 23、`content-split` 8、`content-wide` 15。同页按内容混用整行论述、并排卡片、连续横行、紧凑横带、标题侧栏和宽表/流程，不再按章节奇偶或子元素数量猜测布局。
- 23 个工具项目页的“相关资源”必须以可点击入口组结束，构建检查会拒绝卡片组之后出现孤立说明段；当前源码和重新生成的 HTML 均不存在旧构建中曾出现的内部契约式尾段。
- 手机端所有显式专题版式按语义顺序折叠为单列；面包屑和导航按钮保持同一行，菜单展开时锁定背景滚动，菜单自身保留纵向滚动与边界约束，关闭动画、Esc 和外部点击关闭均通过浏览器验证。
- 代码复审删除了未被任何页面使用的 `grid3` 与 `checklist` 样式，并移除共享头部曾同时维护的 `portal-*` 历史别名及重复 CSS；自动检查阻止这些推断式选择器、未使用别名和重复尾段重新进入站点。
