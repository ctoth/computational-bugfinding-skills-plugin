# Bounds, assumptions and model correspondence

This pack's working record is the real producer, legal setup, assertion, finite domain and observed result. Reuse the project's existing note/harness; no solver-specific service or copied implementation is required.

## Choose the dimension that is missing

Separate input maximum, object/container size, number of operations and loop/recursion unwind. Kani's worked example needs a larger unwind after bounding its input; with too-small unwinding "many of the other properties Kani is verifying become" undetermined ([loop tutorial](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)). A larger loop bound cannot admit an input excluded by the harness.

CBMC counts backjumps: in the manual's `i<100` loop the condition is evaluated 101 times, so "the loop requires a limit of 101, and not 100". Obtain real IDs with `--show-loops`, then use `--unwindset` for a relevant loop rather than inflate every loop indiscriminately ([unwinding guide](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). Retain which bounds completed and which assertions still require exploration.

Use the target's actual widths, macros, entrypoint, language and environment; those are configurable analysis inputs (`--LP64`-style width flags, `-D`, `--function`, `--c11`-style standards, `--arch`/`--os`) ([CBMC manual, C/C++ frontend and Platform options](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). A source component can be a valuable finite target without proving its enclosing service.

## Keep assumptions weaker than the property

Assumptions restrict only later checks ("assumptions are never retroactive"), must be satisfiable, and do not turn a constraint on one nondeterministic array index into a universal array invariant ("nondeterminism cannot be used to obtain the effect of universal quantification in assumptions") ([assumptions guide, Modeling with Assumptions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/modeling-assumptions.md)). Construct legal state from real setup or justified invariants; separately retain deliberate invalid-input contracts.

Illustrative diagnosis: a harness assumes both `n > 0` and `n < 0`, then reports its safety assertion green. Inspect reach after each assumption before adding compute. If an arbitrary internal struct violates an application constructor invariant, a red result can instead be model-only. The source-linked setup and actual contract decide which interpretation is justified.

## Preserve the model's exclusions

JBMC's library classes are models, and unavailable/excluded method bodies can become stubs ([library support](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md), [actual frontend](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)). Keep classpath, loaded method/body and model identity with the trace.

Kani documents sequential checking ("Concurrent programs are not supported"), missing aliasing/immutable-mutation guarantees and unsupported inline assembly; valid-value and uninitialized-memory checks are opt-in unstable flags; programs allocating more than `2^N` objects (default 16 object bits) "may exhibit incorrect wrapping behavior"; and `--restrict-vtable` "is a known soundness issue". Do not extend its result to arbitrary concurrency or complete Rust UB coverage ([soundness, What Kani Does NOT Check and Soundness Caveats](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/soundness.md)). An abstract specification is useful only with explicit correspondence to the real producer and its executions. No supported native Go route is established by these recipes.

A valuable next experiment increases a documented boundary size, reaches a previously excluded state or checks a new real invariant. A nominally larger run that stubs the difficult operation or assumes its result changes the question instead.
