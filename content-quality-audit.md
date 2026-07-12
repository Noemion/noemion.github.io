# Noemion 内容、系统闭环与路由审计

状态：Noemion 项目层与 Endem 工程词汇分层后的权威审计基线
范围：`sitemap.md` 登记的全部正式 HTML 路由

## 结论边界

Noemion 已经接受以 Endem 为核心制品的工程词汇和单一应用拓扑，但尚未发布规范编码、可执行程序、ABI、实验结果或正式版本。页面存在只证明设计可审查，不证明实现可用、性能成立、研究结论有效或已获得任何知识产权/标准化认可。

## 审计问题

每条路由按自身角色回答以下问题，不用同一模板衡量门户、规范、应用与手册：

1. 读者进入页面要解决什么问题，首屏是否给出直接结论？
2. 该页面、组件、制品或子命令是否有独立消费者、权威、权限、生命周期或失败责任？
3. 输入由谁产生，输出由谁消费；若没有消费者，是否应删除或合并？
4. 来源忠实、结构有效、语义有效、闭包完整、签名真实、环境授权、证据充分和任务满足是否分别判断？
5. 候选、开放问题、已接受决定和实现证据是否明确分开？
6. 链接、目录、上下页、移动布局、键盘操作和正文宽度是否可用？

## 当前领域闭环

```text
source signs ─ poie ─► Endem ─ pleko ─► Synem ─ praxe ─► Dromen ─► phain / Tekmor ─► Decision
                         │                 │
                         └──── theor ──────┘
```

### 正式名词

| 名词 | 存在价值 | 生产者 | 消费者 | 省略条件 |
| --- | --- | --- | --- | --- |
| Endem | 保存一个根期望终态及 rhem/semion/skena/telis/krin/apor | Poiet 的 `poie` | elenk、theor、pleko、注册表与人工审查 | 不可省略；它是最小原语 |
| Synem | 固定多 Endem 引用、依赖、冲突结论与发布范围 | Poiet 的 `pleko/tasse/sphra` | Praxor、部署与审计 | 单一自包含 Endem 或没有组合消费者时省略 |
| Dromen | 保存一次运行已重新验证的不可变实现态和能力上限 | Praxor 的 `praxe` | Harness 与实现后端 | 不作为磁盘制品或公开格式 |
| Tekmor | 把事件、观察、证据范围、环境、策略与决定绑定 | Praxor/Harness/决策权威 | 用户、CI、审计与离线评估 | 只有权威或保密边界确实不同时才拆 sidecar |

Debug Companion 与 Signing Request/Response 可以独立，因为它们分别具有不同访问控制和外部签名权威。临时诊断、link map、coverage、trace 与 praxe report 默认只是上述制品的类型化记录，不为流程对称单独造格式。

### 三个实现域

| 实现域 | 不可替代边界 | 禁止合并的内容 |
| --- | --- | --- |
| Poiet | 唯一规范 Writer、生产 Parser、来源绑定、elenk、pleko、tasse 与签名请求核对 | 模型不得写规范字节；Poiet 不持有私钥或实时能力 |
| Theor | 独立解析任意不可信字节，为差分和安全审查提供第二条证据链 | 不复用生产 parser，不产生 verified handle，不修复输入 |
| Praxor | 重新验证实际 Synem，建立 Dromen，控制能力与反馈，形成 Tekmor | 模型不持有句柄、不扩大权限、不自我验收 |

一个公开 CLI `endem` 只统一用户入口，不统一上述信任域。

## 应用存在性审计

| 子命令 | 独立消费者 | 失败责任 | 当前阶段 |
| --- | --- | --- | --- |
| poie | 作者、CI、pleko | 未授权语义、类型/约束、布局、非确定性 | Phase 1 |
| elenk | Poiet、Praxor、发行流程 | 结构、引用、语义、资源、完整性 | Phase 1 |
| theor | 开发者、安全审查、差分 CI | 畸形输入、未知关键结构、资源超限 | Phase 1，独立实现 |
| peira | 规范与发布评审 | 条款/向量/实现差异、复现失败 | Phase 1 |
| pleko | 多 Endem 消费者 | 引用、版本、冲突、权限与闭包 | Phase 2，有真实案例才实现 |
| tasse | 发行流程 | 裁剪等价、发布范围、Debug Companion | Phase 3 |
| sphra | 外部签名系统与发行流程 | 请求/响应/主体不匹配 | Phase 3 |
| praxe | 用户、CI、审计 | 装载、能力、预算、漂移、证据与升级 | Phase 4，独立进程 |

