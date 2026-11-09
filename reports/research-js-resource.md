# Research: JS/TS (Node, React) routes for `resource-complexity-testing`

Phase 3 per-skill research, group C. Branch `js-web-bugfinding`. Date 2026-11-09. Status: complete. No tools installed or run against a target; only read-only fetches of docs and source.

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md` lines 38 (resource-complexity-testing row), 59-64 (ReDoS bullet), 105-106 (fixtures).
- `reports/skill-research-js-web-bugfinding.md` F6 (lines 103-118), F8 (128-147), F14 (219-231).
- `plugins/bugfinding/skills/resource-complexity-testing/SKILL.md` and all of `references/` (`search-and-confirmation.md`, `metrics-and-lifecycle.md`, `common-mistakes.md`, `runtime-recipes.md`, `sources.yaml`).
- `reports/research-resource-complexity-testing.md` (evidence standard: pinned refs observed with `git ls-remote`, raw files read, short exact fragments, synthesis labeled as such).
- Paper notes (paper-reader, page images): `C:/Users/Q/code/papers/Vilk_2018_BLeakAutomaticallyDebuggingMemoryLeaks/notes.md`, `C:/Users/Q/code/papers/Staicu_2018_FreezingWebStudyReDoS/notes.md`.

Existing-skill facts relevant below (from the files read):
- `SKILL.md:20` already requires promoting candidates to "repeated matched observations" and separating candidates from confirmed violations.
- `references/search-and-confirmation.md` "Confirm an actual violation" already requires raw samples, matched ordinary valid controls, variation/effect size, and says statistical significance is not an application threshold.
- `references/metrics-and-lifecycle.md` already requires preserving "the measured size/history family and ordinary controls" and says "a fitted curve is not an asymptotic proof".
- The phrase "a single slow run treated as a bug" quoted in F14 comes from `reports/skill-plan-computational-bugfinding.md:244` (Excludes), not from the skill files (grep over the skill directory: no match).

## Findings

### R1. memlab pin

`git ls-remote https://github.com/facebook/memlab` gives `HEAD` = `refs/heads/main` = `8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d`; `gh api repos/facebook/memlab` resolves to `meta/memlab`, default branch `main`, pushed 2026-11-09. Same commit as F6. All memlab citations below are raw files at `https://raw.githubusercontent.com/meta/memlab/8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d/<path>`.

### R2. memlab browser oracle is one action/back cycle and three snapshots, not BLeak's every-snapshot growth

Facts:
- `website/docs/how-memlab-works.md:10-26`: baseline snapshot `SBP` after `url`, target snapshot `STP` after `action`, final snapshot `SFP` after `back`. Lines 41-53: leak candidates are `(STP \ SBP) ∩ SFP`, objects "allocated during the target interaction" "but are still alive when they should have been released". Lines 55-57: built-in detectors refine this; "memlab also identifies the React Fiber tree and detects unmounted Fiber nodes".
- `plugins/memlab/skills/memlab-find-web-leaks/SKILL.md:13-17`: "takes two more snapshots"; "By default memlab reports detached DOM elements and unmounted React Fiber nodes, grouped into clusters by retainer trace." Lines 118-122: "The built-in detector only reports detached DOM and unmounted Fiber nodes"; `memlab find-leaks --trace-all-objects` treats every object `action` allocated as a leak, narrowed with `--trace-object-size-above <bytes>`.
- Scenario callbacks (`plugins/memlab/skills/memlab-find-web-leaks/references/scenario-api.md:7-19`): only `url` is required; `cookies`, `beforeInitialPageLoad`, `setup` (before the baseline snapshot), `action` (target snapshot after), `back` (final snapshot after), `isPageLoaded` (polled every 200 ms; default waits for `networkidle0` plus a fixed delay, lines 54-56), `repeat` ("Extra `action`/`back` cycles before the target snapshot"), `beforeLeakFilter`, `leakFilter` ("return `true` to report it"; "A `leakFilter` replaces that rule", lines 83-84), `retainerReferenceFilter`. Lines 139-140: `repeat` is "only to amplify a small leak".
- Validity rules (`memlab-find-web-leaks/SKILL.md:53-65`): no full reloads in `action`/`back` (memlab stops: "MemLab cannot analyze heap across page reloads"); "`back` must really undo `action`"; `page` is a Puppeteer `Page` (memlab 2.x uses Puppeteer 24); log in through `cookies` or `setup`, not `action`.
- React detector source: `packages/core/src/lib/leak-filters/rules/FilterUnmountedFiberNode.rule.ts:16-38`: "mark React FiberNodes without a React Fiber Root as memory leaks", gated by `config.detectFiberNodeLeak`, excluding nodes dominated by the deletions array.
- Readable traces need non-minified code (F6; `memlab-find-web-leaks/SKILL.md:107-108`).

