# Fault model and activation

Choose a failure interaction the existing lane does not exercise, with a real producer and refutable promise. The experiments below are this pack's designs; verify their target contracts before execution. Jepsen's actual nemesis packages expose process, partition, packet and clock operations with matching repair generators ([source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

## Match the fault to the claim

| Intended search | Establish before attributing a failure |
|---|---|
| Acknowledged data survives failover | Actual acknowledgment/durability promise, affected replication topology, known completed writes and supported final-read mode |
| Pause crosses a lease/ownership change | Real ownership/fencing contract, which process paused, elapsed ownership transition and protected effect |
| Replication partitions while clients remain connected | Actual directed links blocked, node roles and which client/server paths still work |
| Recovery loses data after the outage | Actual healed/recovered state and final observation, before cleanup destroys it |

A majority/minority selection, an asymmetric partition and a paused process are different experiments. Source node/partition selectors are useful starting points, but recorded affected links and observed behavior establish which case occurred ([selectors](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

Do not equate process kill with power loss: the actual etcd `--lazyfs` route additionally loses un-fsynced writes. Route a storage model to `crash-consistency-testing` ([etcd options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

## Observe activation and repair

Record requested action, selected resource, observed activation and observed repair separately. Use the target's existing process-state, connectivity/packet or clock-offset evidence rather than add a universal injector service. The historical Jepsen 0.3.15 changelog says `grepkill!` faults silently did nothing starting in 0.3.12 and were fixed; this is a fixed framework incident, not a claim current faults still fail ([changelog](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md)).

A healthy history from a no-op fault is narrower evidence. Diagnose the adapter/version/targeting before buying a longer run. Validate the same recorder/checker with a healthy case and representative justified violation through `harness-sensitivity`; logical operation observations and inference must remain faithful ([Elle, §§3–4](https://arxiv.org/abs/2003.10554)).

## Worked ownership-transition experiment

Given an actual lease-protected mutation, retain the lease-holder's read, pause it, observe another valid owner, resume the old holder, and check the protected state. Compare the promised effects rather than only a return value. The etcd test exposes lock-set/pause as a real workload class; its documented example is not a universal statement about every lock implementation ([etcd workloads](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

Reduce irrelevant operations and faults only while the ownership transition, original permitted conditions and same forbidden effect remain. General reduction belongs to `failure-reduction`; a shorter client timeout is a different candidate.
