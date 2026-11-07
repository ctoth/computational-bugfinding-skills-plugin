---
name: coverage-guided-fuzzing
description: Builds and operates instrumented fuzzing lanes with runtime-specific discovery, reset and replay semantics. Use when configuring AFL++, libFuzzer, Go fuzzing, cargo-fuzz, Atheris, Jazzer or FuzzTest, or diagnosing low useful coverage in an existing campaign.
---

# Coverage-guided fuzzing

Make the real target execute under feedback, with the intended oracle and reproducible lifecycle. A running fuzz binary or growing corpus does not establish useful target reach ([AFL++ Fuzzing in Depth](https://aflplus.plus/docs/fuzzing_in_depth/)).

## Select the actual lane

Read the target entrypoint, build graph, enabled features, runtime/architecture, decoder and property. Identify which target modules receive instrumentation and what changes under the fuzz build; a driver-only instrumented path or a feature enabled only on its wrapper can miss the intended implementation ([Rust Fuzz Book guide](https://rust-fuzz.github.io/book/cargo-fuzz/guide.html), [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html)).

Use the existing fitting producer and build owner. Choose only the applicable execution reference:

| Target | Read |
|---|---|
| Native source/binary, AFL++ or libFuzzer | [Native runners](references/native-runners.md) |
| Go or Rust | [Go and Rust](references/go-rust.md) |
| Python/native extensions or JVM | [Python and JVM](references/python-jvm.md) |
| C++ property domains with FuzzTest | [C++ FuzzTest](references/cpp-fuzztest.md) |

Verify the selected release's prerequisites and installed help before changing configuration. References record a dated source snapshot, not a promise that every version/platform supports the same flags. Invoke within the user's existing authority; this skill does not itself authorize installations, target edits or external spending.

## Run a finite informative pilot

Establish discovery mode, relevant target instrumentation, state reset and a working oracle before adding workers. Go seed replay, Jazzer regression and FuzzTest unit mode differ from their discovery modes ([Go fuzzing](https://go.dev/doc/security/fuzz/), [Jazzer README](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/README.md), [FuzzTest Bazel quickstart](https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md)).

Observe decoder admission, intended operation, successful effects and property evaluations separately from engine coverage. Diagnose rejected formats, hidden state or unmet dependencies using [reach, reset and feedback](references/reach-reset-feedback.md). Select dictionary/comparison feedback or structural mutation against a demonstrated blocker; each changes a different part of search ([AFL++ CmpLog](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md), [Google structure-aware fuzzing guide](https://raw.githubusercontent.com/google/fuzzing/master/docs/structure-aware-fuzzing.md)).

Keep per-input, fuzz-time, wall-time, worker/CPU and memory controls distinct; include setup/replay cost in the authorized envelope. AFL++ `-V` is fuzz time and `-E` is approximate executions; neither is aggregate process CPU ([AFL++ selected-ref CLI source](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c)). Use separate owned outputs and bounded cleanup of owned processes. Refer to `bugfinding-campaign` for allocation decisions.

## Interpret and retain evidence

Preserve exact input/typed arguments, build/configuration/instrumentation, initial state or sequence, command/limits, raw engine output, target/property counters and emitted replay material. Cross-invocation state and lifecycle differences can invalidate one-file reproduction ([Go fuzzing](https://go.dev/doc/security/fuzz/), [Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java)).

Return what actually executed, the property observed, resource use, candidates and omissions. Distinguish discovery from regression, coverage from semantic reach, and candidate failure from product attribution. Use `corpus-evolution` for compatible retention/exchange, `failure-reduction` for witness-preserving shrinking and `evidence-based-triage` for attribution. Historical seed-selection results depend on their target/scheduler; don't turn them into universal throughput or yield promises ([Rebert et al., pp.864,871,873](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

For concrete misleading runs and corrections, read [common mistakes](references/common-mistakes.md). No target-specific new framework follows from this skill.
