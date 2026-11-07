# WRONG / RIGHT configuration decisions

Each entry is **Wrong** first, then **Right**, then why.

## Treating pairwise coverage as all bugs found

**Wrong:** "The 2-way array passed, so the configuration space is clean."

**Right:** Report modeled tuple coverage and remaining interactions; fault estimates need a profile and exercised premises, and fault coverage "is only an approximation" ([Kuhn et al., §III, p.5](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

**Why:** "faults are not necessarily uniformly distributed across the input space", so uncovered tuples can hold the failures.

## Deleting invalid generated rows

**Wrong:** Generate unconstrained rows, drop the invalid ones, and keep the coverage claim.

**Right:** Generate with supported constraints, as PICT advises to "eliminate disallowed combinations during the generation process" ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** "an offending test case may cover other, possibly valid, pairs that would not otherwise be tested."

## Excluding a promised configuration because it fails

**Wrong:** Add `IF [Backend] = "accelerated" THEN [Capability] = "present";` after the fallback lane crashes.

**Right:** Keep it as a candidate; derive restrictions from the real contract, since constraints "express inherent limitations of the modelled domain" ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** a constraint written to remove red output hides the failing supported tuple from every later run.

## Assuming every regression row was retained

**Wrong:** Pass `/e:regressions.tsv` and treat every listed row as executed.

**Right:** Inspect seed omissions and preserve regression evidence independently; a seed row violating constraints "will be skipped entirely" ([PICT, Seeding](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

**Why:** unknown columns and values are also ignored, so a complete regression row can silently become partial.

## Misreading `/s` and `/t`

**Wrong:** Use `/s` to save the test matrix or `/t` as subject concurrency.

**Right:** `/s` will "Show model statistics" instead of rows, and `/t` sets generator worker threads ([parser, `showUsage`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp), [producer, `execute`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp)).

**Why:** with `/s` the producer prints statistics and no rows; parallelism "never changes the produced test suite" and runs no target ([PICT, Parallelism](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

## Counting generated rows as exercised semantics

**Wrong:** Report the generated row count as the tested configuration space.

**Right:** Save effective configuration and actual property evaluations; modeled tuple coverage is not detected-fault evidence ([Kuhn et al., §II, p.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

**Why:** "When test sets do not include settings corresponding to actual faults, the faults will not be detected"; an unapplied or ineffective setting includes nothing.

## Using aliases for distinct behavioral modes

**Wrong:** `Codec: zstd | lz4` because both are "compressed".

**Right:** Model distinct behavior as separate values; for aliases "only the first name counts" in constraints ([PICT, Aliasing](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md), [value methods, `GetNamesForComparisons`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp)).

**Why:** aliases "do not change the combinatorial complexity of the model", so the second spelling gets no interactions of its own.

## Publishing a guessed Advanced ACTS command

**Wrong:** Write an Advanced ACTS command line from memory.

**Right:** Verify the acquired artifact; the NIST page offers Basic directly but says of "the advanced ACTS tool, which supports constraints" to "please send a request" ([NIST distribution, Downloadable Tools](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools)).

**Why:** an unacquired tool's interface is unverified, and the page names constraint support only for the advanced tool.
