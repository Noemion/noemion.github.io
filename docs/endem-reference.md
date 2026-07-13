---
layout: "manual"
title: "Endem 应用参考 · Noemion"
page_role: "content"
footer_text: "Noemion · Endem 应用参考"
permalink: "/docs/endem-reference.html"
manual_id: "docs"
manual_group: "reference"
manual_order: 5
nav_title: "Endem 应用参考"
page_heading: "Endem 应用参考"
page_lead: "一个公开 CLI、八个短动作、三个不能合并的信任域。"
summary: "按生命周期查找 endem 子命令、消费者、失败责任和实施阶段。"
badges: ["One CLI", "8 Verbs", "Unreleased"]
---

## 应用总览

`endem` 是唯一公开应用。它提供一致的用户入口，但不会把 Poiet、独立 Theor 与隔离 Drasor 链接进同一信任域。

| 子命令 | 直接职责 | 输出 | 何时建设 |
| --- | --- | --- | --- |
| `poie` | 来源绑定、规范化、确定性写入 | Endem、诊断 | 第一阶段 |
| `elenk` | 生产验证实际字节 | 分层结论、内部验证句柄 | 第一阶段 |
| `theor` | 独立只读解析、查看与比较 | 有界视图与差异 | 第一阶段 |
| `peira` | 规范、语料、Poiet/Theor 差分与复现 | 一致性报告 | 第一阶段 |
| `pleko` | 解析引用、冲突与依赖闭包 | Synem、绑定映射 | 第二阶段；有真实组合案例后 |
| `tasse` | 类型化裁剪和发布闭包 | 发布候选、调试伴随记录 | 第三阶段 |
| `sphra` | 生成请求并核对外部签名响应 | attested Synem | 第三阶段 |
| `drase` | 重新验证、装载、能力循环与验收 | Dromen、Iknem、最终决定 | 第四阶段 |

## Poiet 子命令

`poie/elenk/pleko/tasse/sphra/peira` 共享规范注册表，但只有一个规范写入器。任意变换、归档、裁剪或格式转换不成为稳定命令；只有语义明确、有消费者且能证明不变量的类型化变换进入相应步骤。

`sphra` 不持有私钥。外部签名系统拥有独立权威和生命周期，因此签名请求与响应保持独立伴随材料。

## `theor` 的独立性

`endem theor` 的用户界面可以由主命令调度，但实现必须单独构建，不能复用 Poiet 的解析器、写入器、组合器或内部验证句柄。它只能回答“这些字节在有界读取下怎样显示”，不能回答“这些字节已经可信”。

建议二级动作保持普通短词：`view`、`diff`、`refs`、`size`、`trace`。是否全部成为稳定接口取决于真实消费者。

## `drase` 的隔离性

`endem drase` 启动独立 Drasor 进程。Drasor 重验实际字节并建立 Dromen；控制平面持有能力句柄；模型或其他后端位于受限子进程，只能提交候选和能力请求。Iknem 记录真实观察、事件完整性、证据范围和最终权威决定。

## 不建设独立模型平台

数据、训练、评估和量化优先适配外部成熟工具，不在第一阶段建立四个新产品。只有 Noemion 特有的血缘、资格或设备约束无法由现有工具表达，并且实验显示不可替代增益时，项目才新增研究适配面。该适配面永远不能写 Endem、签名或最终验收决定。

[打开完整 Endem 手册](../endem/docs/) · [查看实施路线](../development/implementation-roadmap.html)
