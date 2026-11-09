# Maintainer handoff

Use the project's report format. Keep the trigger, actual observation, replay instructions and target identity together; LLVM's maintainer guidance asks for "All information necessary to reproduce the problem" and "The reduced test case that triggers the bug" ([LLVM reporting, Introduction](https://llvm.org/docs/HowToSubmitABug.html#introduction-got-bugs)). Check the project's own policy on LLM help: LLVM says "You must not post any description you don't understand", requires that "any AI assistance must be noted", and asks fuzzer-generated testcases to describe their framework ([LLVM reporting, AI policy](https://llvm.org/docs/HowToSubmitABug.html#ai-policy)). Drafting a handoff does not authorize publication.

An illustrative compact handoff, with facts filled only from retained evidence:

```text
Trigger: [public operation, legal input/state and relevant conditions]
Guarantee: [primary contract location and applicable configuration]
Expected / actual: [observable contradiction, including effects if relevant]
Evidence: [original input, raw output and witness paths]
Replay: [build/runtime/options; exact invocation; actual attempts/outcomes]
Reduced case: [path and verified relationship to original, or not available]
Disposition: [supported conclusion; unresolved details]
Cause: [established mechanism, hypothesis, or unknown]
Impact: [observed user effect; no unsupported severity/exploit claim]
Next action: [specific missing evidence or useful investigation]
```

This is a convenient record, not a required schema. Reproduction reliability, source revision and execution conditions are meaningful evidence; a reproducible contract violation and a fully explained cause are distinct facts. ClusterFuzz filters on "Reliability of reproducing the crash", gives a regression range "only available for reliably reproducible crashes", and calls culprit-finding from stacks "more of an art than an exact science" ([ClusterFuzz triage, Filtering testcases, Regression revision range and Crash stacktrace](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).

For JavaScript, attach the runtime's own artifacts. A Playwright trace is written to `trace.zip` under `test-results` and opens with `npx playwright show-trace path/to/trace.zip` ([Playwright trace viewer](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/trace-viewer.md)); for command-line inspection use Playwright's own `playwright-trace` skill ([playwright-trace skill](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/packages/playwright-core/src/tools/skills/playwright-trace/SKILL.md)). Node writes `--cpu-prof` and `--heap-prof` profiles "before exit", so a killed process may leave none; `--report-uncaught-exception` and `--report-on-fatalerror` write a diagnostic report, and the first does not fire if the exception "is handled" ([Node CLI](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/cli.md)). Review both before sharing: a report includes environment variables unless `--report-exclude-env` is set ([Node diagnostic report](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/report.md)), and a trace includes source files by default and, with DOM snapshots, network activity ([Playwright test options, trace](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-api/class-testoptions.md)).

For a history finding, attach the machine history and witness before explaining the contradiction in prose. Elle uses the graph edges of a cycle "to construct a human-readable explanation for the cycle", within its observation model ([Elle, §6](https://arxiv.org/abs/2003.10554)). If a missing outcome determines the inference, state the uncertainty. If only one representative of a symptom group was investigated, say so rather than imply every member was reproduced or shares that cause ([ClusterFuzz glossary](https://google.github.io/clusterfuzz/reference/glossary/)).
