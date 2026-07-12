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
hero_title: "发布与运行"
hero_description: "冻结发布载荷、核对外部签名，并在隔离 Runner 中建立 Frame 与 Witness。"
summary: "pack、seal、外部签名、Runner、Frame、能力循环与最终决定。"
badges: ["pack", "seal", "run"]
---

## pack 冻结什么

`endem pack` 读取 bound Endem 或 Weave、发布 Profile、覆盖要求和调试策略，产生不可变候选载荷、manifest、Signing Request 和 Pack Witness。

它可以外置不影响运行的调试和详细来源内容，但必须证明以下属性未改变：

- 每个根 `aim`；
- 所有 `must` 的强度与作用域；
- `done` 的条件、证据和权威；
- 仍需运行处理的 `open`；
- 绑定结果、能力上限和披露边界。

没有冻结的属性级等价规则时，`pack` 应保守保留内容或失败。

## 外部签名与 seal

私钥始终留在外部签名系统。流程为：

1. `pack` 冻结候选并产生 Signing Request；
2. 外部系统验证授权并返回 Signature Response；
3. `seal` 同时读取原候选、原请求和响应；
4. 验证载荷、算法、签名者和策略版本；
5. 在被签载荷之外附加 Signature Envelope，形成 sealed Endem/Weave。

任何被签载荷变化都要求重新 pack 和重新签名。签名有效只证明指定身份对指定字节作出签名，不证明语义正确或当前环境授权。

## run 的隔离域

`endem run` 是用户入口，实际工作由不拥有 Core Writer 的隔离 Runner 完成。Runner 先重新验证实际 sealed 字节，再读取 Execution Policy、后端绑定和 Capability Catalog。

> 预先生成的 Check Witness 不能替代对实际运行输入的重新检查。

## Frame

Runner 为一次会话建立 Frame。Frame 只披露当前任务所需的 Endem/Weave 语义和能力参数结构；它不是文件，不进入发布包，也不包含凭据、token、文件描述符、网络连接或其他实时句柄。

对象、策略、环境或能力身份变化时，旧 Frame 立即失效。会话结束后 Frame 销毁。

## 能力与反馈循环

1. 后端读取 Frame 并返回候选或类型化 Capability Request。
2. Runner 检查参数、权限、预算、副作用、幂等和当前状态。
3. Runner 执行或拒绝请求，把真实结果写为 Capability Observation 和 Run Witness。
4. 后端可以根据观察继续求解，但不能直接持有句柄或修改 sealed 制品。
5. 重复失败、预算耗尽、状态漂移或需要价值判断时，Runner 按预注册策略停止或请求外部权威。

MCP 和 A2A 只适合作为 Runner 外缘协议适配器：

- https://modelcontextprotocol.io/specification/2025-11-25
- https://a2a-protocol.org/v1.0.1/specification/

远端工具说明、Agent Card、Task 状态、schema 和返回内容均是不可信声明，不能直接成为能力授权、Endem 状态或最终决定。

## Witness 与最终决定

Witness 记录有限的来源、检查、绑定、签名、运行或决定依据。它不等于数学证明，也不自动证明 claim 为真。

最终状态至少区分 `accepted`、`unsatisfied`、`pending-review`、`failed` 和 `interrupted`。只有 `done` 的全部必需条件可判定、Witness 足够且决定权威匹配时，才能形成 `accepted`；否则必须保留失败或待复核状态。
