# Endem 应用视觉签名

本文件为唯一公开应用 `endem` 及其五个动作定义视觉方向。共享布局、六章语义结构、可访问性和动效仍以 `tool-project.md` 为准；动作差异只帮助读者辨认当前任务、产物和权限边界，不能暗示已经实现，也不能把动作包装为独立产品。

正式应用入口是 `/endem/index.html`，手册位于 `/endem/docs/`。页面可以由默认布局写入 `body[data-endem-action]`；共享 CSS 根据动作选择有限的色彩、签名文字、网格角度和焦点位置。不得在单个 HTML 或 Markdown 页面内添加样式。

## 共同制品语言

- Endem 记录面板固定以 `source_expression / meaning_projection / situation / goal_direction / satisfaction_criteria / unresolved_meaning` 六行作为识别骨架；`meaning_projection` 与 `situation` 必须通过共享符号和关系位置显示投影，不能只画六条无关联文字。运行证据用 `structured_observation ↔ situation` 显示结构比较，`goal_direction` 独立显示目标方向。
- Endem closure 使用明确的引用边和闭包外框，不能画成会在运行时无限扩张的网络。
- session contract 使用有边界的装载区域、能力票据和预算刻度，不能暗示全局权限。
- evidence entry 使用“主体 + 范围 + 方法 + 结果 + 限制”五部分标记，不能只显示通过图标。
- Noemion 只出现在品牌导航和项目归属，不进入动作签名、格式标签或对象类型。

## 动作签名

### form

- 签名：`SOURCE / FORM`
- 色彩：来源薄荷、成形蓝、诊断橙。
- 母题：来源片段沿稳定顺序进入投影语义骨架，再形成单个 Endem 边界。
- 内容强调：来源定位、确定性投影、一个根 `situation`、`unresolved_meaning` 保留与 deterministic producer 的字节生成权。
- 不得暗示：模型直接生成 `.endem`、自由文本天然有效或来源推断等于原文。

### lint

- 签名：`STRUCTURE / LINT`
- 色彩：检查绿、规则紫、拒绝红。
- 母题：从边界、字段、引用、语义到策略的分层检查线。
- 内容强调：稳定错误类别、精确定位、checked arithmetic、资源上限和失败即停止。
- 不得暗示：检查通过等于目标已经实现或最终验收通过。

### compose

- 签名：`REFERENCE / COMPOSE`
- 色彩：链接深蓝、冲突红、闭包薄荷。
- 母题：多个 Endem 的显式引用在固定顺序中解析为 Endem closure 外框。
- 内容强调：内容身份、必需/可选关系、冲突拒绝、闭包完整性与确定性 Link Map。
- 不得暗示：环境搜索、弱优先级、延迟碰运气或模型选择依赖。

### inspect

- 签名：`BYTES / INSPECT`
- 色彩：检视青、偏移橙、只读蓝。
- 母题：独立观察窗直接切开不可信字节，显示字段、引用、闭包和 evidence entry 范围。
- 内容强调：independent inspector 与 deterministic producer 代码独立、只读权限、直接解析、边界检查和差分验证。
- 不得暗示：independent inspector 调用 deterministic producer 的形成侧解析器、修复输入、写回文件、访问密钥或启动 bounded runner。

### run

- 签名：`SESSION / RUN`
- 色彩：运行蓝、能力绿、拒绝红。
- 母题：Endem closure 依次通过检查、策略和能力门进入有边界的 session contract，事件向 evidence entry 流出。
- 内容强调：bounded runner 独立权限域、最小能力、预算、可观察事件、人工升级和不可修改已封装制品。
- 不得暗示：通用 shell、无限会话、模型自扩权或 bounded runner 自行宣告验收。

## 权限域视觉规则

1. deterministic producer、independent inspector、bounded runner 和密钥域使用不同边界线，不得放在同一无边界容器中。
2. `form/lint/compose` 可以共享 deterministic producer 色系，但必须显示不同输入和产物。
3. 外部签名集成只接受确定性产物与精确身份，不能画出反向修改 Endem/Endem closure 的箭头；它不是公开动作。
4. `inspect` 只能从制品指向只读视图，不能存在回写箭头。
5. `run` 只能从已检查 Endem closure 建立 session contract；能力从策略域单向授予并可撤销。
6. evidence entry 从具体检查或运行事件产生，范围标记始终可见；不得使用一个全局“Verified”覆盖所有结论。

## 共同行为

- 动作签名只替换应用引言中的制品面板文字，不替代页面 H1，也不改变唯一应用名 Endem。
- 动作色彩用于应用引言、章节短线、状态面板和有限悬停反馈，不改变正文对比度。
- 手册页面只继承当前任务的强调色；侧栏宽度、Markdown 排版和动态目录保持统一。
- 所有交互继续使用 0.96 按压反馈、具体属性过渡和减少动态效果支持。
- 页面或目录不得出现并列工具卡片；需要导航五个动作时使用同一应用内的任务列表或手册目录。内部符合性门禁和外部签名集成都不得获得动作签名。
- 视觉状态必须区分“规范已冻结”“实现中”“可运行”“有 evidence entry”和“验收通过”，不能把其中任意两个状态合并。
