# Improve bounded-model-checking

Skill: `plugins/bugfinding/skills/bounded-model-checking/`. Accessed 2026-11-07.

## Findings

Sources were fetched with curl at the already-pinned SHAs (cbmc `826c1c739051aa1c2dd8846282e12691db1cee35`, kani `94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca`) into the session scratchpad; quotes below come from those bytes.

1. `references/tool-recipes.md:13` — ERROR. Text: "coverage and explicit unwinding assertions are incompatible in that manual ([assumptions](.../modeling-assumptions.md))". The assumptions page says nothing about that incompatibility. The man page says `--unwinding-assertions` "cannot be used with --cover" ([cbmc.1](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/man/cbmc.1)), and the CBMC frontend exits with a usage error: "--cover and --unwinding-assertions must not be given together", and otherwise warns "unwinding-assertions will be defaulted to false" ([cbmc_parse_options.cpp](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/cbmc/cbmc_parse_options.cpp)). Fix: re-cite to man page + source, state usage-error behaviour.
2. `SKILL.md:20`, `references/tool-recipes.md:10,22` — WARNING (gap). Skill says "Retain completeness checks" but never says that in the pinned source unwinding assertions are on by default (standard checks, 6.0+) and are turned off by `--no-unwinding-assertions` / `--no-standard-checks`. CBMC: `set_default_analysis_flags` "Checks enabled by default in v6.0+" sets unwinding-assertions unless already set ([cbmc_parse_options.cpp](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/cbmc/cbmc_parse_options.cpp)); JBMC sets it to `isset("unwinding-assertions") || !isset("no-unwinding-assertions")` ([jbmc_parse_options.cpp](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)). Fix: name the disabling flags in SKILL.md and tool-recipes.
3. `references/counterexamples-and-replay.md:9`, `references/common-mistakes.md:9` — WARNING (gap). Partial-loop text omits the unwinding guide's qualifier: with `--unwinding-assertions` also on, a trace that "does not include a report of a violated unwinding assertion" is "not impacted by insufficient loop unwinding" ([cbmc-unwinding.md](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). Fix: add the qualifier in counterexamples-and-replay.
4. `references/tool-recipes.md:27` — WARNING (gap). "Inspect ... exception properties" without the manual's fact that `--throw-runtime-exceptions` is needed "To have JBMC reliably notify about all uncaught exceptions" ([jbmc-user-manual.md, Exceptions](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/jbmc-user-manual.md)). Fix: add cited sentence.
5. Exit codes (`tool-recipes.md:43`), license four conditions (`:15`), JBMC README release/develop (`:25`), `--java-threading` → `allow-pointer-unsoundness` (`:27`), stub generation (`SKILL.md:12`, `bounds-and-models.md:21`), backjump 101 and `--show-loops`/`--unwindset` (`bounds-and-models.md:9`), assumptions non-retroactive / vacuous / no universal quantification (`bounds-and-models.md:15`), `--arch` defaults to host (`SKILL.md:14`) — INFO, verified against the fetched bytes; quotes added where load-bearing.
6. `SKILL.md:8` — WARNING. Text cites "CBMC paper, pp.169-171" for "converts program constraints and a negated property into a solver query; adequate unwinding and model assumptions delimit its conclusion". Page images (paper-reader pngs, `C:/Users/Q/code/bugfinding-literature/bounded-model-checking/papers/Clarke_2004_ToolCheckingANSI/pngs/page-001..003.png`, read this session) show on printed p.170: "we convert C ∧ ¬P into CNF" and unwinding assertions "assert that the unwinding bound is actually large enough". Nothing on pp.169-171 says "model assumptions delimit its conclusion". Fix: narrow page to p.170, quote both fragments, drop the unsupported "model assumptions" clause from the paper-cited sentence.
7. `SKILL.md:30`, `references/counterexamples-and-replay.md:3` — WARNING. Text: "the reported failure location can be downstream of the fault ([p.171])" / "because the failure line need not reveal the cause". Printed p.171 says the GUI allows stepping through a trace "also backward, giving the user the ability to determine more easily the causes of the error". The paper does not state the failure location is downstream of the fault. Fix: restate as the paper's words with quote.
8. `SKILL.md:20` — WARNING (gap). No primary statement that a bounded result depends on passing unwinding assertions. Kani soundness: "Verification results are sound only if all unwinding assertions pass." ([soundness.md, Bounded verification](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/soundness.md)). Fix: add quote.
9. `SKILL.md:18` — WARNING (gap). Reach check only names CBMC `--cover assume`; Kani's documented over-constraint check is the coverage report: "Check the coverage report using `--coverage -Z source-coverage`" and less than 100% "it's usually because you've assumed too much" ([tutorial-real-code.md, Your first proof](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)). Kani results also say an unreachable or unsatisfiable cover "may indicate an incomplete proof" ([verification-results.md, Cover property results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). Fix: add both.
10. `references/tool-recipes.md:37` — INFO. "Harness-specific/default/global override semantics differ" is vague; tutorial: `--default-unwind x` applies to every harness that "**does not** have an explicit bound", while `--unwind` overrides "only when running a specific harness"; also `break`/`continue` loops can need "two more" or "three more" ([tutorial-loop-unwinding.md](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)). Fix: state precisely.
11. `references/bounds-and-models.md:23` — INFO (gap). Kani soundness caveats omitted: object bits default 16 with "incorrect wrapping behavior" beyond `2^N` objects, and `--restrict-vtable` "is a known soundness issue"; valid-value/uninit checks are opt-in unstable ([soundness.md](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/soundness.md)). Fix: add one cited sentence.
12. `references/common-mistakes.md` whole file — ERROR (check 6). Entries are a two-column table with no separate one-line why; house style (transactional-history-testing) and skill-draft Step 3 require WRONG-first-then-RIGHT pairs with a one-line why. Fix: convert each row to `## title / **Wrong:** / **Right:** (cited, quoted) / **Why:**`, keeping the same eight entries.
13. Playback (`counterexamples-and-replay.md:16-20`), results/JSON `started_at` (`:24`), install platforms and versioned install (`tool-recipes.md:39`), README harness/license, Kani sequential-only/aliasing/inline asm (`bounds-and-models.md:23`), real-code "follow your testing"/no I/O (`SKILL.md:12`) — INFO, verified; quotes added.

