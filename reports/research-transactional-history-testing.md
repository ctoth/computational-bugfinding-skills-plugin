# Research: transactional-history-testing

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This is the only owned repository output. Literature uses paper-reader and page images only; no target execution, mutation, installation, commits or publication.

## Evidence ledger

Actual Elle history/analysis contracts, standalone CLI source, selected reused paper-reader page images and Barn baseline were inspected. Proposed capability advances below are designs, not executed product-defect or yield claims.

## Reused literature images

Kingsbury and Alvaro (2020), *Elle: Inferring Isolation Anomalies from Experimental Observations*, https://arxiv.org/abs/2003.10554. Existing completed reader artifacts at `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/`. Directly reread printed pp.3,6,7,8,9,12 as local images on 2026-11-07; no extracted text or new ingestion/collection writes.

- p.3: unique write values recover provenance; append traces expose version order that overwriting registers hide. Choose observable data representations rather than merely increase transaction count.
- pp.6-8: unknown outcomes and compatible interpretations constrain inference. Sound detected anomalies and complete detection differ; a clean finite history cannot prove the entire isolation model.
- pp.8-9: process/realtime/version dependencies add distinct constraints, and witnesses explain cycles. Do not label a session or real-time violation as ordinary serializability without selecting the actual promised model.
- p.12: the paper excludes predicates. Point-object histories cannot by themselves establish range/predicate isolation; a separate justified observer/model is needed.

## Early primary findings

- Actual `elle.rw-register` source assumes initial nil and unique values. Its `check` docstring warns that per-key strengthening options may misreport cycles. A direct-library `:transaction-order` map accepts externally justified order by completion index; no corresponding flag is exposed in the inspected CLI. Preserve provenance and verify the selected checker version; don't enable assumptions to manufacture stronger evidence. Its `ext-index` indexes only successful operations and notes an info-write omission. These are source-scoped inference limits, not executed defect findings. Source: https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj (ext-index, initial-state-version-graphs, transaction-order-graphs, check).
- Actual `elle.list-append` source validates read/append micro-operation shape and unique invocation values; malformed or duplicate generator provenance can yield unknown. Keep these experiment defects distinct from anomalies inferred from valid observations. Source: https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj (verify-mop-types, verify-unique-appends).
- Source-read Barn `origin/master:engine/elle_recorder_test.go` already covers committed suspend/exception slices, discarded retries, irreversible publication splitting, terminal commit failure and uncertain later attempts. `scripts/check_elle.py` already has twenty negative controls and requires explicit true/false/unknown plus witness evidence. None is a new capability introduced by this plugin.

## Primary source inventory and operational handoff

All sources accessed 2026-11-07. Mutable main/master sources are dated evidence, not the identity of a future execution. No command below was executed against a target or checker.

### S1: Elle documented integration and scope

https://github.com/jepsen-io/elle (Usage, Types of Tests, Completeness). Small quote fragment: “checking reported anomalies by hand”. Documented entrypoints are list-append/check and rw-register/check. A JVM caller can invoke them directly; other languages can send histories through an existing file/stream wrapper. The implementation requests manual witness inspection and acknowledges incomplete inference. This is an oracle/analysis integration, not a workload scheduler or a promise of exhaustive anomaly detection. Prefer existing maintained integration; no universal bridge is required.

### S2: Jepsen history semantics

https://github.com/jepsen-io/history (Operation Structure, Operation Semantics). Small quote fragment: “must have no logical effect”. `:invoke` starts an operation; `:ok` confirms completion, `:fail` means definite no-effect failure, and `:info` preserves indeterminate outcome. A logical client process is single-threaded; an info-ending crashed process cannot simply resume as the same process. Times are nanoseconds since test start; indices identify events. Keep raw attempts and the source of each outcome classification. A transport timeout is not automatically `:fail`, and a language exception can follow a committed transaction boundary. Extra diagnostic fields can preserve client/attempt/build provenance without inventing a new history service.

### S3: Actual list-append producer/validation

https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj ; verify-mop-types:38-57, verify-unique-appends:58-78, preprocessing caller:548-561, check:858-924, gen:931-944. Shapes are `[:append key unique-value]` and `[:r key observed-list]`. Actual preprocessing invokes validation tasks; reused invocation values or unsupported micro-operations are experiment errors, distinct from observed duplicate elements. Failed operations remain relevant to aborted-read detection. Check options select promised models, additional graphs, per-SCC search limits and optional output. Preserve complete micro-operation order and all outcome observations; never flatten a transaction into independently committed writes to fit the checker.

### S4: Actual rw-register limits and order evidence

