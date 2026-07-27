---
slug: types-and-python
number: "05"
lang: en
title: "Types and Python — Why It Became the Center of the AI-Native Language"
subtitle: "C# is technically solid, but it cannot handle the AI-native substrate cleanly. That is the structural consequence of being a halfway language."
description: "Java/C# stalled at stage 3 of type evolution (objects). Handling the AI-native substrate (Markdown, DataFrame, JSON, Parquet) permanently requires translation labor through class definitions. Python's dynamic typing and duck typing — long derided as weaknesses — invert in the AI era into its greatest strengths. Where performance is needed, have AI write Rust. C# has entered the era in which it should be discarded."
date: 2026.05.23
label: Structural Analysis 5
part_title: Outline of the New World
part: "2"
prev_slug: two-layer-ai-revolution
prev_title: "What the AI Revolution Really Is — A Two-Layer Simultaneous Change"
next_slug: translation-labor
next_title: "The Discovery of Translation Labor — The Real Reason So Many People Were Needed"
cta_label: Choose
cta_title: Language choice is the entry point to AI-native work.
cta_text: Choosing Python is the only choice that lets you handle the AI-native substrate cleanly. Do not invest time in halfway languages.
cta_btn1_text: "Next: The Discovery of Translation Labor — The Real Reason So Many People Were Needed"
cta_btn1_link: /en/insights/translation-labor/
cta_btn2_text: "Previous: What the AI Revolution Really Is — A Two-Layer Simultaneous Change"
cta_btn2_link: /en/insights/two-layer-ai-revolution/
---

## The History of Types — Four Stages of Evolution

The previous chapter noted that "the types programmings languages can handle have expanded." This chapter examines that history and its structural meaning in detail.

The "types" a programming language can express evolved in four stages over half a century.

:::compare
| Stage | Types handled | Representative languages | Era |
| --- | --- | --- | --- |
| 1. Machine | bit, byte, word | Assembly, early Fortran | ~1960s |
| 2. Structs | int, float, char, struct, array | C, Pascal | 1970s–80s |
| 3. Objects | + class, interface, generics | C++, Java, C# | 1990s–2010s |
| 4. AI-native substrate | **+ Markdown, DataFrame, JSON, Parquet, RDB, HTML, embedding** | **Python (especially AI-integrated)** | **2020s–** |
:::

Each transition happened **when the limits of the previous stage became visible**:

- Stage 1 → 2: Machine language could no longer let humans manage large programs
- Stage 2 → 3: Structs could no longer model business concepts (customer, order, invoice)
- Stage 3 → 4: Objects could no longer handle cleanly **data whose shape is not known in advance**

## Java / C# Stalled at Stage 3

Java / C# were designed as the pinnacle of stage 3. Their worldview is: **write class definitions in advance, then pour data through them**.

:::highlight
**The stage-3 language assumption:**
Before touching data, declare its shape as a class.
Strong typing, compile-time checks, refactoring support, IDE completion — all of it rests on this assumption.
:::

That assumption was rational for building business systems. The shape of a customer table is fixed in advance. The structure of an order is fixed. CRUD applications were a world where you could declare a schema upfront.

But the AI-native substrate is a world where **shape is not fixed in advance**:

:::chain
**Characteristics of the AI-native substrate:**
Markdown → body structure is a dynamic AST, different per document
DataFrame → column layout depends on the data
JSON → fields can be omitted or added
Parquet → has types but structure is fluid
RDB → the shape of JOIN results depends on the query
HTML → the DOM is not fixed in advance
embedding → dimensionality and semantics depend on training outcomes
:::

All of it is data **whose shape is not fixed until you touch it**. Class-based languages demand the shape before you touch it — the order is reversed.

## Concrete Impedance Mismatch

Write the same thing in both languages and the gap is immediately apparent.

**Example: extracting a value from JSON**

Python:
```python
data = json.loads(text)
print(data["customer"]["address"]["city"])
```

C#:
```csharp
public class Address { public string City { get; set; } }
public class Customer { public Address Address { get; set; } }
public class Root { public Customer Customer { get; set; } }

var data = JsonSerializer.Deserialize<Root>(text);
Console.WriteLine(data.Customer.Address.City);
```

**Python can touch data without knowing its shape.** C# demands class definitions before touching it. In AI dialogue, this is a decisive gap — when you ask an AI to "look at this JSON and transform it," Python takes 3 lines; C# starts with class definitions.

**Example: reading a YAML config**

Python:
```python
config = yaml.safe_load(open("config.yaml"))
db_url = config["database"]["url"]
```

C#:
```csharp
var deserializer = new DeserializerBuilder().Build();
var config = deserializer.Deserialize<MyConfigClass>(reader);
var dbUrl = config.Database.Url;
```

C# forces you to "declare the YAML's shape as a class first." For dynamically varying configs (which most YAMLs are), it is fundamentally unsuited.

**Example: DataFrame and Parquet**

Python takes one line: `pl.read_parquet("file.parquet")`. C# has **no central DataFrame abstraction**. Microsoft.Data.Analysis exists as an official package, but the community does not use it. The ecosystem is orders of magnitude smaller than pandas or polars.

## Python's "Weaknesses" Inverted Into Strengths

Python has long been criticized for:

- Dynamic typing — not type-safe
- Duck typing — type errors are not caught until runtime
- Interpreter-based — slow
- GIL — true parallelism impossible

**Every one of these "weaknesses" inverted into a strength in the AI era:**

