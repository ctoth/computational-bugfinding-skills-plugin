# Scenario A bounded behavior evaluation

## Goal and state

Complete. One implementation defect demonstrated through two public rejected-move paths. Both original histories and reduced witnesses were reproduced; healthy/allowed-error controls were accepted. Only scenario-a public files and the released skill subset were read. No target edits, network, Git, installations, or subagents.

## Next step

Stop computation and hand off the preserved fixture evidence. This is a bounded artifact evaluation, not a production bug claim or a comparison against unassisted work.

## Executable experiment

Artifact root: `C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-a/`.
One authored runner: `test_quota.py`. It imports the real public `QuotaStore`, creates all states through API calls, and observes `state()` before/after every call. The independent oracles are complete snapshot equality after a rejected call and `used == sum(artifacts.values())` with quota bounds after every call. These do not copy move implementation branches. Exceptions are limited to the three contract exception classes; arbitrary exceptions propagate. A missing-setup candidate does not qualify as the selected failure.

The finite search generated 56 valid setup histories: source capacity 3, source size 0..3, destination capacity 0..3, and destination artifact absent or size 0..capacity, followed by a move. Each history also used a separate noise bucket through create/put/remove. This exercises state-producing create/put/remove/move paths, legal successes, rejected moves, and error effects. It is deterministic enumeration rather than coverage-guided fuzzing. No Hypothesis integration was assumed or installed; the inspected Python recipe was conditional on an existing fitting integration, and the dependency-free bounded loop fits the task envelope.

## Raw trigger and finding

The saved `search.txt` begins each original finding with its complete raw history and per-call snapshots. The capacity original is:

```json
[["create_bucket","noise",3],["put","noise","unused",2],["remove","noise","unused"],["create_bucket","a",3],["create_bucket","b",0],["put","a","x",1],["move","a","b","x"]]
```

The duplicate original inserts `["put","b","x",0]` immediately before move. Both start with an empty store and all setup calls succeed.

Contract: `scenario-a/contract.md` guarantees each rejected operation leaves the entire state unchanged, and each bucket's used equals its artifact-size sum. The capacity move returns the allowed `ValueError: destination capacity exceeded`; the duplicate move returns the allowed `ValueError: artifact already exists at destination`. The exception itself is expected. The observed violation is that source `a` changes from `used: 1, artifacts: {x: 1}` to `used: 0, artifacts: {x: 1}`. Destination remains unchanged. The checker reports both `changed_on_error: true` and `accounting_valid: false`.

Source cause is established for this artifact: `scenario-a/target.py:62-63` removes the artifact and decrements used before destination checks at 65-68. The error handler at 71-73 restores the artifact alone, leaving used decremented. These two error paths reach the same incomplete rollback, so they are two witnesses of one implementation defect, not two claimed unique bugs. This directly demonstrates misleading source quota accounting following a rejected move; broader subsequent-call effects were not tested.

## Reduction and replay

The reducer tries single-operation deletion to a fixed point, followed by smaller integer arguments, preserving the same rejected-move error text plus both violated guarantees. It uses public API replay for every candidate. It made 21 attempts, removed the three noise operations, and lowered source capacity from 3 to 1. The reduced capacity witness is four calls:

```json
[["create_bucket","a",1],["create_bucket","b",0],["put","a","x",1],["move","a","b","x"]]
```

The reduced duplicate witness adds `["put","b","x",0]` before the move, totaling five calls. Original and reduced histories, error strings, before/after states, and oracle observations remain separate in `search.txt`. The retained reduced witnesses were then replayed in fresh processes with the commands below. This is reduction relative to those operations, smaller integers, selected error path, and observed guarantee; no absolute global minimality claim.

| Exact command | Saved raw output | Status | Measured loop CPU |
|---|---|---|---|
| `python C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-a/test_quota.py` | `search.txt` | 1 | 0.1875 s |
| `python C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-a/test_quota.py capacity` | `replay-capacity.txt` | 1 | 0.203125 s |
| `python C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-a/test_quota.py duplicate` | `replay-duplicate.txt` | 1 | 0.140625 s |

