# Research: distributed-fault-testing

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This report is the only owned repository output. Literature uses paper-reader and direct page images only. No target execution, fault injection, installation, target changes, commits or publication.

## Evidence ledger

Inspecting actual Jepsen client, generator, nemesis, checker and recovery contracts. Tool names and inherited reports are discovery leads, not primary evidence.

## Literature evidence reused through paper-reader images

Kingsbury and Alvaro (2020), *Elle: Inferring Isolation Anomalies from Experimental Observations*, https://arxiv.org/abs/2003.10554. Existing completed collection at `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/`; directly viewed images for printed pp.3,7,8,9,12 on 2026-11-07. Parent domain researcher previously read all fourteen pages and completed its artifacts. No new ingestion, collection mutation, extracted paper-text reading or process/tag/reconcile workflow.

- p.3: unique identities and append order expose otherwise hidden dependencies. A real fault workload should choose observations that can discriminate a forbidden result, not merely cause outages.
- pp.7-8: unknown transaction outcomes and incomplete observations affect what can soundly be inferred. A network timeout must not automatically become known noncommit.
- p.9: dependency cycles can support human-readable contradictions; keep the actual history and witness, not only an LLM explanation or graph screenshot.
- p.12: this paper omits predicate inference and has other model limits. Fault coverage cannot expand an oracle's guarantee by itself. No historical detection/throughput number is generalized here.

## Established primary-source findings

### S1: Jepsen client lifecycle and ambiguous operations

- URLs: https://jepsen-io.github.io/jepsen/jepsen.client.html and https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/client.clj ; accessed2026-11-07. Read Client/Reusable/Validate/Timeout, full visible153-line source.
- Actual source: open!/close! must not change logical test state (lines13-21); setup! owns initialization. Validate requires completion type :ok/:info/:fail and same process/function (79-97). Timeout wrapper returns :info with timeout error (119-122), not known failed operation. Reusable defaults false for a crashed/indeterminate client unless implemented.
- Decision: distinguish connection lifecycle from data setup, preserve operation identity and uncertain effects, and inspect whether reconnecting/retrying changes logical operation count. A valid completion shape is not proof of a correct client mapping. The word :info is an observation category, not a successful commit or a rejected request.

### S2: Actual combined nemesis producer/recovery

- URL: https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/nemesis/combined.clj ; accessed2026-11-07, namespace warning, db-generators, partition-package, packet-package and clock-package.
- The source explicitly calls its API unstable. Packages carry nemesis, generator and final-generator together. Process kill/pause generators depend on the database implementing Process/Pause; final operations start/resume nodes. Partition package pairs faults with stop-partition. Packet setup/teardown clear shaping; clock final generator resets node clocks. These are configured attempts, not observed proof of recovery.
- Decision: select faults the actual target adapter supports and retain heal/recovery evidence. Record actual affected nodes and behavior; a generated :kill does not prove a process died. Do not run generic node-wide cleanup against a shared host.

### S3: Runtime/version and license scope

- URL: https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/project.clj ; accessed2026-11-07, project/dependencies/javac options. Main declares0.3.16-SNAPSHOT, Clojure1.12.6, Java --release21, Elle0.2.8 and separate io.jepsen/generator dependency. Published Codox pages identify0.3.11. Pick one actual compatible version/source set; do not present main APIs as that released documentation.
- Project declares Eclipse Public License with EPL1.0 URL; actual license text still to inspect before final claim. No install/build/target command has run.

### S4: Current generator, synchronization and time limits

- URLs: https://raw.githubusercontent.com/jepsen-io/generator/main/README.md and https://raw.githubusercontent.com/jepsen-io/generator/main/src/jepsen/generator.clj ; accessed2026-11-07. Read generator protocol/context introduction, TimeLimit1443-1467, Stagger1468-1521, Synchronize1587-1603, phases1604-1615 and until-ok1667-1671. This is now a separate library; the old Jepsen monorepo generator.clj URL returns404 and published old generator docs identify0.3.8.
- Actual behavior: op/update compose stateful choices; phases synchronizes workers between phases. time-limit stops emitting operations after its lazy cutoff, rather than interrupting arbitrary in-flight calls. until-ok needs an actual successful completion and can continue while operations fail. Current stagger is exponential with a mean global interval. The README's recovery example heals, waits, then performs final reads.
- Decision: bound workload emission, calls, recovery observation and total resources separately. A sleep is a pacing choice, not evidence of convergence. Retain actual completion/health evidence before final correctness observations. Separate generator README declares EPL2.0 with stated secondary-license conditions; this is distinct from core project metadata.

### S5: Checker result and actual run/analysis lifecycle

