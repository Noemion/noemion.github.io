# Noemion Pages Repository Rules

- 本目录对应 `https://github.com/Noemion/noemion.github.io`，发布地址为 `https://noemion.github.io/`；仓库名和站点域名使用全小写。
- 本仓库是 GitHub Pages 的 Jekyll 源目录。保留 `_config.yml` 与 `.github/workflows/pages.yml`，不得添加 `.nojekyll`。
- 站点必须由 Jekyll 生成：公共文档外壳只维护在 `_layouts/` 与 `_includes/`；正式页面只保留 YAML Front Matter 和职责对应的 `<main>` 正文，不复制 `<head>`、站点头部或页脚。
- 修改前先读 `README.md`；其中的正式 HTML 注册表、页面角色、模块化内容规范和维护规则是本仓库的唯一详细路由来源。
- 当前处于开发阶段，不保留旧 HTML 路径、别名、重定向或兼容垫片；路由变化同步 README、共享目录配置、入口和交叉链接。
- 站点整体采用 GNU/sourceware 风格；统一基础视觉和目录引擎，但正文按项目、架构、规范、指南、工具、资源、开发、新闻或 FAQ 的模块职责编写，不套用同一内容模板。
- 全站正文必须先回答读者问题再引入项目术语：先交代现实场景、核心缺口和直白结论，再说明哲学启发、工程映射与技术名称；思想来源、工程类比、规范要求和已验证事实必须明确区分。
- 正式 HTML 只面向开发者、普通用户和潜在使用者，不得出现提示词、生成过程、用户指令、内部 review、补写过程、页面制作或为了验收而编写等幕后表述；状态信息只说明产品、规范、实现和证据本身。
- 网站是 Noemion 后续设计、实现与互操作工作的标准和规范入口；采用“直白解释 + 精确定义”双层表达，不能为了可读性删减术语边界、规范性强度、不变量、失败语义、成熟度或权威来源。
- 外部书目、论文、规范、下载和其他资源链接必须在正文中保留可见的原始 URL，不得只用概括性标题替代链接本身；解释与 URL 分开书写。内部路由仍使用能说明目标内容的链接文字。
- 工具项目页与工具文档分离；只有存在实质专题时才建立 `tools/<tool>/docs/`。
- 全站样式只在 `assets/style.css` 和 `assets/directory.css` 维护，目录数据与渲染只在 `assets/directory.js` 维护；禁止页面级 CSS 和复制目录链接。
- 公开页面不得把设计提案、候选名称、未来能力、论文、专利、软著或标准化意图表述为已实现或已获认可的成果。
- 路由或页面角色变化后先运行 `python3 tests/site_quality_test.py`；发布前构建 `_site`，再运行 `python3 tests/site_quality_test.py _site` 并检查浏览器实际渲染。
- 内容审查状态记录在 `content-quality-audit.md`；项目级要求变化时同步本文件或 README，避免规则散落。
