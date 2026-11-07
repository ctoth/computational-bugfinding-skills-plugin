---
name: distributed-fault-testing
description: Searches real distributed deployments for correctness bugs under network, process and clock faults. Use when extending a Jepsen-style campaign, testing failover or recovery, or investigating whether injected faults and ambiguous requests were represented faithfully.
---

# Distributed fault testing

Choose a promised result or effect that a real deployment can violate during failure or recovery. Jepsen combines a target client, workload generator, nemesis and history checker; an outage or performance plot is not itself a consistency counterexample ([architecture](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

## Establish the executable experiment

Read the actual target adapter, operation/acknowledgment contract, enabled read/durability mode and checker. Keep known acknowledgments, definite no-effect failures and uncertain requests distinct; Jepsen's timeout wrapper returns `:info`, not a known abort ([history semantics](https://raw.githubusercontent.com/jepsen-io/history/61d2776c889ad84f7c6922977cf05e8f11970402/README.md), [client source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj)).

Use an existing fitting integration and owned disposable nodes. Check the selected build, dependencies, host requirements and actual runner options in [Jepsen operation](references/jepsen-operation.md). Do not substitute framework names for a working target client and oracle; node operations can alter firewalls, processes and clocks ([environment](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

## Search an actual failure boundary

Inventory the baseline first. If concurrent histories and injected checker controls already exist, choose an additional real deployment boundary: acknowledged-write failover, a lease holder paused past ownership change, asymmetric communication, or an applicable recovery transition. Treat these as target-specific hypotheses, not generic bug claims; [fault model and activation](references/fault-model-and-activation.md) develops the experiments.

Specify affected nodes/roles/links, directions and timing relative to meaningful operations. Select faults supported by the target adapter; combined nemesis packages pair generators with final repair generators and depend on implemented database protocols ([combined nemesis](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

Observe fault activation independently of the request log, then observe healing. Jepsen 0.3.15 documents a fixed helper bug that made some earlier kill/pause/resume faults no-ops; a named nemesis event cannot establish that the intended fault occurred ([historical incident](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md)).

## Execute through recovery and the oracle

Budget setup, calls, load, healing, final observations, analysis and teardown separately. Generator time limits stop operation emission; CLI load duration excludes setup/teardown, and a seed does not guarantee replay of real timing/responses ([generator](https://raw.githubusercontent.com/jepsen-io/generator/3073ba45cb3db0b6dcc5aa915907a2e67b04eef5/src/jepsen/generator.clj), [CLI](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj)).

Use the target's final repair and observation phases. The etcd producer heals before final workload reads; its fixed recovery sleep is an implementation choice, not proof another target has converged ([real producer](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj)). Read [recovery and evidence](references/recovery-and-evidence.md) before teardown.

Inspect explicit checker and subchecker results, admission and witnesses. Checker exceptions can become `:unknown`; a false sub-result dominates unknown in composition ([checker source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/checker.clj)). Use `linearizability-checking` or `transactional-history-testing` for the promised history model, `crash-consistency-testing` for storage-failure semantics, and `deterministic-simulation` for controlled environment replay.

## Finish with retained evidence

Return the tested guarantee, actual activated faults/topology, reached successful operations, uncertain outcomes, recovery observations, explicit verdict/witness, resource use and artifact paths. Preserve source/build/configuration, raw history and actual replay attempts; traceable observations enable inspectable contradictions but have model limits ([Elle, §§3, 4.3, 6 and 9](https://arxiv.org/abs/2003.10554)).

Use `failure-reduction` to shrink workload and fault sequence while retaining the same violation; use `evidence-based-triage` for attribution and `bugfinding-campaign` for further allocation. Read [common mistakes](references/common-mistakes.md) when requested faults, completed reads and checked guarantees diverge. Invocation preserves existing execution and publication authority.
