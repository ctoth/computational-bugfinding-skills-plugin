# Contracts and reference uncertainty

## Write the promise first

As an engineering convention, record these fields before generating inputs:

- Producer and domain: exact serialized bytes or float bits, conversion path, dimensions, units and admissible measurement uncertainty.
- Promise: correctly rounded primitive; stepwise rounded graph; absolute/relative/ULP bound; residual/backward-error bound; interval inclusion; or explicit allowed outcomes.
- Environment: input/intermediate/output formats, rounding mode, exponent range, subnormal policy, fusion/reassociation permissions, compiler/library/backend and CPU.
- Observations: numerical result and any promised sign, exception status, branch or externally visible effect.

Do not infer the promise from a convenient reference. MPFR specifies individual operation rounding; Herbie accepts a mathematical specification distinct from the expression being improved, and "will use the `:spec` expression to evaluate error" ([MPFR §§4.4–4.5](https://www.mpfr.org/mpfr-4.2.2/mpfr.html); [Herbie specifications](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/input.html)).

## Compare only what the contract defines

For finite result `y` and reference `r`, absolute error is `|y-r|`; relative error is `|y-r|/|r|` for nonzero `r`. A clamped denominator defines a different metric: DLMF names `|y-r|/max(|r|,1)` separately ("The mollified error is", equation 3.1.11), and the FPGen study's `|r-r0|/max{FLT_MIN,|r0|}` is another such convention. Bind its scale to the actual promise ([DLMF §3.1(v), equations 3.1.8–3.1.11, version 1.2.8, 2026-09-15](https://dlmf.nist.gov/3.1); [FPGen §3.3, p.1268](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).

Define a ULP comparator's format, ordering, zeros and boundary convention explicitly. Herbie's representable-distance score is `log2(n + 1)` bits for values `n` apart; values like "0 and -0 are treated as having 0 bits of error", and NaN against a non-NaN value scores "the maximum number of bits of error". Use it for its documented purpose rather than silently adopting it as the product contract ([bits of error](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/error.html)).

Derived conditioning example: if `s=sum(x_i)` and `|delta x_i|<=eta|x_i|`, the triangle inequality gives `|delta s|<=eta sum|x_i|`. For nonzero `s`, divide by `|s|` for a relative sensitivity bound. This is input sensitivity, not an algorithm-error allowance. Keep measurement uncertainty separate from the numerical implementation promise (engineering derivation using the [absolute/relative definitions](https://dlmf.nist.gov/3.1)).

## Bound reference uncertainty

MPFR rounds each destination operation correctly for the specified precision and mode, and "The input variables are regarded as exact"; this does not make an arbitrary composed computation exact. Its `mpfr_can_round` requires an approximation-error bound and decides "assuming an unbounded exponent range", returning 0 for NaN and Inf; check overflow, underflow and subnormal outcomes of the target format separately. For binary64 emulation, follow §5.13's precision, exponent limits and per-operation `mpfr_subnormalize` handling. §1's 53-bit binary64 statement sits beside "the default exponent range is much wider", so precision 53 alone does not reproduce binary64's range or subnormals ([MPFR §§1, 4.4, 5.11, 5.13](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)).

For a mathematical-value oracle, use a justified enclosure with outward endpoint rounding ("appropriate roundings of the end points") and valid operation domains. Division by an interval containing zero needs separate treatment; DLMF's interval division is defined "only if the divisor interval does not contain zero" ([DLMF §3.1(ii), equation 3.1.6](https://dlmf.nist.gov/3.1)). Engineering decision rule: if all values in the enclosure imply the same allowed rounded answer, adjudicate; if it overlaps an acceptance boundary, refine or mark inconclusive. Repeated agreement at larger precision supplies evidence, not a proof of enclosure. Preserve stepwise rounding when that is the promise.

Classify finite, infinity, NaN and signed zero before error arithmetic; then test only promised distinctions. MPFR's single NaN ("there is a single NaN") cannot establish payload/signaling preservation ([MPFR §1](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)). The FPGen printer's arithmetic and ordered maxima are unsuitable as a complete special-value oracle: it computes `abs_err / (abs_hdata<FLT_MIN? FLT_MIN: abs_hdata)` and keeps maxima with `rel_err>maxrel?rel_err:maxrel`, so a NaN error never replaces the maximum ([print_error.c lines 64–80](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/utils/print_error.c)).
