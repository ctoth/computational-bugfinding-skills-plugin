# Common mistakes

The WRONG/RIGHT choices below are this pack's operational corrections, with their factual basis cited.

| WRONG | RIGHT and why |
|---|---|
| Port target logic into a convenient solver language and call the result a target bug. | Link the actual target and preserve setup/environment; the paper's drivers exercise real program paths ([KLEE, §§4 and6](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)). |
| Assume the desired result, then celebrate an assertion pass. | Constrain the legal domain separately: assumptions restrict future values, so the assumed result is no longer independently checked ([assume semantics](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/docs/intrinsics.md)). |
| Allow every external call to make unsupported code run. | Establish the real model/concretization boundary; the actual source distinguishes all and over-approx policies ([Executor](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/Executor.cpp)). |
| Use `replay_exit == 0` as the healthy-target oracle. | Inspect the native case diagnostics and property; the selected wrapper does not propagate monitored child status ([replay loop](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/tools/klee-replay/klee-replay.c)). |
| Continue after a symbolic object mismatch to get a completed replay. | Preserve the exact names/sizes/order and repair the driver/test identity; nonfatal replay substitutes behavior ([intrinsics](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/runtime/Runtest/intrinsics.c)). |
| Count generated files or a helper timeout as complete search. | Distinguish proposals, checked candidates, pruned/killed attempts and confirmed violations ([SymCC helper](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/util/symcc_fuzzing_helper/src/symcc.rs)). |
| Mix old QSYM_BACKEND prose with another runtime main. | Verify actual compiler/runtime CMake and the selected parent submodule ([compiler](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/CMakeLists.txt), [runtime](https://raw.githubusercontent.com/eurecom-s3/symcc-rt/892f817f38f5abfa083dd0c1caa7ced821566bf5/CMakeLists.txt)). |
| Increase solver time when a library concretizes the input. | Fix a demonstrated supported instrumentation/model boundary or record the omission; more time does not restore lost symbolic expressions ([C++ route](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/C%2B%2B.txt)). |
