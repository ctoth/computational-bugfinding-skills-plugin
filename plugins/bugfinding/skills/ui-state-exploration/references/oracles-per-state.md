# Per-state oracles and hand-offs

Invariants are what turn a crawl into a test. ATUSA checks them on every new state inside the crawl loop ([Mesbah et al., TSE 2012, p.38](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)) and states that without them "it is very hard to determine when a failure occurs" ([TSE 2012, p.50](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Choosing the contract belongs to `correctness-oracles`; this file covers where and when checks run during exploration.

## Generic checks on every event and new state

- **Uncaught page errors.** `pageerror` is "Emitted when an uncaught exception happens within the page"; context `webError` is "Emitted when exception is unhandled in any of the pages in this context" ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md); [Playwright BrowserContext API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-browsercontext.md)). Unhandled promise rejections are not described in those docs; chaosbringer's source says that in Chromium they fire both the DOM event and `pageerror` ([crawler.ts:575-577](https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/src/crawler.ts)). Firefox and WebKit behaviour is unverified, so capture the `unhandledrejection` DOM event too.
- **Console errors.** `console` is "Emitted when JavaScript within the page calls one of console API methods" ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md)). "By default, React will log all errors to the console" ([react.dev createRoot](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/createRoot.md)).
- **Dead clickables.** ATUSA detects events whose server request fails from request and response traffic, because the Ajax engine hides server errors from the DOM ([TSE 2012, p.42](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). In Playwright, "HTTP Error responses, such as 404 or 503, are still successful responses from HTTP standpoint", so they complete with `requestFinished`, not `requestFailed` ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md)). Attribute HTTP status codes of finished requests to the event that caused them.
- **Error text in the page.** ATUSA's generic invariant rejects strings such as "404 Not Found", "500 Internal Server Error", "Session Timeout" and "MySQL error", from a configurable list ([TSE 2012, p.41](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Add the target's own error banners and the React error-boundary fallback.
- **Structure and accessibility.** ATUSA also checks DOM validity and accessibility per state ([TSE 2012, p.41](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Use these only where the target claims them.

DOM-only checks are not enough: two of ten seeded TUDU faults "were silently swallowed by the JAVASCRIPT engine and did not affect the DOM" ([TSE 2012, p.48](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)).

## React error channels

An error boundary lets React "display some fallback UI instead of the part that crashed" ([react.dev Component](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/Component.md)). A boundary-caught render error therefore appears as fallback UI and a console log, not as `pageerror` (inference from the two docs, not executed). Check for the target's fallback in each state.

Boundaries "do not catch errors for" event handlers, server-side rendering, errors in the boundary itself, and asynchronous code such as `setTimeout` callbacks, except inside `startTransition` ([react.dev Component](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/Component.md)). Expect those to surface as uncaught errors (inference).

Where the target can be configured, the root options `onCaughtError`, `onUncaughtError` and `onRecoverableError` report caught, uncaught and recovered errors; "Some recoverable errors may include the original error cause as `error.cause`" ([react.dev createRoot](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/createRoot.md)). Route the choice of these channels to `correctness-oracles`.

## Application invariants with preconditions

ATUSA expresses application invariants as an XPath that must match, a regex on the DOM string, a JavaScript expression that must be true, a URL condition, or a visible element, combined with NOT, OR, AND, NAND, and each limited to states by a precondition ([TSE 2012, p.41](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Invariants can also read JavaScript variables ([TSE 2012, p.42](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). In Playwright, evaluate such checks once on the settled state; an auto-retrying assertion waits "until the condition is met" ([Playwright actionability](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/actionability.md)) and passes over a transient violation. "The hardest part is deciding which application-specific invariants to adopt" ([TSE 2012, p.50](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)).

A structural invariant can expose growth: in TaskFreak, an invariant allowing at most one calendar element revealed that cancelling a pop-up left its element in the DOM, "leading to a (slowly) growing DOM tree" ([TSE 2012, p.46](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Treat that as a leak candidate for `resource-complexity-testing`, not a confirmed leak.

## Graph checks after the crawl

ATUSA checks the Back button returns to the expected state and checks temporal "Source - Action -> Target" properties over the inferred graph, for example logoff from any state reaches the logged-off state ([TSE 2012, p.42](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)). Add reload consistency where the app promises it.

## Classify each violation

Keep the evidence needed to decide "whether a reported failure is caused by a real fault or a legal change": ATUSA's report includes the DOM diff, a screenshot, the fired event sequence and the applied comparators ([TSE 2012, p.44](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)); Roest's also shows the stripped and full DOMs ([Roest et al., ICST 2010, p.132](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Replay the path in a fresh context before reporting; a violation that does not replay stays visible as unreplayed.

## Hand-offs

- **Cycles to leak checks.** A path A to ... to A with stable locators and a settle predicate is a BLeak-style loop. BLeak's oracle is growth across repeated returns to the same visual state, requires growth between every consecutive snapshot, defaults to 8 round trips, and its only false positives were structures growing to a cap or timeout, removed by more round trips ([Vilk and Berger, BLeak, PDF pp.2, 5-6, 11](https://raw.githubusercontent.com/plasma-umass/BLeak/2b2db0832ea412fa56683de045420134e3c3aa79/paper.pdf)). BLeak loops are hand-written lists of states with `check` and `next` functions ([BLeak, PDF p.4](https://raw.githubusercontent.com/plasma-umass/BLeak/2b2db0832ea412fa56683de045420134e3c3aa79/paper.pdf)); a discovered cycle supplies those states. Confirmation belongs to `resource-complexity-testing`.
- **Failing paths.** Path, inputs, normalizer list and trace go to `failure-reduction` and `evidence-based-triage`.
- **Loading windows.** Suspected bugs in disabled or loading windows, or in response order, go to `schedule-exploration`.
- **Understood regions.** A graph region whose behaviour is understood can become a model for `stateful-property-testing`.
- **Configurations.** The same crawl in two browsers or builds, compared state by state, goes to `configuration-differential-testing`; ATUSA lists running its generated tests in another browser to find incompatibilities as one use ([TSE 2012, p.43](https://people.ece.ubc.ca/amesbah/resources/papers/tse11.pdf)).
