# Improvement pass: JS/TS additions to linearizability-checking, transactional-history-testing, distributed-fault-testing

Scope: sentences added in commit "Add Node history recording and Toxiproxy fault routes" under `plugins/`.

## Summary

Every added sentence was checked against its pinned source (fetched 2026-11-09). Two text/metadata errors fixed (F2, F3), three pre-existing fragment mismatches fixed (F1). No quote was found inexact; no API name, toxic type, version or license was wrong. Drafter open items: `slow_close` registration confirmed (below); the Knossos file-order item does not apply because none of the three skills mentions Knossos (`grep -rni knossos` over the three directories: no output). Other drafter open items (unexecuted recorder patterns, Go global rand seeding, runtime behaviour of a cast `packet_loss` body, MSW modules beyond `http`, hrtime across processes on Windows) are not claimed by the text beyond what the sources show, so no edit.

INFO, not edited: some distributed-fault-testing sources.yaml `sections_used` items name material read for support but not quoted (Toxiproxy README "port 8474"; toxic.go "New (registry lookup)", which is the lookup behind `ErrInvalidToxicType`; node-client package.json "engines"). They are accurate descriptions of what was read.

## Findings

Sources fetched 2026-11-09 to the session scratchpad from the pinned URLs in the text. Node pin 18b32a3 is v26.13.0 (`src/node_version.h`: MAJOR 26, MINOR 13, PATCH 0, IS_RELEASE 1).

### F1 linearizability-checking/references/sources.yaml:43, :68 — WARNING (pre-existing URL mismatch)
- Said: text cites `https://go.dev/ref/mem#overview` (SKILL.md, common-mistakes.md:9), `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags` and `#hdr-Test_packages` (porcupine-operation.md:35); sources.yaml listed `https://go.dev/ref/mem` and one `https://pkg.go.dev/cmd/go@go1.27.3` entry.
- Source / convention: other skills record the fragment exactly as cited (`coverage-guided-fuzzing/references/sources.yaml:89`, `race-detection-campaigns/references/sources.yaml:35`: `url: "https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags"`). Anchors verified live: go.dev/ref/mem `id="overview">Informal Overview`; pkg.go.dev `id="hdr-Test_packages">Test packages`, `id="hdr-Testing_flags">Testing flags`.
- Fix: go.dev URL given `#overview`; the go command entry split into two entries, one per cited fragment, each keeping its own sections_used.

