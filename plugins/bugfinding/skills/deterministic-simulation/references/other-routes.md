# Existing target-embedded and hosted routes

## FoundationDB / Flow

Use the target's existing simulator/workload ownership. FDB documents production and simulated Flow execution plus setup/start/check workload phases; blocking or independent workload threads can break its repeatability ([testing](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/testing.rst), [Parallelism and Determinism; Workload lifecycle](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst)). An already-built compatible simulator documents this command shape:

```text
fdbserver -r simulation -f testfile.txt
```

Keep the actual test file, binary, configuration and emitted cluster seed. Inspect selected build help/test formats; UNIT_TEST_SEED and standalone unit simulation are different registrations, not the cluster campaign ([client Run the simulator](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/client-testing.rst), [standalone testing](https://raw.githubusercontent.com/apple/foundationdb/7e7611f8270952a2b1cffd75aa523c4b057afd62/documentation/sphinx/source/testing.rst)). Use actual outer resource limits; do not invent a seed flag or replace a cluster experiment with broad unit CI.

## TigerBeetle VOPR

VOPR executes TigerBeetle production code with modeled clock/network/disk and state checkers, including packet reordering and storage corruption in its documented model ([VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/docs/internals/vopr.md)). Those controls do not establish another simulator's capabilities. The selected build source declares Zig 0.16.0 and its VOPR step documents:

```text
zig build vopr -- 42
```

Use the actual compatible source/toolchain and chosen seed; retain the source identity with it ([build definition, version and VOPR](https://raw.githubusercontent.com/tigerbeetle/tigerbeetle/68958eb757747d0fc96a79d1f9c2fa6766b67b48/build.zig)). This is an existing target-specific route, not a generic library for another application's code.

## Antithesis

The observed documentation requires x86-64 Linux images, Compose/Kubernetes topology, no nested virtualization and an isolated dependency environment ([prerequisites, Architecture and compilation through Complete network isolation](https://antithesis.com/docs/faq/prerequisites/)). Keep actual dependencies or explicit mocks and a workload; a substituted service narrows the tested contract.

The setup guide requires registry credentials and a ready signal after required initialization. Its first setup-complete signal starts testing/faults; emitting it before readiness changes the experiment ([Compose Requirements and Add a ready signal](https://antithesis.com/docs/setup/docker_compose/)). Reuse the selected service's current integration. This skill supplies no account, image upload, paid run or automatic setup framework.
