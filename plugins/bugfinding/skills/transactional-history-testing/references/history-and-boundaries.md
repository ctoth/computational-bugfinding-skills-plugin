# History and boundaries

Map source-level publication into the promised logical transactions before recording. A retry may produce multiple attempts; an exception may follow a committed slice. Preserve request/attempt provenance in raw evidence, then justify which effects belong to each checker transaction. Jepsen operation semantics, rather than an exception name, determine outcome classification ([history contract](https://raw.githubusercontent.com/jepsen-io/history/main/README.md)).

| Recorded outcome | Required evidence |
|---|---|
| `:ok` | Successful logical operation under the API contract |
| `:fail` | Definite failure with no logical effect |
| `:info` | Effect/completion remains indeterminate |
| Recorder/setup failure | Preserve separately; it does not decide target isolation |

Logical processes are single-threaded; a crashed process cannot resume subsequent requests under the same identity. Preserve matching invocation/completion and original observations when adapting formats ([history structure and semantics](https://raw.githubusercontent.com/jepsen-io/history/main/README.md)).

Validate initialization and types against the actual frontend. Register inference orders nil before other versions; an existing non-nil state needs a faithful representation. Append invocation values must be unique per key; preserve repeated/intermediate micro-operations inside the real transaction ([register source](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj), [append source](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj)).

Illustrative control: a write commits, loses its response and is retried. Retain raw attempt identity and evidence of publication; compare mappings that preserve possible effects. Marking the first attempt aborted or counting both attempts as new successful requests can change the history's meaning. Establish the real idempotency/transaction contract before selecting either mapping ([history semantics](https://raw.githubusercontent.com/jepsen-io/history/main/README.md)). This is an experiment design, not an observed defect.

Exercise healthy and known-violating recordings through the same converter. Preserve malformed input, missing observations and checker-unknown separately; append validation can reject unsupported operations or duplicate invocation provenance before meaningful anomaly analysis ([append validation](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj)). Sensitivity execution belongs to `harness-sensitivity`.
