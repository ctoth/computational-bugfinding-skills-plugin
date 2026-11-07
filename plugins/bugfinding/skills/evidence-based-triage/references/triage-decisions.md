# Triage decisions

Use these examples to decide what evidence is missing. They are illustrative, not executed product findings. Preserve the actual target's contract rather than inherit a classifier's assumptions.

| Observed candidate | Useful next distinction | Supported conclusion |
|---|---|---|
| Generated native driver crashes immediately | Trace the real call and object lifetime against the API precondition | A proven invalid driver call supports a harness finding; early timing alone does not. |
| Paired engines return different values | Establish matched configuration and the feature's shared contract | A documented semantic difference can invalidate this comparison; a bare disagreement selects no winner. |
| History checker reports an anomaly | Inspect actual operations, outcomes, model and contradiction witness | Preserve only the anomaly the evidence supports; unresolved outcomes may limit the inference. |
| Saved file fails only after hours in a worker | Compare build/options, initialization, preceding inputs and concurrent events | A fresh-process miss leaves missing-state and accumulated-product-failure explanations open. |
| Many inputs share top stack frames | Retain per-input evidence, then compare demonstrated mechanisms | Use a provisional bucket until a common cause is established. |

These distinctions follow the actual failure/replay and witness boundaries in [Go fuzzing](https://go.dev/doc/security/fuzz/), [libFuzzer](https://llvm.org/docs/LibFuzzer.html), [ClusterFuzz's grouping terminology](https://google.github.io/clusterfuzz/reference/glossary/) and [Elle, §§4.3 and 6](https://arxiv.org/abs/2003.10554). Differential validity belongs to `semantic-differential-testing`; history algorithms belong to `transactional-history-testing` or `linearizability-checking`.

## Inspect classifier provenance

The inspected OSS-Fuzz-Gen semantic analyzer has special handling for early crashes, null dereferences and resource symptoms; its ordinary crash-artifact route excludes several resource artifact names. These are generated-harness evaluation heuristics, not universal reasons to dismiss real target defects ([semantic analyzer source](https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/semantic_analyzer.py)). Record the classifier revision, input and conclusion separately from the contract/replay evidence.

## Replay with the right representation

Go corpus arguments carry types and order. Use the failure's emitted focused selector, such as `go test -run=FuzzFoo/CASE_ID`, in the target's permitted runner; do not feed a structured choice-byte record to a string-source decoder and call its rejection a product failure ([Go corpus and replay](https://go.dev/doc/security/fuzz/)).

For an existing compatible OSS-Fuzz integration, `python3 infra/helper.py reproduce PROJECT FUZZ_TARGET TESTCASE` replays a retained testcase after the appropriate build. It is not a generic setup command for arbitrary projects. Preserve the original and reduced input, architecture, sanitizer and actual command/output ([OSS-Fuzz reproduction](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)).

An authentic trace whose missing sequence cannot be recovered remains unresolved evidence. Record what is unavailable and stop when the task's investigation budget is spent; do not invent a replay or silently erase the case ([ClusterFuzz reliability](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).