通用 transform、archive、strip、符号程序、预算程序、数据程序、训练程序、评估程序和量化程序不再作为独立应用承诺。相应职责进入有语义约束的子命令、测试模块或外部成熟工具适配器。

## 内容与成熟度规则

- “已接受”只能用于 ADR 已冻结的术语、边界和不变量。
- “待验证设计”用于尚无实现或实验的机制；“尚待确定”用于没有唯一候选；“后续计划”不得承诺日期。
- 历史术语只允许出现在被替代的 ADR 中；正文、路由、导航、样式 ID 与测试都使用当前词汇。
- Noemion 始终承担项目、新领域与社区总名；Endem 只承担最小制品、对应规范、生命周期、应用和 CLI 职责，不得替代项目名。
- 哲学来源只提出问题和反例；工程正文使用 Endem 与直白动作，不让来源术语决定 ABI。
- 所有对象输入、模型输出、远端协议描述和工具返回均视为不可信。

## 路由质量基线

- `sitemap.md` 是正式路由注册表；测试不得把某个固定数量当作产品不变量。
- 当前稳定家族为门户、about、architecture、specifications、components、endem、docs、development、downloads、faq 与 news。
- 旧应用和旧制品路由没有重定向、别名或隐藏导航入口。
- 每条手册路由由 `_data/manuals.yml` 登记，并由共享布局生成目录、面包屑和上下页。
- 源码测试和 `_site` 成品测试都必须通过；外链状态与内部链接状态分别报告。

## 公共页面结构审计 · 2026-07-12

以下 33 个 HTML 源文件已逐个阅读；检查范围包括页面职责、现行术语、历史标记、链接关系、共享布局、移动目录与可访问性。Markdown 生成的手册页面另由路由测试和构建产物审计覆盖。

| 文件 | 审计角色 | 结论 |
| --- | --- | --- |
| `_includes/docs-rail.html` | 服务端手册目录 | 通过 |
| `_includes/project-timeline.html` | 阶段时间线 | 通过 |
| `_includes/site-footer.html` | 全站页脚 | 通过 |
| `_includes/site-header.html` | 全站页头与目录容器 | 通过 |
| `_layouts/default.html` | 通用页面外壳 | 通过 |
| `_layouts/manual.html` | 手册页面外壳 | 通过 |
| `index.html` | 项目门户与六语义面总览 | 通过 |
| `about/index.html` | 项目背景入口 | 通过 |
| `about/background.html` | 问题与工程边界 | 通过 |
| `about/intellectual-foundations.html` | 哲学来源与采用界线 | 通过 |
| `architecture/index.html` | 架构总览 | 通过 |
| `architecture/endem-lifecycle.html` | Endem 生命周期 | 通过 |
| `architecture/decisions.html` | 决策权威顺序 | 通过 |
| `architecture/adr-0008-endem-system.html` | 已取代的历史决定 | 通过，显式标记 Superseded |
| `architecture/adr-0009-propositional-kernel.html` | 已取代的历史语义 | 通过，显式标记 Superseded |
| `architecture/adr-0010-native-lexicon.html` | 现行词汇与事态模型 | 通过 |
| `architecture/open-questions.html` | 未冻结问题 | 通过 |
| `specifications/index.html` | 规范入口 | 通过 |
| `specifications/endem.html` | 六语义面与最小制品 | 通过 |
| `specifications/synem.html` | 多 Endem 组合闭包 | 通过 |
| `specifications/tekmor.html` | phain 与有范围证据 | 通过 |
| `components/index.html` | 三实现域入口 | 通过 |
| `components/poiet.html` | 确定性生产域 | 通过 |
| `components/theor.html` | 独立只读解释域 | 通过 |
| `components/praxor.html` | 隔离实现域 | 通过 |
| `endem/index.html` | 唯一公开应用 | 通过 |
| `development/index.html` | 开发入口 | 通过 |
| `development/current-stage.html` | 当前阶段与证据要求 | 通过 |
| `development/implementation-roadmap.html` | 分阶段实施路线 | 通过 |
| `development/testing.html` | 验证体系 | 通过 |
| `downloads/index.html` | 真实可用性 | 通过 |
| `faq/index.html` | 关键概念答疑 | 通过 |
| `news/index.html` | 可核验进展 | 通过 |

