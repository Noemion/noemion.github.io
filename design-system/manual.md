# 手册与指南设计

适用范围：`layout: manual` 或带 `manual_id` 的 Markdown 页面。

## 权威源

- 手册正文只维护 `.md` 文件；公开 `.html` 由 Jekyll 构建。
- Markdown 不复制 `<main>`、面包屑、Hero、分页、侧栏或页脚。
- 手册级配置维护在 `_data/manuals.yml`；页面只声明所属手册、分组、顺序、标题和摘要。
- 新页面的 `permalink` 是公开路由，删除或改名不保留兼容入口。

## Front Matter 契约

```yaml
layout: manual
title: 页面标题
page_role: docs-topic
footer_text: 页脚文字
permalink: /tools/example/docs/topic.html
manual_id: example
manual_group: start
manual_order: 1
nav_title: 导航短标题
hero_title: 页面主标题
hero_description: 一句话摘要
summary: 目录卡片摘要
badges: [Documentation]
```

手册首页增加 `manual_is_index: true`；需要作为术语索引入口的页面增加 `manual_index_entry: true`。

## 动态生成规则

- Jekyll 按 `manual_id` 收集页面，按 `manual_order` 生成上一页和下一页。
- 侧栏和移动目录按 `_data/manuals.yml` 中的分组顺序、页面 `manual_group` 与 `manual_order` 生成。
- 手册首页自动生成分组目录卡片，新页面无需修改 HTML 或 JavaScript。
- 参考索引链接自动指向同一手册中标记 `manual_index_entry` 的页面；未设置时使用当前手册配置的首页名称并回到手册首页，不能把首页误标为“索引”。

## 正文样式

- 字号、行高、正文最大宽度和长内容节奏同时遵守 [`readability.md`](readability.md)。
- 使用 `##` 作为手册章节标题，`###` 作为章节内小标题。
- 普通表格使用 Markdown 表格；代码使用围栏代码块；列表使用标准 Markdown。
- 重要判断使用标准 Markdown 引用块；警告语义直接在引用文字中明确写出。
- 正文不得使用原始 HTML、Kramdown 专有属性或页面级 include。网格、流程和入口列表必须先用标准列表、表格或普通链接表达，再由共享 CSS 对生成元素进行统一增强。

## 布局

- 桌面侧栏 320px、阅读区 880px；侧栏显示手册名称、分组、数量和当前页。阅读区内普通正文限制在约 720–760px，表格和代码可以使用阅读区完整宽度。
- 桌面侧栏中的全部分组首次加载时默认展开，保证完整目录和当前页面始终可见；分组标题仍允许用户手动收起，目录内容超过视口时只滚动侧栏本身。
- 阅读区使用紧凑 Hero、30px 左右章节标题和顶部/底部分页。
- 1000px 以下隐藏固定侧栏，由移动目录接管；正文、表格和代码块不得造成页面级横向滚动。
