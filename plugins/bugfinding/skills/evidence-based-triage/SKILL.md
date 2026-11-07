---
name: evidence-based-triage
description: Triages computational bugfinding candidates into evidence-backed findings, harness defects, expected behavior or unresolved cases. Use when interpreting fuzz, sanitizer, differential or history failures, grouping duplicates, investigating flaky replay, or using an LLM to prepare maintainer findings.
---

# Evidence-based triage

Turn retained observations into a finding another maintainer can assess. Keep **disposition, reproduction and cause** separate: authentic failure evidence can remain unresolved, and a demonstrated contract violation need not have an established root cause. Use the project's existing records rather than introduce a verdict database ([ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).

## Preserve before interpreting

Locate the real producer, original input and raw failure. Retain build/configuration, architecture, instrumentation, invocation and relevant limits; keep starting state, prior operations and controlled choices where the failure depends on them. Link original and reduced artifacts separately. Matching a testcase's sanitizer and architecture can be necessary for replay ([OSS-Fuzz reproduction](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)); in-process failures may depend on earlier inputs or persistent threads ([libFuzzer limitations](https://llvm.org/docs/LibFuzzer.html#q-when-libfuzzer-is-not-a-good-solution-for-a-problem)).

Do not replace raw evidence with an LLM summary. Record which conclusion came from which checker, classifier, source inspection or actual replay. In the inspected OSS-Fuzz-Gen analyzer, `true_bug` is assigned from an LLM conclusion tag; that boolean is not a second, independent observation ([analyzer source](https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/crash_analyzer.py)).

## Audit the claimed violation

1. **Establish the contract and legal producer.** Read the actual API/language guarantee, enabled configuration and calling path. Check generated harness preconditions before attributing its failure to the product. For example, a compiler disagreement on an undefined program does not establish miscompilation ([LLVM reporting](https://llvm.org/docs/HowToSubmitABug.html#miscompilations)). Use `correctness-oracles` and the relevant differential/history specialist for their interpretation rules.
2. **State the narrow observation.** Separate a returned wrong value, invalid access or supported history contradiction from hypotheses about its mechanism or impact. Elle's inference relies on observable information and has stated model limits; preserve the witness and assumptions ([Elle, §§4.3, 6 and 9](https://arxiv.org/abs/2003.10554)).
3. **Read actual replay results.** Preserve attempts, conditions and outcomes. If a fresh-process replay misses, investigate configuration, initialization, prior-input sequence and uncontrolled events. Do not silently discard the original trace or count the case as a confirmed unique defect ([ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/), [libFuzzer limitations](https://llvm.org/docs/LibFuzzer.html)).
4. **Choose the supported disposition.** Distinguish demonstrated product violation, harness/input/oracle defect, documented expected behavior, evidenced infrastructure cause, and unresolved evidence. A fuzzer failure can originate in the test; a timeout can also reflect intended behavior ([Go fuzzing, Failing input](https://go.dev/doc/security/fuzz/#failing-input)). Keep reproduction and root-cause status alongside that disposition.

For conditional investigations and worked cases, read [triage decisions](references/triage-decisions.md). This is triage, not authority to fix targets or post findings.

## Spend LLM effort on checkable work

Supply the actual artifacts and relevant source/contract sections. Ask for a narrow observation, missing evidence, and the next permitted check that would distinguish explanations. Verify cited locations and actual tool results before adopting the explanation. Tool use alone does not validate a conclusion: the OSS-Fuzz-Gen analyzer checks debugger use and parses a verdict, which remain different operations ([analyzer source](https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/crash_analyzer.py)).

Keep provisional symptom groups to amortize investigation, preserving every member's input and outcome. A stack signature is a grouping aid, not proof that every member has one cause. Mark duplicates only when evidence connects them. If reduction changes the violation, retain both candidates and use `failure-reduction` for the reduction mechanics ([ClusterFuzz glossary, Crash state and Minimization](https://google.github.io/clusterfuzz/reference/glossary/)).

## Return a usable finding

Return the observable trigger, governing guarantee, expected/actual behavior, artifact paths, actual replay history, disposition, supported user effect, cause status and remaining uncertainty. Read [maintainer handoff](references/maintainer-handoff.md) for a compact example. Include exact invocation and reduced testcase when available; do not invent a successful replay or require a fix before recording evidence ([LLVM reporting](https://llvm.org/docs/HowToSubmitABug.html)).

Finish with the next useful action or a reasoned unresolved result. Report confirmed causes separately from candidates and provisional groups. Use `bugfinding-campaign` to decide whether remaining compute belongs in triage or further generation. For shortcuts that lose real evidence, read [common mistakes](references/common-mistakes.md).
