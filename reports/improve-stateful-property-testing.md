# Improve stateful-property-testing: citation and content audit

Skill: `plugins/bugfinding/skills/stateful-property-testing/`
Date: 2026-11-07

## Findings

Hughes paper evidence: re-read page images `page-013.png` to `page-016.png` (PDF pages 14-17; the images carry no printed page numbers, so "p. N" in the skill means PDF page N) in `C:/Users/Q/code/bugfinding-literature/stateful-property-testing/papers/Hughes_2016_QuickCheckHardStuff/pngs/`, produced by paper-reader. Quotes below are from those images.

### F1. SKILL.md:14, model-and-sequences.md:7, common-mistakes.md:6 — WARNING — Hughes case presented without its parallel context
- Text said: create/close/reopen "reached hidden state that a shorter visible-equivalent setup did not", presented as sequential-model guidance; SKILL.md:26 also says "Keep sequential modeling separate from concurrency claims".
- Source says (PDF p. 15): the failing test is a `Prefix:` of open/close/open followed by a `Parallel:` block of three operations; "Three parallel operations are needed because the first makes the dets server busy". The lifecycle point holds: "the first call to open *creates* the file, while the second call opens an *existing* file" and removing the first open and close made the test pass "every single time". URL: https://publications.lib.chalmers.se/records/fulltext/232550/local_232550.pdf
- Fix: state that the reopen prefix was the sequential prefix of a parallel test; add the quote fragment.

### F2. SKILL.md:12, runtime-recipes.md:42 — WARNING — "Start model and system in equivalent states" cited to a file that does not say it
- Text cited `include/rapidcheck/state/Command.h` and the fast-check guide for the matching-initial-state rule.
- Source: Command.h (pinned 2c3c436) only declares `checkPreconditions`, `apply`, `run`, `show`, `nextState`; the fast-check guide does not discuss initial-state agreement. RapidCheck `doc/state.md` "Putting it all together" says "The initial state must obviously match the state of the System Under Test". URL: https://raw.githubusercontent.com/emil-e/rapidcheck/2c3c4365aca21ef4e612768fdc95b1ce8b39a651/doc/state.md
- Fix: cite state.md (Putting it all together) for initial-state agreement with the quote; keep fast-check guide for the "not a carbon copy" model rule with its quote.

### F3. All files — ERROR — moving-branch URLs (`/master/`, `/main/`, `/en/latest/`)
- 16 distinct URL targets (17 sources.yaml entries less the fixed Hughes PDF) used moving branches. Pinned to commits resolved with `gh api repos/<o>/<r>/commits/<branch> --jq .sha`; content re-read at those SHAs (see Pinned URLs).

### F4. runtime-recipes.md:27 — WARNING — Rapid "can stop" understates a test failure
- Text said: "Rapid retries skipped actions and can stop when none is valid".
- Source (statemachine.go @6706a6f, `executeAction`): retries up to `validActionTries  = 100`, then `panic(stopTest(noValidActionsMsg))` with message "can't find a valid (non-skipped) action"; engine.go `checkTB` reports a `stopTest` as `[rapid] failed after %v tests`. Also `checkTB` errors "only generated %v valid tests from %v total" when too few valid tests. URLs: https://raw.githubusercontent.com/flyingmutant/rapid/6706a6fd83736ba24aaf55ef2621fdf00c2c27e8/statemachine.go , .../engine.go
- Fix: say the test fails with that message and that low valid-test counts are reported as errors; both are admissibility evidence.

### F5. runtime-recipes.md:36 — INFO — fail-file version handling stated vaguely
- Text said: "file-format changes can invalidate replay".
- Source (engine.go `checkFailFile`): "ignoring fail file: version %q differs from rapid version %q"; and the failure report prints `-rapid.failfile=%q (or -rapid.seed=%d)`.
- Fix: state that a fail file from a different Rapid version is ignored, and that the failure message prints the reproduce flags to keep.

### F6. common-mistakes.md:11, runtime-recipes.md:38 — INFO — README wording
- README @6706a6f: rapid "lacks coverage-guided feedback and mutations"; "any rapid test can be used as a fuzz target for the standard fuzzer". Text omitted "mutations". Fix: add quote fragment.

