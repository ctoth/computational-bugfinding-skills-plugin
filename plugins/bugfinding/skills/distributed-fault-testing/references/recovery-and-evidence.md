# Recovery and evidence

A useful experiment includes final repair and post-recovery observations. The actual etcd producer separates timed load, healing, recovery wait and final workload operations; its literal sleep is not a universal convergence guarantee ([producer](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj)).

## Observe before cleanup

Use the actual adapter's repair actions, then supported readiness/convergence evidence and final reads within the authorized budget. Record unsuccessful repair and unavailable final observations separately. Nemesis final generators request start/resume/link/clock repair, but those requests alone do not demonstrate the system recovered ([nemesis source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj)).

Capture the state required by the oracle before teardown. Jepsen's log collection may kill the database before copying files, unless configured to leave it running; `finally` cleanup attempts do not prove repair succeeded ([core source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/core.clj)).

Keep fault/cleanup operations confined to the known test-owned deployment. Adapters may control node-wide processes, firewalls and clocks, so never transplant their cleanup onto unrelated shared-host resources ([environment requirements](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

## Preserve a replayable investigation

Retain target/client/checker/build/configuration, initial data and promised modes; actual operations and ambiguous outcomes; requested/observed fault and repair sequence; raw histories, server/client logs, final observations, explicit checker results/witnesses and resource costs. Stored test data omits executable client/checker objects, so keep compatible source/dependencies and arguments too ([stored tests](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

Use traceable values where they reveal the promised behavior. Explain the contradiction from actual operations and dependency evidence; model/observation limits remain even under many injected faults ([Elle, §§3, 4.3, 6 and 9](https://arxiv.org/abs/2003.10554)).

## Worked recovery decision

Suppose a permitted failure interrupts load and all reads time out. Healing plus a successful final observation can establish whether known acknowledged values remain; absent final observation leaves that guarantee unresolved. A stale-read option or weaker acknowledgment policy changes the premise and must be recorded. The real etcd options distinguish stale reads and loss of un-fsynced writes ([options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

Spend the next bounded allocation on the missing activation/recovery/observation dimension, not automatically higher request volume. Report load success, ambiguity, fault coverage and checked histories separately. This allocation is the pack's design; use `bugfinding-campaign` for its broader decision.

Preserve originals while reducing workload plus fault sequence. Keep acknowledgment, failure model, recovery boundary and the same witness; losing the effect and retaining only a timeout changes the candidate. Route mechanics to `failure-reduction` and attribution to `evidence-based-triage`.
