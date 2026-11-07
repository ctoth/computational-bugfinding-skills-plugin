# Search and reduction

## Select on error, decide on the promise

FPGen inserts checks for precision loss and cancellation to guide symbolic exploration, then evaluates generated inputs against higher-precision executions: "we transform the program into higher precision" and compare. An input exercising a path need not expose that path's large numerical error; it "does not necessarily trigger large numerical errors on that path". These motivate a numerical search objective alongside coverage, not universal FPGen thresholds or predicted bug yield ([FPGen §§1, 3.3, pp.1262, 1268](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).

The following is a proposed campaign design derived from that distinction:

1. Seed from real producer inputs. Add domain-valid adjacent representable values around zero, normal/subnormal transitions, overflow, cancellation, denominator zeros, piecewise branches and rounding ties relevant to the expression.
2. Mutate sign, exponent and significand separately; use paired operands to maintain cancellation or a prescribed scale ratio. For arrays, vary length and operand order only where the input contract permits them.
3. Rank by contract-bound excess, certified reference distance, or a labeled exploratory error score. Keep special-value and branch/effect failures as separate classes. Maintain a reservoir per numerical regime so a single large score does not erase distinct evidence.
4. Re-evaluate retained cases with the actual acceptance oracle. Store unresolved references as inconclusive, with their precision/enclosure limit; they are neither accepted cases nor confirmed bugs.

Herbie's sampled average accuracy concerns valid, computable inputs. It can omit points whose reference cannot be computed ("you'll get a warning if this happens"), so retain excluded regions and warnings when interpreting results ([valid inputs and percentage accuracy](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/error.html)). Use `corpus-evolution` and `bugfinding-campaign` for corpus and compute allocation rather than introducing another campaign engine.

## Reduce while preserving numerical meaning

Use `failure-reduction` with this method-specific predicate (engineering synthesis from the separation of generation and measurement in [FPGen §3.3](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)):

- Preserve exact input bits, domain membership, producer conversion and chosen environment. Recompute the reference and acceptance decision for every candidate.
- Simplify shape or delete operands first when legal; then simplify exponent/significand and move toward nearby representable boundary values. A numerically tiny value need not be structurally irrelevant.
- Preserve the observable violation: wrong rounding, error beyond a named bound, classification, flags, branch or effect. Do not accept merely a larger exploratory score.
- Preserve the required cancellation, scale ratio or condition regime when removing it would change the claim. Record whether the result is minimal under the tried transformations; do not claim global minimality.

Example design: for a real-sum accuracy promise, explore triples of large positive, small positive and large negative values; keep exact bits and evaluate the declared summation algorithm against a certified sum. For a stepwise language-semantics promise, the same cancellation may be the required answer, so the predicate must change. The FPGen evaluation's higher-precision summation comparison ("we implemented summations that use 128-bit precision") illustrates the first type, not a universal language-semantics violation ([FPGen §4, p.1268](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).
