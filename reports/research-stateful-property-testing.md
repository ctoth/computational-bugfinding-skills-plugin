# Research: stateful-property-testing

Date: 2026-11-07

## State

Per-skill research complete for drafting. This is the only owned repository output; paper-reader artifacts are task-local outside the repository. No drafting, target mutation/execution, installation, commit or publication.

## Evidence ledger

Reading the approved scope, primary stateful-testing tools, implementation details and relevant literature through paper-reader/page images only. No target execution is claimed.

### S1: Hypothesis stateful tests

- URL: https://hypothesis.readthedocs.io/en/latest/stateful.html ; accessed 2026-11-07; rule-based machines, bundles and runtime test integration.
- Quote fragment: “entire tests”.
- Finding: state-machine rules compose into operation sequences; bundles pass actual earlier results to later operations. `consumes()` removes a selected value from a bundle; state-dependent draws beyond bundles can use `runner().flatmap(...)` or `data()`. Ordinary strategies do not automatically inspect current machine state.
- Decision: express identities and dependencies deliberately. A bundle is not by itself a complete lifetime/permission model; encode actual admissibility and the promised effect. Do not regenerate unrelated identifiers for every operation and mistake rejected calls for deep state coverage. Python-specific APIs are not a Go integration.
- Documented integration: `RuleBasedStateMachine.TestCase` works with unittest/pytest. Current compatible Python/runtime/package setup remains to verify; no command run.

### S2: RapidCheck stateful model and command contracts

- URL: https://raw.githubusercontent.com/emil-e/rapidcheck/master/doc/state.md ; accessed 2026-11-07; Command<Model,Sut>, command generation and state check.
- Quote fragment: “always assert all preconditions”.
- Finding: model and SUT start in matching states; `apply` updates the abstract model, `run` exercises the actual system, and command preconditions are checked during generation and shrinking. A command's generation-time state can differ from the state in which a shrunk case executes. The framework can generate valid state by executing valid operations when arbitrary-state constructors are unavailable or hide relevant state.
- Decision: recompute validity from the replayed/shrunk prefix, not captured generation assumptions. Keep a small contract model distinct from implementation internals; use real setup operations for hidden state. C++ integration is a conditional runtime route, not a required package.

### Existing ownership and discovery limits

Read installed golang/go-testing-advanced: native fuzz arguments/corpus basics, coverage and synctest are already covered. New material must be dependent operation generation, semantic model/identity/lifetime constraints and valid sequence shrinking. No exhaustive skill-marketplace novelty claim.

fast-check's supplied advanced-model page timed out twice through web; no technical claim is inferred from the failed responses. Official repository docs/source will be used instead. The developer-referenced researcher role file does not exist at its stated path; explicit assigned task constraints apply.

### S3: fast-check model-based commands and replay

- URL: https://raw.githubusercontent.com/dubzzz/fast-check/main/website/docs/advanced/model-based-testing.md ; accessed 2026-11-07; command definition, runners and replay.
- Quote fragment: “what was really executed”.
- Finding: commands provide `check`, `run` and readable serialization; `commands` shrinks executed commands and requires its emitted `replayPath` in addition to assertion `seed`/`path`. Synchronous, asynchronous and scheduled runners have distinct roles. Position-based selection from the current model can keep dependent choices valid, but logs should identify the resolved object.
- Decision: save actual executed sequence, identities and full replay fields; seeds alone are not sufficient. Prefer the appropriate sequential runner here; controlled scheduling belongs to schedule-exploration. Do not clone the SUT as its model.

### S4: fast-check executable runner source

- URL: https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/ModelRunner.ts ; accessed 2026-11-07; lines 43-64, 71-87 and 135-149.
- Quote fragment: `if (cmd.check(m))`.
- Actual behavior: sync commands run only when check returns true; async runner awaits both check and run; scheduled runner wraps scheduled commands and drains controlled work. A generated command list can contain skipped commands, so generated count is not successful operation count. Mutable main source is a dated snapshot, not a reproducibility pin.
- Decision: measure admitted/executed successful operations and property evaluations, not raw list length. Await the selected async runner; an unawaited test can miss failures.

### S5: Rapid state machine implementation for Go

