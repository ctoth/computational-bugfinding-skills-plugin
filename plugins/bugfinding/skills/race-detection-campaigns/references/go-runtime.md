# Go race workloads

## Fit the actual toolchain

Use an existing race-enabled integration. The pinned official guide says the detector "requires cgo to be enabled, and on non-Darwin systems requires an installed C compiler". On Windows, as of Go 1.21, it needs a C compiler with "version 8 or later of the `mingw-w64` runtime libraries"; the probe is the configured compiler's `--print-file-name libsynchronization.a` result, where an older compiler "will just echo the argument" ([Requirements](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)). Check the installed toolchain's actual target and build inputs before running.

Do not combine support lists from different versions. The inspected development source admits `linux/riscv64`, which the pinned website article does not list; its ARM64 admission also lacks runtime VMA-width knowledge ("Race detector only supports 48-bit VMA on arm64"). Those observations are not a released-support union ([selected platform source](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/internal/platform/supported.go), [article Requirements](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)). Go's inspected source license is BSD-3-Clause ([LICENSE](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/LICENSE)).

## Run a selected ordinary-test workload

Conditional, unexecuted example in an existing fitting project; choose package/test and limits from actual scope and cost:

```text
go test ./path/to/pkg -race -run '^TestSharedLifecycle$' -count=1 -cpu=1,2,4 -timeout=2m
```

`-count=1` prevents cached success ("The idiomatic way to disable test caching explicitly is to use -count=1"); `-cpu` varies GOMAXPROCS for ordinary tests. Neither count nor cpu applies to fuzz tests selected by `-fuzz`; `-parallel` is not the application's actor count ([Go 1.27.3 testing flags](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)). The duration is illustrative, not an assurance threshold.

Keep the paired-access/creation stacks and selected `GORACE` settings. Output-path, first-report and history controls affect retained diagnostics: `log_path` writes `log_path.pid`, `halt_on_error` defaults to `0`, and raising `history_size` "can avoid a \"failed to restore the stack\" error". `exitcode` defaults to `66` after a detected race, so classify that status separately from the workload's own failures. Race build constraints may exclude code/tests ([guide Report Format, Options and Excluding Tests](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)).

## Inspect the end-to-end boundary

Dynamic Go plugins "are poorly supported by the Go race detector"; "Even simple race conditions may not be automatically detected". Retain host/plugin toolchain, tags, flags and source identities; the same warnings predict runtime crashes unless all parts use "exactly the same version of the toolchain, the same build tags" ([plugin warnings](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/plugin/plugin.go)). In the inspected cgo flag-construction path, only the `cfg.BuildMSan` and `cfg.BuildASan` branches prepend `-fsanitize=memory`/`-fsanitize=address` to cgo flags; native TSan is not added automatically. Inspect actual native compilation/linkage before claiming FFI coverage ([build source, lines 3553–3560](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go)). No generic mixed Go/native TSan link recipe is established here.

Long-lived race-instrumented goroutines can retain defer/recover auxiliary allocations ("an extra 8 bytes per `defer` and `recover` statement", "not recovered until the goroutine exits") that "will not show up in the output of" `runtime.ReadMemStats` or `runtime/pprof`. Compare instrumented versus ordinary process/lifecycle evidence before calling that growth a target leak ([Runtime Overhead](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)).
