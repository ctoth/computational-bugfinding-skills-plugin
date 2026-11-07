# Research: semantic-program-generation

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned repository output; no skill drafting, target execution/mutation, installation, commit or publication occurred.

## Evidence ledger

Primary docs Csmith README, FuzzTest domains/quickstart and SQLite testing account read. Csmith PLDI 2011 author PDF retrieved at `C:/Users/Q/code/bugfinding-literature/semantic-program-generation/papers/Yang_2011_FindingCompilerBugs/paper.pdf`, rendered via paper-reader helper to 12 page images; ALL twelve images read directly. No extracted paper text used. Referenced developer researcher role file is absent. Paper-reader notes, metadata, description, paraphrased abstract artifact, 32-entry bibliography, index/ledger and generated keymap exist; nested reconcile/tag/process orchestration is excluded by parent instruction. No claim of completing those excluded workflows is made. No PDF adoption move/deletion was needed: retrieval created the canonical paper.pdf directly and rendering preserved it.

### S1: Complete paper-image findings

Source: Yang, Chen, Eide and Regehr, *Finding and Understanding Bugs in C Compilers* (PLDI 2011), author PDF https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf ; DOI https://doi.org/10.1145/1993498.1993532 . Accessed 2026-11-07.

- pp.2-4: generation interleaves grammar choices with environment, points-to and read/write effect information. A fragment is committed only after analysis and safety checks; failure rolls back local state. Loop backedges can invalidate an earlier locally safe dereference, so closing loops needs global fixpoint checks. **Decision:** grammar validity and type compatibility are insufficient for a semantically informative successful execution.
- p.5: equivalent implementation-defined choices delimit valid differential comparisons; generated programs need not terminate. **Decision:** preserve target configuration/classes and distinguish an allowed nonterminating program from a wrong-result witness; do not impose Csmith's C rules on unrelated language contracts.
- pp.7-8: raw failing tests cannot automatically be mapped to distinct underlying bugs; size and conventional code coverage are incomplete proxies for discovery. **Decision:** measure semantic interactions and successful property reach separately, and tune size by observed target costs rather than assert a universal sweet spot.
- pp.9-10: the paper identifies incorrect optimization analyses, safety guards and transformations; reducing a wrong-code input can introduce undefined behavior. **Decision:** generate feature interactions but re-establish the same valid semantic contract after each shrink; a smaller mismatch is not enough.
- pp.11-12: prior generators make expressiveness/predictability tradeoffs. **Decision:** select generation constraints for the intended target phase rather than maximizing syntactic variety universally. Historical results and parameter settings are not expected yield for another runtime.

### S2: Csmith current README, platform guide and license

- URLs: https://raw.githubusercontent.com/csmith-project/csmith/master/README.md ; https://raw.githubusercontent.com/csmith-project/csmith/master/doc/build-csmith-on-windows.md ; https://raw.githubusercontent.com/csmith-project/csmith/master/COPYING . Accessed 2026-11-07, README About/Install/Use, Windows prerequisites/build, license conditions.
- Quote fragment: “generated programs might contain infinite loops”.
- Documented operation: generator emits C, then selected compilers build/run the same program. README Ubuntu prerequisites are g++, CMake and m4; Windows instructions distinguish Visual Studio/CMake/m4. License is two-clause BSD form. Current docs advise limits for nontermination; a mismatch can also originate in the generator.
- Verified command shape (not executed): `csmith` produces source on stdout; compile the saved source with the selected compiler and the installation's include directory, then execute under owned resource limits. `csmith -h`/`-hh` enumerate the installed version's generation options. Shell redirection examples are documentation, not permission to bypass this workspace's editing-only authored-file rule.
- Relevance: Csmith is a C generator, not a ready MOO/Go generator. Reuse its design reasoning, not its runtime as a universal backend. The Windows page prescribes system-directory changes; do not turn that into automatic installation authority.

### S3: FuzzTest domain combinators

- URL: https://raw.githubusercontent.com/google/fuzztest/main/doc/domains-reference.md ; sections Map/ReversibleMap, FlatMap/ReversibleFlatMap, Filter, Recursive Domains. Accessed 2026-11-07.
- Quote fragment: “parameters that are dependent”.
- Verified mechanics: dependent domains and reversible mappings can preserve relationships; inverse round-trip conditions matter. Map/FlatMap don't support ordinary external initial seeds. Restrictive filters waste search and can abort; the current recursive-domain docs warn that an absent recursion bound can exhaust resources. Check actual input ranges: a dependent index domain still needs nonempty containers and arithmetic without overflow.
- Decision: construct valid semantic relationships and preserve replay representation deliberately; a domain combinator alone is not a proof of lifetime/effect correctness. Use explicit node/depth budgets and measure rejection reasons.

