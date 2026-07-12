# ADR-0003：工具链产物闭环与签名边界

- 状态：已接受为架构设计原则
- 日期：2026-07-12
- 影响范围：对象生命周期、工具职责、发布封装、运行证据与评估

## 问题

单个工具的职责可以分别成立，但如果上游产物没有明确消费者，或下游要求的输入没有明确生产者，工具链仍然无法闭环。当前设计需要统一回答以下问题：

- 源内容、确定性对象、链接对象、发布对象与运行结果怎样连续转换；
- 覆盖证明、验证结论、调试伴随文件和模型包在哪个阶段进入发布闭包；
- 发布包由谁建立签名范围、由谁持有密钥、签名结果怎样回填；
- Agent Harness、Fulfillment Runtime、观察工具和评估工具怎样共享同一次运行的身份与证据；
- 研究评估与发布验收怎样区分，避免单一分数替代对象安全或任务正确性。

## 决定

Noemion 采用以下主产物流：

1. **来源 → NOBJ：**`noemcompile` 或 `noemassemble` 产生可重定位 NOBJ；`noemformat`、`noemanalyze`、`noeminspect`、`noemvalidate`、`noemcompare` 和 `noembudget` 提供前后检查与分析。
2. **NOBJ → 链接对象 / HOBJ：**`noemarchive` 与 `noemsymbols` 提供归档和符号视图，`noemlink` 解析符号、重定位、约束和依赖闭包。
3. **链接对象 → 发布对象：**`noemreduce` 删除允许移除的开发信息并产生 Debug Companion、对象摘要与等价证据；`noemcoverage` 对最终发布对象、来源和 Assembly/Compiler Evidence Ledger 建立 Release Coverage Proof；`noemvalidate` 对准备打包的对象执行所需验证层。
4. **发布对象 → 签名包：**`noembundle` 消费发布对象、Release Coverage Proof、验证结论、依赖锁定以及带 eligible-for-bundle 资格记录的模型包，先生成不可变候选包和 Signing Request。私钥始终留在外部签名系统；回填时必须同时读取原候选包、原 Signing Request 与 Signature Response，并只在候选载荷外附加 Signature Envelope，不能改变被签字节。
5. **签名包 → 运行记录：**`noemexecute` 重新验证实际包字节和运行策略，建立装载状态、Agent Harness 会话和 Fulfillment Runtime 调用，输出 Run Record、Session State、Run Report、Trace Stream 与 Trace Integrity Metadata。
6. **运行记录 → 验收与评估：**`noemobserve` 规范化 Trace Stream 并产生 Trace Integrity Report；`noemcoverage` 检查运行证据是否形成 Evidence Closure Report；`noemexecute finalize` 按 Acceptance Policy 产生 Run Result 与 Acceptance Decision；`noemevaluate` 只在此后离线评估模型资格或 Agent 场景，不反向成为同一次运行的覆盖输入。
7. **跨阶段认证：**`noemcertify` 使用规范套件和各阶段报告检查跨工具一致性，但不替代发布决策、签名授权或独立安全审查。

## 签名边界

- `noembundle` 负责计算签名范围、生成待签摘要、验证回填签名并封装签名包。
- 外部签名系统负责私钥保护、授权、算法执行、审计和撤销策略。
- Signature Response 必须绑定 Signing Request、候选包身份、算法、签名者和策略版本；不匹配时必须拒绝。
- 无签名响应时只能产生 Unsigned Package Candidate，不得标记为可执行发布包。

## 运行边界

- Noema Object System 负责把签名包转换为不可变 Loaded State；其中只保存能力需求和授权上限，不保存实时句柄。
- Agent Harness 负责会话、上下文、会话级能力绑定、预算、观察、证据闭包、Acceptance Policy 与人工升级。
- Fulfillment Runtime 负责在受限语义视图和验收契约下求解，产生候选、Candidate Assessment 与 Capability Request，不产生最终 Acceptance Decision。
- 三者可以由 `noemexecute` 统一驱动，但必须保留各自的失败分类和证据。

## 后果

所有工具页面、架构图、指南和测试必须使用同一产物名称与责任边界。任何新增工具或产物必须说明上游生产者、下游消费者、身份绑定、失败责任和是否进入签名范围；不能留下无人消费的正式产物或来源不明的必需输入。
