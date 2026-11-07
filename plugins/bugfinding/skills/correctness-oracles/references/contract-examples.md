# Contract-to-observation examples

These are illustrative designs, not executed campaigns or reports of defects. Use the target's actual build and contract before adapting them.

## Expected error, wrong state

Suppose the promise is SQLite statement-level ABORT behavior. Given a unique-key table, this illustrative sequence separates earlier transaction work from the failing statement:

```sql
CREATE TABLE item(id INTEGER PRIMARY KEY);
INSERT INTO item VALUES (2);
BEGIN;
INSERT INTO item VALUES (1);
INSERT OR ABORT INTO item VALUES (3), (2);
-- Capture the constraint error, then query the still-active transaction:
SELECT id FROM item ORDER BY id;
```

Under the documented ABORT contract, the failing statement's changes are undone while "changes caused by prior SQL statements within the same transaction are preserved". The observation therefore needs both the error and state: IDs 1 and 2 remain, 3 does not. The duplicate-key setup exercises a real constraint producer; it does not require a crash to expose a violation ([SQLite ABORT](https://www.sqlite.org/lang_conflict.html)).

Do not reuse that post-state expectation for FAIL. Its contract can retain changes made before the failure within the statement. The policy also depends on the constraint kind: "The FAIL behavior only works for uniqueness, NOT NULL, and CHECK constraints", and a foreign-key violation under FAIL behaves as ABORT. Determine which effects the actual execution performed and the selected policy permits; do not assume an unspecified visitation order. This difference is why a returned error alone cannot decide the effect guarantee ([SQLite FAIL](https://www.sqlite.org/lang_conflict.html)).

The same design question applies to a documented permission-denial API: if denial promises no protected-state change, observe protected state as well as status. Derive that promise from the real API; the SQLite example supplies the boundary distinction, not a permission contract for another product ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

## Healthy structure, unchecked relationship

Suppose the guarantee concerns SQLite foreign-key relationships. Establish support and enforcement on the connection outside an active transaction:

```sql
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;
```

Inspect the returned setting instead of assuming the command changed it. If the query "returns no data instead of a single row containing "0" or "1"", the build does not support foreign keys; record that as an unmet precondition, not a passed check. Setting enforcement during an active transaction "simply has no effect"; applications should "not depend on the default setting" ([foreign-key prerequisites](https://www.sqlite.org/foreignkeys.html#fk_enable), [foreign_keys contract](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

For the relationship observation, consider `PRAGMA foreign_key_check` and retain violating rows; it "returns one row output for each foreign key violation". `integrity_check` "does not find FOREIGN KEY errors"; a healthy `integrity_check` verdict does not answer the relationship question. For a nullable child reference, NULL can be legal: the constraint holds if "one or more of the child key columns are NULL", so a custom invariant must preserve that case ([SQLite PRAGMAs](https://www.sqlite.org/pragma.html#pragma_foreign_key_check), [integrity_check](https://www.sqlite.org/pragma.html#pragma_integrity_check), [foreign-key semantics](https://www.sqlite.org/foreignkeys.html#fk_basics)).

Choose the observation point from the constraint's timing. An immediate foreign key is checked at the end of each statement; a deferred one may be violated inside an open transaction, and "COMMIT will fail as long as foreign key constraints remain in violation". A mid-transaction `foreign_key_check` row for a deferred constraint is therefore legal intermediate state; the promised boundary is the commit outcome and the committed state ([deferred foreign keys](https://www.sqlite.org/foreignkeys.html#fk_deferred)).

For another product, repeat the derivation from its actual configuration and relationship contract. Do not transplant SQLite's setting names, NULL policy or observer behavior.

## More informative histories

If an oracle needs write provenance or ordering, choose observations that expose them. Elle demonstrates unique write values and ordered append objects; blind register writes "destroy history". The generator and recorder must preserve the information the checker requires ([Elle §3](https://arxiv.org/abs/2003.10554v1)).

Hand transaction-specific design to `transactional-history-testing`. The advance is the newly observable guarantee, not simply more samples or relabeling an existing history checker. This paper states "Our approach ignores predicates", so its result cannot decide every predicate-sensitive contract ([Elle §9](https://arxiv.org/abs/2003.10554v1)).
