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
hero_title: "安全与独立检查"
hero_description: "区分生产 check 与独立 see，并对所有不可信制品执行有界读取。"
summary: "生产验证、独立 Reader、checked arithmetic、分层结论和差分测试。"
badges: ["check", "see", "Fail Closed"]
---

## check 与 see 回答不同问题

| 入口 | 主要问题 | 能否进入生产信任链 |
| --- | --- | --- |
| `endem check` | 这份实际字节是否满足请求的结构、语义、状态、完整性与策略层？ | 可以；全部所需层通过后，Core 内部可产生绑定字节和配置的 Verified Handle |
| `endem see` | 独立实现怎样读取和显示这份实际字节？ | 不可以；只提供观察、差分和诊断 |

`see` 可解析对象不表示 `check` 已通过；`check` 通过也不能替代 `see` 在一致性测试中的第二种解释。

## 独立 Reader 要求

`see` 不得复用 Core 的生产 Reader、Writer、绑定器、生成代码或错误分类实现。它只共享公开规范和测试向量，并使用独立数据结构与资源限制。

GNU `readelf` 独立于 BFD 的做法提供了工程先例：

https://www.sourceware.org/binutils/docs/binutils/readelf.html

BFD 面向多格式 canonical representation，可能隐藏格式特有信息；Endem 第一阶段不链接 BFD：

https://sourceware.org/binutils/docs/bfd.html

这些资料只支持“独立直接读取”的方法，不决定 Endem 格式，也不使 `see` 成为传统对象工具的复刻。

## 有界读取

所有对象输入都不可信。实现必须在分配和解释前检查：

- `offset + length`；
- `count × entry_size`；
- 对齐上取整和累计大小；
- 字符串、节点、边、成员和 Witness 数量；
- 解压后的逻辑大小；
- 递归、循环和图遍历深度；
- 单次输出和总内存预算。

计算使用 checked arithmetic。任何溢出、越界、重叠、非法对齐或资源放大都关闭失败，不能产生部分可信对象。

## 分层结论

`check` 对每个请求层返回 `pass`、`fail` 或 `not-run`。建议至少区分：

1. 物理结构和边界；
2. 五组语义与引用；
3. open/bound/sealed 状态不变量；
4. 内容摘要、签名范围与撤销材料；
5. 当前策略、能力上限和目标环境兼容性。

未执行层不得显示为通过。签名存在不等于信任层通过，内部摘要匹配也不等于发布者身份有效。

## test 怎样使用两条路径

`endem test` 对合法、边界和畸形向量分别运行 Core 与 Reader，并比较字段解释、失败位置和分类。任何分歧都阻断一致性发布，先调查规范是否含糊，再修复实现；不能简单选择某一实现作为事实来源。
