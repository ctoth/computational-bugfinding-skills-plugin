# Common oracle mistakes

## Counting a skip as successful comparison

**Wrong:** Increment the equality count whenever neither query produces a reported mismatch.

**Better:** Inspect the check's skip/error paths. NoREC's sentinel handling does not evaluate equality: when either count is `-1` it throws `IgnoreMeException`; preserve that outcome separately ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

## Accepting every expected error without observing effects

**Wrong:** Return success immediately on a documented constraint error.

**Better:** Check the permitted post-state too. ABORT and FAIL have different effect boundaries, and under ABORT "the transaction remains active"; do not assert total transaction rollback for both ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

## Trusting configuration syntax

**Wrong:** Set `foreign_keys` after `BEGIN` and label subsequent tests enforcement-enabled.

**Better:** Set it at a permitted boundary and query the effective value. A command's acceptance does not establish that the setting changed: it "is a no-op within a transaction" ([SQLite foreign_keys](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

## Asking a checker a question outside its scope

**Wrong:** Treat `integrity_check` success as proof that foreign-key relationships hold.

**Better:** Check what the observer covers. `integrity_check` looks for formatting faults and "UNIQUE, CHECK, and NOT NULL constraint errors", but "does not find FOREIGN KEY errors". Select the applicable relationship observation and preserve legal NULL cases ([SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check), [foreign-key semantics](https://www.sqlite.org/foreignkeys.html)).

## Making the checker repeat the implementation

**Wrong:** Copy a complex target algorithm and call the second copy an independent model.

**Better:** Derive a simpler invariant or justified relation from the guarantee, and state shared assumptions. Independent evidence can come from separate engines, as in SQLite's SQL Logic Test, or from a relation over different execution paths, as in SQLite's optimization-disabled reruns. Same-engine comparison can still be useful when its relation is valid and its limitations are explicit ([SQLite testing §2](https://www.sqlite.org/testing.html#test_harnesses), [§9](https://www.sqlite.org/testing.html#disabled_optimization_tests), [NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

## Extending a verdict beyond its observation model

**Wrong:** A successful history check establishes every isolation guarantee.

**Better:** State exactly which dependencies and anomalies the observation/checker can decide. Elle's paper states "Our approach ignores predicates"; absence of its reported anomalies does not establish that omitted dimension ([Elle §§4.3 and 9](https://arxiv.org/abs/2003.10554v1)).

## Reading "no crash" as "no unhandled rejection"

**Wrong:** The Node process exited 0, so no promise rejection went unhandled.

**Better:** Read the effective `--unhandled-rejections` mode and every installed listener. Under the default `throw` mode the crash happens only "If this hook is not set", and with an `uncaughtException` handler "the process will exit with 0" unless the handler sets `process.exitCode`; a no-op `.catch` suppresses the event entirely ([Node CLI, --unhandled-rejections](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/cli.md), [Node process](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/process.md)).

## Adding an `uncaughtException` listener to log errors

**Wrong:** Install `process.on('uncaughtException', log)` in the harness to collect errors.

**Better:** Use `uncaughtExceptionMonitor`, which "does not change the behavior". An `uncaughtException` handler replaces the crash with exit code 0 unless it sets `process.exitCode`, and Node warns "It is not safe to resume normal operation after `'uncaughtException'`" ([Node process, uncaughtExceptionMonitor and uncaughtException](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/process.md)).

## Reading a clean console in a production build as a passed React contract

**Wrong:** The production bundle logged no React warnings, so snapshots are cached and hydration attributes match.

**Better:** State the build mode and check the contract directly. The getSnapshot and hydration-attribute warnings are development-only, and StrictMode checks "are development-only and do not impact the production build" ([ReactFiberHooks.js](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-reconciler/src/ReactFiberHooks.js), [ReactFiberHydrationContext.js](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-reconciler/src/ReactFiberHydrationContext.js), [react.dev StrictMode](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/StrictMode.md)). See the snapshot check in [JavaScript observation channels](javascript-observation-channels.md).

## Counting React warnings as offenders

**Wrong:** One getSnapshot warning was logged, so one component returns uncached snapshots.

**Better:** One message means at least one offender. The warning is guarded by the module-level `didWarnUncachedGetSnapshot` flag, so later offenders are silent ([ReactFiberHooks.js](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-reconciler/src/ReactFiberHooks.js)).

## Trusting a green run with unhandled-error suppression configured

**Wrong:** Vitest or Jest passed, so the code under test raised no unhandled errors.

**Better:** Read the runner configuration first. With Vitest `dangerouslyIgnoreUnhandledErrors`, "Vitest will not fail the test run if there are unhandled errors", and an error filtered by `onUnhandledError` "no longer affects the result of the test run". Without `--waitForUnhandledRejections`, Jest may report a handled rejection or miss an unhandled one ([Vitest dangerouslyIgnoreUnhandledErrors](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/config/dangerouslyignoreunhandlederrors.md), [Vitest onUnhandledError](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/config/onunhandlederror.md), [Jest CLI, --waitForUnhandledRejections](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/CLI.md)).
