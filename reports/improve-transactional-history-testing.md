# Improve transactional-history-testing

Scope: `plugins/bugfinding/skills/transactional-history-testing/` (SKILL.md + references/).

## Findings

Sources fetched this session at pinned SHAs into
`C:/Users/Q/AppData/Local/Temp/claude/C--Users-Q-code-computational-bugfinding-skills-plugin/60a7bbfd-6621-4126-b3b4-02fa9ba90204/scratchpad/thtsrc/`.

### F1 ERROR — moving-branch URLs everywhere
- Where: SKILL.md:12,14,18,20,26; references/common-mistakes.md:5-11; elle-operation.md:5,7,9,19,23,25,27; history-and-boundaries.md:3,12,14,16,18; observable-dependencies.md:13,17,21; sources.yaml (10 entries).
- Text: `raw.githubusercontent.com/<org>/<repo>/main|master/...`.
- Source: skill-draft Step 5 forbids moving aliases. Resolved SHAs (gh api, 2026-11-07): jepsen-io/elle main = 4e359e597c52938b0afebb8bc42273914d68a424; jepsen-io/history main = 61d2776c889ad84f7c6922977cf05e8f11970402; ligurio/elle-cli master = 3c2504815945cd4ab1b5cc0142d2fe206e1ee285; jepsen-io/jepsen main = 6766ba09682bcb668d44c025e687dd8b1616e8a2. Content read at those SHAs.
- Fix: replace every link and sources.yaml url with the SHA permalink.

### F2 WARNING — CLI exit-code statement incomplete
- Where: SKILL.md:26, elle-operation.md:23, common-mistakes.md:8.
- Text: "exit zero also covers unknown-only output or help without analysis".
- Source: cli.clj@3c25048 lines 247-249 (nil model or `--help` prints usage then `(System/exit 0)`), 251 (`doseq [filepath arguments]` — zero file arguments analyse nothing, then line 267 exits 0), 267 `(System/exit ({true 1 false 0} (lazy-contains? (vals @results) false)))` (exit 1 only when some result is `false`), 238-241 (option errors also `(System/exit 1)`), 269-272 (exceptions, incl. missing file at 252-253, exit 255). https://raw.githubusercontent.com/ligurio/elle-cli/3c2504815945cd4ab1b5cc0142d2fe206e1ee285/src/elle_cli/cli.clj
- Fix: name the no-file case and that exit 1 is shared by option-parse errors.

### F3 WARNING — CLI default model omitted
- Where: elle-operation.md:11-19.
- Text: example passes `--consistency-models serializable`; nothing says what happens without it.
- Source: cli.clj@3c25048 lines 123-126: `:default [:strict-serializable]`; lines 127-130 `--anomalies` `:default [:G0]`.
- Fix: one sentence that omitting the flag checks strict serializability, which adds realtime constraints a serializable-only contract does not promise.

### F4 ERROR — rendering requirement cited to a page that does not say it
- Where: elle-operation.md:7 ("optional graph rendering needs its fitting environment", cited to CLI README).
- Source: CLI README@3c25048 has no Graphviz requirement (grep for graphviz/dot: only plot option text). Elle README@4e359e5 line 41: "First, you'll need a copy of Graphviz installed." https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/README.markdown
- Fix: cite Elle README Demo for the Graphviz requirement; add Elle README to sources.yaml. Also cite Elle README Usage for the non-JVM file/stream route ("write your history to a file or stream").

### F5 WARNING — `true` verdict scope not stated (gap exposed by source)
- Where: elle-operation.md:21-25, SKILL.md:24-26.
- Source: txn.clj@4e359e5 `result-map` lines 1003-1030: `reportable` is `select-keys` of anomalies over the prohibited set for the selected models, and `(if (empty? reportable) {:valid? true} ...)` — anomalies not prohibited by the selected models are dropped. `unknown-anomaly-types` (650-654) = `:empty-transaction-graph`, `:cycle-search-timeout`. Elle README@4e359e5 Completeness: "Elle is not complete: it may fail to identify anomalies which were present in the system under test."
- Fix: state that `true` means no anomaly prohibited by the selected models was found, not that the model holds; name empty-graph as an unknown class.

