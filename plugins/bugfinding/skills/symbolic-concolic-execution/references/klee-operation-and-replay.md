# KLEE operation and replay

## Prerequisites and real build

Use a selected compatible KLEE/LLVM/solver installation and actual target build. The inspected KLEE3.4-pre source requires CMake3.16, C++17 and LLVM15+; optional POSIX/libc++ support must actually be built. Minimum-version admission is not a tested matrix. The source license is Illinois/NCSA with separately identified components ([build](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/CMakeLists.txt), [license](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/LICENSE.TXT)).

For a configured single-translation-unit driver, the documented shape is below. Compile/link any separate real target/dependency bitcode through its existing build owner; this example does not copy it into the driver ([tutorial, Compiling and Running](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/tutorials/testing-function.md)).

```text
clang -I KLEE_INCLUDE -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone driver.c -o driver.bc
klee --max-time=300s --max-solver-time=5s --output-dir=OWNED_RUN driver.bc
```

Limits and paths are illustrative, chosen from the authorized envelope. Per-query time differs from interpreter max-time and its watchdog; keep a fitting owned outer limit where needed. Actual state-search choices/interleaving change explored work, not the strength of an interrupted result ([query limit](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Solver/SolverCmdLine.cpp), [watchdog and module loading](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/tools/klee/main.cpp), [state search](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/UserSearcher.cpp)).

For a compatible POSIX build, `klee -posix-runtime target.bc -sym-arg 8 -sym-files 1 64` selects bounded modeled arguments/files. KLEE options precede bitcode; modeled application options follow it. Preserve concrete files, metadata, libc choices and failure assumptions; these flags do not model arbitrary host services ([symbolic environment](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/tutorials/using-symbolic.md), [option order](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/docs/options.md)).

Inspect unsupported operations and warnings before changing external policies. The selected source's over-approx policy exceeds older option prose and drops concretization constraints after calls; do not treat it as a stronger proof or enable it merely to bypass a missing model ([policy source](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/Executor.cpp)).

## Replay through the same property

Retain `.ktest`, generated error/warning output, executed bitcode, driver/target/dependency identities and object values. A native intrinsic driver links the same actual target with `libkleeRuntest`, using compatible include/library paths; `KTEST_FILE=CASE.ktest ./native_driver` selects the testcase in POSIX syntax. Adapt environment assignment to the actual shell. Preserve object names/sizes/order; making replay mismatches nonfatal does not establish a faithful run ([tutorial, Replaying](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/tutorials/testing-function.md), [identity checks](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/runtime/Runtest/intrinsics.c)).

For an existing POSIX replay integration: `KLEE_REPLAY_TIMEOUT=30 klee-replay --keep-replay-dir ./native_target CASE.ktest`. It reconstructs real files and monitors owned child processes; inspect its temporary-directory, debugger-on-timeout and cleanup behavior before running in an authorized disposable location. The selected outer loop waits without propagating child status and returns0: retain per-case crash/timeout/exit diagnostics and the actual property witness ([replay source, process_status/run_monitored/main](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/tools/klee-replay/klee-replay.c)).

A modeled syscall failure may require a supported native fault mechanism; a plain native run without it is not equivalent. Record model-only, native-reproduced and unresolved outcomes separately. The paper identifies practical model/nondeterminism false positives and difficult environmental replay ([KLEE, §§2 and 4](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)).
