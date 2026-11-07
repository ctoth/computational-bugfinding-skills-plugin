# Common mistakes

## Coverage is treated as rejection

**Wrong:** “The faulty line ran, so this oracle detects the fault.”

**Use instead:** establish the control's relevant state change and its propagation to the intended assertion. Static reachability, observed coverage and semantic detection answer different questions ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/), [Just et al., §2.5](https://doi.org/10.1145/2635868.2635929)).

## A tool's detected count substitutes for the witness

**Wrong:** “Mutation score increased, so the new effect checker works.”

**Use instead:** inspect the per-control outcome and rejecting check. Stryker counts timeouts as detected; invalid compile/runtime cases are excluded from its mutation score. Neither fact demonstrates rejection by a separate effect oracle ([Stryker states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)).

## A survivor is automatically a missing assertion

**Wrong:** add assertions until every survivor dies.

**Use instead:** distinguish an uncovered path, equivalent/irrelevant mutation, missing prerequisite and genuinely unobserved violation. PIT documents these different outcomes and equivalence cases ([PIT concepts](https://pitest.org/quickstart/basic_concepts/)).

## Setup failure is counted as a healthy/faulty distinction

**Wrong:** a mutant fails to load, but its nonzero exit is recorded as successful semantic detection.

**Use instead:** establish that both cases reach the intended checker and preserve its exact result. PIT reports nonviable and run-error outcomes separately from killed mutations ([PIT concepts](https://pitest.org/quickstart/basic_concepts/)).

## A dry run is presented as sensitivity evidence

**Wrong:** “PIT generated mutants and coverage, so the tests caught representative faults.”

**Use instead:** preserve dry-run output as setup evidence. PIT's dry-run mode does not execute tests against mutants ([PIT Maven, Dry Run Mode](https://pitest.org/quickstart/maven/#dry-run-mode)).

## Broad mutation replaces contract-specific controls

**Wrong:** maximize a generic score instead of checking the new recovery, world-effect or numerical guarantee.

**Use instead:** select controls that can violate that actual promise. Missing algorithms, contexts and invariants can escape common operators ([Just et al., §3.2](https://doi.org/10.1145/2635868.2635929)). Keep real regressions and unresolved cases; do not translate score into expected product bugs.

## The mutation tool's runtime changes the application's target

**Wrong:** retarget an application solely to satisfy Stryker.NET's installation prerequisite.

**Use instead:** verify the selected tool release's runtime separately from the application's supported target. The checked documentation distinguishes those requirements ([Stryker.NET prerequisites](https://stryker-mutator.io/docs/stryker-net/getting-started/)).
