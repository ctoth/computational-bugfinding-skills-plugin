# Improve schedule-exploration

Skill: `plugins/bugfinding/skills/schedule-exploration/`. Accessed 2026-11-07.

## Findings

### F1 references/rust-controllers.md:9 — ERROR
- Said: "The inspected crate is 0.7.2, Rust 1.73 minimum, MIT", cited to `tokio-rs/loom/master/Cargo.toml`.
- Source: loom `master` (acaa24a9…, 15 commits ahead of tag v0.7.2) still says `version = "0.7.2"` but `rust-version = "1.73"`; the released crate's Cargo.toml at tag v0.7.2 (https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/Cargo.toml) and docs.rs published source (https://docs.rs/crate/loom/0.7.2/source/Cargo.toml.orig) both say `rust-version = "1.65"`, `edition = "2018"`. The unreleased master text was attributed to the released 0.7.2.
- Fix: changed to Rust 1.65 and pinned all loom raw links to the v0.7.2 tag commit `a7033ee06a97c52eb2f8131c095fbea6c6eecba3`, which matches the docs.rs 0.7.2 pages the skill cites.

### F2 references/sources.yaml:31 — WARNING
- Said: model.rs "Builder check lines 153-175; checkpoint modules 227-255".
- Source: src/model.rs at a7033ee (identical at master): `pub fn check` starts line 137, the checkpoint/permutation/duration polling block is lines 166-189 inside `if i % self.checkpoint_interval == 0`, and the `#[cfg(feature = "checkpoint")]` / `#[cfg(not(feature = "checkpoint"))]` modules are lines 246-279 (the latter: `panic!("not compiled with `checkpoint` feature")`).
- Fix: sections_used corrected to those line ranges.

### F3 references/sources.yaml:79 — WARNING
- Said: Shuttle README sections "Integration; License".
- Source: README.md at 855ae5d (= tag v0.9.10) has headings "Getting started", "Randomly testing concurrent code with Shuttle", "License"; no "Integration" heading. License line: "This project is licensed under the Apache-2.0 License."
- Fix: sections_used corrected.

### F5 references/dotnet-and-go.md:17 — WARNING
- Said: "Default invocation may run only one iteration".
- Source: Coyote using-coyote.md at 2202e75 (https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/using-coyote.md, "Testing options"): "If this option is not provided, the tester will perform 1 iteration by default." Hedge "may" contradicts the definite source.
- Fix: stated definitively with quote.

