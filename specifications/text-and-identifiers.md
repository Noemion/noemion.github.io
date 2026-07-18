---
layout: content
title: 文本与标识符边界规范
page_role: content
footer_text: Noemion · Text and Identifier Boundaries
permalink: "/specifications/text-and-identifiers.html"
summary: 说明自然语言和机器标识符进入制品、界面与模型时怎样解码、比较、定位和显示，避免人机输入不一致。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 规范参考指南
  url: index.html
page_heading: 文本与标识符边界
page_lead: 规定自然语言和机器标识符从来源文件进入制品、界面与模型时，怎样解码、比较、定位和显示，并让人类复核内容与机器实际输入能够逐项核对。
badges:
- TEXT-IDENTIFIER-CORE 0.1.0-draft
- 当前策略
- Unicode Profile 待定
- 尚无文本处理组件
previous_url: identity.html
previous_label: 精确内容身份与签名
next_url: "../architecture/adr-0028-text-and-identifier-boundaries.html"
next_label: ADR-0028
---

## 先看一段文本怎样进入发布

假设一份实验性来源清单包含服务说明、关系 ID 和供模型复核的自然语言。开发者不能把原文件字节、解码后的内容、安全显示视图和模型实际取得的码点统称为“同一段文本”。

1. 原始来源字节
2. 严格 UTF-8 解码
3. 提交后的来源表达
4. 结构标识符与范围
5. 安全显示视图
6. 模型实际输入

| 处理位置 | 开发者要固定什么 | 失败时怎样处理 |
| --- | --- | --- |
| 读取来源 | 原始字节身份、字符编码和解码 Profile | 无效 UTF-8 在形成对象前原子失败，不以替换字符或本地编码猜测继续解析 |
| 写入 `source_expression.content` | 转义和换行规则应用后的来源表达，以及发生过的变换 | 不能把提交后的文本称为原始来源文件的逐字节副本 |
| 比较关系 ID 与登记词 | 现行 ASCII Profile、原始字节和区分大小写的比较 | 搜索命中、locale、NFKC 或同形骨架不能选择安全对象 |
| 显示正文与范围 | 精确文本主体、Unicode 标量范围，以及转义、截断、方向和不可见字符清单 | 屏幕列、字素、UTF-16 单元或短显示不能冒充规范范围和安全引用 |
| 提交模型或检索器 | 实际输入身份、全部预处理、模型与 tokenizer 身份，以及人类复核视图 | 显示与实际输入不同必须明示；模型输出仍是不可信候选 |

每个字符串还要先声明自己的文本槽：`source-content` 保存来源表达，`structural-identifier` 承担机器引用，`registered-token` 只接受登记值，`descriptive-text` 供人阅读，`display-message` 只负责呈现。复制字符串不会把一种职责带到另一种槽。

**当前策略：**来源内容允许 Unicode 但不静默规范化，结构标识符继续使用封闭 ASCII Profile；显示、搜索、同形提示和模型相似度不得替代精确机器内容、授权意义或最终决定。

## 文本与标识符必须怎样处理

按十二项责任检查每个文本槽；同一字符串进入不同槽时，必须重新核对用途和信任边界。

| 规则 | 开发者应做什么 | 必须拒绝什么 |
| --- | --- | --- |
| `TEXT-SLT-001` | 声明槽类别、允许字符、比较、变换、长度单位、显示和失败责任 | 来源正文、本地化消息和机器标识符混用 |
| `TEXT-ENC-001` | 先按 RFC 3629 严格解码 UTF-8，再进行字段解析或其他变换 | 过长编码、代理项、非法标量和平台编码猜测 |
| `TEXT-SRC-001` | 分开来源字节、解码文本、变换结果和信息损失 | 变换后沿用输入身份，或把解码内容称为原文件副本 |
| `TEXT-IDN-001` | 结构标识符使用各自登记的封闭 ASCII 语法 | Unicode 同形、默认 locale、宽度映射和静默大小写折叠 |
| `TEXT-NRM-001` | 规范化绑定文本槽、Unicode 版本、具体形式和身份影响 | 盲目应用 NFC 或 NFKC、覆盖原文，或据此宣称语义相同 |
| `TEXT-CMP-001` | 明确按字节、标量、具名规范化结果、排序域还是风险骨架比较 | 搜索、排序、同形提示或模型相似度替代精确相等 |
| `TEXT-RNG-001` | 范围绑定精确主体、表示版本、半开区间和 Unicode 标量单位 | 混用字节、UTF-16、字素、屏幕列和模型 token |
| `TEXT-BID-001` | 以逻辑顺序保存和定位；显示按绑定版本的 UAX #9 隔离方向 | 视觉顺序参与身份，或安全视图隐藏方向控制 |
| `TEXT-HID-001` | 列出不可见字符、变体选择符、混合脚本和同形风险 | 静默删除、自动合并身份，或仅凭警告判定恶意 |
| `TEXT-MET-001` | 分别验证语言、媒体、方向和 locale 声明 | 自报语言触发未登记变换，或取得语义权威 |
| `TEXT-AIM-001` | 绑定模型实际输入、预处理、风险清单、模型、tokenizer 和复核视图 | 审核者看清洗文本，模型却取得另一组码点 |
| `TEXT-OUT-001` | 显示、复制与导出披露转义、截断、脱敏和方向处理 | 短显示、日志摘要或经过清洗的文本充当安全引用 |

