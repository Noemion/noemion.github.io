---
layout: manual
title: "安全读取与诊断 · theoria 使用手册 · Noemion"
page_role: docs-topic
footer_text: "Noemion · theoria 使用手册"
permalink: "/tools/theoria/docs/safe-reading.html"
manual_id: "theoria"
manual_group: "security"
manual_order: 3
nav_title: "安全读取与诊断"
hero_title: "安全读取与诊断"
hero_description: "约束畸形对象、压缩载荷、字符串、图遍历和结构化输出的资源使用。"
summary: "不可信对象下的 checked arithmetic、预算、诊断分层和输出安全。"
badges: ["theoria", "Checked Reader"]
---

## 不可信输入

文件名、签名状态或下载来源都不能跳过结构检查。读取器必须把 Preamble、目录、字符串、记录、压缩载荷、符号和重定位分别视为可能畸形的数据。

## 必需预算

| 预算 | 防止的问题 |
| --- | --- |
| 文件与总映射大小 | 超大输入和地址空间耗尽。 |
| Section/Segment 数量 | 计数放大和目录扫描耗尽。 |
| 字符串长度与总字节 | 终端、JSON 和内存放大。 |
| 记录/节点/边数量 | 图展开和排序耗尽。 |
| 递归与依赖深度 | 循环、深层结构和栈耗尽。 |
| 解压后大小与比例 | 压缩炸弹。 |
| 诊断数量与输出字节 | 错误风暴和日志耗尽。 |

所有 `offset + size`、`count × entry_size`、对齐上取整和索引换算都在执行前使用 checked arithmetic。发现一个错误后继续扫描只能使用已经验证的边界，不能为了更多诊断访问不可信范围。

## 输出安全

- 控制字符、终端转义和无效 Unicode 必须转义。
- 敏感来源、凭据和受限调试 Section 默认只显示摘要和大小。
- JSON/CBOR 输出必须有结构版本，并区分 raw、derived 和 verdict 字段。
- 图输出限制节点、边、标签长度和递归深度。
- 诊断排序使用稳定位置与错误码，不依赖并行完成顺序。

## 错误层次

| 层次 | 示例 |
| --- | --- |
| Container | 截断 Header、目录越界、非法对齐。 |
| Encoding | 无效 UTF-8、记录长度不匹配、压缩格式错误。 |
| Schema | 未知 required 类型、字段类别错误、索引越界。 |
| Reference | 悬空符号、错误重定位目标、来源引用缺失。 |
| Policy | 权限、签名、依赖和验收策略；由验证器判断。 |

`theoria` 可以报告前四层的观察，但只有 noemvalidate 产生共享的分层验证结论。查看器必须避免使用“安全”“可信”或“可执行”描述单纯可解析对象。