### F6 INFO — verified claims (no change beyond pin/quote)
- history README@61d2776 Operation Structure/Semantics: `:info` "the operation either may or may not have completed"; `:fail` "*must* have no logical effect on the system"; crashed process "can never invoke an operation again". Matches SKILL.md:12, history-and-boundaries.md:3-12.
- list_append.clj@4e359e5 verify-mop-types 40-59, verify-unique-appends 61-80 throw `{:valid? :unknown ...}`; preprocess 582-597 calls both. Matches history-and-boundaries.md:14,18.
- rw_register.clj@4e359e5 initial-state-version-graphs 184-188 "We assume the initial state of every key is `nil`"; check 909-960 documents `:transaction-order` and the WARNING over `:sequential-keys?`, `:linearizable-keys?`, `:wfr-keys?`. CLI opts (cli.clj 99-170) have no transaction-order flag. Matches observable-dependencies.md:17, elle-operation.md:9.
- jepsen CHANGELOG@6766ba0 0.3.15: "Elle 0.2.8 fixes a major correctness bug which caused `rw-register` workloads to incorrectly infer cyclic version orders". Matches elle-operation.md:9.
- txn.clj@4e359e5 wr-txns 1068-1110 options `:key-dist` (exponential/zipf/uniform), `:key-count`, `:min-txn-length`, `:max-txn-length`, `:max-writes-per-key`. Matches SKILL.md:20, observable-dependencies.md:21.
- cli project.clj@3c25048 declares elle-cli 0.1.11, `[elle "0.2.8"]`, `[jepsen "0.3.11"]`, license "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"; elle project.clj@4e359e5 0.2.9-SNAPSHOT, same license, `--release 21`. CLI README@3c25048 Requirements: "Java 21 or later"; Usage `lein deps`/`lein uberjar`. Matches elle-operation.md:5-7.

### F7 INFO — key lifetime claim uncited
- Where: SKILL.md:18 "short/long key lifetimes" carries only the paper/model citation.
- Source: jepsen CHANGELOG@6766ba0 0.3.12 New Features: "Now we generate a variety of short-lived and long-lived keys in a single test."
- Fix: cite changelog 0.3.12 on SKILL.md:20 generator sentence.

### F8 INFO — Elle main equals v0.2.8 code, which elle-cli 0.1.11 bundles
- Source: `gh api repos/jepsen-io/elle/compare/2843344620c7d0653eef1c20728aa8580a05f505...4e359e597c52938b0afebb8bc42273914d68a424` → ahead_by 1, files `["project.clj"]` (v0.2.8 tag = 2843344). cli project.clj@3c25048 `[elle "0.2.8"]`.
- Fix: one sentence in elle-operation.md so the reader knows the cited source matches the CLI-bundled library, citing the compare URL.

### F9 WARNING — paper claims vs page images (Kingsbury & Alvaro 2020, pngs read this session: page-002, -006, -007, -008, -011 = printed pp.3,7,8,9,12)
- SKILL.md:8 "more transactions cannot recover information never observed (§3)": §3 (p.3) does not say this; it says "the version resulting from a blind write carries no information about the previous version" and that blind writes "destroy history". Fix: replace the sentence with the §3 statement and quote.
- SKILL.md:30 "a cycle does not establish root cause or durability loss ([Elle, §6])": §6 (p.9) says witnesses explain "why it implies a contradiction"; Theorem 1 (§4.3.2, p.8) scopes a cycle to phenomena in "every clean interpretation". Root cause is not in §6. Fix: cite §§4.3.2 and 6 for what a cycle shows, keep root-cause routing as instruction.
- Predicate exclusion: §9 (p.12) "Our approach ignores predicates and deals only in individual objects"; §4.1 (p.3) "We omit predicates for simplicity". Verified; add quote at observable-dependencies.md:19.
- §5 (pp.8-9): §5.1 process and real-time dependencies, §5.2 version dependencies incl. initial version and exposed metadata. Verified for SKILL.md:18, observable-dependencies.md:13.
- sources.yaml sections_used listed images 3,8,9,12 and omitted §4.1/§4.3.2 actually used. Fix sections_used.

### F11 INFO — added paper citations checked on page images
- §7 (p.10, page-009.png): "When a client thread times out while committing a transaction ... Jepsen spawns a new logical process for that thread to execute." Added to history-and-boundaries.md (quoted only the verified clause; an earlier draft wording "rather than treating as aborted" was not in the paper and was removed before finishing).
- §6.1 (p.9): "Duplicate writes can occur when a client or database retries an append operation". Added to history-and-boundaries.md retry control.
- §7 (p.10): "fewer writes per object stresses codepaths involved in the creation of fresh database objects, and more writes per object allows the detection of anomalies over longer time periods". Available for observable-dependencies.md:21.

### F10 INFO — jepsen.io model pages (fetched 2026-11-07, no versioned URL)
- serializable: "it does not impose any real-time, or even per-process constraints"; "a process can fail to observe its own prior writes"; serializability "may act on predicates". strong-serializable: "if operation A completes before operation B begins, then A should appear to precede B". Verified SKILL.md:24, observable-dependencies.md:15, common-mistakes.md:7. Kept exact URL + accessed date (no immutable alternative).

