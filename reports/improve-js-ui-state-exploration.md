# Improvement pass: ui-state-exploration

Scope: plugins/bugfinding/skills/ui-state-exploration/ (SKILL.md and references), checked sentence by sentence against the pinned sources and the paper-reader notes/page images in C:/Users/Q/code/papers/.

Accessed 2026-11-09. Six findings, all WARNING, all fixed in place (10 lines changed across 6 files). No ERROR-level finding: every quotation matched its source word for word.

## Findings

### F4 references/common-mistakes.md:15 and references/oracles-per-state.md:39 — WARNING (stronger than source)
- Said: "its false positives disappeared with more round trips" / "its only false positives were structures growing to a cap or timeout, removed by more round trips".
- Source: BLeak extended version, PDF p.11 (pngs/page-010.png), §6.2: "There are only three false positives. All point to an object that continuously grows until some threshold or timeout occurs; developers using BLeak can avoid these false positives by increasing the number of round trips." The paper states they are avoidable; it reports no rerun in which they disappeared.
- Fix: "disappeared with more round trips" → "were objects growing to a threshold or timeout, avoidable by more round trips"; "removed by more round trips" → "avoidable by more round trips".

### F5 references/playwright-crawl-loop.md:56 and references/sources.yaml:184 — WARNING (line range and scope)
- Said: chaosbringer "records every response with status 400 or higher, not only transport failures" ([crawler.ts:575-577, 2194-2206]).
- Source: crawler.ts at 5f69d89 (https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/crawler.ts): lines 2194-2206 are the comment ("Always on, for the HTTP status of every request that answered >= 400") and the `answeredWithError` set; the recording is lines 2217-2227: `if (status < 400) return; ... if (this.isIgnoredHttp(url)) return; resources.outcome({ url, method, status, ... })`. Responses matching its ignore patterns are not recorded, so "every" is too strong.
- Fix: range changed to 2194-2227 (SKILL reference and sources.yaml), and "every response" qualified with "outside its ignore patterns".

### F6 references/sources.yaml:113 — WARNING (line reference)
- Said: "line 12 per-context storage and cookies; newContext example".
- Source: browser-contexts.md v1.65.0: line 12 is the "own local storage, session storage, cookies etc." paragraph; the first `browser.newContext()` example is line 44.
- Fix: "line 12 per-context storage and cookies; line 44 newContext example".

### F2 SKILL.md:22 and references/common-mistakes.md:5 — WARNING (hypothetical reported as observed)
- Said: "positional locators selected "a similar element", causing "a transition to a different state than expected"" / "a positional locator selected "a similar element"".
- Source: ICST 2010 p.129 (pngs/page-002.png), "State Transitions": "A worse scenario is that a similar element is mistakenly selected, which causes a transition to a different state than expected. For instance, consider a test case that uses the XPath expression of the remove clickable of the Cleaning item ... will remove the Groceries item instead". The paper presents a possible scenario with a constructed TODO example, not an observed incident.
- Fix: "selected" changed to "can select" in both places.

### F3 references/state-abstraction.md:17 — WARNING (misstated subject)
- Said: "one Google Reader attribute alone could yield "200+ state differences" per state".
- Source: ICST 2010 p.134 (pngs/page-007.png): "ATUSA strips the predefined HTML attributes (closure_hashcode_[a-zA-Z0-9]+), which are different after every load, and could easily result in 200+ state differences alone per state." A pattern of attributes, not one attribute.
- Fix: "Google Reader's `closure_hashcode_[a-zA-Z0-9]+` attributes alone could yield".

### F1 references/common-mistakes.md:9 and references/playwright-crawl-loop.md:43 — WARNING (stronger than source)
- Said: "ATUSA used a back-end reset on URL load and a per-run SQL reset ([TSE 2012, pp.44, 48])" and "ATUSA reset the back end on URL load and TUDU's database by SQL script per run".
- Source: TSE 2012 p.44 (page image pngs/page-009.png), Table 3 "Plugin Types": row `OnUrlLoadPlugin` | "After the initial URL is (re)loaded" | Examples: "Reset back-end state". This is a plugin extension point with an example use, not a report that ATUSA reset the back end. (The TUDU SQL reset per run is on p.48 and stands.)
- Fix: reworded both to "ATUSA's plugin types include a back-end reset after the initial URL is (re)loaded".

### Checked and entailed so far (no finding)
- Playwright v1.65.0: aria-snapshots.md lines 142-146, 214-217, 224-225, 252; class-page.md 171, 399, 534-536, 2346-2352, 4442-4482, 4966-4970, 5117-5126; params.md 7, 1007; class-browsercontext.md 295-300; actionability.md 8-9, 38, 46-48, 52, 124; locators.md 192, 1730-1732; auth.md 115; clock.md 8-20; class-tracing.md 150-158; network.md 411-470. Every quote exact.
- react.dev at 7594a2b: createRoot.md 48-50, 358; Component.md 1272, 1275-1280; act.md 7; Suspense.md 7; useTransition.md 44. Every quote exact.
- Crawljax GitHub API: language Java, pushed_at 2023-09-18T07:08:58Z, archived false.
- chaosbringer crawler.ts at 5f69d89: 277-278 (`visited`, `queue`), 575-577 (quote exact), 917-925 (`visited.has(normalizeUrl(entry.url))` skip, `visited.add`; FIFO `queue.shift()` in the live-crawl branch). aria-snapshot.ts:170 `node.attrs.cursor === "pointer"` returns "button". action-targets.ts:516-530 `selectorFor`: `:has-text` for text under 50 chars, then aria-label/placeholder/name attributes, then `:nth-match([role=...])`. README line 3 quote exact. package.json line 3 `"version": "0.15.0"`, line 19 `"node": ">=22"`.
- playwright-cli SKILL.md at 95e5dca: description "Automate browser interactions, test web pages and work with Playwright tests."
- Playwright docs contain no statement about unhandled promise rejections in class-page.md or class-browsercontext.md (grep for "rejection"/"unhandled": only the webError line), so oracles-per-state.md:7's "not described in those docs" holds.

