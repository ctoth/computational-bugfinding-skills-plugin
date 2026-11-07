---
name: transactional-history-testing
description: Generates informative transaction histories and checks isolation guarantees with Elle. Use when searching for transactional anomalies, extending an existing history checker, or investigating recorder boundaries, uncertain outcomes and missing dependency evidence.
---

# Transactional history testing

Choose a promised isolation model and observations that can refute it. Append traces reveal version order that overwritten registers can hide; more transactions cannot recover information never observed ([Elle, §3](https://arxiv.org/abs/2003.10554)). Read [observable dependencies](references/observable-dependencies.md) when choosing the workload.

## Establish the actual transaction boundary

Read the public producer, effective mode, initial state, retry path and publication points. Keep logical requests, physical attempts and committed transactions distinct. Jepsen histories distinguish successful, definite no-effect and indeterminate outcomes; a transport failure must not become a definite abort without supporting evidence ([history semantics](https://raw.githubusercontent.com/jepsen-io/history/main/README.md)). Use [history and boundaries](references/history-and-boundaries.md) for mapping and controls.

Preserve micro-operation order, write provenance and the selected frontend's assumptions. List-append checks validate allowed operations and unique append invocations; register inference has different initial-state and order assumptions ([append validation](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj), [register inference](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj)). Validate conversion through the real recorder, with a healthy case and a justified violation; use `harness-sensitivity` for that experiment.

## Search a missing observation or interaction

Inventory existing workloads before adding another lane. If ordinary concurrent transactions and recorder controls already exist, investigate an uncovered guarantee or dependency: supported session/realtime order, exposed version provenance, short/long key lifetimes, or a predicate-aware observation. Require the actual contract and a compatible analyzer; the 2020 paper's predicate exclusion does not establish the limits of every newer extension ([Elle, §§5 and 9](https://arxiv.org/abs/2003.10554), [current model mapping](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/consistency_model.clj)).

Vary contention, read/write patterns, transaction lengths and lifetimes according to useful observed dependencies, not raw transaction count. Existing Elle generators expose key distributions and write lifetimes; keep generator choices and admitted/committed operations visible ([transaction generation](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj)). Use `stateful-property-testing` for dependent operations and `schedule-exploration` for controlled choices.

## Run and interpret the selected checker

Read [Elle operation](references/elle-operation.md) for an existing JVM/CLI integration, exact option scope, artifact dependencies and result handling. Select the actual promised model: serializability alone omits realtime and session order, while strict serializability adds realtime constraints ([serializable](https://jepsen.io/consistency/models/serializable), [strong serializable](https://jepsen.io/consistency/models/strong-serializable)).

Require analysis of the requested history and an explicit verdict. A CLI exit code can include unknown-only results; retain structured anomalies and witness explanations. Per-component search and plotting limits do not bound the entire process ([CLI source](https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj), [analysis results](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj)). Account execution, conversion, analysis and rendering separately within `bugfinding-campaign`'s authorized budget.

## Return inspectable evidence

Preserve original events, converted history, selected model/checker/build/configuration, raw verdict, dependency witness and actual replay attempts. Explain the contradiction from observed operations and justified edges; a cycle does not establish root cause or durability loss ([Elle, §6](https://arxiv.org/abs/2003.10554)). Reduce only while retaining boundaries, provenance, uncertainty and the same supported anomaly; route reduction and attribution to `failure-reduction` and `evidence-based-triage`.

Return the guarantee tested, reached workload/dependency shapes, actual costs, explicit outcomes, witness paths and untested dimensions. For false-finding traps, read [common mistakes](references/common-mistakes.md). Invocation preserves the user's existing execution and publication authority.
