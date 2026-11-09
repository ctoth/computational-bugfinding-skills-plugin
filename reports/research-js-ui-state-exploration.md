# Research: `ui-state-exploration` skill (group D, JS/TS web extension)

Date: 2026-11-09. Status: complete for drafting (chaosbringer evaluation added as X2). No skill, manifest, README or agent-note edits; nothing installed, committed or pushed.

## Inputs read (repository)

- `reports/skill-plan-js-web-bugfinding.md:80-97` (skill scope: model-free search over a discovered state graph; excludes model-based sequences, driver mechanics, visual regression; gaps Mesbah 2009, Roest 2010, React settle signals).
- `reports/skill-research-js-web-bugfinding.md:149-192` (F9 React, F10 Playwright/Puppeteer, F11 RTL/MSW), `:260-264` (failure space 2), `:288-297` (existing skills overlap).
- `reports/research-js-fuzzing-corpus.md:145-154` (J12, chaosbringer from README), `:224`, `:279`, `:297`.
- `plugins/bugfinding/skills/stateful-property-testing/SKILL.md` (house style: inline pinned-URL quotes; sections "Model", "Generate", "Shrink", "Select route"; references `model-and-sequences.md`, `runtime-recipes.md`, `common-mistakes.md` with "Wrong/Better" bullets, `sources.yaml` with name/url/type/accessed/sections_used).
- `plugins/bugfinding/skills/bugfinding-campaign/SKILL.md:27-37` (routing table; the new skill needs a row).
- `reports/research-stateful-property-testing.md` (evidence standard: per-source URL, quote fragment, finding, decision).
- Paper notes: `C:/Users/Q/code/papers/Mesbah_2012_CrawlingAjaxBasedWebApplications/notes.md` (cited "Crawljax p.N", TWEB article page 3:N), `C:/Users/Q/code/papers/Vilk_2018_BLeakAutomaticallyDebuggingMemoryLeaks/notes.md` (cited "BLeak p.N", PDF page).

## Findings

### L1. Mesbah, van Deursen, Roest 2012 (TSE), oracle companion — read via paper-reader

- Paper: "Invariant-Based Automatic Testing of Modern Web Applications", IEEE TSE 38(1):35-53, DOI 10.1109/TSE.2011.28. Author copy https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf. All 19 page images read. Notes: `C:/Users/Q/code/papers/Mesbah_2012_InvariantBasedAutomaticTesting/notes.md`. It is the "substantially expanded and revised version" of the ICSE 2009 paper (p.36); the ICSE 2009 version itself was not read. Cited below as "TSE p.N" (printed journal page).
- Findings:
  - Invariants are checked on every new state inside the crawl loop: Algorithm 2 line 11 `testInvariants(ns)` right after `runOnNewStatePlugins(ns)` (p.38). "just running CRAWLJAX would correspond to conducting a smoke test ... it is very hard to determine when a failure occurs—which is solved in ATUSA through the use of invariants" (p.50).
  - Generic DOM invariants: W3C-valid DOM after each state change; no error-message strings (404, 500, "Session Timeout", "MySQL error"), list configurable; accessibility/i18n checks per state (p.41).
  - Application-specific invariants: XPath (≥1 match), regex on DOM string, JavaScript expression true, URL contains, element visible; combinable NOT/OR/AND/NAND; each limited to states by a precondition (Table 2, p.41; Fig. 5, p.42). Invariants on JS variables (p.42, p.47).
  - Graph-level invariants: no dead clickables, detected from request/response traffic after each event because the Ajax engine swallows server errors (p.42); Back button returns to the graph's expected state (p.42); "Source - Action -> Target" temporal properties checked after inference (p.42).
  - Comparators "can also be too permissive, grouping DOM trees that should be considered different"; fix: comparator preconditions (p.40).
  - Exclude destructive elements: "exclude elements that are not of importance or can cause problems (delete items or log the user out)" (p.39); TUDU excluded `A:title=Log out` (p.48); HitList excluded delete links and limited "add contact" to once via a crawl condition (p.47).
  - Inputs: random defaults (8 alpha chars; checkbox/radio p<0.5; random list item), custom values, multiple custom values replayed with the transition; inputs stored with the clickable for replay (Table 1 and §4.7, p.40).
  - Reset hook: `OnUrlLoadPlugin` "After the initial URL is (re)loaded", example "Reset back-end state" (Table 3, p.44); TUDU reset its database by SQL script per test run (p.48).
  - Reproduction: "Whenever a fault is detected, the error report along the causing execution path is saved so that it can be easily reproduced later" (p.43); report includes DOM diff, screenshot, fired event sequence, applied comparators, to decide "real fault or a legal change" (p.44).
  - Results: TUDU 8 of 10 seeded faults; the two misses "were silently swallowed by the JAVASCRIPT engine and did not affect the DOM" (p.48). Depth 3 exceeded 60 min without changing fault detection (p.48). Commercial app: six fault types, three via generic and three via app-specific invariants; one needed "a very specific click trail" and "ATUSA gives no guarantee of covering the complete state" (Table 7, p.49-50).
  - TaskFreak: invariant "at most one calendar pop-up" found that cancel left the div in the DOM, "a (slowly) growing DOM tree" (p.46). A leak found by a structural invariant.
  - The hard part is "deciding which application-specific invariants to adopt" (p.50).
- Decision relevance: the oracle section attaches checks per new state (generic channels plus app invariants with preconditions) and over the graph (dead network calls, back/reload consistency, action→target). Faults that never reach the DOM need other channels (console, `pageerror`, network); the TSE misses motivate that. Destructive-action exclusion and back-end reset are required configuration, not options.

