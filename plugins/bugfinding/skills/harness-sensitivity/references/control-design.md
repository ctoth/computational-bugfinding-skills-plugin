# Control design and interpretation

Use this reference when a new harness appears healthy but its ability to detect the promised violation is unknown. The examples below are illustrative experiment designs, not observed product defects.

## Choose a discriminating control

Write the actual producer, configuration, guarantee and forbidden effect beside the proposed control. Prefer a known regression whose failure has been isolated to the relevant change. Historical fault studies exclude unrelated changes and nondeterminism precisely because those can contaminate the comparison: Just et al. discard failing tests such as "dependent tests" or "non-deterministic tests" that "do not expose a real fault", and isolate fixes because "unrelated changes could affect the outcome" ([Just et al., §§2.2.2–2.2.3](https://doi.org/10.1145/2635868.2635929)).

For a new effect oracle, choose a control that changes the effect while leaving easy checks intact. For example, suppress a required committed update while preserving the returned success value. Establish this behavior from the actual source and contract; do not assume an arbitrary mutation has the intended consequence. Common mutation operators do not represent every context, algorithm or invariant defect; "Mutation analysis is context insensitive, while bugs can be context sensitive" ([Just et al., §3.2](https://doi.org/10.1145/2635868.2635929)).

### Known-defect sources for JavaScript

These sources were checked on 2026-11-09; none was built or run for this skill.

- **BugsJS** (MIT, "Number of Bugs: 453", 10 Node.js projects, of which ESLint has 333) provides three revisions per bug: `buggy`, `fixed-only-test-change` ("only the tests introduced in the bug fixing commit, applied to the buggy revision") and `fixed`. The second and third give a faulty and a healthy case under the same fault-revealing test ([BugsJS README](https://raw.githubusercontent.com/BugsJS/bug-dataset/7abbad3e4df12cd5294110bb5db11b7d5bc758a6/README.md), [LICENSE](https://raw.githubusercontent.com/BugsJS/bug-dataset/7abbad3e4df12cd5294110bb5db11b7d5bc758a6/LICENSE), [Versions.txt](https://raw.githubusercontent.com/BugsJS/bug-dataset/7abbad3e4df12cd5294110bb5db11b7d5bc758a6/Versions.txt), [Projects.csv](https://raw.githubusercontent.com/BugsJS/bug-dataset/7abbad3e4df12cd5294110bb5db11b7d5bc758a6/Projects.csv)). Limits: the 10 listed Node.js projects only, none of them React, and its Docker image starts `FROM node:8.16-jessie` ([BugsJS Dockerfile](https://raw.githubusercontent.com/BugsJS/docker-environment/252cf8d79f0d0ecc9a80afc518f7e7d4b7ae6400/env/Dockerfile)); confirm the selected bug builds and fails as claimed before using it.
- **sola-da/ReDoS-vulnerabilities**, the benchmark released with Staicu and Pradel's ReDoS study ([Staicu and Pradel 2018, p.362](https://www.usenix.org/conference/usenixsecurity18/presentation/staicu)), lists 23 vulnerable npm modules with bug reports and, for 14 of them, advisories ([README](https://raw.githubusercontent.com/sola-da/ReDoS-vulnerabilities/ccb8d7dc74fd9cff835b47548bdffb7c010bb60f/README.md)). The vulnerable version is the faulty case; for modules marked FIXED, the fixed release is the healthy case, and modules without a fix have no healthy counterpart. Each exploit script runs each crafted input once and prints its execution time, with no assertion or threshold ([test-forwarded.js](https://raw.githubusercontent.com/sola-da/ReDoS-vulnerabilities/ccb8d7dc74fd9cff835b47548bdffb7c010bb60f/test-forwarded.js)), so the harness must supply the decision rule; `resource-complexity-testing` owns it. The repository has no license file; its scripts carry an MIT-style header, and its GitHub description says the resources are "provided for research purpose only" ([GitHub repository metadata](https://api.github.com/repos/sola-da/ReDoS-vulnerabilities)).
- **NodeCB** ([Wang et al. 2017](https://doi.org/10.1109/ASE.2017.8115663)): the dataset URL given in the paper (p.2) returned HTTP 404 on 2026-11-09, and its last archived page offered the data "only for teaching and research purposes" behind a contact form ([Wayback snapshot 2022-12-07](http://web.archive.org/web/20221207163016id_/http://www.tcse.cn/~wsdou/project/NodeCB/)). What remains is GitHub issue URLs for 22 of the 57 bugs in the paper's references (p.11). Each is a pointer, not a control: build the buggy and fixed revisions and a failing test from the report first.

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