All fixes in findings 1-12 were applied with targeted Edits. Additional quote-only edits (no claim change) in `SKILL.md:12,14`, `bounds-and-models.md:7,9,11,15`, `counterexamples-and-replay.md:13,20,24`, `tool-recipes.md:15,19,25,37,39,43`. `references/sources.yaml`: new entry for `src/cbmc/cbmc_parse_options.cpp`; `sections_used` corrected for CBMC manual, unwinding guide, JBMC manual (dropped unused "Loop unwinding"), JBMC frontend (dropped unused "frontend help"), exit codes, Kani real-code, loop, results, soundness, install, and the paper (now §2.1 p.170 and §3 p.171 only). Claims cut: 1 (the paper-attributed "model assumptions delimit its conclusion" in `SKILL.md:8`, kept only as uncited skill policy pointing to the bounds section) plus the overstated "failure location can be downstream of the fault" reading (replaced by the paper's words).

Mechanical quote check: a scratchpad script compared every double-quoted fragment of 8+ chars in the skill against the fetched source bytes (whitespace, markdown links, `**`, troff escapes and `//` comment breaks normalized). All matched except: the three TACAS2004 fragments (source is page images, verified visually on page-002.png / page-003.png this session) and `the verified target` (a heading label for the wrong claim, not a source quote).

## Pinned URLs

No moving URLs existed before; every raw GitHub link already used a full 40-hex SHA (cbmc `826c1c739051aa1c2dd8846282e12691db1cee35`, kani `94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca`), and each fetched successfully at that SHA this session. One new pinned URL was added: `https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/src/cbmc/cbmc_parse_options.cpp` (fetched at that SHA). The paper URL `https://www.kroening.com/papers/tacas2004.pdf` is an author-hosted PDF with no versioned alternative; it was fetched (675779 bytes, same size the research report recorded).

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/bounded-model-checking
Skill is valid!
exit=0
--- cited not in yaml / yaml not cited (comm cols 1 and 2):
--- moving urls:
--- local links:
OK references/bounds-and-models.md
OK references/tool-recipes.md
OK references/counterexamples-and-replay.md
OK references/common-mistakes.md
--- diff check:
rc=0
--- line counts/eof:
SKILL.md lines=32 last2=.\n
references/bounds-and-models.md lines=25 last2=.\n
references/common-mistakes.md lines=65 last2=.\n
references/counterexamples-and-replay.md lines=26 last2=.\n
references/sources.yaml lines=120 last2="\n
references/tool-recipes.md lines=45 last2=.\n
```

Skill-audit checks 1-6: frontmatter name matches directory, description is third-person what+when and matches body (CBMC, JBMC, Kani, bounds, vacuity, playback); SKILL.md 32 lines; no filler phrases found; all local links resolve. No ERROR left.

## Unverified

- No tool was executed (no CBMC/JBMC/Kani installed or run, per scope). Flag behaviour is stated from the pinned docs and source only; whether `cbmc --cover assume` on a released 6.x binary prints the warning was read from source, not observed.
- `sources.yaml` keeps the pre-existing extra field `evidence_fragment` on each entry (not in the skill-draft schema, but not forbidden); left as is.
