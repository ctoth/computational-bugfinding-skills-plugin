# Runtime integrations for existing mutation setups

Read only the applicable integration. These are primary-documented entrypoints checked on 2026-11-07 at the commits pinned in each link, not commands executed for this skill. Select a compatible tool release and project runner before execution; documentation and runtime requirements can change. Prefer current project regressions/controls when they answer the audit without a new dependency.

## JVM: PIT with Maven

PIT is Apache-2.0 licensed ([PIT LICENSE.txt](https://raw.githubusercontent.com/hcoles/pitest/1edd5b4e14fbe3a7169d79bc179ac2f4cc5e417c/LICENSE.txt)). Use an existing `org.pitest:pitest-maven` integration with compatible JVM/test-runner configuration. Narrow `targetClasses` and `targetTests` to the relevant owner; "By default pitest will mutate all code in your project". From that Maven project, the documented goal is ([PIT Maven, Getting started and mutationCoverage goal](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/maven.markdown)):

```text
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

Inspect the generated per-mutant report and exact rejecting test. Bytecode requires line-number/source-file metadata; preserve nonviable, uncovered and runner-error cases separately ([PIT basic concepts, Mutation Operators and Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)). Dry-run mode, "Introduced in 1.17.3", gathers coverage and mutants "without running any tests against the mutants". Cross-module mutation also needs deliberate class ownership: without each class "reported only once, the results are undefined" ([PIT Maven, Dry Run Mode and Cross module tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/maven.markdown)).

## JavaScript/TypeScript: StrykerJS

StrykerJS is Apache-2.0 licensed ([StrykerJS LICENSE](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/LICENSE)). From an already configured compatible project, use the project's installed runner integration ([StrykerJS getting started, 3 Let's kill some mutants](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/getting-started.md)):

```text
npx stryker run
```

Inspect `mutate`, actual test-runner support, any build command and validity checker. Per-test coverage requires a supporting runner. The default `command` runner "bases the result on the exit code of that program", so a killed mutant under it shows only a nonzero exit; read the rejecting assertion from the test output. Coverage analysis lets Stryker distinguish between `"Survived" and "NoCoverage"`, and the `command` runner is excluded from it. Command-line values "**completely replace** (**not** supplement !)" their corresponding configuration values ([StrykerJS configuration, Command Line vs. Config File, coverageAnalysis and testRunner](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/configuration.md)).

For a newly authorized setup, the documented `npm init stryker@latest` "will first install Stryker and then run the Stryker initializer"; it is not a read-only prerequisite check ([StrykerJS getting started, 2 Install](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/getting-started.md)). Verify the chosen package's Node/test-runner requirements rather than assume one runtime floor; at the checked commit, `@stryker-mutator/core` 10.1.1 declares `"node": ">=22.0.0"` ([StrykerJS core package.json, engines](https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/packages/core/package.json)). Retain the per-mutant states alongside the score; use [control design](control-design.md) to identify what each actually establishes.

## .NET: Stryker.NET

Stryker.NET is Apache-2.0 licensed ([Stryker.NET LICENSE](https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/LICENSE)). Inspect an existing tool manifest and installed release. The checked documentation says "Stryker requires the dotnet 10 runtime or newer" while "Your application does not need to target dotnet 10 or newer"; .NET Framework builds also need NuGet. Recheck the selected release rather than retarget the application ([Stryker.NET getting started, Install prerequisites](https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/docs/getting-started.md)).

For an existing local tool manifest, restoration uses `dotnet tool restore`. From the "*unit test* project dir", the documented execution is ([Stryker.NET getting started, Install in project, Prepare and Let's kill some mutants](https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/docs/getting-started.md)):

```text
dotnet stryker
```

Restoring tools changes local dependencies; use the task's existing authority. These commands do not make the integration applicable to Go, Rust or Python. No mutation backend for those runtimes is prescribed here; existing targeted regressions and fault controls remain usable audit inputs.

## Optional reachability evidence

Where a compatible OSS-Fuzz integration exists, Fuzz Introspector can compare static reachable code with observed execution. Its checked page covers "projects written in C/C++, Python and Java" with specific LLVM LTO/Gold, PyCG or Soot build dependencies; do not infer Go support ([Fuzz Introspector, introduction and Differences in build tooling](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)). Reachability output diagnoses a missing producer or blocked path; it does not replace the healthy/faulty oracle observation.

## JavaScript/TypeScript: reachability, order and leak probes

Checked on 2026-11-09 at the pinned commits; not executed for this skill. Use the project's existing runner and coverage tool. For mutation testing use the StrykerJS section above.

### Coverage answers the Producer step only

- **c8:** "By default v8 will only give us coverage for files that were loaded by the engine", so a producer file the tests never loaded is absent from the report rather than shown at 0%. `--all` adds unloaded files under `--src` "with a default of 0% coverage". `/* c8 ignore next */` and `start`/`stop` comments remove lines. At the checked commit, c8 declares `"node": "^20.19.0 || ^22.12.0 || >=23"` ([c8 README, Checking for "full" source coverage using --all and Ignoring Uncovered Lines, Functions, and Blocks](https://raw.githubusercontent.com/bcoe/c8/ae5a0cf4349b92cac910cf7275e724ab7a725b9d/README.md), [c8 package.json, engines](https://raw.githubusercontent.com/bcoe/c8/ae5a0cf4349b92cac910cf7275e724ab7a725b9d/package.json)).
- **node:test:** with `--experimental-test-coverage`, "Node.js core modules and files within `node_modules/` directories are, by default, not included in the coverage report" unless `--test-coverage-include` names them; test files are excluded too, and `/* node:coverage ignore next */` comments remove lines ([Node test, Collecting code coverage](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)). `NODE_V8_COVERAGE` "will automatically propagate to subprocesses" ([Node CLI, NODE_V8_COVERAGE](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/cli.md)).
- **Jest:** `coverageProvider` values "are `babel` (default) or `v8`" ([Jest configuration, coverageProvider](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/Configuration.md)). Say which provider produced a reachability claim.
- **Vitest:** the default `v8` provider "Does not work on environments that don't use V8, such as Firefox or Bun"; use the `istanbul` provider there ([Vitest coverage guide](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/guide/coverage.md)).

Check that the claimed producer file and function appear and executed, and that no ignore comment covers them. Activation, state, observation and rejection still need the healthy/faulty comparison.

### Order randomization probes leaked state

- **node:test:** `--test-randomize` randomizes "both discovered test files and queued tests within each file" and prints "Randomized test order seed: 12345"; `--test-random-seed=<number>` replays the order and enables randomization by itself. It is not supported with `--watch`. When subtests are awaited one by one, "the runner keeps declaration order instead of randomizing it" ([Node test, Randomizing tests execution order](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)). The flags were added in v26.1.0 and in v24.16.0 on the 24 LTS line ([Node CLI v26.13.0](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/cli.md), [Node CLI v24.22.2, --test-randomize](https://raw.githubusercontent.com/nodejs/node/f7f273a9bb6445f6f7fb6349105e7532972045fb/doc/api/cli.md), [CHANGELOG_V24, 24.16.0](https://raw.githubusercontent.com/nodejs/node/f7f273a9bb6445f6f7fb6349105e7532972045fb/doc/changelogs/CHANGELOG_V24.md)). Under default process isolation each file runs in its own child process; with `--test-isolation=none` tests can "interact with each other in ways that are not possible when isolation is enabled" ([Node test, Test runner execution model](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)). Inference from that model: under process isolation, file-order shuffling can expose only state shared outside the process (files, databases, ports); in-file shuffling exposes in-memory leakage.
- **Jest:** `--randomize` shuffles "the order of the tests within a file" and is "only supported using the default `jest-circus` test runner"; `--seed` also orders test suites, and `--showSeed` prints the seed. "When dealing with flaky tests, rerunning with the same seed might help reproduce the failure" ([Jest CLI, --randomize, --seed and --showSeed](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md)).
- **Vitest:** `sequence.shuffle` helps "track tests that accidentally depend on another test run previously"; `sequence.seed` defaults to `Date.now()` ([Vitest sequence](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/config/sequence.md)). The page does not say the seed is printed, so set `--sequence.seed` explicitly for every recorded run.

A shuffled failure shows an order-dependent pair, not which test leaked. Keep the seed and both orders as replay evidence; a shuffled pass covers only what was shuffled.

### Leaked async work and open handles

- **node:test:** async activity can outlive its test, and the runner "does not delay the reporting of test results in order to accommodate it"; only errors from it and subtests created too late are reported ([Node test, Extraneous asynchronous activity](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)). Silent leaked mutation needs an order probe or a state observation.
- **Jest:** `--detectOpenHandles` "implies `--runInBand`, making tests run serially" and is implemented using `async_hooks`, so a flake that disappears under it is not shown fixed. `--forceExit` "is an escape-hatch"; when Jest does not exit, "external resources are still being held on to or timers are still pending". `openHandlesTimeout` (default `1000`) prints a warning about "probable open handles" ([Jest CLI, --detectOpenHandles and --forceExit](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md), [Jest configuration, openHandlesTimeout](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/Configuration.md)). Read the project config for `forceExit` before concluding there is no leak.
