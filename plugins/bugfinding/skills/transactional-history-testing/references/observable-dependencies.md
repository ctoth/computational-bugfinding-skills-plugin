# Observable dependencies

Choose observations for the missing guarantee, then generate interactions that expose them. These are candidate experiments, not promises that every target supports the proposed observation.

| Observation | What must be justified |
|---|---|
| Traceable append values | They exercise the actual producer and preserve unique write provenance |
| Register/version metadata | The exposed order really constrains committed versions |
| Session/process order | The API promises it and the recorder preserves that session |
| Realtime order | Genuine non-overlap is established, without inventing cross-host clock edges |
| Predicate/range membership | A compatible analyzer consumes queried predicates and membership/absence observations |

Append traceability and additional order evidence expose different dependency information; the paper's model omits predicates ([Elle, §§3, 5 and 9](https://arxiv.org/abs/2003.10554)). Current model labels do not by themselves show that a particular frontend records predicate data ([current model mapping](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/consistency_model.clj)).

**Session extension.** A serializable history may violate a separately promised session order. Preserve actual session identity and use a supported model that checks that promise. Without the extra guarantee, this is not automatically a defect ([serializable model](https://jepsen.io/consistency/models/serializable)).

**Hidden version order.** Blind overwrites can leave the needed relation unknown. A supported traceable representation or trustworthy exposed commit/version order may improve inference. Register `:transaction-order` is a direct-library option keyed by completion indices; it is not an inspected CLI flag. Its assumptions need actual source/version evidence ([register options](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj), [CLI options](https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj)).

**Predicate extension.** Recording only returned point keys can omit the absence/membership information required by a range guarantee. Select a verified predicate-aware observer or leave that dimension untested; renaming a scan as a point read does not supply the missing observation ([Elle, §9](https://arxiv.org/abs/2003.10554)).

Measure committed/admitted transaction shapes, informative reads, observed dependency kinds and unknown outcomes. Tune contention, length and key lifetime together where the producer supports them; the current generator exposes distributions, transaction length and writes-per-key controls ([generator source](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj)). Reuse an existing workload owner rather than add a generic history service.
