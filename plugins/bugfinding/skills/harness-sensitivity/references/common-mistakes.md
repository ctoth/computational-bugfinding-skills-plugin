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
