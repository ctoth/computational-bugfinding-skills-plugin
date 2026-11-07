# Improve liveness-testing

## Findings

Paper evidence: CHESS (Musuvathi et al., OSDI 2008) page images `bugfinding-literature/schedule-exploration/papers/Musuvathi_2008_FindingReproducingHeisenbugs/pngs/page-007..009.png` and FoundationDB (Zhou et al., SIGMOD 2021) `bugfinding-literature/deterministic-simulation/papers/Zhou_2021_FoundationDB/pngs/page-008.png`, produced by paper-reader, viewed as images this session.

### F1 — ERROR — CHESS section citations point to §5 for monitor content that is in §4.5
- Locations: `SKILL.md:8` ("§§4.2–4.3 and 5"), `references/common-mistakes.md:5` ("§§4.2–4.3 and 5"), `references/witnesses-and-replay.md:8` ("§§4.2 and 5"), `references/sources.yaml:7`.
- Source: the enabled-task deadlock monitor, the fair-termination reduction of liveness and the "abnormally high bound on the length of the execution" are in §4.5 "Monitoring executions" (page image 009, left column). §5 is "Evaluation"; only §5.2 mentions sleep/yield calls. URL: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf
- Fix: section references changed to §§4.2, 4.3, 4.5 (and §§4.2, 4.5 for the deadlock row); quote fragments added.

### F2 — WARNING — Witness interpretation omits Coyote's end-of-execution hot-monitor check
- Locations: `SKILL.md:24`, `references/witnesses-and-replay.md:9`, `references/runtime-and-model-routes.md:17`.
- Text: only the temperature-threshold heuristic is described as Coyote's liveness evidence.
- Source: `CoyoteRuntime.cs` `CheckLivenessErrors()` runs at test termination ("Checks for any liveness errors at test termination.") and reports "detected liveness bug in hot state '{1}' at the end of program execution" for a monitor still hot, and "Found liveness bug at the end of program execution" for an unsatisfied task monitor; this check is not gated by the threshold. The how-to calls this the "safety property and easily checked" half. URLs: https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Runtime/CoyoteRuntime.cs, https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/liveness-checking.md
- Fix: added a witness-table row and a sentence in routes distinguishing a terminated execution with a hot monitor from threshold exhaustion.

### F3 — WARNING — Coyote route omits that unfair schedulers cannot find liveness violations, and the --max-steps-derived bounds
- Location: `references/runtime-and-model-routes.md:11-17`.
- Source (liveness-checking.md, "Fair and unfair scheduling"): "Unfair schedulers have a role to play in finding violations of safety properties, but not in finding violations of liveness properties."; `prioritization` "is unfair"; with `--max-steps N` a fair execution "can go to up 10N steps" and staying hot "for more than 5N steps" flags a liveness bug. `Configuration.cs` sets the default threshold to `MaxFairSchedulingSteps / 2`.
- Fix: one sentence added to the Coyote route; Configuration.cs added to sources.yaml.

### F4 — WARNING — Coyote `--no-repro` replay limit not stated
- Location: `references/runtime-and-model-routes.md:15` ("Unsupported operations need their actual model/replay limits") and `references/witnesses-and-replay.md:16`.
- Source (using-coyote.md, "Supported scenarios"): `--no-repro` ignores unsupported-type errors "by *disabling the ability to reproduce* bug traces (i.e., no `.trace` file will be produced when a bug is found)".
- Fix: cited and stated concretely in routes and witnesses.

### F5 — WARNING — Go synctest's own deadlock panic is not mentioned; skill implies synctest gives only quiescence
- Locations: `SKILL.md:24`, `references/witnesses-and-replay.md:7`, `references/runtime-and-model-routes.md:33`.
- Source (synctest.go package doc, "Blocking"): when every bubble goroutine is durably blocked and no time advance unblocks one, "there is a deadlock and [Test] panics"; durably blocked means "can only be unblocked by another goroutine in the same bubble". Mutex/I-O/syscall waits are excluded, so a mutex deadlock is not this witness. URL: https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/synctest/synctest.go
- Fix: added the bubble-deadlock panic as a supported witness with its scope, in routes and the witness table.

### F6 — WARNING — "step budget exhausted" row does not say Coyote treats a reached step bound as a non-failure by default
- Location: `references/witnesses-and-replay.md:9`.
- Source: `CoyoteRuntime.cs` `CheckIfSchedulingStepsBoundIsReached()` asserts only `if (this.Configuration.FailOnMaxStepsBound)`, else logs and `Detach(ExecutionStatus.BoundReached)`; `Configuration.cs` defaults `FailOnMaxStepsBound = false`. using-coyote.md: after N steps "the iteration is killed and a new one is started".
- Fix: row text states the default bound-reached outcome and cites runtime + Configuration.cs.

### F7 — WARNING — Coyote how-to temperature prose differs from the pinned code
- Location: `references/runtime-and-model-routes.md:17`.
- Source: liveness-checking.md says the temperature "goes up by a unit if the monitor transitions to a hot state"; `Monitor.cs:616-628` increments on every call while `this.ActiveState.IsHot && threshold > 0`, and `CoyoteRuntime.cs:870-873` calls it at each scheduling point when `IsIterationFair`.
- Fix: one clause noting the code counts fair scheduling steps spent hot, so read the code over the prose.

### F8 — WARNING — TLC command `-config` cited only to USE.md, which does not document `-config`
- Location: `references/runtime-and-model-routes.md:21-25`.
- Source: USE.md shows only `java tlc2.TLC -help` and `-dump`/`-dumpTrace`/`-loadTrace`; `-config` is defined in `TLC.java` ("provide the configuration file; defaults to SPEC.cfg").
- Fix: added TLC.java citation for `-config`.

