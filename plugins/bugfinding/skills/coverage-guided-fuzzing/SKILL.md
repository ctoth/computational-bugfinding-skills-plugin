---
name: coverage-guided-fuzzing
description: Builds and operates instrumented fuzzing lanes with runtime-specific discovery, reset and replay semantics. Use when configuring AFL++, libFuzzer, Go fuzzing, cargo-fuzz, Atheris, Jazzer or FuzzTest, or diagnosing low useful coverage in an existing campaign.
---

# Coverage-guided fuzzing

Make the real target execute under feedback, with the intended oracle and reproducible lifecycle. A running fuzz binary or growing corpus does not establish useful target reach: "The `corpus count` value is a bad indicator for checking how good the coverage is" ([AFL++ Fuzzing in Depth §3.g](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)).

## Select the actual lane

Read the target entrypoint, build graph, enabled features, runtime/architecture, decoder and property. Identify which target modules receive instrumentation and what changes under the fuzz build; a driver-only instrumented path or a feature enabled only on its wrapper can miss the intended implementation. cargo-fuzz feature options "control the `fuzz_targets` crate" until forwarded, and libFuzzer separates instrumentation (`-fsanitize=fuzzer-no-link`) from linking its `main()` ([Rust Fuzz Book guide, Cargo features](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/guide.md), [LLVM libFuzzer, Fuzzer Usage](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

Use the existing fitting producer and build owner. Choose only the applicable execution reference:

| Target | Read |
|---|---|
| Native source/binary, AFL++ or libFuzzer | [Native runners](references/native-runners.md) |
| Go or Rust | [Go and Rust](references/go-rust.md) |
| Python/native extensions or JVM | [Python and JVM](references/python-jvm.md) |
| C++ property domains with FuzzTest | [C++ FuzzTest](references/cpp-fuzztest.md) |

Verify the selected release's prerequisites and installed help before changing configuration. References record a dated source snapshot, not a promise that every version/platform supports the same flags. Invoke within the user's existing authority; this skill does not itself authorize installations, target edits or external spending.

## Run a finite informative pilot

Establish discovery mode, relevant target instrumentation, state reset and a working oracle before adding workers. Go seed replay, Jazzer regression and FuzzTest unit mode differ from their discovery modes: plain `go test` runs seeds "much like a unit test", "Jazzer operates in regression mode unless fuzzing mode is explicitly enabled", and FuzzTest unit mode runs "without sanitizer and coverage instrumentation" ([Go fuzzing, Running fuzz tests](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md), [Jazzer README, Regression mode](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/README.md), [FuzzTest Bazel quickstart, Create and run a fuzz test](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md)).

Observe decoder admission, intended operation, successful effects and property evaluations separately from engine coverage; byte mutation of a compressed format can leave "virtually all generated inputs to be invalid for `uncompress`" ([Google structure-aware fuzzing guide, Example: Compression](https://raw.githubusercontent.com/google/fuzzing/734e55f3cfed1adbb51bf6cb5c65b4c1197b7089/docs/structure-aware-fuzzing.md)). Diagnose rejected formats, hidden state or unmet dependencies using [reach, reset and feedback](references/reach-reset-feedback.md). Select dictionary/comparison feedback or structural mutation against a demonstrated blocker; each changes a different part of search ([AFL++ CmpLog](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md), [Google structure-aware fuzzing guide](https://raw.githubusercontent.com/google/fuzzing/734e55f3cfed1adbb51bf6cb5c65b4c1197b7089/docs/structure-aware-fuzzing.md)).

Keep per-input, fuzz-time, wall-time, worker/CPU and memory controls distinct; include setup/replay cost in the authorized envelope. AFL++ `-V` is "(fuzz time only!)" and `-E` is "an approx. no. of total executions"; neither is aggregate process CPU ([AFL++ selected-ref CLI source, usage text](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c)). Go `-timeout` does not bound the fuzzing phase ([Go and Rust](references/go-rust.md)). Use separate owned outputs and bounded cleanup of owned processes; libFuzzer says of exact artifact paths "Do not use the same path for several parallel processes" ([LLVM libFuzzer, Options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). Refer to `bugfinding-campaign` for allocation decisions.

## Interpret and retain evidence

Preserve exact input/typed arguments, build/configuration/instrumentation, initial state or sequence, command/limits, raw engine output, target/property counters and emitted replay material. Cross-invocation state and lifecycle differences can invalidate one-file reproduction: Go requires that "the state of a fuzz target should not persist past the end of each call", and Jazzer's default `PER_TEST` is "more likely to unintentionally preserve state between fuzz test executions" ([Go fuzzing, Suggestions](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md), [Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java)).

Return what actually executed, the property observed, resource use, candidates and omissions. Distinguish discovery from regression, coverage from semantic reach, and candidate failure from product attribution. Use `corpus-evolution` for compatible retention/exchange, `failure-reduction` for witness-preserving shrinking and `evidence-based-triage` for attribution. Historical seed-selection results depend on their target/scheduler; Rebert et al. found one hypothesis "false under the optimal scheduling" yet tested it again under Round-Robin. Don't turn them into universal throughput or yield promises ([Rebert et al., pp.864,871,873](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

For concrete misleading runs and corrections, read [common mistakes](references/common-mistakes.md). No target-specific new framework follows from this skill.
