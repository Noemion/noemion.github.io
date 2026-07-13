# ADR-0007：Phase 0/1 首个实现纵向切片与外部技术采用边界

- 状态：Superseded by ADR-0008
- 日期：2026-07-12
- 影响范围：未来实现工作区、规范制品、测试向量、安全读取器、对象写入器、工具拓扑、GNU 技术采用与外部 AI 协议适配

> 这是已被取代的历史设计记录。项目当前尚未进入代码开发阶段，本文中的实现路径、目录和工作包都不是现存组件或开工授权。

## 问题

站点已经描述 23 项工具职责，但当前没有正式规范制品、可执行程序或独立实现证据。如果按页面数量直接创建二进制，会在格式未冻结前扩大维护面，也会把诊断工具误接入可信主链。

同时，ELF/GNU Binutils、可复现构建工具和正在形成的 AI 协议都提供了可借鉴机制。直接嵌入 BFD、通用链接脚本、模型 SDK 或协议状态机，会让第一阶段的安全核心承担不必要的许可、兼容和攻击面。

## 决定一：先实现一条可反驳的最小纵向切片

首条实现路径固定为：

```text
Canonical Text NIR
  → morphe 前端
  → Noesis Core 共享校验与对象写入边界
  → Relocatable NOBJ
  → noemvalidate 生产读取器与分层验证
  → theoria 独立直接读取器与只读视图
  → noemcertify 差分与一致性报告
```

- `morphe` 不能拥有另一套对象语义；它调用与 `noesis` 共用的确定性 Noesis Core 校验和写入边界。
- `theoria` 的第一条直接读取路径不复用生产写入器、链接器或 BFD 的解析代码。它只提供独立观察与差分证据，不产生 `Verified Object Handle`。
- `noemvalidate` 直接读取原始对象、配置和信任材料；它不能把 `theoria` 的文本或结构化视图当作可信输入。
- 链接、HOBJ、发布封装、装载、Agent Harness 和模型均不进入这条切片。只有最小对象格式、拒绝路径和跨实现解释一致后，才开始后续阶段。

## 决定二：工具页表示职责，不承诺 23 个独立二进制

代码阶段开启后，如果建立实现工作区，应至少分离以下职责目录：

```text
spec/        规范条款、注册表和版本说明
vectors/     合法、边界与畸形测试向量
core/        生产读取器、验证器与对象写入器
oracle/      不共享解析代码的独立只读实现
tools/       最小 CLI 外壳与一致性运行器
```

工具可以先作为同一可执行文件的子命令或共享库的薄外壳。只有出现独立版本、权限隔离、资源边界或真实下游消费者时才拆分二进制或仓库。`noemtransform`、`noembudget`、`noemdecode`、`noemsymbols` 等职责可以先由检查器或测试工具提供；没有消费者时停止建设，不为 GNU 工具数量或页面对称复制命令。

## 决定三：GNU/ELF 只提供机制先例，不进入第一阶段可信核心

- 采用 ELF 的 Section/Segment 双视图、显式符号与重定位、未知关键扩展拒绝，以及 GNU `readelf` 独立于 BFD 的交叉检查做法。
- 不链接 BFD。BFD 的多格式 canonical form 会扩大信任面，并可能丢失格式特有信息；NOBJ 需要直接、有界、可逐字段审计的解析器。
- 不采用 gold、动态环境搜索、lazy binding、weak symbol 选择、隐式初始化、DWARF 表达式或通用链接脚本。它们不属于最小语义对象核心。
- 借鉴 GNU `ar -D` 的确定性元数据、`objcopy --only-keep-debug` 的调试伴随文件和 linker map 的可审计决策输出，但不照搬传统机器地址与 CRC 身份模型。
- GNU Make、Autoconf、Automake、Libtool、Texinfo、gettext 和 Guix 只在出现真实构建、发行、手册、本地化或复现消费者时进入核心外层。Guix 可以成为 Linux 的附加复现通道，不能成为 NOBJ Runtime 依赖。

## 决定四：AI 协议与模型能力只通过外部适配器进入

