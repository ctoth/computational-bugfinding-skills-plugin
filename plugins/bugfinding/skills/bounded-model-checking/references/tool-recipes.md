# Conditional tool operation

These are source-read shapes for an existing compatible integration, not executed examples. Select real paths, entrypoint, dependency/model version, language/ABI, budget and project-permitted runner. Installation is a target change; prefer an existing fitting tool.

No bounded model checker for JavaScript or TypeScript source was verified (bounded GitHub search, 2026-11-09).

## CBMC: actual source or linked GOTO target

The manual accepts source or fully linked GOTO input and distinguishes automatically generated/user properties ([Description](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). A harness must call the actual target, not contain its copied implementation:

```text
cbmc harness.c target.c --function harness --unwind 12 --unwinding-assertions --trace --json-ui
```

Twelve is an illustrative finite bound. Keep complete structured output and selected checks. The same source's standard-check section says "From version 6.0 onwards" the standard checks, including `--unwinding-assertions`, apply by default, despite its `cbmc-5.59.0` header; verify the chosen binary, not a merged tutorial/version assumption ([manual, Standard Checks](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). On such a binary the explicit flag is redundant; the completeness check is lost only through `--no-unwinding-assertions` or `--no-standard-checks` ([cbmc_parse_options.cpp](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/cbmc/cbmc_parse_options.cpp)).

Run `--cover assume` as a separate diagnostic run when diagnosing reach. The manual says `--unwinding-assertions` "cannot be used with --cover" ([manual, BMC options](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)); the pinned frontend exits with a usage error when both are given ("--cover and --unwinding-assertions must not be given together") and otherwise warns that "unwinding-assertions will be defaulted to false" ([cbmc_parse_options.cpp](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/cbmc/cbmc_parse_options.cpp)). A coverage run is therefore never the completeness evidence for the bound.

The CBMC/JBMC source license lists four numbered redistribution conditions, including an advertising acknowledgement ("All advertising materials mentioning features or use of this software"); solver/dependency terms remain separate ([license](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/LICENSE)).

## JBMC: bytecode plus the selected library model

Compile the real Java source with debug information: "to see the original parameter names in the trace output, the Java source must be compiled in debug mode: `javac -g`" ([user manual, User assertions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md)). A selected method can be checked with:

```text
jbmc package.Class.method --unwind 12 --unwinding-assertions --trace
```

Set the actual classpath, including the compatible `core-models.jar` where needed; the library model is not the real JVM implementation: "The core models library simulate the behavior of the Java Library" ([user manual, Java Library support](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md)). Respect the host's path-list syntax rather than copying Unix separators into Windows. Its README says "Releases are tested and for production use", while develop versions "are not recommended for production use", and requires the CBMC prerequisites plus JBMC submodule setup ([versions/build](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/README.md)).

Inspect actual body loading/stubs and exception properties. The manual adds `--throw-runtime-exceptions` "To have JBMC reliably notify about all uncaught exceptions"; without it, the same null dereference is reported only as a null pointer check failure ([user manual, Exceptions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md)). Enabling `--java-threading` sets `allow-pointer-unsoundness`, which the frontend comment calls "unsound"; it is not a blanket concurrent-Java guarantee ([source, java-threading](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)). JBMC also turns unwinding assertions on unless `--no-unwinding-assertions` is given ([source, unwinding-assertions option](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)).

## Kani: a proof harness calling real Rust code

Start from an actual tested component and a small meaningful nondeterministic domain; I/O is outside the documented real-code route ([entrypoint guidance](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)). In a fitting configured crate, select a real harness:

```text
cargo kani --harness HARNESS --unwind 11
```

Eleven comes from the tutorial's particular size-ten example, not a universal bound: Kani needs the unwinding bound to be "one more than" the number of loop iterations, and `break`/`continue` can require "two more" or "three more". The three settings differ: `#[kani::unwind]` on the harness is the recommended form, `--default-unwind x` applies to every harness that does not have an explicit bound, and `--unwind` overrides a harness's bound only when running a specific harness ([loop bounds, Unwinding value specification](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)).

The install guide lists ready binaries for `x86_64-unknown-linux-gnu`, `x86_64-apple-darwin` and `aarch64-apple-darwin`; other platforms "are either not yet supported or require instead that you build from source". If dependency setup is authorized, its versioned installer route is `cargo install --locked kani-verifier --version SELECTED_VERSION` followed by `cargo kani setup`; setup fetches the matching support environment ([installation](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/install-guide.md)). Kani's README shows calling the real function with nondeterministic inputs and records dual MIT/Apache-2.0 terms ([harness/license](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/README.md)). Do not infer support from the host's unrelated stable Rust compiler.

## Read the operation and result together

CPROVER defines safe 0, unsafe 10 and inconclusive 5, but `CPROVER_EXIT_CONVERSION_FAILED` also uses 10; usage (1), parsing (2) and internal/exception/incorrect-task (6) failures are separate ([exit definitions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/util/exit_codes.h)). Preserve operation mode and per-property results instead of equating any nonzero status with a product bug. For Kani, inspect every relevant assertion and cover result, not merely the summary ([results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)).
