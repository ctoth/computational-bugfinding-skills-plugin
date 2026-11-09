# Draft report: JS/TS schedule exploration (group B)

Drafter: draft-js-schedule. Branch: js-web-bugfinding. Skills: `schedule-exploration` (main), `race-detection-campaigns` (boundary note).

## Status

- [x] Inputs read
- [x] schedule-exploration edits
- [x] race-detection-campaigns boundary note
- [x] Validation

Nothing committed or pushed. No other skills, manifests, README or agent-notes edited.

## Inputs read

- `reports/research-js-schedule.md` (all 314 lines: S1-S7, L1-L2, decisions, common mistakes, sources inventory, unverified list).
- `reports/skill-plan-js-web-bugfinding.md` lines 1-80 (schedule-exploration and race-detection rows; "Literature folded in (batch 2)").
- `reports/skill-research-js-web-bugfinding.md` F5 (lines 89-101), F16 (238-249), and F3 pin line 70 (Node.fz repo pin and last commit).
- `reports/draft-schedule-exploration.md` (draft-report format; its link/source check fails on orphan or unused inventory entries, so every new sources.yaml entry must be cited and every new citation inventoried).
- `plugins/bugfinding/skills/schedule-exploration/SKILL.md`, all five references and `sources.yaml`; `plugins/bugfinding/skills/race-detection-campaigns/SKILL.md`, `references/common-mistakes.md`, `references/sources.yaml` head (schema: name/url/type/accessed/revision/sections_used/quote).
- Paper notes (grep of the page-cited lines used): Endo 2020 NodeRacer, Davis 2017 Node.fz, Wang 2017 NodeCB, Raychev 2013 EventRacer, Adamsen 2017 EventRaceCommander. Chang 2019 NodeAV notes: 3 lines, "Status: in progress. PDF retrieval pending; nothing below is read yet." (checked at start; rechecked at end, see below).

## Findings and decisions (appended as work proceeds)

