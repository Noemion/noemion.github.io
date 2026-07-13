# Noemion 与 Endem 名称冲突筛查

证据时间：2026-07-13T08:06:31+08:00
工程责任：首次发行负责人
法律责任：目标法域的合格知识产权专业人员
状态：开发阶段初筛；不是法律意见，不代表名称门禁已经通过

## 先给结论

- `Noemion` 可以继续作为项目、新领域与社区的候选品牌。当前精确查询没有发现同名软件包、GNU 包或 IANA 媒体类型；GitHub 上的精确组织名和仓库名属于本项目。正式商标检索仍未完成。
- `Endem`、`endem` 与 `.endem` 可以继续用于内部规范和开发，但不能再写成“没有强冲突”。三个第三方 GitHub 仓库和一个 GitHub 用户使用精确名 `endem`，`endem.com` 也已登记。
- PyPI、npm 与 crates.io 的 `endem` 精确包名在本次查询时均返回 404，Homebrew、Arch Linux、Fedora 和 Debian 也没有精确同名包。这个结果只说明查询时没有精确登记，不构成包名保留。
- 当前工程结论是中等风险：名称的语义辨识度仍然足够，但公开检索和仓库发现会遇到同名对象。第一次可安装发行前必须完成目标法域商标检索、近音检索、软件类别复核和包名取得；任一项出现相邻领域强冲突时，立即启动新命名 ADR。

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
Synem Dromen Tekmor
Poiet Theor Praxor
poie elenk pleko tasse sphra theor praxe peira
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
| `endem` | `brew search '/^endem$/'` | 没有 formula 或 cask | 只覆盖本次 Homebrew 索引 |
| `endem` | [Debian 名称查询](https://packages.debian.org/search?keywords=endem&searchon=names&suite=all&section=all) | 仅返回包含该字串的 `sendemail`，没有精确包 | Debian 查询是包含匹配，必须人工排除假阳性 |
| `endem` | [Arch Linux 精确名称 API](https://archlinux.org/packages/search/json/?name=endem) | `results=0` | 只覆盖官方包查询 |
| `endem` | [Fedora 精确包入口](https://packages.fedoraproject.org/pkgs/endem/) | HTTP 404 | 只说明精确入口不存在 |
| 两个名称 | [GNU 当前与退役软件包目录](https://www.gnu.org/software/software.html) | `endem` 与 `noemion` 均无精确文本 | 不代表全部自由软件生态 |
| 两个名称 | [IANA 媒体类型登记表](https://www.iana.org/assignments/media-types/media-types.xhtml) | 均无精确文本 | `.endem` 尚无正式媒体类型；不得据此自行宣称已登记 |
| 两个命令 | 本机执行 `command -v endem` 与 `command -v noemion` | 均未找到 | 只覆盖本次 macOS 环境，不代表其他系统 |

同一时间对全部现行内部领域词执行 PyPI、npm 与 crates.io 精确 API 查询，均返回 404。这说明当前词组没有直接的软件包占位，但不能替代大小写、近音、仓库、产品和商标检索。

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

## 词源边界

语言学后缀 `-eme` 只帮助解释“最小区别单位”的构词思路。古希腊词根也只帮助记忆。`rhem`、`semion`、`skena`、`telis`、`krin`、`apor`、Synem、Dromen、Tekmor、Poiet、Theor 与 Praxor 的含义始终由 ADR、数据结构、不变量和测试定义；词源不能替代工程规范。
