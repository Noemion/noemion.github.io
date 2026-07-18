---
layout: spec
title: "Noemion `goal_direction` 发行词研究 · Noemion"
page_role: "content"
footer_text: "Noemion · 规范源"
permalink: "/spec/goal_direction-release-terms-proposal.html"
summary: "保存目标方向名称的候选比较与反例，说明为什么当前采用 reach 与 maintain，并保留人类读音验证边界。"
document_status: "非规范研究提案"
---
# Noemion `goal_direction` 发行词研究

状态：非规范研究提案
日期：2026-07-14
结论状态：职责与桌面审查已由 ADR-0037 采用；人类读音仍待验证
适用范围：`goal_direction` 的两个目标方向、公开解释、END-DIRECTION-001、END-P2 与历史迁移

> 当前词表使用 `reach / maintain`。以下内容保留采用前的候选比较、反例与人类验证方案；现行定义与迁移范围以 [ADR-0037](../architecture/adr-0037-terminology-simplification.html) 为准。

本提案不构成 ADR、CORE 规范、内容 Profile、登记项或实现要求，不进入 `registry.json`。它不创建新语义面、结果域、命令、组件、文件格式、扩展名或兼容别名。ADR-0037 已一次性把旧枚举迁移为 `reach / maintain`，并同步 END-DIRECTION-001、Profile、向量、诊断和公开资料。

## 直接结论

`kine / mene` 不适合作为首次正式发行的拼写。这个结论不需要等待听测：它们已经未通过职责透明和首次阅读两个桌面门禁。

