# Improve pass: JS/TS additions to stateful-property-testing (commit 3965efe)

Scope: every sentence added under `plugins/` in 3965efe, checked against the cited pinned sources.

## Findings

Accessed 2026-11-09. Sources fetched raw at the pinned commits in the text. Tag check: `gh api repos/dubzzz/fast-check/git/tags/5da531a1…` -> v4.10.2 object `c77afa8277a67250d798c52e61343b8ed5fd268b` (matches). npm dist-tags `latest: 4.10.2`. Commits fd17f486 ("💥 Rename `asyncProperty` into `property` (#7412)") and 33342651 ("💥 Drop ability to default import from fast-check (#7307)") are on `main` and not ancestors of v4.10.2 (`compare v4.10.2...<sha>` = diverged). Nessie commit 7875cb57 author/committer date 2023-08-05T17:27:21Z (matches).

### F1 references/common-mistakes.md:12 and references/ui-and-async-js.md:15 — WARNING (stronger than source)
- Said: RTL registers cleanup in `afterEach` "only `if (typeof afterEach === 'function')`".
- Source: https://raw.githubusercontent.com/testing-library/react-testing-library/20ce75f2907ca0e5c5a8ae595c0e9a4e368c7800/src/index.js lines 12-22: `if (typeof afterEach === 'function') { afterEach(() => { cleanup() }) } else if (typeof teardown === 'function') { teardown(() => { cleanup() }) }`. "only" omits the `teardown` fallback.
- Fix: added "else a global `teardown` if one exists" in both places.

### F2 SKILL.md:18, references/ui-and-async-js.md:29, references/sources.yaml:324 — ERROR (stronger than source)
- Said: SKILL.md "Values that exist only inside a callback, such as file handles, need a call nested in that callback (Nessie, ICSE 2022, p.1495)"; ui-and-async-js.md "Some values, such as file handles, exist only inside a callback"; sources.yaml "p.1495 values available only inside callbacks".
- Source: Nessie p.1495 (page image `C:/Users/Q/code/papers/Arteca_2022_NessieAutomaticallyTestingJavaScript/pngs/page-001.png`, consistent with notes.md line 19): "Since file-handle objects are created inside the library ... While it is possible for a test generator to create suitable file-handle objects using a purely random approach, the chances of successfully creating a valid file-handle would be small. Therefore, the most effective way to obtain a valid file-handle and expose the bug is to invoke `exists` with some callback function f, and invoke `read` with the file-handle that is passed to f". The paper says nesting is the most effective way, not required, and that handles are created inside the library, not that they exist only inside a callback.
- Fix: SKILL.md -> "Values a library creates and passes to a callback, such as file handles, are most effectively reached by a call nested in that callback"; ui-and-async-js.md -> "are created inside the library and handed to a callback, so random construction rarely yields a valid one"; sources.yaml section label updated to match.

## Checked and entailed (no change)

