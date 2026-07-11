# Noemion GitHub Pages

本仓库是 [`Noemion/noemion.github.io`](https://github.com/Noemion/noemion.github.io) 的 Jekyll 源目录，计划发布到 <https://noemion.github.io/>。Noemion 是一套面向生成式计算的表征对象编译、链接与可信装载工具链；一级入口负责项目、架构、资源和开发信息，工具项目页介绍单个工具，只有实际存在的 `docs/` 子树承载手册式专题文档。

## Jekyll 与发布

- `_config.yml` 定义账户站点 URL、仓库身份、语言、Markdown 处理器和构建排除项；账户站点的 `baseurl` 必须保持为空。
- `.github/workflows/pages.yml` 在 `main` 分支推送时先运行路由测试，再通过 GitHub 官方 Jekyll Pages Actions 构建和部署 `_site`。
- 当前 66 个正式页面由 Jekyll 处理：46 个普通页面使用 HTML 正文源，20 个手册/指南页面使用 Markdown 权威源；公共 `<head>`、站点头部、目录容器和页脚由共享布局生成。新增 Markdown 手册页面会增加对应正式 HTML 路由，不添加第三方主题，也不创建 `.nojekyll`。
- 本地可在安装兼容 Ruby 与 Bundler 后运行 `bundle install` 和 `bundle exec jekyll serve`；当前工作区自带的系统 Ruby 不作为发布环境基线。

## Jekyll 源码模型

- `_layouts/default.html`：全站 HTML 外壳，负责语言、标题、共享 CSS/JavaScript、页面角色和正文插槽。
- `_layouts/manual.html`：手册布局，负责面包屑、Hero、正文容器、动态索引和上下页导航，并继承默认外壳。
- `_includes/site-header.html`：品牌入口与空目录容器；具体目录由 `assets/directory.js` 按当前路由生成，项目阶段入口从统一时间线配置读取。
- `_includes/project-timeline.html`：通用项目时间线渲染器，接收页面指定的数据对象并生成阶段列表。
- `_includes/manual-directory-data.html`：构建时扫描所有带 `manual_id` 的页面，并向目录引擎提供动态清单。
- `_includes/site-footer.html`：根据页面 Front Matter 生成模块化页脚。
- `_data/manuals.yml`：登记手册级名称、根路由、上级入口、面包屑和分组，不逐页复制目录链接。
- `_data/project_timeline.yml`：项目阶段、当前状态摘要和页头阶段入口的唯一人工配置源。
- 普通正式 `.html` 使用 `layout: default` 并编写职责对应的 `<main>`；手册 `.md` 使用 `layout: manual` 并只编写 Markdown 正文，公开文件名由 `permalink` 确定。
- `assets/`：继续维护现有视觉、目录引擎、动画和图形资源；Jekyll 不改变其内容。

### 手册内容源与生成

`docs/*.md` 与 `tools/noemld/docs/*.md` 是当前 20 个手册/指南页面的唯一正文源，由 Jekyll 通过专用文档布局生成现有 `.html` 公开路由：

- 作者只编辑 Markdown 正文和必要的 Front Matter，不编辑构建目录中的 HTML。
- 源文件可由 `docs/getting-started.md` 生成 `/docs/getting-started.html`，由 `tools/noemld/docs/contract.md` 生成 `/tools/noemld/docs/contract.html`；公开 URL 与目录链接保持不变。
- `<main>`、面包屑、文档 Hero、手册分页、固定左栏和页脚由 `_layouts/`、`_includes/` 与共享目录数据生成，不在每个 Markdown 文件中复制。
- 正文只使用通用 Markdown 的标题、段落、列表、链接、引用、表格和围栏代码块；不写原始 HTML、Kramdown 专有属性或页面级 include。特殊视觉由共享布局和 CSS 根据标准生成元素统一呈现。
- 仓库中不保留对应的手写 `.html` 源文件或双轨内容；质量测试按 Front Matter 的 `permalink` 校验 Markdown 源与正式 HTML 路由。

本迁移同时覆盖跨项目 `docs/` 指南和工具 `tools/<tool>/docs/` 手册；工具项目入口 `tools/<tool>/index.html`、普通内容页和门户页不因本规则自动改为 Markdown。

新增手册页面时，只需在对应目录创建 Markdown 并填写以下元数据；目录侧栏、移动目录、手册首页索引以及上一页/下一页会在构建时自动调整：

```yaml
---
layout: manual
title: "新专题 · 示例手册 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · example documentation"
permalink: "/tools/example/docs/new-topic.html"
manual_id: "example"
manual_group: "start"
manual_order: 2
nav_title: "新专题"
hero_title: "新专题"
hero_description: "本页解决的问题。"
summary: "显示在动态目录卡片中的摘要。"
badges: ["Documentation"]
---
```

新建一套手册时，先在 `_data/manuals.yml` 登记手册级信息与允许的分组；已有手册新增专题不修改该数据文件。`manual_order` 在同一手册内必须唯一，`manual_group` 必须对应已登记分组。手册首页使用 `manual_is_index: true`，术语索引入口使用 `manual_index_entry: true`。

源码检查运行 `python3 tests/site_quality_test.py`。完整发布检查先运行 `bundle exec jekyll build`，再运行 `python3 tests/site_quality_test.py _site`；GitHub Actions 按同一顺序验证并部署。

### 项目时间线配置与嵌入

项目进度只编辑 `_data/project_timeline.yml`，不在页面或 JavaScript 中重复填写阶段节点。`current_stage_id` 必须对应 `items` 中唯一一个 `state: current` 的条目；可用状态为 `confirmed`、`current`、`next` 和 `future`。`header` 控制全站页头的阶段标签、简短值和目标页面，`current` 控制当前阶段摘要与事实栏，`items` 按书写顺序生成时间线。

需要嵌入时间线的普通 HTML 页面在 Front Matter 中声明 `timeline_data: "project_timeline"`，正文先通过 `site.data[page.timeline_data]` 取得配置，再调用 `{% raw %}{% include project-timeline.html timeline=timeline %}{% endraw %}`。Jekyll 会在每次本地构建和 `main` 分支 Pages 构建时自动生成最终 HTML；不需要手工维护构建产物。新增另一套时间线时可在 `_data/` 新建同结构 YAML，并把页面的 `timeline_data` 改为对应文件名。

## 站点结构

- `index.html`：项目门户，概括定位、能力、状态和主要入口。
- `about/`：项目背景、动机、范围、非目标，以及思想与方法基础的采用边界。
- `architecture/`：系统关系、对象生命周期、信任边界和开放问题。
- `specifications/`：GSIR、GOBJ、SSO 等规范的权威来源与成熟度。
- `components/`：Compiler Core、链接装载、Runtime 和 NSFE 等组件入口。
- `tools/`：23 个工具的分类目录；`tools/<tool>/index.html` 是工具项目页。
- `tools/<tool>/docs/`：仅在存在实质帮助手册时建立；目录内 Markdown 由 Jekyll 生成 HTML 手册页，工具项目入口本身继续使用 HTML。
- `docs/`：保存入门、使用、架构、开发、工具和规范六类任务型文档；正文链接权威页面，不复制第二套规范。
- `downloads/`、`faq/`、`development/`、`news/`：资源状态、常见问题、开发入口和经确认的进展。

## 浏览与共享资源

从 `index.html` 开始浏览。Jekyll 布局通过 `relative_url` 统一加载共享资源，正文内部继续使用与正式路由对应的相对链接。`assets/style.css` 统一导入 `assets/directory.css`；目录的基础布局、折叠、高亮、响应式行为和滚动条在共享 CSS 中维护。`assets/directory.js` 同时承担目录渲染引擎和模块配置中心，根据当前路由选择项目、架构与对象、文档、资源、开发、工具、单个工具或工具文档目录。空目录容器只存在于共享 include，不在页面源码中复制导航链接。

导航一致性以“可达”而不是“完全相同”为准：每个非门户页面至少提供返回直接上级 `index.html`、所属模块目录页或路由表登记的特定目录页的方式。面包屑、模块目录中的上级入口以及手册导航中的“上级”都可以承担这一职责。

全站顶部导航采用项目任务分组：一级入口在悬停或键盘聚焦时展开纵向内容面板，先说明分组用途，再显示带专属 SVG 封面的入口卡片；移动端复用同一目录数据。箭头和内容面板采用约 180–220ms 的快速过渡，卡片按 45ms 错峰进入，并支持减少动态效果设置。

## Noemion 全站设计系统

桌面端统一使用约 1200px 居中连续画布、64px 顶部导航、近白纸面、细分隔线、大字号编辑式标题和高密度内容行；移动端按阅读顺序折叠为单列。布局围绕 Noemion 的对象语义、工程内容、图形、配色和成熟度语言建立，不以装饰削弱技术边界。

页面角色采用同一设计语言下的不同页面范式：`portal` 使用首页叙事；`section` 使用分组列表；`content` 使用编辑式文章；`tool-project` 使用主内容与状态面板；所有 `/docs/` 路由及 `docs-index`、`docs-topic` 使用固定文档栏和阅读区。所有顶部一级入口必须支持悬停与键盘聚焦展开，卡片标题、圆形箭头和表面提供一致反馈；按压缩放为 0.96，进入与状态切换支持减少动态效果。完整规则见 [`sitewide-design-system.md`](sitewide-design-system.md)，首页内容蓝图见 [`homepage-design.md`](homepage-design.md)。

修改页面前从 [`design-system/README.md`](design-system/README.md) 进入设计路由，并按页面角色读取门户、目录、专题、工具项目、手册或共享组件对应文档。设计文档目录被 Jekyll 排除，不会生成公开站点页面。

23 个内部工具分别拥有独立视觉签名，详见 [`design-system/internal-tools.md`](design-system/internal-tools.md)。默认布局根据 `tools/<tool>/...` 路径自动写入 `data-tool-id`，共享 CSS 再应用对应的配色、对象面板签名、网格角度和强调状态；工具项目页不维护页面级 CSS。工具帮助手册继承工具强调色，但正文、目录和分页继续遵循统一手册规范。

Noemion 的视觉识别由“语义频谱”与机器对象语言形成：薄荷、青蓝、朱橙和琥珀的光谱只标记来源、歧义、对象层与状态；黑色对象记录面板表示可检查的 GSIR/GOBJ/SSO；等宽序号、阶段脉冲和证据门表达成熟度。任何装饰都不得取代权威性、失败语义和证据边界。

全站统一品牌、字体、颜色、基础间距、面包屑和目录引擎；具体目录分组、正文结构、表格、清单、手册分页和状态展示由模块职责决定。模块可以共享布局组件，但不得为了视觉对称强行增加不适用的章节。

运行测试前必须安装可从命令行调用的 Node.js。源码阶段验证 66 个页面的 Front Matter、固定路由、共享布局和目录注册；Jekyll 构建后，质量测试会直接检查 `_site` 中的最终 HTML，并加载同一份生产 `assets/directory.js`，验证模块覆盖、页面类型、工具文档高亮以及模块不会向全局对象暴露 API。

每个 `kind=tool` / `data-page-role=tool-project` 页面都是项目入口而非手册：必须包含“项目 / 工具 / 当前工具”面包屑，以及“工具简介”“当前状态”“主要能力”“输入与产物”“处理边界”“相关资源”六个语义章节。当前状态必须明确处于设计阶段、当前未发布可执行程序，并说明命令行接口、参数和文件扩展名尚未冻结；只有实际存在实质内容时才链接或创建工具 `docs/`。

## 内容质量与研究治理

内容审查不得使用一套完整模板覆盖全部 HTML。Why / How / What、IPD、研究治理和详细设计是可选择的检查视角，只有与页面职责相关时才进入正文；目录页不需要伪造详细设计，资源页不需要套用工具契约，手册页也不应被管理术语打断阅读。

### 全站可读性规则

1. 页面先回答读者正在问什么、为什么重要和本页结论，再引入 GSIR、GOBJ、SSO、Strict、Lowering 等项目术语。
2. 缩写和专业词第一次出现时使用完整名称或直白解释；不能要求读者先理解整个 Noemion 体系才能读懂入口页。
3. 抽象机制优先用一个具体问题、因果链、流程或对照关系解释，再进入结构、字段和不变量。
4. 哲学概念只作为问题框架和工程启发；必须明确区分思想来源、工程类比、正式规范和验证证据，不能用哲学术语替代技术定义。
5. 段落只承担一个主要论点；并列概念优先使用列表、表格或短卡片，但不为视觉整齐拆碎本应连续的论证。
6. 链接文字应说明读者点击后能回答什么问题，避免只有“更多”“详情”或重复页面标题。
7. 已确认原则、设计提案、开放问题、未来阶段和真实成果继续使用明确状态语言；清晰易读不能以省略证据边界为代价。
8. 正式 HTML 面向开发者、普通用户和潜在使用者，只解释项目、产品、规范、使用场景与真实状态；不得出现用户指令、内容生成、内部 review、补写过程、页面制作或测试驱动文案等幕后信息。
9. 网站作为后续设计、实现和互操作工作的标准与规范入口，采用“直白解释 + 精确定义”双层表达；解释可以增加，但不得弱化规范术语、约束强度、不变量、失败语义、成熟度标记和权威来源。
10. 外部书目、论文、规范、下载和其他资源链接必须显示原始 URL，不能只保留概括性标题；资源说明和可复制链接分开书写。站内导航继续使用明确的目标名称。

### 模块化内容规范

| 模块或页面类型 | 应重点回答 | 不应强行套用 |
| --- | --- | --- |
| 项目门户与 `about/` | 项目背景、受众、问题、范围、非目标、原则、状态和主要入口 | 命令参数、对象字段或手册式逐章导航 |
| `architecture/` 与 `components/` | 系统关系、职责分层、对象或控制流、信任边界、质量属性、关键决策和开放问题 | 发布资源清单或重复规范字段定义 |
| `specifications/` | 权威来源、成熟度、术语、规范性要求、数据模型、不变量、错误语义、版本演进和一致性验证 | 营销承诺、未经批准的候选结论或使用指南式重复说明 |
| 跨项目 `docs/` 指南 | 面向读者任务说明前置知识、背景、阅读或操作顺序、预期结果、常见误解、下一步和权威参考 | 复制第二套规范，或机械加入与任务无关的 IPD、专利和架构章节 |
| 工具项目页 `tools/<tool>/index.html` | 在既定六个章节中说明定位、状态、能力、输入输出、边界、阶段门和资源入口 | GNU 手册章节编号、完整 CLI 手册或顺序分页 |
| 工具 `docs/` 与专题页 | 按 GNU 手册方式组织目录、连续阅读路径、契约、调用语义、处理步骤、诊断、安全、测试、依赖和索引；只编写该工具实际需要的专题 | 为目录对称创建空页面，或把项目介绍反复复制到每个专题 |
| `downloads/` 资源页 | 真实资源状态、版本、格式或平台、大小、许可、来源、校验值、签名、SBOM、发布日期、撤回与归档信息 | 虚构下载按钮、仓库、版本、校验值或安装命令 |
| `development/` | 路线图、当前阶段、进入条件、退出证据、规范/ADR 流程、测试、安全、贡献和报告渠道 | 把计划任务写成已完成能力 |
| `news/` 与 `faq/` | 新闻记录日期、范围、证据、限制和下一决策门；FAQ 直接回答高频问题并链接权威页面 | 用占位公告制造历史，或在 FAQ 中重新定义技术规范 |

入口和目录页面可以简洁，只要能说明模块职责、当前状态、内容地图与返回路径；专题页面才承担与其主题匹配的概要或详细设计。评价页面质量时，应先判断模块属性和读者任务，再使用相应规范检查，不能以章节数量、字符数或模板一致性代替内容质量。

研发治理参考 IPD 的概念、计划、开发、验证、发布和生命周期阶段。阶段状态必须同时给出进入条件、退出证据和未满足门槛。研究与知识产权内容还应逐步建立研究问题、可证伪假设、创新点候选、现有技术边界、实验或测试证据、ADR、版本和规范条款之间的追溯关系。论文、专利、软著或标准化意图不等于成果已经形成；专利候选在公开披露前需要知识产权审查，标准提案需要稳定术语、可测试条款、互操作性案例和安全分析。

逐页审查状态与剩余缺口维护在 [`content-quality-audit.md`](content-quality-audit.md)。该清单用于规划内容工作，不是对页面成熟度的自我认证。

## 正式 HTML 路由

本 README 是固定站点结构、页面角色、既有正式路由和维护规则的登记来源；不要在项目级 `AGENTS.md` 中复制路由表或页面级维护细节。下表登记当前正式 HTML 路由；新增手册 Markdown 的 `permalink` 会被质量测试和 Jekyll 自动纳入，不要求同步复制 JavaScript 目录链接。

| 路由 | 类型 | 上级入口 | 顺序 | 职责 |
| --- | --- | --- | ---: | --- |
| `index.html` | portal | `` | 0 | Noemion 项目门户 |
| `about/index.html` | section | `index.html` | 1 | 项目背景入口 |
| `architecture/index.html` | section | `index.html` | 2 | 架构入口 |
| `specifications/index.html` | section | `index.html` | 3 | 规范与成熟度入口 |
| `components/index.html` | section | `index.html` | 4 | 系统组件入口 |
| `tools/index.html` | section | `index.html` | 5 | 工具项目分类目录 |
| `docs/index.html` | section | `index.html` | 6 | 跨项目文档中心 |
| `downloads/index.html` | section | `index.html` | 7 | 下载与资源状态入口 |
| `faq/index.html` | section | `index.html` | 8 | 站点级常见问题 |
| `development/index.html` | section | `index.html` | 9 | 开发与贡献入口 |
| `news/index.html` | section | `index.html` | 10 | 新闻与进展入口 |
| `about/background.html` | content | `about/index.html` | 1 | 项目动机、范围与边界 |
| `about/intellectual-foundations.html` | content | `about/index.html` | 2 | 分析哲学、语言哲学与工程采用边界 |
| `architecture/object-lifecycle.html` | content | `architecture/index.html` | 1 | 对象生命周期与信任边界 |
| `architecture/open-questions.html` | content | `architecture/index.html` | 2 | 设备条件与开放问题 |
| `specifications/gsir.html` | content | `specifications/index.html` | 1 | GSIR 语义与状态 |
| `specifications/gobj.html` | content | `specifications/index.html` | 2 | GOBJ 对象格式与状态 |
| `specifications/sso.html` | content | `specifications/index.html` | 3 | SSO 与渐进式披露 |
| `components/compiler-core.html` | content | `components/index.html` | 1 | 确定性 Compiler Core |
| `components/linker-loader.html` | content | `components/index.html` | 2 | Linker、Loader 与 Runtime |
| `components/nsfe.html` | content | `components/index.html` | 3 | NSFE 架构与模型工程状态 |
| `development/current-stage.html` | content | `development/index.html` | 1 | 当前项目阶段、证据门与进度时间线 |
| `development/implementation-roadmap.html` | content | `development/index.html` | 2 | 实施阶段、工具职责与放行门 |
| `development/testing.html` | content | `development/index.html` | 3 | 测试、Fuzz 与验证策略 |
| `docs/getting-started.html` | content | `docs/index.html` | 1 | 项目入门、核心对象与推荐阅读路径 |
| `docs/installation-and-usage.html` | content | `docs/index.html` | 2 | 当前可用性、未来使用流程与发布原则 |
| `docs/architecture-guide.html` | content | `docs/index.html` | 3 | 系统分层、对象生命周期与信任边界指南 |
| `docs/development-guide.html` | content | `docs/index.html` | 4 | 第一阶段、规范先行、测试与贡献指南 |
| `docs/tools-reference.html` | content | `docs/index.html` | 5 | 23 个工具职责、阶段与文档状态参考 |
| `docs/specifications-reference.html` | content | `docs/index.html` | 6 | 规范权威性、成熟度与对象参考入口 |
| `tools/noemconform/index.html` | tool | `tools/index.html` | 1 | noemconform 工具项目页 |
| `tools/noemobj/index.html` | tool | `tools/index.html` | 2 | noemobj 工具项目页 |
| `tools/noemverify/index.html` | tool | `tools/index.html` | 3 | noemverify 工具项目页 |
| `tools/noemcopy/index.html` | tool | `tools/index.html` | 4 | noemcopy 工具项目页 |
| `tools/noemsize/index.html` | tool | `tools/index.html` | 5 | noemsize 工具项目页 |
| `tools/noemas/index.html` | tool | `tools/index.html` | 6 | noemas 工具项目页 |
| `tools/noemdis/index.html` | tool | `tools/index.html` | 7 | noemdis 工具项目页 |
| `tools/noemfmt/index.html` | tool | `tools/index.html` | 8 | noemfmt 工具项目页 |
| `tools/noemdiff/index.html` | tool | `tools/index.html` | 9 | noemdiff 工具项目页 |
| `tools/noemc/index.html` | tool | `tools/index.html` | 10 | noemc 工具项目页 |
| `tools/noemlint/index.html` | tool | `tools/index.html` | 11 | noemlint 工具项目页 |
| `tools/noemar/index.html` | tool | `tools/index.html` | 12 | noemar 工具项目页 |
| `tools/noemnm/index.html` | tool | `tools/index.html` | 13 | noemnm 工具项目页 |
| `tools/noemld/index.html` | tool | `tools/index.html` | 14 | noemld 工具项目页 |
| `tools/noemstrip/index.html` | tool | `tools/index.html` | 15 | noemstrip 工具项目页 |
| `tools/noemcov/index.html` | tool | `tools/index.html` | 16 | noemcov 工具项目页 |
| `tools/noempack/index.html` | tool | `tools/index.html` | 17 | noempack 工具项目页 |
| `tools/noemrun/index.html` | tool | `tools/index.html` | 18 | noemrun 工具项目页 |
| `tools/noemtrace/index.html` | tool | `tools/index.html` | 19 | noemtrace 工具项目页 |
| `tools/noemdata/index.html` | tool | `tools/index.html` | 20 | noemdata 工具项目页 |
| `tools/noemtrain/index.html` | tool | `tools/index.html` | 21 | noemtrain 工具项目页 |
| `tools/noemeval/index.html` | tool | `tools/index.html` | 22 | noemeval 工具项目页 |
| `tools/noemquant/index.html` | tool | `tools/index.html` | 23 | noemquant 工具项目页 |
| `tools/noemld/docs/index.html` | docs | `tools/noemld/index.html` | 0 | noemld 文档中心 |
| `tools/noemld/docs/contract.html` | topic | `tools/noemld/docs/index.html` | 1 | noemld 职责与稳定契约 |
| `tools/noemld/docs/inputs-outputs.html` | topic | `tools/noemld/docs/index.html` | 2 | noemld 输入输出对象 |
| `tools/noemld/docs/invocation.html` | topic | `tools/noemld/docs/index.html` | 3 | noemld 命令行调用 |
| `tools/noemld/docs/pipeline.html` | topic | `tools/noemld/docs/index.html` | 4 | noemld 端到端处理流程 |
| `tools/noemld/docs/symbol-resolution.html` | topic | `tools/noemld/docs/index.html` | 5 | noemld 符号解析 |
| `tools/noemld/docs/relocations.html` | topic | `tools/noemld/docs/index.html` | 6 | noemld 重定位与 ID 重映射 |
| `tools/noemld/docs/sso-linking.html` | topic | `tools/noemld/docs/index.html` | 7 | noemld SSO 链接与披露闭包 |
| `tools/noemld/docs/loader-security.html` | topic | `tools/noemld/docs/index.html` | 8 | noemld 装载完整性与安全 |
| `tools/noemld/docs/diagnostics.html` | topic | `tools/noemld/docs/index.html` | 9 | noemld 诊断与失败边界 |
| `tools/noemld/docs/testing.html` | topic | `tools/noemld/docs/index.html` | 10 | noemld 测试与放行门 |
| `tools/noemld/docs/dependencies.html` | topic | `tools/noemld/docs/index.html` | 11 | noemld 上下游依赖 |
| `tools/noemld/docs/reference-index.html` | topic | `tools/noemld/docs/index.html` | 12 | noemld 命令术语与对象索引 |

## 许可证

除非文件中另有说明，本仓库的源码与文档采用 [Apache License 2.0](LICENSE) 发布。该许可证不授予使用 Noemion 名称、标识或相关商标的权利；为说明作品来源或重现许可声明所必需的合理使用除外。

## 维护规则

1. 内容修改只编辑权威专题页面；项目介绍、正式规范、开放问题和工具文档保持职责分离。
2. 全局 HTML 外壳只编辑 `_layouts/default.html`，站点头部和页脚只编辑 `_includes/`；全局颜色和正文排版只编辑 `assets/style.css`，目录样式只编辑 `assets/directory.css`。禁止页面复制公共外壳、页面级 CSS、内联 `<style>` 或 `style=`。
3. `assets/directory.js` 维护目录渲染和全部模块配置；模块目录可以拥有不同的内容与分组，但必须覆盖注册表中的全部 HTML 路由，并为每个页面选择正确的模块目录。新增模块目录时继续使用同一共享引擎，不在页面源码或 include 中复制目录链接。
4. 每个工具的全部 HTML 页面只保存在 `tools/<tool>/`。工具 `index.html` 是项目页；只有存在实质专题文档时才创建 `docs/index.html` 与语义命名的专题页，不为空目录制造文档树。
5. 新增、删除、移动或改名页面时，同步本注册表、`assets/directory.js`（仅当全局落地页变化）、受影响的模块目录、对应入口、顺序导航和全部交叉链接；每个非门户页面必须保留可用的上级或指定目录返回入口。
6. 路由、目录和命名直接采用当前规范；不保留旧入口、旧路径、旧别名、重定向或兼容垫片。
7. 每次路由或页面角色变更先运行 `python3 tests/site_quality_test.py` 检查 Jekyll 源码，再构建并运行 `python3 tests/site_quality_test.py _site`，确认最终 HTML、README 注册表、全局目录和页面角色一致。
8. 新增工具时创建 `tools/<tool>/index.html`，并同步 `tools/index.html`、本注册表和全局目录的对应工具分类。
9. 正式技术规范逐步迁移为 Markdown；HTML 保留为导航和设计总览。
10. `docs/index.html` 的六个入口必须指向 `docs/` 下实际存在的任务型 HTML；这些页面负责解释和阅读路径，不替代权威规范。
11. 网页改动完成并通过源码、Jekyll 构建、构建产物和浏览器验收后，默认继续提交、推送并确认 GitHub Pages 部署，再提供在线地址；只有用户明确要求不发布时才停留在本地。
