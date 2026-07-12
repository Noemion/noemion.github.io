---
layout: manual
title: "参考索引 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/reference.html"
manual_id: "endem"
manual_group: "reference"
manual_order: 5
manual_index_entry: true
nav_title: "参考索引"
page_heading: "参考索引"
page_lead: "集中查找 endem 子命令、制品、状态、组件和稳定失败类别。"
summary: "八个入口、Endem/Synem/Dromen/Tekmor、状态、失败和权威参考。"
badges: ["Reference", "Unfrozen CLI"]
---

## 子命令索引

| 子命令 | 主要输入 | 主要输出 | 权限边界 |
| --- | --- | --- | --- |
| `poie` | 受控来源、投影候选与具名决定 | nascent Endem、Poie Tekmor | 唯一规范写入入口 |
| `elenk` | 原始制品、层、限制和信任材料 | 分层结论、Elenk Tekmor | 生产验证路径 |
| `pleko` | Endem、组合策略和依赖锁 | coherent Endem/Synem、Pleko Tekmor | 不读取环境隐式依赖 |
| `tasse` | coherent 制品和发布配置 | 候选、清单和签名请求 | 不持有私钥 |
| `sphra` | 原候选、请求和外部签名响应 | attested 制品、Sphra Tekmor | 不修改被签载荷 |
| `theor` | 任意原始制品、视图和预算 | 只读视图、差分、诊断 | 独立 Theor，不生成生产验证句柄 |
| `praxe` | attested 制品、执行策略、后端与能力 | Dromen、运行记录、Tekmor 和决定 | 隔离 Praxor，不拥有写入器 |
| `peira` | 规范向量、实现和复现配置 | 一致性、差分、模糊与复现报告 | 不替代第三方认证或发布授权 |

`.endem` 扩展名已经采用；参数、选项、退出码、Synem/Tekmor 扩展名和尚未发布的安装接口仍未冻结。本表只冻结职责，不应据此编写依赖具体参数的脚本。

## 制品与视图

| 名称 | 定义 |
| --- | --- |
| Endem | 具有一个根 `skena` 和六个语义面的最小目标制品 |
| Synem | 两个或更多 Endem 的已解析组合闭包 |
| Dromen | Praxor 为一次会话建立的实现态，不是文件 |
| Tekmor | 封装 phain、来源、范围、方法、限制或决定依据的证据记录 |

## 状态索引

| 对象 | 状态 | 含义 |
| --- | --- | --- |
| Endem | `nascent` | 结构合法，但仍可能有 apor、引用或确认事项 |
| Endem | `coherent` | 必需引用、冲突、能力和验收关系已解析 |
| Endem | `attested` | 发布载荷冻结并绑定外部签名响应 |
| 满足判断 | `met / unmet / agno / fault` | skena 相对 phain 和 krin 的满足判断 |
| Praxe | `accepted` | krin 条件为 met、必需 Tekmor 齐全且决定权威匹配 |
| Praxe | `unsatisfied` | 可判定条件没有满足 |
| Praxe | `pending-review` | 需要指定外部权威判断 |
| Praxe | `failed` | 系统、策略、对象或后端失败 |
| Praxe | `interrupted` | 取消、预算、环境或外部停止导致未完成 |

## 稳定失败类别

END-ERRCAT 0.1 已登记结构与 END-P0 的实验错误码；完整 CLI 诊断 ABI 尚未冻结。实现还必须稳定区分以下更高层失败：

- source invalid；
- contract incomplete；
- malformed object；
- unsupported required feature；
- resource limit exceeded；
- pleko unresolved；
- pleko conflict；
- permission widening；
- tasse changes semantics；
- signature mismatch；
- load rejected；
- capability denied；
- backend failed；
- state drift；
- Tekmor insufficient；
- implementation disagreement；
- reproducibility failed。

## 权威页面

- [Endem 规范](../../specifications/endem.html)
- [Synem 规范](../../specifications/synem.html)
- [Tekmor 规范](../../specifications/tekmor.html)
- [Endem 生命周期](../../architecture/endem-lifecycle.html)
- [ADR-0010](../../architecture/adr-0010-native-lexicon.html)
- [Poiet、Theor 与 Praxor](../../components/index.html)

## 外部工程资料

这些资料只提供机制先例，不定义 Endem ABI：

- GNU `readelf`：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- GNU BFD：https://sourceware.org/binutils/docs/bfd.html
- MCP 2025-11-25：https://modelcontextprotocol.io/specification/2025-11-25
- A2A 1.0，文档快照 v1.0.1：https://a2a-protocol.org/v1.0.1/specification/
- OpenTelemetry 生成式 AI 语义约定迁移说明：https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- OpenAI 关于智能体控制平面工程的实践文章：https://openai.com/index/harness-engineering/
