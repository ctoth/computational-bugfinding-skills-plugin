# Existing target-embedded and hosted routes

## FoundationDB / Flow

Use the target's existing simulator/workload ownership. FDB documents that "Flow supports both production execution and deterministic simulated execution" plus setup/start/check workload phases. A workload runs in the main network thread, where a blocking call "will result in a deadlock"; starting threads for the blocking API means "test failures will be non-deterministic" ([testing](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/testing.rst), [Parallelism and Determinism; Workload lifecycle](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst)). An already-built compatible simulator documents this command shape:

```text
fdbserver -r simulation -f testfile.txt
```

Keep the actual test file, binary, configuration and emitted cluster seed. Inspect selected build help/test formats; `UNIT_TEST_SEED` is "independent of the cluster simulation seed", and standalone unit simulation is a different registration, not the cluster campaign ([client Run the simulator](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst), [standalone testing, Running C++ unit tests](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/testing.rst)). Use actual outer resource limits; do not invent a seed flag or replace a cluster experiment with broad unit CI.

## TigerBeetle VOPR

VOPR executes TigerBeetle production code with stubbed clock/network/disk and state checkers; its seed-tuned faults "may drop and reorder packets, partition the network, or corrupt reads and writes" ([VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/docs/internals/vopr.md)). Those controls do not establish another simulator's capabilities. The selected build source requires exactly Zig 0.16.0 (any other major/minor/patch fails with "unsupported zig version: expected {f}, found {f}") and its VOPR step documents:

```text
zig build vopr -- 42
```

Use the actual compatible source/toolchain and chosen seed; retain the source identity with it ([build definition, version and VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/build.zig)). This is an existing target-specific route, not a generic library for another application's code.

## Antithesis

The observed documentation requires code "compiled for x86-64", "standard Linux container images", Compose/Kubernetes topology, no nested virtualization ("Nested hardware virtualization is not supported.") and an isolated dependency environment ([prerequisites, Architecture and compilation through Complete network isolation](https://antithesis.com/docs/faq/prerequisites/)). Keep actual dependencies or explicit mocks and a workload; a substituted service narrows the tested contract.

The setup guide requires "a container registry and credentials" and a `setup_complete` signal after required initialization. Antithesis "will treat the first such message sent by any running process as its signal to begin testing and injecting faults"; emitting it before readiness changes the experiment ([Compose Requirements and Add a ready signal for fuzzing](https://antithesis.com/docs/setup/docker_compose/)). Reuse the selected service's current integration. This skill supplies no account, image upload, paid run or automatic setup framework.
