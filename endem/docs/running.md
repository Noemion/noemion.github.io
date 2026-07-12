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

`endem tasse` 读取 coherent Endem 或 Synem、发布 Profile、覆盖要求和调试策略，产生不可变候选载荷、manifest、Signing Request 和 Tasse Tekmor。

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

1. `tasse` 冻结候选并产生 Signing Request；
2. 外部系统验证授权并返回 Signature Response；
3. `sphra` 同时读取原候选、原请求和响应；
4. 验证载荷、算法、签名者和策略版本；
5. 在被签载荷之外附加 Signature Envelope，形成 attested Endem/Synem。

任何被签载荷变化都要求重新 tasse 和重新签名。签名有效只证明指定身份对指定字节作出签名，不证明语义正确或当前环境授权。

## praxe 的隔离域

`endem praxe` 是用户入口，实际工作由不拥有 Poiet Writer 的隔离 Praxor 完成。Praxor 先重新验证实际 attested 字节，再读取 Praxe Policy、后端绑定和 Capability Catalog。

> 预先生成的 Elenk Tekmor 不能替代对实际运行输入的重新检查。

## Dromen

Praxor 为一次会话建立 Dromen。Dromen 只披露当前任务所需的 Endem/Synem 语义和能力参数结构；它不是文件，不进入发布包，也不包含凭据、token、文件描述符、网络连接或其他实时句柄。

对象、策略、环境或能力身份变化时，旧 Dromen 立即失效。会话结束后 Dromen 销毁。

## 能力与反馈循环

1. 后端读取 Dromen 并返回候选或类型化 Capability Request。
2. Praxor 检查参数、权限、预算、副作用、幂等和当前状态。
3. Praxor 执行或拒绝请求，把真实结果规范化为 phain，再写入 Capability Observation 和 Praxe Tekmor。
4. 后端可以根据观察继续求解，但不能直接持有句柄或修改 attested 制品。
5. 重复失败、预算耗尽、状态漂移或需要价值判断时，Praxor 按预注册策略停止或请求外部权威。

MCP 和 A2A 只适合作为 Praxor 外缘协议适配器：

- https://modelcontextprotocol.io/specification/2025-11-25
- https://a2a-protocol.org/v1.0.1/specification/

远端工具说明、Agent Card、Task 状态、schema 和返回内容均是不可信声明，不能直接成为能力授权、Endem 状态或最终决定。

## Tekmor 与最终决定

Tekmor 记录有限的来源、检查、绑定、签名、运行或决定依据。它不等于数学证明，也不自动证明 claim 为真。

满足判断先区分 `met`、`unmet`、`agno` 和 `fault`。最终运行状态再区分 `accepted`、`unsatisfied`、`pending-review`、`failed` 和 `interrupted`。只有 `krin` 对适用 phain 的全部必需条件为 `met`、Tekmor 足够、没有阻断性 `apor` 且决定权威匹配时，才能形成 `accepted`。
