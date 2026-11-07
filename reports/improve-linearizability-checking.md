# Improve linearizability-checking: citation and content audit

Skill: `plugins/bugfinding/skills/linearizability-checking/`
Date: 2026-11-07

## Findings

Porcupine sources were fetched at the pinned commit `97cd067defd99df172053ba7f4ca5bbae57fe446` (resolved with `gh api repos/anishathalye/porcupine/commits/master --jq .sha`, committer date 2026-09-21) with `curl` from `raw.githubusercontent.com/anishathalye/porcupine/<sha>/<file>`: model.go (373 lines), porcupine.go (48), checker.go (471), porcupine_test.go (2039), visualization.go (269), go.mod (3), LICENSE.md (22), README.md (287). Line numbers below are in those pinned files.

### F1 ERROR: every Porcupine link uses the moving `/master/` branch
- Where: SKILL.md:12,14,16,22,24,28; references/common-mistakes.md:6,7,8,10,11,12; references/model-and-history.md:7,13,17,23; references/partition-and-cost.md:7,15; references/porcupine-operation.md:5,11,25,37,39; references/sources.yaml:3,8,13,18,23,43,48; plus `https://github.com/anishathalye/porcupine` (README) at model-and-history.md:11, porcupine-operation.md:37, sources.yaml:28.
- Source: skill-draft Step 5 forbids moving aliases. Master resolves to `97cd067defd99df172053ba7f4ca5bbae57fe446`.
- Fix: all replaced with `https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/<file>`; the README link is replaced with the raw README.md at the same SHA. sources.yaml updated to match.

### F2 WARNING: common-mistakes.md is a two-column table with no one-line why
- Where: references/common-mistakes.md:3-12.
- Source: skill-draft Step 3 requires "WRONG first, then RIGHT", each pair with "a one-line *why*"; the foundation skill `bugfinding-campaign/references/common-mistakes.md` uses `## heading`, `**Wrong:**`, `**Better:**` sections.
- Fix: converted each row to the foundation's Wrong/Better section form, adding a cited one-line why per entry (targeted per-row edits; no entry dropped).

### F3 WARNING: unmatched Event calls are silently misread, not just "not repaired"
- Where: references/model-and-history.md:13 said "the implementation pairs events rather than repairing them".
- Source (checker.go at pinned SHA): `makeLinkedEntries` builds a call node with `match: match[elem.id]` (line 201), which is nil when no return with that id follows; `checkSingle` treats a node with nil `match` as a return (`if entry.match != nil {` line 271, else-branch backtracks), and sizes the search as `n := len(history) / 2` (line 258). No error is raised.
- Fix: sentence now states that an unmatched or out-of-order call is read as a return without any error, with checker.go line citation and a quote fragment.

### F4 INFO: timeout behavior differs between verbose and non-verbose calls
- Where: SKILL.md:24, partition-and-cost.md:15, common-mistakes.md:11 ("verbose checking waits for workers").
- Source (checker.go): on timeout `checkParallel` calls `cancel()` and breaks (lines 405-408); only when `computeInfo` is set does it drain every worker ("make sure we've waited for all goroutines to finish", lines 413-418). A non-verbose call therefore returns `Unknown` at the deadline while a worker blocked in a legacy `Step` keeps running; a verbose call does not return until that worker finishes. `StepContext` is preferred when set: "allowing the model to stop work promptly when a timeout expires" (model.go:114-116).
- Fix: partition-and-cost.md:15 made precise with these two cases and quote fragments.

