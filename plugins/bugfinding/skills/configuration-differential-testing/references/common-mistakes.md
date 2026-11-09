# WRONG / RIGHT configuration decisions

Each entry is **Wrong** first, then **Right**, then why.

## Treating pairwise coverage as all bugs found

**Wrong:** "The 2-way array passed, so the configuration space is clean."

**Right:** Report modeled tuple coverage and remaining interactions; fault estimates need a profile and exercised premises, and fault coverage "is only an approximation" ([Kuhn et al., §III, p.5](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

**Why:** "faults are not necessarily uniformly distributed across the input space", so uncovered tuples can hold the failures.

## Deleting invalid generated rows

**Wrong:** Generate unconstrained rows, drop the invalid ones, and keep the coverage claim.

**Right:** Generate with supported constraints, as PICT advises to "eliminate disallowed combinations during the generation process" ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** "an offending test case may cover other, possibly valid, pairs that would not otherwise be tested."

## Excluding a promised configuration because it fails

**Wrong:** Add `IF [Backend] = "accelerated" THEN [Capability] = "present";` after the fallback lane crashes.

**Right:** Keep it as a candidate; derive restrictions from the real contract, since constraints "express inherent limitations of the modelled domain" ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** a constraint written to remove red output hides the failing supported tuple from every later run.

## Assuming every regression row was retained

**Wrong:** Pass `/e:regressions.tsv` and treat every listed row as executed.

**Right:** Inspect seed omissions and preserve regression evidence independently; a seed row violating constraints "will be skipped entirely" ([PICT, Seeding](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** unknown columns and values are also ignored, so a complete regression row can silently become partial.

## Misreading `/s` and `/t`

**Wrong:** Use `/s` to save the test matrix or `/t` as subject concurrency.

**Right:** `/s` will "Show model statistics" instead of rows, and `/t` sets generator worker threads ([parser, `showUsage`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp), [producer, `execute`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp)).

**Why:** with `/s` the producer prints statistics and no rows; parallelism "never changes the produced test suite" and runs no target ([PICT, Parallelism](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

## Counting generated rows as exercised semantics

**Wrong:** Report the generated row count as the tested configuration space.

**Right:** Save effective configuration and actual property evaluations; modeled tuple coverage is not detected-fault evidence ([Kuhn et al., §II, p.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

**Why:** "When test sets do not include settings corresponding to actual faults, the faults will not be detected"; an unapplied or ineffective setting includes nothing.

## Using aliases for distinct behavioral modes

**Wrong:** `Codec: zstd | lz4` because both are "compressed".

**Right:** Model distinct behavior as separate values; for aliases "only the first name counts" in constraints ([PICT, Aliasing](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md), [value methods, `GetNamesForComparisons`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp)).

**Why:** aliases "do not change the combinatorial complexity of the model", so the second spelling gets no interactions of its own.

## Publishing a guessed Advanced ACTS command

**Wrong:** Write an Advanced ACTS command line from memory.

**Right:** Verify the acquired artifact; the NIST page offers Basic directly but says of "the advanced ACTS tool, which supports constraints" to "please send a request" ([NIST distribution, Downloadable Tools](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools)).

**Why:** an unacquired tool's interface is unverified, and the page names constraint support only for the advanced tool.

## Assuming the browser time zone setting covers the server

**Wrong:** Set Playwright `timezoneId` and treat both the server render and the browser as running in that zone.

**Right:** Set the server process `TZ` separately and record both; Node reads the `TZ` environment variable ([Node CLI, `TZ`](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/cli.md)).

**Why:** Playwright's setting "only affects the browser timezone and locale, not the test runner timezone" ([Playwright emulation](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/emulation.md)).

## Treating the requested `NODE_ENV` as the loaded React build

**Wrong:** Start the browser tests with `NODE_ENV=production` and label the lane "React production".

**Right:** Check the build that actually loaded, for example with the proposed, unexecuted probe `typeof React.captureOwnerStack`, which is "`undefined` in production builds" ([captureOwnerStack](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/captureOwnerStack.md)).

**Why:** React picks its build from `process.env.NODE_ENV` when its module loads ([react npm index](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react/npm/index.js)), so what counts is the value the bundle saw, not the variable set on the test command.

## Reporting Playwright WebKit as Safari

**Wrong:** "The `webkit` project passed, so Safari is covered."

**Right:** Report it as Playwright WebKit at a recorded version.

**Why:** Playwright's WebKit "is derived from the latest WebKit main branch sources" and Playwright "doesn't work with the branded version of Safari" ([Playwright browsers](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/browsers.md)).

## Using a hard-coded Node.js version list

**Wrong:** `Node: 20, 22, 24, 26, 27` copied from an old matrix.

**Right:** Take the supported set from the target's `engines` and CI, checked against the current nodejs/Release table ([README](https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/README.md)).

**Why:** 20.x reached end of life on 2026-04-30 and 27.x was Alpha on 2026-11-09 ([schedule.json](https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/schedule.json)); an end-of-life or pre-release lane is not a supported configuration.

## Assuming ESM fuzzing on Node.js 26 is instrumented

**Wrong:** "Jazzer.js needs Node.js 20.6 for ESM, and this lane runs 26, so ESM code is instrumented."

**Right:** Check each Node × Load lane for the Jazzer.js ESM warnings and for rising coverage on ESM code ([Jazzer.js fuzz targets](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/docs/fuzz-targets.md)).

**Why:** its ESM path calls `module.register` and on failure prints a warning and continues uninstrumented ([instrument.ts](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/packages/instrumentor/instrument.ts)); Node.js 26 runtime-deprecates that API as DEP0205 ([Node deprecations](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/deprecations.md)).
