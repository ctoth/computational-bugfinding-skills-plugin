# Research: JS/TS differential testing (group F)

Skills: `semantic-differential-testing`, `configuration-differential-testing`.
Branch: js-web-bugfinding. Researcher: Phase 3 group F.

Status: complete. Nothing here was executed against a target; every "inference" or "proposed" label marks a claim not stated by the cited source.

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md:34-35` (skill rows), `:71-78` (LambdaTester bullet, tool-availability note).
- `reports/skill-research-js-web-bugfinding.md:26-46` (F1 Jazzer.js), `:149-169` (F9 React), `:171-183` (F10 Playwright/Puppeteer).
- `plugins/bugfinding/skills/semantic-differential-testing/SKILL.md` and all four references; `plugins/bugfinding/skills/configuration-differential-testing/SKILL.md` and all four references. Both are currently database/compiler-only (SQLancer, SQLite, PostgreSQL, Csmith, LLVM, PICT, Kuhn); no JS content.
- Paper notes: `C:/Users/Q/code/papers/Selakovic_2018_TestGenerationHigherOrderFunctions/notes.md`, `C:/Users/Q/code/papers/Arteca_2022_NessieAutomaticallyTestingJavaScript/notes.md`.
- Evidence standard: `reports/research-semantic-differential-testing.md:1-40` and `reports/research-configuration-differential-testing.md:1-30` (skimmed for format: pinned source URL, quoted fragment, line numbers, explicit "Decision:" per source, no effectiveness counts adopted). This report follows that standard; the rest of those two files was not read.

## Pins used (HEAD or latest release on 2026-11-09, via `gh api`)

| Source | Pin |
|---|---|
| reactjs/react.dev | `7594a2b008489121bdf25f97320d11ac0422510e` (same as F9) |
| facebook/react | tag `v19.3.1` = `61aa00df822d0eb76d0362eb8b6fdd3527693efe` (latest release, 2026-10-14) |
| vercel/next.js | `cb4cc5b123ff918e2ab89a6a2c865b0b2d930f40` (`errors/react-hydration-error.mdx`) |
| nodejs/Release | `6065a837c0c151577f449c666fec019069ffba77` (`README.md`, `schedule.json`) |
| nodejs/node docs | tag `v26.13.0` = `daaa22aeddb87085542376ea1f4854dcea080baf` (latest LTS release, 2026-10-28) |
| microsoft/playwright | `95e5dca31981bcd0970165853fcc713269d2433a` (same as F10) |
| CodeIntelligenceTesting/jazzer.js | `f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1` (same as F1) |
| mdn/content | `0a6ff1e3b8887f979b66c34cefdb73f846041879` |
| tc39/ecma262 | `828d35d00f8584c4a0fbcac7742b57c7b959c3f3` (`spec.html`) |

## Findings

### P1. LambdaTester execution summary (from paper notes; page numbers are the notes')

- Def 4.1 execution summary: receiver-object state and return values; state of arguments passed to callbacks, serialized at every callback invocation; number of callback invocations; stdout; stderr (Selakovic notes line 89, p.13).
- Serialization: primitives as values; non-constructor objects (arrays) via JSON; constructor-created objects (promises) recorded only by constructor name "because internal representation varies across polyfills" (notes line 90, p.13). The notes' Limitations: internal-state differences in such objects are invisible to the oracle (line 178, p.13).
- Streams differ only if one is empty and the other non-empty, because message text varies (line 91, p.13). Warning-message differences were treated as benign and excluded (line 93, p.16); many error-message differences "can likely be considered as false positives" (line 170, p.16).
- Reference: native output is ground truth; the design is polyfill-vs-native, not version-vs-version (line 88, p.13; line 175). Applying it across library versions is an adaptation the paper did not evaluate (line 210).
- Which callbacks matter: Base (no callbacks) found 0 differences in all 13 libraries; Cb-Writes found differences in 12/13 (lines 198-199, p.16). The polyfill.io `find` bug changes only callback invocation count (1 vs 3) while both return `undefined`, so only the invocation-count oracle detects it (line 151, pp.19-20).
- Tool: github.com/sola-da/LambdaTester, built on Jalangi, evaluated on Node.js 8.5 (lines 206-207). Nessie re-implemented it because the original "lacks ES6+ support and was benchmark-specific" (Selakovic notes line 247, citing Nessie pp.1494-1495, 1499). GitHub API (2026-11-09): `sola-da/LambdaTester` MIT, not archived, last push 2018-09-27.
- Inference for the drafter: native-as-ground-truth is a property of the polyfill setting (a polyfill's contract is "behave like native"). It does not contradict the skill's "majority output is not ground truth" (`semantic-differential-testing/SKILL.md:30`), but the text must say a reference stands in for the specification only when the other side's contract is defined as "match the reference".

### P2. Nessie cross-commit differential (from paper notes)

- 100 tests generated on the earlier commit, run on both commits under mocha (Arteca notes line 202, p.1501).
- Logged: all API argument values before and after each call; the API function a callback was passed to and all callback parameter values when it runs; return value of successful calls; API function name on failure (line 203).
- Difference kinds: error vs success; different return value; different argument or callback parameter; callback called in one commit only; mocha internal async error in one commit only (line 204).
- Nondeterminism: each test run 10 times per commit; compare sets of observed outputs; report only an output seen in one commit and never in the other (line 207, p.1501).
- Non-functional differences (renames, supported Node.js version change, `strict` migration syntax errors) were manually identified and configured to be ignored (line 205). Equivalence: same kind from same API function counted once (line 206); approximate (line 244, p.1503).
- Results were classified Bug / Bug fix / Upgrade (line 210, p.1502): a cross-commit difference is not automatically a bug; intended upgrades produce differences.
- Artifact: zenodo.org/record/5874851 (line 279, pp.1494, 1504). Zenodo API (2026-11-09): title "[Artifact] Nessie: ...", published 2021-11-09, CC-BY-4.0, one file `ExperimentalData.tgz`; its description says it includes setup instructions for the tool and that reruns "will not be exactly the same as those in the paper" because Nessie uses a random number generator. GitHub API: `emarteca/nessie` MIT, not archived, last push 2023-08-05 (that this repo is the paper's tool is inferred from owner and name; not confirmed from the paper). Evaluated on Node.js 14.16.1 (notes line 199, p.1503).

### R1. React hydration contract (react.dev `7594a2b`, `src/content/reference/react-dom/client/hydrateRoot.md`)

- Root options (lines 44-46): `onCaughtError` "called when React catches an error in an Error Boundary"; `onUncaughtError` "called when an error is thrown and not caught by an Error Boundary"; `onRecoverableError` "called when React automatically recovers from errors ... Some recoverable errors may include the original error cause as `error.cause`." Line 47: `identifierPrefix` for `useId` "Must be the same prefix as used on the server."
- Caveats (lines 57-58): content must be "identical with the server-rendered content. You should treat mismatches as bugs"; "In development mode, React warns about mismatches during hydration. There are no guarantees that attribute differences will be patched up".
- Line 87: calling `root.render` before hydration finishes makes React "clear the existing server-rendered HTML content and switch the entire root to client rendering."
- Pitfall (lines 188-199): common causes are extra whitespace around the root's HTML, `typeof window !== 'undefined'` checks, browser-only APIs like `window.matchMedia`, and "Rendering different data on the server and the client"; worst case "event handlers can get attached to the wrong elements."
- `suppressHydrationWarning` (lines 238-274): for "a single element's attribute or text content" that is unavoidably different (e.g. timestamp); "only works one level deep ... escape hatch ... React will **not** attempt to patch mismatched text content." `reference/react-dom/components/common.md:37` adds: React "will not warn you about mismatches in the attributes and the content of that element."
- Intended difference (lines 280-325): two-pass render via an `isClient` state set in an Effect keeps the first client render equal to the server. Line 278 is a TODO comment and line 327 names `use(browser())`; the TODO says "Remove this subsection when browser is available in Stable", so `browser()` is not in the stable release (inference from the TODO; React's exports not checked).
- Error logging (lines 385-456): "By default, React will log all errors to the console"; the sample passes all three handlers to `hydrateRoot`.

### R2. What React 19.3.1 actually reports, production vs development (facebook/react `61aa00df`)

All line numbers below are in the pinned files.

- `packages/react-reconciler/src/ReactFiberHydrationContext.js:388-416` `throwOnHydrationMismatch`: builds `Error("Hydration failed because the server rendered ${text|HTML} didn't match the client. As a result this tree will be regenerated on the client. ...")`, queues it with `queueHydrationError` and throws an internal `HydrationMismatchException`. Only the appended diff is `__DEV__`-gated (lines 390-398); the error itself is created in production too. The message lists `typeof window` branches, "`Date.now()` or `Math.random()`", "Date formatting in a user's locale which doesn't match the server", external data without a snapshot, invalid tag nesting, and browser extensions (lines 400-411).
- Callers in production paths: no next hydratable node or `tryHydrateInstance` fails (lines 475-483), text node claim fails (497-503), activity/suspense instance missing (511-527), form-state marker missing (554), `hydrateInstance` returns false (578-580), `hydrateTextInstance` returns false (649-651).
- `ReactFiberHydrationContext.js:907-919` `upgradeHydrationErrorsToRecoverable`: after "a forced client render" succeeds, the queued hydration errors go to `queueRecoverableErrors`, i.e. they reach `onRecoverableError`.
- What production compares on elements: `packages/react-dom-bindings/src/client/ReactDOMComponent.js:3152-3312` `hydrateProperties` returns false only when string/number/bigint `children` differ from `domElement.textContent` (lines 3272-3285), unless `suppressHydrationWarning === true`. It does not compare attributes; the comment at 3265-3269 says "Our requirement is not to produce perfect HTML and attributes."
- Text nodes: `ReactDOMComponent.js:3384-3398` `hydrateText` returns false when `nodeValue !== text`, the parent lacks `suppressHydrationWarning`, and the normalized strings differ. `checkForUnmatchedText` (363-373) compares after `normalizeMarkupForTextOrAttribute` (newline normalization and null/replacement-char removal, 356-360).
- Attribute mismatches are development-only console output: `emitPendingHydrationWarnings` (`ReactFiberHydrationContext.js:933-969`) is wrapped in `if (__DEV__)` and calls `console.error("A tree hydrated but some attributes of the server rendered HTML didn't match the client properties. This won't be patched up. ...")`. It does not call `onRecoverableError`.
- Production message text: `scripts/error-codes/codes.json` maps code 418 to the "Hydration failed ..." message, 422 to "... recover by instead client rendering from the nearest Suspense boundary.", 423 to "... client rendering the entire root.", 424 to the early-update case, 421 to a Suspense boundary updated before it finished hydrating. `packages/shared/formatProdErrorMessage.js` produces "Minified React error #<code>; visit https://react.dev/errors/<code>?args[]=... for the full message". react.dev `src/content/errors/index.md:3`: "In the minified production build of React, we avoid sending down full error messages". So in production `onRecoverableError` receives an error whose message is the minified code plus args (`text` or `HTML` for 418).
- Defaults: `packages/react-reconciler/src/ReactFiberErrorLogger.js:123-128` `defaultOnRecoverableError` calls `reportGlobalError(error)`. `packages/react-dom/src/client/ReactDOMRoot.js:184-186` defaults the three handlers.

Consequences for the oracle (inference from the code above, not executed):

1. Production `onRecoverableError` sees text and structure mismatches but never attribute-only mismatches. A differential that must catch attribute mismatches has to compare server HTML against a client render itself (R4), or run a development build and capture `console.error`.
2. `suppressHydrationWarning` on the parent disables the production text check for that element's own text, so no recoverable error fires and the server text stays (hydrateRoot.md:274 "will not attempt to patch").
3. In production compare on error code (418/421/422/423/424), not message text.
4. `onCaughtError`/`onUncaughtError` are about render errors and error boundaries, not hydration mismatches; a server/client difference that throws on the client (e.g. a client-only API read in render) reaches them, a plain content difference does not (from the option definitions at hydrateRoot.md:44-46 and the code paths above).

### R3. Server render APIs: what the "server side" of the pair is

- `renderToString` (`reference/react-dom/server/renderToString.md`): "does not support streaming or waiting for data" (line 7); "If a component suspends, `renderToString` immediately sends its fallback as HTML" (line 54; detail at 149-151). Its `identifierPrefix` "Must be the same prefix as passed to `hydrateRoot`" (line 46).
- `renderToPipeableStream` (`.../renderToPipeableStream.md`): `onAllReady` fires "when all rendering is complete, including both the shell and all additional content" and is for "crawlers and static generation"; "The stream will contain the final HTML" (line 61). `onShellReady` streams before nested Suspense content finishes (lines 65, 344). `onError` fires for every server error, recoverable or not (line 63). When a server error inside a Suspense boundary is retried successfully on the client, "the server `onError` callback and the client `onRecoverableError` callbacks will fire" (line 437).
- `prerender` (`reference/react-dom/static/prerender.md`): Web Streams API, returns `{prelude, postponed}` (line 10); "Unlike `renderToString`, `prerender` waits for all data to load before resolving" (line 82); Node should use `prerenderToNodeStream` (line 19).
- Consequence for the drafter: the server artifact to save is the full HTML after `onAllReady` / `prerender` resolution, or the `renderToString` string; an `onShellReady` capture is an incomplete observation. A server `onError` paired with a client `onRecoverableError` is a server failure recovered on the client, not a content mismatch; keep the two outcomes distinct.

### R4. Comparing server HTML with the client's first render directly

- `useId` (`reference/react/useId.md:174`): "**`useId` requires an identical component tree on the server and the client**. If the trees you render on the server and the client don't match exactly, the generated IDs won't match." Line 188: IDs come from the "parent path". Lines 312-338: `identifierPrefix` must match between server API and `hydrateRoot` when multiple apps share a page.
- `useSyncExternalStore` (`reference/react/useSyncExternalStore.md:48`): `getServerSnapshot` "will be used only during server rendering and during hydration of server-rendered content on the client. The server snapshot must be the same between the client and the server". Line 368: "returns the same exact data on the initial client render as it returned on the server".
- `renderToString.md:127-141` documents the browser route `createRoot` + `flushSync` + `div.innerHTML`. `reference/react-dom/flushSync.md:56`: "`flushSync` may run pending Effects and synchronously apply any updates they contain before returning." Consequence (inference): a `createRoot`+`flushSync` render is not the hydration first render. It uses `getSnapshot` instead of `getServerSnapshot` (useSyncExternalStore.md:48), and it may already include the `isClient` second pass that hydrateRoot.md:280-325 documents as a legal intended difference. Comparing that output to server HTML produces false alarms for correct code.
- `react-dom` 19.3.1 `package.json` `exports["./server"]` resolves `"browser"` and `"worker"` conditions to `./server.browser.js` (fetched at the pinned tag). So `renderToString` can run inside the real browser page. renderToString.md:127 discourages it in shipped client code for bundle size only.
- Proposed direct comparator (this report's design, not executed, not documented by React as a mismatch detector): run the same component with the same props and serialized server data through `renderToString` twice, once in the server process and once inside the browser page (Playwright), then compare the two strings. Both sides use the same renderer, no Effects run, and `getServerSnapshot` is used on both sides; only environment differs (time, `Intl` locale/time zone, `typeof window`, `matchMedia`, `Math.random`). This catches attribute differences that production `onRecoverableError` cannot. It does not observe parser normalization, browser extensions or intermediaries (R5), so keep the real `hydrateRoot` run with `onRecoverableError` as the second observation.
- Raw-DOM comparison caveat: SSR emits `<!-- -->` separators between adjacent text nodes (example at hydrateRoot.md:251, `Current Date: <!-- -->01/01/2020`), so a server-HTML vs client `innerHTML` byte comparison differs for correct code unless those markers are accounted for. Comparing `renderToString` with `renderToString` avoids this.

### R5. Next.js hydration error page (next.js `cb4cc5b`, `errors/react-hydration-error.mdx`)

- No contract beyond react.dev. It defines the error as a difference "between the React tree that was prerendered from the server and the React tree that was rendered during the first render in the browser (hydration)".
- It adds causes outside application code: invalid HTML nesting (`<p>` in `<p>`, `<div>` in `<p>`, nested interactive content), browser extensions modifying HTML, misconfigured CSS-in-JS, an Edge/CDN rewriting the HTML (Cloudflare Auto Minify), and iOS format detection turning phone numbers/emails into links (fix: `<meta name="format-detection" content="telephone=no, date=no, email=no, address=no">`).
- Use for adjudication only: a mismatch seen in a real browser but not in the renderToString-vs-renderToString pair points at parsing, intermediaries or the browser, not at render-phase nondeterminism (inference).
- Decision: do not cite Next.js in the skill unless the drafter wants the CDN/iOS causes; React's own 418 message already lists nesting and extensions.

### R6. Nondeterminism sources and their documented controls

| Source | Documented as a cause | Documented control |
|---|---|---|
| Time (`Date.now()`, `new Date()`) | React 418 message (`ReactFiberHydrationContext.js:404`); Next page cause 4 | Render from a timestamp passed as data; `suppressHydrationWarning` only for unavoidable single-element cases (hydrateRoot.md:240) |
| Locale / `Intl` | React 418 message line 405 ("Date formatting in a user's locale") | MDN `Intl/DateTimeFormat/DateTimeFormat/index.md:55`: default locale is "the runtime's default locale"; `:83` default `timeZone` "is the runtime's time zone". Pass explicit `locales`/`timeZone`. |
| Time zone (server) | as above | Node `doc/api/cli.md:4664-4668`: `TZ` env var sets the zone, supports IANA IDs like `'Etc/UTC'` |
| Time zone / locale (browser) | as above | Playwright `docs/src/emulation.md:311-334` `locale`, `timezoneId`; `:383` "this only affects the browser timezone and locale, not the test runner timezone" |
| ICU data | not a React cause | Node `doc/api/intl.md:28,42`: full ICU is the default build; `small-icu`/`system-icu` builds differ (`:73-106`). Record `process.versions.icu` (inference: field name not checked in docs) |
| `Math.random()` | React 418 message line 404 | Seed or pass the value as data |
| `useId` | useId.md:174 | identical tree; same `identifierPrefix` (hydrateRoot.md:47, useId.md:312-338) |
| `typeof window`, `matchMedia` | hydrateRoot.md:195-196 | two-pass `isClient` (hydrateRoot.md:280-325); Playwright `colorScheme` / `emulateMedia` (emulation.md:587-589) |
| External store data | useSyncExternalStore.md:48, 368 | `getServerSnapshot` returning serialized server data |
| Whitespace, nesting, extensions, CDN, iOS | hydrateRoot.md:194; React 418 lines 407-409; Next page | Adjudication, not render control |

### N1. Node.js release lines (nodejs/Release `6065a83`)

- On 2026-11-09 (`README.md:5-15`): 22.x Jod Maintenance LTS, EOL 2027-04-30; 24.x Krypton Maintenance LTS since 2026-10-20, EOL 2028-04-30; 26.x Lithium Active LTS since 2026-10-28, EOL 2029-04-30; 27.x in Alpha since 2026-10-28, Current from 2027-04-22. "Dates are subject to change." `schedule.json`: 20.x ended 2026-04-30; 25.x ended 2026-06-01.
- Schedule change (`README.md:23-33`, `:123-147`): from Node 27, every line goes Alpha (6 months) then Current (6 months) then LTS for 30 months, and every line is promoted to LTS; lines up to 26 keep the old even/odd scheme (odd lines never LTS; 12 months Active then 18 months Maintenance).
- Latest releases (`gh api repos/nodejs/node/releases`): v26.13.0 and v24.22.2 (2026-10-28), v22.23.4 (2026-10-21), v27.0.0-alpha.0.0.0 (2026-10-29).
- Factor consequence: the Node-supported set on this date is {22, 24, 26}; 27 alpha is a pre-release lane. The target's `engines` field and CI matrix decide the target's own supported set; the skill must say to read those and must not hard-code this list (it changes every October under the new schedule).

### N2. ESM vs CJS loading differences (Node v26.13.0 docs)

- `doc/api/esm.md:583-627`: importing CJS from ESM gives `module.exports` as default; named exports come from a static analysis that "does not always correctly detect named exports" (625-626); "Live binding updates or new exports added to `module.exports` are not detected for these named exports" (622-623).
- `esm.md:633-682`: in ESM there is no `require`/`exports`/`module.exports`, no `__filename`/`__dirname`, no addon loading, no `require.main`, no `require.resolve`, no `NODE_PATH`, no `require.extensions`, and no `require.cache` ("the ES module loader has its own separate cache").
- `esm.md:705-710`: JSON import needs `with { type: 'json' }` and exposes only `default`.
- `doc/api/modules.md:313-317`: `require()` of an ES module whose graph has top-level `await` throws `ERR_REQUIRE_ASYNC_MODULE`.
- `doc/api/packages.md:715-722`: in `"exports"` key order is significant and "Using the `"import"` and `"require"` conditions can lead to some hazards" (the dual-package section at 946-948 now only links to an external examples repository, not read). `packages.md:789-795`: `--conditions=development` adds user conditions; `:831-836` `"development"` and `"production"` conditions "Must always be mutually exclusive".
- Factor consequence (inference from 681-682 and 720-722): ESM vs CJS is not a pure loader toggle. A package with `"import"`/`"require"` conditions can resolve to different files, and the separate caches mean one process can hold two instances of a module. Record the effective value as the resolved file path per run (`import.meta.resolve` / `require.resolve`, both named at esm.md:660-667).

### N3. Jazzer.js ESM instrumentation floor and Node 26 (F1 re-checked)

- `docs/fuzz-targets.md:112-119` (pin `f23bc5a`): ESM instrumented via "a Node.js loader hook (`module.register`)"; "Requirements: Node.js >= 20.6. Function hooks (bug detectors) additionally require Node.js >= 20.11 ... On older Node versions, ESM loading still works but modules are not instrumented."
- `packages/instrumentor/instrument.ts:330-400`: checks `nodeVersionAtLeast(20, 6)` and prints "WARN: [jazzer.js] ES module instrumentation requires Node.js >= 20.6" (336-339), "ES module function hooks require Node.js >= 20.11" (349-352), calls `register(loaderUrl, options)` (395) and on failure prints "WARN: [jazzer.js] Failed to register ESM loader hooks." (396-399).
- Node v26.13.0 `doc/api/module.md:179-204`: `module.register` is "Stability: 0 - Deprecated: Use `module.registerHooks()` instead." `doc/api/deprecations.md:4574-4597` DEP0205: runtime deprecation since v26.0.0; "will be removed in a future version of Node.js."
- GitHub code search for `registerHooks` in the Jazzer.js repo returned no results (index may lag; the pinned `instrument.ts` calls `register`).
- Factor consequence: every supported Node line (22, 24, 26) is above the 20.6/20.11 floor, so the floor gives no PICT constraint today. The live interaction is Node line x module format x Jazzer.js: on 26 the ESM path uses a runtime-deprecated API, and on a future Node that removes it Jazzer.js would print the "Failed to register" warning and run ESM uninstrumented (inference from 395-399; no such Node release exists yet). The effective-value evidence is the absence of those warnings plus coverage counters rising on ESM code.

### N4. Browser engines via Playwright projects (playwright `95e5dca`)

- `docs/src/test-projects-js.md:8`: "A project is logical group of tests running with the same configuration"; lines 14-60 configure `chromium`, `firefox`, `webkit` via `devices['Desktop Chrome' | 'Desktop Firefox' | 'Desktop Safari']`, plus mobile devices and branded channels. Line 67: "Playwright will run all projects by default"; line 86: `npx playwright test --project=firefox`.
- `docs/src/browsers.md:339`: Chromium-based projects use open-source Chromium builds that run ahead of branded Chrome/Edge; `:446` branded Stable/Beta channels can be selected; `:584` "Playwright's Firefox version matches the recent Firefox Stable build ... doesn't work with the branded version of Firefox since it relies on patches"; `:590` "Playwright's WebKit is derived from the latest WebKit main branch sources, often before these updates are incorporated into Apple Safari ... doesn't work with the branded version of Safari".
- Factor consequence: the Browser factor's values are Playwright's patched engines; a `webkit` result is not a Safari result and a `firefox` result is not branded-Firefox. Record the Playwright version and `browser.version()` per run as effective-value evidence (inference: `browser.version()` not checked in the pinned docs).

### N5. React development vs production builds and `NODE_ENV` (react `61aa00df`, react.dev `7594a2b`)

- `packages/react/npm/index.js` and `packages/react-dom/npm/client.js`: `if (process.env.NODE_ENV === 'production')` require `./cjs/*.production.js`, else `./cjs/*.development.js`. The switch happens at module load.
- What differs, per react.dev: StrictMode double render/Effects/ref callbacks are "development-only and do not impact the production build" (F9, `StrictMode.md:89-94`); hydration mismatch diffs and attribute warnings are dev-only (R2); production errors are minified codes (`errors/index.md:3`); `<Profiler>` "is disabled in the production build by default" (`reference/react/Profiler.md:40`); `captureOwnerStack` "will always return `null` outside of development" (`captureOwnerStack.md:54`) and "is only exported in development builds. It will be `undefined` in production builds" (`:386`).
- Factor consequence: React build mode changes the observer, not only performance. A production lane observes hydration through `onRecoverableError` codes only; a development lane adds attribute warnings and StrictMode double invocation. They are two observation lanes for one contract, so a dev-only warning without a prod recoverable error is expected for attribute mismatches (R2), not a dev/prod semantic disagreement.
- Effective-value evidence (proposed): `typeof React.captureOwnerStack` is `'function'` in development and `'undefined'` in production builds (from captureOwnerStack.md:386); this checks the bundle actually loaded rather than the requested `NODE_ENV`.

### S1. JS value comparison: `util.isDeepStrictEqual` (Node v26.13.0)

- `doc/api/util.md:1848-1872`: returns true on deep strict equality; by default compares prototypes and constructors; `skipPrototype: true` (added v24.9.0) skips that. It refers to `assert.deepStrictEqual()` for the rules (`util.md` about line 1898).
- `doc/api/assert.md:608-630` comparison details: primitives by `Object.is()` (so `NaN` equals `NaN`, `0` differs from `-0`, examples 667-690); type tags must match; `[[Prototype]]` compared with `===`; only enumerable own properties (plus enumerable own Symbols); Error `name`, `message`, `cause`, `errors` always compared; Map keys and Set items unordered; "Recursion stops when both sides differ or either side encounters a circular reference"; WeakMap, WeakSet and Promise "are **not** compared structurally. They are only equal if they reference the same object."
- Consequences (inference): (a) two Promises from two runs or two library versions are always unequal under `isDeepStrictEqual`, which is why a constructor-name placeholder (LambdaTester, P1) or an awaited-settlement observation is needed; (b) prototype `===` makes objects from two separately loaded copies of a library (two versions, or the dual instance of N2) unequal even with equal data unless `skipPrototype` is set; (c) it compares live objects in one process, so a cross-process pair (two Node versions, server vs browser) needs a serialization step first.

### S2. Serialization losses: JSON and structured clone

- JSON (MDN `JSON/stringify/index.md`, pin `0a6ff1e`): `undefined`, functions and Symbols "are either omitted (when found in an object) or changed to `null` (when found in an array)" (line 70); "`Infinity` and `NaN`, as well as the value `null`, are all considered `null`" (71); Symbol-keyed properties ignored (75); `toJSON` replaces the value, `Date` serializes via `toISOString` (77-82); "Only enumerable own properties are visited. This means `Map`, `Set`, etc. will become `"{}"`" (84); throws on a circular reference or a BigInt (61-62, 69).
- `-0`: ECMA-262 (`spec.html`, pin `828d35d`) SerializeJSONProperty returns `! ToString(value)` for finite Numbers (lines 48015-48017) and `Number::toString` returns `"0"` for "either +0 or -0" (line 2151). So `JSON.stringify(-0)` is `"0"`.
- Structured clone (MDN `Web_Workers_API/Structured_clone_algorithm/index.md`): keeps cycles ("maintaining a map of previously visited references", line 12) and supports Map, Set, Date, RegExp, Error types, typed arrays, plain objects (26-42); but functions and DOM nodes throw `DataCloneError` (16-17); RegExp `lastIndex`, property descriptors/getters/setters, the prototype chain and class private elements are not preserved (18-23); Error names outside the listed seven become `"Error"` (46).
- Consequence for the drafter: neither format is a faithful observation by default. A comparison serializer must state its losses and tag the cases that JSON collapses (`undefined` vs missing vs `null`, `NaN`/`Infinity` vs `null`, `-0` vs `0`, Map/Set vs `{}`, cycles, BigInt) and the cases structured clone drops (class identity, getters, private state, functions). LambdaTester's constructor-name placeholder (P1) is one stated loss; it hides internal state of those objects.

## Decisions for the drafter

1. **Worked hydration example: put it in `semantic-differential-testing/references/worked-paired-cases.md`** as a new section "Server HTML versus first client render", in the existing style ("illustrative experiment design, not executed findings"). Content:
   - Contract: hydrateRoot.md:57 identity; legal exceptions are the two-pass `isClient` pattern (280-325) and `suppressHydrationWarning` on one element (238-274).
   - Pair: server `renderToString` (or `onAllReady`/`prerender` output, not `onShellReady`) versus the same tree through `renderToString` inside the browser page with identical props and serialized store data (R4). Second observation: real `hydrateRoot` with `onRecoverableError`, `onCaughtError`, `onUncaughtError` recorders, in both a development and a production build.
   - Matched state: same props, same `getServerSnapshot` data, same `identifierPrefix`; server `TZ` and Playwright `timezoneId`/`locale` set deliberately (equal for the healthy pair, unequal to provoke); `Math.random`/time passed as data.
   - Outcomes kept distinct: string mismatch; production 418/422/423 recoverable error; dev-only attribute `console.error`; server `onError` plus client recoverable error (server failure, not mismatch); uncaught client render error.
   - Sensitivity control (for `harness-sensitivity`): a component rendering `new Date().toLocaleDateString()` under differing `TZ`/`timezoneId` must be flagged; the same component under equal settings must pass; an attribute-only difference must be flagged by the string comparison while the production `onRecoverableError` lane stays silent (R2 consequence 1).
2. **Nondeterminism table (R6) goes in `semantic-differential-testing/references/matched-state-and-effects.md`** as a JS subsection under "Define logical observations", because it is about establishing matched starting conditions.
3. **JS value comparison (S1, S2, P1) goes in `semantic-differential-testing/references/comparison-and-normalization.md`** as a section "JavaScript values and callbacks": what `isDeepStrictEqual` compares, JSON/structured-clone losses, and the LambdaTester/Nessie observation set (callback arguments at every invocation, invocation counts, arguments before and after each call, error vs success). Include Nessie's repeat-and-compare-sets rule (10 runs, an output counts only if never seen on the other side) as the async-nondeterminism treatment, and its Bug/Bug fix/Upgrade classification as the adjudication step for cross-commit pairs.
4. **SKILL.md for `semantic-differential-testing`**: one short paragraph under "Observe what the contract promises" naming the React production/development observer split (R2) and pointing at the worked case; one sentence under "Search, replay and adjudicate" that a reference implementation is ground truth only when the other side's contract is "match it" (P1). Common mistakes 1-10 below go in `semantic-differential-testing/references/common-mistakes.md`.
   - Description wording (proposed): "Guides comparisons of implementations, versions or execution modes under matched semantic conditions, including observable state effects, callback behavior and server-rendered HTML versus client hydration. Use when extending differential fuzzing beyond printed results, investigating disagreements, or designing contract-specific equivalence and replay."
5. **`configuration-differential-testing/references/factors-and-coverage.md`**: add a JS factor subsection mapped onto the existing PICT model format; no new machinery. Illustrative model (values must come from the target's `engines`, `exports`, Playwright config and build scripts):

   ```text
   Node: 22, 24, 26
   Load: esm, cjs
   ReactBuild: development, production
   Browser: chromium, firefox, webkit
   ```

   State per factor: requested control (`nvm`/CI image, entry file or `"type"`, bundler `NODE_ENV` define, `--project`), effective-value evidence (`process.version`, resolved file path, `typeof React.captureOwnerStack`, Playwright `browser.version()`), and that `Browser` applies only to client lanes and `Node` to server lanes (run them as separate sub-models or record "n/a" rather than inventing constraints). Say explicitly that the Jazzer.js 20.6/20.11 floor creates no constraint on the supported lines (N3), and that a package without a CJS entry makes `Load` single-valued by contract, not by constraint.
6. **`configuration-differential-testing/references/common-mistakes.md`**: add common mistakes 11-15 below.
   - Description wording (proposed): "Searches constrained build, runtime, platform and capability combinations for contract violations, including Node release lines, module format, browser engines and development versus production builds. Use when defaults pass but interacting configurations may change behavior, or when extending differential testing across supported modes."
7. **Tool routes**: cite LambdaTester and Nessie as methods, not installable routes. Both repos exist (MIT; last pushes 2018-09-27 and 2023-08-05); neither was installed or run. LambdaTester targets Node 8.5 and lacks ES6+ support per Nessie.

## Common mistakes with evidence

Format matches the skills' existing files (Wrong, Right, Why). Items 1-10 belong to `semantic-differential-testing`; 11-15 to `configuration-differential-testing`.

1. **Wrong:** "No `onRecoverableError` in production, so server and client agree." **Right:** production compares text and structure only; attribute mismatches appear only as a development `console.error` (`ReactDOMComponent.js:3272-3285`, `ReactFiberHydrationContext.js:933-969`). **Why:** the production observer cannot see the attribute dimension.
2. **Wrong:** render with `createRoot` + `flushSync` in the browser and diff `innerHTML` against server HTML. **Right:** compare `renderToString` against `renderToString` in the browser, and keep real hydration as a second observation. **Why:** `flushSync` "may run pending Effects" (flushSync.md:56) and `createRoot` uses `getSnapshot` not `getServerSnapshot` (useSyncExternalStore.md:48), so legal two-pass components look like mismatches; SSR `<!-- -->` separators also differ (hydrateRoot.md:251).
3. **Wrong:** add `suppressHydrationWarning` to make the differential pass. **Right:** use it only for one documented unavoidable element and keep that element out of the equality claim. **Why:** it "only works one level deep" and React "will **not** attempt to patch mismatched text content" (hydrateRoot.md:274); in production it disables the text check (`ReactDOMComponent.js:3280`, `3392`).
4. **Wrong:** match production hydration errors by message text. **Right:** match on the code (418, 421-424). **Why:** production messages are "Minified React error #<code>" (`formatProdErrorMessage.js`, `codes.json`).
5. **Wrong:** save server HTML at `onShellReady`. **Right:** save after `onAllReady`, `prerender`, or from `renderToString`. **Why:** nested Suspense content may still be loading at `onShellReady` (renderToPipeableStream.md:344); `onAllReady` output "will contain the final HTML" (line 61).
6. **Wrong:** compare JS results with `JSON.stringify` equality. **Right:** use a serializer that tags `undefined`, `NaN`, `Infinity`, `-0`, Map, Set, BigInt and cycles. **Why:** JSON drops or nulls `undefined`, nulls `NaN`/`Infinity`, turns Map/Set into `{}`, throws on cycles and BigInt (MDN stringify lines 61-84) and prints `-0` as `"0"` (ECMA-262 Number::toString).
7. **Wrong:** `util.isDeepStrictEqual(resultV1, resultV2)` across two library copies or with Promises inside. **Right:** compare settled values and constructor names, or use `skipPrototype` deliberately. **Why:** Promises are equal only by reference and prototypes are compared with `===` (assert.md:612, 625-628).
8. **Wrong:** compare only return values of a higher-order function. **Right:** record callback arguments at every invocation and invocation counts (LambdaTester Def 4.1), plus arguments before and after each call (Nessie). **Why:** the polyfill.io `find` bug returns `undefined` on both sides and differs only in callback count (Selakovic notes line 151, pp.19-20).
9. **Wrong:** run each async test once per version and report any difference. **Right:** repeat and compare output sets; report only outputs never seen on the other side. **Why:** Nessie runs each test 10 times per commit for scheduling nondeterminism (Arteca notes line 207, p.1501).
10. **Wrong:** every cross-version difference is a bug. **Right:** classify Bug / Bug fix / Upgrade against the changelog and contract. **Why:** Nessie's sampled differences include intended upgrades (Arteca notes line 210, p.1502) and needed manual filtering of renames and Node-version changes (line 205).
11. **Wrong:** set Playwright `timezoneId` and assume the server side shares it. **Right:** set the server process `TZ` separately and record both. **Why:** Playwright's setting "only affects the browser timezone and locale, not the test runner timezone" (emulation.md:383); Node reads `TZ` (cli.md:4664).
12. **Wrong:** set `NODE_ENV=production` when starting the browser test and assume the production React build ran. **Right:** check the loaded build (e.g. `typeof React.captureOwnerStack`). **Why:** React picks its build from `process.env.NODE_ENV` at module load (`packages/react/npm/index.js`), which a browser bundle fixes at build time (inference); `captureOwnerStack` is `undefined` in production builds (captureOwnerStack.md:386).
13. **Wrong:** treat the Playwright `webkit` project as Safari coverage. **Right:** report it as Playwright WebKit at a recorded version. **Why:** it is "derived from the latest WebKit main branch sources" and Playwright "doesn't work with the branded version of Safari" (browsers.md:590).
14. **Wrong:** include Node 20 or 27-alpha as supported lanes. **Right:** take the supported set from the target's `engines`/CI and the current nodejs/Release table. **Why:** 20.x reached EOL 2026-04-30 and 27.x is Alpha on 2026-11-09 (`schedule.json`, `README.md:11-15`).
15. **Wrong:** assume ESM fuzzing on Node 26 is instrumented because Jazzer.js's floor is 20.6. **Right:** check for the Jazzer.js ESM warnings and rising coverage per Node line. **Why:** its ESM path calls `module.register` (`instrument.ts:395`), runtime-deprecated in Node 26 (DEP0205) and slated for removal; failure prints a warning and continues (396-399).

## Sources inventory

- react.dev `7594a2b`: `src/content/reference/react-dom/client/hydrateRoot.md`, `reference/react-dom/server/renderToString.md`, `reference/react-dom/server/renderToPipeableStream.md`, `reference/react-dom/static/prerender.md`, `reference/react/useId.md`, `reference/react/useSyncExternalStore.md`, `reference/react-dom/flushSync.md`, `reference/react-dom/components/common.md`, `reference/react/StrictMode.md`, `reference/react/Profiler.md`, `reference/react/captureOwnerStack.md`, `errors/index.md`, `errors/generic.md`.
- facebook/react `v19.3.1` (`61aa00df`): `packages/react-reconciler/src/ReactFiberHydrationContext.js`, `packages/react-reconciler/src/ReactFiberErrorLogger.js`, `packages/react-dom/src/client/ReactDOMRoot.js`, `packages/react-dom-bindings/src/client/ReactDOMComponent.js`, `packages/react-dom-bindings/src/client/ReactFiberConfigDOM.js`, `scripts/error-codes/codes.json`, `scripts/error-codes/transform-error-messages.js`, `packages/shared/formatProdErrorMessage.js`, `packages/react/npm/index.js`, `packages/react-dom/npm/client.js`, `packages/react-dom/package.json`.
- vercel/next.js `cb4cc5b`: `errors/react-hydration-error.mdx`.
- nodejs/Release `6065a83`: `README.md`, `schedule.json`. GitHub releases API for nodejs/node.
- nodejs/node `v26.13.0`: `doc/api/esm.md`, `modules.md`, `packages.md`, `module.md`, `deprecations.md`, `cli.md`, `intl.md`, `util.md`, `assert.md`.
- microsoft/playwright `95e5dca`: `docs/src/test-projects-js.md`, `docs/src/browsers.md`, `docs/src/emulation.md`.
- CodeIntelligenceTesting/jazzer.js `f23bc5a`: `docs/fuzz-targets.md`, `packages/instrumentor/instrument.ts`, `package.json`, `packages/core/package.json`.
- mdn/content `0a6ff1e`: `web/api/web_workers_api/structured_clone_algorithm/index.md`, `web/javascript/reference/global_objects/json/stringify/index.md`, `web/javascript/reference/global_objects/intl/datetimeformat/datetimeformat/index.md`.
- tc39/ecma262 `828d35d`: `spec.html` (Number::toString, SerializeJSONProperty).
- Paper notes (produced through paper-reader by other agents): Selakovic 2018 LambdaTester; Arteca 2022 Nessie.
- APIs: GitHub API for `sola-da/LambdaTester`, `emarteca/nessie`, code search in jazzer.js; Zenodo API record 5874851.
- Raw copies of all fetched files: `C:/Users/Q/AppData/Local/Temp/claude/C--Users-Q-code-computational-bugfinding-skills-plugin/273e826b-42ea-4339-a414-a6b8f162d6a3/scratchpad/src/`.

## Unverified

- None of the proposed comparators (renderToString in browser vs server, `captureOwnerStack` build probe, serializer tagging) was executed. Whether `renderToString` from `react-dom/server.browser` in a Playwright page produces byte-identical output to Node for a deterministic tree is untested.
- `use(browser())` status in stable React: inferred from a TODO comment in hydrateRoot.md:278, not checked against React's exports.
- Whether production React's recovery from a text mismatch regenerates to the nearest Suspense boundary or the root in each case: codes 422/423 exist, but which path fires for a given tree was not traced.
- `process.versions.icu` and Playwright `browser.version()` as effective-value probes: not checked in the pinned docs.
- That `emarteca/nessie` is the paper's tool: inferred from owner and name; the Zenodo record lists only `ExperimentalData.tgz`.
- Jazzer.js on Node 26: the deprecation warning text and whether ESM instrumentation still works were not run. The GitHub code-search "no `registerHooks`" result may reflect a stale index.
- LambdaTester's handling of async promise reactions (open question in the Selakovic notes, line 216, and the tension at line 253).
- The Node dual-package hazard details now live in an external examples repository that was not read.
- Only the opening sections of `reports/research-semantic-differential-testing.md` and `reports/research-configuration-differential-testing.md` were read.
