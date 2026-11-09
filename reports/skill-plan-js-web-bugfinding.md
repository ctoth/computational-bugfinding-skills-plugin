# Skill Plan: JS/TS (Node.js and React) Bugfinding

**Date:** 2026-11-09
**Request (Q):** "A lot of this here is low-level. we need also how to do this same thing in like React 'n Node 'n shit huh? can you build this out to the same quality?"
**Research source:** `reports/skill-research-js-web-bugfinding.md` (domain research F1-F16, route table, failure spaces).
**Literature (paper-reader, page images; notes under `C:/Users/Q/code/papers/`), all 10 read:** Endo_2020 NodeRacer, Davis_2017 Node.fz, Raychev_2013 EventRacer, Vilk_2018 BLeak, Mesbah_2012 Crawljax, Staicu_2018 ReDoS, Arteca_2022 Nessie, Wang_2017 Node concurrency study, Adamsen_2017 EventRaceCommander, Selakovic_2018 LambdaTester. The domain report's other leads (e.g. Madsen 2017 promises, Alimadadi 2018 broken promises, Chang 2019 Node atomicity, Petrov 2012, Artzi 2011, Mesbah 2009, Roest 2010) remain unread; each Phase 3 researcher reads the ones its skill needs through paper-reader.
**Base plan:** `reports/skill-plan-computational-bugfinding.md` (25 method skills, method-first layout, runtime specifics in references).

## State

Complete; awaiting Q's "make it so". No skill, manifest or README changes. Remaining "PENDING" words in the table below refer to the batch-2 paper notes, which are now folded in under "Literature folded in (batch 2)".

## Problem being solved

1. **Selection.** An agent picks a skill from its frontmatter description. Current descriptions name only native/Go/Rust/.NET/JVM tools (e.g. `schedule-exploration`: "with Loom, Shuttle, Coyote or existing target seams"; `coverage-guided-fuzzing` has no JS route at all). A Node or React request therefore either selects nothing or selects a skill whose runtime lanes say no controller exists. This is the "low-level" problem.
2. **Routes.** The research found real, maintained JS routes for most methods (route table, research report Summary) that the skills do not carry: Jazzer.js, fast-check scheduler, memlab, c8/`NODE_V8_COVERAGE`, Node test-runner randomization and extraneous-async reporting, React hydration/StrictMode/`onRecoverableError` contracts, RTL/Playwright drivers, MSW, Toxiproxy Node client, elle-cli for Node histories, ReDoS detectors.
3. **Methods without maintained tools.** The literature supplies methods whose tools are stale (Node.fz on Node 0.12.7; NodeRacer on Node 10; EventRacer on 2012 WebKit; BLeak Chrome-only, untested on current Chrome). The method is still usable as guidance where a current seam exists.

## Design

Keep the method-first layout of the base plan: a runtime belongs in references of the method skill whose search dimension and oracle it uses. Add a new skill only where the literature shows a search dimension or oracle no existing skill carries. The domain research found every web failure space maps to an existing boundary; the one open candidate is UI state exploration (below).

Each changed skill gets: (a) its description updated so Node/React requests select it, naming the JS route; (b) one JS/web reference file (or a section in an existing runtime reference) at the same evidence standard as existing references: pinned source, short quotes, license, runtime floor, what the tool does not control; (c) `sources.yaml` entries; (d) `common-mistakes.md` entries where the research or papers show a JS-specific mistake.

## Changes per skill

