# Fault design and replay

## Spend compute on a discriminating environment

Start with a supported small workload and an observed property. FDB tunes fault distributions to avoid repeatedly collapsing into a small state-space; its swarm approach varies configuration, workloads and fault parameters rather than maximizing fault frequency ([FoundationDB, §4 p. 9](https://www.foundationdb.org/files/fdb-paper.pdf)). Record what rare semantic condition actually occurred, not only how many seeds ran.

For a progress guarantee, derive an environment in which the contract requires progress. TigerBeetle's liveness account heals a selected core and freezes failures elsewhere because eventual healing/restarts could erase the failure being sought ([Teaching the VOPR](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). Preserve that assumption with the witness; do not import it as every system's fault policy.

## Worked experiment: retained state after interruption

This is an illustrative design, not an executed finding. Given a compatible Go service with a documented acknowledgment/recovery guarantee, retain initial state and admitted operation, acknowledge it, induce a supported Crash or sync fault, then restart/restore using the actual model controls. Check recovered externally visible data. Keep an unchanged healthy case and a justified known violation through the same observer. Gosim's graceful/crash requests and bounded snapshots are distinct mechanisms; switching between them changes the premise ([machine controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/machine_sim.go), [crash-state controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/fs/recovery_sim.go)).

Vary a small real interaction, such as interruption around acknowledged state plus a supported asymmetric network partition. Preserve setup, sequence, fault parameters and witness; qualify any conclusion by the model. Gosim's public network controls support directed links, but unsupported packet controls cannot be presumed from another simulator ([network controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/net/control_sim.go), [features](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/features.md)). Detailed storage guarantees belong to `crash-consistency-testing`.

## Replay before interpretation

Keep source/build/compiler/configuration, initial state or causal prefix, workload, generated choices, environment/fault settings, raw trace, observer and actual replay results. VOPR defines replay with seed plus commit; Gosim publishes more detailed build/replay identity ([VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/docs/internals/vopr.md), [RunInfo](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/rt/info.go)). Changing only logging may be harmless in a particular design, but FDB's paper describes that as its own behavior, not a universal instrumentation guarantee ([§6.2 p. 11](https://www.foundationdb.org/files/fdb-paper.pdf)).

Reduce through existing workload/fault representations while preserving enabledness and the same violation. Record a changed witness as changed evidence. If replay fails, investigate identity differences and uncontrolled boundaries before attributing a product fault; FDB explicitly improved simulator fidelity to reproduce native failures it had missed ([§6.2 p. 11](https://www.foundationdb.org/files/fdb-paper.pdf)). General reduction and attribution stay in their specialist skills.

Return bounded/model-admitted coverage, truncation/unsupported outcomes, actual CPU/wall/resource cost and remaining space. Virtual-time speedup is not measured real-runtime performance ([FoundationDB §4 limitations](https://www.foundationdb.org/files/fdb-paper.pdf)).
