# Conditional tool operation

These are source-read shapes for an existing compatible integration, not executed examples. Select real paths, entrypoint, dependency/model version, language/ABI, budget and project-permitted runner. Installation is a target change; prefer an existing fitting tool.

## CBMC: actual source or linked GOTO target

The manual accepts source or fully linked GOTO input and distinguishes automatically generated/user properties ([Description](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). A harness must call the actual target, not contain its copied implementation:

```text
cbmc harness.c target.c --function harness --unwind 12 --unwinding-assertions --trace --json-ui
```

Twelve is an illustrative finite bound. Keep complete structured output and selected checks. The same source's standard-check section describes 6.0+ defaults despite its older header; verify the chosen binary, not a merged tutorial/version assumption ([manual](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)). Run `--cover assume` separately when diagnosing reach: coverage and explicit unwinding assertions are incompatible in that manual ([assumptions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/modeling-assumptions.md)).

The CBMC/JBMC source license has four redistribution conditions; solver/dependency terms remain separate ([license](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/LICENSE)).

## JBMC: bytecode plus the selected library model

Compile the real Java source with debug information (`javac -g`) for meaningful parameter traces. A selected method can be checked with:

```text
jbmc package.Class.method --unwind 12 --unwinding-assertions --trace
```

Set the actual classpath, including the compatible `core-models.jar` where needed; the library model is not the real JVM implementation ([user manual](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md)). Respect the host's path-list syntax rather than copying Unix separators into Windows. Its README distinguishes tested releases from development builds and requires the CBMC prerequisites plus JBMC setup ([versions/build](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/README.md)).

Inspect actual body loading/stubs and exception properties. Enabling `--java-threading` sets an explicitly unsound shared-pointer option in the inspected frontend; it is not a blanket concurrent-Java guarantee ([source](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)).

## Kani: a proof harness calling real Rust code

Start from an actual tested component and a small meaningful nondeterministic domain; I/O is outside the documented real-code route ([entrypoint guidance](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)). In a fitting configured crate, select a real harness:

```text
cargo kani --harness HARNESS --unwind 11
```

Eleven comes from the tutorial's particular size-ten example, not a universal bound. Harness-specific/default/global override semantics differ; inspect the selected harness and tool help ([loop bounds](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)).

The install guide lists ready binaries for Linux x86-64 and macOS x86-64/arm64. If dependency setup is authorized, its versioned installer route is `cargo install --locked kani-verifier --version SELECTED_VERSION` followed by `cargo kani setup`; setup fetches the matching support environment ([installation](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/install-guide.md)). Kani's README shows calling the real function with nondeterministic inputs and records dual MIT/Apache-2.0 terms ([harness/license](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/README.md)). Do not infer support from the host's unrelated stable Rust compiler.

## Read the operation and result together

CPROVER defines safe 0, unsafe 10 and inconclusive 5, but conversion failure also uses 10; usage, parsing and internal failures are separate ([exit definitions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/util/exit_codes.h)). Preserve operation mode and per-property results instead of equating any nonzero status with a product bug. For Kani, inspect every relevant assertion and cover result, not merely the summary ([results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)).
