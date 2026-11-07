# Worked campaign: from valid programs to observable effects

This is an illustrative decision record, not a reported experiment or a finding against a real product. Its frontier is motivated by SQLite's joint state/input fuzzing and Elle's informative observation design ([SQLite §2](https://www.sqlite.org/testing.html), [Elle §3](https://arxiv.org/abs/2003.10554)).

## Given baseline and request

Suppose source inspection establishes that an interpreter project already has valid-IR source generation, cross-engine compilation/result/error comparison, persisted-bytecode mutation and transaction history checks. The current VM lane creates an empty world; its generated operations often fail before exercising an object permission transition. The user authorizes a finite discovery budget on disposable test state.

Do not propose valid-IR generation or basic cross-engine comparison as new capability. Read the actual permission contract, world-creation producer and effect-observation APIs. Confirm the apparent omission in the target revision before treating it as the experiment's premise. This applies reachability diagnosis rather than substituting guessed behavior ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)).

## Candidate pilot

Write a compact record using the project's existing artifact convention:

```text
Target/config: inspected interpreter and reference builds; named core capabilities
Gap: successful permission-dependent effects are not exercised by the current lane
Contract: cite the precise documented permission/effect guarantee
Input: initial world + generated operation sequence; retain both
Oracle: permitted/denied outcome and relevant before/after world effects
Comparison: equivalent per-case starting states in both implementations
Control: a known or independently justified violation of this same contract
Budget: use a tranche of the user's finite envelope; include replay/triage time
Replay: original world, operations, exact builds/options and raw outcomes
```

The oracle must distinguish legal errors and intended implementation differences from wrong effects. More histories do not supply missing observations automatically; Elle's dependency inference depends on the recorded information ([Elle §§3 and 4.3](https://arxiv.org/abs/2003.10554)). Delegate detailed stateful generation and semantic comparison to their owners.

## Three possible pilot outcomes

1. **The operation is still almost never reached.** Preserve accepted-operation counters and inspect the generator's prerequisites. Spend the next tranche improving the state/operation relation, rather than multiplying identical workers. Joint state/input search is a mechanism worth testing, not a guaranteed source of bugs ([SQLite §4.1.3](https://www.sqlite.org/testing.html)).
2. **A repeatable wrong effect appears.** Preserve the original world, sequence, outputs and builds; allocate to reproducing and reducing that candidate with the same oracle. Keep the minimized case alongside the original. Reproduction depends on the actual testcase and compatible instrumentation/configuration ([OSS-Fuzz reproduction](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)).
3. **Deep effects are reached but no violation appears.** Report a useful bounded negative result. Continue only if remaining search and budget justify it, or pilot another evidence-backed dimension. Do not call the target correct or the new lane superior. Comparative claims require observations under matched conditions, with variation visible ([FuzzBench report](https://google.github.io/fuzzbench/reference/report/)).

## Close the record

Report actual consumed resources and property reach, candidate classifications and evidence paths, the decision on the remaining budget, and untested states/behaviors. If a failure is intermittent, retain its conditions and reproduction attempts; ClusterFuzz records reliability and platform/job distinctions for this reason ([ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).

The useful output is an executable experiment with a stated observation and a reasoned next allocation. Merely producing this proposal is not evidence of discovery power. Evaluate the skill on isolated raw artifacts without revealing the intended defect or forcing this particular method.
