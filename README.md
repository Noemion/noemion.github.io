# Noemion 网站

本仓库维护 [Noemion 官方网站](https://noemion.github.io/)及其公开技术资料，包括项目介绍、架构设计、规范、指南、Endem 使用手册和开发进展。

Noemion 目前处于研究、规范与验证方案设计阶段，尚未发布 producer、inspector、runner 或 `endem` 命令行工具的实现。仓库中的测试用于检查资料、路由和草案之间的一致性，不代表组件已经实现。

## 从哪里开始

- 想了解项目：访问[网站首页](https://noemion.github.io/)。
- 读者想查找公开页面：使用[全部页面](https://noemion.github.io/pages/index.html) HTML 目录。
- 维护者想核对正式路由：查看 [`sitemap.md`](sitemap.md)。这是正式路由的唯一清单。
- 想参与内容、研究或规范工作：从[开发与贡献](https://noemion.github.io/development/)选择对应入口。
- 想了解许可证：查看 [Apache License 2.0](LICENSE)。Noemion 名称和标识不随源码许可证一并授权。

## 仓库内容

- `about/`、`architecture/`、`components/`、`specifications/`：面向开发者的项目、架构与规范说明；其中技术正文以 Markdown 作为唯一可编辑来源。
- `docs/`：入门、架构和开发等任务型指南。
- `endem/`：Endem 应用介绍和使用手册。
- `spec/`：版本化的规范条款与设计提案；Markdown 是唯一正文源，Jekyll 自动生成同路径 HTML 正式页面。
- `vectors/`：与规范条款对应的测试资料和实验性字节样例。
- `experiments/`：被正式 ADR 引用的历史研究实验与结果，不是建站维护中间材料，也不代表组件实现。
- `assets/`、`_layouts/`、`_includes/`、`_data/`：全站共享的样式、行为、页面外壳和导航数据。
- `tests/`：检查规范登记、测试资料、页面源码和构建结果。

构建生成的 `_site/` 只用于预览和检查，不是内容编辑入口。

## 修改内容

先找到与主题最接近的页面，只在权威位置修改：

- 面向开发者的技术解释与正式约束都以 Markdown 为唯一正文源并自动生成 HTML；首页、栏目入口、目录和应用入口等界面页可以保留手写 HTML，但不承载第二套技术正文。
- 指南和 Endem 手册编辑对应的 Markdown 文件，不编辑生成后的 HTML。
- 页面、路径或名称变化时，同步 `sitemap.md`、相关导航、入口和交叉链接。
- 页面样式与交互使用共享文件，不在单个页面中复制全站外壳、导航或样式。
- 页面设计通过共享样式、布局、导航数据和自动检查保持一致。

公开内容只陈述项目的真实现状、能力、限制和计划。提案、实验、测试通过或未来目标不能写成已经发布的产品能力。

## 本地预览

需要 Ruby、Bundler、Node.js 和 Python 3。Ruby 版本记录在 `.ruby-version` 中，依赖版本由 `Gemfile.lock` 固定。

```bash
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve
```

启动后访问 <http://127.0.0.1:4000/>。

## 提交前检查

普通页面和路由修改至少运行：

```bash
python3 tests/site_quality_test.py
bundle exec jekyll build
cp sitemap.md _site/sitemap.md
python3 tests/site_quality_test.py _site
```

修改 `spec/`、`vectors/` 或登记信息时，还要运行 `tests/` 中与主题对应的规范和向量检查。修改界面、布局或交互时，需要在真实浏览器中检查受影响页面和目标视口。

推送到 `main` 后，GitHub Actions 会重新构建并发布网站。
