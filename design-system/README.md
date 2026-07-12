# Noemion 页面设计路由

本目录是修改站点页面、共享布局、目录和交互动效时的设计路由入口。开始改动前，先根据目标文件或 `page_role` 读取下表指定文档；涉及多个角色时读取所有对应文档。

修改任何公开文案、组件名称、对象术语、工具名称、文件名或路由时，还必须读取 [`language-and-naming.md`](language-and-naming.md)；核心命名决定见 [`adr-0001-noemion-nomenclature.md`](adr-0001-noemion-nomenclature.md)。

修改智能体上下文、能力接口、反馈循环、运行证据或人工升级边界时，还必须读取 [`adr-0002-agent-harness-boundary.md`](adr-0002-agent-harness-boundary.md)。

修改工具输入输出、发布闭包、签名回填、运行产物或跨工具消费者关系时，还必须读取 [`adr-0003-toolchain-artifact-flow.md`](adr-0003-toolchain-artifact-flow.md)。

修改模型候选升级、运行能力、候选评价、证据闭包或最终验收决定时，还必须读取 [`adr-0004-candidate-capability-acceptance-boundary.md`](adr-0004-candidate-capability-acceptance-boundary.md)。

全局原则、品牌语言、断点和验收基线见 [`../sitewide-design-system.md`](../sitewide-design-system.md)。本目录文档负责把这些原则落实到具体页面类型，不能改变 Noemion 的成熟度、权威性或证据边界。

## 路由表

| 修改范围 | 识别条件 | 必读设计文档 |
| --- | --- | --- |
| 全站外壳、顶部导航、页脚、目录 | `_layouts/default.html`、`_includes/site-header.html`、`_includes/site-footer.html`、`assets/directory.*` | [`global-shell.md`](global-shell.md) |
| 首页门户 | `page_role: portal`、`index.html` | [`portal.md`](portal.md)、[`../homepage-design.md`](../homepage-design.md) |
| 模块目录与聚合页 | `page_role: section` | [`section.md`](section.md) |
| 架构、规范和普通专题 | `page_role: content` 且没有 `manual_id` | [`content.md`](content.md) |
| 工具项目入口 | `page_role: tool-project`、`tools/<tool>/index.html` | [`tool-project.md`](tool-project.md) 与 [`internal-tools.md`](internal-tools.md) 中当前工具条目 |
| 手册与指南 | `layout: manual` 或存在 `manual_id` | [`manual.md`](manual.md) |
| 技术长文、工具说明与手册正文可读性 | 修改正文宽度、字号、行高、固定信息栏或长内容节奏 | [`readability.md`](readability.md)，并继续读取所属页面角色文档 |
| 卡片、按钮、表格、Callout、流程、动效 | 修改共享视觉组件或状态反馈 | [`components-motion.md`](components-motion.md) |
| 图片、照片、生成式视觉、裁切与图片动效 | 新增或替换 `assets/images/`，或修改页面中的 `<img>` / 图片背景 | [`images.md`](images.md)，并继续读取所属页面角色文档 |

工具页按路径中的 `<tool>` 路由。例如修改 `tools/noeminspect/index.html` 时，先读 `tool-project.md`，再读 `internal-tools.md#noeminspect`；修改 `tools/noemlink/docs/*.md` 时读 `manual.md`，并继承 `internal-tools.md#noemlink` 的工具视觉签名。

## 冲突处理

1. 项目架构、安全与内容治理规则优先于视觉对称。
2. `sitewide-design-system.md` 定义全局基线，本目录角色文档定义局部布局。
3. 角色文档与实际 CSS 不一致时，先判断是实现偏离还是规范过期；不得静默以当前实现覆盖规范。
4. 页面需要新范式时，先新增对应设计文档和路由，再编写实现。
5. 设计文档不参与 Jekyll 公开站点构建，不得从正式页面链接到本目录。

## 修改后的最低验证

- 运行 `python3 tests/site_quality_test.py`。
- 涉及 JavaScript 时运行 `node --check assets/directory.js`。
- 涉及布局或样式时检查桌面约 1512px 与移动约 390px。
- 检查键盘焦点、减少动态效果、深浅色和页面级横向溢出。
- 手册变更还要构建 `_site`，确认动态目录、索引和分页顺序。
