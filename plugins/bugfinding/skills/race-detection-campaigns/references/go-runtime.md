# Go race workloads

## Fit the actual toolchain

Use an existing race-enabled integration. The pinned official guide requires cgo and, outside Darwin, a C compiler; its Windows probe checks the configured compiler's `--print-file-name libsynchronization.a` result ([Requirements](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)). Check the installed toolchain's actual target and build inputs before running.

Do not combine support lists from different versions. The inspected development source admits more targets than the pinned website article; ARM64 admission also lacks runtime VMA-width knowledge. Those observations are not a released-support union ([selected platform source](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/internal/platform/supported.go), [article Requirements](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)). Go's inspected source license is BSD-3-Clause ([LICENSE](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/LICENSE)).

## Run a selected ordinary-test workload

Conditional, unexecuted example in an existing fitting project; choose package/test and limits from actual scope and cost:

```text
go test ./path/to/pkg -race -run '^TestSharedLifecycle$' -count=1 -cpu=1,2,4 -timeout=2m
```

`-count=1` prevents cached success; `-cpu` varies GOMAXPROCS for ordinary tests. Neither count nor cpu applies to fuzz tests selected by `-fuzz`; `-parallel` is not the application's actor count ([Go 1.27.3 testing flags](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)). The duration is illustrative, not an assurance threshold.

Keep the paired-access/creation stacks and selected `GORACE` settings. Output-path, first-report and history controls affect retained diagnostics; a missing older stack can require history diagnosis. Race build constraints may exclude code/tests ([guide Report Format, Options and Excluding Tests](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)).

## Inspect the end-to-end boundary

Dynamic Go plugins can miss even simple races; retain host/plugin toolchain, tags, flags and source identities ([plugin warnings](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/plugin/plugin.go)). In the inspected cgo flag-construction path, MSan/ASan options are appended but native TSan is not added automatically; inspect actual native compilation/linkage before claiming FFI coverage ([build source, lines3325–3332](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go)). No generic mixed Go/native TSan link recipe is established here.

Long-lived race-instrumented goroutines can retain defer/recover auxiliary allocations invisible to Go heap profiles. Compare instrumented versus ordinary process/lifecycle evidence before calling that growth a target leak ([Runtime Overhead](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html)).