Comparison with BLeak (Vilk 2018 notes): BLeak drives a loop of visual states, snapshots at the same state after each round trip, 8 round trips by default (p.5, p.8, p.10), and reports a heap path only if its outgoing-edge count rises strictly between every consecutive pair of snapshots (Fig. 4, p.6). It tracks paths, not object identity, so a replaced-larger array still counts (p.5). Its only false-positive class was structures that grow until a cap or timeout, removed by more round trips (p.11).

Inference for the drafter: memlab's default run is a single-cycle retention oracle ("allocated by `action`, alive after `back`"), filtered to detached DOM and unmounted Fiber nodes. That is a different oracle from BLeak's repeated-growth oracle. After one cycle, a bounded first-use cache or lazily loaded module looks the same as a leak once the filter is widened (`--trace-all-objects` or a size `leakFilter`). `repeat` adds cycles before `STP` but still produces three snapshots, so it does not test growth between every cycle. Repeated-growth confirmation stays this skill's work, using a snapshot series (R3). The default detached-DOM/unmounted-Fiber filter is a structural oracle on its own (a Fiber with no root, retained after unmount, is past its lifecycle end), so a default-filter report after a `back` that really undoes `action` is evidence of retention past a cleanup boundary; a growth claim needs R3.

### R3. memlab growth over a series: `unbound-object` is weaker than BLeak's rule; the MCP sequence tool labels "every step" growth

Facts:
- `packages/heap-analysis/src/plugins/ObjectUnboundGrowthAnalysis.ts:34-44`: command `unbound-object`, "a single object with growing retained size". Line 65: with a snapshot directory it requires `minSnapshots: 2`. It tracks objects by heap node id (lines 87-120); lines 112-116: only when `config.monotonicUnboundGrowthOnly` is set does it drop an object whose retained size falls below its maximum. Lines 185-195: an object is reported if it is present in the last snapshot, `min !== max`, and its last retained size is at least `config.unboundSizeThreshold`.
- `packages/core/src/lib/Config.ts:544-546`: defaults `monotonicUnboundGrowthOnly = false`, `unboundSizeThreshold = 10 * 1024`. GitHub code search for `monotonicUnboundGrowthOnly` in `meta/memlab` returns only Config.ts, ObjectUnboundGrowthAnalysis.ts and CollectionUnboundGrowthAnalysis.ts (no CLI option found that sets it; the search index may lag the pinned commit).
- Lines 145-149: `global.gc()` is called in the analyzer process before loading each snapshot; this frees analyzer memory, it does not collect the target's heap.
- MCP route (skill docs only, MCP source not read): `plugins/memlab/skills/memlab-analyze-heap-snapshot/SKILL.md:114-121`: `memlab_sequence_analysis` "separates 'grows at every step' (leak signal) from noisy growth"; "Growth across a short series can still be a bounded cache or work in flight. Before calling it a leak, check whether it plateaus or is released after idle and garbage collection." `references/investigation-paths.md:234-243`: it reports each class's count at every step, labels "↑ every step" vs "grew net (noisy)", and object ids match across captures only within one isolate (no reload or restart).
- Series capture recipe (`plugins/memlab/skills/memlab-capture-heap-snapshots/SKILL.md:86-98`): warm up, snapshot 0, repeat the interaction N times (e.g. 10) returning to the start state, snapshot, 3-5 times; optional idle-plus-GC "settle" snapshot ("Growth that disappears here was work in flight, not a leak").

Inference: default `unbound-object` reports any object whose retained size changed and ended at or above 10 KiB; it does not require monotone growth, let alone BLeak's strict growth at every step, and it follows node ids rather than paths, so replaced-larger containers are missed (BLeak p.5 names exactly that case). For a growth claim the drafter should require BLeak's rule (strict growth between every consecutive same-state snapshot, more cycles to rule out capped structures) and treat `unbound-object` output as candidates. `memlab_sequence_analysis` "↑ every step" is the closest existing implementation, at class-count granularity (doc-level fact; implementation unread).

### R4. memlab Node in-process heap assertions

