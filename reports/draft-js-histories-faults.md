# Draft: JS/TS (Node) extension, group H (histories and faults)

Drafter: draft-js-histories-faults. Skills: linearizability-checking, transactional-history-testing, distributed-fault-testing.

## Progress

- [x] Inputs read: `reports/research-js-histories-faults.md` (H1-H10), `reports/skill-plan-js-web-bugfinding.md` rows 39-40, all three skills' SKILL.md, `model-and-history.md`, `porcupine-operation.md`, `elle-operation.md`, `history-and-boundaries.md`, `fault-model-and-activation.md`, each `common-mistakes.md` and `sources.yaml`; `reports/draft-js-resource.md` for report shape.
- [x] Re-fetch pinned sources and check every quote to be cited (curl/gh, read-only, into scratchpad `h/`)
- [x] Edit linearizability-checking: description adds "recording histories from Go or Node.js clients"; SKILL.md route clause; `model-and-history.md` new section "Record from a Node.js client" (clock, bigint JSON, single-loop event order, invoke/return placement, one op per ClientId, worker threads, never-settling promises; labelled synthesis, not executed); `porcupine-operation.md` paragraph on Porcupine reading no files; 2 common mistakes; 7 sources.
- [x] Edit transactional-history-testing: description adds "checking histories recorded by a Node.js or other non-JVM client with elle-cli"; SKILL.md route clause; `elle-operation.md` license-file sentence and new section "Write elle-cli JSON from a Node.js recorder" (keywordization, field semantics, fixtures, missing README path, file order is realtime evidence, integer `time`); `history-and-boundaries.md` abort/timeout -> `:info`, fresh process id; 2 common mistakes; 6 new sources, 2 existing entries' sections_used extended. Removed an `AbortError` name claim (research lists it unverified).
- [x] Edit distributed-fault-testing: description adds "injecting network faults into a Node.js service with Toxiproxy"; SKILL.md route clause; `fault-model-and-activation.md` new section "Node.js services without Jepsen" (Toxiproxy scope, registered toxics, direction, `down`, routing, unseeded toxicity, auth; node client license/gaps; @testcontainers/toxiproxy; child_process and testcontainers process control; no clock route; MSW); 4 common mistakes; 14 sources with evidence fragments (each grepped on one line of the fetched file; tree page fragment checked in the HTML).
- [x] Validate (outputs below)

Status: draft complete, validation passed. Nothing committed or pushed. No recorder, client or command in the edits was executed.

## Files changed

- `plugins/bugfinding/skills/linearizability-checking/SKILL.md` (description; route clause)
- `plugins/bugfinding/skills/linearizability-checking/references/model-and-history.md` (section "Record from a Node.js client")
- `plugins/bugfinding/skills/linearizability-checking/references/porcupine-operation.md` (Porcupine reads no files; Go decoder)
- `plugins/bugfinding/skills/linearizability-checking/references/common-mistakes.md` (2 entries)
- `plugins/bugfinding/skills/linearizability-checking/references/sources.yaml` (7 entries)
- `plugins/bugfinding/skills/transactional-history-testing/SKILL.md` (description; route clause)
- `plugins/bugfinding/skills/transactional-history-testing/references/elle-operation.md` (license-file sentence; section "Write elle-cli JSON from a Node.js recorder")
- `plugins/bugfinding/skills/transactional-history-testing/references/history-and-boundaries.md` (abort/timeout paragraph)
- `plugins/bugfinding/skills/transactional-history-testing/references/common-mistakes.md` (2 entries)
- `plugins/bugfinding/skills/transactional-history-testing/references/sources.yaml` (6 entries; 2 sections_used extended)
- `plugins/bugfinding/skills/distributed-fault-testing/SKILL.md` (description; route clause)
- `plugins/bugfinding/skills/distributed-fault-testing/references/fault-model-and-activation.md` (section "Node.js services without Jepsen")
- `plugins/bugfinding/skills/distributed-fault-testing/references/common-mistakes.md` (4 entries)
- `plugins/bugfinding/skills/distributed-fault-testing/references/sources.yaml` (14 entries)
- `reports/draft-js-histories-faults.md` (this report)

No new reference files: the lead asked for sections in existing files, so research decision 3's optional `node-toxiproxy.md` was not created.

## Validation output

```text
uv run --no-project --with pyyaml python .../quick_validate.py plugins/bugfinding/skills/linearizability-checking
Skill is valid!
... transactional-history-testing
Skill is valid!
... distributed-fault-testing
Skill is valid!

git diff --check -- (the three skill dirs)
(no output) exit 0

scratchpad check_links.py (read-only; cited URL set vs sources.yaml URL set, duplicate URLs, local link targets)
linearizability-checking: sources 21 dups []
  cited-not-in-inventory ['https://go.dev/ref/mem#overview', 'https://pkg.go.dev/cmd/go@go1.27.3#hdr-Test_packages', 'https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags']
  inventory-not-cited ['https://go.dev/ref/mem', 'https://pkg.go.dev/cmd/go@go1.27.3']
  errors []
transactional-history-testing: sources 21 dups [] cited-not-in-inventory [] inventory-not-cited [] errors []
distributed-fault-testing: sources 29 dups [] cited-not-in-inventory [] inventory-not-cited [] errors []
```

The linearizability mismatches are pre-existing (committed text cites `#fragment` URLs whose inventory entries omit the fragment); they differ only by fragment, and none involves an entry added here. Every URL added in this draft matches its inventory entry exactly, including `https://tc39.es/ecma262/#sec-serializejsonproperty`.

