# Improve: correctness-oracles

Skill: `plugins/bugfinding/skills/correctness-oracles/`. Accessed 2026-11-07.

## Findings

### F1. Moving-branch SQLancer URL (ERROR, check 4)
- Where: SKILL.md:8, 25, 27, 37; references/common-mistakes.md:7, 31; references/partial-observations.md:5, 15, 21, 27; references/sources.yaml:3.
- Text: `https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java`.
- Source: `gh api repos/sqlancer/sqlancer/commits/main` -> `a7d60ee450e6a22ca38599c14e984a49773f4745`; fetched the file at that SHA (227 lines; research report described a 206-line snapshot, so the file had changed since research).
- Fix: replace with `https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java` everywhere, and remove partial-observations.md:17 text "The linked source follows a mutable branch", which becomes false once pinned.

### F2. Elle repository URL is a moving page (ERROR, check 4)
- Where: SKILL.md:39; references/partial-observations.md:29; sources.yaml:41.
- Text: `https://github.com/jepsen-io/elle` (rendered default-branch README).
- Source: `gh api repos/jepsen-io/elle/commits/main` -> `4e359e597c52938b0afebb8bc42273914d68a424`; README is `README.markdown` (README.md at that SHA returns 404). Fetched https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/README.markdown, lines 33-35: "Elle is still under active development, and we're not 100% confident in its inference rules yet. Jepsen recommends checking reported anomalies by hand to make sure they're valid."
- Claim check: SKILL.md:39 "recommends checking reported anomalies rather than treating the label as final authority" and partial-observations.md:29 "explicitly recommends checking reported anomalies" match the source. Fix: pin URL, add verbatim fragment "checking reported anomalies by hand".

### F3. NoREC expected-error vs unexpected-error paths under-described (WARNING, check 8 content gap)
- Where: references/partial-observations.md:5 and table row "Sentinel/error path skipped" (line 13).
- Text: treats "sentinel/error path" as one skipped outcome.
- Source (pinned NoRECOracle.java): `countRows`/`extractCounts` return `-1` when `rs == null` or iteration throws `SQLException` (lines 183-192, 207-216); `check` throws `IgnoreMeException` on `-1` (148-150). `SQLQueryAdapter.internalExecuteAndGet` returns `null` only after `checkException` accepts an expected error (pinned SQLQueryAdapter.java lines 155-167, 205-209); an unexpected error is thrown as `AssertionError`, and `check` builds an `errorReproducer` and rethrows it (NoRECOracle.java 142-146). So expected errors are skipped while unexpected errors are reported failures, not skips.
- Fix: state that split in partial-observations.md and add an "Unexpected DBMS error" row.

### F4. SQLite claims verified; no verbatim fragments on load-bearing claims (WARNING, check 3)
- Where: SKILL.md:12, 31, 33; contract-examples.md:19, 21, 34, 36; common-mistakes.md:13, 19, 25.
- Sources fetched 2026-11-07 (sqlite.org publishes no versioned URL; page footers read: pragma.html "last updated on 2026-10-04", lang_conflict.html "2025-11-22", foreignkeys.html "2026-10-25"):
  - https://www.sqlite.org/pragma.html#pragma_foreign_keys: "This pragma is a no-op within a transaction".
  - https://www.sqlite.org/pragma.html#pragma_integrity_check: "PRAGMA integrity_check does not find FOREIGN KEY errors."
  - https://www.sqlite.org/lang_conflict.html ABORT: "changes caused by prior SQL statements within the same transaction are preserved"; FAIL: "does not back out prior changes of the SQL statement that failed".
  - https://www.sqlite.org/foreignkeys.html#fk_enable: "must be enabled separately for each database connection"; "it simply has no effect."
- Claims match. Executed the contract-examples.md SQL with Python sqlite3 (SQLite 3.50.4): ABORT left `[(1,), (2,)]` with transaction active; FAIL left `[(1,), (2,), (3,)]`; `PRAGMA foreign_keys = ON` inside BEGIN left the value `0`.
- Fix: add short verbatim fragments to the load-bearing sentences; record page-updated dates in sources.yaml names.

### F5. FAIL applies only to some constraints; FK violation becomes ABORT (WARNING, content gap)
- Where: contract-examples.md:21; SKILL.md:31.
- Text: "Do not reuse that post-state expectation for FAIL. Its contract can retain changes made before the failure within the statement."
- Source https://www.sqlite.org/lang_conflict.html FAIL: "The FAIL behavior only works for uniqueness, NOT NULL, and CHECK constraints.  A foreign key constraint violation causes an ABORT."
- Fix: add that the effect boundary depends on the constraint kind as well as the selected policy (contract-examples.md).

