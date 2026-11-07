---
name: symbolic-concolic-execution
description: Guides symbolic and concolic searches for hard-to-reach program paths, with real-target linkage and concrete replay. Use when mutation stalls behind input constraints or when solver-generated counterexamples need validation against actual execution.
---

# Symbolic and concolic execution

Spend solver work on an identified hard path and replay its candidate through the actual target oracle. KLEE's paper distinguishes intended exact execution from practical model/nondeterminism failures; generated inputs need native validation ([KLEE, §2, p.3](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)).

## Select a fitting producer

Inspect the real entrypoint, build, ABI, dependencies and intended property before choosing a solver. KLEE executes LLVM bitcode with optional runtime models; its selected source requires LLVM15+, which is a lower bound rather than an admitted tuple for every newer compiler. SymCC instruments concrete execution with symbolic expressions and documented dependency limits. Verify the selected build, not merely a language name or IR emitter ([KLEE build](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/CMakeLists.txt), [SymCC README](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md)).

Use existing production code in the driver/build. A reimplementation in another language changes the tested producer. Separate legal-input constraints, concrete setup, environmental assumptions and the assertion; a success stub or concretized dependency can remove the intended path. For boundary design and worked cases, read [target and environment](references/target-and-environment.md) ([KLEE, §§4 and 5.5](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf), [external-call source](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/Executor.cpp)).

## Run a bounded informative search

Choose KLEE for a compatible bitcode/model boundary; use [KLEE operation and replay](references/klee-operation-and-replay.md) for actual compile, input, query-limit and native-replay contracts. Choose a compatible SymCC concrete-path/hybrid lane using [concolic operation](references/concolic-hybrid-operation.md). One SymCC run follows one concrete path and proposes alternatives; its helper's pruning and attempt timeout are not completeness or whole-campaign bounds ([SymCC README](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md), [helper producer](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/util/symcc_fuzzing_helper/src/symcc.rs)).

Diagnose unreachable code, lost symbolic influence, path growth and expensive queries separately. Keep finished, interrupted, unsupported, pruned and timed-out work distinct. KLEE exposes per-query limits and multiple state-search policies; more generated files or completed paths do not independently establish expected-output correctness ([solver options](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Solver/SolverCmdLine.cpp), [search implementation](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/UserSearcher.cpp), [KLEE, §§3 and 5.5](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)).

## Establish a native witness

Retain original and generated inputs, symbolic object names/sizes/order, setup, model/build/runtime identity, constraints where useful, raw diagnostics, budgets and actual replay attempts. Replay through the same contract and real producer. KLEE's intrinsic replay checks object identity; its POSIX replay wrapper can return0 after monitoring a failed child, so wrapper status alone is insufficient ([intrinsic replay](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/runtime/Runtest/intrinsics.c), [POSIX replay loop](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/tools/klee-replay/klee-replay.c)).

Treat an unreplayed model result as model-bound evidence. Explain concretization, missing fault injection or unsupported behavior rather than invent native confirmation; the paper specifically identifies environment fidelity and native replay as practical concerns ([KLEE, §§2 and 4](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)). Use `failure-reduction` for witness-preserving reduction, `evidence-based-triage` for attribution, and `bounded-model-checking` for explicit bounded invariant checking. Those are this pack's responsibility boundaries.

## Finish

Return the actual target/contract, selected compiler/runtime/solver/model, explored and unresolved scope, cost, exact generated/replay artifacts, and narrowest demonstrated violation. Preserve a zero-finding or unsupported result. For misleading interpretations, read [common mistakes](references/common-mistakes.md). Invocation preserves current target-change, installation, execution and publication authority.