| Skill | Change | Evidence |
|---|---|---|
| `coverage-guided-fuzzing` | New `references/node-jazzerjs.md`: in-process libFuzzer-based Node fuzzing; Babel instrumentation; ESM uninstrumented below Node 20.6; async targets awaited; bug detectors (command injection, path traversal, prototype pollution, SSRF) and `reportFinding`; Jest `it.fuzz`; regression mode; 2025 maintenance gap and floor mismatch stated. Browser: state no route. Description names Node. | F1 |
| `corpus-evolution` | Node section: Jazzer.js corpus directories and regression mode; c8/`NODE_V8_COVERAGE` for coverage-diverse selection, distinct from the Babel counters that guide Jazzer.js. | F1, F7 |
| `schedule-exploration` | New `references/javascript-event-loop.md`. fast-check `scheduler`/`schedulerFor`/`scheduledModelRun` (wrapped promises only; `fetch`/external emitters uncontrolled; randomized, not exhaustive); timers via fake timers; MSW response ordering; React `act` batching limit; Node mock timers are virtual time, not schedule search. Method guidance from the literature: NodeRacer-style record of callback causality then postponement of ready callbacks, bounded one-postponement diagnosis to localize the culprit callback (Endo 2020 pp.3-6); Node.fz shows races also land in databases and the file system, not just memory (Davis 2017 pp.5-6), and that perturbations must stay inside documented ordering guarantees (p.10). Both tools stated as unmaintained. Description names Node/browser promises. | F2, F8, F9, F11; NodeRacer, Node.fz notes |
| `race-detection-campaigns` | Short boundary note: JS event races are schedule problems, routed to `schedule-exploration`; memory-race detection applies only to `SharedArrayBuffer` across workers, no detector found. Verify the single-thread premise from a primary source before writing. | F16 |
| `stateful-property-testing` | Browser/React section in `runtime-recipes.md` or new `references/ui-sequences.md`: fast-check commands driving RTL (component) or Playwright (page); auto-wait/retrying assertions can mask a transient wrong state; `act`; accessibility-tree observation; browser state reset between runs. Async Node library APIs with callbacks: **PENDING** Nessie. **PENDING** Crawljax for state abstraction (see open question 1). | F10, F11 |
| `semantic-differential-testing` | Worked example: SSR vs first client render against React's documented identity contract; observe via `onRecoverableError` (not only dev warnings); control time/locale/`matchMedia`/`typeof window` sources. Library-version differential: **PENDING** LambdaTester. | F9 |
| `configuration-differential-testing` | JS factors: Node LTS lines, ESM vs CJS (changes Jazzer.js instrumentation), Chromium/Firefox/WebKit via Playwright, React dev vs prod build. | F1, F9, F10 |
| `correctness-oracles` | JS observation channels: `--unhandled-rejections` mode decides whether a rejection is a crash signal; test-runner extraneous-async failures; `onRecoverableError`; StrictMode as a development-only purity/cleanup oracle that says nothing about production builds; `useSyncExternalStore` snapshot-stability contract. | F8, F9 |
| `harness-sensitivity` | c8 reachability check; `--test-randomize`/`--test-random-seed` order-dependence probe (Node >= 26.1); extraneous async activity as state leakage. StrykerJS route unchanged. | F7, F8, F15 |
| `resource-complexity-testing` | New `references/javascript-memory-and-redos.md`. Leak oracle from BLeak: heap growth across repeated returns to the same UI state, growth required between every consecutive snapshot, 8 round trips default, false positives from capped/timeout structures removed by more round trips (Vilk 2018 pp.2, 5-6, 11); route capture mechanics to memlab and its own plugin; Node heap-snapshot caveats (blocks event loop, ~2x heap, V8-version-specific). ReDoS: detectors (recheck, redos-detector) as candidate producers, confirmation by matched size families at the real call site; single event loop means one slow request stalls all. **PENDING** Staicu 2018 for reachability-from-HTTP and slowdown thresholds. | F6, F8, F14; BLeak notes |
| `linearizability-checking`, `transactional-history-testing` | Note on recording invoke/complete histories from an event-loop client, including promises that never settle, then checking with Porcupine (Go model) or elle-cli (Java 21+). | F13 |
| `distributed-fault-testing` | Toxiproxy + Node client: network faults only, no process/clock faults; MSW mocks are not deployment faults. | F11, F12 |
| `symbolic-concolic-execution` | Decided: gated ExpoSE route. Jalangi2 + Z3, Node programs and limited Electron browser mode, tested only on Node v21.7.2, `replay` option, last commit 2024-07; the applicability check comes first, and if it fails the agent says JS has no supported backend for the target and does not port anything. Same treatment the base pack gives research-grade tools. | F4 |
| `failure-reduction`, `evidence-based-triage` | Playwright traces as replay artifacts; fast-check seed/path/replayPath already covered. Jazzer.js minimization: verify before writing. | F10 |
| `bugfinding-campaign` | Baseline-inventory example lists JS lanes (Jest/Vitest/node:test, fast-check, Stryker, Playwright, Jazzer.js) so an agent inventories a JS project correctly. | route table |
| No change | `semantic-program-generation`, `native-memory-instrumentation` (addons only, no recipe verified), `deterministic-simulation`, `crash-consistency-testing`, `bounded-model-checking`, `numerical-oracles`, `liveness-testing`, `metamorphic-testing` (method-neutral). Where a JS user would look, state "no verified JS route" in one line rather than silence. | F16 |

