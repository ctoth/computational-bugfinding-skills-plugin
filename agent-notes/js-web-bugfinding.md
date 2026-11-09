# JS/TS (Node and React) bugfinding coverage

## Goal

Q, 2026-11-09: "A lot of this here is low-level. we need also how to do this same thing in like React 'n Node 'n shit huh? can you build this out to the same quality?"

Extend the `bugfinding` plugin so its computational bugfinding methods work on Node.js services and React/browser applications, built through the same research -> plan -> draft -> improve -> audit -> behavioral-evaluation pipeline used for the original 25 skills. No skill or manifest changes until Q says "make it so".

## State

- Read `reports/skill-plan-computational-bugfinding.md` (design basis, skills 1-4, relationships, runtime coverage, exclusions, build order, acceptance). It records JS/TS as "fast-check only; no verified coverage-guided JS runtime chosen" and excluded GUI/browser skills pending method/tool evidence.
- Existing JS in skills: fast-check in `stateful-property-testing` references; Stryker in `harness-sensitivity/references/runtime-integrations.md`. No JS route in `coverage-guided-fuzzing`, schedule/race, resource or memory skills.
- `C:/Users/Q/code/papers/` has no JS/Node/web-testing papers.
- Phase 1 running. Domain report `reports/skill-research-js-web-bugfinding.md` in progress (F1 Jazzer.js, F2 fast-check scheduler, F3 Node.fz no current route, F4 ExpoSE weak, F5 Jalangi2/NodeProf, F6 memlab, F7 c8 so far).
- Papers read (paper-reader, page images), checked on disk: Endo_2020 NodeRacer (11 pp), Vilk_2018 BLeak (24 pp extended version from authors' GitHub; sci-hub blocked by classifier). In progress: Davis_2017 Node.fz, Raychev_2013 EventRacer, Mesbah_2012 Crawljax.
- Batch 2 launched: Staicu_2018 ReDoS, Arteca_2022 Nessie, Wang_2017 Node concurrency study, Adamsen_2017 EventRaceCommander (fallback AjaxRacer), Selakovic_2018 LambdaTester.

## Decisions and why

- Method-first layout retained: runtime specifics go into references of existing method skills unless research shows a distinct search dimension or oracle (the original plan's separation rule).
- Literature read through research-papers `paper-reader` only, page images only (AGENTS.md).
- 26th skill `ui-state-exploration`: Crawljax shows model-free discovery of a DOM state graph (state equivalence by comparators, DOM-change transition test, reload-and-replay reset, settle detection) that `stateful-property-testing` does not carry.
- ExpoSE as a gated route: matches the base pack's treatment of research-grade tools; applicability check first.
- Skill descriptions get Node/React wording: selection is driven by descriptions, which currently name only native/Go/Rust/.NET tools (the "low-level" complaint).
- Separate from the pending publication work in `agent-notes/computational-bugfinding-marketplace.md`; do not touch its README/CI plan.

## Surprises

- NodeRacer agent first wrote a DOI guessed from memory (wrong paper, DANTE); corrected from Crossref to 10.1109/icst46399.2020.00022. Later paper prompts forbid guessed identifiers.
- Late reports from stopped Phase 1 agents: Wang 2017 NodeCB dataset URL returned HTTP 404 on 2026-11-09 (22 of 57 bugs still listed as GitHub issue URLs, p.11); tool repos named in papers: github.com/cs-au-dk/EventRaceCommander, github.com/sola-da/LambdaTester (Node 8.5), zenodo.org/record/5874851 (Nessie), all unchecked. Open conflict: Nessie says LambdaTester handles only sync callbacks; LambdaTester tests promise then/catch without saying how it awaits.
- Rule breaks reported by agents: the domain researcher put Q's email in a Crossref request header and removed it before the script ran (its report); the EventRaceCommander agent moved a placeholder file with shell `mv` (copy at C:/Users/Q/AppData/Local/Temp/claude/erc_notes_hold.md). sci-hub was refused by the permission classifier for every paper; author copies used instead.
- BLeak suggests a JS route inside `resource-complexity-testing` (repeated UI-loop heap growth oracle) rather than a new skill; decide in the plan.

## Next step

Build authorized: Q, 2026-11-09, "Make it so!". Branch `js-web-bugfinding` (publication README/marketplace-note edits ride along uncommitted; never stage them). Groups: A fuzzing+corpus, B schedule+race boundary, C resource, D ui-state-exploration (new), E stateful, F semantic+configuration differential, G oracles+harness, H linearizability+transactional+distributed-fault, I symbolic/reduction/triage/campaign/no-route notes. Researchers write `reports/research-js-<group>.md`; drafters write `reports/draft-js-<group>.md` and edit only their skill dirs; parent checks and commits each group. Running: all nine researchers A-I (files created). Next: as each report lands, check it and start that group's drafter.

Phase 1 complete: domain report, all 10 papers read and folded into `reports/skill-plan-js-web-bugfinding.md`. Decided from evidence (not asked, per AGENTS.md "never ask about an option I'd mark Recommended"): new skill `ui-state-exploration` (Crawljax), gated ExpoSE route. All research agents stopped. Waiting for Q's "make it so" before any skill/manifest edit; then run the plan's build pipeline (per-skill research -> draft -> improve -> audit -> Node/React fixture evaluation).
