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
hero_title: "参考索引"
hero_description: "集中查找 endem 子命令、制品、状态、组件和稳定失败类别。"
summary: "八个入口、Endem/Weave/Frame/Witness、状态、失败和权威参考。"
badges: ["Reference", "Unfrozen CLI"]
---

## 子命令索引

| 子命令 | 主要输入 | 主要输出 | 权限边界 |
| --- | --- | --- | --- |
| `form` | Goal Card、候选与绑定决定 | open Endem、Form Witness | 唯一规范写入入口 |
| `check` | 原始制品、层、限制和信任材料 | 分层结论、Check Witness | 生产验证路径 |
| `bind` | Endem、Binding Policy、Dependency Lock | bound Endem/Weave、Binding Witness | 不读取环境隐式依赖 |
| `pack` | bound 制品、发布 Profile | 候选、manifest、Signing Request | 不持有私钥 |
| `seal` | 原候选、请求、Signature Response | sealed 制品、Seal Witness | 不修改被签载荷 |
| `see` | 任意原始制品、视图、预算 | 只读视图、差分、诊断 | 独立 Reader，不生成 Verified Handle |
| `run` | sealed 制品、执行策略、后端与能力 | Frame、Run Record、Witness、决定 | 隔离 Runner，不拥有 Writer |
| `test` | 规范向量、实现和复现配置 | 一致性、差分、模糊与复现报告 | 不替代第三方认证或发布授权 |

`.endem` 扩展名已经采用；参数、选项、退出码、Weave/Witness 扩展名和尚未发布的安装接口仍未冻结。本表只冻结职责，不应据此编写依赖具体参数的脚本。

## 制品与视图

| 名称 | 定义 |
| --- | --- |
| Endem | 具有一个根 `aim` 和五组语义的最小目标制品 |
| Weave | 两个或更多 Endem 的已解析组合闭包 |
| Frame | Runner 为一次会话建立的只读视图，不是文件 |
| Witness | 对来源、检查、绑定、签名、运行或决定作出有限主张的证据记录 |

## 状态索引

| 对象 | 状态 | 含义 |
| --- | --- | --- |
| Endem | `open` | 结构合法，但仍有未决语义或引用 |
| Endem | `bound` | 必需引用、冲突、能力和验收关系已解析 |
| Endem | `sealed` | 发布载荷冻结并绑定外部签名响应 |
| Run | `accepted` | done 条件、必需 Witness 和决定权威均满足 |
| Run | `unsatisfied` | 可判定条件没有满足 |
| Run | `pending-review` | 需要指定外部权威判断 |
| Run | `failed` | 系统、策略、对象或后端失败 |
| Run | `interrupted` | 取消、预算、环境或外部停止导致未完成 |

## 稳定失败类别

具体错误码尚未冻结，但实现必须稳定区分：

- source invalid；
- contract incomplete；
- malformed object；
- unsupported required feature；
- resource limit exceeded；
- binding unresolved；
- binding conflict；
- permission widening；
- pack changes semantics；
- signature mismatch；
- load rejected；
- capability denied；
- backend failed；
- state drift；
- witness insufficient；
- implementation disagreement；
- reproducibility failed。

## 权威页面

- [Endem 规范](../../specifications/endem.html)
- [Weave 规范](../../specifications/weave.html)
- [Witness 规范](../../specifications/witness.html)
- [Endem 生命周期](../../architecture/endem-lifecycle.html)
- [ADR-0008](../../architecture/adr-0008-endem-system.html)
- [Core、Reader 与 Runner](../../components/index.html)

## 外部工程资料

这些资料只提供机制先例，不定义 Endem ABI：

- GNU `readelf`：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- GNU BFD：https://sourceware.org/binutils/docs/bfd.html
- MCP 2025-11-25：https://modelcontextprotocol.io/specification/2025-11-25
- A2A 1.0.1：https://a2a-protocol.org/v1.0.1/specification/
- OpenAI Harness Engineering：https://openai.com/index/harness-engineering/
