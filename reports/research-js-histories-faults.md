# Research: JS/TS (Node) extension for linearizability-checking, transactional-history-testing, distributed-fault-testing

Group H, Phase 3 per-skill research. Branch `js-web-bugfinding`. Date 2026-11-09. Status: complete.

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md` lines 39-40 (rows for these three skills).
- `reports/skill-research-js-web-bugfinding.md` F11 (lines 185-192), F12 (194-203), F13 (206-217).
- `plugins/bugfinding/skills/linearizability-checking/SKILL.md`, `references/porcupine-operation.md`, `references/model-and-history.md`, `references/common-mistakes.md`, `references/sources.yaml`.
- `plugins/bugfinding/skills/transactional-history-testing/SKILL.md`, `references/elle-operation.md`, `references/history-and-boundaries.md`, `references/sources.yaml` (URL list).
- `plugins/bugfinding/skills/distributed-fault-testing/SKILL.md`, `references/fault-model-and-activation.md`, `references/jepsen-operation.md` (first section), `references/sources.yaml` (URL list), `references/common-mistakes.md` (headings).
- `reports/research-js-resource.md` (head, for format/evidence standard).

Already covered by the existing skills (not repeated here): Porcupine API, pairing and unknown-output handling (`linearizability-checking/references/model-and-history.md:13-17`); elle-cli options, exit codes, Java 21 and EPL/GPL in `project.clj` (`transactional-history-testing/references/elle-operation.md:5-23`); Jepsen `:ok`/`:fail`/`:info` semantics and the timeout wrapper (`distributed-fault-testing/SKILL.md:12`).

No papers were needed or read for this group; every claim below comes from source code, docs or specs at the cited pins.

## Findings

### H1. Node clocks for invoke/complete timestamps

Pinned: `nodejs/node` tag `v26.13.0` (commit `18b32a3b1552e199a01f1a8d9fd64aa756d3b75b`, observed with `git ls-remote` 2026-11-09; bundled libuv 1.52.1 per `deps/uv/include/uv/version.h`). Raw files read: `doc/api/process.md`, `doc/api/perf_hooks.md`, `src/node_process_methods.cc`, `src/node_perf.cc`, `src/node_perf_common.h`, `lib/internal/perf/utils.js`, `deps/uv/docs/src/misc.rst`, `deps/uv/src/unix/core.c`, `deps/uv/src/unix/linux.c`, `deps/uv/src/win/util.c`.

Facts (docs):
- `process.hrtime.bigint()` (process.md:2580-2593, "added: v10.7.0"): "returning the current high-resolution real time in nanoseconds as a `bigint`"; differences are "computed directly by subtraction of the two `bigint`s".
- `process.hrtime([time])` is "Stability: 3 - Legacy. Use [`process.hrtime.bigint()`][] instead." (process.md:2526). Its text carries the clock property: "These times are relative to an arbitrary time in the past, and not related to the time of day and therefore not subject to clock drift." (process.md:2544-2546). The bigint section does not repeat that sentence; it calls itself "The `bigint` version of the [`process.hrtime()`][] method".
- `performance.now()` (perf_hooks.md:345-346): "Returns the current high resolution millisecond timestamp, where 0 represents the start of the current `node` process." Returns {number} (double, milliseconds).
- `performance.timeOrigin` (perf_hooks.md:372-373): "the high resolution millisecond timestamp at which the current `node` process began, measured in Unix time."
- Node's docs at this tag never call `performance.now()` "monotonic" (grep `monoton` in perf_hooks.md: only an unrelated histogram field, line 2654).
- libuv `uv_hrtime` (deps/uv/docs/src/misc.rst:669-674): "It is relative to an arbitrary time in the past. It is not related to the time of day and therefore not subject to clock drift."

Facts (source):
- `HrtimeImpl` and `HrtimeBigIntImpl` both read `uv_hrtime()` (src/node_process_methods.cc:719, 726).
- `performance.now()` is `PerformanceNowImpl`: `(uv_hrtime() - performance_process_start) / NANOS_PER_MILLIS` (src/node_perf.cc:375-378). `performance_process_start` is a process-wide `const uint64_t` initialized once (src/node_perf.cc:41; `PERFORMANCE_NOW()` is `uv_hrtime()`, src/node_perf_common.h:19). So `performance.now()` and `process.hrtime.bigint()` are the same clock with a fixed offset and different units, and in this Node version a worker thread's `performance.now()` has the same zero as the main thread (process-global constant, not per-Environment). This differs from the HR-Time model for browser workers (below).
- `uv_hrtime()` is `uv__hrtime(UV_CLOCK_PRECISE)` on Unix (deps/uv/src/unix/core.c:154-156), which on Linux uses `clock_id = CLOCK_MONOTONIC` for the precise type (deps/uv/src/unix/linux.c:1603-1618). On Windows it is `QueryPerformanceCounter` scaled to ns (deps/uv/src/win/util.c:458-482).
- Linux `clock_gettime(2)` (man-pages 6.19, 2026-03-07, https://man7.org/linux/man-pages/man2/clock_gettime.2.html): `CLOCK_MONOTONIC` is "A nonsettable system-wide clock that represents monotonic time"; it "is not affected by discontinuous jumps in the system time".

HR-Time (W3C Editor's Draft, `w3c/hr-time` main at `76c362ed3194d99d8563608be0bb6a73e06935b8`, rendered https://w3c.github.io/hr-time/, read 2026-11-09):
- Wall clock: "its wall clock sometimes needs to be adjusted, which means the unsafe current time can decrease, making it unreliable for performance measurement or recording the orders of events. The web platform shares a wall clock with [ECMA-262] time." (rendered text line 1148). `Date.now()` is ECMA-262 time, so it is that wall clock.
- Monotonic clock: "never decreases, so it can’t be changed by system clock adjustments. The monotonic clock only exists within a single execution of the user agent" (line 1151).
- "the monotonic properties only apply for contexts that can reach each other by exchanging messages" (line 1155).

ECMA-262 (living draft, https://tc39.es/ecma262/, read 2026-11-09), 25.5.4.2 SerializeJSONProperty: "If value is a BigInt, throw a TypeError exception." So `JSON.stringify` of a raw `hrtime.bigint()` value throws unless a `toJSON`/replacer converts it.

Conclusion for the drafter (synthesis from the facts above):
- Use `process.hrtime.bigint()` for invoke and complete timestamps. `Date.now()` is wall-clock time that can be adjusted backward, which can invent or erase real-time precedence. `performance.now()` is the same clock in Node but a double in ms.
- Serialization: a bigint must be converted for JSON. Converting raw `hrtime` ns to a JS Number loses integer precision above 2^53 ns (about 104 days since the clock's origin; on Linux that origin is boot). Subtract the first sample (bigint arithmetic) or emit decimal strings, then parse to `int64` on the Go side or a long on the JVM side. (Arithmetic inference from the documented types; not executed.) Porcupine's `Call`/`Return` are `int64` (H4).
- Across worker threads of one process, `hrtime.bigint()` values come from one `uv_hrtime` source and are comparable (source fact). Across processes on one Linux host, `CLOCK_MONOTONIC` is system-wide, so values are comparable (inference from the man page + libuv source; Windows QPC cross-process comparability not verified). Across hosts there is no common monotonic clock; keep the existing rule "do not invent real-time edges from unsynchronized client clocks" (`model-and-history.md:11`).
- Within one process the recorder can drop timestamps and append events in program order (H3), which Porcupine `CheckEvents` and Elle both read as real-time order (H4, H5).

### H2. Recording invocation and completion around a promise; never-settling promises; timeouts

Pinned: same Node tag. Raw files: `doc/api/globals.md`, `lib/internal/abort_controller.js`, `doc/api/process.md`; WHATWG DOM Living Standard (https://dom.spec.whatwg.org/, read 2026-11-09).

Facts:
- `AbortController`: "A utility class used to signal cancelation in selected `Promise`-based APIs." (globals.md:44). Aborting has an effect only where the called API accepts the signal.
- `AbortSignal.timeout(delay)` "Returns a new `AbortSignal` which will be aborted in `delay` milliseconds." (globals.md:120-131; added v17.3.0, v16.14.0). `AbortSignal.any(signals)` composes signals; "Its [`abortSignal.reason`][] will be set to whichever one of the `signals` caused it to be aborted." (globals.md:133-146; added v20.3.0, v18.17.0).
- Source: the timeout aborts with `new DOMException('The operation was aborted due to timeout', 'TimeoutError')` (lib/internal/abort_controller.js:210-214). The DOM standard also specifies a "TimeoutError" DOMException for `timeout(milliseconds)` (rendered text lines 3069-3073, 3142-3164).
- Source: the timeout timer is unref'd and weakly bound: "We also don't want the timer to keep the Node.js process open on it's own. Therefore, we wrap the AbortSignal in a WeakRef ... and we unref the created timer object. Separately, we add the signal to a FinalizerRegistry that will clear the timeout when the signal is gc'd." (lib/internal/abort_controller.js:196-203; `timeout.unref()` at 217).
- `'beforeExit'` "is emitted when Node.js empties its event loop and has no additional work to schedule." It is "_not_ emitted for conditions causing explicit termination, such as calling [`process.exit()`][] or uncaught exceptions." (process.md:32-42).
- Exit code `13` "**Unsettled Top-Level Await**: `await` was used outside of a function in the top-level code, but the passed `Promise` never settled." (process.md:4630-4631).

Consequences for a recorder (synthesis):
- Record `invoke` synchronously before starting the call (before the promise-returning function is called), and the completion synchronously as the first statement of the `.then`/`.catch` continuation. Recording invoke after the request is sent can only shrink the interval and can manufacture a real-time edge; recording completion late only widens it (the checker becomes more permissive, never wrongly stricter). (Inference from the closed-interval definition cited in H4.)
- Do not use `finally` alone: it does not receive the value or the error, so it cannot classify `ok`/`fail`/`info`. (ECMA-262 `Promise.prototype.finally` callback arguments not re-read here; listed unverified.)
- A promise that never settles produces no completion; the recorder must close it itself at history end as `:info` (Elle/Knossos) or a model-specific unknown output (Porcupine), never `:fail`. Nothing in the runtime does this.
- An `AbortSignal.timeout` timer does not keep the process alive and is cleared if the signal is garbage-collected. If the only outstanding work is a promise with no live handle, Node can exit (exit code 13 under top-level await, otherwise after `beforeExit`) before the timeout fires, and open invocations are lost unless the recorder flushes them on `beforeExit`/`exit` or the driver holds an explicit ref'd deadline and keeps the signal reachable. (Inference from the two facts; not executed.)
- Aborting a client signal only stops the client waiting (for APIs that honor it). Whether the request changed the server is unknown, so a `TimeoutError`/`AbortError` completion is `:info`. A late settlement of the original promise after `:info` must not be written as a second completion; that logical process "can never invoke an operation again" (jepsen.history README, already cited at `history-and-boundaries.md:12`). Keep it as raw evidence and continue with a fresh logical process id, as the Elle paper's tests do (`history-and-boundaries.md:12`).

### H3. Concurrency: logical clients in one event loop vs worker_threads/child processes

Sources: `nodejs/learn` main at `ea10f2a6af515ec69885f517984ef8628f0eb37b`, `pages/asynchronous-work/dont-block-the-event-loop.md` (the guide lives in `nodejs/learn`, located with `gh search code`); Node v26.13.0 `doc/api/worker_threads.md`.

Facts:
- "Node.js runs JavaScript code in the Event Loop (initialization and callbacks), and offers a Worker Pool to handle expensive tasks like file I/O." (line 12). "In Node.js there are two types of threads: one Event Loop (aka the main loop, main thread, event thread, etc.), and a pool of `k` Workers in a Worker Pool" (line 26).
- worker_threads: "enables the use of threads that execute JavaScript in parallel" (worker_threads.md intro); "Workers (threads) are useful for performing CPU-intensive JavaScript operations. They do not help much with I/O-intensive work." "Unlike `child_process` or `cluster`, `worker_threads` can share memory."

Synthesis for the drafter:
- Many logical clients in one event loop are enough to produce overlapping operations against a remote service: each client starts a request and awaits it, so requests are in flight concurrently while JS callbacks run one at a time. This is the cheap default.
- Because callbacks run one at a time on the main thread, appending to one in-memory array at invoke and at completion yields a total order consistent with what the client observed; this ordered list is what Porcupine `CheckEvents` and Elle consume (H4, H5). Timestamps are then optional.
- A busy event loop delays completion callbacks; that widens intervals and hides violations but cannot invent them. Record client load with the evidence. (Inference.)
- Worker threads or child processes are needed only when the client-side code itself is the concurrent object under test (e.g. `SharedArrayBuffer`/`Atomics` objects) or when one loop cannot generate enough load. Then events are recorded per thread with `hrtime.bigint()` (shared clock, H1) and merged by timestamp, keeping equal timestamps as concurrent; never merge by message arrival order at a coordinator.
- Each logical client id must map to Jepsen's "logically singlethreaded" `:process` / Porcupine `ClientId`: one outstanding operation per logical client at a time. A `Promise.all` of several calls from one "client" breaks that and must be split into distinct ids. (From the jepsen.history README text in H5.)

### H4. Porcupine input format (exact)

Pinned: `anishathalye/porcupine` tag v1.3.1, commit `97cd067defd99df172053ba7f4ca5bbae57fe446` (same pin as the skill; still the latest commit on 2026-11-09, committed 2026-09-21; latest tag v1.3.1 per `git ls-remote`). File `model.go`.

Facts:
- `type Operation struct { ClientId int // optional, unless you want a visualization; zero-indexed; Input interface{}; Call int64 // invocation timestamp; Output interface{}; Return int64 // response timestamp; Metadata interface{}; _ struct{} }` (model.go:19-29). Metadata "is not used for linearizability checking but can be used for visualization."
- `type Event struct { ClientId int; Kind EventKind; Value interface{}; Id int; Metadata interface{}; _ struct{} }` with `CallEvent EventKind = false`, `ReturnEvent EventKind = true` (model.go:50-77). "In the Event representation, function calls and returns are only relatively ordered and do not have absolute timestamps." "The Id field is used to match a function call event with its corresponding return event."
- model.go:31-47 explains the closed interval with a monotonic clock example ("successive calls to the clock return values that are always greater than _or equal to_ previously returned values") and concludes "The only sensible approach is to interpret the interval [Call, Return] as a closed interval."
- model.go has no `json` struct tags (grep `json`: no matches). Porcupine has no file reader; `Input`/`Output` are `interface{}` interpreted only by the user's Go `Model`.

Consequence: a Node history needs a small Go program: decode the Node-written JSON into the user's typed input/output structs, build `[]porcupine.Operation` (timestamps as `int64` ns, H1) or `[]porcupine.Event` (file order), and call the bounded API already documented in `porcupine-operation.md`. `ClientId` must be zero-indexed ints if visualization is wanted. Pending operations need the model-specific unknown output already described in `model-and-history.md:17`. No JS linearizability checker was found in F13; not re-searched here.

### H5. elle-cli JSON history format (exact) and Knossos/Elle field names

Pinned: `ligurio/elle-cli` master `3c2504815945cd4ab1b5cc0142d2fe206e1ee285` (still latest commit on 2026-11-09, committed 2026-10-16). Files: `README.md`, `src/elle_cli/cli.clj`, `project.clj`, `test/test-data/*.json`. `jepsen-io/history` README at `61d2776c889ad84f7c6922977cf05e8f11970402`. `jepsen-io/elle` `src/elle/core.clj` at `4e359e597c52938b0afebb8bc42273914d68a424`.

Field semantics (jepsen.history README, "Operation Structure", lines 43-86):
- `:type` "must be one of `:invoke`, `:ok`, `:info`, or `:fail`".
- `:time` "is a long: The time since the start of the test, in nanoseconds."
- `:process` "is a logical identifier for the process executing this operation, like `2` or `:nemesis`. Processes are logically singlethreaded, and can execute only one thing at a time."
- `:f` "is a function being applied. This may be any object, but is often something like `:read`, `:write`, `:txn`".
- `:value` "stores arguments to and/or return values from the operation"; for a read invocation it "is typically left `nil`".
- `:index` "is a unique, monotonically ascending integer"; "users may omit indices".
- `:error` "encodes error information". "Clients ... have integer `:process` identifiers" (lines 89-90).

elle-cli JSON parsing (cli.clj):
- `read-json-history` = `(json/read-str (slurp filepath) :key-fn keyword :value-fn value-reader)` (cli.clj:70-75), using `org.clojure/data.json "2.4.0"` (project.clj:16). JSON keys become keywords.
- `value-reader` keywordizes the values of `type` and `f` (`(or (= key :type) (= key :f)) (keyword value)`), and for a `value` that is a non-empty vector of vectors whose first element is a string, keywordizes the first element of each micro-op (cli.clj:59-68; comment `;; e.g. {:value [[:append :x 1] [:r :y nil]]}`). Nothing else is converted: keys inside micro-ops stay strings or numbers; JSON `null` is nil.
- Format is chosen by `--format` or the file extension (`read-fn-by-extension`, cli.clj:220-224).
- Knossos models (`cas-register`, `mutex`) go through `history/parse-ops`; Elle models get the history directly (cli.clj:195-208).
- Bundled versions: `[jepsen "0.3.11"]`, `[knossos "0.3.15"]` (project.clj:19-20).

Real sample files (all are one JSON array of op objects):
- `test/test-data/rw-register-partial-info.json`: `{"index":0,"process":0,"type":"invoke","f":"txn","value":[["w","x",1]]}`, ... `{"index":3,"process":1,"type":"info","f":"txn","value":[["r","x",1]]}`, and a final `invoke` (index 6) with no completion. Expected result file: `{"valid?":true}`.
- `test/test-data/list-append-anomaly-g1a-aborted-read.json`: `[{"index":0,"process":0,"type":"invoke","value":[["append",1,1]]}, {"index":1,"process":0,"type":"fail","value":[["append",1,1]]}, {"index":2,"process":1,"type":"invoke","value":[["r",1,null]]}, {"index":3,"process":1,"type":"ok","value":[["r",1,[1]]]}]` (no `f`, no `time`).
- `list-append-dirty-update-info-fail-result.json` shows ops echoed with `"time":-1` and `"f":null` when absent: `time` and `f` are optional for list-append.
- README cas-register example (Knossos): `{:process 7, :type :invoke, :f :cas, :value [2 3]}`, `{:process 1, :type :invoke, :f :read, :value nil}` then `{:process 1, :type :ok, :f :read, :value 2}` (README lines 341-350).
- The README's own example path `histories/elle/rw-register.json` (README:56) does not exist at this commit (`gh api .../git/trees/3c25048...?recursive=1`: 0 paths under `histories/`). Use `test/test-data/` files as fixtures.

Elle real-time order is file order, not `:time`: `realtime-graph` docstring "a < b if a ends before b begins", and the implementation comment "iterate through the history, and for any given :ok op, create an edge from that :ok to the :ok or :info corresponding to subsequent :invokes" (elle/core.clj:371-385). So a Node recorder that writes ops sorted by id, or groups invoke/complete pairs, destroys realtime evidence for `strict-serializable` checks (the elle-cli default model).

JSON mapping from a Node recorder (synthesis): emit one array; each element `{"index": n, "process": <int logical client>, "type": "invoke"|"ok"|"fail"|"info", "f": "<fn>", "value": ..., "time": <ns since test start, as integer>, "error": ...}` in observed order. For list-append, append values must be unique per key (existing skill, `history-and-boundaries.md:14`). JSON integers above 2^53 are not exact in JS; `time` since test start avoids that (H1).

### H6. elle-cli license (resolves F13 "NOASSERTION")

- `LICENSE` at the pinned commit is the full "Eclipse Public License - v 2.0" text (280 lines), whose Exhibit A gives the Secondary Licenses notice naming "GNU General Public License ... either version 2 of the License, or (at your option) any later version, with the GNU Classpath Exception" (LICENSE:262-270), followed by "Simply including a copy of this Agreement, including this Exhibit A is not sufficient to license the Source Code under Secondary Licenses." (LICENSE:272-273).
- `project.clj:4`: `:license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"`.
- GitHub API `repos/ligurio/elle-cli/license`: `spdx_id` `NOASSERTION`, name "Other".
- Resolution: the project declares `EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0` in `project.clj` and ships the EPL-2.0 text. Why GitHub's detector says NOASSERTION is not established (possibly the appended Exhibit A text; inference). The drafter should write "EPL-2.0 (LICENSE file); project.clj declares EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0", which matches what `elle-operation.md:5` already says about the manifests.

### H7. Toxiproxy server: what it injects and what it cannot

Pinned: `Shopify/toxiproxy` main `49299d8838525126e09c85ebe0ba89940a3261e5` (latest commit 2026-10-14; same pin as F12; latest tag v2.13.0; MIT per GitHub API; not archived). Files: `README.md`, `toxics/*.go`, `toxics/toxic.go`, `toxic_collection.go`, `link.go`, `go.mod`.

Facts:
- "Toxiproxy usage consists of two parts. A TCP proxy written in Go (what this repository contains) and a client communicating with the proxy over HTTP. You configure your application to make all test connections go through Toxiproxy" (README:15-18).
- Registered toxic types in source (`Register("...")` in `toxics/*.go`): `latency`, `bandwidth`, `slow_close`, `timeout`, `reset_peer`, `slicer`, `limit_data`, `packet_loss`, `noop`. `packet_loss` is also documented in the v2.13.0 README (grep count 2), so it is in a release.
- `down` "is not technically a toxic in the implementation of Toxiproxy. This is done by `POST`ing to `/proxies/{proxy}` and setting the `enabled` field to `false`." (README:400-404). Adding a toxic of an unregistered type returns `ErrInvalidToxicType` (`toxic_collection.go`: `if toxics.New(wrapper) == nil { return nil, ErrInvalidToxicType }`; `toxics.New` returns nil when the type is not in `ToxicRegistry`, toxics/toxic.go:172-179).
- Direction: "Toxics are directional: by default a latency toxic is attached to the `downstream` stream (`server -> client`)." (README:390-393). Toxic fields: `stream` "defaults to `downstream`"; `toxicity` "probability of the toxic being applied to a link (defaults to 1.0, 100%)"; "`upstream` applies the toxic on the `client -> server` connection, while `downstream` applies the toxic on the `server -> client` connection." (README:498-510).
- `timeout`: "Stops all data from getting through, and closes the connection after `timeout`. If `timeout` is 0, the connection won't close, and data will be dropped until the toxic is removed." (README:422-426). `reset_peer`: "Simulate TCP RESET (Connection reset by peer)" (README:432-434). `limit_data`: "Closes connection when transmitted data exceeded limit." (README:452-456).
- Toxicity sampling: `randomToxicity := rand.Float32()` then `if randomToxicity < toxic.Toxicity { toxic.Pipe(s) } else { new(NoopToxic).Pipe(s) }` per `ToxicStub.Run` (toxics/toxic.go:89-100). The draw uses Go's global `math/rand` with no user seed; `go.mod` declares `go 1.27.0`. So a `toxicity < 1` run is not replayable from a seed. (Global-source auto-seeding behavior of Go >= 1.20 is from Go docs not read here; listed unverified.)
- API: HTTP on port 8474; endpoints include `POST /proxies`, `POST /proxies/{proxy}` (update, e.g. `enabled`), `DELETE /proxies/{proxy}`, `POST /proxies/{proxy}/toxics`, `DELETE /proxies/{proxy}/toxics/{toxic}`, `POST /reset` ("Enable all proxies and remove all active toxics") (README:513-528). "Changing the `listen` or `upstream` fields will restart the proxy and drop any active connections." (README:488).
- Auth: "The API is unauthenticated by default ... start the server with `TOXIPROXY_AUTH_TOKEN` set; every request must then send `Authorization: Bearer <token>`." (README:473-478). Present in the v2.13.0 README too.
- FAQ: MySQL "will prefer the local Unix domain socket for some clients ... if the host is set to `localhost`" (README:620-624), so traffic can bypass the proxy.

What it cannot do (from the above): it acts only on TCP connections routed through its listen address. It has no operation that kills, pauses or restarts a process and none that changes a clock: no such toxic is registered and no such endpoint is listed. (Absence established from the registered-toxic list and the endpoint list; it does not prove no external plugin exists.) A partition between two database nodes needs their replication traffic routed through Toxiproxy too, not only the app-to-database link. (Inference.)

### H8. toxiproxy-node-client: API, gaps vs the server, license

Pinned: `ihsw/toxiproxy-node-client` master `d7782a4ee344ad30f7030f7dc63a8567f052c5e2` (committed 2026-04-26; repo pushed 2026-09-07; not archived). npm `toxiproxy-node-client` latest 4.1.0, published 2026-04-26, `license: "ISC"`, `engines: {"node":">=18"}`, no runtime `dependencies` (npm registry JSON). Listed in Toxiproxy README client list (README:90).

API (source):
- `new Toxiproxy(host)`; `createProxy(body)`, `populate(body)`, `get(name)`, `getVersion()`, `reset()`, `getAll()` (src/Toxiproxy.ts:24-62).
- `Proxy.remove()` (DELETE), `Proxy.update(body)` ("Updates the existing proxy on the server (e.g. disable an enabled proxy)"), `Proxy.addToxic(body)`, `Proxy.getToxic(name)` (src/Proxy.ts:66-102).
- `Toxic.remove()`, `Toxic.update(body)` (src/Toxic.ts:176-186). Toxic body fields `name`, `stream`, `type`, `toxicity` ("Percentage of connections the toxic will affect"), `attributes` (src/interfaces.ts:57-86).
- README example: `toxiproxy.createProxy({listen: "localhost:0", name: "redis", upstream: "redis:6379"})` then `proxy.addToxic({attributes: {rate: 1000}, type: "bandwidth"})` (README:15-33).
- HTTP is global `fetch` (src/HttpClient.ts:48-51); non-2xx throws `ToxiproxyError` "Request failed with status code ...".

Gaps (source facts):
- `type Type = "latency" | "down" | "bandwidth" | "slow_close" | "timeout" | "slicer" | "limit_data" | "reset_peer"` (src/Toxic.ts:9-16): no `packet_loss`, and it lists `down`, which the server does not register as a toxic (H7). Bring a proxy down with `proxy.update({ enabled: false })` instead. (The TS type union is compile-time only; whether a `packet_loss` body passes at runtime with a cast was not executed.)
- The client sets only `Content-Type` (src/HttpClient.ts:30-34); it sends no `Authorization` header, so it cannot talk to a server started with `TOXIPROXY_AUTH_TOKEN` (H7) without modification.

License discrepancy resolved: no `LICENSE` file in the repo tree at the pin (tree listing) nor in the npm 4.1.0 tarball (tarball file list: `dist/*`, `package.json`, `README.md` only); `package.json:22` and npm metadata say `"license": "ISC"`; GitHub API license is null because there is no license file to detect. So the only license statement is the package.json ISC declaration. The drafter should write "ISC (declared in package.json; no license file shipped)".

Also found: `@testcontainers/toxiproxy` 12.2.1 (npm, MIT, published 2026-10-13) depends on `toxiproxy-node-client ^4.1.0` and `testcontainers ^12.2.1`; its `ToxiProxyContainer` starts the server image and `createProxy` picks the next free port from 8666 with control port 8474 (testcontainers-node tag v12.2.1, `packages/modules/toxiproxy/src/toxiproxy-container.ts:4-89`). This is a maintained way to get a disposable Toxiproxy server from a Node test.

### H9. MSW is in-process request interception, not deployment faults

Pinned: docs repo `mswjs/mswjs.io` main `bda552ebaadde6d75870b4d07de734f9de35fd89` (read 2026-11-09); library pin from F11 `mswjs/msw` `9bbfe99cd52beeb952fdaa1cd2901c019e4b858e` (still latest, 2026-11-06).

Facts:
- `setupServer`: "A function that configures the interception of requests in a Node.js process. Despite the word "server" in the name, it _does not_ establish any servers, operating entirely in the thread of your process." and "it augments the standard request modules like `http` in order to react to outgoing requests and respond to them from your mock definitions." (`src/content/api/setup-server/index.md`).
- Network errors: `HttpResponse.error()` "results in a network error, **aborting the pending request**"; used "to simulate network errors, such as: DNS errors; Connection timeouts; Client going offline." The client receives "a generic `TypeError: Failed to fetch` error" (`src/content/docs/http/mocking-responses/network-errors.md`).
- MSW describes itself as "network behavior ... a contract-like description of the network's expected state" (`src/content/docs/philosophy.md:21`) and says it "intercepts requests on the network level" (`src/content/docs/faq.md:21`). Use MSW's own wording; do not call it "application-layer" as a quote.

Consequence (synthesis): with MSW the request never reaches a real server; the handler is the server. A mocked network error therefore has a known effect (whatever the handler did), so it cannot produce the real ambiguous case where a write was applied and the response lost, unless the handler models that state itself. It intercepts only requests made through the patched modules in the same process; a database driver's raw TCP socket or another process is not intercepted (the doc names "standard request modules like `http`"; which other modules are patched was not enumerated, unverified). MSW belongs to client-side error-handling tests and `schedule-exploration` response ordering (F11), not to `distributed-fault-testing` verdicts about a deployment.

### H10. Node-native process kill/restart/pause in tests: what exists

Facts:
- Node core: `subprocess.kill([signal])` "sends a signal to the child process. If no argument is given, the process will be sent the `'SIGTERM'` signal." "While the function is called `kill`, the signal delivered to the child process may not actually terminate the process." On Windows "`'SIGKILL'`, `'SIGTERM'`, `'SIGINT'` and `'SIGQUIT'` terminate the process forcefully and abruptly", and "A signal name that does not exist on Windows (such as `'SIGSTOP'`) throws an `ERR_UNKNOWN_SIGNAL` error." "On Linux, child processes of child processes will not be terminated when attempting to kill their parent." (v26.13.0 `doc/api/child_process.md`, section `subprocess.kill([signal])` from line 1697). So a test that spawned the server can kill it, and on POSIX pause/resume it with `SIGSTOP`/`SIGCONT`; Windows has no pause signal.
- testcontainers-node v12.2.1 (MIT, pushed 2026-11-09, not archived): `StartedTestContainer` has `stop(options?)`, `restart(options?)`, `exec(...)` and no pause method (`packages/testcontainers/src/test-container.ts:71-91`). `restart` and `stop` default `timeout: 0` (`started-generic-container.ts:94, 129`); `stop` also defaults `remove: this.autoRemove` and `removeVolumes: true` (line 129). Docs: `container.stop({ timeout: 10_000 }); // 10 seconds` and `stop({ remove: false })` to keep the container for copying files (`docs/features/containers.md:384-396, 233-236`). What Docker does with timeout 0 (immediate SIGKILL) is from Docker API semantics not read here (unverified).
- `h2non/toxy` (Node HTTP fault-injection proxy): archived, last push 2022-02-17 (GitHub API). Stale; not selected.
- npm search `keywords:chaos-engineering` (registry API, 2026-11-09) returned only small recent packages (e.g. `chaosbringer`, `faultlib`, `@mizchi/playwright-faults`); none was evaluated, and no maintained, widely used Node-native tool for process or clock faults was found. Clock faults: none found for real processes (Node mock timers are virtual time inside one process, F8).

Consequence: for a Node service under `distributed-fault-testing`, process faults come from the test's own process control (`child_process` kill/signals, or testcontainers `stop`/`restart`) or from Jepsen; network faults from Toxiproxy; clock faults have no Node route and stay with Jepsen or are declared out of scope. Fault activation must still be observed independently (existing rule, `distributed-fault-testing/SKILL.md:22`), e.g. confirm the child's `'exit'`/`'close'` signal or the container state.

## Decisions for the drafter

1. `linearizability-checking`: add a short "Recording from a Node client" section to `references/model-and-history.md` (it already holds recorder rules at lines 9-13): `process.hrtime.bigint()` not `Date.now()` (H1); invoke before the call, completion first thing in `.then`/`.catch` (H2); one event list in program order is valid real-time evidence for `CheckEvents` (H3, H4); never-settling promises closed at history end as model-specific unknowns (H2); bigint serialization (H1). Add to `references/porcupine-operation.md` a two-line note that Porcupine reads no files, so a Node history needs a Go decoder to `Operation{ClientId, Input, Call, Output, Return}` or `Event{ClientId, Kind, Value, Id}` (H4). No new reference file needed.
2. `transactional-history-testing`: add a "Node recorder to elle-cli JSON" section to `references/elle-operation.md` with the exact field list and keywordization rule (H5), the file-order rule for realtime (H5), the fixture path `test/test-data/` (README path missing, H5), and the license wording (H6). Mapping `TimeoutError`/`AbortError` to `:info` and fresh process ids goes in `references/history-and-boundaries.md` next to line 12.
3. `distributed-fault-testing`: add a new `references/node-toxiproxy.md` (or a section in `fault-model-and-activation.md`): Toxiproxy server facts and limits (H7), the Node client API with its two gaps and ISC-by-package.json license (H8), `@testcontainers/toxiproxy` as the disposable-server route (H8), process faults via `child_process`/testcontainers (H10), no clock route (H10), MSW is not a deployment fault (H9).
4. Description wording (proposed, each under the current length style):
   - `linearizability-checking`: "... Use for linearizability models, Porcupine integration, recording histories from Go or Node.js clients, history partitioning, or investigating a concurrent object counterexample."
   - `transactional-history-testing`: "... Use when searching for transactional anomalies, checking histories recorded by a Node.js or other non-JVM client with elle-cli, extending an existing history checker, or investigating recorder boundaries, uncertain outcomes and missing dependency evidence."
   - `distributed-fault-testing`: "... Use when extending a Jepsen-style campaign, injecting network faults into a Node.js service with Toxiproxy, testing failover or recovery, or investigating whether injected faults and ambiguous requests were represented faithfully."

## Common mistakes (with evidence)

- **Timestamping with `Date.now()`.** Wall clock "can decrease, making it unreliable for performance measurement or recording the orders of events" (HR-Time, H1). Use `process.hrtime.bigint()`.
- **`JSON.stringify` on bigint timestamps, or `Number(hrtime)` of raw values.** Throws TypeError (ECMA-262 25.5.4.2); Number conversion loses precision above 2^53 ns (H1).
- **Recording invoke after the request is sent / sorting events by op id before export.** Porcupine Events and Elle's `realtime-graph` use list order as time (H4, H5); late invoke shrinks intervals (H2).
- **Relying on `AbortSignal.timeout` to close pending operations.** Its timer is unref'd and cleared on GC (H2); the process can exit with operations never closed. Close open invocations as `:info` yourself.
- **Writing a timeout/abort as `:fail`.** The request may have been applied; aborting only stops the client waiting (H2; Jepsen semantics in existing skills).
- **Several concurrent calls under one logical client id.** Processes "are logically singlethreaded" (H5).
- **Using the client's `type: "down"` toxic.** The server registers no `down` toxic and returns `ErrInvalidToxicType`; use `proxy.update({ enabled: false })` (H7, H8).
- **Expecting `packet_loss` or auth-token support from toxiproxy-node-client 4.1.0.** Not in its type union; no Authorization header (H8).
- **Setting `toxicity < 1` and expecting replay.** Unseeded `rand.Float32()` per link (H7).
- **Proxying only app-to-DB traffic and calling it a partition.** Toxiproxy acts only on connections routed through it; MySQL on `localhost` may use a Unix socket and bypass it (H7).
- **Counting an MSW `HttpResponse.error()` as a deployment fault.** MSW "does not establish any servers, operating entirely in the thread of your process" (H9).
- **Calling `container.stop()` to simulate a crash and then looking for data.** testcontainers `stop` defaults to removing the container and volumes when auto-remove is on (H10); use `restart()` or `stop({ remove: false })`.
- **Sending `SIGSTOP` on Windows.** Throws `ERR_UNKNOWN_SIGNAL` (H10).

## Sources inventory

| Source | Pin / version | Used for |
|---|---|---|
| nodejs/node `doc/api/process.md`, `perf_hooks.md`, `globals.md`, `worker_threads.md`, `child_process.md` | tag v26.13.0, commit 18b32a3b1552e199a01f1a8d9fd64aa756d3b75b | H1, H2, H3, H10 |
| nodejs/node `src/node_process_methods.cc`, `src/node_perf.cc`, `src/node_perf_common.h`, `lib/internal/perf/utils.js`, `lib/internal/abort_controller.js` | same | H1, H2 |
| libuv (bundled) `deps/uv/docs/src/misc.rst`, `src/unix/core.c`, `src/unix/linux.c`, `src/win/util.c` | libuv 1.52.1 in Node v26.13.0 | H1 |
| Linux clock_gettime(2) | man-pages 6.19, 2026-03-07 | H1 |
| W3C High Resolution Time (Editor's Draft) | w3c/hr-time main 76c362ed3194d99d8563608be0bb6a73e06935b8 | H1 |
| ECMA-262 living draft, 25.5.4.2 SerializeJSONProperty | tc39.es/ecma262, read 2026-11-09 | H1 |
| WHATWG DOM Living Standard, AbortSignal.timeout | dom.spec.whatwg.org, read 2026-11-09 | H2 |
| nodejs/learn `pages/asynchronous-work/dont-block-the-event-loop.md` | main ea10f2a6af515ec69885f517984ef8628f0eb37b | H3 |
| anishathalye/porcupine `model.go` | v1.3.1, 97cd067defd99df172053ba7f4ca5bbae57fe446 | H4 |
| ligurio/elle-cli `README.md`, `src/elle_cli/cli.clj`, `project.clj`, `LICENSE`, `test/test-data/*.json` | master 3c2504815945cd4ab1b5cc0142d2fe206e1ee285 | H5, H6 |
| jepsen-io/history `README.md` | 61d2776c889ad84f7c6922977cf05e8f11970402 | H5 |
| jepsen-io/elle `src/elle/core.clj` | 4e359e597c52938b0afebb8bc42273914d68a424 | H5 |
| Shopify/toxiproxy `README.md`, `toxics/*.go`, `toxic_collection.go`, `link.go`, `go.mod` | main 49299d8838525126e09c85ebe0ba89940a3261e5; v2.13.0 README for release check | H7 |
| ihsw/toxiproxy-node-client `README.md`, `package.json`, `src/*.ts` | master d7782a4ee344ad30f7030f7dc63a8567f052c5e2; npm 4.1.0 tarball and registry JSON | H8 |
| testcontainers/testcontainers-node toxiproxy module, `test-container.ts`, `started-generic-container.ts`, `docs/features/containers.md` | tag v12.2.1 (tag object 17316dbd001bf7468023087e3620a134466f32c5); npm @testcontainers/toxiproxy 12.2.1 | H8, H10 |
| mswjs/mswjs.io `api/setup-server/index.md`, `docs/http/mocking-responses/network-errors.md`, `docs/philosophy.md`, `docs/faq.md` | main bda552ebaadde6d75870b4d07de734f9de35fd89 | H9 |
| GitHub API repo metadata (license, archived, pushed) for elle-cli, toxiproxy, toxiproxy-node-client, toxy, testcontainers-node | read 2026-11-09 | H6, H7, H8, H10 |
| npm registry search `keywords:chaos-engineering` | read 2026-11-09 | H10 |

## Unverified (stated, not checked)

- Windows `QueryPerformanceCounter` values being comparable across processes (H1).
- Float rounding of `performance.now()` ties in practice (H1); only the {number} type is documented.
- ECMA-262 `Promise.prototype.finally` passes no arguments to its callback (H2).
- Default `AbortError` name for `abort()` without a reason (DOM standard not re-read for that clause) (H2).
- Whether elle-cli's `json/read-str` accepts newline-separated JSON objects rather than one array; all real samples are arrays, so use an array (H5).
- Whether Knossos (via `history/parse-ops`) also uses file order rather than `:time` for real time; Elle's use of file order is verified (H5).
- Why GitHub reports elle-cli's license as NOASSERTION (H6).
- Go `math/rand` global source auto-seeding semantics for Go >= 1.20 (H7).
- Whether a `packet_loss` toxic body sent through toxiproxy-node-client with a type cast works at runtime (H8).
- Which Node modules MSW's `setupServer` patches beyond `http` (H9).
- Docker stop/restart with timeout 0 meaning immediate SIGKILL (H10).
- The small npm chaos packages found in H10 were not evaluated.
- No code in this report was executed.
