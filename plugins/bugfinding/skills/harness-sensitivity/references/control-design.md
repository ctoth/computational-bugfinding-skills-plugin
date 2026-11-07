# Control design and interpretation

Use this reference when a new harness appears healthy but its ability to detect the promised violation is unknown. The examples below are illustrative experiment designs, not observed product defects.

## Choose a discriminating control

Write the actual producer, configuration, guarantee and forbidden effect beside the proposed control. Prefer a known regression whose failure has been isolated to the relevant change. Historical fault studies exclude unrelated changes and nondeterminism precisely because those can contaminate the comparison: Just et al. discard failing tests such as "dependent tests" or "non-deterministic tests" that "do not expose a real fault", and isolate fixes because "unrelated changes could affect the outcome" ([Just et al., §§2.2.2–2.2.3](https://doi.org/10.1145/2635868.2635929)).

For a new effect oracle, choose a control that changes the effect while leaving easy checks intact. For example, suppress a required committed update while preserving the returned success value. Establish this behavior from the actual source and contract; do not assume an arbitrary mutation has the intended consequence. Common mutation operators do not represent every context, algorithm or invariant defect; "Mutation analysis is context insensitive, while bugs can be context sensitive" ([Just et al., §3.2](https://doi.org/10.1145/2635868.2635929)).

Keep the control's activation scoped to the owned test experiment. Existing project controls and historical checkouts can suffice; a new fault-injection framework is not required. Preserve the healthy case, actual faulty case and exact observation that distinguishes them. These are audit recording choices, not a prescribed storage format.

## Find the first missing observation

Use the table to decide what evidence to obtain next. Its rows are this skill's audit convention. They split the paper's two relations, covering a mutant ("reaches and executes the mutated code") and detecting it, with activation and state steps between ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)). Static reachability and observed coverage provide different evidence too ([Fuzz Introspector overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)).

| Observation | Supported conclusion | Next useful work |
|---|---|---|
| Intended producer is unreachable in this lane | Claimed behavior has not been exercised | Inspect the existing entrypoint, capability/configuration and setup state. |
| Producer runs; control activation is unknown | Source coverage alone does not establish the selected fault occurred | Inspect the selected control/build and its activation evidence. |
| Control is active; relevant state does not change | Control may be irrelevant, equivalent or missing a prerequisite | Establish the input/state in which the contract-relevant change occurs. |
| Relevant state changes; checker sees the same observation | The observation may omit the effect, or the effect may be outside its promise | Compare the actual guarantee and observer boundary. |
| Intended oracle rejects the fault and accepts the healthy case | Sensitivity to this representative violation under these conditions | Preserve replay evidence and state the bounded conclusion. |
| A watchdog fires before the intended effect assertion | Completion failed; effect-oracle sensitivity is unestablished | Diagnose progress and the actual rejecting mechanism. |
| Mutant fails to build/load, runner fails or evidence is malformed | The intended comparison did not complete | Repair the experiment's verified defect. |
| Checker outcome is unknown | The claimed violation has not been decided | Preserve missing observations and checker limits. |
| Healthy and faulty cases both fail | Useful discrimination has not been established | Diagnose baseline health, preconditions and the rejecting check. |

Do not infer outcome from exit status alone when the intended result requires a particular assertion or witness. In particular, tools may classify timeouts as detected mutations while compile/runtime errors fall outside their score: Stryker counts a timeout as "detected" and says of runtime and compile errors "It is not represented in your mutation score" ([Stryker mutant states and metrics](https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a4f816358a06701b7680d54bbb56180c19781c25/docs/mutant-states-and-metrics.md)).

## Worked example: returned success hides a world effect

Suppose two execution lanes compare only printed outcomes, while their documented contract also promises an object update. Establish equivalent initial worlds and successful execution of the update. Use an existing regression or a justified control that suppresses that update while preserving printed success.

Save both post-states and comparator observations. If the state differs but the comparator accepts the cases, record that the effect was unobserved. Improve the existing comparator only for the promised effect, then replay the same healthy/faulty pair. The new rejection demonstrates that specific observation now discriminates this case; it does not establish equivalence of every possible effect. The experiment applies this skill's State and Observation steps; the paper supports only the coarser point that executing a fault is not detecting it ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)). The target's own contract supplies the promised update.

## Worked example: recovery after acknowledgment

First establish a real documented durability guarantee and its failure model. Use a disposable target and a known lost-update regression or an authorized narrow control at the actual persistence boundary. Save the acknowledged operation, fault point, recovery evidence and recovered-state observation.

The intended discriminator is the promised recovered state, not the fact that a process died. If a harness stops at the expected crash, the recovery assertion was never evaluated. Require the same healthy and faulty sequence to reach recovery and distinguish the promised state. Treat this as an experiment design until the actual target contract, fault model and execution support it; `crash-consistency-testing` owns those details.

## Bound the conclusion

Report sensitivity to the selected representative faults and conditions. Keep unresolved controls visible rather than fold them into a pass percentage. Real-fault research supports useful relationships with mutation detection while documenting faults missed by common operators; it does not establish completeness or a bug-yield forecast for another target. The paper's own conclusion warns that test selection, minimization and prioritization evaluated on mutants "might lead to a reduced real fault detection rate of the test suite, even if the mutation score does not decrease" ([Just et al., §§3.2 and 5](https://doi.org/10.1145/2635868.2635929)).
