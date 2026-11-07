# Boundaries and oracles

## Select an implementation that actually admits the target

Keep production source as the owner. A simulator may legitimately replace environmental operations, but that model's fidelity is a separate assumption: FoundationDB's paper identifies missed dependencies and weaker-than-assumed OS contracts as blind spots ([§4, p. 9](https://www.foundationdb.org/files/fdb-paper.pdf)). Inspect actual syscall, scheduler, lifecycle and dependency paths before claiming controlled execution.

Distinguish three results: a model-admitted test, a replayed simulated contradiction, and a contract-adjudicated target finding. FDB's simulator uses local assertions, generated-workload invariants and a recoverable-environment progress check; none substitutes automatically for the others ([§4, pp. 8-9](https://www.foundationdb.org/files/fdb-paper.pdf)). This pack's reporting convention keeps those evidence states separate.

A fitting seam can be translated source, as in Gosim's loader, or a target's existing runtime, as in Flow. Gosim loads with CGO disabled; FDB's client workloads require callback-based main-network-thread execution for determinism ([Gosim loader](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/internal/translate/load.go), [FDB Parallelism and Determinism](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst)). An incompatible target is a method-selection result, not a reason to copy its implementation or change its runtime.

## Derive the oracle at a real boundary

For a promised acknowledged-recovery property, retain the acknowledged operation and specified failure model, then observe recovered state. For progress, establish a recoverable regime before requiring it: FDB heals modeled hardware sufficiently for recovery, while TigerBeetle deliberately preserves failures outside a healthy core ([FDB §4 p. 9](https://www.foundationdb.org/files/fdb-paper.pdf), [TigerBeetle liveness account](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). Choose the target's actual guarantee; these are different examples, not universal quorum rules.

A mock narrows the observed dependency contract. Antithesis requires isolated dependencies deployed alongside the application or mocked; passing that environment does not test an omitted external vendor's behavior ([prerequisites, Complete network isolation](https://antithesis.com/docs/faq/prerequisites/)). Keep the substitution explicit rather than treating an unavailable service as successfully tested.

## Complementary evidence

Retain native races/weak memory, real OS/filesystem contracts, external dependencies and performance where the simulation omits them. FDB documents separate simulation, live performance and hardware testing, and its C API tester exercises real-cluster client layers ([Simulation and Testing](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/testing.rst), [API Tester](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst)). Use the corresponding race, crash-consistency, distributed-fault and resource skills for those dimensions; more identical seeds cannot add an absent observer or environment.
