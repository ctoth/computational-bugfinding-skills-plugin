# Common mistakes

## Recording a timeout as a definite abort

**Wrong:** A commit request times out, so the recorder writes `:fail`.

**Right:** Record `:info` unless the actual contract or evidence proves no effect. In Jepsen histories `:fail` "*must* have no logical effect on the system", while `:info` means "the operation either may or may not have completed" ([jepsen.history README, Operation Structure and Operation Semantics](https://raw.githubusercontent.com/jepsen-io/history/61d2776c889ad84f7c6922977cf05e8f11970402/README.md)).

**Why:** a `:fail` for a write that committed hides its effect, so later reads of that value look like aborted reads.

## Splitting one transaction into independently committed writes

**Wrong:** Record each micro-operation of a multi-key transaction as its own `:txn` operation to simplify conversion.

**Right:** Keep the original micro-operation boundaries and order in one operation value. Elle infers dependencies between transactions from the micro-operations inside each operation's `:value` ([list_append.clj `preprocess`, `check`](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/src/elle/list_append.clj)).

**Why:** split operations describe a different, weaker workload; a clean result on it says nothing about the real transaction.

## Reading every guarantee into a serializable result

**Wrong:** A `--consistency-models serializable` run returns `true`, so session and realtime guarantees are reported as tested.

**Right:** Select session/realtime guarantees explicitly. Serializability "does not impose any real-time, or even per-process constraints" ([Jepsen, Serializability, Informal](https://jepsen.io/consistency/models/serializable)), and Elle keeps only anomalies prohibited by the selected models ([txn.clj `result-map`](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/src/elle/txn.clj)).

**Why:** process and realtime anomalies outside the selected model are dropped from the result, not reported as passing.

## Accepting exit 0 as a checked healthy history

**Wrong:** `java -jar elle-cli.jar ...` exits 0, so the history is recorded as valid.

**Right:** Require the requested file's explicit verdict and admitted input. elle-cli exits 1 only when some result is `false`; unknown-only output, `--help`, a missing `--model` and no history argument all exit 0 ([cli.clj `-main`](https://raw.githubusercontent.com/ligurio/elle-cli/3c2504815945cd4ab1b5cc0142d2fe206e1ee285/src/elle_cli/cli.clj)).

**Why:** an exit code cannot distinguish "checked and clean" from "never checked" or "inconclusive".

## Strengthening register inference with an assumed order

**Wrong:** Pass `:linearizable-keys? true` or a `:transaction-order` built from client wall clocks to get more cycles.

**Right:** Establish the actual exposed ordering and the selected version's assumptions first. `:transaction-order` is documented as "'whitebox' dependency order information from a database system", and the docstring warns the per-key options "may not work correctly" ([rw_register.clj `check`](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/src/elle/rw_register.clj)).

**Why:** an assumed order manufactures version edges, so a resulting cycle may reflect the assumption rather than the target.

## Treating more overwritten values as more information

**Wrong:** Add more blind register writes to "increase coverage" of version order.

**Right:** Choose observations that recover write/version provenance, such as unique list appends: "the version resulting from a blind write carries no information about the previous version" ([Elle, §3](https://arxiv.org/abs/2003.10554v1)).

**Why:** blind writes "destroy history"; more of them raise cost without adding ww/rw evidence.

## Dropping timeout evidence or discarding every partial search

**Wrong:** Treat any `:cycle-search-timeout` as a failed run and discard its output, or report it as clean.

**Right:** Retain discovered prohibited anomalies and unresolved analysis separately. On timeout Elle keeps cycles already found plus a fallback cycle, and a found prohibited anomaly still yields `false` ([txn.clj `cycle-cases-in-scc`, `result-map`](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/src/elle/txn.clj)).

**Why:** a timeout in one SCC does not erase a witness found in it or elsewhere.

## Shrinking to a different cycle by erasing setup or uncertainty

**Wrong:** Delete the setup transaction and turn `:info` operations into `:ok` until the history is small.

**Right:** Preserve the original and revalidate the reduced witness's premises. Elle's soundness argument relies on a trace-recoverable observation and covers every compatible interpretation of it ([Elle, §§4.3 and 6](https://arxiv.org/abs/2003.10554v1)).

**Why:** removing provenance or resolving uncertainty changes the set of interpretations, so the reduced cycle may not witness the original anomaly.

Use `failure-reduction` for minimizing the dependent evidence and `evidence-based-triage` for supported attribution; this skill owns transaction observations and isolation interpretation.
