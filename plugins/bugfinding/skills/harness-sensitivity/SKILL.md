---
name: harness-sensitivity
description: Audits whether a bugfinding harness reaches its claimed behavior and rejects representative violations through the intended oracle. Use when validating a new fuzz target, effect or recovery check, interpreting surviving mutants, or diagnosing high coverage with uninformative results.
---

# Harness sensitivity

Determine what a representative fault actually demonstrates before expanding search. Execution coverage, changed state and rejection by an assertion are separate observations; mutation tools also report outcomes that do not establish semantic detection ([PIT concepts](https://pitest.org/quickstart/basic_concepts/), [Just et al., §§2.5–3.2](https://doi.org/10.1145/2635868.2635929)).

## Select the claim and a relevant control

Read the actual producer, enabled configuration, assertion and guarantee. Identify the promised result or effect and the evidence its oracle must expose. For general contract design use `correctness-oracles`; this audit checks whether the implemented experiment can distinguish a representative violation. Reachability and observed execution can differ even within a fuzz suite ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)).

Prefer an existing historical regression or fault switch that exercises that guarantee. Confirm the historical failure is attributable to the defect rather than unrelated revision changes. When a new control is necessary and authorized, derive it from the real producer and violated contract; a syntax error or broken setup is not a substitute for the intended wrong effect. Generic operators can miss algorithmic, contextual and invariant faults ([Just et al., §§2.1 and 3.2](https://doi.org/10.1145/2635868.2635929)).

Use the current harness and runner. Do not install a mutation framework merely to perform this audit. Where a compatible integration already exists, read [runtime integrations](references/runtime-integrations.md) for scoped PIT or Stryker execution and interpretation.

## Follow the fault to the intended oracle

Compare healthy and faulty cases under matched input, initial state and configuration. Record the first boundary unsupported by evidence. The following audit convention distinguishes execution, state change and observation rather than inferring them from line coverage ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929), [OSS-Fuzz integration](https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/)):

1. **Producer:** did the intended operation execute through the actual target path?
2. **Activation:** did the selected control become active in this execution?
3. **State:** did it change the contract-relevant result or state?
4. **Observation:** did that change reach the checker without being hidden or discarded?
5. **Rejection:** did the intended oracle report the violation with its expected evidence?

Use existing logs, snapshots, histories or focused observations to answer the missing question. Preserve the original healthy/faulty artifacts and control provenance; adding a second implementation or generic instrumentation layer is not the audit's default. Read [control design](references/control-design.md) for outcome interpretation and worked world-effect/recovery cases.

## Interpret the actual outcome

Report an inactive control, equivalent or irrelevant change, changed-but-unobserved effect, intended rejection, invalid experiment and inconclusive checker separately when they lead to different decisions. PIT explicitly distinguishes surviving, uncovered, invalid and runtime-failure outcomes ([PIT concepts](https://pitest.org/quickstart/basic_concepts/)).

Inspect the rejecting assertion or witness. Stryker includes timeouts in its detected count; that does not demonstrate that a separate value/effect assertion rejected the fault. If progress itself is the promised property, use its justified liveness oracle instead ([Stryker states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)). A healthy case rejected by the same setup also leaves discrimination unestablished.

Repair a verified reach, observation or checker defect in its existing owner when the task authorizes that change. Preserve the representative control when it protects the intended guarantee, and state exactly which cases it covers. Mutation evidence has documented limitations; no universal score or real-bug yield follows from a passing control ([Just et al., §§3.2 and 5](https://doi.org/10.1145/2635868.2635929)). For misleading shortcuts, read [common mistakes](references/common-mistakes.md).

## Complete the audit

Return the producer and cited guarantee, healthy/faulty execution identities, control provenance, observed boundaries, intended-oracle result and witness paths. State the narrow sensitivity conclusion and unresolved boundary; use the project's report format rather than a new required schema. Route retained candidates to `evidence-based-triage` and the next compute allocation to `bugfinding-campaign`.

Keep the audit proportional to the new experiment. It does not introduce a recurring approval round, prescribe a mutation percentage, or authorize target edits, tool installation or external publication by invocation alone.
