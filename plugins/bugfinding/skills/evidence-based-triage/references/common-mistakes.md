# Common mistakes

| Misleading shortcut | Correction |
|---|---|
| “The LLM marked it true, so it is confirmed.” | Preserve the classifier's input, revision and conclusion; establish the violation from real contract and execution evidence. The inspected analyzer parses a model tag into `true_bug` ([source](https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/crash_analyzer.py)). |
| “It is an early/null/OOM failure, so discard it.” | Check actual producer preconditions and resource guarantees. Generated-harness heuristics do not settle arbitrary product cases ([heuristic source](https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/semantic_analyzer.py)). |
| “The seed did not replay, therefore nothing happened.” | Keep the actual input and trace; investigate missing state, prior sequence and persistent threads ([libFuzzer limitations](https://llvm.org/docs/LibFuzzer.html)). |
| “Fifty files mean fifty bugs,” or “one stack means one bug.” | Keep individual evidence and provisional groups; establish shared causes before collapsing counts ([ClusterFuzz glossary](https://google.github.io/clusterfuzz/reference/glossary/)). |
| “Any timeout proves deadlock.” | Determine whether the configured deadline contradicts the target's actual progress guarantee; the test or intended behavior can cause a fuzz failure ([Go failure cases](https://go.dev/doc/security/fuzz/)). |
| “The checker label establishes every stronger guarantee.” | Preserve model, assumptions and witness. Elle's stated observation/model limits qualify its conclusions ([Elle, §§4.3 and 9](https://arxiv.org/abs/2003.10554)). |

Keep original evidence when a reducer discovers a different smaller failure; minimization aims to retain the underlying bug, not merely any failing exit ([ClusterFuzz minimization](https://google.github.io/clusterfuzz/reference/glossary/)). Route reduction mechanics to `failure-reduction`.