Facts:
- `plugins/memlab/skills/memlab-memory-tests/SKILL.md:21-62`: `takeNodeMinimalHeap()` from `@memlab/core`, `tagObject(obj, tag)` + `heap.hasObjectWithTag(tag)`, `hasObjectWithClassName`, `getAnyObjectWithClassName`, `hasObjectWithPropertyName`; "Drop **every** reference the test holds"; snapshot plus parse takes "from under a second to many seconds"; `takeNodeFullHeap()` from `@memlab/heap-analysis` for retained sizes; `dumpNodeHeapSnapshot()` to save one.
- Source `packages/core/src/lib/NodeHeap.ts:59-62` (`tagObject` via `MemLabTaggedStore`; "does not modify the object instance", lines 21-24), `84-95` (`dumpNodeHeapSnapshot` calls `v8.writeHeapSnapshot(file)` into a temp dir), `152-161` (`takeNodeMinimalHeap` = dump, parse with `buildNodeIdIndex`, unlink). No explicit `global.gc()` call in these functions.
- CI browser route: `@memlab/api` `run({scenario, skipWarmup, consoleMode: 'CONTINUOUS_TEST', workDir})` returns `{leaks, runResult}`; `findLeaksBySnapshotFilePaths(baseline, target, final)` for snapshots from an existing Playwright/Puppeteer test (`memlab-memory-tests/SKILL.md:64-122`). `memlab measure --scenario <file>` "runs the scenario several times to show how much is noise" (lines 129-130).

Inference: the Node assertion is a single-point reachability oracle (is this tagged instance still reachable after release), the right shape for a lifecycle check at a cleanup boundary (`metrics-and-lifecycle.md` "Observe before reset"). It parses the snapshot inside the process under test, which perturbs that process's heap; the observer-perturbation point already in `metrics-and-lifecycle.md` applies.

### R5. memlab's own plugin: route to it, do not duplicate

`plugins/memlab/README.md:11-16`: four skills: `memlab-analyze-heap-snapshot`, `memlab-find-web-leaks`, `memlab-capture-heap-snapshots`, `memlab-memory-tests`; plus the memlab MCP server ("more than 150 tools"). Install `claude plugin marketplace add meta/memlab` / `claude plugin install memlab@memlab` (lines 20-23); Codex equivalents lines 41-44. Requirements: Node.js 18+, MCP server started with `NODE_OPTIONS=--max-old-space-size=8192` (lines 62-66); `memlab_eval` runs agent-written JS with server privileges, keep on manual approval (lines 67-70). License MIT (`plugins/memlab/.claude-plugin/plugin.json`). Heap snapshots contain every string in memory; `memlab anonymize` before sharing (`memlab-capture-heap-snapshots/SKILL.md:104-111`).

Decision: our reference names the four skills by purpose and owns only what they lack: choosing the cycle that returns to the same state (BLeak loop), the every-step growth rule and cycle count, matched controls, lifecycle phase, and taking discovered cycles from `stateful-property-testing` crawls.

### R6. Node core measurement facts (tag `v26.13.0`)

Pin: `git ls-remote --tags https://github.com/nodejs/node` shows `v26.13.0` = `daaa22aeddb87085542376ea1f4854dcea080baf`, the highest v26 tag; no v27 tag listed. Raw files at `https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/<file>`.

- `v8.writeHeapSnapshot` (`v8.md:577-621`): schema "specific to the V8 engine, and may change from one version of V8 to the next"; "specific to a single V8 isolate" (main-thread snapshot excludes workers); needs "memory about twice the size of the heap", "risk of OOM killers"; "a synchronous operation which blocks the event loop for a duration depending on the heap size". The page does not say whether a GC runs before the snapshot (open).
- `v8.queryObjects(ctor[, options])` (`v8.md:372-405`; added v22.0.0/v20.13.0, no longer experimental as of v25.4.0/v24.13.1): searches "for objects that have the matching constructor on its prototype chain in the heap after a full garbage collection, which can be useful for memory leak regression tests"; returns a count by default (or `format: 'summary'` strings), never references; avoid on constructors you don't control. Not in F8. A built-in, snapshot-free count oracle for a Node class-count growth series.
- `--heapsnapshot-near-heap-limit=max_count` (`cli.md:1841-1880`; added v15.1.0/v14.18.0; no longer experimental as of v25.4.0, v24.13.1, v22.22.1): "garbage collection may be triggered and bring the heap usage down", so several snapshots may be written; they "can be compared to determine what objects are being allocated during the time consecutive snapshots are taken"; exact count not guaranteed. `--heapsnapshot-signal=signal` at `cli.md:1895`.
- `process.memoryUsage()` (`process.md:2770-2846`): `heapTotal`/`heapUsed` are V8; `external` is C++ objects bound to JS; `arrayBuffers` (included in `external`) covers `ArrayBuffer`/`SharedArrayBuffer`/`Buffer`; `rss` is whole-process including workers; the call "iterates over each page" and "might be slow"; "On Linux ... sustained `rss` growth despite stable `heapTotal` due to fragmentation caused by the glibc `malloc` implementation".
- `--expose-gc` (`cli.md:4702-4721`): listed under "Useful V8 options" with no description; that section says V8 options "have _no stability guarantee_" and are not covered by Node's stability guarantees. Node docs at this tag do not document `global.gc()` semantics (grep of `globals.md` for "gc": no match).
- `perf_hooks.monitorEventLoopDelay([options])` (`perf_hooks.md:1924-1975`): returns an `ELDHistogram` of event-loop delay in nanoseconds; default interval sampling with `resolution` 10 ms; `samplePerIteration` (added v26.5.0) samples once per loop iteration; "The two sampling modes produce significantly different results and should not be compared directly"; with interval sampling "every sample includes the `resolution`"; delays above `highest` are counted in `histogram.exceeds`; `lowest`/`highest`/`figures` added v26.11.0.
- `perf_hooks.eventLoopUtilization([u1[, u2]])` (`perf_hooks.md:1851-1923`; module-level alias added v25.2.0/v24.12.0; `performance.eventLoopUtilization` added v14.10.0/v12.19.0, lines 117-141): cumulative `idle`/`active` ms and `utilization`; delta form from a previous result; "ELU is similar to CPU utilization, except that it only measures event loop statistics and not CPU usage"; a `spawnSync('sleep', ['5'])` example reports utilization `1` while the CPU is idle, because the loop is blocked.
- libuv threadpool (`cli.md:4690-4700`): threadpool-backed APIs (listed above that line, including all non-sync `zlib` APIs) share a fixed pool, default size 4, so one slow task degrades "seemingly unrelated" APIs; `UV_THREADPOOL_SIZE` must be set before startup.