- URL: https://raw.githubusercontent.com/flyingmutant/rapid/master/statemachine.go ; accessed 2026-11-07; T.Repeat, StateMachineActions and executeAction.
- Quote fragment: “before/after every other action invocation”.
- Actual behavior: `T.Repeat` runs a random sequence; the empty-key action is the invariant hook, also run initially. It retries skipped actions, bounds those attempts with `validActionTries = 100` in this snapshot, and reports inability to find a valid action. `StateMachineActions` derives actions from eligible exported methods, excluding `Check`. MPL-2.0 header.
- Decision: a concrete Go-native stateful route exists. Avoid interpreting action starvation/skip exhaustion as product failure; construct useful admissible choices rather than rely on random nonexistent handles. The bound is an implementation detail, not a skill-prescribed test threshold. No code was executed.

### S6: Hughes stateful testing literature, paper-reader image evidence

- John Hughes (2016), *Experiences with QuickCheck: Testing the Hard Stuff and Staying Sane*. Primary author PDF: https://publications.lib.chalmers.se/records/fulltext/232550/local_232550.pdf ; DOI: https://doi.org/10.1007/978-3-319-30936-1_9 . Accessed 2026-11-07.
- Downloaded into canonical task-local paper directory, counted/rendered 18 pages using installed paper-reader `render_pages.py`, and directly read every page image page-000 through page-017. Title/author verified visually on page 1. No PDF text extraction used for reading; web PDF response auto-extraction was not used as evidence. No paper-process/tag/reconcile orchestration.
- Findings from direct images: model preconditions can be wrong; call statistics reveal omitted APIs (pp. 4-9). Tests must preserve hidden-state setup: a create/close/reopen prefix mattered to a historical storage failure, even when simpler state appeared equivalent (pp. 14-15). Return-value model checks accepted traces whose independent corruption check failed (pp. 14-16). Specifications can themselves be defective, and repeated reduction can converge on already-known bugs (pp. 16-17).
- Decision relevance: track operation/semantic reach, preserve state-establishing prefixes, check effects beyond immediate results, and adjudicate model versus implementation. Historical examples are not a promised yield or a current defect finding. Detailed concurrent-history algorithms are other skills' owners.

### S7: Rapid runtime setup, execution and replay

- URLs: https://raw.githubusercontent.com/flyingmutant/rapid/master/README.md ; https://raw.githubusercontent.com/flyingmutant/rapid/master/go.mod ; https://raw.githubusercontent.com/flyingmutant/rapid/master/engine.go ; accessed 2026-11-07.
- Sections: README Usage/Comparison; module declaration; engine command-line flags, MakeFuzz, checkTB/checkFailFile and T thread-safety comments. No claim of an exhaustive read of all 862 engine lines.
- Setup facts: selected master snapshot declares Go 1.23; MPL-2.0. Existing tests use `rapid.Check`; optional `rapid.MakeFuzz` returns the `func(*testing.T, []byte)` shape used by `testing.F.Fuzz`. Ordinary Rapid search itself lacks coverage feedback; the adapter delegates to Go fuzzing.
- Verified command patterns for an existing integration (not run): `go test ./path/to/pkg -run '^TestWorldState$' -args -rapid.checks=COUNT -rapid.steps=STEPS`; replay with the emitted `-rapid.failfile=PATH` or `-rapid.seed=SEED`. Choose COUNT/STEPS from target cost/budget; defaults are not universal recommendations. Preserve fail file, framework version and operation trace. Source checks fail-file format version and can ignore mismatched versions.
- Important limit: draws from a shared Rapid T are not safe for concurrent generation. A generated operation sequence is not systematic goroutine schedule exploration. Fail-file/seed controls only framework choices, not external services or uncontrolled scheduling.

### S8: fast-check package support and existing upstream skill

- URLs: https://github.com/dubzzz/fast-check ; https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/package.json ; https://raw.githubusercontent.com/dubzzz/fast-check/main/skills/javascript-testing-expert/SKILL.md ; accessed 2026-11-07.
- Snapshot package manifest reports 4.10.2, Node engine >=12.17.0 and MIT; recheck the selected release and module format, not merely this permissive minimum. Documented install when authorized: `npm install fast-check --save-dev` (or project package-manager equivalent). Existing project runner executes the test file; no new mandatory runner.
- Upstream skill already covers broad JS testing/property-test/reset/replay practices; inspected its description and initial guidelines. New pack should not copy its layout/runner mandates or turn suggested installs into permission. This stateful skill adds cross-runtime dependent-state generation, legitimate model boundaries and causal sequence shrinking.

### S9: Hypothesis setup and license

