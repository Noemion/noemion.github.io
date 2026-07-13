---
layout: manual
title: "发布与运行 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/running.html"
manual_id: "endem"
manual_group: "running"
manual_order: 4
nav_title: "发布与运行"
page_heading: "发布与运行"
page_lead: "冻结发布载荷、核对外部签名，并在隔离 Praxor 中建立 Dromen 与 Tekmor。"
summary: "tasse、sphra、外部签名、Praxor、Dromen、能力循环与最终决定。"
badges: ["tasse", "sphra", "praxe"]
---

## tasse 冻结什么

`endem tasse` 读取 coherent Endem 或 Synem，以及发布配置、覆盖要求和调试策略。它产生不可变候选载荷、清单、签名请求和 Tasse Tekmor。

它可以外置不影响运行的调试和详细来源内容，但必须证明以下属性未改变：

- 每个根 `skena` 的关系、组合与极性；
- `telis` 的 kine/mene 与时间边界；
- `semion` 中所有符号、关系位置和作用域；
- `krin` 的满足条件、观察、证据和权威；
- 仍需运行处理的 `apor`；
- 绑定结果、能力上限和披露边界。

没有冻结的属性级等价规则时，`tasse` 应保守保留内容或失败。

## 外部签名与 sphra

私钥始终留在外部签名系统。流程为：

1. `tasse` 冻结候选并产生签名请求；
2. 外部系统验证授权并返回签名响应；
3. `sphra` 同时读取原候选、原请求和响应；
4. 验证载荷、算法、签名者和策略版本；
5. 在被签载荷之外附加签名包络，形成 attested Endem/Synem。

任何被签载荷变化都要求重新 tasse 和重新签名。签名有效只证明指定身份对指定字节作出签名，不证明语义正确或当前环境授权。

## praxe 的隔离域

`endem praxe` 是用户入口，实际工作由不拥有 Poiet 写入器的隔离 Praxor 完成。Praxor 先重新验证实际 attested 字节，再读取运行策略、后端绑定和能力目录。

> 预先生成的 Elenk Tekmor 不能替代对实际运行输入的重新检查。

## Dromen

Praxor 为一次会话建立 Dromen。Dromen 只披露当前任务所需的 Endem/Synem 语义和能力参数结构；它不是文件，不进入发布包，也不包含凭据、token、文件描述符、网络连接或其他实时句柄。

对象、策略、环境或能力身份变化时，旧 Dromen 立即失效。会话结束后 Dromen 销毁。

## 能力与反馈循环

1. 后端读取 Dromen 并返回候选或类型化能力请求。
2. Praxor 检查参数、权限、预算、副作用、幂等和当前状态。
3. Praxor 执行或拒绝请求，把真实结果规范化为 phain，再写入能力观察和 Praxe Tekmor。
4. 后端可以根据观察继续求解，但不能直接持有句柄或修改 attested 制品。
5. 重复失败、预算耗尽、状态漂移或需要价值判断时，Praxor 按预注册策略停止或请求外部权威。

MCP 和 A2A 只适合作为 Praxor 外缘的协议适配器：

- [MCP 2025-11-25 稳定规范](https://modelcontextprotocol.io/specification/2025-11-25)；后续正式版本只有完成兼容、安全、错误来源、降级和权限复核后才进入新适配基线
- [A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)

远端工具说明、Agent Card、任务状态、参数结构和返回内容均是不可信声明，不能直接成为能力授权、Endem 状态或最终决定。A2A 的补丁号只固定查阅的文档快照，不进入协议协商。

运行观测以后可以通过带版本的 [OpenTelemetry GenAI 语义约定](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)导出。该约定当前处于 Development；输入、输出和工具数据可能含有敏感信息，因此默认不导出正文，外部字段也不构成 Tekmor 身份。

## Tekmor 与最终决定

Tekmor 记录有限的来源、检查、绑定、签名、运行或决定依据。它不等于数学证明，也不自动证明 claim 为真。

满足判断先区分 `met`、`unmet`、`agno` 和 `fault`。具名权威随后形成 `accepted`、`rejected` 或 `deferred`；Praxe 会话另行记录 `completed`、`failed` 或 `interrupted`。只有 `krin` 对适用 phain 的全部必需条件为 `met`、必需 Tekmor 有效且覆盖充分、没有阻断性 `apor` 且决定权威匹配时，才能形成 `accepted`。

这三个结果域不能互相替代。会话 `completed` 只说明运行按终止规则结束；它可以对应 `unmet` 和 `rejected`。验证器或后端故障产生 `fault` 或会话 `failed`，不能冒充目标本身 `unmet`。完整禁止推导见 [ADR-0015](../../architecture/adr-0015-result-domains.html)。
