# Partitioning and checker cost

## Preserve the specification when splitting

Use a partition only when the whole history is linearizable if and only if all its partitions are. Independent set/map operations can permit key partitioning; a global size operation generally cannot use that split. Transfers, scans or allocation constraints require their own contract reasoning, not a convenient key field ([P-compositionality, pp.5-6,9](https://arxiv.org/abs/1504.00204)).

Preserve each operation's call and return in the same partition. Porcupine provides separate partition functions for interval and event histories; leaving them unset retains one history. Its KV example maps event identities to keys so responses follow calls ([model](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go), [actual examples](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go)). Small whole/partitioned comparisons can reveal an adapter mistake; agreement on samples does not prove arbitrary partition validity.

Illustrative failure: a map adds an atomic transfer and a total-balance observation. Dropping those operations from per-key histories makes checks cheaper by omitting their guarantee. Use a justified whole-object model or establish a different valid decomposition. Do not serialize overlaps to make checking finish: that changes the real-time premise ([paper, pp.5-9](https://arxiv.org/abs/1504.00204)). This is a design example, not a target finding.

## Interpret limits and outcomes

Budget checker work separately from generating the history. Preserve operation count, overlap and partition distribution where available, model/equality cost, elapsed/CPU/memory, chosen deadline and result. The paper's historical runtimes exclude timed-out observations from some summaries; do not silently count exhausted checks as accepted histories ([paper, pp.11-14](https://arxiv.org/abs/1504.00204)).

Current Porcupine returns `Illegal` for an established rejection, `Unknown` when checking times out without that decision, and `Ok` on completed acceptance. Its verbose path waits for workers before returning evidence. A blocking legacy `Step` can defeat a nominal timeout; a supported `StepContext` must actually honor cancellation. A deadline and a task-owned outer execution limit serve different purposes ([API](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go), [checker source](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)). Keep truncated/unresolved evidence distinct from a product violation.

An accepted observed history does not establish all possible schedules; a rejected one still depends on recorder fidelity and the right sequential contract. Use workload/schedule search to seek further histories, not a larger correctness claim from one checked trace ([paper, pp.13-14](https://arxiv.org/abs/1504.00204)).
