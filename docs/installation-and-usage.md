---
layout: "manual"
title: "获取与使用指南 · Noemion"
page_role: "content"
footer_text: "Noemion · 获取与使用指南"
permalink: "/docs/installation-and-usage.html"
manual_id: "docs"
manual_group: "start"
manual_order: 2
nav_title: "获取与使用指南"
hero_title: "获取与使用指南"
hero_description: "说明当前可用资源、计划中的 Endem 流程和正式发布的完整性要求。"
summary: "查看当前可用资源、计划中的 Endem 流程和正式发布要求。"
badges: ["Unreleased", "Endem CLI", "Integrity First"]
---

## 当前可用性

> 当前没有正式版本、二进制安装包或可执行 `endem`。`.endem` 是已接受的工程扩展名选择，但规范编码、MIME 登记、CLI 参数和 ABI 仍未发布。

资源状态以[下载与资源](../downloads/)为准。正式制品出现时，安装入口必须同时说明版本、平台、大小、摘要、签名、SBOM、许可证和支持范围。

## 计划中的使用流程

```text
endem form goal.endem.txt -o goal.endem
endem check goal.endem
endem see goal.endem
endem bind goal.endem dep.endem -o release.weave
endem pack release.weave
endem seal release.weave --request signing.req
endem run release.weave
```

以上仅说明子命令职责，不冻结参数拼写或 Weave 扩展名。

1. 作者提交受控 Source Card；模型只能协助提出 `mean/case/when/open` 投影候选，不能把候选写成规范事实。
2. `form` 依据确定性规则与 Source Binding Decision 写入 Endem。
3. `check` 直接读取实际字节并分层验证；`see` 以独立实现提供只读视图。
4. 有真实多目标消费者时，`bind` 才解析引用并形成 Weave。
5. `pack` 证明裁剪等价；`seal` 只产生请求并核对外部签名响应，私钥不进入 Core。
6. `run` 在隔离进程重新验证 Weave，建立 Frame，由 Harness 控制能力，最终形成 Witness 与 Acceptance Decision。

## 发布原则

- 开发快照与正式版本明确区分，不共享含糊的“最新版”入口。
- 依赖内容寻址并锁定来源；构建固定 locale、时区、路径和构建纪元。
- 候选版本公开前完成双环境复现、安全/模糊测试、许可证核对、SBOM 和跨 Reader 一致性。
- 下载后先验证摘要和签名，再解析制品；签名有效不意味着当前运行策略允许其能力。
- 撤回、漏洞响应、密钥轮换、支持周期和长期归档必须在稳定发布前建立。

## 命名发布门

Endem 已通过互联网与 PyPI/npm/crates 等相邻工程命名初筛；正式软件和商标发布前仍必须完成目标司法辖区与类别的专业商标检索。若发现阻断冲突，应在 ABI 冻结前通过 ADR 一次性改名，不保留旧命令或格式别名。