Inference:
- A ReDoS (or any synchronous CPU) stall in a request handler is visible to other requests as event-loop delay. `monitorEventLoopDelay` in the server process, or a concurrent probe request's latency (the Staicu p.368 victim/attacker design), measures the "stalls everyone" consequence; ELU shows the loop was busy. These measure the shared-availability contract, separate from per-request latency. Keep the sampling mode fixed across candidate and control (doc rule above).
- Forcing GC before a heap measurement needs `--expose-gc`, a V8 flag outside Node's stability guarantee; `v8.queryObjects` gives a documented after-full-GC count without it (Node >= 22.0/20.13). Record which one was used.
- `process.memoryUsage().rss` growth with flat `heapUsed` is not a JS-heap leak claim (glibc fragmentation note); `external`/`arrayBuffers` are where Buffer retention shows. This maps onto the existing "preserve metric identity" rule in `metrics-and-lifecycle.md`.

### R7. recheck: released v4.6.2 outputs a pumped attack string; runtime verification on Node exists only in v5.0.0-beta.1 and main

Pins (`git ls-remote`): main `HEAD` = `f008739a7470038fa41aa841a648237243cabfb4` (same as F14); tag `v4.6.2` = `419ffcb586bff18779cfbbef279832da5538286d` (latest stable release, 2026-10-26); tag `v5.0.0-beta.1` = `11d18a47b6e86849b280ed9292f8fa9063ea58c1` (prerelease, 2026-11-06, `gh api .../releases`). Main `packages/recheck/package.json`: `"license": "MIT"`, `"node": ">=22"`.

Released v4.6.2 (`website/docs/usage/diagnostics.md` at tag `v4.6.2`):
- Lines 18-34: three statuses; complexities `safe`/`constant`/`linear`, `polynomial` with `degree`, `exponential`.
- Lines 43-52: `vulnerable` diagnostics have an `attack` field: "a string with a repetition structure. It consists of `pumps`, `suffix`, and the `base` repetition count. Each `pump` consists of `prefix`, `repeating` substrings, and the individual repetition count `n`. The actual string forms `prefix + repeating.repeat(base + n) + ... + suffix`." Line 52: "computed in theoretical, because of the real matching implementation's optimization, it may not invoke the matching time explosion."
- Lines 55-60: `hotspot`. The `usage/` directory at v4.6.2 has no `runtime-attack-verification` page (contents API: `as-eslint-plugin.mdx`, `as-javascript-library.mdx`, `as-scala-library.mdx`, `diagnostics.md`, `parameters.md`; raw fetch of that page at v4.6.2 returns 404).

