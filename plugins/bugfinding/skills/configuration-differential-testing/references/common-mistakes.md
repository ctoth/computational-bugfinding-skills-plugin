# WRONG / RIGHT configuration decisions

| WRONG | RIGHT |
|---|---|
| Treat pairwise coverage as all bugs found. | Report modeled tuple coverage and remaining interactions; fault estimates need a profile and exercised premises ([Kuhn et al., pp.2–7](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). |
| Delete invalid generated rows and retain the coverage claim. | Generate with supported constraints; deleted rows can uniquely carry valid tuples ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)). |
| Add an exclusion because a promised configuration fails. | Keep it as a candidate; derive restrictions from the real contract rather than use the generator to hide evidence (this pack's procedure; [coverage-model premises](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). |
| Assume every regression row was retained. | Inspect seed conversion/omissions and preserve regression evidence independently ([PICT, Seeding](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)). |
| Use `/s` to save the test matrix or `/t` as subject concurrency. | `/s` is statistics; `/t` controls generation workers ([parser](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp), [producer](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp)). |
| Count requested labels or generated rows as exercised semantics. | Save effective configuration and actual property evaluations; modeled tuple coverage is not detected-fault evidence ([Kuhn et al., pp.2–7](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). |
| Use aliases for distinct behavioral modes. | Alias comparison uses the primary name; model distinct behavior as separate values ([actual value methods](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp)). |
| Publish a guessed Advanced ACTS command. | Verify the acquired artifact; the observed distribution distinguishes Basic and requested Advanced ([NIST](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools)). |
