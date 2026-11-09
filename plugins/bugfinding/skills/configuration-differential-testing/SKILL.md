---
name: configuration-differential-testing
description: Searches constrained build, runtime, platform and capability combinations for contract violations, including Node.js release lines, ESM versus CommonJS loading, browser engines and React development versus production builds. Use when defaults pass but interacting configurations may change behavior, or when extending differential testing across supported modes.
---

# Configuration differential testing

Spend compute on supported configuration interactions and inputs that exercise them. A covering array covers modeled value tuples; predicting fault detection also needs a fault profile and relevant exercised behavior, since "faults are not necessarily uniformly distributed across the input space" ([Kuhn et al., §III, p.5](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). This skill's procedure combines that distinction with constrained generation; it is not an empirical guarantee of bug yield.

## Establish the executable configuration model

Read the actual build/runtime producer and shared guarantee. Record each factor's finite values, source of support/exclusions, and evidence that a requested setting became effective. Separate product-invalid tuples from supported lanes unavailable on this machine. An unexplained supported build failure stays a candidate, not a new exclusion. Use [factor and coverage design](references/factors-and-coverage.md); the distinction between modeled values and the variables actually reaching a branch matters: the paper's branch-coverage result requires decision-predicate variables to take values from the covered set, which it calls "a relatively strong assumption in practice" ([Kuhn et al., §IV, pp.6–7](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). For Node.js, module format, Playwright browser and React build factors, read the JavaScript section of that reference; the supported Node.js set changes with the release schedule, whose own table says "Dates are subject to change" ([nodejs/Release](https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/README.md)).

Group executions by a justified common contract. Preserve intended differences, optional-feature rejection rules and input preconditions; use `semantic-differential-testing` for observation/equivalence design. The paper's fault-coverage model assumes "deterministic software that computes the same output" for a given input within one system; it does not establish that arbitrary modes promise identical semantics ([Kuhn et al., §III, p.3](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

## Generate, execute and observe

Use full valid-domain enumeration when tractable, otherwise an explicit interaction strength plus necessary regression/higher-order cases. Integrate supported constraints during generation; deleting invalid output rows can lose valid interactions, because "an offending test case may cover other, possibly valid, pairs" ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)). For the concrete PICT route, setup, commands and ACTS availability limits, read [tool operation](references/pict-operation.md).

Apply each saved row through the existing target runner with controlled input/state. Record requested/effective values, selected binary/build, real capability evidence, raw outputs and actual oracle evaluation. Count generated, buildable, applied and compared cases separately: factor coverage alone does not establish a triggered or detected fault; the paper calls its fault-coverage figure "only an approximation" ([Kuhn et al., §III, p.5](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)). Use the pack's corpus/generation owners for input diversity; do not build a matrix service.

Spend the next allocation on missing valid tuples, stronger interactions, additional meaningful inputs or actual platform lanes. PICT's best-of-N "keeps the smallest resulting suite", and its worker threads are "purely a performance option" of generation, not target concurrency; neither is a defect-prioritization oracle ([PICT, Best-of-N generation and Parallelism](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md), [PICT generation](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp), [CLI](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp)).

## Reduce and return the actual pair

Preserve the original supported configurations, effective settings, input/setup, compared contract and raw witness. Reduce factors toward a supported baseline with prerequisite closure, then input/history; alternate when useful. This is the pack's reduction procedure, not a proof of global causal minimality. Read [paired reduction and worked cases](references/paired-reduction.md); use `failure-reduction` for general interestingness and `evidence-based-triage` for attribution. A t-way array will "always include other combinations beyond t-way as well", so discovery in pairwise tests does not establish a two-factor cause ([Kuhn et al., §III, p.4](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Return the modeled/actually executed domain, strength and residual space, concrete replay pair, dispositions and evidence paths. Preserve zero findings and unexecuted supported lanes. For misleading shortcuts, read [WRONG/RIGHT mistakes](references/common-mistakes.md).

Invocation preserves existing execution and publication authority; it does not itself authorize installs, target changes or external services.
