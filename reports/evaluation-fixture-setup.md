# Isolated behavior-evaluation fixtures

## State

Fixture setup and calibration complete. This report and the new isolated evaluation workspace are the only owned outputs. No skills, shared note, index, real target projects, dependencies or host configuration were changed.

## Evidence

The intended workspace `C:/Users/Q/code/bugfinding-skill-evaluation` did not exist when checked before authoring. It now contains two independent public scenarios, plus private calibration material outside both public directories. The workspace is not a Git repository and is not inside the plugin repository. All authored files were created with apply_patch.

## Public scenario artifacts

Give an independent evaluator only the relevant public directory, the completed skill set and its evaluation request. Both scenarios are standard-library-only Python, have a published API/domain/error contract and a runnable healthy demonstration, and require no service or installation. No public file includes a diagnosis, failing example, defect key or intended search technique.

| Scenario | Contract | Sole implementation |
| --- | --- | --- |
| A | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-a/contract.md` | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-a/target.py` |
| B | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-b/contract.md` | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-b/target.py` |

SHA256 identities of the public artifacts after calibration:

| Artifact | SHA256 |
| --- | --- |
| scenario-a/contract.md | DCEAA11C76CDFA2C47F4CA6AF34DCDDB3FFB692B4FBCB0EFAF849FAB6B85690B |
| scenario-a/target.py | 3928F93192D780ECED95D68174BB354519F9B5D53FE979D0DFCFBACA8BE38309 |
| scenario-b/contract.md | 2356CF30363D5B805F927BC3C657B63F55BB890BF10084BD111E9DD022B29B68 |
| scenario-b/target.py | A67FBB3EF27771F2C6D1E084A4E57AA65D3481CC8A73D309AC13AC8EF5FD141E |

## Calibration evidence

Executed only the explicit private setup test file:

```text
python C:/Users/Q/code/bugfinding-skill-evaluation/fixture_selftest.py
..........
----------------------------------------------------------------------
Ran 10 tests in 0.012s

OK
```

The command exited 0; tool-observed wall time was 0.6809232 seconds. Tests establish healthy and documented error behavior, independent state observations, reachable seeded violating behavior, and the public healthy demonstrations. Targets were loaded or demonstrated in-process by this single test file. Generated Python bytecode remains within the owned isolated workspace. No broad local suite or real project target ran. This is calibration evidence, not evidence that any skill discovers a defect, reduces a case or improves bug yield.

## Ownership and evaluation limits

Private ground truth and the setup test remain outside both public directories. The parent receives their locations separately; evaluators must not read them. Each later scenario evaluation has a finite envelope of at most 30 seconds CPU and modest RAM; no cloud spending, network/service interaction, dependency installation or real repository mutation is needed. Source inspection is permitted as ordinary engineering, but conclusions must be backed by the evaluator's own computational counterexample and raw replay evidence.

These are intentionally small injected-defect targets authored for isolated behavior testing. They do not model Barn's implementation, establish native-tool/platform compatibility, measure production discovery yield, or provide a controlled comparison against an unassisted agent. No skill/source improvement is implied merely by this calibration passing. No Git staging, commit, host registration or publication occurred.

## Next step

Parent dispatches independent evaluators with minimal public artifacts and the skill set, withholding the private calibration material and intended diagnoses. Parent compares their saved artifacts with calibration ground truth afterward.
