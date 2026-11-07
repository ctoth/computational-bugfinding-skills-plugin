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

For a history finding, attach the machine history and witness before explaining the contradiction in prose. Elle uses the graph edges of a cycle "to construct a human-readable explanation for the cycle", within its observation model ([Elle, §6](https://arxiv.org/abs/2003.10554)). If a missing outcome determines the inference, state the uncertainty. If only one representative of a symptom group was investigated, say so rather than imply every member was reproduced or shares that cause ([ClusterFuzz glossary](https://google.github.io/clusterfuzz/reference/glossary/)).
