---
layout: "manual"
title: "重定位与 ID 重映射 · synthesis 使用手册 · Noemion"
page_role: "docs-topic"
footer_text: "Noemion · synthesis 使用手册"
permalink: "/tools/synthesis/docs/relocations.html"
manual_id: "synthesis"
manual_group: "linking"
manual_order: 7
nav_title: "重定位与 ID 重映射"
hero_title: "重定位与 ID 重映射"
hero_description: "说明 Section 合并后怎样重映射标识符并修正类型化引用。"
summary: "说明 Section 合并后怎样重映射标识符并修正类型化引用。"
badges: ["synthesis", "Phase 4 / Phase 5"]
---

## 为什么使用类型化重定位

NIR/NOBJ 中的引用不只是字节地址，也可能指向符号、资源、策略、评价器、模型、结构定义或能力。若所有引用都退化为无类型整数，链接器就无法验证目标类别、权限和生命周期。类型化重定位让每次修正都携带“来源位置、期望目标和允许变换”，从而可以在写入前验证。

## 处理范围

- 合并兼容 Section、字符串表、概念表和语义原型表。
- 重新编号 NIR Node、Edge 与产物 ID。
- 应用资源、模型、评价器、策略和能力引用的类型化重定位。

## 重定位记录的最低契约

| 字段职责 | 要求 |
| --- | --- |
| 来源定位 | 明确输入对象、Section、记录或字段；必须验证边界和对齐。 |
| 重定位类型 | 决定期望目标类别、编码宽度、空值与溢出语义。 |
| 目标身份 | 通过符号或局部 ID 定位，不能依赖未验证的绝对偏移。 |
| 加数或变换 | 若允许，必须定义符号范围、算术宽度和 checked arithmetic。 |
| 来源版本 | 绑定对象格式和 ABI 版本，禁止把未知类型按已知类型解释。 |

## ID 重映射算法

1. 验证所有局部 ID 唯一、在表范围内且目标类别与声明一致。
2. 按规范稳定顺序为保留实体分配全局 ID，先形成不可变映射表。
3. 逐项验证引用，使用 checked arithmetic 计算目标字段和值；写入前检查宽度和编码。
4. 应用修正后重新遍历，证明不存在悬空局部 ID、错误类型目标或未消费的必需重定位。
5. 把旧 ID、新 ID、来源对象和修正原因写入链接映射。

失败必须是事务性的：不得在验证到一半时把已修改缓冲区作为候选产物继续传递。

## 重定位类型候选

```text
R_NIR_SYMBOL
R_NIR_RESOURCE
R_NIR_POLICY
R_NIR_EVALUATOR
R_NIR_MODEL
R_NIR_SCHEMA
R_NIR_PROTOTYPE
R_NIR_CAPABILITY
```

> 以上名称是候选类型，不是已冻结 ABI；正式编号和记录布局必须由对象格式规范与 ADR 确定。

## 必须失败与验证

- 未知必需重定位类型、来源越界、目标缺失、目标类别不匹配、编码溢出或不允许的跨权限引用。
- 两个输入实体被错误映射到同一全局 ID，或同一输入实体在相同上下文得到不同全局 ID。
- 重定位后仍存在指向被裁剪、未拉入或不可见实体的 required import。

测试应覆盖每类重定位的最小值、最大值、边界外一位、错误类别、排列变化和往返解析，并验证链接映射能复现每个映射决定。
