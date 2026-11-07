# Replay and reduction

## Retain the execution bundle

Keep original setup/world, input/workload, code/build/configuration, controller version/features, policy/bounds, controlled choices and raw observer/witness. CHESS leaves important input/initial-state reconstruction to the test environment; schedule capture alone does not replay successful external reads: "when the call succeeds CHESS does not log the contents of the file read" ([CHESS, §3.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

Exercise the actual saved trace/checkpoint under the same controller. Record reproduced, clipped, unsupported and uncontrolled outcomes separately. Shuttle replay explicitly requires no other nondeterminism, and Coyote iteration state is shared unless reset: "the iterations run in shared memory" ([Shuttle replay](https://docs.rs/shuttle/0.9.10/shuttle/fn.replay.html), [Coyote, Test entry point](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/using-coyote.md)).

## Reduce workload and choices together

This pack's reduction adaptation is: remove irrelevant work, then regenerate/revalidate feasible decisions through the existing controller and re-evaluate the same contract witness. Deleting an operation can change identity/enabledness and ordinal decisions; do not assume the old step numbers retain their meaning. CHESS labels each event with "a task, a synchronization variable, and an operation" and records the thread scheduled at each point "together with the set of threads enabled" ([CHESS, §§3.3–3.4, 4.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). Use `failure-reduction` for reducer selection and continuity mechanics.

Illustrative case: shrinking a validation/publication workload removes the object setup and now triggers an unrelated missing-object assertion. Retain the original and reject that case as a reduction of the selected state/history violation. If cause is unknown, claim observed witness continuity rather than identical root cause. No generic cross-runtime trace reducer is supplied.

## Interpret partial progress

A bound crossing is an exploration observation. Check the real fairness/progress promise before calling it starvation or deadlock; CHESS's fair scheduler is guaranteed not to miss safety errors only "Under the condition that a thread yields only when it is unable to make progress" ([CHESS, §4.3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). Route liveness-contract interpretation to `liveness-testing`.

Example: Shuttle reaches a step cap while one task never receives service. Preserve its choices and cap outcome; do not convert it to a proven application hang or a successful completed execution. Its time limit cannot interrupt the iteration ([steps](https://docs.rs/shuttle/0.9.10/shuttle/enum.MaxSteps.html), [time limit](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html)).