- [Cambridge Dictionary](https://dictionary.cambridge.org/us/pronunciation/english/kine)把英语 `kine` 读作 /kaɪn/；[Merriam-Webster](https://www.merriam-webster.com/dictionary/kine)把它登记为古旧的 `cow` 复数。现有英语词义与 Noemion 的目标方向无关。
- `mene` 没有给目标读者提供稳定的英语拼读线索。即使项目补写“官方读音”，也不能让首次读者从拼写推回“持续成立”的职责。
- [GNU Coding Standards 的 Names 规则](https://www.gnu.org/prep/standards/html_node/Names.html)要求名称提供有用的意义，并限制晦涩缩写。`kine / mene` 把解释成本转移给术语表，与该原则相反。
- 两个名称的语义职责仍然有效：一个方向要求事态达到成立，另一个方向要求事态持续成立。失败的是发行拼写，不是 `goal_direction` 分层，也不是 ADR-0016 的时间与连续性模型。

桌面审查支持采用 `reach / maintain`；两项拼写仍须进入人类验证：

- `reach` 表达“达到某个状态或水平”。[Cambridge Dictionary](https://dictionary.cambridge.org/us/dictionary/english/reach)登记 /riːtʃ/，并明确包含“达到特定水平”的常用义。
- `maintain` 表达“继续保持存在或不让其降低”。[Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/maintain)登记 /meɪnˈteɪn/，该义直接对应持续成立。
- 两词的首音、重音、音节数和结尾都明显不同，书写也不共享易误删的词干。这只降低预期混淆，不是人类证据。

ADR-0037 已修改 END-DIRECTION-001 与 END-P2，且没有增加别名。人类验证决定的是发行口头传播风险，不会恢复旧枚举。

## 语义先于拼写

候选词必须映射到已经存在的两个职责，不能借改名改变判断规则。

| 既有职责 | 必须保留的含义 | 不得偷带的含义 |
| --- | --- | --- |
| 迁移前 `kine` | 要求根 `situation` 达到成立；结果型目标在判断前已经成立时仍可按 `satisfaction_criteria` 得到 `met` | 本次一定执行了动作、发生了可证明转变、某主体造成结果 |
| 迁移前 `mene` | 要求根 `situation` 在具名时间范围和连续性政策下持续成立 | 稀疏采样等于连续覆盖、会话完成等于持续满足 |

因此，候选词只能帮助读者区分目标方向。它不能取代 `situation`、`satisfaction_criteria`、观察 `structured_observation`、evidence entry、满足结果或权威决定。

## 候选比较

桌面比较使用六项门禁：职责透明、英语词义、读音可预期、成对听辨风险、与现有工程概念的误导、是否需要新造词解释。桌面门禁只能排除明显不合格候选；不能代替人类实验。

| 候选对 | 优点 | 主要反例 | 桌面结论 |
| --- | --- | --- | --- |
| `kine / mene` | 短，外观成对 | `kine` 已有 /kaɪn/ 和无关词义；`mene` 读音不明；名称不说明职责 | 排除发行拼写；保留为迁移前规范值 |
| `make / keep` | 最短，中文容易直译 | `make` 会被读成 GNU Make 或制品构建动作；`keep` 也可能表示存储、所有权或不删除 | 排除；混淆目标方向与工具动作 |
| `attain / sustain` | 两词都接近所需语义 | 共享 /əˈteɪn/ 韵尾，弱信号下容易混听；`sustain` 还可表示支撑、承受 | 排除；口头成对风险过高 |
| `become / remain` | 直接描述状态变化与保持 | `become` 暗示必须观察到前态与转变，而结果型目标允许事态原本已成立 | 排除；会加强未获规范支持的转变语义 |
| `achieve / maintain` | 常用词，职责较透明，读音区别明显 | `achieve` 容易暗示行动者已经成功实现结果，可能把目标方向与动作或因果混合 | 次选；若首选在人类验证中失败再评估 |
| `reach / hold` | 简短，声音区别明显 | `hold` 多义，可能表示占有、暂停、锁定或一次瞬时状态 | 排除；持续性责任不够明确 |
| `reach / maintain` | 常用词；达到与保持的职责区分直接；/riːtʃ/ 与 /meɪnˈteɪn/ 差异明显 | `reach` 仍可能让读者误以为必须证明一次状态转变 | 首选人类验证候选；必须用“原本已成立”反例验证边界 |

不比较 PyPI、npm 或 crates.io 上的 `reach` 与 `maintain` 精确包名。这两个词是格式内的枚举候选，不是包、命令、组件或品牌；要求它们在全球软件注册表中唯一会把分发坐标门禁错误施加到普通语义值。未来若有人建议把它们提升为命令或组件名，必须重新执行独立名称审查。

## 支持案例与反例

| 场景 | 预期职责 | 候选词必须让读者理解什么 | 失败信号 |
| --- | --- | --- | --- |
| 服务原本不健康，之后达到健康 | 达到成立 | `reach` 指向期望终态 | 读者把它解释成某个具体修复动作 |
| 服务在会话开始前已经健康 | 达到成立 | 仍可按终态得到 `met`，不需要虚构转变 | 读者认为没有发生变化就必须 `unmet` |
| 服务必须整段窗口保持健康 | 持续成立 | `maintain` 需要范围与连续性证据 | 读者把一次采样当成持续满足 |
| 短暂健康后回退 | 持续成立 | 已证实违约产生 `unmet` | 读者只看最终采样或会话成功 |
| 工具成功但终态未成立 | 两种方向都不自动满足 | 动作结果与目标判断分开 | 候选词让读者把工具成功直接写成 `met` |
| 负目标要求关系不成立 | 方向与极性正交 | `reach / maintain` 不编码禁止力量 | 读者用第二套否定枚举替代 `skena.negative` |
| 观察覆盖不足 | 持续成立 | 结果是 `undetermined`，不是默认成功 | 读者把“未观察到失败”解释成保持成功 |
| 时钟或适配器违约 | 持续成立 | 结果是 `fault` | 读者把基础设施故障解释成目标 `unmet` |

## 人类验证方案

测试遵守 [ADR-0034](../architecture/adr-0034-pronunciation-and-oral-distinction.html)，但当前验证只比较 `reach / maintain` 与完整现行词表，不把 `kine / mene` 当作兼容选项。

### 发现阶段

在 `zh-CN` 与一个明确登记的英语变体中，分别由至少 24 名首次接触 Noemion 的参与者完成：

1. 看到 `goal_direction` 的直白职责和一个候选词，首次朗读并写下自然分词与重音。
2. 从“达到成立”“持续成立”“动作完成”“无法判断”中选择职责。
3. 阅读“事态原本已成立”“短暂成立后回退”“没有观察到失败”三个反例，说明候选是否诱导错误判断。
4. 在完整词表中指出最容易混淆的现行名称，并手写回填候选拼写。

发现阶段只寻找读法、误解和风险对，不产生通过结论。

### 发行门禁阶段

换用没有参加发现阶段的独立听者。每个目标语言、每个候选、每种音频条件至少收集 60 个首次判断。每次判断必须同时完成名称选择、手写拼写和职责匹配。

以下任一情况都使候选失败：

- 被误选为另一个现行名称或另一个 `goal_direction` 方向；
- 职责被匹配成动作发生、状态转变、因果归因或会话完成；
- 稳定出现无法从音频恢复的替代拼写；
- 在“原本已成立”反例中把 `reach` 错读为必须发生转变；
- 在连续性反例中把 `maintain` 错读为一次采样即可证明。

TTS、ASR 和语音模型可以补充发现异常转写，但不计入样本，也不能决定候选通过。

## 已执行的迁移范围

ADR-0037 已在同一变更中完成以下工作：

1. 修改 END-DIRECTION-001、END-CORE、END-P2 枚举和来源清单。
2. 修改语义与线格式正反向量、诊断目录、场景和资料一致性检查。
3. 修改公开页面、图示、手册、站点索引和项目路由说明。
4. 删除旧枚举的现行入口；旧词只保留在迁移 ADR、研究记录和名称审计中。
5. 不增加别名、双写、自动规范化、重定向或兼容读音。

若后续人类验证发现稳定混淆，项目应回到职责和反例重新选词，而不是增加隐藏纠错表或降低验证标准。

## 当前决定边界

当前可依赖三项结论：

1. 旧枚举未通过职责透明和首次阅读门槛，只保留为迁移证据。
2. `reach` 表示达到目标事态，`maintain` 表示在声明时间范围与连续性政策下保持目标事态；两者都不证明某个动作造成了状态变化。
3. `reach / maintain` 已是现行术语，但人类读音与听写验证仍未完成。

evidence entry、deterministic producer、Endem 与 Endem closure 的口头区分仍是独立验证问题，不能从这项桌面审查推导为通过。
