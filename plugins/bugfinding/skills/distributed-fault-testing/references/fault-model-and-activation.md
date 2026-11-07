# Fault model and activation

Choose a failure interaction the existing lane does not exercise, with a real producer and refutable promise. The experiments below are this pack's designs; verify their target contracts before execution. Jepsen's actual nemesis packages expose partition, packet, file-corruption, clock and process (kill/pause) operations. Partition, packet, clock and process packages carry a `:final-generator`; `file-corruption-package` returns none, so corrupted files are not repaired by the package ([jepsen.nemesis.combined, nemesis-packages and file-corruption-package](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

## Match the fault to the claim

| Intended search | Establish before attributing a failure |
|---|---|
| Acknowledged data survives failover | Actual acknowledgment/durability promise, affected replication topology, known completed writes and supported final-read mode |
| Pause crosses a lease/ownership change | Real ownership/fencing contract, which process paused, elapsed ownership transition and protected effect |
| Replication partitions while clients remain connected | Actual directed links blocked, node roles and which client/server paths still work |
| Recovery loses data after the outage | Actual healed/recovered state and final observation, before cleanup destroys it |

A majority/minority selection, an asymmetric partition and a paused process are different experiments. Source node/partition selectors are useful starting points, but recorded affected links and observed behavior establish which case occurred. The built-in partition specs are `:one`, `:majority`, `:majorities-ring`, `:minority-third` and `:primaries`, each a computed grudge (other values pass through as a literal grudge), and packet behavior "is applied to all traffic to and from the target nodes", so neither built-in gives a one-direction link fault by name ([jepsen.nemesis.combined, grudge and packet-nemesis](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

Do not equate process kill with power loss: the actual etcd `--lazyfs` route "alters the `kill` nemesis to also lose un-fsynced writes". Route a storage model to `crash-consistency-testing` ([jepsen.etcd README, Options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

## Observe activation and repair

Record requested action, selected resource, observed activation and observed repair separately. Use the target's existing process-state, connectivity/packet or clock-offset evidence rather than add a universal injector service. The historical Jepsen 0.3.15 changelog says `control.util/grepkill!` "has silently done nothing since 0.3.12" because "a misplaced paren left its timeout with an empty body", and that "It sends signals again."; this is a fixed framework incident, not a claim current faults still fail ([Jepsen CHANGELOG, 0.3.15 Bugfixes](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md)). A `db-nemesis` completion replaces `:value` with the result of running the DB's start/kill/pause/resume function through `c/on-nodes` on the selected nodes; read that value, not only the requested `:f` ([jepsen.nemesis.combined, db-nemesis](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

A healthy history from a no-op fault is narrower evidence. Diagnose the adapter/version/targeting before buying a longer run. Validate the same recorder/checker with a healthy case and representative justified violation through `harness-sensitivity`; logical operation observations and inference must remain faithful. Elle's detection depends on what is observed: "the fewer indeterminate transactions it holds, the more non-cycle anomalies we can catch" ([Elle, §§3 and 4.3](https://arxiv.org/abs/2003.10554v1)).

## Worked ownership-transition experiment

Given an actual lease-protected mutation, retain the lease-holder's read, pause it, observe another valid owner, resume the old holder, and check the protected state. Compare the promised effects rather than only a return value. The etcd test exposes lock-set/pause as a real workload class (`lein run test --workload lock-set --nemesis pause --time-limit 120` "to demonstrate lost updates to a set protected by an etcd lock"); its README's verdict that "etcd locks are fundamentally unsafe" is about etcd, not a universal statement about every lock implementation ([jepsen.etcd README, Quickstart and Workloads](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)). A pause-across-ownership sequence is the kind of fault ordering the combined package "is *not* intended for"; write the sequence as an explicit generator and use the nemesis only to execute its operations ([jepsen.nemesis.combined, nemesis-package](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

Reduce irrelevant operations and faults only while the ownership transition, original permitted conditions and same forbidden effect remain. General reduction belongs to `failure-reduction`; a shorter client timeout is a different candidate.
