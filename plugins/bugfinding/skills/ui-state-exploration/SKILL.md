---
name: ui-state-exploration
description: Guides model-free exploration of browser and React UI states by discovering clickable events, abstracting and deduplicating states, resetting and replaying paths, and checking oracles at every new state, driven by Playwright. Use when asked to crawl a web app, explore a React or single-page UI, or find bugs by clicking through an app; when bugs need unknown click and input paths and no operation model exists; or to find UI state cycles for leak checks.
---

# UI state exploration

Discover reachable UI states without a model and check each one as it appears. A crawl alone is not a test: "just running CRAWLJAX would correspond to conducting a smoke test" ([Mesbah et al., TSE 2012, p.50](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Choose `stateful-property-testing` instead when an operation model with preconditions exists or is cheap to write. Crawljax, the reference crawler, is Java and was last pushed 2023-09-18 ([repository](https://github.com/crawljax/crawljax)); write a small target-specific loop over Playwright, not a general crawler framework.

## Define the state key before crawling

Build the key from an aria snapshot or a filtered DOM, passed through an ordered list of named normalizers, each limited by a precondition to the states it applies to. Aria snapshots "provide a YAML representation of the accessibility tree", detailing "**roles**, **attributes**, **values**, and **text content**" ([Playwright aria snapshots](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/aria-snapshots.md)). Normalizers hide faults when broad: comparators "can also be too permissive, grouping DOM trees that should be considered different" ([TSE 2012, p.40](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)), and "Using only the generic comparators would result in a false negative, namely the leading-zero bug" ([Roest et al., ICST 2010, p.134](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Remove nondeterminism at its source first with `setFixedTime` ([Playwright clock](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/clock.md)) and `route.fulfill` ([Playwright network](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/network.md)). Compare each new state against all visited states, not only its parent ([Mesbah et al., TWEB 2012, p.9](https://doi.org/10.1145/2109205.2109208)). A URL is not a state key. Read [state abstraction](references/state-abstraction.md).

## Discover, fire and settle

Take candidates from interactive roles in the current snapshot, new ones first; Crawljax extracts candidates from the DOM diff and counts a candidate as a transition only if firing it changes the DOM under the chosen comparison ([TWEB 2012, pp.8-9](https://doi.org/10.1145/2109205.2109208)). Handlers registered with `addEventListener` are invisible to DOM inspection ([TWEB 2012, p.5](https://doi.org/10.1145/2109205.2109208)); record that blind spot. Exclude elements that "can cause problems (delete items or log the user out)" unless that path is the target ([TSE 2012, p.39](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)).

Wait on an app-specific settle predicate with `waitForFunction` ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md)). `'networkidle'` is "**DISCOURAGED**" ([Playwright params](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/params.md)); a fixed wait is slow or unsafe and an app completion flag is more reliable ([TWEB 2012, p.27](https://doi.org/10.1145/2109205.2109208)); comparing an incomplete DOM gives false failures ([ICST 2010, p.135](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Auto-wait hides early windows: Playwright will click a button "regardless of when the [`method: Locator.click`] call was made" ([Playwright actionability](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/actionability.md)). Read [crawl loop](references/playwright-crawl-loop.md).

## Reset and replay by path

Open a fresh browser context per replayed path; each context "has its own local storage, session storage, cookies etc." ([Playwright browser contexts](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/browser-contexts.md)), and cookies broke Crawljax's reload reset ([TWEB 2012, p.26](https://doi.org/10.1145/2109205.2109208)). Reset server state with a hook ([TSE 2012, p.44](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf); [ICST 2010, p.135](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Label edges by event, role and accessible name, re-resolved after reload: positional locators selected "a similar element", causing "a transition to a different state than expected" ([ICST 2010, p.129](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)), and aria refs "resolve against the latest snapshot" ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md)). Record a replay that lands in a different state as a nondeterminism finding; do not merge it silently.

## Check oracles at every new state

Attach generic checks (page errors, console errors, HTTP error responses, error-boundary fallback, error strings), application invariants with preconditions, and graph checks after the crawl ([TSE 2012, pp.38, 41-42](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). DOM-only checks miss faults "silently swallowed by the JAVASCRIPT engine" ([TSE 2012, p.48](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Read [per-state oracles and hand-offs](references/oracles-per-state.md).

## Bound, route and return

Bound depth, state count, time and exclusions; depth 1 to 2 grew one site from 148 to 1,071 states ([TWEB 2012, p.18](https://doi.org/10.1145/2109205.2109208)), and depth 3 exceeded 60 minutes without changing fault detection ([TSE 2012, p.48](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Default to your own Playwright loop. chaosbringer can serve as a random-crawl baseline and oracle harness where the target already uses it, but it deduplicates by URL only ([crawler.ts:917-925](https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/crawler.ts)).

- Model-based sequences with preconditions and shrinking: `stateful-property-testing`.
- Leak loops from discovered cycles: `resource-complexity-testing`.
- Contract and observation-channel design: `correctness-oracles`.
- Replay and path reduction: `failure-reduction`; attribution: `evidence-based-triage`.
- Races in loading windows and response reordering: `schedule-exploration`.
- Driver mechanics: Playwright's own skills, such as [`playwright-cli`](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/packages/playwright-core/src/tools/skills/playwright-cli/SKILL.md).

Return the normalizer list, states and labeled edges, unsettled and unreplayable paths, oracle evaluations and violations with replay traces, and blind spots. The graph is "an instance" of the state machine, not "the" instance ([TWEB 2012, p.26](https://doi.org/10.1145/2109205.2109208)); zero findings is a bounded result. Read [common mistakes](references/common-mistakes.md).