### F7. SKILL.md, runtime-recipes.md, common-mistakes.md — ERROR — Hypothesis docs cited at `/en/latest/` with no versioned equivalent
- `https://hypothesis.readthedocs.io/en/hypothesis-python-6.170.15/stateful.html` and `/en/v6.170.15/stateful.html` both returned HTTP 404 (WebFetch), so Read the Docs publishes no per-release path for the current release. Per skill-draft Step 5 fallback, cited the docs source at the release commit instead: `HypothesisWorks/hypothesis` tag `v6.170.15` = 9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2. `reference/api.html` is autodoc (`hypothesis/docs/reference/api.rst` lines 204-222 are `autoclass`/`autofunction`), so its claims now cite the docstrings in `src/hypothesis/stateful.py` and `src/hypothesis/_settings.py` at that SHA. The `#hypothesis.stateful.Bundle` anchor has no meaning on a raw file and was dropped; the section is named in text instead.
- Claims re-verified at that SHA: `initialize` docstring "``@initialize()`` methods may not have preconditions" and "in an arbitrary order"; `Bundle` docstring "Bundles can contain the same value more than once"; `stateful_step_count` "effectively multiplicative with max_examples"; compatibility.rst "function-scoped fixtures run only once for the entire test, not per-input" and "CPython and PyPy 3.11+"; quickstart.rst `pip install hypothesis`; LICENSE.txt MPL 2.0 "except where explicitly noted otherwise".

### F8. common-mistakes.md:9 — INFO — fixture rule is stated in Hypothesis docs for `@given`
- compatibility.rst describes fixtures passed to `@given` tests and the `HealthCheck.function_scoped_fixture` warning; the sentence itself is general ("function-scoped fixtures run only once for the entire test"). Kept the claim, added the exact quote; no change of meaning.

### F9. SKILL.md, model-and-sequences.md, common-mistakes.md — WARNING — load-bearing claims lacked verbatim fragments
- Added quotes retrieved this session: fast-check `if (cmd.check(m)) cmd.run(m, r);` and `if (await cmd.check(m)) await cmd.run(m, r);` (ModelRunner.ts); "should not be a carbon copy of the system" and "`commands` must be called with `{ replayPath: string }`" (model-based-testing.md); RapidCheck "_**always assert all preconditions**_" (rendered as "always assert all preconditions"), "there might be hidden state that we cannot easily replicate", "without even running the actual System Under Test" (state.md); Hughes "a bug in the model" (PDF p. 14) and "two independent descriptions" (PDF p. 17).

### F10. model-and-sequences.md:5 — WARNING — uncited rule
- Text: "Do not perform a target mutation in a precondition just to discover whether the operation is allowed." No citation. RapidCheck state.md: the model lets RapidCheck "generate valid sequences of commands without even running the actual System Under Test", and `checkPreconditions(const Model &s0)` receives only the model (Command.h). Fix: cite both.

### F11. runtime-recipes.md:19 — INFO — fast-check replay example also sets `endOnFailure: true`
- model-based-testing.md "Replay model-based tests" passes `{ seed: 670108017, path: '96:5', endOnFailure: true }` with `replayPath`. Fix: mention the field as part of the emitted replay parameters.

### F12. runtime-recipes.md:3 — WARNING — header said moving sources were inspected
- Replaced with a statement that links are pinned to the commits read on 2026-11-07, naming the fast-check package version 4.10.2 and Hypothesis tag v6.170.15.

Severity totals: ERROR 2 (F3, F7); WARNING 6 (F1, F2, F4, F9, F10, F12); INFO 4 (F5, F6, F8, F11). Claims cut: 0 (every uncited or miscited claim had a primary source that supports it, so each was re-cited instead).

common-mistakes.md: all 9 entries are Wrong-then-Better pairs (house style of `bugfinding-campaign/references/common-mistakes.md`), each now with a why clause and a pinned citation; entry 8 gained an explicit why and entry 10 gained the `replayPath` why quote.

Skill-audit checks 1-6: frontmatter valid (name matches directory, description third person with trigger); SKILL.md 37 lines; reference files under 100 lines (no TOC needed); local links resolve; sibling skills named in routing text all exist under `plugins/bugfinding/skills/`. No ERROR or WARNING found in checks 1-6; no changes made for them.

