# Noemion 生命周期与结果词边界研究提案

状态：非规范研究提案  
日期：2026-07-14  
结论状态：对象边界桌面审查完成；语义迁移与发行命名分别等待决定

适用范围：Endem 形成阶段、外部签名与证明关系、满足结果、形成失败、会话终止、证据有效性与覆盖度

本提案不构成 ADR、CORE 规范、内容 Profile、登记项、迁移决定或实现要求，不进入 `registry.json`。它不修改现行 `nascent / coherent / attested`、`met / unmet / agno / fault`、`aseme`、`accepted / rejected / deferred`、`completed / failed / interrupted`、`valid / invalid / revoked`、`sufficient / insufficient`，也不提前改写 Dromen 提案向量中的 `subject.attested`。候选词不是别名、兼容值或规范化结果。

## 直接结论

现行五个结果域的分离方向正确，但“制品生命周期”把三种不同事实塞进了一条状态链：

1. Endem 内容已经确定性形成；
2. 内容内部的投影、引用、冲突、能力上限与判断关系已经解决；
3. 某个外部签名陈述或证明结果在特定政策与截止点下绑定到精确内容。

前两项是内容形成分类；第三项是内容与外部陈述之间的多值、可撤销、依赖政策的关系。第三项不能成为精确内容自身的单值终态。因此本提案建议：

- 停止把 `attested` 作为 Endem 生命周期状态；
- 把现行 `nascent / coherent` 同 `formed / resolved` 比较，但始终写成 `content state: formed` 与 `content state: resolved`，避免把“目标已形成”误听成“目标已完成”；
- 用显式的 signed-statement binding（已签陈述绑定）或适用 attestation relation（证明关系）表达外部伴随事实，不增加第三个内容状态；
- Dromen 建立条件未来应读取“精确 resolved 内容 + 精确外部陈述 + 验证政策 + 截止点 + 撤销状态”，不能读取 `attested=true`；
- 保留 `met / unmet / fault` 进入人类验证，以 `undetermined` 比较 `agno`；
- 以 `no_allowed_projection` 比较 `aseme`，继续用此前提案的 `unresolved_meaning` 比较 `apor`；
- 暂时保留清楚的权威决定和证据状态值，但公开表达必须带结果域名称；
- 把会话终止的 `interrupted` 同 `stopped` 比较，因为 Dromen 不可恢复，而日常语义中的 interrupted 常暗示稍后继续。

这些只是候选方向。现行规范、向量与页面在用户决定、人类验证和迁移 ADR 完成前继续使用当前值。

## 两条迁移轴必须分开

对象边界修正和发行词替换不能绑成一个决定。前者回答“哪一类事实属于精确内容”，后者回答“人类与机器以后使用什么名称”。两条轴的证据与失败条件不同：

| 迁移轴 | 修正范围 | 当前证据 | 进入规范前还缺什么 |
| --- | --- | --- | --- |
| A · 对象边界 | 从内容形成分类移除 `attested`，把外部陈述、验证结果和依赖方判断显式分开 | ID-CORE 的不可变身份边界、RFC 9334 的角色与消息分层、in-toto 多签包络，以及多政策、撤销和截止点反例 | 用户接受边界方向；形成迁移 ADR；同步 END-CORE、DRO-CORE、登记、威胁、场景和向量 |
| B · 发行命名 | 比较 `nascent/coherent` 与 `formed/resolved`，并审查其他结果词 | GNU 名称可读性原则、桌面职责审查和读音风险清单 | 两批独立人类职责匹配、朗读、听写和成对混淆证据；形成单独命名迁移结论 |

A 轴不引入 `formed`、`resolved` 或其他候选词。若它先获接受，现行 `nascent/coherent` 可以暂时继续表示两项内容形成分类，`attested` 则退出内容状态；这样不让未经验证的新名字拖延对象边界修正。B 轴以后若获证据支持，再按新规范身份一次性替换名称，不建立别名或双写。

