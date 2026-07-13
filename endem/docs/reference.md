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
| 权威决定 | `accepted` | krin 结果为 met、必需 Tekmor 有效且覆盖充分，并且决定权威匹配 |
| 权威决定 | `rejected` | 具名权威依据 unmet 或预先登记政策作出否定决定 |
| 权威决定 | `deferred` | 尚无获授权的最终决定，或 agno、fault 与授权缺口仍未解决 |
| Praxe 会话 | `completed` | 按声明终止规则结束；不说明目标是否满足 |
| Praxe 会话 | `failed` | 系统、策略、对象、求值器或后端使会话无法继续 |
| Praxe 会话 | `interrupted` | 取消、预算、环境、输入或授权条件使会话中断 |
| Tekmor 有效性 | `valid / invalid / revoked` | 记录身份、完整性和适用性 |
| 证据覆盖度 | `sufficient / insufficient` | 一组有效 Tekmor 是否覆盖指定 krin |

## mene 时间索引

| 类别 | 值 | 含义 |
| --- | --- | --- |
| 时间范围 | `fixed` | 具名权威解析的 UTC 半开区间 `[start,end)` |
| 时间范围 | `elapsed` | 从具名事件开始、由单调时钟测量的固定经过时长 |
| 连续性 | `strict` | skena 在整个目标区间都必须成立 |
| 连续性 | `budgeted` | 只允许在累计、单次和次数预算内违约 |
| 覆盖缺口 | `agno` | 判据明确，但观测区间不完整或时间不确定度过大 |
| 时钟故障 | `fault` | 时钟、同步、适配器或求值器没有按契约完成 |

这些值由 ADR-0016 冻结为抽象语义，不是 END-P1 字段、CLI 参数或稳定 ABI。

## 否定与缺席索引

| 证据情况 | 结果 | 含义 |
| --- | --- | --- |
| 显式负观察 | 可支持 `met` | 保留目标的关系、角色和顺序，只改变极性 |
| 同构正反例 | `unmet` | 目标要求关系不成立，但观察表明关系成立 |
| 查询未命中 | 默认 `agno` | 只说明给定输入和查询中没有匹配 |
| 封闭范围内完整缺席 | 可支持 `met` | 权威、全集、路径、时间、枚举与损失边界全部有效 |
| 观察契约故障 | `fault` | 观察器、适配器或日志链没有按契约完成 |

这些分类由 ADR-0017 冻结为抽象语义。END-P1 只有原子负极性规范字节，没有封闭声明字段、CLI 参数或运行实现。

## 稳定失败类别

END-ERRCAT 0.1 已登记 END-P0 结构错误和首组 END-P1 语义错误；完整 CLI 诊断 ABI 尚未冻结。实现还必须稳定区分以下更高层失败：

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
- [ADR-0015 判断与运行结果分层](../../architecture/adr-0015-result-domains.html)
- [ADR-0016 mene 时间与连续性模型](../../architecture/adr-0016-mene-time-model.html)
- [ADR-0017 否定事态与缺席证据](../../architecture/adr-0017-negation-and-absence.html)
- [Poiet、Theor 与 Praxor](../../components/index.html)

## 外部工程资料

这些资料只提供机制先例，不定义 Endem ABI：

- [GNU `readelf` 手册](https://www.sourceware.org/binutils/docs/binutils/readelf.html)
- [GNU BFD 手册](https://sourceware.org/binutils/docs/bfd.html)
- [MCP 2025-11-25 稳定规范](https://modelcontextprotocol.io/specification/2025-11-25)
- [A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)
- [OpenTelemetry GenAI 语义约定（Development）](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)
- [智能体控制平面工程实践](https://openai.com/index/harness-engineering/)
