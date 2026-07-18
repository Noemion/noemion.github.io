---
layout: architecture-decision
title: ADR-0023 · 文件能读，不等于内容成立
page_role: content
footer_text: Noemion · ADR-0023
permalink: "/architecture/adr-0023-endem-content-standard.html"
summary: 说明读取一份 Endem 时为什么要依次检查字节结构、该格式允许的字段和目标内容；前一项通过不能证明后一项成立。
decision_id: ADR-0023
page_heading: ADR-0023 · 文件能读 · 不等于内容成立
page_lead: 读取一份 Endem 时，先检查字节能否安全分段，再检查该格式允许哪些字段，最后检查目标内容是否成立。三步分别使用版本化规则，前一步通过不能替后一步作出结论。
badges:
- 当前策略
- END-CORE 0.1.0-draft
- END-P2 0.1.0-draft
- 尚未实现
previous_url: adr-0022-evidence-and-appraisal.html
previous_label: ADR-0022
next_url: adr-0024-session-contract.html
next_label: ADR-0024
---

## 用一次读取流程理解三层符合性

读取器收到一份声明为 END-P2 的实验性 `.endem` 文件。它可以安全读出六个记录，也可以确认字段和引用闭合；但在外部授权决定尚未核对时，仍不能声称 END-CORE 内容已经成立。

1. 固定格式与Profile 版本
2. 检查头部目录范围与编码
3. 检查字段枚举引用与预算
4. 核对外部授权与伴随资料
5. 判断 END-CORE内容是否成立
6. 另行判断目标与最终接受

| 处理阶段 | 当前文件可以证明 | 必须停止的情况 |
| --- | --- | --- |
| 固定解释规则 | 头部声明 `END-FMT 0.1` 和 `profile_id=3`，调用方也明确支持相应草案。 | 按“最新版本”、文件扩展名、环境搜索或猜测解释。 |
| 容器检查 | 固定前导、目录、偏移、长度、对齐和确定性 CBOR 可以安全解释。 | 越界、重叠、非最短编码、未知关键记录或预算超限。 |
| Profile 检查 | 六个记录满足 END-P2 的封闭字段、类型、枚举、排序、来源范围和引用规则。 | 未知字段、悬空引用、未经登记的状态或能力。 |
| 内容检查 | 只有外部 AUT-CORE 授权等前置条件也精确绑定并通过后，才可能声明 END-CORE 内容接受。 | 把权威名称、签名外观、本地 ACL 或缓存成功当成外部义务已经完成。 |
| 后续判断 | 内容可进入证据、会话和目标判断流程。 | 把内容接受直接提升为目标满足、可执行、已签署或最终获准。 |

因此，通用 CBOR 解码成功、六个记录齐全或 END-P2 检查通过，都不能简写为“有效 Endem”。

## 通用内容、内容 Profile 与物理容器各自负责什么

