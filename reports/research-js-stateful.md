# Research: stateful-property-testing, JS/TS (Node and React) extension

Phase 3 per-skill researcher, group E. Branch js-web-bugfinding. Date 2026-11-09.
Status: complete for drafting. No skill, manifest, README or agent-note edits; nothing installed, executed against a target, committed or pushed. The code sketch in J7 is a pattern for the drafter and has not been run.

## Repository inputs read

- `reports/skill-plan-js-web-bugfinding.md:33` (stateful row), `:65-70` (Nessie bullet: "fast-check commands do not nest calls inside callbacks. The reference must say so and give the nesting pattern."), `:78` (tool availability open), `:80-97` (ui-state-exploration owns model-free crawl; this skill keeps model-based UI sequences).
- `reports/skill-research-js-web-bugfinding.md` F2 (:48-66), F9 (:149-169), F10 (:171-183), F11 (:185-192), existing-skills table (:292).
- Skill files: `plugins/bugfinding/skills/stateful-property-testing/SKILL.md` (JS route at :33), `references/runtime-recipes.md` (fast-check section :15-21 already covers `check`/`run`/`toString`, `modelRun` vs `asyncModelRun`, replayPath, scheduledModelRun as separate concern, MIT/ESM/Node floor), `references/model-and-sequences.md`, `references/common-mistakes.md`, `references/sources.yaml`. Existing fast-check links are pinned at `5ec2e3ac` (package 4.10.2).
- Evidence standard: `reports/research-stateful-property-testing.md` (S-numbered ledger: URL, quote fragment, finding, decision).
- Paper notes: `C:/Users/Q/code/papers/Arteca_2022_NessieAutomaticallyTestingJavaScript/notes.md`; `C:/Users/Q/code/papers/Selakovic_2018_TestGenerationHigherOrderFunctions/notes.md`.

## Findings

### J1. fast-check main is a v5 development line; pin released API to tag v4.10.2

- Sources: `dubzzz/fast-check` main at `cd9c1884e8a39fe945600fbcda1ec92d518feaa0` (committed 2026-11-09); tag `v4.10.2` -> commit `c77afa8277a67250d798c52e61343b8ed5fd268b` (annotated tag object `5da531a1`); `npm view fast-check` on 2026-11-09: `latest: '4.10.2'`.
- Fact: main carries breaking commits after 4.10.2, e.g. `fd17f486` 2026-10-04 "💥 Rename `asyncProperty` into `property` (#7412)", `33342651` 2026-09-17 "💥 Drop ability to default import from fast-check (#7307)". Main's `packages/fast-check/package.json` still says 4.10.2, so the version field does not reveal this.
- Fact: the same example differs between the two pins. At v4.10.2, `examples/005-race/todolist/main.spec.tsx:5,19-20,40-42` uses `import fc from 'fast-check'`, `fc.asyncProperty(...)` and `.beforeEach(async () => { await cleanup(); })`. At main, `:5,19,40-44` uses `import * as fc`, `fc.property(...)` with an async predicate and `plugins: [fc.beforeEach(async () => { await cleanup(); })]`.
- Fact: at tag v4.10.2 the property-level `.beforeEach` is already marked `@deprecated Prefer the life-cycle plugins: \`fc.assert(property, { plugins: [fc.beforeEach(fn)] })\`` (`packages/fast-check/src/check/property/AsyncProperty.generic.ts:134-143`), and the plugin `fc.beforeEach` ("Register a callback to be called before each run of your predicate", "Hook to be executed before each execution of the predicate", "@remarks Since 4.10.0") exists in `packages/fast-check/src/check/plugin/LifeCyclePlugins.ts:180-196`. So the plugin form works on released 4.10.x; only `asyncProperty` vs `property` differs from main.
- Fact: `ModelRunner.ts` is identical between the two pins apart from added `/** @internal */` comments (diff run 2026-11-09). So `modelRun`, `asyncModelRun`, `scheduledModelRun` claims hold for both.
- Decision for drafter: cite fast-check examples at tag commit `c77afa82` (released 4.10.2), recommend the `plugins: [fc.beforeEach(...)]` form (4.10.0+), and say that the unreleased v5 line renames `asyncProperty` to `property`; check the project's installed version before copying an example. Runner-source citations may stay at the existing `5ec2e3ac` pin.

