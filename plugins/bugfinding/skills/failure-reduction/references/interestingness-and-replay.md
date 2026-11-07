# Interestingness and replay

## Define what survives

Keep the original and reduced artifacts separately. Describe the selected contradiction, its legal-input/setup conditions and observable witness. A recognizable symptom is useful but cannot generally prove identical root cause; compiler wrong-code cases are an explicit example: unlike crash strings, "wrong-code bugs have no obvious fingerprint" ([Regehr et al., §7.7](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

Use this pack's working convention for an interestingness result:

| Observation | Reduction action |
|---|---|
| Required setup and operation execute; selected contradiction remains | Candidate may replace the current best after required replay evidence |
| Healthy behavior under the selected check | Reject this move |
| Domain or setup invalid; checker cannot decide | Retain the reason separately; do not accept as the chosen failure |
| A different genuine violation appears | Preserve it as another candidate; do not silently substitute it |

This convention preserves information beyond a binary exit code. A concrete precedent is delta debugging's PASS/FAIL/UNRESOLVED distinction, where an outcome "different from the original failure" is `UNRESOLVED` rather than a failure ([Delta Debugging, generic_test](https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb)). C-Reduce's `--also-interesting` exit code is a native way to save the different-violation row's variant ([C-Reduce options](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in)). It requires no new schema or reducer framework.

## Reduce dependent material together

The following are method adaptations. Establish each transformation through the target's actual producer/replay interface; no generic world or schedule reducer is implied.

| Material | Useful moves | Condition to retain |
|---|---|---|
| Program and initial world | Remove unused entities/declarations and dependent uses; simplify values through existing IR | Selected operation remains reachable with valid identities, permissions and state |
| API operations | Remove blocks and their dependent uses; simplify model-supported arguments | Legal lifetime/sequence and selected result/effect relation |
| Workload and schedule | Remove irrelevant operations with their matching decisions | Controller can replay remaining decisions and expose the same contract violation |
| Recovery workload and faults | Remove unrelated work/faults using recorded event identity | Relevant acknowledgment, fault boundary and recovered-state discrepancy |
| Resource/numerical family | Simplify parameters while retaining the measured regime | Original growth/error contract and matched observations |

Use `stateful-property-testing`, `semantic-program-generation`, `schedule-exploration`, `crash-consistency-testing` or the relevant oracle owner for representation-specific validity. Shrink construction decisions through the existing producer where supported; replay the resulting artifact rather than assuming a smaller decision stream preserves behavior. In Seq-Reduce, changes near the start of a decision sequence "tend to perturb Csmith's internal state" ([Regehr et al., §6.1](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

## Resolve unstable observations

Inspect actual source/build/options, initialization, prior operations and controlled schedule/fault choices. Preserve original and reduced trial outputs. Hypothesis specifically identifies unreset filesystem/database state, global state and unmanaged randomness, including "thread scheduling, network timing", as flakiness sources; "Only the sequence of calls to Hypothesis APIs" such as `draw` and the pass/fail outcome need to be deterministic, not hidden implementation events ([Hypothesis flakiness](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/flaky.rst)).

Use an existing replay seam when available. If the missing behavior remains uncontrolled, report the smallest actually reproduced case and its uncertainty. Do not quietly cache a flaky verdict as deterministic or change resource limits just to keep a candidate failing. This is the pack's evidence policy, not a universal statistical acceptance threshold.
