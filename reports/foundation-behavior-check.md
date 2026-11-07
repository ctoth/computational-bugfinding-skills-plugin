# Foundation behavior check

## State

Independent application and bounded analysis complete. This report is the only owned output; no target execution or mutation was performed.

## Request applied

Given existing native Go fuzzing, structured programs, engine comparison and transactional histories, inspect the baseline and propose a concrete bugfinding campaign using an additional eight CPU-hours.

## Evidence

Inspected foundation SKILL.md plus all four shipped references directly. Inspected Barn's actual local instructions and fetched `origin/master` workflow, VM fuzz executor, structured generator and differential reader. No target program, test or campaign was executed. Required role file `C:/Users/Q/.Codex/AGENTS.md.d/gauntlet.md` is absent; this bounded analyst task continues under its explicit prompt.

## Applied campaign proposal

### Baseline and scope

Read-only snapshot: Barn local HEAD `69ac215d4a866c20f0a2b5e3d29c2a91454677be`, already-fetched `origin/master` `5e0717ab2d82bc2d79284f172e5e0890900c91b7`. The local checkout is behind 20 commits and dirty; no fetch, checkout, target mutation or claim about live remote HEAD was made. The following references mean the fetched ref, not the older worktree.

- `.github/workflows/fuzz.yml:38-54` lists thirteen native targets and one ToastDifferential lane. Structured generation is already present, so it is not proposed as a new method.
- `internal/fuzzseed/structured.go:56-80` maps arbitrary choice bytes to complete IR and uses the production formatter to render source. `:94-104` supplies choice-byte seeds. `vm/fuzz_test.go:27-33` consumes `[]byte` and runs the rendered program; `:36-64` uses core capabilities/private empty store, treats compile diagnostics as failures for structured inputs, and checks literal round trips after returns. `:65-75` runs forked children serially in creation order, with a shared tick bound. This is not systematic scheduler exploration.
- `.github/workflows/fuzz.yml:112-115` supplies only the string-source VM/compiler corpus/cache paths to the differential lane. `scripts/fuzz_differential.py:89-102` decodes exactly one `string(...)` corpus value; `:144-164` skips undecodable inputs and applies explicit exclusions. Therefore supplying structured-choice corpus files unchanged cannot exercise their rendered programs in this lane.
- `scripts/fuzz_differential.py:54-76,105-118` excludes deliberate Unicode/runtime facts and scheduler/process effects; `:199-220` distinguishes completed comparison from aborted probes. These exclusions cannot be removed merely to raise case counts.

### Selected pilot

**New dimension:** connect the existing semantic generator's rendered programs to the existing completed-result differential oracle. This is a specific producer/representation gap in the inspected workflow, not a claim that all Barn differential tooling is absent or that no uninspected branch has equivalent work. It also does not yet establish which generated programs survive existing exclusions or whether the lane finds a defect.

**Producer:** use the existing `fuzzseed.Source(choices)` rather than duplicate IR or formatter logic. Preserve both exact choice bytes and rendered source. A small target-owned export/replay seam would be needed before execution; this evaluation has not created one. Treat its implementation/validation cost separately from compute expenditure.

**Oracle:** on matched pinned Barn/Toast builds and documented fixture/configuration, compare compilation success and completed values/error codes within the current supported contract intersection. Record excluded, malformed-output and aborted probes separately. Initially choose generated pure deterministic expressions with no persistent world mutation, so the existing process-batched execution does not silently substitute unmatched evolving state. Source audit of selected generated forms and actual lane setup is required before this precondition is established. Any difference is a candidate requiring contract adjudication; it is not automatically a Barn defect.

**Sensitivity:** replay one already-confirmed historical differential regression through the same rendered-source path and one healthy case. If no suitable historical case exists, design a justified observation-level negative control and document that it establishes checker sensitivity only. A failed control or zero successfully compared cases ends this pilot for diagnosis rather than triggering the full search allocation.

### Eight CPU-hour envelope

| Allocation | CPU-hour ceiling | Purpose |
|---|---:|---|
| Producer/decoder replay and sensitivity pilot | 0.5 | Confirm byte-to-source provenance, matched build/configuration and nonzero completed comparison counts. |
| Initial structured differential search | 1.5 | Measure submitted/generated, excluded by reason, completed comparisons, both/one-sided aborts, candidates and semantic-family reach. |
| Evidence-directed continuation | 4.0 | Extend if successful comparisons keep reaching relevant new forms; otherwise correct a verified harness bottleneck or stop with a negative result. Do not automatically multiply identical workers. |
| Replay, reduction and triage reserve | 2.0 | Reproduce candidates independently, retain original/minimized inputs and investigate intended differences or infrastructure loss. Unspent reserve remains unspent. |
| **Total maximum** | **8.0** | Sum process CPU across Barn, Toast, generators and reducers; account build/tool CPU inside this total if charged to the requested envelope. |

