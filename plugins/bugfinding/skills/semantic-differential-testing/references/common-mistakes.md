# Common mistakes

| Misleading shortcut | Correction and source |
|---|---|
| Same input file means comparable semantics | Check the effective contract and implementation-defined target class ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). |
| Same initial fixture means every batched case starts equivalent | Inspect the producer and preserve/re-establish the relevant setup or causal prefix ([SQLancer logs and reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). |
| Equal returned values prove equal effects | Observe the promised state/output boundary; answer checks and failure/storage checks are distinct ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)). |
| Sort everything or compare sets universally | Derive order and multiplicity from the contract; retain complete required rows ([PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html), [ORDER BY](https://www.postgresql.org/docs/current/queries-order.html)). |
| A helper named result equality compares every result dimension | Read its actual caller and extraction/comparison path ([SQLancer comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java), [real DQP caller](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/mysql/oracle/MySQLDQPOracle.java)). |
| Missing output or expected-error skip is agreement | Keep skipped comparisons separate from successfully evaluated equality ([SQLancer comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). |
| The majority implementation is correct | Treat disagreement as evidence to adjudicate; shared wrong answers can escape differential detection ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). |
| Any smaller mismatch is the reduced finding | Revalidate the input and selected mismatch after shrinking ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [LLVM validity investigation](https://llvm.org/docs/HowToSubmitABug.html#miscompilations)). |