## Remaining unverified

- Recorder patterns (invoke before call, return first in continuation, one array per event loop, bigint-difference serialization, closing open calls from the driver's deadline, fresh process id after abort) are labelled synthesis and were not executed.
- ECMA-262 is an unversioned living draft (read 2026-11-09).
- Go global `math/rand` seeding semantics: the text says only that the toxic exposes no seed, not how Go seeds the global source.
- `slow_close` registration was taken from the research report plus the `toxics/slow_close.go` filename; its `Register("slow_close")` line was not grepped (my fetch used the wrong filename).
- Whether a `packet_loss` body sent through toxiproxy-node-client with a type cast works at runtime; the text claims only the TS union omits it.
- Which modules MSW's `setupServer` patches beyond `http` (text quotes "like `http`" only).
- Whether Knossos histories also use file order for real time; the text claims file order only for Elle's `realtime-graph`.
- Windows cross-process comparability of hrtime; the text applies the existing "do not invent real-time edges from unsynchronized client clocks" rule across processes and hosts instead.
- Default name of a reasonless `abort()` rejection; removed from the text.
- Research cited HR-Time at `index.html`, which 404s at the pin; the draft cites `index.bs` at the same commit, where the quotes were found.

## Source re-check (this turn)

All fetched at the research pins and grepped for the exact text to be quoted. Matched:

- Node v26.13.0 (commit `18b32a3b...`): `process.md` hrtime.bigint "current high-resolution real time in nanoseconds as a `bigint`" (2588-2589), legacy hrtime "not related to the time of day and therefore not subject to clock drift" (2544-2546), `beforeExit` (32-42), exit 13 "never settled" (4631); `perf_hooks.md:345`; `node_perf.cc:41, 375-376` (`uv_hrtime() - performance_process_start`); `node_process_methods.cc:719`; `abort_controller.js:196-217` (unref'd timer, WeakRef, FinalizerRegistry, `TimeoutError`); `globals.md:44, 131`; `child_process.md:1743-1757`.
- `nodejs/learn` `ea10f2a6`: `dont-block-the-event-loop.md:12, 26`.
- W3C hr-time `76c362ed`: research cited `index.html`, which 404s; the source file is `index.bs` (tree listing). Quotes at `index.bs:249` ("can decrease, making it unreliable ... recording the orders of events") and `:252` ("never decreases"). Cite the pinned `index.bs`.
- ECMA-262 living draft: SerializeJSONProperty contains "If value is a BigInt, throw a TypeError exception." (after the toJSON step, which also applies to BigInt values).
- Porcupine `model.go`: no `json` occurrences; `Operation`/`Event` fields as research H4.
- elle-cli `3c25048`: `cli.clj` `value-reader` and `read-json-history` text as H5; `project.clj:4` license and `:16` data.json 2.4.0; README:56 example path; tree has 0 `histories/` paths; the two test-data fixtures match H5 byte for byte in content; `LICENSE` line 1 "Eclipse Public License - v 2.0", Exhibit A at 262-273.
- Elle `core.clj` `realtime-graph` docstring and comment (371-385).
- jepsen.history README lines 48, 56, 59, 69, 72, 75.
- Toxiproxy `49299d8`: README 15, 390, 402-404, 424, 434, 458 (`packet_loss` section), 472-476 (8474, auth), 503 (toxicity), 528 (`/reset`), 620-624 (MySQL socket); `toxic.go:89-100` (`rand.Float32()`), `:172-179`; `toxic_collection.go:112`; `Register(...)` set: latency, bandwidth, timeout, reset_peer, slicer, limit_data, packet_loss, noop, plus `slow_close.go` (not grepped; filename confirmed in tree). No toxic file for process or clock (tree listing).
- toxiproxy-node-client `d7782a4`: `Toxic.ts:9-16` union; `HttpClient.ts:30-34` only Content-Type; `Proxy.ts:71-75` update; `package.json:22` ISC; tree has no LICENSE file; npm 4.1.0 license ISC.
- testcontainers-node v12.2.1 (`17316dbd...`, lightweight tag, same file content fetched by hash): toxiproxy container ports 8474/8666 and client import; `test-container.ts` stop/restart/exec, no pause; `started-generic-container.ts:94, 129` defaults; `containers.md:235, 388, 395`. npm `@testcontainers/toxiproxy@12.2.1` MIT, depends on `toxiproxy-node-client ^4.1.0`.
- MSW docs `bda552e`: `setup-server/index.md:14, 18`; `network-errors.md:12-26`. Correction vs research: the docs text says `Response.error()` "results in a network error, **aborting the pending request**", with code example `HttpResponse.error()`; quote accordingly.

## Plan

1. linearizability-checking: description names Node.js clients; Node recorder section in `model-and-history.md`; Porcupine-reads-no-files note in `porcupine-operation.md`; two common mistakes; sources.
2. transactional-history-testing: description; "Node recorder to elle-cli JSON" section in `elle-operation.md` (fields, keywordization, file order, fixtures, license file); abort/timeout mapping in `history-and-boundaries.md`; two common mistakes; sources.
3. distributed-fault-testing: description; Node section in `fault-model-and-activation.md` (Toxiproxy limits, node client gaps, testcontainers, child_process, no clock route, MSW); one route line in SKILL.md; common mistakes; sources.
