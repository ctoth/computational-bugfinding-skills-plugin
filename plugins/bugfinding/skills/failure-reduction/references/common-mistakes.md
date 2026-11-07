# Common mistakes

| Misleading shortcut | Correction and evidence |
|---|---|
| Accept any exception or nonzero target exit | Require the selected violation; classify unrelated exceptions/setup failures separately ([Delta Debugging, generic_test](https://www.debuggingbook.org/html/DeltaDebugger.html)). |
| Smaller wrong-code input introduces undefined behavior | Keep the experiment's validity conditions alongside its failure predicate ([Regehr et al., §5](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)). |
| Invoke every reducer test with a candidate path | Honor its real interface: C-Reduce expects no arguments and a temporary working directory; llvm-reduce's example passes a path ([C-Reduce contract](https://raw.githubusercontent.com/csmith-project/creduce/master/creduce/creduce.in), [LLVM example](https://llvm.org/docs/CommandGuide/llvm-reduce.html)). |
| Use coverage-corpus reduction as crash reduction | Select the actual predicate: merge, feature preservation and crash minimization are distinct libFuzzer modes ([options](https://llvm.org/docs/LibFuzzer.html#options)). |
| Treat an explicit Hypothesis example as a shrink request | Explicit examples replay without shrinking; preserve generated readable arguments and use the existing shrinker ([replay guide](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)). |
| Call one unstable smaller observation a completed reduction | Investigate visible outcome changes and retained external state; save actual replay results ([Hypothesis flakiness](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html)). |
| Claim globally smallest from a deletion fixed point | State the predicate, moves, completion and budget limits; 1-minimal is a narrower claim ([Delta Debugging, minimality](https://www.debuggingbook.org/html/DeltaDebugger.html)). |

For dependent artifacts, a smaller setup error, impossible schedule or shifted fault event does not satisfy the chosen predicate. Apply the explicit correspondence rules in [worked reductions](worked-reductions.md) rather than silently weakening the oracle. These are this pack's adaptations, not claims of a general automatic reducer.
