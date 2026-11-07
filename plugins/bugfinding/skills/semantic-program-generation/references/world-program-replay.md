# World/program replay and shrinking

## Keep the generator's input and its actual product

Retain original choices and rendered source together with starting-state construction, target configuration and witness. A changed choice can alter later choices and dependencies; revalidate what the producer actually emits. For Csmith-style comparisons, preserve language-defined behavior and matched implementation-defined choices, not merely parse success; Csmith can "perform differential testing within an equivalence class but not across classes" of implementation-defined integer behavior ([Csmith, §§2.2–2.6 and 4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

Use the target's existing representation and creation paths. A directly fabricated visible map is not automatically equivalent to a world established through lifecycle operations; only claim equivalence when the actual target contract/source supports it. SQLite's account of a fuzzer that mutates "both the input database and the input SQL" motivates treating state and SQL together without prescribing a universal world format ([SQLite testing, §4.1.3](https://www.sqlite.org/testing.html)).

## Reduce dependencies with their uses

| Candidate move | Required observation before accepting |
|---|---|
| Remove an object or definition | No retained operation requires it, or uses are validly rewritten through existing identities |
| Simplify a value/type/range | The intended semantic operation still executes within its selected domain |
| Remove a state-changing prefix | Required receiver/lifetime/permission facts still hold through actual setup |
| Simplify branches or loops | Relevant effects and validity facts remain true on the replayed paths |
| Shorten generation choices | Regenerated world/program still exhibits the selected violation |

The table describes proposed moves, not a ready generic reducer. Verify them using the maintained target representation and the selected oracle. Csmith's report notes that C reducers "introduce undefined behavior", so a reduced program can retain a mismatch while losing its meaning; smaller output is insufficient evidence ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Worked dependent-index case

For a documented successful indexed-update contract, construct a nonempty collection and select an index from its real valid range. If an earlier mutation changes its length, derive a new valid index from the resulting state or deliberately switch to a separately specified invalid-index check. A reduced case that removes initialization and fails on an empty collection is not the minimized successful-update violation. Array/range and initialization checks serve distinct purposes in Csmith's safety design, where variables "are forced to be in bounds using the modulo operator" separately from initializer safety ([Csmith, §2.4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Measure reached semantics

Keep observed counts for constructed, parsed/compiled, entered-operation, completed-effect and evaluated-oracle cases when they distinguish bottlenecks. Record setup errors, permitted target errors, resource aborts and incomplete observations separately. These are the plugin's measurement choices; Csmith's study reports size-dependent results and little incremental ordinary coverage despite its discoveries ([Csmith, §§3.3 and 3.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

Report the retained artifact bundle and actual replays, not only a seed. Route minimality/interestingness algorithms to `failure-reduction`, matched engine semantics to `semantic-differential-testing`, and unresolved attribution to `evidence-based-triage`.
