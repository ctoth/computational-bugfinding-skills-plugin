# Improvement pass: JS/TS additions to schedule-exploration and race-detection-campaigns (commit d423a35)

Skills: `plugins/bugfinding/skills/schedule-exploration/`, `plugins/bugfinding/skills/race-detection-campaigns/`. Accessed 2026-11-09. Every source below was fetched raw at the pinned URL this session (copies in the session scratchpad `src/`).

Status: complete. All edits are in the working tree, not committed.

## Findings

### F1 schedule-exploration references/javascript-event-loop.md:7, SKILL.md:22, common-mistakes.md (fast-check entries), sources.yaml (3 fast-check entries) — ERROR
- Said: "docs and source pinned at fast-check 4.10.2", and sources.yaml names the guide "(4.10.2)", but every fast-check URL is pinned at `cd9c1884e8a39fe945600fbcda1ec92d518feaa0`.
- Source: `gh api repos/dubzzz/fast-check/git/tags/5da531a1…` → tag `v4.10.2` points at `c77afa8277a67250d798c52e61343b8ed5fd268b` (commit message "v4.10.2"; `packages/fast-check/package.json` there: `"version": "4.10.2"`). `compare c77afa82...cd9c1884` → `diverged`, ahead 258, behind 4: cd9c1884 is an unreleased main commit ("Add `beforeAll` hook on our plugin system (#7544)", 2026-11-09), not 4.10.2.
- Identity check of each cited text at c77afa82 vs cd9c1884 (`diff` of the raw files):
  - `website/docs/advanced/race-conditions.md`: differs only at line 41-42 (type alias formatting) and line 253 (`fc.property` vs `fc.asyncProperty` in the act snippet). Every quoted sentence ("will resolve when the scheduler decides to resolve it", "not impacted by the scheduler", "only postponing the resolution of the function. The call to the function itself is started immediately", "deprecated since v4.2.0", "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters", "might make replay of failures harder", "Neither `check` nor `run` should rely on the completion of other scheduled tasks", "the mocked-server will always receive the calls in the same order as they were made", `s.schedule(Promise.resolve('Server received the call')).then(() => f(...args))`, "in the order they get executed by the scheduler", "are ordered", `jest.getTimerCount()`, `jest.advanceTimersToNextTimer()`, "when testing React applications, one cannot perform updates of states outside of `act`") is present verbatim at c77afa82 (lines 23, 82, 117, 33-35, 27, 28, 310, 213, 221, 29, 267, 284, 290, 259).
  - `packages/fast-check/src/arbitrary/scheduler.ts`: identical.
  - `packages/fast-check/src/arbitrary/_internals/SchedulerArbitrary.ts`: differs (released uses `Stream.nil()` and `mrng.nextInt`, main uses `nil` and `clonedMrng.nextInt`), but the quoted fragments `nextInt(0, scheduledTasks.length - 1)` (line 19) and "Not supported yet" (lines 35, 40) are present at c77afa82. Line numbers move: `buildNextTaskIndex` is lines 14-22, `canShrinkWithoutContext`/`shrink` lines 34-42.
  - "uniform" verified at c77afa82 `src/random/generator/Random.ts:64-66`: `nextInt(min, max)` returns `uniformInt(this.internalRng, min, max)`.
  - "printed `schedulerFor` block" verified at c77afa82 `SchedulerImplem.ts:423-425`: `toString()` emits ``'schedulerFor()`\n' +``.
- Fix: repinned every fast-check URL in both skill files to c77afa82; sources.yaml line ranges updated to the released file; removed the "these scheduler facts are from cd9c1884" note.