Status 1 is deliberate failing-contract-test status, not an infrastructure failure. Both replays printed the same selected violation, with healthy controls accepted in each process. An initial unsaved-output pilot also ran the identical search: status 1, 551 calls, 84 histories, 0.09375 s measured loop CPU; its exact output remains in the tool transcript. The repeated saved search is identified above. Total measured loop CPU for all four runs is 0.625 s; measurement starts after imports and excludes Python startup. The four short executions are far below the 30-second process-CPU envelope; no long-lived process or large data structures were used.

The saved search accounts for 84 total histories including controls/reduction, 551 API calls and invariant checks, 471 successes, and 80 expected errors with 80 error-state checks. Capacity replay accounts for 22 calls/6 histories; duplicate replay 23 calls/6 histories. Snapshot-independence control is additional to those counters. No code coverage instrumentation or coverage claim.

## Controls and sensitivity limits

Every invocation accepts the healthy cross-bucket move, same-bucket successful no-op, ordinary capacity-rejected put, duplicate destination with zero-sized source (unchanged state), and missing-bucket setup error. A nested snapshot mutation does not affect the store. These are public target executions, not target mutations. The real positive-sized rejected moves activate the incorrect rollback, change state, reach the before/after snapshot and accounting checks, and are rejected by those checks. Zero-sized source and successful-move controls distinguish permitted errors/successes from the wrong effect. No general mutation score or universal oracle sensitivity is claimed.

## Skill use and identities

All paths below are relative to `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/`. Only these six released skills and two references were used; no held peer directory was read. The first broad read truncated a small middle portion of correctness-oracles, which was then reread completely before harness construction.

| File | SHA256 | Applied decision |
|---|---|---|
| `bugfinding-campaign/SKILL.md` | `3E49E2C6D64BCA818B112B0B09549AA1830F8AEE2F9B5935B2CB50FDF3F1F6CA` | Bounded search, preserve counters and stop for replay/triage |
| `stateful-property-testing/SKILL.md` | `7A00C709FC2B1F23B09E210651A771944D25CF5F7AAE45C5331217E325A3BB29` | API-produced dependent histories and setup-preserving reduction |
| `correctness-oracles/SKILL.md` | `061D705455904EF16B8ECCB344950E2129092A485909F80CCD0406AA3E33EFEE` | Rejected-call state effects independently of allowed exception |
| `failure-reduction/SKILL.md` | `DB9473747EE9CE56B45E90AD15F3CBD1A85A81A1C587F45050BE5689B6AFA39D` | Original/reduced separation, same selected violation |
| `harness-sensitivity/SKILL.md` | `E8B538AF4C1BB70DD1BD5ED38A2E8EB3AFCD41980E315206EB5BD2175AFF1A5F` | Healthy, allowed-error and setup controls alongside actual rejection |
| `evidence-based-triage/SKILL.md` | `270E201E0DE93FB9ED091DB98A66F4FD3F430A6C0E19FCE3AF635BAC8C576730` | Distinguish exception from violation and connect shared cause |
| `failure-reduction/references/interestingness-and-replay.md` | `D9F34D60F37BFFD66C12FAF6DA3F1528FD29E71483E60C1D14F6126377AFB248` | Require same operation/error/effect after reduction |
| `stateful-property-testing/references/runtime-recipes.md` | `5728A0FD09E3230E7A8AA7CDCBDAA7950E6343F8C9A686630D38AC7479A37889` | Conditional runtime route; no dependency installation |

Target SHA256: `3928f93192d780eced95d68174bb354519f9b5d53fe979d0dfcfbaca8be38309`.
Contract SHA256: `DCEAA11C76CDFA2C47F4CA6AF34DCDDB3FFB692B4FBCB0EFAF849FAB6B85690B`.
Runtime recorded in all logs: Python 3.13.6, MSC v.1944 32 bit, Windows 11 build 26200.

## Remaining limits

Only a small domain and fixed sequential history shape were explored. Sizes/capacities 4..64, arbitrary names and invalid argument types, arbitrary longer recovery histories, and exhaustive return-value/model agreement remain untested. Successful-move conservation was exercised by a control but is not independently checked in the search oracle. The contract excludes concurrency, so concurrency methods were not applicable. No exhaustive correctness, discovery-rate improvement, or statistical superiority follows from this evaluation. Evidence supports the identified quota-accounting rollback defect in this isolated artifact only.
