# Improve: deterministic-simulation

Date: 2026-11-07

## Findings

Sources retrieved this session: FoundationDB paper page images page-007.png, page-008.png, page-010.png from the existing paper-reader collection (C:/Users/Q/code/bugfinding-literature/deterministic-simulation/papers/Zhou_2021_FoundationDB/pngs/); all 12 pinned Gosim files at 64ac3b2a20806bb4f9470232e12fabdfd5d13852 (HTTP 200 each); TigerBeetle vopr.md and build.zig at 68958eb757747d0fc96a79d1f9c2fa6766b67b48; FoundationDB testing.rst and client-testing.rst at 7e7611f8270952a2b1cffd75aa523c4b057afd62.

### F1 references/gosim-route.md:5 — WARNING — Go/patch replay scope missing
- Text said: Go 1.25/1.26 families on Linux AMD64/ARM64 and Darwin ARM64; nothing on prerelease compilers or cross-patch replay.
- Source (README, Technical introduction; Manual certification; https://raw.githubusercontent.com/neria-cloud/gosim/64ac3b2a20806bb4f9470232e12fabdfd5d13852/README.md): "Prerelease and development compilers are unsupported." and "a family policy does not promise replay across different patches." The README "Current scope of features" Platforms row reads "Linux AMD64 and Darwin ARM 64", which disagrees with the Technical introduction's three hosts.
- Fix: added both quotes; noted the README's internal platform disagreement so hosts are checked, not assumed.

### F2 references/gosim-route.md:26 — WARNING — network row omits real controls and misattributes omissions
- Text said: only Partition/Repair; omissions cited to features.md.
- Source (net/control_sim.go): `SetLinkPolicy` with `policy.Latency` and `policy.Loss` (`FailProbability`, `RepairProbability`) and `ResetLinkPolicy` exist; `linkValue` rejects non-IPv4 (`!link.From.Is4()`). README Current scope: "UDP, IPv6 and hostname resolution are outside the supported model"; "TLS/certificate operations abort".
- Fix: added SetLinkPolicy latency/loss and README citation.

### F3 references/gosim-route.md:27 — WARNING — storage row omits real controls
- Text said: SetCrashMode and SetSyncFault only.
- Source (fs/control_sim.go; docs/features.md fs rows): `SetReadOnly` exists ("A write attempted while read-only returns `EROFS`"); `fs.Config.CapacityBytes` gives `ENOSPC`; SetCrashMode "selects `DurableOnly` or `SamplePending`"; random faults row: "General random I/O errors, silent corruption, and injected short reads are not exposed as controls."
- Fix: named the two crash modes, added SetReadOnly/CapacityBytes, quoted the non-exposed faults.

### F4 references/gosim-route.md:29 — WARNING — time row cited features.md for a scheduler claim it does not make
- Text said: "virtual timeout is not a demonstrated CPU-bound-loop interrupt".
- Source (docs/design.md Engine): "cooperative coroutine scheduling"; "When no goroutine is runnable, simulated time can advance to the next scheduled event." features.md: "`rt.SetTimeout` bounds simulation time."
- Fix: restated with those quotes and design.md citation.

### F5 references/gosim-route.md:31 — WARNING — replay gap: Ed25519 nil reader
- Text said: nothing on host-randomness escapes.
- Source (docs/design.md; features.md native hashing row): "`GenerateKey(nil)` uses native host randomness and is not replay-deterministic."
- Fix: added one sentence with citation.

### F6 SKILL.md:20, fault-design-and-replay.md:21, common-mistakes.md:12 — WARNING — paper limitation paraphrased past its text
- Text said: "virtual-time acceleration is not a performance prediction" cited to FDB §4 limitations.
- Source (FDB paper p. 9, page-008.png, Limitations): "Simulation is not able to reliably detect performance issues". The paper discusses faster-than-real-time only under "Latency to bug discovery", not as a limitation.
- Fix: reworded to the paper's claim with quote.

### F7 references/other-routes.md:5 — WARNING — FDB blocking/thread effect misstated
- Text said: "blocking or independent workload threads can break its repeatability".
- Source (client-testing.rst, Parallelism and Determinism): blocking in the main network thread "will result in a deadlock"; threads mean "test failures will be non-deterministic".
- Fix: separated the two effects with quotes.

### F8 references/other-routes.md:15 — INFO — Zig version is an exact-match compile check
- Source (build.zig zig_version + comptime block): "unsupported zig version: expected {f}, found {f}" when major/minor/patch differ from 0.16.0.
- Fix: stated exact 0.16.0 requirement with quote.

### F9 references/boundaries-and-oracles.md:7 — WARNING — uncited normative sentence
- Text said: "This pack's reporting convention keeps those evidence states separate."
- Source: none; no primary source supports a pack convention.
- Fix: cut (claim cut).

### F10 references/other-routes.md:27 — INFO — section name and readiness wording
- Text cited "Add a ready signal"; page heading is "Add a ready signal for fuzzing". Page: "Antithesis will treat the first such message sent by any running process as its signal to begin testing and injecting faults."
- Fix: corrected section name, added quote.

### F11 references/common-mistakes.md — WARNING — rows lack the one-line why (skill-draft Step 3 / task check 6)
- Fix: added a Why column, one line per row; headers renamed WRONG / RIGHT and source / Why.

### F12 all files — INFO — load-bearing claims lacked verbatim fragments
- Fix: added 4-10 word quotes retrieved this session (FDB paper images, Gosim README/features/design, VOPR, FDB rst, TigerBeetle blog, Antithesis pages). Each verified by grep against fetched raw text or read from the page image.

### F13 verified without change
- Gosim families 1.25/1.26 (families_gen.go), CGO_ENABLED=0 (load.go sourceEnvironment), Stop/Crash distinct StopGraceful/StopCrash (machine_sim.go), CrashStates/MaxStates/Next/Restore/Close (recovery*.go), RunInfo fields and Certified "Always false" (rt/info.go), MIT license, VOPR seed+commit and fault model, UNIT_TEST_SEED "independent of the cluster simulation seed" (testing.rst), `fdbserver -r simulation -f testfile.txt`, API tester complement, TigerBeetle core healing, Antithesis x86-64/no nested virtualization/no internet access, FDB paper §4 swarm, buggification, recoverability check, §6.2 logging and fidelity sentences. FoundationDB PDF at the cited URL is 1053117 bytes, identical size to the paper-reader copy.

### F14 fault-design-and-replay.md:13 — INFO — `crash-consistency-testing` not yet in the pack
- That skill directory does not exist yet; agent-notes says its research is underway, and five other skills route to it the same way. Left unchanged.

### F15 audit checks 1-6 — INFO
- Frontmatter name/description valid; description matches body scope; SKILL.md 28 lines; all local links resolve; no filler found. No change.

## Pinned URLs

None needed: every GitHub link was already a commit-SHA permalink (gosim 64ac3b2a20806bb4f9470232e12fabdfd5d13852, tigerbeetle 68958eb757747d0fc96a79d1f9c2fa6766b67b48, foundationdb 7e7611f8270952a2b1cffd75aa523c4b057afd62); all fetched at those SHAs with HTTP 200. The TigerBeetle blog (dated URL) and the two Antithesis docs pages have no versioned URL; kept as-is with accessed 2026-11-07 and section names in sources.yaml. The FoundationDB PDF URL is a fixed file (1053117 bytes, same as the paper-reader copy).

## Validation

```
$ python -I C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/deterministic-simulation
Skill is valid!
exit 0
```
(An earlier run failed with `UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d` because of a curly-quote fragment in SKILL.md under the Windows cp1252 default; I swapped it for an ASCII verbatim fragment from the same blog section, and the validator then passed without flags.)

Read-only checker (scratchpad check_ds.py): every quoted fragment was searched in the fetched raw text.
```
cited-not-in-yaml: []
yaml-not-cited: []
moving-urls: []
missing-local-links: []
ending-ok SKILL.md 28 lines
ending-ok boundaries-and-oracles.md 19 lines
ending-ok common-mistakes.md 12 lines
ending-ok fault-design-and-replay.md 21 lines
ending-ok gosim-route.md 31 lines
ending-ok other-routes.md 27 lines
ending-ok sources.yaml 148 lines
```
All non-paper quotes: FOUND. The 12 FoundationDB paper quotes report NOT-IN-FETCHED-TEXT by design (no extracted paper text used); each was read on page images page-007.png (p. 8), page-008.png (p. 9) and page-010.png (p. 11) this session.

`git diff --check -- plugins/bugfinding/skills/deterministic-simulation`: no output, exit 0.

## Unverified

- Printed page numbers do not appear on the page images; "p. 8/9/11" means PDF page order (page-007/008/010.png), as the draft used.
- The commands in gosim-route.md and other-routes.md were not run (no installs or target execution allowed); they match the pinned README/rst/build.zig text only.
- The Antithesis and TigerBeetle-blog pages can change under the same URL; quotes are verified as of 2026-11-07 only.
