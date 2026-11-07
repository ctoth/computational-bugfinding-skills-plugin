---
name: failure-reduction
description: Reduces computational test failures while preserving the selected violation, valid setup and replay evidence. Use when shrinking fuzz inputs, programs with worlds, API histories, schedules or fault traces, especially when smaller cases change the symptom or stop reproducing.
---

# Failure reduction

Obtain a smaller useful counterexample to the selected guarantee. Preserve the original: "naïve reducers tend to introduce problematic undefined" behavior, and reduction can switch bugs, particularly in wrong-result cases, where "wrong-code bugs have no obvious fingerprint" ([Regehr et al., §§4, 5.1, 7.5 and 7.7](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). This skill owns reduction; use `evidence-based-triage` for attribution and verified duplicate causes.

## Choose the predicate and reduction unit

Read the real producer, enabled configuration and violated contract. Retain original inputs, initial state, raw outputs, witness and actual replay invocation; C-Reduce keeps a `.orig` backup by default because it "is useful when reductions go wrong" ([C-Reduce source](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in)). State which validity conditions belong to this experiment: malformed inputs may be legitimate robustness cases, while wrong-code comparisons require the language's defined-behavior conditions; compiler-crash cases have "weaker validity requirements than do the test cases for wrong-code bugs" ([Regehr et al., §§5.1 and 5.2.4](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

Accept a reduction only when the intended operation still executes and the selected result/effect/history violation remains observable; the paper's reducers use one test that "determines if the variant triggers the compiler bug and also, if necessary," checks validity ([Regehr et al., §6](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). Treat setup failure, invalid candidate, changed violation and insufficient observation separately. A reducer can distinguish unresolved outcomes even when its search accepts only interesting/not-interesting: the Debugging Book's `generic_test` returns `UNRESOLVED` for an exception whose type or message differs from the expected one (any exception is `FAIL` when no expected exception is given), and "The `ddmin` algorithm treats such unresolved outcomes as if they were passing" ([Delta Debugging, generic_test and ddmin](https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb)). For the pack's dependent-artifact convention, read [interestingness and replay](references/interestingness-and-replay.md).

Choose the current generator's shrinker or a compatible maintained reducer. Reduce the material that causes the observation: typed arguments, source plus world, operation sequence plus schedule, or acknowledged work plus storage fault. These are adaptation choices, not a promise of a generic reducer for every representation. Coordinated structural transformations, such as "removing an argument from a function and simultaneously all its call sites", can escape limits of contiguous deletion ([Regehr et al., §§3–4 and 6](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

## Execute a compatible reducer

Read [tool recipes](references/tool-recipes.md) for the applicable route:

| Existing artifact | Route |
|---|---|
| C/C++ source or selected text format | C-Reduce, with its actual no-argument test and temporary working directory |
| LLVM IR/MIR | llvm-reduce, with candidate-path test invocation |
| A libFuzzer crash input | Crash reduction, distinct from coverage-corpus reduction |
| Go or Hypothesis generated inputs | Existing typed replay and shrinker; preserve extra dependent state |

Check selected tool/version, input format, predicate invocation and working-directory behavior before running. Exercise the original, a healthy candidate and an invalid/setup candidate through that same interface; C-Reduce's help says that if the original does not return zero in a fresh temporary directory, "the interestingness test is flawed". Use `harness-sensitivity` if the intended rejection is unestablished. Do not interpret reducer process success as proof of final replay: llvm-reduce "returns 0 under normal operation" ([C-Reduce executable contract](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in), [llvm-reduce exit status](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/CommandGuide/llvm-reduce.md)).

## Spend reduction compute on trustworthy improvements

Keep separate per-attempt and whole-job limits, worker/resource use, invalid/unresolved attempts and useful size or readability improvements. Native controls have different scopes: libFuzzer's `-minimize_crash` says "Use with -runs=N or -max_total_time=N to limit the number of attempts"; Go's `-fuzzminimizetime` applies "during each minimization attempt" ([libFuzzer options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md), [Go custom settings](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)). Choose actual limits from the authorized task, not universal numbers.

When replay changes, investigate missing state, prior inputs, uncontrolled choices and environment before accepting the smaller case. "Non-deterministic execution of the system under test can cause test-case reduction to fail" ([Regehr et al., §7.7](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). Hypothesis documents that external state or changing visible outcomes prevent reliable replay, and a strategy that depends on external state leaves it "unable to shrink to a minimal failing input" ([flaky failures](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/flaky.rst)). Preserve observed trials and partial results; no fixed retry count proves continuity. For practical dependent-world, schedule and recovery examples, read [worked reductions](references/worked-reductions.md).

## Complete the reduction

Replay original and reduced artifacts under the retained guarantee and configuration. State the preserved witness, changed identities and any uncertainty about common cause. Return artifact paths, actual commands/limits, chosen size metric, transformations attempted, final replay results and stopping reason. A deletion-fixed point is relative to its predicate and moves; it is not an absolute smallest case. 1-minimal means "every character contained is required to produce the error" ([Delta Debugging, minimality](https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb)), and "all test-case minimization work that we are aware of is heuristic" ([Regehr et al., §3](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). Keep a useful partial reduction when the budget or observability ends.

Use the project's regression conventions for a confirmed reproducer; do not rely only on a version-sensitive opaque replay blob; Hypothesis's blob "is not stable across Hypothesis versions" ([Hypothesis replay](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/replaying-failures.rst)). Read [common mistakes](references/common-mistakes.md) when reduction appears successful but changes the evidence. Invocation does not enlarge authorization to edit targets, install tools or publish findings.
