# Improve numerical-oracles

Skill: `plugins/bugfinding/skills/numerical-oracles/`. Accessed 2026-11-07.

## Findings

### F1 references/contracts-and-references.md:28, references/sources.yaml:84 — ERROR (wrong line range)
- Text said: FPGen printer "arithmetic and ordered maxima" at `lines 60–74`.
- Source (https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/utils/print_error.c, fetched with curl): line 60 is a `printf` of high-precision output; the error loop is lines 64–80 — clamp at line 73 `rel_err = abs_err / (abs_hdata<FLT_MIN? FLT_MIN: abs_hdata);`, double casts at lines 74 and 80, ordered maxima at lines 76–77 (`maxrel = rel_err>maxrel?rel_err:maxrel;`).
- Fix: cite lines 64–80 in text and sources.yaml; add quote of line 73 fragment.

### F2 SKILL.md:8, references/search-and-reduction.md:5 — WARNING (section imprecise)
- Text said: FPGen `§§3–4, pp.1262,1268` for separating generation from measurement.
- Source (paper page images page-001.png = p.1262, page-007.png = p.1268, read this session): p.1262 is §1 Introduction ("For each input generated, we measure the error it exposed"); the measurement step is §3.3 "Error Measurement" on p.1268. §4 is the evaluation.
- Fix: cite `§§1, 3.3, pp.1262, 1268`; add verbatim fragments.

### F3 references/common-mistakes.md:3-11 — ERROR (format)
- Text said: a two-column WRONG/RIGHT table with no one-line why.
- Pattern: skill-draft Step 3 / sibling `bounded-model-checking/references/common-mistakes.md` use `## heading`, `**Wrong:**`, `**Right:**`, `**Why:**` per entry.
- Fix: same seven entries rewritten as Wrong/Right/Why sections; citations kept, quotes added.

