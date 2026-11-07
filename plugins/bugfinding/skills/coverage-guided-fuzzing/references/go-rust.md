# Go and Rust

Use the existing project runner and permitted execution environment. Numeric limits below are illustrative allocations, not required defaults.

## Go

Confirm the chosen `FuzzName` signature, ordered typed inputs and effective target configuration. Discovery currently uses AMD64/ARM64 coverage instrumentation. A configured focused invocation is:

```sh
go test ./path/to/pkg -run='^$' -fuzz='^FuzzName$' -fuzztime=5m -parallel=2 -timeout=8m
```

`-run` avoids unrelated ordinary tests for this selected invocation; follow repository policy if it requires them elsewhere. The fuzz regexp must select one target. Fuzz duration, worker processes, each minimization attempt and test-binary timeout are different limits. Preserve the emitted failure replay selector and actual typed corpus; `[]byte` construction decisions are not a source `string` ([Go fuzzing](https://go.dev/doc/security/fuzz/), [Go testing flags](https://pkg.go.dev/cmd/go#hdr-Testing_flags)).

Make state independent across input calls; nondeterministic worker order must not supply hidden setup. Encode a required operation sequence in one replayable input or use `stateful-property-testing`. A seed-only regression run is not native discovery ([Go fuzzing](https://go.dev/doc/security/fuzz/)).

## Rust cargo-fuzz

Verify nightly and matching sanitizer/C++ support. Current setup includes Windows; its Windows instructions require fitting MSVC/AddressSanitizer tooling and DLL paths. Do not repeat an obsolete Unix-only claim or assume a Windows compiler is configured merely because cargo exists ([Rust Fuzz Book setup](https://rust-fuzz.github.io/book/cargo-fuzz/setup.html), [Rust Windows setup](https://rust-fuzz.github.io/book/cargo-fuzz/windows/setup.html)).

```sh
cargo +nightly fuzz run target -- -max_total_time=300
cargo +nightly fuzz coverage target
```

The first searches; the second replays a corpus for coverage and needs compatible LLVM coverage tools. Use installed help to select actual targets/options ([Rust Fuzz Book guide](https://rust-fuzz.github.io/book/cargo-fuzz/guide.html), [Rust coverage](https://rust-fuzz.github.io/book/cargo-fuzz/coverage.html)).

Feature flags configure the fuzz crate: forward intended features to the production crate. Record `cfg(fuzzing)` changes across the dependency graph; a path removed for fuzzing cannot supply production coverage of that path. The inspected cargo-fuzz manifest is MIT OR Apache-2.0; verify the selected package and target dependencies separately ([Rust Fuzz Book guide](https://rust-fuzz.github.io/book/cargo-fuzz/guide.html), [cargo-fuzz package manifest](https://raw.githubusercontent.com/rust-fuzz/cargo-fuzz/master/Cargo.toml)).
