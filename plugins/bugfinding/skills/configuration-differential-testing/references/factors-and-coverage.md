# Factor model and exercised coverage

This is the pack's experiment-design procedure. Use the target's real supported contracts and producers; the literature supplies coverage distinctions, not a ready target model; value selection stays a modeling choice, and "test effectiveness is also dependent on the values selected" ([Kuhn et al., §II, p.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

For each factor save its requested value, concrete control (binary, build option, runtime setting or platform), documented support constraint, effective-value observation, and the guarantee tested. An unavailable runner is unexecuted support, not evidence of product invalidity. A capability documented to fall back when absent must remain in the valid domain; do not constrain away its crash. PICT constraints "express inherent limitations of the modelled domain", not observed failures ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

Separate semantic classes before comparison: a relaxed numeric mode, deliberately stale read mode or different format version may change the promise. Establish shared input/state preconditions and observe the actual promised result/effects. This is contract selection, not a covering-array feature: the paper's fault-coverage model assumes "deterministic software that computes the same output" for one system under test ([Kuhn et al., §III, p.3](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)); the detailed paired oracle belongs to `semantic-differential-testing`.

## Define the constrained universe

For factor subset J, define V_J as tuples extendable to at least one supported full configuration; define E_J from configurations whose relevant test and oracle actually executed. The proposed constrained measure is |E_J|/|V_J|, with empty denominators explicit. It adapts the paper's simple t-way, total variable-value and minimum-coverage distinctions (in its Table I, simple 2-way coverage is 33% while total variable-value coverage is 79%); it is not its theorem about fault detection ([Kuhn et al., §II, pp.2–3](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Save model/constraint provenance, exclusions, generated rows and actual execution dispositions. A tuple's occurrence in a table is less evidence than its execution with a relevant input. Report the tested input family too: configuration-only coverage on inert inputs can omit the decisive branch values; for predicates on "internal variables not included in the test set", the paper's branch condition must be validated by inspecting internal state, which it says "may in most cases be impractical" ([Kuhn et al., §IV, p.7](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Use exhaustive valid rows for small domains. Otherwise state chosen strength, higher-order groups, regression rows and untested residual space. PICT sub-models are parameter groups that "get their own combinatory orders"; its packing heuristics are not a universal strength policy ([PICT, Sub-Models](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

## Illustrative capability model

The following names are invented. The implication is legitimate only if the actual target requires the capability; a promised fallback would make this exclusion wrong ([PICT, Constraints and Conditional Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)):

```text
Runtime: base, candidate
Backend: portable, accelerated
Capability: absent, present
Optimize: off, on
IF [Backend] = "accelerated" THEN [Capability] = "present";
```

A supported failing tuple remains in the campaign. Record unsupported syntax, an ignored option and a genuine supported build failure separately; adjusting constraints merely to remove red output changes the experiment.