### F9 — WARNING — LiveHourClock is cited as a model to imitate without noting its config deliberately checks a false property
- Location: `references/runtime-and-model-routes.md:27`, `SKILL.md:18`.
- Source: LiveHourClock.cfg has `PROPERTY ClockSettles` and `POSTCONDITION PostCondition`; LiveHourClock.tla's `PostCondition` asserts a specific `CounterExample`. URL: https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/test-model/examples/SpecifyingSystems/Liveness/LiveHourClock.cfg
- Fix: caution added in routes; .cfg added to sources.yaml.

### F10 — INFO — TLC symmetry/distributed citations are Toolbox help pages; README marks the Toolbox unmaintained
- Location: `references/runtime-and-model-routes.md:29`, `references/common-mistakes.md:10`.
- Source: README "Use": "The Eclipse-based TLA⁺ Toolbox GUI is also available from this repository, but it is currently unmaintained."
- Fix: provenance clause added in routes; sources.yaml section names updated. Not re-verified against distributed TLC source (see Unverified).

### F11 — ERROR — common-mistakes.md rows lack the one-line why required by skill-draft Step 3
- Location: `references/common-mistakes.md:3-12`.
- Fix: added a WHY column to each row, keeping WRONG first then RIGHT; quote fragments added.

### F12 — WARNING — load-bearing claims lacked verbatim quote fragments
- Locations: SKILL.md:8,12,14,20,24,26,28; progress-contracts.md:7,9,13,15; runtime-and-model-routes.md:7,15,17,21,29,33; witnesses-and-replay.md rows.
- Fix: 4-10 word fragments retrieved this session added before each citation.

### F13 — WARNING — uncited normative sentences
- `references/progress-contracts.md:7` "Idle service with no admitted work differs from unfinished admitted work." Fix: cited Coyote liveness-checking.md (hot/cold obligation; "any terminated execution of the program must not have a monitor in a hot state").
- `references/progress-contracts.md:9` "A harness that withholds the only required response has changed the premise." Fix: cited CHESS §4.3 ("consider these interleavings impossible or unlikely in practice").
- `SKILL.md:14` "Do not invent eventual delivery or a deadline" Fix: cited TigerBeetle's environment-conditioned property ("if the operating environment is sufficiently healthy").
- `SKILL.md:20` compute allocation over admissible faults. Fix: cited FDB §4 ("avoid driving the system into a small state-space").
- `SKILL.md:28` "a model witness still needs implementation correspondence". Fix: cited USE.md trace dump/load "to support model-based testing and trace validation".

### F14 — INFO — TigerBeetle's liveness oracle is a timeout applied after the healthy regime is fixed
- Location: `references/progress-contracts.md:15`.
- Source: the simulation "reports the liveness bug" "when, after a timeout, a replica is still missing some log entries". This bounds the skill's "do not invent a deadline" guidance: their timeout is applied only inside the frozen healthy-core regime.
- Fix: one clause added with quote.

## Pinned URLs

No moving URLs were present: every raw.githubusercontent.com link already used a 40-hex SHA (Coyote `2202e75a861f4e8a63149366c2e41ea21d73ae54`, TLA+ `d8fb231de4e4b5d02c1b2ed1ac759c086f694021`, Go `dcc06a82727b447270b1a58cc5f86b49736e317c`), and each was fetched at that SHA this session with curl. Two new citations were added at the same pins: `Source/Core/Configuration.cs` (Coyote) and `.../Liveness/LiveHourClock.cfg` (TLA+). The CHESS and FDB PDFs and the TigerBeetle blog are publisher URLs with no versioned form; sources.yaml records the date/sections (TigerBeetle: dated 2023-07-06, author matklad). URLs pinned: 0 (none needed).

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/liveness-testing
Skill is valid!
exit 0

$ git diff --check -- plugins/bugfinding/skills/liveness-testing
exit 0

$ python -I scratchpad/check_live.py plugins/bugfinding/skills/liveness-testing scratchpad/live   (NOCACHE lines for the two PDFs omitted)
cited not in yaml: []
yaml not cited: []
QUOTE MISS runtime-and-model-routes.md 'Time in a bubble only advances when every goroutine in the bubble is durably blocked' g_synctest.go
problems: 1
```

The single QUOTE MISS is a checker artifact: in synctest.go the sentence spans a comment line break (`// Time in a bubble only advances when every goroutine in the` / `// bubble is durably blocked.`); the words are verbatim. The checker also confirmed: no broken local links, no moving/unpinned URLs, every file ends with exactly one newline. PDF quotes (CHESS, FDB) were checked by eye against the page images listed above.

Line counts: SKILL.md 30; references 12/21/33/20 lines; sources.yaml 20 entries, every entry has name/url/type/accessed='2026-11-07'/sections_used.

Claims cut: 0. Files touched: only `plugins/bugfinding/skills/liveness-testing/**` and this report. Nothing staged or committed.

## Unverified

- "Distributed TLC does not check liveness" rests on the Toolbox help page (README marks the Toolbox unmaintained); not checked against the distributed TLC server source. The text now states that provenance.
- The FDB quotes come from printed p.9 under §4; the subsection labels "Test oracles" and "Fault injection" are the paragraph run-in heads on that page, not numbered subsections.
- No Coyote, TLC or Go command was executed; behaviour claims are from source reading at the pinned SHAs, not from released binaries.
