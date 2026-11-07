# Scenario B behavior evaluation

## Goal
Investigate only the public scenario B contract and implementation within the released nineteen-skill subset and a 30-second process CPU envelope.

## State
Complete: two reproducible contract-violation symptoms in the isolated target, with original witnesses, corrected reductions, independent replay and healthy/allowed-error controls. Owned artifacts: `bugfinding-skill-evaluation/evaluation-b/` and this report. No target edits, installation, network, Git operations or publication. A separate `C:/Users/Q/code/agent-notes/blind-behavior-b.md` was created solely to satisfy a higher-priority developer checkpoint; no shared parent task note was edited.

## Decisions and evidence
Public prompt, common restrictions, source, contract, and five selected released skills read. Bounded computation, corrected reductions, fresh replay, controls, raw evidence preservation, and identity recording are complete as documented below.

## Selected method
Read `bugfinding-campaign`, `correctness-oracles`, `failure-reduction`, `metamorphic-testing`, and `harness-sensitivity` released SKILL.md files. The campaign routes numerical work to `numerical-oracles`, but that directory is held and was not read. Therefore this evaluation uses an exact contract identity on a restricted legal family: for any nonempty list whose elements have equal absolute magnitude, the specified RMS is exactly that magnitude. No approximate square-root reference is needed. This does not assess general mixed-magnitude numerical accuracy.

The executable will generate binary64 powers of two through `math.ldexp`, vary legal list lengths and signs, compare the real API result to the exact magnitude using the contract's own tolerances, and preserve the first witness of each observed violation. It will reduce cardinality and exponent while preserving the same observed symptom and legal domain. Healthy/allowed-error and synthetic wrong-output controls will exercise the assertion.

## Computation and artifacts

- Executable: `C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-b/search_rms.py`.
- Raw command lines, stdout/stderr, exit statuses and runner wall times: `C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-b/raw-output.md`.
- Python 3.13.6 on Windows 11. All executions use `python -B` and only that explicit test file.
- The search enumerated 33,568 legal homogeneous-magnitude cases: all 2,098 exponents from -1074 through 1023, eight lengths, positive/alternating-sign patterns. Duplicate singleton sign patterns remain counted as executions. It found 8,544 zero-result accuracy violations and 8,202 nonfinite-result violations; these are cases, not independent bugs. No exceptions occurred for generated legal inputs.
- Two full searches were run: the second followed addition of replay length support, with unchanged search logic and identical case counts. No broad search followed the reducer correction.
- Nine Python invocations used 1.718750 seconds in summed printed process-CPU measurements, measured after standard-library imports; combined runner wall time was 6.8956136 seconds. This includes discovery, initial reduction, replay, controls and corrected reduction, comfortably inside the 30-second process-CPU envelope. No child processes or dependencies were used. Arrays have at most eight elements and the generator streams cases; memory was not measured.
- 68,363 valid target calls across runs; 63 allowed-error controls are excluded from that counter. Synthetic checker controls do not call the target. Every invocation ran six healthy cases, seven specific allowed-error cases, and four synthetic wrong-output checks.

## Finding: squaring small accepted values loses the specified RMS

Raw first triggering input: eight floats each `0x0.0000000000008p-1022` (exactly `2**-1071`). Expected RMS is that same subnormal number; actual returned float is positive zero. Its absolute error is eight times the smallest binary64 positive value, exceeding the permitted four times smallest value. All inputs satisfy the domain, and accepted inputs were observed unchanged.

Corrected reduced witness: one float `0x0.8000000000000p-1022` (exactly `2**-1023`), still a subnormal specified result. Actual is `0x0.0p+0`. Absolute error is `2**-1023`, while the permitted bound is `2**-1072`, a factor of `2**49` smaller. The exact replay command is:

`python -B C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-b/search_rms.py --replay=-1023`

It exits 1 at the RMS property assertion after printing the actual and expected hex values. `target.py:16` multiplies each accepted value by itself in binary64 before summation; the square of `2**-1023` rounds to zero, and `target.py:17` then returns zero. The specified complete-expression result remains representable.

The first reducer retained the zero symptom but moved the original subnormal result into the normal tolerance regime. Its `2**-538` singleton, also returning zero, is retained in raw evidence as a **supplemental normal-regime witness**, not a valid same-regime reduction. That witness has relative error 1 versus permitted `4e-15`. The governing reducer predicate was corrected to reject normal/subnormal regime changes before running retained-original reduction only. The corrected reduction made 62 attempts overall across both findings. It removes seven values, then moves the exponent toward zero until the next move would change tolerance regime. No absolute minimality is claimed.

