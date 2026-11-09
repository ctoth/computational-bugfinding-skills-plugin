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

## Reading a "flaky" JavaScript test as passing

**Wrong:** "Playwright passed it on retry, so there is nothing to triage."

**Better:** Keep the first failure as a candidate and measure replay with `--repeat-each` and retries off. A fail-then-pass test is labelled "flaky", and a retry runs after Playwright will "discard the entire worker process along with the browser" ([Playwright retries](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-retries-js.md)); flaky tests fail the run only with `--fail-on-flaky-tests` ([Playwright CLI](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-cli-js.md)).

**Why:** the passing retry ran in a fresh worker, so it says nothing about the failing run's state.

## Expecting the failing run's trace from `on-first-retry`

**Wrong:** Configure `trace: 'on-first-retry'` and look for the failure in the trace.

**Better:** Use `'retain-on-failure'` or `'retain-on-failure-and-retries'`; for "Fails, then passes on retry", `'on-first-retry'` keeps only "first retry" ([Playwright trace table](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-use-options-js.md)).

**Why:** the kept trace is the passing retry, not the failure.

## Handing off Node reports or traces unreviewed

**Wrong:** Attach the default diagnostic report or `trace.zip` to a public issue as is.

**Better:** Exclude or redact environment variables (`--report-exclude-env`) ([Node diagnostic report](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/report.md)) and review trace sources and network records ([Playwright test options, trace](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-api/class-testoptions.md)).

**Why:** by default "the environment variables are included" in a report, and trace `sources` "Defaults to true".

## Expecting a profile from a killed Node process

**Wrong:** Kill a hung process and look for its `--cpu-prof` output.

**Better:** Let the process exit, or on Node v26.11+ use `--process-timeout`, after which profiles "are still written" ([Node CLI](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/cli.md)).

**Why:** `--cpu-prof` and `--heap-prof` write their profile "before exit"; a process killed by a signal that cannot be handled does not reach that point (inference).