Main / v5.0.0-beta.1 (`website/docs/usage/diagnostics.mdx` at main unless noted):
- Lines 8-12: `Diagnostics` "is not a final verdict"; "Whether a finding matters depends on how the regular expression is used, e.g. how long an input can reach it and which engine runs it."
- Lines 31-38: `safe` from the fuzz checker is "weaker evidence"; `unknown` kinds include `runtime-attacks-refuted`.
- Lines 62-88: pump fields renamed to `prefix`, `pump`, `bias`: "`prefix + pump.repeat(base + bias) + ... + suffix`"; `attack.string`, and `attack.pattern` (JavaScript `'a'.repeat(31) + '\x00'` for `/^(a|a)*$/`).
- Lines 94-103: `runtimeAttack` records `runtime` (e.g. `node v26.13.0`), `timeout`, `result.kind` (`finish`, `timeout`, `engine-limit`, `engine-error`), `isConfirmed`.
- `website/docs/usage/runtime-attack-verification.mdx` (exists at main and v5.0.0-beta.1): lines 13-19 model "a naive backtracking engine"; line 23 and 57-61 runs only when `runtimeAttackTimeout` is positive, "off by default"; lines 83-84 not in the browser or `worker`/`pure` backends; lines 102-104 `engine-error` refutes; lines 110-111 runtime from `PATH`, overridable by env var; lines 125-135 `recheck generate-runtime-attack-script` writes a standalone script with no timeout.
- `schema/parameters.schema.yaml:372-386` (main): `runtimeAttackTimeout` default `-1000`, "skipped if this value is not positive", `x-since: "5.0.0"`. Line 63: `attackTimeout` (default 1000 ms); line 350: `randomSeed` (default 0); line 422: `timeout` exceeded gives `unknown`.
- `website/docs/usage/dialects/javascript.mdx` (main): line 13 "follows the syntax and the semantics of ECMAScript 2026 `RegExp`, as V8 implements it"; lines 55-64 supported flags `d g i m s u v y` (no `l`); lines 68-69 with `y` only `lastIndex` 0 is modeled; lines 73-77 runtime attack command `node -`, `RegExp.prototype.exec`, engine errors `RangeError`, env var `RECHECK_NODE`.
- JS API (`website/docs/usage/as-javascript-library.mdx:38-61`, main): `check(source, flags, params)` (async; external CLI backend when possible) and `checkSync`; backend chosen with `RECHECK_BACKEND` (lines 150-152).

Inference: recheck is the strongest ReDoS producer for this skill because its output is a size family, not a single string: varying `base` with the pump structure fixed yields Staicu's "linearly increasing size" family directly. The field names differ between v4.6.2 (`repeating`, `n`) and v5 beta/main (`pump`, `bias`), so the reference must name the version it describes. The runtime attack (v5 only) is one timed run of one size with a timeout: a candidate filter on the real engine, not this skill's confirmation (no controls, no size family, no call site).

### R8. redos-detector: an ambiguity score, no attack string

Pin: `git ls-remote https://github.com/tjenkinson/redos-detector HEAD` = `db112c6a74361db91f9591df8fa85d4026e9cbe5` (same as F14). README (raw at that commit):
- Lines 9-13: computes paths through the pattern; the score is the highest number of other paths matching a prefix of a candidate path; "If the score is `1` this means no backtracks can occur".
- Line 34: the score "is just the highest for a given prefix of the input string. This is because we don't know the maximum length the input string could be".
- Line 15: ECMA-262 engines only.
- Lines 52-113: result `{safe, error: null|'hitMaxScore'|'hitMaxSteps'|'timedOut', trails, patternDowngraded, pattern, score}`; `trails` are pairs of overlapping path sides with node source spans, not input strings.
- Lines 119-126: `maxScore` default 200 ("considered unsafe" above it), `maxSteps` 20000, `timeout` Infinity, `downgradePattern` true. Lines 144-148: CLI exit non-zero if unsafe; `--json` always exits 0, check `safe`. Line 158: `isSafe(regexp)` supports only the `i` and `u` flags.

Inference: redos-detector flags ambiguity but gives no attack string and no growth estimate; `maxScore` 200 is the tool's threshold, not a product contract. `safe: false` is a candidate; the agent still builds the size family by hand from `trails`.

### R9. eslint-plugin-regexp: two static rules

Pin: `git ls-remote https://github.com/ota-meshi/eslint-plugin-regexp HEAD` = `0a79e7c0a91af4412b56f7b4110386e3e63a7088`; `package.json` version 3.3.3, MIT.
- `docs/rules/no-super-linear-backtracking.md`: "disallow exponential and polynomial backtracking"; enabled in `flat/recommended` and `recommended`; auto-fixable; "only implements a very simplistic detection method and can only detect very simple cases"; option `report: "certain"` (default; only when it "can prove that there exists a rejecting suffix") or `"potential"`. It decomposes an attack into prefix, repeated non-empty string, rejecting suffix.
- `docs/rules/no-super-linear-move.md`: "disallow quantifiers that cause quadratic moves" (an unanchored regex moved across the input; `/a+b/` is O(n^2) on n `a`s); its header lists no preset config; reports an attack-string class (e.g. "any attack string `/[\n\r\u2028\u2029]+/`"); "attackers need strings with lengths >1000 character to exploit the quadratic runtime"; options `report`, `ignoreSticky` (prose says default `true`; the sample options block shows `false`), `ignorePartial` (default `true`: regex fragments are not checked).

Inference: the linter is a cheap whole-codebase candidate sweep; `no-super-linear-move` covers the quadratic "move" class on unanchored patterns, which Staicu's `[^=]+=` example illustrates (notes p.364). Both are candidate producers; the defaults `ignorePartial: true` and `report: "certain"` hide fragment-built and potential cases.

