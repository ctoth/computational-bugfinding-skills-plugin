# Research: linearizability-checking

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This is the only owned repository output; paper-reader artifacts are external. Literature uses paper-reader and page images only. No target execution, installation, target mutation, commits or publication.

## Evidence ledger

Inspecting actual Porcupine operation/event/model APIs, pending and ambiguous outcomes, partitioning and witness/resource limits, then foundational linearizability literature as paper images.

### Early verified primary evidence

- Porcupine model.go documents closed operation intervals: equal response/invocation timestamps leave operations concurrent. It also requires pure Step transitions and partitioning whose per-partition results are equivalent to whole-history linearizability. Sources: https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go (Operation; Model), accessed 2026-11-07.
- porcupine.go supplies bounded/verbose checker APIs with explicit CheckResult; timeout zero means unlimited. A checker budget exhausted is not a non-linearizable verdict. Source: https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go (CheckOperationsTimeout/Verbose; CheckEventsTimeout/Verbose), accessed 2026-11-07.
- Jepsen's formal model page distinguishes real-time single-object order from sequential consistency and multi-object transactional guarantees. Source: https://jepsen.io/consistency/models/linearizable (Formally), accessed 2026-11-07. The primary paper linked there is being selected for image reading; no paper finding is yet claimed.

Referenced developer researcher role file does not exist at its supplied path. Explicit parent task constraints govern this bounded research.

### Literature image evidence

Alex Horn and Daniel Kroening (2015), *Faster linearizability checking via P-compositionality*, https://arxiv.org/abs/1504.00204 and https://arxiv.org/pdf/1504.00204 . Retrieved canonical PDF, rendered with installed paper-reader helper (15 pages), visually verified title/authors on page 1, and directly read all fifteen local images page-000 through page-014. Local paper-reader directory: `C:/Users/Q/code/bugfinding-literature/linearizability-checking/papers/Horn_2015_PCompositionality/`. No extracted paper text used and no process/tag/reconcile orchestration.

- pp.3-5 define histories, matching calls/returns, executable sequential specifications and real-time precedence. The paper assumes completed/deadlock-free histories for its decision procedure. **Decision:** recorder validity and treatment of incomplete observations are prerequisites; a checker is not a deadlock/liveness detector.
- pp.5-7 define P-compositionality as an if-and-only-if property over partitions. Key partitioning is valid for independent set/map operations but generally not for a global size operation (p.6). **Decision:** partition by proved semantic independence, not convenient key fields; cross-key/aggregate operations can invalidate the speed optimization.
- pp.7-10 describe WGL backtracking over a persistent executable state, cached pairs of linearized operation IDs and model state, and independent parallel partitions. **Decision:** pure model state/equality/hash semantics and controlled checker cost matter; mutating prior model states can corrupt backtracking.
- pp.11-12 report historical experiments: four threads, 70K operations each, key domain [0,24), >700 histories, one-hour cutoff. Runtime/memory means exclude timed-out runs. **Decision:** budget and report checker-inconclusive outcomes, and do not infer contemporary universal speedups or bug yield from this study.
- pp.13-14 distinguish finite observed-history checking from verification of all possible implementation executions, and limit the optimization to P-compositional specifications. **Decision:** an accepted history is bounded evidence; the workload/schedule search and oracle model remain separate.

Paper-reader artifacts inspected: canonical PDF and fifteen images, dense page-cited notes with equations/algorithms/parameters/results, metadata, description, abstract paraphrase, all 31 bibliography identities, index, processed ledger and helper-generated keymap. Reader's nested reconcile is excluded by parent/Q reader-only instructions; it was not invoked. No process/tag/reconcile or propstore workflow ran.

## Primary source handoff (accessed 2026-11-07)

### S1 — Porcupine model and history contract

URL: https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go ; Operation/Event and Model/NondeterministicModel sections. Quote fragment: “purely functional”.

Pure transitions, semantic state equality and equal-state hashing govern search correctness; default equality uses Go ==, so mutable/map/slice states need a fitting explicit equality. Closed numeric intervals preserve concurrency at tied endpoints; Event identities pair calls/returns. NondeterministicModel represents permitted successor sets, not uncertain observations converted into success. Check selected release availability of StepContext and other newer APIs; mutable master is dated evidence, not a release guarantee. Master ref observed via git ls-remote was 97cd067defd99df172053ba7f4ca5bbae57fe446, but actual campaigns must retain their own selected revision. No source file or target was changed.