1. Tool staleness is stated from pinned evidence only: NodeRacer repo README says Node LTS 10.16.3, last commit 2022-12-15 (F5); Node.fz repo last commit 2019-07-07, built on Node v0.12.7 (F3; Davis notes p.10); EventRacer last push 2015-09-21 and needs instrumented WebKit (F5; Raychev notes p.2, p.10). EventRaceCommander repo (https://github.com/cs-au-dk/EventRaceCommander, Adamsen notes p.7) maintenance state was not checked by any input; the reference says "not checked" rather than "unmaintained".
2. Page numbers: Endo, Davis, Raychev and Wang notes use PDF page numbers; Adamsen notes use printed page numbers 1-11. Citations copy each note's convention.
3. Node.fz "legal ordering" citation: the notes put the fidelity/legality section at p.10-11 and the kept timer/EventEmitter orders at p.9-10; the reference cites pp.9-11.
4. Followed research corrections: `waitNext`/`waitIdle`/`waitFor` only, deprecated `waitOne`/`waitAll`/`count()` named as deprecated; `schedulerFor` replay requires comparing `report()`; timer recipe stated as Jest-only, Vitest port labelled unexecuted, `node:test` MockTimers stated as lacking count/next-step; `createHook` stated Experimental with "Please migrate away"; Playwright service-worker, HTTP-cache, popup, redirect and undefined init-script-order caveats included.
5. Scheduler facts cite fast-check `cd9c1884`; `stateful-property-testing` pins `5ec2e3ac`. The divergence is recorded in the sources.yaml `sections_used` of the guide entry, not reconciled (scheduler files at `5ec2e3ac` not read by anyone).
6. Chang 2019 NodeAV notes were complete (300 lines, all 12 pages read per the notes) when the main draft was done; added one bullet ("Where to place seams first", pp.6-7, 9) and one sources entry. The "force the order to confirm" step is labelled as this pack's guidance, not the paper's.
7. async_context and v8.promiseHooks were left out (not needed for the plan rows); no hook-based scheduler shipped.

## Files changed

- `plugins/bugfinding/skills/schedule-exploration/SKILL.md`: description now names the fast-check scheduler and Node event-loop, promise, timer and browser/React async-ordering races; one JS lane bullet.
- `plugins/bugfinding/skills/schedule-exploration/references/javascript-event-loop.md` (new, 68 lines): control boundary, search policy and replay, timers, React, response order (MSW, Playwright), literature methods (NodeRacer, Node.fz, Wang 2017, NodeAV, EventRaceCommander; tools' staleness from pins), async_hooks as record-only.
- `plugins/bugfinding/skills/schedule-exploration/references/common-mistakes.md`: 7 entries (exhaustive claim, `waitIdle` vs fetch/emitters, `schedulerFor`-only replay, `node:test` timer port, `act` flush granularity, unguided perturbation, service-worker routing).
- `plugins/bugfinding/skills/schedule-exploration/references/sources.yaml`: 22 entries added (19 to 41).
- `plugins/bugfinding/skills/race-detection-campaigns/SKILL.md`: one boundary paragraph (ECMA-262 one job per agent; data races only over Shared Data Blocks; Node worker_threads share SharedArrayBuffer; route to schedule-exploration; no verified detector).
- `plugins/bugfinding/skills/race-detection-campaigns/references/common-mistakes.md`: one row.
- `plugins/bugfinding/skills/race-detection-campaigns/references/sources.yaml`: 2 entries (ECMA-262, worker_threads), existing schema with revision and quote.

## Validation output

Default `python` (Python313) lacks PyYAML (`ModuleNotFoundError: No module named 'yaml'`); reran with `C:/Users/Q/scoop/apps/python311/current/python.exe`.

```text
== schedule-exploration
Skill is valid!
== race-detection-campaigns
Skill is valid!
```

Link/inventory check (scratchpad script `check_links.py`: resolves every local Markdown link, compares cited http URLs to sources.yaml URLs both ways):

```text
plugins/bugfinding/skills/schedule-exploration: sources=41 cited=41
plugins/bugfinding/skills/race-detection-campaigns: sources=18 cited=18
errors: ['...race-detection-campaigns: cited but not in sources.yaml: https://pkg.go.dev/cmd/go@go1.27.3', '...race-detection-campaigns: in sources.yaml but not cited: https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags']
```

The one reported pair is pre-existing (HEAD sources.yaml line 35) and an artifact of my script stripping `#fragment` from citations but not from inventory URLs; it is the same URL. No missing local links. The new `references/javascript-event-loop.md` link from SKILL.md resolves.

```text
git diff --check -- plugins/bugfinding/skills/schedule-exploration plugins/bugfinding/skills/race-detection-campaigns
[no output, exit 0]
git diff --no-index --check /dev/null plugins/bugfinding/skills/schedule-exploration/references/javascript-event-loop.md
[no output; exit 1 only because the files differ]
```

These checks establish structure and inventory, not that each sentence is entailed by its source.

## Remaining unverified

- Nothing was executed. Unexecuted compositions, labelled in the reference: Vitest port of the Jest timer recipe; MSW resolver awaiting a scheduled promise; Playwright held routes released in order and `route.fetch()` plus held `fulfill`; `waitUntil: 'commit'` with held scripts; init-script wrappers; forcing a NodeAV triple's order at a seam.
- Inferences labelled as such: one schedule step per `act` flush; async_hooks cannot postpone.
- fast-check scheduler behavior at the `5ec2e3ac` pin used by `stateful-property-testing`; whether another fast-check file implements non-random scheduling.
- EventRaceCommander repository maintenance state (stated as "not checked"); NodeRacer tool URL brics.dk/noderacer; EventRacer README.
- MSW browser-mode resolver context; Playwright WebSocket routing; React production scheduling versus the act queue; `@sinonjs/fake-timers` with `node:test`.
- SharedArrayBuffer detector absence rests on a bounded search (five GitHub queries, one web search).
- Quotes from pinned docs were taken from `reports/research-js-schedule.md`; I did not refetch the primary pages in this pass. Paper facts were checked against the paper-reader notes, not the page images.
- Loring 2017 (async JS semantics) and the promise papers remain unread.