### L2. Roest, Mesbah, van Deursen 2010 (ICST), comparator pipeline — read via paper-reader

- Paper: "Regression Testing Ajax Applications: Coping with Dynamism", ICST 2010 pp.127-136, DOI 10.1109/ICST.2010.59. Author copy https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf. All 10 page images read. Notes: `C:/Users/Q/code/papers/Roest_2010_RegressionTestingAjaxApplications/notes.md`. Cited below as "Roest p.N" (printed proceedings page).
- Findings:
  - Nondeterminism sources named: "(HTTP) network delays, asynchronous client/server interactions, non-sequential handling of requests by the server, randomly produced or constantly changing data" (p.128-129).
  - Each comparator strips one targeted difference (regex or XPath), outputs are pipelined, and a plain string comparison decides equality (OCP, p.129-130). Hash of the stripped DOM per state (p.131).
  - Preconditions because generic comparators "can have the side-effect of missing real bugs because they are too broad" (p.129-130). Evidence: "Using only the generic comparators would result in a false negative, namely the leading-zero bug, which is ignored by the Table comparator" (p.134).
  - Templates for repeating structures (lists, tables) make more states equivalent, shrinking the state space; augmented templates become invariants (p.130-131).
  - Positional locators: "a similar element is mistakenly selected, which causes a transition to a different state than expected" (p.129); resolver uses "event handler(s), attributes, children nodes, and text value" (p.131); without the resolver V2 produced "many wrong transitions" (p.134).
  - Back-end state: "reset the back-end to an initial state" is "often used but cumbersome" (p.129); they still needed a clean-up post-crawl plugin and `oneTimeTearDown` restoring the database because deletes only work once (p.135).
  - Settling: "it is very important to have a large enough delay for the DOM tree to be updated completely ... Otherwise, an incomplete DOM state could be compared with a complete state" (p.135).
  - Drift: "The time between crawling and testing also had a large influence on the number of the found state differences" (p.134). Google Reader: generic comparators 35-55% reduction, custom up to 95% (Table IV, p.134); `closure_hashcode_*` attributes alone could yield "200+ state differences ... per state" (p.134).
  - Report shows stripped and full DOMs "to check whether differences are falsely ignored by the comparators" (p.132).
- Decision relevance: state abstraction must be a named, ordered list of normalizers, each scoped (precondition) and recorded with the graph; the agent inspects what each normalizer removed and keeps at least one planted-difference control so a normalizer that hides real faults is caught (the leading-zero case). An accessibility-tree snapshot is one coarse normalizer, not a free pass.

### L3. Crawljax and BLeak (already read; facts reused)

- Crawljax (TWEB 2012): transition iff DOM changes under the chosen comparison (p.8); global dedup against all visited states (p.9); candidates from the DOM diff because `addEventListener` handlers are invisible to DOM inspection (p.5, p.9); reset by reload and replay of the recorded path (p.10-11); cookies broke reset and web storage was expected to (p.26); fixed waits slow or unsafe, app completion flag reliable (p.27); depth 1→2 grew states 148→1,071 and 145→1,234 (p.18, p.20); no built-in oracle (p.19); elements needing repeated clicks missed by default (p.19).
- BLeak (PLDI 2018): leak oracle is growth across repeated returns to the same visual state (p.2); growth required between every consecutive snapshot (p.6); default 8 round trips (p.5, p.8); its only false positives were structures growing to a cap or timeout, removed by more round trips (p.11); loops are hand-written `check`/`next` state lists (p.4). Both notes record the conceptual link: a discovered state-graph cycle can supply the loop.

### P1. Playwright: pinned primary docs

Pin: tag `v1.65.0` (released 2026-11-05; tag object `a1f35e1955976e84411f9c10358228a80b763ebe`), files under `https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/`. Apache-2.0 and `"node": ">=20"` are from F10 (main `95e5dca3`); not re-read at the tag. Line numbers are in the v1.65.0 files.

- **State abstraction: aria snapshots.**
  - `aria-snapshots.md:142`: "aria snapshots provide a YAML representation of the accessibility tree of a page." `:146`: it details "**roles**, **attributes**, **values**, and **text content**."
  - Matching (`:214-217`): "case-sensitive and normalizes whitespace within names and text values"; "order-sensitive". Partial matching (`:224-225`, `:252`): omitting an attribute means "the test will pass regardless of the checkbox state". Regex in templates (`:336-339`).
  - `api/class-page.md:4442-4474`: `Page.ariaSnapshot` (since v1.59), `mode` `"ai"|"default"` ("When set to `"ai"`, returns a snapshot optimized for AI consumption: including element references like `[ref=e2]` and snapshots of `<iframe>`s"), `depth` ("limits the depth of the snapshot"), `boxes` (since v1.60). `Page.ariaSnapshotJSON` (since v1.63, JS only) returns the same tree as JSON (`:4476-4482`).
  - `api/class-page.md:2346-2352`: `Page.getByRef` (since v1.64): refs "resolve against the latest snapshot taken in the element's frame."
  - `docs/src/api/class-accessibility.md` at v1.65.0 returned an empty body: the old `page.accessibility` API is not documented at this tag. Inference: use `ariaSnapshot`.
  - Decision: an aria snapshot is a ready coarse state key (roles, names, states, values; no CSS). Refs resolve only against the latest snapshot (`:2351`), so inference: refs are not persistent edge labels; record edges as role + accessible name (+ scope) so replay after reload re-resolves them, the Playwright counterpart of Roest's resolver (Roest p.131). An omitted attribute or a `depth` limit is a normalizer and can merge states that differ (L2).