### J2. fast-check runs a flat, sequential command list; it has no nesting inside callbacks

- Source: `packages/fast-check/src/check/model/ModelRunner.ts` at `cd9c1884`, lines 26-44 (`genericModelRun`), 56-60 (`runSync`), 90-92 (`runAsync`), 144-157 (`scheduledModelRun`); `packages/fast-check/src/check/model/command/ICommand.ts` and `AsyncCommand.ts` at the same commit.
- Fact: `genericModelRun` iterates `for (const c of cmds)` over an `Iterable` and chains each command after the previous one (`state = then(state, () => runCmd(c, model, real))`). The async runner is `if (await cmd.check(m)) await cmd.run(m, r);`.
- Fact: the command interface is `check(m: Readonly<Model>)`, `run(m: Model, r: Real): RunResult`, `toString()`. `run` receives only the model and the real system; there is no parameter or return channel through which a command could receive a callback's arguments or schedule a child command. `AsyncCommand` fixes `RunResult` to `Promise<void>`.
- Fact: `scheduledModelRun` wraps the commands with `scheduleCommands(scheduler, cmds)` and awaits `scheduler.waitFor(out)` then `scheduler.waitAll()`; commands are still the same flat list, with the scheduler deciding when each starts relative to scheduled promises. Docs (`website/docs/advanced/race-conditions.md:310-312` at `cd9c1884`): "Neither `check` nor `run` should rely on the completion of other scheduled tasks to fulfill themselves. But they can still trigger new scheduled tasks as long as they don't wait for them to resolve."
- Inference (from the interface, not a doc statement): a command can still make nested calls inside its own `run` body (call API A with a callback that calls API B with A's callback argument), but fast-check then neither generates nor shrinks that inner structure; only the outer command list is generated and shrunk. No fast-check doc or source says "commands cannot nest" in those words; the claim rests on the interface above. The reference should phrase it as "the runner executes a flat list; `run(model, real)` has no access to callback arguments", not as a quote.

### J3. fast-check ships one model-based React UI example: RTL + user-event + act + scheduler

- Source: `examples/005-race/todolist/` at main `cd9c1884` (and the same files at tag `c77afa82`): `main.spec.tsx`, `model-based/Model.ts`, `model-based/AddItemCommand.ts`, `model-based/ToggleItemCommand.ts`; `examples/package.json` (devDependencies `@testing-library/react ^16.3.3`, `@testing-library/user-event ^14.6.8`, `@testing-library/dom ^10.4.2`, `happy-dom ^21.0.4`, `react ^19.3.1`, `vitest ^5.1.0`; MIT).
- Facts, `main.spec.tsx` (main pin):
  - `/** @vitest-environment happy-dom */` (line 2); imports `render, act, cleanup` from `@testing-library/react` (line 9).
  - Arbitraries: `fc.scheduler()`, `fc.commands([...])`, initial server todos, and an iterator of booleans that decides per call whether the mocked API fails (lines 20-25).
  - Mock API functions are wrapped with `s.scheduleFunction(fn, act)` (lines 64-124): the scheduler resolves each response inside React `act`.
  - Each run renders afresh, `render(<TodoList {...mockedApi} />)`, then `await fc.scheduledModelRun(s, () => ({ model: { todos: [], wrapper }, real: {} }), commands)` (lines 30-31).
  - Final check after all commands: no item still loading and DOM list equals the mock server's list (lines 34-36).
  - Cleanup between runs: `fc.beforeEach(async () => { await cleanup(); })` plugin (lines 40-44); the tag uses the deprecated `.beforeEach(...)` form (J1).
- Facts, commands:
  - `AddItemCommand.run` reads the DOM list, then `await act(async () => { await userEvent.clear(...); await userEvent.type(...); await userEvent.click(...) })`, then re-reads and compares the before/after lists (AddItemCommand.ts:18-33). It escapes `{` and `[` before `userEvent.type` because user-event treats them as key descriptors (lines 6-9, "Copied from https://github.com/testing-library/user-event/issues/586").
  - `ToggleItemCommand.check` reads the real DOM (`await listTodos()`) and admits the command only if some item is not loading (ToggleItemCommand.ts:9-13). Its `run` selects `position % nonLoadingTodos.length`, records the resolved item in `runDetails`, and `toString()` prints it (lines 15-23, 46-48).
  - The model object `{ todos: [], wrapper }` is never updated by these commands; the oracle is per-command before/after DOM observation plus a final comparison with the mock server state.
  - `Model.ts:23-40` observes the UI through `screen.queryAllByTestId('todo-item')` and raw `getElementsByTagName`, not role queries. Commands call the `userEvent.click/type` direct API, not `userEvent.setup()`.
- Decision for drafter: this is the primary-source React recipe to cite. State its departures honestly: `check` reads real DOM (it is an async command, `CheckAsync = true`, Model.ts:11), so admissibility is not recomputed from a model on shrink; the model is unused. The skill's own rule (keep a contract model; recompute admissibility from the reduced prefix) still applies; the example shows wiring, not modeling discipline. Do not present it as using role queries.
- Playwright: GitHub code search `repo:dubzzz/fast-check playwright` (2026-11-09) returned only `skills/javascript-testing-expert/SKILL.md` (which names `@vitest/browser-playwright` as tooling). No fast-check doc or example drives Playwright with commands. Code search for `testing-library` returned only the `examples/005-race/*` files, the skill, changelogs and two blog posts (not read).

### J4. RTL cleanup and act environment are per test-runner hook, not per property run

- Sources: `testing-library/react-testing-library` main `20ce75f2907ca0e5c5a8ae595c0e9a4e368c7800`, `src/index.js:4-39`, `src/pure.js:39-61`; `testing-library/testing-library-docs` main `7c49d046b100e657c64bae78270a5813c1c02eb6`, `docs/react-testing-library/api.mdx:317-354`; `vitest-dev/vitest` main `3a76b87324ecb8d25509cd009aa87fbe56819c39`, `docs/config/globals.md`; react.dev `act.md` lines per F9 (`reports/skill-research-js-web-bugfinding.md:161`). npm on 2026-11-09: `@testing-library/react` 16.3.3, `@testing-library/user-event` 14.6.8.
- Facts:
  - RTL auto-cleanup registers `afterEach(() => { cleanup() })` only `if (typeof afterEach === 'function')`, and sets `IS_REACT_ACT_ENVIRONMENT` true in `beforeAll` only if global `beforeAll`/`afterAll` exist (`src/index.js:12-15, 27-37`). Skippable with `RTL_SKIP_AUTO_CLEANUP` (line 9).
  - Docs: cleanup "is called automatically if your testing framework (such as mocha, Jest or Jasmine) injects a global `afterEach()` function"; "Failing to call `cleanup` when you've called `render` could result in a memory leak and tests which are not \"idempotent\"" (api.mdx:319-343).
  - Vitest `globals` "**Default:** `false`" and its tip: "some libraries, e.g., `@testing-library/react`, rely on globals being present to perform auto cleanup."
  - RTL's `act` "is a light wrapper around the [`react` `act` function]" (api.mdx:350-354). React `act` "requires setting `global.IS_REACT_ACT_ENVIRONMENT=true`" (F9).
  - RTL's `asyncWrapper` (used by `waitFor`/`findBy*`) sets the act environment to false during the wait and restores it after (pure.js:39-61).
  - fast-check's `fc.beforeEach` plugin runs "before each execution of the predicate" (`LifeCyclePlugins.ts:191`, tag `c77afa82`).
- Inference: one fast-check property inside one `it` performs many `render` calls; `afterEach` fires once after the whole property. Without per-run cleanup, earlier runs' trees remain in `document.body`, so `screen` queries see stale components and a failure may depend on earlier runs (not reproducible from the shrunk case alone). fast-check's own example calls `cleanup()` in a per-run `beforeEach` (J3). Under Vitest with default `globals: false`, neither auto-cleanup nor the `IS_REACT_ACT_ENVIRONMENT` setup runs unless the project configures globals or does them explicitly.
- Decision for drafter: recipe line: render inside the predicate, call `cleanup()` per run through `plugins: [fc.beforeEach(...)]`, and confirm `IS_REACT_ACT_ENVIRONMENT` is true in the project's setup (do not assume RTL did it under Vitest).

### J5. Interaction semantics and retrying observation (Testing Library)

- Sources: testing-library-docs `7c49d046`: `docs/user-event/intro.mdx:23-49, 60`, `docs/user-event/options.mdx:9-13, 51-62`, `docs/dom-testing-library/api-events.mdx:9-13`, `docs/dom-testing-library/api-async.mdx:46-90`, `docs/queries/about.mdx:55-75, 94-110`.
- Facts:
  - "`fireEvent` dispatches _DOM events_, whereas `user-event` simulates full _interactions_, which may fire multiple events and do additional checks along the way" (intro.mdx:25-27). user-event "adds visibility and interactability checks" and "factors in that the browser e.g. wouldn't let a user click a hidden element or type in a disabled text box" (:38-41). Some interactions "aren't yet implemented"; "In these cases you can use `fireEvent`" (:44-49). "We recommend invoking `userEvent.setup()` before the component is rendered" (:60).
  - api-events.mdx:11-13: "Most projects have a few use cases for `fireEvent`, but the majority of the time you should probably use `@testing-library/user-event`."
  - user-event `delay` (default `0`): input is "delayed per `setTimeout`", which "moves the next changes at least to the next macro task and allows other (asynchronous) code to run between events" (options.mdx:51-62). With fake timers `advanceTimers` must be set (options.mdx:9-13).
  - `waitFor`: "the callback must throw an error in order to retry"; it "may run the callback a number of times until the timeout is reached"; default interval 50ms, timeout 1000ms; re-runs on DOM mutations (api-async.mdx:46-90). `findBy*` = `getBy*` + `waitFor`, rejected "after a default timeout of 1000ms" (about.mdx:58-75).
  - Query priority: "`getByRole`... every element that is exposed in the accessibility tree... This should be your top preference for just about everything" (about.mdx:94-110).
- Inference: a command that observes with `findBy*`/`waitFor` passes as soon as the expected state appears once inside the window; an intermediate wrong state (flash of stale data, a control enabled before its data loaded) is never asserted. Use `findBy*`/`waitFor` only to wait for settledness, then assert the full expected observation with synchronous `getBy*`/`queryBy*`; when the transient state is itself the contract (no flash of stale data), assert it at a scheduler-controlled point (with `fc.scheduler` `waitNext`, F2) rather than by polling. The user-event `delay` macrotask gap is itself an interleaving point with app async work.
- Decision for drafter: (a) commands drive input with `user-event` (via `userEvent.setup()`), fall back to `fireEvent` only for unimplemented interactions, and record which; a `fireEvent.click` on a disabled/hidden element is not a user-reachable transition. (b) Observe by role/accessible name where the UI exposes it; record a test-id fallback as a limit. (c) Retrying assertions are settle waits, not the oracle.

### J6. Playwright page-level sequences: context per test, auto-wait, retrying assertions, aria snapshots

- Sources: `microsoft/playwright` main `95e5dca31981bcd0970165853fcc713269d2433a` (F10 pin; repo `package.json` 1.66.0-next; npm `playwright` latest 1.65.0 on 2026-11-09): `docs/src/browser-contexts.md:8-12`, `docs/src/test-assertions-js.md:21-28, 64-68`, `docs/src/actionability.md:5-17`, `docs/src/aria-snapshots.md:7-9`, `docs/src/api/class-locator.md:153-158, 243-248`, `docs/src/api/class-browser.md:177-185`, `docs/src/test-timeouts-js.md:15`, `docs/src/locators.md:76`.
- Facts:
  - Isolation: "Playwright creates a context for each test, and provides a default [Page] in that context"; contexts give each test "its own local storage, session storage, cookies etc." (browser-contexts.md:12). `Browser.newContext` "won't share cookies/cache with other browser contexts"; close it explicitly via `BrowserContext.close` (class-browser.md:181-185).
  - Actions auto-wait: for `click`, Playwright ensures the element is Visible, Stable, Receives Events, Enabled, Not Inert; failure after `timeout` is `TimeoutError` (actionability.md:7-17).
  - Assertions: auto-retrying assertions "will retry until the assertion passes, or the assertion timeout is reached"; default 5 seconds (test-assertions-js.md:21-28). Non-retrying assertions exist; docs say "Prefer auto-retrying assertions whenever possible" (:64-68).
  - Observation: `toMatchAriaSnapshot` asserts "the accessibility tree of a page against a predefined snapshot template" (aria-snapshots.md:9); `Locator.ariaSnapshot()` (since v1.49) returns the snapshot string; `Locator.ariaSnapshotJSON()` (since v1.63, JS) returns a JSON object (class-locator.md:153-158, 243-248). Locators: "we recommend prioritizing user-facing attributes and explicit contracts such as `page.getByRole`" (locators.md:76).
  - Playwright Test timeout is "30 seconds by default" per test, including fixtures and `beforeEach` (test-timeouts-js.md:15).
- Inference: the Playwright Test fixture context is per `test`, not per fast-check run; a property with many runs inside one `test` must create and close `browser.newContext()` (and its page) per run, or state (storage, cookies, service workers, server-side data) leaks between runs. The whole property shares one 30 s test timeout, so the run budget must be set against it. The same masking issue as J5 applies with a 5 s window: web-first `expect` is a settle wait; for the oracle, capture a single non-retrying observation (`ariaSnapshotJSON()` or role-locator reads) after an app-specific settle signal and compare it with the model. Auto-wait means a command on a disabled control waits and then times out instead of exercising "click on disabled"; such a command needs an explicit admissibility check or its own expectation. Server-side state behind the page is not reset by a new context.
- Decision for drafter: one paragraph in the UI section; route driver mechanics to Playwright's own skills (`playwright-cli`, F10 table at `skill-research-js-web-bugfinding.md:294`) and settle-signal design to `ui-state-exploration`.

### J7. Node async callback APIs: Nessie-style call trees expressed with fast-check

- Sources: Nessie notes pp.1495-1499, 1501 (`Arteca_2022.../notes.md`); fast-check `website/docs/core-blocks/arbitraries/combiners/recursive-structure.md:9-80` at tag `c77afa82` (`fc.letrec(builder)`, `tie`, `maxDepth`/`depthIdentifier`, `depthSize`, `withCrossShrink`); `packages/fast-check/src/arbitrary/array.ts:51` (`array` accepts `depthIdentifier`) at the same tag; J2 for the runner limit.
- Paper facts (from notes, page numbers printed):
  - Values that exist only inside callbacks (file handles) and ordering (call `read` after `exists` completes) are reached by nesting the second call in the first call's callback and passing callback parameters (p.1495).
  - Test case tree, Def. 2-3: call nodes and callback nodes; an argument may be a pool value, the return value of a left sibling (or of a left sibling of an ancestor), a parameter of a callback on the root path, or a callback (p.1497).
  - Extension points are only callbacks that executed in exception-free tests; never-invoked callbacks get none (p.1498).
  - Callback position and sync/async discovered by probing: callback log after "Test executed" means async, before the call returns means sync (p.1496). One callback per probe; multi-callback signatures are missed (p.1496, 1500).
  - Oracle: differential across consecutive commits, each test run 10 times per commit, output sets compared (p.1501). Every inspected difference could in principle be exposed by a sequence-only test; nesting's benefit is reaching diverse behavior faster (p.1502).
  - Generation targets callback-style APIs; promise/async-await generation is not described (notes, Open Questions; p.1494).
- Pattern for the drafter (inference; adapts the paper's tree to fast-check; not run):
  1. Signatures: take callback positions from the API's documentation or types; where neither exists, run the paper's probe (p.1496) once and save the result as a fixture.
  2. Generate a tree, not a list: `fc.letrec(tie => ({ calls: fc.array(tie('call'), { depthIdentifier: 'cb' }), call: fc.record({ api: fc.constantFrom(...apis), args: fc.array(argRef), inCallback: tie('calls') }) }))`, where `argRef` is either a literal arbitrary or `{ scope: fc.nat() }`. `calls` children of a node run inside that node's callback (contains edge, p.1497).
  3. Interpreter resolves scope at execution time: a scope reference picks `scope[k % scope.length]` from the values lexically in scope (callback parameters on the root path, earlier return values), as fast-check's own `ToggleItemCommand` resolves `position % length` (J3). This keeps every shrunk tree well-formed (the same reason RapidCheck recomputes preconditions; existing skill text), and the resolved value must be logged because shrinking can change what an index refers to.
  4. Callbacks record that they ran and their parameters, then interpret their children with an extended scope. For promise-returning APIs, the same tree applies with children run in `.then(v => ...)` (inference; the paper does not cover promises).
  5. Count reach as the paper's extension rule implies: children under a callback that never ran, or under a call that threw, did not execute; report executed-node counts, not generated-node counts (p.1498). fast-check has no feedback loop, so this is a measurement, not a generation bias.
  6. The property awaits completion of all invoked callbacks with a timeout per run; a callback that runs twice, never, or after the timeout is an observation, not noise (Nessie's difference kinds include "callback called in one commit only", p.1501).
  7. Oracle: a contract model per callback where one exists; otherwise route the paper's commit-to-commit differential (10 runs, set comparison) to `semantic-differential-testing` (plan line `:71-76` already routes LambdaTester there).
  - A tree can be the payload of one fast-check command if the target also needs flat sequences around it; the command's `toString` must print the resolved tree.
- Decision for drafter: put this in the Node section of the JS reference as an ordered pattern with a short sketch, not a library. Do not claim fast-check offers nesting; do not ship a generic tree interpreter.

### J8. Nessie and LambdaTester availability

- `emarteca/nessie`: GitHub, MIT, language Rust, last commit `7875cb576ba4ec1ecf23c6ac4ff8f4cdeee7dcf7` 2023-08-05 "more docs", not archived (GitHub API 2026-11-09). README: requires rustup, Node.js, npm, yarn; "`nessie` has only been tested on linux" (test timeout uses Linux `timeout`); usage `cargo run -- --lib-name <pkg> --num-tests <n>` with optional mined-data and mode flags (`OGNessie`, ..., `Head` default). Paper artifact: Zenodo record 5874851, "[Artifact] Nessie: Automatically Testing JavaScript APIs with Asynchronous Callbacks", license CC-BY-4.0, published 2021-11-09 (Zenodo API).
- `sola-da/LambdaTester`: GitHub, MIT, last commit `f993f9d67eab0120b14111be1a56d40b4c5ac9af` 2018-09-27; README requires Node.js ">v6" and Jalangi2 checked out alongside. Nessie re-implemented it because the original "lacks ES6+ support" (Nessie notes p.1499).
- Decision: both are research artifacts; neither is a maintained route. Name them as method sources only. Nessie on Linux could be tried by a user as a one-off generator for a callback-heavy library; nothing here verifies it runs on current Node (not executed).

### J9. Official fast-check skill: what to route there and what to own here

- Source: `skills/javascript-testing-expert/SKILL.md` at fast-check main `cd9c1884`, 406 lines, read in full; last three commits to the file include `fd17f486` 2026-10-04 (asyncProperty rename).
- Facts:
  - Description: "Expert-level JavaScript testing skill ... Advocates for property-based testing with fast-check and protects against indeterministic code in tests. Does not cover black-box e2e testing." (line 3). Scope line 6: "Testing functions and components, not black-box e2e."
  - Contents: tooling list including `vitest`, `fast-check`, `@fast-check/vitest`, `@testing-library/*`, `@vitest/browser-playwright`, `msw` (line 15); file layout and naming (20-44); AAA, stubs over mocks, msw for network, reset globals in `beforeEach` (46-99); stable values via `vi.setSystemTime` or generated dates (140-160); role/label/text queries over test ids (195); property guidelines, including "❌ NEVER specify any `maxLength` on an arbitrary if it is a not a requirement of the algorithm" and avoid overusing `.filter`/`fc.pre` (200-247); v4 vs v5 `asyncProperty`/`property` note and "always await `fc.assert(...)`" (204-206); race conditions with `fc.scheduler()` and `scheduleFunction`/`waitFor` (249-293); faker bridge (295-341); `@fast-check/vitest` equivalences (343-406).
  - `grep -niE "command|model|asyncModelRun|act\(|playwright|e2e"` on the body matched only lines 3, 6 and 15: it has no `fc.commands`, model-based testing, `asyncModelRun`/`scheduledModelRun`, replayPath, `act`, cleanup-per-run, or Playwright page content.
- Decision:
  - Route to it: general fast-check test authoring style (file layout, AAA, naming), arbitrary-construction hygiene, `@fast-check/vitest` usage, v4/v5 API spelling, basic `fc.scheduler()` race tests on a single async function.
  - Own here: command/model design, admissibility and shrink-safe selection, replay artifacts (`replayPath`), executed-vs-generated counts, UI command recipes (RTL per-run cleanup/act, Playwright context per run), retrying-assertion masking, Node call trees.
  - Page-level Playwright sequences are outside its stated scope ("not black-box e2e"), so there is no overlap there.
  - Tension to note: its "NEVER specify any `maxLength`" rule is about value arbitraries; the call-tree sketch in J7 bounds depth with `depthIdentifier`/`depthSize` rather than `maxLength`, so it does not conflict.

## Decisions for the drafter

1. **Which file.** Create `references/ui-and-async-js.md` (or extend `runtime-recipes.md` with two subsections under "JS/TS: fast-check"; the plan row allows either). Recommendation: a new reference file, because the UI and callback-tree material is longer than the other runtime sections and `runtime-recipes.md` should stay a per-language route table. Contents:
   - Pins: examples at fast-check tag `c77afa82` (4.10.2); `plugins: [fc.beforeEach(...)]` (4.10.0+); note v5 spelling (J1).
   - React component sequences (J3, J4, J5): render per run, `cleanup()` per run via the `fc.beforeEach` plugin, `IS_REACT_ACT_ENVIRONMENT` check, wrap user-event interactions and scheduled responses in `act` (`scheduleFunction(fn, act)`), user-event over fireEvent, role queries, retrying queries as settle waits only, log resolved targets in `toString`; cite the todolist example and its departures (unused model, DOM-reading `check`).
   - Playwright page sequences (J6): `browser.newContext()` per run and close, one test timeout for the whole property, auto-wait vs deliberate disabled-control commands, `ariaSnapshotJSON()` or role reads as a single observation after an app settle signal, server state not reset by a new context.
   - Node callback/promise APIs (J7): flat-list limit, call-tree pattern, executed-node counting, oracle routing.
2. **SKILL.md.** Change the JS/TS bullet at `SKILL.md:33` to point to the new file for React UI sequences and Node callback APIs. Add one sentence in "Generate meaningful dependent operations": values available only inside a callback need a nested call, which fast-check's flat command list does not generate (J2, Nessie p.1495).
3. **Description wording** (frontmatter). Proposed: "Guides model-based property testing of dependent API, protocol and UI operation sequences. Use when bugs require object lifetimes, permissions, session transitions or setup history; for React components or pages driven by Testing Library or Playwright with fast-check commands; or for Node async APIs where later calls need values from earlier callbacks or promises; and when shrinking must preserve those dependencies." Keep the boundary sentences in the body: model-free UI crawling is `ui-state-exploration`, controlled interleavings are `schedule-exploration`, general fast-check test authoring is the fast-check `javascript-testing-expert` skill.
4. **sources.yaml.** Add entries listed in the inventory below with `accessed: '2026-11-09'`.
5. **common-mistakes.md.** Add the mistakes below.
6. **Do not** ship a tree-interpreter library, a crawler, or Playwright fixture code; do not quote fast-check as saying "commands cannot nest".

## Common mistakes (with evidence)

- **Wrong:** Rely on RTL auto-cleanup between property runs. **Better:** call `cleanup()` per run; auto-cleanup is a test-level `afterEach` and only registers if `afterEach` is global (RTL `src/index.js:12-15`; Vitest `globals` default `false`); fast-check's example cleans in a per-run `beforeEach` (todolist `main.spec.tsx:40-44`), which runs "before each execution of the predicate" (`LifeCyclePlugins.ts:191`).
- **Wrong:** Use `findBy*`/`waitFor` or Playwright web-first `expect` as the command's oracle. **Better:** use them to wait for a settled state, then assert the full observation once; they retry until the condition holds (1000 ms default, `api-async.mdx:75-78`; 5 s default, `test-assertions-js.md:21-28`), so a transient wrong state passes.
- **Wrong:** `fireEvent.click` on a disabled or hidden control counts as a reachable user transition. **Better:** drive with user-event, which "wouldn't let a user click a hidden element or type in a disabled text box" (`user-event/intro.mdx:38-41`); keep `fireEvent` for unimplemented interactions and label them.
- **Wrong:** Reuse the Playwright test's `page`/`context` across property runs. **Better:** `browser.newContext()` per run and close it; Playwright "creates a context for each test" (`browser-contexts.md:12`), not per run; server-side state needs its own reset.
- **Wrong:** Expect `fc.commands` to place a call inside an earlier call's callback, or count generated nested calls as exercised. **Better:** generate a call tree and count only nodes under callbacks that ran (runner loop `ModelRunner.ts:36-41`; Nessie extension rule p.1498).
- **Wrong:** Copy fast-check examples from `main` into a project on 4.x. **Better:** read examples at the released tag; main renamed `asyncProperty` to `property` and dropped the default import (J1).
- **Wrong:** Treat fast-check's todolist example as a modeling template. **Better:** use it for wiring only; its model is never updated and `check` reads the DOM (`ToggleItemCommand.ts:9-13`), so the skill's model and shrink rules still apply.

## Sources inventory (all accessed 2026-11-09)

| Source | Pin | Used for |
|---|---|---|
| fast-check `examples/005-race/todolist/{main.spec.tsx, model-based/*.ts}` | tag v4.10.2 `c77afa8277a67250d798c52e61343b8ed5fd268b`; also main `cd9c1884` | J1, J3 |
| fast-check `src/check/property/AsyncProperty.generic.ts`, `src/check/plugin/LifeCyclePlugins.ts` | tag `c77afa82` | J1, J4 |
| fast-check `packages/fast-check/src/check/model/ModelRunner.ts`, `command/ICommand.ts`, `command/AsyncCommand.ts` | main `cd9c1884e8a39fe945600fbcda1ec92d518feaa0` (runner identical to tag) | J2 |
| fast-check `website/docs/advanced/race-conditions.md` (act section :247-263; model-based :306-312) | main `cd9c1884` | J2, J3 |
| fast-check `website/docs/advanced/model-based-testing.md` (:76-81 runners) | main `cd9c1884` | J2 |
| fast-check `website/docs/core-blocks/arbitraries/combiners/recursive-structure.md`; `src/arbitrary/array.ts` | tag `c77afa82` | J7 |
| fast-check `skills/javascript-testing-expert/SKILL.md` | main `cd9c1884` | J9 |
| fast-check commit log (`fd17f486`, `33342651`); npm `fast-check` dist-tags | GitHub API, npm | J1 |
| react-testing-library `src/index.js`, `src/pure.js` (MIT) | `20ce75f2907ca0e5c5a8ae595c0e9a4e368c7800` | J4 |
| testing-library-docs `react-testing-library/api.mdx`, `user-event/intro.mdx`, `user-event/options.mdx`, `dom-testing-library/api-events.mdx`, `dom-testing-library/api-async.mdx`, `queries/about.mdx` | `7c49d046b100e657c64bae78270a5813c1c02eb6` | J4, J5 |
| vitest `docs/config/globals.md` | `3a76b87324ecb8d25509cd009aa87fbe56819c39` | J4 |
| react.dev `act.md` | per F9, `7594a2b0` | J4 |
| playwright `docs/src/{browser-contexts, test-assertions-js, actionability, aria-snapshots, locators, test-timeouts-js}.md`, `docs/src/api/{class-locator, class-browser}.md` (Apache-2.0) | `95e5dca31981bcd0970165853fcc713269d2433a` | J6 |
| `emarteca/nessie` README, repo metadata | `7875cb576ba4ec1ecf23c6ac4ff8f4cdeee7dcf7` | J8 |
| Zenodo record 5874851 (Nessie artifact) | record metadata | J8 |
| `sola-da/LambdaTester` README, repo metadata | `f993f9d67eab0120b14111be1a56d40b4c5ac9af` | J8 |
| Arteca et al. 2022, Nessie, ICSE (paper notes) | pp.1494-1504 | J7, J8 |
| Selakovic et al. 2018, LambdaTester, OOPSLA (paper notes) | p.14 (availability) | J8 |

## Unverified or open

- The J7 call-tree sketch has not been executed; `fc.letrec` + `fc.array({ depthIdentifier })` shrinking behavior on such trees is taken from the docs, not observed.
- `fc.beforeEach` runs "before each execution of the predicate" per its doc comment; I did not trace the runner to confirm that shrink-phase executions go through the same hook (the doc wording implies they do).
- Nessie and LambdaTester were not installed or run; whether either works on current Node is unknown.
- Whether user-event 14 already wraps its interactions in React `act` (through DOM Testing Library configuration) was not read in source; the todolist example wraps user-event calls in an explicit `act`. Whether the outer `act` is redundant or required is not established.
- Playwright inside fast-check: no primary example exists (J3); the per-run context advice is inference from the per-test context docs.
- Promise-returning API nesting (`.then` children) is my extension; the Nessie paper does not cover it.
- The two fast-check blog posts that mention testing-library (3.13.0, 4.6.0) were not read.
- Vitest's own `cleanup` integration options (e.g. `vitest-browser-react`) were not examined.
