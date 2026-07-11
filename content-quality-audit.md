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

- HTML 总数：65。
- 页面角色：`portal` 1、`section` 10、`content` 18、`tool-project` 23、`docs-index` 1、`docs-topic` 12。
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
- **对象与路由：**README 机器可读注册表、实际 HTML、页面角色、共享目录配置和上级入口一致；65 个路由各登记一次，23 个工具项目页和 noemld 13 页文档子树均可定位。
- **浏览器验收：**65/65 页面保持结构检查基线；本轮新增的思想与方法基础页以及受影响的首页、项目背景、背景与边界、GSIR、对象生命周期和开放问题页已在 Jekyll 成品中复查。桌面端无横向溢出、活动目录正确、四张提案卡片等宽；390px 移动端无整页溢出，长表格在自身容器内滚动，浏览器无脚本错误。项目、架构、文档、资源、开发、工具项目和工具文档目录的折叠切换沿用既有基线。
- **动画与可访问性：**页面主体采用 110ms 轻微渐显，卡片与目录采用 150–200ms 过渡；浏览器确认动画生效，CSS 同时为 `prefers-reduced-motion` 提供零时长降级。

当前 HTML 内容架构审查已经完成，但这只表示设计信息、状态边界和证据路线已覆盖，不表示 Noemion 的技术主张已经被实现或验证。未来形成规范条款、ADR、源码、测试、实验、论文、专利材料或互操作报告时，仍应沿现有路由逐项回填真实证据并重新审查。

## 可读性复审基线

- 首页采用“提示词工程现状 → 意义对象缺口 → 哲学与语义启发 → 确定性工程转译 → 实际建设内容 → 非目标与状态”的顺序，不再要求首次访问者从项目缩写反推设计动机。
- 全站入口页应先使用读者语言解释问题，再引入项目术语；专题页可以更技术化，但必须保留前置知识、状态和权威来源。
- Noesis/Noema、意义与指称等思想只用于解释设计视角，正式语义仍以规范、ADR、数据结构、不变量和测试为准。
- 后续逐页评审不仅检查内容是否存在，还要检查论点顺序、术语首次解释、链接预期和思想来源与工程结论是否混淆。

## 完成判定

单页只有同时满足其角色要求、权威边界明确、关键主张有证据路线、风险与未决项未被隐藏，并通过链接与浏览器检查后，才能从“待深审”移入“已完成”。本轮 65 页均已达到设计阶段的 HTML 内容门；任何未来实现或研究成果仍必须以新增的真实证据重新触发对应页面审查。
