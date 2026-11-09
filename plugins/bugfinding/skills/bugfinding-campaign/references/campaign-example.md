# Worked campaign: from valid programs to observable effects

This is an illustrative decision record, not a reported experiment or a finding against a real product. Its frontier is motivated by SQLite's joint state/input fuzzing and Elle's informative observation design ([SQLite §2](https://www.sqlite.org/testing.html), [Elle §3](https://arxiv.org/abs/2003.10554)).

## Given baseline and request

Suppose source inspection establishes that an interpreter project already has valid-IR source generation, cross-engine compilation/result/error comparison, persisted-bytecode mutation and transaction history checks. The current VM lane creates an empty world; its generated operations often fail before exercising an object permission transition. The user authorizes a finite discovery budget on disposable test state.

Do not propose valid-IR generation or basic cross-engine comparison as new capability. Read the actual permission contract, world-creation producer and effect-observation APIs. Confirm the apparent omission in the target revision before treating it as the experiment's premise. This applies reachability diagnosis, comparing "static reachability potential" with dynamic coverage, rather than substituting guessed behavior ([Fuzz Introspector, overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)).

## Candidate pilot

Write a compact record using the project's existing artifact convention:

```text
Target/config: inspected interpreter and reference builds; named core capabilities
Gap: successful permission-dependent effects are not exercised by the current lane
Contract: cite the precise documented permission/effect guarantee
Input: initial world + generated operation sequence; retain both
Oracle: permitted/denied outcome and relevant before/after world effects
Comparison: equivalent per-case starting states in both implementations
Control: a known or independently justified violation of this same contract
Budget: use a tranche of the user's finite envelope; include replay/triage time
Replay: original world, operations, exact builds/options and raw outcomes
```

The oracle must distinguish legal errors and intended implementation differences from wrong effects. More histories do not supply missing observations automatically; Elle's dependency inference depends on the recorded information ([Elle §§3 and 4.3](https://arxiv.org/abs/2003.10554)). Delegate detailed stateful generation and semantic comparison to their owners.

## Three possible pilot outcomes

1. **The operation is still almost never reached.** Preserve accepted-operation counters and inspect the generator's prerequisites. Spend the next tranche improving the state/operation relation, rather than multiplying identical workers. Joint state/input search is a mechanism worth testing, not a guaranteed source of bugs; SQLite reports it found "some obscure faults" missed by single-dimension fuzzers ([SQLite §4.1.3](https://www.sqlite.org/testing.html)).
2. **A repeatable wrong effect appears.** Preserve the original world, sequence, outputs and builds; allocate to reproducing and reducing that candidate with the same oracle. Keep the minimized case alongside the original. Reproduction depends on the actual testcase and compatible instrumentation/configuration: the testcase "contains the bytes that were fed to the" target, built with the reported sanitizer ([OSS-Fuzz reproduction, Fuzz target bugs and Build the image and the fuzzers](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/reproducing.md)).
3. **Deep effects are reached but no violation appears.** Report a useful bounded negative result. Continue only if remaining search and budget justify it, or pilot another evidence-backed dimension. Do not call the target correct or the new lane superior. Comparative claims require observations under matched conditions, with variation visible, as FuzzBench's "distribution of the reached coverages" shows ([FuzzBench report, Per-benchmark summary](https://raw.githubusercontent.com/google/fuzzbench/3234e151d70f6093272a9b4155e68ee57faf986c/docs/reference/report.md)).

## Close the record

Report actual consumed resources and property reach, candidate classifications and evidence paths, the decision on the remaining budget, and untested states/behaviors. If a failure is intermittent, retain its conditions and reproduction attempts; ClusterFuzz filters on reproduction reliability and job, and "tracks which platform issues reproduce on" ([ClusterFuzz triage, Filtering testcases and Crash statistics](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/triaging-new-crashes.md)).

The useful output is an executable experiment with a stated observation and a reasoned next allocation. Merely producing this proposal is not evidence of discovery power. Evaluate the skill on isolated raw artifacts without revealing the intended defect or forcing this particular method.

## Inventorying a JavaScript or TypeScript project

Read `package.json` `scripts` and `devDependencies` first, then each lane's configuration:

- **Jest:** `jest.config.js|ts|mjs|mts|cjs|cts|json` or the `"jest"` key in `package.json`; default `testMatch` covers `__tests__` directories and `*.spec`/`*.test` files; `projects` can hold several configurations ([Jest configuration](https://raw.githubusercontent.com/jestjs/jest/v30.5.2/docs/Configuration.md)).
- **Vitest:** `vitest.config.{ts,mts,cts,js,mjs,cjs}` first, then the `test` property of `vite.config.*` ([Vitest config](https://raw.githubusercontent.com/vitest-dev/vitest/v5.1.0/docs/config/index.md)); default `include` is `['**/*.{test,spec}.?(c|m)[jt]s?(x)']` ([Vitest include](https://raw.githubusercontent.com/vitest-dev/vitest/v5.1.0/docs/config/include.md)).
- **node:test:** `node --test` runs files such as `**/*.test.{cjs,mjs,js}` and `**/test/**/*.{cjs,mjs,js}`, plus TypeScript variants unless `--no-strip-types` is supplied ([Node test runner](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/test.md)).
- **Playwright:** `playwright.config.ts` `testDir`, `testMatch`, `projects`, `retries` and `use.trace` ([Playwright configuration](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-configuration-js.md)).
- **fast-check:** the `fast-check` dependency or its `@fast-check/jest` and `@fast-check/vitest` integrations ([`@fast-check/jest`](https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/packages/jest/package.json), [`@fast-check/vitest`](https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/packages/vitest/package.json)); read the properties themselves for what they generate.
- **StrykerJS:** `stryker.conf.*`, `.stryker.conf.*`, `stryker.config.*` or `.stryker.config.*` ([Stryker config file](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/config-file.md)); the default `testRunner` `'command'` "just runs all tests for all mutants" ([Stryker configuration](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/configuration.md)).
- **Jazzer.js:** `@jazzer.js/core` or `@jazzer.js/jest-runner`, and a Jest project with `"testRunner": "@jazzer.js/jest-runner"` matching `*.fuzz.js` ([Jazzer.js Jest integration](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/docs/jest-integration.md)).

Record retry settings as observation limits: Playwright `retries` turns a fail-then-pass test into "flaky" ([Playwright retries](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-retries-js.md)), and Jest `jest.retryTimes` and Vitest `retry` rerun failing tests ([Jest object API](https://raw.githubusercontent.com/jestjs/jest/v30.5.2/docs/JestObjectAPI.md), [Vitest retry](https://raw.githubusercontent.com/vitest-dev/vitest/v5.1.0/docs/config/retry.md)).
