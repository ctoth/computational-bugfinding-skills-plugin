# ExpoSE for JavaScript (gated)

ExpoSE is the only JavaScript route here, and it is gated: run the applicability check on the real target before selecting it. If the check fails, report that JavaScript has no supported symbolic backend for this target and stop. Do not port the code to C or another language to reach KLEE or SymCC; a port is a different producer ([common mistakes](common-mistakes.md)).

## Status

ExpoSE "supports symbolic execution of Node.js programs and JavaScript in the browser" and "is based on Jalangi2 and the Z3 SMT solver". It requires "`node` version v21.7.2 (other versions may work but are not tested)" plus `clang`, `make` and Python 3 ([ExpoSE README](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/README.md)). The pinned commit is the latest on master, dated 2024-07-02 ([GitHub commits API](https://api.github.com/repos/ExpoSEJS/ExpoSE/commits?sha=ec03edf85f883248612b1d498c6a7d9189d16d6f&per_page=1)). Its `package.json` declares `"node": "^21.7.2"` while `.nvmrc` still says `v10.22.0`; follow the README and `package.json` ([package.json](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/package.json), [.nvmrc](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/.nvmrc)). Its entry script is `#!/usr/bin/env bash` and the repository ships a Debian `Dockerfile`, so plan for a POSIX host, WSL or that container; native Windows is not documented ([expoSE script](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/expoSE), [Dockerfile](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Dockerfile)). Treat it as a research-grade tool.

## Applicability check

1. The target is plain JavaScript loaded through `require`. Compile TypeScript first.
2. Check syntax. ExpoSE instruments through its Jalangi2 fork, which runs Babel 6 with the `es2017` and `es2015` presets and then parses with acorn at `ecmaVersion: 6` ([Jalangi2 fork instrumenter](https://raw.githubusercontent.com/ExpoSEJS/jalangi2/c2961c4374fa5f5fb35d114b98621cbe38b5c85f/src/js/instrument/esnstrument.js)). Newer syntax may fail instrumentation; that is an inference from these versions, not a tested limit.
3. Check features. The pinned test tree has one async test (`tests/async/settimeout.js`), many regex tests, and no promise, `async`/`await` or ES-module test ([GitHub trees API](https://api.github.com/repos/ExpoSEJS/ExpoSE/git/trees/ec03edf85f883248612b1d498c6a7d9189d16d6f?recursive=1)). A hard branch that depends on promises, async functions or ESM has no in-repo evidence of support.
4. Run ExpoSE on the real target file under Node 21.7.2 with `EXPOSE_PRINT_PC=1`. Select it only if instrumentation succeeds and at least one path reports a non-empty path condition.

## Harness and run

A harness does `var S$ = require("S$")`, makes inputs with `S$.symbol(name, concrete)` or `S$.pureSymbol(name)`, and calls real production code. `S$.assume(val)` throws `NotAnErrorException` when false, which discards the path rather than reporting an error; `S$.assert(value, desc)` or a thrown value is the failure ([S$ API](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/lib/S%24/src/symbols.js)). Run `expoSE <target.js>`. Set limits explicitly: `EXPOSE_MAX_TIME` defaults to `"2h"`, `EXPOSE_TEST_TIMEOUT` (per test case) to `"40m"`, and `EXPOSE_MAX_CONCURRENT` to the CPU count; `EXPOSE_JSON_PATH` writes JSON output, which is off by default ([Config.js](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Config.js)).

## Read the output

ExpoSE prints `[!] <error>` and an `expoSE replay` line per error, ends with `[+] ExpoSE Finished. N paths, M errors`, and sets `process.exitCode = errors` ([Distributor.js](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Distributor.js)). The same error list receives "Exit code non-zero" for any non-zero child exit and "Error extracting final output - a fatal error must have occured" when the analyser wrote nothing ([Center.js](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Center.js)); a timed-out case is killed with `SIGKILL` ([Spawn.js](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Spawn.js)). So the error count mixes target failures, analyser crashes and timeouts. Classify each entry before counting it.

## Native witness

`expoSE replay` runs the target through Jalangi2 with `--analysis bin/Analyser.js` ([scripts/play](https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/scripts/play)), so it is not a native run. Confirm each candidate by passing its input to the real entry point under the project's own Node version and checking the selected property.
