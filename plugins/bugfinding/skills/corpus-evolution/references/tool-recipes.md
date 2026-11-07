# Conditional corpus operations

These source-documented recipes assume an existing fitting target/build and authorization for their output. Names such as `INPUTS` are project-selected paths. Choose resource limits from the actual budget; commands below were not executed to validate a target.

## AFL++

Select coverage inputs into a distinct empty destination; use `@@` for a file consumer and omit it for stdin, "as this is the default" ([depth guide, §2b](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)). Ordinary `afl-cmin` refuses a populated destination ("Output directory '%s' is not empty") ([selected cmin source, output check](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)):

```sh
afl-cmin -i INPUTS -o SELECTED -- ./target @@
```

The selected revision also provides `afl-merge`, which "only appends inputs that cover something the output corpus does not already cover"; its help says "existing output files are never changed or removed". Check that the installed version exposes it before use ([depth guide, §2b](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md), [selected cmin/merge source, usage](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)):

```sh
afl-merge -o CURRENT -i INCOMING -- ./target @@
```

That source distinguishes per-run `-t` milliseconds ("timeout for each run (default: 5000ms)"), child `-m` memory and `-T` workers; none is a whole-job budget. Crashing inputs are left out of the selection unless `-A` ("allow crashes and timeouts (not recommended)") or `-C` is given, and timeouts unless `-A` is given (source run-result checks around lines 1337-1356), so a default pass over a set containing failures drops them from the output. `--crash-dir` moves crashes; do not use it on the only original evidence. The usage also states "Only the first %ld bytes of an input are given to the target", with `MAX_FILE` defined as `(1 * 1024 * 1024L)`; for a larger input, the measured coverage reflects only that prefix ([selected cmin source, usage](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c), [config.h, `MAX_FILE`](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/include/config.h)). Current licensing must be checked by selected component: the inspected project/combined `afl-fuzz` is AGPL-3.0-or-later, while individual Apache-2.0 files include the inspected `afl-cmin.c` (`SPDX-License-Identifier: Apache-2.0`). The Apache-2.0 option applies to those files "taken individually, not to the combined AGPL work"; this is source provenance, not a conclusion about every binary ([licensing scope](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md), [file header](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)).

## libFuzzer

For the existing instrumented executable, merge into the first directory or replay explicit files without mutation: with a list of files the binary "will not perform any fuzzing" ([libFuzzer, Corpus and Options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)):

```sh
./fuzzer -merge=1 SELECTED FULL
./fuzzer -merge=1 CURRENT INCOMING
./fuzzer case-a case-b
```

Merge selects coverage additions. `-reduce_inputs`, on by default while fuzzing, shrinks inputs "while preserving their full feature sets". `-minimize_crash` targets one crash input; use it "with -runs=N or -max_total_time=N to limit the number of attempts". They answer different questions. Preserve originals separately. A resumable merge can use `-merge_control_file=PATH` and continue "by executing the same command"; stop only owned processes rather than the documentation's process-name-wide `killall` ([libFuzzer, Options and Resuming merge](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). Instrumentation/platform setup belongs to the runner skill.

## Go and authorized OSS-Fuzz access

Retain a saved failure's typed file and emitted replay selector, such as `go test -run=FuzzName/CASE_ID`, in the project's allowed runner. The exploration cache is not the same retained artifact as the finite failure regression. Before saving, "the fuzzing engine will attempt to minimize the input", so the saved file is the minimized value rather than the first failing mutation ([Go fuzzing, Failing input and Glossary](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

For an already authorized OSS-Fuzz project, inspect its target-specific bucket or daily backup. These corpora are "synthesized by the fuzzing engines", and the documented bucket path names one engine and fuzz target (for example `.../libFuzzer/expat_parse_fuzzer`), so replay them on the matching receiver. The documented acquisition shape is `gcloud storage cp -r gs://BUCKET_PATH LOCAL_DIRECTORY`. Access requires being "listed as the primary contact or as an auto cc" in the project's `project.yaml`; OSS-Fuzz also keeps "daily zipped backups". This optional route creates no plugin dependency on an account or cloud SDK ([OSS-Fuzz corpora, Obtain access, Downloading the corpus, Corpus backups](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/corpora.md)).
