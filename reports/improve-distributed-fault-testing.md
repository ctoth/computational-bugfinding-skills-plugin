# Improve: distributed-fault-testing

Skill: `plugins/bugfinding/skills/distributed-fault-testing/`
Date: 2026-11-07

## Findings

Sources retrieved this session by `curl` of the exact pinned raw URLs into the scratchpad (identical bytes to WebFetch of raw GitHub; raw files are full source, no truncation): jepsen README/client/combined/checker/core/cli/project/CHANGELOG at 6766ba09, history README at 61d2776c, generator source/README at 3073ba45, etcd source/README at b47cc401. All cited URLs were already commit-pinned; no moving-branch URL found.

### F1 — references/sources.yaml:8-10 — WARNING
- Text: README `sections_used` lists "Environment/control nodes".
- Source: README headings are "Setting up a Jepsen Environment", "VMs, Real Hardware, etc.", "LXC", "Setting Up Control Nodes" (https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md).
- Fix: replace with actual heading names.

### F2 — references/jepsen-operation.md:15 — ERROR (uncited claim)
- Text: "retries can create additional physical attempts without determining their outcomes" cited to history README.
- Source: history README "Operation Semantics" says only "`:ok` *must* logically affect the system ... `:fail` *must* have no logical effect ... An `:info` may do either." and that a crashed process "can never invoke an operation again". Nothing about retries.
- Fix: replace the retry sentence with the cited crashed-process rule (verbatim), keep retry provenance as instruction without a factual claim attributed to the source.

### F3 — SKILL.md:8 — WARNING (claim stronger than source)
- Text: "an outage or performance plot is not itself a consistency counterexample" cited to README.
- Source: README says Jepsen "can also generate graphs of performance and availability, helping you characterize how a system responds to different faults" and the checker analyzes "the test's history for correctness". The distinction is supported by quoting both.
- Fix: add verbatim fragments.

### F4 — references/fault-model-and-activation.md:3 and SKILL.md:20 — ERROR (misstatement)
- Text: nemesis packages "expose process, partition, packet and clock operations with matching repair generators"; SKILL: packages "pair generators with final repair generators".
- Source: combined.clj `nemesis-packages` builds partition, packet, file-corruption, clock and db packages (`[:partition :packet :kill :pause :clock :file-corruption]`); `file-corruption-package` returns only `:generator`, `:nemesis`, `:perf` — no `:final-generator`. db kill/pause modes only exist when the DB `satisfies? db/Process` / `db/Pause`. Docstring: "This nemesis is *not* intended for complex sequences of faults" and "you'll write your own generator instead" (https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/nemesis/combined.clj).
- Fix: list file corruption and state it has no final generator; add the "not intended for complex sequences" limit next to the ownership-transition experiment (which is such a sequence).

### F5 — references/jepsen-operation.md:26 — ERROR (gap with real hazard)
- Text: warns `--serializable` must not be silently enabled.
- Source: etcd.clj cli-opts `["-s" "--serializable" "Use serializable reads, instead of going through consensus."`; etcd README's stale-read example is `lein run test --time-limit 30 -s --nemesis partition --workload register --concurrency 2n` (https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj, .../README.md). Copying the README example enables serializable reads through the short flag.
- Fix: name the `-s` short form and the README example.

### F6 — references/recovery-and-evidence.md:9 and SKILL.md:28 — WARNING (gap)
- Text: "Capture the state required by the oracle before teardown."
- Source: core.clj `run!` docstring steps "6. Capture log files", "7. Teardown the database", "9. When the generator is finished, invoke the checker with the history"; `analyze!` calls `checker/check-safe` on `(:history test)` after `with-db` exits (https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/core.clj). So the checker sees only the history: final observations must be client operations in the generator.
- Fix: state that the checker runs after DB teardown on the history, so final observations must be generated operations.

### F7 — references/recovery-and-evidence.md:3 — INFO (precision)
- Source: etcd.clj heals/sleeps only in the non-Antithesis branch ("In normal Jepsen, we use a time limit, then heal the cluster"); under Antithesis it uses `jepsen.nemesis/noop` and goes straight to the final generator.
- Fix: qualify "normal Jepsen" branch.