> **权威边界：**[TEXT-IDENTIFIER-CORE 条款源](https://noemion.github.io/spec/text-identifier-core.html)定义规范义务。这份说明帮助开发者选择检查顺序，不建立第二套条款。

## 遇到更强问题时再查对应资料

| 开发问题 | 继续核对 | 当前停止条件 |
| --- | --- | --- |
| 需要证明原文件没有改变 | 精确内容身份、原始字节身份、解码 Profile 和完整变换链 | `source_expression.content` 只保存提交后的来源表达，不能反推原文件字节 |
| 需要 Unicode 结构标识符 | [UAX #31](https://www.unicode.org/reports/tr31/)、[UTS #39](https://www.unicode.org/reports/tr39/)和独立内容 Profile | 真实生产者、消费者、迁移规则和正反向量出现前继续使用 ASCII |
| 需要规范化、搜索或语言排序 | [UAX #15](https://www.unicode.org/reports/tr15/)与 [RFC 8264](https://www.rfc-editor.org/rfc/rfc8264.html)，并为具体用途定义版本化比较 Profile | 规范化、搜索命中和排序结果都不能替代内容身份或语义等价 |
| 需要双向编辑或同形风险处置 | [UAX #9](https://www.unicode.org/reports/tr9/)、UTS #39、威胁模型与实际字体和界面测试 | 风险提示不能自动改写来源、合并对象或判定恶意 |
| 需要构造模型或检索上下文 | [模型上下文组装研究](https://noemion.github.io/spec/model-context-assembly-proposal.html)，同时核对授权、预算、外部适配和诊断责任 | 当前没有模型输入网关；模型输出不能写入规范字节或扩大权限 |
| 需要把文本用于确认或授权 | AUT-CORE 的安全显示视图、精确机器请求、决定主体和适用范围 | TEXT-IDENTIFIER 只证明显示怎样对应机器内容，不证明观看者有决定权 |
| 需要判断名称怎样公开使用 | [ADR-0037](../architecture/adr-0037-terminology-simplification.html)区分普通职责词、机器文档 ID 与两个自造名称 | 字符合法不能证明职责准确；普通词也不能替自造名称提供完整读音证据 |

## 规范来源与当前上限

截至 2026 年 7 月 16 日，[Unicode 17.0](https://www.unicode.org/versions/Unicode17.0.0/)仍是当前版本，UTS #39 的安全数据与它同步更新。UAX #31 要求实现说明采用的标识符要求或 Profile；UTS #39 也说明同形程度会随字体、书写系统和使用者变化，因此风险骨架不能成为精确身份。

[RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html)提供 UTF-8 的合法编码边界；[GNU libunistring](https://www.gnu.org/software/libunistring/manual/libunistring.html)把编码表示、规范化、大小写、字素、词和行处理分成不同接口。Noemion 借鉴这种职责分离，不据此选择实现库或建立组件。

- [文本与标识符威胁模型](https://noemion.github.io/spec/text-identifier-threat-model.html) — 覆盖编码、规范化、范围、双向显示、隐藏字符和模型视图威胁。
- [设计场景](https://noemion.github.io/spec/text-identifier-scenarios.html) — 用支持案例、反例与待确认场景检查责任边界；场景不是实现证据。
- [文本与标识符提案向量](https://github.com/Noemion/noemion.github.io/tree/main/vectors/text-identifier) — 检查允许包络与确定拒绝；向量不证明 Unicode 库、界面或模型网关已经实现。
- [ADR-0028 · 显示相同，不等于输入相同](../architecture/adr-0028-text-and-identifier-boundaries.html) — 说明 ASCII 标识符、不统一规范化和模型输入绑定的权衡与采用限制。

**待定内容：**Unicode 国际化结构标识符、来源文本重写、语言检测、分词、字素级编辑、搜索排序、字体信任、tokenizer 协议、同形自动处置、双向编辑器和原始来源字节字段都保持开放。当前没有 Unicode 处理器、规范化器、同形检测器、模型输入网关或新的文本格式。
