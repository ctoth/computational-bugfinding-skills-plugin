# State abstraction and equivalence

The state key decides which states the crawl merges. There is no single correct key: coarser equality gives a smaller, more abstract graph, and the right level depends on the use ([Mesbah et al., TWEB 2012, pp.18-19](https://doi.org/10.1145/2109205.2109208)). Choose the key for the bugs being hunted and record it with the graph.

## Normalizer pipeline

Use the comparator pipeline from Roest et al.: each comparator strips one targeted difference (by regex or XPath), its output feeds the next, and a plain string comparison decides equality; a hash of the stripped state is stored per state ([ICST 2010, pp.129-131](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Give each normalizer a name, the difference it removes, and a precondition naming the states where it applies. Roest et al. added preconditions because generic comparators "can have the side-effect of missing real bugs because they are too broad" ([ICST 2010, pp.129-130](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)).

Templates for repeating structures (lists, tables) make more states equivalent and shrink the state space; an augmented template can serve as an invariant ([ICST 2010, pp.130-131](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). The same mechanism hid a fault: a phone number saved without its leading zero was ignored by the generic Table comparator and caught only by a custom contact template ([ICST 2010, pp.133-134](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)).

Inspect what each normalizer removed. Roest's failure report shows stripped and full DOMs "to check whether differences are falsely ignored by the comparators" ([ICST 2010, p.132](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Keep at least one planted difference that a correct key must distinguish, and check that the pipeline still separates it after every normalizer change; `harness-sensitivity` owns that control in general.

## Remove nondeterminism at the source

Roest et al. name the sources: "(HTTP) network delays, asynchronous client/server interactions, non-sequential handling of requests by the server, randomly produced or constantly changing data" ([ICST 2010, pp.128-129](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)). Prefer fixing the input over stripping the output. Playwright's `setFixedTime` "Sets the fixed time for `Date.now()` and `new Date()`" ([Playwright clock](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/clock.md)), and `route.fulfill` serves a fixed response for a matched request ([Playwright network](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/network.md)). A stubbed endpoint no longer exercises the real server, so record which endpoints were fixed.

Drift between runs is real: "The time between crawling and testing also had a large influence on the number of the found state differences", and Google Reader's `closure_hashcode_[a-zA-Z0-9]+` attributes alone could yield "200+ state differences" per state ([ICST 2010, p.134](https://people.ece.ubc.ca/amesbah/resources/papers/icst10.pdf)).

## Aria snapshots as a coarse key

An aria snapshot is a YAML rendering of the accessibility tree with roles, attributes, values and text content ([Playwright aria snapshots](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/aria-snapshots.md)). `Page.ariaSnapshot` (since v1.59) takes `mode` (`"ai"` adds element references like `[ref=e2]` and iframe snapshots) and `depth` ("limits the depth of the snapshot"); `Page.ariaSnapshotJSON` (since v1.63, JS only) "Returns the same tree" as JSON ([Playwright Page API](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/api/class-page.md)).

Treat the snapshot as one normalizer, not a free pass. It omits CSS-only differences (inference from the documented fields). A `depth` limit drops subtrees. When matching against a template, the comparison "normalizes whitespace within names and text values", is "order-sensitive", and an omitted attribute means "the test will pass regardless of the checkbox state" ([Playwright aria snapshots](https://raw.githubusercontent.com/microsoft/playwright/v1.65.0/docs/src/aria-snapshots.md)). Whether the same DOM yields identical snapshots across browsers is unverified; do not compare keys across browsers without checking.

## Deduplicate globally

Compare each new state against every visited state; a match adds only an edge ([TWEB 2012, p.9](https://doi.org/10.1145/2109205.2109208)). A JavaScript banner that kept changing the DOM made every examined candidate count as a clickable until a higher similarity threshold was set ([TWEB 2012, p.24](https://doi.org/10.1145/2109205.2109208)): when nearly every event creates a new state, look for an unnormalized volatile region before raising bounds.

## Worked example (illustration, not executed)

A todo app shows a "saved 3 seconds ago" label and a list of items. Two candidate keys:

1. Global list template plus a global relative-time regex. Every list length becomes one state, so a save that drops an item, or stores "0641" as "641", never produces a distinct state or a failed check.
2. Clock fixed with `setFixedTime`, so the label is stable; a relative-time normalizer kept only for a region the clock does not control, with a precondition naming that region; list items kept in the key with an invariant on their format.

Choose 2. Record both normalizer lists with the graph, and keep a planted item-format difference that key 2 must distinguish.
