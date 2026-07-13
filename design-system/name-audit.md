# Noemion 与 Endem 名称冲突筛查

证据时间：2026-07-13T20:33:09+08:00
工程责任：首次发行负责人
法律责任：目标法域的合格知识产权专业人员
状态：开发阶段工程初筛；ADR-0031 与 ADR-0032 已接受直接迁移；不是法律意见

## 先给结论

- `Noemion` 可以继续作为项目、新领域与社区的候选品牌。当前精确查询没有发现同名软件包、GNU 包或 IANA 媒体类型；GitHub 上的精确组织名和仓库名属于本项目。正式商标检索仍未完成。
- `Endem`、`endem` 与 `.endem` 可以继续用于内部规范和开发，但不能再写成“没有强冲突”。三个第三方 GitHub 仓库和一个 GitHub 用户使用精确名 `endem`，`endem.com` 也已登记。
- 旧执行域名 Praxor 与旧证据对象名 Tekmor 已触发项目自己的停止条件。前者被多个活跃软件、人工智能和大模型研究主体使用；后者被相邻的可证明身份、零知识证明、TEE 与 attestation 项目使用。
- ADR-0031 已采用 `Drasor`、`drase` 与 `Iknem`。它们在本轮没有发现活跃的相邻 AI、执行、证明、协议或开发工具同名项目，但正式商标和权利复核仍未完成。
- 旧组件名 `Poiet` 与公开动作 `poie` 必须共同退出。`POIE` 已被 PFA Open Inference Engine 用于预测与分析模型评分，大小写不能形成可靠工程区分；ADR-0032 已采用 `Ktisor` 与 `ktise`。
- `TXT-CORE` 容易被读成 `.txt` 文件或原始文本文件，已触发实际对象边界误解。ADR-0033 采用 `TEXT-IDENTIFIER-CORE`；它是标准 ID，不是新文件格式、制品或组件名。
- `Synem`、`Dromen` 与 `Theor` 存在大小写无关或近似的软件与应用使用，目前记录为发现混淆；尚未达到必须立即更名的程度。
- PyPI、npm 与 crates.io 的 `endem` 精确包名在本次查询时均返回 404，Homebrew、Arch Linux、Fedora 和 Debian 也没有精确同名包。这个结果只说明查询时没有精确登记，不构成包名保留。
- 当前工程结论不再是统一的中等风险。Endem 保持中等风险；旧名称的高风险已经通过直接替换处理；Drasor、drase、Iknem、Ktisor 与 ktise 只通过开发阶段初筛，首次正式发行仍由法律和实际包名取得门禁阻断。

## 筛查对象与判定方法

发布面名称包括：

```text
Noemion
Endem
endem
.endem
```

内部领域词包括：

```text
rhem semion skena telis krin apor
Synem Dromen Iknem
Ktisor Theor Drasor
ktise elenk pleko tasse sphra theor drase peira
```

本轮把结果分成三类：

1. **精确工程冲突**：包、命令、仓库、媒体类型或标准使用相同名称。
2. **发现混淆**：名称属于不同领域，却会占据搜索结果、账户或主要域名。
3. **法律冲突**：目标法域、商品或服务类别中的相同及近似商标。只有正式数据库检索和专业复核能判断这一项。

搜索结果为空只能降低工程混淆，不能证明名称可注册、可独占或未来仍可取得。

## 可自动复查的精确查询

### 软件包与系统目录

