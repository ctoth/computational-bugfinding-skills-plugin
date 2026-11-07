# Go and Rust

Use the existing project runner and permitted execution environment. Numeric limits below are illustrative allocations, not required defaults.

## Go

Confirm the chosen `FuzzName` signature, ordered typed inputs and effective target configuration. Run discovery on a platform with coverage instrumentation, "currently AMD64 and ARM64" ([Go fuzzing, Running fuzz tests](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)). A configured focused invocation is:

```sh
go test ./path/to/pkg -run='^$' -fuzz='^FuzzName$' -fuzztime=5m -parallel=2
```

`-run` avoids unrelated ordinary tests for this selected invocation; follow repository policy if it requires them elsewhere. The package argument must match one package and the "regexp must match exactly one fuzz test within that package". `-fuzztime` (default "run forever"; `Nx` counts iterations), `-parallel` ("the maximum number of subprocesses that may call the fuzz function simultaneously") and `-fuzzminimizetime` (per minimization attempt, default 60s) are different limits ([Go testing flags](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)).

`-timeout` does not bound discovery. It is documented as "If a test binary runs longer than duration d, panic.", but the test binary stops that alarm before fuzzing: `m.stopAlarm()` runs before `runFuzzing(m.deps, m.fuzzTargets)`, and `go test` sets its backup kill timer only when `testFuzz == ""` ([Go testing.go `M.Run`, go1.27.3](https://raw.githubusercontent.com/golang/go/2aae1000ea1d4b28923b96db28acf4e3b99d6aff/src/testing/testing.go), [cmd/go test.go, go1.27.3](https://raw.githubusercontent.com/golang/go/2aae1000ea1d4b28923b96db28acf4e3b99d6aff/src/cmd/go/internal/test/test.go)). Enforce any outer wall-clock bound outside `go test`.

Preserve the emitted failure replay selector and actual typed corpus; corpus values "must match the fuzzing arguments exactly, in that order", so `[]byte` construction decisions are not a source `string` ([Go fuzzing, Failing input and Corpus file format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

Make state independent across input calls: the target runs "in parallel across multiple workers and in nondeterministic order", so its state "should not persist past the end of each call". Encode a required operation sequence in one replayable input or use `stateful-property-testing`. A seed-only regression run is not native discovery; without `-fuzz`, fuzz tests "are run much like a unit test" ([Go fuzzing, Suggestions and Running fuzz tests](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

## Rust cargo-fuzz

Verify nightly and matching sanitizer/C++ support: "This project requires the nightly compiler", and listed sanitizer platforms are x86-64 Linux, x86-64 and aarch64 macOS, and Windows. The Windows instructions require MSVC build tools, "C++ AddressSanitizer" and a shell that can "find the MSVC-based AddressSanitizer DLL". Do not repeat an obsolete Unix-only claim or assume a Windows compiler is configured merely because cargo exists ([Rust Fuzz Book setup](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/setup.md), [Rust Windows setup](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/windows/setup.md)).

```sh
cargo +nightly fuzz run target -- -max_total_time=300
cargo +nightly fuzz coverage target
```

The first searches; the second "runs the program _without fuzzing_ on the provided corpus" and needs the LLVM coverage tools (`llvm-tools-preview` for the nightly toolchain). Use installed help (`cargo fuzz --help`, `-- -help=1`) to select actual targets/options ([Rust Fuzz Book guide](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/guide.md), [Rust coverage](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/coverage.md)).

Feature flags "control the `fuzz_targets` crate": forward intended features to the production crate. Record `cfg(fuzzing)` changes across the dependency graph, since "the project crate, and their entire dependency tree" compile with `--cfg fuzzing`; a path removed for fuzzing cannot supply production coverage of that path. The inspected cargo-fuzz 0.13.2 manifest is MIT OR Apache-2.0; verify the selected package and target dependencies separately ([Rust Fuzz Book guide, Cargo features and `#[cfg(fuzzing)]`](https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/guide.md), [cargo-fuzz package manifest](https://raw.githubusercontent.com/rust-fuzz/cargo-fuzz/bf2fc668dafda5295aa6fd01825ee67b885f0f2b/Cargo.toml)).
