# Matched state and observable effects

Use this when compared operations depend on objects, sessions or prior work. The following design procedure extends paired comparison to a target's actual state contract; it is not a generic engine adapter. SQLancer's replay logs include database setup because the query alone does not identify the case ([SQLancer logs](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)).

## Choose the replay unit

- **Independent operation:** restore the relevant logical state through an existing supported fixture/reset owner, execute one case, observe the promised effects and discard its state.
- **Dependent sequence:** replay setup and the operation prefix through public producers, comparing the relevant states along the sequence. Do not remove a lifecycle transition simply because its final visible fields resemble another setup.
- **Execution-mode comparison:** match the starting state and behavioral guarantee while varying a supported strategy. SQLite uses optimization-on/off comparisons for answer tests, but excludes tests whose purpose is measuring optimization work ([SQLite testing, §9](https://www.sqlite.org/testing.html)).

The independent/sequence choice is this pack's experiment design. Inspect the real runner to establish which one it currently provides. In a batched worker, initially equal fixtures do not establish equal later pre-states after earlier operations; inspect or replay the causal prefix before interpreting a later mismatch ([SQLancer setup and reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)).

## Define logical observations

Derive the observation from the target's public guarantee, not its internal serialization. For an effectful object operation, a proposed observation can include the returned value/error, reachable property values, identity/alias relationships and allowed external output. For recovery, use acknowledged operations and recovered state under a specified failure model; same-answer checking does not replace storage-order/failure testing ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)).

When implementations allocate different physical handles, retain a justified correspondence between logical identities. The mapping must preserve equality, reuse and alias relationships required by the contract. Mapping every handle to the same placeholder would remove that information. This is an observation-design consequence, not a promised general-purpose identity library; use the target's existing supported observations and retain both raw states ([SQLancer observer as a concrete information boundary](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)).

Record observer effects too. If the observation itself changes a session/cache/world, define the comparison boundary accordingly. Unsupported observation or an unavailable state-establishing prefix leaves the comparison unresolved rather than proving an implementation difference. Use `correctness-oracles` to settle the guarantee before building a new query/reset seam ([SQLancer generation and logging](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)).

## Localize before reducing

Keep setup, workload and paired raw observations together. If a sequence diverges, identify the earliest demonstrated unequal observable state where possible; later output differences may depend on it. Shrink the prefix and operation together, re-establishing validity on both sides. Retain the original if a smaller case changes the selected mismatch or loses legal state; invalid reduction is a documented wrong-code hazard ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).