### F2 transactional-history-testing/references/elle-operation.md:13 — WARNING (condition misstated)
- Said: `value-reader` keywordizes micro-operation names "for a `value` that is a non-empty vector of vectors starting with a string".
- Source: elle-cli cli.clj:59-68 at 3c25048 (https://raw.githubusercontent.com/ligurio/elle-cli/3c2504815945cd4ab1b5cc0142d2fe206e1ee285/src/elle_cli/cli.clj): `(and (= key :value) (vector? value) (not (empty? value)) (vector? (first value)) (not (empty? (first value))) (string? (ffirst value))) (map #(assoc %1 0 (keyword (first %1))) value)`. Only the first element is tested; "vector of vectors" claims a check on every element that the code does not make.
- Fix: "a non-empty vector whose first element is a non-empty vector starting with a string".

### F3 transactional-history-testing/references/sources.yaml:136 — WARNING (sources.yaml lists a section the text does not use)
- Said: globals.md entry sections_used includes "Static method: AbortSignal.timeout(delay)".
- Source: the only citation of globals.md (history-and-boundaries.md:14) quotes the `AbortController` class text (globals.md:44 "A utility class used to signal cancelation in selected `Promise`-based APIs."); the `AbortSignal.timeout` claim in that sentence is cited to abort_controller.js.
- Fix: removed that sections_used item.

### Checked, entailed (transactional-history-testing additions)
- cli.clj:70-75 `read-json-history` = `(json/read-str (slurp filepath) :key-fn keyword :value-fn value-reader)`; :61 keywordizes `:type`/`:f`; :62 comment exact; cli.clj:256 `(h/history (read-history filepath))`.
- rw-register-partial-info.json first record exact, last record `{"index":6,"process":3,"type":"invoke",...}` with no completion; list-append-anomaly-g1a-aborted-read.json has no `f` or `time`.
- elle-cli README:56 example path `histories/elle/rw-register.json`; recursive tree API listing at 3c25048 (180 paths, `"truncated": false`) has no path containing `histor`.
- Elle core.clj:373 "a < b if a ends before b begins", :382 "iterate through the history".
- jepsen.history README:48 "must be one of `:invoke`, `:ok`, `:info`, or `:fail`", :56 "is a long: The time since the start of the test, in nanoseconds", :59-60 "logically singlethreaded, and can execute only one thing at a time", :75-76 "users may omit indices".
- elle-cli LICENSE line 1 "Eclipse Public License - v 2.0"; Exhibit A (:262-270) names "GNU General Public License ... version 2 ... or (at your option) any later version, with the GNU Classpath Exception"; project.clj:4 license string exact.
- globals.md:44 AbortController text exact; abort_controller.js:211-214 DOMException text exact.

### Drafter open item resolved: Toxiproxy `slow_close` registration
- toxics/slow_close.go:33 at 49299d8 (https://raw.githubusercontent.com/Shopify/toxiproxy/49299d8838525126e09c85ebe0ba89940a3261e5/toxics/slow_close.go): `Register("slow_close", new(SlowCloseToxic))`. The full `Register(` set in `toxics/` is bandwidth.go:95, latency.go:55, limit_data.go:59, noop.go:24, packet_loss.go:101, reset_peer.go:37, slicer.go:99, slow_close.go:33, timeout.go:52 — exactly the nine names in fault-model-and-activation.md. Repo-wide (recursive tree, `"truncated": false`), the only other `toxics.Register` calls are in `_examples/toxics/` (`debug`, `http`), a directory the Go tool ignores. The text's list is correct; no edit.

### Checked, entailed (distributed-fault-testing additions)
- Toxiproxy README:15 "A TCP proxy written in Go", :17 "configure your application to make all test connections go through Toxiproxy", :390-391 "Toxics are directional: by default a latency toxic is attached to the `downstream` stream (`server -> client`)", :502 `stream` "defaults to `downstream`", :402-404 down "is not technically a toxic ... `POST`ing to `/proxies/{proxy}` and setting the `enabled` field to `false`", :474-476 "unauthenticated by default", "every request must then send `Authorization: Bearer <token>`", :620-621 MySQL "will prefer the local Unix domain socket for some clients ... if the host is set to `localhost`".
- toxic.go:5 `"math/rand"`, :94-95 `randomToxicity := rand.Float32()` / `if randomToxicity < toxic.Toxicity`; `ToxicWrapper` (:54-63) has no seed field; no "seed" anywhere in toxics/, toxic_collection.go or README.
- toxic_collection.go:111-112 `if toxics.New(wrapper) == nil { return nil, ErrInvalidToxicType }`.
- toxiproxy-node-client d7782a4 (= npm 4.1.0 `gitHead`): package.json:3 `"version": "4.1.0"`, :22 `"license": "ISC"`; root tree has no LICENSE file; Toxic.ts `Type` union includes `"down"`, lacks `packet_loss`; Proxy.ts:71 "Updates the existing proxy on the server (e.g. disable an enabled proxy)."; HttpClient.ts sets only `{ "Content-Type": "application/json" }`, no Authorization.
- testcontainers-node 17316dbd is tag v12.2.1 (refs/tags API, type commit); npm `@testcontainers/toxiproxy@12.2.1` license MIT, gitHead a3465510 is 1 commit ahead (version-bump: package.json/package-lock files). toxiproxy-container.ts `CONTROL_PORT = 8474`, `FIRST_PROXIED_PORT = 8666`, imports `toxiproxy-node-client`. test-container.ts:71-91 `stop`, `restart`, `exec`; no pause. started-generic-container.ts:129 `{ remove: this.autoRemove, timeout: 0, removeVolumes: true, ...options }`; generic-container.ts:62 `autoRemove = true`.
- child_process.md:1743-1744 "may not actually terminate the process", :1754 `'SIGSTOP'` "throws an `ERR_UNKNOWN_SIGNAL` error", :1757 "On Linux, child processes of child processes will not be terminated".
- MSW setup-server/index.md:14 "_does not_ establish any servers, operating entirely in the thread of your process", :18 "augments the standard request modules like `http`"; network-errors.md:12 "results in a network error, **aborting the pending request**".

### Checked, entailed (linearizability-checking Node additions)
- process.md:2589 "current high-resolution real time in nanoseconds as a `bigint`"; process.md:2544-2546 "not related to the time of day and therefore not subject to clock drift"; process.md:41-42 `'beforeExit'` "_not_ emitted for conditions causing explicit termination, such as calling [`process.exit()`][] or uncaught exceptions" (the skill drops the link brackets; wording exact).
- hr-time index.bs:249 "can decrease, making it unreliable for performance measurement or recording the orders of events. The web platform shares a [=wall clock=] with [[ECMA-262]] time".
- node_perf.cc:41 `performance_process_start = PERFORMANCE_NOW()`, :375-377 `(uv_hrtime() - performance_process_start) / NANOS_PER_MILLIS` as double.
- node_process_methods.cc:725-726 `HrtimeBigIntImpl` uses `uv_hrtime()`.
- abort_controller.js:196-217 comment "keep the Node.js process open on it's own", `timeout.unref()`, FinalizerRegistry clears on GC, `new DOMException('The operation was aborted due to timeout', 'TimeoutError')`.
- ECMA-262 SerializeJSONProperty: "If _value_ is a BigInt, throw a *TypeError* exception."
- nodejs/learn dont-block-the-event-loop.md:12 "Node.js runs JavaScript code in the Event Loop (initialization and callbacks)".
- Porcupine model.go:20,68 `ClientId int // optional, unless you want a visualization; zero-indexed`; Input/Output/Value `interface{}`; no `json:` tags; no non-test file in the repo opens or decodes files (grep of porcupine.go, checker.go, visualization.go, bitset.go).
- node_perf_common.h:19 `#define PERFORMANCE_NOW() uv_hrtime()`, so `performance.now()` is the same source.

## Validation (after edits)

- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/<skill>`: `Skill is valid!` for linearizability-checking, transactional-history-testing, distributed-fault-testing.
- Relative links and URL two-way match (scratchpad script `check_links_jshf.py`: every `](...)` target in each skill's .md files vs `references/sources.yaml` `url`s): all three skills report "broken relative links: none", "cited in text, not in sources.yaml: none", "in sources.yaml, not cited in text: none".
- `git diff --check` on the three skill directories and this report: no output, exit 0.
- Diff: linearizability-checking/references/sources.yaml (+9 −4), transactional-history-testing/references/elle-operation.md (1 line), transactional-history-testing/references/sources.yaml (−1). Not committed or pushed.
