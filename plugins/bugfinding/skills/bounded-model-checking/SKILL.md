---
name: bounded-model-checking
description: Guides source-linked CBMC, JBMC and Kani checks with explicit input domains, unwind bounds and executable counterexamples. Use when finite hard paths or invariants merit solver search beyond fuzzing, or when interpreting bounded verification, vacuous success or counterexample playback.
---

# Bounded model checking

Choose a supported real component and a falsifiable finite guarantee. Bounded checking converts program constraints and a negated property into a solver query; adequate unwinding and model assumptions delimit its conclusion ([CBMC paper, pp.169-171](https://www.kroening.com/papers/tacas2004.pdf)). This skill owns domain/completeness interpretation; use `symbolic-concolic-execution` for path-generation and hybrid-search mechanics.

## Select the actual producer and model

Call the real target from its existing harness or supported entrypoint; preserve initialization and application invariants. Kani recommends following existing tests and warns that directly porting large random operation models is impractical. Its pure-component route does not establish surrounding I/O behavior ([real-code guide](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)). Inspect bytecode, library summaries, missing bodies and enabled configuration before treating an abstracted call as the actual producer; JBMC can generate stubs for missing/excluded methods ([frontend, generate_function_body](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)).

Record input/state ranges, operation/container sizes, loop/recursion bounds, ABI and environment assumptions separately. CBMC accepts source or a linked GOTO binary and exposes target platform configuration; selecting the host defaults is not evidence of the intended target semantics ([manual, Description and platform options](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). Read [bounds and models](references/bounds-and-models.md).

## Establish meaningful reach and sufficient bounds

Check that legal setup reaches the asserted property. Contradictory assumptions can empty the search; CBMC offers a separate `--cover assume` observation to locate this ([assumptions, Coverage](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/modeling-assumptions.md)). Use `harness-sensitivity` for representative healthy/wrong controls.

Retain completeness checks. A failed unwinding assertion is evidence about the chosen bound, not the separate product assertion; partial-loop paths can be spurious ([unwinding guide](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). Increase the missing dimension justified by evidence; do not disable a check or assume the desired result to make a run pass.

## Run a fitting finite lane

Use the selected tool/version's actual prerequisites, supported target and help. Read [conditional CBMC/JBMC/Kani operation](references/tool-recipes.md) for source-native commands, setup and result modes. Its numbers are illustrative allocations, not defaults. Keep whole-job resource limits separate from semantic bounds; a truncated search does not become complete because its process ended.

Inspect individual results and coverage. Kani distinguishes failed, unreachable and undetermined checks; a successful summary can contain vacuous checks ([verification results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). Neither a solver timeout nor an unsupported model operation is an exercised healthy property.

## Preserve and replay the counterexample

Retain exact producer/harness/model/checker/build identity, assumptions, dimensions/bounds, raw results, trace and concrete inputs/state. Relate the trace to the real assertion before proposing cause; the reported failure location can be downstream of the fault ([CBMC paper, p.171](https://www.kroening.com/papers/tacas2004.pdf)). Read [counterexamples and replay](references/counterexamples-and-replay.md) before interpreting native confirmation: Kani playback excludes failing non-panic checks and requires matching version/options ([playback limitations](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)).

Return the exact checked guarantee/domain, completed or unresolved bounds, per-property result, model omissions, actual native replay and evidence paths. Preserve model-only findings explicitly. Use `failure-reduction` and `evidence-based-triage` for their separate concerns; read [common mistakes](references/common-mistakes.md) for misleading green/red outcomes. Invocation adds no installation, target-change, external-publication or spending authority.