### F12 ERROR — common-mistakes.md not in WRONG/RIGHT/why form
- Where: references/common-mistakes.md:3-12 (two-column table "Misleading shortcut | Correction", no why line).
- Source: skill-draft Step 3 requires WRONG first, then RIGHT, plus a one-line why.
- Fix: converted the same eight entries to `## heading` / **Wrong:** / **Right:** / **Why:** with pinned citations and verbatim fragments; no new mistakes added. Closing routing paragraph kept.

### F13 WARNING — vague link text without section
- Where: every inline source link ("[CLI source]", "[register options]", "[history]" etc.).
- Fix: link text now names the file plus function/section (e.g. `[cli.clj `-main`]`, `[jepsen.history README, Operation Semantics]`), matching `([Elle §4.3](...))` style.

### Fixes applied (summary)
- SKILL.md: lines 8, 12, 14, 18, 20, 24, 26, 30 edited (pins, quotes, F2/F5/F7/F9 content).
- history-and-boundaries.md: lines 3-18 (pins, outcome-table quotes, §7 timeout process, §6.1 retry duplicate writes, validation error map).
- observable-dependencies.md: lines 13-21 (pins, register docstring scope, `:strong-session-serializable` mapping + process graph, `:transaction-order` docstring quote and warning scope, predicate scope quotes, §7 writes-per-object).
- elle-operation.md: lines 5-9, 19-27 (F2, F3, F4, F5, F8).
- common-mistakes.md: F12.
- sources.yaml: all urls pinned; added Elle README and Elle compare entries; sections_used corrected; 15 entries.
- Claims cut/replaced: SKILL.md:8 "more transactions cannot recover information never observed" (not in §3) replaced by §3 text; elle-operation.md:7 "optional graph rendering needs its fitting environment" (not in cited CLI README) replaced by Elle README Graphviz quote; SKILL.md:30 §6 root-cause attribution re-scoped to §4.3.2/§6.

## Pinned URLs

| Before | After |
|---|---|
| jepsen-io/elle/main/{src/elle/list_append.clj, rw_register.clj, txn.clj, consistency_model.clj, project.clj} | jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/... |
| jepsen-io/history/main/README.md | jepsen-io/history/61d2776c889ad84f7c6922977cf05e8f11970402/README.md |
| ligurio/elle-cli/master/{src/elle_cli/cli.clj, project.clj, README.md} | ligurio/elle-cli/3c2504815945cd4ab1b5cc0142d2fe206e1ee285/... |
| jepsen-io/jepsen/main/jepsen/CHANGELOG.md | jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md |
| arxiv.org/abs/2003.10554 | arxiv.org/abs/2003.10554v1 (WebFetch: only v1 exists, 23 Mar 2020) |
| (new) | jepsen-io/elle/4e359e5.../README.markdown; github.com/jepsen-io/elle/compare/2843344...4e359e5 |
| jepsen.io/consistency/models/{serializable,strong-serializable} | unchanged: no immutable URL; sources.yaml names "unversioned page, read 2026-11-07" + section |

12 moving URLs pinned (10 raw GitHub files + arXiv + 2 new pinned additions).

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/transactional-history-testing
Skill is valid!
exit=0

sources.yaml: 15 entries; fields ok: True   (yaml.safe_load; each entry exactly name/url/type/accessed/sections_used)
cited-not-in-yaml: (none)
yaml-not-cited: (none)
moving: (none)   (grep -rnE '/(main|master|HEAD|latest|stable)/')
local links: ok SKILL.md -> references/{observable-dependencies,history-and-boundaries,elle-operation,common-mistakes}.md
git diff --check -- plugins/bugfinding/skills/transactional-history-testing: clean
last two bytes of every file: ". \n" or "\" \n" (exactly one trailing newline)
line counts: SKILL.md 32, common-mistakes.md 67, elle-operation.md 27, history-and-boundaries.md 18, observable-dependencies.md 21, sources.yaml 103
```

Frontmatter: name matches directory, description 263 chars (measured with wc -c), third person, has "Use when" triggers; unchanged.

## Unverified

- Retrieval method: raw GitHub files were fetched with `curl` at the pinned SHAs (and `gh api`) rather than WebFetch, so quotes are byte-exact; WebFetch was used for the arXiv abstract and the compare page. The compare page via WebFetch confirmed 1 commit / 1 file but did not name the file; `gh api .../compare` named it `project.clj`.
- jepsen.io model pages have no versioned URL; content can change after 2026-11-07.
- elle-cli JSON-mode stack/exit path for Elle validator `throw+` (unsupported micro-op/duplicate append) was not executed; the skill states only that the validators throw an error map with `:valid? :unknown`, which is what the source shows.
- No checker, CLI or target was executed; all CLI behaviour statements are source-read from cli.clj@3c25048.
- Adya paper: not cited by this skill; not used.
