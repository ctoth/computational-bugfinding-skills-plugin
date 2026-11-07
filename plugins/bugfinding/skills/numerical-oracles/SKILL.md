---
name: numerical-oracles
description: Guides adversarial numerical testing with contract-specific rounding and accuracy oracles, bounded high-precision references, special-value classification, and error-directed input search. Use when testing floating-point algorithms, numerical libraries, approximate results, or numerical mismatches.
---

# Numerical oracles

Turn numerical disagreement into a decision about a named promise. Higher precision is a reference technique; a search score is a way to select inputs. Neither alone establishes a defect. The FPGen study explicitly separates input generation from error measurement ([§§3–4, pp.1262,1268](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).

1. **Bind the contract to a real producer.** Record input bits and conversion, valid domain, units, promised accuracy or rounding, and observable effects. Distinguish a correctly rounded operation, a specified sequence of rounded operations, and an approximation to a mathematical function. Read [contracts and reference uncertainty](references/contracts-and-references.md) before selecting a comparator.
2. **Classify before subtracting.** Preserve finite/nonfinite class, sign, zero sign and any promised flags/payloads. Select a reference that can express those obligations; MPFR has a single NaN and does not natively implement subnormals ([manual §1](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)).
3. **Spend compute on numerical novelty.** Search boundary neighborhoods and cancellation/exponent regimes, retain high-error cases even after path coverage stabilizes, then adjudicate separately. Use [search and reduction](references/search-and-reduction.md); the FPGen paper motivates numerical search beyond path selection ([p.1262](https://web.cs.ucdavis.edu/~rubio/includes/icse20.pdf)).
4. **Choose an applicable route.** [Tool routes](references/tool-routes.md) cover MPFR, Herbie and historical FPGen without assuming universal runtime support. Keep reference uncertainty and unsupported input classes visible.
5. **Reduce the violation, then report its scope.** Preserve the producer, domain, rounding environment and violation predicate. Deliver exact input, actual and expected observations, reference confidence, contract citation, environment and replay command. Follow the numerical reduction rules below and delegate general reduction to `failure-reduction`.

Read [common mistakes](references/common-mistakes.md) before accepting a finding. Use `correctness-oracles` for general oracle design, `semantic-differential-testing` for cross-implementation adjudication, `configuration-differential-testing` for environment lanes, and `bugfinding-campaign` for budgets and evidence retention. The workflow and handoff fields above are engineering synthesis; [sources](references/sources.yaml) identifies their numerical foundations.