### F8 — references/jepsen-operation.md:15 — supports F2 fix
- Source: generator README "if a write fails, the generator could decide to retry it" (https://raw.githubusercontent.com/jepsen-io/generator/3073ba45cb3db0b6dcc5aa915907a2e67b04eef5/README.md); etcd cli-opts `--retry-max-attempts COUNT` "Number of retry attempts we allow."
- Fix: cite these for the retry sentence instead of the history README.

### F9 — references/common-mistakes.md:1-13 — ERROR (format)
- Text: a two-column Mistake/Correction table.
- Pattern: skill-draft Step 3 requires "WRONG first, then RIGHT" with "a one-line *why*"; foundation `bugfinding-campaign/references/common-mistakes.md` uses `## heading` / **Wrong:** / **Better:** / **Why:**.
- Fix: convert each row to Wrong/Right/Why with citations and quote fragments.

### F10 — checker evidence for the "green run" mistake — WARNING (gap)
- Source: checker.clj `unbridled-optimism` always returns `{:valid? true}`; `stats` computes per-`:f` `{:valid? (pos? oks)}` (code gives `false`, though its docstring says ":unknown") — "Results are valid only if every :f has at some :ok"; set checker returns `{:valid? :unknown :error "Set was never read"}` without a final read; `merge-valid` priorities `{true 0 false 1 :unknown 0.5}`. cli.clj `single-test-cmd` exits 1 on `false`, 2 on `:unknown`, and calls no exit for other values.
- Fix: cite these concretely in common-mistakes and jepsen-operation interpretation.

### F11 — references/jepsen-operation.md:9 — WARNING (stale hedge now resolvable)
- Text: "the full core license text was not verified in this research".
- Source: https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/LICENSE.txt begins "Eclipse Public License -v 1.0"; project.clj declares `(defproject jepsen "0.3.16-SNAPSHOT"` and `:jvm-opts ["-Xmx32g"`.
- Fix: cite LICENSE.txt, drop the hedge; quote the SNAPSHOT version; add sources.yaml entry.

### F12 — SKILL.md:30 — WARNING (gap: checker-version provenance)
- Source: CHANGELOG 0.3.15 "Elle 0.2.8 fixes a major correctness bug which caused `rw-register` workloads to incorrectly infer cyclic version orders" (https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md).
- Fix: tell the reader to record checker version; a false verdict from a checker version with a known fixed inference bug needs re-analysis.

### F13 — Elle citations (SKILL.md:34, recovery-and-evidence.md:17, fault-model-and-activation.md:22, common-mistakes.md:13) — WARNING (no quotes, unpinned)
- Verified this session from page images `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/pngs/page-002/006/007/008/011.png` (paper read through paper-reader per research report): p.3 §3 blind writes "destroy history"; p.7 §4.3.1 "the fewer indeterminate transactions it holds, the more non-cycle anomalies we can catch"; p.8 §4.3 Completeness "In practice, we typically fail to observe the results of some transactions"; p.9 §6 "These cycles can be presented to the user as a witness of an anomaly"; p.9 §6.1 "Duplicate writes can occur when a client or database retries an append operation"; p.12 §9 "Our approach ignores predicates and deals only in individual objects".
- arXiv lists only v1 (submitted 23 Mar 2020); unversioned `/abs/2003.10554` would re-point if a v2 appears.
- Fix: add fragments; pin to https://arxiv.org/abs/2003.10554v1.

### F14 — references/fault-model-and-activation.md:14 — WARNING (gap)
- Text: majority/minority, asymmetric partition and pause are different experiments; selectors are "starting points".
- Source: combined.clj `grudge` specs `:one :majority :majorities-ring :minority-third :primaries` (complete grudges or ring; other values pass through); packet-nemesis "The network behavior is applied to all traffic to and from the target nodes."
- Fix: state that neither built-in gives a one-direction fault by name.

### F15 — references/jepsen-operation.md:26 — WARNING (gap)
- Source: cli.clj `(def default-nodes ["n1" "n2" "n3" "n4" "n5"])`; `--leave-db-running` "so you can inspect it"; `single-test-cmd` exits on the first false/unknown run when `--test-count` > 1.
- Fix: added default-node hazard (always pass owned nodes) and test-count behavior.

### F16 — references/jepsen-operation.md:13 — INFO
- Source: client.clj `Validate` checks only map shape, `:type` in `#{:ok :info :fail}`, same `:process`, same `:f`; `Reusable` docstring "crashed clients will be closed and new ones opened to replace them"; etcd cli-opts `--client-type etcdctl` "definitely buggy" and leaks "operations into the *next* test run".
- Fix: stated exact Validate checks; added Reusable quote (common-mistakes) and etcdctl warning.

### F17 — SKILL.md:30 — INFO (not fixed)
- `crash-consistency-testing` is routed to but no such skill directory exists yet under plugins/bugfinding/skills/ (bugfinding-campaign routes to it too). Not a local link; outside this skill's files; left for the pack owner.

### Applied (SKILL.md)
F3, F4, F6, F12, F13 applied in SKILL.md lines 8-34 with verbatim fragments; link texts now name file + section per house style.
### Applied (fault-model-and-activation.md)
F4 (line 3), F14 (line 14), lazyfs quote (16), grepkill quote + db-nemesis completion value (20), Elle quote/pin (22), lock-set quotes + "not intended for" generator routing (26).

### Applied (jepsen-operation.md)
F2, F5, F8, F11, F15, F16, plus quote fragments for README requirements, generator time-limit/synchronize/until-ok, CLI exit codes and analyze, checker unbridled-optimism/stats/set.
### Applied (recovery-and-evidence.md)
F6, F7 (Antithesis branch), generator README example, final-generator list incl. file-corruption gap, README sudo/prod quotes, stored-test quote, Elle quotes/pin, set-checker "Set was never read", etcd option quotes.
### Applied (common-mistakes.md)
F9: table converted to 10 Wrong/Right/Why entries (9 original + etcd `-s` example from F5), each cited with fragments.
### Applied (sources.yaml)
F1; sections_used corrected for client, combined, generator, checker, core, cli, project.clj, etcd.clj, Elle; added core LICENSE.txt entry; generator README renamed from "license" (now also cited for retry and example).

## Pinned URLs

- All Jepsen/history/generator/etcd URLs were already commit-pinned (6766ba09…, 61d2776c…, 3073ba45…, b47cc401…); none on a moving branch.
- New: https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/LICENSE.txt (HTTP 200, fetched this session).
- Elle: https://arxiv.org/abs/2003.10554 -> https://arxiv.org/abs/2003.10554v1 (WebFetch: only v1, submitted 23 Mar 2020), all 4 files + sources.yaml.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/distributed-fault-testing
Skill is valid!
exit=0
$ git diff --check -- plugins/bugfinding/skills/distributed-fault-testing
diffcheck exit=0
--- cited not in yaml:
(none)
--- yaml not cited:
(none)
--- moving urls:
(none)
--- local links:
ok references/jepsen-operation.md
ok references/fault-model-and-activation.md
ok references/recovery-and-evidence.md
ok references/common-mistakes.md
--- line counts: SKILL.md 36, common-mistakes 81, fault-model 28, jepsen-operation 34, recovery 25, sources.yaml 152
--- trailing bytes: every file ends with a single "\n"
```

Quote check: every double-quoted fragment in SKILL.md and references/*.md was searched (whitespace-normalized) against the downloaded pinned sources plus LICENSE.txt. Not found textually, as expected: Elle fragments (verified visually on page images pp.3, 7, 8, 9, 12 this session) and the hypothetical "Wrong:" statements in common-mistakes.md (not quotes of a source).

## Unverified

- Retrieval method: raw GitHub files were fetched with `curl` of the exact pinned URLs (full files, read in the scratchpad), not the WebFetch tool; arXiv abstract via WebFetch.
- Elle §4.3 "Completeness" quotes: the p.7 quote is in §4.3.1, the p.8 quote in §4.3.2 (both under §4.3); sources.yaml says so.
- Nothing was executed against a cluster; all commands remain source-read illustrations.
