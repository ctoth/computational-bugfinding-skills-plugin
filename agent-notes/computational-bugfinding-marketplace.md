# Computational bugfinding marketplace

## Goal

Research and plan a new marketplace/plugin skill set for computational bugfinding: spend compute to discover actual bugs, using LLMs for evidence-based triage.

## State

Q approved the 25-skill scope with “Make it so!” Phase 3 research and drafting are authorized. The approved domain research and plan are `reports/skill-research-computational-bugfinding.md` and `reports/skill-plan-computational-bugfinding.md` in `C:/Users/Q/code/computational-bugfinding-skills-plugin`.

- **Local package:** Bootstrap and four approved Claude/Codex manifests are committed. Claude manifest validation passed; Codex JSON/path probes passed. Codex host loading is untested. No remotes, installation or publication. Evidence: `reports/package-bootstrap.md`.
- **Foundation:** `bugfinding-campaign` research, skill, four references and draft report are committed. Its entry point is 57 lines; bundled quick_validate, local links/source inventory and staged whitespace checks passed. Evidence: `reports/research-bugfinding-campaign.md` and `reports/draft-bugfinding-campaign.md`.
- **Independent foundation application:** `reports/foundation-behavior-check.md` found no blocking skill defect and supports using the foundation as the drafting reference. It produced a source-grounded eight-CPU-hour Barn campaign proposal; it did not execute a campaign, establish a product bug or demonstrate improved discovery yield.
- **Correctness oracles:** `correctness-oracles` is drafted and committed with four references and research/draft reports. Its entry point is 45 lines; focused frontmatter, local links/source inventory and staged whitespace checks passed. No independent behavior or yield claim is established. Evidence: `reports/research-correctness-oracles.md` and `reports/draft-correctness-oracles.md`.
- **Evidence-based triage:** `evidence-based-triage` is drafted and committed with four references and research/draft reports. Its entry point is 35 lines; bundled quick_validate, local links/source inventory and staged whitespace checks passed. No independent behavioral or empirical accuracy/yield claim is established. Evidence: `reports/research-evidence-based-triage.md` and `reports/draft-evidence-based-triage.md`.
- **Harness sensitivity:** `harness-sensitivity` is drafted and committed with four references plus research/draft reports. Its entry point is 42 lines; frontmatter, local links/source inventory and staged whitespace checks passed. Evidence: `reports/research-harness-sensitivity.md` and `reports/draft-harness-sensitivity.md`.
- **Failure reduction:** failure-reduction is drafted and committed with five references and its research/draft reports. Entry point 41 lines; focused validator/link/source-inventory/staged whitespace checks passed. No behavioral/yield claim established.
- **Stateful properties:** stateful-property-testing is drafted and committed with four references plus research/draft reports. Entry point 37 lines; focused validator/link/source-inventory/staged whitespace checks passed. Runtime references include verified Go Rapid, Hypothesis and fast-check routes and replay restrictions.
- **Semantic generation:** semantic-program-generation is drafted and committed with five references plus research/draft reports. Entry point 32 lines; focused validator/link/source-inventory/staged whitespace checks passed. Its scope is phase-specific semantic environment/effect/world construction and replay; no empirical yield claim.
- **Semantic differential:** semantic-differential-testing is drafted and committed with five references plus research/draft reports. Entry point 30 lines; focused validator/link/source-inventory/staged whitespace checks passed. It covers matched logical state/causal prefixes and contract-specific effect/value equality.
- **Corpus evolution:** corpus-evolution is drafted and committed: entry point 32 lines, five references, source/native-tool recipes with selected-version licensing scope. Focused frontmatter/link/source-inventory/staged whitespace checks passed; task note traveled with substantive commit.
- **Metamorphic testing:** metamorphic-testing is drafted and committed: entry point 32 lines, five references covering relation validity, composition, concrete worked relations and conditional SQLancer operations. Focused validator/link/source-inventory/staged whitespace checks passed.
- **Coverage-guided fuzzing:** draft completed and focused validation passed: entry point 39 lines, seven progressive runtime/method references and primary-source inventory. Native, Go/Rust, Python/JVM and C++ FuzzTest setup/discovery/reset/replay contracts are covered. Staged whitespace check caught extra EOF blank lines; writer is correcting those with the editing tool before the scoped commit, including this task note.
- **Current research/drafting:** schedule-exploration and linearizability-checking research in progress. Completed paper image evidence and runtime applicability limits are in research reports. Parent serializes commits.
- **Remaining work:** Complete the approved specialist research/draft batches, then audit the full collection and perform isolated behavioral evaluations. No target behavior or empirical discovery campaign has run as part of these research/draft steps.

## Decisions and why

- Q's replacing AGENTS.md on 2026-11-07 requires the research-papers plugin's paper-reader only, never paper-process, and direct page-image reading. Parent messaged active agents and updated shared researcher/drafter prompts; the plan now carries the same forward-looking instruction. Existing historical artifacts remain evidence and are not rewritten or deleted.
- Follow the requested skillbuilder research → plan → user confirmation → draft → audit pipeline.
- Research methods and decision criteria before deciding skill boundaries.
- Preserve distinctions among candidate failures, harness defects, semantic disagreements, and verified product defects.
- Plan by independent search dimension and correctness contract, with tool/runtime references inside method owners. One plugin avoids artificial method dependencies; no generic scheduler, simulation layer or duplicate target implementation is proposed.
- Treat Barn's valid-IR generation, native fuzzing, Toast result replay, restored-bytecode execution and strong Elle workloads/controls as baseline. Proposed advances must expose new evidence beyond them.
- Four proposed skills are explicitly research-first: crash consistency, liveness, configuration differentials and numerical oracles. Every other skill still requires Phase 3 primary-source/literature work; no implementation readiness or empirical bug yield is claimed.

## Surprises

- Barn's local committed master was behind its already-fetched tracking ref by 20 commits and had unrelated dirty work. Reading the tracking ref showed that valid-IR structured generation and corpus-based Toast differential checking already exist; neither can be sold as a new capability. The report distinguishes both refs and scopes the proposed advances above the stronger baseline. Barn was not mutated.
- Elle's 14-page PDF was retrieved, rendered and fully read as page images. Notes, description, abstract artifact, all 38 bibliography entries, metadata/citation key, index, processed ledger and generated keymap now exist in the task-local papers collection. Tagging and reconciliation are complete: three tags, no other processed papers to link, four new leads. The abstract artifact uses a short excerpt plus paraphrase; retrieved metadata retains the source abstract. No propstore or sibling collection changes.
- Current OpenAI docs describe portable root `plugin.json` and retain `.codex-plugin/plugin.json` as compatibility fallback. Bootstrap preserves the approved fallback layout. Claude validation distinguishes valid local manifests from public-directory requirements: README, license and icon remain absent; no public submission readiness is claimed.

## Next step

Continue the approved research/draft batches using the completed foundation as the reference. Parent serializes commits. Component/host validation, full collection audit and isolated behavioral evaluation remain required. Future literature work uses paper-reader only and page images. The Elle collection remains at `C:/Users/Q/code/papers/`; the distributed plugin must not require it. Preserve Barn and unrelated work. No publication or remote mutation is authorized.
