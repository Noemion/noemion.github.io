# Noemion GitHub Pages

本仓库是 [`Noemion/noemion.github.io`](https://github.com/Noemion/noemion.github.io) 的 Jekyll 源目录，发布于 <https://noemion.github.io/>。Noemion 是项目、新领域与社区的总名和品牌；站点在这个总名之下定义 Endem、Synem、Dromen、Iknem、Ktisor、Theor、Drasor 与唯一 `endem` 应用，一级入口负责项目、规范、应用、指南和开发信息，`endem/docs/` 承载 CLI 使用手册。

当前尚未进入组件代码开发阶段。本仓库只维护哲学与语言研究、术语、架构、规范、威胁模型、验证方案、公开文档和网站；Ktisor、Theor、Drasor 与 `endem` CLI 均没有实现源码。规范检查脚本只能证明资料一致，不能被描述为组件实现。

## Jekyll 与发布

- `_config.yml` 定义账户站点 URL、仓库身份、语言、Markdown 处理器和构建排除项；账户站点的 `baseurl` 必须保持为空。
- `.github/workflows/pages.yml` 在 `main` 分支推送时先按 `.ruby-version` 与 `Gemfile.lock` 设置锁定环境、运行路由测试并构建 `_site`，再通过 GitHub 官方 Pages Actions 加入公开 `sitemap.md`、上传并部署。
- 全部正式页面由 Jekyll 处理：普通页面使用 HTML 正文源，手册与指南页面使用 Markdown 权威源；公共 `<head>`、站点头部、目录容器和页脚由共享布局生成。新增 Markdown 手册页面会增加对应正式 HTML 路由，不添加第三方主题，也不创建 `.nojekyll`。页面数量以 `sitemap.md` 和质量测试的实际结果为准，不在 README 固定重复。
- `spec/*.md` 保存 END-CORE、END-FMT、END-SRCM、SYN-CORE、DRO-CORE、IKN-CORE、DIA-CORE、ADP-CORE、ID-CORE、TEXT-IDENTIFIER-CORE 与 AUT-CORE 等版本化规范条款。END-CORE 是 Endem 通用内容标准，`spec/profiles/end-p1.json` 是当前封闭内容 Profile，END-FMT 是实验性容器；其余 CORE 分别约束组合、会话、证据、诊断、适配、身份、文本以及权威与授权决定，都不因此建立新的文件格式或组件。`spec/registry.json` 保存机器可读成熟度和验证映射，`vectors/` 保存语义外壳、专题提案矩阵和实验性规范字节。这些工程源文件由 Jekyll 排除；公开规范页面负责直白解释并链接精确源文件，不能复制另一套条款。
- 本地构建基线固定为 `.ruby-version` 中的 Ruby 3.4.10 与 `Gemfile.lock` 中的 Bundler 2.6.9；当前工作区自带的系统 Ruby 不作为发布环境基线。macOS 已安装 Homebrew Ruby 时，先运行 `export PATH="$(brew --prefix ruby@3.4)/bin:$PATH"`，再运行 `bundle config set --local path vendor/bundle`、`bundle install` 和 `bundle exec jekyll build`。

## Jekyll 源码模型

- `_layouts/default.html`：全站 HTML 外壳，负责语言、标题、共享 CSS/JavaScript、页面角色和正文插槽。
- `_layouts/default.html` 同时根据正式路由写入 `data-site-module`；共享样式据此应用背景、架构、规范、组件、Endem、指南、开发、资源和常见问题各自的几何母题，页面不手写模块样式。
- `_layouts/manual.html`：手册布局，负责面包屑、手册引言、正文容器、动态索引和上下页导航，并继承默认外壳。
- `_includes/site-header.html`：构建品牌入口、五个可直接访问的一级任务入口、按需增强的模块目录容器和项目时间线入口。
- `_includes/project-timeline.html`：通用项目时间线渲染器，接收页面指定的数据对象并生成阶段列表。
- `_includes/docs-rail.html`：构建时扫描当前 `manual_id` 的页面，直接输出可在无脚本环境阅读的文档栏，并作为移动目录的只读数据来源。
- `_includes/manual-pagination.html`：根据手册顺序为顶部和底部复用同一套上一页、上级、目录、下一页与索引导航。
- `_includes/site-footer.html`：根据页面 Front Matter 生成模块化页脚。
- `_data/manuals.yml`：登记手册级名称、根路由、上级入口、面包屑和分组，不逐页复制目录链接。
- `_data/navigation.yml`：登记顶部导航卡片与普通页面模块目录；Jekyll 同时生成一级入口和 `/assets/navigation-data.json`。
- `_data/site_header.yml`：全站页头独立行动入口的唯一配置源，当前提供 `TIMELINE` 项目时间线入口。
- `_data/project_timeline.yml`：项目阶段与当前状态摘要的唯一人工配置源，只服务承担进度说明职责的页面。
- 普通正式 `.html` 使用 `layout: default` 并编写职责对应的 `<main>`；手册 `.md` 使用 `layout: manual` 并只编写 Markdown 正文，公开文件名由 `permalink` 确定。
- `assets/site.mjs`：小型全站入口，只判断页面能力和设备布局后加载 `assets/modules/*.mjs`；路由模型、数据仓库、顶部导航、模块目录、移动端状态和正文增强分别维护独立接口。移动目录、移动页头和桌面导航复用同一个紧凑布局媒体状态，避免相邻判断产生空档；页头与摘要栏再通过共享布局观察器响应容器、字体和视口变化。1000px 以下立即准备纯文字移动目录；1000px 及以上且存在精确指针时提前准备体积很小的导航控制器、数据和 SVG 缓存，但只在实际打开时生成当前分组卡片。粗指针平板继续在主动打开时按需准备，手机不导入桌面控制器，也不请求或合成桌面封面。`assets/mobile-directory-guard.js` 通过独立透明遮罩冻结后方手势，并约束目录的滚轮、单指触摸和滚动边界，不改写正文定位或滚动坐标。`assets/theme.js` 在 CSS 加载前恢复全站 `Light / Dark / System` 选择，并负责持久化、系统主题监听和页脚菜单交互；`assets/images/` 保存经过裁切和压缩的站点图片。
- `sitemap.md`：不带 Front Matter 的公开 Markdown 发现索引，也是唯一正式路由注册表；它不进入 Markdown 转换，由 Pages 工作流在 Jekyll 构建后原样加入 `/sitemap.md`，供读者和自动化工具按内容家族读取全部正式 HTML 路由、顺序和职责。README 不再复制路由表，质量测试直接以该文件核对源码与构建产物。

### 手册内容源与生成

`docs/*.md` 与 `endem/docs/*.md` 是手册和指南页面的唯一正文源，由 Jekyll 通过专用文档布局生成 `.html` 公开路由。Endem 手册固定覆盖总览、格式、绑定、安全、运行与参考六类任务：

- 作者只编辑 Markdown 正文和必要的 Front Matter，不编辑构建目录中的 HTML。
- 源文件可由 `docs/getting-started.md` 生成 `/docs/getting-started.html`，由 `endem/docs/binding.md` 生成 `/endem/docs/binding.html`；公开 URL 只采用当前路由。
- `<main>`、面包屑、手册引言、手册分页、固定左栏和页脚由 `_layouts/`、`_includes/` 与共享目录数据生成，不在每个 Markdown 文件中复制。
- 正文只使用通用 Markdown 的标题、段落、列表、链接、引用、表格和围栏代码块；不写原始 HTML、Kramdown 专有属性或页面级 include。特殊视觉由共享布局和 CSS 根据标准生成元素统一呈现。
- 仓库中不保留对应的手写 `.html` 源文件或双轨内容；质量测试按 Front Matter 的 `permalink` 校验 Markdown 源与正式 HTML 路由。

这一规则同时覆盖跨项目 `docs/` 指南和 `endem/docs/` 手册；Endem 应用入口 `endem/index.html`、普通内容页和门户页不因本规则自动改为 Markdown。仓库不保留旧工具树、旧命令页面、重定向或兼容别名。

新增手册页面时，只需在对应目录创建 Markdown 并填写以下元数据；目录侧栏、移动目录、手册首页索引以及上一页/下一页会在构建时自动调整：

```yaml
---
layout: manual
title: "新专题 · 示例手册 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · example documentation"
permalink: "/docs/example-topic.html"
manual_id: "example"
manual_group: "start"
manual_order: 2
nav_title: "新专题"
page_heading: "新专题"
page_lead: "面向读者的页面用途与直接结论。"
summary: "显示在动态目录卡片中的摘要。"
badges: ["文档"]
---
```

新建一套手册时，先在 `_data/manuals.yml` 登记手册级信息与允许的分组；已有手册新增专题不修改该数据文件。`manual_order` 在同一手册内必须唯一，`manual_group` 必须对应已登记分组。手册首页使用 `manual_is_index: true`，术语索引入口使用 `manual_index_entry: true`。

规范登记检查运行 `python3 tests/spec_contract_test.py`，语义与各专题提案向量分别运行对应的 `tests/*_vector_test.py`；AUT-CORE 使用 `python3 tests/authority_vector_test.py`。END-P0 结构字节运行 `python3 tests/wire_vector_test.py`，END-P1 完整载荷运行 `python3 tests/p1_payload_test.py`，源码页面检查运行 `python3 tests/site_quality_test.py`。完整发布检查随后运行 `bundle exec jekyll build`，加入 `sitemap.md`，再运行 `python3 tests/site_quality_test.py _site`；这些检查只证明资料一致性和实验字节符合当前草案。

### 项目时间线配置与嵌入

项目进度只编辑 `_data/project_timeline.yml`，不在页面或 JavaScript 中重复填写阶段节点。`current_stage_id` 必须对应 `items` 中唯一一个 `state: current` 的条目；可用状态为 `confirmed`、`current`、`next` 和 `future`。`overview` 控制状态摘要与路线图入口，`current` 控制当前阶段摘要与事实栏，`items` 按书写顺序生成“已完成 / 正在进行 / 后续规划”时间线及对应计数。项目阶段不进入全站页头，避免把内部研发进度误解成版本、页面或可用状态。

全站页头的右侧行动入口只编辑 `_data/site_header.yml`。当前只显示 `TIMELINE` 并链接 `/development/current-stage.html`；不附加图形、Endem、当前阶段名或完成比例，让文字本身承担完整导航含义。入口默认继承页头背景，只用分隔线定义铺满的单元边界；悬停时才显示轻微主题色变化，不建立带外边距的内层卡片或常态选中表面。

需要嵌入时间线的普通 HTML 页面在 Front Matter 中声明 `timeline_data: "project_timeline"`，正文先通过 `site.data[page.timeline_data]` 取得配置，再调用 `{% raw %}{% include project-timeline.html timeline=timeline %}{% endraw %}`。Jekyll 会在每次本地构建和 `main` 分支 Pages 构建时自动生成最终 HTML；不需要手工维护构建产物。新增另一套时间线时可在 `_data/` 新建同结构 YAML，并把页面的 `timeline_data` 改为对应文件名。

## 站点结构

- `index.html`：项目门户，概括定位、能力、状态和主要入口。
- `about/`：项目背景、动机、范围、非目标，以及思想与方法基础的采用边界。
- `architecture/`：系统关系、Endem 生命周期、Agent 运行事实边界、信任边界和开放问题；生命周期入口是 `/architecture/endem-lifecycle.html`，跨层 Agent 入口是 `/architecture/agent-system-boundaries.html`。
- `specifications/`：Endem、Synem、Dromen、Iknem 与跨对象边界的权威规范和成熟度入口；目录页统一列出对象、诊断、适配、身份、文本以及权威与授权决定规范的正式路由。
- `spec/` 与 `vectors/`：实现可逐条引用的规范源、Profile、机器可读登记、语义外壳和实验字节向量；它们不生成并列 Pages 路由，也不冒充稳定 ABI。
- `experiments/`：历史、非生产且当前冻结的语言研究材料；这里保存彼此独立的 C/Rust 读取原型与既有结果。目录不生成 Pages 路由，当前不自动运行或扩展这些实验，公开页面只总结历史结果及其限制。
- `components/`：Ktisor、Theor 与 Drasor 的职责和隔离边界，正式路由分别是 `/components/ktisor.html`、`/components/theor.html` 与 `/components/drasor.html`。
- `endem/index.html`：唯一公开应用入口，介绍 `.endem`、五个动作、当前状态、信任边界和手册入口。
- `endem/docs/`：唯一 CLI 使用手册；Markdown 生成总览、格式、绑定、安全、运行与参考六个正式 HTML 路由。
- `docs/`：保存入门、使用、架构、开发、Endem 和规范六类任务型文档；正文链接权威页面，不复制第二套规范。
- `downloads/`、`faq/`、`development/`、`news/`：资源状态、常见问题、开发入口和经确认的进展。

## 浏览与共享资源

从 `index.html` 开始浏览。Jekyll 布局通过 `relative_url` 统一加载共享资源，正文内部继续使用与正式路由对应的相对链接。`assets/style.css` 与 `assets/directory.css` 由共享布局加载并携带同一构建版本；目录布局、折叠、高亮和响应式行为只在 `assets/directory.css` 维护。一级导航与手册侧栏在构建期成为可直接访问的 HTML；移动端同步守卫在目录控制器载入前后都负责页面冻结和手势边界，控制器建立后只接管菜单状态。`assets/site.mjs` 按页面需要加载移动目录、富导航、正文增强和摘要栏控制器。摘要栏控制器以容器实际宽度、摘要栏需求和主内容最低可读宽度决定双栏或单栏，并在字体与尺寸变化后重算；无脚本时保持完整单栏。模块职责与失败降级见 [`design-system/frontend-architecture.md`](design-system/frontend-architecture.md)。

导航一致性以“可达”而不是“完全相同”为准：每个非门户页面至少提供返回直接上级 `index.html`、所属模块目录页或路由表登记的特定目录页的方式。面包屑、模块目录中的上级入口以及手册导航中的“上级”都可以承担这一职责。

全站顶部导航采用项目任务分组：桌面一级入口在悬停或键盘聚焦时展开纵向内容面板，先说明分组用途，再显示带专属 SVG 封面的入口卡片；精确指针桌面提前准备共享资源，实际打开时只生成当前分组。移动端只复用同一目录数据和文字，不创建、请求或合成这些不可见封面。达到桌面宽度但仍使用无悬停粗指针的横屏平板，初始状态同样不加载封面；第一次触摸一级入口时才按需建立即将显示的富菜单，第二次触摸标题可进入目录，也可直接选择菜单卡片。触摸产生的焦点本身不提前加载资源，外接键盘使用 Tab 聚焦时仍可展开完整菜单。箭头和内容面板采用约 160–180ms 的快速过渡，卡片按 15ms 错峰进入，并支持减少动态效果设置。

1000px 以下统一使用移动目录，避免 iPhone 14 Pro 等设备横屏时落入依赖悬停、无法隔离背景滚动的桌面下拉导航。非首页由共享页头控制器比较品牌、`TIMELINE`、导航按钮的固有宽度与实时可用宽度：能完整放下时导航按钮留在第一行，只有放不下时才进入面包屑所在第二行；窗口和字体变化会触发重新计算。目录首次点击即开始与图标同步的 180ms 展开动画，不等待模块、数据或动画延时；再次点击、点击外部或按 `Escape` 时立即开始反向动画。外部关闭只响应完成的点击，不响应滑动开始，避免屏幕边缘的滚动手势误关目录。首页没有面包屑，继续使用单行移动头部。

移动目录作为独立固定图层显示在透明交互遮罩上方，不把根元素或正文改成固定定位、隐藏溢出，也不修改正文尺寸、滚动坐标或页头定位。菜单高度由实际条目决定，只有内容超过实时视觉视口的可用高度时才在面板内纵向滚动。Safari 工具栏、方向或可视高度变化会同步更新高度上限；同步守卫在捕获阶段拦截遮罩的点击、滚轮、触摸和滚动按键以及目录边界继续滑动，不能把输入传给后方正文。门户按钮的文字颜色不继承普通链接的已访问颜色，访问前后保持各主题规定的前景色。

## Noemion 全站设计系统

桌面端统一使用约 1200px 居中连续画布、64px 顶部导航、近白纸面、细分隔线、大字号编辑式标题和高密度内容行；移动端按阅读顺序折叠为单列。画布宽度、两侧留白、页头高度以及文档侧栏与正文列宽由共享 CSS 变量统一计算，页头、正文、页脚和目录不分别复制设备公式。布局围绕 Noemion 领域及 Endem 等具体制品的工程语义、图形、配色和成熟度语言建立，不以装饰削弱技术边界。

页面角色采用同一设计语言下的不同页面范式：`portal` 使用首页叙事；`section` 使用分组列表；`content` 使用编辑式文章；`tool-project` 使用主内容与状态面板；所有 `/docs/` 路由及 `docs-index`、`docs-topic` 使用固定文档栏和阅读区。所有顶部一级入口必须支持悬停与键盘聚焦展开，卡片标题、圆形箭头和表面提供一致反馈；按压缩放为 0.96，进入与状态切换支持减少动态效果。完整规则见 [`sitewide-design-system.md`](sitewide-design-system.md)，首页内容蓝图见 [`homepage-design.md`](homepage-design.md)。

模块视觉身份由 [`design-system/geometric-layouts.md`](design-system/geometric-layouts.md) 统一维护：同一模块的目录页、专题页和手册共享一个可解释的几何母题，页面角色只调整面积与密度。所有形状由共享布局和 CSS 生成，普通页面和 Markdown 手册正文不写页面级几何标记。

分析哲学相关视觉由 [`design-system/philosophical-visual-language.md`](design-system/philosophical-visual-language.md) 约束：只使用与项目直接相关的表达、命题、关系、对象和证据线图，不把哲学家肖像、古典装饰或名言当作技术内容。

修改页面前从 [`design-system/README.md`](design-system/README.md) 进入设计路由，并按页面角色读取门户、目录、专题、Endem 应用、手册或共享组件对应文档。设计文档目录被 Jekyll 排除，不会生成公开站点页面。

修改公开文案、组件名称、制品术语、动作、文件名或路由时，还必须遵循 [`design-system/language-and-naming.md`](design-system/language-and-naming.md)。Noemion 只作为品牌；Endem 是 `end` 与表示最小区别单位的 `-eme` 融合形成的新词，表示最小、独立有效且可验证的期望终态单元。正式扩展名为 `.endem`，唯一公开 CLI 为 `endem`。

每个 Endem 按固定顺序表达 `rhem`、`semion`、`skena`、`telis`、`krin` 与 `apor`。`rhem` 保存来源记号，`semion` 保存经确定性规则或范围有限具名权威确认的符号与关系投影，`skena` 保存一个根中性可能事态，`telis` 保存达到或维持该事态的目标方向，`krin` 保存结构比较与决定契约，`apor` 保存仍未解决的投影缺口。规范把 `semion` 的外部确认称为语义授权；它不授予工具、部署或运行权限。六个语义面不是六段文本；禁止事项在 `skena` 内显式表达，不以另一个目标力量重复编码。

ADR-0010 规定现行语义底线：`semion`、`skena` 与观察图 `phain` 必须共享稳定符号、角色和可比较关系位置；逻辑形式由图结构显示，不设置自填的 `logical_form`、`valid` 或 `true` 字段；无可接受投影、可表达但未获授权的歧义、观察不足和求值故障分别使用 `aseme`、`apor`、`agno` 与 `fault`，不得互相代替。

ADR-0011 规定 END-FMT 0.1 的实验性容器边界：64 字节固定前导、48 字节记录目录、六种关键记录、受限确定性 CBOR 和 END-P0 有限预算。结构接受必须与 END-CORE 语义接受分离；当前字节不构成稳定 ABI，也不承诺向后兼容。

ADR-0012 参考 P0-LANG-001 留下的历史 C/Rust 研究结果，把 Rust 1.97.0 记录为未来 Ktisor 与制品形成侧读取核心的候选语言。项目当前不运行该实验，也没有组件实现；进入代码阶段后必须重新审查工具链、依赖和验证范围。

ADR-0013 保留 END-P0 作为结构实验，并建立 profile 2 的 END-P1 作为首个设计 Profile。END-P1 固定六个记录的字段键、嵌套 map、枚举、规范数组顺序与引用闭包；当前 14 个字节向量供版本化验证脚本比较 3 个语义接受和 11 类预期拒绝，其中包含正负极性、非空 `apor`、截断、目录乱序、非最短 CBOR以及资源边界。它仍不是稳定 ABI，也没有组件实现。

ADR-0014 采用首个实验性 Ktisor 来源清单。它用直白的逐行指令分开自然语言来源、授权投影和未决 <code>apor</code>，并确定性映射到 END-P1；它不是稳定源语言，正式语言出现后直接删除。

ADR-0015 分开五个结果域：制品生命周期、满足判断、权威决定、Drase 会话终止，以及 Iknem 有效性与证据覆盖度。外部 Agent 的 `completed`、工具成功和会话正常结束都不能直接成为 `met` 或 `accepted`；这项决定不增加 END-P1 字段，也不表示决定引擎已经实现。

ADR-0016 固定 `mene` 的抽象时间与连续性语义：跨系统时段使用具名权威解析的 `fixed` UTC 半开区间，会话内经过时长使用具名事件和单调时钟的 `elapsed` 范围；连续性只使用 `strict` 或完整 `budgeted` 政策。END-P1 继续只支持 `kine`，当前没有时间字段或运行组件。

ADR-0017 分开否定事态、记录缺席和观察故障。负目标保留同一关系、角色与顺序；空日志和未命中查询默认只能支持 `agno`。只有具名权威证明有限观察范围已经封闭时，完整缺席才能支持 `met`；END-P1 当前只补齐原子负极性向量，没有封闭声明字段或运行组件。

ADR-0018 固定抽象量化范围与集合成员资格。`all`、`some`、`at_least`、`at_most` 和 `exactly` 必须绑定一个关系角色、成员权威、截止点与身份规则；基数只按不同成员计数，空集合不能默认产生满足。END-P1 当前没有量化字段，也没有成员目录或求值组件。

ADR-0019 固定抽象测量谓词与阈值契约。可测量判断必须先固定构念、总体、数值域、单位、观察窗口、测量程序、聚合器、阈值和不确定度政策；固定基准分数不得冒充对未测试总体的推广结论，点估计也不得越过阈值区间单独决定满足。END-P1 当前没有测量字段，也没有采集、统计或求值组件。

ADR-0020 固定抽象复合事态与判据组合。一个 Endem 只能用有限无环的 `all_of / any_of` 描述同一不可分终态，`skena` 与 `krin` 叶必须对齐；四种结果按固定矩阵传播，决定性短路必须保留依据和求值覆盖。独立目标仍须拆成多个 Endem 与 Synem。END-P1 当前没有组合字段，也没有组合求值组件。

ADR-0021 与 SYN-CORE 固定 Synem 的抽象组合边界。Synem 至少包含两个精确 Endem 和全部必需传递依赖；引用唯一绑定，图有限无环，权限只取交集，成员结果保持独立。会话期激活只选择固定成员，并使用 `active / inactive / unresolved / error`；它不改变闭包身份、不映射为满足结果，也不扩大权限。当前没有物理 Synem 格式或组件实现。

ADR-0022 与 IKN-CORE 固定 Iknem 的抽象证据边界。每项记录必须绑定精确主体、范围、有限无环溯源、观察、类别、限制和披露；有效性由外部政策评估，覆盖相对精确 `krin` 计算，最终决定仍由具名权威作出。当前没有物理 Iknem 格式或组件实现。

ADR-0023 固定 Endem 内容标准分层：END-CORE 定义通用内容语义，END-P1 定义当前封闭内容 Profile，END-FMT 定义实验性容器。容器接受、Profile 接受和内容接受必须分别报告，任何一层成功都不能提升为目标满足、签名、运行或最终接受。

ADR-0024 与 DRO-CORE 固定 Dromen：它是 Drasor 为一个 Drase 会话从精确 attested Endem 或 Synem、政策、环境、能力、预算和证据责任封存的只读执行契约。Dromen 永远不是文件、凭据包、可转移状态或可恢复权限；实质漂移使旧契约失效。Iknem 是绑定明确主体、声明范围、方法、环境、结果和限制的证据，只支持声明范围内的判断，不能自动升级为最终验收。

ADR-0025 与 DIA-CORE 固定跨对象结构化诊断：机器码与人类消息分开，诊断必须固定生产语境、失败层次和类型化位置，并确定性选择唯一主阻断诊断。恢复分类不授予权限，外部协议错误不等于本地结果，披露与资源必须有界；阻断错误不得伴随部分可信成功。当前没有诊断生产器、协议适配器或运行时。

ADR-0026 与 ADP-CORE 固定 Drasor 外部协议适配边界：绑定精确协议版本和对端，能力取交集，外部状态与本地结果分开，映射保留来源和损失，取消不冒充回滚，重试需要幂等证据，异步交付需要完整证据，凭据和网络目标保持最小化。当前没有 MCP、A2A、HTTP、SDK 或其他协议 Profile 和适配器实现。

ADR-0027 与 ID-CORE 固定跨制品精确内容身份与签名边界：完整身份绑定对象语境、算法、长度和摘要，安全引用不依赖名称、路径、URL、build ID 或短显示；签名陈述、验证材料、主体授权、截止点有效性、撤销、决定与可复现性分别判断。裁剪、调试、压缩和迁移制品各有身份及显式关系。当前没有冻结发行算法、签名物理 Profile、证书、透明日志、撤销协议、Semantic Key 或密码组件实现。

ADR-0028 与 TEXT-IDENTIFIER-CORE 固定跨制品文本与标识符边界：来源字节、严格 UTF-8 解码文本、显式变换、结构标识符、范围、人类显示和模型实际输入分别绑定；当前来源内容与 END-P1 结构标识符不做隐式规范化，结构标识符保持 ASCII、大小写敏感且与 locale 无关。双向显示、不可见字符、同形提示和模型相似度不得改变身份或取得语义权威。当前没有 Unicode 处理器、规范化器、同形检测器或模型输入网关。

ADR-0029 与 AUT-CORE 固定跨制品权威与授权决定边界：意义确认、动作授权、会话能力和最终决定分别判断。语义授权只确认精确来源中的一个候选投影；动作授权另以精确政策、主体、对象、动作、目的、范围、截止点与失败责任形成 `grant / deny / defer`。委托只能逐级收窄，任一授权都不能被提升为真值、满足、证据或最终接受。当前没有权威目录、政策求值器、同意界面、能力代理或决定服务。

ADR-0030 固定 Endem 内容与授权伴随关系：内容身份只由身份域内的规范字节决定，END-P1 中看似权威的字段只是待外部解析的选择器，不能自证授权。独立 `.endem` 最多达到 Profile 接受；完整内容接受还需精确绑定的外部授权决定。签名、证据、授权和最终决定都不能改变同一 Endem 的内容身份。授权伴随物理 Profile 仍未冻结，也不新增制品或组件。

ADR-0031 记录发布名称冲突门禁：采用 Iknem 表示有范围证据记录，采用 Drasor 表示受限执行域，并将对应动作固定为 `drase`。当前阶段不保留旧名称路由、别名、重定向或兼容垫片；更名不改变 IKN-CORE、DRO-CORE、结果域、身份或权限边界。

ADR-0032 修复此前没有把大小写无关公开动作作为独立发布面检查的遗漏。PFA Open Inference Engine 使用相同字母组合且处于相邻的人工智能工程发现空间，因此确定性制作组件与动作直接改为 Ktisor/`ktise`。更名不改变唯一写入责任、规范字节、内容身份或权限边界。

ADR-0033 将容易被误读为 `.txt` 文件的旧文本标准 ID 直接替换为 TEXT-IDENTIFIER-CORE，条款前缀采用 `TEXT-*`，公开入口采用 `/specifications/text-and-identifiers.html`。这个标准约束跨制品字符串槽、结构标识符、显示和模型输入，不对应原始文本文件，也不创建新格式或文本处理组件。旧 ID、文件、向量目录、测试名和公开路由不保留别名、重定向或兼容垫片。

ADR-0034 把目标语言读音和词表内口头区分加入发行名称门禁。职责、书写检索、读音稳定和听辨必须分别通过；现行职责保持有效，但具体发行拼写与读音尚未冻结。`Iknem`、`Ktisor/ktise` 和 Endem/Synem 仍需优先复核；`kine/mene` 已先未通过桌面门禁。读音提示不是命令别名，TTS、ASR 或语音模型输出也不能替代人类证据、授权或最终决定。

[`spec/telis-release-terms-proposal.md`](spec/telis-release-terms-proposal.md)已完成 `kine/mene` 的发行拼写桌面筛选：现有英语词义、职责透明度与首次阅读门禁足以判定它们不适合作为首次正式发行拼写。现行规范值暂不改变；`reach/maintain` 只是等待独立人类朗读、听写、职责匹配和反例验证的首选候选，不是别名或现行枚举。

ADR-0035 把公开动作收敛为 `ktise`、`elenk`、`pleko`、`theor` 与 `drase`。派生封装由对应制品生产者在 Profile 确定后承担；签名保持为独立外部集成；差分、恶意输入、复现和互操作检查仍是发布前验证责任。三类责任不再占用公开动作名，也没有兼容别名。

[`spec/release-terminology-simplification-proposal.md`](spec/release-terminology-simplification-proposal.md)在读音门禁之前增加专名必要性审查。桌面结论暂时保留 Endem 进入人类验证，并建议把 Synem、Dromen、Iknem、Ktisor、Theor、Drasor 及五个动作分别同 Endem closure、session contract、scoped evidence record、deterministic producer、independent inspector、bounded runner 和 `form/check/compose/inspect/run` 比较。提案不是 ADR、规范、别名或现行 CLI；只有人类验证通过并形成迁移 ADR 后，才会一次性修改规范 ID、字段、页面、路由和向量。

[`spec/semantic-facet-terminology-proposal.md`](spec/semantic-facet-terminology-proposal.md)继续审查六个语义面与结构化观察的现行拼写。桌面结论保留全部职责分层，但建议把 `rhem/semion/skena/telis/krin/apor/phain` 同 `source_expression/meaning_projection/situation/goal_direction/satisfaction_criteria/unresolved_meaning/structured_observation` 比较。候选不改变一个根事态、授权、观察对齐、满足或结果域，也不是现行字段；人类验证和迁移 ADR 形成前不修改 END-CORE、Profile、来源清单或向量。

[`spec/lifecycle-and-result-terminology-proposal.md`](spec/lifecycle-and-result-terminology-proposal.md)发现生命周期词表还存在对象边界问题：`attested` 把外部多签名、验证政策、截止点与撤销关系压成 Endem 自身的单值状态，Dromen 提案向量的 `subject.attested` 布尔值也不足以保存这些责任。提案把迁移拆成两条轴：对象边界修正可以暂时保留 `nascent/coherent`，只把外部陈述、验证记录和依赖方判断移出内容状态；发行命名再比较 `formed/resolved/undetermined/no_allowed_projection/stopped` 并等待人类证据。提案不修改现行规范、向量或结果值。

[`docs/terminology-and-pronunciation.md`](docs/terminology-and-pronunciation.md)把该门禁落实为两阶段人类验证：先用独立首次朗读发现自然变体，再用另一批听者在清晰与远程会议条件中完成名称选择、手写拼写和职责匹配。60 个零关键混淆判断只支持约 5% 的单侧 95% 上界，不证明全球无错误；当前研究尚未执行。

主产物流按“来源 → `ktise` → Endem → `pleko` → Synem → 生产者物理封装 → 外部发布与签名 → `drase` → Dromen → Iknem → 人工或确定性验收”组织。每项正式输入必须有明确生产者，每项正式输出必须有明确消费者或说明它只服务人工检查。

Ktisor 负责确定性的 `ktise`、`elenk` 与 `pleko`；模型不得决定规范字节、内容身份或签名。外部签名集成位于独立密钥权限域。`theor` 背后的 Theor 必须与生产写入路径独立实现、保持只读且无写入/密钥/运行权限；`drase` 背后的 Drasor 必须位于独立最小权限域。统一 CLI 不能被描述成统一实现或统一权限。

模型、检索与智能体控制位于确定性 Ktisor 外部。模型只能提出不可信来源候选、计划和能力参数，不能修改已封装或已签名制品、删除 `apor` 中的歧义、自行扩大 Drasor 权限或宣告验收通过。控制平面负责版本化上下文、类型化能力、策略检查、观察反馈、预算与人工升级，并把结果记录为有范围的 Iknem。

目标、计划与重规划的当前边界记录在 [`spec/planning-and-replanning-proposal.md`](spec/planning-and-replanning-proposal.md)。Endem/Synem 固定终态，Dromen 固定会话上限，可变计划留在控制平面；步骤、工具、handoff、A2A/MCP Task 和轨迹完成都不能直接成为目标满足或最终接受。该提案不创建计划制品、命令、组件或 CORE；责任分配只有形成正式 ADR 后，才会进入现有规范。

语义等价与迁移的当前边界记录在 [`spec/semantic-equivalence-and-migration-proposal.md`](spec/semantic-equivalence-and-migration-proposal.md)。精确身份、封闭结构同构、有范围观察等价、迁移、强化/弱化和模型相似度必须分开；当前没有通用裁剪动作或裁剪等价，无法依据冻结的保留关系证明允许变换时必须保留或失败。该提案不创建 Semantic Key、等价制品、命令、组件或 CORE；责任分配只有形成正式 ADR 后，才会进入现有规范。

`END-DET-001` 中的确定性只比较同一封闭形成输入：实际使用的解码文本与文本槽、严格解码 Profile、显式变换和损失、授权决定、配置、依赖、规范、内容 Profile 与格式版本必须全部固定。项目不再使用未定义的“规范化来源”，也不把来源到 Endem 再到显示文本的回转写成通用语义等价证明。

状态变化与因果归因的当前边界记录在 [`spec/state-change-and-causal-attribution-proposal.md`](spec/state-change-and-causal-attribution-proposal.md)。现有 `krin` 可以判断终态，却不能单凭后态证明动作发生、状态转变或某主体造成结果；提案因此建议把 `kine` 澄清为“要求事态达到成立”的目标方向。该结论仍在研究，不修改 END-TEL-001，也不创建因果制品、命令、组件或 CORE。

预览、模拟与批准的当前边界记录在 [`spec/preview-simulation-and-approval-proposal.md`](spec/preview-simulation-and-approval-proposal.md)。预览只说明决定者看到了什么，dry-run 只说明声明条件下预计什么，grant 只允许精确请求尝试；执行、事后观察、满足与最终决定继续分别判断。该提案不创建预览制品、模拟格式、批准结果域、命令、组件或 CORE；责任分配只有形成正式 ADR 后，才会修订现有 TEXT-IDENTIFIER、AUT、DRO、ADP、IKN、ID、END 与 DIA。

记忆、检查点与恢复的当前边界记录在 [`spec/memory-checkpoint-and-resumption-proposal.md`](spec/memory-checkpoint-and-resumption-proposal.md)。提案分开九类状态：会话历史只是候选输入，跨运行记忆必须绑定来源、适用范围与截止点，压缩必须披露损失，检查点不是 Dromen 或证据，工作区快照不恢复远端状态，外部 Task 句柄不证明历史完整；恢复必须重新验证并建立新会话，重放、重试、回滚与补偿分别处理。该提案不创建记忆制品、检查点格式、恢复命令、组件或 CORE；责任分配只有形成正式 ADR 后，才会修订现有 TEXT-IDENTIFIER、ID、DRO、ADP、AUT、IKN、DIA、END 与 SYN。

能力发现与调用的当前边界记录在 [`spec/capability-discovery-and-negotiation-proposal.md`](spec/capability-discovery-and-negotiation-proposal.md)。Agent Card、工具列表和 schema 只是能力声明，协议初始化只形成协商结果，AUT 决定动作授权，Dromen 固定会话上限，调用前还要核对即时可用性；列表新增不能扩大旧会话，一次成功也不能成为长期权限、`met` 或 `accepted`。该提案不创建 `CAP-CORE`、能力制品、命令、组件或新专名；责任分配只有形成正式 ADR 后，才会进入现有 ADP、AUT、DRO、DIA、IKN、ID、TEXT-IDENTIFIER 与 END。

软件 Agent 身份与责任链的当前边界记录在 [`spec/software-agent-identity-and-accountability-boundaries-proposal.md`](spec/software-agent-identity-and-accountability-boundaries-proposal.md)。模型身份、Agent 定义、部署、工作负载、运行实例、会话、凭据、主体委托和一次动作分别定位不同事实；服务账户、工作负载认证或 Agent Card 都不能替代实际行动者、被代表主体与逐动作授权。该提案不创建 Agent 身份 CORE、制品、目录、服务、命令、组件或新专名；责任分配只有形成正式 ADR 后，才会进入现有 ID、AUT、DRO、ADP、IKN、DIA 与 TEXT-IDENTIFIER。

并行与推测执行的当前边界记录在 [`spec/parallel-and-speculative-execution-proposal.md`](spec/parallel-and-speculative-execution-proposal.md)。并行只改变尝试顺序，不扩张权限或预算；分支默认只产生候选，外部副作用必须通过单一提交路径重新核对对象身份、授权、会话、协议和交付前提。取消不能撤销已经发生或未知的效果，最快完成、模型评分和外部 Task completed 也不能成为提交权、`met` 或 `accepted`。该提案不创建 `PAR-CORE`、事务制品、调度器、命令、组件或新专名，责任仍优先归还 DRO、AUT、ADP、ID、IKN、DIA、END 与 SYN。

模型、适配器与能力域的当前隔离边界记录在 [`spec/model-adapter-isolation-proposal.md`](spec/model-adapter-isolation-proposal.md)。隔离必须分别说明模型输入、控制面、授权、凭据与实时句柄、协议适配、文件、网络、资源终止、观察和外部目标；容器、seccomp、超时或提示词都不能单独成为隔离证明。模型不接收原始凭据和实时句柄，强制控制不可用时对应能力关闭失败，取消或主进程退出也不等于子进程、远端任务和副作用已经停止。该提案不创建 `ISO-CORE`、`SANDBOX-CORE`、隔离制品、沙箱格式、命令、组件或新专名，责任仍优先归还 DRO、AUT、ADP、DIA、IKN、ID 与 TEXT-IDENTIFIER。

模型参与评测的当前边界记录在 [`spec/model-assisted-evaluation-proposal.md`](spec/model-assisted-evaluation-proposal.md)。评测目的、构念、可观察标准、题目与候选、协议、模型评审调用、原始输出、统计汇总和使用决定必须分开。模型评审输出继续是 `model-candidate`；位置、冗长、格式、来源、提示注入、相关评审者和模型漂移都要接受反例检查。多个模型投票、排行榜或模型自报置信度不能自动成为独立证据、统计区间、`met` 或 `accepted`。该提案不创建 `EVAL-CORE`、`JUDGE-CORE`、评测制品、裁判服务、命令、组件或新专名，责任仍优先归还 END、TEXT-IDENTIFIER、ID、ADP、DRO、IKN、AUT 与 DIA。

模型训练与更新的当前边界记录在 [`spec/model-training-and-update-boundaries-proposal.md`](spec/model-training-and-update-boundaries-proposal.md)。会话历史、检索、提示变化、训练数据、反馈、基础模型、适配权重、训练活动、评测、发布和回滚必须分开；人工或模型反馈先是有范围记录，训练或微调产生新的外部派生模型身份。可复现环境、权重字节复现、行为评测、用途适合和发布决定也是五个不同主张。该提案不创建 `TRAIN-CORE`、`MODEL-CORE`、`FEEDBACK-CORE`、模型制品、训练平台、命令、组件或新专名，责任仍优先归还 TEXT-IDENTIFIER、ID、AUT、IKN、ADP、DRO、DIA 与 END。

模型开放性与软件自由的当前边界记录在 [`spec/model-openness-and-software-freedom-boundaries-proposal.md`](spec/model-openness-and-software-freedom-boundaries-proposal.md)。托管 API、模型参数、架构、推理与训练代码、训练数据说明、数据、文档、许可、首选修改形式、复现和外部分类必须分开；开放权重不自动等于 Open Source AI、自由软件或可复现模型。Apache-2.0 只覆盖实际置于其下的仓库材料，不自动扩张到未来模型全栈和第三方对象。该提案不创建 `OPEN-MODEL-CORE`、`LICENSE-CORE`、模型发行格式、合规服务、命令、组件或新专名，责任仍优先归还 ID、AUT、IKN、ADP、TEXT-IDENTIFIER 与 DIA。

托管人工智能服务与用户控制的当前边界记录在 [`spec/hosted-ai-service-and-user-control-boundaries-proposal.md`](spec/hosted-ai-service-and-user-control-boundaries-proposal.md)。软件自由、实际执行控制、数据控制和服务可移植性必须分开；第三方托管执行、自主管理执行、设备内执行和通信服务也不能只用“本地”或“云”合并。调用成功、AGPL、数据驻留、导出或 API 兼容都不能自动证明用户控制服务实例、完整复现或无损切换。该提案不创建服务 CORE、网关、云平台、导出格式、命令、组件或新专名，责任仍优先归还 ID、ADP、AUT、DRO、IKN、TEXT-IDENTIFIER、DIA 与 END。

软件 Agent 数据使用、保留与删除的当前边界记录在 [`spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.md`](spec/software-agent-data-use-retention-and-deletion-boundaries-proposal.md)。访问、授权、实际处理、披露、保留、删除请求、删除操作、清除验证、清除确认、备份与派生物传播必须分开；TTL、逻辑删除、命令成功或供应商收据不能自动证明全部副本不可恢复。该提案不创建数据、隐私或删除 CORE，不建立数据制品、删除服务、清除证明、命令、组件或新专名，责任仍优先归还 ID、TEXT-IDENTIFIER、AUT、ADP、DRO、IKN、DIA、END 与 SYN。

技术长文、Endem 应用介绍和手册正文还必须读取 [`design-system/readability.md`](design-system/readability.md)。1200px 是连续画布而不是正文行宽：普通段落保持约 700–760px 阅读列，桌面正文采用 17–18px 与约 1.75–1.8 行高。需要利用右侧空间时，优先形成约 800px 主阅读列与约 380px 粘性信息栏，并从对应页面角色的引言区起让信息栏持续承载章节目录、成熟度、可用状态、关键制品、输入输出或下一阅读入口；没有足够信息时使用单列，不为排版保留空栏。

图片只在能增强概念解释、页面辨识或内容氛围时使用。选择顺序为许可清晰的素材库、经授权的项目素材、项目定制生成图；素材必须下载到仓库并压缩，不能依赖第三方热链。来源、许可、裁切焦点、替代文本和生成提示记录在 [`design-system/images.md`](design-system/images.md)，公开页面不暴露设计参考或模仿关系。

唯一 Endem 应用及五个动作的视觉签名见 [`design-system/internal-tools.md`](design-system/internal-tools.md)。默认布局可以按当前动作写入状态标识，共享 CSS 再应用有限的配色、制品面板签名、网格角度和强调状态；应用页不维护页面级 CSS。手册可以继承动作强调色，但正文、目录和分页继续遵循统一手册规范。视觉差异不得把动作伪装成独立产品。

Noemion 的视觉识别由“语义频谱”与 Endem 语言形成：薄荷、青蓝、朱橙和琥珀只标记来源记号、意义投影、可能事态、满足观察与未决边界；黑色记录面板表示可检查的关系结构、引用、闭包和证据范围。任何装饰都不得取代权威性、失败语义和证据边界。

全站统一品牌、字体、颜色、基础间距、紧凑面包屑和目录引擎；具体目录分组、正文结构、表格、清单、手册分页和状态展示由模块职责决定。面包屑链接保留至少 40px 的命中高度，同时减少整条路径占用的垂直空间并允许自然换行。模块可以共享布局组件，但不得为了视觉对称强行增加不适用的章节。

普通专题页不再使用固定空白偏移，也不通过 `nth-of-type` 或 `:has()` 猜测版式。每个 HTML 章节显式使用 `content-split`、`content-stack`、`content-band`、`content-wide`、`content-grid` 或 `content-rows` 中的一种；需要镜像论证时才附加 `content-split-reverse`。只有真实目录、项目状态、证据边界或阅读概览可以使用共享摘要栏；控制器依据实际可用空间动态决定双栏或单栏，短页面和已有专用侧栏的页面不重复套用。

运行测试前必须安装可从命令行调用的 Node.js。源码阶段按 `sitemap.md` 验证全部页面的 Front Matter、固定路由、共享布局、导航数据和模块接口；Jekyll 构建后，质量测试检查 `_site` 中的最终 HTML、生成的导航 JSON、路由模块行为、页面类型和手册高亮。

`endem/index.html` 是应用入口而非手册：必须包含“项目 / Endem”面包屑，以及“它解决什么问题”“当前状态”“它怎样工作”“它读取什么，产生什么”“它不会做什么”“继续阅读”六个语义章节。当前状态必须明确实现与发行成熟度；`.endem`、`endem` 和五个动作已经冻结，但未冻结的参数、字节布局和能力不得伪装成可用接口。只有实际存在实质内容时才链接对应 `endem/docs/` 专题。

“继续阅读”章节以资源卡片结束，只承担规范、组件、开发路线、Endem 应用或手册目录的跳转职责；不得在卡片后追加孤立的候选接口、内部约束或重复状态段落。仍有必要公开的接口边界必须在“当前状态”或“它不会做什么”中用完整上下文说明。

## 内容质量与研究治理

内容审查不得使用一套完整模板覆盖全部 HTML。Why / How / What、产品开发生命周期、研究治理和详细设计是可选择的检查视角，只有与页面职责相关时才进入正文；目录页不需要伪造详细设计，资源页不需要套用工具契约，手册页也不应被管理术语打断阅读。

### 全站可读性规则

1. 页面先回答读者正在问什么、为什么重要和直接结论，再引入 Endem、`rhem/semion/skena/telis/krin/apor`、Synem、Dromen、Iknem、Ktisor、Theor 和 Drasor 等项目术语。
2. 缩写和专业词第一次出现时使用完整名称或直白解释；不能要求读者先理解整个 Noemion 体系才能读懂入口页。
3. 抽象机制优先用一个具体问题、因果链、流程或对照关系解释，再进入结构、字段和不变量。
4. 哲学概念只作为问题框架和工程启发；必须明确区分思想来源、工程类比、正式规范和验证证据，不能用哲学术语替代技术定义。
5. 段落只承担一个主要论点；并列概念优先使用列表、表格或短卡片，但不为视觉整齐拆碎本应连续的论证。
6. 链接文字应说明读者点击后能回答什么问题，避免只有“更多”“详情”或重复页面标题。
7. 已确认原则、设计提案、开放问题、未来阶段和真实成果继续使用明确状态语言；清晰易读不能以省略证据边界为代价。
8. 正式 HTML 面向开发者、普通用户和潜在使用者，只解释项目、产品、规范、使用场景与真实状态。阶段限制写成“当前没有组件实现”等客观事实；状态说明使用“当前策略、已有成果、正在研究、待定内容、限制条件”，不使用内部治理话术，正式字段或不可替代的技术术语除外。
9. 网站作为后续设计、实现和互操作工作的标准与规范入口，采用“直白解释 + 精确定义”双层表达；解释可以增加，但不得弱化规范术语、约束强度、不变量、失败语义、成熟度标记和权威来源。
10. 外部书目、论文、规范、下载和其他资源链接必须使用能说明目标内容的链接文字；不得把完整 URL 当作正文标签。需要复制地址时由浏览器提供，站内导航继续使用明确的目标名称。
11. 所有公开界面使用产品化语言，直接说明现状、能力、限制、开发计划和验证结果；不出现“本页”“阶段门”“证据门”“放行”“退出证据”或未解释的 IPD 等内部制作与管理术语。规范、安全和学术内容可以保留必要专业词，但首次出现要给出直白解释。
12. 组件、动作和界面元素必须说明存在价值、与上下游的关系以及省略或合并条件；没有正式消费者的输出只能标为诊断、人工材料或候选接口，不能为了目录或视觉对称假装形成闭环。
13. 人为创造的工具、组件、制品、动作和关键领域术语优先使用不含数字的短词；ADR、条款、Profile、协议版本、日期、位宽和向量编号等精确标识可以保留数字，但不能被写成概念名称，正文必须同时说明其直白职责。
14. 当前状态页、指南和资源页不手工复制场景、威胁、条款或向量总数；精确范围只由对应源文件、`spec/registry.json` 和版本化验证结果给出。日期明确的历史记录可以保留当时数量，但不得与同一句中的分类明细自相矛盾。
15. 规范解释页先用一个贯穿案例说明对象、输入、判断和失败责任，再按开发者问题选择能够区分失败域的代表场景。完整场景、反例和向量保留在版本化权威源中，不在 HTML 中逐行复制非规范语料。

### 模块化内容规范

| 模块或页面类型 | 应重点回答 | 不应强行套用 |
| --- | --- | --- |
| 项目门户与 `about/` | 项目背景、受众、问题、范围、非目标、原则、状态和主要入口 | CLI 参数、规范字段或手册式逐章导航 |
| `architecture/` 与 `components/` | 系统关系、职责分层、制品或控制流、存在必要性、上下游、信任与失败边界、关键决策和开放问题 | 发布资源清单、重复规范字段定义或没有消费者的形式组件 |
| `specifications/` | 权威来源、成熟度、术语、规范性要求、数据模型、不变量、错误语义、版本演进和一致性验证 | 营销承诺、未经批准的候选结论或使用指南式重复说明 |
| 跨项目 `docs/` 指南 | 面向读者任务说明前置知识、背景、阅读或操作顺序、预期结果、常见误解、下一步和权威参考 | 复制第二套规范，或机械加入与任务无关的 IPD、专利和架构章节 |
| Endem 应用页 `endem/index.html` | 在既定六个章节中说明问题、状态、五个动作、输入输出、Ktisor/Theor/Drasor/密钥边界和后续阅读入口 | GNU 手册章节编号、完整 CLI 手册或顺序分页 |
| `endem/docs/` 与专题页 | 按 GNU 手册方式组织目录、连续阅读路径、格式、绑定、安全、运行、诊断、测试和参考；只编写唯一 CLI 实际需要的专题 | 为动作对称创建空页面，或把五个动作包装为独立产品 |
| `downloads/` 资源页 | 真实资源状态、版本、格式或平台、大小、许可、来源、校验值、签名、SBOM、发布日期、撤回与归档信息 | 虚构下载按钮、仓库、版本、校验值或安装命令 |
| `development/` | 路线图、已完成工作、当前工作、后续规划、规范/ADR 流程、测试、安全、贡献和报告渠道 | 把计划任务写成已完成能力，或把内部评审条件直接写给使用者 |
| `news/` 与 `faq/` | 新闻记录日期、范围、证据、限制和下一决策点；FAQ 直接回答高频问题并链接权威页面 | 用占位公告制造历史，或在 FAQ 中重新定义技术规范 |

入口和目录页面可以简洁，只要能说明模块职责、当前状态、内容地图与返回路径；专题页面才承担与其主题匹配的概要或详细设计。评价页面质量时，应先判断模块属性和读者任务，再使用相应规范检查，不能以章节数量、字符数或模板一致性代替内容质量。

研发治理按问题定义、设计规划、开发实现、系统验证、发布维护和退役演进组织。公开阶段状态只展示已经完成的工作、正在进行的任务、后续规划及其真实验证结果；内部评审条件保留在版本化计划和决策记录中。研究与知识产权内容还应逐步建立研究问题、可证伪假设、创新点候选、现有技术边界、实验或测试证据、ADR、版本和规范条款之间的追溯关系。论文、专利、软著或标准化意图不等于成果已经形成；专利候选在公开披露前需要知识产权审查，标准提案需要稳定术语、可测试条款、互操作性案例和安全分析。

逐页审查状态与剩余缺口维护在 [`content-quality-audit.md`](content-quality-audit.md)。该清单用于规划内容工作，不是对页面成熟度的自我认证。

## 正式路由注册表

公开且权威的正式路由注册表维护在 [`sitemap.md`](sitemap.md)。该文件按内容家族登记全部正式 HTML URL、阅读顺序与职责，并由质量测试直接核对 Jekyll 源文件和构建产物；README 不再复制第二份路由表。

## 贡献

[`CONTRIBUTING.md`](CONTRIBUTING.md)说明当前可接受的资料、研究、术语、规范和网站贡献，以及主张、证据、读音与验证要求。公开问题使用仓库的结构化 Issue 表单；当前没有私密安全报告渠道，不得在公开 Issue 中披露未公开漏洞、凭据、密钥或个人数据。

## 许可证

除非文件中另有说明，本仓库的源码与文档采用 [Apache License 2.0](LICENSE) 发布。该许可证不授予使用 Noemion 名称、标识或相关商标的权利；为说明作品来源或重现许可声明所必需的合理使用除外。

## 维护规则

1. 内容修改只编辑权威专题页面；项目介绍、正式规范、开放问题、Endem 应用页和 CLI 手册保持职责分离。
2. 全局 HTML 外壳只编辑 `_layouts/default.html`，站点头部和页脚只编辑 `_includes/`；全局颜色和正文排版只编辑 `assets/style.css`，目录样式只编辑 `assets/directory.css`。禁止页面复制公共外壳、页面级 CSS、内联 `<style>` 或 `style=`。
3. `_data/navigation.yml` 维护顶部卡片和普通模块目录；`_data/manuals.yml` 与页面 Front Matter 维护手册结构。`assets/site.mjs` 只编排按需加载，有状态控制器放在 `assets/modules/`，无状态路由逻辑保持纯函数。不得在页面源码复制目录链接或建立第二份正式路由表。
4. 唯一应用的全部页面只保存在 `endem/`。`endem/index.html` 是应用页；`endem/docs/` 只保留总览、格式、绑定、安全、运行和参考六类实质手册，不为动作制造独立产品树。
5. 新增、删除、移动或改名页面时，同步 `sitemap.md`、`_data/navigation.yml`（仅当全局或普通模块入口变化）、手册 Front Matter、对应入口、顺序导航和全部交叉链接；每个非门户页面必须保留可用的上级或指定目录返回入口。
6. 路由、目录和命名直接采用当前规范；不保留旧入口、旧路径、旧别名、重定向或兼容垫片。
7. 每次路由或页面角色变更先运行 `python3 tests/site_quality_test.py` 检查 Jekyll 源码；完整本地发布检查在构建后执行 `cp sitemap.md _site/sitemap.md`，再运行 `python3 tests/site_quality_test.py _site`，确认最终 HTML、正式路由注册表、全局目录和页面角色一致。GitHub Pages 工作流自动执行同一复制步骤。
8. 不新增并列公开工具。新增能力时先判断能否成为 `endem` 的现有动作、选项或内部组件；确有不可替代的新边界时先更新规范与 ADR，不能直接创建新的命令品牌或工具路由。
9. 正式技术规范的唯一条款源维护在 `spec/*.md`，机器可读成熟度与验证映射维护在 `spec/registry.json`；HTML 负责直白解释、成熟度和精确源链接，不能复制第二套条款。
10. `vectors/semantic/` 中的 JSON 只承载语义测试外壳，不是 `.endem` 物理格式；`vectors/wire/` 中的十六进制表达 END-FMT 实验字节。每个向量必须固定规范版本、预期结果、条款 ID 与拒绝位置；登记由 `tests/spec_contract_test.py` 检查，语义结果由 `tests/semantic_vector_test.py` 执行，字节结果由 `tests/wire_vector_test.py` 解码验证。
11. `docs/index.html` 的六个入口必须指向 `docs/` 下实际存在的任务型 HTML；这些页面负责解释和阅读路径，不替代权威规范。
12. 网页改动完成并通过源码、Jekyll 构建、构建产物和浏览器验收后，默认继续提交、推送并确认 GitHub Pages 部署，再提供在线地址；只有用户明确要求不发布时才停留在本地。