- URLs: https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/checker.clj (34-108) and https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/core.clj (with-db164-173, client/nemesis teardown174-220, run-case221-227, analyze228-241, log-results242-254, run contract329 onward); accessed2026-11-07.
- checker/check-safe converts checker exceptions to :unknown with error details. compose gives false higher priority than unknown, then true. Inspect sub-results too. Actual runner writes results and wraps lifecycle cleanup; those attempts can fail and do not establish the cluster healed. Core log collection may kill the DB before copying logs unless leave-db-running is enabled.
- Decision: retain history, subchecker results/errors, fault log, target logs and observed recovery. Capture required live/recovered-state observations before cleanup destroys them. Performance/availability plots and process termination are not substitutes for the promised consistency/data oracle. No checker was invoked here.

### S6: Actual CLI and scoped existing-test recipe

- URL: https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/cli.clj ; accessed2026-11-07; options126-155, usage169-179, single-test-cmd383-465, test-all result handling466-522.
- --seed explicitly does not guarantee general determinism: timing/responses still matter. --time-limit excludes setup/teardown. single-test runner maps false to exit1 and unknown to exit2; outer run handles argument/internal errors separately. Analyze reconstructs the test map from retained original arguments and stored test before rechecking history; it is analysis replay, not system-execution replay. The suite assigns a new seed per test.
- Conditional existing integration shape: `lein run test --nodes-file OWNED_NODES --time-limit 60 --test-count 1 --seed 12345` plus the chosen target's verified workload/fault options. These illustrative values are not defaults or a ready generic test. Read the actual target runner help/source; a library alone does not supply its DB client/model. No command executed.

### S7: Current real producer in Jepsen's etcd test

- URLs: https://raw.githubusercontent.com/jepsen-io/etcd/master/src/jepsen/etcd.clj and https://raw.githubusercontent.com/jepsen-io/etcd/master/README.md ; accessed2026-11-07. Read workload/nemesis tables34-85, etcd-test87-165 and options166-205.
- Actual producer builds workload and nemesis packages, combines them, then in ordinary mode phases timed load, healing, recovery wait and final workload observations. Main source warns its etcdctl client is experimental and can leak operations into the next run; selected jetcd client is default. This is target-version-specific, not generic client guidance. --serializable intentionally changes read semantics; enabling it then asserting linearizable reads manufactures the wrong premise.
- The README's conditional fitting-target example is `lein run test --workload register --nemesis partition --time-limit 60 --concurrency 2n`, with owned node options from actual CLI. Verify selected target version/help/config before executing; no run or new dependency. Its --lazyfs route changes crash semantics by discarding un-fsynced writes, rather than ordinary kill alone representing power loss. Target test is EPL2.0 with stated secondary-license conditions. Full fault catalog is not this skill's scope.

### S8: Primary fault-injector incident and actual control helper

- URLs: https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/CHANGELOG.md (0.3.15) and https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/src/jepsen/control/util.clj (grepkill!356-379, stop-daemon!436-468); accessed2026-11-07.
- Changelog records that grepkill!-based kill/pause/resume faults did nothing starting in0.3.12 because the timeout body was empty;0.3.15 fixes it. Current source has the signal execution inside the body. This is historical documented framework behavior, not a newly reproduced defect or a claim current injection still fails.
- Decision: verify actual process state, connectivity/packet behavior or clock offset for selected fault; a nemesis request/log label is insufficient. The same changelog records an Elle0.2.8 rw-register inference fix from Bifurcan bugs, reinforcing checker version provenance. Current helper uses pattern/name-based process selection; do not copy it as shared-host cleanup. Use the test's actually owned disposable nodes/resources and supported adapter, with ownership checked before actions.

### S9: Setup and environmental applicability

- Source: https://raw.githubusercontent.com/jepsen-io/jepsen/main/README.md ; accessed2026-11-07, Design Overview, Setting up Environment, Control Nodes and Working With REPL.
- Current README requires a control JVM21+, Leiningen, JNA, Gnuplot and Graphviz; most adapters expect Linux/Debian, SSH and privileged network/process operations on DB nodes. Containers share clocks, so ordinary containers do not supply independent node-clock behavior; VMs are a documented alternative. Docker support is community-maintained, marked unsupported here. Actual adapter/environment requirements govern, not the framework name.
- Results live under store/test-name/date. A stored test omits executable checker/client objects, so retain compatible source, dependencies and CLI arguments too. Existing REPL `store/test PATH` loads retained evidence; it does not recreate cluster execution. Core declares EPL with EPL1.0 URL; root and package LICENSE guesses failed, so full core license text was not verified here. Do not substitute generator/etcd EPL2.0 licenses for core metadata. No installation, cloud spend or environment changes occurred.

## Decisions that create new useful fault search

The following is plugin design inferred from S1-S9 and the paper, not a new framework, fixed schema, mandatory test suite or promised bug rate.

### Start with the claim and real client, then choose faults

