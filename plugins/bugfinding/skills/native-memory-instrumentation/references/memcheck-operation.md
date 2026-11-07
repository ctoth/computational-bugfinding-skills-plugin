# Memcheck operation

The consulted manual identifies Valgrind 3.28.0, 23 October 2026 ([manual identity](https://valgrind.org/docs/manual/index.html)). Select an actual supported OS/ISA and executable; the current platform page lists Windows only under historical ports and states "Windows is not under consideration". Do not infer a current native Windows route from an old port ([platforms, Current and Historical](https://valgrind.org/info/platforms.html)). The project declares itself "a GPL'd system"; full selected-package terms remain its own license, not the documentation's separate license ([about](https://valgrind.org/info/about.html)).

## Existing fitting binary

```text
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --errors-for-leak-kinds=definite,possible --track-origins=yes --error-exitcode=99 --log-file=memcheck.%p.log ./target CASE
```

The chosen error code is illustrative; ensure it is distinguishable from target status. Full leak checking and selected error kinds determine which leaks affect the error summary/exit policy: `--errors-for-leak-kinds` "Specifies the leak kinds to count as errors in a full leak search", while `--show-leak-kinds` is a separate display choice. Without `--track-origins=yes`, Memcheck "cannot tell you where the uninitialised value came from"; origins add that context and cost ([Memcheck, §§4.2.10–4.3](https://valgrind.org/docs/manual/mc-manual.html)). Preserve categories and suppressed counts rather than flattening every leak into one score.

Start the actual executable and retain matching debug symbols. Exec-child tracing is separate (`--trace-children` defaults to `no`), and `%p` in `--log-file` "is replaced with the current process ID", so per-process logs avoid mixing evidence. Default `--error-exitcode=0` returns the application's own status. Valgrind "serialises execution so that only one (kernel) thread is running at a time", and "your program will see very different scheduling", so this is not an exhaustive concurrency result ([core, §§2.1–2.4, 2.7.2 Basic Options, 2.7.3 Error-related Options and 2.8](https://valgrind.org/docs/manual/manual-core.html)).

## Observe the right phase

Undefined copied bytes may report only when they affect a checked use: a program "can copy around junk (uninitialised) data as much as it likes" and Memcheck "does not complain" until the data might affect externally visible behaviour. Pools/custom allocators require faithful existing client-request descriptions, because "Left to itself, Memcheck is unable to understand" custom allocators. Naming a block with `VALGRIND_CREATE_BLOCK` "does not actually change the state of memory". Finish a leak phase after the relevant lifecycle or use a supported explicit request such as `VALGRIND_DO_LEAK_CHECK`, which runs a full leak check "right now"; a killed worker with no scan is incomplete evidence ([Memcheck, §§4.2.2, 4.5, 4.7–4.8](https://valgrind.org/docs/manual/mc-manual.html)).

For a long-lived pool workload, preserve setup, repeated operations, pool metadata, scan point and original output. Investigate whether the real contract concerns unreachable allocations or reachable retention; route the latter's growth measurement to `resource-complexity-testing`. Do not discard an expensive case merely because it lowers executions per second.
