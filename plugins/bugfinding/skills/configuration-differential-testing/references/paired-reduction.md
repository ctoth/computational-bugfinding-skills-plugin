# Paired reduction and worked cases

This is the pack's proposed investigation procedure. Coverage theory measures modeled interactions, "the proportion of t-way combinations of variable settings included in a test set"; it does not provide causal attribution or a target's semantic comparison contract ([Kuhn et al., §II, p.1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Retain two actual executions: supported configuration, effective settings, build/runtime/architecture, input/world or history, raw observations and the governing shared guarantee. Establish that both reached the same relevant property. A baseline binary accidentally reused for both labels has not exercised a configuration difference.

Reduce changed factors toward a supported baseline, maintaining prerequisite closure. If factors are coupled, try valid groups. Then reduce input/state/history under that same pair, revisiting factors when simplification permits. Preserve the original and reject reductions that merely create an invalid build or erase the compared behavior. Report local reduction relative to attempted moves; pairwise discovery does not identify global interaction order, because a t-way array "can detect t-way faults" and also a proportion of (t+1)-way faults through ancillary coverage ([Kuhn et al., §III, pp.4–5](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

## Worked scenarios

These are illustrative designs, not executed product findings.

- **Optimizer and backend.** Derive real runtime/backend/capability/optimization factors. Keep the same defined-semantics input, verify effective backend, then compare its promised effects. Increase a relevant higher-order group or input family when ordinary rows never reach lowering behavior. A documented fallback must not be excluded just because it fails.
- **Storage variants.** Compare logical records across a supported codec/architecture/runtime pair only where the format promises compatibility. Preserve duplicate/order/numeric rules. A disabled feature's documented rejection needs its own assertion, not equality with an enabled result.
- **Capability absence.** Keep absence in the valid domain when fallback is promised; confirm the fallback actually ran. If invalid combinations instead require clean rejection, test that separate contract. PICT's `~` negative values are generated so that "two out-of-range values do not appear in the same test case", so multi-invalid interactions are deliberately never covered and need their own cases if the contract governs them ([PICT, Negative Testing](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

For each result save model/constraints and their sources, generated and executed rows, supported-build evidence, both raw outcomes, normalization/preconditions, replay invocation, reduction attempts and exclusions. Use `failure-reduction` and `evidence-based-triage` for their separate mechanics; do not infer blame from one platform pair.
