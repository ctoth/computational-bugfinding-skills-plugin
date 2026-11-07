---
name: failure-reduction
description: Reduces computational test failures while preserving the selected violation, valid setup and replay evidence. Use when shrinking fuzz inputs, programs with worlds, API histories, schedules or fault traces, especially when smaller cases change the symptom or stop reproducing.
---

# Failure reduction

Obtain a smaller useful counterexample to the selected guarantee. Preserve the original: reduction can introduce invalid behavior or switch bugs, particularly in wrong-result cases ([Regehr et al., §§4, 5.2 and 7.7](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). This skill owns reduction; use `evidence-based-triage` for attribution and verified duplicate causes.

## Choose the predicate and reduction unit

Read the real producer, enabled configuration and violated contract. Retain original inputs, initial state, raw outputs, witness and actual replay invocation. State which validity conditions belong to this experiment: malformed inputs may be legitimate robustness cases, while wrong-code comparisons require the language's defined-behavior conditions ([Regehr et al., §5.2](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

Accept a reduction only when the intended operation still executes and the selected result/effect/history violation remains observable. Treat setup failure, invalid candidate, changed violation and insufficient observation separately. A reducer can expose unresolved outcomes even when its interface ultimately accepts only interesting/not-interesting ([Delta Debugging, generic_test and ddmin](https://www.debuggingbook.org/html/DeltaDebugger.html)). For the pack's dependent-artifact convention, read [interestingness and replay](references/interestingness-and-replay.md).

Choose the current generator's shrinker or a compatible maintained reducer. Reduce the material that causes the observation: typed arguments, source plus world, operation sequence plus schedule, or acknowledged work plus storage fault. These are adaptation choices, not a promise of a generic reducer for every representation. Coordinated structural transformations can escape limits of contiguous deletion ([Regehr et al., §§3–4 and 6](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

## Execute a compatible reducer

Read [tool recipes](references/tool-recipes.md) for the applicable route:

| Existing artifact | Route |
|---|---|
| C/C++ source or selected text format | C-Reduce, with its actual no-argument test and temporary working directory |
| LLVM IR/MIR | llvm-reduce, with candidate-path test invocation |
| A libFuzzer crash input | Crash reduction, distinct from coverage-corpus reduction |
| Go or Hypothesis generated inputs | Existing typed replay and shrinker; preserve extra dependent state |

Check selected tool/version, input format, predicate invocation and working-directory behavior before running. Exercise the original, a healthy candidate and an invalid/setup candidate through that same interface. Use `harness-sensitivity` if the intended rejection is unestablished. Do not interpret reducer process success as proof of final replay ([C-Reduce executable contract](https://raw.githubusercontent.com/csmith-project/creduce/master/creduce/creduce.in), [llvm-reduce exit status](https://llvm.org/docs/CommandGuide/llvm-reduce.html)).

## Spend reduction compute on trustworthy improvements

Keep separate per-attempt and whole-job limits, worker/resource use, invalid/unresolved attempts and useful size or readability improvements. Native controls have different scopes: libFuzzer documents a total-time crash-reduction limit; Go's minimization setting applies to each attempt ([libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options), [Go custom settings](https://go.dev/doc/security/fuzz/)). Choose actual limits from the authorized task, not universal numbers.

When replay changes, investigate missing state, prior inputs, uncontrolled choices and environment before accepting the smaller case. Hypothesis documents that external state or changing visible outcomes can prevent reliable replay and shrinking ([flaky failures](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html)). Preserve observed trials and partial results; no fixed retry count proves continuity. For practical dependent-world, schedule and recovery examples, read [worked reductions](references/worked-reductions.md).

## Complete the reduction

Replay original and reduced artifacts under the retained guarantee and configuration. State the preserved witness, changed identities and any uncertainty about common cause. Return artifact paths, actual commands/limits, chosen size metric, transformations attempted, final replay results and stopping reason. A deletion-fixed point is relative to its predicate and moves; it is not an absolute smallest case ([Delta Debugging, minimality](https://www.debuggingbook.org/html/DeltaDebugger.html)). Keep a useful partial reduction when the budget or observability ends.

Use the project's regression conventions for a confirmed reproducer; do not rely only on a version-sensitive opaque replay blob ([Hypothesis replay](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)). Read [common mistakes](references/common-mistakes.md) when reduction appears successful but changes the evidence. Invocation does not enlarge authorization to edit targets, install tools or publish findings.