- URLs: https://hypothesis.readthedocs.io/en/latest/quickstart.html ; https://hypothesis.readthedocs.io/en/latest/compatibility.html ; https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/LICENSE.txt ; accessed 2026-11-07.
- Documented install: `pip install hypothesis`, only when task scope authorizes dependency changes; use existing project tooling/environment. Existing unittest/pytest integration runs `RuleBasedStateMachine.TestCase`; focused example `pytest path/to/test_world_state.py` is runner selection, not a command executed here. MPL-2.0 except explicitly identified inherited code. Package compatibility comes from selected release/current official compatibility page; guessed setup.py/setup.cfg/pyproject.toml URLs failed and supply no facts.
- Current official compatibility snapshot states CPython/PyPy 3.11+ and tested macOS/Windows/Linux/Emscripten. Function-scoped pytest fixtures run once per whole test, not once per generated input; do not presume they reset each state machine execution. Current thread-safety policy still requires deterministic outcomes/draw sequences. These version-sensitive facts must be rechecked for the selected release.

### S10: Hypothesis stateful API details and resource controls

- URL: https://hypothesis.readthedocs.io/en/latest/reference/api.html ; accessed 2026-11-07; stateful_step_count, initialize, precondition, invariant and run_state_machine_as_test.
- Findings: `@precondition` chooses whether a rule is admissible; `@initialize` methods each run once before rules in arbitrary order and cannot have preconditions; invariants normally run after rules and after all initialization, with `check_during_init=True` available. `stateful_step_count` bounds additional rule calls per example, so increasing examples and steps multiplies work. The factory runner permits explicit settings.
- Decision: encode dependent setup as explicit dependencies, not presumed initializer ordering; put per-sequence reset/cleanup in the actual machine lifecycle. Tune operation count and number of sequences separately within budget; do not silently suppress slow/reset health checks to scale a broken experiment.

## Proposed skill decisions

These are proposed design choices grounded in the sources above, not a standard requiring new framework machinery.

### Represent the contract state, not the implementation

Read the real public producer and enabled configuration. Model only the facts that determine admissibility and expected observations: logical object identity and lifetime, ownership/permissions, membership, transaction/session state, acknowledged results and expected error effects. Keep actual returned handles in a separate map from stable model identities. The model should not replicate target caches, storage layout or implementation branches (S1-S4; S6 pp. 3-9).

An initial world can be generated directly only where that reproduces the relevant supported state. Otherwise generate setup through actual API calls. Preserve setup, workload and outcome as one replay unit. A world constructor that bypasses cache/session/lifecycle transitions may erase the state that matters (S2; S6 pp. 14-15). This does not authorize new layers or a copy of production code.

### Construct useful sequences and make invalid calls deliberate

Build legal-operation choices from current model facts; include boundary states and interactions rather than uniform nonexistent identifiers. Generate creation, successful use, mutation, permission change, deletion and later observation where those operations are real contracts. Avoid putting SUT calls with side effects inside generation/check-only phases: those phases may run under shrinking or without the corresponding actual sequence (S2-S4).

Separate a deliberate invalid-operation rule, with its documented error/effect oracle, from a skipped precondition. A skipped command is not execution of the invalid API. Track generated, admitted/executed, successful semantic operation and oracle-evaluation counts separately; a long list mostly skipped by check() is weak evidence of deep state testing (S4,S5). Do not invent a minimum success percentage.

### Keep dependency-aware reduction and replay

When a prefix changes, recompute live handles, admissibility and expected state. Do not capture mutable generation-time state as the replay contract. Dependency mechanisms such as bundles and command selectors help preserve useful relationships; they do not prove every domain precondition. Shrink initial world/setup and workload together, retaining a source-of-truth original trace and same property violation. Use the failure-reduction owner for general minimizer mechanics (S1-S4; S6 pp. 5-6,14-15).

Log resolved identities and operations, not merely a choice index whose meaning changes with model contents. Preserve actual starting state/setup, choices, executed commands, raw results/effects, selected framework/build/config and framework replay fields. For fast-check that includes command replayPath plus assertion seed/path. For Rapid retain the fail file as well as seed and version (S3,S7). Neither is a promise to reproduce uncontrolled asynchronous history.

### Broaden observations at real boundaries

Compare the promised returned result, error, and relevant externally visible effects after admitted operations. Use independent structural/integrity/world observations when they test a separate documented guarantee. An error-only or return-only model can miss forbidden side effects; conversely the model can be wrong. Adjudicate the actual contract before calling a disagreement a product bug (S1-S4; S6 pp. 6,14-17). Effect/oracle design belongs to correctness-oracles; scheduler/history interpretation belongs to specialist skills.

