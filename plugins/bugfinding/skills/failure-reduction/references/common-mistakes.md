# Common mistakes

Each entry is WRONG first, then RIGHT, then why.

## Accepting any exception as the failure

**Wrong:** The interestingness test returns "interesting" for any exception or nonzero target exit.

**Right:** Require the selected violation; classify unrelated exceptions and setup failures separately.

**Why:** the Debugging Book's `generic_test` counts every exception as `FAIL` unless an expected exception is given, and then an outcome "different from the original failure" is `UNRESOLVED` ([Delta Debugging, generic_test](https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb)).

## Dropping validity from a wrong-code predicate

**Wrong:** Accept a smaller wrong-code input because the two compilers still disagree.

**Right:** Keep the experiment's validity conditions inside its failure predicate.

**Why:** a variant that reads uninitialized storage "is not a valid test case" even when it shows the divergence ([Regehr et al., §5.1](https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)).

## Invoking every reducer test with a candidate path

**Wrong:** Write one test script that reads the candidate from `$1` and use it with every reducer.

**Right:** Honor each real interface: C-Reduce's test "should not expect any command line arguments" and runs in a fresh temporary directory; llvm-reduce's example script reads the candidate as `$1`.

**Why:** a C-Reduce test that needs an argument fails its sanity check on the original ([C-Reduce contract](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in), [llvm-reduce example](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/CommandGuide/llvm-reduce.md)).

## Using coverage-corpus reduction as crash reduction

**Wrong:** Run `-merge=1` or rely on `-reduce_inputs` to shrink a crashing input.

**Right:** Use `-minimize_crash=1`, which "minimizes the provided crash input", and replay the result against the selected predicate.

**Why:** merge preserves "the full coverage" of a corpus and `-reduce_inputs` preserves "full feature sets"; neither targets the crash ([libFuzzer corpus and options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

## Treating an explicit Hypothesis example as a shrink request

**Wrong:** Paste the failing value into `@example` and expect Hypothesis to shrink it.

**Right:** Preserve the generated readable arguments and let the existing generator shrink.

**Why:** "examples provided using |@example| do not shrink" ([replay guide](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/replaying-failures.rst)).

## Calling one unstable smaller observation a completed reduction

**Wrong:** Report the reduced case after it failed once.

**Right:** Investigate visible outcome changes and retained external state; save actual replay results.

**Why:** with external state Hypothesis can be "unable to shrink to a minimal failing input" ([Hypothesis flakiness](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/flaky.rst)).

## Claiming the globally smallest case from a deletion fixed point

**Wrong:** "The reducer stopped, so this is the smallest failing input."

**Right:** State the predicate, moves, completion and budget limits; claim 1-minimality only when single-element deletion was exhausted.

**Why:** 1-minimal means "every character contained is required to produce the error", not global minimality ([Delta Debugging, minimality](https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb)).

For dependent artifacts, a smaller setup error, impossible schedule or shifted fault event does not satisfy the chosen predicate. Apply the explicit correspondence rules in [worked reductions](worked-reductions.md) rather than silently weakening the oracle. These are this pack's adaptations, not claims of a general automatic reducer.