### F6. "structural checker" mislabels integrity_check (WARNING, accuracy)
- Where: common-mistakes.md:21-25; SKILL.md:27; contract-examples.md:36.
- Text: integrity_check is "a structural checker" asked "a semantic question".
- Source https://www.sqlite.org/pragma.html#pragma_integrity_check lists "UNIQUE, CHECK, and NOT NULL constraint errors" among what it looks for, then "does not find FOREIGN KEY errors."
- Fix: state precisely that integrity_check covers some constraints but not foreign keys (common-mistakes.md entry), keeping the heading's point.

### F7. Deferred foreign keys: mid-transaction FK observation can flag legal state (WARNING, content gap in boundary derivation)
- Where: contract-examples.md "Healthy structure, unchecked relationship".
- Source https://www.sqlite.org/foreignkeys.html#fk_deferred: "Deferred foreign key constraints are not checked until the transaction tries to COMMIT." and "COMMIT will fail as long as foreign key constraints remain in violation." Verified with Python sqlite3 3.50.4: with a DEFERRABLE INITIALLY DEFERRED reference, `PRAGMA foreign_key_check` inside the open transaction returned `[('ch', 1, 'p', 0)]` (NULL child row not reported) while integrity_check returned `ok`, and COMMIT raised "FOREIGN KEY constraint failed".
- Fix: one sentence in contract-examples.md tying the observation point to immediate vs deferred constraints (the skill's existing "promised boundary" step).

### F8. Elle paper section/page citations verified against page images (INFO)
- Read page images page-002.png (printed p.3), page-006.png (p.7), page-011.png (p.12) of C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/pngs/ this session, plus notes.md (paper-reader output, "All 14 PDF page images read directly").
- §3 "DEDUCING DEPENDENCIES" is on p.3: "blind writes to a register “destroy history”". §4.1 (p.3): "We omit predicates for simplicity". §4.3 "Soundness of Elle" starts p.7: "In practice, observations are rarely complete"; "comes close to guaranteeing completeness". §9 "FUTURE WORK & CONCLUSIONS" p.12: "Our approach ignores predicates and deals only in individual objects".
- All existing Elle claims (SKILL.md:8, 21, 37, 45; common-mistakes.md:37; contract-examples.md:42, 44; partial-observations.md:23, 27) match. sources.yaml section names/pages correct. Fix: add verbatim fragments to load-bearing ones.

### F9. arXiv link is the unversioned alias (WARNING, check 4)
- Where: every `https://arxiv.org/abs/2003.10554` link; sources.yaml:33.
- Source: https://arxiv.org/abs/2003.10554 submission history shows only `[v1]`; paper metadata.json `pdf_url` is `https://arxiv.org/pdf/2003.10554v1` (the read PDF).
- Fix: pin to `https://arxiv.org/abs/2003.10554v1`.

### F10. Unused sources.yaml entry (ERROR, check 5)
- Where: sources.yaml:46-51 "How SQLite Is Tested", section "Coverage testing of defensive code"; no inline citation of testing.html anywhere in the skill.
- Fix: rather than delete, use it for F11 (uncited independence claims) and set sections_used to the sections actually cited.

### F11. Uncited independence claims (ERROR, check 1)
- Where: SKILL.md:25 "Prefer a justified abstract model, independently specified invariant or valid relation over a copied production algorithm. A second implementation is one option" (only the NoREC half was cited); partial-observations.md:21 "A checker that calls the same transformation ... may reproduce the defect" (only the NoREC sentence cited).
- Source https://www.sqlite.org/testing.html (footer "last updated on 2026-04-21"): §2 Test Harnesses, SLT runs statements "against both SQLite and several other SQL database engines and verify that they all get the same answers"; §9 Disabled Optimization Tests: "SQLite should always generate exactly the same answer with optimizations enabled and with optimizations disabled".
- Fix: cite §2 for the second-implementation option and §9 for the same-engine relation. No primary source fetched states the copied-algorithm anti-pattern itself; it stays as design guidance grounded by these two examples (listed under Unverified).

### F12. Boundary list and default-setting claims uncited or weakly cited (WARNING, check 1)
- Where: SKILL.md:12 boundary list (operation, statement, transaction ...) uncited; contract-examples.md:34 "defaults also should not be assumed" and "Unsupported builds" had no source text.
- Source: lang_conflict.html ABORT (statement boundary); foreignkeys.html#fk_deferred (transaction boundary); pragma.html#pragma_foreign_keys: "applications should set the foreign key enforcement flag as required by the application and not depend on the default setting"; foreignkeys.html#fk_enable tip: "If the command "PRAGMA foreign_keys" returns no data instead of a single row containing "0" or "1", then the version of SQLite you are using does not support foreign keys".
- Fix: add these citations/fragments.

### F13. Routing names to skills not yet in the repo (INFO, check 7)
- SKILL.md:41 routes to `numerical-oracles`, `resource-complexity-testing`, `liveness-testing`, which are absent from plugins/bugfinding/skills/ today; the foundation skill routes to the same planned names. Plain names, not links, so nothing breaks. Not changed (out of scope to edit the plan).

### F14. common-mistakes.md format (INFO, check 6)
- Every entry is Wrong-first then Better with the reason and a citation inside the Better line, matching the foundation skill (bugfinding-campaign/references/common-mistakes.md uses the same **Wrong:**/**Better:** labels). No structural change.

### F15. Sentinel source wording corrected during edit (INFO, self-check)
- My first edit said the adapter returns `null` "only after" an accepted expected error. Pinned SQLQueryAdapter.java lines 199-200 also return `null` when the driver returns no result set, and NoRECOracle.java lines 190-192/214-216 set `-1` on a failed result read. Corrected SKILL.md:37 and partial-observations.md (paragraph and table row) to list all three sentinel causes.

### Audit checks 1-7 summary
- Frontmatter: name matches directory, description 251 chars, third person, has trigger clause; no unknown fields. Lines: SKILL.md 45/500. Local links resolve. No filler phrases found. Description still matches body (no scope change).

## Pinned URLs

| Before | After |
|---|---|
| https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java | https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java |
| https://github.com/jepsen-io/elle | https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/README.markdown |
| https://arxiv.org/abs/2003.10554 | https://arxiv.org/abs/2003.10554v1 |
| (new) | https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/query/SQLQueryAdapter.java |

sqlite.org pages have no versioned URL; the page "last updated" footer date read on 2026-11-07 is recorded in each sources.yaml `name`.

## Validation

```text
python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/correctness-oracles
Skill is valid!
cited-not-in-sources set()
sources-not-cited set()
local-link/EOF errors []
moving-branch URLs []
git diff --check: clean
   45 plugins/bugfinding/skills/correctness-oracles/SKILL.md
   37 plugins/bugfinding/skills/correctness-oracles/references/common-mistakes.md
   46 plugins/bugfinding/skills/correctness-oracles/references/contract-examples.md
   32 plugins/bugfinding/skills/correctness-oracles/references/partial-observations.md
   60 plugins/bugfinding/skills/correctness-oracles/references/sources.yaml
```

URL probe: all four GitHub/arXiv URLs returned HTTP 200; every sqlite.org anchor cited (fk_basics, fk_deferred, fk_enable, pragma_foreign_key_check, pragma_foreign_keys, pragma_integrity_check, test_harnesses, disabled_optimization_tests) exists as an `id` in the fetched HTML (curl's `-w %{http_code}` printed 000 for sqlite.org with `-L -o /dev/null`, but the bodies were fetched and grepped).

Quote probe: every web-sourced quoted fragment in the skill was found verbatim (whitespace-normalised) in the fetched source text. Elle paper fragments ("destroy history", "observations are rarely complete", "The more recoverable a history is", "Our approach ignores predicates") were checked against page images page-002/006/011, not text.

SQL in contract-examples.md executed with Python sqlite3 3.50.4 (results in F4, F7).

## Unverified

- The anti-pattern "copying the production algorithm gives no independence" (SKILL.md:25, common-mistakes.md "Making the checker repeat the implementation", partial-observations.md:23) has no primary source stating it directly. It is kept as design guidance, now cited to SQLite's SLT (separate engines) and optimization-disabled reruns (different path) as examples of where independence comes from.
- SQLite behavior was executed on 3.50.4 only; other builds (e.g. SQLITE_DEFAULT_FOREIGN_KEYS, OMIT_FOREIGN_KEY) not executed.
- No behavioral forward-test of the skill was run.