Read the actual public operation path, enabled durability/consistency policy and acknowledgment boundary. Identify externally observable results and effects the checker can refute. A crash-free process, available port or eventual healthy healthcheck is not the same claim as no lost acknowledged writes. Ordinary availability degradation during a partition may be permitted. Conversely, recovery may reveal a forbidden lost write after the fault is gone. Pick a history/effect oracle for the promised model; transaction dependency and linearizability details belong to their specialist owners.

Inspect client translation of retries, rejected operations, transport failures and response timeouts. Each attempt can have its own possible effect; a retry is not automatically the same logical operation unless the actual idempotency contract establishes that. Preserve request/attempt identity and available response evidence without inventing successful or aborted outcomes. Ensure reconnect/open/close does not reset the data the workload is testing. A well-shaped completion record still needs a correct semantic mapping (S1; Elle pp.3,7-9).

Use a meaningful healthy control plus a representative known/justified violation through the same recorder/checker. Barn already has sophisticated healthy/faulty history controls; this skill must not sell their reimplementation as new capability. A potential advance is exercising actual external process/network/clock failure boundaries and post-recovery observations not represented by an in-memory held interleaving. This is a candidate to establish from source, not proof Barn lacks it across all branches.

### Make the fault model observable

Describe which communication links/directions, nodes, roles, processes and clocks are affected, and which requests can still complete. Model a minority, majority, asymmetric/bridge or overlap topology only where it tests the contract. Random node names do not prove a quorum boundary was crossed. A process pause differs from crash/restart, client disconnection from replication partition, and process kill from loss of unflushed storage. The selected target and fault adapter define what is actually induced (S2,S7,S9).

Record requested and observed fault activation separately. For each selected fault, use existing observable process state, connectivity/shaping evidence or measured clock offsets where appropriate. Reconcile mismatches before allocating a long campaign. The historical grepkill no-op is a real reason for this distinction (S8). Don't add a universal injector protocol or independent service when current target-owned adapters suffice.

Budget timing and phase interactions: fault while an operation is in flight, after acknowledgment, during leadership/membership transition or before recovery observation only when real supported producer boundaries make those meaningful. Combine a small justified set before varying many factors; otherwise overlapping faults can obscure whether the intended guarantee was tested. A seed may reproduce generator choices but cannot recreate a real cluster's scheduling, response timing or background recovery (S4,S6). Preserve the actual history/fault sequence and observations.

### Heal, observe recovery, then clean owned resources

Keep a target-supported final repair phase and a final observation phase. Start/resume nodes, heal selected links and reset clocks through the existing adapter, then verify actual repair/recovery rather than assume a generator emitted success. Where convergence is required before a final read, use the target's meaningful readiness or convergence evidence and an explicit finite resource budget. An arbitrary sleep may be useful pacing but cannot establish the guarantee. Record recovery failure/incomplete observations separately from a healthy property evaluation (S2,S4,S7).

Reserve time/resources for final reads, evidence capture and cleanup; the load-duration flag does not cover every cost (S6). Recovery-only bugs can disappear if the DB is torn down immediately. Capture required state/logs before destructive teardown; understand that Jepsen log gathering itself may kill processes (S5). Never clean unrelated workloads with global process-name kills or host-wide network resets. The test must operate on the authorized disposable deployment and its known owned nodes/processes/paths. This ownership requirement follows real helper behavior, not a reason to impose a new platform or approval system.

### Retain a witness and spend compute on missing dimensions

Preserve exact target/client/checker/library source/build/config, selected topology and initial data, effective acknowledgment/consistency settings, generated/actual operations, attempt outcomes, fault request/activation/heal records, client/server logs, history/checker/subchecker results and witnesses, resource use, final observations and unrecovered state. A shell exit or performance graph alone cannot replace these artifacts. Reanalysis of retained history can validate checker/model changes without rerunning a cluster, but cannot prove the original environment is reproducible (S5,S6,S9).

Use repeated bounded runs to explore actual missing timing/state/topology combinations, tracking successful operations, informative observations, injected fault coverage, unknown outcomes and checked histories separately. Do not treat total outages or zero successful operations as evidence the intended consistency property was exercised. High request rates can just produce timeouts, queue buildup and checker complexity; tune against observed useful semantic work and total discovery/reduction/triage cost. General allocation belongs to bugfinding-campaign.

Reduce a real candidate's workload and fault sequence while preserving acknowledgment, actual failure boundary, legal history semantics and same witness. A shorter outage that merely times out the client is not the original lost-write counterexample. Preserve original evidence when execution replay is nondeterministic or reduction switches the fault. Failure-reduction and evidence-based-triage own detailed mechanics and attribution. No target bug was found or replayed in this research.

## Advanced worked scenarios

