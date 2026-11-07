# Common oracle mistakes

## Counting a skip as successful comparison

**Wrong:** Increment the equality count whenever neither query produces a reported mismatch.

**Better:** Inspect the check's skip/error paths. NoREC's sentinel handling does not evaluate equality: when either count is `-1` it throws `IgnoreMeException`; preserve that outcome separately ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

## Accepting every expected error without observing effects

**Wrong:** Return success immediately on a documented constraint error.

**Better:** Check the permitted post-state too. ABORT and FAIL have different effect boundaries, and under ABORT "the transaction remains active"; do not assert total transaction rollback for both ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

## Trusting configuration syntax

**Wrong:** Set `foreign_keys` after `BEGIN` and label subsequent tests enforcement-enabled.

**Better:** Set it at a permitted boundary and query the effective value. A command's acceptance does not establish that the setting changed: it "is a no-op within a transaction" ([SQLite foreign_keys](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

## Asking a checker a question outside its scope

**Wrong:** Treat `integrity_check` success as proof that foreign-key relationships hold.

**Better:** Check what the observer covers. `integrity_check` looks for formatting faults and "UNIQUE, CHECK, and NOT NULL constraint errors", but "does not find FOREIGN KEY errors". Select the applicable relationship observation and preserve legal NULL cases ([SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check), [foreign-key semantics](https://www.sqlite.org/foreignkeys.html)).

## Making the checker repeat the implementation

**Wrong:** Copy a complex target algorithm and call the second copy an independent model.

**Better:** Derive a simpler invariant or justified relation from the guarantee, and state shared assumptions. Independent evidence can come from separate engines, as in SQLite's SQL Logic Test, or from a relation over different execution paths, as in SQLite's optimization-disabled reruns. Same-engine comparison can still be useful when its relation is valid and its limitations are explicit ([SQLite testing §2](https://www.sqlite.org/testing.html#test_harnesses), [§9](https://www.sqlite.org/testing.html#disabled_optimization_tests), [NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

## Extending a verdict beyond its observation model

**Wrong:** A successful history check establishes every isolation guarantee.

**Better:** State exactly which dependencies and anomalies the observation/checker can decide. Elle's paper states "Our approach ignores predicates"; absence of its reported anomalies does not establish that omitted dimension ([Elle §§4.3 and 9](https://arxiv.org/abs/2003.10554v1)).