| 规范层次 | 回答的问题 | 当前权威源 | 不得越界 |
| --- | --- | --- | --- |
| 通用内容 | 什么是一个 Endem；六个语义面、关系、状态、身份和信任边界怎样成立。 | [END-CORE 0.1.0-draft](https://noemion.github.io/spec/endem-core.html) | 不规定魔数、字段宽度、记录编号或具体编码。 |
| 内容能力集（Profile） | 这一版本实际允许哪些字段、枚举、组合、顺序、状态和资源上限。 | [END-P2 0.1.0-draft](https://github.com/Noemion/noemion.github.io/blob/main/spec/profiles/end-p2.json) | 只能收窄能力或补齐字段，不能改写六个语义面的职责。 |
| 物理容器 | 读取器怎样定位记录、解释字节并拒绝越界、歧义和非规范编码。 | [END-FMT 0.1.0-draft](https://noemion.github.io/spec/endem-format.html) | 结构合法不等于字段闭合，更不等于内容成立。 |
| 版本与验证索引 | 精确版本、条款、威胁、场景和正反向量是否能够追溯。 | [规范与验证索引](https://github.com/Noemion/noemion.github.io/blob/main/spec/registry.json)及向量目录 | 测试结果不能建立第二套语义，也不能证明组件已经实现。 |

项目需要一份 Endem 内容标准，但不新增重复规范 ID：现有 END-CORE 正式承担通用内容标准，ADR 只解释采用理由，登记与向量只提供可审查证据。

## END-P2 与未来发布 Profile 不是连续信任等级

| Profile | 用途与内容 | 单文件最高结论 | 不能怎样使用 |
| --- | --- | --- | --- |
| END-P2<br>含来源形成 Profile | 保存实际进入形成过程的自然语言、六个非空语义记录、来源范围和封闭引用。 | `profile-accept`<br>`content=external-prerequisites-not-evaluated` | 不能发布为最终裁剪制品，也不能凭权威名称补齐外部授权。 |
| 未来裁剪发布 Profile | 移除原始自然语言和可逆副本，保留运行必需的语义结构，并重新定义来源绑定和披露边界。 | 尚未定义 | 不能直接删除 `source_expression.content` 后沿用 END-P2、旧身份、签名或接受状态。 |

形成版与发布版必须是两个精确对象。它们在生命周期上类似“含调试资料的构建产物”和 GNU `strip` 处理后的发行产物，但 Noemion 不照搬 ELF 节、符号或 `.gnu_debuglink`；未来 Profile 必须逐项定义保留、删除、降精度、重写和失败责任。

新增 Profile 或字段前，必须有不可替代的消费者、生产者、规范化规则、未知能力行为、资源上限、威胁、支持案例、反例和正反向量。模型提示、推理轨迹、实时凭据、遥测导出、签名、证据和最终决定不进入 Endem 内容身份。

## 每一层都要用自己的结果名称

| 结果层 | 当前报告方式 | 它明确没有证明什么 |
| --- | --- | --- |
| 容器接受 | `container-accept`，或带 `layer=structure` 的拒绝诊断。 | 没有证明字段集合符合任何内容 Profile。 |
| Profile 接受 | `profile-accept`，并记录精确 Profile 身份。 | 没有证明外部授权、签名、证据或撤销前置条件已经核对。 |
| 内容接受 | 未来符合性报告必须绑定 END-CORE、Profile 和全部外部前置条件的结果。 | 没有证明现实目标已经满足、会话可以运行或最终权威已经接受。 |
| 目标满足 | `met / unmet / undetermined / fault`。 | 没有作出发布、部署或其他权威决定。 |
| 权威决定 | `accepted / rejected / deferred`，并绑定决定者、范围和依据。 | 不会反向改变 Endem 内容身份或历史检查结果。 |

三个 END-P2 接受向量使用 `profile-accept / external-prerequisites-not-evaluated`。这一结果准确反映机器检查完成的范围，并与 END-P2 的声明上限一致。

> **名称与口头边界：**Profile 在中文交流中可能指用户画像、性能剖析或配置文件，首次出现应写“内容能力集（Profile）”。不要只说“通过了”，应说“END-P2 含来源形成 Profile”“容器接受”或“Profile 接受”。日志也不得用裸露的 `valid=true` 合并层次。

## 系统格式与 AI 格式只能提供哪些借鉴

**复核日期：**2026-07-16。ELF 不是由 IETF RFC 定义；当前 gABI 页面本身标为 4.3 Draft，因此这里只采用可验证的结构机制，不把它当作 Endem 的语义权威。

| 外部资料 | 可采用的机制 | Noemion 不继承 |
| --- | --- | --- |
| [ELF gABI 对象格式](https://gabi.xinuos.com/elf/01-intro.html) | 固定头部提供文件路线图，节与程序头面向不同读取任务；处理器补充另行约束机器细节。 | 不采用地址、指令、装载段、处理器 ABI 或链接语义。 |
| [RFC 8949 CBOR](https://www.rfc-editor.org/rfc/rfc8949.html) | 提供确定长度、最短编码和映射键排序等确定性编码基础。 | 具体协议仍须明确允许类型、字段语义和拒绝规则；通用解码成功不是符合性。 |
| [GNU readelf](https://sourceware.org/binutils/docs/binutils/readelf.html) | 独立于 BFD 解析 ELF，支持未来形成器与独立检查器采用不同代码路径。 | 工具独立不自动证明两套实现都正确。 |
| [GNU ar 确定性模式](https://sourceware.org/binutils/docs/binutils/ar-cmdline.html) | `-D` 清除 UID、GID、时间戳差异并固定文件模式，减少环境噪声。 | 确定字节不等于内容语义正确或来源可信。 |
| [GNU strip 与独立调试资料](https://sourceware.org/binutils/docs/binutils/strip.html) | `--strip-debug`、`--only-keep-debug` 和 `.gnu_debuglink` 展示形成资料与发行制品分离的生命周期。 | 删除错误节可能让文件不可用；Noemion 必须用新 Profile 和新身份定义裁剪。 |
| [ONNX 1.23.0 IR](https://onnx.ai/onnx/repo-docs/IR.html) | 分别版本化 IR、模型和算子集；模型必须声明所依赖算子集，运行时不支持就拒绝。 | 不采用计算图、算子语义或运行时执行能力；模型格式可读也不证明模型安全可靠。 |
| [SPDX 3.0.1 模型与序列化](https://spdx.github.io/spdx-spec/v3.0.1/serializations/) | 分开逻辑数据模型、物理序列化，并分别进行结构与语义验证。 | 不采用 RDF、JSON-LD 或 SPDX Profile；序列化一致不等于 Endem 内容接受。 |
| [OCI Content Descriptor](https://specs.opencontainers.org/image-spec/descriptor/) | 以媒体类型、摘要和字节大小精确引用外部内容，并在读取前核对。 | 摘要只标识字节，不证明被引用内容满足 Endem 语义或获得授权。 |

## 当前还不能承诺哪些实现与兼容性

END-FMT 与 END-P2 都是实验草案，不是稳定 ABI。量化、时间、测量、裁剪发布、内容摘要、签名包络、Semantic Key、evidence 绑定、压缩、加密、流式传输、MIME 类型和跨版本升级尚未确定。

当前规范、登记和 END-P2 正反字节向量只说明草案怎样分类已覆盖输入，不能证明任何写入器、读取器、CLI 或运行时已经实现。项目也没有可执行的裁剪命令、生产格式兼容承诺或供应商私有语义区。

第一版稳定标准之前，改变字段、编号或结果域就直接产生新草案版本，不保留含义漂移的别名。遇到未知的必需能力时必须拒绝继续；没有真实消费者和失败责任的字段不进入内容标准。

- [查看 Endem 开发者规范](../specifications/endem.html) — 从六项职责进入通用内容标准。
- [查看容器格式手册](../endem/docs/format.html) — 核对固定头部、目录、Profile 和拒绝顺序。
- [查看字节读取边界](adr-0011-endem-container.html) — 理解为何必须先做有界结构检查。
- [查看形成版与发布版](adr-0036-source-bearing-and-stripped-release.html) — 了解来源保留和未来裁剪 Profile 的边界。
