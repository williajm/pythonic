---
title: What makes Python great
hide:
  - toc
---

<div class="pyx-hero" markdown>
<p class="pyx-hero__prompt">&gt;&gt;&gt; import this</p>

# Beautiful is better than ugly.

<p class="pyx-hero__lede" markdown>The Zen of Python, made concrete: ten
short chapters of pythonic idioms on Python 3.14, where every code block
is embedded from source the test suite runs — CI holds this site to 100%
line-and-branch coverage, so nothing here is hand-waved.</p>

[Start with comprehensions](comprehensions.md){ .md-button .md-button--primary }
[See how honesty is enforced](toolchain.md){ .md-button }
</div>

## What "pythonic" means

**Pythonic** is the word Python programmers use for code that works *with*
the language instead of against it — code where the idiom carries the
bookkeeping so the intent stands alone. Tim Peters compressed the
philosophy into [the Zen of Python](https://peps.python.org/pep-0020/)
(`import this`); these chapters show what it means in practice. Most set
the pythonic idiom against the habit it replaces, in code; all of them
are honest about the trade-offs.

## The honesty rules

This is an educational site, and education built on cherry-picked examples
teaches the wrong thing. So:

1. **Every code block is real.** The snippets are embedded directly from
   [the repository's `src/` directory](https://github.com/williajm/pythonic/tree/main/src/pythonic)
   — each one carries its source path and a *tested in CI* mark, and CI
   enforces 100% line *and branch* coverage, so the site cannot show code
   the test suite doesn't run.
2. **The counter-examples work too.** The test suite checks that the
   "unpythonic" versions produce the same results (except where they
   genuinely don't — and then the bug is tested and documented). The
   argument for the idiom is almost never *correctness*; it is what the
   code costs to read, extend, and get right the next time.
3. **Every chapter has a "when not to" clause.** Idioms oversold become
   cargo cults. Comprehensions nest badly, EAFP is not a dogma, and
   pattern matching is not a switch statement.
4. **When the stdlib already ships the answer, we say so** — even when it
   makes our own example redundant (see
   [`running_total` vs `itertools.accumulate`](generators.md), or
   [`count_words` vs `collections.Counter`](eafp.md)).

One of those rules has already earned its keep: property-based testing
caught a real bug in a counter-example we believed was merely ugly.
[The strings chapter tells the story](strings.md).

## The chapters

| Chapter | The habit it retires |
| --- | --- |
| [Comprehensions](comprehensions.md) | Create-append-return loops |
| [Iteration](iteration.md) | `range(len(...))` index juggling |
| [Generators](generators.md) | Materialising data you'll mostly discard |
| [Context managers](context-managers.md) | Cleanup that skips the exception path |
| [EAFP](eafp.md) | Pre-checks that re-implement the operation, wrongly |
| [Records](records.md) | Hand-written `__init__`/`__repr__`/`__eq__` boilerplate |
| [Protocols](protocols.md) | Inheritance where a capability was meant |
| [Pattern matching](pattern-matching.md) | if/elif chains that re-destructure by hand |
| [Paths](paths.md) | String surgery on file paths |
| [Strings](strings.md) | `+=` assembly and separator bookkeeping |

## The toolchain is part of the argument

Python's greatness in 2026 is not just syntax: it is `uv` resolving locked,
hash-verified environments in milliseconds, `ruff` linting with every rule
it has, `mypy --strict` type-checking teaching examples, and `hypothesis`
finding the bugs we didn't know we'd written.
[The toolchain chapter](toolchain.md) shows how this repository is built,
tested, and secured.