### F2 stateful-property-testing references/sources.yaml (outside this pass's edit scope) — WARNING, reported only
- The brief says stateful-property-testing cites the released tag 4.10.2 at c77afa82. The working tree does not: its fast-check entries are pinned at `5ec2e3aceae60eb510b8b967bcb153274f3abad7` and labelled "package manifest (4.10.2)". `compare c77afa82...5ec2e3ac` → `diverged`, ahead 253, behind 4: 5ec2e3ac is also a main commit ("Update dependency oxlint to ^1.92.0 (#7550)"), not the tag. Not edited (outside the two skill directories); the owner of that skill should check it.

### F3 race-detection-campaigns references/sources.yaml (Node worker_threads entry) — WARNING (minor)
- Said: sections_used "Introduction and stability (1-36); Class Worker (1474)".
- Source: worker_threads.md at v26.13.0: the quoted sentence ends on line 37: "Unlike `child_process` or `cluster`, `worker_threads` can share memory. They do so by transferring `ArrayBuffer` instances or sharing `SharedArrayBuffer`" (36) / "instances." (37). Line 1474 is correct ("The `Worker` class represents an independent JavaScript execution thread.", inside `## Class: \`Worker\`` at 1466).
- Fix: intro range 1-36 → 1-37.

### F4 schedule-exploration references/sources.yaml (async_hooks entry) — WARNING
- Said: "createHook callbacks not async (205-208)".
- Source: async_hooks.md at v26.13.0 lines 208-210: "the `init()`, `before()`, `after()`, and `destroy()` callbacks _must not_ be async functions that return promises."
- Fix: 205-208 → 208-210.

### F5 schedule-exploration references/javascript-event-loop.md:56 — WARNING (stronger than source)
- Said: "Node.fz had no replay; reproduction was a rate over reruns (pp.11-13)."
- Source: Davis_2017 paper-reader notes, "Replay / reproduction": "The paper describes **no record/replay or schedule-logging mechanism** for replaying a failing fuzzed schedule. Reproduction is statistical: rerun the test N times under node_FZ. *(p.11-13; not found anywhere in pp.1-16)*". The notes support absence from the paper, not a statement about the tool.
- Fix: "The paper describes no replay; reproduction was a rate over reruns (pp.11-13)."

### Paper claims checked against paper-reader notes, entailed, no change
- Endo 2020 (C:/Users/Q/code/papers/Endo_2020_NodeRacerEventRaceDetectionNodejs/notes.md): one observed run, HB graph, postpone only when more than one indegree-0 callback, postponed only once, postpone when predecessors not run (Algorithm 2, p.5); observable-failure oracle (p.2; hang p.3); NR-naive 64.1% avg runs with HB violation and "more than half of NR-naive failures involve an HB violation" (Table II, p.8); random timeouts in objection.js test broke HB (p.9); diagnosis mode one callback per run, different each run (p.6); Async Hooks does not say which functions are callbacks, njsTrace onEntry/onExit (p.4).
- Davis 2017 (…/Davis_2017_NodeFzFuzzingServerSideEventDriven/notes.md): built on Node.js v0.12.7, libuv-only changes (p.10); only documented-legal decisions, completion after task kept, libuv timer order and EventEmitter order kept, races depending on them not explored (pp.9-11); KUE 2014 timer-precision "race against time" (pp.12-13).
- Wang 2017 (…/Wang_2017_ComprehensiveStudyRealWorldConcurrency/notes.md): shared variable 54%, database 26%, file 14% (p.7); 93% ≤4 events (p.7), 95% one process, 86% one resource (p.8); Porybox#157 findOne/save interleaving (p.5).
- Raychev 2013 (…/Raychev_2013_EffectiveRaceDetectionEventDriven/notes.md): modified WebKit logs the trace (p.2).
- Adamsen 2017 (…/Adamsen_2017_RepairingEventRaceErrors/notes.md, printed pages): two developer expectations (p.3); mitmproxy instrumentation, controller loaded before app code, setTimeout and `XMLHttpRequest.prototype.send` interception (p.7); postponing one event may require others, user-event order preserved (p.4); harmfulness left to the user (p.4); replay failed where Ajax URLs depend on input, random numbers, timestamps (p.9).
- Chang 2019 (…/Chang_2019_DetectingAtomicityViolationsNodejs/notes.md): atomic pair and RWR/WWR/WRW/RWW patterns (pp.6-7); predictive, one trace, no schedule control (p.6); 12 reports: 3 harmful, 8 benign, 1 false positive where t prevents u (p.9); no tool URL or artifact in the paper.
- Repositories (gh api this session): noderacer 2317c673 committed 2022-12-15 and is HEAD; README line 21 "version used LTS 10.16.3". NodeFz 1ce111e3 committed 2019-07-07 and is HEAD; license `NOASSERTION`. eth-sri/EventRacer `pushed_at` 2015-09-21T15:01:12Z.