- **Event discovery.**
  - `locators.md:192`: `getByRole` "reflects how users and assistive technology perceive the page"; `:268` "We recommend prioritizing role locators". `:1730-1732`: locators are strict.
  - Inference (not from a doc): candidate events per state = interactive roles in the aria snapshot (button, link, checkbox, textbox, combobox, menuitem, tab, ...). This has the blind spot Crawljax records (p.5): a `div` with an `addEventListener` click handler and no role does not appear. chaosbringer's source (X2) relies on a `[cursor=pointer]` attribute in aria snapshots to recover such elements; that attribute is not in the Playwright docs read (unverified).
- **Actionability and auto-wait (what it hides).**
  - `actionability.md:8-9`: Playwright "auto-waits for all the relevant checks to pass and only then performs the requested action"; checks Visible, Stable, Receives Events, Enabled, Editable, Not Inert (`:11-42`).
  - `:93`: Stable means "the same bounding box for at least two consecutive animation frames." `:89`: "Elements with `opacity:0` **are** considered visible."
  - `:124`: "Playwright will click `Sign Up` button regardless of when the [`method: Locator.click`] call was made" (disabled during a server check, then replaced by an enabled one).
  - `:52`: "auto-retrying assertions that remove flakiness by waiting until the condition is met". `:46-48`: `force` "disables non-essential actionability checks". `:38`: `dispatchEvent` has no actionability checks.
  - Decision: auto-wait makes the explorer a patient user; it never fires the click a real user can fire during the disabled/loading window, and retrying assertions skip transient wrong states. Searching those windows needs a deliberate early action (`dispatchEvent`, `force`) or schedule control (`schedule-exploration`). Checks on a settled state read a one-shot snapshot, not a retrying assertion, when the transient is the bug.
- **Settle signals.**
  - `api/params.md:7`, `:1007`: `'networkidle'` is "**DISCOURAGED** ... no network connections for at least `500` ms. Don't use this method for testing, rely on web assertions to assess readiness instead."
  - `api/class-page.md:5117-5126`: `waitForLoadState` resolves on `load` by default; "Most of the time, this method is not needed because Playwright auto-waits before every action."
  - `api/class-page.md:4966-4970`: `waitForFunction` "Returns when the [`param: expression`] returns a truthy value."
  - Decision: none of these says "the app has finished reacting to the event". Use an app-specific settle predicate via `waitForFunction` (Crawljax completion flag, p.21, p.27), plus a stability check (two consecutive equal state keys; inference) and a timeout recorded as "unsettled", not as a state. Roest p.135 shows the cost of comparing incomplete DOMs.
- **Reset between runs.**
  - `browser-contexts.md:12`: each test "has its own local storage, session storage, cookies etc."; contexts "are equivalent to incognito-like profiles. They are fast and cheap to create and are completely isolated".
  - `auth.md:115`: "IndexedDB is not included in the snapshot by default" (option `indexedDB: true`). `auth.md:595`: "Playwright does not provide API to persist session storage".
  - Decision: a fresh context per replay path fixes Crawljax's cookie/web-storage reset failure (Crawljax p.26) for client state only. Server state still needs a reset hook (TSE p.44, p.48; Roest p.135). When seeding a logged-in context with `storageState`, include IndexedDB if the app uses it.
- **Oracle channels.**
  - `api/class-page.md:171`: `console` "Emitted when JavaScript within the page calls one of console API methods". `:396-400`: `pageError` "Emitted when an uncaught exception happens within the page." `api/class-browsercontext.md:295-300`: `webError` "Emitted when exception is unhandled in any of the pages in this context."
  - `api/class-page.md:511-538`: `requestFailed` fires on transport failure; "HTTP Error responses, such as 404 or 503, are still successful responses from HTTP standpoint, so request will complete with [`event: Page.requestFinished`] event and not with [`event: Page.requestFailed`]."
  - Decision: these give TSE's "dead clickable" invariant (TSE p.42) and catch faults that never reach the DOM (TSE p.48). A dead-clickable check reads response status (`response`/`requestfinished`), not only `requestfailed`. Unhandled promise rejections: not stated in the Playwright docs read; chaosbringer's source says "Rejections in Chromium fire both the DOM event and Playwright's CDP-level pageerror" (X2; third-party, Chromium only).
- **Network and time control.**
  - `network.md:28-44`, `:411-470`: `route.abort()`, `route.fulfill(...)`, `route.continue(...)`. `clock.md:8-20`: `setFixedTime` for `Date.now()`/`new Date()`; `install` with `pauseAt`, `fastForward`, `runFor`.
  - Decision: freezing time and fulfilling volatile endpoints removes nondeterminism at the source, preferable to a broad comparator that may hide faults (L2). Holding or reordering responses is schedule search and belongs to `schedule-exploration`.
- **Replay artifacts.**
  - `api/class-tracing.md:150-158` (JS): `snapshots` `{ dom, aria, screen }`: "Capture DOM snapshot on every action and record network activity", "Capture aria snapshot of the page on every action".
  - Decision: record a trace per failing path replay, with aria snapshots, as the artifact for `failure-reduction`/`evidence-based-triage`.

### R1. React: what a page-level explorer can observe (react.dev pinned)

Pin: `reactjs/react.dev` main `7594a2b008489121bdf25f97320d11ac0422510e` (same pin as F9), `src/content/reference/...`. Docs content CC-BY-4.0 (F9).

