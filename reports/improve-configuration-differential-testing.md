# Improve configuration-differential-testing

## Findings

Paper evidence: Kuhn, Kacker, Lei preprint page images `page-000.png`..`page-006.png` re-read this session from `C:/Users/Q/code/bugfinding-literature/configuration-differential-testing/papers/Kuhn_2016_MeasuringCombinatorialCoverage/pngs/` (paper-reader collection). Section map from the images: §II Combinatorial Coverage pp.1-3; §III Fault Coverage pp.3-6; §IV Relationship with Code Coverage pp.6-7; §V Implications for Testing pp.7-8.

### F1. SKILL.md:12, references/factors-and-coverage.md:13 — ERROR — wrong section
- Text: cites "[Kuhn et al., §III]" for modeled values vs variables actually reaching a branch / inert inputs omitting decisive branch values.
- Source: that material is §IV "Relationship with Code Coverage" (pp.6-7): the branch coverage condition requires "all variables in decision predicates have values from the variable set" and the paper calls this "a relatively strong assumption in practice" (p.7). §III is Fault Coverage. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142
- Fix: change to §IV, pp.6-7, add quote.

### F2. references/factors-and-coverage.md:7 — WARNING — citation does not support claim
- Text: "This is contract selection, not a covering-array feature ([Kuhn et al., §III])".
- Source: §III is the fault-coverage estimate; it assumes "deterministic software that computes the same output for a given set of input parameters and values" (p.3) — a single SUT, no cross-mode contract.
- Fix: cite §III p.3 with that quote, stating what the model assumes.

### F3. SKILL.md:14 — WARNING — vague page range for a negative claim
- Text: "The paper's coverage model does not establish that arbitrary modes promise identical semantics ([Kuhn et al., pp.4–7])".
- Source: the relevant statement is the §III deterministic-SUT assumption on p.3 (quote above); pp.4-7 discuss profiles and branch coverage.
- Fix: cite §III p.3 with quote.

### F4. SKILL.md:8, :20, references/common-mistakes.md:5,:10 — INFO — load-bearing claim lacks quote
- Source: p.5 (§III) "The effectiveness of fault detection clearly depends on both the proportion of t-way combinations covered and the distribution of faults"; "faults are not necessarily uniformly distributed across the input space".
- Fix: added quote fragments and §III, p.5 locators.

### F5. SKILL.md:26, references/paired-reduction.md:7 — INFO — load-bearing claim lacks quote
- Source: p.4 (§III) a covering array "will always include other combinations beyond t-way as well".
- Fix: added quote with §III, p.4.

PICT evidence: all six cited files fetched with curl at commit ab76c2548f551fcb46314e58653a1bd1172f3a72 (`gh api repos/microsoft/pict/commits/ab76c25...` returns that SHA, committed 2026-09-08; it is also current `main`). Verified true against source: `/o` order default 2, `/r` seed, `/e` seed file, `/b:N` deterministic seeds `baseSeed + i`, "smallest suite wins, ties broken by earliest seed" (pict.cpp:144), `/t` worker threads, `/s` prints statistics instead of rows (pict.cpp:263-283), `/f:json` (cmdline.cpp:274-279, showUsage :347), `/x` and `/p` hidden from usage (cmdline.cpp:351-352), aliases compare by primary name (model.cpp:14-19), round-robin output names (model.cpp:24-31), seed-row rules (pict.md Seeding rules 1-3), case-insensitive default (pict.md Case Sensitiveness), README build steps, MIT license.

### F6. references/pict-operation.md:20 — WARNING — wrong section locator
- Text: "ordinary table output is tab-separated with a header ([PICT, Model File/Seeding])".
- Source: pict.md "Output Format": "The first line of the output contains names of the parameters... Values in each line are separated by a tab."
- Fix: locator changed to "Output Format"; sources.yaml sections_used updated.

### F7. references/paired-reduction.md:15 — WARNING — imprecise statement of PICT negative testing
- Text: "PICT's negative-value design does not establish safety of every multi-invalid interaction".
- Source: pict.md Negative Testing: PICT ensures "two out-of-range values do not appear in the same test case" — multi-invalid tuples are deliberately never generated, not merely unproven.
- Fix: stated what PICT does, with quote.

### F8. references/pict-operation.md:22 — INFO — load-bearing claim lacks quote
- Source: cmdline.cpp:351 hidden usage line "Approximate generation (best effort, might not cover all combinations)"; pict.md Parallelism "Parallelism is purely a performance option".
- Fix: added quotes.

### F9. SKILL.md:22 — INFO — workers claim cited only to source code
- Source: pict.md Parallelism: "it never changes the produced test suite"; Best-of-N: "keeps the smallest resulting suite".
- Fix: added pict.md citation and quotes.

### F10. references/sources.yaml:37-43 — INFO — sections_used do not match headings
- Text: "Building on Windows; Building on Linux".
- Source: README headings are "Building and testing on Windows with MsBuild" and "Building on Linux, OS/X, *BSD, etc.".
- Fix: exact headings.

