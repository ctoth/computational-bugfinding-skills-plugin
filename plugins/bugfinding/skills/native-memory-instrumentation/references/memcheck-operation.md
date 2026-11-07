# Memcheck operation

The consulted manual identifies Valgrind 3.28.0, 23 October 2026 ([manual identity](https://valgrind.org/docs/manual/index.html)). Select an actual supported OS/ISA and executable; the current platform page treats Windows ports as historical. Do not infer a current native Windows route from an old port ([platforms](https://valgrind.org/info/platforms.html)). The project declares GPL; full selected-package terms remain its own license, not the documentation's separate license ([about](https://valgrind.org/info/about.html)).

## Existing fitting binary

```text
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --errors-for-leak-kinds=definite,possible --track-origins=yes --error-exitcode=99 --log-file=memcheck.%p.log ./target CASE
```

The chosen error code is illustrative; ensure it is distinguishable from target status. Full leak checking and selected error kinds determine which leaks affect the error summary/exit policy; displayed kinds are a separate choice. Origins add earlier definedness context and cost ([Memcheck, §§4.2–4.3](https://valgrind.org/docs/manual/mc-manual.html)). Preserve categories and suppressed counts rather than flattening every leak into one score.

Start the actual executable and retain matching debug symbols. Exec-child tracing is separate, and per-process logs avoid mixing evidence. Default error-exitcode zero preserves application status. Valgrind changes thread scheduling, so this is not an exhaustive concurrency result ([core, §§2.1–2.4, Error-related options and §2.8](https://valgrind.org/docs/manual/manual-core.html)).

## Observe the right phase

Undefined copied bytes may report only when they affect a checked use. Pools/custom allocators require faithful existing client-request descriptions. Naming a block does not establish addressability. Finish a leak phase after the relevant lifecycle or use a supported explicit request; a killed worker with no scan is incomplete evidence ([Memcheck, §§4.2.2, 4.5, 4.7–4.8](https://valgrind.org/docs/manual/mc-manual.html)).

For a long-lived pool workload, preserve setup, repeated operations, pool metadata, scan point and original output. Investigate whether the real contract concerns unreachable allocations or reachable retention; route the latter's growth measurement to `resource-complexity-testing`. Do not discard an expensive case merely because it lowers executions per second.