### Paper quotations confirmed on the page image (word for word)
- TSE 2012 (Mesbah_2012_InvariantBasedAutomaticTesting/pngs): p.39 "can cause problems (delete items or log the user out)" (page-004); p.40 "can also be too permissive, grouping DOM trees that should be considered different" and "there is no guarantee that we find the same element on the DOM-tree and can reach the exact same state" (page-005); p.41 error strings "404 Not Found", "500 Internal Server Error", "Session Timeout", "MySQL error", Table 2, NOT/OR/AND/NAND, preconditions (page-006); p.42 "Source - Action -> Target", logoff example, dead clickables, Back button, JS-variable invariants (page-007); p.43 "the error report along the causing execution path ... can be easily reproduced later", other-browser use (page-008); p.44 Table 3 and "whether a reported failure is caused by a real fault or a legal change" (page-009); p.46 "leading to a (slowly) growing DOM tree", at-most-one-calendar invariant (page-011); p.48 "silently swallowed by the JAVASCRIPT engine and did not affect the DOM", 8 of 10, depth 3 past 60 minutes without changing fault detection, SQL reset per run, `A:title=Log out` exclusion (page-013); p.50 "just running CRAWLJAX would correspond to conducting a smoke test", "it is very hard to determine when a failure occurs", "The hardest part is deciding which application-specific invariants to adopt" (page-015). p.38 Algorithm 2 `testInvariants(ns)` and p.47 HitList exclusions confirmed against the paper-reader notes (not quoted in the skill).
- ICST 2010 (Roest_2010_RegressionTestingAjaxApplications/pngs): pp.128-129 nondeterminism list (page-001/002); p.129 "a similar element", "a transition to a different state than expected" (page-002, see F2); pp.129-130 "can have the side-effect of missing real bugs because they are too broad" (page-003); p.131 "event handler(s), attributes, children nodes, and text value", stripped-DOM hash (page-004); p.132 "to check whether differences are falsely ignored by the comparators" (page-005); p.134 "Using only the generic comparators would result in a false negative, namely the leading-zero bug", "many wrong transitions", "The time between crawling and testing also had a large influence on the number of the found state differences", "200+ state differences" (page-007); p.135 "an incomplete DOM state could be compared with a complete state", clean-up plugin and `oneTimeTearDown` (page-008).
- TWEB 2012 (Mesbah_2012_CrawlingAjaxBasedWebApplications/pngs): p.5 "since the event model maintaining the handler registration information is separated from the DOM" (page-004); p.26 cookies and Web storage, "an instance" / not necessarily "the" instance (page-025); p.27 fixed wait slow when high, completion flag "more reliable", used on AdSense (page-026). Unquoted TWEB claims (pp.8-11, 18-21, 24) checked against the paper-reader notes.
- BLeak (Vilk_2018_BLeakAutomaticallyDebuggingMemoryLeaks/pngs): PDF p.5 "the default setting is eight" (page-004); PDF p.11 false positives (page-010, see F4). PDF pp.2, 4, 6 claims (round-trip oracle, `check`/`next` loop, growth between every consecutive snapshot) checked against the paper-reader notes; not quoted in the skill.

### Judged entailed, no edit
- SKILL.md:18 and TWEB p.27 "a fixed wait is slow or unsafe": the page says a high wait is slow and partially loaded DOMs hurt accuracy; "unsafe" is a fair compression.
- playwright-crawl-loop.md:36 "will click a button that is disabled during a server check": actionability.md:124-126 describes the disabled button being replaced by an enabled one that Playwright then clicks; the sentence does not claim a click on a disabled element.
- SKILL.md:22 "each context "has its own local storage, session storage, cookies etc."": the source sentence's subject is "each test", achieved through one BrowserContext per test (same paragraph); quoted words are exact.

## Validation (run after the fixes)
- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/ui-state-exploration` → `Skill is valid!` (exit 0).
- Relative links: SKILL.md → references/state-abstraction.md, playwright-crawl-loop.md, oracles-per-state.md, common-mistakes.md; playwright-crawl-loop.md → state-abstraction.md, oracles-per-state.md. All resolve.
- Cited URLs vs sources.yaml `url:` entries: no URL in the markdown missing from sources.yaml, none in sources.yaml unused (`comm` both ways empty).
- Trailing whitespace: `grep -rnE '[[:space:]]+$' SKILL.md references/` → no matches (exit 1).
- Not committed, not pushed.
