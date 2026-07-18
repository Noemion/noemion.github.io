# P0-W4 实现语言实验

- 实验 ID：`P0-LANG-001`
- 日期：2026-07-13
- 输入：`END-FMT 0.1.0-draft`、`END-P0 0.1.0-draft`、`vectors/wire/`
- 状态：可重复实验；不是生产实现，也不构成语言选型结论本身

## 目的

本实验比较 C17 与安全 Rust 对同一组不可信 END-P0 字节的解释。它只回答首版固定前导、记录目录、范围、对齐、六记录基数和空映射载荷能否由小型实现稳定拒绝；不解析完整六语义面，不写 Endem，也不评估 CLI、closure、evidence 或 runner。

## 不变量

1. 两个原型只共享公开规范、Profile 和字节向量，不共享源码、解析库、生成代码或错误分类实现。
2. Rust 原型使用 `#![forbid(unsafe_code)]`、标准库和显式 `checked_add/checked_mul`，不使用第三方 crate。
3. C 原型使用定宽整数、固定 64 项栈目录、显式溢出检查和逐字段读取，不把磁盘字节强制转换为结构体。
4. 每个规范向量必须得到清单指定的接受或主错误码。
5. 两个原型对确定性变异语料必须给出相同首个错误类别，且不得崩溃、挂起或输出部分可信对象。
6. C 原型必须通过 AddressSanitizer 与 UndefinedBehaviorSanitizer；具有 libFuzzer runtime 的符合性环境还必须完成 10,000 次覆盖引导运行。缺少 runtime 时必须登记为证据缺口。
7. 两种优化构建分别在两个输出目录重复生成；实验记录二进制摘要是否一致、文件大小和动态依赖，不把单机一致误写成跨平台复现。

## 运行

```text
RUSTC=/path/to/rustc python3 experiments/p0-language/run_experiment.py
RUSTC=/path/to/rustc python3 experiments/p0-language/run_experiment.py --require-libfuzzer
```

脚本在临时目录生成原始二进制向量和编译产物，不修改仓库。它要求 `clang` 与 `rustc`，并输出 JSON 报告到标准输出。环境没有 Rust 时必须明确失败，不能静默只测 C。仓库的 Linux 工作流固定 Rust 1.97.0，并使用 `--require-libfuzzer` 把缺少覆盖引导证据视为失败。

## 解释边界

- `all_vectors_match=true` 只证明当前 6 个结构向量一致。
- `differential_mutations_match=true` 只证明当前确定性变异集的错误优先级一致。
- `repeated_binary_sha256_match=true` 只证明同一台机器、同一工具链、同一源码路径下的两次优化构建一致。
- Sanitizer 或 libFuzzer 未发现崩溃不等于不存在漏洞。
- 语言选择还必须考虑所有权/边界安全、依赖、构建锁定、跨平台、审计难度、FFI 和长期维护。

## 权威机制来源

- Rust 所有权由编译器检查，用于在无垃圾回收器的情况下管理内存：https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html
- Rust 无符号整数提供 `checked_add`、`checked_mul` 等显式受检运算：https://doc.rust-lang.org/stable/std/primitive.u64.html
- GNU GCC 提供 AddressSanitizer、UndefinedBehaviorSanitizer 与覆盖引导插桩：https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
- LLVM libFuzzer 直接接收任意字节，并要求目标快速、确定、可重复且不因畸形输入退出：https://llvm.org/docs/LibFuzzer.html