## Worked advanced applications for the drafter

These are proposed experiments, not observed Barn defects or executed target tests.

1. **Object/permission lifecycle.** Model logical objects, live returned handles and documented permissions. Generate create, successful permitted mutation, permission transition, attempted mutation by another identity, observation and deletion. Construct compatible choices from current state; give deliberate denial attempts an error-plus-state oracle. Shrink away unrelated objects while preserving the permission transition and same forbidden effect. This tests successful dependent state beyond an empty-world program lane, without claiming Barn lacks such tests elsewhere.
2. **API/protocol session sequence.** Derive session states from the actual API. Generate establish/authenticate/use/close/reopen through real public operations, plus selected invalid transitions with specified behavior. Keep authentication state, opaque handles and the external transcript replayable. A generic packet fuzzer is not automatically a session model; a session state machine is not a network-scheduler controller.
3. **Hidden lifecycle state.** If create and reopen have different supported producer paths, represent the setup sequence rather than collapse both into equal visible maps. Explore a mutation followed by independent effect/integrity observation only where the real contract supports it. The paper's historical case motivates checking the difference; it does not prove this difference matters in every application.

## Runtime routes and prerequisites

| Target | Verified initial route | Boundary |
|---|---|---|
| Python | Hypothesis RuleBasedStateMachine, rule/bundle/precondition/invariant APIs, TestCase | Current package compatibility; external target must have real client/setup/replay seams |
| JS/TS | fast-check commands with modelRun/asyncModelRun and framework replay fields | Await async commands; check() skips are not target errors; scheduled path belongs to schedule owner |
| Go | Rapid T.Repeat and StateMachineActions; MakeFuzz adapter where appropriate | Selected module/toolchain compatibility; no automatic schedule control or coverage feedback in ordinary Rapid search |
| C++ | RapidCheck rc::state Command<Model,Sut>, check/apply/run | Current build/test integration still to verify; no new universal wrapper |

No installed dependencies, builds or test runs were performed. Runtime setup is conditional and should reuse an existing fitting library. If a target already has a good sequence generator, improve that owner rather than port it just to use a named tool. The baseline report already establishes Barn's strong fuzz/history capabilities; no fresh complete Barn absence audit was performed here.

## Reference depth and behavioral evaluation

Ship domain-specific references for model/dependency design, stateful shrinking/replay and selected runtime recipes, plus required common-mistakes and source inventory. Entry point should route, not teach a generic list/stack tutorial. Link correctness-oracles, semantic-program-generation, failure-reduction, schedule-exploration and history owners for their independent concerns.

Evaluate with raw API contracts and an advanced existing harness: hidden setup transition, many skipped commands, identity reuse and a model that duplicates an implementation assumption. Observe whether the agent reaches successful dependent behavior, saves a replayable world/sequence and shrinks without changing the violation. A historical or injected defect can supply a blind evaluation; do not reveal the expected diagnosis. No behavioral effectiveness or empirical discovery-yield test was performed in this research.

## Literature artifact status and limits

Hughes paper images 000-017 all read; notes, metadata, description, paraphrased abstract, 12 bibliography entries, index, reader ledger and helper-generated keymap are written in the task-local paper collection. Reader's separate reconcile-skill orchestration was not invoked under the explicit parent/Q reader-only instruction; no other processed papers exist in this task-local collection. Raw PDF/page images stay local, outside distributed plugin and git staging. No extracted paper text read; no claim from unread cited literature.

DOI landing-page fetch was inaccessible; the author PDF/title/image evidence supports the paper's identity. Container metadata was left null rather than assert an unverified book title. Initial Hypothesis packaging path guesses and a fast-check commands-doc guess returned 404, so no recipe relies on those responses. Primary linked documentation/source supplied the supported mechanisms described above. Current main/latest sources are a dated snapshot, not a promised version pin; actual campaigns must preserve selected framework revisions. No discovery-yield claim or behavioral effectiveness evaluation was performed.

## Completion

Research ready for drafting: S1-S10 primary documentation/source entries, full paper-reader page-image evidence, concrete state/model/shrinking/replay guidance and advanced worked scenarios. Only this repository report and isolated paper artifacts were authored. No skill code, target test, dependency installation, git operation or publication occurred.