## 全站逐页可读性复核 · 2026-07-13

本轮逐一复核 `sitemap.md` 登记的 40 条正式 HTML 路由，包括 27 个 HTML 正文源和 13 个由 Markdown 生成的页面。复核重点不是统一文风，而是让每种页面先完成自己的读者任务：门户给出项目定义，目录给出选择依据，专题给出结论与边界，应用给出状态与输入输出，手册给出连续操作逻辑。

| 页面家族 | 已逐页复核的正式路由 | 本轮处理 |
| --- | --- | --- |
| 门户（1） | `/index.html` | 保持 Noemion 为项目主语；把控制平面和下一步入口改为无需内部术语即可理解的表达。 |
| 项目背景（3） | `/about/index.html`、`/about/background.html`、`/about/intellectual-foundations.html` | 把核心问题拆成形成、组合、实现、验收四步；集中加入《逻辑哲学论》五条短引文，并逐条说明工程启发与不采用部分。 |
| 架构与 ADR（7） | `/architecture/index.html`、`/architecture/endem-lifecycle.html`、`/architecture/decisions.html`、`/architecture/adr-0008-endem-system.html`、`/architecture/adr-0009-propositional-kernel.html`、`/architecture/adr-0010-native-lexicon.html`、`/architecture/open-questions.html` | 生命周期先解释每阶段回答什么；历史 ADR 首屏标明怎样阅读和哪些名称已经失效；开放问题改用直白问题与发布条件。 |
| 组件（4） | `/components/index.html`、`/components/poiet.html`、`/components/theor.html`、`/components/praxor.html` | 首段先解释三个组件为什么不能合并；把 Writer、Parser、Policy、Handle、Request 等名称改为中文职责，保留必要接口标识。 |
| 规范（4） | `/specifications/index.html`、`/specifications/endem.html`、`/specifications/synem.html`、`/specifications/tekmor.html` | 先给直白定义，再给六语义面和规范词；把“Tekmor 能证明什么”改为“能支持什么判断”，避免把证据完整性误写成事实为真。 |
| 跨项目指南（7） | `/docs/index.html`、`/docs/getting-started.html`、`/docs/installation-and-usage.html`、`/docs/architecture-guide.html`、`/docs/development-guide.html`、`/docs/endem-reference.html`、`/docs/specifications-reference.html` | 删除未冻结却看似可执行的 `.weave` 命令示例；统一用中文解释候选、控制平面、验证句柄、签名材料和最终决定。 |
| Endem 应用与手册（7） | `/endem/index.html`、`/endem/docs/index.html`、`/endem/docs/format.html`、`/endem/docs/binding.html`、`/endem/docs/safety.html`、`/endem/docs/running.html`、`/endem/docs/reference.html` | 应用页先说明唯一入口解决什么问题；手册按来源、形成、组合、独立读取、发布和受控实现展开，移除未解释的 Rhem Source、Profile、Manifest 等表达。 |
| 开发（4） | `/development/index.html`、`/development/current-stage.html`、`/development/implementation-roadmap.html`、`/development/testing.html` | 阶段名称、验证条件和停止条件全部改为用户可读表达；明确当前仍在规范设计，尚未开始核心实现。 |
| 资源与支持（3） | `/downloads/index.html`、`/faq/index.html`、`/news/index.html` | 下载页直说为什么不能发布；FAQ 拆开 Synem、Dromen、Tekmor 定义；项目动态只陈述可核对进展。 |

本轮同时加入自动回归规则：现行页面不得出现 `.weave`、Rhem Source、SAY → DONE、未解释的 Harness/Acceptance Decision/Verified Handle 等历史或内部表达；普通段落中的单句不得超过 70 个汉字；思想基础页必须保留经核对的作者、译者、书名、命题编号、短引文和“不直接决定软件规范”的采用边界。

## 重新审计条件

- 新增正式制品、子命令、进程或仓库。
- 冻结编码、ABI、扩展 registry 或签名 profile。
- 第一次发布 Endem Poiet、Theor、Praxor 或规范版本。
- 接入模型、MCP/A2A、远端能力或外部签名服务。
- 页面不再能明确区分候选、决定和证据，或路由开始为历史兼容而膨胀。
