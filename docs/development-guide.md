---
layout: "manual"
title: "开发指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 开发指南"
permalink: "/docs/development-guide.html"
manual_id: "docs"
manual_group: "guides"
manual_order: 4
nav_title: "开发指南"
page_heading: "Noemion 开发指南"
page_lead: "面向 Endem 规范、安全核心、独立 Theor 与隔离 Drasor 的开发纪律。"
summary: "面向 Endem 规范、安全核心、独立 Theor 与隔离 Drasor 的开发纪律。"
badges: ["Spec First", "Checked Arithmetic", "Fuzz Early"]
---

## 第一阶段范围

第一阶段只做规范和最小安全核心，不引入模型、LLVM、MLIR、多格式抽象或大型框架。

ADR-0012 已把 Rust 1.97.0 选为未来 Poiet 与生产读取核心的候选语言。项目尚未进入代码开发阶段；禁止 `unsafe`、第三方 crate、工具链锁、`Cargo.lock` 与 release 溢出检查都只是未来实现门禁。C/Rust 语言材料只作历史研究依据，不进入生产代码。

当前没有 Poiet、Theor、CLI 工作区或实现级 fuzz。十四个 END-P1 字节向量用于检查规范资料，不能证明解析器、写入器或独立读取路径存在。只有用户明确开启代码阶段后，以下开发纪律才进入实施：

- 冻结 `rhem/semion/skena/telis/krin/apor` 的最小语义、不变量、错误和资源限制。
- 保持规范写入器、生产侧结构检查与 `endem poie/elenk` 的确定性边界。
- 继续让 `endem theor` 独立实现读取、字段与引用验证，禁止共享生产解析代码。
- 规划合法、边界、畸形和对抗语料，以及未来长时公开 CI、故障注入和跨平台复现。

## 规范与 ADR 先行

- 格式、语义、执行、信任边界或应用职责变化必须先更新规范或记录 ADR。
- 开放问题不能因为实现方便而静默变成默认行为。
- 一个新制品或子命令必须说明不可替代价值、上游、下游、失败责任和停止条件。
- 正式接口只描述真实存在且通过验证条件的行为；示例不自动成为 ABI。

## 实现工作流

1. 确认消费者、输入、输出、权限与失败责任。
2. 引用唯一规范条款或先补 ADR。
3. 先加入失败向量，固定缺失行为与诊断。
4. 实现最小确定性变化；解析计算全部使用 checked arithmetic。
5. 运行合法/畸形语料、属性/模糊测试、Poiet/Theor 差分、往返与复现检查。
6. 更新规范、ADR、路线、手册和公开成熟度；删除被替代入口，不保留兼容垫片。

## 建议仓库边界

```text
spec/       权威条款、registry 与错误码
vectors/    规范字节、注释、合法与畸形向量
poiet/      Rust 写入器、生产解析器、poie/elenk/pleko
theor/      独立只读 Theor，不依赖生产解析器
cli/        endem 调度与独立进程边界
```

没有独立版本、权限、保密或真实消费者时不拆仓库。`theor` 只能共享公开规范与向量，不能共享生成常量、生产解析状态机或错误分类实现；`drase` 建立后必须是不同进程并使用最小权限。

## 审查清单

| 层 | 必查项 |
| --- | --- |
| 结构 | magic、版本、偏移、长度、计数、索引、对齐、重叠、环、上限 |
| 语义 | 一个根 skena、rhem/semion 投影、关系角色、kine/mene、krin、apor/agno/aseme 与权威 |
| 组合 | 引用身份、版本、依赖闭包、冲突矩阵、权限交集、顺序无关 |
| 发布 | 裁剪等价、调试伴随记录、主体摘要、外部签名、软件物料清单和复现结果 |
| 运行 | 实际字节重验、能力最小化、真实观察、事件完整、验收分层 |

## 模型与协议

模型加入前必须先建立无模型基线。模型输出只作为不可信候选进入系统；MCP 和 A2A 只通过 Drasor 外缘的协议适配器接入。外部参数结构合法不等于语义正确或权限允许。若模型无法在错误确定率、上下文成本或任务成功率上证明净增益，项目就停止自研模型平台投入。

完整完成标准见[开发路线图](../development/implementation-roadmap.html)，测试矩阵见[测试与验证](../development/testing.html)。
