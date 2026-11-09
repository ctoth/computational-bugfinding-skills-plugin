---
name: harness-sensitivity
description: Audits whether a bugfinding harness reaches its claimed behavior and rejects representative violations through the intended oracle. Use when validating a new fuzz target, effect or recovery check, interpreting surviving mutants, or diagnosing high coverage with uninformative results, including JavaScript/TypeScript suites checked with c8 or NODE_V8_COVERAGE coverage, Node/Jest/Vitest test-order randomization, leaked async work or open handles (detectOpenHandles), StrykerJS, or known-defect sets such as BugsJS.
---

# Harness sensitivity

Determine what a representative fault actually demonstrates before expanding search. Execution coverage, changed state and rejection by an assertion are separate observations: a test covers a mutant if it "reaches and executes the mutated code", but detects it only when "a test assertion fails or the test causes an exception" ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)). Mutation tools also report outcomes that do not establish semantic detection ([PIT basic concepts, Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)).

## Select the claim and a relevant control

Read the actual producer, enabled configuration, assertion and guarantee. Identify the promised result or effect and the evidence its oracle must expose. For general contract design use `correctness-oracles`; this audit checks whether the implemented experiment can distinguish a representative violation. Reachability and observed execution can differ even within a fuzz suite; Fuzz Introspector compares each fuzzer's "static reachability potential" against "dynamic coverage" ([Fuzz Introspector overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)).

Prefer an existing historical regression or fault switch that exercises that guarantee. Confirm the historical failure is attributable to the defect rather than unrelated revision changes: "unrelated changes could affect the outcome" of a fault comparison ([Just et al., §2.2.3](https://doi.org/10.1145/2635868.2635929)). When a new control is necessary and authorized, derive it from the real producer and violated contract; a syntax error or broken setup is not a substitute for the intended wrong effect, and PIT reports a mutant that "could not be loaded by the JVM" as non viable, not killed ([PIT basic concepts, Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)). Generic operators can miss algorithmic, contextual and invariant faults; for those real faults "results derived from mutation analysis do not generalize" ([Just et al., §3.2](https://doi.org/10.1145/2635868.2635929)).

Use the current harness and runner. Do not install a mutation framework merely to perform this audit. Where a compatible integration already exists, read [runtime integrations](references/runtime-integrations.md) for scoped PIT or Stryker execution and interpretation, and for JavaScript coverage, test-order and open-handle probes with the project's existing runner.

## Follow the fault to the intended oracle

Compare healthy and faulty cases under matched input, initial state and configuration. Record the first boundary unsupported by evidence. The following steps are this skill's audit convention, not a published standard. They refine Just et al.'s two relations, covering versus detecting a mutant, so that detection is not inferred from line coverage ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)). The producer step follows OSS-Fuzz's requirement to check that a target "can make at least some progress" ([OSS-Fuzz ideal integration, Fuzz Target](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md)):

1. **Producer:** did the intended operation execute through the actual target path?
2. **Activation:** did the selected control become active in this execution?
3. **State:** did it change the contract-relevant result or state?
4. **Observation:** did that change reach the checker without being hidden or discarded?
5. **Rejection:** did the intended oracle report the violation with its expected evidence?

Use existing logs, snapshots, histories or focused observations to answer the missing question. Preserve the original healthy/faulty artifacts and control provenance; adding a second implementation or generic instrumentation layer is not the audit's default. Read [control design](references/control-design.md) for outcome interpretation and worked world-effect/recovery cases.

## Interpret the actual outcome

Report an inactive control, equivalent or irrelevant change, changed-but-unobserved effect, intended rejection, invalid experiment and inconclusive checker separately when they lead to different decisions. PIT reports separate outcomes, among them "**Survived**", "**No coverage**", "**Non viable**", "**Timed Out**" and "**Run error**" ([PIT basic concepts, Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)).

Inspect the rejecting assertion or witness. Stryker defines Detected as "`killed + timeout`", counting a timeout because "the tests will never complete" ([Stryker mutant states and metrics](https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a4f816358a06701b7680d54bbb56180c19781c25/docs/mutant-states-and-metrics.md)). That is a completion signal; it does not demonstrate that a separate value/effect assertion rejected the fault. If progress itself is the promised property, use its justified liveness oracle instead. A healthy case rejected by the same setup also leaves discrimination unestablished: Just et al.'s fault-revealing suite "fails on V1 [the faulty version] but passes on the fixed source code version" ([Just et al., §2.3](https://doi.org/10.1145/2635868.2635929)).

Repair a verified reach, observation or checker defect in its existing owner when the task authorizes that change. Preserve the representative control when it protects the intended guarantee, and state exactly which cases it covers. Mutation evidence has documented limitations; the study "reveals some inherent limitations of mutation analysis", and no universal score or real-bug yield follows from a passing control ([Just et al., §§3.2 and 5](https://doi.org/10.1145/2635868.2635929)). For misleading shortcuts, read [common mistakes](references/common-mistakes.md).

## Complete the audit

Return the producer and cited guarantee, healthy/faulty execution identities, control provenance, observed boundaries, intended-oracle result and witness paths. State the narrow sensitivity conclusion and unresolved boundary; use the project's report format rather than a new required schema. Route retained candidates to `evidence-based-triage` and the next compute allocation to `bugfinding-campaign`.

Keep the audit proportional to the new experiment. It does not introduce a recurring approval round, prescribe a mutation percentage, or authorize target edits, tool installation or external publication by invocation alone. PIT's own threshold option warns that "your build may contain equivalent mutations" ([PIT Maven, mutationThreshold](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/maven.markdown)).
