---
name: linearizability-checking
description: Checks concurrent operation histories against an executable sequential specification while preserving real-time order and uncertain outcomes. Use for linearizability models, Porcupine integration, history partitioning, or investigating a concurrent object counterexample.
---

# Linearizability checking

Select a real operation contract and check whether its observed concurrent history admits a legal sequential order consistent with real time. Establish object scope first; transaction isolation or race freedom does not supply this guarantee ([Jepsen model](https://jepsen.io/consistency/models/linearizable)).

## Build the experiment

Read the public operation producer, actual configuration, initial state and error/effect semantics. Build a small abstract model rather than port target internals. Keep transitions pure and state equality correct for backtracking; a partition is valid only when its checks are equivalent to the whole-history check ([Porcupine model](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go)). Read [model and history](references/model-and-history.md) before importing traces.

Retain genuine call/return ordering and matching identities. Preserve raw records alongside the converted history; completion-order sorting can erase overlap. Porcupine treats tied interval endpoints as concurrent and its event representation uses explicit matched IDs ([history contract](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go), [conversion source](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)).

Resolve pending or ambiguous observations through the target's permitted outcomes and the selected adapter/model. Do not turn a response timeout into a known no-op or fabricated success. Porcupine's example adapter completes pending calls with modeled unknown outputs; that is an application-specific construction, not automatic support for arbitrary unmatched events ([actual adapter](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go)). Keep evidence unresolved when its possibilities cannot be represented soundly.

Use known legal and contract-violating histories through the same recorder/model path to check discrimination; `harness-sensitivity` owns detailed controls. Include overlap, uncertainty and any cross-object operation the contract permits. Read [partitioning and cost](references/partition-and-cost.md): a global size operation can invalidate an otherwise useful per-key split ([P-compositionality, pp.5-6](https://arxiv.org/abs/1504.00204)).

## Execute the selected checker

For a compatible Go integration, read [Porcupine operation](references/porcupine-operation.md) for dependency/API selection, bounded checking and visualization. Retain `Ok`, `Illegal` and `Unknown` separately; timeout zero is unlimited. A completed accepted history covers that history and model, not unseen executions ([API](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go), [paper, pp.13-14](https://arxiv.org/abs/1504.00204)).

Allocate workload generation and checking separately. More overlap, operations and coupled keys can expand the checker's work; model cost and valid partitioning matter too. Record actual history size, partitions, limits, resource cost and completed result. A nominal timeout cannot interrupt a blocking model callback automatically; use supported cancellation and task-owned outer limits where needed ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)). `bugfinding-campaign` owns further compute allocation; `schedule-exploration` and `stateful-property-testing` own their search dimensions.

## Preserve the finding

Save raw/converted histories, initial state, model and adapter, checker/build/configuration, limits and actual result. Keep verbose partial-linearization evidence with any visualization; a picture is neither a minimal contradiction nor a root-cause proof ([visualization](https://raw.githubusercontent.com/anishathalye/porcupine/master/visualization.go)). Explain the contradiction from the contract and actual real-time edges, then use `evidence-based-triage` for attribution.

Reduce matched operations, setup and values while retaining their true ordering, uncertainty and selected violation; use `failure-reduction`. The paper's completed-history decision procedure does not supply a general liveness check ([paper, pp.3-5](https://arxiv.org/abs/1504.00204)). Read [common mistakes](references/common-mistakes.md) for invalid shortcuts.

Return the checked object guarantee, history/model scope, actual result and cost, witness/replay paths, and unresolved recorder/model assumptions. Follow the task's existing execution and publication authority.
