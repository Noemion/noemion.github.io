---
layout: manual
title: "证据与确定性 · noesis 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · noesis 使用手册"
permalink: "/tools/noesis/docs/evidence-and-determinism.html"
manual_id: "noesis"
manual_group: "reference"
manual_order: 5
nav_title: "证据与确定性"
hero_title: "证据与确定性"
hero_description: "区分 NIR 运行语义、Compiler Evidence Ledger、Build Manifest 和调试副产物。"
summary: "确定性排序、构建来源、模型指纹和编译证据的边界。"
badges: ["noesis", "Reproducible"]
---

## 四种信息不能混写

| 信息 | 作用 | 是否进入运行语义 |
| --- | --- | --- |
| NIR/NOBJ 核心记录 | 表达目标、约束、验收、能力需求和产物契约。 | 是。 |
| Compiler Evidence Ledger | 说明每个 Source Unit 怎样映射、保留、拒绝或保持未决。 | 不直接进入 Runtime；发布覆盖需要。 |
| Build Manifest | 保存输入摘要、配置、依赖、工具/模型指纹和决定制品摘要。 | 否。 |
| Debug Byproducts | 保存原文、完整候选、诊断上下文和可重建中间视图。 | 否，可裁剪或外置。 |

SLSA Provenance 把 BuildDefinition 与 RunDetails 分开，提醒构建输入和一次执行的环境元数据具有不同用途。Noemion 同样不把构建时间、工作目录或临时日志写进 NIR 语义。

## 确定性输入闭包

对象字节必须绑定以下输入：

- 规范版本、NIR/NOBJ 结构版本和启用特性；
- Source Package 与 Source Binding Decision 摘要；
- Frontend、规则、本体库、结构定义和锁定依赖；
- 影响候选生成的模型包、候选协议与窗口指纹；
- 资源限制、目标编码 Profile 和规范排序规则；
- `noesis`、Noesis Core 和对象写入器版本。

模型候选的生成可以非确定，但候选一旦作为输入制品冻结，后续验证、选择、NIR 构造和对象写入必须确定。

## 规范排序

- 字符串按规范化字节排序，不能使用区域设置比较。
- 记录按类别、稳定语义键、来源键和局部定义顺序的规范组合排序。
- 无序集合在编码前排序；有序列表必须明确说明顺序具有语义。
- Map 的传输顺序不能被当作语义，除非格式规范明确限制为确定性编码顺序。
- 填充字节固定为零或规范值，并纳入对象字节摘要。

## OpenAI 工程经验的采用边界

OpenAI 的 Harness Engineering 强调版本化仓库资料、可机器读取的 UI/日志/指标、边界处解析数据结构，以及用检查器和结构测试强制不变量。Noemion 采用这些工程原则来组织结构定义、诊断和回归测试；文章不定义 NIR 字段、NOBJ ABI，也不能证明模型候选忠实于来源。

原文：https://openai.com/zh-Hans-CN/index/harness-engineering/

## 验证

确定性测试至少改变工作目录、文件发现顺序、线程数、缓存状态、区域设置、时区和进程环境，并要求对象字节不变。模型关闭后，Deterministic Profile 的结构定义、拒绝结果和对象格式也必须保持不变。