Source URL and bounded findings are recorded under Early primary findings above; actual inspected regions: namespace:1-32, ext-index:151-168, initial-state-version-graphs:169-193, transaction-order-graphs:194-236, graph:822-848 and check:850-923. Small quote fragment: “following three options may not work correctly”. Normal primitive shapes are `[:w key unique-value]` and `[:r key value]`. A non-nil initialized target needs an explicit faithful initialization/history mapping; suppressing that setup can create incorrect inferred orders. Blind-write histories lose version evidence. Where a real API exposes justified version/commit order, direct-library order evidence can improve inference, but arbitrary client timestamps or an assumed serial order cannot substitute. Do not promise a white-box feature through a CLI that does not pass it.

### S5: Result, model and search semantics from code

https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj ; unknown-anomaly-types/additional-graphs:608-651, SCC search:793-837, cycles!:902-935, result-map:937-961. Empty graphs and cycle-search timeouts are explicit inconclusive analysis classes. Timeouts retain already-found cycles and a fallback cycle; a known prohibited anomaly still yields false, while an unresolved search without one yields unknown. Per-SCC cycle-search timeout is not a whole-process/plot budget. Analysis files are written for selected anomalies; retain structured output and raw history even if visualization is absent. Model selection adds process/realtime graph dependencies where required; it is not just a display label.

https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/consistency_model.clj ; Choices:31-36, aliases:183-204, prohibited anomalies:372 onward, boundary:546-557. The source uses conflict serializability for its serializable label. Anomaly implication/model boundaries are version-specific. Don't copy every advertised model name into an assurance claim or infer a broader formal contract from one alias.

### S6: Exact standalone CLI route

https://github.com/ligurio/elle-cli (Requirements, Usage); https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj (readers:24-69, options:91-139, dispatch/main:181-252). Inspected source supports EDN maps/collections and JSON input, converts operation tags, dispatches both Elle frontends, and prints per-file true/false/unknown. Exit0 only says no false result was collected; unknown-only output also exits0. Missing model/help can exit0 without checking a history. Exceptions exit255; parse errors exit1. Require the requested file's explicit verdict, not an exit code or stray true word. Validate conversion against actual operations/types and preserve original input; a successful JSON parse is not a faithful transaction recorder.

Conditional source-read invocation for an existing compatible build:

```text
java -jar ELLE_CLI_JAR --model list-append --consistency-models serializable --cycle-search-timeout 1000 --directory EVIDENCE HISTORY.edn
```

Choose the actual promised model and limits; 1000ms is an illustrative per-SCC setting, not a universal recommendation. Current source exposes `--output json` for analysis output; text mode makes file/result association explicit. Do not invent transaction-order or arbitrary graph flags. Use selected build `--help`/`--version` and dependency manifest to establish actual support before a campaign.

### S7: Runtime, build and license identity

https://raw.githubusercontent.com/ligurio/elle-cli/master/project.clj declares CLI0.1.11 with Elle0.2.7 and Jepsen0.3.11. Its README requires Java21+ due to bundled class references. Existing source build uses Leiningen `lein deps` and `lein uberjar`; optional graph output requires fitting Graphviz support. The project config includes `-Xmx32g`; treat that as selected packaging configuration, not a required allocation for every history. Read selected artifact's manifest/runtime options rather than assume a requested heap from another build.

https://raw.githubusercontent.com/jepsen-io/elle/main/project.clj currently declares0.2.9-SNAPSHOT, Clojure1.12.6, Java release21 and license expression EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0. CLI project/license text supplies the same expression and actual EPL text: https://raw.githubusercontent.com/ligurio/elle-cli/master/LICENSE . This is a scoped source observation, not legal interpretation. Latest-library source and bundled CLI dependencies are different versions; recheck features against what the built artifact actually contains. No installation, build or runtime was executed.

### S8: Consistency contract selection

https://jepsen.io/consistency/models/serializable and https://jepsen.io/consistency/models/strong-serializable (Informal/Formal). Serializability alone does not require real-time or session order; strong/strict serializability adds real-time constraints. Read the target's actual promised API mode and recorder ordering before choosing one. Do not force a real-time edge from uncalibrated cross-host clocks or treat isolated per-key histories as a multi-object guarantee. These pages are primary author documentation; unread linked formal papers supply no claims here.

## Actual Barn baseline and meaningful capability delta

Read already-fetched `origin/master` source only, without fetch/checkout/execution or mutation. This is a bounded source inventory, not current remote/CI state or an absence proof over all worktrees.

