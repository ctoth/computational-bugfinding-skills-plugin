# Progress contracts and useful search

This pack uses an obligation record as an engineering aid, not a required framework: actual admitted work, start, allowed success/abort/cancellation, prerequisite availability/fairness and observable discharge. The distinction matters concretely when a success-only helper is applied to a task whose contract permits cancellation ([Coyote TaskLivenessMonitor](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Specifications/Monitors/TaskLivenessMonitor.cs)).

## An obligation that really remains pending

For a real worker, follow the producer of the awaited event and the code that can still send it. Idle service with no admitted work differs from unfinished admitted work. In a synctest bubble, durable blocking is internal to the bubble; mutex acquisition, I/O and syscalls do not generally supply that evidence ([synctest, Blocking](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/synctest/synctest.go)). Use the target's existing request identities and wait relationships; a new universal monitor is unnecessary.

For fairness-sensitive work, show which action remains enabled and what scheduling/delivery the actual contract provides. CHESS's historical strategy deliberately restricts exploration to fair schedules for algorithms that rely on them; that strategy is not a guarantee about an arbitrary production scheduler ([CHESS, §4.3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). A harness that withholds the only required response has changed the premise.

## Recovery without continually repairing the bug

Inspect the target's actual recoverable state. FDB's documented recovery oracle restores its modeled hardware to an environment where recovery should be possible ([FDB, p.9](https://www.foundationdb.org/files/fdb-paper.pdf)). Do not transplant its assumptions into a different storage or quorum contract.

TigerBeetle's dated implementation account describes selecting and healing a healthy core while keeping failures outside it permanent. It exposed a retry-target resonance that ordinary eventual healing/restarts masked ([Teaching the VOPR and Resonance](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). The transferable decision is to vary the admissible fault regime and retain the problematic retry state, not to prescribe that quorum for every system.

**Illustrative experiment, not an observed target bug:** retain a real request ID, its retry-target history and a contract-supported available core. Search operation/fault choices before fixing that regime; then observe the required semantic completion. If no such availability promise exists, preserve nonprogress as a candidate or environment-limited result rather than invent the promise. Detailed fault controls remain `distributed-fault-testing`/`deterministic-simulation` responsibilities.

## Cancellation is a contract outcome

**WRONG:** treat any terminal task as satisfying Coyote's successful-completion helper, or classify allowed cancellation as a product liveness failure. **RIGHT:** inspect the real permitted discharge events and use the appropriate existing monitor; the selected helper explicitly tests RanToCompletion ([IsSatisfied](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Specifications/Monitors/TaskLivenessMonitor.cs)). Do not weaken a genuine success-only requirement just to make output green.
