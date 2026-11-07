# Common mistakes

## One global epsilon

**Wrong:** Accept every result within one global epsilon.

**Right:** Select a bound and scale from the specific promise. DLMF defines relative error only for a nonzero reference `x` (equation 3.1.9) and names the clamped variant separately ("The mollified error is", equation 3.1.11) ([DLMF §3.1(v)](https://dlmf.nist.gov/3.1)).

**Why:** a single epsilon silently picks an absolute, relative or clamped metric the contract never named.

## High-precision replay as mathematical truth

**Wrong:** Treat a high-precision replay as mathematical truth.

**Right:** Track approximation uncertainty. A rounding decision requires the relevant bound, as `mpfr_can_round` explicitly assumes: "Assuming b is an approximation of an unknown number x" with a stated error bound ([MPFR §5.11](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)).

**Why:** more bits shrink the error of a composed computation without bounding it.

## Calling specified cancellation a bug

**Wrong:** Call cancellation in a specified rounded expression a bug because a real-algebra rewrite differs.

**Right:** Identify whether the promise is that graph or mathematical accuracy. Herbie's separate `:spec` makes this distinction explicit: it "will use the `:spec` expression to evaluate error" ([Herbie input format, Specifications](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/input.html)).

**Why:** when the stepwise rounded result is the promise, the cancellation is the required answer.

## Zero-merging score for a zero-sign promise

**Wrong:** Use a signed-zero-merging score to test a zero-sign promise.

**Right:** Classify the promised distinction separately. In Herbie's metric, values like "0 and -0 are treated as having 0 bits of error" ([Herbie bits of error](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/error.html)).

**Why:** the score reports zero error for exactly the violation being tested.

## Stopping search when coverage stabilizes

**Wrong:** Stop exploring a path after coverage stabilizes.

**Right:** Retain error-directed numerical search when applicable. An input covering a path "does not necessarily trigger large numerical errors on that path" ([FPGen §1, p.1262](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).

**Why:** error varies along one path, so saturated coverage says nothing about the largest error.

## Running the FPGen driver as a read-only probe

**Wrong:** Run the historical FPGen comparison script as a portable read-only probe.

**Right:** Inspect its fixed paths and file mutations before considering an isolated adaptation; it sets `rootpath=/home/fptesting/FPTesting` and ends with `rm -f out-* test_input` ([compute_error.sh lines 3, 39](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/scripts/compute_error.sh)).

**Why:** it writes and deletes files in the current directory and depends on a fixed install path.

## Shrinking until the violation vanishes

**Wrong:** Shrink until the input looks simple while the original violation vanishes.

**Right:** Preserve the numerical violation predicate and remeasure each candidate; generation and final measurement are distinct, since generated inputs "are evaluated by computing the numerical error they trigger" ([FPGen §3.3, p.1268](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).

**Why:** a reduced input that no longer violates the promise reproduces nothing.

Reduction and environment recording are proposed workflow conventions; they do not establish applicability to a target without its producer and contract.
