# Improve metamorphic-testing: citation and content audit

Target: `plugins/bugfinding/skills/metamorphic-testing/` (SKILL.md + references/). Accessed 2026-11-07.

## Findings

Paper verification basis: TLP paper-reader page images at `C:/Users/Q/code/bugfinding-literature/metamorphic-testing/papers/Rigger_2020_QueryPartitioning/pngs/` re-read this session (page-001..006, 010, 011, 017..020, 024, 025). Section map from printed headings: §2 BACKGROUND starts p.3, §3 APPROACH starts p.6, §4 SELECTED BUGS starts p.12, §5.2 p.19, §5.3 p.20, §5.4 p.21, §6 DISCUSSION p.25, §7 RELATED WORK p.26. The "Soundness" paragraph on p.18 belongs to §5.1 (precedes §5.2 on p.19).

### F1 — SKILL.md:8 — ERROR — wrong section cited
- Text: agreement cannot establish ground truth ... `[Query Partitioning, §§3 and 6]`.
- Source: §3 (Approach) does not say this. §2 p.4: metamorphic oracles "cannot provide a ground truth (i.e., since the output based on which the new test case is generated might be incorrect)"; §6 p.25: "it cannot establish a ground truth (i.e., an operator or function might be consistently behave incorrectly". https://www.manuelrigger.at/preprints/TLP.pdf
- Fix: cite §§2 and 6 and add quote fragment "cannot establish a ground truth".

### F2 — SKILL.md:30 — ERROR — wrong section cited
- Text: TLP paper limits its model and distinguishes dialect-dependent behavior `[§§4 and 6]`.
- Source: §4 is "SELECTED BUGS" (examples only). Limits are §6 p.25 "Limitations": "Our testing does not apply to transactions, window functions, sequences, and non-deterministic functions." The dialect dispute (MySQL empty string vs DECIMAL, reports closed as false positives) is the §5.1 "Soundness" paragraph, p.18.
- Fix: cite §§5.1 and 6 with the limitations quote.

### F3 — references/relation-design.md:15 — WARNING — imprecise section and paraphrase
- Text: "Adding clauses indiscriminately can suppress the optimization ... complementary clause-specific behavior rather than coverage alone explaining detection `[§§5–6]`".
- Source: §5.3 p.20: "the GROUP BY oracle might overlook bugs in the handling of WHERE since an optimization might no longer be applicable"; p.21: coverage range only 55.3%-55.9% yet "each test oracle found unique bugs", and "coverage information provides only limited insights for DBMS". §6 adds nothing to this claim.
- Fix: cite §5.3 with quote fragments.