- 第一阶段不调用模型，不引入 MCP、A2A、OpenTelemetry GenAI 语义或供应商 SDK。
- 后续 MCP/A2A 适配器位于 Agent Harness 外缘，只把远端声明翻译为 Noemion 自有的 Capability、Task、Evidence 与 Policy 结构。工具说明、Agent Card、schema 和远端结果均是不可信声明，不是授权。
- JSON Schema 2020-12 可用于外部交换、能力参数和测试夹具；模式合法只证明语法与结构，不能证明字段值、权限或任务语义正确。
- OpenTelemetry GenAI 只可作为版本化导出映射，不能进入 NOBJ、运行事件或 Acceptance Decision 的稳定身份。
- 模型、长上下文或知识图能力必须先与规则、BM25、向量检索和外部模型基线比较。未形成来源隔离证据前，Horizon Engine 仍是可省略研究分支。

## 工作包与完成标准

| 工作包 | 必须产出 | 完成标准 |
| --- | --- | --- |
| P0-W1 权威规范 | 版本化 Markdown、条款 ID、术语与成熟度注册表 | 每个实现义务能定位到唯一条款，HTML 只做解释和入口。 |
| P0-W2 威胁与限制 | 解析威胁模型、最大值、checked arithmetic 规则、扩展 criticality、身份与摘要域 | 每类溢出、越界、重叠、循环、自引用与资源放大都有拒绝语义。 |
| P0-W3 测试向量 | 规范字节样本、字段注释、合法/畸形/边界语料、期望诊断 | 两个读取器不依赖实现内部状态即可得到同一字段解释和失败分类。 |
| P0-W4 语言与构建 ADR | Rust 与 C/C++ 的同向量最小读取实验、依赖/许可清单、复现与模糊测试结果 | 依据内存安全、受检算术、跨平台、构建复现、FFI 和维护成本选定首版语言；偏好不能替代数据。 |
| P1-W1 生产核心 | 失败原子的 Reader、Validator、Writer 与不可变读取视图 | 畸形对象不产生部分可信状态；相同输入得到相同字节与稳定诊断。 |
| P1-W2 独立读取器 | 不共享解析代码的原始字段检查与有界输出 | 能发现生产读写器共同假设；其输出不进入信任决定。 |
| P1-W3 差分与模糊测试 | 字段差分、性质测试、语料回归、资源上限与覆盖引导模糊测试 | 生产与独立实现对全部基准向量一致，对所有畸形类别稳定拒绝。 |
| P1-W4 构建复现 | 两个路径和两个隔离环境的重复构建、逐字节比较、构建清单 | 对象产物和工具二进制分别报告复现结果；签名真实性作为第三种属性单独验证。 |

## 参考与采用边界

- ELF gABI：https://gabi.xinuos.com/elf/
- GNU Binutils 2.46.1 当前发行与 2.46 文档：https://sourceware.org/binutils/
- GNU `readelf` 独立解析边界：https://www.sourceware.org/binutils/docs/binutils/readelf.html
- GNU `ar` 确定性模式：https://sourceware.org/binutils/docs/binutils/ar-cmdline.html
- GDB separate debug files：https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html
- Reproducible Builds `SOURCE_DATE_EPOCH`：https://reproducible-builds.org/specs/source-date-epoch/
- MCP 2025-11-25：https://modelcontextprotocol.io/specification/2025-11-25
- A2A 1.0 版本化规范：https://a2a-protocol.org/v1.0.0/specification/
- JSON Schema 2020-12：https://json-schema.org/draft/2020-12
- OpenTelemetry GenAI 语义约定（Development）：https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai
- OpenTelemetry GenAI 独立语义仓库：https://github.com/open-telemetry/semantic-conventions-genai

## 后果

当前下一项工作不是创建全部工具，而是完成 P0-W1 至 P0-W4，并让第一条 NOBJ 纵向切片具备两条独立读取路径。任何新增框架、二进制、格式字段或协议映射都必须说明真实消费者、信任与失败责任，以及不采用时会失去的能力。
