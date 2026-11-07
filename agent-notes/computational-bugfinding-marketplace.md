# Computational bugfinding marketplace

## Goal

Research and plan a new marketplace/plugin skill set for computational bugfinding: spend compute to discover actual bugs, using LLMs for evidence-based triage.

## State

Q approved the 25-skill scope with “Make it so!” Skillbuilder Phases 1 and 2 are available in this repository's `reports/skill-research-computational-bugfinding.md` and `reports/skill-plan-computational-bugfinding.md`. Local git and the four approved host manifests are created at `C:/Users/Q/code/computational-bugfinding-skills-plugin`. Claude manifest validation passed; Codex JSON parsed. `reports/package-bootstrap.md` records exact scope and directory-submission findings. No skills or implementation code have been drafted by bootstrap.

## Decisions and why

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

Phase 3 is authorized: foundation research/draft first, batches of two or three researchers/drafters, then audit and isolated behavioral evaluation. Bootstrap is complete; component/host validation must follow drafting. This note and the approved reports now live in the new repository. The Elle collection remains at `C:/Users/Q/code/papers/`; the distributed plugin must not require it. Preserve Barn and unrelated work. No publication or remote mutation is authorized.