### S2 — Actual checker producer/search and results

URL: https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go ; makeEntries 118-129, makeLinkedEntries 178-195, checkSingle 241-317, checkParallel 352-432, checkEvents/checkOperations 434-451. Quote fragment: “matching return”.

Operations become paired entries, events are renumbered and converted in supplied order, and the search explores model-admissible orders. It does not infer missing responses or repair malformed recorders. Validate matching IDs/order and preserve recorder errors separately. A raw unmatched call is not the documented general-purpose representation of an ambiguous completed request. The result construction can return Illegal for an established rejected partition, Unknown for exhausted checking without a completed decision, or Ok for completed acceptance. Verbose mode waits for partition workers to finish; legacy blocking Step callbacks do not automatically become interruptible. Prefer the supported cancellation-aware callback when model work can block and retain an outer authorized resource envelope. These are inspected source boundaries, not a defect report; no violating target was executed.

### S3 — Current public checker APIs

URL: https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go ; full 44-line source read. CheckOperations/CheckEvents return bool without timeout; bounded APIs return CheckResult, verbose forms additionally return LinearizationInfo. Timeout 0 means no deadline. Conditional source-derived invocation in an existing Go test: call `porcupine.CheckOperationsVerbose(model, operations, chosenTimeout)` and handle Ok/Illegal/Unknown distinctly. A finite duration is chosen from the actual model/history cost and budget, not a pack default. No checker call was run here.

### S4 — Real pending-operation adapter and partition callers

URL: https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go ; register examples 19-123, etcd model 219-286 and parseJepsenLog 288-383, kvModel 1235-1300, nondeterministic tests 1794 onward. Quote fragment: “unknown”.

The actual etcd test adapter records uncertain read outputs and appends modeled unknown returns for calls left open at history end (379-381), then its checker caller invokes CheckEvents (386-392). The KV model partitions both calls and their matched returns by key. These are real example producers, not authorization to assign every timeout the same semantics. The adapter must preserve the target's possible outcomes/effects and interval uncertainty. Do not copy a test parser or assume a timed-out write never committed. Model tests also check unknown results/cancellation and nondeterministic state sets; these demonstrate APIs, not coverage of an arbitrary new model.

### S5 — Evidence and visualization

URLs: https://raw.githubusercontent.com/anishathalye/porcupine/master/visualization.go (Visualize/VisualizePath, 219-255); https://github.com/anishathalye/porcupine (Usage, Notes, Visualizing histories).

Verbose evidence can retain accepted complete orders or rejected partial orders and render them as self-contained HTML via Visualize/VisualizePath. Save the raw history and model too: a partial search visualization is not a minimal unsatisfiable core or root-cause proof. Current README warns that timestamp instrumentation can itself be unsound on weakly ordered architectures. Recording must bracket the actual operation with justified ordering; do not infer real-time edges from unsynchronized client clocks. Rendering replays the model, so impurity can also invalidate visualization. No HTML was generated or displayed here.

### S6 — Real-time contract and shortcut failure

Sources: https://jepsen.io/consistency/models/linearizable (Formally); https://github.com/anishathalye/porcupine/issues/35 (author's September 2025 follow-up, lines 180-184).

The target contract determines object scope and real-time precedence; transaction isolation does not supply this guarantee. In the primary issue, an attempted performance shortcut removed sorting and accidentally turned overlapping calls into alternating call/return pairs. The reporter recognized that this changed the history rather than safely optimized search. Decision: never improve checking speed by serializing or deleting inconvenient overlaps. Internal revision/order hints require justified constraints that preserve all admissible real-time/model orders, not a guessed total order.

### S7 — Setup, module and license

Sources: https://raw.githubusercontent.com/anishathalye/porcupine/master/go.mod ; https://raw.githubusercontent.com/anishathalye/porcupine/master/LICENSE.md ; https://go.dev/doc/modules/managing-dependencies (Adding a dependency; Getting a specific dependency version).

Module path is github.com/anishathalye/porcupine, inspected go.mod declares Go 1.16, and actual LICENSE.md is MIT. This declaration is not proof of compatibility with every future toolchain/platform. Prefer a fitting existing integration and inspect selected-release API/source. If dependency changes are authorized, Go supports `go get github.com/anishathalye/porcupine@SELECTED_VERSION`; that changes go.mod/go.sum and downloads source. No installation/update was run. Use the project's permitted focused test runner for its real history/model test; this skill need not install a CLI, container, universal client or new recorder service. Ordinary package/module mechanics remain existing language-skill ownership.

