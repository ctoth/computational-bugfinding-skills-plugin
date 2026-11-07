---
name: deterministic-simulation
description: Guides reproducible fault search using existing production-code simulators and supported translated runtimes. Use when exploring interacting machine, network, storage and timing failures, choosing a fitting simulation seam, or reproducing a simulated counterexample.
---

# Deterministic simulation

Choose a supported execution model, then search state, workload and environmental choices with a real correctness oracle. FoundationDB runs database code under simulated network/disk/time/randomness, while its paper explicitly separates local, workload and recoverability checks ([FoundationDB, §4, pp. 8-9](https://www.foundationdb.org/files/fdb-paper.pdf)).

## Establish the controlled boundary

Read the real producer, enabled configuration and promised behavior. Map relevant scheduling, time, randomness, networking, disk, process lifecycle and dependencies to controlled, native or unsupported paths. A top-level simulator wrapper does not establish coverage of every dependency: FDB excludes non-Flow code and third-party components in its stated model ([FoundationDB, §4 limitations](https://www.foundationdb.org/files/fdb-paper.pdf)). Use [boundaries and oracles](references/boundaries-and-oracles.md) before selecting a route.

Use an existing fitting production-code seam; do not implement another system or retrofit a universal simulation layer. For compatible Go targets, [the selected Gosim route](references/gosim-route.md) translates application/dependency source with a restricted compiler and environment contract ([Gosim source loading](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/internal/translate/load.go)). For target-embedded or hosted environments, read [other routes](references/other-routes.md); their controls are not interchangeable.

## Search the missing interaction

Pair a small meaningful state/workload with the target's result, effect, recovery or progress assertion. Vary faults and topology according to semantic reach: excessive faults can trap FDB in a small state-space, while TigerBeetle's continuously healing safety regime missed persistent liveness failures ([FoundationDB, §4 p. 9](https://www.foundationdb.org/files/fdb-paper.pdf), [TigerBeetle, Teaching the VOPR](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). Use [fault design and replay](references/fault-design-and-replay.md) for a concrete experiment.

Record admitted setup, controlled operations, intended state/effect reached, assertion evaluations, recovery observations, unsupported outcomes and total resource cost. A simulator's virtual-time acceleration is not a performance prediction; retain separate native performance/OS/dependency evidence ([FoundationDB, §4 limitations](https://www.foundationdb.org/files/fdb-paper.pdf)). Route general allocation to `bugfinding-campaign`, observation design to `correctness-oracles`, and representative controls to `harness-sensitivity`.

## Replay and interpret

Preserve actual initial state or prefix, workload, source/build/compiler/configuration, environmental choices, fault parameters, raw trace and witness. Seed identity is model-specific: VOPR couples its seed to a commit, and Gosim exposes BuildDigest and ReplayRevision ([VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/docs/internals/vopr.md), [Gosim RunInfo](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/rt/info.go)).

Replay with compatible identity before reducing state/workload/faults together. A changed crash model or graceful restart changes the experiment; Gosim implements graceful and crash stops as distinct requests ([machine controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/machine_sim.go)). Use `failure-reduction` and `evidence-based-triage` for their independent mechanics. Preserve partial or unreproduced evidence; simulation agreement covers its model, not omitted real-world behavior ([FoundationDB, §4 limitations](https://www.foundationdb.org/files/fdb-paper.pdf)).

Return the tested guarantee, supported model and omissions, actual search/replay evidence, resource use, counterexample or bounded negative result, and next decision. Read [common mistakes](references/common-mistakes.md) when a tool invocation or replay claim exceeds its evidence. Invocation does not authorize installations, target rewrites, service submission, spending or publication.