- `engine/elle_workload_test.go:25-36` defines property, relationship, definition, code, name, inherited, waif and map rows. `:306-341` records seed/round/settings; `:650-736` generates unique tokens, multiple transaction slices/operations, blind/repeated/intermediate register patterns, suspend/exception/fork behavior, and concurrent permission/object/definition/invariant operations.
- `engine/elle_recorder_test.go:18-57,59-79,81-120,122-147` explicitly checks committed slices, retry discard, irreversible boundaries, terminal failure and later uncertain attempts. Recording at real publication boundaries is already established work.
- `scripts/check_elle.py:11-18,22-30,58-103` uses twenty controls, matched cases, explicit requested-file verdict and anomaly witnesses. `.github/workflows/elle.yml:92-104` builds a pinned CLI/checker under Java21; the runtime's actual dependency differs from latest library source.

The skill must not sell those controls, richer ordinary transactions, or invoke/complete retention as newly introduced. Concrete candidate advances are: an independently supported session/realtime guarantee omitted by a serializable-only analysis; provenance/version observations exposing dependency information that blind overwritten values hide; or a distinct range/predicate observation with an actually supported frontend/custom analyzer. Each needs target-source/model/recorder evidence first. These are investigations, not findings that Barn has a defect or lacks every such test.

The 2020 paper excludes predicates; current core can represent predicate-related anomaly labels, so do not extrapolate that historical exclusion into a claim that all present Elle extensions are impossible. The inspected append/register micro-operation schemas do not themselves record range membership/predicate observations. A range guarantee needs a verified fitting extension or separate oracle, not renaming a range scan as a point read.

## Decisions that change useful history testing

The following is plugin design grounded in S1-S8 and image evidence, not a new mandatory framework/schema or a proven optimal workload.

### Design observations alongside transactions

Identify the actual public producer, promised model, enabled options, initial state and atomic publication boundary. Choose supported data and observations that reveal provenance and order. Unique operation identities are necessary where the selected frontend assumes them; retain actual repeated/intermediate operations where they test an explicit guarantee. A final snapshot adds observation but may still leave overwritten states unobserved. Do not serialize every worker merely to make attribution easy and then claim concurrent coverage.

Generate interactions that exercise the promised coupling: multiple objects, read/write skew, deliberate contention, blind writes, intermediate values, mutation of definitions/permissions or lifecycle only where actual semantics require them. Track admitted/committed transaction and micro-operation shapes, observed dependencies, failed/uncertain operations, recorder exclusions and checker outcomes separately. High transaction count with few informative reads is a search-quality issue, not evidence of isolation assurance. Stateful generation and controlled schedules remain their specialist owners.

### Preserve logical requests, attempts and real commits

A client request can retry internally, publish more than once, suspend between committed slices, or throw after a committed effect. Map those actual boundaries from production source; don't infer them from function names or final API status. Keep attempt identity and request provenance in raw evidence. The canonical checker history should represent the promised logical transactions without phantom aborted writes, duplicated successful attempts or erased uncertain effects. Reusing a token for repeated attempts can violate unique-write assumptions; changing tokens can falsely represent multiple logical writes unless the recorder distinguishes intent and publication correctly.

Classify no-effect abort only when evidence/contract establishes it. Transport loss, deadline, node failure and cancellation may leave application uncertain. Preserve possible effects and actual observation loss. Reconciliation is a target-specific evidence task, not permission to force every unknown into success or fail. Barn already has good recorder tests for several of these boundaries; extend the existing owner when a concrete new boundary is shown.

### Match inference to justified information

Select models explicitly and inspect actual backend aliases/inference. Additional session/realtime/version edges can refute guarantees omitted by ordinary dependency cycles, but must follow from real recorder order or supported version metadata. An assumed property cannot be used as evidence that the same property holds. For current register options with documented warnings, investigate selected-version source/tests or choose a better-supported observation, not blanket-enable stronger inference to raise detection counts.

Do not add synthetic edges solely because two clients' wall clocks suggest a convenient order. Preserve the source of every non-data dependency. A white-box order can complement black-box observation only when its actual contract establishes the relevant ordering; a sampled local sequence number may mean something weaker. Keep original raw observations so the inference can be reexamined independently.

For predicates, derive what was queried and which concurrent versions satisfy it; point-object traces can miss absent-row/range dependencies. Verify an existing implementation that actually consumes those observations. If no supported checker exists, record this dimension as untested or design the smallest justified target-owned observation within a separately scoped task; don't invent a universal graph adapter.

### Preserve explicit outcomes and search cost

Require actual parsing/admission and analysis of the requested nonempty history. Missing input, checker exception, unsupported micro-operations, reused provenance, empty graph and exhausted search are not accepted isolation evidence. A timeout can coexist with a discovered prohibited witness; inspect full structured results rather than replacing every timeout with one generic verdict. Preserve selected model, anomalies, inferred edge explanations and version-specific assumptions.