- fast-check todolist (c77afa82): `render` inside predicate, `fc.scheduledModelRun(s, () => ({ model: { todos: [], wrapper }, real: {} }), commands)`, every mocked API `s.scheduleFunction(fn, act)`, final DOM vs `expectedTodos()` comparison, `.beforeEach(async () => { await cleanup(); })` (main.spec.tsx). AddItemCommand wraps user-event in `act`, compares before/after, calls direct `userEvent.*` (no `setup()`). ToggleItemCommand `check` calls `listTodos()` (DOM), `run` uses `this.position % nonLoadingTodos.length`, `toString` prints `runDetails`. No command (Add/Toggle/Remove) writes to `m`. Model.ts uses `screen.queryAllByTestId('todo-item')` and `getElementsByTagName`.
- LifeCyclePlugins.ts:191-196 "Hook to be executed before each execution of the predicate", "@remarks Since 4.10.0"; `beforeEach` exported from fast-check-default.ts:465; Parameters.ts:253 `plugins?: Plugin<T>[]`; AsyncProperty.generic.ts:44 `@deprecated Prefer the life-cycle plugins: \`fc.assert(property, { plugins: [fc.beforeEach(fn)] })\``.
- ModelRunner.ts (c77afa82): line 39 `for (const c of cmds)`, line 97 `if (await cmd.check(m)) await cmd.run(m, r);`, `genericModelRun` / `internalAsyncModelRun` names exist. ICommand.ts exposes only `check`, `run`, `toString`.
- race-conditions.md line 259 "when testing React applications, one cannot perform updates of states outside of `act`" under "Wrapping calls automatically using `act`"; line 310 "Neither `check` nor `run` should rely on the completion of other scheduled tasks" under "Model based testing and race conditions".
- fc.letrec sketch API names at c77afa82: `letrec(builder)` with `tie(key)`; `option` constraints `maxDepth`, `depthIdentifier` (option.ts:39,48); `oneof` constraints `maxDepth`, `depthIdentifier` (oneof.ts:78,87); `array` constraint `depthIdentifier` (array.ts:51); `constantFrom`, `record`, `nat` exported. All exist. Not executed.
- recursive-structure.md: `maxDepth` + `depthIdentifier` with `option`/`oneof`, `fc.array(tie('node'), { depthIdentifier: 'node' })`.
- RTL api.mdx `cleanup`: "could result in a memory leak and tests which are not "idempotent"". RTL index.js beforeAll/afterAll guard for act environment.
- Vitest globals.md: Default `false`; tip "some libraries, e.g., `@testing-library/react`, rely on globals being present to perform auto cleanup".
- user-event intro.mdx: both quotes exact; `fireEvent` for not-yet-implemented interactions; recommends `userEvent.setup()` before rendering. options.mdx delay: "to the next macro task and allows other (asynchronous) code to run between events", default `0` (setTimeout still called; `null` prevents it).
- queries/about.mdx Priority: "should be your top preference for just about everything". api-async.mdx: "`waitFor` may run the callback a number of times until the timeout is reached", default timeout 1000ms, `findBy` = `getBy` + `waitFor`.
- Playwright (95e5dca): browser-contexts.md "Playwright creates a context for each test"; class-browser.md newContext "It won't share cookies/cache with other browser contexts", recommends `BrowserContext.close`; test-timeouts-js.md "30 seconds by default"; actionability.md click checks Visible/Stable/Receives Events/Enabled/Not Inert, `TimeoutError`; test-assertions-js.md "retry until the assertion passes, or the assertion timeout is reached", default 5 seconds; class-locator.md `Locator.ariaSnapshotJSON` "since: v1.63", "langs: js" (npm `playwright` latest 1.65.0, so released); locators.md recommends prioritizing `getByRole`.
- javascript-testing-expert SKILL.md line 6 "Testing functions and components, not black-box e2e"; has "File and code layout", arbitrary-constraint rules and `@fast-check/vitest`. playwright-cli SKILL.md covers browser automation and `tracing-start`/`tracing-stop`.
- package.json at c77afa82: version 4.10.2, MIT. Nessie README line 10 "`nessie` has only been tested on linux".
- Nessie notes (pp.1496, 1497 Defs. 2-3, 1498, 1501, 1502): one callback per probe misses multi-callback signatures; tree argument kinds; extension points only at executed callbacks and not after API exceptions (page image page-004.png confirms "code that will never execute"); difference kind "callback called in one commit only"; 10 runs per commit with set comparison; every inspected difference could in principle be exposed without nesting.

## Validation (after fixes)

- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/stateful-property-testing` -> `Skill is valid!` (exit 0).
- Relative links and URL/sources.yaml match (Python over the 5 .md files and sources.yaml): `md files 5 cited urls 51 yaml urls 51`, `broken rel links []`, `cited not in yaml []`, `yaml not cited []`.
- `git diff --check -- plugins/bugfinding/skills/stateful-property-testing` -> no output, exit 0.
- Not committed, not pushed.