Healthy controls include the smallest positive subnormal, for which zero is within the allowed absolute error, and singleton `2**-537`, which returned the exact expected value and exited 0 on explicit replay. This prevents treating every zero at tiny magnitudes as a defect.

## Finding: accumulation overflows before averaging

Raw first triggering input: eight floats each `0x1.0000000000000p+511` (exactly `2**511`). Actual returned float: `inf`; specified RMS: finite `2**511`. Reduced witness: four copies of the same float. The exact replay command is:

`python -B C:/Users/Q/code/bugfinding-skill-evaluation/evaluation-b/search_rms.py --replay=511 --length=4`

It exits 1 at the intended property assertion. Each individual square is `2**1022`, but four such squares sum to `2**1024`, overflowing the binary64 accumulation at `target.py:16`. The subsequent division at `target.py:17` cannot recover the finite specified complete-expression result. This violates the explicit finite-result guarantee regardless of tolerance.

Deleting a fifth-to-fourth value preserves the symptom; deleting one more gives a healthy three-element witness. The explicit `--replay=511 --length=3` control returned exactly `2**511` and exited 0. Lowering the retained exponent one step also loses the overflow symptom. This is a fixed point for the implemented deletion/one-step-toward-zero reductions, not a globally smallest overflow input. Both original and reduced observations survive fresh processes in raw evidence.

## Skill usage and exact SHA256 identities

Only the following released skill files were read or used; no reference files were opened. Paths below are relative to `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/`.

| Skill file | SHA256 | Concrete use |
|---|---|---|
| `bugfinding-campaign/SKILL.md` | `3E49E2C6D64BCA818B112B0B09549AA1830F8AEE2F9B5935B2CB50FDF3F1F6CA` | Finite streaming search, CPU and case accounting, stop after evidence rather than expand compute |
| `correctness-oracles/SKILL.md` | `061D705455904EF16B8ECCB344950E2129092A485909F80CCD0406AA3E33EFEE` | Exact RMS identity, contract tolerances, expected-error controls, mutation check |
| `failure-reduction/SKILL.md` | `DB9473747EE9CE56B45E90AD15F3CBD1A85A81A1C587F45050BE5689B6AFA39D` | Preserve originals, reduce input count/exponent, detect and correct tolerance-regime switch, replay |
| `metamorphic-testing/SKILL.md` | `4AA5B7F5DAC935FD020CCBBCDFB25358703B5DF250A874892EAE372CBFCD7EBB` | Derive equal-magnitude, replication and sign-invariance family from the specified exact expression |
| `harness-sensitivity/SKILL.md` | `E8B538AF4C1BB70DD1BD5ED38A2E8EB3AFCD41980E315206EB5BD2175AFF1A5F` | Healthy and permitted-error distinction; independently synthetic zero, infinity, inaccurate and negative-zero outputs rejected by the classifier |

Target `scenario-b/target.py` SHA256: `a67fbb3ef27771f2c6d1e084a4e57aa65d3481cc8a73d309ac13ac8ef5fd141e`.

Contract `scenario-b/contract.md` SHA256: `2356CF30363D5B805F927BC3C657B63F55BB890BF10084BD111E9DD022B29B68`.

Final test SHA256: `a72ece2fa57c016dcf014f8c629bfda03af7f9998b59e022cfc6343b86c8e3d6`. Prior test identities and their raw runs remain recorded in the raw artifact; the target stayed unchanged.

## Limits and next step

Stop: bounded search produced useful confirmed violations and replay evidence. This is seeded isolated target evidence from one artifact evaluation, not a new production-bug claim, empirical yield comparison, statistical superiority, or exhaustive correctness claim. The nineteen released methods define the available subset; only the five listed were applied. **`numerical-oracles` and the other five held directories were excluded and were not read. This is not coverage of all twenty-five methods.**

Untested: general mixed magnitudes/mantissas, arbitrary bit patterns, broad tuple coverage, container subclasses, every invalid combination, external side effects beyond this source's visible behavior, and broad statelessness permutations. Existing controls exercise lists and a tuple; fresh-process witness replay provides narrow independence from earlier calls. No claim of general numerical accuracy follows from the healthy controls. The checker does not use a general high-precision reference or approximate mathematical library. Parent can compare saved public evidence to its separate calibration; no target repair was authorized or attempted.