- `react-dom/client/createRoot.md:48-50`: root options `onCaughtError` ("called when React catches an error in an Error Boundary"), `onUncaughtError` ("called when an error is thrown and not caught by an Error Boundary"), `onRecoverableError` ("called when React automatically recovers from errors"; "Some recoverable errors may include the original error cause as `error.cause`"). `:358`: "By default, React will log all errors to the console."
- `react/Component.md:1272`: with an error boundary React displays "some fallback UI instead of the part that crashed". `:1275-1280`: boundaries "do not catch errors for": event handlers; server side rendering; errors in the boundary itself; asynchronous code (`setTimeout`, `requestAnimationFrame`), except errors inside a `startTransition` function.
- `react/act.md:7`: "`act` is a test helper to apply pending React updates before making assertions." `:53`: updates "are added to an internal act queue, which are then flushed together". F9 records it needs `IS_REACT_ACT_ENVIRONMENT=true` (`act.md:158`).
- `react/Suspense.md:7`, `:78`: `<Suspense>` displays "a fallback until its children have finished loading". `:1950`: "A Transition doesn't wait for *all* content to load. It only waits long enough to avoid hiding already revealed content."
- `react/useTransition.md:44`: `isPending` "tells you whether there is a pending Transition". `:116`: "A state update marked as a Transition will be interrupted by other state updates."
- Decisions:
  - A boundary-caught render error shows as fallback UI, not as `pageerror` (inference from `Component.md:1272` and Playwright `pageError` = "uncaught exception"). Oracle channels: console errors (React's default logging, `createRoot.md:358`), or `onCaughtError`/`onUncaughtError`/`onRecoverableError` when the target exposes them, plus a per-state invariant "no error-boundary fallback visible" (TSE-style generic error-message invariant, TSE p.41).
  - Event-handler and async errors bypass boundaries (`Component.md:1275-1280`); they surface as uncaught errors (inference) → `pageerror`.
  - Settle: I found no react.dev API by which a browser-level test learns that React has no pending work; `act` applies only in an act test environment. Inference: settle predicates come from the app (no Suspense fallback visible; transition `isPending` exposed as e.g. `aria-busy`; the Crawljax-style completion flag). Suspense fallbacks and pending transitions are intermediate states: count them as states only if the settle predicate deliberately allows it.
  - `act` and RTL belong to component-level `stateful-property-testing`; this skill drives a real page (Playwright), so `act` is out of scope except as the reason component-level exploration does not see production interleaving (F9).

### X1. Maintained JS/TS crawler or model-free explorer; existing skills (checked 2026-11-09)

- `crawljax/crawljax`: Java, 558 stars, last push 2023-09-18, not archived (`gh search repos crawljax`). Related: `tsigalko18/apogen` (Java, archived, pushed 2018-06-20); `owtf/spyderjax` (Python, archived, 2015).
- `marmelab/gremlins.js`: MIT, 9,103 stars, last push 2023-03-06; npm `gremlins.js` 2.2.0 published 2020-07-21, description "A monkey testing library written in JavaScript, for Node.js and the browser". Random events; README not read, so whether it keeps any state model is unverified.
- npm text searches ("ui crawler playwright", "monkey testing web", "crawljax") found no JS/TS state-graph crawler. GitHub repo searches "web app state crawler playwright", "gui ripping web", "state-flow graph crawler", "automated exploratory testing playwright" returned no results. My searches did not surface chaosbringer; group A found it by web search (J12). Negative results are bounded, not proof of absence.
- AI exploratory-testing packages (npm "exploratory testing", 2026):
  - `willcoliveira/qualiow-exploratory-testing-skills` (MIT, pushed 2026-11-03, HEAD `11a2b22e0cf709f6ba6802f0b0e75abf948a0f15`): Claude Code skills incl. `qa-explore`, description "Run a full AI-driven exploratory testing session against a web application. Acts as a Principal QA Engineer — understands the business first, risk-ranks features ...", tools `playwright-cli`. Grep of its SKILL.md for state graph / equivalence / reset / replay / invariant / oracle / dedup / visited matched none; one hit for "check console and requests" in a Discovery phase. Overlap: driving and console checks; no state abstraction, dedup, reset or replay discipline on the grep evidence (phase files not read).
  - `breakit` 1.2.1 (npm; "Drives a real browser to surface UX issues, functional bugs, and console errors, with replay-verified findings"); its GitHub repo `petrkindlmann/breakit` returned 404. Not inspected.
  - `vegapunk` 0.1.7 ("AI-assisted exploratory testing on top of Playwright"; repo 0 stars, pushed 2026-10-02), `@athenaflow/plugin-exploratory-testing` (charters). Not inspected.
- Already recorded in F-report (`skill-research-js-web-bugfinding.md:294-295`): Playwright's own skills (`playwright-cli`, `playwright-trace`) and `anthropics/skills` `webapp-testing` cover driving and inspection, no search or oracle method.

### X2. chaosbringer at a pinned commit (source read, not executed)

Pin: `mizchi/chaosbringer` `5f69d89ef300cc1fb213301d7942ab17f28c82be` (2026-11-08; same pin as J12). Files read: `packages/chaosbringer/src/crawler.ts` (3,975 lines; grepped and excerpts read), `src/action-targets.ts`, `src/aria-targets.ts`, `src/aria-snapshot.ts` (grep), `src/ddmin.ts` (header), `package.json`, `README.md` (feature list, invariants intro, reproducibility, HAR), `.claude/skills/chaosbringer/SKILL.md` (frontmatter). `src/settle.ts`, `src/coverage.ts` body, drivers and fault modules not read.

- **Repository and maintenance.** MIT, TypeScript, created 2026-01-15, last push 2026-11-08, 50 stars, not archived (GitHub API). Contributors by commit count: `claude` 263, `mizchi` 234, `mizchi-release-bot[bot]` 7. At least 100 commits since 2026-10-01 (API page cap reached). `packages/chaosbringer/package.json:3` version `0.15.0`; `:18-19` `"engines": {"node": ">=22"}` — J12 recorded npm 0.15.0 with `>=20`, so the repo and the published package differ (not resolved). Playwright `^1.59.0` / `^1.63.0` appear in `package.json:78`, `:103` (which field each is in was not checked). Monorepo also has `playwright-faults`, `server-faults`, `cf-faults`, `lightbringer`, `playwright-v8-coverage`.
- **What it is.** `README.md:3`: "Playwright-based chaos testing for web apps. Crawls the pages you point it at, performs weighted random actions, injects network faults, evaluates invariants, and reports what broke — with a seed you can replay." Its own Claude skill describes itself as for writing "fault-injection and chaos tests for a web app", also to "sweep an unfamiliar site for bugs and slow spots (`chaosbringer scan`)".
- **State abstraction.** The unit of exploration is the page URL, not a UI state: `crawler.ts:277-278` `visited: Set<string>` and `queue`; `:917-925` BFS loop `while (this.queue.length > 0 && this.visited.size < this.options.maxPages)`, skipping `this.visited.has(normalizeUrl(entry.url))`. Links, SPA `history.pushState`/`replaceState` navigations and sitemaps feed the queue (`README.md:22`; `crawler.ts:1223-1267`). Within a page it performs up to `maxActionsPerPage` weighted random actions (`crawler.ts:780-781`). I found no DOM- or aria-based state key, no dedup of in-page states, and no state-flow graph in the code read. Inference: two different UI states at the same URL are one node; Crawljax/Roest state equivalence is not implemented.
- **Event discovery.** `action-targets.ts:127-284`: CSS scrape of `a[href]`, `button, [role='button']`, eight ARIA roles (`menuitem`, `tab`, `checkbox`, `radio`, `switch`, `slider`, `listbox`, `option`), form fields, `select`. `aria-targets.ts:1-20`: joins the scrape with the aria snapshot to add "targets the scrape misses: a `<div onclick>` with a pointer cursor, a `<summary>`, a control past the scrape's cap"; `aria-snapshot.ts:170`: `if (node.attrs.cursor === "pointer") return "button";`. Weighting: "an unvisited link is worth 3x a visited one" (`action-targets.ts` header); README `:20` "nav links > buttons > inputs > scroll". Optional V8-coverage boost (J12).
- **Element identity for replay.** `action-targets.ts:508-530` `selectorFor`: `tag:has-text("…")` when text < 50 chars, else `aria-label`, `placeholder`, `name`, else positional `:nth-match([role="…"], index+1)`. Inference: text- and position-based selectors carry Roest's wrong-element risk (Roest p.129) when list content changes between runs.
- **Oracles.** `crawler.ts:2110-2323`: collectors for `console`, `pageerror`, `response`, `requestfailed`, crash; `:2194-2206` records every response with `status() >= 400` (so it does not rely on `requestfailed` alone). Unhandled rejections captured by an init script that calls `preventDefault` (`:2390-2396`) and reclassified (`:575-577`: "Rejections in Chromium fire both the DOM event and Playwright's CDP-level pageerror, so we dedupe here"). Invariants run per page in phases `afterLoad`, `afterActions` (default), `afterVisit` (`README.md:599-601`; `crawler.ts:608-652` records violations as `invariant-violation`). Built-in invariant sets referenced in README: `--axe`, `--data-safety`, `--visual-baseline`, `noOffsiteRedirect` (README `:168`; not read in detail). This is a real per-page oracle layer, close to TSE's generic invariants.
- **Reset.** One `browser.newContext(...)` per crawl run (`crawler.ts:830-841`, optional `storageState`), and a new page per visit from that context (`:2031`). Inference: cookies and storage persist across visits within a run (Crawljax p.26 problem) unless lifecycle faults wipe them; the README lists "storage wipe (localStorage / sessionStorage / cookies / IndexedDB)" as a fault, not a reset. No server reset hook seen besides a "pre-run setup hook" heading (README `:357`, not read).
- **Settle.** Imports `settleAdaptive` from `settle.ts` (`crawler.ts:165-169`); a resolved `settle` option "how each load and each action waits" (`:467-473`), with an in-flight-request count and a `networkidle` mode. `settle.ts` not read; its semantics are unverified.
- **Replay and reduction.** Seeded RNG; "same seed, same action order" and a printed `Repro:` line (README `:21`, `:70-71`, `:158-168`). Fault rules and invariants set in code are not carried by the CLI repro line (README `:168`). HAR record/replay (README `:792-833`), trace record/replay/minimize and Zeller ddmin (`ddmin.ts`; README `:36`). Failure bundles with screenshot, HTML, errors, trace prefix and `repro.sh` (README `:37`). Coverage-feedback runs reproduce from `(seed, coverageFeedback)`, not the CLI alone (J12).
- **Scope beyond this skill.** Network, lifecycle, runtime (`reject-fetch`, `never-settle-fetch`, `clock-skew`) and iframe faults; deterministic fault schedules; Quint model-driven fault plans (README `:23-28`). These overlap `distributed-fault-testing`/`schedule-exploration`/`correctness-oracles`, not state exploration.
- **Assessment.** It is a maintained, Chromium-centred (coverage feature only; J12) random UI-action crawler with a strong per-page oracle and repro layer, but its exploration unit is the URL with random in-page actions. It does not do model-free UI *state* exploration in the Crawljax sense (no state key, no in-page state dedup, no state graph, no per-path context reset, no replay-by-path to a chosen state). Single human maintainer plus heavy AI-authored commits, pre-1.0, ~10 months old.
- **Decision for the skill.** Name chaosbringer in the route section as an existing random-crawl lane worth using as a baseline or harness where the target already uses it: its oracle collectors, rejection capture, HTTP-status check, seeded repro and failure bundles are directly reusable, and its `cursor=pointer` aria heuristic addresses the listener-only blind spot. The skill's own contribution remains the parts chaosbringer lacks: a state key with scoped normalizers, in-page state dedup and graph, per-path reset, replay-by-path with robust locators, and cycle hand-off to leak checks. Do not build on it as a required dependency (pre-1.0, Node floor mismatch, unexecuted). Its Claude skill overlaps fault injection, not this skill.

### Decision (X1 + X2)

No maintained JS crawler does state-graph exploration; the skill guides a small target-specific loop over Playwright (plan line 91), routes driver mechanics to Playwright's skills, names chaosbringer as an optional random-crawl baseline and oracle harness, and states that AI exploratory-QA skills are complementary, not a substitute for recorded states, normalizers, reset and replay.

## Proposed SKILL.md outline

```yaml
---
name: ui-state-exploration
description: Guides model-free exploration of browser and React UI states by discovering events, abstracting and deduplicating states, resetting and replaying paths, and checking oracles at every new state. Use when bugs need unknown click/input paths through a web UI, when no operation model exists, or to find state cycles for leak checks; drives Playwright.
---
```

Sections (house style of `stateful-property-testing/SKILL.md`: short imperative sections, each claim with a pinned link and a short quote):

1. **Purpose and boundary** (one paragraph). Discover reachable UI states without a model; choose `stateful-property-testing` when an operation model with preconditions exists or is cheap; no general crawler framework (plan line 91). Crawl alone is a smoke test (TSE p.50).
2. **Define state before crawling.** State key = aria snapshot or filtered DOM through an ordered list of named normalizers, each scoped by a precondition; prefer removing nondeterminism at source (`clock.setFixedTime`, `route.fulfill`) over broad normalizers; dedup against all visited states (Crawljax p.9); keep a planted-difference control (Roest p.134). A URL is not a state key (X2).
3. **Discover and fire events.** Candidates = interactive roles in the current snapshot, new-in-diff first (Crawljax p.9), plus pointer-cursor elements where available (X2, unverified attribute); a candidate is a transition only if the state key changes (Crawljax p.8); exclusions for destructive actions and external links (TSE p.39, p.47-48); inputs: defaults plus custom values stored with the edge (TSE p.40); record coverage limit for listener-only elements (Crawljax p.5).
4. **Settle before observing.** App-specific predicate via `waitForFunction`; not `networkidle` (params.md:7); stability check; timeouts recorded as unsettled (Roest p.135; Crawljax p.27). Auto-wait/retrying assertions hide transients (actionability.md:52, :124).
5. **Reset and replay.** Fresh browser context per path (browser-contexts.md:12); server reset hook (TSE p.44; Roest p.135); edges labeled by role + accessible name, re-resolved after reload (Roest p.129, p.131; class-page.md:2351); replay mismatch is a finding about nondeterminism, logged, not silently merged (Crawljax p.25-26).
6. **Check oracles at every new state.** Generic: `pageerror`/`webError`, unhandled rejections, console errors, error-boundary fallback visible, HTTP ≥400 responses per event (dead clickable), error strings (TSE p.41-42; class-page.md:396, :535; createRoot.md:48-50, :358). App invariants with preconditions (TSE Table 2 p.41). Graph invariants after crawl: back/reload consistency, Source-Action->Target (TSE p.42). Route contract choice to `correctness-oracles`.
7. **Bound and allocate.** Depth, state count, time, exclusions; depth growth evidence (Crawljax p.18, p.20; TSE p.48); report states, transitions, unsettled, unresolved replays, oracle evaluations; zero findings is a bounded result.
8. **Select a route.** Own Playwright loop (default); chaosbringer as an optional baseline/oracle harness where already in use (X2); AI exploratory-QA skills as complementary.
9. **Hand off.** Cycles → `resource-complexity-testing` BLeak loop (BLeak p.2, p.6, p.11); failing path + trace → `failure-reduction`, `evidence-based-triage`; races in loading windows → `schedule-exploration`; mismatch between two configurations of the same graph → `configuration-differential-testing`.
10. **Return.** Graph (states, normalizer list, edges), oracle results, replay artifacts, limits.

## Reference files and contents

- `references/state-abstraction.md`: normalizer pipeline (Roest OCP, preconditions, templates), aria-snapshot matching rules and what they drop (aria-snapshots.md:214-252), source-level nondeterminism removal (clock, route), dedup and hashing, the planted-difference control, worked example: a timestamp normalizer scoped to one region vs a global list normalizer that hides a data bug (Roest p.133-134 leading-zero case).
- `references/playwright-crawl-loop.md`: a minimal target-specific loop (snapshot → candidates → act → settle → key → dedup → check → record edge; reset by new context + replay); event wiring for `pageerror`, `console`, `response`, `webError`, unhandled rejections; trace capture with `snapshots: { dom, aria }`; early-action option (`dispatchEvent`/`force`) and its caveat; pins and runtime floor; a short chaosbringer section (what to reuse, what it lacks; X2). Short code sketch, clearly marked unexecuted.
- `references/oracles-per-state.md`: generic invariant catalog (TSE §5.1, §5.3), React error channels and boundary limits (createRoot.md:48-50; Component.md:1275-1280), invariant-with-precondition form, graph invariants, how to classify fault vs legal change (TSE p.44; Roest p.132).
- `references/common-mistakes.md`: below.
- `references/sources.yaml`: inventory below.

## Common mistakes (Wrong/Better, with evidence)

1. **Wrong:** Count a crawl that completed as a test. **Better:** Attach oracles per state; "just running CRAWLJAX would correspond to conducting a smoke test" (TSE p.50).
2. **Wrong:** Add broad normalizers until differences disappear. **Better:** One named, scoped normalizer per difference; check what it removed; "Using only the generic comparators would result in a false negative, namely the leading-zero bug" (Roest p.134; TSE p.40).
3. **Wrong:** Store positional selectors or `[ref=eN]` as edge identity. **Better:** Role + accessible name re-resolved after reload; positional XPath selected "a similar element" causing "a transition to a different state" (Roest p.129); refs "resolve against the latest snapshot" (class-page.md:2351).
4. **Wrong:** Settle with `networkidle` or one fixed sleep. **Better:** App settle predicate plus stability; `networkidle` is "DISCOURAGED" (params.md:7); incomplete DOMs cause false failures (Roest p.135); fixed waits slow or unsafe (Crawljax p.27).
5. **Wrong:** Rely on auto-wait and retrying assertions when the suspected bug is a transient or a too-early click. **Better:** One-shot snapshot checks and deliberate early actions or schedule control; Playwright clicks "regardless of when the click call was made" once enabled (actionability.md:124); assertions retry "until the condition is met" (:52).
6. **Wrong:** Reuse one browser context and reload to reset. **Better:** New context per path, plus IndexedDB in seeded `storageState`; cookies broke Crawljax reset (Crawljax p.26); contexts isolate cookies and storage (browser-contexts.md:12); "IndexedDB is not included in the snapshot by default" (auth.md:115).
7. **Wrong:** Reset only the browser. **Better:** Reset or snapshot server state per path; deletes succeed only once (Roest p.135); TSE used an `OnUrlLoad` back-end reset and SQL reset (TSE p.44, p.48).
8. **Wrong:** Let the explorer click everything. **Better:** Exclude logout, delete and external links unless that path is the target (TSE p.39, p.47-48; Roest Table I p.133).
9. **Wrong:** Check only the DOM. **Better:** Also `pageerror`, unhandled rejections, console errors and network status; two seeded faults "were silently swallowed by the JAVASCRIPT engine and did not affect the DOM" (TSE p.48).
10. **Wrong:** Detect dead clickables with `requestfailed`. **Better:** Inspect response status; 404/503 "complete with requestFinished ... and not with requestFailed" (class-page.md:535-538).
11. **Wrong:** Treat no `pageerror` as no React error. **Better:** Check console errors, root error callbacks and boundary fallbacks; boundaries display "fallback UI" (Component.md:1272); React logs errors to console by default (createRoot.md:358). Event-handler and async errors are not caught by boundaries (Component.md:1275-1280).
12. **Wrong:** Raise depth for coverage by default. **Better:** Raise it on evidence; depth 1→2 grew states ~7x (Crawljax p.18, p.20); TSE depth 3 exceeded 60 min without new faults (TSE p.48).
13. **Wrong:** Report a heap increase across one revisit of a discovered cycle as a leak. **Better:** Hand the cycle to `resource-complexity-testing`; BLeak requires growth in every consecutive round trip, 8 by default, and its false positives disappeared with more round trips (BLeak p.5-6, p.11).
14. **Wrong:** Claim the explored graph is the app's state space. **Better:** Report it as one instance with listed blind spots (listener-only elements, repeated-click elements); "not all states are necessarily reached" (Crawljax p.19, p.26).
15. **Wrong:** Treat a URL-level random crawl (e.g. chaosbringer's visited-URL BFS with random in-page actions) as UI state coverage. **Better:** Count distinct state keys reached; chaosbringer dedups by `normalizeUrl(entry.url)` only (`crawler.ts:917-925`), so in-page states at one URL are not distinguished (X2, inference from source).

## Boundaries

- **`stateful-property-testing`:** owns model-based sequences (commands with `check`/`run`, preconditions, shrinking against a model), including fast-check + RTL/Playwright UI sequences (plan line 97). This skill has no model: it discovers states and transitions and checks oracles per state. Hand-over: a discovered graph region whose behavior is understood can become a model for `stateful-property-testing`.
- **`resource-complexity-testing`:** owns leak confirmation. This skill supplies cycles (state A → … → A with stable edge locators and a settle predicate) as BLeak-style loops (BLeak p.4: `check`/`next` per visual state). It does not take heap snapshots or rank leaks; DOM-growth invariants (TSE p.46) may flag a candidate, which is then confirmed there.
- **`correctness-oracles`:** owns choosing the contract and observation channels in general (incl. the React `onRecoverableError`/StrictMode notes planned there). This skill owns when and where oracles run during exploration (every new state, every edge, post-crawl graph checks) and the UI-specific generic invariant list.
- Also: `schedule-exploration` (reordering responses, acting inside loading windows by controlled schedules); `distributed-fault-testing` (chaosbringer-style network/runtime fault injection is fault work, not state exploration); `failure-reduction`/`evidence-based-triage` (trace, path reduction); `configuration-differential-testing` (same crawl across browsers; TSE p.43, Table 4 CrossBrowser Tester); Playwright's own skills (driver mechanics); visual regression excluded (plan line 94).
- `bugfinding-campaign` routing table needs a row, e.g. "Unknown UI event paths and per-state UI oracles | `ui-state-exploration`".

## Sources inventory (for `sources.yaml`)

| name | url | type | sections used |
|---|---|---|---|
| Mesbah, van Deursen, Roest 2012 TSE | https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf (DOI 10.1109/TSE.2011.28) | research-paper | pp.38-50 |
| Roest, Mesbah, van Deursen 2010 ICST | https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf (DOI 10.1109/ICST.2010.59) | research-paper | pp.128-135 |
| Mesbah, van Deursen, Lenselink 2012 TWEB | DOI 10.1145/2109205.2109208 (author copy people.ece.ubc.ca/amesbah/resources/papers/tweb-final.pdf per notes) | research-paper | pp.5-27 |
| Vilk, Berger 2018 BLeak | https://raw.githubusercontent.com/plasma-umass/BLeak/master/paper.pdf (DOI 10.1145/3192366.3192376) | research-paper | pp.2-11 |
| Playwright aria snapshots | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/aria-snapshots.md | official-documentation | :142-146, :210-252, :336, :430-462 |
| Playwright Page API | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md | official-documentation | :165-171, :396-400, :511-538, :2346-2352, :4442-4482, :4966-4970, :5117-5126 |
| Playwright BrowserContext API | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-browsercontext.md | official-documentation | :295-300 |
| Playwright params | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/params.md | official-documentation | :1-7, :1000-1007 |
| Playwright actionability | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/actionability.md | official-documentation | :8-52, :89-93, :124 |
| Playwright locators | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/locators.md | official-documentation | :192, :268, :1730 |
| Playwright browser contexts | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/browser-contexts.md | official-documentation | :8-12 |
| Playwright auth | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/auth.md | official-documentation | :115, :595 |
| Playwright network | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/network.md | official-documentation | :28-44, :411-470 |
| Playwright clock | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/clock.md | official-documentation | :8-20 |
| Playwright tracing API | https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-tracing.md | official-documentation | :150-158 |
| react.dev createRoot | https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/createRoot.md | official-documentation | :48-50, :358 |
| react.dev Component (error boundaries) | https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/Component.md | official-documentation | :1272-1280 |
| react.dev act | https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/act.md | official-documentation | :7, :53 |
| react.dev Suspense | https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/Suspense.md | official-documentation | :7, :78, :1950 |
| react.dev useTransition | https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/useTransition.md | official-documentation | :44, :116 |
| chaosbringer crawler source | https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/crawler.ts | primary-source-code | :277-278, :575-577, :608-652, :830-841, :917-925, :2031, :2110-2323, :2390-2396 |
| chaosbringer action targets | https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/action-targets.ts | primary-source-code | header, :127-284, :508-530 |
| chaosbringer aria targets / snapshot | https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/aria-targets.ts (and aria-snapshot.ts) | primary-source-code | aria-targets :1-20; aria-snapshot :170 |
| chaosbringer README and package.json | https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/README.md | official-documentation | :3, :19-37, :158-168, :599-601, :792-833; package.json :3, :18-19 |
| crawljax repo metadata | https://github.com/crawljax/crawljax | repository-metadata | last push 2023-09-18 |
| gremlins.js metadata | https://github.com/marmelab/gremlins.js ; https://registry.npmjs.org/gremlins.js | repository-metadata | last push 2023-03-06; npm 2.2.0 2020-07-21 |
| qualiow qa-explore skill | https://raw.githubusercontent.com/willcoliveira/qualiow-exploratory-testing-skills/11a2b22e0cf709f6ba6802f0b0e75abf948a0f15/.claude/skills/qa-explore/SKILL.md | skill (third-party) | frontmatter; grep for method terms |

All accessed 2026-11-09.

## Unverified / open

1. ICSE 2009 "Invariant-Based Automatic Testing of AJAX User Interfaces" itself not read; only its TSE 2012 extension.
2. Unhandled promise rejections as `pageerror`: not stated in the Playwright docs read; chaosbringer's source comment (`crawler.ts:575-577`) says Chromium fires both; Firefox/WebKit behaviour unknown.
3. Whether any Playwright API enumerates event listeners; and whether `[cursor=pointer]` in aria snapshots is a documented Playwright attribute (chaosbringer relies on it; not in the docs read).
4. Playwright license and Node floor at tag v1.65.0: carried from F10 (main `95e5dca3`), not re-read at the tag.
5. Stability of aria-snapshot output across browsers for the same DOM: not checked.
6. Inferences marked in R1 (boundary-caught errors absent from `pageerror`; no browser-level React "settled" API) are from docs reading, not executed tests.
7. gremlins.js README, qualiow phase files, breakit (repo 404), vegapunk: not read beyond metadata/grep.
8. chaosbringer: `settle.ts`, coverage body, drivers, server-reset/setup hook, fault modules not read; Node floor `>=22` in repo vs `>=20` on npm 0.15.0 (J12) unresolved; nothing executed. The "no state key / no in-page dedup" conclusion is from the files read, not an exhaustive read of 160 KB `crawler.ts`.
9. Paper-reader Step 7 (reconcile) was not run: it would edit the Crawljax notes owned by another agent. The two new paper directories carry their own cross-references; `papers/index.md`, `papers/_reader_done.tsv` and `papers/keymap.tsv` were updated.
10. No code was executed against any target; the loop in the proposed reference is design, not tested.