### S4: FuzzTest execution and platform constraints

- URLs: https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md ; https://raw.githubusercontent.com/google/fuzztest/main/doc/fuzz-test-macro.md ; https://raw.githubusercontent.com/google/fuzztest/main/LICENSE . Accessed 2026-11-07.
- Read prerequisite/setup/execution and property-function/seed contracts. Current quickstart uses Linux or experimental macOS, Clang, Bazel and C++17; unit-test and instrumented fuzzing modes differ. `bazel test :TARGET` differs from `bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY` in an already configured project. Not executed here; dependency setup belongs to the chosen runner owner.
- Property invocations share a process; deterministic initialization and avoiding exit remain relevant. Apache-2.0 covers the general source, with separately listed exceptions in LICENSE. Do not transpose these C++ build rules to Go or claim Windows support from Csmith's different platform guide.

### S5: Joint data and program mutation in SQLite

- URL: https://www.sqlite.org/testing.html ; §4.1.3, accessed 2026-11-07.
- Quote fragment: “both the SQL input and the database file”.
- SQLite reports that joint database/SQL mutation reached faults missed by either dimension alone. dbsqlfuzz is proprietary and uses a structure-aware mutator; this is project experience, not a promised public installer or universal yield.
- Decision: a program's meaningful semantics can depend on its starting world. Treat initial data, program and selected semantics as one shrink/replay artifact rather than vary source over an empty state forever.

## Actual Barn baseline read and capability delta

Read existing fetched `origin/master` versions without fetching, checkout or target mutation. This is a source snapshot, not live-remote/CI or campaign evidence.

- `internal/fuzzseed/structured.go:11-22` bounds nodes/depth/length; `:25-56` declares initialized variables and builtin/literal palettes. `:60-80` maps choice bytes into complete IR, adds a value prologue, and formats through production `parser.FormatMOOChecked`. This is already structured generation with bounded choices, not an advance supplied by the plugin.
- The same file's `generator` at `:109-118` holds assigned variable names, loop scope, an input budget and index-boundary context. Expression construction at `:311-365` chooses operands/index bases/property bases/verb receivers/arguments recursively. These inspected excerpts do not maintain a dependent type, object-existence, permission or successful-operation proof. This is a description of this generator's shown fields/choices, not proof of absence elsewhere in Barn.
- `vm/fuzz_test.go:27-49` requires structured inputs to compile. `:36-64` selects core capabilities/private empty store, accepts runtime errors/tick exhaustion and checks literal round trips after return. `:65-75` runs fork children in creation order. A meaningful new lane must generate initial state and semantic dependencies that reach intended successful world effects, not merely claim this existing compile-valid lane as new.

The new skill should first inventory actual producers and semantics; it must not prescribe Csmith, a new analyzer framework or a duplicate runtime for Barn. Existing production IR/formatter and target-owned creation/fixture APIs are the starting owners. Further implementation requires the actual target contracts, not invented MOO permission rules.

## Generation decisions for the drafter

These are plugin design recommendations derived from S1-S5 and the inspected baseline, not externally proven universal rules or empirical yield claims.

### Decide what validity buys

Name the target phase and guarantee. Parser rejection, runtime error handling, optimizer semantic preservation and successful state mutation need different input contracts. Keep deliberate invalid-input/error lanes when they test a real guarantee; add a successful-path lane where errors prevent reaching the intended operation. Do not turn every target exception into a harness failure, nor accept every exception while claiming an unexecuted success property.

For a successful-path lane, carry only the facts the selected contract needs: variable/type/range, live object identity, known property/verb, owner/capability, legal indices and expected effects. Derive them from actual language/API rules. Build creation/initialization dependencies before their use. A variable-name environment prevents one class of invalidity but does not establish the remaining facts. S1 supplies environment/effect checks; S3 supplies dependent domain construction; S5 motivates joint state+program search.

### Generate from a supported representation

Prefer the existing AST/IR and formatter. Generate choices over constructors and semantically constrained operands, not a second parser/printer. For primitive type/range/index constraints, constructive domains can avoid a low-yield post-filter. For state/effect constraints, select or establish a valid dependency using actual target seams. Recompute facts at joins/loops/exception edges when earlier assumptions may no longer hold; use the smallest analysis required by the intended operation rather than port all of Csmith.

Guarantees about the generator need their own evidence: construction, parse/compile success, entered semantic operation, completed effect and evaluated oracle are different counts. A generator assertion that compilation must succeed does not establish successful execution. Observe the actual boundary relevant to the target property. Route sensitivity to harness-sensitivity and oracle reasoning to correctness-oracles.

### Make search diversity semantic