反过来，读音流畅也不能提前通过 A 轴。即使参与者都能顺利朗读 `attested`，它仍无法表示一份内容关联多个签名、验证政策、截止点和撤销结果的事实结构。

## 发现的对象边界错误

### 精确内容不会在原身份内“演进”

ID-CORE 已规定：内容身份绑定精确规范输入与字节；变换、裁剪、迁移和派生结果各有自己的身份。由 nascent 内容形成 coherent 内容时，只要规范内容发生变化，就产生新的精确对象与显式派生关系，而不是同一个身份原地改变。

[W3C SCXML](https://www.w3.org/TR/scxml/)把状态定义为状态机当前进入且尚未退出的配置，并以 transition 改变活动状态。Noemion 的精确内容对象却是不可变值；“生命周期转移”在这里容易掩盖新身份与派生边。面向读者的流程图可以继续显示形成顺序，但规范不能把顺序图当成同一对象的可变状态机。

候选模型因此分成两层：

| 层 | 回答的问题 | 候选表达 | 身份后果 |
| --- | --- | --- | --- |
| 内容形成分类 | 这份精确内容内部还保留哪些形成责任？ | `content state: formed / resolved` | 内容变化产生新身份和派生关系 |
| 外部伴随关系 | 哪个外部陈述在什么政策与截止点下绑定这份内容？ | signed-statement binding / attestation relation | 不改变内容身份；关系本身有独立身份、验证和有效期 |

### `attested` 不是签名存在的同义词

[RFC 9334 RATS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html)分开 Attester 产生的 Evidence、Verifier 按评估政策形成的 Attestation Results，以及 Relying Party 对结果的后续使用。Attestation Result 是验证者评估的产物，不是“某段载荷附有一个签名”的布尔别名。

[in-toto Attestation Framework 的 Envelope 规范](https://github.com/in-toto/attestation/blob/main/spec/v1/envelope.md)把包络定义为处理序列化和数字签名的最外层，并要求能够包含多个签名。一个精确载荷可以同时关联多个签名、签名者、包络和验证结果；同一签名也会随参考值、撤销状态、政策和截止点产生不同适用结论。

因此现行 `attested` 至少混合了四件事：

1. 载荷是否冻结；
2. 签名响应是否逐字节绑定该载荷；
3. 签名或证明是否在指定政策与截止点下验证通过；
4. 当前依赖方是否允许该对象进入会话。

把它们压成 `subject.attested: true` 会丢失签名数量、陈述类型、验证者、政策、截止点、撤销与依赖方。更危险的是，布尔值看起来像制品能够自证，违反现行 ID-CORE、IKN-CORE、AUT-CORE 与 Dromen 的外部重验证边界。

### Dromen 主体准入需要显式关系集

未来的 Dromen 主体准入不能读取内容中的 `attested` 标志，也不能把“存在签名”缩写成“允许运行”。下面是职责模型，不是字段名、schema、Profile 或兼容接口：

| 必须绑定的事实 | 最低内容 | 防止的错误 |
| --- | --- | --- |
| 精确内容主体 | 对象种类、完整内容身份、适用 CORE 与 Profile | 路径、标签、最新版或短摘要替代实际字节 |
| 内容形成分类 | 当前规范下适用的形成分类及其精确内容身份 | 把外部陈述写回内容状态，或让同一身份原地演进 |
| 外部陈述集合 | 每项陈述的完整身份、类型、精确主体、包络和生产者 | 单一布尔值截断多签、多陈述或陈述类型 |
| 验证记录 | 验证者、验证政策、参考值、实际检查、结果和失败原因 | “签名存在”自动变成“签名有效” |
| 时间与撤销 | 具名截止点、新鲜度依据、有效期、撤销来源和查询结果 | 缓存成功、过期材料或撤销失明继续进入会话 |
| 依赖方判断 | Dromen 建立政策、所需陈述集合、适用性结论和具名决定者 | Verifier 结果自动取得会话准入权或最终权威 |

```text
精确 coherent 内容（沿用现行词）
  + 一个或多个有类型的外部陈述
  + 每项陈述的验证记录、截止点与撤销状态
  + Dromen 建立政策对所需陈述集合的适用性判断
  -> 允许或拒绝建立新 Dromen
```

这条流程只产生一次会话的主体准入结论。它不改变内容身份，不产生 `met`，不创建 Iknem 充分性，不形成 `accepted`，也不证明实际环境和能力仍满足会话条件。

为保持现行安全强度，A 轴的第一版迁移应继续要求至少一项由具名政策要求且在截止点适用的外部陈述。是否允许无外部陈述的本地会话属于另一项安全策略变化，不能借删除 `attested` 顺便放宽。

### 主体准入反例矩阵

| 输入情况 | Dromen 建立结果 | 必须保留的原因 |
| --- | --- | --- |
| 精确内容、一个有类型陈述、验证通过、未撤销且满足建立政策 | 可以继续检查环境、能力、预算与证据责任 | 主体准入通过仍不是完整 Dromen 建立成功 |
| 同一内容关联两个签名，建立政策要求二者 | 两项都必须逐项验证并保留 | 不能压成一个 `true` 后丢失签名者和失败来源 |
| 签名字节有效，但签名者不满足建立政策 | 拒绝 | 密码有效性不授予主体资格或权威 |
| 陈述主体绑定另一份内容 | 拒绝 | 包络存在不能补偿主体替换 |
| 验证结果为正，但已超过依赖方允许的新鲜度 | 拒绝 | Verifier 结论不能脱离依赖方截止点复用 |
| 一项必需陈述已撤销，另一项仍有效 | 按显式集合政策判断；不得静默忽略撤销项 | 多签策略必须说明 all-of、阈值或具名选择规则 |
| 只保存上次“通过”的缓存，没有原陈述、政策和截止点 | 拒绝 | 缓存布尔值无法重新验证 |
| 外部 Task、Agent Card 或模型声称对象可信 | 拒绝 | 外部状态和模型输出不是签名陈述或依赖方判断 |

### `coherent` 描述评价，不描述检查责任

`coherent` 在普通语言和哲学中常表示“连贯、一致、合乎逻辑”。现行条款实际要求的却是有限的工程闭合：必需投影、引用、冲突、能力上限和判断关系已经解析。它不证明命题为真、目标合理、整体无矛盾、证据充分或权威接受。

候选 `resolved` 仍可能被误听为“问题已解决”，所以必须与 `content state` 连用，并在支持案例中验证首次读者能否恢复“形成责任已解决”而不是“目标已实现”。若人类测试仍持续误解，应改用更长但更精确的 `formation_resolved`，不能退回哲学评价词。

### `nascent` 增加记忆负担却没有增加精度

现行定义只是“结构已形成”。`nascent` 的日常含义是新生或初现，不能告诉读者结构、语义、引用或授权究竟完成到哪里。候选 `formed` 与条款的直接定义一致；但孤立的 formed 容易与最终完成混淆，因此机器字段、诊断和口头报告都必须带 `content state` 限定。

## 结果域审查

### 保留域，不保留无必要专名

[GNU Automake 测试框架](https://www.gnu.org/software/automake/manual/html_node/Scripts_002dbased-Testsuites.html)明确区分 `PASS / FAIL / SKIP / XFAIL / XPASS / ERROR`。它说明成熟工具链不会把“未运行”“预期失败”“意外通过”和“测试设施错误”压成一个成功布尔值。Noemion 应保留同样的分域纪律，但不需要复制 GNU 的结果词，因为满足判断、会话和权威决定回答的问题不同。

当前 AI 协议也支持这项分离：

- [MCP 2025-11-25 Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)把 `completed / failed / cancelled` 定义为任务终态，并要求 `tasks/result` 另行返回底层请求的最终结果；任务完成本身不是业务判断。
- [A2A 1.0 版本化规范](https://a2a-protocol.org/v1.0.0/specification/)把 `completed / failed / canceled / rejected` 作为 Task 终态，同时把 `input_required / auth_required` 作为中断状态。外部 Agent 的任务状态不能直接成为 Noemion 的满足结果、权威决定或会话证据。

因此五域结构继续成立，但名称应带域限定：

| 结果域 | 现行值 | 桌面结论 | 人类验证候选 |
| --- | --- | --- | --- |
| 内容形成分类 | `nascent / coherent / attested` | 必须拆分；`attested` 不是内容状态 | `content state: formed / resolved`；外部关系单列 |
| 满足判断 | `met / unmet / agno / fault` | 四分法保留；`agno` 不通过职责与读音门禁 | `satisfaction: met / unmet / undetermined / fault` |
| 权威决定 | `accepted / rejected / deferred` | 值清楚，保留比较 | `decision: accepted / rejected / deferred` |
| 会话终止 | `completed / failed / interrupted` | 前两项清楚；第三项可能暗示可恢复 | `session: completed / failed / stopped` |
| 证据有效性 | `valid / invalid / revoked` | 值清楚，但不得无域使用 | `evidence validity: valid / invalid / revoked` |
| 证据覆盖度 | `sufficient / insufficient` | 值清楚，但不得同有效性合并 | `evidence coverage: sufficient / insufficient` |

表中出现六行，是因为现行“证据状态”本来就包含有效性与覆盖度两个正交判断；这不是新增结果域，而是把现有两项责任显示出来。

### `agno` 的候选是 `undetermined`，不是 `unknown`

现行 `agno` 覆盖缺失、过期、越出范围、覆盖不足，以及测量不确定区间跨越阈值等情况。`unknown` 容易被理解为完全没有信息；`insufficient_observation` 又不能覆盖观察齐全但不确定度仍不足以决定阈值的情况。

`undetermined` 只表达“当前绑定的判断依据不能形成 met 或 unmet”，不声称原因只有缺数据。原因仍必须用稳定诊断保存，例如 missing observation、expired evidence、coverage gap 或 threshold-crossing interval。它也必须写成 `satisfaction: undetermined`，从而与 `decision: deferred`、`session: stopped` 和未解决意义分开。

[NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)要求 AI 风险测量采用严格测试、性能评估、不确定度度量、基准比较和正式报告，并指出独立复核可以降低偏差。模型置信度或一次 Agent 成功不能跨越不确定度替代满足判断；无法决定时保留 undetermined 比强行产生 met/unmet 更符合这项趋势。

### `aseme` 应改为可恢复职责的形成失败名

`aseme` 的现行定义是“没有任何允许投影”。它不是观察不足、未授权候选、解析器故障或目标未满足。候选 `no_allowed_projection` 直接保存失败条件，并与此前候选 `meaning_projection` 对齐。

| 情况 | 正确分类 | 不能使用 |
| --- | --- | --- |
| 没有任何符合允许规则的意义投影 | `no_allowed_projection` 候选 | `unresolved_meaning`、`undetermined`、`fault` |
| 有两个允许候选但无人获权选择 | `unresolved_meaning` 候选 | `no_allowed_projection`、`undetermined` |
| 运行观察不足以判断满足 | `satisfaction: undetermined` 候选 | `unresolved_meaning`、`no_allowed_projection` |
| 求值器或适配器违反契约 | `satisfaction: fault` | `unmet`、`undetermined` |

### `interrupted` 是否应保留仍需反例

现行 Dromen 一旦会话结束就不可恢复，扩大授权必须开始新会话。`interrupted` 在一般交流中却常表示暂停后继续；A2A 也把 input-required 和 auth-required 称为 interrupted state，而不是终态。候选 `stopped` 更直接表示“本会话已终止，但不是内部失败”。

`stopped` 仍不能合并取消者、外部政策、预算、截止点或环境漂移；这些进入原因码。若未来确实需要区分 user-cancelled、policy-stopped 与 environment-lost，应先证明下游消费者会作不同处理，再增加类型化原因，不能扩充一组风格对称的终态词。

## 支持案例与反例

| 场景 | 候选表达 | 正确理解 | 失败信号 |
| --- | --- | --- | --- |
| 结构已经确定性形成，但仍有获允许的未决意义 | `content state: formed` | 这是精确内容分类；不是无效、满足或可运行 | 读者把 formed 当 completed |
| 投影、引用、冲突和判断关系均已解决 | `content state: resolved` | 形成责任已闭合；新内容有自己的精确身份 | 读者把 resolved 当目标 met |
| 同一内容有两个外部签名 | 两项 signed-statement binding | 内容身份不变；各自绑定陈述、签名者和包络 | 把两个关系压成 `attested=true` |
| 签名有效，但撤销信息在截止点前生效 | 验证记录为 revoked 或不适用 | 不能建立本次会话 | 内容状态被原地改成 unattested |
| 观察区间跨越阈值 | `satisfaction: undetermined` | 当前不能决定 met/unmet | 用模型点估计强行产生 met |
| 没有允许的意义投影 | `no_allowed_projection` | 形成失败，尚未进入运行观察 | 写成 satisfaction: undetermined |
| 会话正常结束，但目标被有效反例证伪 | `session: completed` + `satisfaction: unmet` | 两域均保留 | completed 自动提升为 met |
| 会话因外部政策停止 | `session: stopped` 候选 + 原因码 | 本会话不可恢复；不是内部 fault | 把 stopped 当 deferred 或稍后 resume |
| 一份证据记录有效但只覆盖半个窗口 | `evidence validity: valid` + `evidence coverage: insufficient` | 记录可用但不足以决定满足 | valid 自动提升为 sufficient 或 accepted |

## 威胁与替代方案

### A 轴威胁清单

| 威胁 | 失败机制 | 迁移后的要求 |
| --- | --- | --- |
| 布尔压缩 | 多个陈述、验证者和政策被折叠 | 保存外部陈述集合与逐项验证记录 |
| 主体替换 | 陈述绑定相邻内容或可变选择器 | 比较完整内容身份、对象域与 Profile |
| 多签截断 | 只保留第一项或最后一项签名 | 保存完整集合和集合政策，不按输入顺序选择 |
| 包络与载荷混淆 | 包络验证成功却未核对陈述主体和类型 | 验证认证载荷类型、陈述主体与签名集合 |
| 签名者越权 | 密码正确被升级为授权正确 | AUT 或建立政策单独判断签名者资格与范围 |
| 政策擦除 | 验证结果脱离实际验证政策传播 | 验证记录绑定政策身份、版本和参考值 |
| 截止点漂移 | 旧成功在新会话中继续使用 | 每次建立绑定具名截止点和新鲜度依据 |
| 撤销失明 | 缓存成功掩盖后续撤销 | 绑定撤销来源、查询结果和适用时间 |
| 依赖方省略 | Verifier 正结果直接变成会话准入 | 依赖方按自己的建立政策再次判断 |
| 内容自证 | 内容内字段声称自己已经被证明 | 外部关系不得进入内容身份域或规范载荷 |
| 外部状态升级 | Task、Agent 或工具成功替代陈述验证 | 保留来源状态，只作为不可信输入或事件 |
| 失败来源合并 | 无陈述、签名错误、撤销和政策拒绝共用一个错误 | 产生稳定分层诊断，不改变结果域 |

### 保留 `attested`，只加强说明

否决。标准领域已经赋予 attestation 明确角色；说明文字无法让单值生命周期状态表达多个包络、政策、截止点和撤销关系。继续保留还会鼓励 Dromen 读取自填布尔值。

### 把第三个状态改成 `signed`

否决。`signed` 仍把外部多值关系写成内容自身状态，并容易推出签名已验证、签名者获授权或当前仍有效。签名陈述必须是外部对象与关系。

### 把第三个状态改成 `published`

否决。发布可以不签名，签名也可以不公开发布；发布位置、可发现性和分发政策又是另一组事实。`published` 不能替代签名或证明关系。

### 全部改用一个 `status`

否决。它会重建 ADR-0015 已消除的混淆，使外部任务完成、会话成功、满足判断和最终决定再次共享一个字段。

### 直接采用 MCP 或 A2A 的任务状态

否决。它们描述外部请求执行，不描述 Endem 内容形成、满足、证据覆盖或权威决定。适配器必须保留来源状态和显式损失，不能把协议便利变成 Noemion 语义。

### 以短新词替换 `agno/aseme`

否决。问题正是首次读者不能从拼写与读音恢复职责。除非普通短语造成可证明的互操作错误，否则不再为结果或失败分类创造词根。

## 读音与口头区分审查

桌面审查只发现风险，不能代替人类证据：

- `nascent` 与 `coherent` 有登记英语读音，但名称本身不恢复工程条件；发音正确仍可能理解错误。
- `attested` 易读，却与可信计算、供应链和证明语境中的既有意义冲突；读音流畅不能弥补对象边界错误。
- `agno` 没有在项目中登记目标语言、重音或稳定首次读法，可能出现 ag-no、ag-noh 等分裂；更重要的是听者无法从声音恢复“满足判断依据不足”。
- `aseme` 同样缺少稳定首次读法，且与 `semion`、`asemic` 等相邻形式形成额外记忆负担。
- `formed / resolved / undetermined / stopped` 都有普通读音，但必须在完整域限定短语中验证；孤立朗读不能证明职责清楚。

## 人类验证方案

验证遵守[术语与读音验证指南](../docs/terminology-and-pronunciation.html)，并使用两批独立参与者。发现阶段至少包含：

1. `content state: formed / resolved` 与现行 `nascent / coherent` 的职责匹配。
2. “两个签名、一个撤销、两个截止点”场景，检查参与者是否仍选择单值 attested 状态。
3. `satisfaction: met / unmet / undetermined / fault` 的缺数据、反例、阈值跨越与求值故障分类。
4. `no_allowed_projection / unresolved_meaning / satisfaction: undetermined` 的三向反例。
5. `session: completed / failed / stopped` 与 MCP/A2A 外部 Task 状态的来源域匹配。
6. `evidence validity` 与 `evidence coverage` 的成对朗读、听写和职责重建。
7. 完整句测试：“session completed, satisfaction unmet, decision rejected”与“evidence valid, coverage insufficient, satisfaction undetermined”。

候选出现以下任一情况就不能通过：

- formed 或 resolved 持续被理解为目标已经完成或满足；
- signed-statement binding 被理解为内容身份的一部分或最终信任结论；
- undetermined 被合并到 deferred、unresolved meaning 或 fault；
- stopped 被理解为可恢复同一 Dromen；
- valid 持续被理解为 claim 为真、覆盖充分或 accepted；
- 多词域限定在日常技术对话中总被截短到重新产生歧义。

## 接受后的迁移边界

### A 轴：对象边界修正

若用户接受 A 轴，迁移 ADR 应只纠正对象与关系，不等待 B 轴选出新名称，也不把候选名称写入接口：

1. 将 Endem “生命周期”改写为不可变内容形成分类与显式派生关系；说明每次内容变化产生新身份。
2. 从 END-CORE 的内容形成分类移除 `attested`，暂时保留 `nascent / coherent`；同步 END-LIF-001、ADR-0015、生命周期页、状态图、诊断位置与登记。
3. 以外部 typed signed statement、attestation result、验证记录、政策、截止点和撤销状态替换 Dromen 的 `subject.attested` 布尔值；同步 DRO-SUB-001、DRO-IMM-001、威胁模型、场景与全部提案向量。
4. 为单项有效陈述、多签、签名者无权、主体不匹配、过期、撤销、缓存结论和外部状态升级分别建立正反向量；不得只测试“布尔值为真”。
5. 保持内容身份、陈述验证结果和依赖方准入决定三个结果域正交；任何单项通过都不得自动推出其余两项。
6. 删除现行页面、图示、登记和新向量中的旧入口，不保留字段别名、重定向、双读或读取器兼容；旧表达只留在历史 ADR、迁移 ADR 和名称审计中。
7. 明确迁移测试只能证明资料、登记与向量一致，不能证明签名器、验证器、Drasor、Dromen 建立器或 CLI 已实现。

### B 轴：发行命名

B 轴只有在真人职责复述、成对朗读、听写和跨语言测试留下可审计证据后，才能形成独立决定：

1. 若接受 `formed / resolved`，发布新的 CORE/Profile 版本并处理身份域；不保留 `nascent / coherent` 别名。
2. 若接受 `undetermined`、`no_allowed_projection` 或 `stopped`，同步条款、状态矩阵、组合传播、原因码、场景和正反向量；不得用读取器兼容旧值。
3. 保持 `accepted / rejected / deferred`、证据有效性与覆盖度的独立身份，并在所有 UI、日志、诊断与协议映射中显示域限定。
4. 未通过人类验证的候选词继续留在研究提案，不得因 A 轴已经迁移而获得规范地位。

### 可验证的完成条件

A 轴只有同时满足以下条件才算完成：

- END-CORE、DRO-CORE、ADR、登记、公开说明、场景与向量对内容状态、外部陈述和依赖方决定给出同一套边界；
- 除历史 ADR、迁移 ADR、研究提案与名称审计外，现行接口不再出现 Endem `attested` 或 Dromen `subject.attested`；
- 每个上述拒绝类至少有一个能够指出失败责任域的反向量，多签场景不会因只验证第一项签名而通过；
- 迁移后的规范和 Profile 使用新版本，不把原有 `0.1` 内容静默改成另一套语义；
- 全站检查、规范引用检查、向量检查与静态构建全部通过，且公开页面不把资料一致性描述成组件实现。

B 轴只有在人类验证记录、失败条件、最终选择及受影响规范清单进入迁移 ADR 后才算完成。A 轴通过不表示 B 轴通过，B 轴选词也不能改写 A 轴的安全边界。

具体新字段、规范版本、Profile ID、条款前缀、物理包络和签名算法不能由本提案提前冻结。若外部签名与证明存在多个消费者，应优先复用 ID-CORE、IKN-CORE、AUT-CORE 和适配边界，不为“签过名”新增第五种制品。

## 当前决定边界

本提案现在形成一项待用户接受的边界结论，以及四项仍待人类验证的命名结论：

1. ADR-0015 的结果域正交原则继续成立。
2. `attested` 不应继续作为 Endem 内容生命周期状态；外部签名与证明必须建模为显式伴随关系。
3. `nascent / coherent` 没有通过职责透明度门禁；`content state: formed / resolved` 取得进入人类验证的资格。
4. `agno / aseme` 没有通过专名必要性与读音门禁；`satisfaction: undetermined` 与 `no_allowed_projection` 取得进入人类验证的资格。
5. 清楚的普通结果值可以保留，但必须带域限定；`interrupted / stopped` 仍需通过不可恢复会话反例决定。

这些结论不会在本轮改变任何现行规范值。用户可以单独接受 A 轴并形成对象边界迁移 ADR；这不会接受 `formed / resolved` 等 B 轴候选词。B 轴何时开始人类验证、采用哪些名称以及是否形成后续迁移 ADR，仍需另行决定。
