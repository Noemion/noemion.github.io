---
layout: manual
title: "安全与独立检查 · endem 使用手册"
page_role: docs-topic
footer_text: "Noemion · endem 使用手册"
permalink: "/endem/docs/safety.html"
manual_id: "endem"
manual_group: "safety"
manual_order: 3
nav_title: "安全与独立检查"
page_heading: "安全与独立检查"
page_lead: "说明为什么写文件的程序不能独自证明文件正确，以及两条读取路径怎样安全处理损坏、恶意或超大输入。"
summary: "比较 elenk 与独立 theor，并查看越界、溢出和共同错误怎样被发现。"
badges: ["elenk", "theor", "封闭失败"]
---

## elenk 与 theor 回答不同问题

| 入口 | 主要问题 | 能否供制品形成与发布流程继续使用 |
| --- | --- | --- |
| `endem elenk` | 这份实际字节是否满足请求的结构、语义、状态、完整性与策略层？ | 可以；全部所需层通过后，Ktisor 内部可以保留绑定精确字节、规范/Profile、检查配置和已完成层次的引用 |
| `endem theor` | 独立实现怎样读取和显示这份实际字节？ | 不可以；只提供观察、差分和诊断 |

`theor` 可解析对象不表示 `elenk` 已通过；`elenk` 通过也不能替代 `theor` 在一致性测试中的第二种解释。Ktisor 内部引用不是 CLI 输出、Iknem、签名、授权或最终决定，也不能跨入 Theor 的信任域。

## 独立 Theor 要求

`theor` 不得复用 Ktisor 的形成侧解析器、写入器、组合器、生成代码或错误分类实现。它只共享公开规范和测试向量，并使用独立数据结构与资源限制。

GNU [`readelf` 手册](https://www.sourceware.org/binutils/docs/binutils/readelf.html)说明它独立于 BFD，为第二条直接读取路径提供了工程先例。

[GNU BFD 信息损失说明](https://sourceware.org/binutils/docs/bfd/BFD-information-loss.html)指出，不同对象格式进入共同表示后，目标格式无法承载的信息可能丢失。Endem 第一阶段因此使用格式专用路径，不让通用表示代替实际字节。

这些资料只支持“独立直接读取”的方法，不决定 Endem 格式，也不使 `theor` 成为传统对象工具的复刻。

## 有界读取

所有对象输入都不可信。实现必须在分配和解释前检查：

- `offset + length`；
- `count × entry_size`；
- 对齐上取整和累计大小；
- 字符串、节点、边、成员和 Iknem 数量；
- 解压后的逻辑大小；
- 递归、循环和图遍历深度；
- 单次输出和总内存预算。

计算使用 checked arithmetic。任何溢出、越界、重叠、非法对齐或资源放大都关闭失败，不能产生部分可信对象。

## 分层结论

`elenk` 对每个请求层返回 `pass`、`fail` 或 `not-evaluated`。建议至少区分：

1. 物理结构和边界；
2. 六个语义面与引用；
3. `nascent / coherent` 内容形成责任，以及现行 `attested` 草案值不能推出的结论；
4. 外部陈述的主体摘要、类型、签名范围、验证政策与撤销材料；
5. 当前策略、能力上限和目标环境兼容性。

未执行层不得显示为通过。签名存在不等于信任层通过，内部摘要匹配也不等于发布者身份有效。

## 一致性验证怎样使用两条路径

一致性验证对合法、边界和畸形向量分别运行生产侧 `elenk` 路径与独立 Theor，并比较字段解释、失败位置和分类。任何分歧都阻断发布，先调查规范是否含糊，再分别修正规范或出错实现并重跑两条路径；不能简单选择某一实现作为事实来源，也不能改写输入来制造一致。它不是 `endem` 动作。
