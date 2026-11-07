# Common oracle mistakes

## Counting a skip as successful comparison

**Wrong:** Increment the equality count whenever neither query produces a reported mismatch.

**Better:** Inspect the check's skip/error paths. NoREC's sentinel handling does not evaluate equality; preserve that outcome separately ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

## Accepting every expected error without observing effects

**Wrong:** Return success immediately on a documented constraint error.

**Better:** Check the permitted post-state too. ABORT and FAIL have different effect boundaries; do not assert total transaction rollback for both ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

## Trusting configuration syntax

**Wrong:** Set `foreign_keys` after `BEGIN` and label subsequent tests enforcement-enabled.

**Better:** Set it at a permitted boundary and query the effective value. A command's acceptance does not establish that the setting changed ([SQLite foreign_keys](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

## Asking a structural checker a semantic question

**Wrong:** Treat `integrity_check` success as proof that foreign-key relationships hold.

**Better:** Select the applicable relationship observation and preserve legal NULL cases ([SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check), [foreign-key semantics](https://www.sqlite.org/foreignkeys.html)).

## Making the checker repeat the implementation

**Wrong:** Copy a complex target algorithm and call the second copy an independent model.

**Better:** Derive a simpler invariant or justified relation from the guarantee, and state shared assumptions. Same-engine comparison can still be useful when its relation is valid and its limitations are explicit ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

## Extending a verdict beyond its observation model

**Wrong:** A successful history check establishes every isolation guarantee.

**Better:** State exactly which dependencies and anomalies the observation/checker can decide. Elle's paper omits predicate analysis; absence of its reported anomalies does not establish that omitted dimension ([Elle §§4.3 and 9](https://arxiv.org/abs/2003.10554)).
