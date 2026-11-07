# Common mistakes

| WRONG | RIGHT |
|---|---|
| Accept every result within one global epsilon. | Select a bound and scale from the specific promise; relative error excludes a zero reference ([DLMF §3.1(v)](https://dlmf.nist.gov/3.1)). |
| Treat a high-precision replay as mathematical truth. | Track approximation uncertainty; a rounding decision requires the relevant bound, as `mpfr_can_round` explicitly assumes ([MPFR §5.11](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)). |
| Call cancellation in a specified rounded expression a bug because a real-algebra rewrite differs. | Identify whether the promise is that graph or mathematical accuracy; Herbie's separate `:spec` makes this distinction explicit ([specifications](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/input.html)). |
| Use a signed-zero-merging score to test a zero-sign promise. | Classify the promised distinction separately; Herbie's metric deliberately merges zeros ([bits of error](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/error.html)). |
| Stop exploring a path after coverage stabilizes. | Retain error-directed numerical search when applicable; path selection alone need not maximize error ([FPGen p.1262](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)). |
| Run the historical FPGen comparison script as a portable read-only probe. | Inspect its fixed paths and file mutations before considering an isolated adaptation ([driver](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/scripts/compute_error.sh)). |
| Shrink until the input looks simple while the original violation vanishes. | Preserve the numerical violation predicate and remeasure each candidate; generation and final measurement are distinct ([FPGen §3.3](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)). |

Reduction and environment recording are proposed workflow conventions; they do not establish applicability to a target without its producer and contract.