Use cumulative process user+system CPU or an equivalent verified owned-resource accounting mechanism. Worker-count × elapsed time is only a conservative allocation bound under a CPU cap, not measured CPU. Wall-clock time, compilation/setup effort and LLM/human triage effort are separate columns. At most two CPU-capped workers would put a 1.5 CPU-hour search ceiling at 45 wall minutes only under full utilization; actual process accounting is authoritative. Stop launching new work before exhausting the envelope and retain enough reserve for existing candidates.

### Retained artifacts and decisions

Retain actual source/ref/build/configuration identity; original choice bytes and rendered programs; original supported corpus inputs; paired raw outputs, exclusions and aborts; generator and execution options; seeds and any controlled decisions; resource counters; reproduction/reduction attempts and case classifications. Do not retain only a seed or stack summary.

Continue only on observed useful completed comparisons and property-relevant reach, or shift the remaining allocation to candidate reproduction. If most generated programs remain excluded/rejected, diagnose the production/generation mismatch first. If the existing comparison cannot faithfully observe the chosen semantics, change or stop the experiment instead of interpreting output differences. Zero confirmed defects is a legitimate bounded result. The proposal is not an executed experiment, a ready adapter, an empirical improvement claim or a product defect finding.

### Decision effect observed

Applying the skill produced a source-cited producer/oracle gap, an explicit supported-contract restriction, a representation-preserving replay proposal, separate sensitivity and resource accounting, and conditional allocation. It did not simply increase native fuzz duration or relabel Barn's existing mechanisms. This is observed decision/artifact behavior from one evaluator, not evidence of increased discovery yield or a controlled comparison with an unassisted agent.

## Foundation quality findings

**Proceed with this foundation as the drafting reference. No blocking defect was established in this bounded check.** This is a skill-quality judgment, not approval of a Barn campaign or a claim of bug yield.

- SKILL.md is 57 lines, with portable name/description frontmatter, a precise campaign-selection trigger, and conditional specialist routing. All four shipped references were read. Local Markdown reference links resolve; all ten distinct cited primary URLs have matching sources.yaml entries. No unfinished scaffold, hardcoded user path, executable framework or companion-plugin dependency was found in these files.
- Primary Fuzz Introspector documentation supports the static-reachability/dynamic-coverage distinction and its documented language restriction; SQLite's actual testing page supports joint SQL/database input search and its mutation-testing section; FuzzBench's actual report documentation supports repeated trial variability. Elle's already-processed paper was independently checked as page images 3, 7 and 12 for recoverability/traceability, soundness versus completeness and omitted predicate analysis. These checks support the foundation's bounded claims without claiming every linked external page was exhaustively reaudited.
- The illustrative campaign reference explicitly labels its scenario as unexecuted and requires confirming the presumed gap against actual source. This avoided turning the example's empty-world/permission premise into a statement about all Barn tests.
- The foundation does repeat a few short reminders about reach, replay and uncertainty in its references. They apply to different failure decisions; this check did not establish redundancy that prevents useful loading or warrants a blocking rewrite.

## Limits and follow-through

- At this foundation-only stage the 24 named specialist skills are not all present. Their names are a routing promise to the approved build, not evidence of presently usable methods; collection audit must verify every name and scope once drafting is complete. This does not block using the completed foundation as the quality reference for that drafting.
- No new adapter, instrumented build, campaign, sensitivity control or negative result was executed. The proposed eight-CPU-hour experiment needs its target-owned replay seam and contract/configuration checks before execution. No source finding here establishes an actual product bug.
- This evaluation saw the skill's own worked example, as an ordinary consumer does; it did not read parent research/plan conclusions before generating the proposal. A single evaluator cannot establish a causal improvement relative to an unassisted baseline. Later blind historical-defect evaluations remain necessary for any discovery-power claim.
- Shared checkout dirt and already-fetched refs were preserved. No claims were made about current live remote head, CI or production behavior. The absent gauntlet role file is recorded above; no substitute tool/role policy was invented.
