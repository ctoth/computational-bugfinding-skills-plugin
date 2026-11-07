# Conditional corpus operations

These source-documented recipes assume an existing fitting target/build and authorization for their output. Names such as `INPUTS` are project-selected paths. Choose resource limits from the actual budget; commands below were not executed to validate a target.

## AFL++

Select coverage inputs into a distinct empty destination; use `@@` for a file consumer and omit it for stdin ([depth guide, §2](https://aflplus.plus/docs/fuzzing_in_depth/)):

```sh
afl-cmin -i INPUTS -o SELECTED -- ./target @@
```

The inspected 2026-11-07 source also provides `afl-merge`, which leaves existing output files unchanged and adds coverage-contributing inputs. Check that the installed version exposes it before use ([selected cmin/merge source, usage](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)):

```sh
afl-merge -o CURRENT -i INCOMING -- ./target @@
```

That source distinguishes per-run `-t` milliseconds, child `-m` memory and `-T` workers; none is a whole-job budget. Check its crash/timeout policy. Do not use moving crash options on the only original evidence. Current licensing must be checked by selected component: the inspected project/combined `afl-fuzz` is AGPL-3.0-or-later, while individual Apache-2.0 files include the inspected `afl-cmin.c`; this is source provenance, not a conclusion about every binary ([licensing scope](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md), [file header](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)).

## libFuzzer

For the existing instrumented executable, merge into the first directory or replay explicit files without mutation ([corpus/running/options](https://llvm.org/docs/LibFuzzer.html)):

```sh
./fuzzer -merge=1 SELECTED FULL
./fuzzer -merge=1 CURRENT INCOMING
./fuzzer case-a case-b
```

Merge selects coverage additions; `-reduce_inputs` preserves features and `-minimize_crash` targets a failure. They answer different questions. Preserve originals separately. A resumable merge can use `-merge_control_file=PATH` with the same operation/configuration; stop only owned processes. Instrumentation/platform setup belongs to the runner skill.

## Go and authorized OSS-Fuzz access

Retain a saved failure's typed file and emitted replay selector, such as `go test -run=FuzzName/CASE_ID`, in the project's allowed runner. The exploration cache is not the same retained artifact as the finite failure regression ([Go failing inputs](https://go.dev/doc/security/fuzz/)).

For an already authorized OSS-Fuzz project, inspect its target-specific bucket or daily backup. The documented acquisition shape is `gcloud storage cp -r gs://BUCKET_PATH LOCAL_DIRECTORY`; project contact access is required. This optional route creates no plugin dependency on an account or cloud SDK ([corpus access and backups](https://google.github.io/oss-fuzz/advanced-topics/corpora/)).
