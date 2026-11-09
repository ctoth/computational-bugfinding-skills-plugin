# Common mistakes

## Relabeling another guarantee as linearizability

**Wrong:** “Elle found the transactions serializable and the race detector is clean, so the object is linearizable.”

**Better:** Establish the object's actual sequential contract and real-time ordering, then check that.

**Why:** serializability "does not impose any real-time, or even per-process constraints" ([Jepsen serializable](https://jepsen.io/consistency/models/serializable)), race freedom yields only that "data-race-free programs execute in a sequentially consistent manner" ([Go memory model, Informal Overview](https://go.dev/ref/mem#overview)), and linearizability is ordered "consistent with the real-time ordering of those operations" ([Jepsen linearizable](https://jepsen.io/consistency/models/linearizable)).

## Sorting calls into completion-order pairs

**Wrong:** Emit each operation as an adjacent call/return pair in completion order to make the event list tidy.

**Better:** Retain observed overlap and matched event identity; the checker searches admissible orders, not an invented serialization.

**Why:** event conversion takes slice position as time (comment: `use index as "time"`), so reordering events rewrites the real-time evidence ([conversion source](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/checker.go)).

## Feeding pending calls as raw unmatched events, or treating a timeout as no effect

**Wrong:** Leave a call with no `ReturnEvent` in the history, or drop a timed-out write as if it failed.

**Better:** Validate pairing and derive a justified uncertainty model; the existing etcd adapter's unknown completion (`etcdOutput{unknown: true}`) is specific to its model.

**Why:** an unmatched call gets a nil match and the search treats a nil-match node as a return, with no error ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/checker.go)); the etcd model pairs its appended unknown returns with `|| out.unknown` acceptance ([adapter](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/porcupine_test.go)).

## Timestamping Node.js operations with `Date.now()`

**Wrong:** Record `Call` and `Return` from `Date.now()` in a Node.js client.

**Better:** Use `process.hrtime.bigint()`, or one in-order event list from a single event loop ([model and history](model-and-history.md)).

**Why:** the wall clock "can decrease, making it unreliable for performance measurement or recording the orders of events" ([HR-Time](https://raw.githubusercontent.com/w3c/hr-time/76c362ed3194d99d8563608be0bb6a73e06935b8/index.bs)); the hrtime clock is "not related to the time of day and therefore not subject to clock drift" ([Node v26.13.0 process.md](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/process.md)).

## Waiting for `AbortSignal.timeout` to close pending Node.js calls

**Wrong:** Rely on an `AbortSignal.timeout` rejection to write the completion of a call that never settles.

**Better:** Close every call still open at history end yourself, with the model-specific unknown output.

**Why:** the timeout timer is unref'd so it does not "keep the Node.js process open on it's own", and it is cleared when the signal is garbage-collected ([abort_controller.js](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/lib/internal/abort_controller.js)); the process can end with the call never recorded.

## Mutating prior model state while stepping

**Wrong:** `Step` appends to the map or slice held in `state` and returns the same value.

**Better:** Keep model transitions pure: copy, change the copy, return it.

**Why:** `Step` "must be a pure function: it cannot mutate the given state" ([model](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/model.go)); on backtrack the checker restores the saved `callsTop.state`, which a mutation has already changed ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/checker.go)).

## Splitting every history by key despite global size/transfer calls

**Wrong:** Partition by key and assign the global `size()` or two-key transfer to one arbitrary key, or drop it.

**Better:** Establish the partition's semantic equivalence or keep the coupled model.

**Why:** a "‘size’ operation that returns the number of elements" in a collection "cannot be generally partitioned this way" ([paper, p.6](https://arxiv.org/abs/1504.00204)).

## Counting `Unknown` as a completed accepted history

**Wrong:** Follow the upstream hint that "you can interpret an Unknown result as Ok" when reporting coverage.

**Better:** Preserve exhausted checking distinctly and report the actual budget/result.

**Why:** `Unknown` is commented `// timed out`: no decision was reached ([CheckResult](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/model.go), [API](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/porcupine.go)).

## Treating a nominal checker deadline as a hard interrupt for any callback

**Wrong:** Pass a 30-second timeout to `CheckOperationsVerbose` and assume the call returns within 30 seconds whatever `Step` does.

**Better:** Use a supported cancellation-aware model (`StepContext`) and a fitting outer limit.

**Why:** on timeout the checker only calls `cancel()`, and the verbose path waits for every worker ("make sure we've waited for all goroutines to finish") ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/checker.go)).

## Inferring a minimal cause from the HTML display

**Wrong:** Name the operation highlighted in the visualization as the root cause.

**Better:** Retain raw histories and model; visualized partial orders are search evidence.

**Why:** for a rejected history the page "shows partial linearizations and illegal linearization points", not a minimal contradiction ([visualization](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/visualization.go)).
