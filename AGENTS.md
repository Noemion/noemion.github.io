# Noemion Pages Repository Rules

- 本目录对应 `https://github.com/Noemion/noemion.github.io`，发布地址为 `https://noemion.github.io/`；仓库名和站点域名使用全小写。
- 本仓库是 GitHub Pages 的 Jekyll 源目录。保留 `_config.yml` 与 `.github/workflows/pages.yml`，不得添加 `.nojekyll`。
- 站点必须由 Jekyll 生成：公共文档外壳只维护在 `_layouts/` 与 `_includes/`；正式页面只保留 YAML Front Matter 和职责对应的 `<main>` 正文，不复制 `<head>`、站点头部或页脚。
- 修改前先读 `README.md`；其中的正式 HTML 注册表、页面角色、模块化内容规范和维护规则是本仓库的唯一详细路由来源。
- 当前处于开发阶段，不保留旧 HTML 路径、别名、重定向或兼容垫片；路由变化同步 README、共享目录配置、入口和交叉链接。
- 站点整体采用 GNU/sourceware 风格；统一基础视觉和目录引擎，但正文按项目、架构、规范、指南、工具、资源、开发、新闻或 FAQ 的模块职责编写，不套用同一内容模板。
- 工具项目页与工具文档分离；只有存在实质专题时才建立 `tools/<tool>/docs/`。
- 全站样式只在 `assets/style.css` 和 `assets/directory.css` 维护，目录数据与渲染只在 `assets/directory.js` 维护；禁止页面级 CSS 和复制目录链接。
- 公开页面不得把设计提案、候选名称、未来能力、论文、专利、软著或标准化意图表述为已实现或已获认可的成果。
- 路由或页面角色变化后先运行 `python3 tests/site_quality_test.py`；发布前构建 `_site`，再运行 `python3 tests/site_quality_test.py _site` 并检查浏览器实际渲染。
- 内容审查状态记录在 `content-quality-audit.md`；项目级要求变化时同步本文件或 README，避免规则散落。