### F11. references/pict-operation.md:32 and common-mistakes.md:12 — WARNING — claim beyond page text
- Text: "do not ... substitute Basic for its constraints"; implies the page says Basic lacks constraints. The NIST page (fetched 2026-11-07, "Updated June 08, 2026") names constraint support only for the advanced tool: "To obtain the advanced ACTS tool, which supports constraints, please send a request" (punctuation checked in the raw HTML). It says nothing about Basic's constraint support. Public-domain sentence: "this software is public domain".
- Fix: reworded to what the page says, with quotes.

### F12. references/common-mistakes.md:3-12 — ERROR — format does not meet skill-draft Step 3 / audit check 7
- Text: two-column WRONG/RIGHT table with no one-line why; several rows cited only to a page range ("pp.2–7") or a link labeled "coverage-model premises" for a pack-procedure claim.
- Source: skill-draft Step 3 requires each pair "WRONG first, then RIGHT" plus "a one-line *why*"; sibling `semantic-differential-testing/references/common-mistakes.md` uses Wrong/Right/Why sections.
- Fix: converted the same eight entries to Wrong/Right/Why sections with concrete wrong examples, section+page locators and verified quotes. The "coverage-model premises" citation (paper does not discuss exclusions) replaced by PICT Constraints "express inherent limitations of the modelled domain".

### F13. references/factors-and-coverage.md:3, :5, :11; references/paired-reduction.md:3; references/pict-operation.md:28 — WARNING — uncited or page-range-only claims
- Text: "the literature supplies coverage distinctions, not a ready target model (pp.2–7)"; fallback-capability rule uncited; "subset, total-tuple and minimum-coverage distinctions (§II)" without page; "Coverage theory measures modeled interactions (pp.2–7)"; "The generator does not execute configurations" uncited.
- Source: Kuhn §II p.2 "test effectiveness is also dependent on the values selected"; §II pp.2-3 Table I 33% simple vs 79% total coverage; §II p.1 "the proportion of t-way combinations of variable settings included in a test set"; PICT Usage "accepts a plain-text model file as an input and produces a set of test cases".
- Fix: cited with section/page and quotes; terminology aligned to the paper's "simple t-way" / "total variable-value" names.

### F14. references/sources.yaml — WARNING — non-format field and inaccurate sections_used
- Text: every entry carried `evidence_fragment` (not in the skill-draft Step 7 format; siblings do not use it); paper entry listed "pp.2,4,5,15; ... Appendix IV" though no inline text cites p.15/Appendix IV; PICT guide omitted Usage, Best-of-N, Parallelism, Output Format, Case Sensitiveness, Conditional Constraints now cited.
- Fix: removed `evidence_fragment`; sections_used rewritten to the sections actually cited. 8 entries, 8 cited URLs, matched both ways.

### F15. Audit checks 1-6 — INFO — no defects
- Frontmatter name matches directory, description 236 chars, third person, has "Use when" trigger; SKILL.md 30 lines; all four local links resolve; no filler phrases found. No change.

## Pinned URLs

None needed. All six GitHub URLs were already raw.githubusercontent.com at full SHA ab76c2548f551fcb46314e58653a1bd1172f3a72 (verified to exist with `gh api repos/microsoft/pict/commits/<sha>`; content fetched at that SHA). The NIST paper URL is a fixed publication-record PDF. The NIST tools page has no immutable URL; sources.yaml records observation date 2026-11-07 and the page's "Updated June 08, 2026".

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/configuration-differential-testing
Skill is valid!
exit=0
$ git diff --check -- plugins/bugfinding/skills/configuration-differential-testing
diffcheck=0
--- cited not in yaml / yaml not cited
(no output: 8 cited URLs, 8 sources.yaml entries, matched both ways)
--- local links
ok references/factors-and-coverage.md
ok references/pict-operation.md
ok references/paired-reduction.md
ok references/common-mistakes.md
--- moving urls
(no output)
--- EOF last 2 bytes: every file ends ".\n" or "\"\n" (exactly one newline)
   30 SKILL.md
   67 references/common-mistakes.md
   29 references/factors-and-coverage.md
   17 references/paired-reduction.md
   32 references/pict-operation.md
   58 references/sources.yaml
```

YAML parses: 8 sources, keys accessed/name/sections_used/type/url. Quote check: every PICT and NIST quote matched as an exact substring of the fetched files (scratchpad script `checkquotes.py`, read-only); the paper quotes were checked by eye against page images page-000..page-006.

## Unverified

- Paper quotes are checked against page images by reading, not by machine match (no text extraction used, per rules).
- PICT command lines in pict-operation.md were not executed (no installed PICT; installs not authorized). They are checked against the parser source only.
- The paper's page numbers are the 15-page NIST preprint's PDF pages, not the journal pagination (ISSE 12(4) 249-261).
