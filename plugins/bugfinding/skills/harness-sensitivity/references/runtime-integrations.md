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
