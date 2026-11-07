# Selected Gosim route

## Applicability before setup

This reference selects neria-cloud/gosim at the pinned sources below; do not mix it with another fork or release. Its admitted compiler families are Go 1.25/1.26, with Linux AMD64/ARM64 and Darwin ARM64 hosts documented in the selected README ([family table](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/internal/buildspec/families_gen.go), [README Technical introduction](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/README.md)). A module's minimum Go version alone is not an admission check. Inspect the actual target toolchain, CGO and dependencies; this evidence does not establish Go 1.27 or Windows compatibility.

Application loading explicitly sets CGO_ENABLED=0 and selects simulation source/configuration; source translation redirects concurrency and state into the controlled runtime ([loader](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/internal/translate/load.go), [architecture](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/design.md)). Do not advertise ordinary native execution or exhaustive weak-memory checking. If a compiler contract or dependency is unsupported, retain that limit and choose a fitting method; do not downgrade production or bypass an unexpected diagnostic.

## Configured execution

Prefer an existing compatible integration. The selected README documents module dependency setup and a launcher build using its internal-linkname mode; inspect that exact recipe and project ownership before an authorized setup change. For a configured launcher and actual named test, these source-read shapes select features and bounded seed choices ([README, deterministic test and debugging](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/README.md)):

```text
./.gosim/gosimtool test -features rt,fs,net -seeds 1-20 -run TestScenario .
./.gosim/gosimtool debug -features rt,fs,net -package . -test TestScenario -seed 1 -step 11
```

Replace the name/seed range/step with actual evidence and budget. The debug route requires fitting Delve setup; a seed range bounds selected seeds, not host CPU time. Recheck selected command help rather than infer an installed release matches this source ([README](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/README.md)). No command here is a tested integration or an instruction to install dependencies automatically.

Feature selection occurs before initialization. NewMachine is unstarted: configure relevant services, call Start, then check every control result. Stop is graceful, Crash selects crash termination, and Restart changes machine epoch/globals ([architecture](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/design.md), [machine controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/machine_sim.go)). Preserve the distinction when testing durability; a clean return from a machine main is not the desired abrupt failure.

## Choose faults the model actually exposes

| Needed dimension | Selected capability and boundary |
|---|---|
| Network | Public Partition/Repair controls validate IPv4 link direction. The documented model supports TCP but excludes DNS, UDP, IPv6, TLS execution and arbitrary packet reordering; repaired loss can require reconnecting ([controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/net/control_sim.go), [feature inventory](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/features.md)). |
| Storage failure | SetCrashMode and SetSyncFault are actual controls, with modeled durability and explicit crash behavior. Do not attribute arbitrary corruption/short-read injection to them ([controls](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/fs/control_sim.go), [feature inventory](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/features.md)). |
| Recovery alternatives | CrashStates takes MaxStates, Next yields retained snapshots, and Restore applies one to a machine. Close iterator/snapshots according to actual ownership; exhaustion is bounded modeled coverage ([declarations](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/fs/recovery.go), [implementation](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/fs/recovery_sim.go)). |
| Time | The feature inventory supplies virtual timers and cooperative seeded scheduling. Inspect host/resource interruption separately; virtual timeout is not a demonstrated CPU-bound-loop interrupt ([features](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/docs/features.md)). |

Retain Seed, Toolchain, Profile, AdapterRevision, RuntimeRevision, Features, host/simulation architecture and BuildDigest/ReplayRevision; the deprecated Certified field is always false ([RunInfo](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/rt/info.go)). Replaying a seed after source, compiler, feature or race-policy changes is a different build-identity experiment ([README](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/README.md)). Selected Gosim is MIT-licensed; that says nothing about a target's complete dependency licensing ([license](https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/LICENSE)).