:::compare
| Property | Stage-3 era assessment | AI-native era assessment |
| --- | --- | --- |
| Dynamic typing | Weakness (slow error detection) | **Strength (can handle data whose shape is unknown)** |
| Duck typing | Weakness (ambiguous, hard to maintain) | **Strength (accepts AI's dynamic output as-is)** |
| Slow execution | Weakness (insufficient performance) | **Irrelevant (everything underneath escapes to C/Rust)** |
| GIL | Weakness (parallelism impossible) | **Irrelevant (heavy computation is parallelized in external libraries)** |
:::

"Python is slow" has effectively become a lie:

- pandas / polars / NumPy → C / Fortran / Rust internals
- PyTorch / JAX → C++ / CUDA / XLA
- DuckDB → vectorized SQL in C++
- uv / ruff / orjson → written in Rust
- Numba → JIT-compiled to near-C speed

**Python's body is the API; every engine is native.** This is a completed division of labor.

## Python + AI-Generated Rust — The Strongest Combination

This is the key of the AI era. **Find the hotspot in Python, then have AI write the Rust extension.**

```python
# A Python computation that's running slow
def heavy_calculation(data: list[float]) -> float:
    return sum(complicated_formula(x) for x in data)
```

Tell AI "rewrite this as a Rust PyO3 extension," and in 5 minutes:

```rust
use pyo3::prelude::*;

#[pyfunction]
fn heavy_calculation(data: Vec<f64>) -> f64 {
    data.iter().map(|x| complicated_formula(*x)).sum()
}
```

`maturin build` produces an extension callable from Python. **Performance is C-level; the development experience stays Python.**

Three years ago this was a job for a Rust specialist. **Now AI writes it.**

C# has no such escape hatch. Options for speeding up a hotspot in C#: unsafe code (safety breaks down), P/Invoke (cumbersome), C++/CLI (Windows-only, declining), AOT (does not reach Rust-level speed) — all are halfway measures. **C# lacks the clean division of "productive at the front, fast at the back."**

## The Structural Meaning of C# Being "Halfway"

C# is technically well-made. The reason it still cannot win in the AI era is that **it takes first place on no axis**:

:::compare
| Axis | First place | C#'s position |
| --- | --- | --- |
| Raw performance | Rust / C++ | Loses |
| Data / ML productivity | Python | Loses badly |
| Web front-end | TypeScript | Loses |
| Cross-platform | Python / Go / Rust | Loses (feels like an outsider on Linux) |
| AI compatibility | Python | Loses badly (training data ratio) |
| GPU / parallel | CUDA / PyTorch | Loses |
| Scripting / automation | Python / Shell | Loses |
| Enterprise business systems | Java / C# | Tied (the only axis) |
:::

**There is not a single axis where C# comes first.** Even in enterprise business systems it only ties with Java — no dominance. **Second or lower on everything** — that is the structural meaning of "halfway."

Historically, "halfway languages" have been culled: Pascal, Delphi, Perl, Scala — every time a new paradigm arrives, general-purpose halfway languages fall away. In the AI era, Java / C# are becoming the next targets.

## Three Surviving Contexts for C# — All Path-Dependency

Surveying where C# is still used:

1. **Existing Microsoft enterprise** — large corporations with 20-year-old .NET Framework assets
2. **Unity game development** — no choice, since the game engine adopted C#
3. **Windows-only desktop** — WPF / WinForms assets

**All of them are "it's already there" circumstances, not new choices.** None of them is a positive reason to choose the language for a new project.

## Microsoft Ownership — The Problem Before the Technical One

C# / .NET has a problem that precedes technical merit: **Microsoft owns it**.

:::compare
| | C# / .NET | Python |
| --- | --- | --- |
| Organization that controls design | Microsoft | Python Software Foundation (non-profit) |
| Roadmap announced at | Microsoft Build, .NET Conf | PEP, python.org |
| Strategic dependency | Azure / Visual Studio / Windows | None |
| "What if Microsoft abandons it?" | Evolution stops | Cannot happen |
:::

C# is open-sourced, but **Microsoft controls its strategic direction**. It is "a good language made by Microsoft," not "a language as public infrastructure." The relationship is close to Word and .docx.

Microsoft's track record with languages and frameworks makes the risk clear: VBScript → abandoned, Silverlight → abandoned, WPF → reduced, WinForms → maintenance only, UWP → quietly wound down, Xamarin → replaced by MAUI amid confusion. **When Microsoft pivots strategy, C#'s priority shifts with it.**

Python belongs to no one, so **its direction of evolution does not change with a vendor's mood.**

## "Discard" Is the Correct Verdict

When choosing a language for a new project in 2026, the options sort out as follows:

:::chain
**Language selection for the AI era:**
AI-native work → Python (no argument)
Performance-critical parts → Rust (have AI write it)
Web front-end → TypeScript (provisional, discussed later)
CLI tools → Go or Rust
Data analysis → Python + DuckDB
New business systems → Python + FastAPI
Mobile → Swift / Kotlin
Embedded → Rust / C
:::

**There is structurally no scenario in which you choose C#.** Java is in the same position (halfway, but surviving on enterprise inertia).

"Discard" is the correct verdict. **There is no longer a rational reason to choose C# / .NET for new development.**

## Conclusion — Language Choice Is a Structural Choice

To enter AI-native work, you must **choose a language that can handle the AI-native substrate cleanly**. Python is the only one that satisfies this. C# / Java remain stuck at OOP, and the impedance mismatch with the new substrate persists permanently.

This is not a question of technology selection — it is a question of **whether you can stand inside the AI revolution**. As long as you stay in a halfway language, you experience the revolution only halfway.

:::quote
Python did not win because it is technically superior.
It is the only language that can handle the AI-native substrate cleanly.
C# / Java stalled at OOP and require "declare a class before touching it" for the new substrate.
Where performance is needed, have AI write Rust.
There is no longer any reason to invest time in halfway languages.
:::

The next chapter examines what **social consequences** this "poverty of types" produced. It reveals the real reason so many people were needed in software development.