Conditional runner shape for an existing authorized integration: `go test ./path/to/pkg -run '^TestLinearizability$' -count=1 -timeout=60s`. Official flags source https://pkg.go.dev/cmd/go#hdr-Testing_flags was read for selection/cache-count/test-binary timeout. The 60-second value is illustrative, not a recommendation or checker-specific deadline; the Porcupine timeout and model cancellation remain separate. No test command executed.

## Decisions that change useful checking

The following is proposed plugin design derived from S1-S7 and the paper, not a universal schema or a new checker implementation.

### Establish the actual sequential contract

Read the real public operation producer, enabled configuration, initialization and failure semantics. Model the abstract facts necessary for admissibility and returned/effect outcomes; do not port target internals. A set's insert/remove/contains differs from a map with cross-key transactions or a queue with blocking calls. An operation that can legitimately fail must have its actual failure/effect semantics represented. A completed error is not automatically no-op, while a response timeout does not determine whether a request took effect. Keep unsupported semantics or missing observations explicit. S1/S4 and paper pp.3-5 ground the boundary.

Test model/recorder sensitivity using known legal and deliberately illegal histories through the same import path. Check initial state, matching IDs, duplicate/missing responses, within-operation order, serialized parameter values and actual call brackets. Distinguish model rejection from malformed input, panic and checker exhaustion. Do not require a new mutation framework; use existing justified controls. Detailed sensitivity belongs to harness-sensitivity, result attribution to evidence-based-triage.

### Treat time and incomplete operations as evidence

Preserve the recorder's genuine happens-before relations and uncertainty. A controller's ordered event log and a set of cross-host wall-clock timestamps have different evidential properties. Ties in Porcupine Operation intervals mean overlap. Do not sort by completion/revision to erase concurrent candidates. Preserve original raw client/server observations separately from the converted checker representation (S1/S2/S5/S6).

For missing/ambiguous responses, derive a supported completion/abstraction from the actual API contract: possible applied and unapplied effects, known rejection, and latest admissible completion boundary. The exact model may require nondeterministic successor states or explicit case exploration. Preserve all relevant possibilities when claiming an Illegal result; if those possibilities cannot be encoded or bounded soundly, report the history unresolved. Appending a modeled unknown response at the end is one actual test-adapter technique (S4), not a universal proof that an arbitrary pending call is safe to complete that way. Never invent a successful output or drop an uncertain write merely to make the checker accept. An adapter that loses uncertainty changes the experiment.

### Prove the partition, then use it

P-compositionality is a semantic iff condition, not a heuristic. Single-key independent operations may permit per-key models. Global size, scans, multi-key compare/swap, transfer, allocation limits or cross-key invariants can couple partitions; read the actual contract before splitting. Omitting a global operation from every partition is lost evidence, not an optimization. Preserve both Call/Return events in the same partition; the real KV example uses an identity-to-key map (S4). Small partitioned/unpartitioned cross-checks can expose a broken adapter, but are not a proof of all future partition validity. If independence is unestablished, keep a whole model and a finite bound rather than weaken the oracle. Paper pp.5-9 and S1 support this decision.

### Bound checking separately from workload generation

Useful compute can buy more operations, more overlap, more key interactions or more checker time, but each changes cost and evidence differently. Heavy overlap and weak observations expand alternative orderings; pure model/equality/hash costs and partition sizes matter. Record history/operation count, peak overlap if available, partition distribution, model-check elapsed/CPU/memory, deadline and result. Avoid universal history length or timeout thresholds. One accepted history does not cover unseen schedules; one Unknown is not a linearizable result. Keep observed accepted/rejected/inconclusive histories separate even where an upstream API comment permits a user to treat Unknown as no found violation (S1/S2 and paper pp.11-14).

StepContext is a selected-version cancellation seam, not a hard process timer; a callback that ignores cancellation can still block a worker. The verbose collector's wait and later visualization replay have their own cost. Use target/task-approved outer limits and owned resources where needed, not broad process cleanup or relaxed checking. The general campaign skill allocates the budget; this skill interprets the actual checker outcomes.

### Preserve a reviewable witness