Also update the base plan's runtime table row for JS/TS and the README skill list wording. (README is part of the uncommitted publication work in `agent-notes/computational-bugfinding-marketplace.md`; coordinate, do not overwrite.)

## Literature folded in (batch 2)

- **Browser event races (`schedule-exploration` JS reference).**
  - EventRacer (Raychev 2013): browser happens-before model (listener lists and DOM ids as memory locations, race coverage), but it needs instrumented 2012 WebKit, has no automatic oracle and predates promises and frameworks (notes pp.3, 10-13, 15).
  - EventRaceCommander (Adamsen 2017) shows the controllable seam in an unmodified browser: instrument the page's HTML and JS through a proxy so a controller intercepts each event's begin and dispatches, postpones or discards it. The original happens-before order (script load after script execution) and the order of user events must be preserved (notes pp.2-5). The paper uses this for repair. For bugfinding the same seam steers *toward* the developer assumptions it names: user acts before scripts load; an Ajax response arrives after the next user action (p.3). Harm is a user decision, not automatic (p.4).
  - Current route to verify in Phase 3: Playwright request routing to hold or reorder network responses and to act before load. Inference, not yet read from Playwright docs.
- **Node schedule bounds (`schedule-exploration`).** Wang 2017 (57 real Node bugs):
  - 65% are atomicity violations, 30% order violations, 5% starvation.
  - 93% need an ordering of at most 4 events, 95% one process, 86% one racing resource (notes p.2, 4-9).
  - Racing resources include databases and files (read-modify-write across two async calls, e.g. findOne then save), and starvation comes from nextTick/setImmediate priority.
  - So start small-bound searches at a few events on one resource, and model DB/file resources, not only memory. Its dataset (project#issue URLs, p.2, 11) and the Staicu exploit benchmark are known-defect sources for `harness-sensitivity`.
- **ReDoS confirmation (`resource-complexity-testing`).** Staicu 2018:
  - Vulnerable means linearly growing input gives super-linear matching time (p.364).
  - Reachability is confirmed by data flow from an HTTP header or body to the regex (p.365).
  - Oracle: equal-size crafted and random inputs at k=5 sizes, 3 warm-up and 5 measured requests each. Exploitable only if the confidence intervals separate at every size and the crafted-minus-random difference strictly increases (pp.365-366). Sizes are chosen so no request blocks longer than about 2 s (p.365).
  - One request blocks the whole Node event loop (p.361).
  - Benchmark of 25 vulnerabilities with exploits: github.com/sola-da/ReDoS-vulnerabilities (p.362).
- **Async callback APIs (`stateful-property-testing` Node section).** Nessie (Arteca 2022):
  - It discovers callback positions and sync vs async invocation by probing. A callback logged after the test body ends is async; one logged before the call returns is sync (p.1496).
  - Tests are trees, so a call can be nested inside a previous call's callback and use its parameters (Defs 2-3, p.1497). This is how values that exist only inside callbacks (file handles) are reached.
  - Extension points are only callbacks that actually ran without exceptions (p.1498).
  - Its oracle is differential across consecutive commits (p.1499).
  - fast-check commands do not nest calls inside callbacks. The reference must say so and give the nesting pattern.
- **Callback-aware differential (`semantic-differential-testing`).** LambdaTester (Selakovic 2018):
  - It compares a polyfill against the native implementation (pp.12-14).
  - Its execution summary includes callback-argument state at every invocation and callback invocation counts, beyond return values and receiver state (Def 4.1, p.13).
  - Engine-specific objects such as promises are recorded only by constructor name (p.13).
  - Callbacks that write locations the method reads after the callback (Cb-Writes) reach behavior that empty or random-return callbacks do not (pp.10-11).
  - Applies to polyfill vs native, two library versions, or SSR vs client utilities.

Tool availability for Nessie, LambdaTester and EventRaceCommander was not established from the notes read; the Phase 3 researchers check it. These methods go in as guidance regardless.

## New skill: `ui-state-exploration` (decided after Crawljax)

**Decision:** add one skill, the 26th. Crawljax (Mesbah, van Deursen, Lenselink 2012, notes pp.5-16, 24-27) is a model-free search over a discovered state graph, which `stateful-property-testing` (model-based sequences with preconditions) does not carry:
- state = runtime DOM with a configurable equivalence: edit-distance threshold or a comparator chain that strips noise such as timestamps and banners (pp.8-9, 24-25); new states deduplicated against all visited states (p.9);
- candidate events from the DOM diff after each transition, because `addEventListener` handlers are invisible to DOM inspection; a candidate is a transition only if firing it changes the DOM under the chosen comparison (pp.5, 7-9);
- labeled state-flow multigraph with event type plus element locator on each edge (p.6);
- reset by reload and replay of the recorded event path; cookies and web storage break reset (pp.10-11, 26);
- DOM settling: a fixed wait is slow or unsafe; an app-provided completion flag is more reliable (p.27);
- bounds: depth, state count, time, exclusions; depth 1 to 2 grew states about 7-8x (pp.18, 20, 27);
- no built-in oracle (p.19): checks attach per new state.

For React today: Playwright as the driver (F10), the accessibility tree or a filtered DOM as state, a settle signal tied to the app (not auto-wait alone), per-state oracles from `correctness-oracles` (`onRecoverableError`, console errors, invariants), and discovered cycles handed to `resource-complexity-testing` as BLeak-style leak loops (BLeak notes p.4; conceptual link in both notes). No maintained JS crawler exists (F10), so the skill guides a small target-specific crawl loop over the existing driver. It must not build a general crawler framework.

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Excludes:** model-based sequence generation (stateful-property-testing), driver mechanics (Playwright's own skills), visual regression.
- **Research gaps for its Phase 3 researcher:** Mesbah & van Deursen 2009 (invariant-based Ajax testing, the oracle companion) and Roest et al. 2010 (comparator pipeline) are new leads, not read; read them through paper-reader before drafting. Also confirm React-specific settle signals from primary docs.

`stateful-property-testing` still gets the browser/React section for model-based UI sequences (fast-check commands with RTL or Playwright).

## Build pipeline (same as the 25)

1. Per changed skill: one primary-source researcher writes `reports/research-js-<skill>.md` (pinned sources, quotes, licenses, runtime floors), reusing the domain report and paper notes rather than repeating them.
2. Drafter edits that skill's description, reference, sources.yaml and common mistakes; writes `reports/draft-js-<skill>.md`. Batches of two or three; commits sequential.
3. Improvement pass on citations.
4. Update this plan, the task note and the base plan runtime row; commit with the work.

Struck 2026-11-09: a collection audit and behavioral evaluations with Node, React and control fixtures were listed here. Q never asked for either ("NEVER DID I ASK FOR IT", "DID NOT ASK FOR EVALS"); "same quality" did not authorize extra pipeline stages.

## Excluded

- New skills for ReDoS, StrictMode/concurrent rendering, JS event-race detection, flaky tests (research report "Candidate new skills": each maps to an existing owner).
- Reviving or porting Node.fz, NodeRacer, EventRacer or BLeak: no shown target problem; the methods go in as guidance.
- Duplicating fast-check's own `javascript-testing-expert` authoring advice, memlab's plugin skills, or Playwright's driver skills; route to them.
- Prototype pollution as a security skill: Jazzer.js detector mentioned in the fuzzing reference only.

## Decisions taken (formerly open questions)

1. UI state exploration: dedicated skill `ui-state-exploration` (Crawljax evidence above). Manifests and README skill count change from 25 to 26.
2. ExpoSE: gated route in `symbolic-concolic-execution`.

No open design questions remain that the evidence does not settle. Skill edits wait for Q's "make it so".
