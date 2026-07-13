# Noemion 规范源

本目录保存实现可以逐条引用的规范源。公开 HTML 负责直白解释和阅读入口；本目录负责版本、条款 ID、规范强度与验证映射。二者冲突时，先停止实现并通过 ADR 修正文档，不能由当前代码行为反向改写规范。

## 当前规范

| 规范 | 版本 | 状态 | 已覆盖 | 明确未覆盖 |
| --- | --- | --- | --- | --- |
| [`endem-core.md`](endem-core.md) | `0.1.0-draft` | 草案；已接受语义边界的第一份条款化表达 | Endem 最小性、六个语义面、事态与方向分离、未知状态、确定性、安全读取、身份分层与验证责任 | END-P1 之外的量化、时间、求值、摘要与签名 |
| [`endem-format.md`](endem-format.md) | `0.1.0-draft` | 已采用的实验性草案；尚非稳定 ABI | 固定前导、定宽目录、确定性 CBOR、END-P0 结构实验与 END-P1 封闭语义载荷 | coherent/attested、签名、压缩、Synem 和跨版本承诺 |
| [`endem-source-manifest.md`](endem-source-manifest.md) | `0.1.0-draft` | 实验性 Poiet 输入；正式来源语言出现后删除 | UTF-8 逐行指令、转义、基数、授权边界和 END-P1 映射 | 注释元数据、包含、模块、量化、时间、求值语言和兼容承诺 |

[`endem-threat-model.md`](endem-threat-model.md) 把不可信输入、资源放大、歧义清洗、身份混淆和解析器共同故障映射到规范条款。[`profiles/end-p0.json`](profiles/end-p0.json) 给出第一组跨实现实验的有限上限；这些数值不是生产规模证明，提高时必须采用新的 Profile 身份。

[`endem-errors.md`](endem-errors.md) 登记结构与 Profile 错误码。[`registry.json`](registry.json) 是机器可读的规范、术语、条款、威胁、成熟度与验证登记。`../vectors/semantic/` 保存 JSON 语义外壳；`../vectors/wire/` 保存真实字节的十六进制表达。结构接受向量不等于语义有效 Endem。

[`endem-scenarios.md`](endem-scenarios.md) 是非规范性的自然语言设计审查语料。它用八个场景检查达到成立、持续保持、否定事态、指称歧义、观察不足、求值故障、授权不足和多根拆分是否能被现行六语义面解释。它不规定语法或字节，也不是可执行测试；案例暴露的缺口必须回到 ADR、规范条款或开放问题。

`registry.json` 还登记非规范实验及其决定链。P0-LANG-001 的协议与结果位于 `../experiments/p0-language/`；它支持 ADR-0012 的首版核心语言决定，但不会改变 END-CORE 或 END-FMT 的条款含义，也不把原型登记为生产实现。

## 规范强度

只有大写的 `MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT` 与 `MAY` 具有规范强度，解释遵循 BCP 14。正文在首次出现时同时给出中文含义。

- RFC 2119：https://www.rfc-editor.org/rfc/rfc2119.html
- RFC 8174：https://www.rfc-editor.org/rfc/rfc8174.html

普通中文“必须、不得、可以”用于解释时仍应忠实于相邻条款，但不能替代条款 ID。每条实现义务只能由一个主条款定义；其他文档只能引用，不能复制第二套要求。

## 成熟度维度

规范状态、实现状态与证据状态分开登记：

- `decision_status`：设计边界是否已经由当前 ADR 接受；
- `implementation_status`：是否存在声称符合该条款的实现；
- `evidence_status`：仓库内是否已有覆盖向量或测试；
- `wire_status`：物理编码是否冻结。

`implementation_status` 当前只允许 `unimplemented` 与 `vector-checker-only`。后者表示仓库存在只服务规范资料的检查脚本，不表示项目组件已经实现。`decision_status: accepted` 不表示实现存在，也不表示证据充分；`wire_status: experimental-draft` 只允许草案向量，任何程序都不得声称产生可互操作的稳定 `.endem` 字节。

## 变更规则

1. 改变现有条款含义时，先新增或更新 ADR，再提升规范版本。
2. 新条款必须登记唯一 ID、成熟度、失败责任与验证方式。
3. 删除条款必须保留版本历史，并说明替代条款或删除理由。
4. `covered-by-repo` 只能用于仓库中实际存在且由自动检查读取的证据。
5. `planned` 表示验证尚未实现，不能在公开页面写成已经通过。
6. 格式草案变化必须同步 ADR、END-FMT、Profile、错误目录、登记和正反字节向量；不得把语义向量 JSON 直接改名为 `.endem`。
7. 场景语料变化必须保持非规范状态；只有转化为唯一条款、登记验证方式并形成正反向量后，案例中的判断才可能成为符合性要求。
