# Noemion 原生词汇冲突审计

日期：2026-07-12
状态：ADR-0010 的工程命名证据；不是法律意见

## 审计范围

- 语言关键字：C、C++、Rust、Go、Python、Java、ECMAScript、Swift、Kotlin。
- 注册表精确名：PyPI、npm、crates.io。
- 相邻技术检索：编译器、对象格式、人工智能协议、开发工具和学术软件。
- 现行词：`endem`、六个语义面、四个正式系统名词、三个组件名、八个动作。

## 结论

`case`、`open`、`when` 明确与主流语言关键字冲突，退出现行接口。`say`、`mean`、`seek`、`keep`、`avoid` 以及 Core、Reader、Runner、Frame、Witness 虽不全是关键字，但过于通用，无法形成独立领域身份，也退出现行接口。

现行词如下：

```text
rhem semion skena telis krin apor
Endem Synem Dromen Tekmor
Poiet Theor Praxor
poie elenk pleko tasse sphra theor praxe peira
```

上述词在审计语言的关键字集合中无精确冲突。2026-07-12 的 PyPI、npm、crates.io 精确查询未发现这些词同时形成强占用；大小写变体、近音词、其他行业名称和未来登记仍可能出现。

## 权威关键字来源

- Rust Reference：https://doc.rust-lang.org/stable/reference/keywords.html
- Go Language Specification：https://go.dev/ref/spec#Keywords
- Python Language Reference：https://docs.python.org/3/reference/lexical_analysis.html#keywords
- Java Language Specification：https://docs.oracle.com/javase/specs/jls/se26/html/jls-3.html#jls-3.9
- ECMAScript Language Specification：https://tc39.es/ecma262/#sec-keywords-and-reserved-words
- Swift Language Reference：https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html
- Kotlin Keyword Reference：https://kotlinlang.org/docs/keyword-reference.html
- C/C++ 标准工作组入口：https://www.open-std.org/jtc1/sc22/wg14/ 、https://www.open-std.org/jtc1/sc22/wg21/

## 注册表查询入口

- PyPI JSON API：`https://pypi.org/pypi/<name>/json`
- npm Registry：`https://registry.npmjs.org/<name>`
- crates.io API：`https://crates.io/api/v1/crates/<name>`

精确包名未登记不等于名称权利。首次发行前仍须保存查询时间、响应、近似名、目标法域商标、产品分类、命令、扩展名、MIME、域名与法律复核结果。

## 词源边界

词根仅帮助记忆，不决定软件含义。古希腊语查询使用芝加哥大学 Logeion 汇集的 LSJ 等词典；例如 *lexis* 的基本义为 speaking/saying/speech：https://logeion.uchicago.edu/%CE%BB%CE%AD%CE%BE%CE%B9%CF%82 。

Noemion 对词根进行了缩写或再造，因此 `rhem`、`semion`、`skena`、`telis`、`krin`、`apor`、`Synem`、`Dromen`、`Tekmor`、`Poiet`、`Theor` 与 `Praxor` 都必须以 ADR-0010 的工程定义为准，不能用古典词义替代规范。