### R10. V8/Node linear-time regex engine: present, experimental, off by default in Node v26.13.0

Facts (raw at `https://raw.githubusercontent.com/nodejs/node/v26.13.0/deps/v8/<path>`):
- `include/v8-version.h`: V8 14.6.202.34.
- `include/v8-regexp.h:22-37`: "The kLinear value ('l') is experimental and can only be used with --enable-experimental-regexp-engine. RegExps with kLinear flag are guaranteed to be executed in asymptotic linear time wrt. the length of the subject string."
- `src/flags/flag-definitions.h:3355-3379`: `enable_experimental_regexp_engine` ("recognize regexps with 'l' flag, run them on experimental engine"), `default_to_experimental_regexp_engine` (default false, "run regexps with the experimental engine where possible"), `enable_experimental_regexp_engine_on_excessive_backtracks` ("fall back to a breadth-first regexp engine on excessive backtracking"), `regexp_backtracks_before_fallback` default 50000. Lines 245-247: `DEFINE_EXPERIMENTAL_FEATURE` defines a bool defaulting to `false` that implies `experimental`.
- Same file lines 3296-3305: `regexp_tier_up` true ("enable regexp interpreter and tier up to the compiler after the number of executions set by the tier up ticks flag"), `regexp_tier_up_ticks` 1; `regexp_results_cache` true.
- `src/regexp/regexp.h:218-223`: `RegExpResultsCache` "is used during global calls to RegExp.prototype.exec and @@split", keyed by subject string and pattern.
- Node `doc/api/cli.md` at this tag: grep for "regexp" finds no documented option; these are V8 options under the "no stability guarantee" section (R6).
- Secondary only (web search; not used for current status): V8 blog post on the non-backtracking engine (https://v8.dev/blog/non-backtracking-regexp); TC39 proposal-linear-matching (https://tc39.es/proposal-linear-matching/), reported at Stage 0.

Inference:
- On stock Node v26.13.0 every regex runs on the backtracking engine, and `/.../l` is rejected unless the process starts with `--enable-experimental-regexp-engine`. `--default-to-experimental-regexp-engine` and `--enable-experimental-regexp-engine-on-excessive-backtracks` change whether a given regex is super-linear in that process. Vulnerability is a property of (pattern, flags, V8 version, process V8 flags), so a confirmation must record `node --version`, `process.versions.v8`, and `process.execArgv`/`NODE_OPTIONS`, and confirm on the deployment's configuration.
- Tier-up: the first execution of a regex is interpreted and later ones compiled (ticks = 1), so the first timed call differs from later ones; Staicu's warm-up requests (3 per input, notes p.366) cover this. The results cache can serve repeated global `exec`/`split` on the same subject and pattern, so repeating an identical string through those paths may measure the cache (inference from the source comment; whether failing matches are cached was not read).

### R11. Staicu 2018 confirmation discipline mapped onto the skill

| Staicu element (notes page) | Existing skill text | What the JS reference adds |
|---|---|---|
| Vulnerable = linearly increasing input gives super-linear matching time (p.364) | `metrics-and-lifecycle.md`: preserve "the measured size/history family"; "a fitted curve is not an asymptotic proof"; SKILL.md:28 keeps size and structure separate | The family is recheck's `base` count with the pump structure fixed; sizes chosen from a local run so each call stays under a fixed wall bound (Staicu targeted ~100 ms to 2 s, p.366, p.369) |
| Crafted vs random input of equal size (p.365) | `search-and-confirmation.md`: "matched ordinary valid controls"; equal-size collision family | Same rule. The control must be valid for the call site (e.g. a realistic header value of the same length) so the request reaches the regex |
| k = 5 sizes (p.366) | No numeric rule (the pack avoids fixed counts except benchstat's floor) | Report 5 as the paper's choice, not a rule |
| n_w = 3 warm-ups, n_m = 5 measured per input (p.366) | Preserve cold/warm mode (`search-and-confirmation.md`); benchstat's "at least 10 times" floor (SKILL.md:20) | V8 regexp tier-up (R10) is the concrete Node reason for warm-ups; keep the pack's floor, cite Staicu's 3/5 as theirs |
| Confidence intervals separate at every size (p.365) | benchstat medians/CIs; "significant is not large" | Same. Separation at every size, not pooled |
| Crafted-minus-random difference strictly increases with size (p.366) | Not stated in the skill | New rule for growth claims: the candidate-minus-control difference must increase at every step of the family. Same shape as BLeak's every-snapshot rule (R2); state it once for ReDoS and leaks |
| Reachability: data flow from HTTP header/body to the regex (p.365) | SKILL.md:8 "on the real producer"; SKILL.md:12 public entrypoint | Confirm through the real request path with the framework's own limits; header-size limits (p.366, p.371) are contract facts to record; bodies may remain reachable (p.372) |
| One request blocks the whole event loop (p.361, p.363) | None JS-specific | Measure the shared consequence with a concurrent probe request or `monitorEventLoopDelay` (R6) |
| Exploit threshold "more than 5 seconds" (p.365); 2 s cap (p.365) | SKILL.md:12 "does not invent a latency threshold" | Keep the pack's rule: 5 s and 2 s are study parameters, not product budgets |
| A crafted header froze a live site for about a minute (p.365) | None | Run attack families only against a local or owned instance; bound sizes from a local run first |

### R12. Staicu exploit benchmark

`gh api repos/sola-da/ReDoS-vulnerabilities`: last push 2017-12-06, not archived, no repository license detected; HEAD `ccb8d7dc74fd9cff835b47548bdffb7c010bb60f`. Files: one `test-<module>.js` per vulnerable module (25), `run-all.js`, `utils.js`. Each test file carries an MIT header ("Copyright 2017 Software Lab, TU Darmstadt"); `test-fresh.js` builds one string (`genstr(60000, ' ') + "x"`) and times one call with `process.hrtime` (`utils.js` `measureTime`). README lists the issue and advisory per module.

Inference: these are single-size, single-run reproducers of known-vulnerable package versions; useful as known-defect inputs for `harness-sensitivity` (does our confirmation procedure flag them), not as a confirmation harness.

### R13. Literature: no further paper read

Not reading Davis 2018 or ReScue. The open questions were tool behavior (attack-string output, engine configuration) and confirmation shape; both were settled from primary tool and V8 sources plus Staicu's oracle (already read). Neither paper has been read, so nothing from them is stated here.

## Decisions for the drafter

### New `references/javascript-memory-and-redos.md` contents

1. **Leak oracle (BLeak).** Pick a cycle that returns to the same UI state (or the same Node lifecycle point). Snapshot at that state after each cycle. A growth claim requires growth between every consecutive snapshot; BLeak's default is 8 round trips; its only false-positive class (capped/timeout structures) goes away with more cycles (Vilk pp.2, 5-6, 10-11). Track by path or class count, not object id, because replaced-larger containers change identity (p.5).
2. **memlab routing (R2-R5).** The default `memlab run` is one action/back cycle, three snapshots, filtered to detached DOM and unmounted React Fiber nodes. Treat it as a single-cycle retention oracle: good evidence that something outlived its cleanup boundary, but not a growth test. `repeat` does not add snapshots. `unbound-object` is a candidate list: non-monotone, node-id based, 10 KiB floor. Growth series go through memlab's capture recipe and `memlab_sequence_analysis` "↑ every step", then this skill's every-step rule. Name memlab's four skills by purpose and send capture/analysis mechanics there.
3. **Node measurement (R6).** `v8.writeHeapSnapshot`: blocks the loop, about 2x heap, format tied to the V8 version, one isolate only. `v8.queryObjects`: after-full-GC count, Node >= 22.0/20.13. `--expose-gc` is an unstable V8 flag. `process.memoryUsage` field meanings, including the glibc RSS caveat. Snapshots must come from the same isolate with no restart.
4. **ReDoS producers (R7-R9).** Use recheck for candidates plus a pumped attack string, citing v4.6.2 field names (`repeating`, `n`) or v5 (`pump`, `bias`) explicitly. redos-detector gives an ambiguity score without an attack string. eslint-plugin-regexp's `no-super-linear-backtracking` and `no-super-linear-move` work as a static sweep. None of these is a finding.
5. **ReDoS confirmation (R11).** Build the size family by varying recheck's `base`. Use equal-size valid controls through the real request path, warm-ups, and separation at every size. The candidate-minus-control difference must strictly increase across the family. Measure the shared stall with a concurrent probe or `monitorEventLoopDelay`. Run only against local or owned instances.
6. **Engine configuration (R10).** Record `node --version`, `process.versions.v8`, `execArgv`/`NODE_OPTIONS`. The V8 linear engine and the `l` flag exist but are experimental and off by default at Node v26.13.0. They change the verdict for a given pattern.
7. **React and handoff.** Cycles discovered by `stateful-property-testing` crawls come here as leak loops. Readable traces need a non-minified build, but development builds hold extra memory (`memlab-capture-heap-snapshots/SKILL.md:23-25`). Name the build that was measured.

### Description wording

Current description already covers "CPU, allocation, memory-retention or handle-growth". Proposal: add JS triggers without widening scope, e.g. "... including Node.js event-loop stalls from super-linear regular expressions and browser or Node heap growth across repeated UI or request cycles." Keep it under the existing length style; the drafter decides final wording.

### Sources (for `sources.yaml`)

- memlab `8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d`: `website/docs/how-memlab-works.md`; `plugins/memlab/README.md`; `plugins/memlab/skills/memlab-find-web-leaks/SKILL.md` and `references/scenario-api.md`; `plugins/memlab/skills/memlab-memory-tests/SKILL.md`; `plugins/memlab/skills/memlab-capture-heap-snapshots/SKILL.md`; `plugins/memlab/skills/memlab-analyze-heap-snapshot/SKILL.md` and `references/investigation-paths.md`; `packages/heap-analysis/src/plugins/ObjectUnboundGrowthAnalysis.ts`; `packages/core/src/lib/Config.ts`; `packages/core/src/lib/NodeHeap.ts`; `packages/core/src/lib/leak-filters/rules/FilterUnmountedFiberNode.rule.ts`.
- Node `v26.13.0`: `doc/api/v8.md`, `doc/api/cli.md`, `doc/api/process.md`, `doc/api/perf_hooks.md`; `deps/v8/include/v8-regexp.h`, `deps/v8/include/v8-version.h`, `deps/v8/src/flags/flag-definitions.h`, `deps/v8/src/regexp/regexp.h`.
- recheck `v4.6.2` `website/docs/usage/diagnostics.md`; main `f008739a7470038fa41aa841a648237243cabfb4` `website/docs/usage/diagnostics.mdx`, `runtime-attack-verification.mdx`, `dialects/javascript.mdx`, `as-javascript-library.mdx`, `schema/parameters.schema.yaml`.
- redos-detector `db112c6a74361db91f9591df8fa85d4026e9cbe5` `README.md`.
- eslint-plugin-regexp `0a79e7c0a91af4412b56f7b4110386e3e63a7088` `docs/rules/no-super-linear-backtracking.md`, `docs/rules/no-super-linear-move.md`.
- Papers: Vilk & Berger, BLeak, PLDI 2018 (notes pp.2-6, 8, 10-11); Staicu & Pradel, Freezing the Web, USENIX Security 2018 (notes pp.361-372).
- Benchmark: `sola-da/ReDoS-vulnerabilities` `ccb8d7dc74fd9cff835b47548bdffb7c010bb60f` (for `harness-sensitivity`).

### Common mistakes (candidates for `common-mistakes.md` or the new reference)

- **Reading one memlab run as a growth leak.** Wrong: the default run reports something, so memory grows without bound. Right: default memlab shows retention after one cycle. Growth needs a same-state series with growth at every step (R2, R3; BLeak p.6).
- **Taking `unbound-object` output as confirmed growth.** It reports any changed retained size at or above 10 KiB, non-monotone by default (R3).
- **Treating a detector verdict as a ReDoS finding.** recheck "is not a final verdict", redos-detector's `maxScore` is a tool threshold, and the lint rules are "simplistic". Confirm with a size family at the real call site (R7-R9, R11).
- **One slow request as proof.** Staicu requires separation at all 5 sizes and a strictly increasing crafted-minus-random difference (p.366).
- **Ignoring the engine configuration.** The same pattern can be linear under V8's experimental engine flags; record versions and flags (R10).
- **Timing the first call.** V8 regexp tier-up makes first executions different; warm up (R10; Staicu p.366).
- **Comparing heap snapshots across restarts or Node versions.** Ids match only within one isolate, and the format is V8-version specific (R3, R6).
- **Calling RSS growth a JS leak.** Check `heapUsed`/`external`, given the glibc fragmentation note (R6).
- **Attacking a shared service.** Staicu froze a live site for about a minute with one header (p.365). Bound sizes locally first.

## Unverified / open

- Whether `v8.writeHeapSnapshot` (and so memlab's Node assertions) performs a full GC before writing: not stated in Node `v8.md`; V8 source not read.
- `memlab_sequence_analysis` implementation (MCP server source) not read; its "↑ every step" semantics are from skill docs only.
- Whether any memlab CLI flag sets `monotonicUnboundGrowthOnly` (code search only; CLI option sources not read).
- Whether memlab's browser driver forces GC before each snapshot: not read.
- Whether V8's `RegExpResultsCache` caches failing matches, and whether non-global `exec`/`test` is affected: only the header comment was read.
- recheck v4.6.2's own handling of the `l` flag, and whether v4.6.2 JS-dialect semantics match main's page: v4.6.2 dialect docs not read.
- recheck fuzz-checker internals and the "fuzzing with static analysis" claim: docs-level only (F14).
- `eslint-plugin-redos-detector` and recheck's `eslint-plugin-redos`: exist (README links, repo tree) but not read.
- Exact current status of the V8 linear engine beyond Node v26.13.0 source (blog and TC39 page from web search only, not fetched).
- No tool was run; every command shape is source-read, not executed.
