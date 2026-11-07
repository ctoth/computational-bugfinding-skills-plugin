# Common mistakes

These wrong/right contrasts describe this pack's interpretation policy; their tool facts are grounded below.

| Wrong | Right and why |
|---|---|
| Treat a failed unwind check as the desired product assertion failure. | Identify the actual failed property; the Kani example first fails completeness and only later exposes the index defect ([loop tutorial](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)). |
| Assume the expected answer, then count the green assertion. | Establish satisfiable legal setup and check reach; contradictory assumptions can empty later search ([CBMC assumptions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/modeling-assumptions.md)). |
| Add `--partial-loops` to make an inconvenient loop finish and call the path real. | Preserve the selected completeness requirement and investigate the bound; partial-loop paths can be spurious ([unwinding](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). |
| Accept missing Java methods as actual library behavior. | Inspect body/stub/model provenance; the frontend generates simple stubs for unavailable or excluded methods ([source](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)). |
| Interpret a `SUCCESS` summary as every assertion having executed. | Inspect per-property reach and unsupported outcomes; Kani documents vacuous success and undetermined checks ([results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). |
| Declare a UB witness disproved because playback did not crash. | Check the supported playback category; non-panic UB checks need another appropriate observer ([limitations](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)). |
| Read an old JSON success after killing the new verifier. | Match run identity and completion; this export version can preserve the earlier file ([JSON output](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). |
| Call an I/O-heavy replacement implementation “the verified target.” | Select an actual supported component and state the narrower guarantee; Kani does not model I/O ([real-code guide](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)). |
