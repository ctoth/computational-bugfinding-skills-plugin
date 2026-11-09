# Common mistakes

## Coverage is treated as rejection

**Wrong:** “The faulty line ran, so this oracle detects the fault.”

**Use instead:** establish the control's relevant state change and its propagation to the intended assertion.

**Why:** covering a mutant means it "reaches and executes the mutated code"; detecting it requires that "a test assertion fails or the test causes an exception" ([Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)). Static reachability is a third, separate signal ([Fuzz Introspector overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)).

## A tool's detected count substitutes for the witness

**Wrong:** “Mutation score increased, so the new effect checker works.”

**Use instead:** inspect the per-control outcome and rejecting check.

**Why:** Stryker's Detected is "`killed + timeout`", and runtime/compile errors are "not represented in your mutation score"; neither fact demonstrates rejection by a separate effect oracle ([Stryker mutant states and metrics](https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a4f816358a06701b7680d54bbb56180c19781c25/docs/mutant-states-and-metrics.md)).

## A survivor is automatically a missing assertion

**Wrong:** add assertions until every survivor dies.

**Use instead:** distinguish an uncovered path, equivalent/irrelevant mutation, missing prerequisite and genuinely unobserved violation.

**Why:** PIT separates "**No coverage**" from "**Survived**", and an equivalent mutant may behave "in exactly the same way as the original" or differently "in a way that is outside the scope of testing" ([PIT basic concepts, Equivalent Mutations and Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)). Stryker's state list glosses Survived as "You're missing a test for it" ([Stryker mutant states and metrics](https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a4f816358a06701b7680d54bbb56180c19781c25/docs/mutant-states-and-metrics.md)); treat that as the tool's default reading, not a diagnosis of this control.

## Setup failure is counted as a healthy/faulty distinction

**Wrong:** a mutant fails to load, but its nonzero exit is recorded as successful semantic detection.

**Use instead:** establish that both cases reach the intended checker and preserve its exact result.

**Why:** PIT reports a mutant that "could not be loaded by the JVM" as non viable and "something went wrong" as a run error, both separate from killed ([PIT basic concepts, Running the tests](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown)).

## A dry run is presented as sensitivity evidence

**Wrong:** “PIT generated mutants and coverage, so the tests caught representative faults.”

**Use instead:** preserve dry-run output as setup evidence.

**Why:** PIT's dry run generates mutants "without running any tests against the mutants" and is meant "to iron out any problems pitest has with the test suite" ([PIT Maven, Dry Run Mode](https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/maven.markdown#dry-run-mode)).

## Broad mutation replaces contract-specific controls

**Wrong:** maximize a generic score instead of checking the new recovery, world-effect or numerical guarantee.

**Use instead:** select controls that can violate that actual promise. Keep real regressions and unresolved cases; do not translate score into expected product bugs.

**Why:** missing algorithms, contexts and invariants can escape common operators, and for such faults "results derived from mutation analysis do not generalize" ([Just et al., §3.2](https://doi.org/10.1145/2635868.2635929)); selection evaluated on mutants can lower real-fault detection "even if the mutation score does not decrease" ([Just et al., §5](https://doi.org/10.1145/2635868.2635929)).

## The mutation tool's runtime changes the application's target

**Wrong:** retarget an application solely to satisfy Stryker.NET's installation prerequisite.

**Use instead:** verify the selected tool release's runtime separately from the application's supported target.

**Why:** the checked documentation says "Your application does not need to target dotnet 10 or newer. You only need the runtime installed so stryker can run." ([Stryker.NET getting started, Install prerequisites](https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/docs/getting-started.md)).

## A coverage percentage is read as producer reachability

**Wrong:** “c8 reports 95%, so the producer runs.”

**Use instead:** check that the specific producer file and function appear in the report and executed, with no ignore comment over them.

**Why:** "By default v8 will only give us coverage for files that were loaded by the engine"; unloaded files appear only with `--all` ([c8 README](https://raw.githubusercontent.com/bcoe/c8/ae5a0cf4349b92cac910cf7275e724ab7a725b9d/README.md)). node:test coverage leaves out `node_modules/` files by default ([Node test, Collecting code coverage](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)).

## A shuffled pass is read as no order dependence

**Wrong:** “The suite passed with randomization on, so tests are independent.”

**Use instead:** state what was shuffled and keep the seed.

**Why:** node:test keeps declaration order for subtests awaited one by one, and under default process isolation each test file runs in its own process ([Node test, Randomizing tests execution order and Test runner execution model](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)). Jest `--randomize` shuffles "the order of the tests within a file" and needs `jest-circus` ([Jest CLI, --randomize](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md)).

## The failing shuffle seed is lost

**Wrong:** rerun a shuffled failure without its seed and call it a flake when it passes.

**Use instead:** set or record the seed for every recorded run and replay with it.

**Why:** node:test prints "Randomized test order seed" and replays with `--test-random-seed` ([Node test](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/test.md)); Jest prints it with `--showSeed` or `--randomize` ([Jest CLI](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md)); Vitest's `sequence.seed` defaults to `Date.now()` and its page does not say the seed is printed ([Vitest sequence](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/config/sequence.md)).

## A leak or flake is declared gone under a diagnostic mode

**Wrong:** “No failure under `--detectOpenHandles`, so the leak is fixed.”

**Use instead:** compare under the original execution mode, and read the config for `forceExit`.

**Why:** `--detectOpenHandles` "implies `--runInBand`, making tests run serially", and `--forceExit` "is an escape-hatch" for resources "still being held on to" ([Jest CLI, --detectOpenHandles and --forceExit](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md)).