### F6 references/dotnet-and-go.md:19 — INFO (gap)
- Said: library `TestingEngine` integration covers rewriting, `TestReport`, `TryEmitTraces`, but not how the library route replays.
- Source: unit-testing.md at 2202e75, "Replaying a trace": `Configuration.Create().WithReproducibleTrace(trace)`; input is "the contents of a `.trace` file or the `string` value of `TestingEngine.ReproducibleTrace`".
- Fix: one clause added (replay is inside this skill's scope: "preserving and reducing a replayable scheduling counterexample").

### F7 references/replay-and-reduction.md:11 — WARNING (section mismatch)
- Said: "CHESS exposes enabled alternatives and actual resource/task identities for this reason ([CHESS, §§3.2, 4.1])".
- Source (CHESS page images p.5-7 read this session via the paper-reader artifacts at C:/Users/Q/code/bugfinding-literature/schedule-exploration/papers/Musuvathi_2008_FindingReproducingHeisenbugs/pngs/): task/synchronization-variable identity is §3.3 ("annotated with a triple—a task, a synchronization variable, and an operation") and §3.4; enabled alternatives are §4.1 ("together with the set of threads enabled at each point"). §3.2 is abstraction-layer choice, not identity.
- Fix: section changed to §§3.3–3.4, 4.1.

### F8 SKILL.md:14 — WARNING (section mismatch)
- Said: "do not merely rerun that pair or replace it with sleeps ... ([CHESS, §§3.2, 4.4–4.5])".
- Source: the sleep claim is CHESS §5.2 (p.10): "such calls impede the coverage achieved with CHESS as the scheduler (§4.3) assumes that a yielding thread is not able to make progress". §§3.2/4.4 do not discuss sleeps; §4.5 covers the invariant/monitor.
- Fix: cite §§4.5, 5.2 with quote.

### F9 references/controlled-boundaries.md:15 — ERROR (citation without link)
- Said: "scheduling and monitoring are independent concerns in CHESS (§4.5)" with no URL.
- Source: CHESS §4.5 (p.9): monitoring "is a orthogonal but important problem".
- Fix: inline link + quote added.

### F10 references/replay-and-reduction.md:17 — WARNING (misstatement)
- Said: "CHESS's fair-suffix assumption specifically depends on yielding only when progress cannot occur".
- Source: CHESS §4.3 (p.9): "Under the condition that a thread yields only when it is unable to make progress, this fair scheduler is guaranteed to not miss any safety error". The condition qualifies the fair scheduler's safety guarantee, not a "fair-suffix assumption"; §4.1 separately describes the record phase as "a fair, nonpreemptive scheduler".
- Fix: reworded to the source's claim with quote.

### F11 references/rust-controllers.md:19 — WARNING (uncited / vague)
- Said: "PCT parameters are not a general confidence guarantee" (no source says this); depth meaning not stated.
- Source: docs.rs shuttle 0.9.10 crate docs: PCT "can be configured with a "bug depth" (the number of preemptions)"; "Shuttle is not sound (a passing Shuttle test does not prove the code is correct)".
- Fix: replaced with the documented depth meaning and soundness statement.

### F12 references/rust-controllers.md:21 — INFO (gap)
- Source: MaxSteps docs (0.9.10): "By default, Shuttle fails a test after 1,000,000 steps." The default step bound is load-bearing for interpreting a FailAfter outcome nobody configured.
- Fix: one clause added.

### F13 references/common-mistakes.md:1-12 — ERROR (format)
- Said: a two-column table "Shortcut | Correction and evidence"; no WRONG-first/RIGHT/why structure required by skill-draft Step 3/7.
- Fix: each of the 8 rows rewritten in place as **Wrong:** / **Right:** / **Why:** with the same citations (pinned), no entries added or dropped.

### F14 all files — ERROR (citation rule) / WARNING (moving URLs)
- No verbatim fragments existed anywhere; load-bearing claims (Loom invisibility, checkpoint panic, false alarms/missed executions, Shuttle max_time, replay precondition, Coyote OutputPath overwrite, host matching, SC model, timeout modeling, synctest durable blocking, CHESS input onus) had paraphrase only.
- `microsoft.github.io/coyote/...` and `pkg.go.dev/testing/synctest` are unversioned (move with each release). Coyote docs pinned to their source markdown at commit 2202e75 (content compared against the rendered binary-rewriting page this session: same sections and sentences); synctest pinned to `@go1.27.3`, the version pkg.go.dev served.
- Fix: quotes added from text retrieved this session; URLs pinned.

### F4 references/rust-controllers.md:9, references/common-mistakes.md:8, SKILL.md:24 — WARNING (moving URL)
- Said: loom links `/master/`, docs.rs `/latest/` Builder.
- Fix: pinned (see Pinned URLs).

## Pinned URLs

SHAs resolved with `gh api repos/<org>/<repo>/commits/HEAD` and tags API; content fetched at each SHA before citing.

| Old | New |
|---|---|
| https://raw.githubusercontent.com/tokio-rs/loom/master/README.md | https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/README.md (tag v0.7.2; master acaa24a9 differs, see F1) |
| https://raw.githubusercontent.com/tokio-rs/loom/master/src/model.rs | .../a7033ee06a97c52eb2f8131c095fbea6c6eecba3/src/model.rs (byte-identical to master) |
| https://raw.githubusercontent.com/tokio-rs/loom/master/Cargo.toml | .../a7033ee06a97c52eb2f8131c095fbea6c6eecba3/Cargo.toml |
| https://docs.rs/loom/latest/loom/model/struct.Builder.html | https://docs.rs/loom/0.7.2/loom/model/struct.Builder.html |
| https://raw.githubusercontent.com/awslabs/shuttle/main/README.md | https://raw.githubusercontent.com/awslabs/shuttle/855ae5d92a02dd3c02ddd3ca99dfaeb3b5e31d5b/README.md (main = tag v0.9.10) |
| https://raw.githubusercontent.com/microsoft/coyote/main/LICENSE | https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/LICENSE |
| https://microsoft.github.io/coyote/concepts/binary-rewriting/ | .../coyote/2202e75a.../docs/concepts/binary-rewriting.md |
| https://microsoft.github.io/coyote/how-to/unit-testing/ | .../coyote/2202e75a.../docs/how-to/unit-testing.md |
| https://microsoft.github.io/coyote/get-started/using-coyote/ | .../coyote/2202e75a.../docs/get-started/using-coyote.md |
| https://microsoft.github.io/coyote/get-started/install/ | .../coyote/2202e75a.../docs/get-started/install.md |
| https://pkg.go.dev/testing/synctest | https://pkg.go.dev/testing/synctest@go1.27.3 |

Total: 11 URLs pinned (sources.yaml updated to match; 19 entries).

## Validation

Every cited URL was fetched this session: docs.rs loom 0.7.2 crate page and Builder, docs.rs shuttle 0.9.10 crate/Config/MaxSteps/replay/check_pct/check_dfs (WebFetch), all four rendered Coyote pages (WebFetch, matching the pinned markdown), raw loom/shuttle/coyote files at the pinned SHAs and pkg.go.dev synctest@go1.27.3 plus `src/testing/synctest/synctest.go` at tag go1.27.3 (curl, for exact text). CHESS pages 3-10 read as page images this session from the existing paper-reader artifacts.

Quote check (read-only python over fetched text): every quoted fragment from web sources found verbatim; the 11 CHESS fragments were checked by eye against page images p.4, 5, 7, 9, 10. The double-quoted lines under **Wrong:** in common-mistakes.md are example mistaken statements, not source quotes.

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/schedule-exploration
Skill is valid!

cited-not-in-yaml []
yaml-not-cited []
local SKILL.md references/controlled-boundaries.md True
local SKILL.md references/rust-controllers.md True
local SKILL.md references/dotnet-and-go.md True
local SKILL.md references/replay-and-reduction.md True
local SKILL.md references/common-mistakes.md True
moving []
unversioned []
SKILL.md 34 ends1nl True
references\common-mistakes.md 67 ends1nl True
references\controlled-boundaries.md 22 ends1nl True
references\dotnet-and-go.md 27 ends1nl True
references\replay-and-reduction.md 19 ends1nl True
references\rust-controllers.md 23 ends1nl True
references/sources.yaml 115 ends1nl True
diffcheck-clean   (git diff --check -- plugins/bugfinding/skills/schedule-exploration)

sources.yaml: yaml.safe_load OK, 19 entries, all have exactly name/url/type/accessed/sections_used, accessed 2026-11-07
```

Skill-audit 1-6: frontmatter name matches directory, description third-person with triggers (unchanged); SKILL.md 34 lines; no filler found; all local links resolve. No ERRORs in checks 1-6.

Claims cut: 1 ("PCT parameters are not a general confidence guarantee", replaced with the documented depth meaning and soundness statement). No other claim removed.

## Unverified

- Commands and APIs were read, not executed (no Loom/Shuttle/Coyote/Go toolchain run); this skill has no compilable code blocks that ship as RIGHT examples.
- Sentences explicitly labeled as this pack's adaptation or routing (dotnet-and-go.md:27, replay-and-reduction.md:11 first sentence and :13, controlled-boundaries.md:11-18, SKILL.md:16, :34) carry no external source by design.
- Not committed (per instruction; another session commits in this repo).