### Checked, entailed, no change (sources fetched raw this session)
- ECMA-262 at 828d35d0: "Only one Job may be actively undergoing evaluation at any point in time in an agent." line 12152; execution contexts clause 11881-11883; Agents 12330-12337; memory model 52687 ("possible orderings of Shared Data Block events, arising via accessing TypedArray instances backed by a SharedArrayBuffer and via methods on the Atomics object"); data race over SharedDataBlockEventSet 53249-53258, data race freedom 53260-53265.
- Node v26.13.0 test.md: Class `MockTimers` 2894; methods `enable` 2915, `reset` 3000, `[Symbol.dispose]` 3025 ("Calls `timers.reset()`"), `tick` 3029, `runAll` 3346, `setTime` 3411; no timer-count or next-timer method in 2894-3498.
- Node v26.13.0 async_hooks.md: line 5 "Stability: 1 - Experimental. Please migrate away from this API, if you can."; 44-45 independent `async_hooks` per Worker; 349 `type` "can change in any Node.js release"; 373 "shows _why_ a resource was created"; 438 not safe as `WeakMap` key; before/after/promiseResolve 589-660; 918 "significant performance overhead".
- Jest at 72614448 JestObjectAPI.md: 904 fakes `queueMicrotask()`; 906 Node `process.nextTick()`; 940 `doNotFake`; 1086 `advanceTimersToNextTimer`; 1118 `getTimerCount`.
- Vitest at 3a76b873 vi.md: 1002, 1058, 1211; 1226 "`vi.useFakeTimers()` does not automatically mock `process.nextTick` and `queueMicrotask`."
- React act.md at 7594a2b0: 45 "it doesn't work in all cases"; 53 "are added to an internal act queue, which are then flushed together".
- MSW delay.md at bda552eb: 28 random realistic time; 44 "when testing in Node.js, the implicit delay is negated"; 99 "making it pend forever".
- Playwright at 95e5dca3: class-page.md 575 "before any of its scripts were run", 618-619 order "is not defined", 3752 "stall unless it's continued, fulfilled or aborted", 3755 redirect first-url note, 3759 "will not intercept requests intercepted by Service Worker", 3763 popup first request, 3895 "Enabling routing disables http cache"; class-route.md 36, 446 "Performs the request and fetches result without fulfilling it", 568; params.md 1-9 `'commit'` "when network response is received and the document started loading".

## Validation (run after the edits)
- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/schedule-exploration` → "Skill is valid!", exit 0.
- Same for `race-detection-campaigns` → "Skill is valid!", exit 0.
- `git diff --check` on both skill directories and this report → no output, exit 0.
- Relative links (script over every `.md` in both skills): none broken.
- Cited URLs vs sources.yaml: schedule-exploration matches both ways. race-detection-campaigns matches both ways: the one mismatch my script printed came from it stripping `#hdr-Testing_flags`; SKILL.md:26, references/go-runtime.md:17 and sources.yaml:35 all use `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags`.
- `grep cd9c1884` in both skills: no matches.
- Diff: 5 files, 18 insertions, 18 deletions; no content added or restructured.