| 名称 | 查询入口与查询式 | 2026-07-13 观察 | 结论边界 |
| --- | --- | --- | --- |
| `endem` | [PyPI JSON API](https://pypi.org/pypi/endem/json) | HTTP 404 | 当时没有精确项目；不是保留 |
| `endem` | [npm Registry](https://registry.npmjs.org/endem) | HTTP 404 | 当时没有精确包；不是保留 |
| `endem` | [crates.io API](https://crates.io/api/v1/crates/endem) | HTTP 404 | 当时没有精确 crate；不是保留 |
| `noemion` | [PyPI JSON API](https://pypi.org/pypi/noemion/json)、[npm Registry](https://registry.npmjs.org/noemion)、[crates.io API](https://crates.io/api/v1/crates/noemion) | 三项均为 HTTP 404 | 当时没有精确包；不是保留 |
| `ktise` | [PyPI 简单索引](https://pypi.org/simple/ktise/)、[npm Registry](https://registry.npmjs.org/ktise)、[crates.io API](https://crates.io/api/v1/crates/ktise) | 分别为 HTTP 404、Not found、crate does not exist | 当时没有精确包；不是保留 |
| `ktisor` | [PyPI 简单索引](https://pypi.org/simple/ktisor/)、[npm Registry](https://registry.npmjs.org/ktisor)、[crates.io API](https://crates.io/api/v1/crates/ktisor) | 分别为 HTTP 404、Not found、crate does not exist | 当时没有精确包；不是保留 |
| `text-identifier-core` | [PyPI JSON API](https://pypi.org/pypi/text-identifier-core/json)、[npm Registry](https://registry.npmjs.org/text-identifier-core)、[crates.io API](https://crates.io/api/v1/crates/text-identifier-core) | 三项均返回精确项目不存在 | 标准 ID 不等于未来软件包名；结果也不是保留 |
| `endem` | `brew search '/^endem$/'` | 没有 formula 或 cask | 只覆盖本次 Homebrew 索引 |
| `endem` | [Debian 名称查询](https://packages.debian.org/search?keywords=endem&searchon=names&suite=all&section=all) | 仅返回包含该字串的 `sendemail`，没有精确包 | Debian 查询是包含匹配，必须人工排除假阳性 |
| `endem` | [Arch Linux 精确名称 API](https://archlinux.org/packages/search/json/?name=endem) | `results=0` | 只覆盖官方包查询 |
| `endem` | [Fedora 精确包入口](https://packages.fedoraproject.org/pkgs/endem/) | HTTP 404 | 只说明精确入口不存在 |
| 两个名称 | [GNU 当前与退役软件包目录](https://www.gnu.org/software/software.html) | `endem` 与 `noemion` 均无精确文本 | 不代表全部自由软件生态 |
| 两个名称 | [IANA 媒体类型登记表](https://www.iana.org/assignments/media-types/media-types.xhtml) | 均无精确文本 | `.endem` 尚无正式媒体类型；不得据此自行宣称已登记 |
| 两个命令 | 本机执行 `command -v endem` 与 `command -v noemion` | 均未找到 | 只覆盖本次 macOS 环境，不代表其他系统 |

初轮曾对当时的内部词执行 PyPI、npm 与 crates.io 精确 API 查询。ADR-0031 之后的 Iknem、Drasor 与 <code>drase</code> 属于新选择，只完成了当前记录的索引和产品初筛；正式发行前必须重新执行三类注册表的精确查询并实际取得所需坐标。搜索为空不能替代取得、近音检索或商标复核。

### GitHub 精确名候选

查询式：

- [仓库名称包含 `endem`](https://api.github.com/search/repositories?q=endem+in%3Aname&per_page=100)，遍历当时返回的六页结果，再以大小写无关的精确仓库名过滤。
- [用户登录名包含 `endem`](https://api.github.com/search/users?q=endem+in%3Alogin&per_page=100)，遍历当时返回的三页结果，再以大小写无关的精确登录名过滤。
- [仓库名称包含 `noemion`](https://api.github.com/search/repositories?q=noemion+in%3Aname&per_page=100)，再以大小写无关的精确仓库名过滤。

| 精确对象 | 最后推送或更新 | 当前用途 | 风险判断 |
| --- | --- | --- | --- |
| [`shivangx/Endem`](https://github.com/shivangx/Endem) | 2023-12-14 | JavaScript/React 项目，没有清晰产品定义 | 同名软件仓库；相邻性低，但会造成发现混淆 |
| [`parmarjh/endem`](https://github.com/parmarjh/endem) | 2025-06-04 | EcoSense 环境监测说明与网页材料 | 同名技术项目；领域不同，但仍是有效搜索冲突 |
| [`klu2200031072/endem`](https://github.com/klu2200031072/endem) | 2024-12-07 | 仅公开 `endem.zip` | 内容不足以判断权利或产品状态，不能忽略 |
| [`github.com/endem`](https://github.com/endem) | 2016-02-27 更新；无公开仓库 | 第三方个人账户 | 精确登录名已被占用；Noemion 不能取得该全局账户名 |
| [`Noemion/Noemion`](https://github.com/Noemion/Noemion) | 2026-07-12 推送 | 本项目组织简介仓库 | 属于本项目，不是第三方冲突 |

GitHub 允许不同账户使用相同仓库名，因此第三方 `endem` 仓库不会阻止创建 `Noemion/endem`。它们仍然证明 `Endem` 不是全网唯一名称，公开说明、仓库描述和软件包元数据必须始终先写清 Noemion 项目与自然语言目标工程职责。

## 第二轮产品与相邻领域检索

第二轮不只查询包名，而是检查公开产品、人工智能系统、开发工具和证明技术中的精确或大小写无关使用。结果用于判断工程发现与语义相邻性，不代替商标数据库。

| 名称 | 2026-07-13 可核对使用 | 相邻性 | 当前风险 |
| --- | --- | --- | --- |
| 旧名 Praxor | [Praxor Lab](https://praxorlab.com/)研究 LLM 解释性、推理、适配和强化学习，并开发训练基础设施；[Praxor.ai](https://www.praxor.ai/)提供 Agentic AI 系统；[praxor.dev](https://www.praxor.dev/)提供软件工程与开发工具服务 | 与 Noemion 的受限执行域处在同一 AI 与软件工程发现空间 | 高；已经退役 |
| 旧名 Tekmor | [tekmor.xyz](https://www.tekmor.xyz/)以同名提供隐私 KYC、零知识证明、TEE、确定性构建、链上登记和 attestation | 与 Noemion 的证据、完整性、验证、证明和信任链直接重叠 | 高；已经退役 |
| 旧名 Poiet / <code>poie</code> | [PFA Open Inference Engine](https://github.com/datamininggroup/POIE)使用大小写无关的精确动作拼写，公开说明其参考实现用于执行预测与分析模型评分 | 与 Noemion 的人工智能工程和模型处理发现空间直接重叠；旧组件词族也会延续混淆 | 高；已经退役 |
| `Synem` | [SynEM](https://elifesciences.org/articles/26414)是有论文与公开代码的自动突触检测机器学习方法 | 大小写无关时精确，属于 ML 软件，但对象和消费者不同 | 中；继续观察 |
| `Dromen` | [Dromen, Inc.](https://www.dromeninc.com/about/)运营服务与移动应用；应用商店也存在使用该词的 AI 梦境产品 | 精确公司与软件使用，领域不同 | 中低；记录发现混淆 |
| `Theor` | [THEOR-E](https://theor-e.com/)正在建设 AI 心理健康平台，另有使用 Theor 的软件与教育服务记录 | 近似软件品牌，职责不同 | 中低；继续观察 |
| `Ktisor` | 本轮没有找到可信度足以进入相邻冲突表的精确 AI 或开发工具产品 | 搜索为空不是权利或未来可用证明 | 未证实低风险；继续复查 |
| `ktise` | 本轮没有找到精确的活跃 AI、编译、构建或开发工具产品；主要语言包索引也没有精确登记 | 动作仍需单独于组件名持续复查 | 未证实低风险；继续复查 |
| `TXT-CORE` | 与 `.txt` 文件扩展名形成直接视觉关联，实际读者已询问它是否就是原始文件层 | 标准实际治理文本槽、结构标识符、显示和模型输入，误读会混淆对象与来源身份 | 高；已经退役 |
| `TEXT-CORE` | [Interedition Text Core](https://mvnrepository.com/artifact/eu.interedition/text-core) 已使用精确名称处理范围标注文本模型 | 同名且职责相邻，并继续暗示通用文本文件核心 | 高；拒绝 |
| `TIB-CORE` | [SemEval-2025 LLMs4Subjects](https://aclanthology.org/2025.semeval-1.328/)使用 `tib-core` 数据集训练和评估技术文献主题标注 | 与文本和人工智能发现空间相邻 | 高；拒绝 |
| `TEXT-IDENTIFIER-CORE` | GitHub 精确仓库名为零；PyPI、npm 与 crates.io 没有精确项目；GNU 软件目录没有精确文本 | 完整列出两个治理对象，不伪装成文件格式或工程品牌 | 采用；标准 ID 仍需持续复查 |

搜索引擎结果可能遗漏未收录、地区限制、未公开或新发布对象。这里的“高风险”只表示工程命名和发现门禁已经失败，不表示对外部主体的权利、有效性或优先顺序作出法律判断。

### 替代名称初筛

| 候选 | 观察 | 决定边界 |
| --- | --- | --- |
| `Iknem` | 没有发现精确的活跃 AI、证明、协议或开发工具；可见结果主要是课程缩写、航空航路点和零散人名 | 采用；搜索为空不是权利结论 |
| `Vekem` | 与面向 AI Agent 的记忆软件 `vemem` 仅差一个字母 | 拒绝，发现区分度不足 |
| `Pistem` | 与 PiSTEM 教育组织及使用 AI 的能源模型透明度项目发生拆词和大小写混淆 | 拒绝 |
| `Drasor` / `drase` | 没有发现精确的活跃 AI、Agent、运行时或开发工具；可见结果属于酶缩写、房地产主体、音乐和早期 FORTRAN 子程序 | 采用；仍需正式复核 |
| `Dranor` / `dran` | `dran` 已是活跃 PyPI 科学软件名，DRAN 也用于生成式 AI 研究 | 拒绝 |
| `Drast` | 已有同名 AI 销售自动化产品 | 拒绝 |
| `Ktisor` / `ktise` | 没有发现精确相邻产品、GitHub 仓库名或主要语言包；组件与动作关系清楚 | 采用；仍需正式复核 |
| `Teukor` / `teuke` | 精确软件冲突较少，但 Teuke 已作为姓氏和人名稳定使用，搜索区分度较弱 | 拒绝 |

## 域名与社区入口

| 对象 | 2026-07-13 观察 | 处理 |
| --- | --- | --- |
| `endem.com` | Verisign RDAP 返回已登记，权威名称服务器指向停放服务 | 视为不可依赖，不把 `.com` 可取得性作为采用前提 |
| `noemion.com` | Verisign RDAP 当时未返回登记对象 | 结果随时会变；未完成实际注册前不得称为已取得 |
| `endem.org`、`endem.dev`、`noemion.org`、`noemion.dev` | 对应注册局 RDAP 当时未返回登记对象 | 只记录时间点，不构成保留或法律结论 |
| GitHub `endem` 用户名 | 已被第三方占用 | 统一使用 `Noemion` 组织，不建立局部工程名品牌账户 |

域名是否可取得不会决定对象格式、命令或 ABI。域名已占用也不自动构成商标冲突；域名空缺更不证明名称安全。

## 语言关键字与旧词淘汰

当前词在 C、C++、Rust、Go、Python、Java、ECMAScript、Swift 与 Kotlin 的关键字集合中没有精确冲突。权威入口包括 [Rust 关键字](https://doc.rust-lang.org/stable/reference/keywords.html)、[Go 关键字](https://go.dev/ref/spec#Keywords)、[Python 关键字](https://docs.python.org/3/reference/lexical_analysis.html#keywords)、[Java 关键字](https://docs.oracle.com/javase/specs/jls/se26/html/jls-3.html#jls-3.9)、[ECMAScript 保留字](https://tc39.es/ecma262/#sec-keywords-and-reserved-words)、[Swift 词法结构](https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html)与 [Kotlin 关键字](https://kotlinlang.org/docs/keyword-reference.html)。

`case`、`open` 与 `when` 明确与主流语言关键字冲突，已经退出现行接口。`say`、`mean`、`seek`、`keep`、`avoid` 以及 Core、Reader、Runner、Frame、Witness 虽不全是关键字，但过于通用，也已经退出。历史 ADR 可以记录它们，现行格式、命令和页面不得重新引入。

## 当前采用决定

| 对象 | 当前决定 | 首次发行前必须满足 |
| --- | --- | --- |
| `Noemion` | 继续作为候选品牌 | 完成目标法域商标、近音、翻译和软件类别复核 |
| `Endem` | 继续作为最小目标制品名 | 没有相邻开发工具、AI 产品、协议或格式的阻断性近似权利 |
| `endem` | 继续作为内部 CLI 名 | 取得实际发行包名；验证 Windows、macOS、GNU/Linux 命令路径；完成混淆测试 |
| `.endem` | 继续作为实验扩展名 | 在格式冻结前决定媒体类型、桌面关联与安全处理；不得提前宣称 IANA 登记 |
| `Drasor` / `drase` | 采用为受限执行域与对应动作 | 正式发行前重查工程生态并完成专业权利复核；取得实际分发坐标 |
| `Iknem` | 采用为有范围证据记录，标准为 IKN-CORE | 正式发行前重查工程生态并完成专业权利复核；不得把名称当作真实性或充分性声明 |
| `Ktisor` / `ktise` | 采用为确定性制作组件与对应动作 | 正式发行前重查大小写、近音、AI 产品、开发工具、命令和包坐标；取得实际分发坐标 |
| `TEXT-IDENTIFIER-CORE` | 采用为跨制品文本与标识符标准 ID，条款使用 `TEXT-*` | 保持它与 `.txt`、原始来源文件和未来组件名分离；规范职责变化时重审名称 |
| `Synem / Dromen / Theor` | 保持现行设计名并继续监测 | 正式发行前更新精确、近音、产品和商标检索，不得称为全网唯一 |
| npm 分发坐标 | 若未来需要 npm，优先评估 `@noemion/endem` | 作用域只是分发定位，不改变 `endem` 命令、格式名或 ABI |
| crates.io 分发坐标 | 当前仅保留 `endem` 候选 | 发布前再次查询并实际取得；crates.io 没有作用域命名空间 |

公共页面继续以 Noemion 说明项目身份，以 Endem 说明局部制品。为了搜索唯一性而把 Noemion 前缀塞回命令、格式、字段或组件，会破坏已经确立的品牌与工程边界，因此不是本轮解决方案。

## 正式商标门禁仍未完成

本轮没有对商标权作出否定或肯定结论。首次可安装发行前，发行负责人必须保存正式报告，至少完成：

1. 在 [WIPO Global Brand Database](https://www.wipo.int/en/web/global-brand-database)、[中国国家知识产权局商标网上查询](https://wcjs.sbj.cnipa.gov.cn/)和实际发行地区的官方数据库中检索 `Noemion`、`Endem`、大小写变体、近音、拆词和视觉近似。
2. 让合格专业人员确认适用商品与服务类别；软件、可下载开发工具、SaaS、研究与技术服务常涉及不同类别，不能由项目自行猜定。
3. 保存查询日期、数据库、查询式、命中记录、权利状态、类别、地域、相似理由、负责人和复核结论。
4. 对仍有效且接近人工智能、开发工具、编译/链接、文件格式、自动化或软件服务的候选逐项判断混淆风险。
5. 在包名、仓库、域名和社区入口实际取得后再发布安装说明；查询为空不能代替取得。

## 必须停止或改名的条件

出现以下任一情况时，项目不得靠文案消解，必须暂停正式发行并创建新的命名 ADR：

- 相同或近似名称已用于活跃的人工智能产品、开发工具、编程语言、对象格式、协议或标准。
- 目标法域存在有效且覆盖相邻商品或服务的相同或近似权利，专业复核认为可能混淆。
- 无法取得可维护的软件包身份，安装过程只能依赖误导性拼写、历史包接管或不受控下载入口。
- 用户测试持续把 Endem 误认成其他软件、把 Endem 当作项目总名，或无法区分 Noemion 与局部制品。
- 为保留名称必须改变格式语义、信任边界、权限模型或测试不变量。

若触发改名，名称变化不得静默改变六个语义面、对象身份、错误语义或 END-FMT 字节。新 ADR 必须分别处理品牌、制品、命令、扩展名和分发坐标。

旧名称已经触发第一项停止条件并退出当前接口。[ADR-0031](../architecture/adr-0031-release-name-collision-gate.html)记录 Iknem 与 Drasor/drase 的采用决定；[ADR-0032](../architecture/adr-0032-deterministic-maker-name-collision.html)记录 POIE 冲突、Ktisor/ktise 的采用决定和动作成熟度差异；[ADR-0033](../architecture/adr-0033-text-identifier-specification-name.html)记录文本与标识符标准 ID 的可读性问题、候选冲突和一次性迁移。三项迁移都不保留兼容入口。

## 词源边界

语言学后缀 `-eme` 只帮助解释“最小区别单位”的构词思路。古希腊词根也只帮助记忆。`rhem`、`semion`、`skena`、`telis`、`krin`、`apor`、Synem、Dromen、Iknem、Ktisor、Theor 与 Drasor 的含义始终由 ADR、数据结构、不变量和测试定义；词源不能替代工程规范。