Save original history, converted history, adapter rules and uncertainty, exact model/checker/build/configuration, initial-state evidence, invocation/options/resource limits, result and LinearizationInfo/HTML if produced. Explain the contradiction using actual calls, real-time edges and sequential contract; do not infer a target root cause from a partial order visualization. Reduce operations/values only while preserving matching calls/returns, initialization, true real-time edges, possible unknown outcomes and the same contract violation. Required setup or coupled operations may not be removable. Failure-reduction owns generic reduction; schedule-exploration supplies controlled schedule traces when available. The checker does not generate workload or inject faults by itself.

## Advanced worked scenarios

Illustrative designs, not executed targets or established Barn defects.

1. **Same-key stale read after an acknowledged write.** The actual contract promises linearizable read/write of one register. Preserve initialization, call/return brackets and values; a read that begins after acknowledged write completion must fit a legal model order. Overlapping reads may legally observe earlier state. A checker rejecting both cases could reveal a recorder/model defect rather than a product fault. Keep matched healthy/illegal controls and inspect the real-time edge.
2. **Per-key checking hides a coupled operation.** A target adds an atomic two-key transfer or global size call to an existing independent-key API. Retaining only per-key reads/writes or assigning the global call to one arbitrary key loses the coupling. Establish a whole-object model or a justified richer partition; do not sell a faster key check as the same guarantee.
3. **Timed-out mutation with a later observed value.** Client loses the response to a write; a later completed read observes the write's value. Treating the timeout as a known failed/no-op write can manufacture a violation. Conversely, blindly completing every pending operation successfully can hide another case. Preserve uncertain effect/completion possibilities according to the real API and use an appropriate model or leave the evidence unresolved.
4. **Performance shortcut serializes the history.** Replacing overlapping event order with successive operation pairs can make search fast by deleting legitimate alternatives and changing the premise. The actual issue S6 records this failure. Preserve observations and optimize model/partition/search only where equivalence is established.

## Barn calibration and existing ownership

The domain report already documents strong Barn serializable-history/Elle fault controls and operation boundaries. This research did not re-audit Barn or infer its public operations promise linearizability. The new capability is a suitable executable sequential model plus genuine real-time histories for an applicable operation contract; it cannot be obtained by relabeling an Elle result. Installed go-race-and-memory-model was read: it owns data races/memory-model authoring, not this abstract concurrent-history oracle. Race-free execution and correct transaction isolation remain distinct evidence.

Stateful generators, schedule controllers, distributed fault injection and transaction dependency checking are separate skill owners. Link them rather than duplicate their implementation. No universal client, model-copy framework, generic event schema service, installation requirement or recurring approval gate is warranted.

## Drafter handoff and evaluation

Suggested references: model-and-history.md (pure model/recorder/uncertainty); partition-and-cost.md (semantic iff, cross-key counterexample, explicit results/cancellation); porcupine-operation.md (conditional selected-version APIs/setup and visualization), plus required common-mistakes.md and sources.yaml. Inventory actual source URLs and paper pages; local paper paths are provenance only, never distributed dependencies. Keep entrypoint concise and tool operationally useful.

Blind evaluation can supply a raw API contract and histories including a legal overlap, genuine stale read, incomplete mutation, malformed pairing, invalid key partition and exhausted checker result. Ask the agent to produce a justified model/conversion and preserve the actual result/evidence without expected diagnoses. A finite legal history, unchecked pending operation or output picture is not an empirical discovery-yield claim. No such evaluation was run here.

## Verification limits and completion

All technical findings come from actual primary docs/source or fifteen directly read paper images. Full source files model.go/porcupine.go/checker.go and relevant visualization sections were read; test source reads were bounded to named actual producers, not all 1946 lines. Primary issue author comments were read, not treated as an accepted library feature. Source/main refs are dated snapshots; selected-version API support remains an execution prerequisite. Herlihy/Wing's original PDF was located but not read and supplies no paper claims here. No guessed pending-call API, automatic completion support or cross-runtime CLI is advertised.

Paper artifacts inspected externally: PDF, fifteen images, notes with equations/parameters/algorithm/results, metadata, description, abstract paraphrase, all31 bibliography identities, index, reader ledger and keymap. Source abstract is retained only in canonical PDF, not copied verbatim. Parent/Q reader-only instruction excludes reconciliation/tagging/process workflows, so no such completion is claimed. No installs, checker/target tests, target mutation, git changes/commits, host registration or publication. Report ready for independent drafting.
