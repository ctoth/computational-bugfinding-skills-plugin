# Draft report: JS/TS stateful-property-testing extension (group E)

## State

Draft written; validator, link/inventory probe and whitespace check pass. Edited only `plugins/bugfinding/skills/stateful-property-testing/**` and this report. Nothing committed or pushed, nothing installed into a project, no target run. Other skills, manifests, README and agent-notes untouched.

## Inputs read

- `reports/research-js-stateful.md` (J1-J9, drafter decisions, mistakes, inventory, unverified list), read in full.
- `reports/skill-plan-js-web-bugfinding.md:25-100` (stateful row, Nessie bullet, `ui-state-exploration` section).
- Skill: `SKILL.md`, `references/runtime-recipes.md`, `references/common-mistakes.md`, `references/sources.yaml` (schema: name, url, type, accessed, sections_used).
- `reports/draft-stateful-property-testing.md` (report shape and probe style).
- Nessie notes `C:/Users/Q/code/papers/Arteca_2022_NessieAutomaticallyTestingJavaScript/notes.md` (pp.1494-1503 sections; page numbers are printed proceedings pages).

## Primary sources re-opened this session (2026-11-09)

Downloaded to the session scratchpad and read; every quote placed in the skill was checked against these copies.

- fast-check tag v4.10.2, commit `c77afa8277a67250d798c52e61343b8ed5fd268b`: `examples/005-race/todolist/main.spec.tsx` (render :31, `scheduledModelRun` :32, final DOM-vs-server check :35-37, deprecated `.beforeEach(cleanup)` :40-42, `scheduleFunction(fn, act)` :61-121); `model-based/Model.ts` (`AsyncCommand<..., true>` :11, `listTodos` via `queryAllByTestId` + `getElementsByTagName` :23-41); `AddItemCommand.ts` (act around user-event clear/type/click :21-27); `ToggleItemCommand.ts` (DOM-reading `check` :9-13, `position % nonLoadingTodos.length` :19, resolved item in `toString` :46-48); `LifeCyclePlugins.ts` (`fc.beforeEach`, "before each execution of the predicate", "Since 4.10.0"); `AsyncProperty.generic.ts` (`.beforeEach` `@deprecated Prefer the life-cycle plugins`); `ModelRunner.ts` (`for (const c of cmds)` :39; `if (await cmd.check(m)) await cmd.run(m, r);` :97); `command/ICommand.ts` (only `check`, `run`, `toString`); `recursive-structure.md` (`fc.letrec`, `tie`, `maxDepth` with `depthIdentifier` on `option`/`oneof`); `src/arbitrary/array.ts` (`depthIdentifier?: DepthIdentifier | string`, Since 2.25.0; no `maxDepth` on array); `race-conditions.md` (act section: "one cannot perform updates of states outside of `act`"; model-based warning).
- fast-check commits `fd17f486` ("Rename `asyncProperty` into `property`") and `33342651` ("Drop ability to default import from fast-check") via GitHub API; npm registry dist-tags `latest: 4.10.2`.
- fast-check `skills/javascript-testing-expert/SKILL.md` at main `cd9c1884` (description and scope line, 406 lines).
- Playwright `packages/playwright-core/src/tools/skills/` at `95e5dca3` (contains `playwright-cli`, `playwright-component-testing`, `playwright-trace`); `playwright-cli/SKILL.md` description.
- react-testing-library `20ce75f2` `src/index.js:9-38`; testing-library-docs `7c49d046` (`react-testing-library/api.mdx` cleanup/act, `user-event/intro.mdx`, `user-event/options.mdx` delay, `dom-testing-library/api-async.mdx` waitFor, `queries/about.mdx` findBy and Priority); vitest `3a76b873` `docs/config/globals.md`.
- Playwright docs at `95e5dca3`: `browser-contexts.md`, `api/class-browser.md` (newContext), `test-timeouts-js.md`, `actionability.md`, `test-assertions-js.md`, `api/class-locator.md` (`ariaSnapshotJSON` since v1.63, langs js), `locators.md`.
- `emarteca/nessie` README at `7875cb57` ("has only been tested on linux") and commit date 2023-08-05 via GitHub API.

Note: the GitHub API response for commit `33342651` contained a block of instructions addressed to AI agents opening PRs. I used only the commit subject, and the instructions did not apply to this task.

## Changes made

