---
layout: content
title: deterministic producer · 确定性制品核心
page_role: content
footer_text: Noemion · deterministic producer
permalink: "/components/producer.html"
summary: 介绍未来的确定性制品形成者怎样写入 Endem 或 Endem closure，并说明它不负责签名、授权、会话或证据。
breadcrumbs:
- label: 项目
  url: "../index.html"
- label: 系统组件
  url: index.html
page_heading: 确定性目标制品生产边界
page_lead: deterministic producer 未来只负责把已经确认的目标结构写成 Endem 或 Endem closure 规范字节，并检查生产路径；它不签名、不授权动作，也不生产会话与证据对象。
badges:
- 确定性生产
- 只生产 Endem / Endem closure
- 私钥与签名外置
- 尚未实现
previous_url: index.html
previous_label: 系统组件
next_url: inspector.html
next_label: independent inspector
---

## 为什么需要独立生产边界

同一句自然语言可能有多种解释。如果界面、模型和运行器都能各写一份“自己理解的目标”，开发者就无法确认两次处理使用的是不是同一件东西。deterministic producer 只接收已经确认的解释，按固定规范和 Profile 产生确定结果，并在输入、引用或格式不完整时停止。

这里的“已经确认”是指具有精确范围的语义授权：它只允许某项候选解释进入目标内容，不授予动作权限，也不允许 deterministic producer 自行调用工具。模型和外部 Agent 只能提出不可信候选；它们不能决定字段、顺序、字节布局、引用绑定或内容身份。

deterministic producer 可以是一组库，而不必成为独立服务。它的逻辑边界仍然只包含三个生产职责：`form` 形成 Endem，`lint` 检查生产侧实际字节，`compose` 在具备真实消费者和物理 Profile 后形成 Endem closure。independent inspector、bounded runner、外部签名系统和未来 evidence entry 生产者都不能取得这条写入路径。

> **名称状态：**deterministic producer 是由普通英语词组成的设计阶段职责名称，已经按逐词词首、职责和关键字语料接受。它不表示生产组件已经实现；首次说明时先写“确定性目标制品生产边界”，再用 deterministic producer 指向这里的定义。

## 用一次依赖更新理解 deterministic producer

以“更新服务依赖，并确认当前版本可以发布”为例：受控来源先给出服务、目标版本、允许变化、发布判据和待确认事项；模型可以提出包名或版本候选，但具名主体必须确认这些候选怎样进入六个语义面。deterministic producer 随后固定实际来源、意义决定、规范、Profile、配置和依赖，再形成来源保留的 END-P2。

1. 受控来源
2. 模型只提候选
3. 具名主体确认意义
4. form 形成 END-P2
5. lint 检查实际字节
6. inspect 独立读取
7. 多目标时再研究 compose
8. 发布 Profile 确定后再派生

若“发布判据”仍有两种解释，`form` 必须保留明确 `unresolved_meaning` 或拒绝形成，不能用默认提示、文本猜测或最后一个模型答案消除歧义。生产侧检查通过只说明对应检查层已经完成，不表示目标满足、动作获准或制品可以发布。

## 三个生产动作各自交付什么

| 动作 | 封闭输入 | 交付结果 | 必须停止的情况 |
| --- | --- | --- | --- |
| `form` | 受控来源、候选与具名意义决定、END-CORE、内容 Profile、END-FMT、配置和资源上限 | 当前只设计来源保留的 formed Endem；形成记录的 evidence entry 物理格式仍未定义 | 来源无效、意义未确认、根事态不唯一、`unresolved_meaning` 被静默删除、字段或引用不闭合 |
| `lint` | 实际制品字节、检查层、精确规范/Profile、检查配置和预算 | 结构、Profile、语义与策略层分别通过、失败或未执行；生产内部引用不跨入 independent inspector | 未知关键能力、受检算术失败、资源超限、主诊断不唯一或阻断失败留下部分可信结果 |
| `compose` | 至少两个精确 Endem、组合策略、完整依赖锁和权限上限 | 当前只能确定完整传递闭包；Endem closure 规范字节必须等待真实消费者与物理 Profile | 绑定不唯一、必需引用缺失、循环、冲突、环境搜索、权限扩大或成员结果被聚合洗白 |

相同封闭输入必须产生相同规范结果；在精确 END-FMT 与 Profile 内还必须逐字节相同。当前目录、区域设置、当前时间、哈希表遍历顺序、并发完成顺序、未记录默认值和模型随机性都不能成为隐式输入。偏移、长度、计数、索引、对齐和累计预算必须使用 `checked arithmetic`。

## 发布、签名和证据为什么不能混入

| 相邻关系 | 现行归属 | 与 deterministic producer 的边界 |
| --- | --- | --- |
| 来源裁剪的发布制品 | 发布 Profile 确定后，由 Endem 或 Endem closure 的对应生产者执行类型化派生 | END-P2 不能直接删除原文后继续使用；派生结果取得新身份，并重新闭合来源引用 |
| 待签陈述与签名包络 | 独立外部签名集成和密钥权限域 | 签名系统消费精确制品身份，但外部签名响应不是 deterministic producer 输入，私钥也不进入 deterministic producer |
| 形成、检查与复现记录 | 未来有范围的 evidence entry 生产者与独立验证流程 | deterministic producer 可以提供实际输入和已完成层次，但不能把内部检查引用冒充 evidence entry、签名或授权 |
| 会话、能力与最终决定 | bounded runner、session contract、能力域、满足判断和具名权威 | deterministic producer 不持有实时句柄，不运行目标，也不把形成或检查成功提升为 `met` 或 `accepted` |

[GNU `objcopy`](https://www.sourceware.org/binutils/docs/binutils/objcopy.html)把完整对象、裁剪对象和独立调试资料作为不同输出，并明确不当删除可能使输出不可用；[GNU GDB 的独立调试资料机制](https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html)再用显式关系重新定位伴随资料。Noemion 只采用“先形成、再按明确规则派生、最后建立关系”的生产纪律，不复制 ELF、DWARF、CRC、build ID 或节删除语义。

[SLSA 1.2 Provenance](https://slsa.dev/spec/v1.2/provenance)把制品的来源、时间和生产方式记录为可验证的外部信息。这个先例支持把生产记录与制品字节分开，但不定义 Endem、evidence entry、授权、签名 Profile 或目标满足。

## 当前可以实现到哪一层

**已有成果：**deterministic producer 的 Endem/Endem closure 生产边界、模型候选限制、确定性输入闭包、失败原子性、生产侧检查和independent inspector 分离已经进入现行规范与 ADR。

**待定内容：**当前没有 deterministic producer、END-P2 写入器或可执行组件。END-P2 只定义含原始自然语言的形成版；最终发布 Profile、Endem closure 物理格式、evidence entry 物理格式、发布派生规则和稳定诊断 ABI 均未定义。

**限制条件：**未来每个拒绝都必须遵守 [DIA-CORE](../specifications/diagnostics.html)，固定实际输入、规则版本、失败层次和唯一主诊断。现有规范与向量只能证明已登记关系一致，不能证明写入器安全、输出可复现或组件已经实现。
