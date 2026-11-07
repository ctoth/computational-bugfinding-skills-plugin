# Runtime integrations for existing mutation setups

Read only the applicable integration. These are primary-documented entrypoints checked on 2026-11-07, not commands executed for this skill. Select a compatible tool release and project runner before execution; documentation and runtime requirements can change. Prefer current project regressions/controls when they answer the audit without a new dependency.

## JVM: PIT with Maven

PIT is Apache-2.0 licensed ([PIT repository](https://github.com/hcoles/pitest)). Use an existing `org.pitest:pitest-maven` integration with compatible JVM/test-runner configuration. Narrow `targetClasses` and `targetTests` to the relevant owner. From that Maven project, the documented goal is ([PIT Maven](https://pitest.org/quickstart/maven/)):

```text
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

Inspect the generated per-mutant report and exact rejecting test. Bytecode requires line-number/source-file metadata; preserve nonviable, uncovered and runner-error cases separately ([PIT concepts](https://pitest.org/quickstart/basic_concepts/)). Dry-run mode, introduced in PIT 1.17.3, gathers coverage and mutants without mutant test execution. Cross-module mutation also needs deliberate class ownership to avoid duplicated/undefined aggregation ([PIT Maven](https://pitest.org/quickstart/maven/)).

## JavaScript/TypeScript: StrykerJS

StrykerJS is Apache-2.0 licensed. From an already configured compatible project, use the project's installed runner integration ([StrykerJS getting started](https://stryker-mutator.io/docs/stryker-js/getting-started/)):

```text
npx stryker run
```

Inspect `mutate`, actual test-runner support, any build command and validity checker. Per-test coverage requires a supporting runner. Command-line values replace their corresponding configuration values rather than extending them ([StrykerJS configuration](https://stryker-mutator.io/docs/stryker-js/configuration/)).

For a newly authorized setup, the documented `npm init stryker@latest` both installs and initializes configuration; it is not a read-only prerequisite check. Verify the chosen package's Node/test-runner requirements rather than assume one runtime floor ([StrykerJS getting started](https://stryker-mutator.io/docs/stryker-js/getting-started/)). Retain the per-mutant states alongside the score; use [control design](control-design.md) to identify what each actually establishes.

## .NET: Stryker.NET

Stryker.NET is Apache-2.0 licensed. Inspect an existing tool manifest and installed release. The checked documentation requires a .NET 10+ tool runtime while explicitly allowing applications targeting older frameworks; .NET Framework builds have additional NuGet prerequisites. Recheck the selected release rather than retarget the application ([Stryker.NET getting started](https://stryker-mutator.io/docs/stryker-net/getting-started/)).

For an existing local tool manifest, restoration uses `dotnet tool restore`. From the unit-test project directory, the documented execution is ([Stryker.NET getting started](https://stryker-mutator.io/docs/stryker-net/getting-started/)):

```text
dotnet stryker
```

Restoring tools changes local dependencies; use the task's existing authority. These commands do not make the integration applicable to Go, Rust or Python. No mutation backend for those runtimes is prescribed here; existing targeted regressions and fault controls remain usable audit inputs.

## Optional reachability evidence

Where a compatible OSS-Fuzz integration exists, Fuzz Introspector can compare static reachable code with observed execution. Its checked page documents C/C++, Python and Java with specific LLVM LTO/Gold, PyCG or Soot build dependencies; do not infer Go support ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)). Reachability output diagnoses a missing producer or blocked path; it does not replace the healthy/faulty oracle observation.
