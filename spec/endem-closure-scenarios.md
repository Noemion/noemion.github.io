---
layout: spec
title: "closure Natural-Language Design Scenarios · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/endem-closure-scenarios.html"
summary: "用报告发布、服务部署和传递依赖案例，检查成员、完整集合、权限和运行期激活是否保持分开。"
document_status: "非规范设计场景"
---
# closure Natural-Language Design Scenarios

- 文档 ID：`CLOSURE-SCEN`
- 版本：`0.1.0-draft`
- 状态：非规范设计语料
- 边界：不是清单语法、解析器、runner、求值器或组件实现

### CLOSURE-SCN-001 — 两个独立目标形成闭包

报告发布与服务部署能独立版本化、接受和失败，因此分别形成 Endem。closure 显式连接二者，而不是把两个根塞进一个 Endem。

### CLOSURE-SCN-002 — 传递依赖不能遗漏

部署 Endem 必需引用配置 Endem，配置又必需引用策略 Endem。只列前两项不是完整闭包；三项与两条关系必须共同固定。

### CLOSURE-SCN-003 — 同名对象不能靠搜索顺序选择

两个仓库都提供名为 policy 的对象但摘要不同。名称和版本提示不能决定绑定；没有唯一允许内容身份时必须拒绝。

### CLOSURE-SCN-004 — 可选翻译包缺失

帮助文本翻译包可以缺失，因为缺失只改变展示语言，不改变 meaning_projection、situation、satisfaction_criteria、unresolved_meaning 或能力上限。若缺失会跳过验收项，它就是必需依赖。

### CLOSURE-SCN-005 — 必需依赖循环

部署要求审批，审批又要求部署已经完成。第一阶段没有固定点语义，必须拒绝循环，不能靠遍历顺序选择起点。

### CLOSURE-SCN-006 — 权限取交集

一个成员需要读取制品，另一个成员请求网络。请求不产生授权；组合策略未授予网络时，闭包不能因为成员需求获得网络句柄。

### CLOSURE-SCN-007 — 成员完成不等于闭包接受

报告会话 completed、报告目标 met，都不能使部署目标或整个 closure 自动 accepted。每个成员保留自己的判断与决定记录。

### CLOSURE-SCN-008 — 审批决定会话期激活

部署成员已在固定闭包中。审批 Endem 的具名 decision-result 为 accepted 且事件未撤销时，部署激活状态为 active；这仍不授予部署能力。

### CLOSURE-SCN-009 — 未激活不是未知满足

审批明确 rejected 时，部署为 inactive。本次没有部署满足结果；不能写成 met、unmet 或 undetermined。

### CLOSURE-SCN-010 — 激活依据缺失与检查失败不同

审批决定事件尚未产生时为 unresolved；事件存在但签名检查器违反契约时为 error。两者都不映射为满足结果域，也不允许模型猜测分支。
