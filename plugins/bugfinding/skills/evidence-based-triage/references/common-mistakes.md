# Common mistakes

## Treating an LLM verdict as confirmation

**Wrong:** “The LLM marked it true, so it is confirmed.”

**Better:** Preserve the classifier's input, revision and conclusion; establish the violation from real contract and execution evidence. The inspected analyzer sets `crash_result.true_bug = True` from the model's `conclusion` tag ([crash analyzer source, `_container_handle_conclusion`](https://raw.githubusercontent.com/google/oss-fuzz-gen/c0982c5d40a7e93ce70fd319705804b9a29954d0/agent/crash_analyzer.py)).

**Why:** a parsed model tag records what the model said, not a second observation of the target.

## Dismissing early, null or resource failures by category

**Wrong:** “It is an early/null/OOM failure, so discard it.”

**Better:** Check actual producer preconditions and resource guarantees. The OSS-Fuzz-Gen heuristic labels a crash within `EARLY_FUZZING_ROUND_THRESHOLD = 3` rounds as "very likely the false positive cases" for generated targets, and its ordinary crash route skips `slow-unit-`, `timeout-`, `leak-` and `oom-` artifacts ([semantic analyzer source, `CRASH_EXCLUSIONS` and `_parse_libfuzzer_logs`](https://raw.githubusercontent.com/google/oss-fuzz-gen/c0982c5d40a7e93ce70fd319705804b9a29954d0/agent/semantic_analyzer.py)).

**Why:** those heuristics judge generated harnesses; a real product can still crash early or exhaust memory on a legal input.

## Dropping a case that did not replay

**Wrong:** “The seed did not replay, therefore nothing happened.”

**Better:** Keep the actual input and trace; investigate missing state, prior sequence and persistent threads. libFuzzer warns that an undetected corruption can lead "to a crash while testing another input" ([libFuzzer limitations](https://llvm.org/docs/LibFuzzer.html#q-when-libfuzzer-is-not-a-good-solution-for-a-problem)).

**Why:** the last saved input may not be the whole cause of an in-process failure.

## Counting files or stacks as bugs

**Wrong:** “Fifty files mean fifty bugs,” or “one stack means one bug.”

**Better:** Keep individual evidence and provisional groups; establish shared causes before collapsing counts. ClusterFuzz's crash state is a signature generated "from the crash stacktrace for deduplication purposes" ([ClusterFuzz glossary, Crash state](https://google.github.io/clusterfuzz/reference/glossary/)).

**Why:** files over-count shared causes, and a stack signature can under-count distinct ones.

## Reading every timeout as a deadlock

**Wrong:** “Any timeout proves deadlock.”

**Better:** Determine whether the configured deadline contradicts the target's actual progress guarantee. Go's documentation says its per-execution fuzz timeout currently "is 1 second" and can fire "from intended behavior in the code" ([Go fuzzing, Failing input](https://go.dev/doc/security/fuzz/#failing-input)).

**Why:** a timeout shows only that a configured limit was exceeded.

## Stretching a checker label

**Wrong:** “The checker label establishes every stronger guarantee.”

**Better:** Preserve model, assumptions and witness. Elle notes "observations are rarely complete" and "Our approach ignores predicates" ([Elle, §§4.3 and 9](https://arxiv.org/abs/2003.10554)).

**Why:** a checker's verdict covers only its observation model.

## Accepting a reducer's different failure as the original

**Wrong:** Replace the original with whatever smaller input still fails.

**Better:** Keep original evidence when a reducer discovers a different smaller failure. ClusterFuzz minimization is meant to keep "the same underlying bug" ([ClusterFuzz glossary, Minimization](https://google.github.io/clusterfuzz/reference/glossary/)), while Go's minimizer only keeps a value "which will still produce an error" ([Go fuzzing, Failing input](https://go.dev/doc/security/fuzz/#failing-input)). Route reduction mechanics to `failure-reduction`.

**Why:** a reducer that accepts any error can hand back a different bug.
