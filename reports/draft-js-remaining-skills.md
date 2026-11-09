# Draft: JS/TS remaining skills (group I)

Drafter: draft-js-remaining-skills. Status: complete (2026-11-09); validation below.

## Inputs read

- `reports/research-js-remaining-skills.md` (full; decisions 1-5, M1-M9, sources inventory, unverified list).
- `reports/skill-plan-js-web-bugfinding.md:41-44,120`.
- `reports/draft-symbolic-concolic-execution.md` (format example).
- symbolic-concolic-execution: `SKILL.md`, `references/sources.yaml`, `references/common-mistakes.md`.
- failure-reduction: `SKILL.md`, `references/tool-recipes.md`, `references/common-mistakes.md`, `references/sources.yaml`.
- evidence-based-triage: `SKILL.md`, `references/triage-decisions.md`, `references/maintainer-handoff.md`, `references/common-mistakes.md`, `references/sources.yaml`.

Plan: follow research decisions 1-5 exactly. Before writing, spot-check the load-bearing quotes against the pinned URLs (curl, read-only).

## Source spot-check (2026-11-09, curl against pinned URLs, read-only)

Confirmed verbatim at the pins: ExpoSE README lines 4, 8, 40; `scripts/play` (Jalangi2 `--analysis bin/Analyser.js`); `symbols.js` `pureSymbol`/`assume`/`NotAnErrorException`/`assert`; `Center.js:167,195`; `Distributor.js:71,73,111,114`; `Config.js:47-53` (`"2h"`, `"40m"`, `EXPOSE_JSON_PATH` comment, `EXPOSE_PRINT_PC`); `.nvmrc` v10.22.0; `package.json` `^21.7.2`; `Spawn.js:130` SIGKILL; Jalangi2 fork `esnstrument.js:41,1881`; GitHub API latest master commit `ec03edf8` 2024-07-02. Note: ExpoSE README line 58 says `EXPOSE_MAX_TIME` is "in milliseconds" while `Config.js:47` parses it with `timeFrom(..., "2h")`; draft states the source default only.
Playwright pin `95e5dca3`: `test-retries-js.md:36,63,83`; `class-testconfig.md:117,438`; `test-cli-js.md:85,104,106`; `class-testoptions.md:715-730,720,723`; `test-use-options-js.md:176-186` table; `trace-viewer.md:25,44`; playwright-trace SKILL.md:3; `test-configuration-js.md:19,28,44`.
Node v26.13.0: `cli.md:909-922,1767-1780` ("before exit" on the wrapped line), `2648,2661,2666,2671,2885`; `report.md:499-501`; `BUILDING.md:649,658`; `test.md:733,740`.
Jest v30.5.2 `JestObjectAPI.md:1187,1197`; `CLI.md:206,347,349`; `Configuration.md:8,140`. Vitest v5.1.0 `retry.md:8`, `sequence.md:15,139`, `config/index.md:13,15`, `api/test.md:159`.
Jazzer.js `options.ts:517-518`; zero "minimi" hits in the three docs; `jest-integration.md:23-26,69`.
Perses README:5,23,51,79-81 (contradiction confirmed); Lithium README:22,27-28,39; Shrink Ray README:97-100,108-128; Fuzzilli README:3,114; IndexedDB `index.bs:932,934`; Stryker `config-file.md:67`.

## Findings and edits

### symbolic-concolic-execution (done)

- New `references/expose-javascript.md`: status, 4-step applicability check (stop and report "no supported JS backend" on failure; no porting), S$ harness, explicit limits, output classification, native witness. Research decision 1 (a)-(f).
- `SKILL.md`: description gains "JavaScript is supported only after an ExpoSE applicability check passes on the target."; one sentence in "Select a fitting producer" linking the reference.
- `references/common-mistakes.md`: three rows (research M1-M3).
- `references/sources.yaml`: 14 ExpoSE/Jalangi2 sources. Added beyond the research's citations: the `expoSE` shebang and `Dockerfile` (verified by curl) to back the POSIX-host sentence; commits/trees API URLs (verified: latest commit 2024-07-02; tree not truncated; `tests/async` = 1 file, `tests/regex` = 168 entries, `tests/es6` = const.js, let.js).