### F4 — all SQLancer links (SKILL.md:18,20,22,26,28; relation-design.md:17; common-mistakes.md:8,10,11; sqlancer-operation.md:3,11,13,15,17; worked-relations.md:11,25; sources.yaml) — ERROR — moving `/main/` URLs
- Text: `https://raw.githubusercontent.com/sqlancer/sqlancer/main/...` (5 distinct files).
- Source: `gh api repos/sqlancer/sqlancer/commits/main --jq .sha` → `a7d60ee450e6a22ca38599c14e984a49773f4745` (committer date 2026-11-05). All five files fetched at that SHA. TLPWhereOracle.java is now 206 lines and ComparatorHelper.java 197 lines (research recorded 187/185 on `main`), confirming the moving link already drifted.
- Fix: every SQLancer link and sources.yaml url pinned to that SHA; line ranges added to link text where the claim depends on specific code (raw files do not support #L anchors).

### F5 — SKILL.md:18, relation-design.md:17 — INFO — producer claims verified at pinned SHA
- TLPWhereOracle.check (lines 141-195): original query with `setWhereClause(null)` (153-155); `predicate`, `negatedPredicate`, `isNullPredicate` variants (171-178); combined via `getCombinedResultSet` with UNION ALL unless ORDER BY (183-184; ComparatorHelper 148-152); `TLPWhereReproducer` retains all four query strings (191-192, 44-58). Claims hold. Added line ranges.

### F6 — SKILL.md:20,22; common-mistakes.md:8,10; worked-relations.md:11 — INFO/WARNING — observer claims verified, one omission
- ComparatorHelper at pinned SHA: `getResultSetFirstColumnAsString` reads `result.getString(1)` (61), strips trailing `.0+` (63), throws `IgnoreMeException` on null result (57-58) or expected error (75-76); `assumeResultSetsAreEqual` checks size (91) then `HashSet` equality (108-112), skipped entirely when `validateResultSizeOnly` is set (111-112).
- Existing text omitted the trailing-zero normalization and the size-only option, both of which further weaken the observation. WARNING; fix: name both in SKILL.md:22 with line refs.

### F7 — SKILL.md:26,28; sqlancer-operation.md:13; worked-relations.md:25; common-mistakes.md:11 — WARNING — README overstated
- Text (SKILL.md:28): "shrinking only the final query can remove the required database state ([SQLancer reduction])".
- Source (README at pinned SHA, line 39 "Logs"): the bug `.log` holds "the statements to reproduce the bug ... including only the last query that was executed along with the other statements to set up the database state"; line 41 "Reducing bugs": manual reduction removes "a statement or feature at a time" and for TLP/NoREC "this would require checking that both queries still produce a different result". The README does not say shrinking only the final query removes state.
- Fix: re-attribute — README supports retaining setup statements and re-checking that the related queries still disagree; the "regenerate variants and re-establish preconditions" instruction is kept as this pack's guidance, with the README cited only for what it says.

### F8 — SKILL.md:12,14,18,22 — ERROR — uncited normative sentences / missing load-bearing quotes
- SKILL.md:12 "Explain what implementation behavior the transformation changes" had no source. Paper §1 p.2: "it is crucial to select one that stresses the DBMS and its query optimizer in different ways". Fix: cited with that quote.
- SKILL.md:14 epsilon guidance cited only SQLite aggregates. Paper §3 p.12: "we also assume SUM() and AVG() to be commutative, although the processing order matters for floating-point numbers" then compare "using an epsilon". Fix: cite §3 for the epsilon being an assumption; added SQLite verbatim fragments "except that with BETWEEN, the x expression is only evaluated once" (lang_expr §6), "is evaluated just once" (§7), "an integer overflow occurs at any point during the computation" and sum NULL vs total 0.0 (lang_aggfunc §3).
- SKILL.md:18 "Reuse the target's existing representation, formatter" had no source. Paper §2 p.4: "any database generator and query generator that provides control over the format of the queries generated can be used". Fix: cited.
- SKILL.md:22 added verbatim SELECT fragments: "works the same way as UNION ALL, except that duplicate rows are removed" (§3) and "the order in which the rows are returned is undefined" (§4). https://www.sqlite.org/lang_select.html

### F9 — SKILL.md:30 — WARNING — false-positive claim attribution
- Paper §5.1 p.18: "the MySQL bug verifiers considered 3 of our bug reports as false positives. For example ..." (empty STRING not a valid DECIMAL). Only one example is the DECIMAL case. Fix text says "three ... false positives, one on whether an empty string is a valid DECIMAL".

### F10 — references/relation-design.md:9,10,11,13 — WARNING — paraphrases replaced by source text, sections added
- :9 now quotes CASE "lazy, or short-circuit, evaluation" (lang_expr §7).
- :10 "a function's determinism claim needs actual implementation support" paraphrased; deterministic.html §1: changes()/last_insert_rowid() "depend on prior SQL statements"; sqlite3_version() "can change when SQLite is upgraded"; §4: a non-deterministic function tagged SQLITE_DETERMINISTIC used in an index means "the associated index may become corrupt". Fix: stated those facts with §§1 and 4.
- :11 "TLP changes composition with the tested SQL feature" made concrete from §3 p.7 ("For both the WHERE and HAVING test oracles, ⋄ corresponds to the multiset addition"; DISTINCT/GROUP BY set union; aggregate partitions "correspond to intermediate values").
- :13 added lang_aggfunc facts: avg() "computed as total()/count()" (§3) and aggregate inputs "occur in an arbitrary order" without ORDER BY (§1); floating point quote "Floating point values are approximate." (floatingpoint §1).

### F11 — references/common-mistakes.md (all 8 rows) — ERROR — not WRONG-first/RIGHT/why pairs
- Text: a two-column "Misleading shortcut | Correction" table with no why line and no concrete wrong example; skill-draft Step 3 requires "the wrong code, the right code, and a one-line *why*".
- Fix applied: same 8 entries rewritten as `## heading` + **Wrong:** (concrete SQL/action) + **Right:** + **Why:** with a cited verbatim fragment each. No entry added or dropped. Quotes used: lang_expr §6, TLP §3 p.6 "one predicate p, one predicate NOT p, and one predicate p IS NULL", lang_select §3, ComparatorHelper lines, lang_aggfunc §3, floatingpoint §1, README Reducing bugs, TLP §6 p.25.

### F12 — references/worked-relations.md:19 — WARNING — gap: no correct aggregate relation given
- Text said only not to compare average-of-averages, without the valid alternative.
- Source: TLP §3 p.11: AVG partitions compute "(SUM(Qp), COUNT(Qp))", "composed by dividing the sum of the first tuple values by the sum of the second"; COUNT partitions "are then summed up using the SUM() aggregate function"; DuckDB example: "the addition of 9223372036854775807 and 2 in SUM() overflowed" while DuckDB "computed the correct result for the original query". lang_aggfunc §3: avg() "computed as total()/count()".
- Fix applied: added the (SUM, COUNT) recomposition and the overflow example, with quotes; sections added to other worked-relations citations (§3 pp.7–11; SELECT §4 quote; BETWEEN quote).

### F13 — references/worked-relations.md:23 — WARNING — unexplained project jargon
- Text: "no universal MOO transformation is asserted". "MOO" is target-specific jargon from the research calibration target; nothing in the skill defines it.
- Fix applied: "no universal identity-preserving transformation is asserted".

### F14 — references/sqlancer-operation.md:3,11,13,15,17 — WARNING — paraphrases, one misstatement
- :3 "version-sensitive backends ... bounded execution" made concrete from README: `--num-tries`/`--timeout-seconds`, "it executes infinitely"; embedded DBMS binaries are JAR dependencies; "supports only a previous *release* version"; other versions give "various false alarms".
- :11 quote "need to precede the name of the DBMS to be tested"; factory lines 89–100.
- :13 ERROR-level misstatement: "reduced reproducer logs" — README never says the `.log` is reduced; it says it holds setup statements and "only the last query that was executed". Since the pinned TLPWhereOracle reproducer holds all four query strings (lines 44–58), the text now tells the user to check the retained log contains every related query. Fix applied.
- :17 "Source/main ... checked" replaced with the pinned commit.

### F15 — references/sources.yaml — WARNING — sections_used inaccurate
- Paper entry listed "Sections 3 and 6" and page images; the skill now cites §§1, 2, 3, 5.1, 5.3, 6. SQLite entries lacked section numbers; SQLancer entries lacked line ranges and used `/main/`.
- Fix applied: every entry's sections_used rewritten to the sections/lines actually cited; SQLite names record the page "last updated" stamp read (sqlite.org publishes no versioned doc URL; SQLite 3.54.1 was the release shown on the home page); SQLancer urls pinned.

### F16 — SKILL.md:14 — INFO — routes to `numerical-oracles`, which does not exist yet in plugins/bugfinding/skills/
- The foundation `bugfinding-campaign` routes to it too; another session is drafting pack skills. Not changed.

## Pinned URLs

Commit `a7d60ee450e6a22ca38599c14e984a49773f4745` (sqlancer/sqlancer, resolved from `main` 2026-11-07), content fetched at that SHA before citing:
- https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/TLPWhereOracle.java
- https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java
- https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md
- https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/sqlite3/SQLite3OracleFactory.java
- https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/LICENSE.md

SQLite pages (lang_expr, lang_select, lang_aggfunc, deterministic, floatingpoint) fetched 2026-11-07 with curl and converted to text for verbatim checking; no versioned URL exists, so the page update stamp is recorded in sources.yaml names.

## Validation

Raw output, run from repository root:

```text
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/metamorphic-testing
Skill is valid!

$ python -I - (read-only probe: sources.yaml fields; inline URLs vs sources.yaml ignoring #fragment; local links; moving-branch strings; trailing newline)
plugins\bugfinding\skills\metamorphic-testing\SKILL.md 32 lines
plugins\bugfinding\skills\metamorphic-testing\references\common-mistakes.md 67 lines
plugins\bugfinding\skills\metamorphic-testing\references\relation-design.md 19 lines
plugins\bugfinding\skills\metamorphic-testing\references\sqlancer-operation.md 17 lines
plugins\bugfinding\skills\metamorphic-testing\references\worked-relations.md 25 lines
cited-not-in-yaml []
yaml-not-cited []
errors []

$ git diff --check -- plugins/bugfinding/skills/metamorphic-testing
diff-check exit 0
```

Verbatim-quote probe: every SQLite and SQLancer README fragment added this session was string-matched (whitespace-normalized) against the fetched text; all 17 returned True. Paper fragments were checked by eye against the page images listed above. Paper URL https://www.manuelrigger.at/preprints/TLP.pdf returned HTTP 200.

Skill-audit checks 1-6: frontmatter name matches directory, description third person with trigger clause, SKILL.md 32 lines, all local links resolve, no filler phrases found. No ERROR remains.

## Unverified

- Fetch method: sources were retrieved with curl (raw HTML/source) and read as text rather than through WebFetch, so quotes could be string-matched exactly. The paper was not re-downloaded; its claims rest on the existing paper-reader page images, re-read this session.
- Whether SQLancer's `TLPWhereReproducer` output (four query strings) is what lands in the bug `.log`: the class holds them, but I did not read `AbstractComparisonReproducer` or the logger. The skill text tells the user to check the log rather than asserting either way.
- `numerical-oracles` sibling skill does not exist yet (F16).
- No command or SQL in the skill was executed.
