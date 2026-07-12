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
page_lead: "面向 Endem 规范、安全核心、独立 Theor 与隔离 Praxor 的开发纪律。"
summary: "面向 Endem 规范、安全核心、独立 Theor 与隔离 Praxor 的开发纪律。"
badges: ["Spec First", "Checked Arithmetic", "Fuzz Early"]
---

## 第一阶段范围

第一阶段只做规范和最小安全核心，不引入模型、LLVM、MLIR、多格式抽象或大型框架。

- 冻结 `rhem/semion/skena/telis/krin/apor` 的最小语义、不变量、错误和资源限制。
- 实现规范写入器、生产解析器、确定性序列化和 `endem poie/elenk`。
- 用不共享解析代码的实现交付 `endem theor`。
- 建立合法、边界、畸形和对抗语料，以及往返、属性、模糊和双构建复现测试。

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
poiet/      写入器、生产解析器、poie/elenk/pleko
theor/      独立只读 Theor，不依赖生产解析器
cli/        endem 调度与独立进程边界
```

没有独立版本、权限、保密或真实消费者时不拆仓库。`theor` 可以共享规范常量生成物，但不能共享生产解析状态机；`praxe` 建立后必须是不同进程并使用最小权限。

## 审查清单

| 层 | 必查项 |
| --- | --- |
| 结构 | magic、版本、偏移、长度、计数、索引、对齐、重叠、环、上限 |
| 语义 | 一个根 skena、rhem/semion 投影、关系角色、kine/mene、krin、apor/agno/aseme 与权威 |
| 组合 | 引用身份、版本、依赖闭包、冲突矩阵、权限交集、顺序无关 |
| 发布 | 裁剪等价、调试伴随记录、主体摘要、外部签名、软件物料清单和复现结果 |
| 运行 | 实际字节重验、能力最小化、真实观察、事件完整、验收分层 |

## 模型与协议

模型加入前必须先建立无模型基线。模型输出只作为不可信候选进入系统；MCP 和 A2A 只通过 Praxor 外缘的协议适配器接入。外部参数结构合法不等于语义正确或权限允许。若模型无法在错误确定率、上下文成本或任务成功率上证明净增益，项目就停止自研模型平台投入。

完整完成标准见[开发路线图](../development/implementation-roadmap.html)，测试矩阵见[测试与验证](../development/testing.html)。