These are illustrative designs for an authorized disposable target, not executed campaigns or claims of current product defects.

1. **Acknowledgment followed by failover.** Establish a target's durable/consistent acknowledgment guarantee, write uniquely identifiable values, induce a supported leader/network fault after known acknowledgments, heal, then observe values with the promised read mode. Separate acknowledged writes, timed-out writes, expected rejections and unsuccessful reads. A loss witness must match the actual guarantee; a stale-read mode may legitimately return older data. Source basis: S1,S2,S7; Elle pp.3,7-9.
2. **Pause outlives a lease.** An operation reads state while its owner holds a lease, then the process pauses while another owner acquires a valid lease. Resume and observe protected effects. The question is whether the actual target contract requires fencing/ownership checks, not whether a lock was acquired once. Keep the sequence, lease policy, operations and effect witness; a printed returned value alone may miss the protected-state change. The existing etcd lock-set example shows this is a real workload class (S7), not a universal lock claim.
3. **Fault request is a no-op.** Nemesis emits kill, but process state stays unchanged. History may remain valid because the intended failure never occurred. Investigate adapter/version/targeting using activation evidence, retaining the run as narrower healthy evidence rather than report successful crash coverage. The actual historical Jepsen incident S8 grounds the control.
4. **Final data loss is invisible during an outage.** Under load, reads continually fail; the time-limited generator ends. Heal and issue final observations using the target-supported state boundary before teardown. If final observation is still unavailable, report unresolved/recovery evidence, not a passing no-anomaly history. The current etcd producer explicitly has a final workload generator (S7); no fixed recovery sleep is established as sufficient for every deployment.

## Boundaries, references and behavioral evaluation

Distributed fault testing owns real deployment failure composition and execution/observation phases. Stateful generation, controlled schedules, linearizability, transactional inference, deterministic simulation and crash consistency remain independent owners. A real Jepsen run is nondeterministic system testing, not exhaustive schedule exploration or deterministic simulation. A SIGKILL campaign does not automatically implement a power-loss filesystem model. Keep specialist algorithms linked rather than copied.

The approved domain report is the source-inspected Barn baseline; this researcher did not freshly audit Barn or assert absence across worktrees. Rich in-memory histories/fault controls remain baseline. The useful advance must establish a real previously untested external failure/recovery boundary with an informative applicable oracle, observed fault activation and reviewable counterexample. No new generic client, wrapper, simulator, fault service or storage system is justified by this research. No exhaustive external-marketplace novelty claim.

Directly read installed protocols/campaign and golang/go-race-and-memory-model skill entrypoints. The former already owns general optimization portfolio/budget selection; the latter owns executed shared-memory race/memory-model guidance. Neither inspected entrypoint supplies the real-cluster client/fault/heal/observation integration above. Keep general budget policy and language race fixes in their owners rather than duplicate them. This bounded overlap check is not a comprehensive ecosystem audit or a model-competence experiment.

Suggested references: fault-model-and-activation.md (topology, actual versus requested fault, historical control), jepsen-operation.md (conditional supported setup/client/generator/checker/CLI), recovery-and-evidence.md (final observations, ownership, replay/reduction), required common-mistakes.md and sources.yaml. Source inventory must use actual primary URLs above, accessed date and section/page scopes. Preserve the separate core/generator/adapter version and license declarations rather than collapse them. Public references must not require this machine's paper collection.

Blind behavior evaluation can provide an actual API contract, current client/fault adapter, raw healthy/partition/recovery histories, ambiguous responses, an intended no-op kill and a final-read gap. Ask the evaluator to establish a useful new failure lane or investigate the counterexample without giving expected diagnoses. Evaluate actual fault activation/recovery evidence, retained operation uncertainty and checker witness, rather than outage duration, a tool logo or exact label matching. No such execution or empirical effectiveness test ran here.

## Verification limits and completion

All documented commands are source-read conditional examples, not executed tests. No remote cluster, process/network/clock fault, target/client/checker run, tool install, target mutation, git operation, host registration or publication occurred. Existing Elle page images were reused directly and artifacts left intact; no new ingestion/process/tag/reconcile and no extracted paper text reading. No additional paper was needed for the selected observation/history decisions; specific failure-model literature belongs to deeper target work when its contract requires it.

Failed guessed main generator.clj path was resolved through actual project dependency and official generator repository. Root/package LICENSE guesses returned404, and an attempted GitHub directory listing through PowerShell returned a shape without the selected name property; no technical claim or broad recovery was based on that response. Core license is recorded only as project metadata declaration, full text unverified. Current main/latest source and published API docs differ; pin/verify actual chosen package and retain its config for execution. The developer researcher role file is absent at the supplied path; explicit task instructions governed this bounded work.

Report ready for independent drafting. Only this repository report was authored; no empirical bug-yield or correctness assurance claim.