### F5 WARNING: Jepsen linearizable page does not say isolation or race freedom fails to supply the guarantee
- Where: SKILL.md:8 ("transaction isolation or race freedom does not supply this guarantee ([Jepsen model](...linearizable))"); common-mistakes.md:5.
- Source: the linearizable page (curl, 2026-11-07) says only "Linearizability is one of the strongest single-object consistency models" and orders operations "consistent with the real-time ordering of those operations". The isolation point is on the Jepsen serializable page: serializability "does not impose any real-time, or even per-process constraints" (https://jepsen.io/consistency/models/serializable). The race-freedom point is in the Go memory model (Version of June 6, 2022): "data-race-free programs execute in a sequentially consistent manner" (https://go.dev/ref/mem), and the linearizable page names sequential consistency as the model for when "real-time constraints are not important".
- Fix: SKILL.md:8 and common-mistakes entry 1 re-cited to the three pages with quote fragments; both new URLs added to sources.yaml.

### F6 INFO: version is now known: pinned master commit is tag v1.3.1
- Source: `gh api repos/anishathalye/porcupine/tags` lists `v1.3.1 97cd067defd99df172053ba7f4ca5bbae57fe446`, the same commit as master.
- Fix: porcupine-operation.md:5 now names v1.3.1 and that `StepContext` is present in that source (model.go:114-117); the vague "Verify newer cancellation APIs in the selected release" kept as an instruction but anchored to that version.

### F7 WARNING: visualization replay calls `Step` and panics on a step the model now rejects
- Where: porcupine-operation.md:37 ("Visualization replays model steps").
- Source (visualization.go): `computeVisualizationData` applies `fillDefault` then calls `model.Step(...)` (line 187) and on rejection `panic("valid partial linearization returned non-ok result from model step")` (lines 188-190). This replay uses `Step`, although model.go:114-116 says "the checker and visualization replay call StepContext instead of Step" (upstream comment/code mismatch; not our text to fix, recorded here).
- Fix: porcupine-operation.md:37 states that replay re-runs the model and an impure or non-repeatable model can make rendering panic, with quote.

### F8 WARNING: paper Definition 5 lets pending calls be completed by appending returns; skill cited it only as "assumes completed histories"
- Where: model-and-history.md:19; SKILL.md:30.
- Source (paper-reader page image page-004.png = paper p.5, read this session): Definition 5, a history is linearizable "if it can be extended to a complete history H′ (by appending zero or more returns)"; "This paper therefore considers only complete histories", justified by the assumption "that the concurrent system is deadlock-free".
- Fix: model-and-history.md:19 now quotes both, which grounds the etcd adapter's appended returns and keeps the "zero" option (a pending call may also never take effect). SKILL.md:30 liveness sentence given the deadlock-free quote.

### F9 WARNING: "Transfers, scans or allocation constraints" attributed to the paper, which does not discuss them
- Where: partition-and-cost.md:5 cites "[P-compositionality, pp.5-6,9]" for transfers/scans/allocation.
- Source (page-005.png = p.6): examples are set, map, array, stack; the limit stated is "a 'size' operation that returns the number of elements in a concurrent collection data type cannot be generally partitioned this way." No transfers/scans/allocation.
- Fix: sentence split so the paper is cited only for set/map partitioning and the size limit (with quote); the transfer/scan sentence is re-cited to Porcupine's iff `Partition` contract (model.go:102-104), which is what makes it a requirement.

### F10 INFO: paper timeout-exclusion and incompleteness claims confirmed and quoted
- partition-and-cost.md:13 (pp.11-14): page-011.png (p.12) "These averages exclude runs that we had to terminate after 1 hour." Confirmed; quote added, citation narrowed to p.12.
- SKILL.md:22, partition-and-cost.md:17 (pp.13-14): page-012.png (p.13) testing techniques are "precise, fully automatic and necessarily incomplete"; page-013.png (p.14) "our work assumes that the specification is P-compositional". Confirmed; quote added at partition-and-cost.md:17.

### F11 WARNING: uncited normative/factual sentences
- SKILL.md:12 "Build a small abstract model rather than port target internals" had no source. Cited to paper p.14 (page-013.png): "strictly separates the concurrent implementation from its specification".
- SKILL.md:24 "More overlap, operations and coupled keys can expand the checker's work" had only a checker.go link for a different clause. Cited to model.go CheckResult: "is an NP-hard problem, so the checker might take a long time", and Model: "Implementing the partition functions can greatly improve performance".
- porcupine-operation.md:7 "this changes dependency files/downloads" now quotes go.dev: "updates the `require` directive in your go.mod file", "downloads module source code".
- porcupine-operation.md:33 `-count=1` caching claim was cited to the Testing flags anchor, but the caching sentence is in "Test packages". Re-cited with quote "The idiomatic way to disable test caching explicitly is to use -count=1." and `-timeout` quoted ("If a test binary runs longer than duration d, panic.").
- SKILL.md:22 added the upstream counter-statement "you can interpret an Unknown result as Ok" (model.go:364-366) so the reader sees why the skill rejects it; the `Unknown` constant is commented `// timed out`.

### F12 INFO: quotes added throughout
- 34 non-paper quote fragments were checked by a read-only script against the fetched source text (Porcupine files at the pinned SHA, Jepsen pages, Go memory model, go.dev, pkg.go.dev go1.27.3): all present. 16 paper fragments were checked by eye against page images page-004, -005, -011, -012, -013 read this session.

### F13 INFO: `pkg.go.dev/cmd/go` link unversioned
- Where: porcupine-operation.md:33, sources.yaml:58.
- Source: `https://go.dev/VERSION?m=text` returned `go1.27.3`; `https://pkg.go.dev/cmd/go@go1.27.3` fetched with curl contains the quoted text.
- Fix: pinned to `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags` and `#hdr-Test_packages`.

## Pinned URLs

| Before | After |
|---|---|
| `https://raw.githubusercontent.com/anishathalye/porcupine/master/{model.go,porcupine.go,checker.go,porcupine_test.go,visualization.go,go.mod,LICENSE.md}` | `https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/<same file>` (tag v1.3.1) |
| `https://github.com/anishathalye/porcupine` (README) | `https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/README.md` |
| `https://pkg.go.dev/cmd/go#hdr-Testing_flags` | `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags` (and `#hdr-Test_packages`) |

9 distinct URLs pinned. Not pinnable (no versioned URL published): `https://jepsen.io/consistency/models/linearizable`, `https://jepsen.io/consistency/models/serializable`, `https://go.dev/doc/modules/managing-dependencies`; `https://go.dev/ref/mem` is cited with its in-page version "Version of June 6, 2022". `https://arxiv.org/abs/1504.00204` is a stable identifier.

New sources added: Jepsen serializable, Go memory model. sources.yaml: 12 entries before, 14 after; every entry's `sections_used` rewritten to the sections actually cited.

## Validation

```text
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/linearizability-checking
Skill is valid!

read-only provenance probe (pathlib/re/yaml/urldefrag over SKILL.md, references/*.md, sources.yaml):
sources 14 cited 14
cited-not-in-sources []
unused-sources []
errors []          # broken local links, /master/ /main/ /HEAD/ /latest/ /stable/, EOF not exactly one newline
lines {'SKILL.md': 32, 'common-mistakes.md': 65, 'model-and-history.md': 23, 'partition-and-cost.md': 17, 'porcupine-operation.md': 39, 'sources.yaml': 71}

$ git diff --check -- plugins/bugfinding/skills/linearizability-checking
git-diff-check-exit=0
```

Quote probe: script `checkquotes.py` in the session scratchpad; 34 OK. The remaining unmatched fragments are all paper quotes (not in the fetched text corpus) plus one false negative where a code span sits inside the quote (`updates the `require` directive in your go.mod file`, confirmed present separately). The paper quotes were checked against page images.

Skill-audit checks 1-6: frontmatter name matches directory, description is third person with a when-clause, body 32 lines, references one level deep, no reference file over 100 lines, local links resolve. No ERRORs found there. Nothing was committed or staged.

## Unverified

- The upstream comment in model.go:114-116 says visualization replay calls `StepContext`; visualization.go:187 calls `model.Step`. Recorded as an upstream mismatch (F7); the skill text describes the code.
- Paper page numbers assume page-NNN.png = paper page NNN+1 (page-004 holds Definitions 5-6, which the existing notes and citations call p.5). Printed page numbers are not visible on the images.
- `pp.9-10` of the paper (partitioner algorithm) were not re-read this session; citations to p.9 were removed rather than relied on.
- The Go and Porcupine example commands and the Go fragment in porcupine-operation.md were not compiled or run (the skill already labels them as not executed).
- No claims were cut. The partition-and-cost.md:5 transfer/scan sentence was kept but re-cited (F9).
