# Noemion 页面设计路由

本目录是修改站点页面、共享布局、目录和交互动效时的设计路由入口。开始改动前，先根据目标文件或 `page_role` 读取下表指定文档；涉及多个角色时读取所有对应文档。

修改任何公开文案、组件名称、制品术语、动作、文件名或路由时，还必须完整读取 [`language-and-naming.md`](language-and-naming.md)。Noemion 只作为品牌；Endem、六个语义面、Synem、Dromen、Tekmor、Poiet、Theor、Praxor、八个动作和唯一 CLI 是当前命名基线，设计文档不得引入旧名称或兼容入口。修改品牌、制品名、命令、扩展名或分发坐标时还必须读取并更新 [`name-audit.md`](name-audit.md)，不能用旧查询结果证明当前可用性。

修改 `.endem`、`rhem/semion/skena/telis/krin/apor`、`phain`、事态投影、引用、内容身份、规范排序、封装布局或证据排布时，先读取当前 Endem、Synem 和 Tekmor 规范，再读取 ADR-0010 与相关活跃 ADR。ADR-0009 及更早记录中的旧词只用于解释决策迁移，不得重新进入公开接口。

修改 Endem 生命周期、Poiet/Theor/Praxor 隔离、独立读取路径、GNU 工具链采用范围或外部 AI 协议落点时，先读取 `/architecture/endem-lifecycle.html`、对应组件页面和它们链接的活跃 ADR。

修改 `poie/elenk/pleko/tasse/sphra/theor/praxe/peira` 的输入输出、失败语义、发布闭包、签名回填或跨组件消费者关系时，先读取 [`internal-tools.md`](internal-tools.md)、Endem 手册与活跃产物流 ADR。

修改模型候选、上下文装配、能力接口、反馈循环、Dromen、Tekmor 或人工升级边界时，必须同时读取 Theor、Praxor 与 Tekmor 规范以及相关活跃 ADR。任何设计都不得让模型决定规范字节、删除 `apor`、扩大能力或宣告最终验收。

修改满足判断、权威决定、Praxe 会话终止、Tekmor 有效性或证据覆盖度时，必须读取 ADR-0015、Endem 生命周期、Praxor 与 Tekmor 规范。不得把外部 Task、工具调用或会话的完成状态直接映射为 `met` 或 `accepted`。

全局原则、品牌语言、断点和验收基线见 [`../sitewide-design-system.md`](../sitewide-design-system.md)。本目录文档负责把这些原则落实到具体页面类型，不能改变 Noemion 的成熟度、权威性或证据边界。

## 路由表

| 修改范围 | 识别条件 | 必读设计文档 |
| --- | --- | --- |
| 全站外壳、顶部导航、页脚、目录 | `_layouts/default.html`、`_includes/site-header.html`、`_includes/site-footer.html`、`assets/directory.*` | [`global-shell.md`](global-shell.md) |
| 前端模块、接口、数据源与按需加载 | `assets/site.mjs`、`assets/modules/*.mjs`、`_data/navigation.yml` | [`frontend-architecture.md`](frontend-architecture.md)、[`global-shell.md`](global-shell.md) |
| 首页门户 | `page_role: portal`、`index.html` | [`portal.md`](portal.md)、[`../homepage-design.md`](../homepage-design.md) |
| 模块目录与聚合页 | `page_role: section` | [`section.md`](section.md) |
| 架构、规范和普通专题 | `page_role: content` 且没有 `manual_id` | [`content.md`](content.md) |
| Endem 应用入口 | `page_role: tool-project`、`endem/index.html` | [`tool-project.md`](tool-project.md) 与 [`internal-tools.md`](internal-tools.md) |
| 手册与指南 | `layout: manual` 或存在 `manual_id` | [`manual.md`](manual.md) |
| 技术长文、Endem 应用说明与手册正文可读性 | 修改正文宽度、字号、行高、固定信息栏或长内容节奏 | [`readability.md`](readability.md)，并继续读取所属页面角色文档 |
| 卡片、按钮、表格、Callout、流程、动效 | 修改共享视觉组件或状态反馈 | [`components-motion.md`](components-motion.md) |
| 图片、照片、生成式视觉、裁切与图片动效 | 新增或替换 `assets/images/`，或修改页面中的 `<img>` / 图片背景 | [`images.md`](images.md)，并继续读取所属页面角色文档 |
| 模块几何母题、页面角色引言、章节形状与文档折页 | 修改任一正式页面的几何布局或模块视觉身份 | [`geometric-layouts.md`](geometric-layouts.md)，并继续读取所属页面角色文档 |
| 分析哲学线条、节点、命题关系与哲学相关图形 | 新增或修改任何哲学来源的视觉表达 | [`philosophical-visual-language.md`](philosophical-visual-language.md)、[`geometric-layouts.md`](geometric-layouts.md) |

修改 `endem/index.html` 时，先读 `tool-project.md`，再读 `internal-tools.md`；修改 `endem/docs/*.md` 时读 `manual.md`，并按当前任务继承 `internal-tools.md` 中对应动作的视觉签名。不得创建并列应用页或旧工具路由。

## 冲突处理

1. 项目架构、安全与内容治理规则优先于视觉对称。
2. `sitewide-design-system.md` 定义全局基线，本目录角色文档定义局部布局。
3. 角色文档与实际 CSS 不一致时，先判断是实现偏离还是规范过期；不得静默以当前实现覆盖规范。
4. 页面需要新范式时，先新增对应设计文档和路由，再编写实现。
5. 设计文档不参与 Jekyll 公开站点构建，不得从正式页面链接到本目录。

## 修改后的最低验证

- 运行 `python3 tests/site_quality_test.py`。
- 涉及 JavaScript 时运行 `node --check assets/site.mjs`、`node --check assets/theme.js`，并检查 `assets/modules/*.mjs`。
- 涉及布局或样式时检查桌面约 1512px 与移动约 390px。
- 检查键盘焦点、减少动态效果、深浅色和页面级横向溢出。
- 手册变更还要构建 `_site`，确认动态目录、索引和分页顺序。