## Pinned URLs

Commit SHAs resolved with `gh api repos/<o>/<r>/commits/<branch> --jq .sha` on 2026-11-07; every file was re-read at the SHA before citing.

| Repo (branch) | SHA | Files |
|---|---|---|
| dubzzz/fast-check (main, package 4.10.2) | 5ec2e3aceae60eb510b8b967bcb153274f3abad7 | website/docs/advanced/model-based-testing.md; packages/fast-check/src/check/model/ModelRunner.ts; .../commands/CommandsContraints.ts; packages/fast-check/src/arbitrary/commands.ts; packages/fast-check/package.json |
| emil-e/rapidcheck (master) | 2c3c4365aca21ef4e612768fdc95b1ce8b39a651 | doc/state.md; include/rapidcheck/state/Command.h |
| flyingmutant/rapid (master) | 6706a6fd83736ba24aaf55ef2621fdf00c2c27e8 | statemachine.go; engine.go; README.md; go.mod |
| HypothesisWorks/hypothesis (master = tag v6.170.15) | 9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2 | hypothesis/docs/stateful.rst; hypothesis/docs/compatibility.rst; hypothesis/docs/quickstart.rst; hypothesis/src/hypothesis/stateful.py; hypothesis/src/hypothesis/_settings.py; LICENSE.txt |

Replaced moving URLs: 12 distinct (5 fast-check, 2 RapidCheck, 4 Rapid, 1 Hypothesis LICENSE on master) plus 4 Read the Docs `/en/latest/` pages (stateful, reference/api, compatibility, quickstart) mapped to 6 pinned Hypothesis sources. sources.yaml went from 17 to 18 entries (API reference split into stateful.py and _settings.py docstrings). The Hughes PDF URL is an institutional fixed record (HTTP 200, Last-Modified 2022-11-25) and was not changed.

## Validation

```text
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/stateful-property-testing
Skill is valid!
```

Read-only probe (python -I: parse sources.yaml, extract markdown links, resolve local links, match URLs ignoring #fragment, scan for /main/ /master/ /HEAD/ /latest/ /stable/, check final newline):

```text
SKILL.md lines 37 ends_one_nl True
common-mistakes.md lines 11 ends_one_nl True
model-and-sequences.md lines 31 ends_one_nl True
runtime-recipes.md lines 42 ends_one_nl True
sources.yaml ends_one_nl True
sources 18 cited 18
orphan citations []
unused sources []
errors []
```

```text
$ git diff --check -- plugins/bugfinding/skills/stateful-property-testing
(no output) diff-check exit 0
```

All 18 sources.yaml URLs returned HTTP 200 via curl.

Quote probe: fetched each pinned file and tested 45 quote fragments by substring. 44 matched exactly. `lacks coverage-guided feedback and mutations` in Rapid README is split by a source line break ("lacks\ncoverage-guided feedback and mutations"); it renders as one sentence, so the quote stands. `in an arbitrary order` in stateful.py likewise spans a docstring line break. Hughes quotes ("the first call to open *creates* the file", "every single time", "All results are consistent with the model—but the corruption check encountered", "a bug in the model", "two independent descriptions") were checked by reading page images page-013 to page-016 this session, not by text probe.

## Unverified

- No code was executed. The runtime recipes (`go test ... -args -rapid.checks=...`, `pytest path/...`, fast-check runner usage) are checked against source and docs text only; skill-draft Step 6 toolchain verification was not run because the skill ships no code examples beyond shell invocations with placeholders.
- Hughes page numbers are PDF page indices (the page images carry no printed page numbers). Pages 1-13 and 18 were not re-read this session; no edited claim relies on them.
- Hypothesis: Read the Docs has no per-release URL for v6.170.15 (two candidate paths returned 404), so citations point at the docs source files at the release commit, not at rendered pages.
- Rapid and RapidCheck are pinned to branch-head commits, not release tags (Rapid's newest tag v1.3.0 is a different commit, 9bafe07); readers of an older Rapid release should recheck `validActionTries` and the flag text.