### F4 references/contracts-and-references.md:24 — WARNING (gap exposed by source)
- Text said: `mpfr_can_round` requires an approximation-error bound.
- Source (https://www.mpfr.org/mpfr-4.2.2/mpfr.html §5.11): the decision is made "assuming an unbounded exponent range" and returns 0 "(including for NaN and Inf)". A can-round answer therefore does not cover overflow/underflow/subnormal outcomes of the emulated format.
- Fix: one clause added saying exponent-range effects are checked separately.

### F5 references/contracts-and-references.md:24 — WARNING (apparent conflict with source)
- Text said: "precision 53 alone is insufficient" for binary64 emulation.
- Source (MPFR §1): "computations in the binary64 format (a.k.a. double precision) can be reproduced by using a precision of 53 bits", in the same sentence as "the default exponent range is much wider, and subnormal numbers are not implemented"; §5.13's binary64 example also calls `mpfr_set_emin (-1073); mpfr_set_emax (1024);` and `mpfr_subnormalize`.
- Fix: sentence now states why 53 bits alone does not match binary64 (default exponent range wider, subnormals not implemented), quoting §1, so it no longer reads as contradicting §1.

### F6 references/contracts-and-references.md:16 — INFO (gap)
- Text said: "A clamped denominator defines a different metric" without naming DLMF's own clamped measure.
- Source (https://dlmf.nist.gov/3.1 §3.1(v), eq. 3.1.11): "The mollified error is" `|x*−x|/max(|x|,1)`; FPGen §3.3 (p.1268) uses `|r−r0|/max{FLT_MIN,|r0|}`.
- Fix: named both as distinct clamped metrics.

### F7 references/contracts-and-references.md:18 — INFO (gap)
- Source (Herbie error.html at d493bef): "NaN is considered to have the maximum number of bits of error against non-NaN values".
- Fix: added to the Herbie metric description, which previously mentioned only zero merging.

### F8 references/sources.yaml (12 entries) — WARNING (format)
- Text had a `quote_fragment` field not in the skill-draft Step 7 format (name/url/type/accessed/sections_used); e.g. the paper's `"Error Measurement"` and the printer's sections were stale (F1).
- Fix: removed `quote_fragment` lines; quotes now live inline next to the claims; sections_used corrected.

### F9 all files — INFO (quotes)
- Load-bearing claims lacked verbatim fragments (skill-draft Step 5). Added 4-10 word fragments, each retrieved this session from the pinned source and placed before its citation link. List in Validation.

### F10 SKILL.md:14 — WARNING (dangling reference)
- Text said: "Follow the numerical reduction rules below"; SKILL.md has no reduction rules below step 5.
- Source: the rules are in `references/search-and-reduction.md` section "Reduce while preserving numerical meaning".
- Fix: linked `references/search-and-reduction.md#reduce-while-preserving-numerical-meaning`.

### F11 references/tool-routes.md:29 — INFO (precision)
- Text said: driver "mutates working-directory files" without naming them or lines.
- Source (compute_error.sh at 5e0102e): line 16 `echo "" >rel-errors`, line 19 `cp $test test_input`, lines 20-22 write `out-64`, `out-128`, `out--`, line 30 `cp $test best_input`, line 39 `rm -f out-* test_input`.
- Fix: named the files and cited lines 3, 16–39.

Verified unchanged (fetched, text matches): Herbie README Racket 8.0+/Rust 1.87.0+; Herbie MIT license; FPGen BSD 3-Clause; Herbie `:spec`, `:pre`, `:precision`; Herbie options (options before paths, per-input timeout, seed); Herbie valid-input exclusion and warning; FPGen `compute_error.sh` hardcoded rootpath and working-directory writes (lines 3, 16-39); FPGen README Ubuntu 14.04.5 LTS; MPFR §2 `cc -o version version.c -lmpfr -lgmp`; MPFR LGPL v3-or-later (§1); DLMF eqs 3.1.8-3.1.11, Version 1.2.8, release 2026-09-15; paper p.1268 128-bit summation reference.

## Pinned URLs

None needed changing. Every GitHub link was already a raw.githubusercontent.com permalink at a full 40-hex SHA (Herbie `d493bef58667fcb62652fc3e6c2fd67527ff0f76`, FPGen `5e0102e587eab4c22d5ef4d0cee03d80a5875a72`); all fetched at those SHAs with curl this session. MPFR uses the versioned `/mpfr-4.2.2/` path. DLMF publishes no versioned URL: `https://dlmf.nist.gov/3.1` kept, with Version 1.2.8 / release 2026-09-15 (read from the page footer) in text and sources.yaml. The FPGen paper URL is the author PDF; DOI 10.1145/3377811.3380359 added to sources.yaml.

## Validation

Quotes: every non-paper quote was matched mechanically against the fetched source text (script `num-oracles-checkquotes.py` in the scratchpad, read-only). The seven paper quotes ("For each input generated, we measure the error it exposed", "does not necessarily trigger large numerical errors on that path", "we transform the program into higher precision", "are evaluated by computing the numerical error they trigger", "we implemented summations that use 128-bit precision") were checked by reading page images page-001.png (p.1262) and page-007.png (p.1268) in `C:/Users/Q/code/bugfinding-literature/numerical-oracles/papers/Guo_2020_ErrorInducingFloatingPoint/pngs/` this session.

Raw output:

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/numerical-oracles
Skill is valid!
--- cited not in yaml:
--- yaml not cited:
--- moving urls:
--- local links:
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/contracts-and-references.md
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/search-and-reduction.md
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/tool-routes.md
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/search-and-reduction.md
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/common-mistakes.md
ok plugins/bugfinding/skills/numerical-oracles/SKILL.md -> references/sources.yaml
ok plugins/bugfinding/skills/numerical-oracles/references/tool-routes.md -> contracts-and-references.md
--- diff check:
rc=0
(each file's last two bytes: "." or '"' then "\n" — exactly one trailing newline)
16 plugins/bugfinding/skills/numerical-oracles/SKILL.md
$ python -c "yaml.safe_load(...)"
12 entries; {'type', 'name', 'sections_used', 'url', 'accessed'}
```

The anchor `#reduce-while-preserving-numerical-meaning` matches the heading `## Reduce while preserving numerical meaning` in search-and-reduction.md.

## Unverified

- No claim was cut; every factual sentence already had or now has a fetched primary source. Sentences labelled "engineering convention", "engineering synthesis", "proposed campaign design" or "engineering decision rule" are the skill's own synthesis and are marked as such in the text; they carry no source claim.
- The research notes' machine description ("Xeon Gold6238R") disagrees with the paper page image p.1268 and FPGen README ("Gold 6238 CPU"); that note is outside the skill and not edited. The skill does not state the CPU.
- Whether Herbie commit d493bef corresponds to a 2.4 release was not checked; tool-routes.md already says the pin is not an assertion of that.