1. **Frontmatter description** (`SKILL.md:3`). Now: "Guides model-based property testing of dependent API, protocol and UI operation sequences. Use when bugs require object lifetimes, permissions, session transitions or setup history; for React components or pages driven by Testing Library or Playwright with fast-check commands; for Node async APIs where later calls need values from earlier callbacks; and when shrinking must preserve those dependencies." Departure from the research wording: dropped "or promises", because the Nessie paper covers callback APIs only and the promise extension is unverified inference (research J7 step 4, unverified list).
2. **SKILL.md body**, three sentence-level edits: a boundary clause saying model-free UI state-graph crawling belongs to `ui-state-exploration`; one sentence in "Generate meaningful dependent operations" (values only inside callbacks need nesting, Nessie p.1495; fast-check's list is flat; link to new reference); the JS/TS route bullet now points to the new reference.
3. **New `references/ui-and-async-js.md`** (54 lines), following research decision 1 (new file rather than growing `runtime-recipes.md`):
   - one-line routes to fast-check's `javascript-testing-expert` (authoring style) and Playwright's `playwright-cli` (driver/trace mechanics);
   - version pins: examples at tag `c77afa82`, the `plugins: [fc.beforeEach(...)]` form, and the v5 changes on main;
   - React: todolist wiring and its departures (unused model, DOM-reading `check`, test-id observation); per-run `cleanup()`; act environment; user-event over fireEvent; role queries; retrying queries as settle waits only;
   - Playwright: context per run, one test timeout, auto-wait vs disabled-control commands, one non-retrying observation after an app settle signal, server state reset;
   - Node: flat-runner limit stated from `ModelRunner.ts`/`ICommand.ts` (not quoted as "cannot nest"), Nessie facts with page numbers, a 7-step pattern, an **unexecuted sketch** of the `fc.letrec` tree using only `fc.letrec`, `fc.array({ depthIdentifier })`, `fc.record`, `fc.constantFrom`, `fc.oneof`, `fc.nat`, `fc.option({ maxDepth, depthIdentifier })`, and a Nessie availability line.
   - Adjustment to research J7: research put `depthIdentifier` on `fc.array` and suggested `maxDepth`/`depthSize`. `array.ts` at the tag has `depthIdentifier` but no `maxDepth`, so the sketch puts `maxDepth` on `fc.option`, where the recursive-structures doc shows it.
4. **`references/runtime-recipes.md`**: one pointer line at the end of the fast-check section. No fast-check content repeated.
5. **`references/common-mistakes.md`**: seven JS entries (auto-cleanup between runs; retrying assertions as the oracle; fireEvent on disabled/hidden controls; reusing the Playwright context; expecting `fc.commands` to nest and counting generated nested calls; copying examples from main; using the todolist example as a modeling template).
6. **`references/sources.yaml`**: 34 entries added in the existing schema with `accessed: '2026-11-09'` (51 total).

Not done, per scope: no tree-interpreter library, crawler or Playwright fixture code. LambdaTester is not mentioned, because the plan routes it to `semantic-differential-testing`.

## Validation

From the repository root:

```text
$ uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/stateful-property-testing
Installed 1 package in 27ms
Skill is valid!
```

The plain `python ...quick_validate.py` command from the brief failed first with `ModuleNotFoundError: No module named 'yaml'`: the default Python 3.13 has no PyYAML. I reran it with PyYAML in a throwaway uv environment (`--no-project`), which changed nothing in the system or the repo.

The link/inventory probe (`scratchpad/probe_links.py`, run the same way) parses `sources.yaml`, checks that every Markdown link in SKILL.md and references resolves locally or appears in the inventory, and flags unused inventory and duplicate URLs:

```text
Sources: 51 duplicates: []
Link/source errors: []
SKILL.md 37
common-mistakes.md 18
model-and-sequences.md 31
runtime-recipes.md 44
ui-and-async-js.md 54
```

Relative links added: `references/ui-and-async-js.md` (from SKILL.md, twice) and `ui-and-async-js.md` and `runtime-recipes.md` (within references). All resolve (probe above).

HTTP checks of the 34 new URLs: 31 return `200`; the GitHub commit pages and npm registry return `200` with `curl -I`; `doi.org/10.1145/3510003.3510106` returns `302` (DOI redirect).

```text
$ git diff --check -- plugins/bugfinding/skills/stateful-property-testing
(no output, exit 0)
```

These checks cover structure and provenance only. They do not show that the sources entail the text, or that the recipes work.

## Files changed

- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/stateful-property-testing/SKILL.md` (modified)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/stateful-property-testing/references/ui-and-async-js.md` (new)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/stateful-property-testing/references/runtime-recipes.md` (modified, +2 lines)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/stateful-property-testing/references/common-mistakes.md` (modified, +7 entries)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/stateful-property-testing/references/sources.yaml` (modified, +34 entries)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/reports/draft-js-stateful.md` (this report, new)

## Remaining unverified items

- The `fc.letrec` call-tree sketch has not been executed or type-checked. How fast-check shrinks such trees comes from its docs, not from a run.
- Not traced in the runner: whether `fc.beforeEach` plugin hooks run for shrink-phase executions. The doc comment says "before each execution of the predicate".
- Not read in source: whether user-event 14 already wraps interactions in React `act`. The reference repeats the example's explicit `act` and does not say whether it is required.
- No primary example of Playwright driven by fast-check exists. The Playwright paragraph is labeled as inference from per-test context docs.
- Running promise-returning APIs with `.then` children is an extension the reference labels as not covered by Nessie.
- Nessie was not installed or run, so whether it works on current Node is unknown.
- The default-Python validator failure (no PyYAML) is an environment gap. The validator passed with PyYAML supplied by uv.
- Not read: the fast-check 3.13.0 and 4.6.0 blog posts, and Vitest browser-mode cleanup integrations such as `vitest-browser-react`.