Vary relationships that exercise real implementation interactions: aliasing/identity, nested updates, boundary ranges, permitted type conversions, exception/finalizer effects, inherited lookup or state-dependent dispatch where the target supports them. Do not add unsupported examples as facts about Barn. Preserve a mix of simple and interacting forms; tune size/depth/rejection using observed useful reach and cost, not the 2011 paper's most productive size band. Coverage alone can hide different internal values/path interactions (S1 p.8).

### Shrink the semantic case, not just its spelling

Preserve original choice representation, rendered source, initial-world/fixture construction, target configuration and actual witness. A reduced choice list can change later selections and relationships; regenerate and revalidate the full case. Remove dependent setup and use together, or rewrite references through a valid existing dependency. Retain the same operation/effect violation; a new type error, missing-object error, quota abort or unrelated mismatch is not the minimized original finding. S1 p.10 establishes invalid reduction risk; detailed reducer algorithms belong to failure-reduction.

If one mapping represents many internal choices, preserve enough provenance to replay the generated program after generator evolution. FuzzTest reversible mapping laws and seed limitations (S3) are concrete examples of this representation problem, not a mandate to install FuzzTest for every language.

## Advanced worked scenarios

Illustrative designs, not observed product defects or executed experiments.

### Successful permissioned world mutation

Given a real target guarantee for a permitted operation, construct a small world through its existing supported fixture/API owner. Generate a live receiver, actual property/verb and principal whose required permissions are established. Produce program IR using those identities, run from that world, and observe both return/error and the promised world effect. Then vary aliasing, inherited lookup or exception paths only where their semantics are documented. Record failure of setup separately from evaluation of the protected effect. Shrinking must preserve the necessary object/principal/definition and violated guarantee. This advances beyond syntax-valid source over empty state without requiring a universal world generator.

### Valid index and mutation dependency

Generate a nonempty supported collection and an index from its actual valid range; when an earlier operation mutates its length, derive the next index from the new state or intentionally test a documented invalid-index policy. Do not independently generate a large integer and discard nearly everything. Check empty-container and integer-overflow cases in generator arithmetic itself. For C++ FuzzTest, FlatMap can express dependencies, but the actual domain range and seed law still require inspection (S3). Equivalent constructions can use a target's existing choice/IR representation without a new library.

### Semantic compiler interactions

For a supported compiler target, construct expressions whose alias/effect/range relationships are legal under the selected semantics and target configuration. Compare the intended outputs/effects through semantic-differential-testing. Retain explicit safety preconditions during reduction rather than rely on majority output to establish validity. This uses S1's design reasoning; it does not imply current Csmith covers every language feature or that compiler winners can be chosen by vote.

## Existing ownership and practical boundaries

Installed `golang/go-testing-advanced` was read: ordinary native fuzz entrypoints/corpus, benchmarks and testing examples are already owned there. The new skill owns semantic preconditions and construction, not Go fuzz syntax or Csmith installation. Stateful-property-testing owns API operation-sequence/model mechanics; this skill owns program construction and the environment/effects that give the generated program its intended semantics. Differential, metamorphic, coverage-runner and reduction details remain their specialist owners.

Tool documentation recipes were verified as documented, not executed. No tool was installed or target campaign run. Sources are mutable documentation snapshots accessed 2026-11-07, not a promise of future version compatibility. Licensing/build details are conditional and belong in a tool-specific reference only where the skill actually uses that tool. Failed/inaccessible initial URLs and search snippets supply no paper facts; only the twelve page images support S1 findings.

## Drafter handoff

Suggested substantive references: semantic-environments.md (minimal fact maintenance, constructive dependent values, phase-specific validity), generation-and-shrinking.md (world/program provenance and replay), plus required common-mistakes.md and sources.yaml. Keep the entrypoint concise: choose semantic lane, reuse production owner, generate dependencies, measure intended reach, preserve/revalidate witness. No scripts, generic solver adapter or universal analyzer is justified by this research.

Inventory S1 author PDF/DOI and page ranges, S2 README/platform/license URLs, S3 domains URL, S4 quickstart/property/license URLs, S5 SQLite §4.1.3. Cite actual sources inline; this report is handoff evidence, not technical authority. Use public primary links in distributed skills, never local paper paths.

Blind evaluation: supply an advanced grammar-valid generator and a real raw API contract where a state-dependent operation rarely completes. Ask the agent to improve discovery under a finite budget without revealing the intended diagnosis. Observe whether it establishes actual setup/type/effect dependencies, measures successful property evaluation and shrinks world+program while retaining the same witness. Do not score on matching a chosen library or claim bug yield from a merely written generator. No such behavioral evaluation was run here.

## Completion

Primary-source research and all twelve paper-image reads completed; paper-reader text artifacts, metadata/index/ledger/keymap exist externally as identified above. No process/tag/reconcile orchestration, target execution, authored implementation, commit, install or publication. Report is ready for independent drafter.