Measure workload execution, conversion, graph construction, SCC/cycle search and rendering separately where costs matter. Per-SCC time and plot-size settings bound distinct work; neither limits the entire campaign. Use the authorized outer compute envelope and owned resources, with no arbitrary universal transaction length/key count or new runner service. More histories, more overlap, more read provenance or a stronger justified observer are different ways to spend compute.

### Retain and reduce a reviewable counterexample

Keep exact original workload/setup, raw client/attempt/publication events, converted history, checker/build/configuration, observer/adapter rules, selected model/options, raw logs, graph/witness and actual replay attempts. Explain the contradiction from transaction micro-operations and dependency edges. An inferred cycle is not a proved root cause or a generic claim of lost durable data.

Reduction must retain relevant initial state, unique write identity, read values, real boundaries, uncertainty and the same supported anomaly. Removing a transaction that explains provenance, collapsing two slices or completing an unknown arbitrarily can switch the experiment. Use the current recorder/controller and reducer seams; generic reduction and LLM attribution remain the corresponding skills' owners. Keep originals and unresolved cases when reduction loses evidence.

## Advanced worked scenarios

Illustrative designs only; no target or checker was run and no product defect is established.

1. **Session observation beyond serializability.** An API explicitly promises session order across successful transactions. A serializable-only checker can accept an ordering that violates that added promise. Preserve a true single-session operation order and analyze using an appropriate supported session model, with a healthy control and a known justified violating history. Without that API promise, the same observation is not automatically a defect.
2. **Blind overwrites hide dependency order.** Two transactions overwrite a register and later reads reveal only the last value. Longer workload generation may leave the overwritten relation unknowable. A supported traceable append representation or trustworthy exposed version observation can add evidence, provided it still exercises the actual producer/contract. Don't replace the production algorithm with an idealized append-only mock to make a check easy.
3. **Range read misses a concurrent insertion.** A transaction reads all objects satisfying a predicate while another inserts a matching object. Encoding only returned point keys omits the absence/membership dependency. Use a verified predicate-aware observer/checker or retain the unsupported guarantee explicitly; a healthy point-item graph cannot decide it. This is a target-specific research path, not a ready generic Elle CLI flag.
4. **Timeout after commit followed by retry.** A write may publish before response loss. Marking it fail erases possible effects; recording every retried attempt as a new successful logical operation can manufacture duplicate writes. Preserve attempt/request identity and actual commit evidence, represent uncertainty faithfully, and test the recorder with the real boundary. Barn already handles multiple related cases; a new capability must demonstrate an additional actual boundary or guarantee.

## Existing ownership, handoff and evaluation

Read installed Go advanced testing guidance: it owns native fuzzing/seed/corpus basics; this skill owns informative transactional observations, actual commit/attempt boundaries and isolation-model interpretation. The domain research already compares other installed owners. No complete external marketplace novelty search was performed; no uniqueness claim.

Suggested substantive references: history-and-boundaries.md (outcome/attempt mapping), observable-dependencies.md (data/session/realtime/version/predicate scope and worked cases), elle-operation.md (conditional Java/CLI/direct-library setup, result/witness/cost interpretation), plus required common-mistakes.md and sources.yaml. Inventory actual public URLs and source sections above, plus Elle paper/page ranges. Do not depend on local machine paths or this user's paper collection in distributed instructions. Keep entrypoint a practical method selector and runner; no new history database, schema, plugin-wide recorder or copied checker implementation.

Blind evaluation can supply a real API contract, raw retry/publication events, a serializable-but-session-invalid history, unknown-only CLI output, and a range query recorded as point reads. Ask the evaluator to derive a faithful history/checker call and supported conclusion without expected diagnoses. Observe preserved provenance, actual supported model, explicit outcomes and witness; the written plan alone is not discovery-yield evidence. Existing controls and small finite histories should exercise the current owner; no recurring approval gate or mandatory mutation platform.

## Verification limits and completion

Primary docs/source and selected reused Elle images were actually read as identified above. No new paper ingestion or collection change; completed artifacts reused via paper-reader. No paper-process/tag/reconcile, extracted paper-text reading, target/checker execution, dependency installation, source changes outside this report, git mutation, host registration or publication.

The guessed history doc path returned404; actual repository README supplied the format contract. Latest master/main source and Barn's pinned artifact are different identities, explicitly recorded. No strong performance/yield claim, full-system absence proof or inferred product defect is made. The referenced developer researcher role file was absent at its supplied path; explicit task constraints governed.