### failure-reduction (done)

- `references/tool-recipes.md`: new "JavaScript and TypeScript" section: fast-check (link to stateful-property-testing runtime recipes; scheduler does not shrink, link to schedule-exploration `javascript-event-loop.md`, which states "Not supported yet"); Jazzer.js `-minimize_crash=1` after `--`, source-accommodated, undocumented, composed command marked unexercised, replay against predicate; links to `node-jazzerjs.md` and `corpus-evolution` for merge (not repeated); Perses (self-contradiction stated), Lithium, Shrink Ray (`--no-llm`); Playwright `--repeat-each` vs retries.
- `SKILL.md`: one route-table row. Description unchanged (its generic wording already selects JS shrinking requests).
- `references/common-mistakes.md`: three entries (research M4 reduction part, M6, M7).
- `references/sources.yaml`: 8 sources.

### evidence-based-triage (done)

- `references/triage-decisions.md` ("Replay with the right representation"): one paragraph: Playwright retries/flaky/`failOnFlakyTests`, trace modes, Jest `retryTimes`/`logErrorsBeforeRetry`, Vitest `retry`, replay-rate via `--repeat-each`/`repeats`, order dependence via Jest `--randomize`/`--seed`, Vitest `--sequence.shuffle --sequence.seed`, Node v26.1+ `--test-randomize`/`--test-random-seed` (verified `cli.md:3260-3290`).
- `references/maintainer-handoff.md`: one paragraph on `trace.zip` (route to Playwright's `playwright-trace` skill), Node profiles "before exit", diagnostic reports, redaction.
- `references/common-mistakes.md`: four entries (M4 triage part, M5, M8, M9; M9's SIGKILL clause marked inference).
- `references/sources.yaml`: 13 sources. Description unchanged ("investigating flaky replay" already selects these requests).

### bugfinding-campaign (done)

- `references/campaign-example.md`: new final section "Inventorying a JavaScript or TypeScript project" (Jest, Vitest, node:test, Playwright, fast-check, StrykerJS, Jazzer.js; retry settings recorded as observation limits). First placement accidentally split "Close the record"; corrected by moving that section's closing paragraph back above the new heading.
- `SKILL.md`: one sentence in "Establish the present capability" linking the section.
- `references/sources.yaml`: 13 sources. No common-mistakes entry (research gives none for this skill). Description unchanged.

### No-route lines (done)

One paragraph each, in the reference a JS user would read; descriptions untouched:
- `semantic-program-generation/references/tool-choices.md`: Fuzzilli for patched engine shells (README:3,114; Targets contents API verified: V8, Spidermonkey, JavaScriptCore among 10); no generator for Node-level consumers. sources.yaml +2.
- `native-memory-instrumentation/references/native-boundaries.md`: new "Node native addons" heading: Linux-only Node ASan build; no addon recipe verified. sources.yaml +1.
- `deterministic-simulation/references/other-routes.md`: no adopted JS route; chronos and determined READMEs at full SHAs (verified by curl), created 2025-04-14 and 2026-03-22 (GitHub API); not evaluated. sources.yaml +4. Note: chronos' latest commit is dated 2026-11-09, so it is active, but adoption is unknown.
- `crash-consistency-testing/references/fault-routes.md`: Node uses existing process-failure/LazyFS routes; no browser-storage fault tool; IndexedDB `"strict"` is "may consider". sources.yaml +1.
- `bounded-model-checking/references/tool-recipes.md`: one sentence, bounded GitHub search dated; no citation (negative search result). sources.yaml unchanged.
- `liveness-testing/references/runtime-and-model-routes.md`: Node `--process-timeout`, Jest `--detectOpenHandles` as observations, not progress contracts. sources.yaml +2.
- `numerical-oracles`: no change (`tool-routes.md:7` already says no JavaScript binding verified).
- `metamorphic-testing`: no change (method-neutral, per plan row and research decision 5).

### bugfinding-campaign: ui-state-exploration routing row (team-lead request, 2026-11-09)

- `SKILL.md` specialist table: added row "Reachable browser or React UI states without an operation model, with per-state oracles and path replay | `ui-state-exploration`", placed after the `stateful-property-testing` row. The wording follows `ui-state-exploration/SKILL.md:3,8` ("model-free exploration of browser and React UI states", "no operation model exists"; choose `stateful-property-testing` when a model exists). No new citation, so `sources.yaml` is unchanged.
- Revalidated: quick_validate `Skill is valid!`; link/source check `bugfinding-campaign: OK`; `git diff --check` exit 0.

## Validation (run 2026-11-09 from repo root)

`uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/<skill>` for each of the ten touched skills (symbolic-concolic-execution, failure-reduction, evidence-based-triage, bugfinding-campaign, semantic-program-generation, native-memory-instrumentation, deterministic-simulation, crash-consistency-testing, liveness-testing, bounded-model-checking): every one printed `Skill is valid!`.

Link/source check (read-only script in the scratchpad, `check_links.py`: resolves local Markdown links including `#anchor` against headings; compares every cited http(s) URL, fragment stripped, with `sources.yaml` both ways; flags duplicates): all ten skills `OK`.

`git diff --check` on the ten skill directories and this report: no output, exit 0.

URL reachability: every URL in the diff and in `expose-javascript.md` returned HTTP 200 (`curl`; five GitHub API URLs and sqlite.org first showed `000` from a curl write-out error, then `HTTP/1.1 200 OK` on a HEAD recheck).

Stray command: I ran `git stash create` once by mistake inside a probe. It only creates an unreferenced commit object; it changes no ref, index or working-tree file.

## Files changed

New:
- `plugins/bugfinding/skills/symbolic-concolic-execution/references/expose-javascript.md`
- `reports/draft-js-remaining-skills.md` (this report)

Modified:
- `symbolic-concolic-execution/`: `SKILL.md` (description + one sentence), `references/common-mistakes.md`, `references/sources.yaml`
- `failure-reduction/`: `SKILL.md` (one route row), `references/tool-recipes.md`, `references/common-mistakes.md`, `references/sources.yaml`
- `evidence-based-triage/references/`: `triage-decisions.md`, `maintainer-handoff.md`, `common-mistakes.md`, `sources.yaml`
- `bugfinding-campaign/`: `SKILL.md` (one sentence), `references/campaign-example.md`, `references/sources.yaml`
- `semantic-program-generation/references/`: `tool-choices.md`, `sources.yaml`
- `native-memory-instrumentation/references/`: `native-boundaries.md`, `sources.yaml`
- `deterministic-simulation/references/`: `other-routes.md`, `sources.yaml`
- `crash-consistency-testing/references/`: `fault-routes.md`, `sources.yaml`
- `liveness-testing/references/`: `runtime-and-model-routes.md`, `sources.yaml`
- `bounded-model-checking/references/tool-recipes.md`

Not touched: numerical-oracles, metamorphic-testing, any skill owned by another group, manifests, README, agent-notes. Nothing committed or pushed.

## Remaining unverified items

- Nothing was installed or executed. ExpoSE install (including the `setup_packages` `Dashboard` step with no `Dashboard/` directory), its behavior on promises/async/ESM/modern syntax, and on any Node other than 21.7.2 are unverified. The Babel 6 syntax limit is inference from the instrumenter's versions.
- ExpoSE README line 58 calls `EXPOSE_MAX_TIME` milliseconds while `Config.js:47` parses `timeFrom(..., "2h")`; the draft states only the source default. Accepted value formats were not checked.
- Jazzer.js `-minimize_crash=1`: the composed command is unexercised and marked so; behavior under the Jest runner is unknown.
- Perses JS support: README contradicts itself (stated in the text). Lithium and Shrink Ray on JS: not run.
- Vitest: whether a fail-then-pass under `retry` is reported as flaky and whether it fails the run (open; draft only says it retries).
- Whether `npm init playwright` generates `retries: process.env.CI ? 2 : 0` and `trace: 'on-first-retry'` like the docs example (not stated in the draft).
- Profile loss on a killed Node process: marked inference.
- Node addon ASan recipe: not searched beyond `BUILDING.md`.
- chronos/determined: READMEs and repo metadata only; correctness and adoption unknown. Bounded-model-checking and browser-storage "none found" lines rest on bounded searches from the research report, not proof of absence.
- ExpoSE paper (SPIN 2017): not read; nothing depends on it.

Status: complete.
